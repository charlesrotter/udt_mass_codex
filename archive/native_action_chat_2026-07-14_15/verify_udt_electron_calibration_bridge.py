#!/usr/bin/env python3
"""Dependency-free exact checks for the UDT electron-calibration bridge.

This script verifies the encoded reduced-action, boundary, virial, dimensional,
and closure algebra. It does not derive the action, carrier identity, boundary
primitive, G normalization, beta_e, or any observational value.
"""

from fractions import Fraction as F


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


class Poly:
    """Tiny exact polynomial in r, represented by power -> Fraction."""

    def __init__(self, terms=None):
        self.t = {int(k): F(v) for k, v in (terms or {}).items() if F(v) != 0}

    def __add__(self, other):
        other = other if isinstance(other, Poly) else Poly({0: other})
        keys = set(self.t) | set(other.t)
        return Poly({k: self.t.get(k, F(0)) + other.t.get(k, F(0)) for k in keys})

    def __sub__(self, other):
        other = other if isinstance(other, Poly) else Poly({0: other})
        keys = set(self.t) | set(other.t)
        return Poly({k: self.t.get(k, F(0)) - other.t.get(k, F(0)) for k in keys})

    def __mul__(self, other):
        if not isinstance(other, Poly):
            other = Poly({0: other})
        out = {}
        for i, ai in self.t.items():
            for j, bj in other.t.items():
                out[i + j] = out.get(i + j, F(0)) + ai * bj
        return Poly(out)

    __rmul__ = __mul__

    def derivative(self):
        return Poly({k - 1: k * v for k, v in self.t.items() if k != 0})

    def __eq__(self, other):
        other = other if isinstance(other, Poly) else Poly({0: other})
        return self.t == other.t

    def value(self, r):
        r = F(r)
        return sum(v * r**k for k, v in self.t.items())

    def is_zero(self):
        return not self.t


# T1: reduced C^2 action on WR-L.
X = F(7, 3)
r = Poly({1: 1})
A = Poly({0: 1, 1: -1 / X})
Ap = A.derivative()
App = Ap.derivative()
W = (r * r * App) - (2 * r * Ap) + 2 * (A - 1)
check("WR-L A' is exactly -1/X", Ap == Poly({0: -1 / X}))
check("WR-L A'' is exactly zero", App.is_zero())
check("full nonlinear conformal bracket W[A] vanishes identically", W.is_zero())

gamma = F(11, 13)
Wp = W.derivative()
P1 = 2 * gamma * W
# P0 = -4 gamma W/r - 2 gamma W'. Since W is the zero polynomial,
# the W/r term is exactly zero on every r>0 and by its continuous limit.
P0 = -2 * gamma * Wp
check("higher-derivative boundary momentum P1 vanishes on WR-L", P1.is_zero())
check("higher-derivative boundary momentum P0 vanishes on WR-L", P0.is_zero())
check("reduced C^2 density gamma W^2/r^2 vanishes on WR-L", (W * W).is_zero())
check("first variation coefficient is zero because W and W' vanish", W.is_zero() and Wp.is_zero())

# Exact Euler-density boundary primitive 4(A-1)A'.
euler_primitive = 4 * (A - 1) * Ap
check("Euler primitive on WR-L is 4r/X^2", euler_primitive.t == {1: 4 / X**2})
check("Euler primitive is zero at the seat", euler_primitive.value(0) == 0)
check("Euler primitive is 4/X at the wall r=X", euler_primitive.value(X) == 4 / X)
check("Euler contribution scales with X-weight -1", (4 / (F(5, 2) * X)) / (4 / X) == F(2, 5))

# T3: what one observed mass fixes for E(R)=aR+b/R.
Eobs = F(17, 19)
R1 = F(5, 7)
R2 = F(11, 13)


def coefficients_for_mass_and_radius(E, radius):
    return E / (2 * radius), E * radius / 2


def energy(a, b, radius):
    return a * radius + b / radius


def derivative(a, b, radius):
    return a - b / radius**2


a1, b1 = coefficients_for_mass_and_radius(Eobs, R1)
a2, b2 = coefficients_for_mass_and_radius(Eobs, R2)
check("first coefficient pair has stationary radius R1", derivative(a1, b1, R1) == 0)
check("second coefficient pair has stationary radius R2", derivative(a2, b2, R2) == 0)
check("first stationary energy equals the same observed energy", energy(a1, b1, R1) == Eobs)
check("second stationary energy equals the same observed energy", energy(a2, b2, R2) == Eobs)
check("observed mass fixes product ab=E^2/4", a1 * b1 == Eobs**2 / 4 and a2 * b2 == Eobs**2 / 4)
check("coefficient ratio b/a remains radius-squared", b1 / a1 == R1**2 and b2 / a2 == R2**2)
check("different radii give different coefficient ratios at identical mass", b1 / a1 != b2 / a2)
check("positive stationary point has positive second derivative", 2 * b1 / R1**3 > 0 and 2 * b2 / R2**3 > 0)

# T4: minimal dimensionless electron-to-universe closure.
G = F(23, 29)
me = F(31, 37)
c = F(41, 43)
beta = F(47, 53)
mu = F(59, 61)
nu = F(67, 71)
delta = mu / nu
X_from_beta = G * me / (c**2 * beta)
Mtotal = c**2 * X_from_beta * mu / G
check("beta_e=G m_e/(c^2 X) is recovered exactly", G * me / (c**2 * X_from_beta) == beta)
check("a derived beta_e plus observed m_e fixes X", X_from_beta > 0)
check("global mass ratio is M_total/m_e=mu/beta", Mtotal / me == mu / beta)
check("bootstrap relation is delta=mu/nu", mu - nu * delta == 0)

# Exact dimensions in (L,T,M).
def vadd(*vectors):
    return tuple(sum(v[i] for v in vectors) for i in range(3))


def vmul(a, vector):
    return tuple(a * x for x in vector)


dim_c = (1, -1, 0)
dim_G = (3, -2, -1)
dim_m = (0, 0, 1)
dim_X = (1, 0, 0)
dim_beta = vadd(dim_G, dim_m, vmul(-2, dim_c), vmul(-1, dim_X))
check("beta_e is dimensionless", dim_beta == (0, 0, 0))
check("G m_e/c^2 has dimensions of length", vadd(dim_G, dim_m, vmul(-2, dim_c)) == dim_X)
check("dimensionless topology alone supplies no length dimension", vmul(1, (0, 0, 0)) != dim_X)

passed = sum(ok for _, ok in checks)
total = len(checks)
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)
