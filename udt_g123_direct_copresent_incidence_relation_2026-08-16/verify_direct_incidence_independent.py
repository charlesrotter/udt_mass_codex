#!/usr/bin/env python3
"""Independent Fraction replay of the G123 finite-dimensional claims."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def mat(rows):
    return [[F(value) for value in row] for row in rows]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def inverse(a):
    n = len(a)
    work = [row[:] + identity for row, identity in zip(a, eye(n))]
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col] != 0)
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
        pivot = next((row for row in range(pivot_row, rows) if work[row][col] != 0), None)
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
        if pivot_row == rows:
            break
    return pivot_row


def horizontal(a, b):
    return [a_row + b_row for a_row, b_row in zip(a, b)]


def phase_lift(radius):
    return mat(
        [
            [0, 0, radius, 0],
            [0, 0, 0, radius],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )


def main() -> None:
    eta = mat([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    M_A = mat([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 4, 0], [0, 0, 0, 4]])
    M_B = mat([[1, 1, 0, 0], [0, F(4, 5), 3, 0], [0, F(-3, 5), 4, 0], [0, 0, 0, 5]])
    M_C = mat([[1, 1, 0, 0], [0, F(4, 5), 0, 3], [0, 0, 5, 0], [0, F(-3, 5), 0, 4]])

    D_BA = multiply(inverse(M_B), M_A)
    D_AB = multiply(inverse(M_A), M_B)
    D_CB = multiply(inverse(M_C), M_B)
    D_CA = multiply(inverse(M_C), M_A)
    H_A = multiply(transpose(M_A), multiply(eta, M_A))
    H_B = multiply(transpose(M_B), multiply(eta, M_B))
    pullback_return = multiply(transpose(D_BA), multiply(H_B, D_BA))

    M_B_col = mat([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 5, 0], [0, 0, 0, 5]])
    D_col = multiply(inverse(M_B_col), M_A)
    lift_A = phase_lift(4)
    lift_B = phase_lift(5)
    carried_B = multiply(lift_B, D_col)

    Lambda_A = mat([[4, 0], [0, 4], [1, 0], [0, 1]])
    Lambda_B = mat([[5, 0], [0, 5], [1, 0], [0, 1]])
    vertex = mat([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

    checks = {
        "regular_ranks_four": rank(M_A) == rank(M_B) == rank(M_C) == 4,
        "direct_incidence_equation": multiply(M_B, D_BA) == M_A,
        "reversal": multiply(D_AB, D_BA) == eye(4),
        "composition": multiply(D_CB, D_BA) == D_CA,
        "pullback_isometry": pullback_return == H_A,
        "angular_to_pair_mixing_in_supplied_split": (
            rank([row[2:] for row in D_BA[:2]]) == 1
        ),
        "phase_lifts_rank_two": rank(lift_A) == rank(lift_B) == 2,
        "source_position_matches": carried_B[:2] == lift_A[:2],
        "source_momentum_not_forced": carried_B[2:] != lift_A[2:],
        "mismatch_intersection_zero": 4 - rank(horizontal(Lambda_A, Lambda_B)) == 0,
        "aligned_intersection_two": 4 - rank(horizontal(Lambda_A, Lambda_A)) == 2,
        "vertex_rank_two": rank(vertex) == 2,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "implementation": "independent standard-library Fraction elimination; no production import",
        "checks": checks,
        "exact_values": {
            "D_BA": [[str(value) for value in row] for row in D_BA],
            "angular_to_pair_block_rank_in_supplied_split": rank(
                [row[2:] for row in D_BA[:2]]
            ),
            "phase_lift_ranks": [rank(lift_A), rank(lift_B)],
            "vertex_rank": rank(vertex),
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
