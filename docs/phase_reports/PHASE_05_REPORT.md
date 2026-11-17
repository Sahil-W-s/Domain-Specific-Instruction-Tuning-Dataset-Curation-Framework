# Phase 05 Report — Script Catalogue, Dependencies and Execution Evidence

Project: ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework

## Deliverables

- `docs/audit/script_catalogue.md`
- `reports/inventory/script_catalogue.csv`
- `reports/inventory/script_dependency_edges.csv`
- `docs/audit/script_execution_evidence.md`
- `docs/phase_reports/PHASE_05_REPORT.md`

## Inventory result

- Refined script entries: 74.
- Main archive Python files: 73.
- Pipeline archive subset: 13.
- Pipeline subset members also present in main archive: 13.
- Static dependency/path-reference edges: 258.

## Execution evidence result

- Scripts 01 and 02 have completion logs and corresponding output inventory records.
- Script 04 has direct recovery log and output evidence, but the final session stopped on a billing/quota error.
- Other scripts remain execution-unknown until direct evidence is located.

## Historical variant findings

- 35b and 35c are identical-content files; both filenames are retained.
- 35d is a distinct resumable benchmark implementation.
- 47/48, 52/53, 55/60, and 56/61 are distinct historical variants.
- 58 and pipeline_judge.py are related but not identical.
- The three Phase 3 preparation scripts are distinct; V2 adds stronger validation and exclusive output creation.
- 08 and 08b are distinct chunking implementations.

## Risk and limitations

- API indicators do not establish actual execution or total cost.
- Static path references are candidate dependency edges, not runtime-confirmed data flow.
- Potential write operations require review; static inspection cannot guarantee absence of side effects.
- No historical script was executed during this phase.
- Source archives and original inventory files were read only.

## Phase 5 exit gate

**Status: PARTIALLY SATISFIED — do not mark Phase 5 complete yet.**

The script inventory and major historical variants are catalogued. Initial execution evidence is established for scripts 01, 02 and 04. However, execution evidence for later generation, evaluation, repair, reconciliation and Phase 3 preparation stages has not yet been established. The dependency graph is a static candidate graph and requires evidence-backed confirmation for critical lineage edges.

Recommended next action: use existing logs and output artifacts to establish the execution lineage of the later production-generation and reconciliation scripts. Do not rerun historical scripts merely to manufacture execution evidence.
