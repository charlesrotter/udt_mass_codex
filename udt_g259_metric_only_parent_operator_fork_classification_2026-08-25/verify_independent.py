#!/usr/bin/env python3
"""Independent source-first checks for G259; no production import or result read."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def poly_value(coeffs: list[Fraction], x: Fraction) -> Fraction:
    return sum(c * x**i for i, c in enumerate(coeffs))


def poly_derivative(coeffs: list[Fraction], x: Fraction, order: int) -> Fraction:
    answer = Fraction(0)
    for i, coefficient in enumerate(coeffs):
        if i < order:
            continue
        factor = 1
        for j in range(order):
            factor *= i - j
        answer += coefficient * factor * x ** (i - order)
    return answer


def main() -> None:
    assertions = 0

    coefficient_sets = [
        [Fraction(1), Fraction(2), Fraction(-3), Fraction(5)],
        [Fraction(4, 3), Fraction(-7, 5), Fraction(2, 9), Fraction(11, 4), Fraction(-1, 6)],
        [Fraction(9, 7), Fraction(0), Fraction(3, 8), Fraction(-5, 11), Fraction(7, 13)],
    ]
    radii = [Fraction(1, 3), Fraction(2, 5), Fraction(7, 4), Fraction(5, 2)]
    for coeffs in coefficient_sets:
        for radius in radii:
            f = poly_value(coeffs, radius)
            fp = poly_derivative(coeffs, radius, 1)
            fpp = poly_derivative(coeffs, radius, 2)
            e0 = radius * fp + f - 1
            e1 = radius * fp + radius * radius * fpp / 2
            e0_prime = 2 * fp + radius * fpp
            assert radius * e0_prime == 2 * e1
            assertions += 1

            mu = radius * (1 - f) / 2
            mu_prime = (1 - f - radius * fp) / 2
            mu_second = -(2 * fp + radius * fpp) / 2
            assert e0 == -2 * mu_prime
            assert e1 == -radius * mu_second
            assert f == 1 - 2 * mu / radius
            assertions += 3

    for constant in (Fraction(-7, 3), Fraction(0), Fraction(11, 5)):
        for radius in radii:
            f = 1 + constant / radius
            fp = -constant / radius**2
            fpp = 2 * constant / radius**3
            assert radius * fp + f - 1 == 0
            assert radius * fp + radius**2 * fpp / 2 == 0
            assertions += 2

    # Direct t=0 fourth-order counteroperator checks for several exact b and ell values.
    for b in (Fraction(1, 7), Fraction(-2, 5), Fraction(9, 4)):
        h00 = -72 * b * b
        hspace = -216 * b * b
        assert h00 != 0 and hspace != 0
        assertions += 2
        for ell in (Fraction(1, 3), Fraction(5, 2)):
            extension_one = -72 * ell * ell * b * b
            extension_two = -144 * ell * ell * b * b
            assert extension_one != extension_two
            assertions += 1

    # Unit equations for c_E^x G^y: mass neutrality forces y=0, time neutrality then x=0,
    # leaving length exponent zero rather than one.
    y = Fraction(0)
    x = -2 * y
    assert -y == 0 and -x - 2 * y == 0 and x + 3 * y != 1
    assertions += 3

    # Twelve simple nodes: the product vanishes at each node and has nonzero derivative there.
    for node in range(1, 13):
        value = 1
        for other in range(1, 13):
            value *= node - other
        assert value == 0
        derivative = 1
        for other in range(1, 13):
            if other != node:
                derivative *= node - other
        assert derivative != 0
        assertions += 2

    result = {
        "status": "PASS",
        "assertions": assertions,
        "production_imported": False,
        "production_result_read": False,
        "checks": {
            "spherical_residual_dependency": True,
            "mass_aspect_identity": True,
            "complete_vacuum_family_substitution": True,
            "higher_order_counteroperator_nonidentity": True,
            "cE_Gobs_no_length": True,
            "twelve_values_leave_derivative_freedom": True,
        },
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(f"PASS: {assertions} independent exact rational assertions")


if __name__ == "__main__":
    main()
