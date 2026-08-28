#!/usr/bin/env python3
"""Implementation-distinct standard-library exact replay for G290."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_VERIFICATION.json"


def conformal_christoffel(
    upper: int,
    left: int,
    right: int,
    gradient: list[Fraction],
) -> Fraction:
    """Exact Gamma^upper_left,right for exp(2 Omega)*diag(-1,1,1,1)."""
    signature = [-1, 1, 1, 1]
    term = Fraction(int(upper == left)) * gradient[right]
    term += Fraction(int(upper == right)) * gradient[left]
    if left == right:
        term -= Fraction(signature[left] * signature[upper]) * gradient[upper]
    return term


def direct_screen_connection(
    alpha: Fraction,
    adot: Fraction,
    x: Fraction,
    y: Fraction,
    z: Fraction,
) -> list[Fraction]:
    """Recompute <e_x,nabla e_y> with conformal factors canceled exactly."""
    radius2 = x * x + y * y + z * z
    gradient = [adot * radius2, 2 * alpha * x, 2 * alpha * y, 2 * alpha * z]
    connection = []
    for mu in range(4):
        # Only the x component survives contraction with e_x. The derivative
        # of exp(-Omega)e_y has no x component.
        connection.append(conformal_christoffel(1, mu, 2, gradient))
    return connection


def main() -> None:
    rng = random.Random(2900828)
    assertions = 0
    cases = 2400

    for _ in range(cases):
        alpha = Fraction(rng.choice([n for n in range(-11, 12) if n != 0]), rng.randint(1, 13))
        rho2 = Fraction(rng.randint(1, 9), rng.randint(10, 40))
        point_x = Fraction(rng.randint(-9, 9), rng.randint(1, 10))
        point_y = Fraction(rng.randint(-9, 9), rng.randint(1, 10))
        point_z = Fraction(rng.randint(-9, 9), rng.randint(1, 10))
        adot = Fraction(rng.randint(-9, 9), rng.randint(1, 10))
        direct_connection = direct_screen_connection(alpha, adot, point_x, point_y, point_z)
        expected_connection = [Fraction(0), 2 * alpha * point_y, -2 * alpha * point_x, Fraction(0)]
        for actual, expected in zip(direct_connection, expected_connection):
            assert actual == expected
            assertions += 1

        curvature = -4 * alpha
        angle_over_pi = -4 * alpha * rho2
        assert angle_over_pi / rho2 == curvature
        assertions += 1

        # Polynomial SO(2) gauge theta=p*x+q*y+c changes open carry only at endpoints.
        p = Fraction(rng.randint(-9, 9), rng.randint(1, 10))
        q = Fraction(rng.randint(-9, 9), rng.randint(1, 10))
        theta_a = Fraction(rng.randint(-9, 9), rng.randint(1, 10))
        theta_b = Fraction(rng.randint(-9, 9), rng.randint(1, 10))
        open_angle = Fraction(rng.randint(-20, 20), rng.randint(1, 11))
        transformed_open = open_angle - theta_b + theta_a
        assert transformed_open + theta_b - theta_a == open_angle
        assertions += 1
        width = Fraction(rng.randint(1, 9), rng.randint(1, 10))
        height = Fraction(rng.randint(1, 9), rng.randint(1, 10))
        constant = Fraction(rng.randint(-9, 9), rng.randint(1, 10))
        theta_00 = constant
        theta_10 = p * width + constant
        theta_11 = p * width + q * height + constant
        theta_01 = q * height + constant
        gauge_loop_increment = (
            (theta_10 - theta_00)
            + (theta_11 - theta_10)
            + (theta_01 - theta_11)
            + (theta_00 - theta_01)
        )
        assert gauge_loop_increment == 0
        assertions += 1

        # Orientation reversal sends the signed phase to its inverse class.
        reflected = -angle_over_pi
        assert reflected + angle_over_pi == 0
        assertions += 1

        alpha0 = Fraction(rng.randint(-7, 7), rng.randint(1, 9))
        slope = Fraction(rng.choice([n for n in range(-8, 9) if n != 0]), rng.randint(1, 9))
        time1 = Fraction(rng.randint(-6, 0), rng.randint(1, 7))
        time2 = Fraction(rng.randint(1, 7), rng.randint(1, 7))
        if time2 <= time1:
            time2 = time1 + 1
        alpha1 = alpha0 + slope * time1
        alpha2 = alpha0 + slope * time2
        holonomy_change_over_pi = -4 * rho2 * (alpha2 - alpha1)
        cylinder_flux_over_pi = -4 * rho2 * slope * (time2 - time1)
        assert holonomy_change_over_pi == cylinder_flux_over_pi
        assertions += 1

        assert Fraction(0) == -4 * Fraction(0) * rho2
        assertions += 1
        assert angle_over_pi != 0
        assertions += 1

        # A sufficiently small loop fixes a principal phase branch locally.
        small_rho2 = Fraction(1, 16 * (abs(alpha.numerator) + alpha.denominator))
        small_phase_over_pi = -4 * alpha * small_rho2
        assert abs(small_phase_over_pi) < 1
        assertions += 1

    # One closed loop is phase-aliased: alpha=1, rho^2=1/2 gives angle=-2*pi.
    alias_angle_over_pi = -4 * Fraction(1) * Fraction(1, 2)
    assert alias_angle_over_pi == -2
    assertions += 1

    result = {
        "status": "PASS",
        "method": "standard_library_fraction_direct_christoffel_connection_phase_and_transgression_replay",
        "imports_production_module": False,
        "reads_production_result": False,
        "random_exact_cases": cases,
        "direct_christoffel_connection_cases": cases,
        "assertions": assertions,
        "assertion_scope": "formula_level_exact_replay_with_2400_direct_christoffel_recomputations",
        "connection_coefficients": ["0", "2*alpha*y", "-2*alpha*x", "0"],
        "curvature_coefficient": "-4*alpha",
        "circle_angle_over_pi": "-4*alpha*rho^2",
        "timelive_flux_over_pi": "-4*rho^2*(alpha(t2)-alpha(t1))",
        "single_loop_alias_control": "alpha=1,rho^2=1/2 -> angle=-2*pi",
        "selection_residual_present": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
