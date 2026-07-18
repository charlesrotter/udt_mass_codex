#!/usr/bin/env python3
"""Independent metadata-only verifier for the frozen R1E candidate universe."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

BASE = "b59005dba9acaf6c575185876655bd6a5c792094"
MIGRATED = "simple_metric_S8_action_provenance_note.md"


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    out = Path(__file__).resolve().parent
    frozen = json.loads((out / "PREREGISTERED_INPUTS.json").read_text(encoding="utf-8"))
    assert frozen["base"] == BASE
    readiness = load(repo / "research/_registry/MIGRATION_READINESS.tsv")
    current = {row["original_path"]: row for row in load(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")}
    inventory = {row["path"]: row for row in load(repo / "reorganization_r1c/FROZEN_ROOT_INVENTORY.tsv")}
    expected = []
    for row in readiness:
        if row["migration_readiness"] != "MOVE_READY" or row["current_path"] == MIGRATED:
            continue
        original = row["current_path"]
        expected.append((original, current[original]["current_path"], row["primary_owner"],
                         inventory[original]["artifact_type"], inventory[original]["git_blob_oid"],
                         inventory[original]["sha256"], row["recommended_destination_if_migrated"],
                         row["migration_readiness"]))
    expected.sort()
    actual_rows = load(out / "PREREGISTERED_CANDIDATE_UNIVERSE.tsv")
    fields = ("original_path", "current_path", "primary_owner", "artifact_type",
              "fixed_base_blob_oid", "fixed_base_sha256", "recommended_destination", "migration_readiness")
    actual = sorted(tuple(row[field] for field in fields) for row in actual_rows)
    assert actual == expected
    assert len(actual) == len({row[0] for row in actual}) == len({row[1] for row in actual}) == 119
    assert MIGRATED not in {row[0] for row in actual}
    assert hashlib.sha256((out / "PREREGISTERED_CANDIDATE_UNIVERSE.tsv").read_bytes()).hexdigest() == frozen["candidate_tsv_sha256"]
    for path, digest in frozen["input_sha256"].items():
        assert hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest
    result = {"result": "PASS", "base": BASE, "candidate_rows": len(actual),
              "unique_original_paths": 119, "unique_current_paths": 119,
              "excluded_already_migrated": MIGRATED,
              "candidate_contents_inspected_before_freeze": False}
    (out / "PREREG_VERIFY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
