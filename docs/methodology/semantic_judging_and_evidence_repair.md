# Semantic Judging and Evidence Repair

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework
**Phase:** 9 — Filtering, semantic judging, human review, and evidence repair
**Evidence basis:** Historical scripts 47–54, reconciliation reports, repair reports, judge result files, and final audit outputs.

## 1. Purpose

This document reconstructs how candidate records were matched to semantic judge outputs, how evidence provenance was corrected, and how final acceptance decisions were made.

The reconstruction uses preserved code and outputs. Historical judge scripts were not executed again during Phase 9.

## 2. Judge-to-candidate reconciliation

### 2.1 Original and corrected implementations

Two reconciliation variants were inspected:

- Script 47: reconciliation v1.
- Script 48: reconciliation v2.

Both use candidate IDs to locate judge records and prioritize the original judge output over the pilot judge output when both are available.

The critical implementation difference is frozen-source text retrieval:

- Script 47 reads the frozen chunk `text` field.
- Script 48 reads the frozen chunk `content` field.

The upstream frozen chunk generator uses `content`. The v1 field mismatch caused evidence provenance failures.

### 2.2 Reconciliation v1 result

The v1 report records:

- 110 candidate records.
- 109 `PROVENANCE_REVIEW_REQUIRED`.
- 1 `REJUDGE_REQUIRED`.
- 0 provenance-verified records.

The issue was recorded as `evidence_block_id_out_of_range`.

### 2.3 Reconciliation v2 result

The corrected v2 report records:

- 110 candidate records.
- 100 `JUDGE_ACCEPTED`.
- 9 `JUDGE_REJECTED`.
- 1 `REJUDGE_REQUIRED`.
- 110 provenance-verified records.
- No remaining provenance issues in that reconciliation report.

The Skynet classification example was corrected following the recorded human-audit correction:

- Example ID: `improved_iot_cloud_case_studies_chunk_0014_classification`.
- The prior pilot judgment was invalidated.
- The record was marked `REJUDGE_REQUIRED`.

The corrected instruction asks for the platform model and cloud deployment description explicitly stated for Skynet. The corrected response identifies IoT platform-as-a-service and private-cloud deployment through Docker.

### 2.4 Matching limitations

The reconciliation implementations use stable example IDs, but have limitations:

- A pilot result without judged text can be marked text-matched based on ID alone. This does not prove that the text judged by the pilot was identical to the candidate text.
- Cross-source duplicate-ID collisions are not explicitly rejected; original-source priority can take precedence.
- The reconciliation reports establish mapping and provenance checks, not independent semantic correctness.

## 3. Evidence repair v1

Script 49 repairs four candidate records using the frozen source chunks and selected source blocks.

Target IDs:

- `production_batch_011_example_04`
- `production_batch_012_example_04`
- `production_batch_013_example_03`
- `production_batch_015_example_04`

The repair report records exact evidence reconstruction for all four records and marks them for judge reevaluation.

For three records, the instruction and response remain unchanged. For `production_batch_015_example_04`, the response is changed to describe the IoT Level 5 system as multiple end nodes and one coordinator node, with the coordinator collecting data and sending it to the cloud.

The repair method checks phrase coverage and reconstructs evidence spans. Phrase coverage is not proof that every response claim is supported.

## 4. Repair v1 semantic judge

Script 50 evaluates the four repaired records plus the Skynet record.

The source code specifies:

- Provider endpoint: Groq.
- Model: `openai/gpt-oss-120b`.
- Temperature: 0.
- Maximum tokens: 1,800.
- Timeout: 180 seconds.
- Maximum retries: 4.
- Retry delay: 20 seconds.

The strict acceptance criteria require a faithfulness score of at least 4, relevant evidence, no unsupported claims, a correct answer, and a complete answer.

The preserved judge summary reports:

- 5 targets.
- 5 completed.
- 4 accepted.
- 1 rejected.
- 0 pending.
- 0 failures in that recorded run.

Accepted records:

- `production_batch_012_example_04`
- `improved_iot_cloud_case_studies_chunk_0014_classification`
- `production_batch_011_example_04`
- `production_batch_015_example_04`

Rejected record:

- `production_batch_013_example_03`

The rejected record received score 2; evidence relevance was true, but unsupported claims were present and correctness was false.

The script appends results and skips IDs already marked completed when resuming. Duplicate result lines are not removed; its summary uses the latest result per ID.

## 5. Human-review-specific HMA repair v2

Script 51 targets only `production_batch_013_example_03`.

It adds evidence block ID 5 to the existing IDs 4, 6, 7, and 8. The instruction and response remain unchanged.

The repair report records phrase coverage and exact reconstruction as verified. It marks the example for a fresh judge evaluation.

This is a repair of evidence selection, not a rewrite of the answer.

## 6. HMA judge variants

Scripts 52 and 53 both judge the single HMA-repaired example using the Groq endpoint and `openai/gpt-oss-120b`.

Both use the strict acceptance criteria. The preserved configuration specifies temperature 0, maximum tokens 1,200, and timeout 180 seconds.

The variants differ in source retrieval:

- Script 52 expects `full_source_chunk` or `source_chunk` fields in the candidate record. Script 51 does not add these fields, so compatibility is not established from those scripts alone.
- Script 53 retrieves the frozen chunk by unique `chunk_id` from `chunks_v1_frozen.jsonl` and records source retrieval in the result/summary.

Script 53 is the corrected retrieval variant.

Neither variant has resume/checkpoint behavior. Both overwrite the result file, and neither independently verifies that the evidence block IDs reconstruct the source.

The preserved HMA judge summary reports one completed and accepted record with mean score 5. This is historical output evidence; the judge was not rerun during this reconstruction.

## 7. Final reconciliation — Script 54

Script 54 combines:

- Repair v2 candidate records.
- Frozen source chunks.
- Original Groq judge results.
- Pilot Groq judge results.
- Repair v1 judge results.
- Repair v2 HMA judge results.

The recorded priority order is:

| Source | Priority |
|---|---:|
| Original Groq | 10 |
| Pilot Groq | 10 |
| Repair v1 | 20 |
| Repair v2 HMA | 30 |

The highest-priority result is selected per example; later rows from the same source supersede earlier rows.

Final acceptance requires exact evidence reconstruction against the frozen corpus, faithfulness score >= 4, relevant evidence, no unsupported claims, correctness, and completeness. Missing judge results or provenance issues lead to rejection.

The script hard-codes an expected candidate count of 110. It does not reject duplicate frozen chunk IDs; the last duplicate silently wins. Its status check can accept a judge result with a missing status field if the other conditions pass. These are implementation limitations.

The script also writes a hard-coded human audit summary of 30 examples, 29 accepted, and one rejected (`production_batch_011_example_03`). It does not load an independent human audit record. This reported audit summary must therefore be distinguished from independently verified human-review evidence.

## 8. Final decision totals

The preserved final reconciliation summary records:

| Outcome | Records |
|---|---:|
| Candidates | 110 |
| Accepted | 105 |
| Rejected | 5 |
| Acceptance rate | 95.45% |

Accepted judge-source counts in the final summary:

- Original: 74.
- Pilot: 26.
- Repair v1: 4.
- Repair v2 HMA: 1.

The audit output's source counts include accepted and rejected records, so its source totals differ from the accepted-only summary. This is expected and should not be interpreted as a mismatch.

The five final rejections all came from the original judge source.

## 9. Review independence and error categories

The available evidence does not establish:

- Independent human reviewer identities.
- A reviewer blinding procedure.
- An independently preserved sampling manifest.
- Completed reviewer annotations supporting the 29/30 summary.
- A second independent semantic judge.
- Exhaustive false-positive or false-negative adjudication.

The final five rejected examples are observed false-positive risks in the upstream candidate pool: they passed earlier stages but failed final semantic acceptance.

False negatives cannot be measured from the preserved reports because rejected heuristic records and independently adjudicated missed cases are not available as a complete labelled reference set.

Unresolved evidence includes the lack of an independent human audit register and the implementation-specific weaknesses described above.

## 10. Execution and preservation boundary

Phase 9 is a historical reconstruction. No original filtering, reconciliation, repair, or judge script was executed; no provider API was called; and no source dataset, frozen chunk, checkpoint, judge result, or historical evaluation output was modified.
