# Phase 4 P4.3 — ZIP Metadata Review

**Date:** 2026-11-17  
**Status:** Step 1 executed and reviewed; Step 2 README-content review pending.

## Scope and evidence

Reviewed the local outputs produced by `scripts/storage/inspect_large_archives.py`:

- `.local/phase4_archive_inspection/inspection_summary.json`
- `.local/phase4_archive_inspection/archive_summary.csv`
- `.local/phase4_archive_inspection/archive_entries.csv`

The inventory contained 17 ZIP records grouped into 9 unique SHA-256 content groups. All 9 unique archive groups were successfully listed, producing 115 entry-metadata records. No archive inspection errors were reported.

## Metadata findings

Across the 9 unique archive groups:

| Metadata check | Count |
|---|---:|
| License / NOTICE / COPYING filename matches | 0 |
| README-named entries | 9 |
| Manifest / config filename matches | 0 |
| Potentially sensitive filename matches | 0 |
| Encrypted entries | 0 |
| Unsafe paths | 0 |
| Symlink entries | 0 |

The reproducibility package listing includes a README, checksum metadata, configuration/JSON material, datasets, evaluation outputs, predictions, and adapter backup ZIPs. The filename scan did not identify a license/notice file or a manifest/config filename matching the inspector's configured patterns.

## Safety properties

The inspection summary confirms:

- No entries were extracted.
- No entry payloads were read.
- No source archive was modified.
- No new source hashes were computed.
- All 9 unique archive groups were inspected without errors.

## Interpretation and limitations

1. The absence of a detected LICENSE/NOTICE/COPYING filename is not evidence that redistribution is permitted or prohibited.
2. The README contents have not yet been read. README filenames alone provide no licence conclusion.
3. The configured filename patterns are heuristic. Zero sensitive-name matches do not prove that archive contents contain no personal data, credentials, or restricted third-party material.
4. The metadata listing does not establish the provenance or terms for datasets, source documents, model weights, or adapter contents.
5. No per-artifact rights or sensitivity status is upgraded based on this metadata-only review.

## Decision

- Keep rights and redistribution status unknown unless supported by upstream terms or explicit evidence.
- Keep sensitivity status unknown pending content review.
- Keep `manifests/storage_map.yml` at `migration_authorized: false`.
- Do not move, delete, rename, extract over, upload, or otherwise modify source artifacts.
- Do not select a canonical B2–B5 adapter/checkpoint without experiment-lineage evidence.

## Next bounded action

Use `scripts/storage/inspect_archive_readmes.py` to read only README-named ZIP entries with a 64 KiB per-entry limit. The script writes a local-only Markdown report and JSON summary under `.local/phase4_archive_inspection/`. Review the output locally for private information before sharing it. Do not commit the generated README contents to the public repository.
