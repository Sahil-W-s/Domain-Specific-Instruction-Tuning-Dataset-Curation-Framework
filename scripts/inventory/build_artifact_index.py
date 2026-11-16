import argparse
import json
import os
import sqlite3
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = ROOT / "manifests" / "artifact_registry.jsonl"
DEFAULT_OUTPUT = ROOT / "artifacts" / "index" / "artifact_index.sqlite"

TEXT_FIELDS = (
    "source_root_id", "relative_path", "file_name", "extension",
    "last_write_time_utc", "artifact_type", "lifecycle", "phase",
    "sensitivity", "redistribution_status", "hash_algorithm",
    "sha256", "hash_status", "first_seen_run_id", "last_verified_utc",
)

def read_registry(path):
    records = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc

            if not isinstance(record, dict) or not record.get("artifact_id"):
                raise ValueError(f"Missing artifact_id on line {line_number}")

            record["size_bytes"] = int(record["size_bytes"])
            records.append(record)

    ids = [r["artifact_id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate artifact_id values found in registry")

    return records

def build(registry, output):
    if not registry.is_file():
        raise FileNotFoundError(registry)

    output.parent.mkdir(parents=True, exist_ok=True)

    # Never overwrite an existing index.
    if output.exists():
        raise FileExistsError(
            f"Index already exists: {output}. Inspect it before rebuilding."
        )

    records = read_registry(registry)
    if not records:
        raise ValueError("Registry contains no artifact records")

    fd, temp_name = tempfile.mkstemp(
        prefix=".artifact_index_", suffix=".sqlite", dir=output.parent
    )
    os.close(fd)
    temp_path = Path(temp_name)

    try:
        conn = sqlite3.connect(temp_path)
        try:
            conn.execute("PRAGMA journal_mode=DELETE")
            conn.execute("""
                CREATE TABLE artifacts (
                    artifact_id TEXT PRIMARY KEY,
                    source_root_id TEXT,
                    relative_path TEXT,
                    file_name TEXT,
                    extension TEXT,
                    size_bytes INTEGER NOT NULL,
                    last_write_time_utc TEXT,
                    artifact_type TEXT,
                    lifecycle TEXT,
                    phase TEXT,
                    sensitivity TEXT,
                    redistribution_status TEXT,
                    hash_algorithm TEXT,
                    sha256 TEXT,
                    hash_status TEXT,
                    first_seen_run_id TEXT,
                    last_verified_utc TEXT
                )
            """)

            conn.execute("""
                CREATE VIRTUAL TABLE artifact_search USING fts5(
                    artifact_id UNINDEXED,
                    file_name,
                    relative_path,
                    source_root_id,
                    artifact_type,
                    lifecycle,
                    phase,
                    tokenize='unicode61'
                )
            """)

            for r in records:
                values = (
                    r["artifact_id"],
                    str(r.get("source_root_id") or ""),
                    str(r.get("relative_path") or ""),
                    str(r.get("file_name") or ""),
                    str(r.get("extension") or ""),
                    int(r["size_bytes"]),
                    str(r.get("last_write_time_utc") or ""),
                    str(r.get("artifact_type") or ""),
                    str(r.get("lifecycle") or ""),
                    str(r.get("phase") or ""),
                    str(r.get("sensitivity") or ""),
                    str(r.get("redistribution_status") or ""),
                    str(r.get("hash_algorithm") or ""),
                    str(r.get("sha256") or ""),
                    str(r.get("hash_status") or ""),
                    str(r.get("first_seen_run_id") or ""),
                    str(r.get("last_verified_utc") or ""),
                )
                conn.execute(
                    "INSERT INTO artifacts VALUES (" + ",".join("?" * 17) + ")",
                    values
                )
                conn.execute("""
                    INSERT INTO artifact_search
                    (artifact_id, file_name, relative_path, source_root_id,
                     artifact_type, lifecycle, phase)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    r["artifact_id"],
                    str(r.get("file_name") or ""),
                    str(r.get("relative_path") or ""),
                    str(r.get("source_root_id") or ""),
                    str(r.get("artifact_type") or ""),
                    str(r.get("lifecycle") or ""),
                    str(r.get("phase") or ""),
                ))

            conn.execute("CREATE INDEX idx_artifact_root ON artifacts(source_root_id)")
            conn.execute("CREATE INDEX idx_artifact_type ON artifacts(artifact_type)")
            conn.execute("CREATE INDEX idx_artifact_lifecycle ON artifacts(lifecycle)")
            conn.execute("PRAGMA user_version=1")
            conn.commit()

            integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
            indexed_count = conn.execute(
                "SELECT COUNT(*) FROM artifacts"
            ).fetchone()[0]
            search_count = conn.execute(
                "SELECT COUNT(*) FROM artifact_search"
            ).fetchone()[0]

            if integrity != "ok" or indexed_count != len(records) or search_count != len(records):
                raise RuntimeError("Index integrity or record-count check failed")
        finally:
            conn.close()

        # Atomic, no-overwrite publication.
        os.link(temp_path, output)
        print(f"[PASS] Registry records indexed: {len(records)}")
        print(f"[PASS] FTS5 records indexed: {len(records)}")
        print("[PASS] SQLite integrity check")
        print(f"[CREATED] {output}")

    finally:
        temp_path.unlink(missing_ok=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build(args.registry.resolve(), args.output.resolve())
