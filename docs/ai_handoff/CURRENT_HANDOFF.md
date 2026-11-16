# ML CP — Current AI Handoff

**Date:** 2026-11-17
**Plan:** ML_CP_Resilient_Implementation_Plan.md, version 2.0
**Active work:** Phase 0 closeout blockers and Phase 1 owner review
**Status:** Phase 0 partial; Phase 1 completed

## Project identity

ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework.

The work has two connected tracks:
1. Dataset engineering: source processing, extraction, chunking, generation, evidence validation, filtering, judging, repair, and dataset assembly.
2. Model experimentation: B0–B5 experiments, training, adapters, predictions, and evaluation.

## Canonical locations

The owner confirmed the canonical workspace as `Domain-Specific-Instruction-Tuning-Dataset-Curation-Framework`.

The original `ML CP` directory is the substantive source and remains separate. Do not merge or reorganize it during discovery.

Actual local paths are stored in the ignored `.local/phase_00_local_paths.txt`.

## Completed and verified

### Recovery

- Original source backup: 26,027 files, 714.07 MB.
- Source backup SHA-256 verification: 26,027 matches, zero mismatches.
- Canonical workspace backup: 7 files, approximately 9.15 MB.
- Both backups are on the same physical SSD; not an independent disaster-recovery copy.

### Git

- Isolated Git repository initialized in canonical workspace.
- Current branch: `main`.
- Latest verified commit: `5268229`.
- Remote tracking: `origin/main`.
- Phase 1 artifacts are uncommitted and require owner review.

### Artifact registry

- `reports/inventory/known_existing_artifacts.csv`
- 501 unique files, `.venv` excluded.
- 501 SHA-256 values.
- 501 source re-verification matches, zero mismatches.
- Canonical and recovery registry SHA-256:
  `BB7C79DD7E254DB600BB6413F053D9142FF4B7403729CFB07338DE90D1B593C7`
- One sensitive `.env` record; do not expose its contents.
- Three zero-byte JSONL records retained for review.

### Historical inventory comparison

- 492 historical path-and-size matches.
- 9 current-only entries.
- 0 historical-only entries.
- 0 size changes.

### Archive verification

- `data/interim.zip`: 327 readable files, 21 directories, zero errors.
- `data/phase3.zip`: 7 readable files, 1 directory, zero errors.
- ZIP manifest and summary are in the recovery inventory directory.

### Classification corrections

- Generation checkpoint JSON files are workflow state, not trained model weights.
- Production batch checkpoints are separately classified.
- `model_weight_candidates.csv` lists ZIP archives.
- `.jsonl.tmp` is temporary dataset output.
- `.pyc` files are generated cache.
- Three zero-byte JSONL files remain registered.

## Pending

1. Register the local copy and SHA-256 of the master implementation plan.
2. Determine whether a separate original project guide exists and register it.
3. Identify an independent physical backup destination or record that none is currently available.
4. Complete Phase 0 closeout and validate this handoff in a fresh session.

## Do not do next

- Phase 1 discovery has been executed and validated. Do not repeat scans unless evidence is missing or a specific discrepancy is found.
- Do not move, delete, rename, or reorganize source material.
- Do not install DVC or configure storage.
- Do not run training, inference, or paid API calls.
- Do not stage or commit files without owner review.

## First action in a new conversation

Read `AI_WORK_PROTOCOL.md`, `docs/ai_handoff/AI_START_HERE.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`, `NEXT_ACTION.md`, and this handoff. Then continue only with the task in `NEXT_ACTION.md`.


## Verified continuation update — 2026-11-17

### Phase 1 result

Phase 1 — Discover all project source locations — has completed its technical work.

- Seven owner-confirmed source roots.
- Three scan batches.
- 1,498 consolidated file records.
- 28 archive records.
- 41 files at least 50 MB.
- Historical master coverage: 26,015 records accounted for; zero missing paths and zero size mismatches.
- 136 targeted SHA-256 records successfully verified.
- 31 confirmed duplicate groups containing 110 files.
- 19/19 Phase 1 validation checks passed.

Read these files first when continuing:

1. `docs/phase_reports/PHASE_01_REPORT.md`
2. `manifests/phase_01_outputs.json`
3. `reports/validation/phase_01_validation.json`
4. `state/phase_status.yml`
5. `NEXT_ACTION.md`

### Phase 0 blockers remain

1. Master implementation plan local SHA-256 registration.
2. Separate original project guide identification.
3. Independent physical backup destination verification.

Do not mark Phase 0 complete without evidence for these items.

### Repository checkpoint

- Branch: `main`.
- Latest verified commit: `5268229`.
- Remote: `origin/main`.
- New Phase 1 and state-update artifacts have not been committed.
- The state-update backup copies are in `reports/state_update_backups/`.

### Preservation constraints

Do not delete or move source files, extract archives, or remove duplicate copies. The seven-root scope is owner-confirmed, not independently exhaustive. The next action is Phase 1 owner review and Phase 0 closeout as specified in `NEXT_ACTION.md`.


## Authoritative continuation — Phase 2 owner review

**Updated:** 2026-11-17  
**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework  
**Current work:** Phase 2 owner review  
**Status:** Phase 0 and Phase 1 owner-approved complete; Phase 2 deliverables generated and validated, owner review pending.

This section supersedes earlier handoff statements where they conflict. Earlier entries are retained as historical records.

### Current Git checkpoint

- Branch: `main`.
- Latest verified commit: `50b9f3054fa0d3ba99c56e97450d918e63a9e2ba`.
- Remote: `origin`.
- Phase 2 outputs and supporting evidence are untracked.
- No Phase 2 files have been staged, committed, or pushed.

### Phase status

- Phase 0: completed by owner approval.
- Phase 1: completed by owner approval.
- Phase 2: technical deliverables generated and validated; owner review pending.

Do not reopen Phases 0 or 1 unless requested by the owner or new evidence requires it.

### Phase 2 verified results

- Registry: 1,531 records and 1,531 unique artifact IDs.
- Schema validation: 1,531 valid, zero invalid.
- Hash statuses: 1,496 verified, 2 not applicable, 33 historical failed.
- All 33 historical failed records have verified replacement records; zero unresolved.
- Independent SHA-256 sample recomputation: 15/15 passed; not exhaustive.
- Artifact inventory: 1,531 rows, exact registry match.
- Large-file report: 41 rows, exact coverage for files at or above 50 MiB.
- Exact duplicates: 564 groups, 1,373 memberships, exact registry match.
- Possible duplicates: 11 groups, 138 candidates, all `pending_manual_review`.
- Phase 2 report: `docs/phase_reports/PHASE_02_REPORT.md`.
- Builder: `scripts/build_phase2_deliverables.py`.

### Important interpretation

The 33 `failed` registry records are preserved historical records, not unresolved operational failures. Each has a verified superseding record. Do not rewrite the historical records.

The 138 possible-duplicate candidates have not been manually adjudicated. They are not confirmed duplicates. No duplicate removal is authorized.

Phase 1's historical reconciliation remains path-and-size based, and its SHA-256 work was targeted rather than exhaustive. No source files were moved, deleted, renamed, or extracted. No DVC, Git LFS, cloud migration, or storage migration has been configured.

### First action in a new conversation

Read `AI_WORK_PROTOCOL.md`, `docs/ai_handoff/AI_START_HERE.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`, `NEXT_ACTION.md`, `state/phase_status.yml`, and this handoff.

Continue with the Phase 2 owner review specified in `NEXT_ACTION.md`. Do not repeat completed phases or commit files without explicit owner approval.


## Authoritative continuation — Phase 4 P4.2 complete

**Updated:** 2026-11-17  
**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework  
**Current task:** P4.3 rights, privacy, redistribution, and archive-content review

This is the latest handoff section and supersedes all earlier continuation instructions above where they conflict. Historical caveats remain preserved.

### Current Git checkpoint

- Repository: `Sahil-W-s/Domain-Specific-Instruction-Tuning-Dataset-Curation-Framework`.
- Branch: `main`.
- Phase 4 classification and decision artifacts were committed through GitHub.
- Latest commit before this handoff update: `a43949a509778e75d78421ab21e0c5bf401fd04c`.

### Phase status

- Phase 0 and Phase 1: owner-approved complete.
- Phase 2: owner-approved complete.
- Phase 3: completed and checkpointed.
- Phase 4 P4.1: feasibility assessment complete.
- Phase 4 P4.2: large-artifact classification complete.
- Phase 4 P4.3: next.

### P4.1 decisions

- Owner-reported 5 TB available in Google Drive.
- Owner-reported GitHub LFS usage/quota 7/10; unclear whether storage or bandwidth.
- Zero additional LFS spending.
- Owner confirmed a dedicated Google Drive folder can be created.
- Preferred architecture: DVC with a restricted Google Drive remote.
- GitHub is for code, safe manifests, reports, and DVC metadata; do not add new bulk LFS artifacts.

### P4.2 verified inventory results

The 41 rows in `reports/inventory/large_files.csv` were cross-matched against the Phase 2 artifact inventory. All 41 matched and have verified SHA-256 values.

- 17 archives and 24 adapter/model files.
- 8 experiment backup ZIP archives.
- 8 adapter backup ZIP archives.
- 1 reproducibility-package ZIP.
- 4 active-run final adapters.
- 8 final-adapter backup copies.
- 12 adapter checkpoint files.
- 21 unique SHA-256 objects and 8 duplicate-hash groups in this large-file subset.
- Physical size across records: 3,186,397,696 bytes.
- Unique content size: 1,735,016,404 bytes.
- Duplicate replica overhead: 1,451,381,292 bytes.

Every one of the 41 records has `sensitivity=unknown` and `redistribution_status=unknown` in the source registry. Do not infer rights or privacy clearance.

### P4.2 committed outputs

- `reports/storage/large_file_classification.csv`
- `manifests/storage_map.yml`
- `docs/phase_reports/PHASE_04_P4_2_CLASSIFICATION.md`
- `DECISIONS.md` appended with D-012.

The storage map is provisional and sets `migration_authorized: false`.

### Next task — P4.3

Review source licences and redistribution terms, inspect archive manifests/file listings without modifying source locations, assess privacy/secrets/third-party content, and record evidence or unresolved status. Do not expose secret values. Do not extract over source files.

Do not install/configure DVC or migrate any source artifact until rights/privacy review and per-artifact storage decisions are approved.

### Preservation rules

- Do not move, delete, rename, or overwrite source artifacts.
- Matching hashes do not establish a canonical copy and do not authorize deletion.
- No artifact migration has started.
- An independent physical backup has not been verified.
- Use the risk-based Phase 3 validation approach; do not repeat completed audits.


### P4.3 Step 1 — Read-only ZIP metadata inspection

- Script: `scripts/storage/inspect_large_archives.py`.
- Tooling commit: `a97250ba08ad4459e1eb6d527611513e4c9d5748`.
- Run from the local repository root after `git pull --ff-only origin main`:
  `python scripts/storage/inspect_large_archives.py`.
- Reads local `.local/source_roots.local.yml` and tracked `reports/inventory/large_files.csv`.
- Groups the 17 ZIP records by their pre-existing SHA-256 and inspects one representative per unique content group.
- Reads central-directory metadata only; does not extract entries, read entry payloads, modify source archives, or recompute hashes.
- Writes local-only outputs to `.local/phase4_archive_inspection/`: `archive_summary.csv`, `archive_entries.csv`, `inspection_summary.json`.
- Execution and inspection of those outputs remain pending. Do not commit generated local outputs before review; internal filenames may be sensitive.


## Authoritative continuation — P4.3 ZIP metadata reviewed

**Updated:** 2026-11-17  
**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework  
**Current task:** P4.3 Step 2 — bounded README-content review.

This is the latest continuation block and supersedes earlier task instructions above where they conflict.

### P4.3 Step 1 evidence

The owner executed `scripts/storage/inspect_large_archives.py` locally and supplied its three generated outputs.

- 17 ZIP records grouped into 9 unique SHA-256 content groups.
- 9/9 unique archive groups metadata-listed successfully.
- 115 entry metadata records; no errors.
- 0 license/notice filename matches.
- 9 README-named entries.
- 0 manifest/config filename matches.
- 0 potentially sensitive filename matches.
- 0 encrypted entries, unsafe paths, or symlinks.
- No extraction, payload reads, source archive modifications, or new source hashes.

Report: `docs/phase_reports/PHASE_04_P4_3_ZIP_METADATA_REVIEW.md`.

### Interpretation

This was metadata-only inspection. It does not establish absence of sensitive content, nor does it establish licence or redistribution permission. README contents and upstream terms remain unreviewed. Rights, redistribution, and sensitivity remain unknown. The storage map must continue to set `migration_authorized: false`.

### Next action

Run after `git pull --ff-only origin main`:

```powershell
python scripts/storage/inspect_archive_readmes.py
```

This bounded script reads only README-named ZIP entries, with a 64 KiB maximum per entry. It does not extract files to disk, read other entry payloads, modify source archives, or compute new hashes.

Local-only outputs in `.local/phase4_archive_inspection/`:

- `archive_readmes_local.md`
- `readme_inspection_summary.json`

The Markdown may contain private project details. Review locally for secrets, personal information, private paths, or restricted material before sharing. Do not commit the outputs to the public repository.

### Preservation and migration gate

- Do not move, delete, rename, overwrite, extract over, or upload source artifacts.
- Do not configure DVC or migrate artifacts.
- Do not select a canonical B2–B5 adapter/checkpoint without experiment-lineage evidence.
- Continue bounded, risk-based validation only.


## Authoritative continuation — P4.3 README review completed

**Updated:** 2026-11-17  
**Current task:** P4.3 Step 3 — source-specific rights and provenance checks.

This is the latest continuation block and supersedes earlier task instructions above where they conflict.

### P4.3 Step 2 evidence

The owner supplied `archive_readmes_local.md` and `readme_inspection_summary.json` generated by `scripts/storage/inspect_archive_readmes.py`.

- 17 ZIP inventory records and 9 unique archive groups.
- 9 archives opened; 9 README entries read; zero skipped by the 64 KiB limit; zero errors.
- Only README-named entries were read. No extraction, source archive modification, or new source hashing occurred.
- Report: `docs/phase_reports/PHASE_04_P4_3_README_REVIEW.md`.

### Findings

- Adapter model-card READMEs identify the base model `Qwen/Qwen2.5-1.5B-Instruct` and PEFT/LoRA but leave licence and key provenance fields incomplete.
- The reproducibility README describes code, datasets, adapters, predictions, evaluation outputs, and provenance artifacts. It does not provide item-level licences or redistribution permission.
- Evaluation caveats are recorded in the P4.3 README report and must be preserved in future comparisons.
- README review does not establish payload-wide privacy clearance. Rights, redistribution, and sensitivity remain unknown.

### Next action — P4.3 Step 3

Use existing package manifests and provenance artifacts to identify upstream sources and terms for the base model and each identifiable dataset/source family. Record separately whether terms permit private storage, derivative training, and redistribution. Retain unknown where evidence is incomplete. Identify payload classes requiring privacy review without exposing secrets or performing broad payload inspection.

### Migration gate

- Keep `manifests/storage_map.yml` at `migration_authorized: false`.
- Do not publish adapters, datasets, predictions, source documents, or archive contents.
- Do not configure DVC or migrate any artifacts.
- Preserve all source paths and copies; no source moves, deletions, renames, overwrites, or extraction over source locations.


## Authoritative continuation — P4.3 partial source-rights review

**Updated:** 2026-11-17  
**Current task:** P4.3 Step 3B — exact package manifest and source provenance reconciliation.

Report: docs/phase_reports/PHASE_04_P4_3_SOURCE_RIGHTS_REVIEW.md.

### Verified source terms and unresolved items

- Base model Qwen/Qwen2.5-1.5B-Instruct: Apache-2.0 on the upstream Hugging Face repository.
- Dolly source candidate databricks/databricks-dolly-15k: CC BY-SA 3.0. Exact revision and B2/B5 subset lineage are not yet verified.
- MMLU source cais/mmlu: MIT. Exact revision, split, 50-question sample IDs, and seed are not yet verified.
- Four original IoT PDF titles are identified in the report. Author, publisher, original URL, edition, and licence remain unknown.
- Whether adapter weights trained on Dolly are adaptations subject to CC BY-SA share-alike remains unresolved.
- Payload privacy review is pending; README and ZIP filename checks are not payload-wide clearance.

### Next bounded action

Use the existing metadata-only ZIP entry listing for the reproducibility package and inspect only the small manifests/configuration files required to establish exact source revisions, subset lineage, sampling manifest, run lineage, and SHA256SUMS metadata. If the entry listing is unavailable, rerun only the bounded metadata export for that package. Do not read dataset/model payloads or extract the archive.

### Migration gate remains closed

- Keep migration_authorized: false.
- No DVC setup or artifact migration.
- No publication of adapters, datasets, predictions, or source documents.
- Preserve every source path and copy; no moves, deletions, renames, overwrites, or extraction over source artifacts.


## 2026-11-17 continuation — original IoT PDFs supplied and reviewed

The owner uploaded the four original IoT PDFs from the project inventory. A bounded inspection of opening pages, extracted text, and basic PDF metadata is recorded in `docs/phase_reports/PHASE_04_P4_3_SOURCE_RIGHTS_REVIEW.md`. Visible titles identify Unit I Introduction to IoT (151 pages), Unit II IoT Platform Design Methodology (60 pages), Unit 4 IoT Protocols and Security (119 pages), and IoT Physical Servers/Cloud Offerings/Case Studies (99 pages). The inspected source text and basic metadata did not establish author, publisher, acquisition URL, edition, copyright notice, licence, or permission. All such rights remain unknown.

Some B3/B4 source IDs have plausible title-level matches to the supplied PDFs, but no original provenance or reuse rights are established. Held-out evaluation refers to `iot_unit5_pdf`, which is not among the four supplied PDFs or four inventoried titles. The Unit II PDF's training/evaluation relationship is also unknown.

Do not use prior external licence lookups as project-source evidence or clearance. Continue source-first with the owner's own records. Next request: upload the existing `source_manifest` spreadsheet and identify/provide the Unit 5 source or its acquisition record. Migration remains unauthorized; do not configure DVC or move/upload source artifacts.


## 2026-11-17 continuation — source manifest and Unit 5 PDF reviewed

Owner supplied `source_manifest(2).csv` and `IOT Unit 5-webofthingsandcloudofthings.pdf`. The manifest contains four training rows: Unit 1 (canonical; the PPTX PDF duplicate is to be excluded), Unit 2 (eligible), Unit 4 protocols/security (eligible), and IoT cloud/case studies (eligible). It contains no Unit 5 row and no author, publisher, acquisition, copyright, or licence fields. These statuses are curation decisions, not rights clearance.

The Unit 5 PDF is 81 pages and its title matches `iot_unit5_pdf` at title/topic level. PDF author/title metadata are blank. Pages 25–27 show the footer “Jaydeep Patil- AISSMS IOIT Pune”; this does not establish a licence or ownership. No explicit copyright/licence/permission text was found in extracted text. It is a plausible match for the held-out source identifier, but its use in the held-out test still needs confirmation from test manifest/row metadata. Do not add Unit 5 to training.

Next: inspect the local held-out IoT test manifest/source IDs, then the exact Dolly/MMLU revision and sampling metadata. Keep rights unknown and migration unauthorized. Preserve all files and paths.
