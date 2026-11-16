# Phase 4 P4.3 — README Content Review

**Date:** 2026-11-17  
**Status:** README review completed; upstream rights/provenance and payload privacy review remain open.

## Evidence reviewed

Local-only outputs supplied by the owner:

- `.local/phase4_archive_inspection/archive_readmes_local.md`
- `.local/phase4_archive_inspection/readme_inspection_summary.json`

The summary reports 17 ZIP inventory records, 9 unique archive groups, 9 archives opened, 9 README entries read, zero entries skipped by the 64 KiB limit, and zero errors. The reader opened only README-named entries; it did not extract entries, modify source archives, or compute new hashes.

Generated README contents were reviewed locally and are intentionally not copied into this public report.

## Findings

### Adapter model-card READMEs

The adapter README entries identify:

- Base model: `Qwen/Qwen2.5-1.5B-Instruct`.
- Adapter ecosystem: PEFT / LoRA.
- Pipeline tag: text generation.
- Framework version recorded: PEFT 0.21.2.

The model-card template leaves the developer, model type, language, licence, fine-tuning data, training procedure, evaluation, model sources, and other provenance fields as `[More Information Needed]`. The README therefore does not establish the adapter licence or redistribution permission.

### Reproducibility package README

The package README describes its contents as code, datasets, trained LoRA adapters, predictions, evaluation outputs, and provenance artifacts. It says the base model is obtained separately from Hugging Face and identifies `Qwen/Qwen2.5-1.5B-Instruct`.

The README records this training configuration:

- 4-bit NF4 quantization with double quantization.
- FP16 compute.
- LoRA fine-tuning.
- Tesla T4-compatible configuration.
- Three epochs.
- Learning rate 2e-4.

It describes baselines B0–B5 and includes evaluation caveats that must remain attached to downstream claims:

- B3 is a reconstructed unfiltered candidate pool, not a verified pre-filter snapshot of B4.
- IoT held-out test: 35 examples, with 12 QA, 8 extraction, 5 summarization, 5 unanswerable, and 5 classification.
- General retention: 50 questions sampled from the `cais/mmlu` test split, seed 42; explicitly not a comprehensive general-capability evaluation.
- Unanswerable-question assessment is preliminary manual labelling requiring independent review.
- The README states paired McNemar tests did not establish statistically significant differences at the 0.05 level for the 50-question retention benchmark.
- B2 validation data overlaps with training data used in the general-domain experiment; independent MMLU questions were used for retention.
- B3 and B4 share IoT validation examples; B5 validation includes IoT and general-domain examples, so validation losses across those compositions are not directly comparable.
- The held-out IoT test set was kept separate from training and validation.

The package layout lists source datasets and held-out test material, model adapter backups, predictions, evaluation artifacts, configuration, and SHA256SUMS metadata.

## Rights and privacy assessment

1. No README states an adapter licence. The model-card licence fields are explicitly incomplete.
2. The package README does not identify licences or redistribution terms for each included dataset, source document, prediction, or model artifact.
3. The stated base-model identifier is a provenance lead, not proof of the applicable base-model terms or permission to redistribute derivative adapters.
4. The README descriptions indicate that the reproducibility archive contains multiple classes of potentially third-party or sensitive material. The README text alone cannot establish whether payloads contain personal data, credentials, confidential material, or restricted source content.
5. No secret values or personal identifiers were observed in the README text reviewed. This is not a payload-wide privacy clearance.
6. No legal or redistribution permission is inferred from the fact that an upstream source may be publicly accessible.

## Decisions

- Keep rights, redistribution, and sensitivity statuses unknown unless separately supported by upstream licence/terms and content evidence.
- Do not publish adapters, datasets, source documents, predictions, or archive contents.
- Keep the Google Drive destination private and restricted.
- Keep `manifests/storage_map.yml` at `migration_authorized: false`.
- Preserve the experiment caveats above in any future reports or model comparisons.
- Do not select a canonical B2–B5 adapter/checkpoint without experiment-lineage evidence.
- No source artifacts were moved, deleted, renamed, extracted over, uploaded, or modified by this review.

## Next bounded action

Perform source-specific rights/provenance checks for the named base model and every identifiable dataset/source family in the package. Use the existing package manifests and provenance artifacts as evidence; inspect only the minimum relevant metadata needed. Record exact upstream terms and evidence per artifact/source family. Where provenance or terms cannot be established, retain `unknown`. Separately determine which payload classes require privacy review before any storage migration. Do not configure DVC or migrate files during this work.
