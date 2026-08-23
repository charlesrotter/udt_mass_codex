#!/usr/bin/env python3
"""Exact regression link from G229 metric jets to G227/G228 projections."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

import derive_metric_3jet_realization as production


ROOT = Path(__file__).resolve().parent
ETA = sp.diag(-1, 1, 1, 1)
TRAINING = (
    (sp.Rational(9), sp.Rational(-1, 2)),
    (sp.Rational(5, 4), sp.Rational(-2, 9)),
    (sp.Rational(-1, 7), sp.Rational(5, 3)),
    (sp.Rational(-1), sp.Rational(-1)),
    (sp.Rational(4, 9), sp.Rational(-2)),
    (sp.Rational(-6, 7), sp.Rational(6)),
    (sp.Rational(1, 6), sp.Rational(-7, 9)),
    (sp.Rational(5, 8), sp.Rational(1, 4)),
    (sp.Rational(1), sp.Rational(-5, 6)),
)
DIRECTIONS = {
    "k": (sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(1)),
    "l": (sp.Rational(1, 2), sp.Integer(0), sp.Integer(0), sp.Rational(-1, 2)),
    "s1": (sp.Integer(0), sp.Integer(1), sp.Integer(0), sp.Integer(0)),
    "s2": (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(0)),
}
DIRECTION_ORDER = ("k", "l", "s1", "s2")


def dot(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return (a.T * ETA * b)[0]


def wedge(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [a[i] * b[j] - a[j] * b[i] for i, j in production.BIVECTORS]
    )


def null_direction(p: sp.Rational, q: sp.Rational) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    denominator = 1 + p * p + q * q
    n = sp.Matrix((2 * p / denominator, 2 * q / denominator, (1 - p * p - q * q) / denominator))
    k = sp.Matrix((1, n[0], n[1], n[2]))
    ez = sp.Matrix((0, 0, 1))
    e1s = n.cross(ez)
    e2s = n.cross(e1s)
    e1 = sp.Matrix((0, e1s[0], e1s[1], e1s[2]))
    e2 = sp.Matrix((0, e2s[0], e2s[1], e2s[2]))
    assert sp.simplify(dot(k, k)) == 0
    return k, e1, e2


def g227_rows(pq: tuple[sp.Rational, sp.Rational]) -> sp.Matrix:
    k, e1, e2 = null_direction(*pq)
    v1 = wedge(e1, k)
    v2 = wedge(e2, k)
    contractions = ((v1, v1), (v1, v2), (v2, v2))
    return sp.Matrix(
        [[(left.T * q * right)[0] for q in production.Q_BASIS] for left, right in contractions]
    )


def direction_projection(direction: tuple[sp.Expr, ...]) -> sp.Matrix:
    matrix = sp.zeros(20, 80)
    for component in range(20):
        for derivative, coefficient in enumerate(direction):
            matrix[component, derivative * 20 + component] = coefficient
    return matrix


def q_from_coefficients(coefficients: sp.Matrix) -> sp.Matrix:
    q = sp.zeros(6, 6)
    for coefficient, basis in zip(coefficients, production.Q_BASIS):
        q += coefficient * basis
    return q


def tidal_matrix(coefficients: sp.Matrix) -> sp.Matrix:
    k = sp.Matrix((1, 0, 0, 1))
    screen = (sp.Matrix((0, 1, 0, 0)), sp.Matrix((0, 0, 1, 0)))
    q = q_from_coefficients(coefficients)
    return sp.Matrix(
        [[(wedge(left, k).T * q * wedge(right, k))[0] for right in screen] for left in screen]
    )


def run() -> dict[str, object]:
    c2 = production.build_c2()
    c3 = production.build_c3()
    bianchi = production.build_differential_bianchi()
    compatible = DomainMatrix.from_Matrix(bianchi).nullspace().to_Matrix().T
    hinv = production.build_h_inverse()
    kinv = production.build_k_inverse(compatible)

    realized_r = c2 * hinv
    realized_d = c3 * kinv
    sign_witness_coefficients = realized_r[:, 0]
    sign_witness_tide = tidal_matrix(sign_witness_coefficients)
    sign_witness_generator = sp.Matrix.vstack(
        sp.Matrix.hstack(sp.zeros(2), sp.eye(2)),
        sp.Matrix.hstack(-sign_witness_tide, sp.zeros(2)),
    )
    g227_null = sp.Matrix.vstack(*(g227_rows(pq) for pq in TRAINING))
    u = sp.Matrix((1, 0, 0, 0))
    e = sp.Matrix((0, 1, 0, 0))
    v_time = wedge(e, u)
    time_row = sp.Matrix([[(v_time.T * q * v_time)[0] for q in production.Q_BASIS]])

    subset_rows: list[dict[str, object]] = []
    for size in range(1, 5):
        for names in itertools.combinations(DIRECTION_ORDER, size):
            projection = sp.Matrix.vstack(*(direction_projection(DIRECTIONS[name]) for name in names))
            projected_metric_jets = projection * realized_d
            image_rank = production.exact_rank(projected_metric_jets)
            subset_rows.append(
                {
                    "key": "+".join(names),
                    "size": size,
                    "target_dimension": 20 * size,
                    "image_rank": image_rank,
                    "codimension": 20 * size - image_rank,
                }
            )

    expected_by_size = {1: (20, 0), 2: (40, 0), 3: (54, 6), 4: (60, 20)}
    subset_pattern_pass = all(
        (row["image_rank"], row["codimension"]) == expected_by_size[row["size"]]
        for row in subset_rows
    )
    result = {
        "landing": "G227_G228_PROJECTIONS_RECOVERED_FROM_REALIZED_METRIC_JETS",
        "universal_composition_checks": {
            "C2_Hinverse_identity": realized_r == sp.eye(20),
            "C3_Kinverse_compatible_basis": realized_d == compatible,
            "therefore_every_linear_null_screen_or_jacobi_contraction_recovers": True,
        },
        "g227": {
            "null_tide_map_rank_after_metric_realization": production.exact_rank(g227_null * realized_r),
            "expected_null_rank": 19,
            "timelike_augmented_rank_after_metric_realization": production.exact_rank(
                g227_null.col_join(time_row) * realized_r
            ),
            "expected_augmented_rank": 20,
        },
        "g228": {
            "subset_count": len(subset_rows),
            "subset_pattern_pass": subset_pattern_pass,
            "subset_census": subset_rows,
        },
        "g188_jacobi_sign_bridge": {
            "frozen_equation": "D''+T D=0",
            "tidal_definition": "T_AB=R(S_A,k,S_B,k)",
            "nonzero_realized_tide": str(sign_witness_tide),
            "first_order_generator": str(sign_witness_generator),
            "lower_left_block_equals_minus_tide": (
                sign_witness_generator[2:4, 0:2] == -sign_witness_tide
            ),
            "nonzero_sign_witness": sign_witness_tide == sp.diag(1, 0),
            "third_vertex_derivative": "D'''(0)=-T",
        },
        "scope": (
            "Regression recovery of conditional contractions only; no screen choice, values, "
            "observer population, transport, or history is selected."
        ),
    }
    result["all_checks_pass"] = (
        all(result["universal_composition_checks"].values())
        and result["g227"]["null_tide_map_rank_after_metric_realization"] == 19
        and result["g227"]["timelike_augmented_rank_after_metric_realization"] == 20
        and subset_pattern_pass
        and result["g188_jacobi_sign_bridge"]["lower_left_block_equals_minus_tide"]
        and result["g188_jacobi_sign_bridge"]["nonzero_sign_witness"]
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = run()
    if not args.no_write:
        (ROOT / "projection_recovery.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
