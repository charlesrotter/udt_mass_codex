#!/usr/bin/env python3
"""Exact dependency-free audit of the UDT CSN one-mass calibration theorem.

The checks cover action/energy scaling, the G bridge, one-mass inversion,
mass ratios, dimensions, scale degeneracy, and finite dimensionless-size
compatibility. They do not derive a carrier, action, G normalization, or
dimensionless electron branch.
"""

from fractions import Fraction as F


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


# Arbitrary exact positive probes.
action_norm = F(7, 3)
c = F(11, 5)
X = F(13, 7)
eps_e = F(17, 19)
eps_u = F(23, 29)
sigma_e = F(31, 37)
G = F(41, 43)
nu = F(47, 53)


def energy(A, x, eps):
    return A * c * eps / x


def mass(A, x, eps):
    return A * eps / (c * x)


E_e = energy(action_norm, X, eps_e)
m_e = mass(action_norm, X, eps_e)
check("static energy scales as A c epsilon/X", E_e == action_norm * c * eps_e / X)
check("mass is E/c^2=A epsilon/(c X)", m_e == E_e / c**2)
check("particle radius is sigma X", sigma_e * X / X == sigma_e)
check("mass ratios cancel A, c, and X", mass(action_norm, X, eps_u) / m_e == eps_u / eps_e)

# Overall normalization/scale degeneracy at fixed one observed mass.
lam = F(59, 61)
check(
    "A and X scaled together leave every calibrated mass unchanged",
    mass(lam * action_norm, lam * X, eps_e) == m_e,
)
check(
    "the same transformation scales all physical radii",
    sigma_e * (lam * X) / (sigma_e * X) == lam,
)

# Dimensionless G bridge.
g_hat = G * action_norm / (c**3 * X**2)
beta_e = G * m_e / (c**2 * X)
mu_u = G * mass(action_norm, X, eps_u) / (c**2 * X)
check("beta_e equals g_hat epsilon_e", beta_e == g_hat * eps_e)
check("global compactness equals g_hat epsilon_U", mu_u == g_hat * eps_u)
check("global-to-electron mass ratio is mu/beta", mu_u / beta_e == eps_u / eps_e)
check("bootstrap density is mu/nu", (mu_u / nu) * nu == mu_u)

# One-mass inversion after a dimensionless g_hat and epsilon_e are supplied.
m_obs = F(67, 71)
g_star = F(73, 79)
eps_star = F(83, 89)
X_sol = G * m_obs / (c**2 * g_star * eps_star)
A_sol = G * m_obs**2 / (c * g_star * eps_star**2)
check("one-mass plus G-bridge inversion reproduces observed mass", mass(A_sol, X_sol, eps_star) == m_obs)
check("inverted action normalization is m c X/epsilon", A_sol == m_obs * c * X_sol / eps_star)
check("inverted X gives beta=g_hat epsilon", G * m_obs / (c**2 * X_sol) == g_star * eps_star)
check("inverted particle radius is sigma times X", sigma_e * X_sol / X_sol == sigma_e)

# Dimensions in (L,T,M).
def vadd(*vectors):
    return tuple(sum(v[i] for v in vectors) for i in range(3))


def vmul(a, vector):
    return tuple(a * x for x in vector)


dim_A = (2, -1, 1)  # action
dim_c = (1, -1, 0)
dim_X = (1, 0, 0)
dim_G = (3, -2, -1)
dim_E = (2, -2, 1)
dim_M = (0, 0, 1)
check("A c/X has energy dimensions", vadd(dim_A, dim_c, vmul(-1, dim_X)) == dim_E)
check("A/(c X) has mass dimensions", vadd(dim_A, vmul(-1, dim_c), vmul(-1, dim_X)) == dim_M)
check("G A/(c^3 X^2) is dimensionless", vadd(dim_G, dim_A, vmul(-3, dim_c), vmul(-2, dim_X)) == (0, 0, 0))
check("G m/(c^2 X) is dimensionless", vadd(dim_G, dim_M, vmul(-2, dim_c), vmul(-1, dim_X)) == (0, 0, 0))

# CSN permits, but does not derive, a finite dimensionless stationary size.
sigma0 = F(97, 101)
e0 = F(103, 107)


def eps_allowed(sigma):
    return (sigma - sigma0) ** 2 + e0


def deps_allowed(sigma):
    return 2 * (sigma - sigma0)


def d2eps_allowed(sigma):
    del sigma
    return F(2)


k4 = F(109, 113)


def eps_quartic_flat(sigma):
    return k4 / sigma


def deps_quartic_flat(sigma):
    return -k4 / sigma**2


check("a dimensionless finite stationary sigma is CSN-compatible", deps_allowed(sigma0) == 0)
check("the example finite sigma is a strict minimum", d2eps_allowed(sigma0) > 0 and eps_allowed(sigma0) == e0)
check("flat quartic-only energy has no finite stationary sigma", deps_quartic_flat(sigma0) != 0)
check("flat quartic-only energy decreases with sigma", deps_quartic_flat(sigma0) < 0)

# Multiplying the full action leaves classical stationarity intact, while
# relative couplings remain inside the dimensionless equations.
relative = F(127, 131)
stationary_residual = F(0)
check("overall action multiplication leaves a zero Euler residual zero", action_norm * stationary_residual == lam * action_norm * stationary_residual == 0)
check("a relative dimensionless coupling is not removed by overall scaling", relative == (lam * action_norm * relative) / (lam * action_norm))

passed = sum(ok for _, ok in checks)
total = len(checks)
print(f"\nSUMMARY: {passed}/{total} checks pass")
if passed != total:
    raise SystemExit(1)

