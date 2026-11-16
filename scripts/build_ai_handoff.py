import argparse
import json
import subprocess
import tempfile
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE_FILES = [
    "AI_WORK_PROTOCOL.md",
    "docs/ai_handoff/AI_START_HERE.md",
    "PROJECT_CONTEXT.md",
    "PROJECT_STATE.md",
    "NEXT_ACTION.md",
    "DECISIONS.md",
    "state/phase_status.yml",
]

RUNS_DIR = ROOT / "manifests" / "runs"
OUTPUT_DIR = ROOT / "docs" / "ai_handoff" / "generated"


def read_text(relative_path):
    path = ROOT / relative_path
    if not path.is_file():
        return f"[NOT FOUND: {relative_path}]"
    return path.read_text(encoding="utf-8-sig")


def git_info():
    def run(args):
        try:
            result = subprocess.run(
                args, cwd=ROOT, capture_output=True,
                text=True, timeout=10, check=False
            )
            return result.stdout.strip() if result.returncode == 0 else "Unavailable"
        except (OSError, subprocess.TimeoutExpired):
            return "Unavailable"

    return {
        "branch": run(["git", "branch", "--show-current"]),
        "commit": run(["git", "rev-parse", "--short", "HEAD"]),
        "status": run(["git", "status", "--short", "--branch"]),
    }


def recent_runs(limit=5):
    results = []
    warnings = []

    if not RUNS_DIR.is_dir():
        return results, ["Run-manifest directory not found."]

    for path in RUNS_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            results.append(data)
        except (OSError, json.JSONDecodeError) as exc:
            warnings.append(f"{path.name}: {exc}")

    results.sort(
        key=lambda item: str(item.get("started_at", "")),
        reverse=True
    )
    return results[:limit], warnings


def format_run(run):
    fields = [
        "run_id", "phase_id", "task_id", "status",
        "started_at", "finished_at", "command"
    ]
    lines = []
    for field in fields:
        if run.get(field) is not None:
            lines.append(f"- **{field}:** {run[field]}")

    for field in ("input_artifacts", "output_artifacts", "validation"):
        value = run.get(field)
        if value:
            lines.append(f"- **{field}:** `{json.dumps(value, ensure_ascii=False)}`")

    return "\n".join(lines) if lines else "- No run details available."


def build(args):
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%dT%H%M%SZ")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / f"AI_HANDOFF_{timestamp}.md"

    if output.exists():
        raise FileExistsError(f"Refusing to overwrite: {output}")

    git = git_info()
    runs, warnings = recent_runs()

    sections = [
        "# ML CP — Generated AI Handoff",
        "",
        f"**Generated:** {now.isoformat()}",
        "**Project:** ML CP — Domain-Specific Instruction-Tuning Dataset Curation Framework",
        f"**Current phase:** {args.current_phase}",
        f"**Current status:** {args.status}",
        "",
        "## Authoritative continuation instructions",
        "",
        args.next_action,
        "",
        "These continuation details were supplied explicitly when this handoff "
        "was generated. They take precedence over conflicting historical status "
        "statements in the source snapshots below.",
        "",
        "## Git checkpoint",
        "",
        f"- **Branch:** {git['branch']}",
        f"- **Commit:** {git['commit']}",
        "- **Working-tree status:**",
        "```text",
        git["status"] or "Clean",
        "```",
        "",
        "## Recent run manifests",
        "",
    ]

    if runs:
        for index, run in enumerate(runs, 1):
            sections.extend([
                f"### Run {index}",
                "",
                format_run(run),
                "",
            ])
    else:
        sections.extend(["No run manifests were found.", ""])

    if warnings:
        sections.extend(["### Run-manifest warnings", ""])
        sections.extend(f"- {warning}" for warning in warnings)
        sections.append("")

    sections.extend([
        "## Project source snapshots",
        "",
        "The following documents are included as source records. "
        "Their contents are preserved, not silently reconciled. "
        "If they conflict with the authoritative continuation instructions "
        "above, follow the latter and update the relevant project state "
        "documents through the normal approved workflow.",
        "",
    ])

    for relative_path in SOURCE_FILES:
        sections.extend([
            f"### `{relative_path}`",
            "",
            read_text(relative_path).rstrip(),
            "",
        ])

    sections.extend([
        "---",
        "",
        "## Handoff safety rules",
        "",
        "- Preserve original source material.",
        "- Do not delete, move, rename, or overwrite historical artifacts.",
        "- Do not expose secrets, credentials, or `.env` contents.",
        "- Do not repeat completed phases without an evidence-based reason.",
        "- Do not use `git add .`.",
        "- Stage, commit, or push only with explicit owner approval.",
        "- Validate only what is necessary to protect data and verify new functionality.",
        "",
    ])

    content = "\n".join(sections)

    fd, temp_name = tempfile.mkstemp(
        prefix=".handoff_", suffix=".tmp", dir=OUTPUT_DIR
    )
    temp_path = Path(temp_name)

    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())

        # Atomic publication without overwriting an existing handoff.
        os.link(temp_path, output)

        print("[PASS] Source documents collected")
        print(f"[PASS] Recent run manifests collected: {len(runs)}")
        print("[PASS] Git checkpoint collected")
        print("[PASS] Historical handoffs preserved")
        print(f"[CREATED] {output}")

    finally:
        temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a timestamped ML CP AI handoff."
    )
    parser.add_argument("--current-phase", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--next-action", required=True)
    build(parser.parse_args())
