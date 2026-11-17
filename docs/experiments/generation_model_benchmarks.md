# Phase 7 — Generation model experiments and production configuration

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework
**Evidence cutoff:** 17 November 2026
**Status:** Reconstructed from recovered source code and historical artifacts; production execution is evidenced, but some runtime parameters were not persisted.

## 1. Executive summary

The recovered production generator used **`nvidia/nemotron-3.5-super-vl:free` through OpenRouter**. The final V2 dataset contains **485 records**, covering all **91 frozen chunks** and all three task types. The production run manifest records two passes, 546 theoretical candidate slots, a similarity threshold of 0.88, and zero request errors. The run summary reports 104 new records added to a prior V2 baseline of 381.

The production dataset was evaluated by a separate Groq-hosted judge, **`openai/gpt-oss-120b`**, across all 485 records: 474 accepted and 11 rejected (97.73% accepted), with mean faithfulness 4.971/5. A separate 66-example judging run yielded 65 accepted and one rejected; it is a distinct subset/run and must not be added to the 485-example totals.

The structural audit reports `PASS_STRUCTURAL_AUDIT`: 485 unique example IDs, coverage of all 91 chunks, 485 examples with exact evidence verified, no missing/invalid evidence IDs, no flagged duplicate pairs at threshold 0.88, zero audit errors, and zero warnings. This is structural/evidence validation plus automated model judging; it is not equivalent to independent human semantic validation of all 485 examples.

## 2. Evidence classes and interpretation

- **Execution-confirmed:** values directly present in run manifests, summaries, output records, judge results, or audit summaries.
- **Source-confirmed default:** a value present in the recovered production script, but not independently recorded as the runtime argument.
- **Unknown:** not established by the recovered artifacts. Do not infer it from defaults.
- **Exploratory:** a smoke test or small benchmark; not the production run.

## 3. Recovered production generator

### 3.1 Identity and input/output

- Script: `scripts/60_generate_production_v2_resumable.py`
- SHA-256: `D55C9E1D28209EE9E38DFA496F60C47B768281CFD7AC0554861EE23C381D25B4`
- Endpoint: `https://openrouter.ai/api/v1/chat/completions`
- Model in run manifest and all 485 output records: `nvidia/nemotron-3.5-super-vl:free`
- Input: `data/frozen/chunks_v1_frozen.jsonl`
- Frozen corpus SHA-256 in manifest and audit: `67e90d3428ff0a421111e19916ceb2dfc007460ae047f18131131be2f80bb827`
- Output: `data/interim/production_generation_v2/dataset_v0_additional_v2_resumed.jsonl`
- Checkpoints: `data/interim/production_generation_v2/checkpoints/`
- Recovered seed file: `data/interim/production_generation_v2/dataset_v2_recovered_20261113.jsonl`

### 3.2 Runtime settings versus script defaults

| Setting | Recovered value | Evidence classification |
|---|---|---|
| Model | `nvidia/nemotron-3.5-super-vl:free` | Execution-confirmed |
| Provider / endpoint | OpenRouter chat completions | Source-confirmed; endpoint in script |
| Passes | 2 | Execution-confirmed in run manifest |
| Selected chunks | 91 / 91 | Execution-confirmed |
| Task types | QA, extraction, classification | Execution-confirmed in manifest and output |
| Similarity threshold | 0.88 | Execution-confirmed in manifest |
| Temperature | 0.35 | Source default; runtime override not ruled out |
| Maximum output tokens | 5000 | Source default; runtime override not ruled out |
| Request timeout | 180 seconds | Source default; runtime override not ruled out |
| Maximum retries | 3 retries after initial attempt | Source default; runtime override not ruled out |
| Retry sleeps | 8, 16, 24 seconds, capped at 45 seconds | Source implementation |
| Inter-request delay | 15 seconds | Source default; runtime override not ruled out |
| Top-p | Not specified in recovered generator source evidence | Unknown / not configured in recovered excerpt |
| Reasoning effort | Not established for production generator | Unknown |
| Runtime command line | Not preserved in supplied manifest | Unknown |

The run manifest does not record temperature, max tokens, timeout, retry count, delay, or a full command line. Those are therefore documented as script defaults, not asserted as proven runtime values.

### 3.3 Prompt and schema

The production system prompt instructs the model to create source-grounded technical IoT instruction/response examples and return one JSON object with an `examples` array. Each example contains:

- `task_type`: `qa`, `extraction`, or `classification`
- `instruction`
- `response`
- `evidence_block_ids`: numeric IDs corresponding to source blocks

The model is asked for up to three examples per chunk/pass: one of each task type when supported. Unsupported task types should be omitted and recorded in `skipped` with a reason. The prompt prohibits outside facts, unsupported claims, broad unrelated questions, trivial/duplicate questions, and repetition of previously generated questions from the same chunk. It requests valid JSON only.

The generator builds a per-chunk prompt including source document identifier, chunk ID, pass focus, numbered evidence blocks, and previously generated questions for that chunk. Four distinct pass-focus descriptions exist in the source; the historical run manifest confirms only passes 1 and 2 were selected.

The recovered code validates returned JSON and fields, checks evidence IDs against the source blocks, and uses evidence spans in output records. It rejects invalid/unsupported candidates and applies a global near-duplicate check using the 0.88 similarity threshold. The exact full runtime prompt payload, response-format parameter, and any provider-side constrained decoding setting are not independently preserved in the run manifest.

### 3.4 Resumption and safety behavior

- One model request per chunk/pass.
- Checkpoint identity is chunk ID plus pass number.
- Existing completed checkpoints are skipped on resume unless retry-skipped behavior is explicitly requested.
- Failed requests are retried up to the configured maximum with bounded waits.
- Per-pass checkpoint files record chunk ID, pass number, status, accepted count, skipped information, and completion timestamp.
- Output appends accepted records; the script documents that it does not replace the existing V2 dataset or mutate the frozen corpus.
- The run summary reports original raw and prior additional datasets as read-only and confirms the frozen corpus was not modified.

## 4. Production execution results

| Measure | Recovered result |
|---|---:|
| Frozen chunks | 91 |
| Selected chunks | 91 |
| Passes | 2 |
| Theoretical candidate slots | 546 |
| Final V2 records | 485 |
| New examples added this run (run summary) | 104 |
| Previous V2 examples (run manifest) | 381 |
| Model skips / validation rejections (run summary) | 12 |
| Global duplicate rejections (run summary) | 4 |
| Request errors | 0 |
| Completed passes reported by run summary | 40 |
| Stopped early | No |
| Output batch label `production_v2_pass_01` | 251 records |
| Output batch label `production_v2_pass_02` | 234 records |

Task distribution in final output:

- QA: 166
- Extraction: 161
- Classification: 158

The output records identify the generator model on all 485 rows. The recovered 73-record seed file has 73/73 IDs present in the final output. The prior additional dataset contains 27 records and is recorded as read-only input.

### 4.1 Explicit reconciliation caveat

The checkpoint directory contains 182 files: 91 for pass 1 and 91 for pass 2. Status distribution is 91 pass-1 complete, 89 pass-2 complete, and 2 pass-2 `no_examples_accepted`. The checkpoint `accepted_count` values sum to **483** (pass 1: 249; pass 2: 234), while the final output contains **485** records (pass 1 batch label: 251; pass 2 batch label: 234). The two-record difference is unresolved.

The run manifest says 381 previous V2 examples and the summary says 104 new examples, which reconcile to 485. The checkpoint totals do not independently reconcile to the output totals. Preserve both recorded figures; do not silently adjust them. The script's checkpoint counts may represent per-pass accepted additions rather than all records carried into the output, but the available evidence does not establish the precise explanation.

## 5. Exploratory model experiments

### 5.1 Smoke tests

**Script 18 — `18_test_structured_generation.py`**
- Model: `nvidia/nemotron-3.5-lightning:free`
- One frozen chunk, one example
- Temperature 0.2, max tokens 1200, reasoning effort `none`
- Output: `data/interim/generation_smoke_test.json`
- Captured result: one example; evidence block ID 10; exact evidence substring check true; 817 prompt tokens and 77 completion tokens; reported cost 0.

**Script 19 — `19_test_batch_generation.py`**
- Model: `nvidia/nemotron-3.5-lightning:free`
- First two chunks; two examples per chunk
- Temperature 0.2, max tokens 2500, reasoning effort `none`
- Output: `data/interim/batch_generation_smoke_test.json`
- Captured result: four examples; all four exact evidence substring checks true; 1,467 prompt and 338 completion tokens; reported cost 0.

These are functional smoke tests, not comparative quality evaluations.

### 5.2 Small model comparison

**Script 22 — `22_benchmark_model_quality.py`**
- Models: `google/gemma-4-26b-a4b-it:free`, `dots-studio/dots-3-note-preview:free`, `nvidia/nemotron-3.5-super-vl:free`, `nvidia/nemotron-3.5-lightning:free`
- Two chunks, one request per model/chunk, max tokens 1800
- Output: `data/interim/model_quality_benchmark.json`
- Captured results: Super VL succeeded on both requests; Gemma failed on both, Dots failed on both, Lightning failed on both.
- Total: 2 successful and 6 failed requests.

This is an eight-request operational smoke benchmark, not a statistically or semantically rigorous quality benchmark. Failure reasons and latency detail should be taken from the raw JSON artifact, not inferred from the summary table.

### 5.3 Super VL batch scaling tests

**Script 24 — `24_test_supervl_multi_chunk.py`**
- Model: `nvidia/nemotron-3.5-super-vl:free`
- Four chunks, one from each of four documents; two examples per chunk
- Max tokens 5000; timeout 180 seconds
- Output: `data/interim/supervl_multi_chunk_test.json`
- Captured result: 8 examples, 4 chunks, 4 documents; latency 92.41 seconds; 2,810 prompt and 3,909 completion tokens.

**Script 26 — `26_test_supervl_large_batch.py`**
- Same model
- Eight chunks, two from each of four documents; two examples per chunk
- Max tokens 9000; timeout 240 seconds
- Output: `data/interim/supervl_large_batch_test.json`
- Captured result: 16 examples; latency 67.54 seconds; 5,408 prompt and 5,641 completion tokens.

The two tests demonstrate successful larger structured responses in those captured runs. Their different chunk counts, token limits, and prompts mean latency and output counts should not be interpreted as a controlled head-to-head comparison.

### 5.4 Connectivity and account diagnostics

- Script 15 tested Google GenAI connectivity using `gemini-3.8-flash`; it was not an IoT dataset generation benchmark.
- Script 16 tested OpenRouter connectivity using the `openrouter/free` route; it was not a dataset generation benchmark.
- Script 17 queried OpenRouter key/free-tier usage counters; it was an account diagnostic.
- Script 21 tested several candidate models using a short fixed WebSocket source and unstructured QUESTION/ANSWER/SUPPORTING EVIDENCE output. It was exploratory and is not a production-quality benchmark.

## 6. Production judging and audit

### 6.1 Full pipeline judge

- Script: `scripts/pipeline_judge.py`
- SHA-256: `2833DED2C694BFD68865632928AD7A268BC759C57BCF4C73A6224BFD34CE2D0A`
- Provider: Groq
- Endpoint: `https://api.groq.com/openai/v1/chat/completions`
- Judge model: `openai/gpt-oss-120b`
- Generator model recorded: `nvidia/nemotron-3.5-super-vl:free`
- Temperature: 0
- Maximum completion tokens: 1200
- Reasoning effort: `low`
- Response format: JSON object
- Judge retries: bounded retry loop; per-example results appended for resumption
- Default input: manually reviewed V2 dataset; pipeline environment variables can override input/output locations.

Observed full-run summary (`pipeline_judge/v2_judge_summary.json`):
- Input: 485
- Judged: 485
- Pending: 0
- Accepted: 474
- Rejected: 11
- Mean faithfulness: 4.971
- Minimum faithfulness: 2
- Errors this run: 0
- Acceptance rule: faithfulness >= 4 AND relevant AND correct AND complete AND evidence_supports_answer AND NOT unsupported_claims

Acceptance rate: 474 / 485 = 97.73%. This is an automated judge result, not a human-reviewed acceptance rate.

### 6.2 Separate 66-example judge run

`groq_judge/v2_judge_summary.json` records a separate run:
- Input/judged: 66
- Accepted: 65
- Rejected: 1
- Mean faithfulness: 4.97
- Minimum faithfulness: 3

Do not add these 66 results to the 485 full-run results. The artifacts identify distinct output directories and run summaries.

### 6.3 Structural audit

`audit_v1/audit_summary.json` reports:
- Status: `PASS_STRUCTURAL_AUDIT`
- Frozen chunks: 91; unique IDs: 91; duplicate chunk IDs: none
- V2 records: 485; unique example IDs: 485; duplicate example-ID groups: 0
- Chunk coverage: 91
- Exact evidence verified: 485/485
- Missing/invalid evidence ID rows: 0
- Evidence reconstruction/source failures: 0
- Near/exact duplicate pairs flagged at threshold 0.88: 0
- Missing required-field rows: 0
- Invalid/missing task-type rows: 0
- Audit errors: 0
- Audit warnings: 0

This establishes the checks implemented by the recovered structural auditor. It does not prove that every answer is semantically correct, that no subtle hallucinations exist, or that a human reviewed every record.

## 7. Production selection rationale and limitations

The recovered evidence supports the following bounded rationale:

1. Lightning was used for the earliest structured-generation smoke tests, but the four-model comparison recorded failures for both Lightning requests and both successful Super VL requests.
2. Super VL then completed the four-chunk and eight-chunk batch tests.
3. The production generator source default, production run manifest, and all final output records consistently identify Super VL as the production generator.
4. The production dataset subsequently passed the recorded structural audit and received 474 automated ACCEPT verdicts from the 485-example Groq judge.

The evidence does **not** establish a rigorous comparative semantic-quality victory over all candidate models. The model comparison was small, operational, and not controlled for all settings. No complete human-evaluation comparison across candidate models was recovered. The production choice is therefore evidenced by operational success, structured-output behavior, and subsequent pipeline execution—not by a statistically robust benchmark.

## 8. External API dependencies and cost boundary

- Generation depends on OpenRouter and `OPENROUTER_API_KEY`.
- Judging depends on Groq and `GROQ_API_KEY`.
- The exploratory smoke-test records report zero cost and `is_byok=false` for the captured free-route calls. This does not establish that all historical or future requests are free.
- Reconstruction of this phase requires no provider calls. Do not rerun generator, judge, or benchmark scripts as part of documentation reconstruction.
- Any future generation/judging run may consume provider quota or incur cost depending on route, account, provider policy, and current pricing. No cost estimate is asserted here.

## 9. Artifact provenance index

| Artifact ID | Relative path | Purpose |
|---|---|---|
| P7-SRC-GEN | `scripts/60_generate_production_v2_resumable.py` | Production generator source |
| P7-SRC-AUDIT | `scripts/61_audit_generation_v2.py` | Structural auditor source |
| P7-SRC-JUDGE | `scripts/pipeline_judge.py` | Groq judge source |
| P7-IN-FROZEN | `data/frozen/chunks_v1_frozen.jsonl` | Frozen input corpus |
| P7-OUT-SMOKE1 | `data/interim/generation_smoke_test.json` | Lightning single-example smoke output |
| P7-OUT-SMOKE2 | `data/interim/batch_generation_smoke_test.json` | Lightning batch smoke output |
| P7-OUT-MODEL-BENCH | `data/interim/model_quality_benchmark.json` | Four-model operational comparison |
| P7-OUT-SUPERVL-4 | `data/interim/supervl_multi_chunk_test.json` | Super VL four-chunk test |
| P7-OUT-SUPERVL-8 | `data/interim/supervl_large_batch_test.json` | Super VL eight-chunk test |
| P7-IN-SEED | `data/interim/production_generation_v2/dataset_v2_recovered_20261113.jsonl` | 73-record recovered seed |
| P7-MANIFEST | `data/interim/production_generation_v2/run_manifest.json` | Production run settings and selected chunks |
| P7-SUMMARY | `data/interim/production_generation_v2/run_summary.json` | Production run summary |
| P7-OUT-PROD | `data/interim/production_generation_v2/dataset_v0_additional_v2_resumed.jsonl` | 485-record V2 output |
| P7-CP | `data/interim/production_generation_v2/checkpoints/` | 182 per-chunk/pass checkpoints |
| P7-AUDIT | `data/interim/production_generation_v2/audit_v1/audit_summary.json` | Structural audit summary |
| P7-JUDGE-485 | `data/interim/production_generation_v2/pipeline_judge/v2_judge_summary.json` | Full 485-example judge summary |
| P7-JUDGE-66 | `data/interim/production_generation_v2/groq_judge/v2_judge_summary.json` | Separate 66-example judge summary |

## 10. Phase 7 exit assessment

**Conditionally satisfied with explicit limitations.** The production generator, model, provider, selected chunks, passes, output, judge model, judge results, and structural audit are evidenced. The production selection rationale is recoverable at an operational level. Runtime overrides for several generation parameters are not recorded, and the two-record checkpoint/output discrepancy remains unresolved. The benchmark evidence is not sufficiently controlled to claim a definitive model-quality winner.
