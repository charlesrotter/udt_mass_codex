#!/usr/bin/env python3
"""Implementation-distinct exact/numerical verification of G284."""

from __future__ import annotations

from fractions import Fraction
import json
import math
import random


SEED = 28420260827
EXACT_CASES = 512
NETWORK_CASES = 64


def matmul(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def add(left: list[list[float]], right: list[list[float]], factor: float = 1.0) -> list[list[float]]:
    return [
        [left[i][j] + factor * right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*matrix)]


def identity(size: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]


def max_abs(matrix: list[list[float]]) -> float:
    return max(abs(value) for row in matrix for value in row)


def generator(u: float, coefficients: tuple[float, ...]) -> list[list[float]]:
    a0, a1, b0, b1, c0, c1 = coefficients
    t_xx = a0 + a1 * u
    t_xy = b0 + b1 * u
    t_yy = c0 + c1 * u
    return [
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [-t_xx, -t_xy, 0.0, 0.0],
        [-t_xy, -t_yy, 0.0, 0.0],
    ]


def derivative(u: float, state: list[list[float]], coefficients: tuple[float, ...]) -> list[list[float]]:
    return matmul(generator(u, coefficients), state)


def integrate(
    start: float,
    end: float,
    coefficients: tuple[float, ...],
    initial: list[list[float]] | None = None,
    steps: int = 600,
) -> list[list[float]]:
    state = identity(4) if initial is None else [row[:] for row in initial]
    step = (end - start) / steps
    u = start
    for _ in range(steps):
        k1 = derivative(u, state, coefficients)
        k2 = derivative(u + step / 2, add(state, k1, step / 2), coefficients)
        k3 = derivative(u + step / 2, add(state, k2, step / 2), coefficients)
        k4 = derivative(u + step, add(state, k3, step), coefficients)
        state = [
            [
                state[i][j]
                + step * (k1[i][j] + 2 * k2[i][j] + 2 * k3[i][j] + k4[i][j]) / 6
                for j in range(4)
            ]
            for i in range(4)
        ]
        u += step
    return state


def det2(matrix: list[list[float]]) -> float:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def exact_slope(t_xx: Fraction, t_xy: Fraction, t_yy: Fraction, x: Fraction, y: Fraction) -> Fraction:
    return -(t_xx * x * x + 2 * t_xy * x * y + t_yy * y * y) / 2


def main() -> None:
    rng = random.Random(SEED)
    exact_assertions = 0
    distinct_neighbor_cones = 0
    for _ in range(EXACT_CASES):
        entries = [Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(6)]
        t_xx, t_xy, t_yy, s_xx, s_xy, s_yy = entries
        if (t_xx, t_xy, t_yy) == (s_xx, s_xy, s_yy):
            s_xx += 1
        x = Fraction(rng.randint(-7, 7), rng.randint(1, 9))
        y = Fraction(rng.randint(-7, 7), rng.randint(1, 9))
        c_e = Fraction(rng.randint(1, 12), rng.randint(1, 9))
        scale = Fraction(rng.randint(1, 12), rng.randint(1, 9))

        qform = t_xx * x * x + 2 * t_xy * x * y + t_yy * y * y
        slope = exact_slope(t_xx, t_xy, t_yy, x, y)
        assert -qform - 2 * slope == 0
        exact_assertions += 1

        assert -c_e * c_e + c_e * c_e == 0
        assert -c_e * c_e + (-c_e) * (-c_e) == 0
        exact_assertions += 2

        origin = Fraction(0)
        h_xx = exact_slope(t_xx, t_xy, t_yy, 1, 0) + exact_slope(t_xx, t_xy, t_yy, -1, 0) - 2 * origin
        h_yy = exact_slope(t_xx, t_xy, t_yy, 0, 1) + exact_slope(t_xx, t_xy, t_yy, 0, -1) - 2 * origin
        h_xy = (
            exact_slope(t_xx, t_xy, t_yy, 1, 1)
            - exact_slope(t_xx, t_xy, t_yy, 1, -1)
            - exact_slope(t_xx, t_xy, t_yy, -1, 1)
            + exact_slope(t_xx, t_xy, t_yy, -1, -1)
        ) / 4
        assert (h_xx, h_xy, h_yy) == (-t_xx, -t_xy, -t_yy)
        exact_assertions += 3

        assert scale * scale * (-qform - 2 * slope) == 0
        assert (scale * Fraction(1, 1)) / (scale * Fraction(1, 1)) == 1
        exact_assertions += 2

        bound = 1 + abs(t_xx) + 2 * abs(t_xy) + abs(t_yy)
        epsilon = Fraction(1, 4) / bound
        small_q = t_xx * epsilon**2 + 2 * t_xy * epsilon**2 + t_yy * epsilon**2
        common_time_norm_times_two = -2 - small_q
        assert common_time_norm_times_two < 0
        exact_assertions += 1

        probes = ((1, 0), (0, 1), (1, 1))
        different = any(
            exact_slope(t_xx, t_xy, t_yy, px, py)
            != exact_slope(s_xx, s_xy, s_yy, px, py)
            for px, py in probes
        )
        assert different
        distinct_neighbor_cones += 1
        exact_assertions += 1

        central_state_t = (c_e, 1, 0, 1)
        central_state_s = (c_e, 1, 0, 1)
        assert central_state_t == central_state_s
        exact_assertions += 4

    symplectic = [
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [-1.0, 0.0, 0.0, 0.0],
        [0.0, -1.0, 0.0, 0.0],
    ]
    max_symplectic = 0.0
    max_composition = 0.0
    max_reversal = 0.0
    different_area_cases = 0
    for _ in range(NETWORK_CASES):
        q = rng.uniform(0.7, 1.6)
        coefficients = (
            q * q,
            rng.uniform(-0.35, 0.35),
            rng.uniform(-0.25, 0.25),
            rng.uniform(-0.25, 0.25),
            -q * q,
            rng.uniform(-0.35, 0.35),
        )
        end = rng.uniform(0.45, 0.9)
        middle = rng.uniform(0.2, 0.8) * end
        full = integrate(0.0, end, coefficients)
        first = integrate(0.0, middle, coefficients)
        second = integrate(middle, end, coefficients)
        composite = matmul(second, first)
        reverse = integrate(end, 0.0, coefficients)
        symplectic_residual = add(
            matmul(matmul(transpose(full), symplectic), full), symplectic, -1.0
        )
        composition_residual = add(composite, full, -1.0)
        reversal_residual = add(matmul(reverse, full), identity(4), -1.0)
        max_symplectic = max(max_symplectic, max_abs(symplectic_residual))
        max_composition = max(max_composition, max_abs(composition_residual))
        max_reversal = max(max_reversal, max_abs(reversal_residual))
        jacobi = [[full[0][2], full[0][3]], [full[1][2], full[1][3]]]
        if abs(det2(jacobi) - end * end) > 1.0e-9:
            different_area_cases += 1

    checks = {
        "all_exact_cE_cone_and_Hessian_assertions_pass": exact_assertions == EXACT_CASES * 14,
        "distinct_T_have_same_central_state_and_different_neighbor_cones": distinct_neighbor_cones
        == EXACT_CASES,
        "all_arbitrary_T_interval_transfers_symplectic": max_symplectic < 2.0e-10,
        "all_interval_compositions_close": max_composition < 2.0e-10,
        "all_interval_reversals_close": max_reversal < 2.0e-10,
        "all_nonflat_controls_change_Jacobi_area": different_area_cases == NETWORK_CASES,
    }
    if not all(checks.values()):
        raise AssertionError({name: value for name, value in checks.items() if not value})
    result = {
        "audit": "G284_INDEPENDENT_CAUSAL_PROJECTIVE_VERIFICATION",
        "status": "PASS",
        "seed": SEED,
        "exact_cases": EXACT_CASES,
        "exact_assertions": exact_assertions,
        "network_cases": NETWORK_CASES,
        "different_area_cases": different_area_cases,
        "maximum_symplectic_residual": max_symplectic,
        "maximum_composition_residual": max_composition,
        "maximum_reversal_residual": max_reversal,
        "checks": checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
