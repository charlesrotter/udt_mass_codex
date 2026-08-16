#!/usr/bin/env python3
"""Standalone Fraction replay of the G114 finite-dimensional identities."""

from fractions import Fraction as F
import json
import math


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def zero(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def tr(a):
    return [list(row) for row in zip(*a)]


def inv(a):
    n = len(a)
    aug = [a[i][:] + eye(n)[i] for i in range(n)]
    for col in range(n):
        pivot = next(r for r in range(col, n) if aug[r][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        p = aug[col][col]
        aug[col] = [x / p for x in aug[col]]
        for r in range(n):
            if r != col:
                q = aug[r][col]
                aug[r] = [aug[r][j] - q * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def det(a):
    n = len(a)
    work = [row[:] for row in a]
    out = F(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if work[r][col] != 0), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            out = -out
        p = work[col][col]
        out *= p
        for r in range(col + 1, n):
            q = work[r][col] / p
            for j in range(col, n):
                work[r][j] -= q * work[col][j]
    return out


def eq(a, b):
    return all(x == 0 for row in sub(a, b) for x in row)


def block2(a, b, c, d):
    return [
        [a, 0, b, 0],
        [0, a, 0, b],
        [c, 0, d, 0],
        [0, c, 0, d],
    ]


def rot(c, s):
    return [[c, -s], [s, c]]


def lift(q):
    return [
        [q[0][0], q[0][1], 0, 0],
        [q[1][0], q[1][1], 0, 0],
        [0, 0, q[0][0], q[0][1]],
        [0, 0, q[1][0], q[1][1]],
    ]


I4 = eye(4)
Z2 = zero(2, 2)
Omega = [[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]]
P = {
    "A": block2(F(1), F(1), F(0), F(1)),
    "B": block2(F(3, 5), F(4, 5), F(-4, 5), F(3, 5)),
    "C": block2(F(1), F(0), F(-2), F(1)),
}
B = {
    "A": I4,
    "B": lift(rot(F(3, 5), F(4, 5))),
    "C": lift(rot(F(5, 13), F(12, 13))),
}
omega = {"A": F(2), "B": F(3), "C": F(5)}


def phase_diag(q, p):
    return [
        [q[0][0], q[0][1], 0, 0],
        [q[1][0], q[1][1], 0, 0],
        [0, 0, p[0][0], p[0][1]],
        [0, 0, p[1][0], p[1][1]],
    ]


q = {
    "A": eye(2),
    "B": rot(F(3, 5), F(4, 5)),
    "C": rot(F(5, 13), F(12, 13)),
}
T_source = {i: phase_diag(q[i], [[x / omega[i] for x in row] for row in q[i]]) for i in "ABC"}


def C_cal(j, i):
    return mm(inv(T_source[j]), T_source[i])


def C(j, i):
    return mm(inv(B[j]), B[i])


def R(j, i, c=None):
    return mm(inv(P[j]), mm(C(j, i) if c is None else c, P[i]))


RBA, RCB, RAC = R("B", "A"), R("C", "B"), R("A", "C")
loop = mm(RAC, mm(RCB, RBA))
H = lift(rot(F(0), F(1)))
RAC_h = R("A", "C", mm(H, C("A", "C")))
loop_h = mm(RAC_h, mm(RCB, RBA))
expected_h = mm(inv(P["A"]), mm(H, P["A"]))

# Physical point-observer variations start in L0={(0,0,p1,p2)}. Express
# their endpoint images in the common source frame and compute exact
# intersection dimensions.
Iota = [[0, 0], [0, 0], [1, 0], [0, 1]]


def rank(a):
    work = [row[:] for row in a]
    rows, cols, r = len(work), len(work[0]), 0
    for col in range(cols):
        pivot = next((i for i in range(r, rows) if work[i][col] != 0), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        p = work[r][col]
        work[r] = [x / p for x in work[r]]
        for i in range(rows):
            if i != r:
                q = work[i][col]
                work[i] = [work[i][j] - q * work[r][j] for j in range(cols)]
        r += 1
    return r


def hjoin(a, b):
    return [a[i] + b[i] for i in range(len(a))]


L = {i: mm(B[i], mm(P[i], Iota)) for i in "ABC"}
intersections = {}
for j, i in [("B", "A"), ("C", "B"), ("A", "C")]:
    intersections[j + i] = rank(L[j]) + rank(L[i]) - rank(hjoin(L[j], L[i]))

P0 = block2(F(1), F(2), F(0), F(1))
P_aligned = {i: mm(inv(B[i]), P0) for i in "ABC"}
L_aligned = {i: mm(B[i], mm(P_aligned[i], Iota)) for i in "ABC"}

# Independently integrate y''+y=0 from 0 to pi with fixed-step RK4 for the
# two scalar fundamental solutions. This does not import or restate the
# production script's closed form.
def rhs(state):
    c, cp, s, sp_ = state
    return [cp, -c, sp_, -s]


def rk4_step(state, h):
    k1 = rhs(state)
    k2 = rhs([state[i] + 0.5 * h * k1[i] for i in range(4)])
    k3 = rhs([state[i] + 0.5 * h * k2[i] for i in range(4)])
    k4 = rhs([state[i] + h * k3[i] for i in range(4)])
    return [state[i] + h * (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6 for i in range(4)]


nstep = 8192
h = math.pi / nstep
osc = [1.0, 0.0, 0.0, 1.0]
for _ in range(nstep):
    osc = rk4_step(osc, h)
c_num, cp_num, s_num, sp_num = osc
P_caustic_num = [
    [c_num, 0.0, s_num, 0.0],
    [0.0, c_num, 0.0, s_num],
    [cp_num, 0.0, sp_num, 0.0],
    [0.0, cp_num, 0.0, sp_num],
]


def mm_float(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def tr_float(a):
    return [list(row) for row in zip(*a)]


Omega_float = [[float(x) for x in row] for row in Omega]
symp_num = mm_float(tr_float(P_caustic_num), mm_float(Omega_float, P_caustic_num))
symp_defect = max(abs(symp_num[i][j] - Omega_float[i][j]) for i in range(4) for j in range(4))
det_phase_num = (c_num * sp_num - s_num * cp_num) ** 2
cal_loop = mm(C_cal("A", "C"), mm(C_cal("C", "B"), C_cal("B", "A")))
cal_conformal = {}
for j, i in [("B", "A"), ("C", "B"), ("A", "C")]:
    c = C_cal(j, i)
    target = [[(omega[j] / omega[i]) * x for x in row] for row in Omega]
    cal_conformal[j + i] = eq(mm(tr(c), mm(Omega, c)), target)

checks = {
    "phase_determinants_one": all(det(p) == 1 for p in P.values()),
    "phase_symplectic": all(eq(mm(tr(p), mm(Omega, p)), Omega) for p in P.values()),
    "junction_descent": eq(mm(C("C", "B"), C("B", "A")), C("C", "A")),
    "common_loop_identity": eq(loop, I4),
    "reversal": eq(R("A", "B"), inv(RBA)),
    "holonomy_conjugacy": eq(loop_h, expected_h),
    "holonomy_nonidentity": not eq(loop_h, I4),
    "caustic_position_numerically_zero": abs(s_num) < 2e-13,
    "caustic_phase_invertible": abs(det_phase_num - 1.0) < 2e-12,
    "caustic_phase_symplectic": symp_defect < 2e-12,
    "generic_full_loop_does_not_force_beam_alignment": all(v == 0 for v in intersections.values()),
    "aligned_beam_control_exists": all(eq(L_aligned[i], L_aligned["A"]) for i in "BC"),
    "unequal_source_frequency_loop_identity": eq(cal_loop, I4),
    "unequal_source_frequency_junctions_conformally_symplectic": all(cal_conformal.values()),
}

print(json.dumps({
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "generic_vertex_image_intersection_dimensions": intersections,
    "independent_caustic": {
        "steps": nstep,
        "position_block_scalar": s_num,
        "phase_determinant": det_phase_num,
        "symplectic_defect_max": symp_defect,
    },
}, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit(1)
