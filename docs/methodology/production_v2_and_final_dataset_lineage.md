# Production V2 and Final Dataset Lineage

## 1. Scope

This document reconstructs Production V2 generation, manual review, judging, validated-pool merging, and Phase 3 dataset preparation for the Domain-Specific Instruction-Tuning Dataset Curation Framework.

The reconstruction is based on preserved scripts, JSONL outputs, run manifests, checkpoints, review records, validation reports, frozen manifests, and reproducibility-package contents.

Historical scripts were inspected, not executed during this reconstruction.

## 2. Production V2 generation

### Original generation

Script: `55_generate_production_v2.py`

SHA-256:
`22B11779BD2796503A54DD4D4D2E5BC51FF85CE43842028472372AD7847D718F`

Original output:
`data/interim/production_generation_v2/dataset_v0_additional_v2.jsonl`

Observed count: 72 records.

### Resumable generation

Script: `60_generate_production_v2_resumable.py`

SHA-256:
`D55C9E1D28209EE9E38DFA496F60C47B768281CFD7AC0554861EE23C381D25B4`

Output:
`data/interim/production_generation_v2/dataset_v0_additional_v2_resumed.jsonl`

SHA-256:
`6316EC13A17EC7D06877EFC8C054225DF63276597D0F14151F6F67A44E81E077`

Observed count: 485 records, all IDs present and unique.

Manifest model: `nvidia/nemotron-3.5-super-vl:free`

Frozen chunk corpus SHA-256:
`67e90d3428ff0a421111e19916ceb2dfc007460ae047f18131131be2f80bb827`

Run summary reports 104 new examples added and a total of 485. The previous V2 count was 381, so 381 + 104 = 485.

The resumable script copies the recovery seed only if the resumed output does not already exist. The manifest's recovery-seed path does not prove that the copy occurred during this run.

### Checkpoint caveat

There are 182 checkpoint files: 91 chunks across two passes. All parse successfully. 180 are complete; the sum of accepted counts is 483. Two checkpoints report no accepted examples.

The checkpoint total of 483 does not reconcile with the final output count of 485. This discrepancy remains unresolved. Checkpoints do not contain record IDs that would independently resolve it.

## 3. Manual review and judging

The located manual-review and judge files each contain 66 records with 66 unique IDs. Their ID sets match exactly.

The located V2 review/judge subset contains:
- 65 accepted
- 1 rejected

Rejected record:
`genv2_iot_cloud_case_studies_chunk_0007_p01_classification`

The rejection reason was that the response did not perform the requested classification.

The historical 66-record judge file is not proven to be the original historical 88-record source. It must not be represented as a complete original judge record.

Pipeline judging later records 11 V2 records as rejected. These decisions are preserved as a separate stage and must not be collapsed into the earlier 66-record judge result.

## 4. Validated candidate pool merge

Script: `59_merge_and_audit_validated_pool.py`

SHA-256:
`F019A850C2B54996E2769D12A51237A8094816B7EEFA3F1E3106B3385749E8D0`

Inputs:
- `production_filter/final_reconciliation/final_accepted_candidates.jsonl` — 105 records
- `production_generation_v2/manual_review/dataset_v2_reviewed.jsonl` — 66 records
- `production_generation_v2/groq_judge/v2_judge_results.jsonl` — 66 records
- `data/frozen/chunks_v1_frozen.jsonl` — 91 chunks

Outputs:
- `data/interim/validated_candidate_pool/combined_validated_candidates.jsonl`
- `global_duplicate_candidates.json`
- `global_pool_audit_errors.json`
- `global_pool_summary.json`

The merged pool contains 170 records: 105 previous accepted records and 65 accepted V2 records.

Independent membership reconciliation found:
- 170 expected IDs
- 170 actual IDs
- 170 unique IDs
- 0 missing IDs
- 0 unexpected IDs

The merge audit reports 170 valid evidence-provenance records, zero invalid records, zero duplicate example-ID groups, zero exact duplicate instruction groups, zero near-duplicate pairs at threshold 0.88, and no structural/provenance errors.

The 78 records without `task_type` originate from the previous raw dataset schema. They are retained as unspecified; no labels have been inferred.

## 5. Phase 3 preparation variant

Three variants were inspected:
- `prepare_phase3_datasets.py`
- `prepare_phase3_datasets_corrected.py`
- `prepare_phase3_datasets_v2.py`

The V2 variant has SHA-256:
`C2BE16FC22E90A53AB697FA615F10E64724C8B5CFABC82E0F5F94FACE2EF79D1`

It is the only inspected variant whose report structure matches the located Phase 3 report, including:
- `source_hashes_before`
- `source_hashes_after`
- `evidence_validation`
- `output_hashes`
- `frozen_sources_modified`

This is strong implementation-level attribution, not direct proof of execution. No recovered execution log independently establishes that this exact script was run.

The Phase 3 report records:
- status: `PASS_DATASET_PREPARATION`
- B2 Dolly: 1,000
- B3 reconstructed pool: 600
- B4 filtered IoT: 577
- B5 domain: 577
- B5 general: 577
- B5 combined: 1,154
- B3 evidence reconstruction: 600 validated
- B4 evidence reconstruction: 577 validated
- evidence mismatches: 0
- frozen sources modified: false

### Phase 3 preparation input hashes

Prior additional dataset:
`6399a0d0f8c5a15b043238e79dc8fbfaaea32130d3aa483fcfba12d9be526dba`

Resumed V2 dataset:
`6316ec13a17ec7d06877efc8c054225df63276597d0f14151f6f67a44e81e077`

B4 source:
`9e541db71c7d5325e3817cd8c29469cfac7137aad0a399cb8b6a88a2e72007a3`

Frozen chunks:
`67e90d3428ff0a421111e19916ceb2dfc007460ae047f18131131be2f80bb827`

The raw dataset hash is intentionally omitted here because its independently established value is not sufficiently clear in the consolidated evidence.

### Phase 3 output hashes

| Output | SHA-256 |
|---|---|
| B2 | `b2f565f3533222b5080f9df1bd037b483e020208082aea28621c39efdc4cbe06` |
| B3 | `f570c5596e28db4c2493988d344abe4efc632a5637d2471d366ef39124292960` |
| B4 | `73c0134aa49137f772418fbb4b58f7e5721f5e64d323080092e45218db77fb58` |
| B5 domain | `73c0134aa49137f772418fbb4b58f7e5721f5e64d323080092e45218db77fb58` |
| B5 general | `c4718ab256c4cffbf006b272932d36399165fcdf566b1902098186573759a505` |
| B5 combined | `e2bec7d9ac16ba82cf21cf3a99acdd7e9a2176f24201e0e4b6fa9e3dc832de60` |

All six output hashes were independently recomputed and matched the Phase 3 report.

## 6. B3 and B4 membership reconciliation

B3 contains 600 unique records:
- 88 raw records
- 27 prior additional records
- 485 V2 records

All 600 source IDs were found in B3. No source IDs were missing and no duplicate IDs were found.

B4 contains 577 unique records. It is an exact subset of B3:
- B3 records absent from B4: 23
- Unexpected B4 IDs: 0
- Duplicate B4 ID groups: 0
- B4 records missing example IDs: 0

All 23 exclusions have a recorded disposition:

### Five approved duplicate removals

- `production_batch_033_example_03`
- `production_batch_011_example_03`
- `production_batch_024_example_02`
- `production_batch_024_example_03`
- `production_batch_024_example_04`

These were excluded through five explicitly approved duplicate decisions in script 46.

### Five automated production-batch judge rejections

- `production_batch_006_example_02`
- `production_batch_008_example_03`
- `production_batch_010_example_03`
- `production_batch_017_example_03`
- `production_batch_019_example_02`

### Two production-batch human-audit rejections

- `production_batch_001_example_01`
- `production_batch_004_example_02`

These two were present in the 105-record accepted reconciliation input but later appear in the human-audit rejection record. Their exclusion must be attributed to the later review evidence, not silently backdated into the earlier merge.

### Eleven V2 pipeline judge rejections

- `genv2_iot_cloud_case_studies_chunk_0005_p02_classification`
- `genv2_iot_cloud_case_studies_chunk_0007_p01_classification`
- `genv2_iot_cloud_case_studies_chunk_0014_p01_classification`
- `genv2_iot_unit1_chunk_0026_p01_classification`
- `genv2_iot_unit1_chunk_0033_p01_extraction`
- `genv2_iot_unit1_chunk_0033_p01_classification`
- `genv2_iot_unit1_chunk_0035_p01_extraction`
- `genv2_iot_unit1_chunk_0046_p01_qa`
- `genv2_iot_unit1_chunk_0049_p01_extraction`
- `genv2_iot_unit1_chunk_0051_p02_extraction`
- `genv2_iot_unit2_chunk_0002_p02_extraction`

These records have pipeline judge verdicts of REJECT. Earlier judging stages may contain different decisions; the chronology is retained.

The 23 B3-to-B4 exclusions therefore reconcile as 5 duplicate removals + 5 automated production-batch rejections + 2 human-audit rejections + 11 V2 pipeline rejections.

This reconciles membership and recorded dispositions. It does not prove the exact historical script or execution sequence that created B4.

## 7. B4 frozen artifact and backup verification

The B4 frozen manifest records:
- 577 records
- 577 unique IDs
- SHA-256 `9e541db71c7d5325e3817cd8c29469cfac7137aad0a399cb8b6a88a2e72007a3`
- 11/11 final integrity checks passed
- human audit sample: 30 records, 28 accepted and 2 rejected
- 549 retained records not individually reviewed in that sample

The reproducibility package contains B4 with SHA-256:
`73c0134aa49137f772418fbb4b58f7e5721f5e64d323080092e45218db77fb58`

This matches the independently hashed Phase 3 B4 output and the package checksum manifest.

Two B4 adapter backup archives were compared internally. All eight corresponding files have identical SHA-256 hashes:
- adapter config
- adapter weights
- chat template
- README
- tokenizer config
- tokenizer
- metrics
- run metadata

The ZIP-level hashes differ because the archive structures differ. The internal contents are identical. Both archives are preserved.

## 8. Script execution and provenance limitations

Script hashes establish the identity of inspected code, not execution.

The following remain unresolved:
- The exact historical B3-to-B4 filtering script and complete execution sequence are not proven.
- The preparation V2 variant is strongly inferred from report structure and matching output hashes, but direct execution evidence is absent.
- The 483 checkpoint accepted-count sum does not reconcile with the 485-record resumed output.
- The recovery seed copy operation during the resumed run is not established.
- The 66-record judge file is not proven to be the historical original 88-record judge source.
- Earlier and later judging stages contain different decisions for some records; their chronology must remain distinct.
- Human-review independence is not established.
- The 30-record B4 audit sample does not individually validate all 577 records.

## 9. Conclusion

The Production V2 output, merge membership, B3 composition, B3-to-B4 membership difference, B4 frozen artifact, and Phase 3 output hashes are substantially reconciled.

The Phase 3 preparation V2 variant is strongly inferred but not proven to have executed. The exact historical filtering implementation responsible for B4 remains unidentified.

Accordingly, Phase 10 documentation is reconstructed, but the approved exit gate is not fully satisfied. Do not claim exact end-to-end reproducibility and do not begin Phase 11 on the assumption that the filtering implementation has been identified.

## 10. Kaggle experimental notebook and reproducibility package

### Notebook role

The sole Kaggle notebook used for the B0-B5 experimental workflow was inspected. It is a downstream consumer of the prepared datasets and the producer of the IoT CP reproducibility package. It is not evidence of the upstream B3-to-B4 filtering execution.

### Confirmed notebook responsibilities

| Notebook location | Observed responsibility |
|---|---|
| Cell 3 | Loads and validates the available dataset artifacts |
| Cell 19 | Compares B3 and B4 membership |
| Cell 20 | Creates comparable training and validation splits |
| Cells 23-44 | Performs the downstream baseline/model training workflow |
| Cells 47-50 | Inspects B4 training records and prepares B1 few-shot examples |
| Cell 82 | Checks B3 and B4 dataset availability |
| Cell 83 | Creates the IoT CP reproducibility package |

The notebook covers the B0-B5 experimental workflow. It consumes B3 and B4 from the Kaggle input dataset location. The B3/B4 membership comparison and split construction are downstream operations on those existing inputs.

### Provenance boundary

The notebook establishes the downstream experimental workflow and reproducibility-package construction. It does not establish:

- The exact historical script that transformed B3 into B4.
- The complete filtering, review, and judging execution sequence that produced the 577-record B4 artifact.
- The historical Kaggle dataset version or upload event that first supplied the B4 artifact.

The notebook's existence must not be used to attribute B3-to-B4 filtering to Kaggle notebook execution. The upstream filtering provenance remains unresolved.
