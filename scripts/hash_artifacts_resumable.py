import argparse
import csv
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "manifests/artifact_registry.jsonl"
ROOT_CONFIG = ROOT / ".local/source_roots.local.yml"
PROGRESS = ROOT / "state/hash_progress.json"
EVENTS = ROOT / "reports/inventory/hash_batches/hash_events.jsonl"
CHUNK_SIZE = 8 * 1024 * 1024

PRIORITY = {
    "notebook": 0,
    "script": 1,
    "dataset": 2,
    "model": 3,
    "adapter": 4,
    "evaluation_output": 5,
    "configuration": 6,
    "archive": 7,
    "documentation": 8,
    "log": 9,
    "other": 10,
    "unclassified": 11,
}

def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def atomic_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)

def save_registry(records):
    temp = REGISTRY.with_name(REGISTRY.name + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, REGISTRY)

def file_signature(path):
    st = path.stat()
    return st.st_size, st.st_mtime_ns

def hash_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()

def append_event(event):
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=10)
    args = parser.parse_args()

    if args.batch_size < 1 or args.batch_size > 50:
        raise SystemExit("Batch size must be between 1 and 50.")

    if not REGISTRY.is_file() or not ROOT_CONFIG.is_file():
        raise SystemExit("Registry or local root configuration is missing.")

    config = yaml.safe_load(ROOT_CONFIG.read_text(encoding="utf-8"))
    roots = {
        item["id"]: Path(item["path"]).resolve()
        for item in config["roots"]
    }

    records = [
        json.loads(line)
        for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    ids = [r["artifact_id"] for r in records]
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate artifact IDs detected; stopping.")

    pending = [r for r in records if r["hash_status"] == "pending"]
    pending.sort(key=lambda r: (
        PRIORITY.get(r["artifact_type"], 99),
        -r["size_bytes"],
        r["source_root_id"],
        r["relative_path"].casefold()
    ))

    batch = pending[:args.batch_size]
    if not batch:
        print("No pending files remain.")
        return

    run_id = "HASH_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    completed = 0
    failed = 0

    print("Run ID:", run_id)
    print("Batch size:", len(batch))
    print("Pending before batch:", len(pending))

    for item in batch:
        root_id = item["source_root_id"]
        root = roots.get(root_id)

        try:
            if root is None:
                raise RuntimeError("Source root ID is not configured.")

            path = (root / item["relative_path"]).resolve()
            if not path.is_relative_to(root):
                raise RuntimeError("Resolved path escapes configured source root.")
            if not path.is_file():
                raise FileNotFoundError("Source file does not exist.")

            before = file_signature(path)
            if before[0] != item["size_bytes"]:
                raise RuntimeError("File size differs from registry baseline.")

            baseline_time = item.get("last_write_time_utc")
            if baseline_time:
                expected = datetime.fromisoformat(baseline_time.replace("Z", "+00:00"))
                actual = datetime.fromtimestamp(
                    before[1] / 1_000_000_000, tz=expected.tzinfo
                )
                if abs((actual - expected).total_seconds()) >= 2:
                    raise RuntimeError("File timestamp differs from registry baseline.")

            digest = hash_file(path)
            after = file_signature(path)

            if before != after:
                raise RuntimeError("File changed while hashing; hash not accepted.")

            item["hash_algorithm"] = "SHA256"
            item["sha256"] = digest
            item["hash_status"] = "verified"
            item["last_verified_utc"] = now()
            item["notes"] = (
                item.get("notes", "") + " "
                + "SHA256 streamed and verified against unchanged file metadata."
            ).strip()
            completed += 1
            outcome = "verified"
            error = None

        except Exception as exc:
            item["hash_algorithm"] = None
            item["sha256"] = None
            item["hash_status"] = "failed"
            item["last_verified_utc"] = None
            item["notes"] = (
                item.get("notes", "") + " "
                + "Hash attempt failed: " + str(exc)
            ).strip()
            failed += 1
            outcome = "failed"
            error = str(exc)

        # Persist each file result immediately.
        save_registry(records)

        event = {
            "run_id": run_id,
            "timestamp_utc": now(),
            "artifact_id": item["artifact_id"],
            "source_root_id": root_id,
            "relative_path": item["relative_path"],
            "status": outcome,
            "sha256": item["sha256"],
            "error": error
        }
        append_event(event)

        counts = {}
        for r in records:
            counts[r["hash_status"]] = counts.get(r["hash_status"], 0) + 1

        atomic_json(PROGRESS, {
            "run_id": run_id,
            "phase_id": "PHASE_02",
            "last_completed_artifact_id": item["artifact_id"],
            "last_completed_relative_path": item["relative_path"],
            "updated_at_utc": now(),
            "batch_size": len(batch),
            "batch_completed": completed,
            "batch_failed": failed,
            "registry_status_counts": counts,
            "remaining_pending": counts.get("pending", 0),
            "remaining_failed": counts.get("failed", 0)
        })

        print(
            outcome.upper(), "|", item["artifact_id"], "|",
            item["source_root_id"], "|", item["relative_path"]
        )

    print("\n===== BATCH SUMMARY =====")
    print("Verified in this batch:", completed)
    print("Failed in this batch:", failed)
    print("Registry status counts:")
    final_counts = {}
    for r in records:
        final_counts[r["hash_status"]] = final_counts.get(r["hash_status"], 0) + 1
    for key, value in sorted(final_counts.items()):
        print(f"{key}: {value}")
    print("Progress checkpoint:", PROGRESS.relative_to(ROOT).as_posix())
    print("Event log:", EVENTS.relative_to(ROOT).as_posix())

if __name__ == "__main__":
    main()
