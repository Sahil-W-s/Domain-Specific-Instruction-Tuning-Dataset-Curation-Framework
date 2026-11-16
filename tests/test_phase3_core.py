import argparse
import importlib.util
import json
import sqlite3
import sys
from datetime import datetime, timezone
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


def test_run_creation_and_checkpoint_update(tmp_path):
    run_id, run_dir, manifest_path = create_run(
        tmp_path,
        "phase_03",
        "integration_test",
        operator="pytest",
        command="pytest",
        working_directory=str(tmp_path),
        code_commit="test",
    )

    assert run_dir.is_dir()
    assert manifest_path.is_file()

    update_run(manifest_path, {"status": "completed"})

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["run_id"] == run_id
    assert manifest["status"] == "completed"
    assert manifest["finished_at"] is not None


def test_atomic_json_refuses_to_overwrite(tmp_path):
    target = tmp_path / "checkpoint.json"

    atomic_write_json(target, {"version": 1})

    with pytest.raises(FileExistsError):
        atomic_write_json(target, {"version": 2})

    saved = json.loads(target.read_text(encoding="utf-8"))
    assert saved == {"version": 1}


def test_sqlite_index_and_fts5_search(tmp_path):
    module = load_module(
        "build_artifact_index_test",
        ROOT / "scripts" / "inventory" / "build_artifact_index.py",
    )

    registry = tmp_path / "registry.jsonl"
    output = tmp_path / "index" / "artifact_index.sqlite"

    record = {
        "artifact_id": "test-artifact-001",
        "source_root_id": "TEST_ROOT",
        "relative_path": "documents/manual.pdf",
        "file_name": "manual.pdf",
        "extension": ".pdf",
        "size_bytes": 1024,
        "last_write_time_utc": "2026-11-17T00:00:00Z",
        "artifact_type": "document",
        "lifecycle": "source",
        "phase": "phase_03",
        "sensitivity": "public",
        "redistribution_status": "unknown",
        "hash_algorithm": "sha256",
        "sha256": "a" * 64,
        "hash_status": "verified",
        "first_seen_run_id": "test-run",
        "last_verified_utc": "2026-11-17T00:00:00Z",
    }

    registry.write_text(
        json.dumps(record) + "\n",
        encoding="utf-8",
    )

    module.build(registry, output)

    assert output.is_file()

    with sqlite3.connect(output) as conn:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        artifact_count = conn.execute(
            "SELECT COUNT(*) FROM artifacts"
        ).fetchone()[0]
        search_count = conn.execute(
            "SELECT COUNT(*) FROM artifact_search"
        ).fetchone()[0]
        matches = conn.execute(
            "SELECT artifact_id FROM artifact_search "
            "WHERE artifact_search MATCH ?",
            ("manual",),
        ).fetchall()

    assert integrity == "ok"
    assert artifact_count == 1
    assert search_count == artifact_count
    assert matches == [("test-artifact-001",)]


def test_handoff_generation_preserves_existing_file(tmp_path, monkeypatch):
    module = load_module(
        "build_ai_handoff_test",
        ROOT / "scripts" / "build_ai_handoff.py",
    )

    monkeypatch.setattr(module, "ROOT", tmp_path)

    output_dir = tmp_path / "generated"
    runs_dir = tmp_path / "manifests" / "runs"

    monkeypatch.setattr(module, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(module, "RUNS_DIR", runs_dir)

    for relative_path in module.SOURCE_FILES:
        source = tmp_path / relative_path
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            f"# Test source: {relative_path}\n",
            encoding="utf-8",
        )

    runs_dir.mkdir(parents=True)
    (runs_dir / "test_run.json").write_text(
        json.dumps({
            "run_id": "test-run",
            "phase_id": "phase_03",
            "task_id": "handoff_test",
            "status": "completed",
            "started_at": "2026-11-17T00:00:00Z",
        }),
        encoding="utf-8",
    )

    class FrozenDateTime:
        @staticmethod
        def now(tz):
            return datetime(2026, 11, 17, 12, 0, 0, tzinfo=tz)

    monkeypatch.setattr(module, "datetime", FrozenDateTime)

    args = argparse.Namespace(
        current_phase="Phase 3",
        status="In progress",
        next_action="Continue focused validation.",
    )

    module.build(args)

    generated = output_dir / "AI_HANDOFF_20261117T120000Z.md"
    assert generated.is_file()

    original_content = generated.read_bytes()
    content = original_content.decode("utf-8")

    assert "Authoritative continuation instructions" in content
    assert "test-run" in content
    assert "Handoff safety rules" in content

    with pytest.raises(FileExistsError):
        module.build(args)

    assert generated.read_bytes() == original_content
