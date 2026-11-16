# Phase 4 P4.3 — Source-Specific Rights and Provenance Review

**Date:** 2026-11-17  
**Status:** Partial source terms verified; source-document provenance, package manifest reconciliation, and payload privacy review remain open.  
**Migration authorization:** Not granted.

## Scope and evidence

Reviewed tracked repository evidence:

- docs/audit/archive_contents.csv — identifies phase-3 training archive members.
- docs/audit/data_artifact_inventory.csv — identifies generated/extracted artifacts and provenance-audit outputs.
- docs/audit/master_file_inventory.csv — identifies four original IoT PDF inputs by title and classifies them as raw inputs. Absolute local paths are omitted.
- docs/phase_reports/PHASE_04_P4_3_README_REVIEW.md — records the reproducibility-package README claims and evaluation caveats.

The archive member inventory identifies b2_dolly_1000.jsonl, b3_iot_unfiltered_reconstructed_600.jsonl, b4_iot_filtered_577.jsonl, b5_domain_577.jsonl, b5_general_577.jsonl, b5_iot_plus_dolly_1154.jsonl, and phase3_validation_report.json.

The package README additionally describes a 50-question sample from cais/mmlu for general-retention evaluation. The tracked archive member listing does not independently confirm the exact MMLU subset file, revision, split, or sampling manifest.

## Source-by-source findings

| Source family | Upstream identity and terms | Private/local storage | Training or evaluation use | Redistribution |
|---|---|---|---|---|
| Base model | Qwen/Qwen2.5-1.5B-Instruct; Hugging Face model repository labels it Apache-2.0. [Model repository](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) | Consistent with the stated license, subject to Apache-2.0 conditions and applicable law. | The license permits use and derivative works, subject to its conditions. Whether each adapter is legally a derivative work and which notices must accompany it still require artifact-level review. | Permitted subject to Apache-2.0 requirements, including applicable license/copyright/NOTICE obligations. Do not infer that adapter licence metadata is complete. |
| Dolly instruction data | The dataset filename b2_dolly_1000.jsonl and README identify Dolly. The matching upstream candidate is databricks/databricks-dolly-15k, whose dataset card states CC BY-SA 3.0 and describes the source data and Wikipedia-derived passages. [Dataset card](https://huggingface.co/datasets/databricks/databricks-dolly-15k) | Copying is consistent with the license grant, subject to applicable conditions and lawful acquisition. | The dataset card explicitly lists training LLMs as an intended use. Whether trained adapter weights constitute an adaptation that must be shared under CC BY-SA is unresolved. | Redistribution of the dataset or adapted dataset material requires attribution and share-alike compliance. Redistribution of model weights trained on it remains unresolved pending legal interpretation and provenance mapping. |
| MMLU evaluation data | README names cais/mmlu; its Hugging Face dataset card labels it MIT. [Dataset card](https://huggingface.co/datasets/cais/mmlu) | Consistent with MIT, subject to retaining applicable copyright/license notices. | README describes evaluation/retention benchmarking, not training. Evaluation use is consistent with MIT. Exact subset revision/split/selection is not yet evidenced by the tracked archive member listing. | MIT permits redistribution subject to inclusion of the copyright and permission notice. Exact contents of the local 50-question sample remain to be reconciled to a source revision and manifest. |
| IoT source PDFs | Four raw input titles appear in the tracked master inventory: 4-iot-protocols-and-security.pdf, 6-iot-physical-servers-cloud-offereings-iot-case-studies.pdf, IOT Unit 1 Contents.pdf, and Unit 2-Iot-platform-design-methodology (1).pptx.pdf. No author, publisher, original URL, source edition, copyright notice, or licence is established by the inventory. | Unknown. Keep restricted; local possession is not proof of a storage right. | Unknown. No source-specific training or text/data-mining permission has been established. | Not cleared. Do not redistribute PDFs, extracted text, or dataset records containing copied source passages. |
| Generated IoT examples and derived datasets | B3/B4/B5 file names establish derived dataset families, but do not provide row-level source-to-example provenance or source-document rights. | Hold pending source-document provenance and privacy review. | Prior generation/curation does not establish permission to continue training or reuse. | Not cleared. |
| Adapters, checkpoints, predictions, evaluation outputs | README describes these artifact classes and identifies Qwen/PEFT/LoRA, but adapter cards leave licence and provenance fields incomplete. Dataset mixture and training lineage are not fully mapped to each artifact. | Keep restricted pending review. | Do not select a canonical B2–B5 checkpoint or infer rights from the base-model licence alone. | Not cleared. |

## Privacy and confidentiality review scope

The following payload classes require a bounded local privacy/secrets review before migration to any cloud remote, even if the remote is private:

1. Original PDFs and extracted text/chunks: check for personal information, confidential course/institution material, third-party copyrighted text, and embedded metadata.
2. Training/evaluation JSONL and derived datasets: check for personal data, copied passages, sensitive examples, and provenance fields.
3. Human-review/audit files: check reviewer identifiers, comments, contact details, and sensitive annotations.
4. Request logs, prompts, API test outputs, and generation logs: check for API keys, tokens, credentials, user-provided content, and provider-specific identifiers. Never print secret values into reports.
5. Predictions, evaluation outputs, adapter weights, and checkpoints: assess memorization/leakage risk and training-data lineage before publication or broad sharing.

The earlier ZIP metadata scan found no suspicious filenames, encrypted entries, unsafe paths, or symlinks, but it did not read general payloads. The README review found no secret values or personal identifiers in README text only. Neither check is a payload-wide privacy clearance.

## Provenance gaps and next evidence required

1. Confirm the exact Dolly upstream repository/revision and the subset/row transformation used to produce b2_dolly_1000.jsonl; map Dolly-derived rows in b5_iot_plus_dolly_1154.jsonl.
2. Confirm the exact MMLU repository revision, split, sample IDs, and seed/selection manifest for the 50-question evaluation subset.
3. For each of the four IoT PDFs, record author/publisher, original source URL or acquisition record, edition/date, copyright notice, and applicable licence/permission. If these cannot be established, retain unknown.
4. Obtain the reproducibility package's exact metadata-only entry listing and the relevant small configuration/provenance manifests (split manifest, dataset validation report, training run manifest, and SHA256SUMS metadata). Do not read dataset/model payloads or extract the archive.
5. Map each B2–B5 adapter/checkpoint to its exact training dataset mixture and run lineage before deciding whether any adapter may be stored or redistributed.

## Decisions and restrictions

- This report is a technical provenance/terms inventory, not legal advice or blanket legal clearance.
- Public availability is not proof of permission.
- Keep rights and privacy status unknown for all 41 large-file inventory records unless per-artifact evidence is completed.
- Keep manifests/storage_map.yml at migration_authorized: false.
- Do not install/configure DVC, upload to Google Drive, publish adapters/datasets/predictions/source documents, or change source locations.
- Preserve every original path and copy. Matching hashes do not authorize deletion or consolidation.
- No source artifacts were moved, deleted, renamed, extracted, uploaded, or modified during this review.
