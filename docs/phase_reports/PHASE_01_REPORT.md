# Phase 1 Report — Source Discovery and Reconciliation

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework
**Execution date:** 2026-11-17
**Phase:** 01 — Discover all project source locations
**Status:** Evidence assembled; final phase closeout pending validation and owner review

## 1. Objective

Discover and inventory the project files across the seven source roots confirmed by the project owner. Preserve source material and establish a traceable inventory, archive register, large-file register, historical reconciliation, and content-hash duplicate analysis.

## 2. Scope

The seven user-confirmed source roots are:

1. MLCP_UPLOAD
2. MLCP_RECOVERY
3. MLCP_REVIEW_SUBSET
4. MLCP_PIPELINE_V1
5. MLCP_GITHUB_STARTER
6. MLCP_PHASE1_DRAFTS
7. MLCP_KAGGLE_WORK

This is the owner's confirmed project scope. It is not an independent proof that no other copies exist anywhere.

## 3. Scan execution

Three scan batches were used:

- `20261117_004111`: MLCP_UPLOAD and MLCP_RECOVERY.
- `20261117_004925`: MLCP_REVIEW_SUBSET, MLCP_PIPELINE_V1, MLCP_GITHUB_STARTER and MLCP_PHASE1_DRAFTS.
- `20261117_011442`: MLCP_KAGGLE_WORK.

The consolidated inventory contains 1,498 file records across seven roots. The scan records include 28 archive files and 41 files at least 50 MB.

The first scan recorded four intentional directory exclusions involving `.git` and `.venv`. These are scan-policy exclusions, not access failures. The later scan batches recorded zero access errors and zero exclusions.

## 4. Historical inventory reconciliation

The historical master inventory contained 26,015 records:

- 489 records were present in the current source comparison.
- 25,526 records were excluded as `.venv` content.
- Zero historical paths were reported missing.
- Zero size mismatches were reported.

This is a path-and-size reconciliation, not a fresh SHA-256 verification of all 26,015 historical records.

## 5. Duplicate analysis

The same-size candidate analysis produced 124 candidate records. A targeted SHA-256 workload covered 136 unique file paths, including archive paths and overlapping candidate paths.

The resolved SHA-256 verification contains 136 valid hashes and zero unresolved hash records.

The duplicate analysis identified:

- 31 confirmed duplicate groups.
- 110 files belonging to duplicate groups.
- 26 files outside those duplicate groups.
- 1,779,256,777 redundant bytes if one copy per group were retained.

The redundant-byte figure is theoretical storage overlap only. It is not authorization to delete or consolidate anything. All source copies remain preserved.

## 6. Preservation and safety

- No source files were deleted or moved.
- No archives were extracted.
- No duplicate copies were removed.
- No model training or inference was performed as part of this inventory.
- The private `.local/source_roots.local.yml` file is excluded from Git.
- The tracked source-root template uses placeholders instead of personal absolute paths.

## 7. Limitations and unresolved items

- The inventory is scoped to the seven owner-confirmed roots.
- The historical reconciliation uses path and size, not a full hash comparison of every historical record.
- SHA-256 was targeted to candidate and archive files, not every file in the project.
- Same-size candidates are not confirmed duplicates until their hashes match.
- Duplicate groups do not establish which copy is canonical or safe to remove.
- Phase 0 remains partial until its previously recorded blockers are resolved: local master-plan hash registration, separate original-guide identification, and an independent physical backup destination.
- Phase 1 Git checkpoint remains subject to owner review; no commit is created by this report-generation step.

## 8. Evidence

The output manifest `manifests/phase_01_outputs.json` registers the scan, consolidation, reconciliation, and SHA-256 evidence files with their sizes and SHA-256 hashes.

The validation result is recorded in `reports/validation/phase_01_validation.json`.

## 9. Conclusion

The seven-root discovery, consolidated inventory, historical path-and-size reconciliation, targeted SHA-256 verification, and duplicate-group analysis have produced a traceable evidence set. Phase 1 closeout remains conditional on successful artifact validation, synchronized project-state documentation, and owner review of the Git checkpoint.


## Privacy-safe evidence publication

Original inventory CSV and log files are retained locally and were not
modified. Git publication uses sanitized copies in
`reports/inventory/public_sanitized/`.

Absolute paths matching the seven configured source roots were replaced
with stable root aliases. CSV row counts, JSON parseability, and sanitized
file hashes were validated. The output manifest registers the sanitized
copies and their SHA-256 hashes. The private `.local` configuration is
not included in publication evidence.
