#!/usr/bin/env python3
"""Hostile mutation checks for the bounded G342 evidence contract."""

from __future__ import annotations

import json
import os


LANDING = (
    "FULL_METRIC_JACOBI_MAP_CLOSES__BOTH_SCREEN_RATES_AND_MEAN_EXPANSION_POSITIVE"
    "__SHEAR_ZERO_ONLY_ON_LONGITUDINAL_SYMMETRY_LOCUS_OR_VERTEX"
    "__EACH_COMPACT_LIFT_RETAINS_POSITIVE_AREA_WITH_PATH_LABEL"
    "__NO_LUMINOSITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)


def validate(state: dict[str, object]) -> tuple[bool, str]:
    requirements = (
        (abs(float(state["tangent_screen_term"])) < 1e-13, "fixed_affine_tangent_error"),
        (abs(float(state["azimuth_normalization_ratio"]) - 1.0) < 1e-13,
         "lost_azimuth_normalization"),
        (float(state["dparallel"]) > float(state["daz"]) > 0.0, "screen_swap_or_erasure"),
        (float(state["tidal_parallel"]) < 0.0 < float(state["tidal_azimuth"]),
         "curvature_sign_flip"),
        (abs(float(state["tidal_cross"])) < 1e-13, "offdiagonal_injection"),
        (abs(float(state["alpha_ratio"]) - 1.0) < 1e-13, "affine_normalization_error"),
        (float(state["oriented_determinant"]) > 0.0, "determinant_absolute_mask"),
        (float(state["longitudinal_axis_response"]) > 0.0,
         "principal_axis_chart_loss"),
        (state["retained_path_labels"] == state["expected_path_labels"],
         "quotient_path_deletion"),
        (state["physical_promotion"] is False, "physical_readout_promotion"),
    )
    for condition, failure in requirements:
        if not condition:
            return False, failure
    return True, "ok"


def main() -> None:
    baseline = {
        "tangent_screen_term": 0.0,
        "azimuth_normalization_ratio": 1.0,
        "dparallel": 1.4,
        "daz": 1.1,
        "tidal_parallel": -0.2,
        "tidal_azimuth": 0.2,
        "tidal_cross": 0.0,
        "alpha_ratio": 1.0,
        "oriented_determinant": 1.54,
        "longitudinal_axis_response": 0.8,
        "retained_path_labels": (0, 1, -1, 2),
        "expected_path_labels": (0, 1, -1, 2),
        "physical_promotion": False,
    }
    ok, message = validate(baseline)
    if not ok:
        raise AssertionError(f"baseline failed: {message}")

    mutations = (
        ("fixed_affine_tangent_error", "tangent_screen_term", 0.1),
        ("lost_azimuth_normalization", "azimuth_normalization_ratio", 0.6),
        ("screen_swap_or_erasure", "dparallel", 1.0),
        ("curvature_sign_flip", "tidal_parallel", 0.2),
        ("offdiagonal_injection", "tidal_cross", 0.07),
        ("affine_normalization_error", "alpha_ratio", 0.8),
        ("determinant_absolute_mask", "oriented_determinant", -1.54),
        ("principal_axis_chart_loss", "longitudinal_axis_response", 0.0),
        ("quotient_path_deletion", "retained_path_labels", (0, 1, -1)),
        ("physical_readout_promotion", "physical_promotion", True),
    )
    checks: dict[str, bool] = {}
    messages: dict[str, str] = {}
    for expected, key, value in mutations:
        mutant = dict(baseline)
        mutant[key] = value
        passed, failure = validate(mutant)
        checks[expected] = not passed and failure == expected
        messages[expected] = failure

    result = {
        "all_passed": all(checks.values()),
        "catches_passed": sum(checks.values()),
        "catches_total": len(checks),
        "checks": checks,
        "landing": LANDING,
        "messages": messages,
        "validator_shared_by_baseline_and_mutants": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
