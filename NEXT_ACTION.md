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

## Completed — P4.3 Step 1: ZIP metadata inspection

The owner ran `scripts/storage/inspect_large_archives.py` locally and supplied all three outputs for review.

- 17 ZIP inventory records grouped into 9 unique SHA-256 content groups.
- All 9 unique archives metadata-listed successfully.
- 115 entry-metadata records; no inspection errors.
- Filename/structure flags: 0 license/notice matches, 9 README entries, 0 manifest/config matches, 0 potentially sensitive filename matches, 0 encrypted entries, 0 unsafe paths, and 0 symlinks.
- Safety summary: no extraction, no entry-payload reads, no source archive modifications, and no new source hashes.
- Review report: `docs/phase_reports/PHASE_04_P4_3_ZIP_METADATA_REVIEW.md`.

Interpretation: zero filename flags do not establish that contents are free of secrets/personal data or that redistribution is permitted. README contents and upstream licensing evidence remain unreviewed. Rights and sensitivity remain unknown; `manifests/storage_map.yml` remains `migration_authorized: false`.

## Completed — P4.3 Step 2: bounded README-content review

The owner ran `scripts/storage/inspect_archive_readmes.py` and supplied the local-only outputs for review.

- 17 ZIP inventory records; 9 unique archive groups.
- 9 archives opened; 9 README entries read; 0 skipped by the 64 KiB limit; 0 errors.
- Only README-named entries were read. No extraction, source archive modification, or new source hashing occurred.
- Review report: `docs/phase_reports/PHASE_04_P4_3_README_REVIEW.md`.
- Adapter model-card READMEs identify Qwen/Qwen2.5-1.5B-Instruct and PEFT/LoRA, but leave licence and provenance fields as `[More Information Needed]`.
- The reproducibility README describes code, datasets, adapters, predictions, evaluation outputs, and provenance artifacts. It does not establish item-level licences or redistribution permission.
- Evaluation caveats from the package README are recorded in the report and must remain attached to future comparisons.

Rights, redistribution, and sensitivity remain unknown. README review is not a payload-wide privacy clearance. Do not commit local README output.

## Immediate next task — P4.3 Step 3: source-specific rights and provenance checks

Use the package's already inventoried manifests and provenance artifacts to identify the exact source families represented in the included datasets and source documents. For each identifiable source family and the named base model:

1. Record the exact upstream source and applicable licence/terms, with evidence.
2. Determine whether terms permit local/private storage, derivative model training, and redistribution; distinguish these permissions rather than treating them as equivalent.
3. Identify dataset and source-document provenance gaps.
4. Record unknown where evidence is missing or ambiguous.
5. Identify payload classes that require privacy review before storage migration; do not inspect unrelated payloads or expose secrets.

Do not infer permission from public availability, a model identifier, or an incomplete model card. Do not publish adapters, datasets, predictions, or source documents. Do not configure DVC or migrate artifacts.

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
