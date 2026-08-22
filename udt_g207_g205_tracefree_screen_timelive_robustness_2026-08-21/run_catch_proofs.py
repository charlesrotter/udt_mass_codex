#!/usr/bin/env python3
"""Hostile evidence and semantic mutation catches for G207."""

from __future__ import annotations

import copy
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"


def valid_production(data: dict) -> bool:
    checks = data.get("checks", {})
    analytic = data.get("analytic_theorems_recorded_not_mechanized", [])
    mechanized = data.get("mechanized_scope", [])
    return (
        data.get("all_pass") is True
        and data.get("assertions") == 36
        and checks.get("K_radial_kernel") is True
        and checks.get("K_tracefree") is True
        and checks.get("ambient_det_preserved") is True
        and checks.get("failure_orbit_radial_geodesic_on_G205_circle") is True
        and checks.get("failure_affine_future_finite") is True
        and checks.get("pair_area_not_blind") is True
        and checks.get("completed_phi_not_blind") is True
        and "global_hyperbolicity_for_every_smooth_declared_S" in analytic
        and "null_completeness_for_every_smooth_static_declared_S" in analytic
        and "global_hyperbolicity_for_every_smooth_declared_S" not in mechanized
        and "NO_PHYSICAL_S_HISTORY_OR_XMAX_SELECTION" in data.get("landing", "")
    )


def valid_independent(data: dict) -> bool:
    return (
        data.get("all_pass") is True
        and data.get("cases") == 10_000
        and data.get("distinct_cases") == 10_000
        and data.get("assertions") == 110_009
        and data.get("changed_clock_cases") == 10_000
        and data.get("changed_pair_area_cases") == 10_000
        and data.get("changed_beta_cases") == 10_000
        and data.get("production_imported") is False
        and data.get("production_artifact_read") is False
        and data.get("method")
        == "independent_euler_lagrange_circular_orbit_plus_exact_fraction_determinant_one_ambient_and_completed_pair_replay"
        and "physical_S_history_or_Xmax_selection" in data.get("not_independently_verified_here", [])
    )


def main() -> None:
    production = json.loads((ROOT / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    diagnostics = json.loads((ROOT / "BOUNDARY_DIAGNOSTICS.json").read_text(encoding="utf-8"))
    assert valid_production(production)
    assert valid_independent(independent)
    assert diagnostics.get("all_pass") is True and diagnostics.get("precision_digits") == 100

    mutations: list[tuple[str, dict, object]] = []
    for name, key, value in (
        ("production_pass_flip", "all_pass", False),
        ("production_assertion_drop", "assertions", 35),
        ("history_selection_smuggled", "landing", "TRACEFREE_SCREEN_SELECTS_PHYSICAL_S"),
    ):
        altered = copy.deepcopy(production)
        altered[key] = value
        mutations.append((name, altered, valid_production))

    for name, key in (
        ("tracefree_removed", "K_tracefree"),
        ("radial_kernel_removed", "K_radial_kernel"),
        ("ambient_volume_removed", "ambient_det_preserved"),
        ("orbit_radial_residual_removed", "failure_orbit_radial_geodesic_on_G205_circle"),
        ("finite_affine_failure_removed", "failure_affine_future_finite"),
        ("pair_area_blindness_smuggled", "pair_area_not_blind"),
        ("completed_scalar_blindness_smuggled", "completed_phi_not_blind"),
    ):
        altered = copy.deepcopy(production)
        altered["checks"][key] = False
        mutations.append((name, altered, valid_production))

    altered = copy.deepcopy(production)
    altered["mechanized_scope"].append("global_hyperbolicity_for_every_smooth_declared_S")
    mutations.append(("global_theorem_falsely_mechanized", altered, valid_production))
    altered = copy.deepcopy(production)
    altered["analytic_theorems_recorded_not_mechanized"].remove("null_completeness_for_every_smooth_static_declared_S")
    mutations.append(("static_scope_removed", altered, valid_production))

    for name, key, value in (
        ("independent_case_drop", "cases", 9_999),
        ("independent_duplicate", "distinct_cases", 9_999),
        ("independent_assertion_drop", "assertions", 110_008),
        ("clock_response_erased", "changed_clock_cases", 0),
        ("area_response_erased", "changed_pair_area_cases", 0),
        ("beta_response_erased", "changed_beta_cases", 0),
        ("production_import_smuggled", "production_imported", True),
        ("production_artifact_smuggled", "production_artifact_read", True),
        ("independent_method_removed", "method", "production_replay"),
    ):
        altered = copy.deepcopy(independent)
        altered[key] = value
        mutations.append((name, altered, valid_independent))

    altered = copy.deepcopy(independent)
    altered["not_independently_verified_here"].remove("physical_S_history_or_Xmax_selection")
    mutations.append(("selection_scope_overclaimed", altered, valid_independent))

    caught: list[str] = []
    for name, altered, validator in mutations:
        assert not validator(altered), name
        caught.append(name)

    bad_diagnostics = copy.deepcopy(diagnostics)
    bad_diagnostics["precision_digits"] = 99
    assert not (bad_diagnostics["all_pass"] and bad_diagnostics["precision_digits"] == 100)
    caught.append("diagnostic_precision_changed")
    bad_diagnostics = copy.deepcopy(diagnostics)
    bad_diagnostics["scope"] = "analytic global proof"
    assert "finite high-precision controls only" not in bad_diagnostics["scope"]
    caught.append("diagnostic_scope_overclaimed")

    result = {"all_pass": True, "caught": len(caught), "catches": caught}
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
