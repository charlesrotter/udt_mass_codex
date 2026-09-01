#!/usr/bin/env python3
"""Dependency-free independent reconstruction for the bounded G311 result."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


Q = Fraction
N = 4
SIG = (-1, 1, 1, 1)
# Deliberately differs from the production component ordering.
SYMMETRIC_COMPONENTS = (
    (0, 0), (1, 1), (2, 2), (3, 3),
    (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
)


def minkowski_dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum(Q(SIG[i]) * left[i] * right[i] for i in range(N))


def reciprocal_shape(u: tuple[Q, ...], n: tuple[Q, ...]) -> list[list[Q]]:
    assert minkowski_dot(u, u) == -1
    assert minkowski_dot(n, n) == 1
    assert minkowski_dot(u, n) == 0
    u_cov = tuple(Q(SIG[i]) * u[i] for i in range(N))
    n_cov = tuple(Q(SIG[i]) * n[i] for i in range(N))
    return [
        [2 * (u_cov[i] * u_cov[j] + n_cov[i] * n_cov[j]) for j in range(N)]
        for i in range(N)
    ]


def independent_pair_family() -> list[list[list[Q]]]:
    basis = [tuple(Q(1) if i == j else Q(0) for i in range(N)) for j in range(N)]
    pairs: list[tuple[tuple[Q, ...], tuple[Q, ...]]] = []
    for spatial in (1, 2, 3):
        pairs.append((basis[0], basis[spatial]))
    for first, second in ((1, 2), (1, 3), (2, 3)):
        n = tuple(Q(4, 5) * basis[first][k] + Q(3, 5) * basis[second][k] for k in range(N))
        pairs.append((basis[0], n))
    # A different rational boost family from the production implementation.
    for spatial in (1, 2, 3):
        u = tuple(Q(13, 5) * basis[0][k] + Q(12, 5) * basis[spatial][k] for k in range(N))
        n = tuple(Q(12, 5) * basis[0][k] + Q(13, 5) * basis[spatial][k] for k in range(N))
        pairs.append((u, n))
    return [reciprocal_shape(u, n) for u, n in pairs]


def row_reduce(matrix: list[list[Q]]) -> tuple[list[list[Q]], list[int]]:
    work = [row[:] for row in matrix]
    if not work:
        return work, []
    pivot_columns: list[int] = []
    next_row = 0
    for column in range(len(work[0])):
        pivot = next((r for r in range(next_row, len(work)) if work[r][column]), None)
        if pivot is None:
            continue
        work[next_row], work[pivot] = work[pivot], work[next_row]
        divisor = work[next_row][column]
        work[next_row] = [value / divisor for value in work[next_row]]
        for r in range(len(work)):
            if r == next_row or not work[r][column]:
                continue
            multiplier = work[r][column]
            work[r] = [
                work[r][c] - multiplier * work[next_row][c]
                for c in range(len(work[r]))
            ]
        pivot_columns.append(column)
        next_row += 1
        if next_row == len(work):
            break
    return work, pivot_columns


def matrix_rank(matrix: list[list[Q]]) -> int:
    return len(row_reduce(matrix)[1])


def kernel_basis(matrix: list[list[Q]]) -> list[list[Q]]:
    reduced, pivots = row_reduce(matrix)
    free = [column for column in range(len(matrix[0])) if column not in pivots]
    result: list[list[Q]] = []
    for free_column in free:
        vector = [Q(0) for _ in range(len(matrix[0]))]
        vector[free_column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        result.append(vector)
    return result


def flattened_shape(tensor: list[list[Q]]) -> list[Q]:
    return [tensor[i][j] for i, j in SYMMETRIC_COMPONENTS]


def balance_functional(tensor: list[list[Q]]) -> list[Q]:
    return [
        Q(1 if i == j else 2) * Q(SIG[i] * SIG[j]) * tensor[i][j]
        for i, j in SYMMETRIC_COMPONENTS
    ]


def inverse_diagonal(metric: list[list[Q]]) -> list[list[Q]]:
    inverse = [[Q(0) for _ in range(N)] for _ in range(N)]
    for i in range(N):
        assert metric[i][i] and all(metric[i][j] == 0 for j in range(N) if j != i)
        inverse[i][i] = 1 / metric[i][i]
    return inverse


def independent_countermetric_at_origin() -> tuple[list[list[Q]], Q, int]:
    """Derive curvature at t=0 directly from exact metric two-jets.

    The metric is diag(-1, exp(2 t^2), exp(2 t^2), exp(2 t^2)), corresponding to b=1.
    Its first metric jet vanishes at t=0 and its only nonzero second jets are
    d_t d_t g_ii=4 for spatial i. Christoffel derivatives and curvature are reconstructed from
    those raw jets rather than importing the production curvature values.
    """

    g = [[Q(0) for _ in range(N)] for _ in range(N)]
    for i, sign in enumerate(SIG):
        g[i][i] = Q(sign)
    g_inv = inverse_diagonal(g)

    dg = [
        [[Q(0) for _ in range(N)] for _ in range(N)]
        for _ in range(N)
    ]
    # d2g[alpha][beta][mu][nu]
    d2g = [
        [
            [[Q(0) for _ in range(N)] for _ in range(N)]
            for _ in range(N)
        ]
        for _ in range(N)
    ]
    # exp(2 t^2)=1+2 t^2+O(t^4), hence the exact second derivative at zero is 2!*2=4.
    spatial_metric_t2_coefficient = Q(2)
    for spatial in (1, 2, 3):
        d2g[0][0][spatial][spatial] = 2 * spatial_metric_t2_coefficient

    # Gamma and dGamma are evaluated at the origin. Gamma vanishes because dg=0.
    gamma = [
        [[Q(0) for _ in range(N)] for _ in range(N)]
        for _ in range(N)
    ]
    for rho in range(N):
        for mu in range(N):
            for nu in range(N):
                gamma[rho][mu][nu] = Q(1, 2) * sum(
                    g_inv[rho][lam]
                    * (dg[mu][lam][nu] + dg[nu][lam][mu] - dg[lam][mu][nu])
                    for lam in range(N)
                )
    assert all(gamma[rho][mu][nu] == 0 for rho in range(N) for mu in range(N) for nu in range(N))

    dgamma = [
        [
            [
                [Q(0) for _ in range(N)]
                for _ in range(N)
            ]
            for _ in range(N)
        ]
        for _ in range(N)
    ]
    for alpha in range(N):
        for rho in range(N):
            for mu in range(N):
                for nu in range(N):
                    dgamma[alpha][rho][mu][nu] = Q(1, 2) * sum(
                        g_inv[rho][lam]
                        * (
                            d2g[alpha][mu][lam][nu]
                            + d2g[alpha][nu][lam][mu]
                            - d2g[alpha][lam][mu][nu]
                        )
                        for lam in range(N)
                    )

    # R^rho_{ sigma mu nu} = d_mu Gamma^rho_{nu sigma} - d_nu Gamma^rho_{mu sigma}
    # at this point because every Gamma vanishes.
    riemann_up = [
        [
            [
                [Q(0) for _ in range(N)]
                for _ in range(N)
            ]
            for _ in range(N)
        ]
        for _ in range(N)
    ]
    for rho in range(N):
        for sigma in range(N):
            for mu in range(N):
                for nu in range(N):
                    riemann_up[rho][sigma][mu][nu] = (
                        dgamma[mu][rho][nu][sigma] - dgamma[nu][rho][mu][sigma]
                    )

    ricci = [[Q(0) for _ in range(N)] for _ in range(N)]
    for sigma in range(N):
        for nu in range(N):
            ricci[sigma][nu] = sum(
                riemann_up[rho][sigma][rho][nu] for rho in range(N)
            )
    scalar = sum(g_inv[i][j] * ricci[i][j] for i in range(N) for j in range(N))
    tracefree = [
        [ricci[i][j] - scalar * g[i][j] / 4 for j in range(N)]
        for i in range(N)
    ]
    assert ricci == [
        [Q(-6), Q(0), Q(0), Q(0)],
        [Q(0), Q(2), Q(0), Q(0)],
        [Q(0), Q(0), Q(2), Q(0)],
        [Q(0), Q(0), Q(0), Q(2)],
    ]
    assert scalar == 12
    assert tracefree == [
        [Q(-3), Q(0), Q(0), Q(0)],
        [Q(0), Q(-1), Q(0), Q(0)],
        [Q(0), Q(0), Q(-1), Q(0)],
        [Q(0), Q(0), Q(0), Q(-1)],
    ]

    riemann_down = [
        [
            [
                [sum(g[a][rho] * riemann_up[rho][bb][c][d] for rho in range(N)) for d in range(N)]
                for c in range(N)
            ]
            for bb in range(N)
        ]
        for a in range(N)
    ]
    nonzero_weyl: list[tuple[int, int, int, int, Q]] = []
    for a in range(N):
        for bb in range(N):
            for c in range(N):
                for d in range(N):
                    value = (
                        riemann_down[a][bb][c][d]
                        - Q(1, 2)
                        * (
                            g[a][c] * ricci[d][bb]
                            - g[a][d] * ricci[c][bb]
                            - g[bb][c] * ricci[d][a]
                            + g[bb][d] * ricci[c][a]
                        )
                        + scalar
                        * (g[a][c] * g[d][bb] - g[a][d] * g[c][bb])
                        / 6
                    )
                    if value:
                        nonzero_weyl.append((a, bb, c, d, value))
    assert not nonzero_weyl
    return tracefree, scalar, len(nonzero_weyl)


def run() -> dict[str, object]:
    shapes = independent_pair_family()
    shape_rank = matrix_rank([flattened_shape(shape) for shape in shapes])
    assert shape_rank == 9
    assert all(
        sum(Q(SIG[i]) * shape[i][i] for i in range(N)) == 0
        for shape in shapes
    )

    balance = [balance_functional(shape) for shape in shapes]
    annihilator = kernel_basis(balance)
    assert matrix_rank(balance) == 9
    assert len(annihilator) == 1
    metric_vector = [Q(SIG[i]) if i == j else Q(0) for i, j in SYMMETRIC_COMPONENTS]
    assert matrix_rank([annihilator[0], metric_vector]) == 1

    tracefree_ricci, scalar, weyl_count = independent_countermetric_at_origin()
    assert any(value for row in tracefree_ricci for value in row)
    assert scalar == 12 and weyl_count == 0

    result = {
        "independent_method": (
            "stdlib_fraction_rref_plus_exact_metric_two_jet_christoffel_riemann_weyl"
        ),
        "standard_library_only": True,
        "shares_production_imports": False,
        "reciprocal_shape_rank": shape_rank,
        "balance_rank": matrix_rank(balance),
        "annihilator_nullity": len(annihilator),
        "annihilator_is_metric_line": True,
        "flrw_evaluation": "b=1,t=0",
        "flrw_scalar_curvature": int(scalar),
        "flrw_tracefree_ricci": [
            str(tracefree_ricci[i][i]) for i in range(N)
        ],
        "flrw_weyl_component_count_nonzero": weyl_count,
        "response_architecture_counterexample_verified": True,
        "conditional_g301_phase_dof_count": 12 - 4 - 4,
        "conditional_g301_configuration_dof_count": (12 - 4 - 4) // 2,
        "checks": 14,
        "verdict": "PASS",
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
