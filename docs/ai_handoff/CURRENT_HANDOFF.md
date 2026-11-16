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
