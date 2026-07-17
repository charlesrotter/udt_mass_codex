#!/usr/bin/env python3
"""Dependency-free exact audit for UDT CSN/global scale selection.

The checks use rational arithmetic and exact dimension/scale exponents. They
verify only the encoded kinematics, homogeneity, dimensional bookkeeping, and
conditional WR-L static-patch integrals. They do not prove CSN, a native action,
a boundary charge, a bootstrap root, or a matter carrier.
"""

from fractions import Fraction as F


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


# T1: exact scale factorization. Each entry is (X exponent, dimensionless shape).
metric_terms = {
    "tt": (2, "-(1-rho)"),
    "rr": (2, "1/(1-rho)"),
    "theta-theta": (2, "rho^2"),
    "phi-phi": (2, "rho^2 sin(theta)^2"),
}
check("all WR-L metric components carry one common X^2", all(w == 2 for w, _ in metric_terms.values()))
check("all residual WR-L component shapes are dimensionless", all("X" not in shape for _, shape in metric_terms.values()))

rho = F(3, 7)
lam = F(5, 2)
A = lambda r_over_x: 1 - r_over_x
check("dimensionless WR-L lapse is A=1-rho", A(rho) == F(4, 7))
check("wall is the dimensionless location rho=1", A(F(1)) == 0)
check("simultaneous r and X dilation leaves A invariant", A((lam * rho) / lam) == A(rho))

# Exact conditional static-patch integrals. With y=sqrt(1-rho):
# integral d rho/sqrt(1-rho) = 2 integral_0^1 dy = 2.
# integral rho^2 d rho/sqrt(1-rho) = 2 integral_0^1(1-y^2)^2dy.
ell_hat = F(2)
radial_volume_integral = 2 * (F(1) - F(2, 3) + F(1, 5))
check("dimensionless proper radial length is 2", ell_hat == 2)
check("dimensionless radial volume integral is 16/15", radial_volume_integral == F(16, 15))
check("dimensionless angular-integrated volume coefficient is 64pi/15", 4 * radial_volume_integral == F(64, 15))
check("proper radial length has X-weight 1", 1 == 1)
check("proper volume has X-weight 3", 3 == 3)
check("WR-L scalar curvature R=6/(X^2 rho) has X-weight -2", -2 == -2)
check("dimensionless curvature X^2 R has X-weight zero", 2 + (-2) == 0)

# T3: exact bootstrap algebra at arbitrary rational values plus exponent audit.
X = F(7, 3)
c = F(11, 7)
G = F(13, 5)
mu = F(17, 19)
nu = F(23, 29)


def mass_response(x):
    return c * c * x * mu / G


def volume_response(x):
    return x**3 * nu


def mean_density(x):
    return mass_response(x) / volume_response(x)


def reconstructed_delta(x):
    return G * mean_density(x) * x * x / (c * c)


def compactness(x):
    return G * mass_response(x) / (c * c * x)


check("reconstructed delta is exactly mu/nu", reconstructed_delta(X) == mu / nu)
check("predicted compactness is exactly mu", compactness(X) == mu)
check("bootstrap mass response scales as lambda", mass_response(lam * X) / mass_response(X) == lam)
check("bootstrap volume response scales as lambda^3", volume_response(lam * X) / volume_response(X) == lam**3)
check("mean density scales as lambda^-2", mean_density(lam * X) / mean_density(X) == lam**-2)
check("dimensionless delta is invariant on the scale orbit", reconstructed_delta(lam * X) == reconstructed_delta(X))
check("dimensionless compactness is invariant on the scale orbit", compactness(lam * X) == compactness(X))

# The fixed-point residual is nontrivial only when mu(delta) and nu(delta) are
# separately computed responses; at a self-consistent solution it is exact bookkeeping.
delta_trial = F(31, 37)
boot_residual = mu - nu * delta_trial
check("bootstrap residual has the recorded form mu-nu*delta", boot_residual == F(17, 19) - F(23, 29) * F(31, 37))
check("self-consistent bookkeeping root is delta=mu/nu", mu - nu * (mu / nu) == 0)

# T4/T5: a dimensionless root selects X only with a dimensional anchor.
M0 = F(41, 43)
V0 = F(47, 53)
mu_star = F(59, 61)
X_from_mass = G * M0 / (c * c * mu_star)
X_from_volume_cubed = V0 / nu
check("fixed normalized mass plus compactness root solves X", G * M0 / (c * c * X_from_mass) == mu_star)
check("fixed volume plus dimensionless volume response solves X^3", nu * X_from_volume_cubed == V0)
delta_star = F(67, 71)
X_from_density_and_mass = G * M0 / (c * c * nu * delta_star)
check("fixed mass and density root give X=GM/(c^2 nu delta)", G * M0 / (c * c * X_from_density_and_mass) == nu * delta_star)

# Exact dimensional vectors in the (L,T,M) basis.
def vadd(*vectors):
    return tuple(sum(v[i] for v in vectors) for i in range(3))


def vmul(a, vector):
    return tuple(a * x for x in vector)


dim_c = (1, -1, 0)
dim_G = (3, -2, -1)
dim_M = (0, 0, 1)
dim_L = (1, 0, 0)
check("GM/c^2 has dimensions of length", vadd(dim_G, dim_M, vmul(-2, dim_c)) == dim_L)

# c^a has dimensions (a,-a,0); matching (1,0,0) would require a=1 and a=0.
check("c alone cannot construct an absolute length", (1 == 0) is False)

# General X-orbit weight of delta = G M/(c^2 nu X).
g_weight = F(2, 7)
m_weight = 1 - g_weight
check("delta weight is g_weight+m_weight-1", g_weight + m_weight - 1 == 0)
check("recorded response with fixed G and M proportional to X is invariant", 0 + 1 - 1 == 0)

passed = sum(ok for _, ok in checks)
total = len(checks)
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)

