# Phase 2 Report — Artifact Registry and Large-File Map

**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework  
**Generated:** 2026-11-16T22:02:44.722741+00:00  
**Status:** Deliverables generated; owner review required

## Scope

Phase 2 establishes a content-aware artifact registry, inventory, duplicate reports,
and large-file map. No source files were moved, deleted, or extracted. No storage
migration or DVC/Git LFS migration was performed.

## Registry

- Total registry records: 1,531
- Unique artifact IDs: 1531
- Verified hashes: 1,496
- Not applicable: 2
- Historical failed records: 33
- Pending hash records: 0

The registry schema validation previously passed for all 1,531 records.
An independent SHA-256 sample recomputation passed for 15 of 15 sampled files.
This sample does not constitute exhaustive independent recomputation of every hash.

## Historical hash failures

- Historical failed records retained: 33
- Records with verified replacement links: 33
- Unresolved records: 0

Historical failures are preserved for auditability and distinguished from current
operational failures. The replacement links are recorded in `hash_failures.csv`.

## Exact duplicates

- Exact duplicate groups: 564
- Duplicate artifact memberships: 1,373

The existing exact duplicate report was checked against the registry. All expected
groups and memberships matched; no missing groups, extra groups, membership
mismatches, or validation errors were found.

## Possible duplicates

- Review groups: 11
- Candidate records: 138
- Review statuses: pending_manual_review

All candidate records remain pending manual review. They are not confirmed duplicates.

## Large files

Threshold: 50 MiB (52,428,800 bytes).

- Files at or above 50 MiB: 41
- Files at or above 100 MiB: 1
- Files at or above 200 MiB: 1

The large-file candidate report was validated against the registry: all 41 expected
records were present, with no missing files, extras, or size mismatches.

## Inventory coverage and provenance

The initial consolidated inventory contained 1,498 root/path pairs. The registry
contains 1,531 root/path pairs, including 33 corrected-path replacement records.
The canonical artifact inventory is generated from the registry so those replacement
records are included.

## Limitations and outstanding work

- The 15-file independent SHA-256 check was a sample, not an exhaustive rehash.
- Possible duplicates require manual review; no duplicate files were deleted.
- File sensitivity classifications should not be treated as confirmed solely from
  field names; content review may still be required.
- This report does not authorize source-file movement, deletion, archive extraction,
  or storage migration.
- Phase 2 completion remains subject to owner review and the implementation plan's
  exit gate.

## Generated deliverables

- `manifests/artifact_registry.schema.json`
- `manifests/artifact_registry.jsonl`
- `reports/inventory/artifact_inventory.csv`
- `reports/inventory/exact_duplicates.csv`
- `reports/inventory/possible_duplicates_review.csv`
- `reports/inventory/large_files.csv`
- `reports/inventory/hash_failures.csv`
- `docs/phase_reports/PHASE_02_REPORT.md`
