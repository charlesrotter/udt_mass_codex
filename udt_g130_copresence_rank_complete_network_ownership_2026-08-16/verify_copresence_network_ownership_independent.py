#!/usr/bin/env python3
"""Independent stdlib/Fraction replay of G130 load-bearing algebra."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def design_row(v: tuple[int, ...], w: tuple[int, ...]) -> list[Fraction]:
    row = [Fraction(v[i] * w[i]) for i in range(4)]
    row.extend(
        Fraction(v[i] * w[j] + v[j] * w[i])
        for i, j in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    )
    return row


def matrix_for(rulers: list[tuple[int, int, int]]) -> list[list[Fraction]]:
    clock = (1, 0, 0, 0)
    rows: list[list[Fraction]] = []
    for xyz in rulers:
        ruler = (0, *xyz)
        rows.extend((design_row(clock, clock), design_row(clock, ruler), design_row(ruler, ruler)))
    return rows


def rank(matrix: list[list[Fraction]]) -> int:
    a = [row[:] for row in matrix]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    pivot_row = 0
    for col in range(n):
        pivot = next((row for row in range(pivot_row, m) if a[row][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [value / scale for value in a[pivot_row]]
        for row in range(m):
            if row != pivot_row and a[row][col]:
                factor = a[row][col]
                a[row] = [x - factor * y for x, y in zip(a[row], a[pivot_row])]
        pivot_row += 1
        if pivot_row == m:
            break
    return pivot_row


def inverse_diagonal(diagonal: list[Fraction]) -> list[list[Fraction]]:
    return [
        [Fraction(1, diagonal[i]) if i == j else Fraction(0) for j in range(4)]
        for i in range(4)
    ]


def independent_scalar_curvature_at_r1_equator(s: Fraction) -> Fraction:
    """Compute R from exact metric value, first jet, and second jet without SymPy."""
    n = 4
    g = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    diagonal = [-s, Fraction(1, s), Fraction(1), Fraction(1)]
    for i, value in enumerate(diagonal):
        g[i][i] = value
    inv = inverse_diagonal(diagonal)

    dg = [[[Fraction(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    # dg[k][i][j] = partial_k g_ij at r=1, theta=pi/2.
    dg[1][2][2] = Fraction(2)
    dg[1][3][3] = Fraction(2)

    ddg = [[[[Fraction(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    # ddg[k][ell][i][j].
    ddg[1][1][2][2] = Fraction(2)
    ddg[1][1][3][3] = Fraction(2)
    ddg[2][2][3][3] = Fraction(-2)

    dinv = [[[Fraction(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dinv[k][i][j] = -sum(
                    inv[i][a] * dg[k][a][b] * inv[b][j]
                    for a in range(n) for b in range(n)
                )

    gamma = [[[Fraction(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    dgamma = [[[[Fraction(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for upper in range(n):
        for i in range(n):
            for j in range(n):
                gamma[upper][i][j] = Fraction(1, 2) * sum(
                    inv[upper][ell]
                    * (dg[i][ell][j] + dg[j][ell][i] - dg[ell][i][j])
                    for ell in range(n)
                )
                for k in range(n):
                    dgamma[k][upper][i][j] = Fraction(1, 2) * sum(
                        dinv[k][upper][ell]
                        * (dg[i][ell][j] + dg[j][ell][i] - dg[ell][i][j])
                        + inv[upper][ell]
                        * (
                            ddg[k][i][ell][j]
                            + ddg[k][j][ell][i]
                            - ddg[k][ell][i][j]
                        )
                        for ell in range(n)
                    )

    ricci = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            ricci[i][j] = sum(
                dgamma[k][k][i][j]
                - dgamma[j][k][i][k]
                + sum(
                    gamma[k][k][ell] * gamma[ell][i][j]
                    - gamma[k][j][ell] * gamma[ell][i][k]
                    for ell in range(n)
                )
                for k in range(n)
            )
    return sum(inv[i][j] * ricci[i][j] for i in range(n) for j in range(n))


def main() -> None:
    axial = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    complete = axial + [(1, 1, 0), (1, 0, 1), (0, 1, 1)]

    exists = (True, False)
    law = (True, False)
    conditional = all((not e) or l for e, l in zip(exists, law))
    total = all(exists)

    potential_a = (Fraction(0), Fraction(1, 3), Fraction(2, 5))
    potential_b = (Fraction(0), Fraction(2, 3), Fraction(-1, 7))

    def edges(potential: tuple[Fraction, ...]) -> dict[tuple[int, int], Fraction]:
        return {
            (i, j): potential[j] - potential[i]
            for i in range(len(potential)) for j in range(len(potential))
        }

    def edge_laws(edge: dict[tuple[int, int], Fraction]) -> bool:
        return all(
            edge[i, j] == -edge[j, i]
            and edge[i, j] + edge[j, k] == edge[i, k]
            for i in range(3) for j in range(3) for k in range(3)
        )

    edge_a, edge_b = edges(potential_a), edges(potential_b)

    positive_scalar = independent_scalar_curvature_at_r1_equator(Fraction(1, 4))
    negative_scalar = independent_scalar_curvature_at_r1_equator(Fraction(4))
    h0 = ((Fraction(-1, 4), Fraction(0)), (Fraction(0), Fraction(4)))
    h1 = ((Fraction(-4), Fraction(0)), (Fraction(0), Fraction(1, 4)))

    checks = {
        "independent_conditional_not_total": conditional and not total,
        "independent_composition_allows_distinct_complete_depth_networks": (
            edge_laws(edge_a) and edge_laws(edge_b) and edge_a != edge_b
        ),
        "independent_one_plane_rank_three": rank(matrix_for(axial[:1])) == 3,
        "independent_axial_rank_seven": rank(matrix_for(axial)) == 7,
        "independent_complete_rank_ten": rank(matrix_for(complete)) == 10,
        "independent_both_pair_determinants_minus_one": (
            h0[0][0] * h0[1][1] == -1 and h1[0][0] * h1[1][1] == -1
        ),
        "independent_pair_values_differ": h0 != h1,
        "independent_positive_depth_scalar_three_halves": positive_scalar == Fraction(3, 2),
        "independent_negative_depth_scalar_minus_six": negative_scalar == -6,
        "independent_nonisometric_countermodel": positive_scalar != negative_scalar,
    }
    if not all(checks.values()):
        raise SystemExit(f"failed independent checks: {[k for k, v in checks.items() if not v]}")
    result = {
        "status": "PASS",
        "landing": "COPRESENCE_DENOTES_EVENT_COMEMBERSHIP_IN_SUPPLIED_S__RECIPROCITY_OWNS_LAW_SCHEMA__RANK_COMPLETE_NETWORK_VALUES_OPEN",
        "checks": checks,
        "independent_check_count": len(checks),
        "scalar_s_quarter": str(positive_scalar),
        "scalar_s_four": str(negative_scalar),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
