# Chunking and Sanitization

## Scope and evidence

This document describes the existing standard chunking, boundary-aware V2 chunking, sanitization, and frozen-corpus artifacts. It is an evidence-based reconstruction. Historical scripts were not rerun.

## Tokenizer

The recorded tokenizer is `Qwen/Qwen2.5-1.5B-Instruct`.

An immutable model revision or commit hash was not recorded. The semantic chunking implementation used `trust_remote_code=True`.

## Standard chunking

Script: `08_create_chunks.py`

Recorded configuration:

- Target chunk size: 450 tokens.
- Minimum: 300 tokens.
- Maximum: 600 tokens.
- Overlap: 50 tokens.
- Special tokens excluded from token counts.
- Fixed token windows with nominal stride 400.
- Explicit `[PAGE BREAK]` separators between pages.

Output: `data/processed/chunks.jsonl`

Observed corpus:

| Metric | Value |
|---|---:|
| Chunks | 104 |
| Total tokens | 46,634 |
| Average tokens | 448.4 |
| Minimum tokens | 338 |
| Maximum tokens | 452 |
| Underfilled | 0 |
| Overfilled | 0 |

By document:

| Document ID | Chunks |
|---|---:|
| `iot_cloud_case_studies` | 17 |
| `iot_unit1` | 59 |
| `iot_unit2` | 9 |
| `iot_unit4_protocols_security` | 19 |

Page references may overlap between adjacent chunks.

## Boundary-aware V2 chunking

Script: `08b_create_semantic_chunks.py`

This implementation is boundary-aware, not embedding-based semantic segmentation.

The recorded method:

1. Reads the merged page corpus.
2. Uses paragraph/sentence-like regular-expression boundaries.
3. Preserves page references.
4. Splits units exceeding 600 tokens into pieces of up to 500 tokens.
5. Segments contiguous page sequences.
6. Packs units around a 450-token target, with a 600-token maximum.
7. Uses no chunk overlap.
8. Attempts to merge short final chunks where possible.

Output: `data/processed/chunks_v2.jsonl`

Observed corpus:

| Metric | Value |
|---|---:|
| Source pages | 407 usable pages |
| Contiguous segments | 15 |
| Chunks | 91 |
| Total tokens | 40,172 |
| Average tokens | 441.45 |
| Minimum tokens | 67 |
| Maximum tokens | 592 |
| Within 300–600 tokens | 81 |
| Underfilled | 10 |
| Overfilled | 0 |
| Token-split chunks | 0 |

Underfilled chunk token counts:

`170, 271, 217, 252, 192, 208, 115, 172, 67, 132`

By document:

| Document ID | Chunks |
|---|---:|
| `iot_cloud_case_studies` | 14 |
| `iot_unit1` | 51 |
| `iot_unit2` | 10 |
| `iot_unit4_protocols_security` | 16 |

The historical reason for choosing V2 rather than the standard chunking output is not established by the available evidence.

## Sanitization

Script: `13_sanitize_training_chunks.py`

Input: `chunks_v2.jsonl`

Output: `chunks_sanitized.jsonl`

The recorded detection patterns include:

- Credential-like assignments.
- Recognizable Google, AWS, GitHub, and `sk`-style tokens.
- Bearer tokens.
- Private-key blocks.
- Heuristic quoted alphanumeric identifiers of at least 16 characters.

The recorded sanitization report identifies one modified chunk and one redaction, categorized as `suspicious_quoted_string`. The modified chunk is:

`iot_cloud_case_studies_chunk_0008`

The raw value is intentionally not reproduced here.

The previous audit found matching chunk IDs, order, and non-content metadata, with one redaction marker. It did not establish that all possible secrets were absent. Manual review remains required. If a value is suspected to be an active credential, it should be revoked or rotated.

## Frozen corpus

Frozen output:

`data/frozen/chunks_v1_frozen.jsonl`

The filename is historical; the contents correspond to the sanitized V2 corpus.

| Property | Value |
|---|---|
| Records | 91 |
| Bytes | 213,930 |
| SHA-256 | `67e90d3428ff0a421111e19916ceb2dfc007460ae047f18131131be2f80bb827` |

The original source copy and the recovery mirror were independently checked. Both match the recorded size and SHA-256 digest.

The V2 input corpus has SHA-256:

`b9f61a023f681591cc3f23c8a4c06c038a6cc6a9fab9e3f6159a53ad711c8e7c`

The sanitized corpus has SHA-256:

`67e90d3428ff0a421111e19916ceb2dfc007460ae047f18131131be2f80bb827`

## Lineage

```text
extracted_text.jsonl (429 page records)
        |
        v
recovered_image_pages.jsonl (19 records)
        |
        v
merged_pages.jsonl (429 records; 407 usable)
        |
        +---------------------------+
        |                           |
        v                           v
chunks.jsonl                  chunks_v2.jsonl
104 chunks                    91 chunks
                                    |
                                    v
                            chunks_sanitized.jsonl
                                    |
                                    v
                            chunks_v1_frozen.jsonl
```

## Limitations

- Ten V2 chunks are below the configured minimum.
- The segmentation boundaries are rule-based.
- The tokenizer revision is not pinned.
- The historical V2 selection rationale is not recorded.
- Sanitization is heuristic and requires manual review.
- The absence of detected patterns does not prove that no secrets remain.
- Historical console transcripts for every processing script are not available.