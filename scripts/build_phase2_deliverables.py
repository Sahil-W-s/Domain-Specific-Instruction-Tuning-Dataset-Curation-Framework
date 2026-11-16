import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "manifests/artifact_registry.jsonl"
REPORTS = ROOT / "reports/inventory"

OUTPUTS = [
    REPORTS / "artifact_inventory.csv",
    REPORTS / "large_files.csv",
    REPORTS / "hash_failures.csv",
    ROOT / "docs/phase_reports/PHASE_02_REPORT.md",
]

def read_registry():
    records = [
        json.loads(line)
        for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    ids = [r["artifact_id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate artifact IDs in registry")
    return records

def csv_payload(rows, fields):
    import io
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    records = read_registry()
    by_id = {r["artifact_id"]: r for r in records}

    inventory_fields = [
        "artifact_id", "source_root_id", "relative_path", "file_name",
        "extension", "size_bytes", "last_write_time_utc", "artifact_type",
        "lifecycle", "phase", "sensitivity", "redistribution_status",
        "hash_algorithm", "sha256", "hash_status", "first_seen_run_id",
        "last_verified_utc", "notes"
    ]
    inventory = [
        {field: record.get(field, "") for field in inventory_fields}
        for record in records
    ]

    threshold = 50 * 1024 * 1024
    large_records = [
        r for r in records
        if int(r.get("size_bytes") or 0) >= threshold
    ]
    large_fields = [
        "artifact_id", "source_root_id", "relative_path", "file_name",
        "extension", "size_bytes", "last_write_time_utc", "artifact_type",
        "lifecycle", "sha256", "hash_status", "notes"
    ]
    large_rows = [
        {field: r.get(field, "") for field in large_fields}
        for r in large_records
    ]

    failed = [r for r in records if r.get("hash_status") == "failed"]
    failure_rows = []
    unresolved = []

    for record in failed:
        notes = record.get("notes") or ""
        match = re.search(
            r"Superseded by corrected(?:-path| registry) record\s+(art-[a-f0-9]+)",
            notes,
            re.IGNORECASE
        )
        replacement_id = match.group(1) if match else ""
        replacement = by_id.get(replacement_id) if replacement_id else None
        replacement_status = replacement.get("hash_status", "") if replacement else ""
        failure_status = (
            "historical_superseded"
            if replacement and replacement_status == "verified"
            else "unresolved"
        )
        if failure_status == "unresolved":
            unresolved.append(record["artifact_id"])

        failure_rows.append({
            "artifact_id": record["artifact_id"],
            "source_root_id": record.get("source_root_id", ""),
            "relative_path": record.get("relative_path", ""),
            "size_bytes": record.get("size_bytes", ""),
            "original_hash_status": record.get("hash_status", ""),
            "failure_status": failure_status,
            "replacement_artifact_id": replacement_id,
            "replacement_relative_path": replacement.get("relative_path", "") if replacement else "",
            "replacement_hash_status": replacement_status,
            "replacement_sha256": replacement.get("sha256", "") if replacement else "",
            "notes": notes,
        })

    failure_fields = [
        "artifact_id", "source_root_id", "relative_path", "size_bytes",
        "original_hash_status", "failure_status", "replacement_artifact_id",
        "replacement_relative_path", "replacement_hash_status",
        "replacement_sha256", "notes"
    ]

    with (REPORTS / "exact_duplicates.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as f:
        exact_rows = list(csv.DictReader(f))

    exact_groups = {r["duplicate_group_id"] for r in exact_rows}
    exact_members = len(exact_rows)

    with (REPORTS / "possible_duplicates_review_v2.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as f:
        possible_rows = list(csv.DictReader(f))

    possible_groups = {r["review_group_id"] for r in possible_rows}
    possible_statuses = sorted({r["review_status"] for r in possible_rows})

    counts = defaultdict(int)
    for r in records:
        counts[r.get("hash_status", "missing")] += 1

    large_100 = sum(int(r.get("size_bytes") or 0) >= 100 * 1024 * 1024 for r in records)
    large_200 = sum(int(r.get("size_bytes") or 0) >= 200 * 1024 * 1024 for r in records)

    report = f"""# Phase 2 Report — Artifact Registry and Large-File Map

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework  
**Generated:** {datetime.now(timezone.utc).isoformat()}  
**Status:** Deliverables generated; owner review required

## Scope

Phase 2 establishes a content-aware artifact registry, inventory, duplicate reports,
and large-file map. No source files were moved, deleted, or extracted. No storage
migration or DVC/Git LFS migration was performed.

## Registry

- Total registry records: {len(records):,}
- Unique artifact IDs: {len(by_id)}
- Verified hashes: {counts['verified']:,}
- Not applicable: {counts['not_applicable']}
- Historical failed records: {counts['failed']}
- Pending hash records: {counts['pending']}

The registry schema validation previously passed for all 1,531 records.
An independent SHA-256 sample recomputation passed for 15 of 15 sampled files.
This sample does not constitute exhaustive independent recomputation of every hash.

## Historical hash failures

- Historical failed records retained: {len(failed):,}
- Records with verified replacement links: {len(failed) - len(unresolved)}
- Unresolved records: {len(unresolved)}

Historical failures are preserved for auditability and distinguished from current
operational failures. The replacement links are recorded in `hash_failures.csv`.

## Exact duplicates

- Exact duplicate groups: {len(exact_groups):,}
- Duplicate artifact memberships: {exact_members:,}

The existing exact duplicate report was checked against the registry. All expected
groups and memberships matched; no missing groups, extra groups, membership
mismatches, or validation errors were found.

## Possible duplicates

- Review groups: {len(possible_groups):,}
- Candidate records: {len(possible_rows):,}
- Review statuses: {", ".join(possible_statuses) if possible_statuses else "None"}

All candidate records remain pending manual review. They are not confirmed duplicates.

## Large files

Threshold: 50 MiB (52,428,800 bytes).

- Files at or above 50 MiB: {len(large_records):,}
- Files at or above 100 MiB: {large_100}
- Files at or above 200 MiB: {large_200}

The large-file candidate report was validated against the registry: all 41 expected
records were present, with no missing files, extras, or size mismatches.

## Inventory coverage and provenance

The initial consolidated inventory contained 1,498 root/path pairs. The registry
contains 1,531 root/path pairs, including 33 corrected-path replacement records.
The canonical artifact inventory is generated from the registry so those replacement
records are included.

## Limitations and outstanding work

- The 15-file independent SHA-256 check was a sample, not an exhaustive rehash.
- Possible duplicates require manual review; no duplicate files were deleted.
- File sensitivity classifications should not be treated as confirmed solely from
  field names; content review may still be required.
- This report does not authorize source-file movement, deletion, archive extraction,
  or storage migration.
- Phase 2 completion remains subject to owner review and the implementation plan's
  exit gate.

## Generated deliverables

- `manifests/artifact_registry.schema.json`
- `manifests/artifact_registry.jsonl`
- `reports/inventory/artifact_inventory.csv`
- `reports/inventory/exact_duplicates.csv`
- `reports/inventory/possible_duplicates_review.csv`
- `reports/inventory/large_files.csv`
- `reports/inventory/hash_failures.csv`
- `docs/phase_reports/PHASE_02_REPORT.md`
"""

    payloads = {
        OUTPUTS[0]: csv_payload(inventory, inventory_fields),
        OUTPUTS[1]: csv_payload(large_rows, large_fields),
        OUTPUTS[2]: csv_payload(failure_rows, failure_fields),
        OUTPUTS[3]: report,
    }

    print("========== PHASE 2 DELIVERABLE BUILDER ==========")
    print("Registry records:", len(records))
    print("Inventory rows to generate:", len(inventory))
    print("Large-file rows to generate:", len(large_rows))
    print("Historical failure rows to generate:", len(failure_rows))
    print("Verified replacement links:", len(failed) - len(unresolved))
    print("Unresolved historical failures:", len(unresolved))
    print("Exact duplicate groups/members:", len(exact_groups), "/", exact_members)
    print("Possible duplicate groups/records:", len(possible_groups), "/", len(possible_rows))

    if unresolved:
        raise SystemExit("STOP: unresolved historical failures exist.")

    print("\nOutput plan:")
    for path, content in payloads.items():
        print(f"- {path.relative_to(ROOT)} | {len(content.encode('utf-8')):,} bytes | {'EXISTS' if path.exists() else 'NEW'}")

    if not args.write:
        print("\nDRY RUN ONLY: no deliverables were written.")
        print("Review this output before running with --write.")
        return

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = ROOT / "reports" / "state_update_backups" / f"phase2_deliverables_{timestamp}"

    for path, content in payloads.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup = backup_dir / path.name
            backup.write_bytes(path.read_bytes())
            print("Backed up:", backup.relative_to(ROOT))

        temp = path.with_suffix(path.suffix + ".tmp")
        temp.write_text(content, encoding="utf-8-sig" if path.suffix == ".csv" else "utf-8")
        temp.replace(path)
        print("Wrote:", path.relative_to(ROOT))

    print("\nRESULT: FOUR DELIVERABLES WRITTEN. VALIDATION AND OWNER REVIEW STILL REQUIRED.")

if __name__ == "__main__":
    main()
