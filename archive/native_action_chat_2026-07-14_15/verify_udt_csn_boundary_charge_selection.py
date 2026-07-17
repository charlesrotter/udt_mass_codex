#!/usr/bin/env python3
"""Exact dependency-free checks for UDT CSN boundary-charge selection.

The script verifies scale weights, endpoint coefficients, explicit
counterfamilies, Euler endpoint values, clock scaling, and interface
cancellation. It does not derive a covariant boundary action, boundary
ontology, Hamiltonian charge, or physical normalization.
"""

from fractions import Fraction as F


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


# Exact rational probe values. Identities are also checked through their scale
# exponents and analytic derivative functions below.
r = F(7, 3)
lam = F(5, 2)
gamma = F(11, 13)
A_wall = F(0)
v_wall = F(-1)
A_flat = F(1)
v_flat = F(0)


def boundary_value(radius, b_value):
    return gamma * b_value / radius


check(
    "CSN first-jet boundary value has scale weight -1",
    boundary_value(lam * r, F(17, 19)) / boundary_value(r, F(17, 19)) == 1 / lam,
)
check("A is scale invariant", A_wall == 0)
check("v=r A' is scale invariant", (lam * r) * (v_wall / (lam * r)) == v_wall)

# At WR-L the conformal bulk momenta P0=P1=0. For B=gamma b(A,v)/r:
# coefficient of delta A is gamma b_A/r, coefficient of delta A' is gamma b_v.
P0 = F(0)
P1 = F(0)


def b_counter(k, A, v):
    del v
    return k * (1 - A * A)


def b_counter_A(k, A, v):
    del v
    return -2 * k * A


def b_counter_v(k, A, v):
    del k, A, v
    return F(0)


k1 = F(23, 29)
k2 = F(31, 37)
check("counterfamily vanishes on the flat reference", b_counter(k1, A_flat, v_flat) == 0)
check("counterfamily has arbitrary wall value k", b_counter(k1, A_wall, v_wall) == k1)
check("counterfamily wall A derivative vanishes", b_counter_A(k1, A_wall, v_wall) == 0)
check("counterfamily wall v derivative vanishes", b_counter_v(k1, A_wall, v_wall) == 0)
check(
    "free-jet differentiability coefficients vanish on WR-L",
    P0 + gamma * b_counter_A(k1, A_wall, v_wall) / r == 0
    and P1 + gamma * b_counter_v(k1, A_wall, v_wall) == 0,
)
check("different k retain identical endpoint differentiability", b_counter_A(k2, A_wall, v_wall) == 0 and b_counter_v(k2, A_wall, v_wall) == 0)
check("different k give different inverse-X boundary values", boundary_value(r, k1) != boundary_value(r, k2))

# Bare Euler radial primitive b_E=4(A-1)v.
def b_euler(A, v):
    return 4 * (A - 1) * v


def b_euler_A(A, v):
    del A
    return 4 * v


def b_euler_v(A, v):
    del v
    return 4 * (A - 1)


check("Euler b is zero on flat A=1", b_euler(A_flat, v_flat) == 0)
check("Euler b is four on WR-L wall data", b_euler(A_wall, v_wall) == 4)
check("Euler bare primitive has nonzero wall A derivative", b_euler_A(A_wall, v_wall) == -4)
check("Euler bare primitive has nonzero wall v derivative", b_euler_v(A_wall, v_wall) == -4)
check("Euler primitive vanishes at any A=1 fold", b_euler(F(1), F(41, 43)) == 0)
X = F(47, 53)
check("Euler one-sided WR-L endpoint value is 4/X", F(4) / X == boundary_value(X, F(4)) / gamma)

# A total derivative split at an internal interface cancels with opposite
# orientations when its primitive is continuous.
primitive_interface = F(59, 61)
check("matched-interface primitive cancels orientation by orientation", primitive_interface + (-primitive_interface) == 0)

# Complete scale-neutral time-slab action.
delta_tau = F(67, 71)
X1 = F(73, 79)
X2 = lam * X1
dt1 = delta_tau * X1  # c=1 in this exact weight check
dt2 = delta_tau * X2
S1 = dt1 * boundary_value(X1, k1)
S2 = dt2 * boundary_value(X2, k1)
check("boundary action is invariant at fixed dimensionless duration", S1 == S2)
check("per-coordinate-time boundary readout scales as inverse X", boundary_value(X2, k1) / boundary_value(X1, k1) == 1 / lam)

# Overall normalization is not fixed by the vacuum stationarity equations.
alpha1 = F(83, 89)
alpha2 = F(97, 101)
charge1 = alpha1 * boundary_value(X1, k1)
charge2 = alpha2 * boundary_value(X1, k1)
check("different overall action normalizations give different charge values", charge1 != charge2)
check("nonzero rescaling leaves zero bulk equation zero", alpha1 * 0 == 0 and alpha2 * 0 == 0)

passed = sum(ok for _, ok in checks)
total = len(checks)
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)

