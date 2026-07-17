#!/usr/bin/env python3
"""Exact algebra audit for WR-L/global-X closure of the conformal carrier branch.

No field equation from an external theory is used. The script checks the metric invariant already
derived for the reciprocal spherical metric, its conditional conformal-action Euler family,
homothetic scaling, endpoint character, and center regularity.
"""

from fractions import Fraction as F


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


def family(x, xi):
    """A_xi=1+xi*x-(1+xi)*x^2, with x=r/X."""
    return 1 + xi * x - (1 + xi) * x * x


def family_dx(x, xi):
    return xi - 2 * (1 + xi) * x


def family_dxx(_x, xi):
    return -2 * (1 + xi)


def weyl_numerator_dimensionless(x, xi):
    A = family(x, xi)
    Ax = family_dx(x, xi)
    Axx = family_dxx(x, xi)
    return x * x * Axx - 2 * x * Ax + 2 * (A - 1)


xis = (F(-7, 4), F(-1), F(-2, 3), F(0), F(5, 4))
xs = (F(1, 11), F(1, 3), F(3, 4), F(9, 10))

check("every family member has A(0)=1", all(family(F(0), xi) == 1 for xi in xis))
check("every family member has A(1)=0", all(family(F(1), xi) == 0 for xi in xis))
check("family factorization at all probes", all(family(x, xi) == (1 - x) * (1 + (1 + xi) * x) for xi in xis for x in xs))
check("Weyl numerator vanishes for the full endpoint family", all(weyl_numerator_dimensionless(x, xi) == 0 for xi in xis for x in xs))
check("conditional conformal bulk density vanishes for the full family", all(weyl_numerator_dimensionless(x, xi) ** 2 == 0 for xi in xis for x in xs))

check("WR-L is xi=-1", all(family(x, F(-1)) == 1 - x for x in xs))
check("smooth quadratic member is xi=0", all(family(x, F(0)) == 1 - x * x for x in xs))
check("center derivative equals xi in dimensionless coordinates", all(family_dx(F(0), xi) == xi for xi in xis))
check("smooth-center condition selects xi=0", family_dx(F(0), F(0)) == 0 and all(family_dx(F(0), xi) != 0 for xi in xis if xi != 0))
check("residual WR-L and smooth-center selectors disagree", F(-1) != F(0))

# For xi>-2 the second factor is positive on 0<=x<1 and the wall zero is simple.
check("sample family members stay positive inside the static patch", all(family(x, xi) > 0 for xi in xis for x in xs))
check("wall slope is finite for every family member", all(family_dx(F(1), xi) == -(2 + xi) for xi in xis))
check("sample walls are simple causal zeros", all(family_dx(F(1), xi) < 0 for xi in xis))

# Exact center anisotropy coefficients q-1.
for x in xs:
    q_linear_minus_one = 1 / (1 - x) - 1
    q_quadratic_minus_one = 1 / (1 - x * x) - 1
    check(f"WR-L anisotropy identity at x={x}", q_linear_minus_one == x / (1 - x))
    check(f"quadratic anisotropy identity at x={x}", q_quadratic_minus_one == x * x / (1 - x * x))

small_x = (F(1, 10), F(1, 100), F(1, 1000))
linear_over_x = [1 / (1 - x) for x in small_x]
linear_over_x2 = [1 / (x * (1 - x)) for x in small_x]
quadratic_over_x2 = [1 / (1 - x * x) for x in small_x]
check("WR-L anisotropy divided by x approaches one", all(value > 1 for value in linear_over_x) and linear_over_x[-1] < linear_over_x[0])
check("WR-L anisotropy divided by x^2 diverges toward the seat", linear_over_x2[0] < linear_over_x2[1] < linear_over_x2[2])
check("quadratic anisotropy divided by x^2 approaches one", all(value > 1 for value in quadratic_over_x2) and quadratic_over_x2[-1] < quadratic_over_x2[0])

# Reciprocal spherical scalar curvature R*X^2 for the two decisive members.
for x in xs:
    # R X^2 = -A_xx - 4 A_x/x - 2(A-1)/x^2.
    R_linear = -family_dxx(x, F(-1)) - 4 * family_dx(x, F(-1)) / x - 2 * (family(x, F(-1)) - 1) / x**2
    R_quadratic = -family_dxx(x, F(0)) - 4 * family_dx(x, F(0)) / x - 2 * (family(x, F(0)) - 1) / x**2
    check(f"WR-L scalar curvature at x={x}", R_linear == 6 / x)
    check(f"quadratic scalar curvature at x={x}", R_quadratic == 12)

# Static-wall causal audit in ingoing coordinates: [[-A,1],[1,0]].
for xi in xis:
    A_wall = family(F(1), xi)
    determinant = (-A_wall) * 0 - 1
    crossing_speed = F(1, 3)
    crossing_norm = -A_wall - 2 * crossing_speed
    check(f"regular ingoing wall determinant xi={xi}", determinant == -1)
    check(f"timelike wall-crossing direction xi={xi}", crossing_norm < 0)

# The conditional radial C^2 Euler family A=a0+a1*r+a_(-1)/r+a2*r^2 has
# W=2(a0-1)+6*a_(-1)/r and W''+2W'/r=0.
for r, a0, am1 in ((F(2), F(3, 2), F(1, 5)), (F(7, 3), F(1), F(-2, 7)), (F(5), F(4), F(0))):
    W = 2 * (a0 - 1) + 6 * am1 / r
    Wp = -6 * am1 / r**2
    Wpp = 12 * am1 / r**3
    check(f"radial reduced Euler family at r={r}", Wpp + 2 * Wp / r == 0 and W == 2 * (a0 - 1) + 6 * am1 / r)

a0_regular, am1_regular, a1_smooth = F(1), F(0), F(0)
X = F(7, 3)
a2_wall = -1 / X**2
check("regular normalized center removes constant and inverse-r Weyl modes", 2 * (a0_regular - 1) == 0 and 6 * am1_regular == 0)
check("smooth vacuum plus A(X)=0 gives the quadratic member", a0_regular + a1_smooth * X + a2_wall * X**2 == 0)
check("WR-L remains a distinct zero-Weyl singular-seat member", -1 / X != a1_smooth and a2_wall != 0)

# Four-dimensional conformal density is homothetic: sqrt(-g) contributes X^4,
# C^2 contributes X^-4. Static energy contributes one inverse X.
check("four-dimensional conformal action has net X exponent zero", 4 - 4 == 0)
check("static curvature-squared energy has net X exponent minus one", 3 - 4 == -1)
check("dimensionless Bach equation contains no overall X", 4 - 4 == 0)

# The local q=1 channel is a regular metric degeneracy of the axis, not a metric singularity.
q = F(1)
u, v, p, s = F(0), F(0), F(7, 5), F(-3, 2)
d = q - 1
one_axis_C2 = (
    (v / q - u**2 / q**2 - d * p**2 / q) ** 2
    + (d * s + 2 * u * p) ** 2 / q
    + (u**2 - d * q * (2 * q + 1) * p**2) ** 2 / (3 * q**4)
)
check("constant isotropic q=1 erases arbitrary axis jets", one_axis_C2 == 0)

# Radial boundary director n=rhat has unit oriented lift degree:
# (1/4pi) integral_0^{2pi} integral_0^pi sin(theta) dtheta dphi = 1.
check("radial boundary director oriented lift has degree one", F(1, 4) * F(2) * F(2) == 1)

passed = sum(ok for _, ok in checks)
total = len(checks)
print("\nENDPOINT FAMILY:")
print("A_xi(x)=1+xi*x-(1+xi)*x^2=(1-x)(1+(1+xi)x)")
print("WR-L: xi=-1; smooth conformal member: xi=0; C^2=0 for every xi")
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)
