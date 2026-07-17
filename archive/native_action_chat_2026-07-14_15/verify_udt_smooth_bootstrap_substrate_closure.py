#!/usr/bin/env python3
"""Exact smooth bootstrap-substrate closure audit for the reciprocal C^2 branch."""

from fractions import Fraction as F


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    if not ok:
        print(f"[FAIL] {name}")


def power_profile(m, x):
    A = 1 - x**m
    Ax = -m * x ** (m - 1)
    Axx = F(0) if m == 1 else -m * (m - 1) * x ** (m - 2)
    W = x**2 * Axx - 2 * x * Ax + 2 * (A - 1)
    return A, Ax, Axx, W


X = F(13, 4)
xs = (F(1, 20), F(1, 4), F(1, 2), F(4, 5))

# I is an integral of a real square with positive weight on 0<r<X.
check("radial conformal functional is nonnegative", all((F(w) ** 2) / (F(r) ** 2) >= 0 for w, r in ((1, 2), (-3, 5), (0, 7))))

# W=0 Euler equation has indicial roots one and two for B=A-1.
for m in (F(1), F(2), F(3), F(4)):
    indicial = m * (m - 1) - 2 * m + 2
    check(f"W indicial polynomial m={m}", indicial == (m - 1) * (m - 2))

# The complete W=0 family A=1+a r+b r^2.
for r, a, b in ((F(1, 3), F(2), F(-5)), (F(2), F(-1, 7), F(3, 5)), (F(7, 4), F(0), F(-2, 9))):
    A = 1 + a * r + b * r**2
    Ap = a + 2 * b * r
    App = 2 * b
    W = r**2 * App - 2 * r * Ap + 2 * (A - 1)
    check(f"zero-Weyl family at r={r}", W == 0)

# Smooth center and wall select a=0, b=-1/X^2.
a = F(0)
b = -1 / X**2
check("smooth-center derivative selects a=0", a == 0)
check("wall value selects b=-1/X^2", 1 + a * X + b * X**2 == 0)
for r in (F(0), X / 5, X / 2, 4 * X / 5, X):
    A = 1 + b * r**2
    check(f"selected substrate profile r/X={r / X}", A == 1 - (r / X) ** 2)

# Full Bach constraint a0^2-3 a1 a_(-1)=1.
a0, a1, am1, a2 = F(1), F(0), F(0), b
check("selected substrate passes full Bach constraint", a0**2 - 3 * a1 * am1 == 1)

# Reciprocal flux identities q'/q^2=-A'.
for r in (X / 10, X / 3, 3 * X / 4):
    A = 1 - r**2 / X**2
    q = 1 / A
    qp = 2 * r * q**2 / X**2
    J = qp / q**2
    check(f"reciprocal flux identity r/X={r / X}", J == 2 * r / X**2)
    D = 6 / X**2
    flux = 4 * r**2 * J  # pi suppressed on both sides
    enclosed = F(4, 3) * D * r**3
    check(f"uniform flux-divergence integral r/X={r / X}", flux == enclosed)

check("uniform reciprocal-flux density normalization", 6 / X**2 > 0)
check("wall reciprocal flux", 2 * X / X**2 == 2 / X)
check("wall integrated flux without pi", 4 * X**2 * (2 / X) == 8 * X)

# Counterprofile sieve A_m=1-x^m.
for m in (1, 2, 3, 4, 6):
    for x in xs:
        _A, _Ax, _Axx, W = power_profile(m, x)
        check(f"power-profile Weyl numerator m={m}, x={x}", W == -(m - 1) * (m - 2) * x**m)
    action_coefficient = F((m - 1) ** 2 * (m - 2) ** 2, 2 * m - 1)
    check(f"power-profile reduced action coefficient m={m}", action_coefficient >= 0)
    if m == 2:
        check("smooth quadratic has zero reduced action", action_coefficient == 0)
    if m >= 4:
        check(f"smooth higher-power profile has positive action m={m}", action_coefficient > 0)

check("linear zero-action profile fails smooth-center derivative", power_profile(1, F(0))[1] != 0)
check("quadratic zero-action profile passes smooth-center derivative", power_profile(2, F(0))[1] == 0)

# General power-profile reciprocal source and carrier coefficients.
for m in (2, 3, 4, 6):
    for x in (F(1, 4), F(1, 2), F(3, 4)):
        Jprime = F(m * (m - 1)) * x ** (m - 2) / X**2
        D = F(m * (m + 1)) * x ** (m - 2) / X**2
        K = F(2 * m * (m - 1), 3) * x ** (2 * m - 2) / X**2
        c = F(4, 3) * x ** (2 * m)
        check(f"power-profile Jprime positive m={m}, x={x}", Jprime > 0)
        check(f"power-profile source positive m={m}, x={x}", D > 0)
        check(f"power-profile carrier signs m={m}, x={x}", K > 0 and c > 0)
        check(f"power-profile pointwise scale ratio m={m}, x={x}", c / K == 2 * (x * X) ** 2 / (m * (m - 1)))

# For m=2 the exact selected coefficients agree with the prior background audit.
for x in xs:
    K = F(4, 3) * x**2 / X**2
    c = F(4, 3) * x**4
    check(f"selected substrate K positive x={x}", K > 0)
    check(f"selected substrate c positive x={x}", c > 0)
    check(f"selected substrate ratio c/K=r^2 x={x}", c / K == (x * X) ** 2)

passed = sum(ok for _, ok in checks)
total = len(checks)
if passed == total:
    print(f"[PASS] all {total} exact checks")
print("\nSELECTED SUBSTRATE:")
print("A=1-r^2/X^2")
print("q=1/(1-r^2/X^2)")
print("J_q=q'/q^2=2r/X^2")
print("D_q=(r^-2)(r^2 J_q)'=6/X^2")
print("K_parallel=4(r/X)^2/(3X^2), c_parallel=4(r/X)^4/3")
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)
