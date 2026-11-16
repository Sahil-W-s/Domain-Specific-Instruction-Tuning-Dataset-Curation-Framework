# Phase 4 P4.4 — Privacy Review, Work Unit 1

**Date:** 2026-11-17  
**Status:** First bounded scan executed; indicator triage pending.  
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

## Execution result — 2026-11-17

Owner executed the scanner successfully.

| Metric | Result |
|---|---:|
| Inventory records | 1,531 |
| Text-extension candidates | 1,286 |
| Unique files scanned | 1,253 |
| Bytes scanned | 369,784,161 (~352.7 MiB) |
| Findings | 87,508 |
| Findings category | 87,508 phone-like; zero reported credential/private-key/email indicators |
| Unavailable or mismatched source records | 33 |
| Non-text extensions excluded | 245 |

The only reported finding category was `phone_like`. This pattern is a broad numeric-format heuristic and can match non-phone content such as IDs, numeric fields, timestamps, and dataset values. Therefore 87,508 is an indicator count, **not** a count of phone numbers or exposed personal records. No actual values were included in the summary, and no secret values should be shared.

The scan reports read-only operation: no source modifications, moves, or deletions; no archive, PDF, or model-weight payload reads; and local-only output. These are the scanner's reported execution properties.

## Required triage before classification

1. Aggregate phone-like indicators by artifact ID and file path to determine whether they cluster in a small number of structured datasets/logs or are broadly distributed.
2. Inspect only the relevant local source context for a small representative sample of flagged records, without copying matched values into chat or GitHub.
3. Determine why 31 source records were unavailable and why 2 failed path/size validation. The current summary exposes only exception classes, not the underlying paths/reasons.
4. Keep excluded non-text, oversized, unavailable, archive, PDF, and model artifacts un-cleared.

## Explicit exclusions and limitations

This first pass does **not** inspect ZIP/archive payloads, PDFs, model weights, images, binary files, or files over configured limits. It does not perform OCR, semantic review, or comprehensive personal-data discovery. A positive indicator is a review lead, not proof of a secret or personal-data exposure. Zero indicators do not establish privacy clearance.

## Current decision

- Scanner implementation is checkpointed and first scan executed.
- Phone-like findings are untriaged; no personal-data exposure is established by the count alone.
- Credential/private-key/email indicators were not reported by this scan.
- All 41 large-file records remain on hold pending privacy review and per-artifact decisions.
- `manifests/storage_map.yml` remains `migration_authorized: false`.
- No DVC setup or artifact migration has begun.

## Next bounded task

Produce a local aggregate of phone-like indicators by artifact ID/path (no matched values), then triage only the highest-concentration files and explain the 33 skipped records. Do not rerun the full scan or inspect unrelated payloads.
