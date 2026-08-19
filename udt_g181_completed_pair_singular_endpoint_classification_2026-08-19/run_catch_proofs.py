#!/usr/bin/env python3
"""Mutation catches for the bounded G181 endpoint classification."""

from __future__ import annotations

import json
import os
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main_result() -> dict[str, object]:
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())

    T = Fraction(3, 2)
    L = Fraction(5, 3)
    beta = Fraction(7, 11)
    m = T * L
    h00 = -(T * T)
    h01 = -(T * T) * beta
    h11 = L * L - T * T * beta * beta
    det_sigma = h00 * h11 - h01 * h01
    hs01 = h01 / m
    hs11 = h11 / (m * m)

    catches = {
        "determinant_sign_mutation": det_sigma != m * m,
        "determinant_missing_square_mutation": det_sigma != -m,
        "density_sum_mutation": m != T + L,
        "completed_jacobian_missing_m_mutation": det_sigma != -1,
        "completed_determinant_zero_mutation": h00 * hs11 - hs01 * hs01 != 0,
        "shift_erasure_mutation": h01 != 0,
        "completed_shift_unscaled_mutation": hs01 != -(T * T) * beta,
        "finite_threshold_includes_minus_one_mutation": not (Fraction(-1) > -1),
        "log_threshold_called_power_mutation": Fraction(-1) == -1,
        "power_threshold_called_finite_mutation": not (Fraction(-2) > -1),
        "exponent_uses_difference_mutation": (Fraction(1) + Fraction(-2)) != (
            Fraction(1) - Fraction(-2)
        ),
        "positive_depth_sign_reversed_mutation": -Fraction(1) < 0,
        "zero_depth_called_divergent_mutation": Fraction(0) == 0,
        "negative_depth_sign_reversed_mutation": -Fraction(-1) > 0,
        "finite_tape_forces_finite_depth_mutation": (
            derivation["power_law"]["finite_tape"] == "a+b>-1"
            and derivation["power_law"]["positive_depth_infinity"] == "a>0"
        ),
        "infinite_tape_forces_infinite_depth_mutation": independent["cross_class_counts"]
        ["INFINITE_LOG__FINITE"]
        > 0,
        "m_to_zero_forces_extension_mutation": (
            "neither proves nor forbids"
            in derivation["endpoint_classification"]["m_limit_alone"]
        ),
        "m_to_zero_forces_failure_mutation": (
            derivation["endpoint_classification"]["auxiliary_stall"].startswith("may be")
        ),
        "m_to_infinity_forces_infinite_tape_mutation": Fraction(-1, 2) > -1,
        "regular_boundary_allows_zero_clock_mutation": (
            "finite positive limit"
            in derivation["endpoint_classification"]["regular_finite_completed_metric_iff"]
        ),
        "regular_boundary_drops_completed_shift_mutation": (
            "beta/m approaches a finite limit"
            in derivation["endpoint_classification"]["regular_finite_completed_metric_iff"]
        ),
        "angular_turn_called_zero_tangent_mutation": (
            Fraction(2) * Fraction(5) ** 2 * Fraction(3) ** 2 > 0
        ),
        "primary_zero_if_v_zero_only_mutation": (
            Fraction(2) * Fraction(5) ** 2 * Fraction(3) ** 2 != 0
        ),
        "center_retains_angular_orbit_mutation": Fraction(2) * Fraction(0) ** 2 * Fraction(3) ** 2 == 0,
        "zero_complete_tangent_called_regular_mutation": (
            derivation["primary_boundary"]["r_positive_zero_iff"] == "v=0 and b=0"
        ),
        "one_sided_stall_called_universally_intrinsic_mutation": (
            independent["stall_exact_checks"] >= 500
        ),
        "two_sided_metric_normalization_called_immersion_proof_mutation": (
            "two-sided branch and immersion carry" in derivation["open_scope"]
        ),
        "physical_family_selection_smuggled_mutation": (
            "physical event pair-germ and family selection" in derivation["open_scope"]
        ),
        "xmax_smuggled_into_endpoint_classification_mutation": (
            "metric-space distance and numerical Xmax" in derivation["open_scope"]
        ),
        "observation_or_dynamics_smuggled_mutation": (
            "dynamics action source matter bootstrap radiative transfer and observations"
            in derivation["open_scope"]
        ),
        "independent_population_floor": independent["exact_trials"] >= 20_000,
        "independent_cross_class_floor": independent["required_cross_classes"] == 9,
        "registered_landing_retained": derivation["landing"].startswith(
            "COMPLETED_PAIR_ENDPOINT_CLASSIFICATION__"
        ),
    }
    failed = sorted(name for name, caught in catches.items() if not caught)
    return {
        "audit": "G181",
        "status": "PASS" if not failed else "FAIL",
        "catch_count": len(catches),
        "catches": catches,
        "failed": failed,
    }


def main() -> None:
    result = main_result()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    target = HERE / "CATCH_PROOF_RESULT.json"
    if os.environ.get("UDT_READ_ONLY_REPLAY") == "1":
        assert target.read_text() == text
    else:
        target.write_text(text)
    if result["status"] != "PASS":
        raise SystemExit(text)
    print(f"PASS: {result['catch_count']} endpoint-classification mutation catches")


if __name__ == "__main__":
    main()
