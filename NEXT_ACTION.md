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

## Completed partially — P4.3 Step 3: source-specific rights and provenance checks

Report: docs/phase_reports/PHASE_04_P4_3_SOURCE_RIGHTS_REVIEW.md.

Verified upstream terms from the identified source records:
- Qwen/Qwen2.5-1.5B-Instruct: Apache-2.0.
- Candidate databricks/databricks-dolly-15k: CC BY-SA 3.0; exact revision and subset lineage still unverified.
- cais/mmlu: MIT; exact revision/split and the 50-question sample manifest still unverified.
- Four IoT source PDFs are identified by title, but author, publisher, original source URL, edition, and licence remain unknown.

The review distinguishes private storage, training/evaluation use, and redistribution. It does not grant blanket clearance. Adapter share-alike/derivative-work treatment remains unresolved. All 41 large-artifact records remain on hold; migration remains unauthorized.

## Immediate next task — P4.3 Step 3B: exact package manifest and source provenance reconciliation

Obtain the existing metadata-only ZIP entry listing for the reproducibility package and inspect only the small provenance/configuration metadata needed to establish:
1. Exact Dolly source revision and the subset/row transformation for B2 and B5.
2. Exact MMLU revision, split, sample IDs, and sampling seed for the 50-question retention set.
3. The package's split manifest, dataset validation report, run manifest, and SHA256SUMS metadata.
4. The source/acquisition records and copyright/licence notices for the four IoT PDFs.

Do not read dataset/model payloads, extract the archive, expose secrets, or infer rights where evidence is absent. If the existing metadata-only listing is not available, rerun only the bounded metadata export for the reproducibility archive.

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


## P4.3 Step 3B update — owner-supplied original IoT PDFs reviewed

The owner uploaded the four original PDFs identified in the master inventory. A bounded inspection of their opening pages, extracted text, and basic PDF metadata is recorded in `docs/phase_reports/PHASE_04_P4_3_SOURCE_RIGHTS_REVIEW.md`.

- The four documents are identifiable by their visible Unit I, Unit II, Unit 4, and IoT cloud/case-study titles.
- The inspected text and basic metadata did not establish author, publisher, original acquisition URL, edition, copyright notice, licence, or permission. Treat all such terms as unknown; do not infer rights from possession or from the slide content.
- Existing row provenance maps some B3/B4 records to `iot_unit1`, `iot_unit4_protocols_security`, and `iot_cloud_case_studies`; title-level matches are plausible but do not establish original provenance or reuse rights.
- Held-out evaluation metadata references `iot_unit5_pdf`; that source is not among the four supplied PDFs or the four inventoried titles. Resolve from the owner's records.
- The Unit II PDF's relationship to training/evaluation rows remains unknown.
- Earlier internet licence lookups are not accepted as project-source evidence and must not be treated as clearance. Continue source-first; do not search for substitute copies.

### Immediate owner evidence needed

Upload the existing `source_manifest` spreadsheet visible in the ML CP folder screenshot. Also provide the Unit 5 source PDF or its exact source/acquisition record if it exists under another filename. These are the smallest next inputs needed to reconcile source IDs and the held-out test reference.

Until then, IoT source terms, rights, and redistribution remain unknown; migration remains unauthorized. Do not move, extract, upload, or modify source artifacts.


## P4.3 source-manifest and Unit 5 update — 2026-11-17

The owner supplied `source_manifest(2).csv` and `IOT Unit 5-webofthingsandcloudofthings.pdf`. Both were inspected locally; no internet copies were used.

- The manifest has four rows: `iot_unit1` (151 pages, train, canonical), `iot_unit2` (60 pages, train, eligible), `iot_unit4_protocols_security` (119 pages, train, eligible), and `iot_cloud_case_studies` (99 pages, train, eligible).
- It explicitly says `IOT Unit 1 Contents.pptx.pdf` is a near-duplicate of the canonical Unit 1 PDF and should be excluded from the training source set. Preserve the file; exclusion is not deletion authorization.
- The manifest contains no Unit 5 row. The supplied Unit 5 PDF is 81 pages and its title matches the `iot_unit5_pdf` held-out source identifier at title/topic level. The PDF has no author/title metadata; pages 25–27 display “Jaydeep Patil- AISSMS IOIT Pune”. No licence/copyright/permission was found in the inspected text. Attribution does not establish reuse rights.
- Unit 5 is a plausible match for the held-out source reference, but actual test-set linkage must be verified from the test-generation manifest or row metadata. Do not add Unit 5 to training.

### Immediate next task — reconcile evaluation provenance

Inspect only the existing held-out IoT test manifest and its source-ID metadata to confirm whether its `iot_unit5_pdf` records map to this supplied Unit 5 PDF. Then reconcile the exact Dolly/MMLU revisions and sample selection from project-local manifests/package metadata. If revision identifiers are absent, record them as unknown.

All five PDFs remain rights-uncleared. The source manifest's canonical/eligible statuses are curation statuses, not licence clearance. Keep migration unauthorized; do not configure DVC or move/upload artifacts.
