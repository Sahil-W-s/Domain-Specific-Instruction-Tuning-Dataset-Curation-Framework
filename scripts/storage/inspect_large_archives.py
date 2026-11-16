#!/usr/bin/env python3
"""Read-only ZIP central-directory inventory for ML CP Phase 4 P4.3.

This script does not extract entries, read entry payloads, modify source archives,
or compute new hashes. It inspects ZIP metadata only.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import stat
import zipfile
from collections import defaultdict
from pathlib import Path, PurePosixPath

SENSITIVE_NAME = re.compile(
    r"(^|[/_.-])(?:\.env(?:\..*)?|secrets?|credentials?|tokens?|"
    r"api[_-]?keys?|client[_-]?secrets?|passwords?|passwd|"
    r"id_rsa|id_ed25519|private[_-]?keys?)(?:$|[/_.-])",
    re.IGNORECASE,
)
LICENSE_NAME = re.compile(r"(^|[/_.-])(license|licence|notice|copying)(?:[._-].*)?$", re.IGNORECASE)
README_NAME = re.compile(r"(^|/)readme(?:[._-].*)?$", re.IGNORECASE)
MANIFEST_NAME = re.compile(
    r"(^|/)(manifest|metadata|dataset_card|model_card|requirements|environment|"
    r"pyproject|setup|config)(?:[._-].*)?$",
    re.IGNORECASE,
)


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value.split(" #", 1)[0].strip()


def load_roots(path: Path) -> dict[str, Path]:
    """Read only id/path pairs from the local YAML file; no YAML dependency."""
    if not path.is_file():
        raise FileNotFoundError(f"Local source-root config not found: {path}")
    roots: dict[str, Path] = {}
    current_id: str | None = None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        id_match = re.match(r"^\s*-\s*id:\s*(.*?)\s*$", line)
        if id_match:
            current_id = scalar(id_match.group(1))
            continue
        path_match = re.match(r"^\s*path:\s*(.*?)\s*$", line)
        if path_match and current_id:
            roots[current_id] = Path(scalar(path_match.group(1))).expanduser()
            current_id = None
    if not roots:
        raise ValueError(f"No root id/path pairs found in {path}")
    return roots


def safe_candidate(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Inventory relative path is absolute or contains '..'")
    resolved_root = root.resolve(strict=True)
    candidate = (resolved_root / rel).resolve(strict=True)
    candidate.relative_to(resolved_root)
    return candidate


def entry_flags(info: zipfile.ZipInfo) -> tuple[bool, bool, bool]:
    name = info.filename.replace("\\", "/")
    posix = PurePosixPath(name)
    unsafe = name.startswith("/") or bool(re.match(r"^[A-Za-z]:", name)) or ".." in posix.parts
    encrypted = bool(info.flag_bits & 0x1)
    mode = (info.external_attr >> 16) & 0o170000
    is_symlink = mode == stat.S_IFLNK
    return unsafe, encrypted, is_symlink


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--roots-config", type=Path, default=Path(".local/source_roots.local.yml"))
    parser.add_argument("--inventory", type=Path, default=Path("reports/inventory/large_files.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path(".local/phase4_archive_inspection"))
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    roots_cfg = args.roots_config if args.roots_config.is_absolute() else repo / args.roots_config
    inventory = args.inventory if args.inventory.is_absolute() else repo / args.inventory
    output_dir = args.output_dir if args.output_dir.is_absolute() else repo / args.output_dir

    roots = load_roots(roots_cfg)
    if not inventory.is_file():
        raise FileNotFoundError(f"Inventory not found: {inventory}")

    with inventory.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [r for r in csv.DictReader(handle) if (r.get("extension") or "").lower() == ".zip"]

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        sha = (row.get("sha256") or "").strip().lower()
        if not re.fullmatch(r"[0-9a-f]{64}", sha):
            row["_inspection_note"] = "missing_or_invalid_inventory_sha256"
        grouped[sha or f"invalid-{row.get('artifact_id','unknown')}"].append(row)

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_rows: list[dict[str, object]] = []
    entry_rows: list[dict[str, object]] = []
    inspected_unique = 0

    for group_key, copies in sorted(grouped.items()):
        representative = None
        resolution_errors: list[str] = []
        for row in copies:
            root_id = row.get("source_root_id", "")
            root = roots.get(root_id)
            if root is None:
                resolution_errors.append(f"{root_id}:root_not_configured")
                continue
            try:
                candidate = safe_candidate(root, row.get("relative_path", ""))
                actual_size = candidate.stat().st_size
                expected_size = int(row.get("size_bytes") or -1)
                if actual_size != expected_size:
                    resolution_errors.append(
                        f"{root_id}:{row.get('relative_path')}:size_mismatch:{actual_size}!={expected_size}"
                    )
                    continue
                representative = (row, candidate)
                break
            except Exception as exc:
                resolution_errors.append(f"{root_id}:{row.get('relative_path')}:{type(exc).__name__}:{exc}")

        summary: dict[str, object] = {
            "archive_sha256": group_key,
            "artifact_ids": ";".join(r.get("artifact_id", "") for r in copies),
            "source_record_count": len(copies),
            "representative_artifact_id": "",
            "representative_source_root_id": "",
            "representative_relative_path": "",
            "inventory_size_bytes": copies[0].get("size_bytes", ""),
            "inspection_status": "not_inspected",
            "entry_count": 0,
            "total_uncompressed_bytes": 0,
            "total_compressed_bytes": 0,
            "license_or_notice_entries": 0,
            "readme_entries": 0,
            "manifest_or_config_entries": 0,
            "potential_sensitive_filename_entries": 0,
            "encrypted_entries": 0,
            "unsafe_path_entries": 0,
            "symlink_entries": 0,
            "inspection_error": "",
        }

        if representative is None:
            summary["inspection_status"] = "source_not_found_or_size_mismatch"
            summary["inspection_error"] = " | ".join(resolution_errors)
            archive_rows.append(summary)
            continue

        row, archive_path = representative
        summary.update({
            "representative_artifact_id": row.get("artifact_id", ""),
            "representative_source_root_id": row.get("source_root_id", ""),
            "representative_relative_path": row.get("relative_path", ""),
        })

        try:
            with zipfile.ZipFile(archive_path, "r") as zf:
                infos = zf.infolist()  # Central-directory metadata only; no payload extraction/read.
                summary["entry_count"] = len(infos)
                summary["total_uncompressed_bytes"] = sum(i.file_size for i in infos)
                summary["total_compressed_bytes"] = sum(i.compress_size for i in infos)
                for info in infos:
                    name = info.filename.replace("\\", "/")
                    unsafe, encrypted, symlink = entry_flags(info)
                    is_license = bool(LICENSE_NAME.search(name))
                    is_readme = bool(README_NAME.search(name))
                    is_manifest = bool(MANIFEST_NAME.search(name))
                    is_sensitive = bool(SENSITIVE_NAME.search(name))
                    summary["license_or_notice_entries"] += int(is_license)
                    summary["readme_entries"] += int(is_readme)
                    summary["manifest_or_config_entries"] += int(is_manifest)
                    summary["potential_sensitive_filename_entries"] += int(is_sensitive)
                    summary["encrypted_entries"] += int(encrypted)
                    summary["unsafe_path_entries"] += int(unsafe)
                    summary["symlink_entries"] += int(symlink)
                    entry_rows.append({
                        "archive_sha256": group_key,
                        "archive_artifact_ids": summary["artifact_ids"],
                        "representative_artifact_id": row.get("artifact_id", ""),
                        "source_root_id": row.get("source_root_id", ""),
                        "archive_relative_path": row.get("relative_path", ""),
                        "entry_name": info.filename,
                        "file_size_bytes": info.file_size,
                        "compressed_size_bytes": info.compress_size,
                        "extension": Path(name).suffix.lower(),
                        "is_directory": info.is_dir(),
                        "is_license_or_notice_name": is_license,
                        "is_readme_name": is_readme,
                        "is_manifest_or_config_name": is_manifest,
                        "potential_sensitive_filename": is_sensitive,
                        "encrypted": encrypted,
                        "unsafe_path": unsafe,
                        "symlink": symlink,
                    })
            summary["inspection_status"] = "metadata_listed_no_extraction"
            inspected_unique += 1
        except (zipfile.BadZipFile, OSError, RuntimeError, ValueError) as exc:
            summary["inspection_status"] = "zip_inspection_error"
            summary["inspection_error"] = f"{type(exc).__name__}: {exc}"

        archive_rows.append(summary)

    def write_csv(path: Path, data: list[dict[str, object]]) -> None:
        if not data:
            path.write_text("", encoding="utf-8")
            return
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(data[0].keys()))
            writer.writeheader()
            writer.writerows(data)

    archive_csv = output_dir / "archive_summary.csv"
    entries_csv = output_dir / "archive_entries.csv"
    summary_json = output_dir / "inspection_summary.json"
    write_csv(archive_csv, archive_rows)
    write_csv(entries_csv, entry_rows)

    result = {
        "task": "ML CP Phase 4 P4.3 read-only ZIP metadata inspection",
        "source_inventory": str(inventory.relative_to(repo)) if inventory.is_relative_to(repo) else inventory.name,
        "archive_records_in_inventory": len(rows),
        "unique_archive_sha256_groups": len(grouped),
        "unique_archives_metadata_listed": inspected_unique,
        "entry_metadata_records": len(entry_rows),
        "archives_not_inspected_or_with_errors": [
            {
                "sha256": a["archive_sha256"],
                "status": a["inspection_status"],
                "error": a["inspection_error"],
            }
            for a in archive_rows
            if a["inspection_status"] != "metadata_listed_no_extraction"
        ],
        "safety": {
            "extracted_any_entries": False,
            "read_any_entry_payloads": False,
            "modified_source_archives": False,
            "computed_new_source_hashes": False,
        },
        "outputs": [archive_csv.name, entries_csv.name, summary_json.name],
    }
    summary_json.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"\nLocal output directory: {output_dir}")
    return 0 if not result["archives_not_inspected_or_with_errors"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
