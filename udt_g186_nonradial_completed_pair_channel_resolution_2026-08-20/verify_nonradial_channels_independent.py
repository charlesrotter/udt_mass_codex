#!/usr/bin/env python3
"""Independent exact-Fraction replay for G186; imports no production code."""

from __future__ import annotations

from fractions import Fraction as F
import json
import random


TRIALS = 20_000
SEED = 1860820


def mmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b, sign=1):
    return [[a[i][j] + sign * b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def rank(matrix):
    a = [row[:] for row in matrix]
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((i for i in range(pivot_row, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [x / scale for x in a[pivot_row]]
        for i in range(rows):
            if i != pivot_row and a[i][col]:
                factor = a[i][col]
                a[i] = [a[i][j] - factor * a[pivot_row][j] for j in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def independent_columns(matrix, needed=2):
    chosen = []
    for j in range(len(matrix[0])):
        candidate = chosen + [[matrix[i][j] for i in range(len(matrix))]]
        test = transpose(candidate)
        if rank(test) > len(chosen):
            chosen = candidate
        if len(chosen) == needed:
            return chosen
    raise AssertionError("projector image did not supply two independent columns")


def direct_h(p, r, v, w00, w01, w10, w11):
    gdiag = [-1 / p, p, r * r, r * r]
    j = [[F(1), F(0)], [F(0), v], [w00, w10], [w01, w11]]
    h = [[sum(gdiag[k] * j[k][i] * j[k][q] for k in range(4))
          for q in range(2)] for i in range(2)]
    return gdiag, j, h


def projector(gdiag, j, h):
    det = h[0][0] * h[1][1] - h[0][1] * h[1][0]
    hinv = [[h[1][1] / det, -h[0][1] / det],
            [-h[1][0] / det, h[0][0] / det]]
    jt_g = [[j[k][i] * gdiag[k] for k in range(4)] for i in range(2)]
    correction = mmul(mmul(j, hinv), jt_g)
    identity = [[F(int(i == q)) for q in range(4)] for i in range(4)]
    return madd(identity, correction, sign=-1)


def assert_projector(gdiag, j, proj):
    zero42 = [[F(0), F(0)] for _ in range(4)]
    zero44 = [[F(0) for _ in range(4)] for _ in range(4)]
    assert mmul(proj, j) == zero42
    assert madd(mmul(proj, proj), proj, sign=-1) == zero44
    for i in range(4):
        for q in range(4):
            assert proj[q][i] * gdiag[q] == gdiag[i] * proj[i][q]
    assert sum(proj[i][i] for i in range(4)) == 2
    basis = independent_columns(proj)
    gram = [[sum(gdiag[k] * basis[i][k] * basis[q][k] for k in range(4))
             for q in range(2)] for i in range(2)]
    assert gram[0][0] > 0
    assert gram[0][0] * gram[1][1] - gram[0][1] ** 2 > 0


def main():
    rng = random.Random(SEED)
    p_choices = [(F(1, 4), F(1, 2)), (F(1), F(1)),
                 (F(9, 4), F(3, 2)), (F(4), F(2))]
    accepted = 0
    assertions = 0
    rotated = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]

    while accepted < TRIALS:
        p, sqrt_p = rng.choice(p_choices)
        r = F(rng.randint(1, 4))
        denom0 = 10 * r * sqrt_p
        w00 = F(rng.randint(-2, 2), 1) / denom0
        w01 = F(rng.randint(-2, 2), 1) / denom0
        if w00 == 0 and w01 == 0 and accepted % 5:
            continue
        w10 = F(rng.randint(-3, 3), 1) / (5 * r)
        w11 = F(rng.randint(-3, 3), 1) / (5 * r)
        v_num = rng.choice([-3, -2, -1, 1, 2, 3])
        v = F(v_num, 2)

        A = w00 * w00 + w01 * w01
        B = w10 * w10 + w11 * w11
        C = w00 * w10 + w01 * w11
        wedge2 = A * B - C * C
        nu2 = p * r * r * A
        gdiag, j, h = direct_h(p, r, v, w00, w01, w10, w11)
        det = h[0][0] * h[1][1] - h[0][1] * h[1][0]
        if not (h[0][0] < 0 and det < 0):
            continue

        expected = [[-(1 - nu2) / p, r * r * C],
                    [r * r * C, p * v * v + r * r * B]]
        m2 = -det
        expected_m2 = ((1 - nu2) * v * v + (r * r / p) * B
                       - r**4 * wedge2)
        assert h == expected
        assert m2 == expected_m2
        assert h[0][1] / h[0][0] == -p * r * r * C / (1 - nu2)
        assert wedge2 == (w00 * w11 - w01 * w10) ** 2
        assertions += 4

        assert_projector(gdiag, j, projector(gdiag, j, h))
        assertions += 7

        rw0 = [rotated[0][0] * w00 + rotated[0][1] * w01,
               rotated[1][0] * w00 + rotated[1][1] * w01]
        rw1 = [rotated[0][0] * w10 + rotated[0][1] * w11,
               rotated[1][0] * w10 + rotated[1][1] * w11]
        _, _, hr = direct_h(p, r, v, rw0[0], rw0[1], rw1[0], rw1[1])
        assert hr == h
        assertions += 1

        k = F(-2)
        _, _, hk = direct_h(p, r, k * v, w00, w01, k * w10, k * w11)
        detk = hk[0][0] * hk[1][1] - hk[0][1] * hk[1][0]
        assert hk[0][0] == h[0][0]
        assert hk[0][1] == k * h[0][1]
        assert hk[1][1] == k * k * h[1][1]
        assert -detk == k * k * m2
        assertions += 4
        accepted += 1

    p, r, v = F(4), F(3), F(1, 2)
    _, _, hc = direct_h(p, r, v, F(1, 12), F(0), F(1, 3), F(0))
    _, _, hn = direct_h(p, r, v, F(1, 12), F(0), F(0), F(1, 3))
    _, _, hs = direct_h(p, r, v, F(0), F(0), F(1, 3), F(0))
    named = {
        "collinear_h": [[str(x) for x in row] for row in hc],
        "collinear_m2": str(-(hc[0][0] * hc[1][1] - hc[0][1] ** 2)),
        "noncollinear_h": [[str(x) for x in row] for row in hn],
        "noncollinear_m2": str(-(hn[0][0] * hn[1][1] - hn[0][1] ** 2)),
        "static_h": [[str(x) for x in row] for row in hs],
        "static_m2": str(-(hs[0][0] * hs[1][1] - hs[0][1] ** 2)),
    }
    print(json.dumps({
        "assertions": assertions,
        "audit": "G186_INDEPENDENT",
        "named_witnesses": named,
        "seed": SEED,
        "status": "PASS",
        "trials": accepted,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
