#!/usr/bin/env python3
"""Independent standard-library exact-rational replay for G227."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BIV = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
TRAINING = (
    (F(9), F(-1, 2)), (F(5, 4), F(-2, 9)), (F(-1, 7), F(5, 3)),
    (F(-1), F(-1)), (F(4, 9), F(-2)), (F(-6, 7), F(6)),
    (F(1, 6), F(-7, 9)), (F(5, 8), F(1, 4)), (F(1), F(-5, 6)),
)
HELD = ((F(2, 7), F(3, 5)), (F(-3, 4), F(1, 8)), (F(7, 6), F(-2, 5)), (F(-5, 9), F(-4, 7)))


def matrix_rank(rows: list[list[F]]) -> int:
    a = [row[:] for row in rows]
    if not a:
        return 0
    rank = 0
    columns = len(a[0])
    for column in range(columns):
        pivot = next((r for r in range(rank, len(a)) if a[r][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][column]
        a[rank] = [value / scale for value in a[rank]]
        for row in range(len(a)):
            if row != rank and a[row][column]:
                factor = a[row][column]
                a[row] = [x - factor * y for x, y in zip(a[row], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def q_basis() -> tuple[list[tuple[int, int]], list[list[list[F]]]]:
    variables = [(i, j) for i in range(6) for j in range(i, 6) if (i, j) != (2, 3)]
    basis = []
    for pair in variables:
        q = [[F(0) for _ in range(6)] for _ in range(6)]
        i, j = pair
        q[i][j] = q[j][i] = F(1)
        if pair == (0, 5):
            q[2][3] = q[3][2] = F(-1)
        elif pair == (1, 4):
            q[2][3] = q[3][2] = F(1)
        basis.append(q)
    return variables, basis


def cross(a: tuple[F, F, F], b: tuple[F, F, F]) -> tuple[F, F, F]:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def wedge(a: tuple[F, ...], b: tuple[F, ...]) -> list[F]:
    return [a[i]*b[j]-a[j]*b[i] for i, j in BIV]


def bilinear(left: list[F], q: list[list[F]], right: list[F]) -> F:
    return sum(left[i] * q[i][j] * right[j] for i in range(6) for j in range(6))


def block(pq: tuple[F, F], basis: list[list[list[F]]]) -> list[list[F]]:
    p, q = pq
    den = F(1) + p*p + q*q
    n = (2*p/den, 2*q/den, (1-p*p-q*q)/den)
    assert sum(x*x for x in n) == 1
    e1s = cross(n, (F(0), F(0), F(1)))
    e2s = cross(n, e1s)
    assert sum(n[i]*e1s[i] for i in range(3)) == 0
    assert sum(n[i]*e2s[i] for i in range(3)) == 0
    k = (F(1), *n)
    e1 = (F(0), *e1s)
    e2 = (F(0), *e2s)
    v1, v2 = wedge(e1, k), wedge(e2, k)
    return [[bilinear(x, qmat, y) for qmat in basis] for x, y in ((v1, v1), (v1, v2), (v2, v2))]


def mat_vec(rows: list[list[F]], vector: list[F]) -> list[F]:
    return [sum(x*y for x, y in zip(row, vector)) for row in rows]


def main() -> None:
    variables, basis = q_basis()
    blocks = [block(pq, basis) for pq in TRAINING]
    cumulative = [matrix_rank([row for group in blocks[:n] for row in group]) for n in range(1, 10)]
    null_rows = [row for group in blocks for row in group]
    constant = [F(-1) if pair in ((0, 0), (1, 1), (2, 2)) else F(1) if pair in ((3, 3), (4, 4), (5, 5)) else F(0) for pair in variables]
    constant_annihilated = all(value == 0 for value in mat_vec(null_rows, constant))

    u = (F(1), F(0), F(0), F(0))
    e = (F(0), F(1), F(0), F(0))
    vt = wedge(e, u)
    time_row = [bilinear(vt, qmat, vt) for qmat in basis]
    augmented_rank = matrix_rank(null_rows + [time_row])
    held_rows = [row for pq in HELD for row in block(pq, basis)]
    held_rank_increase = matrix_rank(null_rows + held_rows) - matrix_rank(null_rows)

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    production_rows = [[F(value) for value in row] for row in production["production_matrix"]]
    matrix_match = production_rows == null_rows
    result = {
        "implementation": "standard-library Fraction with independent builders and elimination",
        "cumulative_null_ranks": cumulative,
        "null_rank": matrix_rank(null_rows),
        "constant_curvature_annihilated": constant_annihilated,
        "timelike_constant_value": str(sum(x*y for x, y in zip(time_row, constant))),
        "augmented_rank": augmented_rank,
        "held_out_rank_increase": held_rank_increase,
        "production_matrix_exact_match": matrix_match,
        "pass": cumulative == [3,6,9,12,15,16,17,18,19]
        and constant_annihilated and augmented_rank == 20 and held_rank_increase == 0 and matrix_match,
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

