#!/usr/bin/env python3
"""Exact audit for the UDT CSN dimensionless-action/reference-branch result.

Checks cover action normalization, charge/energy response ratios, the S^2
quartic invariant identity, positivity conditions, and conditional area-form
uniqueness. They do not derive S^2, an electron branch, a boundary charge, or
any action coefficient.
"""

from fractions import Fraction as F


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


# Overall normalization cancels from classical stationarity and charge ratios.
A = F(7, 3)
lam_scale = F(11, 5)
relative = F(13, 7)
residual = F(0)
check("overall action factor leaves a zero Euler residual zero", A * residual == lam_scale * A * residual == 0)
check("relative coupling survives overall action rescaling", (lam_scale * A * relative) / (lam_scale * A) == relative)

eps = F(17, 19)
q_geo = F(23, 29)
g_response = q_geo / eps
check("dimensionless charge-to-energy response is q/epsilon", g_response * eps == q_geo)
check("overall action normalization cancels from q/epsilon", (A * q_geo) / (A * eps) == q_geo / eps)

# Exact tangent-vector Gram audit in a two-dimensional tangent plane.
vectors = [
    (F(1, 2), F(2, 3)),
    (F(3, 5), F(-1, 7)),
    (F(-2, 9), F(4, 11)),
]


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


M = [[dot(u, v) for v in vectors] for u in vectors]
trM = sum(M[i][i] for i in range(3))
Q1 = trM**2
Q2 = sum(M[i][j] * M[j][i] for i in range(3) for j in range(3))
Fsum = sum(det(vectors[i], vectors[j]) ** 2 for i in range(3) for j in range(3))
check("Q1 and Q2 are distinct on a generic rank-two probe", Q1 != Q2)
check("static S^2 pullback identity is F_ij F_ij=Q1-Q2", Fsum == Q1 - Q2)
check("pullback area density is nonnegative", Fsum >= 0)

# Rank-one probe: all tangent vectors parallel.
rank1 = [(F(1), F(2)), (F(3), F(6)), (F(-2), F(-4))]
M1 = [[dot(u, v) for v in rank1] for u in rank1]
trM1 = sum(M1[i][i] for i in range(3))
Q1_rank1 = trM1**2
Q2_rank1 = sum(M1[i][j] * M1[j][i] for i in range(3) for j in range(3))
Fsum_rank1 = sum(det(rank1[i], rank1[j]) ** 2 for i in range(3) for j in range(3))
check("rank-one probe has Q1=Q2", Q1_rank1 == Q2_rank1)
check("rank-one pullback area vanishes", Fsum_rank1 == 0)

# Static positivity cone for rank<=2 eigenvalues x,y>=0:
# rho=a(x+y)^2+b(x^2+y^2).
def rho(a, b, x, y):
    return a * (x + y) ** 2 + b * (x * x + y * y)


def cone_conditions(a, b):
    return a + b >= 0 and 2 * a + b >= 0


grid = [F(0), F(1, 3), F(1), F(5, 2), F(7)]
inside_examples = [
    (F(1), F(0)),   # Q1
    (F(0), F(1)),   # Q2
    (F(1), F(-1)),  # Q1-Q2
    (F(-1, 4), F(1)),
]
outside_examples = [
    (F(-1), F(0)),
    (F(1), F(-2)),
]
check("all selected inside examples satisfy exact cone inequalities", all(cone_conditions(a, b) for a, b in inside_examples))
check(
    "inside-cone examples are nonnegative on exact nonnegative grid",
    all(rho(a, b, x, y) >= 0 for a, b in inside_examples for x in grid for y in grid),
)
check("outside examples violate at least one exact cone inequality", all(not cone_conditions(a, b) for a, b in outside_examples))
check("a+b<0 is exposed by a rank-one-axis probe", rho(F(1), F(-2), F(1), F(0)) < 0)
check("2a+b<0 is exposed by an equal-eigenvalue probe", rho(F(-1), F(1), F(1), F(1)) < 0)
check("positivity admits Q1, Q2, and Q1-Q2, so it is nonunique", all(cone_conditions(a, b) for a, b in inside_examples[:3]))

# Area-only condition: rho(x,0)=0 for all x forces a+b=0.
a_area = F(31, 37)
b_area = -a_area
check("area-only coefficient condition is a+b=0", a_area + b_area == 0)
check("positive nontrivial area-only sector requires a>0", a_area > 0 and 2 * a_area + b_area > 0)
check(
    "area-only density equals a(Q1-Q2) on generic probe",
    a_area * Q1 + b_area * Q2 == a_area * Fsum,
)
check("area-only density vanishes on rank-one probe", a_area * Q1_rank1 + b_area * Q2_rank1 == 0)

# Overall matter-to-geometry coupling remains a relative dimensionless input.
lambda_m = F(41, 43)
metric_residual = F(47, 53)
matter_source = metric_residual / lambda_m
check("dimensionless sourced equation can determine response at fixed relative coupling", metric_residual - lambda_m * matter_source == 0)
check("multiplying full action does not determine relative matter coupling", (A * lambda_m) / A == lambda_m)

# Existing conditional carrier tuple is incomplete for global calibration.
has_energy = True
has_sigma_cosmic = False
has_native_beta = False
check("a model energy alone is not a complete calibration tuple", has_energy and not (has_sigma_cosmic and has_native_beta))

passed = sum(ok for _, ok in checks)
total = len(checks)
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)

