# AI Work Protocol — ML CP

## Source of truth

The repository, artifact registry, phase reports, manifests, validation files, and handoff documents are authoritative. Chat history is not project storage.

## Mandatory startup sequence

1. Read `AI_WORK_PROTOCOL.md`.
2. Read `docs/ai_handoff/AI_START_HERE.md`.
3. Read `PROJECT_CONTEXT.md` and `PROJECT_STATE.md`.
4. Read `NEXT_ACTION.md` and `docs/ai_handoff/CURRENT_HANDOFF.md`.
5. Read the active phase report and only the evidence files it references.
6. Inspect Git status and confirm the current checkpoint.
7. State the verified position and one bounded next task before modifying anything.

## Execution rules

- Work only on the task specified in `NEXT_ACTION.md`.
- Never assume a script ran because it exists.
- Never claim local commands were executed by the AI unless a connected tool actually executed them.
- Do not rerun completed work without checking saved outputs and hashes.
- Do not overwrite historical datasets, predictions, adapters, or checkpoints.
- Do not move or delete source files during discovery.
- Do not call paid APIs, run training, or run inference without explicit approval.
- Never expose API keys, credentials, `.env` values, or private data.
- Never invent provenance, configuration values, metrics, or results.
- Use artifact IDs and SHA-256 values when referring to files.
- Prefer manifests and selected excerpts over uploading entire large files.
- Preserve exact historical filenames and identifiers.

## Checkpoint requirements

At the end of every work unit:

1. Save outputs to a run-specific location or safe new filename.
2. Validate file structure, counts, and hashes.
3. Save a machine-readable run record.
4. Update the artifact registry where applicable.
5. Update the phase report and validation record.
6. Update `PROJECT_STATE.md`.
7. Update `NEXT_ACTION.md` with one precise task.
8. Update `docs/ai_handoff/CURRENT_HANDOFF.md`.
9. Record whether the checkpoint is committed or uncommitted and why.

## Failure handling

If a task fails or is interrupted:

- Preserve partial outputs.
- Record the exact error and command.
- Do not mark the task complete.
- Save the resume point and required inputs.
- Do not silently retry operations that may duplicate API calls or outputs.

## New-session prompt

You are continuing ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework.

The repository and its manifests are the source of truth; chat history is not.

Read AI_WORK_PROTOCOL.md, AI_START_HERE.md, PROJECT_CONTEXT.md, PROJECT_STATE.md, NEXT_ACTION.md, and CURRENT_HANDOFF.md first.

Do not repeat completed work. Do not overwrite historical artifacts. Do not call paid APIs or run training/inference without explicit approval. Do not move or delete source files during discovery. Never invent missing provenance or results.

Work only on the bounded task in NEXT_ACTION.md. Save outputs, logs, hashes, validation, phase report, updated state, updated handoff, and the exact next action. Do not mark a phase complete until its exit criteria pass.
