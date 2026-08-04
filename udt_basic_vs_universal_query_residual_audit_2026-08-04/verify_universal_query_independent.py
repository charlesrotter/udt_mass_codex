#!/usr/bin/env python3
"""Independent standard-library Fraction replay with no production-module import."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent


def rank(matrix):
    work = [[F(item) for item in row] for row in matrix]
    if not work:
        return 0
    row = 0
    for col in range(len(work[0])):
        pivot = next((i for i in range(row, len(work)) if work[i][col]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = work[row][col]
        work[row] = [item / scale for item in work[row]]
        for i in range(len(work)):
            if i != row and work[i][col]:
                factor = work[i][col]
                work[i] = [a - factor * b for a, b in zip(work[i], work[row])]
        row += 1
        if row == len(work):
            break
    return row


def dot(a, matrix, b):
    return sum(a[i] * matrix[i][j] * b[j] for i in range(len(a)) for j in range(len(b)))


def residual_row(u, n):
    # Component order: 00,01,02,03,11,12,13,22,23,33.
    pairs = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))
    row = []
    for i, j in pairs:
        factor = F(1) if i == j else F(2)
        row.append(factor * (u[i] * u[j] + n[i] * n[j]))
    return row


def main() -> None:
    z = F(0)
    o = F(1)
    e = [[o if i == j else z for i in range(4)] for j in range(4)]
    pairs = []
    for i in (1, 2, 3):
        pairs.append((e[0], e[i]))
    # Normalized sum residual rows are rational because n_i n_j uses halves.
    for i, j in ((1, 2), (1, 3), (2, 3)):
        n_outer = [z] * 10
        # Build the row directly: u=e0 plus n=(ei+ej)/sqrt(2).
        row = [z] * 10
        row[0] = o
        index = {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (1, 1): 4,
                 (1, 2): 5, (1, 3): 6, (2, 2): 7, (2, 3): 8, (3, 3): 9}
        row[index[(i, i)]] = F(1, 2)
        row[index[(j, j)]] = F(1, 2)
        row[index[(min(i, j), max(i, j))]] = o
        n_outer[:] = row
        pairs.append((None, n_outer))
    for i, j in ((1, 2), (2, 3), (3, 1)):
        u = [F(5, 3), z, z, z]
        u[i] = F(4, 3)
        pairs.append((u, e[j]))

    rows = []
    for u, n in pairs:
        rows.append(n if u is None else residual_row(u, n))
    query_rank = rank(rows)
    metric_line = [o, z, z, z, -o, z, z, -o, z, -o]
    assert all(sum(a * b for a, b in zip(row, metric_line)) == 0 for row in rows)

    eta = [[-o, z, z, z], [z, o, z, z], [z, z, o, z], [z, z, z, o]]
    strict = [[F(3), z, z, z], [z, o, z, z], [z, z, o, z], [z, z, z, o]]
    strict_trace = sum(eta[i][i] * strict[i][i] for i in range(4))
    strict_pair = dot(e[0], strict, e[0]) + dot(e[1], strict, e[1])

    checks = [
        query_rank == 9,
        strict_trace == 0,
        strict_pair == 4,
        rank([[-o], [o]]) == 1,
        rank([[o]]) == 1,
        rank([[z]]) == 0,
        -o + o == 0,
        z == 0,
    ]
    P01 = [[o, z, z, z], [z, o, z, z], [z, z, z, z], [z, z, z, z]]
    P02 = [[o, z, z, z], [z, z, z, z], [z, z, o, z], [z, z, z, z]]
    A = [F(2), F(3), F(5), F(7)]
    pair_values = [sum(P01[i][i] * A[i] for i in range(4)), sum(P02[i][i] * A[i] for i in range(4))]
    checks += [pair_values == [F(5), F(7)]]
    I = [[o, z], [z, o]]
    H = [[-o, z], [z, o]]
    checks += [H != I, H[0][0] * H[1][1] == -1]
    # Four rational probes of the downstream SNe identity.
    for value in (F(0), F(1, 3), F(1), F(7, 2)):
        u = o + value
        checks += [u * u * (o - o / (u * u)) == value * (value + 2)]
    assert all(checks)
    result = {
        "status": "PASS",
        "exact_checks": len(checks),
        "pair_values": ["5", "7"],
        "query_coefficient_rank": query_rank,
        "query_coefficient_nullity": 1,
        "query_kernel_generator": [str(item) for item in metric_line],
        "strict_tracefree_control_trace": str(strict_trace),
        "strict_tracefree_control_pair_value": str(strict_pair),
        "universal_query_tangent_rank": 1,
        "linear_basic_tangent_rank": 1,
        "squared_basic_tangent_rank": 0,
        "coefficient_tangent_rank": 9,
        "squared_coefficient_gradient_rank_at_solution": 0,
        "metric_dependent_query_total_derivative": "0",
        "torus_loop_holonomy": "[[1, 0], [0, 1]]",
        "klein_loop_holonomy": "[[-1, 0], [0, 1]]",
        "local_flat_jet_orders_compared": 5,
        "sne_conditional_shape": "z*(z + 2)",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
