#!/usr/bin/env python3
"""Independent exact Fraction replay for G220; imports no production implementation."""

from __future__ import annotations

import json
from fractions import Fraction
from math import gcd


if not __debug__:
    raise RuntimeError("G220 evidence must run with Python assertions enabled; -O is forbidden")


def norm(dt: Fraction, dx: Fraction, n: Fraction, a: Fraction, beta: Fraction) -> Fraction:
    return -(n * (dt + beta * dx)) ** 2 + (a * dx) ** 2


def verify() -> dict[str, object]:
    checks = 0
    endpoint_cases = 0
    world_function_coordinate_cases = 0
    affine_witness_cases = 0
    moving_flat_cases = 0
    return_diff_cases = 0
    affine_positive_d_cases = 0
    affine_negative_d_cases = 0

    def exact(condition: bool) -> None:
        nonlocal checks
        assert condition
        checks += 1

    for i in range(1, 5001):
        n_a = Fraction(2 + i % 7, 3 + i % 5)
        n_b = Fraction(3 + i % 11, 4 + i % 7)
        cp_a = Fraction(5 + i % 13, 3 + i % 3)
        cp_b = Fraction(7 + i % 17, 4 + i % 4)
        beta_a = Fraction(i % 5 - 2, 20)
        beta_b = Fraction(i % 7 - 3, 25)
        a_a = cp_a + n_a * beta_a
        a_b = cp_b + n_b * beta_b
        cm_a = a_a + n_a * beta_a
        cm_b = a_b + n_b * beta_b
        exact(min(n_a, n_b, cp_a, cp_b, a_a, a_b, cm_a, cm_b) > 0)

        right_a = n_a / cp_a
        right_b = n_b / cp_b
        left_a = -n_a / cm_a
        left_b = -n_b / cm_b
        dt_b_dt_a = n_a * cp_b / (cp_a * n_b)
        r = n_b * dt_b_dt_a / n_a
        dt_a_dy = 1 / n_a
        dt_b_dy = dt_b_dt_a * dt_a_dy
        target_norm = norm(dt_b_dy, Fraction(0), n_b, a_b, beta_b)
        inverse = cp_a / cp_b
        # A later left-moving B->A incidence branch has its own first jet.
        dt_a_dt_b_return = n_b * cm_a / (cm_b * n_a)
        future_return = n_a * dt_a_dt_b_return / n_b

        det_a = -(n_a * a_a) ** 2
        det_b = -(n_b * a_b) ** 2
        exact(det_a < 0)
        exact(det_b < 0)
        exact(norm(Fraction(1), right_a, n_a, a_a, beta_a) == 0)
        exact(norm(Fraction(1), right_b, n_b, a_b, beta_b) == 0)
        exact(norm(Fraction(1), left_a, n_a, a_a, beta_a) == 0)
        exact(norm(Fraction(1), left_b, n_b, a_b, beta_b) == 0)
        exact(-n_a / cp_a + n_b * dt_b_dt_a / cp_b == 0)
        exact(r == cp_b / cp_a)
        exact(norm(dt_a_dy, Fraction(0), n_a, a_a, beta_a) == -1)
        exact(target_norm == -(r**2))
        exact((-target_norm) == r**2)
        exact(r * inverse == 1)
        exact(-n_b / cm_b + n_a * dt_a_dt_b_return / cm_a == 0)
        exact(future_return == cm_a / cm_b)
        return_diff_cases += int(future_return != inverse)
        endpoint_cases += 1

        # Direct coordinate reconstruction of the Minkowski world function.
        exp_eta = Fraction(2 + i % 19, 1 + i % 7)
        gamma = (exp_eta + 1 / exp_eta) / 2
        sinh_eta = (exp_eta - 1 / exp_eta) / 2
        emission = Fraction(i % 7, 20)
        separation = Fraction(5 + i % 11, 3)
        reception = exp_eta * (emission + separation)
        delta_t = gamma * reception - emission
        delta_x = separation + sinh_eta * reception
        sigma = (-delta_t**2 + delta_x**2) / 2
        sigma_a_u = delta_t
        sigma_b_u = -gamma * delta_t + sinh_eta * delta_x
        implicit = -sigma_a_u / sigma_b_u
        k_a_u = Fraction(-1)
        k_b_u = -gamma + sinh_eta
        scale = Fraction(5 + i % 12, 11 + i % 7)
        exact(sigma == 0)
        exact(delta_t == delta_x and delta_t > 0)
        exact(sigma_a_u + sigma_b_u * exp_eta == 0)
        exact(implicit == exp_eta)
        exact(k_a_u / k_b_u == exp_eta)
        exact((scale * k_a_u) / (scale * k_b_u) == implicit)
        world_function_coordinate_cases += 1

    for i in range(1, 1001):
        a0 = Fraction(5 + i % 7)
        t_a = Fraction(i % 13, 9)
        d = Fraction((1 + i % 5) * (-1 if i % 2 else 1), 10)
        slope_a = Fraction(3 + i % 7, 5)
        slope_beta = slope_a - d
        t_b = t_a + Fraction(1 + i % 5, 20)
        cp_a = a0 + d * t_a
        cp_b = a0 + d * t_b
        q = cp_b / cp_a
        exact(d == slope_a - slope_beta)
        exact(cp_a == (a0 + slope_a * t_a) - slope_beta * t_a)
        exact(cp_b == (a0 + slope_a * t_b) - slope_beta * t_b)
        exact(t_b == (q * cp_a - a0) / d)
        exact(cp_b / cp_a == q)
        exact(min(cp_a, cp_b, a0 + slope_a * t_a, a0 + slope_a * t_b) > 0)
        affine_positive_d_cases += int(d > 0)
        affine_negative_d_cases += int(d < 0)
        affine_witness_cases += 1

    for m in range(2, 24):
        for n in range(1, m):
            if gcd(m, n) != 1:
                continue
            gamma = Fraction(m * m + n * n, 2 * m * n)
            v = Fraction(m * m - n * n, m * m + n * n)
            exp_eta = Fraction(m, n)
            k_dot_u_a = Fraction(-1)
            k_dot_u_b = -gamma + v * gamma
            exact(gamma * gamma * (1 - v * v) == 1)
            exact(k_dot_u_a / k_dot_u_b == exp_eta)
            moving_flat_cases += 1

    exact(return_diff_cases > 4000)
    return {
        "exact_checks": checks,
        "endpoint_cases": endpoint_cases,
        "world_function_coordinate_cases": world_function_coordinate_cases,
        "affine_witness_cases": affine_witness_cases,
        "moving_flat_cases": moving_flat_cases,
        "return_diff_cases": return_diff_cases,
        "affine_positive_d_cases": affine_positive_d_cases,
        "affine_negative_d_cases": affine_negative_d_cases,
        "implementation": "stdlib_Fraction_no_production_import",
        "all_checks_pass": True,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
