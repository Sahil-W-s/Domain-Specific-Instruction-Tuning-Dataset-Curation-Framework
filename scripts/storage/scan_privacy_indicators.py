#!/usr/bin/env python3
"""Bounded, read-only local privacy/secrets indicator scan for ML CP.

Scans only selected text-like files listed in the tracked artifact inventory.
Never prints matched values or source lines. Outputs are local-only and must
not be committed. Does not inspect archives, PDFs, model weights, or binaries.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

TEXT_EXTENSIONS = {
    ".txt", ".md", ".rst", ".csv", ".tsv", ".json", ".jsonl",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env",
    ".py", ".ipynb", ".sh", ".ps1", ".bat", ".log", ".sql",
    ".xml", ".html", ".js", ".ts",
}
SKIP_PARTS = {".git", ".venv", "venv", "__pycache__", "node_modules"}

PATTERNS = {
    "private_key_block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "aws_access_key_id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github_token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b"),
    "google_api_key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "generic_secret_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|refresh[_-]?token|"
        r"password|passwd|secret[_-]?key)\b\s*[:=]\s*['\"]?([A-Za-z0-9_./+=-]{12,})"
    ),
    "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone_like": re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{8,}\d)(?!\w)"),
}

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
    if not candidate.is_file():
        raise ValueError("Inventory candidate is not a regular file")
    if candidate.stat().st_size != expected_size:
        raise ValueError("Source size differs from tracked inventory")
    if any(part.lower() in SKIP_PARTS for part in candidate.parts):
        raise ValueError("Path is inside an excluded environment/cache directory")
    return candidate

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--roots-config", type=Path, default=Path(".local/source_roots.local.yml"))
    parser.add_argument("--inventory", type=Path, default=Path("reports/inventory/artifact_inventory.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path(".local/phase4_privacy_review"))
    parser.add_argument("--max-file-mib", type=int, default=25)
    parser.add_argument("--max-total-gib", type=float, default=2.0)
    args = parser.parse_args()
    if args.max_file_mib < 1 or args.max_total_gib <= 0:
        parser.error("scan limits must be positive")

    repo = args.repo_root.resolve()
    roots_file = args.roots_config if args.roots_config.is_absolute() else repo / args.roots_config
    inventory_file = args.inventory if args.inventory.is_absolute() else repo / args.inventory
    output_dir = args.output_dir if args.output_dir.is_absolute() else repo / args.output_dir
    roots = load_roots(roots_file)

    with inventory_file.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    max_file = args.max_file_mib * 1024 * 1024
    max_total = int(args.max_total_gib * 1024**3)
    scanned_paths: set[str] = set()
    findings: list[dict[str, object]] = []
    skipped: Counter[str] = Counter()
    category_counts: Counter[str] = Counter()
    scanned_bytes = 0
    scanned_files = 0
    inventory_candidates = 0

    for row in rows:
        ext = (row.get("extension") or Path(row.get("file_name", "")).suffix).lower()
        if ext not in TEXT_EXTENSIONS:
            skipped["non_text_extension"] += 1
            continue
        inventory_candidates += 1
        root_id = row.get("source_root_id", "")
        root = roots.get(root_id)
        if root is None:
            skipped["root_not_configured"] += 1
            continue
        try:
            source = resolve_source(root, row.get("relative_path", ""), int(row.get("size_bytes") or -1))
        except Exception as exc:
            skipped[f"source_unavailable_or_mismatch:{type(exc).__name__}"] += 1
            continue

        identity = str(source).casefold()
        if identity in scanned_paths:
            skipped["duplicate_physical_path"] += 1
            continue
        scanned_paths.add(identity)

        size = source.stat().st_size
        if size > max_file:
            skipped["file_over_per_file_limit"] += 1
            continue
        if scanned_bytes + size > max_total:
            skipped["total_byte_budget_reached"] += 1
            break

        try:
            with source.open("rb") as stream:
                raw = stream.read(size + 1)
            if b"\x00" in raw[:8192]:
                skipped["binary_signature_in_text_extension"] += 1
                continue
            content = raw.decode("utf-8-sig", errors="replace")
        except OSError:
            skipped["read_error"] += 1
            continue

        scanned_files += 1
        scanned_bytes += len(raw)
        for line_no, line in enumerate(content.splitlines(), start=1):
            for category, pattern in PATTERNS.items():
                matches = list(pattern.finditer(line))
                if not matches:
                    continue
                category_counts[category] += len(matches)
                # Store only a one-way short fingerprint, never the matched value.
                for match in matches:
                    token = match.group(0)
                    findings.append({
                        "artifact_id": row.get("artifact_id", ""),
                        "source_root_id": root_id,
                        "relative_path": row.get("relative_path", ""),
                        "line_number": line_no,
                        "category": category,
                        "match_fingerprint": hashlib.sha256(token.encode("utf-8", errors="replace")).hexdigest()[:12],
                    })

    output_dir.mkdir(parents=True, exist_ok=True)
    findings_path = output_dir / "privacy_indicator_findings.csv"
    with findings_path.open("w", encoding="utf-8-sig", newline="") as handle:
        fields = ["artifact_id", "source_root_id", "relative_path", "line_number", "category", "match_fingerprint"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(findings)

    summary = {
        "task": "ML CP P4.4 bounded local text privacy/secrets indicator scan",
        "inventory_records": len(rows),
        "text_extension_candidates": inventory_candidates,
        "unique_files_scanned": scanned_files,
        "bytes_scanned": scanned_bytes,
        "max_file_bytes": max_file,
        "max_total_bytes": max_total,
        "finding_count": len(findings),
        "finding_counts_by_category": dict(sorted(category_counts.items())),
        "skipped_counts": dict(sorted(skipped.items())),
        "safety": {
            "read_only": True,
            "source_files_modified": False,
            "source_files_moved_or_deleted": False,
            "archives_or_zip_payloads_read": False,
            "pdf_payloads_read": False,
            "model_weights_read": False,
            "matched_values_or_source_lines_written": False,
            "outputs_local_only": True,
        },
        "outputs": [findings_path.name, "privacy_scan_summary.json"],
        "interpretation": (
            "Indicators require manual review. Matches may be false positives; "
            "zero matches do not establish privacy clearance. Archives, PDFs, "
            "model weights, oversized files, and skipped/unavailable files were not cleared."
        ),
    }
    (output_dir / "privacy_scan_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"\nLocal-only outputs: {output_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
