# Phase 07 Report — Generation Model Experiments and Production Configuration

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework
**Phase:** 07
**Status:** Conditionally satisfied; evidence and limitations recorded
**Evidence date:** 17 November 2026

## Objective

Establish which model, prompt, schema, and generation settings were tested and why the production method was selected.

## Work completed

1. Recovered and inspected the production generator, structural auditor, and judge source files from the original project tree and script archives.
2. Identified the production generator as `nvidia/nemotron-3.5-super-vl:free` through OpenRouter.
3. Recovered the run manifest and summary: 91/91 chunks selected, two passes, three task types, similarity threshold 0.88, 104 new examples reported, and 485 final V2 records.
4. Recovered exploratory Lightning smoke tests, a four-model operational benchmark, and Super VL batch-scaling tests.
5. Recovered full-run Groq judge results for 485 examples and a separate 66-example judge run.
6. Recovered structural audit results and frozen corpus hash linkage.
7. Documented API dependencies and avoided all provider calls during reconstruction.
8. Created secret-free reconstructed generation and judge configurations, explicitly distinguishing runtime-confirmed values from script defaults and unknowns.

## Key results

- Production output: 485 records across all 91 frozen chunks.
- Task distribution: 166 QA, 161 extraction, 158 classification.
- Production generator: `nvidia/nemotron-3.5-super-vl:free`.
- Full pipeline judge: `openai/gpt-oss-120b` via Groq; 474 ACCEPT, 11 REJECT, mean faithfulness 4.971/5.
- Structural audit: `PASS_STRUCTURAL_AUDIT`; 485/485 exact evidence checks; zero duplicate pairs flagged at threshold 0.88; zero errors and warnings.
- Separate 66-example judge run: 65 ACCEPT, one REJECT. Kept separate from the 485-example result.

## Production selection rationale

The recovered evidence supports an operational rationale: Lightning was used in early smoke tests; the small four-model benchmark recorded two successful Super VL requests and failures for the other three candidate models; subsequent Super VL multi-chunk and larger-batch tests succeeded; the production source, manifest, and output rows consistently identify Super VL. The evidence does not establish a rigorous statistical or human-evaluated quality victory over all candidate models.

## Validation and limitations

- Production runtime settings for passes, model, selected chunks, task types, and similarity threshold are evidenced by the run manifest.
- Temperature 0.35, max tokens 5000, timeout 180 seconds, retry count 3, and delay 15 seconds are script defaults; the run manifest does not preserve the full command line or runtime overrides.
- Top-p and production generator reasoning effort are not established.
- The checkpoint `accepted_count` sum is 483, while the final output contains 485 records. The two-record difference remains unresolved and is preserved as a caveat.
- Automated judge acceptance does not constitute human evaluation of all records.
- Exploratory benchmarks are small and use different prompts, chunk counts, and token limits; they are not fully comparable.
- The 66-example judge run is separate from the full 485-example run.
- No provider API calls were made during Phase 7 reconstruction.

## Required artifacts

- `docs/experiments/generation_model_benchmarks.md`
- `configs/generation/generation_v2_production_reconstructed.json`
- `configs/generation/generation_v2_judge_groq_reconstructed.json`
- `reports/metrics/generation_model_comparison.csv`
- `docs/phase_reports/PHASE_07_REPORT.md`

## Exit gate

**Conditionally satisfied.** The production approach is documented and supported by recovered execution evidence. Missing runtime parameter provenance, non-rigorous model comparisons, and the two-record checkpoint discrepancy remain explicit limitations rather than being filled by assumption.

## Git and data handling

These are newly reconstructed documentation/configuration artifacts. No source datasets, historical logs, checkpoints, or existing files are modified by this package. The artifacts have not been staged or committed.
