# Phase 9 Report — Filtering, Semantic Judging, Human Review, and Evidence Repair

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework
**Phase:** 9 — Reconstruct filtering, semantic judging, human review, and evidence repair
**Status:** Completed with caveats; historical decisions reconstructed from preserved artifacts.

## Objective

Reconstruct the acceptance logic and supporting evidence for the filtered candidate pool. Document heuristic filtering, deduplication, judge reconciliation, evidence repairs, human-review records, and unresolved decision provenance.

## Verified candidate lineage

| Stage | Records |
|---|---:|
| Initial candidate inputs | 88 + 27 = 115 |
| Heuristic-filter accepted | 115 |
| Heuristic-filter rejected | 0 |
| Near-duplicate pairs flagged for review | 8 |
| Deduplication exclusions | 5 |
| Deduplicated candidate pool | 110 |
| Final accepted | 105 |
| Final rejected | 5 |
| Final decision audit records | 110 |

The heuristic filter's fuzzy thresholds were SequenceMatcher >= 0.82 or token Jaccard >= 0.72. These thresholds flagged candidates for manual review; they did not automatically reject them. Exact normalized instruction-response duplicates were handled separately. Input order was preserved, with the first occurrence retained.

Deduplication excluded five records:

- `production_batch_033_example_03`
- `production_batch_011_example_03`
- `production_batch_024_example_02`
- `production_batch_024_example_03`
- `production_batch_024_example_04`

Eight near-duplicate pairs were reviewed; three distinct pairs were retained. The recorded decision provenance says "Explicit user approval in conversation"; the underlying approval evidence was not independently audited during this reconstruction.

## Judge reconciliation

Scripts 47 and 48 were compared. Both match candidate IDs to original Groq and pilot judge records, prioritizing the original source. Script 47 reads frozen chunk text from `text`; script 48 reads `content`, consistent with the upstream chunk representation. Script 48 also contains the corrected Skynet classification mapping and marks the affected pilot judgment for rejudgment.

Script 54 performs final reconciliation using source priorities: original Groq, pilot Groq, repair-v1 Groq, and repair-v2 HMA. It applies the recorded score and evidence criteria and produces 105 accepted and 5 rejected decisions.

The reconstructed final audit contains 110 unique candidate decisions, with no missing candidate-to-audit mappings. Judge-source counts across all audit records are original Groq 79, pilot Groq 26, repair-v1 Groq 4, and repair-v2 HMA 1. Accepted-only source counts are 74, 26, 4, and 1 respectively; the difference is the five rejected original-Groq records.

## Evidence repair

Repair-v1 changed evidence for four candidate records. The response text changed only for `production_batch_015_example_04`; the other three retained their instruction and response text. All four were marked for judge reevaluation.

Repair-v2 added evidence block 5 to `production_batch_013_example_03`, whose evidence IDs became [4, 6, 7, 8]. Its instruction and response remained unchanged. Phrase coverage and exact evidence reconstruction were recorded, but phrase coverage alone does not prove every response claim is supported.

The repair-v1 judge record contains five completed decisions: four accepted and one rejected. The HMA repair-v2 judge record contains one completed accepted decision. These are historical records; the judge scripts were not rerun.

## Final rejected candidates

| Candidate ID | Judge source | Score | Recorded rejection issues |
|---|---|---:|---|
| `production_batch_006_example_02` | Original Groq | 3 | Below threshold; unsupported claims; incorrect and incomplete |
| `production_batch_008_example_03` | Original Groq | 3 | Below threshold; unsupported claims |
| `production_batch_010_example_03` | Original Groq | 3 | Below threshold; irrelevant evidence; unsupported, incorrect, incomplete |
| `production_batch_017_example_03` | Original Groq | 2 | Below threshold; unsupported, incorrect, incomplete |
| `production_batch_019_example_02` | Original Groq | 3 | Below threshold; unsupported, incorrect, incomplete |

Issue counts overlap and must not be interpreted as mutually exclusive categories.

## Human-review evidence and discrepancy

The preserved human-audit CSV contains 30 rows: 28 ACCEPT and 2 REJECT. The separate `human_audit_rejected.jsonl` contains the same two rejected records:

- `production_batch_001_example_01`: reviewer notes identify an unsupported TCP-per-request claim.
- `production_batch_004_example_02`: reviewer notes identify a non-actionable instruction and a response that repeats it.

Both records have `pool_source` marked `previously_validated`. They are not established as members of the final 110-candidate pool. Both are marked ACCEPT in the final candidate judge audit; this is not treated as a contradiction in the same pool.

The historical final summary instead reports 30 reviewed, 29 accepted, and one rejected (`production_batch_011_example_03`). That claim is not supported by the inspected CSV or rejected JSONL. The named record was already excluded during deduplication. The discrepancy is retained as an unresolved historical summary defect; the summary must not be used as the authoritative human-review count.

Reviewer identity, reviewer-selection procedure, blinding, and independence were not established. The review cannot be characterized as an independent evaluation.

## Error analysis and limits

The five final rejected records are judge-based rejections, not independently adjudicated false positives. No independent gold-standard labels were established for the final candidate pool. Consequently, false-positive rates, false-negative rates, precision against human ground truth, and recall against human ground truth cannot be calculated from the available evidence.

The located `v2_judge_results.jsonl` artifact contains 66 records. Its identity as the same source as the historical 88-record original Groq judge dataset was not established. This source ambiguity remains open.

Scripts 45–54 and their relevant helpers were inspected, not executed. The historical output files were reconciled without rerunning generation, filtering, repair, or judge operations. No provider APIs were called.

## Deliverables

- `docs/methodology/filtering_and_acceptance_criteria.md`
- `docs/methodology/semantic_judging_and_evidence_repair.md`
- `reports/validation/judge_reconciliation.json`
- `reports/metrics/filter_and_judge_summary.csv`
- `docs/phase_reports/PHASE_09_REPORT.md`
- `reports/validation/phase_09_validation.json`
- `manifests/phase_09_outputs.json`

## Preservation boundary

No source datasets, frozen chunks, candidate source files, judge outputs, human-review source records, or historical repair outputs were modified. No generation, filtering, repair, or judge scripts were executed. No paid or external provider APIs were called.

## Completion decision

Phase 9 is completed with caveats as a historical reconstruction. The 110-candidate final decision mapping is complete and reconciled to 105 accepted and 5 rejected records. The historical human-review summary discrepancy, reviewer-independence limitations, unavailable gold-standard error rates, and source-provenance ambiguity remain explicitly unresolved. These limitations do not justify inventing or silently changing historical decisions.
