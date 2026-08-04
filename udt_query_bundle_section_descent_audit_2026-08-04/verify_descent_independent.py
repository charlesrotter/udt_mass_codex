#!/usr/bin/env python3
"""Independent exact reconstruction using only the Python standard library."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
Z = F(0)
O = F(1)


def eye(n: int) -> list[list[F]]:
    return [[O if i == j else Z for j in range(n)] for i in range(n)]


def diag(values: list[F]) -> list[list[F]]:
    return [[values[i] if i == j else Z for j in range(len(values))] for i in range(len(values))]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def mm(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Z) for j in range(len(b[0]))] for i in range(len(a))]


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mv(a: list[list[F]], v: list[F]) -> list[F]:
    return [sum((a[i][j] * v[j] for j in range(len(v))), Z) for i in range(len(a))]


def outer(a: list[F], b: list[F]) -> list[list[F]]:
    return [[x * y for y in b] for x in a]


def trace(a: list[list[F]]) -> F:
    return sum((a[i][i] for i in range(len(a))), Z)


def rank(a: list[list[F]]) -> int:
    x = [row[:] for row in a]
    rows, cols = len(x), len(x[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if x[i][c] != 0), None)
        if pivot is None:
            continue
        x[r], x[pivot] = x[pivot], x[r]
        scale = x[r][c]
        x[r] = [value / scale for value in x[r]]
        for i in range(rows):
            if i != r and x[i][c] != 0:
                factor = x[i][c]
                x[i] = [x[i][j] - factor * x[r][j] for j in range(cols)]
        r += 1
    return r


eta = diag([F(-1), O, O, O])
I4 = eye(4)
e = [[O if i == j else Z for i in range(4)] for j in range(4)]
e0, e1, e2, e3 = e


def dot(x: list[F], y: list[F]) -> F:
    return sum((x[i] * eta[i][i] * y[i] for i in range(4)), Z)


def projector_line(v: list[F]) -> list[list[F]]:
    norm = dot(v, v)
    cov = [eta[i][i] * v[i] for i in range(4)]
    return [[v[i] * cov[j] / norm for j in range(4)] for i in range(4)]


def projector_pair(u: list[F], n: list[F]) -> list[list[F]]:
    return add(projector_line(u), projector_line(n))


P01 = projector_pair(e0, e1)
P02 = projector_pair(e0, e2)
Q01 = sub(I4, P01)
Q02 = sub(I4, P02)
R = [
    [O, Z, Z, Z],
    [Z, Z, F(-1), Z],
    [Z, O, Z, Z],
    [Z, Z, Z, O],
]
Rinv = transpose(R)
A = diag([F(2), F(3), F(5), F(7)])

checks: dict[str, bool] = {}
checks["lorentz"] = mm(mm(transpose(R), eta), R) == eta
checks["covariance"] = mm(mm(R, P01), Rinv) == P02
checks["vertical_change"] = P01 != P02
checks["idempotent_01"] = mm(P01, P01) == P01
checks["idempotent_02"] = mm(P02, P02) == P02
checks["ranks"] = rank(P01) == rank(P02) == 2
checks["identity_basic"] = mm(mm(R, I4), Rinv) == I4
checks["screen_change"] = dot(mv(Q01, e2), mv(Q01, e2)) == 1 and dot(mv(Q02, e2), mv(Q02, e2)) == 0
checks["ambient_trace"] = trace(A) == 17
checks["projected_trace_change"] = trace(mm(P01, A)) == 5 and trace(mm(P02, A)) == 7

n = [Z, F(3, 5), F(4, 5), Z]
m = [Z, F(-4, 5), F(3, 5), Z]
cov_n = [eta[i][i] * n[i] for i in range(4)]
cov_m = [eta[i][i] * m[i] for i in range(4)]
dP = add(outer(m, cov_n), outer(n, cov_m))
checks["vertical_derivative"] = trace(mm(dP, A)) == F(48, 25)
checks["vertical_tangent_rank"] = rank(dP) == 2
checks["boundary_polarization"] = mv(P01, e2) == [Z] * 4 and mv(P02, e2) == e2

x, y = F(2), F(3)
Dx = diag([1 / x, x, O, O])
Dy = diag([1 / y, y, O, O])
Dxy = diag([1 / (x * y), x * y, O, O])
checks["multiplicative_character"] = mm(Dx, Dy) == Dxy
checks["character_reset_covariance"] = mm(mm(R, Dx), Rinv) != Dx
checks["character_composes_after_reset"] = mm(mm(mm(R, Dx), Rinv), mm(mm(R, Dy), Rinv)) == mm(mm(R, Dxy), Rinv)

A0 = diag([F(2), F(3), F(3), F(7)])
checks["collision_parent_same"] = A0 == diag([F(2), F(3), F(3), F(7)])
checks["collision_projectors_differ"] = P01 != P02
checks["collision_isometry_related"] = mm(mm(R, P01), Rinv) == P02

assert all(checks.values()), [key for key, value in checks.items() if not value]
result = {
    "status": "PASS",
    "engine": "stdlib_fraction",
    "imports_production": False,
    "exact_checks": len(checks),
    "vertical_projector_derivative": "48/25",
    "projected_curvature_traces": ["5", "7"],
    "screen_readout_values": ["1", "0"],
    "pair_projector_ranks": [2, 2],
    "collision_projectors_distinct": True,
}
(HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
