#!/usr/bin/env python3
"""Build deterministic source lineage and checkpoint summary."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def normalize(value: str) -> str:
    return value.replace("-", "_")


def main() -> None:
    historical_sources = read_tsv(HERE / "CORRECTED_SOURCE_UNIVERSE.tsv")
    source_additions = read_tsv(HERE / "SECOND_PASS_SOURCE_ADDITIONS.tsv")
    sources = historical_sources + source_additions
    if (
        len(historical_sources) != 25
        or len(source_additions) != 1
        or len(sources) != 26
        or len({row["id"] for row in sources}) != 26
        or len({row["path"] for row in sources}) != 26
    ):
        raise AssertionError("source universe coverage")
    lineage = []
    for row in sources:
        path = ROOT / row["path"]
        data = path.read_bytes()
        lineage.append(
            {
                "id": row["id"],
                "path": row["path"],
                "role": row["role"],
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    write_tsv(HERE / "SOURCE_LINEAGE.tsv", lineage)

    contract = read_tsv(HERE / "PREREGISTERED_STATUS_CONTRACT.tsv")
    corrections = read_tsv(HERE / "POST_COMMIT_STATUS_CORRECTIONS.tsv")
    statuses = read_tsv(HERE / "CURRENT_STATUS_LEDGER.tsv")
    maps = read_tsv(HERE / "METRIC_TO_FRONTIER_MAP.tsv")
    guards = read_tsv(HERE / "REGRESSION_GUARD_LEDGER.tsv")
    contract_map = {row["id"]: row for row in contract}
    correction_map = {row["id"]: row for row in corrections}
    status_map = {row["id"]: row for row in statuses}
    if len(contract_map) != 24 or len(status_map) != 24:
        raise AssertionError("status identity coverage")
    if len(corrections) != 2 or len(correction_map) != 2:
        raise AssertionError("status correction coverage")
    for item in contract_map:
        if contract_map[item]["object"] != status_map[item]["object"]:
            raise AssertionError(f"status object mismatch {item}")
        historical = normalize(contract_map[item]["required_status"])
        expected = historical
        if item in correction_map:
            if normalize(correction_map[item]["historical_contract_status"]) != historical:
                raise AssertionError(f"historical correction mismatch {item}")
            expected = normalize(correction_map[item]["corrected_current_status"])
        if expected != normalize(status_map[item]["status"]):
            raise AssertionError(f"status grade mismatch {item}")
        if not ROOT.joinpath(status_map[item]["evidence_path"]).exists():
            raise AssertionError(f"missing status evidence {item}")
    if len(maps) != 13 or len({row["step"] for row in maps}) != 13:
        raise AssertionError("frontier map coverage")
    if len(guards) != 15 or len({row["id"] for row in guards}) != 15:
        raise AssertionError("regression guard coverage")
    for row in maps:
        if not ROOT.joinpath(row["evidence_path"]).exists():
            raise AssertionError(f"missing map evidence {row['step']}")
    for row in guards:
        if not ROOT.joinpath(row["evidence_path"]).exists():
            raise AssertionError(f"missing guard evidence {row['id']}")

    result = {
        "schema": "udt-scientific-consolidation-checkpoint-1.0",
        "python": sys.version.split()[0],
        "base": "e0c6958f9cae7766757ec6466a9659bba1a55f0d",
        "preregistration_commit": "b200b0a",
        "preregistration_correction_commit": "7995470",
        "source_count": len(lineage),
        "source_addition_count": len(source_additions),
        "status_count": len(statuses),
        "post_commit_status_correction_count": len(corrections),
        "frontier_map_count": len(maps),
        "regression_guard_count": len(guards),
        "source_paths_resolve": True,
        "status_contract_matches": True,
        "evidence_paths_resolve": True,
        "physics_derivation_performed": False,
        "artifact_move_performed": False,
        "gpu_work_performed": False,
        "maximum_conclusion": (
            "CURRENT_EVIDENCE_LINKED_NAVIGATION_AND_STATUS_CHECKPOINT_"
            "VERIFIED_WITHOUT_NEW_PHYSICS_OR_ARTIFACT_REORGANIZATION"
        ),
    }
    HERE.joinpath("CHECKPOINT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
