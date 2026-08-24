#!/usr/bin/env python3
"""Hostile semantic mutation catches for G240."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Callable

from derive_null_image_cluster_census import build_result, validate_result


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "CATCH_PROOF_RESULT.json"


def set_nested(result: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = result
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = value


def mutation_case(name: str, mutator: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    result = copy.deepcopy(build_result())
    mutator(result)
    caught = False
    try:
        validate_result(result)
    except (AssertionError, KeyError, TypeError):
        caught = True
    return {"mutation": name, "caught": caught}


def build_result_set() -> dict[str, Any]:
    cases = [
        mutation_case("silent_single_branch_selection", lambda d: set_nested(d, ("query",), "SELECT_ONE_BRANCH")),
        mutation_case("arbitrary_branch_weight_insertion", lambda d: set_nested(d, ("uses_arbitrary_branch_weights",), True)),
        mutation_case("unit_multiplicity_provenance_erasure", lambda d: set_nested(d, ("unit_multiplicity_source",), "FREE_WEIGHT")),
        mutation_case("sibling_term_omission", lambda d: set_nested(d, ("g239_two_cell_control", "Gamma", 0, 1, "exact"), "0/1")),
        mutation_case("image_self_pair_insertion", lambda d: set_nested(d, ("witness", "ordered_distinct_images"), False)),
        mutation_case("wrong_N_squared_normalization", lambda d: set_nested(d, ("formula", "normalized_gamma"), "Gamma=Sigma_sib/N^2")),
        mutation_case("poisson_promoted_to_native_law", lambda d: set_nested(d, ("parent_status",), "DERIVED_UDT_SOURCE_LAW")),
        mutation_case("caustic_scope_promotion", lambda d: set_nested(d, ("general_theorem_scope",), "ALL_CAUSTIC_AND_INFINITE_IMAGE_RELATIONS")),
        mutation_case("physical_history_selection_claim", lambda d: set_nested(d, ("physical_history_selected",), True)),
        mutation_case("observational_anchor_insertion", lambda d: set_nested(d, ("observational_anchor_used",), True)),
        mutation_case("boss_outcome_opening", lambda d: set_nested(d, ("boss_outcomes_opened",), True)),
        mutation_case("forbidden_P1_guard_removal", lambda d: d["forbidden_inputs_absent"].remove("P1")),
        mutation_case("forbidden_Xmax_guard_removal", lambda d: d["forbidden_inputs_absent"].remove("X_max")),
        mutation_case("fitted_coefficient_guard_removal", lambda d: d["forbidden_inputs_absent"].remove("fitted coefficient")),
        mutation_case("protected_payload_guard_removal", lambda d: d["forbidden_inputs_absent"].remove("protected package")),
    ]
    if not all(case["caught"] for case in cases):
        raise AssertionError("hostile mutation escaped")
    return {"audit": "G240_CATCH_PROOFS", "status": "PASS", "cases": cases}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = build_result_set()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        print(payload, end="")
    else:
        OUTPUT.write_text(payload, encoding="utf-8")
        print(payload, end="")


if __name__ == "__main__":
    main()
