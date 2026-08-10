#!/usr/bin/env python3
"""Constructive standard-library verification from coframe and Maurer--Cartan data."""

from __future__ import annotations

import json
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent


def matmul(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a: list[list[Q]]) -> list[list[Q]]:
    return [list(row) for row in zip(*a)]


def inverse(a: list[list[Q]]) -> list[list[Q]]:
    n = len(a)
    augmented = [row[:] + [Q(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column] != 0)
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][j] - factor * augmented[column][j] for j in range(2 * n)
            ]
    return [row[n:] for row in augmented]


def scale_matrix(value: Q, a: list[list[Q]]) -> list[list[Q]]:
    return [[value * item for item in row] for row in a]


def coframe_and_derivatives(
    lam: Q, u: Q, v: Q, a: Q, p1: Q, p2: Q, p3: Q
) -> tuple[list[list[Q]], list[list[list[Q]]]]:
    coframe = [
        [1 / u, a / u, Q(0), Q(0)],
        [Q(0), u, Q(0), Q(0)],
        [Q(0), Q(0), v, Q(0)],
        [Q(0), Q(0), Q(0), v],
    ]
    log_u = [Q(0), p1, p2, p3]
    log_v = [Q(0), lam * p1, lam * p2, lam * p3]
    derivatives = []
    for direction in range(4):
        du = log_u[direction]
        dv = log_v[direction]
        derivatives.append(
            [
                [-du / u, -a * du / u, Q(0), Q(0)],
                [Q(0), u * du, Q(0), Q(0)],
                [Q(0), Q(0), v * dv, Q(0)],
                [Q(0), Q(0), Q(0), v * dv],
            ]
        )
    return coframe, derivatives


def structure_constants(mc_sign: int) -> list[list[list[Q]]]:
    # Base order is (T,Z,X,Y).  Maurer--Cartan gives
    # [X,Y]=+/-2Z, [Y,Z]=+/-2X, [Z,X]=+/-2Y.
    constants = [[[Q(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    value = Q(2 * mc_sign)
    for left, right, output in ((2, 3, 1), (3, 1, 2), (1, 2, 3)):
        constants[left][right][output] = value
        constants[right][left][output] = -value
    return constants


def frame_bracket(
    left: int,
    right: int,
    coframe: list[list[Q]],
    d_coframe: list[list[list[Q]]],
    constants: list[list[list[Q]]],
) -> list[Q]:
    frame = inverse(coframe)
    # Differentiate the inverse constructively: d(F)=-F d(A) F.
    d_frame = [scale_matrix(Q(-1), matmul(matmul(frame, derivative), frame)) for derivative in d_coframe]
    bracket_base = []
    for output in range(4):
        value = Q(0)
        for direction in range(4):
            value += frame[direction][left] * d_frame[direction][output][right]
            value -= frame[direction][right] * d_frame[direction][output][left]
        for first in range(4):
            for second in range(4):
                value += (
                    frame[first][left]
                    * frame[second][right]
                    * constants[first][second][output]
                )
        bracket_base.append(value)
    # Coframe components are the components in the e_a basis.
    return [sum((coframe[row][column] * bracket_base[column] for column in range(4)), Q(0)) for row in range(4)]


def leaf_metric(coframe: list[list[Q]]) -> list[list[Q]]:
    # Tangent columns are the base fields T and Z; no metric coefficient is assigned directly.
    tangents = [
        [Q(1), Q(0)],
        [Q(0), Q(1)],
        [Q(0), Q(0)],
        [Q(0), Q(0)],
    ]
    pulled_coframe = matmul(coframe, tangents)
    eta = [
        [Q(-1), Q(0), Q(0), Q(0)],
        [Q(0), Q(1), Q(0), Q(0)],
        [Q(0), Q(0), Q(1), Q(0)],
        [Q(0), Q(0), Q(0), Q(1)],
    ]
    return matmul(matmul(transpose(pulled_coframe), eta), pulled_coframe)


def verify_witness(
    lam: Q, u: Q, v: Q, a: Q, p1: Q, p2: Q, p3: Q, mc_sign: int
) -> dict[str, bool]:
    coframe, derivatives = coframe_and_derivatives(lam, u, v, a, p1, p2, p3)
    frame = inverse(coframe)
    identity = [[Q(int(i == j)) for j in range(4)] for i in range(4)]
    constants = structure_constants(mc_sign)
    pair = frame_bracket(0, 1, coframe, derivatives, constants)
    screen = frame_bracket(2, 3, coframe, derivatives, constants)
    h = leaf_metric(coframe)
    det_h = h[0][0] * h[1][1] - h[0][1] * h[1][0]
    terminal_ratio = (-det_h) / (h[0][0] * h[0][0])
    return {
        "coframe_inverted_by_gauss_jordan": matmul(coframe, frame) == identity,
        "pair_bracket_derived_transverse_zero": pair[2:] == [Q(0), Q(0)],
        "screen_bracket_derived_pair_nonzero": screen[1] != 0,
        "leaf_metric_derived_twist_retained": h[0][1] != 0,
        "leaf_metric_derived_det_minus_one": det_h == -1,
        "terminal_ratio_derived_u_fourth": terminal_ratio == u**4,
    }


def main() -> None:
    lambdas = [Q(-2), Q(-1), Q(0), Q(1, 2), Q(1), Q(2)]
    witnesses = []
    for index, lam in enumerate(lambdas, start=1):
        for mc_sign in (1, -1):
            values = {
                "lam": lam,
                "u": Q(index + 1, index),
                "v": Q(index + 2, index + 1),
                "a": Q(1, 64),
                "p1": Q(index - 3, index + 2),
                "p2": Q(2 * index - 5, index + 3),
                "p3": Q(4 - index, index + 4),
                "mc_sign": mc_sign,
            }
            checks = verify_witness(**values)
            if not all(checks.values()):
                raise SystemExit(f"FAIL witness {index}/{mc_sign}: {checks}")
            witnesses.append(
                {
                    "id": f"C{index:02d}_MC_{'PLUS' if mc_sign == 1 else 'MINUS'}",
                    "values": {
                        ("lambda" if key == "lam" else key): str(value)
                        for key, value in values.items()
                    },
                    "checks": checks,
                }
            )

    result = {
        "mode": "independent_standard_library_constructive_exact_rationals",
        "imports_production_controller": False,
        "assigns_final_bracket_or_leaf_metric": False,
        "derives_frame_by_gauss_jordan": True,
        "derives_frame_derivatives_by_inverse_identity": True,
        "derives_brackets_from_structure_constants": True,
        "derives_leaf_metric_from_coframe_pullback": True,
        "lambda_strata": 6,
        "maurer_cartan_sign_conventions": 2,
        "witness_count": len(witnesses),
        "checks_per_witness": 6,
        "passed_checks": 72,
        "witnesses": witnesses,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS: 72/72 constructive exact-rational checks; six lambda strata; both MC signs")


if __name__ == "__main__":
    main()
