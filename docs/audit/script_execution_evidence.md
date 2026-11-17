# Phase 5 — Script Execution Evidence

Only direct log and artifact evidence is used for verified classifications.

## Verified execution records

### 01_extract_pdfs.py

- Status: `executed_verified`.
- Log: `logs/pdf_extraction.log`.
- Four documents; 429 pages; 393 nonempty; 36 empty; extraction rate 91.61%.
- Completion marker recorded.
- Outputs: `data/extracted/extracted_text.jsonl` and `data/extracted/extraction_quality.csv`.

### 02_inspect_empty_pages.py

- Status: `executed_verified`.
- Log: `logs/empty_page_diagnostics.log`.
- 36 pages inspected; completion marker recorded.
- Output: `data/extracted/empty_page_diagnostics.csv`.

### 04_recover_image_pages.py

- Status: `executed_verified`; outcome was partial, not complete.
- Log: `logs/image_recovery.log`.
- Successful recovery records are present; final session reported 19 previously recovered pages.
- Final session attempted one page, recorded zero new successes, and stopped on HTTP 402 Payment Required.
- The log reported 16 pages remaining.
- Outputs: `data/recovered/recovered_image_pages.jsonl` and `data/recovered/recovery_errors.jsonl`.
- Billing/quota failure is evidenced; total expenditure is not established.

## Evidence fingerprints

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| `logs/pdf_extraction.log` | 1802 | `2641E1E4950C19A1E59A4533ADCA8C1921EC17441A6171FCC7563FAE5981192A` |
| `logs/empty_page_diagnostics.log` | 1005 | `E4940DE050C8611767B7B459757AF9F83797FDF66F934FBC5D8E3FEAFEFBA8FB` |
| `logs/image_recovery.log` | 106305 | `A9C203E087F36239FA9295A074423B2C0C24E437777ADCE21F0022A58DF95099` |
| `data/extracted/extracted_text.jsonl` | 213727 | `86CF942C08308553A493A0A7026297D5DB76F2B6268459BB2C8BC357AF03FE2A` |
| `data/extracted/extraction_quality.csv` | 789 | `EF8EE9BDA90372C2A500728CA5015E37AC60BBBE837AB707DF7F0EA5F0165222` |
| `data/extracted/empty_page_diagnostics.csv` | 4847 | `02B800F51036213EE71401714A8AC494641BCCBAC0F0E5837C7C765B8B15A7C0` |
| `data/recovered/recovered_image_pages.jsonl` | 36056 | `1ED4563714FD972CD60AD98B482A187A52DACE5B4C608E757EEDAADF951574D3` |
| `data/recovered/recovery_errors.jsonl` | 20630 | `E45DB26E912ED27A2E826785F8C6F331DC300B8BC713DD6571EA97B706E46740` |

## Remaining scripts

All other catalogue entries remain `unknown` for execution unless separate direct evidence is added. Source presence, archive membership, file timestamps, and script names alone are not execution evidence.
