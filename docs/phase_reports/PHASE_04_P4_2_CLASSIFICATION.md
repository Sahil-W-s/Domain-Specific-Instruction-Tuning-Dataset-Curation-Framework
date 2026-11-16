# Phase 4 — P4.2 Large-Artifact Classification

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework  
**Date:** 2026-11-17  
**Status:** Provisional classification complete; migration blocked

## Scope and evidence

Reviewed all 41 records in `reports/inventory/large_files.csv` and cross-matched them against `reports/inventory/artifact_inventory.csv` by artifact ID. All 41 records matched. Every large-file record has a recorded SHA-256 and `hash_status=verified`.

The source inventory threshold is at least 50 MiB. This task covers only those 41 large-file records, not all 1,531 registry records.

## Classification results

| Provisional class | Records | Interpretation |
|---|---:|---|
| Experiment backup archives | 8 | B2–B5 final-backup ZIPs across MLCP_UPLOAD and MLCP_KAGGLE_WORK |
| Adapter backup archives | 8 | B2–B5 adapter-backup ZIPs inside reproducibility-package directories |
| Reproducibility package archives | 1 | Versioned full reproducibility-package ZIP |
| Final adapter files / copies | 8 | B2–B5 adapter_final or backup adapter copies |
| Adapter checkpoint files | 16 | B2–B5 checkpoint adapter_model.safetensors files |
| **Total** | **41** | **17 archives + 24 adapter/model files** |

The lifecycle labels above are provisional path/filename interpretations. The source registry itself leaves most model lifecycles as `unknown`; this classification does not establish which model checkpoint is scientifically canonical or preferred.

## Content identity and duplicate handling

- Physical size across all 41 records: **3,186,397,696 bytes** (~2.97 GiB).
- Unique content across 21 SHA-256 values: **1,735,016,404 bytes** (~1.62 GiB).
- Duplicate replica overhead within this subset: **1,451,381,292 bytes** (~1.35 GiB).
- Eight SHA-256 groups have multiple records: four groups of three adapter-backup ZIP copies and four groups of four adapter-weight copies.
- Matching hashes establish byte identity, not canonical location, scientific preference, backup independence, or permission to delete a copy.

The classification CSV retains all 41 source records and their artifact IDs, paths, hashes, original registry classifications, provisional role/lifecycle, and storage hold status.

## Rights, privacy, and redistribution

The registry records `sensitivity=unknown` and `redistribution_status=unknown` for all 41 large-file records. No rights or privacy clearance can be inferred from filenames, extensions, hashes, or directory names.

**Decision:** Keep the Google Drive destination restricted/private. Do not upload any of these artifacts until the underlying archive contents, source-data licences, model/data redistribution terms, and privacy implications have been reviewed. Do not publish the artifacts through GitHub or Git LFS.

## Storage treatment

- Preferred artifact backend: DVC with a restricted Google Drive remote.
- GitHub: source code, safe manifests, reports, and DVC metadata/pointer files only.
- New bulk Git LFS tracking: disabled under the zero-additional-spend constraint.
- DVC content addressing may avoid storing byte-identical copies more than once, but the source registry must retain every original path and artifact record.
- Do not yet select a canonical B2–B5 model checkpoint. First establish experiment lineage and inspect the reproducibility-package contents.
- No source file was moved, deleted, renamed, uploaded, or rewritten during P4.2.

## Open gates before migration

1. Review rights and redistribution terms for all archive contents and model artifacts.
2. Inspect the reproducibility package manifest and identify any bundled data, source code, secrets, or third-party content without extracting over source locations.
3. Confirm which B2–B5 adapters/checkpoints are required for reproducibility; do not assume the latest-numbered checkpoint is the canonical result.
4. Record the exact Drive folder ID and restricted access policy in local ignored configuration; never commit OAuth credentials.
5. Record backup/recovery status. An independent physical backup has not been verified; the historical Phase 0 risk acceptance does not establish one.
6. Complete and approve `manifests/storage_map.yml` before any migration or DVC tracking of source artifacts.

## Deliverables

- `reports/storage/large_file_classification.csv`
- `manifests/storage_map.yml`
- `docs/phase_reports/PHASE_04_P4_2_CLASSIFICATION.md`

**P4.2 exit status:** Classification and provisional storage mapping recorded. Rights clearance and canonical model selection remain open. Migration remains unauthorized.
