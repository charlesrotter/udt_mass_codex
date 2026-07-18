#!/usr/bin/env python3
"""Fail-closed verification of the R1C correction preregistration."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


ACTIVE_LANES = {"FOUNDATIONS", "NATIVE_ACTION", "PARTICLE_MASS", "MACRO"}
SELECTOR_PATHS = {
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, text=True, stdout=subprocess.PIPE
    ).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    frozen = json.loads(args.inputs.read_text(encoding="utf-8"))
    assert git(repo, "rev-parse", frozen["base"]) == frozen["base"]
    for relative, expected in frozen["inputs"].items():
        assert sha256(repo / relative) == expected, relative

    ownership = {row["current_path"]: row for row in rows(repo / "research/_registry/ROOT_OWNERSHIP.tsv")}
    readiness_rows = rows(repo / "research/_registry/MIGRATION_READINESS.tsv")
    readiness = {row["current_path"]: row for row in readiness_rows}
    assert len(readiness) == len(readiness_rows)
    expected = {
        path: {
            "current_path": path,
            "primary_owner": readiness[path]["primary_owner"],
            "migration_readiness": readiness[path]["migration_readiness"],
            "blocking_or_change_requirement": readiness[path]["blocking_or_change_requirement"],
            "recommended_destination_if_migrated": readiness[path]["recommended_destination_if_migrated"],
        }
        for path in readiness
        if readiness[path]["migration_readiness"] == "MOVE_READY"
        and ownership[path]["primary_owner"] in ACTIVE_LANES
    }
    actual_rows = rows(args.candidates)
    actual = {row["current_path"]: row for row in actual_rows}
    assert len(actual_rows) == len(actual) == frozen["candidate_count"] == 13
    assert actual == expected
    assert not (set(actual) & SELECTOR_PATHS)

    for path in SELECTOR_PATHS:
        row = readiness[path]
        assert row["migration_readiness"] == "IMMUTABLE_PATH"
        assert row["blocking_or_change_requirement"] == "R0_FROZEN_EVIDENCE"
        assert row["recommended_destination_if_migrated"] == "-"

    result = {
        "result": "PASS",
        "base": frozen["base"],
        "candidate_count": len(actual),
        "candidate_paths_sha256": hashlib.sha256(
            "\n".join(sorted(actual)).encode("utf-8")
        ).hexdigest(),
        "selector_audit_paths_excluded": "PASS",
        "selector_audit_paths_confirmed_immutable": "PASS",
        "frozen_input_hashes": "PASS",
        "research_artifact_moves_renames_copies_deletes": 0,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

