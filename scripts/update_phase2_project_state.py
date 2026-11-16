from pathlib import Path
from datetime import datetime, timezone
import shutil

root = Path.cwd()

targets = [
    "PROJECT_STATE.md",
    "NEXT_ACTION.md",
    "docs/ai_handoff/CURRENT_HANDOFF.md",
    "state/phase_status.yml",
    "state/session_log.md",
]

for item in targets:
    if not (root / item).is_file():
        raise SystemExit(f"STOP: required file missing: {item}")

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
backup_dir = root / "reports/state_update_backups" / f"phase2_state_{stamp}"
backup_dir.mkdir(parents=True, exist_ok=False)

for item in targets:
    destination = backup_dir / item
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / item, destination)

print("Backups created:", backup_dir.relative_to(root))

# PROJECT_STATE: preserve history and append authoritative current status.
path = root / "PROJECT_STATE.md"
text = path.read_text(encoding="utf-8")

if "## Authoritative current status — Phase 2" in text:
    raise SystemExit("STOP: Phase 2 state section already exists.")

text += """

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
"""

path.write_text(text, encoding="utf-8")

# NEXT_ACTION: replace stale instructions with the actual next bounded task.
next_action = """# NEXT ACTION — Phase 2 Owner Review

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
"""
(root / "NEXT_ACTION.md").write_text(next_action, encoding="utf-8")

# CURRENT_HANDOFF: append an authoritative continuation section.
path = root / "docs/ai_handoff/CURRENT_HANDOFF.md"
text = path.read_text(encoding="utf-8")

if "## Authoritative continuation — Phase 2 owner review" in text:
    raise SystemExit("STOP: Phase 2 handoff section already exists.")

text += """

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
"""
path.write_text(text, encoding="utf-8")

# phase_status.yml: update approved phases and add Phase 2.
path = root / "state/phase_status.yml"
text = path.read_text(encoding="utf-8")

text = text.replace("current_phase: 1", "current_phase: 2", 1)
text = text.replace(
    "    status: partial\n"
    "    report: docs/phase_reports/PHASE_00_REPORT.md\n"
    "    outputs_manifest: manifests/phase_00_outputs.json\n"
    "    validation: reports/validation/phase_00_validation.json\n"
    "    blockers:\n"
    "    - Local SHA-256 registration of master implementation plan pending\n"
    "    - Separate original guide identity/location pending\n"
    "    - Independent physical backup destination not verified\n",
    "    status: completed\n"
    "    owner_approval: completed\n"
    "    report: docs/phase_reports/PHASE_00_REPORT.md\n"
    "    outputs_manifest: manifests/phase_00_outputs.json\n"
    "    validation: reports/validation/phase_00_validation.json\n"
    "    historical_caveats:\n"
    "    - Master implementation plan local SHA-256 registration was previously recorded as pending\n"
    "    - Separate original guide identity/location was previously recorded as pending\n"
    "    - Independent physical backup destination was not verified in the historical closeout\n",
    1
)

if "  phase_02:" in text:
    raise SystemExit("STOP: phase_02 already exists in phase_status.yml")

text += """
  phase_02:
    name: Build the content-aware artifact registry and large-file map
    status: owner_review_pending
    report: docs/phase_reports/PHASE_02_REPORT.md
    registry: manifests/artifact_registry.jsonl
    schema: manifests/artifact_registry.schema.json
    outputs:
    - reports/inventory/artifact_inventory.csv
    - reports/inventory/exact_duplicates.csv
    - reports/inventory/possible_duplicates_review_v2.csv
    - reports/inventory/large_files.csv
    - reports/inventory/hash_failures.csv
    builder: scripts/build_phase2_deliverables.py
    completed_at: '2026-11-17'
    validation_results:
      registry_records: 1531
      schema_valid_records: 1531
      schema_invalid_records: 0
      verified_hashes: 1496
      not_applicable_hashes: 2
      historical_failed_records: 33
      verified_replacement_links: 33
      unresolved_historical_failures: 0
      independent_sha256_sample_passed: '15/15'
      artifact_inventory_rows: 1531
      large_file_rows: 41
      exact_duplicate_groups: 564
      exact_duplicate_memberships: 1373
      possible_duplicate_groups: 11
      possible_duplicate_candidates: 138
    limitations:
    - Independent SHA-256 recomputation was a targeted 15-file sample, not exhaustive
    - Possible duplicate candidates remain pending manual review
    - Historical failed registry records are retained and superseded by verified replacement records
    - No source files were moved, deleted, renamed, or extracted
"""

(root / "state/phase_status.yml").write_text(text, encoding="utf-8")

# Session log: append an auditable entry.
path = root / "state/session_log.md"
text = path.read_text(encoding="utf-8")
text += """

## 2026-11-17 — Phase 2 registry and deliverables

- Built the content-aware artifact registry: 1,531 unique artifact records.
- Validated all 1,531 records against the registry schema.
- Independently recomputed a targeted SHA-256 sample: 15/15 passed; this was not an exhaustive rehash.
- Preserved 33 historical failed records and verified all 33 replacement links; zero unresolved.
- Generated `reports/inventory/artifact_inventory.csv` with 1,531 rows and exact registry field matches.
- Generated `reports/inventory/large_files.csv` with 41 records; exact coverage for all registry artifacts at or above 50 MiB.
- Validated `reports/inventory/exact_duplicates.csv`: 564 groups and 1,373 memberships, exact registry match.
- Validated 138 possible-duplicate candidates across 11 groups; all remain pending manual review.
- Generated `reports/inventory/hash_failures.csv`: 33 historical superseded records, zero unresolved.
- Generated `docs/phase_reports/PHASE_02_REPORT.md`.
- Created `scripts/build_phase2_deliverables.py` for reproducible generation.
- Created timestamped backups before regenerating deliverables and before updating these state documents.
- Phase 0 and Phase 1 remain owner-approved complete.
- Phase 2 technical deliverables are generated and validated; owner review remains pending.
- No source files were moved, deleted, renamed, or extracted.
- No Phase 2 files were staged, committed, or pushed.
"""

path.write_text(text, encoding="utf-8")

print("\nUPDATED:")
for item in targets:
    print("-", item)

print("\nBackup directory:", backup_dir.relative_to(root))
print("No Git staging, commit, or push was performed.")
