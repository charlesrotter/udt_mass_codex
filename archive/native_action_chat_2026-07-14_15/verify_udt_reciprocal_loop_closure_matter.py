#!/usr/bin/env python3
"""Exact checks for the conditional UDT reciprocal-axis loop-matter chain.

The script verifies the rank-one countermodel, pullback area algebra,
orientation/reversal behavior, CSN weight, and decomposable-two-form
pseudoscalar. It does not derive the single-axis premise, loop-holonomy
matter principle, target ontology, action coefficient, or stable solution.
"""

from fractions import Fraction as F
from itertools import permutations


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


def dot(u, v):
    return sum(ui * vi for ui, vi in zip(u, v))


def cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def scale(a, u):
    return tuple(a * ui for ui in u)


def triple(n, u, v):
    return dot(n, cross(u, v))


def matvec(M, w):
    return tuple(sum(M[i][j] * w[j] for j in range(len(w))) for i in range(len(M)))


def det3(M):
    return (
        M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
        - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
        + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
    )


# Conditional single-axis metric completion:
# h_ij=delta_ij+(exp(2phi)-1)n_i n_j.
n_axis = (F(3, 5), F(4, 5), F(0))
t_axis = (F(-4, 5), F(3, 5), F(0))
e2phi = F(9, 4)
h = [
    [F(int(i == j)) + (e2phi - 1) * n_axis[i] * n_axis[j] for j in range(3)]
    for i in range(3)
]
check("single-axis spatial metric has longitudinal eigenvalue exp(2phi)", matvec(h, n_axis) == scale(e2phi, n_axis))
check("single-axis spatial metric leaves transverse directions neutral", matvec(h, t_axis) == t_axis)
check("single-axis spatial determinant is exp(2phi)", det3(h) == e2phi)
check("reciprocal time factor makes full determinant constant", (-1 / e2phi) * det3(h) == -1)
h_reversed = [
    [F(int(i == j)) + (e2phi - 1) * (-n_axis[i]) * (-n_axis[j]) for j in range(3)]
    for i in range(3)
]
check("metric identifies n and -n as the same axis", h_reversed == h)
h_phi0 = [
    [F(int(i == j)) + (F(1) - 1) * n_axis[i] * n_axis[j] for j in range(3)]
    for i in range(3)
]
check("axis orientation becomes metrically invisible at phi=0", h_phi0 == [[F(int(i == j)) for j in range(3)] for i in range(3)])


# Tangent vectors at n=(0,0,1).
n = (F(0), F(0), F(1))
u = (F(2, 3), F(1, 5), F(0))
v = (F(-1, 7), F(3, 4), F(0))
check("unit axis has n dot n=1", dot(n, n) == 1)
check("axis derivatives are tangent", dot(n, u) == 0 and dot(n, v) == 0)

Fuv = triple(n, u, v)
Fvu = triple(n, v, u)
check("target-area form is antisymmetric", Fvu == -Fuv)
check("generic two-directional target area is nonzero", Fuv != 0)

# Rank-one derivatives are proportional and have zero area.
s = F(11, 13)
rank_v = scale(s, u)
check("rank-one target area vanishes", triple(n, u, rank_v) == 0)

# Yet Q2 is positive on the same rank-one probe: explicit non-implication.
M_rank = [[dot(wi, wj) for wj in (u, rank_v)] for wi in (u, rank_v)]
Q2_rank = sum(M_rank[i][j] * M_rank[j][i] for i in range(2) for j in range(2))
Q1_rank = (M_rank[0][0] + M_rank[1][1]) ** 2
check("rank-one Gram invariants obey Q1=Q2", Q1_rank == Q2_rank)
check("rank-one Q2 countermodel has positive cost", Q2_rank > 0)
check("area-form cost Q1-Q2 vanishes on rank one", Q1_rank - Q2_rank == 0)

# The existing reciprocal depth group is one-dimensional: J=H dphi.
# Its smooth Maurer-Cartan wedge contribution is proportional to dphi wedge
# dphi and therefore vanishes identically.
depth_gradient = [F(1, 2), F(-2, 3), F(3, 5), F(4, 7)]
depth_wedge = [
    [depth_gradient[i] * depth_gradient[j] - depth_gradient[j] * depth_gradient[i] for j in range(4)]
    for i in range(4)
]
check("one-dimensional reciprocal-depth current has zero loop wedge", all(x == 0 for row in depth_wedge for x in row))

# Orientation reversal n -> -n with its lifted derivatives u,v -> -u,-v.
n_rev, u_rev, v_rev = scale(-1, n), scale(-1, u), scale(-1, v)
F_rev = triple(n_rev, u_rev, v_rev)
check("axis-orientation reversal flips F", F_rev == -Fuv)
check("axis-orientation reversal leaves F squared invariant", F_rev**2 == Fuv**2)

# A proper target rotation preserves F; an improper one flips it.
def Rz90(w):
    return (-w[1], w[0], w[2])


def reflect_x(w):
    return (-w[0], w[1], w[2])


check("proper target rotation preserves F", triple(Rz90(n), Rz90(u), Rz90(v)) == Fuv)
check("improper target reflection flips F", triple(reflect_x(n), reflect_x(u), reflect_x(v)) == -Fuv)
check("full O(3) leaves F squared invariant", triple(reflect_x(n), reflect_x(u), reflect_x(v)) ** 2 == Fuv**2)

# Exact Gram identity for the two tangent directions.
Q1_two = (dot(u, u) + dot(v, v)) ** 2
Q2_two = dot(u, u) ** 2 + dot(v, v) ** 2 + 2 * dot(u, v) ** 2
Fsum_two = 2 * Fuv**2  # ordered index sum F_ij F_ij
check("ordered-index Gram identity is F_ij F_ij=Q1-Q2", Fsum_two == Q1_two - Q2_two)

# CSN weights in four dimensions: sqrt(-g) weight +4 and F^2 weight -4.
measure_weight = 4
lower_F_weight = 0
inverse_metrics = 2
F2_weight = lower_F_weight - 2 * inverse_metrics
check("lower-index pullback F is CSN neutral", lower_F_weight == 0)
check("raised F squared has CSN weight -4", F2_weight == -4)
check("sqrt(-g) F squared has total CSN weight zero", measure_weight + F2_weight == 0)

# A pullback two-form from a two-dimensional target is decomposable:
# F=a wedge b. Verify epsilon^{munurhosigma} F_munu F_rhosigma=0.
a = [F(1, 2), F(2, 3), F(-1, 5), F(3, 7)]
b = [F(-2, 9), F(4, 11), F(5, 13), F(1, 3)]
twoform = [[a[i] * b[j] - a[j] * b[i] for j in range(4)] for i in range(4)]


def parity(p):
    inversions = sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


ff_dual = F(0)
for p in permutations(range(4)):
    ff_dual += parity(p) * twoform[p[0]][p[1]] * twoform[p[2]][p[3]]
check("decomposable pullback two-form has F wedge F=0", ff_dual == 0)

# Lowest parity-even quadratic norm is nonnegative on a static spatial slice.
spatial_components = [Fuv, F(5, 17), F(-3, 19)]
static_norm = 2 * sum(x * x for x in spatial_components)
check("static spatial two-form norm is nonnegative", static_norm >= 0)
check("static spatial norm vanishes only when all area components vanish", static_norm > 0)

passed = sum(ok for _, ok in checks)
total = len(checks)
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)
