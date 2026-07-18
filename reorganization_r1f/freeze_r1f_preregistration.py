#!/usr/bin/env python3
"""Freeze the exact R1E B01 plan without inspecting verifier contents."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


BASE = "14ba31a77aed1553c5df8ecd59b0f7a000c10e20"
BATCH = "B01_ACTIVE_MACRO_SYMPY_QUARTET"
REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reorganization_r1f"
PLAN = REPO / "reorganization_r1e/PROPOSED_BATCH_FILE_PLAN.tsv"
INPUTS = [
    PLAN,
    REPO / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv",
    REPO / "research/macro/ROOT_INVENTORY.tsv",
    REPO / "reorganization_r1e/PROPOSED_MIGRATION_LEDGER_SCHEMA.tsv",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=REPO, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def main() -> int:
    if git("rev-parse", "HEAD") != BASE:
        raise AssertionError("R1F preregistration must be frozen at the exact dispatch base")
    with PLAN.open(encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if row["batch_id"] == BATCH]
    if len(rows) != 4 or len({row["current_path"] for row in rows}) != 4:
        raise AssertionError("B01 must contain exactly four unique paths")
    for row in rows:
        source = REPO / row["current_path"]
        destination = REPO / row["destination"]
        if not source.is_file() or destination.exists():
            raise AssertionError(f"bad pre-move path state: {row['current_path']}")
        if git("hash-object", "--no-filters", row["current_path"]) != row["git_blob_oid"]:
            raise AssertionError(f"blob mismatch: {row['current_path']}")
        if sha(source) != row["sha256"]:
            raise AssertionError(f"SHA-256 mismatch: {row['current_path']}")

    fields = list(rows[0])
    with (OUT / "PREREGISTERED_BATCH.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    payload = {
        "result": "PASS",
        "base": BASE,
        "branch": "codex/reorg-r1f-macro-verifier-quartet-2026-07-18",
        "batch_id": BATCH,
        "candidate_rows": 4,
        "candidate_contents_inspected_by_freezer": False,
        "artifact_mutations": 0,
        "input_sha256": {str(path.relative_to(REPO)): sha(path) for path in INPUTS},
        "preregistered_batch_sha256": sha(OUT / "PREREGISTERED_BATCH.tsv"),
        "pre_move_command_template": "env CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 timeout 30s python3 {current_path}",
        "post_move_command_template": "env CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 timeout 30s python3 {destination}",
        "timeout_seconds": 30,
        "behavior_gate": "same exit code and byte-identical stdout/stderr per script",
        "migration_status": "MIGRATED_R1F",
        "migration_commit_then_ledger_commit": True,
    }
    (OUT / "PREREGISTERED_INPUTS.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

