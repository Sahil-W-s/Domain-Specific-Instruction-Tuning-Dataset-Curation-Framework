# NEXT ACTION — Phase 0 Closeout

**Active phase:** Phase 0  
**Status:** partial

## Single bounded task

Complete the source-reference and recovery-location registration required for the Phase 0 closeout.

### Required actions

1. Locate the local copy of `ML_CP_Resilient_Implementation_Plan.md` (version 2.0).
2. Confirm whether a separate original project implementation guide exists.
3. Record each guide's local root alias, relative path, file size, modified time, and SHA-256 in the reference register.
4. If no local copy exists, explicitly record that the guide is available only as a ChatGPT Library reference and that local hash registration is pending.
5. Identify an independent physical backup location, such as an external drive or approved cloud/object store. Do not copy large data until the destination is confirmed and sufficient space is available.
6. Update the Phase 0 report, validation, output manifest, project state, and handoff with the result.

## Acceptance criteria

- The master plan/reference is identified without ambiguity.
- Its SHA-256 is recorded or its local unavailability is explicitly documented.
- The same-SSD recovery limitation is documented.
- An independent backup destination is confirmed or explicitly recorded as unavailable.
- The handoff remains sufficient for a fresh AI session to resume without uploading the entire project.

## Restrictions

- Do not start Phase 1 until this closeout task is resolved.
- Do not move, delete, or reorganize source files.
- Do not install DVC or configure remote storage.
- Do not stage or commit files without explicit review.
