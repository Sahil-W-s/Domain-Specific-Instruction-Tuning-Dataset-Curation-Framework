# NEXT ACTION — Phase 2 Owner Review

**Last updated:** 2026-11-17  
**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework  
**Current phase:** Phase 2 — Build the content-aware artifact registry and large-file map

## Approved phase status

- Phase 0: completed by owner approval.
- Phase 1: completed by owner approval.
- Phase 2: deliverables generated and technically validated; owner review pending.

Do not reopen Phases 0 or 1 unless the owner requests it or new evidence makes it necessary.

## Immediate task — review Phase 2 deliverables

Review the following files:

1. `docs/phase_reports/PHASE_02_REPORT.md`
2. `manifests/artifact_registry.schema.json`
3. `manifests/artifact_registry.jsonl`
4. `reports/inventory/artifact_inventory.csv`
5. `reports/inventory/large_files.csv`
6. `reports/inventory/exact_duplicates.csv`
7. `reports/inventory/possible_duplicates_review_v2.csv`
8. `reports/inventory/hash_failures.csv`
9. `scripts/build_phase2_deliverables.py`

## Verified technical results

- 1,531 registry records; 1,531 unique IDs.
- Schema validation: 1,531 valid, zero invalid.
- Hash statuses: 1,496 verified; 2 not applicable; 33 historical failed.
- All 33 historical failures have verified replacement records; zero unresolved.
- Independent SHA-256 sample: 15/15 passed; this was not an exhaustive rehash.
- Artifact inventory: 1,531 rows, exact registry match.
- Large-file report: 41 rows, all registry files at or above 50 MiB.
- Exact duplicates: 564 groups and 1,373 memberships, exact registry match.
- Possible duplicates: 11 groups and 138 candidates, all pending manual review.
- No source files were moved, deleted, renamed, or extracted.

## Phase 2 exit-gate review

Confirm that:
- Important artifacts have stable registry records.
- All known large files have been identified and classified or explicitly marked pending.
- Historical hash failures are transparently reconciled.
- Duplicate reports distinguish exact duplicates from unreviewed candidates.
- The report's limitations and preservation safeguards are accurate.

Do not treat possible duplicates as confirmed duplicates. Do not delete or consolidate any files.

## After owner review

1. Record explicit owner approval or requested corrections.
2. If approved, mark Phase 2 completed in the state files.
3. Review the full Git diff and untracked-file inventory.
4. Stage only individually reviewed files.
5. Run secret, privacy, and large-file checks before any commit.
6. Commit only after explicit owner approval.

## Restrictions

- Do not use `git add .`.
- Do not commit or push without owner approval.
- Do not rerun completed Phase 0 or Phase 1 work without a specific evidence-based reason.
- Do not move, delete, rename, or extract source material.
- Do not configure DVC, Git LFS, cloud storage, or migration without an approved plan.

## Authoritative next action — Phase 3 owner review

1. Review `docs/phase_reports/PHASE_03_REPORT.md`.
2. Review `reports/validation/phase_03_validation.json`.
3. Review `manifests/phase_03_outputs.json`.
4. Inspect the selected Phase 3 Git changes and ensure no secrets,
   local-only files, or unrelated Phase 2 inventory outputs are staged.
5. Provide explicit approval before staging, committing, or pushing.

Do not use `git add .`. Do not repeat completed Phase 0–2 work.
