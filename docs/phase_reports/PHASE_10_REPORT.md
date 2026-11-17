# Phase 10 Report — Production V2 and Final Dataset Lineage

## Status

**Conditionally reconstructed; exit gate not satisfied.**

## Objective

Identify the exact production outputs and preparation code that produced the final validated dataset pool.

## Work completed

1. Compared Production V2 generation and resumable script behavior.
2. Identified original and resumed V2 output files and counts.
3. Reconstructed manual-review and judging records.
4. Reconciled the 170-record validated candidate pool.
5. Compared the three Phase 3 preparation variants.
6. Strongly inferred the preparation V2 variant from report structure and matching output hashes.
7. Reconciled B3 source membership and B3-to-B4 membership.
8. Assigned recorded dispositions to all 23 B3 records absent from B4.
9. Verified B4 package checksum and internal equivalence of both B4 adapter backup archives.

## Key results

| Artifact | Records | SHA-256 |
|---|---:|---|
| Resumed V2 | 485 | `6316EC13A17EC7D06877EFC8C054225DF63276597D0F14151F6F67A44E81E077` |
| B3 reconstructed | 600 | `f570c5596e28db4c2493988d344abe4efc632a5637d2471d366ef39124292960` |
| B4 filtered | 577 | `73c0134aa49137f772418fbb4b58f7e5721f5e64d323080092e45218db77fb58` |
| B5 domain | 577 | `73c0134aa49137f772418fbb4b58f7e5721f5e64d323080092e45218db77fb58` |
| B5 general | 577 | `c4718ab256c4cffbf006b272932d36399165fcdf566b1902098186573759a505` |
| B5 combined | 1154 | `e2bec7d9ac16ba82cf21cf3a99acdd7e9a2176f24201e0e4b6fa9e3dc832de60` |

B3 contains all 88 raw, 27 prior additional, and 485 V2 records. Its 600 IDs are unique.

B4 is an exact 577-record subset of B3. The 23 absent records have recorded dispositions: 5 approved duplicate removals, 5 automated production-batch rejections, 2 human-audit rejections, and 11 V2 pipeline judge rejections.

Phase 3 evidence validation reports 600 B3 records and 577 B4 records validated with zero mismatches. All six Phase 3 output hashes were independently matched against the report.

The two B4 adapter backup archives have different ZIP-level hashes and structures, but all eight corresponding internal files have matching SHA-256 hashes.

## Limitations

- Checkpoint accepted-count sum is 483, while the resumed output has 485 records.
- Recovery seed copy during the resumed run is not proven.
- The preparation V2 script is strongly inferred, not directly proven to have executed.
- The exact historical B3-to-B4 filtering script and execution sequence remain unidentified.
- The located 66-record judge file is not proven to be the historical original 88-record source.
- Human-review independence is not established.
- The 30-record B4 human audit does not individually review all 577 records.

## Validation

- V2 output record IDs: 485 unique.
- Validated merge: 170 expected, 170 actual, 170 unique, zero missing, zero unexpected.
- B3: 600 records, 600 unique IDs.
- B4: 577 records, 577 unique IDs.
- B3-to-B4: 23 absent, zero unexpected B4 IDs, zero duplicate B4 IDs.
- B4 package checksum matches the independently hashed Phase 3 B4 output.
- B4 adapter archive internal comparison: 8/8 files match.
- Frozen source modification: Phase 3 report states false.

## Exit gate assessment

The exact generation inputs and generation code are identified. The preparation variant is strongly inferred from report structure and matching output hashes. However, direct preparation-script execution evidence is absent, and the exact B4 filtering implementation remains unidentified.

**Phase 10 exit gate: NOT SATISFIED.**

Phase 10 artifacts document the reconstructed lineage and unresolved evidence. Phase 11 must not be treated as authorized by a claim that Phase 10 is fully complete. Further work should target only the missing execution evidence if it is recoverable; do not rerun historical scripts or regenerate datasets.
