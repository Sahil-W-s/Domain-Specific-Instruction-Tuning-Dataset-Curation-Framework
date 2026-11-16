# ML CP — Current Project State

**Last updated:** 2026-11-16
**Plan version:** 2.0
**Current phase:** Phase 0 — Preserve current state and establish a recovery point
**Phase status:** partial

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

- Registry: eports/inventory/known_existing_artifacts.csv
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
