# ML CP — Project Context

## Project identity

**Project name:** ML CP

**Research title:** Domain-Specific Instruction-Tuning Dataset Curation Framework

**Primary objective:** Develop and evaluate a reproducible framework for curating domain-specific instruction-tuning datasets, with evidence-grounded synthetic examples, quality filtering, evaluation, repair, and downstream model experimentation.

## Research workstreams

1. Dataset engineering: source processing, extraction, page recovery, chunking, sanitization, generation, quality control, evidence validation, filtering, judging, repair, and dataset assembly.
2. Model experimentation: B0–B5 experiments, training configurations, adapters, predictions, and evaluation.

## Research pipeline

Source documents
→ extraction and page recovery
→ chunking and sanitization
→ synthetic example generation
→ schema and quality checks
→ evidence validation and judging
→ human review and repair
→ filtered and frozen candidate datasets
→ B0–B5 experiments
→ predictions and evaluation
→ reproducibility package and research documentation.

## Source-of-truth policy

The local project workspace, artifact registry, phase reports, manifests, and validated state files are the source of truth.

Chat history is a temporary working interface. It must not be treated as the only record of project state.

## Current locations

- `MLCP_SOURCE`: original source material; preserve unchanged during discovery.
- `MLCP_WORKSPACE`: canonical project workspace and isolated Git repository.
- `MLCP_RECOVERY`: recovery copy and verification evidence.
- `MLCP_PLAN_REFERENCE`: master implementation plan, version 2.0.

Actual local paths are recorded only in `.local/phase_00_local_paths.txt`. Do not publish personal absolute paths.

## Operating rules

- Do not rerun completed work without first checking saved outputs and hashes.
- Do not overwrite historical datasets, predictions, adapters, or checkpoints.
- Do not delete or reorganize original source material during discovery.
- Never treat a filename as proof of an artifact's validity.
- Never invent provenance, model results, or missing configuration values.
- Never expose or commit `.env`, credentials, private data, or restricted source material.
- Every work unit must leave a durable report, manifest, validation result, state update, and next action.
- A phase is complete only when its exit criteria pass.
