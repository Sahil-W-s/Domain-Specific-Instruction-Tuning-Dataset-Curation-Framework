"""Run management and safe checkpoint utilities for ML CP."""

import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path


VALID_STATUSES = {
    "started", "completed", "failed", "partial", "blocked"
}

TERMINAL_STATUSES = {"completed", "failed", "partial", "blocked"}


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def make_run_id(phase_id, task_id):
    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    phase = re.sub(r"[^a-zA-Z0-9_-]", "_", phase_id)
    task = re.sub(r"[^a-zA-Z0-9_-]", "_", task_id)

    return f"{timestamp}_{phase}_{task}"


def atomic_write_json(path, data, overwrite=False):
    """Write JSON atomically; refuse replacement by default."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False
        ) as handle:
            temp_path = Path(handle.name)
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

        if overwrite:
            os.replace(temp_path, path)
        else:
            # Atomic creation without replacing an existing destination.
            os.link(temp_path, path)
            temp_path.unlink()

    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


def create_run(
    root,
    phase_id,
    task_id,
    operator="human",
    command="",
    working_directory=".",
    code_commit="uncommitted"
):
    """Create an isolated run directory and initial manifest."""

    root = Path(root).resolve()

    run_id = make_run_id(phase_id, task_id)

    run_directory = root / "runs" / run_id
    manifest_path = root / "manifests" / "runs" / f"{run_id}.json"

    run_directory.parent.mkdir(parents=True, exist_ok=True)
    run_directory.mkdir(exist_ok=False)

    manifest = {
        "run_id": run_id,
        "phase_id": phase_id,
        "task_id": task_id,
        "status": "started",
        "started_at": utc_now(),
        "finished_at": None,
        "operator": operator,
        "command": command,
        "working_directory": working_directory,
        "code_commit": code_commit,
        "config_hash": None,
        "input_artifacts": [],
        "output_artifacts": [],
        "environment": {},
        "exit_code": None,
        "validation": [],
        "log_paths": [],
        "notes": ""
    }

    try:
        atomic_write_json(manifest_path, manifest)
    except Exception:
        run_directory.rmdir()
        raise

    return run_id, run_directory, manifest_path


def update_run(manifest_path, updates):
    """Update an existing run manifest without replacing its identity."""

    manifest_path = Path(manifest_path)

    if not manifest_path.is_file():
        raise FileNotFoundError(manifest_path)

    protected = {"run_id", "started_at"}

    if protected.intersection(updates):
        raise ValueError("Run identity and start time cannot be changed.")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if "status" in updates:
        if updates["status"] not in VALID_STATUSES:
            raise ValueError("Invalid run status.")

        if manifest["status"] in TERMINAL_STATUSES:
            raise ValueError("Terminal run cannot be updated.")

    manifest.update(updates)

    if manifest["status"] in TERMINAL_STATUSES:
        manifest["finished_at"] = utc_now()

    atomic_write_json(manifest_path, manifest, overwrite=True)

    return manifest
