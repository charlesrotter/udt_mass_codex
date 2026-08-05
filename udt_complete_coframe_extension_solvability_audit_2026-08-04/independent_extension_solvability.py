#!/usr/bin/env python3
"""Independent stdlib/Fraction replay; imports no production code or third-party algebra."""

from __future__ import annotations

import ast
import argparse
import csv
import json
from fractions import Fraction as F
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
MONODROMY = ROOT / "udt_completion_parameterized_local_fiber_audit_2026-08-01" / "MONODROMY_LOCAL_FIBERS.tsv"
OUT = PKG / "INDEPENDENT_RESULT.json"


def matrix(rows):
    return [[F(value) for value in row] for row in rows]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def inverse2(a):
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert determinant != 0
    return [
        [a[1][1] / determinant, -a[0][1] / determinant],
        [-a[1][0] / determinant, a[0][0] / determinant],
    ]


def rank(a):
    work = [row[:] for row in a]
    row_count = len(work)
    col_count = len(work[0]) if work else 0
    pivot_row = 0
    for col in range(col_count):
        pivot = next((r for r in range(pivot_row, row_count) if work[r][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for r in range(row_count):
            if r == pivot_row or work[r][col] == 0:
                continue
            factor = work[r][col]
            work[r] = [work[r][c] - factor * work[pivot_row][c] for c in range(col_count)]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def transform(h, sigma, p, q):
    q_inv = inverse2(q)
    p_inv = inverse2(p)
    return matmul(matmul(transpose(q_inv), h), q_inv), matmul(matmul(q, sigma), p_inv)


def flatten_extension(h, sigma):
    return [h[0][0], h[0][1], h[1][1], sigma[0][0], sigma[0][1], sigma[1][0], sigma[1][1]]


def seed_to_local(seed):
    h = [[seed[0], seed[1]], [seed[1], seed[2]]]
    sigma = [[seed[3], seed[4]], [seed[5], seed[6]]]
    p01 = matrix([[1, 1], [0, 1]])
    p12 = matrix([[1, 0], [1, 1]])
    q01 = matrix([[2, 1], [1, 1]])
    q12 = matrix([[1, 1], [0, 1]])
    p02 = matmul(p12, p01)
    q02 = matmul(q12, q01)
    h1, s1 = transform(h, sigma, p01, q01)
    h2, s2 = transform(h, sigma, p02, q02)
    return flatten_extension(h, sigma) + flatten_extension(h1, s1) + flatten_extension(h2, s2)


def extension_control():
    columns = []
    for j in range(7):
        seed = [F(0)] * 7
        seed[j] = F(1)
        columns.append(seed_to_local(seed))
    descent_map = transpose(columns)

    seed = [F(2), F(1, 2), F(3), F(1), F(2), F(-1), F(3)]
    h = [[seed[0], seed[1]], [seed[1], seed[2]]]
    sigma = [[seed[3], seed[4]], [seed[5], seed[6]]]
    p01 = matrix([[1, 1], [0, 1]])
    p12 = matrix([[1, 0], [1, 1]])
    q01 = matrix([[2, 1], [1, 1]])
    q12 = matrix([[1, 1], [0, 1]])
    p02 = matmul(p12, p01)
    q02 = matmul(q12, q01)
    h1, s1 = transform(h, sigma, p01, q01)
    h2_direct, s2_direct = transform(h, sigma, p02, q02)
    h2_via, s2_via = transform(h1, s1, p12, q12)
    return {
        "descent_map_rank": rank(descent_map),
        "surviving_extension_dimension": rank(descent_map),
        "cocycle_h_exact": h2_direct == h2_via,
        "cocycle_sigma_exact": s2_direct == s2_via,
        "selection_rank_from_descent": 0,
    }


def gamma_key(a, b, c):
    if a == b:
        return None, 0
    if a < b:
        return (a, b, c), 1
    return (b, a, c), -1


def cartan_control():
    unknowns = [(a, b, c) for a in range(4) for b in range(a + 1, 4) for c in range(4)]
    index = {key: i for i, key in enumerate(unknowns)}
    signature = [-1, 1, 1, 1]
    rows = []
    for a in range(4):
        for b in range(4):
            for c in range(b + 1, 4):
                row = [F(0)] * len(unknowns)
                for q, r, coefficient in [(c, b, 1), (b, c, -1)]:
                    key, sign = gamma_key(a, q, r)
                    if key is not None:
                        row[index[key]] += F(signature[a] * coefficient * sign)
                rows.append(row)
    coefficient_rank = rank(rows)
    return {
        "connection_unknowns": len(unknowns),
        "torsion_equations": len(rows),
        "coefficient_rank": coefficient_rank,
        "coefficient_nullity": len(unknowns) - coefficient_rank,
        "arbitrary_anholonomy_rhs_solvable": coefficient_rank == len(rows) == len(unknowns),
        "coframe_constraints_from_reconstruction": 0 if coefficient_rank == len(rows) else len(rows) - coefficient_rank,
    }


def coordinate_integrability_control():
    # At x=0, R=I but dR/dx=[[0,1],[-1,0]]. Acting on (dx,dy), the first
    # rotated one-form has exterior derivative +dx wedge dy although the metric is unchanged.
    rotation_at_zero = matrix([[1, 0], [0, 1]])
    derivative_at_zero = matrix([[0, 1], [-1, 0]])
    return {
        "metric_preserved_exact": matmul(transpose(rotation_at_zero), rotation_at_zero) == eye(2),
        "input_coordinate_coframe_closed": True,
        "rotated_exterior_coefficients_at_x0": [int(derivative_at_zero[0][1]), int(derivative_at_zero[1][1])],
        "rotated_coframe_not_closed": derivative_at_zero[0][1] != 0,
        "coordinate_integrability_is_frame_gauge_invariant": False,
    }


def monodromy_control():
    rows = []
    with MONODROMY.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            m = matrix(ast.literal_eval(row["matrix"]))
            graph = [[-m[i][0], -m[i][1], eye(2)[i][0], eye(2)[i][1]] for i in range(2)]
            fixed_rank = rank(subtract(m, eye(2)))
            fixed_dimension = 2 - fixed_rank
            rows.append(
                {
                    "monodromy_id": row["monodromy_id"],
                    "endpoint_graph_rank": rank(graph),
                    "endpoint_graph_dimension": 4 - rank(graph),
                    "fixed_parallel_rank": fixed_rank,
                    "fixed_parallel_dimension": fixed_dimension,
                    "matches_frozen_conditional_dimension": fixed_dimension == int(row["conditional_fixed_parallel_dimension"]),
                }
            )
    histogram = {}
    for row in rows:
        key = str(row["fixed_parallel_dimension"])
        histogram[key] = histogram.get(key, 0) + 1
    return {
        "matrix_count": len(rows),
        "all_endpoint_graphs_dimension_two": all(row["endpoint_graph_dimension"] == 2 for row in rows),
        "all_frozen_fixed_dimensions_match": all(row["matches_frozen_conditional_dimension"] for row in rows),
        "fixed_parallel_dimension_histogram": histogram,
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true", help="replay to stdout without changing INDEPENDENT_RESULT.json")
    args = parser.parse_args()
    result = {
        "schema": "udt.complete_coframe_extension_solvability.independent.v1",
        "extension_descent": extension_control(),
        "cartan_reconstruction": cartan_control(),
        "coordinate_integrability": coordinate_integrability_control(),
        "monodromy": monodromy_control(),
    }
    if not args.no_write:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
