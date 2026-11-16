import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
from datetime import datetime, timezone

import yaml

PROJECT = Path(__file__).resolve().parents[1]
REGISTRY = PROJECT / "manifests/artifact_registry.jsonl"
CONFIG = PROJECT / ".local/source_roots.local.yml"
CHECKPOINT = PROJECT / "state/hash_progress.json"
REPORT_DIR = PROJECT / "reports/inventory"
BACKUP_DIR = PROJECT / "state/phase2_repair_backups"

CHUNK_SIZE = 8 * 1024 * 1024
EXCLUDED_DIRS = {".git", ".venv", "__pycache__"}

def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load_jsonl():
    records = [
        json.loads(line)
        for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    ids = [r["artifact_id"] for r in records]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate artifact IDs detected.")
    return records

def counts(records):
    result = {
        "verified": 0,
        "pending": 0,
        "failed": 0,
        "not_applicable": 0
    }
    for r in records:
        status = r["hash_status"]
        if status not in result:
            raise RuntimeError(f"Unexpected status: {status}")
        result[status] += 1
    return result

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()

def atomic_write(path, content):
    temp = path.with_name(path.name + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)

def save_checkpoint(records):
    if not CHECKPOINT.exists():
        return

    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    checkpoint["registry_status_counts"] = counts(records)
    checkpoint["remaining_pending"] = checkpoint["registry_status_counts"]["pending"]
    checkpoint["remaining_failed"] = checkpoint["registry_status_counts"]["failed"]
    checkpoint["reconciled_at_utc"] = now()

    atomic_write(CHECKPOINT, json.dumps(checkpoint, indent=2) + "\n")

def load_roots():
    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    roots = []
    for item in config["roots"]:
        path = Path(item["path"]).resolve()
        if not path.is_dir():
            raise RuntimeError(f"Configured source root unavailable: {item['id']}")
        roots.append((item["id"], path))
    return roots

def build_filename_index(roots, wanted_names):
    index = {name.casefold(): [] for name in wanted_names}

    for root_id, root in roots:
        for current, dirs, files in os.walk(root):
            dirs[:] = [
                d for d in dirs
                if d.casefold() not in EXCLUDED_DIRS
            ]

            for filename in files:
                key = filename.casefold()
                if key in index:
                    path = Path(current) / filename
                    try:
                        resolved = path.resolve()
                        if not resolved.is_file():
                            continue
                        if not resolved.is_relative_to(root):
                            continue
                        index[key].append((root_id, root, resolved))
                    except (OSError, RuntimeError):
                        continue

    return index

def find_replacement(record, candidates):
    expected_size = int(record["size_bytes"])
    baseline = datetime.fromisoformat(
        record["last_write_time_utc"].replace("Z", "+00:00")
    ).timestamp()

    valid = []

    for root_id, root, path in candidates:
        try:
            stat = path.stat()

            if stat.st_size != expected_size:
                continue

            if abs(stat.st_mtime - baseline) >= 2:
                continue

            digest = sha256(path)

            relative = path.relative_to(root).as_posix()
            valid.append({
                "root_id": root_id,
                "root": root,
                "path": path,
                "relative_path": relative,
                "size_bytes": stat.st_size,
                "timestamp": stat.st_mtime,
                "sha256": digest
            })
        except (OSError, PermissionError):
            continue

    if not valid:
        return None, "No candidate matched baseline size and timestamp."

    # Prefer exactly one matching candidate in the original root.
    original_root = record["source_root_id"]
    original_matches = [
        c for c in valid if c["root_id"] == original_root
    ]

    if len(original_matches) == 1:
        return original_matches[0], None

    if len(original_matches) > 1:
        return None, "Multiple matching candidates exist in the original root."

    if len(valid) == 1:
        return valid[0], None

    return None, (
        "Multiple matching candidates exist outside the original root; "
        "manual source-root selection required."
    )

def replacement_id(root_id, relative_path):
    identity = root_id + "\0" + relative_path
    return "art-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not REGISTRY.is_file() or not CONFIG.is_file():
        raise RuntimeError("Registry or local root configuration missing.")

    records = load_jsonl()
    by_id = {r["artifact_id"]: r for r in records}

    unresolved = [
        r for r in records
        if r["hash_status"] == "failed"
        and "Superseded" not in (r.get("notes") or "")
    ]

    if not unresolved:
        print(json.dumps({
            "status": "clean",
            "repaired": 0,
            "unresolved": 0,
            "counts": counts(records)
        }, indent=2))
        return

    roots = load_roots()
    names = {r["file_name"] for r in unresolved}
    index = build_filename_index(roots, names)

    repairs = []
    blocked = []

    for old in unresolved:
        candidates = index.get(old["file_name"].casefold(), [])
        candidate, reason = find_replacement(old, candidates)

        if candidate is None:
            blocked.append({
                "artifact_id": old["artifact_id"],
                "file_name": old["file_name"],
                "reason": reason
            })
            continue

        new_id = replacement_id(
            candidate["root_id"],
            candidate["relative_path"]
        )

        if new_id in by_id:
            existing = by_id[new_id]
            if (
                existing["source_root_id"] == candidate["root_id"]
                and existing["relative_path"] == candidate["relative_path"]
                and existing["hash_status"] in ("pending", "verified")
            ):
                # Existing replacement is valid. Annotate original if needed.
                repairs.append({
                    "old": old,
                    "existing": existing,
                    "candidate": candidate,
                    "new_id": new_id,
                    "already_exists": True
                })
                continue

            blocked.append({
                "artifact_id": old["artifact_id"],
                "file_name": old["file_name"],
                "reason": f"Deterministic replacement ID collision: {new_id}"
            })
            continue

        repairs.append({
            "old": old,
            "candidate": candidate,
            "new_id": new_id,
            "already_exists": False
        })

    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "proposed_repairs": [
                {
                    "old_id": x["old"]["artifact_id"],
                    "new_id": x["new_id"],
                    "root_id": x["candidate"]["root_id"],
                    "relative_path": x["candidate"]["relative_path"],
                    "sha256": x["candidate"]["sha256"],
                    "already_exists": x["already_exists"]
                }
                for x in repairs
            ],
            "blocked": blocked,
            "counts": counts(records)
        }, indent=2))
        if blocked:
            raise SystemExit(2)
        return

    if blocked:
        print(json.dumps({
            "status": "blocked",
            "blocked": blocked,
            "safe_repairs_available": len(repairs)
        }, indent=2))
        raise SystemExit(2)

    if not repairs:
        raise RuntimeError("No safe repairs found.")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy2(REGISTRY, BACKUP_DIR / f"artifact_registry_{stamp}.jsonl")
    if CHECKPOINT.exists():
        shutil.copy2(CHECKPOINT, BACKUP_DIR / f"hash_progress_{stamp}.json")

    report_repairs = []

    for item in repairs:
        old = item["old"]
        candidate = item["candidate"]
        new_id = item["new_id"]

        if not item["already_exists"]:
            new = dict(old)
            new.update({
                "artifact_id": new_id,
                "source_root_id": candidate["root_id"],
                "relative_path": candidate["relative_path"],
                "file_name": candidate["path"].name,
                "hash_algorithm": None,
                "sha256": None,
                "hash_status": "pending",
                "first_seen_run_id": "PHASE_02_AUTO_RECONCILE_" + stamp,
                "last_verified_utc": None,
                "notes": (
                    f"Automatically reconciled path. Candidate SHA256 precheck: "
                    f"{candidate['sha256']}. Original failed record "
                    f"{old['artifact_id']} retained."
                )
            })
            records.append(new)
            by_id[new_id] = new

        old["notes"] = (
            (old.get("notes") or "").rstrip()
            + f" Superseded by corrected-path record {new_id}; original failure retained."
        )

        report_repairs.append({
            "original_artifact_id": old["artifact_id"],
            "replacement_artifact_id": new_id,
            "source_root_id": candidate["root_id"],
            "relative_path": candidate["relative_path"],
            "prechecked_sha256": candidate["sha256"],
            "replacement_already_existed": item["already_exists"]
        })

    content = "".join(
        json.dumps(r, ensure_ascii=False) + "\n" for r in records
    )
    atomic_write(REGISTRY, content)
    save_checkpoint(records)

    report = {
        "run_id": "PHASE_02_AUTO_RECONCILE_" + stamp,
        "created_utc": now(),
        "repairs": report_repairs,
        "blocked": blocked,
        "source_files_modified": False,
        "original_failures_preserved": True,
        "counts": counts(records)
    }

    report_path = REPORT_DIR / f"auto_reconciliation_{stamp}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(report_path, json.dumps(report, indent=2) + "\n")

    print(json.dumps({
        "status": "reconciled",
        "new_records_created": sum(
            not x["replacement_already_existed"] for x in report_repairs
        ),
        "repairs": report_repairs,
        "counts": counts(records),
        "report": str(report_path.relative_to(PROJECT))
    }, indent=2))

if __name__ == "__main__":
    main()
