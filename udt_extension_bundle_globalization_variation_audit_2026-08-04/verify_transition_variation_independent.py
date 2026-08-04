#!/usr/bin/env python3
"""Independent Fraction replay of transition and variation identities."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def add(*matrices):
    return [[sum(m[i][j] for m in matrices) for j in range(len(matrices[0][0]))] for i in range(len(matrices[0]))]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def tr(a):
    return [list(row) for row in zip(*a)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def det(a):
    n = len(a)
    total = F(0)
    for p in itertools.permutations(range(n)):
        inv = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = F(-1 if inv % 2 else 1)
        for i, j in enumerate(p):
            term *= a[i][j]
        total += term
    return total


def inverse(a):
    n = len(a)
    aug = [a[i][:] + eye(n)[i] for i in range(n)]
    for c in range(n):
        pivot = next(i for i in range(c, n) if aug[i][c])
        aug[c], aug[pivot] = aug[pivot], aug[c]
        q = aug[c][c]
        aug[c] = [x / q for x in aug[c]]
        for i in range(n):
            if i != c and aug[i][c]:
                q = aug[i][c]
                aug[i] = [aug[i][j] - q * aug[c][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def block(A, D, S):
    DS = mm(D, S)
    return [A[0] + [F(0), F(0)], A[1] + [F(0), F(0)], DS[0] + D[0], DS[1] + D[1]]


def rank(a):
    work = [row[:] for row in a]
    rows, cols, r = len(work), len(work[0]), 0
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


def flatten(a):
    return [x for row in a for x in row]


checks = {}


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


A = [[F(1, 2), F(0)], [F(0), F(2)]]
D = [[F(3), F(1)], [F(0), F(5)]]
S = [[F(2), F(-1)], [F(4), F(1)]]
dA = [[F(-1, 4), F(0)], [F(0), F(1)]]
dD = [[F(1), F(2)], [F(0), F(-1)]]
dS = [[F(3), F(0)], [F(-2), F(1)]]
E = block(A, D, S)
Ai, Di = inverse(A), inverse(D)
Einv = [Ai[0] + [F(0), F(0)], Ai[1] + [F(0), F(0)], scale(F(-1), mm(S, Ai))[0] + Di[0], scale(F(-1), mm(S, Ai))[1] + Di[1]]
check("block_inverse", mm(E, Einv) == eye(4) and mm(Einv, E) == eye(4))
dDS = add(mm(dD, S), mm(D, dS))
dE = [dA[0] + [F(0), F(0)], dA[1] + [F(0), F(0)], dDS[0] + dD[0], dDS[1] + dD[1]]
right_log = mm(dE, Einv)
expected = [mm(dA, Ai)[0] + [F(0), F(0)], mm(dA, Ai)[1] + [F(0), F(0)], mm(mm(D, dS), Ai)[0] + mm(dD, Di)[0], mm(mm(D, dS), Ai)[1] + mm(dD, Di)[1]]
check("right_log_factorization", right_log == expected)

L1 = [[F(1), F(1), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(1)], [F(0), F(0), F(0), F(1)]]
L2 = [[F(1), F(0), F(1), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(1), F(0), F(1)]]
R1 = [[F(2), F(0), F(0), F(0)], [F(1), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(1), F(1)]]
R2 = [[F(1), F(0), F(0), F(1)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(2), F(0)], [F(0), F(0), F(1), F(1)]]
Ej = mm(mm(L1, E), inverse(R1))
Ek1 = mm(mm(L2, Ej), inverse(R2))
Ek2 = mm(mm(mm(L2, L1), E), inverse(mm(R2, R1)))
check("two_sided_triple_overlap", Ek1 == Ek2)

dE0 = [[F(1), F(0), F(1), F(0)], [F(0), F(-1), F(0), F(0)], [F(1), F(2), F(0), F(1)], [F(0), F(1), F(-1), F(0)]]
dL1 = [[F(0), F(1), F(0), F(0)], [F(1), F(0), F(0), F(0)], [F(0), F(0), F(0), F(1)], [F(0), F(0), F(-1), F(0)]]
dR1 = [[F(1), F(0), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(-1), F(0)], [F(1), F(0), F(0), F(0)]]
dEj = add(mm(mm(dL1, E), inverse(R1)), mm(mm(L1, dE0), inverse(R1)), scale(F(-1), mm(mm(mm(mm(L1, E), inverse(R1)), dR1), inverse(R1))))
ej = mm(dEj, inverse(Ej))
rhs = add(mm(dL1, inverse(L1)), mm(mm(L1, mm(dE0, inverse(E))), inverse(L1)), scale(F(-1), mm(mm(Ej, mm(dR1, inverse(R1))), inverse(Ej))))
check("linearized_two_sided_overlap", ej == rhs)

dL2 = [[F(0), F(0), F(1), F(0)], [F(0), F(1), F(0), F(0)], [F(1), F(0), F(0), F(0)], [F(0), F(0), F(0), F(-1)]]
L21 = mm(L2, L1)
dL21 = add(mm(dL2, L1), mm(L2, dL1))
lhs = mm(dL21, inverse(L21))
rhs = add(mm(dL2, inverse(L2)), mm(mm(L2, mm(dL1, inverse(L1))), inverse(L2)))
check("linearized_left_cocycle", lhs == rhs)

dR2 = [[F(0), F(1), F(0), F(0)], [F(0), F(0), F(0), F(1)], [F(1), F(0), F(0), F(0)], [F(0), F(-1), F(0), F(0)]]
R21 = mm(R2, R1)
dR21 = add(mm(dR2, R1), mm(R2, dR1))
lhs = mm(dR21, inverse(R21))
rhs = add(mm(dR2, inverse(R2)), mm(mm(R2, mm(dR1, inverse(R1))), inverse(R2)))
check("linearized_right_cocycle", lhs == rhs)

def G(a):
    return [[a, F(0)], [F(0), 1 / a]]


def Rev(b):
    return [[F(0), b], [1 / b, F(0)]]


check("reversal_pair_preserves", mm(Rev(F(2)), Rev(F(3))) == G(F(2, 3)))
check("reversal_conjugates_depth", mm(mm(Rev(F(2)), G(F(5))), inverse(Rev(F(2)))) == G(F(1, 5)))
check("even_parity_cocycle", mm(mm(Rev(F(2)), Rev(F(3))), G(F(3, 2))) == eye(2))
check("odd_three_reversal_offdiagonal", mm(mm(Rev(F(2)), Rev(F(3))), Rev(F(5)))[0][0] == 0)

eta2 = [[F(-1), F(0)], [F(0), F(1)]]
swap = Rev(F(1))
check("swap_not_Lorentz_for_diagonal_readout", mm(mm(tr(swap), eta2), swap) == scale(F(-1), eta2))

O = [[F(0), F(-1)], [F(1), F(0)]]
check("screen_rotation_gauge", mm(tr(mm(O, D)), mm(O, D)) == mm(tr(D), D))

H1 = [[F(2), F(0)], [F(0), F(3)]]
H2 = [[F(4), F(1)], [F(1), F(5)]]
Hmid = scale(F(1, 2), add(H1, H2))
check("convex_screen_anchor_positive", Hmid[0][0] > 0 and det(Hmid) > 0)

eta4 = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
q = [[F(2)], [F(1)], [F(3)], [F(-1)]]
qm = scale(F(-1), q)
s = mm(mm(tr(q), eta4), q)[0][0]
sm = mm(mm(tr(qm), eta4), qm)[0][0]
Pq = scale(1 / s, mm(mm(eta4, q), tr(q)))
Pqm = scale(1 / sm, mm(mm(eta4, qm), tr(qm)))
check("dphi_sign_scalar", s == sm)
check("dphi_sign_projector", Pq == Pqm)

# Seven independent local extension directions by matrix positions.
positions = [(2, 2), (2, 3), (3, 3), (2, 0), (2, 1), (3, 0), (3, 1)]
basis = []
for i, j in positions:
    m = [[F(0) for _ in range(4)] for _ in range(4)]
    m[i][j] = F(1)
    basis.append(flatten(m))
check("seven_extension_chart_rank", rank(list(map(list, zip(*basis)))) == 7)

if len(checks) != 16:
    raise AssertionError(f"unexpected check count: {len(checks)}")

result = {
    "schema": "udt-extension-globalization-independent-fraction-1.0",
    "status": "PASS",
    "check_count": len(checks),
    "checks": checks,
    "production_imported": False,
    "third_party_packages": [],
    "maximum_conclusion": "INDEPENDENT_EXACT_REPLAY_OF_TRANSITION_AND_VARIATION_IDENTITIES_ONLY",
}
(HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
