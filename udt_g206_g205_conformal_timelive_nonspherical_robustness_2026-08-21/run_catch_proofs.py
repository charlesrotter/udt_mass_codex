#!/usr/bin/env python3
"""Hostile mutation catches for the G206 evidence contract."""

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
        and data.get("assertions") == 27
        and checks.get("causal_sign_scale") is True
        and checks.get("completed_Phi_shift") is True
        and checks.get("gaussian_affine_integral_finite") is True
        and "global_hyperbolicity_conformal_transfer" in analytic
        and "all_null_geodesic_integral_iff_criterion" in analytic
        and "global_hyperbolicity_conformal_transfer" not in mechanized
        and "all_null_geodesic_integral_iff_criterion" not in mechanized
        and "NO_PHYSICAL_OMEGA_HISTORY_OR_XMAX_SELECTION" in data.get("landing", "")
    )


def valid_independent(data: dict) -> bool:
    return (
        data.get("all_pass") is True
        and data.get("cases") == 10000
        and data.get("distinct_cases") == 10000
        and data.get("assertions") == 160006
        and data.get("production_imported") is False
        and data.get("production_artifact_read") is False
        and data.get("method")
        == "independent_direct_radial_coordinate_geodesic_plus_exact_rational_pair_affine_and_witness_algebraic_core"
        and "global_hyperbolicity_conformal_transfer" in data.get("not_independently_verified_here", [])
        and "physical_Omega_selection" in data.get("not_independently_verified_here", [])
    )


def main() -> None:
    production = json.loads((ROOT / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    diagnostics = json.loads((ROOT / "BOUNDARY_DIAGNOSTICS.json").read_text(encoding="utf-8"))
    assert valid_production(production)
    assert valid_independent(independent)
    assert diagnostics.get("all_pass") is True
    assert diagnostics.get("precision_digits", 0) >= 80
    assert "cancellation" in diagnostics.get("repair_note", "")

    mutations: list[tuple[str, dict, object]] = []
    for name, key, value in (
        ("production_pass_flip", "all_pass", False),
        ("production_assertion_drop", "assertions", 26),
        ("history_selection_smuggled", "landing", "CONFORMAL_COMPLETION_SELECTS_OMEGA"),
    ):
        altered = copy.deepcopy(production)
        altered[key] = value
        mutations.append((name, altered, valid_production))

    for name, key in (
        ("causal_cone_identity_removed", "causal_sign_scale"),
        ("completed_depth_shift_removed", "completed_Phi_shift"),
        ("finite_integral_removed", "gaussian_affine_integral_finite"),
    ):
        altered = copy.deepcopy(production)
        altered["checks"][key] = False
        mutations.append((name, altered, valid_production))

    altered = copy.deepcopy(production)
    altered["mechanized_scope"].append("global_hyperbolicity_conformal_transfer")
    mutations.append(("global_theorem_falsely_mechanized", altered, valid_production))
    altered = copy.deepcopy(production)
    altered["mechanized_scope"].append("all_null_geodesic_integral_iff_criterion")
    mutations.append(("integral_iff_falsely_mechanized", altered, valid_production))
    altered = copy.deepcopy(production)
    altered["analytic_theorems_recorded_not_mechanized"].remove("global_hyperbolicity_conformal_transfer")
    mutations.append(("global_analytic_scope_removed", altered, valid_production))
    altered = copy.deepcopy(production)
    altered["analytic_theorems_recorded_not_mechanized"].remove("all_null_geodesic_integral_iff_criterion")
    mutations.append(("integral_analytic_scope_removed", altered, valid_production))

    for name, key, value in (
        ("independent_case_drop", "cases", 9999),
        ("duplicate_cases", "distinct_cases", 9999),
        ("independent_assertion_drop", "assertions", 160005),
        ("production_import_smuggled", "production_imported", True),
        ("production_artifact_smuggled", "production_artifact_read", True),
        ("direct_geodesic_method_removed", "method", "exact_rational_controls_only"),
    ):
        altered = copy.deepcopy(independent)
        altered[key] = value
        mutations.append((name, altered, valid_independent))

    altered = copy.deepcopy(independent)
    altered["not_independently_verified_here"].remove("physical_Omega_selection")
    mutations.append(("selection_scope_overclaimed", altered, valid_independent))

    caught: list[str] = []
    for name, altered, validator in mutations:
        assert not validator(altered), name
        caught.append(name)

    bad_diagnostics = copy.deepcopy(diagnostics)
    bad_diagnostics["precision_digits"] = 79
    assert not (bad_diagnostics["all_pass"] and bad_diagnostics["precision_digits"] >= 80)
    caught.append("diagnostic_precision_drop")
    bad_diagnostics = copy.deepcopy(diagnostics)
    bad_diagnostics["repair_note"] = ""
    assert "cancellation" not in bad_diagnostics["repair_note"]
    caught.append("diagnostic_repair_disclosure_removed")

    result = {"all_pass": True, "caught": len(caught), "catches": caught}
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
