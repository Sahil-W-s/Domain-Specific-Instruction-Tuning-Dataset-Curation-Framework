# Phase 0 — Backup and Verification Note

**Date:** 2026-11-16

## Source backup

- Source alias: `MLCP_SOURCE`
- Recovery alias: `MLCP_RECOVERY/ML_CP_2026-11-16`
- Files copied: 26,027
- Size: approximately 714.07 MB
- Robocopy failures: 0
- SHA-256 matches: 26,027
- SHA-256 mismatches: 0
- Missing files: 0
- Extra files: 0

## Canonical workspace backup

- Workspace alias: `MLCP_WORKSPACE`
- Recovery alias: `MLCP_RECOVERY/MLCP_WORKSPACE_2026-11-16`
- Files copied: 7
- Size: approximately 9.15 MB
- Robocopy failures: 0
- SHA-256 matches: 7
- SHA-256 mismatches: 0

## Registry recovery

- Canonical registry: `reports/inventory/known_existing_artifacts.csv`
- Recovery registry: `MLCP_RECOVERY/phase0_artifact_registry/known_existing_artifacts.csv`
- SHA-256: `BB7C79DD7E254DB600BB6413F053D9142FF4B7403729CFB07338DE90D1B593C7`
- Recovery hash status: MATCH

## Archive verification

- `data/interim.zip`: 348 entries, 327 readable files, 21 directories, 0 errors.
- `data/phase3.zip`: 8 entries, 7 readable files, 1 directory, 0 errors.

## Critical limitation

C: and D: are partitions on the same physical SSD. The recovery copies protect against accidental modification or deletion but do not protect against physical SSD failure.

No independent physical backup has been verified as of this report.

## Safety

The `.env` file was inventoried by metadata only. Its contents were not printed or included in documentation.
