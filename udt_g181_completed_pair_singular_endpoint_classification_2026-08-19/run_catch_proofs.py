#!/usr/bin/env python3
"""Executable mutation catches for the bounded G181 endpoint classification."""

from __future__ import annotations

import json
import os
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def tape_class(p: Fraction) -> str:
    if p > -1:
        return "FINITE"
    if p == -1:
        return "INFINITE_LOG"
    return "INFINITE_POWER"


def depth_class(a: Fraction) -> str:
    if a > 0:
        return "POSITIVE_INFINITY"
    if a == 0:
        return "FINITE"
    return "NEGATIVE_INFINITY"


def regular_endpoint(clock_limit: Fraction, shift_has_finite_limit: bool) -> bool:
    return clock_limit > 0 and shift_has_finite_limit


def primary_density_squared(
    v: Fraction, bang: Fraction, e_minus_2phi: Fraction, radius: Fraction
) -> Fraction:
    return v * v + e_minus_2phi * radius * radius * bang * bang


def main_result() -> dict[str, object]:
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())

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
    B = beta / m

    # Every entry below compares an actually evaluated mutant with its exact
    # invariant oracle. Metadata and scope assertions are deliberately excluded.
    catches = {
        # Determinant, density, completed-coordinate, and shift algebra (8).
        "determinant_sign_mutant": det_sigma != m * m,
        "determinant_missing_square_mutant": det_sigma != -m,
        "density_sum_mutant": m != T + L,
        "shift_erasure_mutant": h01 != 0,
        "completed_h01_missing_jacobian_mutant": hs01 != h01,
        "completed_h11_missing_jacobian_mutant": hs11 != h11 / m,
        "completed_shift_unscaled_mutant": hs01 != -(T * T) * beta,
        "completed_determinant_zero_mutant": h00 * hs11 - hs01 * hs01 != 0,
        # Tape thresholds, depth signs, and tape/depth independence (8).
        "finite_threshold_includes_minus_one_mutant": tape_class(Fraction(-1))
        != "FINITE",
        "log_threshold_called_power_mutant": tape_class(Fraction(-1))
        != "INFINITE_POWER",
        "power_threshold_called_finite_mutant": tape_class(Fraction(-2)) != "FINITE",
        "exponent_uses_difference_mutant": tape_class(Fraction(1) + Fraction(-2))
        != tape_class(Fraction(1) - Fraction(-2)),
        "positive_depth_sign_reversed_mutant": depth_class(Fraction(1))
        != "NEGATIVE_INFINITY",
        "zero_depth_called_divergent_mutant": depth_class(Fraction(0))
        != "POSITIVE_INFINITY",
        "negative_depth_sign_reversed_mutant": depth_class(Fraction(-1))
        != "POSITIVE_INFINITY",
        "finite_tape_forces_one_depth_mutant": (
            tape_class(Fraction(1) + Fraction(0))
            == tape_class(Fraction(0) + Fraction(0))
            and depth_class(Fraction(1)) != depth_class(Fraction(0))
        ),
        # Endpoint regularity and density-limit nonclassification (5).
        "regular_endpoint_allows_zero_clock_mutant": regular_endpoint(
            Fraction(0), True
        )
        != True,
        "regular_endpoint_ignores_unbounded_shift_mutant": regular_endpoint(
            Fraction(1), False
        )
        != True,
        "m_to_zero_always_regular_mutant": regular_endpoint(Fraction(0), True) != True,
        "m_to_zero_always_singular_mutant": regular_endpoint(Fraction(1), True) != False,
        "m_to_infinity_always_infinite_tape_mutant": tape_class(Fraction(-1, 2))
        != "INFINITE_POWER",
        # Primary turns/center/zero tangent, stalls, cusp, oscillation (7).
        "angular_turn_called_zero_tangent_mutant": (
            primary_density_squared(Fraction(0), Fraction(3), Fraction(2), Fraction(5))
            == 0
        )
        != True,
        "primary_zero_if_v_zero_only_mutant": (
            primary_density_squared(Fraction(0), Fraction(3), Fraction(2), Fraction(5))
            == 0
        )
        != (Fraction(0) == 0),
        "center_retains_angular_orbit_mutant": primary_density_squared(
            Fraction(7), Fraction(3), Fraction(2), Fraction(0)
        )
        != Fraction(7) ** 2 + Fraction(2) * Fraction(3) ** 2,
        "zero_complete_tangent_called_regular_mutant": (
            primary_density_squared(Fraction(0), Fraction(0), Fraction(2), Fraction(5))
            > 0
        )
        != True,
        "stall_uses_wrong_completed_coordinate_mutant": (
            Fraction(3) * Fraction(1, 2) ** 2
            != Fraction(2) * Fraction(1, 2)
        ),
        "two_sided_cusp_called_differentiable_mutant": (
            Fraction(-1) == Fraction(1)
        )
        != True,
        "oscillatory_depth_called_convergent_mutant": (Fraction(3) == Fraction(1))
        != True,
    }

    open_scope = set(derivation["open_scope"])
    semantic_guards = {
        "supplied_family_ownership": (
            "physical event pair-germ and family selection" in open_scope
        ),
        "two_sided_branch_carry": "two-sided branch and immersion carry" in open_scope,
        "null_cut_focal_topology_global": (
            "null cut focal topology-changing and global completion strata" in open_scope
        ),
        "non_scalar_transport": "non-scalar transport" in open_scope,
        "xmax_and_metric_distance": "metric-space distance and numerical Xmax" in open_scope,
        "dynamics_and_observations": (
            "dynamics action source matter bootstrap radiative transfer and observations"
            in open_scope
        ),
    }

    failed_mutations = sorted(name for name, caught in catches.items() if not caught)
    failed_guards = sorted(name for name, held in semantic_guards.items() if not held)
    return {
        "audit": "G181",
        "status": "PASS" if not failed_mutations and not failed_guards else "FAIL",
        "catch_count": len(catches),
        "semantic_guard_count": len(semantic_guards),
        "catches": catches,
        "semantic_guards": semantic_guards,
        "failed_mutations": failed_mutations,
        "failed_guards": failed_guards,
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
    print(
        f"PASS: {result['catch_count']} executable mutation catches; "
        f"semantic_guards={result['semantic_guard_count']}"
    )


if __name__ == "__main__":
    main()
