#!/usr/bin/env python3
"""Hostile in-memory mutation catches for G256."""

from __future__ import annotations

import argparse
import copy
import csv
from fractions import Fraction
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent


def validate_graph_record(record: dict[str, object]) -> None:
    n = int(record["N"])
    edges = int(record["edge_count"])
    rank = int(record["incidence_rank"])
    assert record["kind"] == "complete"
    assert edges == n * (n - 1) // 2
    assert rank == n - 1
    assert int(record["anchored_state_dimension"]) == n - 1
    assert int(record["cycle_rank"]) == edges - n + 1
    assert int(record["cycle_annihilation_rank"]) == edges - n + 1


def validate_angular_record(record: dict[str, object]) -> None:
    assert record["nonzero_for_finite_real_phi"] is True
    assert int(record["owned_residual_count"]) == 0
    assert record["classification"] == "LOCAL_TOMOGRAPHIC_BIJECTION_NOT_VALUE_PROPAGATION"


def validate_hermite_record(record: dict[str, object]) -> None:
    n = int(record["N"])
    assert int(record["condition_count"]) == 3 * n
    assert int(record["matrix_rank"]) == 3 * n
    assert record["all_jets_exact"] is True
    assert record["null_deformation_preserves_all_registered_jets"] is True
    assert Fraction(str(record["third_germ_change_at_first_node"])) != 0


def validate_solver_gate(record: dict[str, object]) -> None:
    assert int(record["owned_residual_count"]) == 0
    assert record["ode_status"] == "GATED_NOT_DEFINED"
    assert record["pde_status"] == "GATED_NOT_DEFINED"
    assert record["gpu_status"] == "GATED_NOT_DEFINED"


def must_fail(label, callback):
    try:
        callback()
    except (AssertionError, KeyError, ValueError):
        return {"mutation": label, "caught": True}
    raise AssertionError(f"mutation escaped: {label}")


def owner_rows() -> list[dict[str, str]]:
    with (PACKAGE / "OWNER_CENSUS.tsv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_owners(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 18
    assert {row["owned_nonidentity_value_law"] for row in rows} == {"no"}


def run() -> dict[str, object]:
    complete = {
        "kind": "complete",
        "N": 7,
        "edge_count": 21,
        "incidence_rank": 6,
        "cycle_rank": 15,
        "cycle_annihilation_rank": 15,
        "anchored_state_dimension": 6,
    }
    validate_graph_record(complete)
    catches = []

    deleted_edge = dict(complete)
    deleted_edge["edge_count"] = int(deleted_edge["edge_count"]) - 1
    catches.append(must_fail("deleted_complete_graph_edge", lambda: validate_graph_record(deleted_edge)))

    corrupted_cycle = dict(complete)
    corrupted_cycle["cycle_annihilation_rank"] = int(corrupted_cycle["cycle_annihilation_rank"]) - 1
    catches.append(must_fail("corrupted_cycle_rank", lambda: validate_graph_record(corrupted_cycle)))

    collapsed_nullity = dict(complete)
    collapsed_nullity["anchored_state_dimension"] = 2
    catches.append(must_fail("collapsed_N_dependent_nullity", lambda: validate_graph_record(collapsed_nullity)))

    bad_hermite = {
        "N": 5,
        "condition_count": 15,
        "matrix_rank": 14,
        "all_jets_exact": False,
        "null_deformation_preserves_all_registered_jets": True,
        "third_germ_change_at_first_node": "6",
    }
    catches.append(must_fail("failed_Hermite_jet", lambda: validate_hermite_record(bad_hermite)))

    bad_angular = {
        "nonzero_for_finite_real_phi": True,
        "owned_residual_count": 1,
        "classification": "PROFILE_RESIDUAL",
    }
    catches.append(must_fail("angular_output_promoted_to_residual", lambda: validate_angular_record(bad_angular)))

    owners = owner_rows()
    smuggled_owner = copy.deepcopy(owners)
    smuggled_owner[0]["owned_nonidentity_value_law"] = "yes"
    catches.append(must_fail("unowned_finite_family_condition", lambda: validate_owners(smuggled_owner)))

    bad_solver = {
        "owned_residual_count": 0,
        "ode_status": "STARTED",
        "pde_status": "GATED_NOT_DEFINED",
        "gpu_status": "GATED_NOT_DEFINED",
    }
    catches.append(must_fail("solver_started_without_residual", lambda: validate_solver_gate(bad_solver)))

    assert all(item["caught"] for item in catches)
    return {"status": "PASS", "catch_count": len(catches), "catches": catches}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
