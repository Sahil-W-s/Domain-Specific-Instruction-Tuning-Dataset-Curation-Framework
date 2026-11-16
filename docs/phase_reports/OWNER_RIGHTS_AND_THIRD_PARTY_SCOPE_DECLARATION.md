# Owner Rights and Third-Party Source Scope Declaration

**Date recorded:** 2026-11-17  
**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework  
**Source:** Explicit owner declaration in the project conversation.

## Owner declaration

The owner declares that the rights to the project materials they created or supplied are theirs and that these materials are open source. The declared scope is limited to the project's own/supplied materials, including:

- Original IoT PDFs supplied by the owner
- Generated and curated datasets
- Project scripts and code
- Project adapters and checkpoints
- Reports and related project outputs

This is recorded as an **owner declaration**, not an independent legal verification. No specific open-source licence identifier or licence text was supplied in the declaration; do not invent one or claim that a particular standard licence applies. Where the project needs to publish or redistribute these materials, the exact licence notice and any required attribution should be recorded in the relevant release/package.

## Third-party sources and dependencies

The owner's declaration does **not** extend to third-party sources, including the identified Dolly dataset, MMLU dataset, and Qwen base model.

The project will not redistribute those third-party source datasets or base-model files. They may be identified as dependencies and referenced by their upstream repository identifiers. Users/researchers who need them are expected to obtain them independently from their respective providers and comply with the terms applicable to the versions they obtain.

This separation does not resolve the provenance/revision gaps already recorded for Dolly and MMLU, nor does it establish the licence of any third-party material embedded in project outputs.

## Continuing controls

- Keep third-party source payloads outside the project's redistribution scope.
- Do not bundle third-party source datasets or the Qwen base-model payload in public project releases.
- Keep source/revision identifiers and dependency instructions where known; mark missing immutable revisions as unknown.
- Owner declaration of rights does not replace the separate privacy/secrets review.
- Do not infer that every derived artifact is automatically clear for publication without checking its contents and lineage.
- Keep `manifests/storage_map.yml` at `migration_authorized: false` until the remaining per-artifact privacy/storage decisions and owner approval are complete.
- Preserve all existing source paths and copies; this declaration does not authorize moving, deleting, or consolidating files.

## Status

The project records the owner's rights declaration for the listed project materials and records third-party source payloads as independently acquired dependencies, not redistributed project assets. The specific open-source licence identifier for the owner's materials remains to be documented if a formal licence grant is intended for public reuse.
