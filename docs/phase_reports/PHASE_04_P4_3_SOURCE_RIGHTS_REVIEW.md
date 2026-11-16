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


## Owner-supplied original IoT PDFs — bounded source-first review (2026-11-17)

The owner supplied the four original PDFs listed in the project inventory. These exact uploaded files were inspected locally; no internet copies were used.

| Original file | PDF pages | Document identity visible in source | Metadata observations |
|---|---:|---|---|
| `IOT Unit 1 Contents.pdf` | 151 | Opens with “UNIT I — Introduction to Internet of Things”; contents include IoT definition/characteristics, physical and logical design, protocols, communication models, enabling technologies, levels, issues, and applications. | PDF Creator reports Google. No author or publisher metadata was present. |
| `4-iot-protocols-and-security.pdf` | 119 | Opens with “Unit -4 — IoT Protocols And Security”. | PDF Creator reports WPS Presentation; creation/modification metadata is 2026-11-03. No author metadata was present. |
| `6-iot-physical-servers-cloud-offereings-iot-case-studies.pdf` | 99 | Opens with “IoT Physical Servers, Cloud Offerings and IoT Case Studies”; contents include communication APIs, cloud storage, WAMP/Autobahn, Xively, Django, AWS IoT, SkyNet, and case studies. | PDF Creator reports WPS Presentation; creation/modification metadata is 2026-11-03. No author metadata was present. |
| `Unit 2-Iot-platform-design-methodology (1).pptx.pdf` | 60 | Opens with “Unit II — IoT Platform Design Methdology”; outlines the ten-step IoT system design methodology and illustrates smart-irrigation and other design examples. | PDF Creator reports Google. No author or publisher metadata was present. |

A bounded text and PDF-metadata inspection found no explicit author, publisher, copyright notice, licence, permission statement, edition, or original acquisition URL in the extracted document text or basic PDF metadata. This is not proof that no such notice exists in a page image or in the original source from which the slides were made. The visible opening title pages do not identify a publisher or author. These files therefore remain **unattributed source documents with unknown terms**.

### Provenance mapping observations

- Existing project records associate B3/B4 IoT source document IDs with `iot_cloud_case_studies`, `iot_unit1`, and `iot_unit4_protocols_security`. The uploaded documents provide plausible title-level matches for those identifiers, but do not by themselves establish the original source, author, acquisition route, or reuse rights.
- The held-out IoT test metadata references `iot_unit5_pdf`. No corresponding Unit 5 source PDF is among the four uploaded files or the four titles previously identified in the master inventory. This remains an unresolved source-identity gap.
- The relationship between the uploaded Unit II platform-design PDF and any training/evaluation rows is not established by the evidence inspected so far.
- The source manifest shown in the owner's folder screenshot has not yet been supplied as a file; its contents have not been reviewed.

### Evidence boundary and correction to earlier external lookups

Earlier external licence lookups for Qwen, Dolly, and MMLU are not evidence from the owner's original project materials. They are not accepted as project-source provenance or as clearance for this review. The upstream terms in the earlier draft table must be treated as **unverified against the owner's source records**; they do not authorize storage, training, or redistribution. Exact source revisions, acquisition records, and applicable terms must be established from the project's own manifests and source records, or remain unknown. No further external source search was used for this PDF review.

### Current decision

- All four uploaded IoT PDFs: source identity partially established by visible title/content; author/publisher/acquisition/licence/copyright status unknown; local-storage, training-use, and redistribution permission not established.
- Do not redistribute the PDFs, extracted text, or derived records containing their material.
- Keep the missing Unit 5 source and the Unit II mapping unresolved until source records are supplied.
- No source files were moved, renamed, extracted, uploaded to cloud storage, or modified by this review.
- `migration_authorized: false` remains unchanged.
 

## Owner-supplied source manifest and Unit 5 PDF — follow-up review (2026-11-17)

### Source manifest

Reviewed the owner-supplied `source_manifest(2).csv` (4 rows, 7 columns: `doc_id`, `filename`, `pages`, `topic`, `split`, `status`, `notes`). It records:

| doc_id | Source | Pages | Split | Status / note |
|---|---|---:|---|---|
| `iot_unit1` | `IOT Unit 1 Contents.pdf` | 151 | train | canonical; near-duplicate `IOT Unit 1 Contents.pptx.pdf` is to be excluded |
| `iot_unit2` | `Unit 2-Iot-platform-design-methodology (1).pptx.pdf` | 60 | train | eligible; distinct source |
| `iot_unit4_protocols_security` | `4-iot-protocols-and-security.pdf` | 119 | train | eligible |
| `iot_cloud_case_studies` | `6-iot-physical-servers-cloud-offereings-iot-case-studies.pdf` | 99 | train | eligible |

The manifest identifies four training sources and resolves the Unit I canonical/near-duplicate decision. It does not contain a Unit 5 row, nor author, publisher, acquisition URL, edition, copyright, licence, or permission fields. Its `status` values (canonical/eligible) are project curation statuses, not rights clearance.

### Unit 5 source

The owner also supplied `IOT Unit 5-webofthingsandcloudofthings.pdf` (81 pages). Its title page identifies “Unit 5-Web of Things and Cloud of Things”, matching the previously referenced `iot_unit5_pdf` label at title/topic level. The PDF metadata has blank author/title/subject fields; creator is WPS Presentation and creation/modification metadata is 2026-11-03. No explicit copyright, licence, or permission text was found in the extracted text. Pages 25–27 carry the footer attribution “Jaydeep Patil- AISSMS IOIT Pune”; this is a visible attribution, not by itself a licence or proof of authorship/ownership. The file's title-level match makes it a plausible identity match for `iot_unit5_pdf`, but the supplied source manifest does not list it or specify its split/use.

### Updated provenance conclusions

- The four manifest rows support the recorded training-source IDs and topics. They do not establish source acquisition, original authorship/publisher, reuse terms, or permission.
- Unit 5 is now present and plausibly matches the held-out test's `iot_unit5_pdf` source reference. Its actual use in the held-out test still requires the test-generation manifest/row metadata to be reconciled.
- The manifest says Unit 1's PPTX PDF is a near-duplicate to exclude; preserve the original file and path, but do not treat it as a canonical training source.
- Unit 5 is not currently listed as a training source. Do not silently add it to the training split.
- The four training-source PDFs and Unit 5 remain uncleared for cloud storage, training reuse beyond the recorded curation, and redistribution. No copyright/licence/permission basis was established by these uploads.
- No source file was moved, renamed, extracted, uploaded to cloud storage, or modified by this review. `migration_authorized: false` remains unchanged.


## Step 3C — held-out IoT, Dolly, and MMLU provenance reconciliation (2026-11-17)

### Held-out IoT test → Unit 5

The existing local reproducibility-package inspection report records `data/heldout_iot_test.jsonl` as 35 records with SHA-256 `70d07aa68b4e125dd573ba01367f059b550651e5e25d4e271e92f55f04c6ff5d`. Its inspected records carry `metadata.doc_id: iot_unit5_pdf`, `metadata.split: test`, and slide-based chunk/source identifiers (examples include `slide_6` and `slide_9`). The evidence text in those records corresponds to the supplied 81-page Unit 5 Web of Things and Cloud of Things PDF. This resolves the source identity at the held-out dataset's metadata/content level: **Unit 5 is the documented source for the held-out IoT test set**. The four-row training source manifest correctly does not list Unit 5 as a training source. Keep it evaluation-only unless a separate owner-approved change is recorded.

### Dolly source and subset provenance

The local dataset-preparation/inspection records identify the source as `databricks/databricks-dolly-15k`, report 15,011 available rows, sampling seed `20261114`, B2 count 1,000, B5 general count 577, and B2/B5 subset disjointness as true. The B2 records carry source IDs of the form `dolly15k:<category>` and metadata identifying the dataset/category/assignment `B2_generic_only`; B5 general records similarly identify the dataset/category and assignment `B5_general_mix`. The B5 combined dataset is recorded as 577 IoT + 577 general = 1,154 records.

The local records establish the repository identifier, sample seed/counts, assignment labels, and recorded disjointness. They do **not** establish an immutable upstream commit/revision, the upstream dataset snapshot date, or a fully reproducible row-selection manifest with source row IDs. Therefore exact Dolly revision and row-level source selection remain unknown/incomplete. Do not infer a revision from the repository name or sampling date.

### MMLU evaluation provenance

The local `general_retention_manifest.json` identifies `cais/mmlu`, split `test`, 50 questions, seed 42, and 9 excluded original indices (237, 740, 1298, 2087, 3895, 4175, 6149, 6865, 9457). Category counts are STEM 13, Humanities 12, Social sciences 13, Professional and applied 12. The 50-record sample hash is `d7c4f24f3ea17f698b0729093ef601cbdf1ecea53623e62844faa4013f2bf78e`. The sample rows retain `original_index`, subject, category, and dataset/split labels.

The manifest does not record an immutable upstream MMLU revision/commit or the exact upstream dataset snapshot. The local sample hash identifies the local sample bytes, not the upstream revision. Record the MMLU revision as unknown; the sampling manifest is otherwise sufficient to describe the local 50-question selection parameters and content identity.

### Scope and remaining gaps

- Unit 5 → held-out IoT test source identity: reconciled from local record metadata and evidence text.
- Dolly repository identity, seed, sample counts, assignment labels, and disjointness: recorded; immutable upstream revision and exact source-row selection remain unknown.
- MMLU repository identity, test split, 50-question sample, seed, category allocation, exclusions, and local sample hash: recorded; immutable upstream revision remains unknown.
- No new dataset/model payload inspection was performed for this step. Findings use existing owner-supplied local inspection/provenance records.
- These provenance findings do not establish copyright/licence permission or privacy clearance. All source rights remain unresolved where source terms are absent.
- No source files were moved, renamed, extracted, uploaded to cloud storage, or modified. `migration_authorized: false` remains unchanged.


## Additional local-code reconciliation — Dolly sampling implementation (2026-11-17)

The owner-provided project script `prepare_phase3_datasets_v2.py` was inspected as source code (not executed). It sets `DOLLY_DATASET = "databricks/databricks-dolly-15k"` and `SEED = 20261114`, calls `load_dataset(DOLLY_DATASET, split="train")` without a pinned `revision` argument, shuffles the full loaded row-index list with `random.Random(SEED)`, assigns the first 1,000 shuffled indices to B2 and the next 577 to B5 general, and asserts the two index sets are disjoint. It records counts/seed/disjointness in the output validation report, but the inspected code does not persist the selected upstream row indices or dataset revision.

This improves the transformation description: B2/B5 sampling is reproducible only if the exact upstream dataset snapshot and row ordering are independently recovered. Since the code does not pin a revision and no row-index manifest was found in the reviewed records, exact historical Dolly row selection cannot currently be reconstructed with certainty. Do not rerun the script or reload the dataset for this review.

The exact MMLU upstream revision remains unknown; its local 50-question sample manifest records the seed, exclusions, category counts, and local file hash but no upstream revision. The package's split manifest, validation report, and B2–B5 run metadata have not yet been directly reviewed as individual files; inspect those existing small metadata files next if supplied.
