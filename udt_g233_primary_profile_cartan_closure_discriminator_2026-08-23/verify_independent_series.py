#!/usr/bin/env python3
"""Independent exact-Fraction series replay of the G233 load-bearing witness.

No SymPy or production helper is imported.  The replay fixes c=2, r0=3 and
compares b=-2 with b=5; these are algebraic test values, not physical pins.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import factorial
from pathlib import Path


OUT = Path(__file__).with_name("independent_results.json")
DEGREE = 12
SAFE_DEGREE = 8


def zero():
    return [Fraction(0) for _ in range(DEGREE + 1)]


def constant(value):
    out = zero()
    out[0] = Fraction(value)
    return out


def variable():
    out = zero()
    out[1] = Fraction(1)
    return out


def add(left, right):
    return [a + b for a, b in zip(left, right)]


def scale(value, series):
    value = Fraction(value)
    return [value * item for item in series]


def multiply(left, right):
    out = zero()
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if i + j <= DEGREE:
                out[i + j] += a * b
    return out


def derivative(series):
    out = zero()
    for degree in range(1, DEGREE + 1):
        out[degree - 1] = degree * series[degree]
    return out


def exp_series(series):
    if series[0] != 0:
        raise ValueError("independent exp_series expects zero constant term")
    out = constant(1)
    power = constant(1)
    for order in range(1, DEGREE + 1):
        power = multiply(power, series)
        out = add(out, scale(Fraction(1, factorial(order)), power))
    return out


def monomial(degree, coefficient=1):
    out = zero()
    out[degree] = Fraction(coefficient)
    return out


def evaluate_zero(series):
    return series[0]


def profile_data(b_value, c_value=2, r0=3):
    s = variable()
    phi = add(add(monomial(3), monomial(4, c_value)), monomial(5, b_value))
    f = exp_series(scale(-2, phi))
    exp_minus_2s = exp_series(scale(-2, s))
    exp_minus_s_phi = exp_series(scale(-1, add(s, phi)))

    numerator = add(
        add(scale(-1, derivative(derivative(f))), scale(-3, derivative(f))),
        scale(2, add(constant(1), scale(-1, f))),
    )
    scalar_curvature = scale(Fraction(1, r0 * r0), multiply(exp_minus_2s, numerator))
    radial_speed = scale(Fraction(1, r0), exp_minus_s_phi)

    radial_values = []
    current = scalar_curvature
    for _ in range(4):
        radial_values.append(evaluate_zero(current))
        current = multiply(radial_speed, derivative(current))

    # In the s chart, Gamma^s_ss=1+phi_s and n^s=exp(-s-phi)/r0.
    gamma_sss = add(constant(1), derivative(phi))
    acceleration = add(
        multiply(radial_speed, derivative(radial_speed)),
        multiply(gamma_sss, multiply(radial_speed, radial_speed)),
    )

    g_tt = scale(-1, f)
    g_ss = scale(r0 * r0, exp_series(scale(2, add(s, phi))))
    return {
        "phi": phi,
        "g_tt": g_tt,
        "g_ss": g_ss,
        "radial_values": radial_values,
        "acceleration": acceleration,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    first = profile_data(-2)
    second = profile_data(5)
    r0 = 3
    delta_b = Fraction(7)
    expected_delta = Fraction(240, r0**5) * delta_b

    metric_equal_through_four = all(
        first[name][order] == second[name][order]
        for name in ("g_tt", "g_ss")
        for order in range(5)
    )
    metric_differs_at_five = any(
        first[name][5] != second[name][5] for name in ("g_tt", "g_ss")
    )
    state_equal = first["radial_values"][:3] == second["radial_values"][:3]
    next_delta = second["radial_values"][3] - first["radial_values"][3]
    acceleration_zero = all(value == 0 for value in first["acceleration"][: SAFE_DEGREE + 1])
    acceleration_zero = acceleration_zero and all(
        value == 0 for value in second["acceleration"][: SAFE_DEGREE + 1]
    )

    checks = {
        "metric_series_equal_through_four": metric_equal_through_four,
        "metric_series_differ_at_five": metric_differs_at_five,
        "scalar_contractions_through_nabla2_equal": state_equal,
        "nabla3_scalar_contraction_differs": next_delta != 0,
        "nabla3_difference_matches_exact_coefficient": next_delta == expected_delta,
        "radial_unit_field_geodesic": acceleration_zero,
        "series_padding_at_least_four_orders": DEGREE - SAFE_DEGREE >= 4,
    }
    result = {
        "implementation": "standard-library Fraction truncated formal series; no production imports",
        "test_values": {"c": 2, "r0": 3, "b_first": -2, "b_second": 5},
        "radial_values_first": [str(value) for value in first["radial_values"]],
        "radial_values_second": [str(value) for value in second["radial_values"]],
        "next_difference": str(next_delta),
        "expected_difference": str(expected_delta),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    if not args.no_write:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
