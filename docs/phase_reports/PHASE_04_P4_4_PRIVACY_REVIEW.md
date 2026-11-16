# Phase 4 P4.4 — Privacy Review, Work Unit 1

**Date:** 2026-11-17  
**Status:** Scanner implemented; owner execution and findings review pending.  
**Migration authorization:** Not granted.

## Objective

Begin the bounded privacy/secrets review without repeating the completed ZIP metadata and README inspections. The first pass targets text-like files already represented in the tracked artifact inventory.

## Implementation

Added `scripts/storage/scan_privacy_indicators.py`.

The script:
- Reads configured local source roots from ignored `.local/source_roots.local.yml`.
- Uses `reports/inventory/artifact_inventory.csv` as its candidate list.
- Scans selected text-like extensions only: text/markup, CSV/TSV, JSON/JSONL, YAML, TOML, INI/config, source code, notebooks, shell/PowerShell, SQL, and logs.
- Uses per-file and total-byte limits (defaults: 25 MiB/file and 2 GiB total).
- Detects indicator patterns for private-key headers, common cloud/GitHub/Google API key formats, generic secret assignments, email addresses, and phone-like strings.
- Writes only artifact/root identifiers, relative paths, line numbers, indicator categories, and short one-way fingerprints. It never writes matched values or source lines.
- Writes outputs only under `.local/phase4_privacy_review/`.

## Explicit exclusions and limitations

This first pass does **not** inspect ZIP/archive payloads, PDFs, model weights, images, binary files, or files over configured limits. It does not perform OCR, semantic review, or comprehensive personal-data discovery. A positive indicator is a review lead, not proof of a secret or personal-data exposure. Zero indicators do not establish privacy clearance.

The script validates configured paths remain within their source roots and checks each file's current size against the tracked inventory before reading. It does not modify, move, delete, extract, or hash source files.

## Owner execution

Run after pulling the latest `main`:

```powershell
python scripts/storage/scan_privacy_indicators.py
```

Expected local-only outputs:
- `.local/phase4_privacy_review/privacy_indicator_findings.csv`
- `.local/phase4_privacy_review/privacy_scan_summary.json`

Review these outputs locally. Do not commit them or paste any matched secret values. Share the summary JSON and, if findings exist, the finding rows with values omitted; paths may be redacted if they reveal private locations.

## Current decision

- Scanner implementation is checkpointed.
- Scan has **not** been executed by the owner; no findings are claimed.
- All 41 large-file records remain on hold pending privacy review and per-artifact decisions.
- `manifests/storage_map.yml` remains `migration_authorized: false`.
- No DVC setup or artifact migration has begun.

## Next bounded task

Owner runs the scanner locally and supplies its summary plus sanitized finding rows. Review only flagged indicators and classify the affected artifacts. Then proceed to separate bounded handling for PDF/archive/model payload classes only where necessary.
