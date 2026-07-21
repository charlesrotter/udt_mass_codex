#!/usr/bin/env python3
"""Fail-closed classification of the transverse-coframe closure audit."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main():
    gauge = load("GAUGE_STRUCTURE.json")
    background = load("BACKGROUND_CLOSURE.json")
    verification = load("VERIFICATION_RESULT.json")
    timeout = (HERE / "GENERAL_TWIST_TIMEOUT.md").read_text(encoding="utf-8")

    product = background["product_control"]
    obstruction = background["variation_domain_obstruction"]
    checks = {
        "gauge_structure_exact": all(gauge["checks"].values()),
        "background_derivation_exact": all(background["checks"].values()),
        "product_density_recovered": product["density_difference"] == "0",
        "product_y_and_area_full_bach_zero": product["on_full_bach"]["y"] == "0" and product["on_full_bach"]["area"] == "0",
        "restricted_shear_obstruction_recorded": product["on_full_bach"]["shear"] == "8*K*(-2*K + Derivative(y(r), (r, 2)))/3",
        "einstein_counterexample_exact": obstruction["einstein_branch_full_constraint"] == "0" and obstruction["einstein_branch_projection"] == "-32*K**2/3",
        "conformal_control_exact": obstruction["conformal_branch_projection"] == "0",
        "angular_integration_not_silently_selected": "no general division by F is valid" in background["angular_reduction_rule"],
        "independent_verification": verification["result"] == "PASS" and all(verification["checks"].values()),
        "mixed_hessian_zero": verification["maxima"]["mixed_block_absolute"] <= 1e-9,
        "pure_twist_control_nonzero": verification["controls"]["minimum_pure_twist_magnitude"] > 1e-6,
        "general_twist_timeout_disclosed": "no `TWIST_CLOSURE.json` exists" in timeout and not (HERE / "TWIST_CLOSURE.json").exists(),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    result = {
        "schema": "udt-c2-transverse-coframe-closure-analysis-1.0",
        "result": "PASS_WITH_INCONCLUSIVE_PURE_TWIST_BLOCK",
        "outcomes": [
            "PRODUCT_BACH_FAMILY_REMAINS_FULL_METRIC_STATIONARY",
            "TWIST_HESSIAN_BLOCK_DIAGONAL_BY_REFLECTION",
            "COFRAME_CONTROL_INCONCLUSIVE",
        ],
        "selector_ruling": {
            "local_full_metric_selector_added": False,
            "restricted_radial_shear_selector_valid": False,
            "reason": "the nonzero r-only shear projection freezes angular shape/domain data and rejects an exact Bach-flat Einstein product; pointwise full Bach remains authoritative",
        },
        "angular_completion_ruling": {
            "status": "OPEN_LOAD_BEARING",
            "reason": "general area/shear action densities carry inequivalent F and F_prime_squared/F weights, so the radial equations require an unselected angular domain and cap/period completion",
        },
        "connection_ruling": {
            "local_gauge_curvature": "H=dA",
            "constant_connection": "LOCAL_ZERO_MODE",
            "mixed_even_odd_hessian": "ZERO",
            "pure_general_area_shear_twist_operator": "INCONCLUSIVE_TIMEOUT",
        },
        "maximum_conclusion": "CONDITIONAL_LOCAL_C2_TRANSVERSE_COFRAME_CLOSURE_PARTIALLY_CHARACTERIZED",
        "checks": checks,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
    }
    (HERE / "CLOSURE_ANALYSIS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": result["result"], "outcomes": result["outcomes"], "checks": len(checks)}, sort_keys=True))


if __name__ == "__main__":
    main()
