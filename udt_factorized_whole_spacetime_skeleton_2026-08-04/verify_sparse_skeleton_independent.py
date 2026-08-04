#!/usr/bin/env python3
"""Independent standard-library rational replay of sparse skeleton identities."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def det(a):
    n = len(a)
    total = F(0)
    for perm in itertools.permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F(-1 if inversions % 2 else 1)
        for i, j in enumerate(perm):
            term *= a[i][j]
        total += term
    return total


def rank(a):
    work = [row[:] for row in a]
    rows, cols = len(work), len(work[0])
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if work[i][c]), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        q = work[r][c]
        work[r] = [x / q for x in work[r]]
        for i in range(rows):
            if i != r and work[i][c]:
                q = work[i][c]
                work[i] = [work[i][j] - q * work[r][j] for j in range(cols)]
        r += 1
    return r


def inv2(a):
    delta = det(a)
    return [[a[1][1] / delta, -a[0][1] / delta], [-a[1][0] / delta, a[0][0] / delta]]


def block_extension(A, D, S):
    DS = matmul(D, S)
    return [A[0] + [F(0), F(0)], A[1] + [F(0), F(0)], DS[0] + D[0], DS[1] + D[1]]


def block_inverse(A, D, S):
    Ai, Di = inv2(A), inv2(D)
    minus_SAi = scale(F(-1), matmul(S, Ai))
    return [Ai[0] + [F(0), F(0)], Ai[1] + [F(0), F(0)], minus_SAi[0] + Di[0], minus_SAi[1] + Di[1]]


def flatten(a):
    return [x for row in a for x in row]


def basis(i, j):
    out = [[F(0) for _ in range(4)] for _ in range(4)]
    out[i][j] = F(1)
    return out


checks = {}


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def pair(p):
    return [[F(1, p), F(0)], [F(0), F(p)]]


p1, p2 = 2, 3
check("pair_composition_rational_character", matmul(pair(p2), pair(p1)) == pair(p1 * p2))
check("pair_reversal_rational_character", matmul(pair(F(1, p1)), pair(p1)) == eye(2))

A = pair(2)
D = [[F(3), F(5)], [F(0), F(7)]]
S = [[F(2), F(-1)], [F(4), F(3)]]
E = block_extension(A, D, S)
Ei = block_inverse(A, D, S)
check("block_inverse_left", matmul(E, Ei) == eye(4))
check("block_inverse_right", matmul(Ei, E) == eye(4))
check("block_determinant", det(E) == det(A) * det(D))

eta = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
g = matmul(matmul(transpose(E), eta), E)
check("metric_symmetric", g == transpose(g))
check("metric_determinant", det(g) == -det(E) ** 2)

# Three angular and four lower-left generator directions.
tangents = [basis(2, 2), basis(2, 3), basis(3, 3), basis(2, 0), basis(2, 1), basis(3, 0), basis(3, 1)]
tangent_columns = list(map(list, zip(*(flatten(x) for x in tangents))))
check("seven_extension_tangent_rank", rank(tangent_columns) == 7)
metric_tangents = [add(matmul(transpose(x), eta), matmul(eta, x)) for x in tangents]
metric_columns = list(map(list, zip(*(flatten(x) for x in metric_tangents))))
check("seven_metric_tangent_rank", rank(metric_columns) == 7)

det_one = [add(basis(2, 2), scale(F(-1), basis(3, 3))), basis(2, 3), basis(2, 0), basis(2, 1), basis(3, 0), basis(3, 1)]
check("six_determinant_one_tangent_rank", rank(list(map(list, zip(*(flatten(x) for x in det_one))))) == 6)

# Upper-triangular K is skew only when all three entries vanish.
K_examples = [basis(2, 2), basis(2, 3), basis(3, 3)]
check("all_nonzero_triangular_K_basis_change_metric", all(add(matmul(transpose(k), eta), matmul(eta, k)) != [[F(0)] * 4 for _ in range(4)] for k in K_examples))

def shift(p, strength=F(5, 2)):
    out = eye(4)
    out[0][0], out[1][1] = F(1, p), F(p)
    out[2][0] = strength * (1 - F(1, p))
    return out


check("shift_counterfamily_composition", matmul(shift(p2), shift(p1)) == shift(p1 * p2))

def angular(p, q):
    return [[F(1, p), F(0), F(0), F(0)], [F(0), F(p), F(0), F(0)], [F(0), F(0), F(1, q), F(0)], [F(0), F(0), F(0), F(q)]]


check("angular_counterfamily_composition", matmul(angular(p2, 5), angular(p1, 7)) == angular(p1 * p2, 35))

O = [[F(0), F(-1)], [F(1), F(0)]]
check("screen_rotation_metric_gauge", matmul(transpose(matmul(O, D)), matmul(O, D)) == matmul(transpose(D), D))
Cscreen = matmul(matmul(D, O), inv2(D))
check("screen_complex_structure", matmul(Cscreen, Cscreen) == scale(F(-1), eye(2)) and det(Cscreen) == 1)

if len(checks) != 15:
    raise AssertionError(f"unexpected check count: {len(checks)}")

result = {
    "schema": "udt-factorized-whole-spacetime-independent-rational-1.0",
    "status": "PASS",
    "check_count": len(checks),
    "checks": checks,
    "production_imported": False,
    "third_party_packages": [],
    "maximum_conclusion": "INDEPENDENT_RATIONAL_REPLAY_OF_SPARSE_BLOCK_IDENTITIES_ONLY",
}
(HERE / "SPARSE_SKELETON_INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
