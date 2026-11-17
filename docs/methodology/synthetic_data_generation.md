# Historical Synthetic Data Generation Methodology

## Scope

This document reconstructs the original `dataset_v0_raw` synthetic-generation workflow from recovered scripts, frozen source chunks, request logs, checkpoints, and generated records. It does not describe or replace the separate Phase 7 `production_generation_v2` workflow.

## Source material

The generation script identifies `data/frozen/chunks_v1_frozen.jsonl` as its input and `data/interim/dataset_v0_raw.jsonl` as its raw output. The recovered frozen file contains 91 chunks.

The generation script identifies the model as `nvidia/nemotron-3.5-super-vl:free`. It configures two chunks per request and two examples per chunk, yielding four examples per successful batch.

## Checkpointing and persistence

The script uses `data/interim/production_checkpoints/` for batch checkpoint files and `data/interim/production_request_log.jsonl` for request outcomes. The recovered checkpoint set contains 22 valid batch files. Each contains four examples associated with two distinct chunk IDs.

The script implements atomic JSON and JSONL writes, checkpoint loading, duplicate example-ID checks, batch-ID checks, required-field checks, and raw-dataset reconstruction from checkpoints. These are code capabilities; this reconstruction does not claim that every code path was independently executed or tested during this phase.

## Recovered execution

The request log contains 36 records: 22 successful requests and 14 failed requests. The successful batch IDs are 001–020, 024, and 033. The failed request records were reported as duplicate normalized question validation failures.

The 22 successful checkpoints contain 88 examples in total. The recovered raw JSONL also contains 88 records. The exact batch-to-checkpoint-to-raw relationships are recorded in `reports/inventory/generation_batch_lineage.csv`.

## Important target discrepancy

The generation script contains comments describing preservation of 80 existing examples and generation of 920 new examples, for a target of 1,000. The recovered raw dataset contains 88 examples. The available evidence therefore establishes a recovered 88-example execution, not completion of the 1,000-example target.

The batch numbering and recovered request history also show gaps. The reconstruction preserves those gaps rather than inferring that missing batches were completed or that all planned chunk slots were attempted.

## Reproducibility limitations

The request log and checkpoints provide evidence of successful and failed requests, but do not fully establish all runtime parameter overrides, the complete intended generation plan as executed, or every provider-side detail. Script defaults must not be presented as confirmed runtime values unless supported by execution artifacts.

No generation requests were issued during this reconstruction. Source chunks, checkpoints, request logs, and raw data were not modified.