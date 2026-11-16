# ML CP — Current Project State

**Last updated:** 2026-11-17
**Plan version:** 2.0
**Current phase:** Phase 1 — Discover all project source locations
**Phase status:** Phase 0 partial; Phase 1 completed

## Verified workspace

- Canonical project workspace has an isolated Git repository.
- Branch: master
- Commit count: 0
- Git remotes: none recorded.
- No Git commit or push has been performed.
- Parent repository was inspected and left untouched.

## Source and recovery

- Original source directory: MLCP_SOURCE.
- Original source inventory before excluding .venv: 26,027 files, approximately 714.07 MB.
- .venv contains approximately 25,526 files and is excluded from the 501-file project artifact registry.
- Canonical workspace recovery copy: 7 files, approximately 9.15 MB.
- Source recovery copy previously verified: 26,027 files, 26,027 SHA-256 matches, zero mismatches.
- Both recovery copies are on the same physical SSD. They protect against accidental changes but not physical drive failure.

## Current artifact registry

- Registry:
reports/inventory/known_existing_artifacts.csv
- Records: 501
- Unique paths: 501
- SHA-256 values: 501
- Blank hashes: 0
- Hash errors: 0
- Reverification: 501 exact size and SHA-256 matches, zero mismatches.
- Canonical registry SHA-256: BB7C79DD7E254DB600BB6413F053D9142FF4B7403729CFB07338DE90D1B593C7
- Recovery registry hash: BB7C79DD7E254DB600BB6413F053D9142FF4B7403729CFB07338DE90D1B593C7
- Recovery registry status: MATCH.
- Sensitive .env record: 1.
- Zero-byte files retained: 3.

## Archive verification

- data/interim.zip: 348 entries, 327 readable files, 21 directories, zero errors.
- data/phase3.zip: 8 entries, 7 readable files, 1 directory, zero errors.
- Both archive entry sets were read to their declared uncompressed sizes.
- Archive hashes and entry verification are recorded in the recovery inventory.

## Historical inventory comparison

- 492 historical project audit entries match current path and size.
- 9 current-only entries.
- 0 historical-only entries.
- 0 size changes.
- The six current-only Python bytecode files are generated cache.
- Three current-only reports are audit/discovery artifacts.

## Classification corrections

- Generation checkpoint JSON records are not trained model weights.
- Production batch checkpoints are separately classified.
- model_weight_candidates.csv is an archive candidate listing.
- Temporary JSONL output is not considered final.
- Execution logs and generated Python cache have separate classifications.

## Known limitations and pending work

1. Recovery is on the same physical SSD, not an independent physical device.
2. The master implementation plan's local copy and SHA-256 registration remain pending.
3. The original project guide/reference must be located and registered if distinct from the master plan.
4. Full source-location discovery has not started.
5. No large-file storage decision has been made.
6. No DVC, Git LFS, cloud storage, or data migration has been configured.
7. Historical evaluation and dataset claims have not all been independently reproduced.

## Git checkpoint

No commit has been created. The phase documentation will remain uncommitted until reviewed and approved.


## Verified status update — 2026-11-17

This section supersedes conflicting historical statements above where noted.
Earlier entries are retained as historical records, not current repository state.

### Current Git workspace

- Repository branch: `main`.
- Latest verified commit: `5268229` — `Complete Phase 0 project preservation and documentation`.
- Remote tracking: `origin/main`.
- Phase 1 inventory and documentation artifacts are currently uncommitted.
- No files have been staged or committed as part of this update.

### Phase 1 — completed technical work

- Seven owner-confirmed source roots scanned across three batches.
- Consolidated inventory: 1,498 file records.
- Archive records: 28.
- Files at least 50 MB: 41.
- Historical master inventory: 26,015 records accounted for by 489 present and 25,526 `.venv` exclusions.
- Historical missing paths: zero.
- Historical size mismatches: zero.
- Same-size duplicate candidates: 124.
- Targeted SHA-256 verification: 136 valid hashes, zero unresolved records.
- Confirmed duplicate groups: 31, containing 110 files.
- Theoretical redundant storage: 1,779,256,777 bytes. This is not deletion authorization.
- Phase 1 validation: 19/19 checks passed.

### Phase 1 deliverables

- `docs/phase_reports/PHASE_01_REPORT.md`
- `manifests/phase_01_outputs.json`
- `reports/validation/phase_01_validation.json`
- Supporting scan, consolidation, reconciliation and hash evidence in `reports/inventory/`.

### Phase 0 remains partial

The following blockers remain unresolved:

1. Local SHA-256 registration of the master implementation plan.
2. Identification and registration of a separate original project guide, if one exists.
3. Verification of an independent physical backup destination.

The seven-root source discovery was executed before those Phase 0 blockers were closed. This sequencing deviation is documented rather than concealed.

### Preservation status

No source files were moved, deleted, extracted, or consolidated. No duplicate removal is authorized. The inventory scope is the seven roots confirmed by the owner and is not independently exhaustive.


## Authoritative current status — Phase 2

**Updated:** 2026-11-17  
**Current phase:** Phase 2 — Build the content-aware artifact registry and large-file map  
**Phase 0:** Owner-approved complete  
**Phase 1:** Owner-approved complete  
**Phase 2:** Technical deliverables generated and validated; owner review pending

This section supersedes earlier status statements in this file where they conflict.
Earlier entries are retained as historical records.

### Git checkpoint

- Branch: `main`.
- Latest verified commit: `50b9f3054fa0d3ba99c56e97450d918e63a9e2ba`.
- Commit message: `Complete Phase 1 source discovery and reconciliation`.
- Remote: `origin`.
- Phase 2 files and supporting evidence are untracked.
- No Phase 2 files have been staged, committed, or pushed.

### Phase 0 and Phase 1

- Phase 0 and Phase 1 are complete by owner approval.
- Phase 1 covered the seven owner-confirmed source roots.
- Historical reconciliation was path-and-size based.
- SHA-256 verification was targeted, not exhaustive.
- No source files were moved, deleted, or extracted.
- Previously recorded caveats concerning the independent physical backup destination, original guide identification, and master-plan hash registration remain historical caveats. They do not reopen the approved phases.

### Phase 2 — registry and inventory results

- Registry: `manifests/artifact_registry.jsonl`.
- Schema: `manifests/artifact_registry.schema.json`.
- Registry records: 1,531; unique artifact IDs: 1,531.
- Schema validation: 1,531 valid records, zero invalid.
- Hash status: 1,496 verified; 2 not applicable; 33 historical failed records.
- All 33 historical failed records have verified replacement records; zero unresolved.
- Independent SHA-256 sample recomputation: 15/15 passed. This is a sample, not exhaustive independent rehashing of all verified records.
- Canonical artifact inventory: 1,531 rows, exact registry match.
- Large-file report: 41 files at or above 50 MiB, exact registry coverage.
- Exact duplicate report: 564 groups, 1,373 artifact memberships; exact registry membership validation passed.
- Possible-duplicate review: 11 groups, 138 candidate records. All remain `pending_manual_review`; they are not confirmed duplicates.
- Hash-failure report: 33 historical superseded records, zero unresolved.
- Phase 2 report: `docs/phase_reports/PHASE_02_REPORT.md`.

### Phase 2 deliverables

- `manifests/artifact_registry.schema.json`
- `manifests/artifact_registry.jsonl`
- `reports/inventory/artifact_inventory.csv`
- `reports/inventory/exact_duplicates.csv`
- `reports/inventory/possible_duplicates_review.csv`
- `reports/inventory/large_files.csv`
- `reports/inventory/hash_failures.csv`
- `docs/phase_reports/PHASE_02_REPORT.md`
- Builder: `scripts/build_phase2_deliverables.py`

### Phase 2 limitations and safeguards

- Possible duplicates require manual review; no duplicate files were deleted.
- Historical failed registry records remain preserved for auditability.
- Independent SHA-256 recomputation was targeted to a 15-file sample, not exhaustive.
- Phase 1's 1,498 initial inventory records plus 33 corrected-path replacement records account for the 1,531 registry records.
- No source files were moved, deleted, renamed, or extracted.
- No DVC, Git LFS, cloud storage, or data migration was configured.
- Phase 2 is not marked complete until the owner reviews the exit gate and approves completion.

## Authoritative current status — Phase 3

**Updated:** 2026-11-16
**Current phase:** Phase 3 — Durable workspace and project memory
**Phase 0:** Owner-approved complete
**Phase 1:** Owner-approved complete
**Phase 2:** Owner-approved complete
**Phase 3:** Technical implementation complete; owner review pending

Phase 3 report: `docs/phase_reports/PHASE_03_REPORT.md`
Validation: `reports/validation/phase_03_validation.json`
Outputs: `manifests/phase_03_outputs.json`

Five focused integration tests passed. The SQLite index contains 1,531
registry records and 1,531 FTS5 records. The index is rebuildable and ignored
by Git. Full JSON Schema instance validation was not performed.

Phase 1 limitations and Phase 2 duplicate-review and targeted-hash caveats
remain unchanged. No source data was moved or deleted.


## Authoritative current status — Phase 4 P4.2

**Updated:** 2026-11-17  
**Current phase:** Phase 4 — Durable artifact storage and retrieval  
**Phase 0:** Owner-approved complete  
**Phase 1:** Owner-approved complete  
**Phase 2:** Owner-approved complete  
**Phase 3:** Completed and checkpointed  
**Phase 4:** P4.1 feasibility assessment complete; P4.2 large-artifact classification complete; P4.3 rights/privacy review is next.

This section is the latest status and supersedes older status blocks above where they conflict. Historical caveats remain preserved.

### P4.1 — Storage feasibility

- Owner-reported Google Drive available capacity: 5 TB.
- Owner-reported GitHub LFS usage/quota: 7/10; exact interpretation (storage versus bandwidth) remains to be clarified.
- Additional LFS spending: zero.
- Dedicated Google Drive folder: owner confirmed it can be created.
- Selected architecture: DVC with a restricted dedicated Google Drive remote as primary large-artifact storage; GitHub for code, safe manifests, reports, and DVC metadata.
- No new bulk Git LFS tracking.

### P4.2 — Large-artifact classification

- Source: `reports/inventory/large_files.csv`, cross-matched to `reports/inventory/artifact_inventory.csv`.
- 41/41 records matched; all 41 have verified SHA-256 values.
- 17 archives and 24 adapter/model files.
- Provisional roles: 8 experiment backup ZIPs, 8 adapter backup ZIPs, 1 reproducibility-package ZIP, 4 active-run final adapters, 8 final-adapter backup copies, 12 adapter checkpoints.
- 21 unique SHA-256 contents and 8 duplicate-hash groups within this 41-record subset.
- Physical bytes across records: 3,186,397,696.
- Unique content bytes: 1,735,016,404.
- Duplicate replica overhead: 1,451,381,292 bytes.
- Every record currently has `sensitivity=unknown` and `redistribution_status=unknown` in the registry.
- No canonical model/checkpoint has been selected.

### Phase 4 artifacts committed

- `reports/storage/large_file_classification.csv`
- `manifests/storage_map.yml` — provisional; migration explicitly unauthorized.
- `docs/phase_reports/PHASE_04_P4_2_CLASSIFICATION.md`
- `DECISIONS.md` — appended D-012 recording the storage architecture and migration hold.

Latest checkpoint at the time of this update: `a43949a509778e75d78421ab21e0c5bf401fd04c`.

### Safety and migration status

- No source artifacts were moved, deleted, renamed, uploaded, or rewritten.
- Preserve every source path and copy. Matching hashes do not authorize deletion.
- The Drive destination must remain private/restricted until rights and privacy review is complete.
- No DVC installation, remote configuration, LFS tracking, or artifact migration has started.
- An independent physical backup has not been verified. Historical Phase 0 risk acceptance does not prove an independent backup exists.

### Next task

P4.3 — Review rights, privacy, redistribution terms, and archive contents. Keep all migration actions blocked until this review is recorded and the storage map is approved.


### P4.3 Step 1 — Read-only archive inspection tooling

- Added `scripts/storage/inspect_large_archives.py`.
- Script uses the local ignored `.local/source_roots.local.yml` and tracked Phase 2 large-file inventory.
- It groups ZIP records by their existing SHA-256 and inspects one representative for each unique ZIP content.
- Inspection is ZIP central-directory metadata only: no extraction, no payload reads, no source modification, and no new hashing.
- Local output directory: `.local/phase4_archive_inspection/`.
- Expected outputs: `archive_summary.csv`, `archive_entries.csv`, and `inspection_summary.json`.
- Tooling checkpoint: `a97250ba08ad4459e1eb6d527611513e4c9d5748`.
- Execution and review of generated local outputs are pending; P4.3 is not complete.


## Authoritative current status — Phase 4 P4.3 ZIP metadata review

**Updated:** 2026-11-17  
**Current task:** P4.3 Step 2 — bounded README-content review.

This section supersedes earlier Phase 4 status blocks above where they conflict. Historical records and caveats remain preserved.

### P4.3 Step 1 results

- Script: `scripts/storage/inspect_large_archives.py`.
- 17 ZIP inventory records grouped into 9 unique SHA-256 content groups.
- All 9 unique archives metadata-listed successfully; 115 entry-metadata records; zero inspection errors.
- Filename/structure checks: 0 license/notice matches, 9 README entries, 0 manifest/config matches, 0 potentially sensitive filename matches, 0 encrypted entries, 0 unsafe paths, and 0 symlinks.
- Safety: no extraction, no entry-payload reads, no source archive modification, and no new source hashes.
- Review report: `docs/phase_reports/PHASE_04_P4_3_ZIP_METADATA_REVIEW.md`.

### Interpretation

Zero filename-level flags do not establish absence of private data/secrets or permission to redistribute. README contents and upstream source terms remain unreviewed. Rights, redistribution, and sensitivity remain unknown for all affected artifacts. No canonical B2–B5 adapter/checkpoint has been selected.

### Current restrictions

- `manifests/storage_map.yml` remains `migration_authorized: false`.
- No DVC setup or artifact migration.
- Preserve all original paths and copies; no source artifact may be moved, deleted, renamed, overwritten, extracted over, or uploaded.
- Do not publish local inspection outputs; they may contain internal filenames or README content.

### Next action

Run `python scripts/storage/inspect_archive_readmes.py` after pulling `origin/main`. The bounded script reads only README-named entries up to 64 KiB each and writes local-only outputs to `.local/phase4_archive_inspection/`: `archive_readmes_local.md` and `readme_inspection_summary.json`. Review locally for sensitive content before sharing. P4.3 remains in progress.
