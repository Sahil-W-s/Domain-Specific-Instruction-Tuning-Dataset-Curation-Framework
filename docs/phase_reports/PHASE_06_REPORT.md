# Phase 6 Report — Source Processing, Chunking, and Sanitization

## Status

**PARTIALLY SATISFIED — evidence reconstruction and lineage validation completed; recovery and governance gaps remain.**

## Scope completed

The phase reconstructed the source-document extraction, image recovery, page merge, standard chunking, boundary-aware V2 chunking, sanitization, and frozen-corpus lineage from existing artifacts.

No historical extraction, vision recovery, chunking, or sanitization scripts were rerun.

## Source and page accounting

- Four source PDFs.
- 429 extracted page records.
- 393 pages with nonempty extracted text.
- 36 initially empty pages.
- 19 successful recovery records.
- 14 meaningful vision recoveries.
- 5 confirmed blank pages.
- 18 error records representing 17 unique failed pages.
- 429 merged page records.
- 407 usable merged pages.
- 22 unusable merged pages.

All 19 recovery records map to merged records. No recovery-to-merge mismatch was detected.

## Chunking

Standard chunking produced 104 chunks and 46,634 tokens.

Boundary-aware V2 produced 91 chunks and 40,172 tokens. It references the 407 usable merged pages. Ten chunks are underfilled; none are overfilled.

V2 was selected as the frozen corpus, but the historical rationale for that selection is not established.

## Sanitization and frozen corpus

The existing sanitization report records one modified chunk and one redaction. Manual review remains required.

The frozen corpus contains 91 records and is 213,930 bytes. Its SHA-256 digest is:

`67e90d3428ff0a421111e19916ceb2dfc007460ae047f18131131be2f80bb827`

The original and recovery copies match this digest and expected size.

## Validation

The generated validation artifact records:

- Extraction-to-merge page-key reconciliation.
- Recovery-to-merge reconciliation.
- Standard and V2 chunk source-page references.
- Sanitized chunk ID and metadata consistency.
- Frozen-to-sanitized record consistency.
- Frozen-copy SHA-256 verification.

The generated provenance graph records source documents, merged pages, standard chunks, V2 chunks, sanitized chunks, and frozen chunks, without embedding source content.

## Outstanding issues

1. Seventeen image pages remain unrecovered.
2. The historical recovery log contains a duplicated failure record for `iot_unit1` page 131.
3. Historical recovery summary arithmetic is inconsistent with final page classifications.
4. Source PDF author, publisher, edition, URL, and license are unknown.
5. Redistribution rights have not been cleared.
6. The tokenizer revision is not pinned to an immutable model commit.
7. The historical rationale for selecting V2 is not established.
8. Sanitization requires manual review and cannot guarantee absence of all secrets.
9. Historical execution transcripts for all processing scripts are unavailable.

## Deliverables

- `docs/methodology/source_document_processing.md`
- `docs/methodology/chunking_and_sanitization.md`
- `reports/validation/chunk_lineage_validation.json`
- `reports/validation/source_page_chunk_provenance.json`
- `docs/phase_reports/PHASE_06_REPORT.md`

## Completion decision

Do not mark Phase 6 fully complete while the unresolved recovery, source-rights, and sanitization-review issues remain open. Preserve the frozen corpus unchanged. Do not rerun historical pipeline scripts or make paid API requests as part of this evidence reconstruction.