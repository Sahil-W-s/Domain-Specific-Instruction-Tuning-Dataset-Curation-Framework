import ast
import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path
from collections import defaultdict

ROOT = Path.cwd()

REFINED = ROOT / "docs" / "audit" / "refined_script_catalogue.csv"
MAIN_ZIP = Path(r"C:\Users\Sahil\Downloads\MLCP UPLOAD\ML CP\MLCP_scripts.zip")
PIPELINE_ZIP = Path(r"C:\Users\Sahil\Downloads\MLCP UPLOAD\ML CP\pipeline_source_scripts.zip")

SOURCE_BASE = Path(r"C:\Users\Sahil\Downloads\MLCP UPLOAD\ML CP")

OUTPUTS = [
    ROOT / "docs/audit/script_catalogue.md",
    ROOT / "reports/inventory/script_catalogue.csv",
    ROOT / "reports/inventory/script_dependency_edges.csv",
    ROOT / "docs/audit/script_execution_evidence.md",
    ROOT / "docs/phase_reports/PHASE_05_REPORT.md",
]

for path in OUTPUTS:
    if path.exists():
        raise SystemExit(
            f"Refusing to overwrite existing deliverable: {path}"
        )

for path in (REFINED, MAIN_ZIP, PIPELINE_ZIP):
    if not path.exists():
        raise SystemExit(f"Required source not found: {path}")

with REFINED.open("r", encoding="utf-8-sig", newline="") as f:
    refined_rows = list(csv.DictReader(f))

refined = {r["FileName"]: r for r in refined_rows}

if len(refined) != len(refined_rows):
    raise SystemExit("Duplicate filenames in refined catalogue.")

# The following execution classifications are supported by the inspected logs.
execution = {
    "01_extract_pdfs.py": ("executed_verified", "PDF extraction completed"),
    "02_inspect_empty_pages.py": ("executed_verified", "36 pages inspected"),
    "04_recover_image_pages.py": (
        "executed_verified",
        "Partial recovery; final session stopped on HTTP 402 quota exhaustion"
    ),
}

variant_notes = {
    "08b_create_semantic_chunks.py":
        "Separate semantic chunking implementation; writes V2 chunk outputs.",
    "35b_benchmark_groq_judge.py":
        "Byte-identical content to 35c; retain both historical filenames.",
    "35c_resume_groq_judge_benchmark.py":
        "Byte-identical content to 35b; retain both historical filenames.",
    "35d_resume_groq_judge_benchmark.py":
        "Distinct resumable benchmark implementation.",
    "47_reconcile_judge_results.py":
        "Earlier reconciliation variant; compare with 48.",
    "48_reconcile_judge_results_fixed.py":
        "Changes source text field and isolates reconciliation_v2 output.",
    "52_judge_hma_repair_groq.py":
        "Earlier HMA judge variant; compare with 53.",
    "53_judge_hma_repair_groq_fixed.py":
        "Adds retrieval of full source chunks from frozen corpus.",
    "55_generate_production_v2.py":
        "Earlier V2 generator; uses temporary-file replacement strategy.",
    "60_generate_production_v2_resumable.py":
        "Recovery-safe resumable V2 generator; direct append and fsync behavior.",
    "56_audit_generation_v2.py":
        "Earlier V2 audit implementation.",
    "61_audit_generation_v2.py":
        "Expanded/resumed V2 audit implementation with broader scope.",
    "pipeline_judge.py":
        "Related to script 58; supports environment-variable input/output overrides.",
    "prepare_phase3_datasets.py":
        "Earlier Phase 3 preparation variant.",
    "prepare_phase3_datasets_corrected.py":
        "Adds exact evidence-block reconstruction and validation.",
    "prepare_phase3_datasets_v2.py":
        "Adds source fingerprints, count checks and exclusive output creation.",
}

def sha256(data):
    return hashlib.sha256(data).hexdigest().upper()

def path_expression(node, path_vars):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value

    if isinstance(node, ast.Name):
        return path_vars.get(node.id)

    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left = path_expression(node.left, path_vars)
        right = path_expression(node.right, path_vars)

        if right:
            return f"{left}/{right}" if left else right

    if isinstance(node, ast.Call):
        if node.args:
            return path_expression(node.args[0], path_vars)

    return None

def looks_like_path(value):
    if not value or len(value) > 300:
        return False

    value = value.replace("\\", "/").lower()

    if not re.search(
        r"\.(py|jsonl|json|csv|txt|pdf|zip|log|yaml|yml|parquet)$",
        value
    ):
        return False

    return any(
        token in value
        for token in (
            "data/", "logs/", "artifacts/", "reports/",
            "scripts/", "checkpoints/", "outputs/"
        )
    )

def inspect_source(source):
    result = {
        "docstring": "",
        "imports": set(),
        "calls": set(),
        "api": set(),
        "writes": set(),
        "path_refs": set(),
        "edges": set(),
        "parse_error": "",
    }

    try:
        tree = ast.parse(source.decode("utf-8-sig"))
    except Exception as exc:
        result["parse_error"] = str(exc)
        return result

    result["docstring"] = ast.get_docstring(tree) or ""

    path_vars = {}

    # First pass: resolve common path constants.
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value_node = node.value

            if value_node is None:
                continue

            for target in targets:
                if isinstance(target, ast.Name):
                    value = path_expression(value_node, path_vars)
                    if value and looks_like_path(value):
                        path_vars[target.id] = value

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result["imports"].update(a.name for a in node.names)

        elif isinstance(node, ast.ImportFrom):
            result["imports"].add(node.module or "(relative import)")

        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if looks_like_path(node.value):
                result["path_refs"].add(node.value.replace("\\", "/"))

        elif isinstance(node, ast.Call):
            func = node.func
            name = (
                func.id if isinstance(func, ast.Name)
                else func.attr if isinstance(func, ast.Attribute)
                else ""
            )

            if not name:
                continue

            result["calls"].add(name)
            low = name.lower()

            if any(k in low for k in (
                "write", "save", "dump", "export", "unlink",
                "remove", "replace", "rename", "copy", "move"
            )):
                result["writes"].add(name)

            if low in ("read_text", "read_bytes", "read_csv",
                       "read_json", "read_jsonl", "load_jsonl",
                       "load_dataset"):
                relation = "read"

            elif any(k in low for k in (
                "write", "save", "dump", "export", "to_csv"
            )):
                relation = "write"

            elif low == "open":
                modes = [
                    a.value for a in node.args[1:]
                    if isinstance(a, ast.Constant)
                    and isinstance(a.value, str)
                ]
                mode = modes[0] if modes else ""

                if any(x in mode for x in ("w", "a", "x")):
                    relation = "write"
                elif "r" in mode or not mode:
                    relation = "read"
                else:
                    relation = "reference"
            else:
                relation = "reference"

            candidates = []

            for arg in list(node.args) + [
                kw.value for kw in node.keywords
            ]:
                value = path_expression(arg, path_vars)
                if value and looks_like_path(value):
                    candidates.append(value.replace("\\", "/"))

            for value in candidates:
                result["path_refs"].add(value)
                result["edges"].add((
                    value, relation, name, getattr(node, "lineno", "")
                ))

    imports_text = " ".join(result["imports"]).lower()
    source_text = source.decode("utf-8-sig", errors="replace").lower()

    for indicator in (
        "google.genai", "groq", "openai", "requests",
        "httpx", "anthropic", "transformers"
    ):
        if indicator in imports_text:
            result["api"].add(indicator)

    for host in (
        "generativelanguage.googleapis.com",
        "api.groq.com",
        "openrouter.ai",
        "api.openai.com"
    ):
        if host in source_text:
            result["api"].add(host)

    return result

# Read the two archives. The second archive is a subset, not extra scripts.
with zipfile.ZipFile(MAIN_ZIP) as z:
    main_members = {
        Path(n).name: z.read(n)
        for n in z.namelist()
        if n.lower().endswith(".py")
    }

with zipfile.ZipFile(PIPELINE_ZIP) as z:
    pipeline_members = {
        Path(n).name
        for n in z.namelist()
        if n.lower().endswith(".py")
    }

if len(main_members) != 73:
    raise SystemExit(
        f"Expected 73 Python files in main archive; found {len(main_members)}"
    )

if not pipeline_members.issubset(main_members):
    raise SystemExit("Pipeline archive contains entries not found in main archive.")

records = []
dependency_edges = []
source_hashes = {}

for filename, metadata in refined.items():
    source = main_members.get(filename)
    archive_membership = []

    if source is not None:
        archive_membership.append("MLCP_scripts.zip")
        if filename in pipeline_members:
            archive_membership.append("pipeline_source_scripts.zip")

        actual_hash = sha256(source)
        actual_size = len(source)

        if actual_hash != metadata["SHA256"].upper():
            raise SystemExit(f"SHA-256 mismatch for {filename}")

        if actual_size != int(metadata["SizeBytes"]):
            raise SystemExit(f"Size mismatch for {filename}")

        inspection = inspect_source(source)
        inspection_status = "inspected"

    elif filename == "pipeline.py":
        archive_membership.append("standalone source")

        candidates = [
            SOURCE_BASE / "pipeline.py",
            ROOT / "pipeline.py",
            ROOT / "scripts" / "pipeline.py",
        ]
        local_source = next((p for p in candidates if p.is_file()), None)

        if local_source:
            source = local_source.read_bytes()
            actual_hash = sha256(source)
            actual_size = len(source)

            if actual_hash != metadata["SHA256"].upper():
                raise SystemExit("pipeline.py SHA-256 mismatch")

            if actual_size != int(metadata["SizeBytes"]):
                raise SystemExit("pipeline.py size mismatch")

            inspection = inspect_source(source)
            inspection_status = "inspected"
        else:
            inspection = {
                "docstring": "",
                "imports": set(),
                "calls": set(),
                "api": set(),
                "writes": set(),
                "path_refs": set(),
                "edges": set(),
                "parse_error": "Source file not found at expected locations",
            }
            inspection_status = "exists"

    else:
        raise SystemExit(f"Refined catalogue entry not found in archive: {filename}")

    source_hashes[filename] = metadata["SHA256"].upper()

    execution_status, execution_note = execution.get(
        filename, ("unknown", "No direct execution evidence established")
    )

    if filename in ("35b_benchmark_groq_judge.py",
                    "35c_resume_groq_judge_benchmark.py"):
        lifecycle = "identical_content_historical_variants"
    elif filename in variant_notes:
        lifecycle = "historical_variant"
    else:
        lifecycle = "not_determined"

    doc = inspection["docstring"].strip()
    role = doc.splitlines()[0].strip() if doc else Path(filename).stem.replace("_", " ")

    records.append({
        "FileName": filename,
        "RelativePath": metadata["RelativePath"],
        "SizeBytes": metadata["SizeBytes"],
        "SHA256": metadata["SHA256"].upper(),
        "ArchiveMembership": ";".join(archive_membership),
        "InspectionStatus": inspection_status,
        "ExecutionStatus": execution_status,
        "ExecutionEvidence": execution_note,
        "Role": role,
        "ModuleDocstring": doc,
        "Imports": ";".join(sorted(inspection["imports"])),
        "ExternalAPIIndicators": ";".join(sorted(inspection["api"])),
        "PotentialWriteOperations": ";".join(sorted(inspection["writes"])),
        "PotentialOverwriteRisk": (
            "review_required" if inspection["writes"] else "not_detected_by_static_scan"
        ),
        "PathReferences": ";".join(sorted(inspection["path_refs"])),
        "Lifecycle": lifecycle,
        "LineageNotes": variant_notes.get(filename, ""),
        "ParseError": inspection["parse_error"],
    })

    for artifact, relation, call, line in inspection["edges"]:
        dependency_edges.append({
            "ScriptFile": filename,
            "ArtifactPath": artifact,
            "Relationship": relation,
            "Evidence": f"AST call: {call}",
            "SourceLine": line,
            "Confidence": "static_reference_requires_review",
        })

if len(records) != 74:
    raise SystemExit(f"Expected 74 refined entries; generated {len(records)}")

# Fingerprints supplied from the inspected local execution evidence.
evidence_files = [
    ("logs/pdf_extraction.log", 1802,
     "2641E1E4950C19A1E59A4533ADCA8C1921EC17441A6171FCC7563FAE5981192A"),
    ("logs/empty_page_diagnostics.log", 1005,
     "E4940DE050C8611767B7B459757AF9F83797FDF66F934FBC5D8E3FEAFEFBA8FB"),
    ("logs/image_recovery.log", 106305,
     "A9C203E087F36239FA9295A074423B2C0C24E437777ADCE21F0022A58DF95099"),
    ("data/extracted/extracted_text.jsonl", 213727,
     "86CF942C08308553A493A0A7026297D5DB76F2B6268459BB2C8BC357AF03FE2A"),
    ("data/extracted/extraction_quality.csv", 789,
     "EF8EE9BDA90372C2A500728CA5015E37AC60BBBE837AB707DF7F0EA5F0165222"),
    ("data/extracted/empty_page_diagnostics.csv", 4847,
     "02B800F51036213EE71401714A8AC494641BCCBAC0F0E5837C7C765B8B15A7C0"),
    ("data/recovered/recovered_image_pages.jsonl", 36056,
     "1ED4563714FD972CD60AD98B482A187A52DACE5B4C608E757EEDAADF951574D3"),
    ("data/recovered/recovery_errors.jsonl", 20630,
     "E45DB26E912ED27A2E826785F8C6F331DC300B8BC713DD6571EA97B706E46740"),
]

def write_csv(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

# Prepare output content before writing.
catalogue_md = [
    "# Phase 5 — Script Catalogue",
    "",
    "Project: ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework",
    "",
    "## Scope and method",
    "",
    "- 74 refined entries: 73 Python files in MLCP_scripts.zip and standalone pipeline.py.",
    "- pipeline_source_scripts.zip contains 13 scripts already present in the main archive.",
    "- Archive source bytes were checked against the refined catalogue size and SHA-256.",
    "- Source was parsed statically; no historical script was imported or executed.",
    "- API indicators and path references are static findings, not proof of actual use.",
    "- Execution status is separate from file existence and source inspection.",
    "",
    "## Status interpretation",
    "",
    "- `inspected`: source was available and statically parsed.",
    "- `exists`: inventory entry exists, but source was not available for parsing.",
    "- `executed_verified`: direct log/output evidence supports execution.",
    "- `unknown`: no direct execution evidence was established.",
    "",
    "## Script register",
    "",
    "| Script | Role | Inspection | Execution | API indicators |",
    "|---|---|---|---|---|",
]

for r in records:
    role = r["Role"].replace("|", "/").replace("\n", " ")[:100]
    api = r["ExternalAPIIndicators"].replace("|", "/") or "—"
    catalogue_md.append(
        f'| `{r["FileName"]}` | {role} | {r["InspectionStatus"]} '
        f'| {r["ExecutionStatus"]} | {api} |'
    )

catalogue_md += [
    "",
    "## Historical variants and lineage notes",
    "",
]

for filename, note in variant_notes.items():
    catalogue_md.append(f"- `{filename}` — {note}")

catalogue_md += [
    "",
    "## Dependency graph limitations",
    "",
    "The CSV records statically detected path references associated with AST calls. "
    "These are candidate read/write/reference edges, not runtime-confirmed dependencies. "
    "Path expressions assembled dynamically, environment variables, helper functions, "
    "and indirect data flow may not be fully resolved.",
    "",
    "## API and overwrite-risk caveats",
    "",
    "API indicators show potential external-service integration. They do not prove a "
    "request was made or establish its cost. Write-operation indicators flag code paths "
    "for review; absence of a detected write call is not proof of read-only behavior.",
    "",
]

execution_md = [
    "# Phase 5 — Script Execution Evidence",
    "",
    "Only direct log and artifact evidence is used for verified classifications.",
    "",
    "## Verified execution records",
    "",
    "### 01_extract_pdfs.py",
    "",
    "- Status: `executed_verified`.",
    "- Log: `logs/pdf_extraction.log`.",
    "- Four documents; 429 pages; 393 nonempty; 36 empty; extraction rate 91.61%.",
    "- Completion marker recorded.",
    "- Outputs: `data/extracted/extracted_text.jsonl` and `data/extracted/extraction_quality.csv`.",
    "",
    "### 02_inspect_empty_pages.py",
    "",
    "- Status: `executed_verified`.",
    "- Log: `logs/empty_page_diagnostics.log`.",
    "- 36 pages inspected; completion marker recorded.",
    "- Output: `data/extracted/empty_page_diagnostics.csv`.",
    "",
    "### 04_recover_image_pages.py",
    "",
    "- Status: `executed_verified`; outcome was partial, not complete.",
    "- Log: `logs/image_recovery.log`.",
    "- Successful recovery records are present; final session reported 19 previously recovered pages.",
    "- Final session attempted one page, recorded zero new successes, and stopped on HTTP 402 Payment Required.",
    "- The log reported 16 pages remaining.",
    "- Outputs: `data/recovered/recovered_image_pages.jsonl` and `data/recovered/recovery_errors.jsonl`.",
    "- Billing/quota failure is evidenced; total expenditure is not established.",
    "",
    "## Evidence fingerprints",
    "",
    "| File | Size (bytes) | SHA-256 |",
    "|---|---:|---|",
]

for rel, size, digest in evidence_files:
    execution_md.append(f"| `{rel}` | {size} | `{digest}` |")

execution_md += [
    "",
    "## Remaining scripts",
    "",
    "All other catalogue entries remain `unknown` for execution unless separate direct "
    "evidence is added. Source presence, archive membership, file timestamps, and script "
    "names alone are not execution evidence.",
    "",
]

report_md = [
    "# Phase 05 Report — Script Catalogue, Dependencies and Execution Evidence",
    "",
    "Project: ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework",
    "",
    "## Deliverables",
    "",
    "- `docs/audit/script_catalogue.md`",
    "- `reports/inventory/script_catalogue.csv`",
    "- `reports/inventory/script_dependency_edges.csv`",
    "- `docs/audit/script_execution_evidence.md`",
    "- `docs/phase_reports/PHASE_05_REPORT.md`",
    "",
    "## Inventory result",
    "",
    f"- Refined script entries: {len(records)}.",
    f"- Main archive Python files: {len(main_members)}.",
    f"- Pipeline archive subset: {len(pipeline_members)}.",
    f"- Pipeline subset members also present in main archive: {len(pipeline_members.intersection(main_members))}.",
    f"- Static dependency/path-reference edges: {len(dependency_edges)}.",
    "",
    "## Execution evidence result",
    "",
    "- Scripts 01 and 02 have completion logs and corresponding output inventory records.",
    "- Script 04 has direct recovery log and output evidence, but the final session stopped on a billing/quota error.",
    "- Other scripts remain execution-unknown until direct evidence is located.",
    "",
    "## Historical variant findings",
    "",
    "- 35b and 35c are identical-content files; both filenames are retained.",
    "- 35d is a distinct resumable benchmark implementation.",
    "- 47/48, 52/53, 55/60, and 56/61 are distinct historical variants.",
    "- 58 and pipeline_judge.py are related but not identical.",
    "- The three Phase 3 preparation scripts are distinct; V2 adds stronger validation and exclusive output creation.",
    "- 08 and 08b are distinct chunking implementations.",
    "",
    "## Risk and limitations",
    "",
    "- API indicators do not establish actual execution or total cost.",
    "- Static path references are candidate dependency edges, not runtime-confirmed data flow.",
    "- Potential write operations require review; static inspection cannot guarantee absence of side effects.",
    "- No historical script was executed during this phase.",
    "- Source archives and original inventory files were read only.",
    "",
    "## Phase 5 exit gate",
    "",
    "**Status: PARTIALLY SATISFIED — do not mark Phase 5 complete yet.**",
    "",
    "The script inventory and major historical variants are catalogued. Initial execution "
    "evidence is established for scripts 01, 02 and 04. However, execution evidence for "
    "later generation, evaluation, repair, reconciliation and Phase 3 preparation stages "
    "has not yet been established. The dependency graph is a static candidate graph and "
    "requires evidence-backed confirmation for critical lineage edges.",
    "",
    "Recommended next action: use existing logs and output artifacts to establish the "
    "execution lineage of the later production-generation and reconciliation scripts. "
    "Do not rerun historical scripts merely to manufacture execution evidence.",
    "",
]

# Create output directories only after all source validation succeeds.
for path in OUTPUTS:
    path.parent.mkdir(parents=True, exist_ok=True)

write_csv(OUTPUTS[1], records)

edge_rows = sorted(
    dependency_edges,
    key=lambda r: (r["ScriptFile"], r["ArtifactPath"], r["Relationship"])
)
write_csv(OUTPUTS[2], edge_rows)

OUTPUTS[0].write_text("\n".join(catalogue_md) + "\n", encoding="utf-8")
OUTPUTS[3].write_text("\n".join(execution_md) + "\n", encoding="utf-8")
OUTPUTS[4].write_text("\n".join(report_md) + "\n", encoding="utf-8")

print("PHASE 5 DELIVERABLE GENERATION COMPLETE")
print("Catalogue entries:", len(records))
print("Main archive Python files:", len(main_members))
print("Pipeline subset:", len(pipeline_members))
print("Dependency/path-reference edges:", len(edge_rows))
print("\nCREATED:")
for path in OUTPUTS:
    print(path.relative_to(ROOT), path.stat().st_size, "bytes")

print("\nNo historical script was executed.")
