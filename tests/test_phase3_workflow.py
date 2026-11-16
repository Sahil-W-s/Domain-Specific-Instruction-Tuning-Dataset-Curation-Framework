import argparse
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mlcp.run_manager import create_run, update_run, atomic_write_json


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_end_to_end_run_checkpoint_resume_and_handoff(tmp_path, monkeypatch):
    # 1. Create an isolated run.
    run_id, run_dir, manifest_path = create_run(
        tmp_path,
        "phase_03",
        "resume_workflow_test",
        operator="pytest",
        command="end-to-end integration test",
        working_directory=str(tmp_path),
        code_commit="test",
    )

    assert run_dir.is_dir()
    assert manifest_path.is_file()

    # 2. Produce a small output artifact atomically.
    output_path = run_dir / "result.json"
    payload = {"records_processed": 3, "result": "ok"}

    atomic_write_json(output_path, payload)
    original_bytes = output_path.read_bytes()

    relative_output = output_path.relative_to(tmp_path).as_posix()

    # 3. Validate the output and persist the checkpoint.
    saved_payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved_payload == payload

    update_run(manifest_path, {
        "output_artifacts": [{
            "path": relative_output,
            "size_bytes": output_path.stat().st_size,
        }],
        "validation": [{
            "check": "result_json_readable",
            "status": "passed",
        }],
        "notes": "Output saved; run is resumable.",
    })

    # 4. Simulate resumption from persisted disk state.
    resumed_manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )

    assert resumed_manifest["status"] == "started"
    assert resumed_manifest["run_id"] == run_id

    if output_path.exists():
        resumed_payload = json.loads(
            output_path.read_text(encoding="utf-8")
        )
        assert resumed_payload == payload
    else:
        atomic_write_json(output_path, payload)

    # Existing output must not be overwritten during resume.
    with pytest.raises(FileExistsError):
        atomic_write_json(output_path, {"records_processed": 999})

    assert output_path.read_bytes() == original_bytes

    # 5. Complete the resumed run.
    completed = update_run(manifest_path, {
        "status": "completed",
        "exit_code": 0,
    })

    assert completed["status"] == "completed"
    assert completed["finished_at"] is not None

    # 6. Generate a handoff using the persisted run manifest.
    handoff = load_module(
        "phase3_workflow_handoff",
        ROOT / "scripts" / "build_ai_handoff.py",
    )

    monkeypatch.setattr(handoff, "ROOT", tmp_path)
    monkeypatch.setattr(
        handoff, "RUNS_DIR",
        tmp_path / "manifests" / "runs"
    )

    output_dir = tmp_path / "docs" / "ai_handoff" / "generated"
    monkeypatch.setattr(handoff, "OUTPUT_DIR", output_dir)

    for relative_path in handoff.SOURCE_FILES:
        source = tmp_path / relative_path
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            f"# Test source: {relative_path}\n",
            encoding="utf-8",
        )

    monkeypatch.setattr(
        handoff,
        "git_info",
        lambda: {
            "branch": "test",
            "commit": "test",
            "status": "Temporary integration test",
        },
    )

    handoff.build(argparse.Namespace(
        current_phase="Phase 3",
        status="Integration test",
        next_action="Continue from the saved checkpoint.",
    ))

    generated = list(output_dir.glob("AI_HANDOFF_*.md"))
    assert len(generated) == 1

    handoff_text = generated[0].read_text(encoding="utf-8")

    assert run_id in handoff_text
    assert "completed" in handoff_text
    assert "result.json" in handoff_text
    assert "Continue from the saved checkpoint." in handoff_text

    # Verify the original output remains unchanged.
    assert output_path.read_bytes() == original_bytes
