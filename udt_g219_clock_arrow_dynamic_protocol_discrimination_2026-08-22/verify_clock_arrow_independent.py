#!/usr/bin/env python3
"""Independent exact Fraction replay; imports no production implementation."""

from __future__ import annotations

import json
from fractions import Fraction
from math import gcd


def verify() -> dict[str, object]:
    assertions = 0
    cases = 0

    def exact_check(condition: bool) -> None:
        nonlocal assertions
        assert condition
        assertions += 1

    for m in range(2, 32):
        for n in range(1, m):
            if gcd(m, n) != 1:
                continue
            gamma = Fraction(m * m + n * n, 2 * m * n)
            v_abs = Fraction(m * m - n * n, m * m + n * n)
            for sign in (-1, 1):
                v = sign * v_abs
                exp_eta = Fraction(m, n) if sign == 1 else Fraction(n, m)
                exact_check(gamma * gamma * (1 - v * v) == 1)
                for a in (Fraction(-2, 7), Fraction(0), Fraction(3, 7)):
                    for length in (Fraction(1), Fraction(5, 3)):
                        b_null = exp_eta * (a + length)
                        b_t = gamma * b_null
                        b_x = length + v * gamma * b_null
                        exact_check(b_t - a == b_x)

                        b_afermi = a / gamma
                        exact_check(gamma * b_afermi == a)

                        b_bfermi = gamma * (a + v * length)
                        delta_t = a - gamma * b_bfermi
                        delta_x = -length - v * gamma * b_bfermi
                        exact_check(-gamma * delta_t + v * gamma * delta_x == 0)
                        exact_check(b_bfermi == gamma * a + gamma * v * length)

                        a_minus = b_null / exp_eta - length
                        a_plus = exp_eta * b_null + length
                        exact_check(a_minus == a)
                        exact_check((a_minus + a_plus) / 2 == gamma * b_null)
                        exact_check((a_plus - a_minus) / 2 == length + v * gamma * b_null)

                        inverse_slope = 1 / exp_eta
                        return_slope = exp_eta
                        echo_slope = exp_eta * exp_eta
                        exact_check(inverse_slope * exp_eta == 1)
                        exact_check(return_slope * exp_eta == echo_slope)
                        exact_check(Fraction(1, gamma) > 0)
                        exact_check(gamma > 0)
                        exact_check(exp_eta > 0)
                        cases += 1

    assert cases > 1000
    return {
        "cases": cases,
        "assertions": assertions,
        "exact": True,
        "implementation": "stdlib_Fraction_no_production_import",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
