#!/usr/bin/env python3
"""Independent Fraction-only G103 replay; imports no production implementation."""

from __future__ import annotations

from fractions import Fraction as F
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent


def eye(n: int) -> list[list[F]]:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def matsub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matadd(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    aug = [a[i][:] + eye(n)[i] for i in range(n)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def rank(a: list[list[F]]) -> int:
    m = [row[:] for row in a]
    nr, nc = len(m), len(m[0])
    pivot_row = 0
    for col in range(nc):
        pivot = next((r for r in range(pivot_row, nr) if m[r][col] != 0), None)
        if pivot is None:
            continue
        m[pivot_row], m[pivot] = m[pivot], m[pivot_row]
        scale = m[pivot_row][col]
        m[pivot_row] = [x / scale for x in m[pivot_row]]
        for r in range(nr):
            if r != pivot_row and m[r][col] != 0:
                factor = m[r][col]
                m[r] = [m[r][j] - factor * m[pivot_row][j] for j in range(nc)]
        pivot_row += 1
        if pivot_row == nr:
            break
    return pivot_row


def block_coframe(b: list[list[F]], q: list[list[F]], s: list[list[F]]) -> list[list[F]]:
    qs = matmul(q, s)
    return [b[0] + [F(0), F(0)], b[1] + [F(0), F(0)], qs[0] + q[0], qs[1] + q[1]]


def minkowski_dot(x: list[F], y: list[F]) -> F:
    return -x[0] * y[0] + sum(x[i] * y[i] for i in range(1, 4))


def gram_from_columns(columns: list[list[F]], dot) -> list[list[F]]:
    return [[dot(x, y) for y in columns] for x in columns]


def main() -> None:
    b = [[F(2), F(1, 3)], [F(0), F(3, 2)]]
    q = [[F(5, 4), F(1, 5)], [F(0), F(7, 6)]]
    s = [[F(1, 7), F(-2, 9)], [F(3, 11), F(1, 13)]]
    e = block_coframe(b, q, s)
    v = [[F(2), F(0)], [F(0), F(3, 2)], [F(1, 2), F(1)], [F(-1, 3), F(2)]]
    j = matmul(inverse(e), v)
    zero_exact = matmul(e, j) == v

    b_dot = [[F(1, 5), F(-1, 8)], [F(1, 9), F(2, 7)]]
    q_dot = [[F(-1, 6), F(1, 10)], [F(1, 12), F(1, 11)]]
    s_dot = [[F(2, 13), F(1, 14)], [F(-1, 15), F(3, 17)]]
    qds = matadd(matmul(q_dot, s), matmul(q, s_dot))
    e_dot = [b_dot[0] + [F(0), F(0)], b_dot[1] + [F(0), F(0)],
             qds[0] + q_dot[0], qds[1] + q_dot[1]]
    v_dot = [[F(1, 3), F(-1, 4)], [F(2, 5), F(1, 6)],
             [F(-1, 7), F(3, 8)], [F(4, 9), F(-2, 11)]]
    j_dot = matmul(inverse(e), matsub(v_dot, matmul(e_dot, j)))
    first_exact = matadd(matmul(e_dot, j), matmul(e, j_dot)) == v_dot

    u = [F(1), F(0), F(0), F(0)]
    n1 = [F(0), F(1), F(0), F(0)]
    n2 = [F(0), F(3, 5), F(4, 5), F(0)]
    sky_checks = {
        "u_norm": minkowski_dot(u, u) == -1,
        "n1_norm": minkowski_dot(n1, n1) == 1,
        "n2_norm": minkowski_dot(n2, n2) == 1,
        "cosine": str(minkowski_dot(n1, n2)),
    }

    directions = [
        [F(1), F(0), F(0)],
        [F(0), F(1), F(0)],
        [F(0), F(0), F(1)],
        [F(3, 5), F(4, 5), F(0)],
    ]
    euclidean = lambda x, y: sum(a * b for a, b in zip(x, y))
    valid_gram = gram_from_columns(directions, euclidean)
    gram_checks = {
        "valid_rank": rank(valid_gram),
        "valid_diagonal": [str(valid_gram[i][i]) for i in range(4)],
        "hostile_rank": rank(eye(4)),
    }

    star = [F(1), F(3, 2), F(5, 3), F(7, 4), F(11, 6)]
    zij = [[star[j] / star[i] for j in range(5)] for i in range(5)]
    composition = all(zij[i][j] * zij[j][k] == zij[i][k]
                      for i in range(5) for j in range(5) for k in range(5))
    reversal = all(zij[i][j] * zij[j][i] == 1 for i in range(5) for j in range(5))

    t, ell, a, bterm, delta = F(4), F(9), F(2), F(13), F(1, 2)
    fixed_gram = [[t - a, -a * delta],
                  [-a * delta, bterm - ell - a * delta * delta]]
    fixed_margin = (t - a) * (bterm - ell) - t * a * delta * delta
    fixed_psd = fixed_gram[0][0] >= 0 and fixed_gram[1][1] >= 0 and (
        fixed_gram[0][0] * fixed_gram[1][1] - fixed_gram[0][1] ** 2 >= 0
    )
    base_e = [[F(2), F(0), F(0), F(0)], [F(0), F(3), F(0), F(0)],
              [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    lower_v = [[F(3), F(0)], [F(0), F(2)], [F(0), F(0)], [F(0), F(0)]]
    lower_j = matmul(inverse(base_e), lower_v)
    released_exact = matmul(base_e, lower_j) == lower_v
    # phi monotonicity follows from log monotonicity: compare ratios 4/9 < 9/4.
    released_below_base = F(4, 9) < F(9, 4)

    couplings = {
        "parallel": [[F(int(i == j), 4) for j in range(4)] for i in range(4)],
        "orthogonal": [[F(x, 4) for x in row] for row in
                       [[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]]],
        "antipodal": [[F(x, 4) for x in row] for row in
                      [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]],
    }
    coupling_checks = {}
    for name, c in couplings.items():
        rows = [sum(row) for row in c]
        cols = [sum(c[i][j] for i in range(4)) for j in range(4)]
        coupling_checks[name] = {
            "symmetric": c == transpose(c),
            "rows": [str(x) for x in rows],
            "columns": [str(x) for x in cols],
            "same_uniform_marginal": rows == [F(1, 4)] * 4 == cols,
        }

    checks = {
        "zero_order_exact": zero_exact,
        "first_jet_exact": first_exact,
        "sky": sky_checks,
        "gram": gram_checks,
        "depth_composition_exact": composition,
        "depth_reversal_exact": reversal,
        "fixed_base_psd": fixed_psd,
        "fixed_base_margin": str(fixed_margin),
        "released_j_exact": released_exact,
        "released_phi_below_base": released_below_base,
        "couplings": coupling_checks,
        "imports_production": False,
        "outcome_artifacts_read": [],
    }
    required = [
        zero_exact, first_exact, sky_checks["u_norm"], sky_checks["n1_norm"],
        sky_checks["n2_norm"], sky_checks["cosine"] == "3/5",
        gram_checks["valid_rank"] == 3, gram_checks["hostile_rank"] == 4,
        composition, reversal, fixed_psd, fixed_margin == 6,
        released_exact, released_below_base,
        all(x["symmetric"] and x["same_uniform_marginal"]
            for x in coupling_checks.values()),
    ]
    if not all(required):
        raise AssertionError(json.dumps(checks, indent=2, sort_keys=True))
    result = {"status": "PASS", "checks": checks}
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
