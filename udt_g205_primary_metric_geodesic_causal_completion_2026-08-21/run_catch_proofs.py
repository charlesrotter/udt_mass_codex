#!/usr/bin/env python3
"""Hostile mutation catches for the G205 evidence contract."""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"


def valid_production(data: dict) -> bool:
    return (
        data.get("all_pass") is True
        and data.get("assertions") == 112
        and set(data.get("geodesic_types", [])) == {"timelike", "null", "spacelike"}
        and set(data.get("outer_cases", [])) == {"E_nonzero", "causal_E_zero_impossible", "spacelike_E_zero"}
        and "global_hyperbolicity" not in data.get("mechanized_scope", [])
        and "optical_spatial_metric_completeness" not in data.get("mechanized_scope", [])
        and "global_hyperbolicity" in data.get("analytic_theorems_recorded_not_mechanized", [])
        and "optical_spatial_metric_completeness" in data.get("analytic_theorems_recorded_not_mechanized", [])
        and data.get("finite_radius_killing_horizon") is False
        and "NO_PARAMETER_XMAX_OR_PHYSICAL_HISTORY_SELECTION" in data.get("landing", "")
        and data.get("null_orbit_stability", {}).get("supercritical_inner_root") == "stable_minimum_of_f_over_r2"
        and data.get("null_orbit_stability", {}).get("supercritical_outer_root") == "unstable_maximum_of_f_over_r2"
    )


def valid_independent(data: dict) -> bool:
    return (
        data.get("all_pass") is True
        and data.get("cases") == 10000
        and data.get("distinct_cases") == 10000
        and data.get("assertions") == 150000
        and data.get("production_imported") is False
        and data.get("production_artifact_read") is False
        and data.get("method") == "independent_exact_rational_algebraic_core_only"
        and "Cauchy_slice_global_hyperbolicity" in data.get("not_independently_verified_here", [])
    )


def main() -> None:
    production = json.loads((ROOT / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    diagnostics = json.loads((ROOT / "BOUNDARY_DIAGNOSTICS.json").read_text(encoding="utf-8"))
    assert valid_production(production)
    assert valid_independent(independent)
    assert diagnostics["precision_digits"] == 80 and diagnostics["all_pass"] is True

    mutations: list[tuple[str, dict, callable]] = []
    for name, key, value in (
        ("all_pass", "all_pass", False),
        ("assertion_count", "assertions", 111),
        ("missing_spacelike", "geodesic_types", ["timelike", "null"]),
        ("missing_E0_case", "outer_cases", ["E_nonzero", "causal_E_zero_impossible"]),
        ("finite_horizon_invented", "finite_radius_killing_horizon", True),
        ("selection_guard_removed", "landing", "FULL_GEODESIC_COMPLETENESS"),
    ):
        altered = copy.deepcopy(production)
        altered[key] = value
        mutations.append((name, altered, valid_production))

    altered = copy.deepcopy(production)
    altered["null_orbit_stability"]["supercritical_inner_root"] = "unstable"
    mutations.append(("inner_orbit_stability_flip", altered, valid_production))
    altered = copy.deepcopy(production)
    altered["null_orbit_stability"]["supercritical_outer_root"] = "stable"
    mutations.append(("outer_orbit_stability_flip", altered, valid_production))

    altered = copy.deepcopy(production)
    altered["mechanized_scope"].append("optical_spatial_metric_completeness")
    mutations.append(("optical_proof_falsely_mechanized", altered, valid_production))
    altered = copy.deepcopy(production)
    altered["mechanized_scope"].append("global_hyperbolicity")
    mutations.append(("global_proof_falsely_mechanized", altered, valid_production))
    altered = copy.deepcopy(production)
    altered["analytic_theorems_recorded_not_mechanized"].remove("optical_spatial_metric_completeness")
    mutations.append(("optical_analytic_scope_removed", altered, valid_production))
    altered = copy.deepcopy(production)
    altered["analytic_theorems_recorded_not_mechanized"].remove("global_hyperbolicity")
    mutations.append(("global_analytic_scope_removed", altered, valid_production))

    for name, key, value in (
        ("independent_case_count", "cases", 9999),
        ("duplicate_independent_cases", "distinct_cases", 9999),
        ("production_import_smuggled", "production_imported", True),
        ("independence_scope_overclaimed", "method", "independent_full_global_proof"),
    ):
        altered = copy.deepcopy(independent)
        altered[key] = value
        mutations.append((name, altered, valid_independent))

    caught = []
    for name, altered, validator in mutations:
        assert not validator(altered), name
        caught.append(name)

    bad_diagnostics = copy.deepcopy(diagnostics)
    bad_diagnostics["precision_digits"] = 79
    assert not (bad_diagnostics["precision_digits"] == 80 and bad_diagnostics["all_pass"] is True)
    caught.append("diagnostic_precision_drop")

    result = {"all_pass": True, "caught": len(caught), "catches": caught}
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
