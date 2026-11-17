# Initial Dataset Evaluation and Human-Audit Preparation

## Evaluation input and outputs

The recovered evaluation file is `data/interim/groq_evaluation_results.jsonl`. It contains 88 records corresponding to the 88 unique examples in `data/interim/dataset_v0_raw.jsonl`.

The record-level ID reconciliation found no raw examples without an evaluation record and no evaluation records without a raw example.

## Evaluation outcome

The recovered evaluation contains:

- 88 evaluated examples
- 80 accepted examples
- 8 rejected examples

The evaluation records include faithfulness score, evidence relevance, unsupported-claim indicators, answer correctness/completeness fields, evidence provenance, judge metadata, and decision status.

The evidence-relevance-false and unsupported-claims-true counts can overlap. They must not be added as if they represent distinct rejected examples.

## Evaluator provenance caveat

The inspected `28_evaluate_dataset.py` script is configured for an OpenRouter/Gemma judge and writes `evaluation_results.jsonl`. The recovered file examined here is `groq_evaluation_results.jsonl`. The repository also contains a separate Groq evaluation script. The available evidence does not justify attributing the Groq results to script 28.

The exact execution provenance should be taken from the recovered result records and associated execution artifacts, not inferred from a similarly named evaluation script.

## Human-audit preparation

The recovered human-audit CSV contains 30 prepared rows. Its summary describes a deterministic selection of 15 examples from the original dataset and 15 from an improved pilot, using seed `20261112` and round-robin stratification by source document and task type.

The reviewer fields `human_verdict`, `issue_category`, and `reviewer_notes` are blank for all 30 rows. No human verdicts were entered. This artifact demonstrates preparation of a review sample, not completed human evaluation or human validation of the dataset.

## Interpretation

Automated acceptance is not equivalent to human validation. The 80 accepted records are accepted under the recovered automated evaluation process only. The 30-row human-audit preparation remains incomplete.

No evaluation API calls or human-review actions were performed during this reconstruction.