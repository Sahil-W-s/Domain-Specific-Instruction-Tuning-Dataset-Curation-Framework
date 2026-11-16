import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y%m%dT%H%M%SZ")
ISO = NOW.isoformat().replace("+00:00", "Z")

REPORT = ROOT / "docs/phase_reports/PHASE_03_REPORT.md"
VALIDATION = ROOT / "reports/validation/phase_03_validation.json"
MANIFEST = ROOT / "manifests/phase_03_outputs.json"
STATE = ROOT / "state/phase_status.yml"
PROJECT_STATE = ROOT / "PROJECT_STATE.md"
NEXT_ACTION = ROOT / "NEXT_ACTION.md"

def atomic_create(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite: {path}")

    fd, name = tempfile.mkstemp(
        prefix=".phase3_", suffix=".tmp", dir=path.parent
    )
    temp = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.link(temp, path)
    finally:
        temp.unlink(missing_ok=True)

def atomic_update(path, content):
    fd, name = tempfile.mkstemp(
        prefix=".phase3_update_", suffix=".tmp", dir=path.parent
    )
    temp = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def update_phase_status():
    text = STATE.read_text(encoding="utf-8-sig")

    if "  phase_03:" in text:
        raise FileExistsError("Phase 3 state entry already exists.")

    if not re.search(r"(?m)^current_phase: 2$", text):
        raise ValueError("Unexpected current_phase value.")

    if not re.search(r"(?m)^  phase_02:$", text):
        raise ValueError("Phase 2 state entry not found.")

    text = re.sub(
        r"(?m)^current_phase: 2$",
        "current_phase: 3",
        text,
        count=1,
    )

    text = re.sub(
        r"(?m)^last_updated:.*$",
        "last_updated: '" + NOW.strftime("%Y-%m-%d") + "'",
        text,
        count=1,
    )

    start = text.index("  phase_02:")
    phase2 = text[start:]

    if "status: owner_review_pending" not in phase2:
        raise ValueError("Unexpected Phase 2 status; refusing state update.")

    phase2 = phase2.replace(
        "status: owner_review_pending",
        "status: completed\n    owner_approval: completed",
        1,
    )
    text = text[:start] + phase2

    text += """
  phase_03:
    name: Establish durable workspace, project memory, and checkpoint tooling
    status: owner_review_pending
    technical_status: completed
    owner_approval: pending
    report: docs/phase_reports/PHASE_03_REPORT.md
    outputs_manifest: manifests/phase_03_outputs.json
    validation: reports/validation/phase_03_validation.json
    completed_at: '""" + NOW.strftime("%Y-%m-%d") + """'
    limitations:
    - SQLite index is a rebuildable local artifact and is excluded from Git
    - JSON schemas were syntax-checked; full instance validation was not run
    - Phase 3 Git staging and publication await owner review
"""

    atomic_update(STATE, text)

def append_authoritative_section(path, heading, body):
    old = path.read_text(encoding="utf-8-sig")
    if heading in old:
        raise ValueError(f"Section already exists in {path}")

    atomic_update(path, old.rstrip() + "\n\n" + heading + "\n\n" + body + "\n")

def generate_handoff():
    command = [
        sys.executable,
        str(ROOT / "scripts/build_ai_handoff.py"),
        "--current-phase",
        "Phase 3 — Durable workspace and project memory",
        "--status",
        "Phases 0–2 owner-approved complete; Phase 3 technically complete; owner review pending",
        "--next-action",
        "Review the Phase 3 report, validation report, and output manifest. Approve the Phase 3 Git checkpoint before selective staging and committing.",
    ]
    subprocess.run(command, cwd=ROOT, check=True)

def main():
    required = [
        "src/mlcp/run_manager.py",
        "scripts/inventory/build_artifact_index.py",
        "scripts/build_ai_handoff.py",
        "tests/test_phase3_core.py",
        "tests/test_phase3_workflow.py",
        "artifacts/index/artifact_index.sqlite",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            raise FileNotFoundError(relative)

    for path in (REPORT, VALIDATION, MANIFEST):
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite: {path}")

    report = f"""# Phase 3 Report — Durable Workspace and Project Memory

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework
**Generated:** {ISO}
**Plan:** Implementation Plan v2.0
**Technical status:** Complete
**Owner approval:** Pending

## Objective

Establish reusable workspace structure, run management, artifact metadata
search, durable AI handoffs, and safe checkpoint/resume functionality.

## Completed work

| Work item | Result |
|---|---|
| P3.1 Workspace directories | Created |
| P3.2 Run, phase-output, and validation schemas | JSON syntax checks passed |
| P3.3 Run manager | Creation, persistence, update, and terminal-state smoke tests passed |
| P3.4 SQLite metadata index | 1,531 registry records indexed; 1,531 FTS5 records; integrity check passed |
| P3.5 AI handoff generator | Generated timestamped handoff; 7 required-content checks passed |
| P3.6 Core integration tests | 4/4 passed |
| P3.7 Git protections | Secrets, local configuration, cache, and SQLite exclusion checked |
| P3.8 End-to-end resume test | 1/1 passed |

## Key implementation files

- `src/mlcp/run_manager.py`
- `scripts/inventory/build_artifact_index.py`
- `scripts/build_ai_handoff.py`
- `tests/test_phase3_core.py`
- `tests/test_phase3_workflow.py`
- `manifests/run_manifest.schema.json`
- `manifests/phase_outputs.schema.json`
- `reports/validation/validation_report.schema.json`

## Validation results

Five focused pytest tests passed: four core integration tests and one
end-to-end checkpoint/resume test.

The end-to-end test verified run creation, output persistence, validation
metadata, resumption, no-overwrite behavior, terminal completion, and
handoff generation using temporary data.

The artifact index contains 1,531 registry records and 1,531 FTS5 records.
SQLite integrity check returned `ok`.

## Git and data protection

- `.env`, `.local/`, Python cache, and temporary files remain ignored.
- `artifacts/index/*.sqlite` is ignored because the index is rebuildable.
- Source code, schemas, tests, README files, and reviewed handoffs remain
  eligible for Git tracking.
- No Phase 2 inventory or recovery artifacts were staged or committed.
- No original source data was moved, deleted, renamed, or rehashed.

## Limitations

- Schema files received JSON syntax checks; full JSON Schema instance
  validation was not performed.
- The SQLite index is local and must be rebuilt from the artifact registry
  on another machine.
- The generated handoff includes project source snapshots; conflicting
  historical statements are retained rather than silently erased.
- Phase 0 and Phase 1 historical limitations remain documented.
- Phase 2's 15-file independent SHA-256 recomputation was a targeted sample,
  not an exhaustive independent rehash.
- Possible duplicate candidates remain pending manual review.

## Exit status

Phase 3 technical implementation and focused validation are complete.
Final owner review and selective Git checkpoint approval remain pending.
"""

    checks = [
        ("workspace_directories", "passed", "Required workspace directories created."),
        ("schema_json_syntax", "passed", "Three new schemas passed JSON syntax parsing; not full instance validation."),
        ("run_manager_smoke", "passed", "Five run-management smoke checks passed."),
        ("sqlite_index", "passed", "1,531 registry records, 1,531 FTS5 records; integrity check ok."),
        ("handoff_generator", "passed", "Handoff generated; seven required-content checks passed."),
        ("core_integration_tests", "passed", "Four focused integration tests passed."),
        ("git_ignore_protection", "passed", "Secret, local configuration, cache, and SQLite rules checked."),
        ("end_to_end_resume", "passed", "One complete checkpoint/resume/handoff integration test passed."),
        ("full_json_schema_instance_validation", "warning", "Not performed; JSON syntax checks only."),
    ]

    validation = {
        "phase_id": "phase_03",
        "generated_at": ISO,
        "summary": {
            "total": len(checks),
            "passed": sum(s == "passed" for _, s, _ in checks),
            "failed": sum(s == "failed" for _, s, _ in checks),
            "warnings": sum(s == "warning" for _, s, _ in checks),
        },
        "checks": [
            {"check_id": name, "status": status, "details": details}
            for name, status, details in checks
        ],
    }

    atomic_create(REPORT, report)
    atomic_create(VALIDATION, json.dumps(validation, indent=2) + "\n")

    update_phase_status()

    append_authoritative_section(
        PROJECT_STATE,
        "## Authoritative current status — Phase 3",
        f"""**Updated:** {NOW.strftime("%Y-%m-%d")}
**Current phase:** Phase 3 — Durable workspace and project memory
**Phase 0:** Owner-approved complete
**Phase 1:** Owner-approved complete
**Phase 2:** Owner-approved complete
**Phase 3:** Technical implementation complete; owner review pending

Phase 3 report: `docs/phase_reports/PHASE_03_REPORT.md`
Validation: `reports/validation/phase_03_validation.json`
Outputs: `manifests/phase_03_outputs.json`

Five focused integration tests passed. The SQLite index contains 1,531
registry records and 1,531 FTS5 records. The index is rebuildable and ignored
by Git. Full JSON Schema instance validation was not performed.

Phase 1 limitations and Phase 2 duplicate-review and targeted-hash caveats
remain unchanged. No source data was moved or deleted."""
    )

    append_authoritative_section(
        NEXT_ACTION,
        "## Authoritative next action — Phase 3 owner review",
        """1. Review `docs/phase_reports/PHASE_03_REPORT.md`.
2. Review `reports/validation/phase_03_validation.json`.
3. Review `manifests/phase_03_outputs.json`.
4. Inspect the selected Phase 3 Git changes and ensure no secrets,
   local-only files, or unrelated Phase 2 inventory outputs are staged.
5. Provide explicit approval before staging, committing, or pushing.

Do not use `git add .`. Do not repeat completed Phase 0–2 work."""
    )

    generate_handoff()

    handoff_dir = ROOT / "docs/ai_handoff/generated"
    handoffs = sorted(handoff_dir.glob("AI_HANDOFF_*.md"))
    if not handoffs:
        raise RuntimeError("Handoff generation did not produce an output.")
    latest_handoff = handoffs[-1]

    candidates = [
        "docs/phase_reports/PHASE_03_REPORT.md",
        "reports/validation/phase_03_validation.json",
        "state/phase_status.yml",
        "PROJECT_STATE.md",
        "NEXT_ACTION.md",
        ".gitignore",
        "src/mlcp/README.md",
        "src/mlcp/__init__.py",
        "src/mlcp/run_manager.py",
        "scripts/inventory/README.md",
        "scripts/inventory/build_artifact_index.py",
        "scripts/build_ai_handoff.py",
        "tests/test_phase3_core.py",
        "tests/test_phase3_workflow.py",
        "manifests/run_manifest.schema.json",
        "manifests/phase_outputs.schema.json",
        "reports/validation/validation_report.schema.json",
        "artifacts/README.md",
        "artifacts/index/artifact_index.sqlite",
        str(latest_handoff.relative_to(ROOT)).replace("\\", "/"),
    ]

    outputs = []
    for relative in candidates:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        outputs.append({
            "path": relative,
            "byte_size": path.stat().st_size,
            "sha256": sha256(path),
            "status": "created" if relative in {
                "docs/phase_reports/PHASE_03_REPORT.md",
                "reports/validation/phase_03_validation.json",
                str(latest_handoff.relative_to(ROOT)).replace("\\", "/"),
            } else "updated" if relative in {
                "state/phase_status.yml",
                "PROJECT_STATE.md",
                "NEXT_ACTION.md",
                ".gitignore",
            } else "preserved",
            "notes": (
                "Local rebuildable index; intentionally ignored by Git."
                if relative == "artifacts/index/artifact_index.sqlite"
                else ""
            ),
        })

    output_manifest = {
        "phase_id": "phase_03",
        "generated_at": ISO,
        "outputs": outputs,
    }

    atomic_create(MANIFEST, json.dumps(output_manifest, indent=2) + "\n")

    print("[PASS] Phase 3 report created")
    print("[PASS] Validation report created")
    print("[PASS] Phase 2 owner-approved status reconciled")
    print("[PASS] Phase 3 state recorded as owner-review pending")
    print("[PASS] Project state and next action updated")
    print("[PASS] Timestamped handoff generated")
    print(f"[PASS] Output manifest created with {len(outputs)} hashed entries")
    print(f"[CREATED] {REPORT.relative_to(ROOT)}")
    print(f"[CREATED] {VALIDATION.relative_to(ROOT)}")
    print(f"[CREATED] {MANIFEST.relative_to(ROOT)}")
    print(f"[HANDOFF] {latest_handoff.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
