#!/usr/bin/env python3
"""Exact checks for UDT_GLOBAL_BOOTSTRAP_DERIVATION_RESULTS.md.

This verifies the encoded geometry, closure, conservation, and scale algebra.  It does not prove
that a bootstrap window exists, that it is narrow, that WR-L is the complete global cell, that an
action is unique, or that a carrier is physical.
"""

import sympy as sp


passed = 0


def check(label, condition):
    global passed
    if condition is not True and condition != sp.S.true:
        raise AssertionError(f"FAIL: {label}: {sp.simplify(condition)}")
    passed += 1
    print(f"PASS {passed:02d}: {label}")


def geometry(metric, coords):
    dim = len(coords)
    inv = sp.simplify(metric.inv())
    gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                gamma[a][b][c] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inv[a, d]
                        * (
                            sp.diff(metric[d, c], coords[b])
                            + sp.diff(metric[d, b], coords[c])
                            - sp.diff(metric[b, c], coords[d])
                        )
                        for d in range(dim)
                    )
                )
    ricci = sp.MutableDenseMatrix(dim, dim, [0] * (dim * dim))
    for a in range(dim):
        for b in range(dim):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(gamma[c][a][b], coords[c])
                    - sp.diff(gamma[c][a][c], coords[b])
                    + sum(
                        gamma[c][c][d] * gamma[d][a][b]
                        - gamma[c][b][d] * gamma[d][a][c]
                        for d in range(dim)
                    )
                    for c in range(dim)
                )
            )
    scalar = sp.simplify(sum(inv[a, b] * ricci[a, b] for a in range(dim) for b in range(dim)))
    einstein_cov = sp.simplify(ricci - sp.Rational(1, 2) * metric * scalar)
    einstein_mixed = sp.simplify(inv * einstein_cov)
    return inv, ricci, scalar, einstein_mixed


# 1. Conditional WR-L static-region geometry.
t, r, th, ph = sp.symbols("t r th ph", real=True)
X, G, M, c = sp.symbols("X G M c", positive=True)
A = sp.Function("A")(r)
metric = sp.diag(-A, 1 / A, r**2, r**2 * sp.sin(th) ** 2)
inv, ricci, R4, Gmixed = geometry(metric, (t, r, th, ph))
R_expected = -sp.diff(A, r, 2) - 4 * sp.diff(A, r) / r - 2 * (A - 1) / r**2
check("reciprocal spherical Ricci scalar", sp.simplify(R4 - R_expected) == 0)

A_WRL = 1 - r / X
R_WRL = sp.simplify(R4.subs(A, A_WRL).doit())
G_WRL = sp.simplify(Gmixed.subs(A, A_WRL).doit())
check("WR-L Ricci scalar is 6/(X r)", sp.simplify(R_WRL - 6 / (X * r)) == 0)
check("WR-L mixed Gtt is -2/(X r)", sp.simplify(G_WRL[0, 0] + 2 / (X * r)) == 0)
check("WR-L mixed Grr is -2/(X r)", sp.simplify(G_WRL[1, 1] + 2 / (X * r)) == 0)
check("WR-L mixed angular component is -1/(X r)", sp.simplify(G_WRL[2, 2] + 1 / (X * r)) == 0)
check("WR-L cannot be EH+constant-Lambda vacuum", sp.diff(R_WRL, r) != 0 and sp.simplify(G_WRL[0, 0] - G_WRL[2, 2]) != 0)


# 2. Proper volume of the conditional static region 0<r<X.
u = sp.symbols("u", nonnegative=True)
radial_integral = sp.integrate(u**2 / sp.sqrt(1 - u), (u, 0, 1))
check("dimensionless WR-L volume integral is 16/15", sp.simplify(radial_integral - sp.Rational(16, 15)) == 0)
V_WRL = sp.simplify(4 * sp.pi * X**3 * radial_integral)
nu = sp.Rational(64, 15) * sp.pi
check("conditional WR-L proper volume is (64 pi/15) X^3", sp.simplify(V_WRL - nu * X**3) == 0)
proper_radius = X * sp.integrate(1 / sp.sqrt(1 - u), (u, 0, 1))
check("conditional WR-L horizon is at finite proper radius 2X", sp.simplify(proper_radius - 2 * X) == 0)


# 3. Density, compactness, and alpha-window relations.
rho_bar = sp.simplify(M / V_WRL)
rho_expected = 15 * M / (64 * sp.pi * X**3)
check("conditional average density", sp.simplify(rho_bar - rho_expected) == 0)
delta = sp.simplify(G * rho_bar * X**2 / c**2)
chi = G * M / (c**2 * X)
check("dimensionless density equals compactness divided by volume factor", sp.simplify(delta - chi / nu) == 0)
alpha = sp.symbols("alpha", positive=True)
check("X=alpha GM/c^2 implies delta=1/(nu alpha)", sp.simplify(delta.subs(X, alpha * G * M / c**2) - 1 / (nu * alpha)) == 0)

dminus, dplus = sp.symbols("dminus dplus", positive=True)
chi_minus, chi_plus = nu * dminus, nu * dplus
alpha_lower, alpha_upper = 1 / (nu * dplus), 1 / (nu * dminus)
check("density-window lower compactness map", sp.simplify(chi_minus / nu - dminus) == 0)
check("density-window upper compactness map", sp.simplify(chi_plus / nu - dplus) == 0)
check("density-window alpha endpoints invert", sp.simplify(1 / alpha_lower - chi_plus) == 0 and sp.simplify(1 / alpha_upper - chi_minus) == 0)


# 4. A window is a continuum constraint, not a unique equation.
s = sp.symbols("s", real=True)
d_family = dminus + s * (dplus - dminus)
check("window parametrization has two distinct endpoints", sp.simplify(d_family.subs(s, 0) - dminus) == 0 and sp.simplify(d_family.subs(s, 1) - dplus) == 0)
check("nonzero window does not pick one density", sp.diff(d_family, s) != 0)


# 5. Global mass-response fixed point.
mu = sp.Function("mu")
M_pred = c**2 * X * mu(delta) / G
chi_pred = sp.simplify(G * M_pred / (c**2 * X))
check("dimensionless mass response equals predicted compactness", sp.simplify(chi_pred - mu(delta)) == 0)
check("WR-L bootstrap fixed point is nu*delta=mu(delta)", sp.simplify(chi.subs(M, M_pred) - mu(delta)) == 0 and sp.simplify(chi - nu * delta) == 0)

dstar, aa, bb = sp.symbols("dstar aa bb", positive=True)
mu1 = nu * dstar + aa * (delta - dstar) ** 2
mu2 = nu * dstar + bb * (delta - dstar) ** 4
check("two distinct response laws share the same bootstrap root", sp.simplify(mu1.subs(delta, dstar) - nu * dstar) == 0 and sp.simplify(mu2.subs(delta, dstar) - nu * dstar) == 0)
check("shared bootstrap root does not reconstruct the response law", sp.simplify(mu1 - mu2) != 0)


# 6. Conservation and volume evolution.
tau = sp.symbols("tau", real=True)
Mt = sp.Function("M")(tau)
Xt = sp.Function("X")(tau)
ct = sp.Function("c")(tau)
rho_t = Mt / (nu * Xt**3)
delta_t = G * Mt / (nu * ct**2 * Xt)
rho_logdot = sp.simplify(sp.diff(rho_t, tau) / rho_t)
delta_logdot = sp.simplify(sp.diff(delta_t, tau) / delta_t)
check("density evolution identity", sp.simplify(rho_logdot - (sp.diff(Mt, tau) / Mt - 3 * sp.diff(Xt, tau) / Xt)) == 0)
check("dimensionless-density evolution identity", sp.simplify(delta_logdot - (sp.diff(Mt, tau) / Mt - sp.diff(Xt, tau) / Xt - 2 * sp.diff(ct, tau) / ct)) == 0)
static_mass_c = {sp.diff(Mt, tau): 0, sp.diff(ct, tau): 0}
check("constant mass and c leave delta controlled by X", sp.simplify(delta_logdot.subs(static_mass_c) + sp.diff(Xt, tau) / Xt) == 0)
fully_static = {sp.diff(Mt, tau): 0, sp.diff(Xt, tau): 0, sp.diff(ct, tau): 0}
check("constant mass, X, and c keep density fixed", sp.simplify(rho_logdot.subs(fully_static)) == 0 and sp.simplify(delta_logdot.subs(fully_static)) == 0)


# 7. One compactness equation cannot determine c and X separately.
scale = sp.symbols("scale", positive=True)
chi_rescaled = sp.simplify(G * M / ((scale * c) ** 2 * (X / scale**2)))
check("c->scale*c and X->X/scale^2 preserve compactness", sp.simplify(chi_rescaled - chi) == 0)


# 8. Standalone flat L2+L4 scale mode contains no universal density.
C2, C4, xi, kap, Rsize = sp.symbols("C2 C4 xi kap Rsize", positive=True)
dvar = sp.symbols("delta_U", positive=True)
Ecarrier = C2 * xi * Rsize + C4 * kap / Rsize
Rstar = sp.sqrt(C4 * kap / (C2 * xi))
check("flat L2+L4 stationary scale", sp.simplify(sp.diff(Ecarrier, Rsize).subs(Rsize, Rstar)) == 0)
check("flat L2+L4 scale curvature is positive", sp.simplify(sp.diff(Ecarrier, Rsize, 2).subs(Rsize, Rstar)) > 0)
check("standalone flat carrier has no total-density variable", sp.diff(Ecarrier, dvar) == 0 and sp.diff(Rstar, dvar) == 0)


# 9. Electron calibration remains one product condition.
me = sp.symbols("me", positive=True)
E_star_sq = 4 * C2 * C4 * xi * kap
product_anchor = me**2 * c**4 / (4 * C2 * C4)
check("electron anchor fixes xi*kappa product", sp.simplify(E_star_sq.subs(kap, product_anchor / xi) - me**2 * c**4) == 0)
free_ratio_family = sp.simplify((product_anchor / xi) / xi)
check("electron anchor leaves coupling ratio free", sp.diff(free_ratio_family, xi) != 0)


print(f"\nRESULT: {passed}/{passed} checks pass")
