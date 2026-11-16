# ML CP — Evidence Index

| Evidence | Location | What it establishes |
|---|---|---|
| Current artifact registry | `reports/inventory/known_existing_artifacts.csv` | 501 current source files, hashes, metadata, classifications |
| Historical inventory comparison | `reports/inventory/historical_inventory_comparison.csv` | Comparison against the historical project audit inventory |
| Hash error report | `reports/inventory/artifact_registry_hash_errors.csv` | Hash failures from initial registry creation |
| Registry summary | `reports/inventory/artifact_registry_summary.txt` | Current registry counts and classification totals |
| Source re-verification | `reports/inventory/artifact_registry_source_reverification.csv` | 501 current source hash and size matches |
| Classification review | `reports/inventory/artifact_classification_review.csv` | Review candidates and current-only paths |
| Historical audit inventory | Original source `project_audit_inventory.csv` | Historical project file audit |
| ZIP verification manifest | Recovery inventory `zip_archive_verification_manifest.csv` | Per-entry archive readability and byte counts |
| ZIP verification summary | Recovery inventory `zip_archive_verification_summary.txt` | Archive totals and errors |
| Source backup hash verification | Recovery root `phase0_sha256_verification.csv` | Source-to-backup SHA-256 comparisons |
| Methodology drafts | Original source `docs/methodology/` | Evidence-based drafts; not yet approved as final |
| Master implementation plan | ChatGPT Library reference | Plan version 2.0; local hash registration pending |

Do not treat an inventory listing as proof of content quality, dataset validity, provenance, or publication rights.
