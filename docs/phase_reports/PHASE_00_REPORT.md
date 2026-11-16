# PHASE 00 REPORT — Preserve Current State and Establish a Recovery Point

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework  
**Plan version:** 2.0  
**Date:** 2026-11-16  
**Status:** partial

## 1. Objective

Preserve the existing project state, establish a verified recovery point, register known artifacts, document the current state, and create a durable handoff for future AI sessions.

## 2. Canonical project boundary

The owner explicitly confirmed the canonical workspace as MLCP_WORKSPACE.

The original MLCP_SOURCE remains separate and was not merged, reorganized, or overwritten.

An isolated Git repository exists in the canonical workspace. The parent repository was left untouched.

## 3. Recovery evidence

### Original source

- 26,027 files copied.
- Approximately 714.07 MB.
- 26,027 SHA-256 matches.
- Zero mismatches, missing files, or extra files.

### Canonical workspace

- 7 files copied.
- Approximately 9.15 MB.
- 7 SHA-256 matches.
- Zero mismatches.

### Limitation

The source and recovery copies reside on different partitions of the same physical SSD. This is not an independent physical backup.

## 4. Git boundary

- Isolated project repository initialized.
- Branch: master
- Commit count at checkpoint: 0
- No remote configured.
- No commit or push performed.
- Parent repository left unchanged.

The Phase 0 checkpoint remains uncommitted pending owner review. This is an explicit exception record, not an accidental omission.

## 5. Historical inventory reconciliation

The original source contained 26,027 files, including the virtual environment.

The historical master inventory contained 26,015 entries. Twelve source files were absent from that older inventory. The current source inventory and earlier data inventory reconcile as follows:

- Historical master inventory: 26,015.
- Additional current source files: 12.
- Current source total: 26,027.
- Historical data inventory: 393.
- Two additional data archives: 2.
- Current data file total: 395.

The historical project audit inventory contained 492 records. The current audit comparison found:

- 492 path-and-size matches.
- 9 current-only files.
- 0 historical-only files.
- 0 size changes.

The nine current-only files include six Python bytecode cache files and three audit/discovery reports.

## 6. Current artifact registry

The registry contains 501 current source files, excluding .venv.

- 501 unique relative paths.
- 501 SHA-256 values.
- 501 source reverification matches.
- 0 mismatches.
- 0 hash errors.
- 1 sensitive configuration record.
- 3 zero-byte files retained.

Canonical and recovery registry SHA-256:

$RegistryHash

The recovery copy hash matches the canonical registry.

### Classification corrections

The initial filename-based classification over-assigned model artifact candidates.

Review of checkpoint paths and representative JSON structures established that:
- Improved-generation checkpoints are generation slot-state records.
- Production-generation V2 checkpoints are generation attempt/pass records.
- Production checkpoints are generated batch state records.
- These are not verified trained model weights.
- model_weight_candidates.csv lists ZIP archives.
- The .jsonl.tmp file is temporary dataset output.
- .pyc files are generated Python cache.
- Logs are execution evidence.

No original source file was modified during these classification corrections.

## 7. Archive verification

data/interim.zip:
- 348 entries.
- 327 readable files.
- 21 directories.
- 0 errors.
- SHA-256: 9109ED7912BD67300CF0A08CD391C248D85BFC3498308C7F3F8F8DB04A0A41C6

data/phase3.zip:
- 8 entries.
- 7 readable files.
- 1 directory.
- 0 errors.
- SHA-256: 20F4CCFF3526FFDBFFBC7F1D47058BB467FEA2E06A30A8CFFBC34947BCE01EC7

The test confirms entry readability and byte counts against ZIP metadata. It does not establish semantic correctness of archive contents.

## 8. Methodology evidence

Two methodology documents were found under the original source docs/methodology/.

They are evidence-based drafts and explicitly request review before merging into the project repository. They were preserved unchanged.

The source-processing evidence describes four training-eligible PDFs totaling 429 pages, extraction and page-recovery work, and remaining limitations.

The chunking evidence distinguishes standard chunking from deterministic paragraph/sentence boundary-aware chunking. It does not establish that all V2 chunks satisfy the configured minimum token target.

## 9. Knowledge retention outputs

Created:
- PROJECT_CONTEXT.md
- PROJECT_STATE.md
- NEXT_ACTION.md
- DECISIONS.md
- AI_WORK_PROTOCOL.md
- docs/ai_handoff/AI_START_HERE.md
- docs/ai_handoff/CURRENT_HANDOFF.md
- docs/ai_handoff/EVIDENCE_INDEX.md
- state/session_log.md

## 10. Remaining blockers

1. Local copy and SHA-256 registration of the master implementation plan remain pending.
2. The exact identity and local location of any separate original project guide remain pending.
3. An independent physical backup destination has not been verified.
4. Full project source-location discovery has not started.
5. Large-file storage strategy has not been selected.
6. Historical datasets and experiment results have not all been independently reproduced.

## 11. Phase conclusion

Phase 0 has established a current artifact registry, preserved recovery copies, verified archive readability, documented the Git boundary, and created durable AI handoff files.

The phase remains **partial**, not completed, because the master guide/reference registration and independent backup location review remain outstanding.

Phase 1 must not start until the exact action in NEXT_ACTION.md is resolved.

## Decision: Independent Backup Requirement Waived

**Date:** 2026-11-17  
**Decision owner:** Project owner

The project owner has explicitly waived the requirement for an independent physical backup during Phase 0.

The intended preservation strategy is to maintain the project in the isolated workspace and publish approved project files to a separate GitHub remote repository.

Important qualifications:
- GitHub is not considered a verified remote copy until the repository is established and the approved files have been committed and pushed successfully.
- Files exceeding GitHub's regular 100 MB individual-file limit must be handled through Git LFS or suitable external artifact storage.
- `.env`, credentials, secrets, and other excluded sensitive configuration must never be committed.
- The original source directory remains unmodified.
- Git staging, committing, and pushing require explicit project-owner approval.

**Risk acceptance:** The project owner accepts the risk of not maintaining an independent physical backup.
