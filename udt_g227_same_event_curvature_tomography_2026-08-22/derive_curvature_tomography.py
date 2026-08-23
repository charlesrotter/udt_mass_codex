#!/usr/bin/env python3
"""Exact production derivation for G227 same-event curvature tomography."""

from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parent
BIVECTORS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
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
HELD_OUT = (
    (sp.Rational(2, 7), sp.Rational(3, 5)),
    (sp.Rational(-3, 4), sp.Rational(1, 8)),
    (sp.Rational(7, 6), sp.Rational(-2, 5)),
    (sp.Rational(-5, 9), sp.Rational(-4, 7)),
)
ETA = sp.diag(-1, 1, 1, 1)


def dot(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return (a.T * ETA * b)[0]


def wedge(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([a[i] * b[j] - a[j] * b[i] for i, j in BIVECTORS])


def curvature_basis() -> tuple[list[tuple[int, int]], list[sp.Matrix]]:
    """Symmetric bivector forms with Q[2,3] = -Q[0,5] + Q[1,4]."""
    variables = [(i, j) for i in range(6) for j in range(i, 6) if (i, j) != (2, 3)]
    assert len(variables) == 20
    basis: list[sp.Matrix] = []
    for pair in variables:
        q = sp.zeros(6)
        i, j = pair
        q[i, j] = 1
        q[j, i] = 1
        if i == j:
            q[i, i] = 1
        if pair == (0, 5):
            q[2, 3] = q[3, 2] = -1
        if pair == (1, 4):
            q[2, 3] = q[3, 2] = 1
        basis.append(q)
    return variables, basis


def direction(p: sp.Rational, q: sp.Rational) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    den = 1 + p * p + q * q
    n = sp.Matrix((2 * p / den, 2 * q / den, (1 - p * p - q * q) / den))
    k = sp.Matrix((1, n[0], n[1], n[2]))
    ez = sp.Matrix((0, 0, 1))
    e1s = n.cross(ez)
    e2s = n.cross(e1s)
    e1 = sp.Matrix((0, e1s[0], e1s[1], e1s[2]))
    e2 = sp.Matrix((0, e2s[0], e2s[1], e2s[2]))
    assert sp.simplify(dot(k, k)) == 0
    assert sp.simplify(dot(e1, k)) == 0
    assert sp.simplify(dot(e2, k)) == 0
    assert sp.simplify(dot(e1, e2)) == 0
    assert dot(e1, e1) > 0 and dot(e2, e2) > 0
    return k, e1, e2


def rows_for(pq: tuple[sp.Rational, sp.Rational], basis: list[sp.Matrix]) -> sp.Matrix:
    k, e1, e2 = direction(*pq)
    v1 = wedge(e1, k)
    v2 = wedge(e2, k)
    pairs = ((v1, v1), (v1, v2), (v2, v2))
    return sp.Matrix([[(left.T * q * right)[0] for q in basis] for left, right in pairs])


def constant_curvature_coordinates(
    variables: list[tuple[int, int]], basis: list[sp.Matrix]
) -> tuple[sp.Matrix, sp.Matrix]:
    q_const = sp.diag(-1, -1, -1, 1, 1, 1)
    coeffs = sp.Matrix([q_const[i, j] for i, j in variables])
    rebuilt = sp.zeros(6)
    for coefficient, element in zip(coeffs, basis):
        rebuilt += coefficient * element
    assert rebuilt == q_const
    return coeffs, q_const


def encode_matrix(m: sp.Matrix) -> list[list[str]]:
    return [[str(m[i, j]) for j in range(m.cols)] for i in range(m.rows)]


def exact_rank(m: sp.Matrix) -> int:
    return int(DomainMatrix.from_Matrix(m).rank())


def main() -> None:
    variables, basis = curvature_basis()
    blocks = [rows_for(pq, basis) for pq in TRAINING]
    cumulative = []
    for count in range(1, len(blocks) + 1):
        cumulative.append(exact_rank(sp.Matrix.vstack(*blocks[:count])))
    a_null = sp.Matrix.vstack(*blocks)
    domain_null = DomainMatrix.from_Matrix(a_null)
    nullspace_rows = domain_null.nullspace().to_Matrix()
    left_nullspace_rows = domain_null.transpose().nullspace().to_Matrix()
    kappa_coeffs, q_const = constant_curvature_coordinates(variables, basis)
    assert a_null * kappa_coeffs == sp.zeros(a_null.rows, 1)

    # Frozen timelike sectional datum: E=(0,1,0,0), U=(1,0,0,0).
    u = sp.Matrix((1, 0, 0, 0))
    e = sp.Matrix((0, 1, 0, 0))
    v_time = wedge(e, u)
    time_row = sp.Matrix([[(v_time.T * q * v_time)[0] for q in basis]])
    augmented = a_null.col_join(time_row)
    constant_time_value = (time_row * kappa_coeffs)[0]

    held_blocks = [rows_for(pq, basis) for pq in HELD_OUT]
    a_held = sp.Matrix.vstack(*held_blocks)
    null_rank = exact_rank(a_null)
    held_rank_increase = exact_rank(a_null.col_join(a_held)) - null_rank
    assert held_rank_increase == 0

    seed_coeffs = sp.Matrix([sp.Rational((i + 3) * (-1 if i % 3 == 0 else 1), i + 2) for i in range(20)])
    training_values = a_null * seed_coeffs
    augmented_system = a_null.row_join(training_values)
    rref_domain, pivots = DomainMatrix.from_Matrix(augmented_system).rref()
    rref = rref_domain.to_Matrix()
    coefficient_pivots = tuple(pivot for pivot in pivots if pivot < 20)
    assert len(coefficient_pivots) == 19 and 20 not in coefficient_pivots
    particular = sp.zeros(20, 1)
    for row_index, pivot_column in enumerate(coefficient_pivots):
        particular[pivot_column] = rref[row_index, 20]
    held_residual = sp.simplify(a_held * particular - a_held * seed_coeffs)
    held_prediction_exact = held_residual == sp.zeros(a_held.rows, 1)

    # Deterministic incompatible synthetic tide: perturb one valid entry until a syzygy detects it.
    incompatible_index = None
    incompatible_augmented_rank = None
    for index in range(a_null.rows):
        candidate = training_values.copy()
        candidate[index] += 1
        if exact_rank(a_null.row_join(candidate)) > null_rank:
            incompatible_index = index
            incompatible_augmented_rank = exact_rank(a_null.row_join(candidate))
            break
    assert incompatible_index is not None

    result = {
        "landing_candidate": "A_NULL_RANK_19_ONE_CONSTANT_CURVATURE_KERNEL__TIMELIKE_RANK_20",
        "whiteboard_pilot_disclosed": True,
        "bivector_order": [f"{i}{j}" for i, j in BIVECTORS],
        "variable_pairs": [[i, j] for i, j in variables],
        "bianchi_constraint": "Q[0,5]-Q[1,4]+Q[2,3]=0",
        "training_directions": [[str(p), str(q)] for p, q in TRAINING],
        "held_out_directions": [[str(p), str(q)] for p, q in HELD_OUT],
        "cumulative_null_ranks": cumulative,
        "null_map_shape": [a_null.rows, a_null.cols],
        "null_rank": null_rank,
        "nullity": nullspace_rows.rows,
        "left_nullity": left_nullspace_rows.rows,
        "constant_curvature_coordinates": [str(value) for value in kappa_coeffs],
        "kernel_generator": [str(value) for value in nullspace_rows.row(0)],
        "kernel_proportional_to_constant_curvature": bool(
            exact_rank(sp.Matrix.hstack(nullspace_rows.row(0).T, kappa_coeffs)) == 1
        ),
        "constant_curvature_matrix": encode_matrix(q_const),
        "timelike_row": [str(value) for value in time_row.row(0)],
        "constant_curvature_timelike_value": str(constant_time_value),
        "augmented_rank": exact_rank(augmented),
        "held_out_rank_increase": held_rank_increase,
        "held_out_prediction_exact": held_prediction_exact,
        "held_out_max_residual": "0" if held_prediction_exact else "nonzero",
        "synthetic_incompatible_perturbed_entry": incompatible_index,
        "synthetic_incompatible_augmented_rank": incompatible_augmented_rank,
        "syzygy_basis": [[str(value) for value in left_nullspace_rows.row(i)] for i in range(left_nullspace_rows.rows)],
        "production_matrix": encode_matrix(a_null),
        "python": sys.version,
        "platform": platform.platform(),
        "sympy": sp.__version__,
    }
    output = ROOT / "DERIVATION_RESULT.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {output.name}")
    print(f"cumulative ranks: {cumulative}")
    print(f"null rank/nullity/left-nullity: {null_rank}/{nullspace_rows.rows}/{left_nullspace_rows.rows}")
    print(f"timelike augmented rank: {exact_rank(augmented)}")
    print(f"held-out prediction exact: {held_prediction_exact}")


if __name__ == "__main__":
    main()
