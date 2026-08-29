#!/usr/bin/env python3
"""Hostile semantic and evidence catches for G296."""

from __future__ import annotations

import copy
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "CATCH_PROOF_RESULT.json"
LANDING = (
    "COMPLETE_METRIC_IS_A_MINIMAL_FAITHFUL_PRIMITIVE_STATE"
    "__SECOND_METRIC_DERIVATIVE_ORDER_IS_THE_FIRST_LOCAL_NATURAL_NONIDENTITY_HOME"
    "__CURRENT_PREMISES_DO_NOT_PRIVILEGE_ONE_RESIDUAL_FORM"
)


def accepts(prod: dict, ind: dict) -> bool:
    c = prod.get("checks", {})
    g = ind.get("gates", {})
    return all([
        prod.get("landing") == LANDING,
        prod.get("all_pass") is True,
        ind.get("all_pass") is True,
        c.get("R_uxux_equals_a") is True,
        c.get("tracefree_einstein_zero") is True,
        c.get("tracefree_nonzero_screen_curvature") is True,
        c.get("scalar_lane_misses_tracefree_screen") is True,
        c.get("Lovelock_class_is_conditional") is True,
        c.get("W6_does_not_supply_order_or_rank") is True,
        c.get("no_formula_selected") is True,
        g.get("different_lawful_data_need_not_be_rejected") is True,
        g.get("first_order_Cartan_requires_classifying_law") is True,
        ind.get("imports_production") is False,
        ind.get("reads_production_output") is False,
    ])


def main() -> None:
    prod = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    ind = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    assert accepts(prod, ind)
    mutations = []

    def mutate(name, target, path, value):
        p = copy.deepcopy(prod)
        i = copy.deepcopy(ind)
        obj = p if target == "prod" else i
        cursor = obj
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        caught = not accepts(p, i)
        assert caught, name
        mutations.append({"name": name, "caught": caught})

    mutate("wrong landing", "prod", ["landing"], "FORMULA_DERIVED")
    mutate("production false pass", "prod", ["all_pass"], False)
    mutate("independent false pass", "ind", ["all_pass"], False)
    mutate("erase screen curvature", "prod", ["checks", "tracefree_nonzero_screen_curvature"], False)
    mutate("claim nonzero Einstein residual", "prod", ["checks", "tracefree_einstein_zero"], False)
    mutate("promote scalar to complete screen law", "prod", ["checks", "scalar_lane_misses_tracefree_screen"], False)
    mutate("promote Lovelock class to founded", "prod", ["checks", "Lovelock_class_is_conditional"], False)
    mutate("claim W6 fixes order and rank", "prod", ["checks", "W6_does_not_supply_order_or_rank"], False)
    mutate("select a formula", "prod", ["checks", "no_formula_selected"], False)
    mutate("demand rejection of all distinct data", "ind", ["gates", "different_lawful_data_need_not_be_rejected"], False)
    mutate("claim Cartan selects without classifying law", "ind", ["gates", "first_order_Cartan_requires_classifying_law"], False)
    mutate("independent imports production", "ind", ["imports_production"], True)
    mutate("independent reads production output", "ind", ["reads_production_output"], True)

    result = {"all_pass": True, "catch_count": len(mutations), "mutations": mutations}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
