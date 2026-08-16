#!/usr/bin/env python3
"""Independent Fraction/check replay for G124; imports no production code."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def inverse(a):
    n = len(a)
    work = [row[:] + ident for row, ident in zip(a, eye(n))]
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col])
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [value / scale for value in work[col]]
        for row in range(n):
            if row == col:
                continue
            scale = work[row][col]
            work[row] = [
                work[row][j] - scale * work[col][j] for j in range(2 * n)
            ]
    return [row[n:] for row in work]


def rank(a):
    work = [row[:] for row in a]
    rows, cols = len(work), len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][col]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            scale = work[row][col]
            work[row] = [
                work[row][j] - scale * work[pivot_row][j] for j in range(cols)
            ]
        pivot_row += 1
    return pivot_row


def check_witness(A: F, s: F, source_ratio: F):
    # Work with exponentiated log quantities so every comparison stays rational.
    exp_2kappa = abs(s)
    exp_2phi = abs(s) / (A * A)
    beta = s / (A * A)
    exp_2zeta = (source_ratio / A) ** 2
    junction_rhs = exp_2phi / exp_2kappa * source_ratio**2
    return exp_2kappa, exp_2phi, beta, exp_2zeta, junction_rhs


def main() -> None:
    flat = check_witness(F(1), F(1), F(1))
    rational = check_witness(F(3, 4), F(25, 16), F(6, 5))
    reversed_ruler = check_witness(F(3, 4), F(-25, 16), F(6, 5))

    # Coefficient vectors [constant, R, R^2] independently replay G116.
    p2, optical, vrel, vdot = F(7, 11), F(5, 13), F(3, 8), F(-2, 9)
    phi_coeff = [F(0), F(0), p2]
    kappa_coeff = [F(0), F(0), optical / 4]
    chi_coeff = [F(0), vrel, vdot]
    junction_coeff = [
        phi_coeff[i] - kappa_coeff[i] + chi_coeff[i] for i in range(3)
    ]
    expected_coeff = [F(0), vrel, p2 + vdot - optical / 4]
    w2 = F(7, 10)
    phi_fixed_coeff = [F(0), F(0), p2 + w2 / 2]
    chi_fixed_coeff = [F(0), vrel, vdot - w2 / 2]
    fixed_junction_coeff = [
        phi_fixed_coeff[i] - kappa_coeff[i] + chi_fixed_coeff[i]
        for i in range(3)
    ]

    turning_A = F(3, 4)
    turning_eps_1, turning_eps_2 = F(1, 9), F(1, 25)
    turning_ratio_1 = (F(1) / (turning_eps_1 * turning_A**2)) / (
        F(1) / turning_eps_1
    )
    turning_ratio_2 = (F(1) / (turning_eps_2 * turning_A**2)) / (
        F(1) / turning_eps_2
    )
    screen_K, screen_R = F(4, 9), F(3, 2)
    screen_theta = 2 * screen_K / screen_R
    screen_exp_2kappa = F(1) / screen_K

    M_A = [[F(1), F(1), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(4), F(0)], [F(0), F(0), F(0), F(4)]]
    M_B = [[F(1), F(1), F(0), F(0)], [F(0), F(4, 5), F(3), F(0)], [F(0), F(-3, 5), F(4), F(0)], [F(0), F(0), F(0), F(5)]]
    M_C = [[F(1), F(1), F(0), F(0)], [F(0), F(4, 5), F(0), F(3)], [F(0), F(0), F(5), F(0)], [F(0), F(-3, 5), F(0), F(4)]]
    D_BA = matmul(inverse(M_B), M_A)
    D_AB = matmul(inverse(M_A), M_B)
    D_CB = matmul(inverse(M_C), M_B)
    D_CA = matmul(inverse(M_C), M_A)

    Lambda4 = [[F(4), F(0)], [F(0), F(4)], [F(1), F(0)], [F(0), F(1)]]
    Lambda5 = [[F(5), F(0)], [F(0), F(5)], [F(1), F(0)], [F(0), F(1)]]
    joined = [Lambda4[i] + Lambda5[i] for i in range(4)]

    checks = {
        "flat_witness": flat == (F(1), F(1), F(1), F(1), F(1)),
        "rational_exp_2kappa": rational[0] == F(25, 16),
        "rational_exp_2phi": rational[1] == F(25, 9),
        "rational_beta": rational[2] == F(25, 9),
        "rational_exp_2zeta": rational[3] == F(64, 25),
        "rational_junction": rational[3] == rational[4],
        "orientation_only_flips_beta": (
            reversed_ruler[0] == rational[0]
            and reversed_ruler[1] == rational[1]
            and reversed_ruler[2] == -rational[2]
            and reversed_ruler[3] == rational[3]
        ),
        "turning_cancellation_exponentiated": (
            turning_ratio_1 == turning_ratio_2 == F(16, 9)
        ),
        "g116_coefficient_replay": junction_coeff == expected_coeff,
        "active_sky_drift_cancellation": fixed_junction_coeff == expected_coeff,
        "screen_link_exponentiated": (
            screen_R * screen_theta / 2 == screen_K
            and screen_exp_2kappa * screen_K == 1
        ),
        "g123_reversal": matmul(D_AB, D_BA) == eye(4),
        "g123_composition": matmul(D_CB, D_BA) == D_CA,
        "phase_images_rank_two": rank(Lambda4) == rank(Lambda5) == 2,
        "mismatched_phase_intersection_zero": 4 - rank(joined) == 0,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "implementation": "independent standard-library Fraction replay; logarithms checked through exact exponentiated ratios; no production import",
        "checks": checks,
        "exact_values": {
            "flat": [str(value) for value in flat],
            "rational": [str(value) for value in rational],
            "orientation_reversed": [str(value) for value in reversed_ruler],
            "g116_coefficients": [str(value) for value in junction_coeff],
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
