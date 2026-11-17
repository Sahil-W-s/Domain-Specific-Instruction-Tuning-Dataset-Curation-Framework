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


## First-pass indicator concentration review — 2026-11-17

Owner supplied local aggregate counts by artifact ID, relative path, and source root. The 87,508 indicators are heavily concentrated in structured audit/inventory files and training checkpoint state files, consistent with numeric-field false positives from the broad phone-like heuristic.

Highest concentrations by path:
- `docs/audit/master_file_inventory.csv` in two roots: 26,027 each (52,054 combined).
- `docs/audit/script_catalogue.csv` in two roots: 11,410 each (22,820 combined).
- `outputs/iot_cp_experiments/runs/B2/checkpoints/checkpoint-339/trainer_state.json`: 1,154.
- `phase0_artifact_registry/known_existing_artifacts*.csv` and corresponding inventory copies: 1,002 each across three listed paths.
- Other high-count paths include additional checkpoint `trainer_state.json` files, project audit inventories, data-artifact inventories, recovery logs, and evaluation JSONL/CSV files.

Highest counts by source root:
- `MLCP_RECOVERY`: 42,114
- `MLCP_UPLOAD`: 41,255
- `MLCP_KAGGLE_WORK`: 3,465
- `MLCP_PHASE1_DRAFTS`: 489
- `MLCP_REVIEW_SUBSET`: 185

This distribution supports prioritizing schema/field-context checks on inventory CSVs and trainer-state JSON, rather than treating the matches as confirmed phone numbers. It does not prove that every match is a false positive. Counts for repeated-looking paths across roots are separate source records; do not deduplicate, delete, or select a canonical copy based on these counts.

### Next bounded triage

Inspect only headers/field names and safe structural context for the two highest-concentration file classes (master inventory CSV and script catalogue CSV), plus one B2 trainer-state JSON. Do not print cell values, matched strings, or full records. Then decide whether the phone-like rule is unsuitable for these structured numeric fields and document any targeted exclusions or detector refinement as a new version; preserve the original scan outputs and source files. Separately inspect the scanner's sanitized skip diagnostics to identify the 31 unavailable and 2 path/size mismatch records.


## Structural review of highest-concentration files — 2026-11-17

Owner inspected CSV headers and the top-level JSON field names for the highest-concentration examples.

- `master_file_inventory.csv` headers: `RelativePath`, `FileName`, `Extension`, `Category`, `SizeBytes`, `LastModified`, `FullPath`.
- `script_catalogue.csv` headers: `FileName`, `RelativePath`, `SizeBytes`, `LastModified`, `SHA256`.
- B2 checkpoint-339 `trainer_state.json` top-level keys include training-state fields such as `global_step`, `epoch`, `log_history`, `best_model_checkpoint`, `total_flos`, and callback/state metadata.

These schemas contain no explicitly named phone, email, or contact columns. They include numeric metadata, timestamps, file paths, hashes, and training metrics that could plausibly trigger the broad phone-like regex. This makes false positives likely for these file classes, but headers and key names alone do not establish the contents of every match or clear all files.

The attempted MLCP_UPLOAD path resolution reported FILE NOT FOUND for the two CSVs using the inventory-relative path as joined to the configured root. Other copies resolved and headers were read. Preserve all copies; do not repair paths or modify the inventory based on this observation.

### Next bounded triage

For the two CSV classes, count phone-like regex matches by column locally and report only column names and counts (never cell values). For the trainer-state JSON, inspect key names inside `log_history` only; do not print metric values. Use the existing finding line numbers to narrow the review. Do not rerun the full scan.
