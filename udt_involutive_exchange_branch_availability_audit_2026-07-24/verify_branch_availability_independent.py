#!/usr/bin/env python3
"""Independent stdlib reconstruction; does not import production code."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GATES = tuple(f"G{i:02d}" for i in range(1, 13))


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    matrix = table("FAMILY_GATE_MATRIX.tsv")
    ids = [row["family_id"] for row in matrix]
    assert ids == [f"B{i:02d}" for i in range(1, 29)]
    assert len(set(ids)) == 28
    passing = [row["family_id"] for row in matrix if {row[g] for g in GATES} == {"YES"}]
    assert passing == []
    assert sum(row["G02"] == "YES" for row in matrix) == 0
    assert sum(row["G03"] == "YES" for row in matrix) == 0

    def rank(row: dict[str, str]) -> tuple[int, int, int, int]:
        values = [row[g] for g in GATES]
        return (
            values.count("YES"),
            values.count("CONDITIONAL"),
            -values.count("NO"),
            -values.count("OPEN"),
        )

    best = max(matrix, key=rank)
    assert best["family_id"] == "B19"
    assert best["G02"] == "CONDITIONAL"
    assert best["G03"] == "CONDITIONAL"
    assert best["G05"] == "OPEN"

    source_specs = (
        ("SOURCE_MANIFEST.tsv", 97),
        ("SOURCE_MANIFEST_CORRECTION_01.tsv", 4),
        ("SOURCE_MANIFEST_CORRECTION_02.tsv", 35),
        ("SOURCE_MANIFEST_CORRECTION_03.tsv", 14),
    )
    source_paths: set[str] = set()
    for name, expected in source_specs:
        rows = table(name)
        assert len(rows) == expected
        for row in rows:
            assert row["path"] not in source_paths
            source_paths.add(row["path"])
            data = (ROOT / row["path"]).read_bytes()
            assert len(data) == int(row["bytes"])
            assert hashlib.sha256(data).hexdigest() == row["sha256"]
            blob = subprocess.run(
                ["git", "rev-parse", f"HEAD:{row['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            assert blob == row["git_blob"]
    assert len(source_paths) == 150

    lifts = table("LIFT_CLASSIFICATION.tsv")
    assert len(lifts) == 4
    assert sum(row["involutive_exchange"] == "YES" for row in lifts) == 2
    assert sum(row["order"] == "4" for row in lifts) == 2
    assert all(
        row["fixed_lattice_rank"] == "0"
        for row in lifts
        if row["order"] == "4"
    )
    assert all(row["selected_by_current_udt"] == "NO" for row in lifts)

    witnesses = table("WITNESS_TYPE_LEDGER.tsv")
    assert len(witnesses) == 7
    assert not any(row["type"] == "NATIVE_ON_SHELL_COMPLETE" for row in witnesses)
    w01 = next(row for row in witnesses if row["witness_id"] == "W01")
    assert w01["type"] == "CONDITIONAL_ON_SHELL_BACH"
    assert w01["exchange_lift"] == "METRIC_BLIND_MULTIPLE_LIFTS"

    catches = table("CATCH_PROOF_RESULTS.tsv")
    assert len(catches) == 12
    assert all(row["result"].startswith("PASS:") for row in catches)

    production = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert production["passing_families"] == passing
    assert production["strongest_near_pass"]["family_id"] == best["family_id"]
    assert production["sources"] == len(source_paths)
    assert production["maximum_ruling"] == "PRESENT_SELECTOR_BOUNDARY_VERIFIED_WITH_CAVEATS"
    assert not any(production["authority_boundary"].values())

    result = {
        "schema": "udt-involutive-exchange-branch-independent-v1",
        "result": "PASS",
        "imports_production_module": False,
        "imports_sympy": False,
        "families": len(matrix),
        "sources": len(source_paths),
        "passing_families": passing,
        "strongest_near_pass": best["family_id"],
        "native_action_gate_yes": 0,
        "native_complete_on_shell_gate_yes": 0,
        "involutive_lifts": 2,
        "selected_lifts": 0,
        "catch_proofs": len(catches),
        "agreement": {
            "no_complete_witness": True,
            "strongest_near_pass": True,
            "source_universe": True,
            "lift_classification": True,
            "authority_boundary": True,
        },
    }
    (HERE / "INDEPENDENT_RESULTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
