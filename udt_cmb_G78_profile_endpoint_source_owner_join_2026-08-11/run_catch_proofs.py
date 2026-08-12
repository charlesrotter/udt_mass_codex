#!/usr/bin/env python3
"""Exercise fail-closed semantic catches for the G78 result layer."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def validate(result: dict, routes: list[dict[str, str]]) -> None:
    assert result["family"]["profiles"] == 591
    assert result["family"]["sampled_degree_one"] == 591
    assert result["family"]["selector_rows_from_regular_topology"] == 0
    assert result["maximum_scope"] == "exact_twenty_source_ownership_audit_plus_frozen_591_profile_finite_mesh_census"
    assert result["scale_factorization"]["non_implication"] == "does_not_make_UDT_scale_free_or_select_R_endpoint_or_Xmax"
    assert result["owned_native_routes"] == 0
    by_route = {row["route"]: row for row in routes}
    assert len(by_route) == len(routes) == 7
    assert by_route["P_REGULARITY"]["status"] == "OPEN_NO_OWNER"
    assert by_route["P_GLOBAL_RELATION"]["status"] == "OPEN_NO_OWNER"
    assert by_route["E_SCALE"]["status"] == "OPEN_NO_OWNER"
    assert by_route["E_SNE"]["status"] == "COMPATIBILITY_ANCHOR_ONLY"
    assert by_route["E_XMAX"]["status"] == "NECESSARY_REQUIREMENT_ONLY"
    assert by_route["S_GEOMETRY"]["status"] == "OPEN_NO_OWNER"
    assert by_route["S_MULTICHANNEL"]["status"] == "CONDITIONAL_IDENTIFIABILITY_ONLY"


def caught(result: dict, routes: list[dict[str, str]], mutation) -> bool:
    trial_result = copy.deepcopy(result)
    trial_routes = copy.deepcopy(routes)
    mutation(trial_result, trial_routes)
    try:
        validate(trial_result, trial_routes)
    except AssertionError:
        return True
    return False


def set_route(routes: list[dict[str, str]], route: str, status: str) -> None:
    next(row for row in routes if row["route"] == route)["status"] = status


def main() -> None:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    routes = table(HERE / "OWNER_ROUTE_LEDGER.tsv")
    validate(result, routes)
    catches = {
        "missing_profile_rejected": caught(result, routes, lambda r, _: r["family"].__setitem__("profiles", 590)),
        "sampled_to_continuum_promotion_rejected": caught(result, routes, lambda r, _: r.__setitem__("maximum_scope", "continuum_global_theorem")),
        "regularity_profile_selection_rejected": caught(result, routes, lambda _, q: set_route(q, "P_REGULARITY", "OWNED_NATIVE")),
        "global_relation_profile_selection_rejected": caught(result, routes, lambda _, q: set_route(q, "P_GLOBAL_RELATION", "OWNED_NATIVE")),
        "scale_free_promotion_rejected": caught(result, routes, lambda r, _: r["scale_factorization"].__setitem__("non_implication", "UDT_IS_SCALE_FREE")),
        "SNe_profile_copy_rejected": caught(result, routes, lambda _, q: set_route(q, "E_SNE", "OWNED_NATIVE")),
        "Xmax_endpoint_identification_rejected": caught(result, routes, lambda _, q: set_route(q, "E_XMAX", "OWNED_NATIVE")),
        "unrestricted_source_promotion_rejected": caught(result, routes, lambda _, q: set_route(q, "S_GEOMETRY", "OWNED_NATIVE")),
        "conditional_identifiability_promotion_rejected": caught(result, routes, lambda _, q: set_route(q, "S_MULTICHANNEL", "OWNED_NATIVE")),
        "native_owner_count_promotion_rejected": caught(result, routes, lambda r, _: r.__setitem__("owned_native_routes", 1)),
    }
    assert all(catches.values())
    output = {
        "schema": "udt-cmb-g78-catch-proofs-v1",
        "status": "PASS",
        "catch_count": len(catches),
        "catches": catches,
    }
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
