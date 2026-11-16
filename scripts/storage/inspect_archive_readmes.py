#!/usr/bin/env python3
"""Bounded, read-only extraction of small README-named ZIP entries.

Reads only README payloads up to 64 KiB. Does not extract files to disk,
read other entry payloads, modify source archives, or compute source hashes.
Output is local-only because README text may contain private details.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path

MAX_README_BYTES = 64 * 1024


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value.split(" #", 1)[0].strip()


def load_roots(path: Path) -> dict[str, Path]:
    if not path.is_file():
        raise FileNotFoundError(f"Local source-root config not found: {path}")
    roots: dict[str, Path] = {}
    current_id: str | None = None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"^\s*-\s*id:\s*(.*?)\s*$", line)
        if match:
            current_id = scalar(match.group(1))
            continue
        match = re.match(r"^\s*path:\s*(.*?)\s*$", line)
        if match and current_id:
            roots[current_id] = Path(scalar(match.group(1))).expanduser()
            current_id = None
    if not roots:
        raise ValueError(f"No source roots found in {path}")
    return roots


def resolve_source(root: Path, relative: str, expected_size: int) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Inventory path is absolute or contains '..'")
    resolved_root = root.resolve(strict=True)
    candidate = (resolved_root / rel).resolve(strict=True)
    candidate.relative_to(resolved_root)
    if candidate.stat().st_size != expected_size:
        raise ValueError("Source size differs from tracked inventory")
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--roots-config", type=Path, default=Path(".local/source_roots.local.yml"))
    parser.add_argument("--inventory", type=Path, default=Path("reports/inventory/large_files.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path(".local/phase4_archive_inspection"))
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    roots_file = args.roots_config if args.roots_config.is_absolute() else repo / args.roots_config
    inventory_file = args.inventory if args.inventory.is_absolute() else repo / args.inventory
    output_dir = args.output_dir if args.output_dir.is_absolute() else repo / args.output_dir
    roots = load_roots(roots_file)

    with inventory_file.open("r", encoding="utf-8-sig", newline="") as handle:
        zip_rows = [r for r in csv.DictReader(handle) if (r.get("extension") or "").lower() == ".zip"]

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in zip_rows:
        key = (row.get("sha256") or "").strip().lower()
        if not re.fullmatch(r"[0-9a-f]{64}", key):
            raise ValueError(f"Invalid tracked SHA-256 for artifact {row.get('artifact_id')}")
        groups[key].append(row)

    output_dir.mkdir(parents=True, exist_ok=True)
    report = [
        "# Local-only ZIP README review",
        "",
        "Only README-named entries were read. No entries were extracted.",
        "Review locally before sharing; README text may contain private details.",
        "",
    ]
    summary = {
        "task": "ML CP P4.3 bounded README payload review",
        "zip_inventory_records": len(zip_rows),
        "unique_archive_groups": len(groups),
        "archives_opened": 0,
        "readme_entries_read": 0,
        "readme_entries_skipped_over_limit": 0,
        "errors": [],
        "safety": {
            "readme_entries_only": True,
            "extracted_any_entries": False,
            "modified_source_archives": False,
            "computed_new_source_hashes": False,
        },
        "output": "archive_readmes_local.md",
    }

    for sha, copies in sorted(groups.items()):
        source = None
        resolution_errors = []
        for row in copies:
            try:
                root = roots[row.get("source_root_id", "")]
                source = resolve_source(root, row.get("relative_path", ""), int(row.get("size_bytes") or -1))
                break
            except Exception as exc:
                resolution_errors.append(f"{row.get('artifact_id')}: {type(exc).__name__}: {exc}")
        if source is None:
            summary["errors"].append({"sha256": sha, "errors": resolution_errors})
            continue

        try:
            with zipfile.ZipFile(source, "r") as archive:
                summary["archives_opened"] += 1
                readmes = [
                    info for info in archive.infolist()
                    if Path(info.filename.replace("\\", "/")).name.lower().startswith("readme")
                    and not info.is_dir()
                ]
                report.extend([
                    "## Archive",
                    f"Inventory relative path: {copies[0].get('relative_path', '')}",
                    f"SHA-256 group: {sha}",
                    "",
                ])
                if not readmes:
                    report.extend(["No README-named entries found.", ""])
                for info in readmes:
                    report.extend([f"### Entry: {info.filename}", ""])
                    if info.file_size > MAX_README_BYTES:
                        summary["readme_entries_skipped_over_limit"] += 1
                        report.extend([f"Skipped: declared size {info.file_size} bytes exceeds {MAX_README_BYTES}-byte limit.", ""])
                        continue
                    with archive.open(info, "r") as stream:
                        payload = stream.read(MAX_README_BYTES + 1)
                    if len(payload) > MAX_README_BYTES:
                        summary["readme_entries_skipped_over_limit"] += 1
                        report.extend(["Skipped: actual read exceeded the size limit.", ""])
                        continue
                    summary["readme_entries_read"] += 1
                    decoded = payload.decode("utf-8", errors="replace")
                    report.extend(["--- README CONTENT START ---", decoded.rstrip(), "--- README CONTENT END ---", ""])
        except Exception as exc:
            summary["errors"].append({"sha256": sha, "error": f"{type(exc).__name__}: {exc}"})

    (output_dir / "archive_readmes_local.md").write_text("\n".join(report), encoding="utf-8")
    (output_dir / "readme_inspection_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"\nLocal-only output directory: {output_dir}")
    return 0 if not summary["errors"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
