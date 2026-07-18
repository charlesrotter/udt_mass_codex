#!/usr/bin/env python3
"""Freeze R1E's exact metadata-only MOVE_READY candidate universe."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

BASE = "b59005dba9acaf6c575185876655bd6a5c792094"
MIGRATED = "simple_metric_S8_action_provenance_note.md"


def run(repo: Path, command: list[str]) -> str:
    result = subprocess.run(command, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, check=False)
    if result.returncode:
        raise AssertionError(f"command failed: {' '.join(command)}\n{result.stderr}")
    return result.stdout


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    out = Path(__file__).resolve().parent
    assert run(repo, ["git", "rev-parse", "HEAD"]).strip() == BASE
    readiness_path = repo / "research/_registry/MIGRATION_READINESS.tsv"
    current_path = repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv"
    inventory_path = repo / "reorganization_r1c/FROZEN_ROOT_INVENTORY.tsv"
    readiness = load(readiness_path)
    current = {row["original_path"]: row for row in load(current_path)}
    inventory = {row["path"]: row for row in load(inventory_path)}
    move_ready = [row for row in readiness if row["migration_readiness"] == "MOVE_READY"]
    assert len(move_ready) == 120
    rows = []
    for row in move_ready:
        original = row["current_path"]
        assert original in current and original in inventory
        if original == MIGRATED:
            assert current[original]["path_status"] == "MIGRATED_R1D"
            continue
        resolved = current[original]["current_path"]
        assert current[original]["path_status"] == "ROOT_RETAINED"
        assert (repo / resolved).exists()
        fixed = inventory[original]
        rows.append({
            "original_path": original,
            "current_path": resolved,
            "primary_owner": row["primary_owner"],
            "artifact_type": fixed["artifact_type"],
            "fixed_base_blob_oid": fixed["git_blob_oid"],
            "fixed_base_sha256": fixed["sha256"],
            "recommended_destination": row["recommended_destination_if_migrated"],
            "migration_readiness": row["migration_readiness"],
        })
    rows.sort(key=lambda item: item["original_path"])
    assert len(rows) == len({row["original_path"] for row in rows}) == len({row["current_path"] for row in rows}) == 119
    output = out / "PREREGISTERED_CANDIDATE_UNIVERSE.tsv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    report = {
        "result": "PASS",
        "base": BASE,
        "candidate_rule": "fixed R1C migration_readiness == MOVE_READY resolved through current map, excluding migrated S8",
        "fixed_move_ready_rows_before_exclusion": len(move_ready),
        "excluded_already_migrated": MIGRATED,
        "candidate_rows": len(rows),
        "unique_original_paths": len({row["original_path"] for row in rows}),
        "unique_current_paths": len({row["current_path"] for row in rows}),
        "candidate_tsv_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "input_sha256": {
            "research/_registry/MIGRATION_READINESS.tsv": hashlib.sha256(readiness_path.read_bytes()).hexdigest(),
            "research/_registry/CURRENT_ARTIFACT_PATHS.tsv": hashlib.sha256(current_path.read_bytes()).hexdigest(),
            "reorganization_r1c/FROZEN_ROOT_INVENTORY.tsv": hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
        },
        "candidate_contents_inspected_before_freeze": False,
        "artifact_mutations": 0,
    }
    (out / "PREREGISTERED_INPUTS.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
