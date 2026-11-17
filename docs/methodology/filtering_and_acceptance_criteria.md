# Filtering and Acceptance Criteria

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework
**Phase:** 9 — Filtering, semantic judging, human review, and evidence repair
**Evidence basis:** Historical scripts 45, 46, and 54; preserved filter, deduplication, and final reconciliation outputs.

## 1. Scope and evidence classification

This document reconstructs the filtering and acceptance logic from preserved source code and historical outputs. It does not claim that the historical scripts were rerun during Phase 9.

The reconstructed pipeline has three distinct decisions:

1. Heuristic validity filtering.
2. Explicit near-duplicate adjudication.
3. Semantic judge and evidence-provenance acceptance.

A record passing one stage is not automatically accepted by the next stage.

## 2. Heuristic filter — Script 45

Script 45 processes two raw input files in order. The historical filter report records:

- 88 records from the initial raw dataset.
- 27 additional records.
- 115 total input records.
- 115 heuristic-accepted records.
- 0 heuristic-rejected records.
- 8 near-duplicate candidate pairs.

The script checks:

- Required example identifiers.
- Non-empty instruction and response.
- Minimum instruction and response lengths.
- Membership of the referenced chunk ID in the known frozen chunk set.
- Refusal-like response phrases.
- Evidence block identifiers and evidence reconstruction.
- Duplicate example IDs.
- Exact duplicates after instruction/response normalization.

For exact normalized instruction-response duplicates, the first encountered record is retained and the later duplicate is rejected. Input-file order therefore affects which record survives.

### 2.1 Near-duplicate thresholds

The script flags a pair for manual review when either condition is met:

- SequenceMatcher similarity >= 0.82; OR
- Token Jaccard similarity >= 0.72.

These thresholds create review candidates. They do not automatically reject records.

The historical CSV contains eight flagged pairs. The filter report records zero automatic rejections and all eight pairs as pending manual review at that stage.

### 2.2 Evidence reconstruction

The heuristic implementation splits source text into blocks using blank-line boundaries and retains blocks at least 30 characters long. Evidence identifiers are checked against the reconstructed block list.

This is a structural provenance check. It does not independently establish that every factual statement in a response is entailed by the cited evidence.

## 3. Manual near-duplicate adjudication — Script 46

The deduplication stage receives 115 heuristic-accepted candidates and records five exclusions, leaving 110 candidates.

The five excluded IDs are:

- `production_batch_033_example_03`
- `production_batch_011_example_03`
- `production_batch_024_example_02`
- `production_batch_024_example_03`
- `production_batch_024_example_04`

Three pairs were explicitly retained as distinct:

- WAMP Pub/Sub Router/Broker versus RPC Router/Dealer.
- AWS versus Skynet.
- Skynet versus Google Compute Engine.

The retained representative IDs recorded in the decisions include:

- `production_batch_009_example_01`
- `production_batch_024_example_01`
- `production_batch_011_example_04`
- `production_batch_016_example_03`
- `production_batch_016_example_04`

The original input order is preserved.

The decision provenance field says “Explicit user approval in conversation.” This is a recorded provenance label; it is not an independently audited approval record.

The human-audit note for `production_batch_011_example_03` refers to a record already excluded from the 110-candidate reconciliation input. It must not be counted as one of the five final reconciliation rejections.

## 4. Semantic and evidence acceptance

The final reconciliation stage applies semantic judge outcomes and evidence provenance checks. The recovered final output contains:

- 110 reconciled candidates.
- 105 accepted.
- 5 rejected.
- 95.45% accepted among the 110 candidates.

A record is accepted only when the final reconciliation requirements are satisfied, including:

- Exact evidence reconstruction against the frozen source corpus.
- Faithfulness score >= 4.
- Evidence relevance confirmed.
- Unsupported claims explicitly absent.
- Answer correctness confirmed.
- Answer completeness confirmed.
- A usable judge decision and candidate mapping.

Missing judge results or provenance failures are not silently treated as accepted.

The five rejected candidate IDs are:

- `production_batch_006_example_02`
- `production_batch_008_example_03`
- `production_batch_010_example_03`
- `production_batch_017_example_03`
- `production_batch_019_example_02`

All five have faithfulness scores below 4. Additional rejection reasons overlap; the reason counts are not mutually exclusive.

## 5. Rejection and uncertainty categories

The final report records these overlapping rejection reason counts:

| Reason | Records |
|---|---:|
| Faithfulness below 4 | 5 |
| Unsupported claims not explicitly false | 5 |
| Answer correctness not confirmed | 4 |
| Answer completeness not confirmed | 4 |
| Evidence relevance not confirmed | 1 |

These are reason incidences, not unique record counts.

Potential false positives include records that pass heuristic checks but contain unsupported or incorrect claims. The five final judge rejections demonstrate why structural filtering alone is insufficient.

Potential false negatives and unresolved cases cannot be quantified from the preserved aggregate reports alone. No claim is made that all semantically weak records were identified.

## 6. Human review limitation

The final summary reports a 30-example human audit, with 29 accepted and one rejected. The rejected ID is `production_batch_011_example_03`, which had already been excluded from the 110-candidate final reconciliation input.

The inspected evidence did not establish an independent reviewer register, sampling manifest, completed annotation sheet, or reviewer identity/independence record. Therefore:

- Treat 29/30 as a reported historical summary.
- Do not treat it as independently verified human validation.
- Do not infer that the final 105 accepted records were human-approved.
- Do not claim reviewer independence or representative sampling.

The separate Phase 8 audit preparation had 30 rows and zero verdicts; it is not the same evidence as the Phase 9 summary and must not be conflated with it.

## 7. Reproducibility boundary

The final inclusion logic is reconstructable from preserved scripts and outputs, subject to the limitations documented in the Phase 9 report.

No source dataset, frozen chunk, judge result, or historical output is modified by this documentation.
