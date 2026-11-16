# NEXT ACTION — Phase 4 P4.3 Rights and Privacy Review

**Last updated:** 2026-11-17  
**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework  
**Current phase:** Phase 4 — Durable artifact storage and retrieval

## Completed and approved phases

- Phase 0: owner-approved complete.
- Phase 1: owner-approved complete.
- Phase 2: owner-approved complete.
- Phase 3: completed and checkpointed.
- Phase 4 P4.1: storage feasibility assessment complete.
- Phase 4 P4.2: provisional large-artifact classification and storage map committed.

Do not reopen Phases 0–3 without a specific evidence-based reason.

## Immediate next task — P4.3 Step 1: read-only ZIP metadata inspection

A local read-only inspector has been added at `scripts/storage/inspect_large_archives.py` (commit `a97250ba08ad4459e1eb6d527611513e4c9d5748`). It reads the local `.local/source_roots.local.yml` plus the tracked large-file inventory, groups ZIP records by their already-registered SHA-256, and inspects one representative of each unique archive. It reads ZIP central-directory metadata only; it does not extract files, read file payloads, modify archives, or recompute hashes.

### Run locally

From the canonical repository root in PowerShell:

```powershell
git pull --ff-only origin main
python scripts/storage/inspect_large_archives.py
```

Expected local-only output directory: `.local/phase4_archive_inspection/` containing:

- `archive_summary.csv`
- `archive_entries.csv`
- `inspection_summary.json`

The output can contain internal filenames. Keep it local until reviewed; do not commit it directly. Share the three generated outputs in this conversation for review, but do not include file contents or secret values.

If Python is not available as `python`, use the Python interpreter already used for the ML CP scripts.

## Immediate next task — P4.3 Step 2: rights, privacy, and content review

After the metadata listing is reviewed, continue rights/privacy assessment for the 41 large-file records using:

1. `reports/storage/large_file_classification.csv`
2. `reports/inventory/large_files.csv`
3. `reports/inventory/artifact_inventory.csv`
4. `manifests/storage_map.yml`
5. `docs/phase_reports/PHASE_04_P4_2_CLASSIFICATION.md`

### Required review

- Identify the upstream source and applicable licence/terms for the source documents and datasets represented in each relevant archive.
- Establish whether trained adapters and checkpoints can be stored privately and whether redistribution is permitted.
- Inspect archive file listings and manifests without extracting over or modifying any source location.
- Check for credentials, `.env` files, personal data, restricted datasets, and third-party content. Never copy secret values into reports or Git.
- Inspect the reproducibility package before deciding whether it is a single archival object or should be separated into approved components.
- Record unknown or unverifiable rights as `unknown`; do not infer permission from public availability or project ownership.

### P4.3 outputs

- Update per-artifact rights and sensitivity fields in the classification/storage records.
- Record evidence and unresolved items in a P4.3 report.
- Keep the Drive remote private and restricted.
- Do not upload, move, delete, rename, extract over, or rewrite source artifacts.
- Do not select a canonical B2–B5 adapter/checkpoint without experiment-lineage evidence.

## Current storage decision

- Primary artifact storage: DVC + restricted Google Drive folder.
- GitHub: code, safe manifests, reports, and DVC metadata only.
- New bulk Git LFS tracking: disabled under the zero-additional-spend constraint.
- The owner reported 5 TB available in Google Drive and confirmed a dedicated folder can be created.
- GitHub LFS usage was reported as 7/10; whether this is storage or bandwidth usage remains unconfirmed.
- The storage map is provisional and explicitly sets `migration_authorized: false`.

## Migration gate

Do not install/configure DVC or migrate source artifacts until:

1. Rights and privacy review is recorded.
2. Archive contents and reproducibility-package composition are understood.
3. The storage map has an explicit per-artifact decision and is approved.
4. The private Drive destination and credential-handling approach are documented.
5. Backup/recovery status is recorded honestly; an independent physical backup has not been verified.

## Preservation constraints

- Preserve all original source copies and paths.
- Matching SHA-256 values establish byte identity only; they do not authorize deletion or consolidation.
- Do not use `git add .`.
- Do not commit credentials, secrets, local absolute paths, or large artifact contents to the public GitHub repository.
- Use bounded, risk-based validation; do not repeat completed Phase 0–3 audits.
