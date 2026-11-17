# Source Document Processing

## Scope

This document records the observed source-document extraction, empty-page diagnosis, vision recovery, and page-merging process for the ML CP project.

The evidence is based on the existing extraction JSONL, recovery JSONL files, merge JSONL, and recorded logs. Historical processing scripts were not rerun to produce this document.

## Source documents

| Document ID | Source PDF | Pages |
|---|---|---:|
| `iot_unit1` | `IOT Unit 1 Contents.pdf` | 151 |
| `iot_unit2` | `Unit 2-Iot-platform-design-methodology (1).pptx.pdf` | 60 |
| `iot_unit4_protocols_security` | `4-iot-protocols-and-security.pdf` | 119 |
| `iot_cloud_case_studies` | `6-iot-physical-servers-cloud-offereings-iot-case-studies.pdf` | 99 |
| **Total** | **4 documents** | **429** |

The source files are registered in the active `ML CP` workspace. Their author, publisher, edition, canonical source URL, and license are not established by the available evidence. Redistribution has not been cleared.

## Text extraction

The existing extraction artifact is:

`data/extracted/extracted_text.jsonl`

Each record includes:

- `doc_id`
- `source_file`
- `page_number`
- `text`
- `char_count`
- `is_empty`

Observed extraction results:

| Document ID | Total pages | Nonempty pages | Initially empty pages |
|---|---:|---:|---:|
| `iot_unit1` | 151 | 130 | 21 |
| `iot_unit2` | 60 | 55 | 5 |
| `iot_unit4_protocols_security` | 119 | 112 | 7 |
| `iot_cloud_case_studies` | 99 | 96 | 3 |
| **Total** | **429** | **393** | **36** |

The overall nonempty extraction rate is 91.61%.

## Empty-page diagnosis and recovery

The diagnostic log records inspection of the 36 initially empty pages. It reports embedded images and vector drawings. Those counts are not mutually exclusive page categories.

The recovery artifacts are:

- `data/recovered/recovered_image_pages.jsonl`
- `data/recovered/recovery_errors.jsonl`

The successful recovery file contains 19 records:

- 14 meaningful vision recoveries.
- 5 records classified as blank and not meaningful.

All 19 records map to corresponding merged-page records. The 14 meaningful recoveries are usable; the five confirmed blanks remain unusable.

The recovery error file contains 18 records representing 17 unique failed page references. `iot_unit1` page 131 occurs twice. The quota-aware recovery log records a subsequent HTTP 402 billing/prepayment failure and states that processing stopped without further API requests.

No additional paid API calls or recovery runs are part of this phase's evidence reconstruction.

## Merged page corpus

The existing merge artifact is:

`data/processed/merged_pages.jsonl`

It contains 429 records and uses the following content classifications:

| Content status | Records | Usable |
|---|---:|---|
| `text_extracted` | 393 | Yes |
| `vision_recovered` | 14 | Yes |
| `confirmed_blank` | 5 | No |
| `unrecovered_image_page` | 17 | No |
| **Total** | **429** | **407 usable** |

The resulting usable page count is:

`393 extracted-text pages + 14 meaningful vision recoveries = 407 usable pages`

The unusable page count is:

`5 confirmed blanks + 17 unrecovered image pages = 22 unusable pages`

The four source documents have no duplicate `(doc_id, page_number)` keys in the extraction or merged artifacts. All successful recovery records map to the merged corpus without a detected mismatch.

## Historical log discrepancy

The first recovery log describes 36 attempted pages, 19 successful records, and 17 failed records. A later quota-aware log reports 36 original image-only pages, five confirmed blanks excluded, 19 previously recovered records, and 17 remaining pages. These historical statements do not reconcile arithmetically.

The final merged corpus provides the authoritative page-level classification used here: 14 meaningful vision recoveries, five confirmed blanks, and 17 unrecovered image pages. The historical log wording is retained as an evidence limitation rather than silently corrected.

## Source rights and limitations

The source PDF bibliographic metadata and licenses remain unknown. Redistribution rights are not cleared. The recovered descriptions are model-generated interpretations and may contain uncertainty, particularly for diagrams, screenshots, and partially legible labels.

No claim is made that all visual information was recovered or that the 17 unrecovered pages contain no useful information.