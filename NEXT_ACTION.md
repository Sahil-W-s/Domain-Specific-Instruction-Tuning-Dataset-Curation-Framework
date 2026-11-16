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


## P4.3 Step 3C — local evaluation and dataset provenance reconciliation

Completed from existing owner-supplied local inspection records:

- Held-out IoT test: 35 records, SHA-256 `70d07aa68b4e125dd573ba01367f059b550651e5e25d4e271e92f55f04c6ff5d`; inspected rows identify `doc_id: iot_unit5_pdf`, `split: test`, and slide-based source IDs/evidence. This reconciles the supplied Unit 5 PDF as the documented held-out source. Keep Unit 5 evaluation-only; it is absent from the four-row training manifest.
- Dolly: local records identify `databricks/databricks-dolly-15k`, 15,011 available rows, seed 20261114, B2 1,000, B5 general 577, and recorded B2/B5 disjointness. Source/category/assignment metadata is present. Immutable upstream revision and exact source-row selection are not recorded.
- MMLU: local manifest identifies `cais/mmlu`, test split, 50 questions, seed 42, 9 excluded original indices, category allocation 13/12/13/12, and local sample SHA-256 `d7c4f24f3ea17f698b0729093ef601cbdf1ecea53623e62844faa4013f2bf78e`. Immutable upstream revision/commit is not recorded.

Report: `docs/phase_reports/PHASE_04_P4_3_SOURCE_RIGHTS_REVIEW.md`.

### Next bounded task

Inspect only the small package metadata/configuration files already identified in the reproducibility package: split manifest, phase3 validation report, and B2–B5 run metadata. Confirm dataset-to-run linkage and any recorded upstream revision identifiers. Do not inspect model/data payloads or extract archives. If the local files contain no immutable revision identifiers, record that gap and stop rather than searching the internet.

Rights and privacy review remain open. Do not configure DVC or migrate artifacts.


### Dolly sampling code finding

The local `prepare_phase3_datasets_v2.py` sets dataset ID `databricks/databricks-dolly-15k`, seed 20261114, loads the train split without a pinned `revision`, shuffles row indices, assigns first 1,000 to B2 and next 577 to B5 general, and asserts disjointness. The script does not persist selected upstream row indices. Exact historical Dolly row selection is therefore not fully reproducible without the upstream snapshot and row-index manifest. The script was inspected, not executed.

Next owner input: upload the existing small package metadata files `configuration/split_manifest.json`, `configuration/phase3_validation_report.json`, and `training/B2/run_metadata.json` through `training/B5/run_metadata.json` (six files total). Review only their metadata for dataset-to-run linkage and revision identifiers. Do not upload dataset/model payloads or extract archives.


## P4.3 Step 3D — package metadata review completed (2026-11-17)

The owner supplied all six requested files. They were inspected locally and their SHA-256 values and findings are recorded in `docs/phase_reports/PHASE_04_P4_3_SOURCE_RIGHTS_REVIEW.md`.

- Dataset preparation report: PASS; B3 600 and B4 577 evidence reconstructions; 0 mismatches; source hashes unchanged; frozen sources not modified.
- Split manifest: seed 42, validation ratio 0.1; 58 shared IoT validation IDs, 519 shared IoT training IDs, 23 B3-only training IDs. B3 train count reconciles as 519+23=542.
- B2–B5 run metadata baseline names/counts match the package README and split manifest. All use the same Qwen2.5-1.5B-Instruct model identifier and common LoRA/training configuration.
- Run metadata does not record dataset input paths/hashes, selected source row IDs, or immutable base-model revision. Dataset-to-run linkage is count/name-level, not hash-bound.
- Dolly upstream revision and row-level source selection remain unknown; MMLU upstream revision remains unknown.
- The run metadata and split manifest do not resolve redistribution rights or payload privacy.

This supersedes the earlier request to upload these six files; no further upload of them is needed.

### Next bounded task — P4.3 Step 3E

Continue source-first rights/provenance review using only existing local evidence. The remaining useful evidence is any locally held source/acquisition record, licence/terms file, course/institution permission, dataset card or cached metadata, and model card/configuration that was part of the original project materials. Do not web-search substitutes. If no such local evidence exists, record the rights as unknown rather than trying to infer them.

Do not inspect bulk dataset/model payloads, configure DVC, or migrate artifacts. `migration_authorized: false` remains in force.


## Owner rights declaration and third-party source boundary — 2026-11-17

The owner explicitly declares that rights to the project materials they created or supplied are theirs and that those materials are open source. The declaration scope is limited to the supplied/project materials: IoT PDFs, generated datasets, scripts, adapters, and reports. It is recorded in `docs/phase_reports/OWNER_RIGHTS_AND_THIRD_PARTY_SCOPE_DECLARATION.md`.

The owner declaration does not cover third-party sources, including Dolly, MMLU, and the Qwen base model. The project will not redistribute third-party source dataset or base-model payloads; users who need those sources are expected to obtain them independently and comply with the terms applicable to their versions. Their repository identifiers may remain in dependency/provenance documentation. Existing immutable-revision gaps remain.

The declaration is recorded as owner-provided, not independent legal verification. No specific standard open-source licence identifier was provided; do not invent one. Record the exact licence notice if a formal public licence grant is to be made. Privacy/secrets review remains separate and pending. The declaration does not authorize source moves/deletions or artifact migration; `manifests/storage_map.yml` remains `migration_authorized: false`.

### Next bounded task

Continue the remaining risk-based privacy/secrets review and per-artifact storage decisions. Do not re-open source-rights discovery for third-party payloads that the project will not redistribute. Preserve third-party dependencies as independently acquired requirements and keep their exact revisions marked unknown where local records do not establish them.


## Phase 4 P4.4 — Privacy review, work unit 1 (2026-11-17)

Implemented and checkpointed `scripts/storage/scan_privacy_indicators.py`. This is a read-only local scan over inventory-listed text-like files only. It checks private-key headers, common cloud/GitHub/Google API-key formats, generic secret assignments, email addresses, and phone-like strings. It never writes matched values or source lines; it records only artifact/root IDs, relative paths, line numbers, indicator categories, and short one-way fingerprints.

Default limits: 25 MiB per file and 2 GiB total. ZIP/archive payloads, PDFs, model weights, images, binary files, and oversized files are excluded. Outputs are local-only under `.local/phase4_privacy_review/`; do not commit or paste secret values.

Report: `docs/phase_reports/PHASE_04_P4_4_PRIVACY_REVIEW.md`.

### Immediate next action

After `git pull --ff-only origin main`, run:

```powershell
python scripts/storage/scan_privacy_indicators.py
```

Return `privacy_scan_summary.json` and sanitized rows from `privacy_indicator_findings.csv` (no matched values). No scan has yet been executed, so no findings are claimed. This scan is only an indicator pass, not comprehensive privacy clearance.

Migration remains unauthorized. Do not configure DVC, upload artifacts, or change source locations during this task.


## P4.4 first scan result — 2026-11-17

Owner ran the bounded scanner successfully. It processed 1,253 unique text-like files (369,784,161 bytes) from 1,286 text-extension candidates among 1,531 inventory records. It reported 87,508 indicators, all in the broad `phone_like` category; no credential/private-key/email indicators were reported. 245 non-text records were excluded; 31 source records were unavailable and 2 failed path/size validation.

The phone-like regex is a broad numeric heuristic. Its count is not a count of phone numbers or confirmed personal-data exposures; numeric IDs, timestamps, and ordinary dataset fields may trigger it. Do not classify these as confirmed PII without local contextual review.

Report: `docs/phase_reports/PHASE_04_P4_4_PRIVACY_REVIEW.md`.

### Immediate next task

Aggregate `.local/phase4_privacy_review/privacy_indicator_findings.csv` by artifact ID and relative path, without printing or sharing matched values. Triage only the highest-concentration files. Also identify the 31 unavailable and 2 path/size-mismatch records from the local inventory/root configuration. Do not rerun the full scan or inspect unrelated payloads.

Migration remains unauthorized. Keep all source paths/copies and the storage map unchanged.
