# Phase 5 — Script Catalogue

Project: ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework

## Scope and method

- 74 refined entries: 73 Python files in MLCP_scripts.zip and standalone pipeline.py.
- pipeline_source_scripts.zip contains 13 scripts already present in the main archive.
- Archive source bytes were checked against the refined catalogue size and SHA-256.
- Source was parsed statically; no historical script was imported or executed.
- API indicators and path references are static findings, not proof of actual use.
- Execution status is separate from file existence and source inspection.

## Status interpretation

- `inspected`: source was available and statically parsed.
- `exists`: inventory entry exists, but source was not available for parsing.
- `executed_verified`: direct log/output evidence supports execution.
- `unknown`: no direct execution evidence was established.

## Script register

| Script | Role | Inspection | Execution | API indicators |
|---|---|---|---|---|
| `01_extract_pdfs.py` | 01 extract pdfs | inspected | executed_verified | — |
| `02_inspect_empty_pages.py` | 02 inspect empty pages | inspected | executed_verified | — |
| `03_create_contact_sheets.py` | 03 create contact sheets | inspected | unknown | — |
| `04_recover_image_pages.py` | 04 recover image pages | inspected | executed_verified | google.genai |
| `04a_test_gemini.py` | 04a test gemini | inspected | unknown | google.genai |
| `05_merge_page_content.py` | 05 merge page content | inspected | unknown | — |
| `06_validate_merged_pages.py` | 06 validate merged pages | inspected | unknown | — |
| `07_analyze_chunk_distribution.py` | 07 analyze chunk distribution | inspected | unknown | transformers |
| `08_create_chunks.py` | 08 create chunks | inspected | unknown | transformers |
| `08b_create_semantic_chunks.py` | 08b create semantic chunks | inspected | unknown | transformers |
| `09_inspect_chunks.py` | 09 inspect chunks | inspected | unknown | — |
| `10_audit_semantic_chunks.py` | 10 audit semantic chunks | inspected | unknown | — |
| `11_audit_content_preservation.py` | 11 audit content preservation | inspected | unknown | — |
| `12_inspect_semantic_chunks.py` | 12 inspect semantic chunks | inspected | unknown | — |
| `13_sanitize_training_chunks.py` | 13 sanitize training chunks | inspected | unknown | — |
| `14_audit_sanitized_chunks.py` | 14 audit sanitized chunks | inspected | unknown | — |
| `15_test_gemini_api.py` | 15 test gemini api | inspected | unknown | google.genai |
| `16_test_openrouter_api.py` | 16 test openrouter api | inspected | unknown | openai;openrouter.ai |
| `17_check_openrouter_limits.py` | 17 check openrouter limits | inspected | unknown | openrouter.ai;requests |
| `18_test_structured_generation.py` | 18 test structured generation | inspected | unknown | openai;openrouter.ai |
| `19_test_batch_generation.py` | 19 test batch generation | inspected | unknown | openai;openrouter.ai |
| `20_inspect_batch_output.py` | 20 inspect batch output | inspected | unknown | — |
| `21_test_stronger_models.py` | 21 test stronger models | inspected | unknown | openai;openrouter.ai |
| `22_benchmark_model_quality.py` | 22 benchmark model quality | inspected | unknown | openai;openrouter.ai |
| `23_inspect_model_benchmark.py` | 23 inspect model benchmark | inspected | unknown | — |
| `24_test_supervl_multi_chunk.py` | 24 test supervl multi chunk | inspected | unknown | openai;openrouter.ai |
| `25_inspect_supervl_multi_chunk.py` | 25 inspect supervl multi chunk | inspected | unknown | — |
| `26_test_supervl_large_batch.py` | 26 test supervl large batch | inspected | unknown | openai;openrouter.ai |
| `27_inspect_supervl_large_batch.py` | 27 inspect supervl large batch | inspected | unknown | — |
| `28_evaluate_dataset.py` | 28 evaluate dataset | inspected | unknown | openai;openrouter.ai |
| `29_generate_production_batch.py` | 29 generate production batch | inspected | unknown | openai;openrouter.ai |
| `30_rebuild_raw_dataset.py` | 30 rebuild raw dataset | inspected | unknown | — |
| `31_audit_generated_examples.py` | 31 audit generated examples | inspected | unknown | — |
| `32_audit_evidence_blocks.py` | Audit evidence-block provenance for generated examples. | inspected | unknown | — |
| `33_test_semantic_judge.py` | One-example smoke test for the independent semantic judge. | inspected | unknown | openrouter.ai;requests |
| `34_test_groq_semantic_judge.py` | One-example Groq semantic-judge smoke test. | inspected | unknown | api.groq.com;requests |
| `35_benchmark_groq_judge.py` | Small-batch Groq judge benchmark: 8 examples, 2 per source document. | inspected | unknown | api.groq.com;requests |
| `35b_benchmark_groq_judge.py` | Corrected Groq judge benchmark: exactly 2 examples per source document (8 total). | inspected | unknown | api.groq.com;requests |
| `35c_resume_groq_judge_benchmark.py` | Corrected Groq judge benchmark: exactly 2 examples per source document (8 total). | inspected | unknown | api.groq.com;requests |
| `35d_resume_groq_judge_benchmark.py` | Robustly resume the 8-example Groq benchmark. | inspected | unknown | api.groq.com;requests |
| `36_evaluate_dataset_groq.py` | Production Groq evaluator for the IoT instruction dataset. | inspected | unknown | api.groq.com;requests |
| `37_inspect_rejected_examples.py` | Inspect rejected Groq judge evaluations. | inspected | unknown | — |
| `38_generate_improved.py` | Improved, independently checkpointed Phase 2 instruction-data generator. | inspected | unknown | openrouter.ai;requests |
| `39_diagnose_openrouter.py` | 39 diagnose openrouter | inspected | unknown | openrouter.ai;requests |
| `40_test_model_text_output.py` | 40 test model text output | inspected | unknown | openrouter.ai;requests |
| `41_generate_improved_safe.py` | Improved, independently checkpointed Phase 2 instruction-data generator. | inspected | unknown | openrouter.ai;requests |
| `42_audit_improved_pilot.py` | Read-only audit of the improved-generation pilot dataset. | inspected | unknown | — |
| `43_evaluate_improved_pilot_groq.py` | Independent Groq judge for the improved-generation pilot. | inspected | unknown | api.groq.com;requests |
| `44_prepare_human_audit_30.py` | Create exactly 30 accepted examples for the Phase 2 human audit. | inspected | unknown | — |
| `45_production_heuristic_filter.py` | Production heuristic filter for the IoT instruction dataset. | inspected | unknown | — |
| `46_apply_approved_deduplication.py` | Apply the approved manual near-duplicate decisions to the 115-example | inspected | unknown | — |
| `47_reconcile_judge_results.py` | 47 reconcile judge results | inspected | unknown | — |
| `48_reconcile_judge_results_fixed.py` | 48 reconcile judge results fixed | inspected | unknown | — |
| `49_repair_evidence_candidates.py` | 49 repair evidence candidates | inspected | unknown | — |
| `50_judge_repaired_examples_groq.py` | 50 judge repaired examples groq | inspected | unknown | api.groq.com;openai |
| `51_repair_hma_evidence.py` | 51 repair hma evidence | inspected | unknown | — |
| `52_judge_hma_repair_groq.py` | 52 judge hma repair groq | inspected | unknown | api.groq.com;requests |
| `53_judge_hma_repair_groq_fixed.py` | 53 judge hma repair groq fixed | inspected | unknown | api.groq.com;requests |
| `54_finalize_judge_reconciliation.py` | 54 finalize judge reconciliation | inspected | unknown | — |
| `55_generate_production_v2.py` | Production generation v2 for the IoT technical instruction dataset. | inspected | unknown | openrouter.ai;requests |
| `56_audit_generation_v2.py` | Read-only audit for Production Generation v2. | inspected | unknown | — |
| `57_apply_v2_manual_review.py` | Apply the seven manually reviewed decisions to Generation v2. | inspected | unknown | — |
| `58_judge_v2_candidates_groq.py` | Cross-model judge for the 66 manually reviewed Generation v2 candidates. | inspected | unknown | api.groq.com;requests |
| `59_merge_and_audit_validated_pool.py` | Merge the previously reconciled 105 candidates with the 65 accepted v2 | inspected | unknown | — |
| `60_generate_production_v2_resumable.py` | Resumable production generation v2 for the IoT technical instruction dataset. | inspected | unknown | openrouter.ai;requests |
| `61_audit_generation_v2.py` | Read-only comprehensive audit for the expanded IoT generation-v2 dataset. | inspected | unknown | — |
| `inspect_evidence_schema.py` | inspect evidence schema | inspected | unknown | — |
| `inspect_hma_evidence_blocks.py` | inspect hma evidence blocks | inspected | unknown | — |
| `inspect_recoverable_examples.py` | inspect recoverable examples | inspected | unknown | — |
| `pipeline_judge.py` | Cross-model judge for the 66 manually reviewed Generation v2 candidates. | inspected | unknown | api.groq.com;requests |
| `prepare_phase3_datasets_corrected.py` | prepare phase3 datasets corrected | inspected | unknown | — |
| `prepare_phase3_datasets_v2.py` | Prepare and validate the B2/B3/B4/B5 training datasets for Phase 3. | inspected | unknown | — |
| `prepare_phase3_datasets.py` | prepare phase3 datasets | inspected | unknown | — |
| `pipeline.py` | Reusable orchestrator for the IoT technical instruction dataset. | inspected | unknown | — |

## Historical variants and lineage notes

- `08b_create_semantic_chunks.py` — Separate semantic chunking implementation; writes V2 chunk outputs.
- `35b_benchmark_groq_judge.py` — Byte-identical content to 35c; retain both historical filenames.
- `35c_resume_groq_judge_benchmark.py` — Byte-identical content to 35b; retain both historical filenames.
- `35d_resume_groq_judge_benchmark.py` — Distinct resumable benchmark implementation.
- `47_reconcile_judge_results.py` — Earlier reconciliation variant; compare with 48.
- `48_reconcile_judge_results_fixed.py` — Changes source text field and isolates reconciliation_v2 output.
- `52_judge_hma_repair_groq.py` — Earlier HMA judge variant; compare with 53.
- `53_judge_hma_repair_groq_fixed.py` — Adds retrieval of full source chunks from frozen corpus.
- `55_generate_production_v2.py` — Earlier V2 generator; uses temporary-file replacement strategy.
- `60_generate_production_v2_resumable.py` — Recovery-safe resumable V2 generator; direct append and fsync behavior.
- `56_audit_generation_v2.py` — Earlier V2 audit implementation.
- `61_audit_generation_v2.py` — Expanded/resumed V2 audit implementation with broader scope.
- `pipeline_judge.py` — Related to script 58; supports environment-variable input/output overrides.
- `prepare_phase3_datasets.py` — Earlier Phase 3 preparation variant.
- `prepare_phase3_datasets_corrected.py` — Adds exact evidence-block reconstruction and validation.
- `prepare_phase3_datasets_v2.py` — Adds source fingerprints, count checks and exclusive output creation.

## Dependency graph limitations

The CSV records statically detected path references associated with AST calls. These are candidate read/write/reference edges, not runtime-confirmed dependencies. Path expressions assembled dynamically, environment variables, helper functions, and indirect data flow may not be fully resolved.

## API and overwrite-risk caveats

API indicators show potential external-service integration. They do not prove a request was made or establish its cost. Write-operation indicators flag code paths for review; absence of a detected write call is not proof of read-only behavior.
