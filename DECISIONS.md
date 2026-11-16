# ML CP — Decision Log

This file is append-only. New decisions must be added with a date and rationale. Do not rewrite historical decisions to hide changed assumptions.

## D-001 — Canonical workspace

**Date:** 2026-11-16  
**Decision:** `Domain-Specific-Instruction-Tuning-Dataset-Curation-Framework` is the canonical project workspace.  
**Reason:** Explicitly confirmed by the project owner.  
**Impact:** Original `ML CP` source directory remains a separate read-only source location during discovery.

## D-002 — Preserve original source

**Date:** 2026-11-16  
**Decision:** Do not merge, reorganize, rename, or overwrite the original source directory during Phase 0.  
**Reason:** Preserve provenance and recovery options.

## D-003 — Recovery copy location

**Date:** 2026-11-16  
**Decision:** Use `MLCP_RECOVERY` as the recovery alias for the current D: recovery directory.  
**Limitation:** D: and C: are partitions on the same physical SSD. This is not an independent physical backup.

## D-004 — Git isolation

**Date:** 2026-11-16  
**Decision:** Keep the canonical workspace as an isolated Git repository. Do not use or modify the parent repository.  
**Reason:** Prevent unrelated parent-directory content from entering the ML CP repository.

## D-005 — No Git publication during Phase 0

**Date:** 2026-11-16  
**Decision:** Do not stage, commit, or push Phase 0 files until the owner reviews the generated documentation and approves the checkpoint.  
**Reason:** The phase is still partial and source-reference registration is pending.

## D-006 — Artifact registry scope

**Date:** 2026-11-16  
**Decision:** The initial current registry contains 501 files and excludes `.venv`.  
**Reason:** `.venv` is an environment, not project-authored research material. It remains preserved in the source backup.

## D-007 — Hash verification

**Date:** 2026-11-16  
**Decision:** Use SHA-256 and byte-size verification for file identity and copy checks.  
**Reason:** Filenames and timestamps alone do not establish content identity.

## D-008 — Checkpoint classification

**Date:** 2026-11-16  
**Decision:** Generation checkpoint JSON files are classified as workflow state, not trained model weights.  
**Reason:** Inspected records contain slot status, attempt state, or generated batch data.

## D-009 — Sensitive files

**Date:** 2026-11-16  
**Decision:** `.env` is registered as sensitive metadata only. Its contents must never be copied into tracked documentation or Git.  
**Reason:** Prevent credential exposure.

## D-010 — Zero-byte files

**Date:** 2026-11-16  
**Decision:** Retain the three zero-byte JSONL files in the inventory.  
**Reason:** Their purpose is not yet established. Empty files must not be silently deleted or interpreted as successful outputs.

## D-011 — Large artifact storage

**Date:** 2026-11-16  
**Decision:** No DVC, Git LFS, or external artifact storage migration during Phase 0.  
**Reason:** Storage decisions require a complete location inventory, rights review, size analysis, and destination approval.

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


## D-012 — Provisional Phase 4 artifact-storage architecture and migration hold

**Date:** 2026-11-17  
**Decision:** Use DVC with a restricted, dedicated Google Drive folder as the preferred primary store for large artifacts. Keep GitHub for code, safe manifests, reports, and DVC metadata. Do not add new bulk artifacts to Git LFS under the zero-additional-spend constraint.  
**Reason:** The owner reported 5 TB of available Google Drive space, confirmed a dedicated folder can be created, and selected zero additional spending. The large-file inventory contains 41 verified records representing 21 unique SHA-256 contents.  
**Conditions:** This is an architecture decision, not migration authorization. All 41 records currently have unknown sensitivity and unknown redistribution status. Rights/privacy review, reproducibility-package inspection, canonical model/checkpoint selection, Drive access configuration, and a recorded storage map are required before upload.  
**Preservation:** Preserve every source path and copy. Matching SHA-256 values may be deduplicated in DVC storage, but do not delete, move, or consolidate source files.  
**Risk:** An independent physical backup has not been verified. The historical Phase 0 risk acceptance does not constitute evidence of an independent backup.
