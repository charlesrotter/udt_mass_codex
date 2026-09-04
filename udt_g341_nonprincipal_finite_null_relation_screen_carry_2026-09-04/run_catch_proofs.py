#!/usr/bin/env python3
"""Hostile mutation controls for the bounded G341 evidence contract."""

from __future__ import annotations

import json
import os
from pathlib import Path


LANDING = (
    "EACH_NONZERO_UNIVERSAL_COVER_LIFT_HAS_ONE_REGULAR_FUTURE_NULL_SOLUTION"
    "__NO_INTERIOR_CONJUGATE_CAUSTIC_ON_THE_SUPPLIED_TAUB_KASNER_NULL_CONE"
    "__MIXED_RAYS_HAVE_NONZERO_G269_NULL_ROTATION_WITH_TRIVIAL_SCREEN_QUOTIENT_ROTATION"
    "__COMPACT_MULTIPLICITY_IS_PATH_LABELLED_NOT_PER_LIFT_NONUNIQUENESS"
    "__NO_LIGHT_MODEL_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)


def validate(state: dict[str, object]) -> tuple[bool, str]:
    requirements = (
        (state["qx_lam"] < 0.0, "folded_endpoint_derivative"),
        (state["qp_lam"] > 0.0, "folded_transverse_derivative"),
        (state["jacobian"] > 0.0, "endpoint_rank_loss"),
        (state["winding_count"] == state["expected_windings"], "deleted_winding"),
        (state["axis_cartesian_rank"] > 0.0, "polar_axis_false_caustic"),
        (abs(state["mixed_w"]) > 0.0, "mixed_screen_erasure"),
        (state["null_gauge_residual"] == 0.0, "null_gauge_omitted"),
        (state["quotient_crossing_is_conjugate"] is False, "branch_crossing_conflation"),
        (state["zero_shift_relation_norm"] > 0.0, "zero_shift_relation_erasure"),
        (abs(state["pair_plane_separator"]) > 0.0, "pair_plane_conflation"),
        (state["physical_distance"] > 0.0, "signed_depth_distance_conflation"),
        (state["screen_quotient_rotation"] == 0.0, "invented_screen_rotation"),
        (state["frequency_ratio"] > 0.0, "frequency_orientation_reversal"),
        (state["physical_route_selected"] is False, "physical_route_selection"),
        (state["light_model_imported"] is False, "light_model_import"),
        (state["scale_or_xmax_selected"] is False, "scale_xmax_promotion"),
    )
    for condition, failure in requirements:
        if not condition:
            return False, failure
    return True, "ok"


def main() -> None:
    baseline = {
        "qx_lam": -0.4,
        "qp_lam": 0.7,
        "jacobian": 0.9,
        "winding_count": 9,
        "expected_windings": 9,
        "axis_cartesian_rank": 0.8,
        "mixed_w": 0.3,
        "null_gauge_residual": 0.0,
        "quotient_crossing_is_conjugate": False,
        "zero_shift_relation_norm": 1.2,
        "pair_plane_separator": -0.17,
        "physical_distance": 1.1,
        "screen_quotient_rotation": 0.0,
        "frequency_ratio": 0.8,
        "physical_route_selected": False,
        "light_model_imported": False,
        "scale_or_xmax_selected": False,
    }
    ok, message = validate(baseline)
    if not ok:
        raise AssertionError(f"baseline failed: {message}")

    mutations = (
        ("folded_endpoint_derivative", "qx_lam", 0.4),
        ("folded_transverse_derivative", "qp_lam", -0.7),
        ("endpoint_rank_loss", "jacobian", 0.0),
        ("deleted_winding", "winding_count", 8),
        ("polar_axis_false_caustic", "axis_cartesian_rank", 0.0),
        ("mixed_screen_erasure", "mixed_w", 0.0),
        ("null_gauge_omitted", "null_gauge_residual", 0.2),
        ("branch_crossing_conflation", "quotient_crossing_is_conjugate", True),
        ("zero_shift_relation_erasure", "zero_shift_relation_norm", 0.0),
        ("pair_plane_conflation", "pair_plane_separator", 0.0),
        ("signed_depth_distance_conflation", "physical_distance", -1.1),
        ("invented_screen_rotation", "screen_quotient_rotation", 0.25),
        ("frequency_orientation_reversal", "frequency_ratio", -0.8),
        ("physical_route_selection", "physical_route_selected", True),
        ("light_model_import", "light_model_imported", True),
        ("scale_xmax_promotion", "scale_or_xmax_selected", True),
    )
    checks: dict[str, bool] = {}
    messages: dict[str, str] = {}
    for expected, key, value in mutations:
        mutant = dict(baseline)
        mutant[key] = value
        passed, failure = validate(mutant)
        checks[expected] = (not passed and failure == expected)
        messages[expected] = failure

    result = {
        "all_passed": all(checks.values()),
        "catches_passed": sum(checks.values()),
        "catches_total": len(checks),
        "checks": checks,
        "messages": messages,
        "landing": LANDING,
        "validator_shared_by_baseline_and_mutants": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_NO_WRITE") != "1":
        Path(__file__).with_name("CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
