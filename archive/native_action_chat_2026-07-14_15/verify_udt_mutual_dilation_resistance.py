#!/usr/bin/env python3
"""Exact algebra checks for the UDT mutual-dilation resistance derivation.

This verifies encoded identities, derivatives, variations, series, and route
comparisons.  It does not prove that MR-1 is the UDT action, that a pair kernel
or continuum measure is native, that a carrier is complete, or that the
candidate's invariant/covariant inventory is exhaustive.
"""

import sympy as sp


passed = 0
failed = 0


def check(label, condition):
    global passed, failed
    ok = bool(condition)
    if ok:
        passed += 1
        print(f"PASS {passed + failed:02d}: {label}")
    else:
        failed += 1
        print(f"FAIL {passed + failed:02d}: {label}")


u = sp.symbols("u", real=True, nonnegative=True)
p = sp.symbols("p", real=True)
R_u = 1 / sp.sqrt(1 - u**2) - 1
R_p = sp.cosh(p) - 1
D = sp.exp(p)

# A. Reciprocal invariant and MR-1
check("reciprocal average equals cosh",
      sp.simplify((D + 1 / D) / 2 - sp.cosh(p)) == 0)
check("MR-1 is reciprocal-even", sp.simplify(R_p.subs(p, -p) - R_p) == 0)
check("MR-1 vanishes at zero difference", R_p.subs(p, 0) == 0)
check("hyperbolic branch gives gamma identity",
      sp.trigsimp((R_u + 1).subs(u, sp.tanh(p))**2 - sp.cosh(p)**2) == 0)
edge_eps = sp.symbols("edge_eps", positive=True)
check("MR-1 diverges at the distance bound",
      sp.limit(R_u.subs(u, 1-edge_eps), edge_eps, 0, dir="+") == sp.oo)

Rp = sp.diff(R_u, u)
Rpp = sp.diff(Rp, u)
check("first derivative", sp.simplify(Rp - u / (1 - u**2)**sp.Rational(3, 2)) == 0)
check("second derivative",
      sp.simplify(Rpp - (1 + 2*u**2) / (1 - u**2)**sp.Rational(5, 2)) == 0)
check("small-u expansion",
      sp.series(R_u, u, 0, 7) ==
      u**2/2 + 3*u**4/8 + 5*u**6/16 + sp.Order(u**7))
check("small-depth expansion",
      sp.series(R_p, p, 0, 7) ==
      p**2/2 + p**4/24 + p**6/720 + sp.Order(p**7))

# Reciprocity and divergence do not select MR-1 uniquely.
R_alt = sp.cosh(2*p) - 1
check("counterfunction is reciprocal-even", sp.simplify(R_alt.subs(p, -p) - R_alt) == 0)
check("counterfunction also vanishes at zero", R_alt.subs(p, 0) == 0)
check("counterfunction is genuinely distinct",
      sp.simplify(R_alt - 2*R_p) != 0)
check("counterfunction also diverges", sp.limit(R_alt, p, sp.oo) == sp.oo)

# B. Exact finite-pair variation on a connected three-node graph.
f1, f2, f3 = sp.symbols("f1 f2 f3", real=True)
w12, w13, w23 = sp.symbols("w12 w13 w23", positive=True)
E = (w12*(sp.cosh(f1-f2)-1) +
     w13*(sp.cosh(f1-f3)-1) +
     w23*(sp.cosh(f2-f3)-1))
fs = sp.Matrix([f1, f2, f3])
grad = sp.Matrix([sp.diff(E, z) for z in fs])
H = sp.hessian(E, fs)
ones = sp.ones(3, 1)

check("common-depth shift gives zero total gradient",
      sp.simplify(sum(grad)) == 0)
check("Hessian has exact common-shift zero mode",
      all(sp.simplify(z) == 0 for z in H*ones))

d1, d2, d3 = sp.symbols("d1 d2 d3", real=True)
dv = sp.Matrix([d1, d2, d3])
q_expected = (
    w12*sp.cosh(f1-f2)*(d1-d2)**2 +
    w13*sp.cosh(f1-f3)*(d1-d3)**2 +
    w23*sp.cosh(f2-f3)*(d2-d3)**2
)
check("full Hessian quadratic form is weighted edge-square sum",
      sp.simplify((dv.T*H*dv)[0] - q_expected) == 0)

stationarity_identity = (
    (f1-f2)*w12*sp.sinh(f1-f2) +
    (f1-f3)*w13*sp.sinh(f1-f3) +
    (f2-f3)*w23*sp.sinh(f2-f3)
)
check("phi dot gradient gives stationarity sum",
      sp.simplify((fs.T*grad)[0] - stationarity_identity) == 0)

# C. Uniform scale mode and force sign.
lam, X, sigma = sp.symbols("lam X sigma", positive=True)
ua, ub, uc = sp.symbols("ua ub uc", positive=True)
wa, wb, wc = sp.symbols("wa wb wc", positive=True)
R = lambda z: 1/sp.sqrt(1-z**2) - 1
E_lam = sigma*(wa*R(lam*ua) + wb*R(lam*ub) + wc*R(lam*uc))
dE_lam = sp.diff(E_lam, lam)
d2E_lam = sp.diff(dE_lam, lam)
expected_dE = sigma*sum(
    w*z**2*lam/(1-(lam*z)**2)**sp.Rational(3, 2)
    for w, z in ((wa, ua), (wb, ub), (wc, uc))
)
expected_d2E = sigma*sum(
    w*z**2*(1+2*(lam*z)**2)/(1-(lam*z)**2)**sp.Rational(5, 2)
    for w, z in ((wa, ua), (wb, ub), (wc, uc))
)
check("positive-sign scale derivative",
      sp.simplify(dE_lam - expected_dE) == 0)
check("positive-sign scale convexity",
      sp.simplify(d2E_lam - expected_d2E) == 0)

d = sp.symbols("d", positive=True)
force_plus = -sp.diff(sigma*R(d/X), d)
force_minus = -sp.diff(-sigma*R(d/X), d)
check("positive energy sign gives attractive radial force",
      sp.simplify(force_plus + sigma*d/(X**2*(1-d**2/X**2)**sp.Rational(3, 2))) == 0)
check("negative energy sign reverses the force",
      sp.simplify(force_minus + force_plus) == 0)

# D. Controlled local expansion and kernel-range scaling.
eps, q, ell = sp.symbols("eps q ell", real=True)
affine_series = sp.series(sp.cosh(eps*q)-1, eps, 0, 7)
check("smooth affine pair expansion through sixth order",
      affine_series ==
      eps**2*q**2/2 + eps**4*q**4/24 + eps**6*q**6/720 + sp.Order(eps**7))
check("L2-normalized local limit suppresses quartic term",
      sp.simplify((ell**2 + ell**4)/ell**2 - (1 + ell**2)) == 0)
check("L4-normalized local limit makes quadratic term divergent",
      sp.simplify((ell**2 + ell**4)/ell**4 - (ell**-2 + 1)) == 0)

# E. Hyperbolic-angular carrier candidate.
a, b, s = sp.symbols("a b s", real=True)
Gamma_H = sp.cosh(a)*sp.cosh(b) - s*sp.sinh(a)*sp.sinh(b)
check("aligned angular states reduce to reciprocal depth difference",
      sp.trigsimp(Gamma_H.subs(s, 1) - sp.cosh(a-b)) == 0)

t, dp, dt = sp.symbols("t dp dt", real=True)
Gamma_near = (sp.cosh(a)*sp.cosh(a+eps*dp) -
              sp.sinh(a)*sp.sinh(a+eps*dp)*sp.cos(eps*dt))
near_series = sp.series(Gamma_near-1, eps, 0, 3).removeO()
check("hyperbolic-angular local metric",
      sp.trigsimp(near_series -
                  eps**2*(dp**2 + sp.sinh(a)**2*dt**2)/2) == 0)

same_depth_angular = sp.simplify(Gamma_H.subs({a: t, b: t}))
check("angular stiffness depends on absolute depth",
      sp.simplify(same_depth_angular - (1 + (1-s)*sp.sinh(t)**2)) == 0)
check("common depth shift is not a symmetry for angular mismatch",
      sp.simplify(sp.diff(same_depth_angular, t) -
                  2*(1-s)*sp.sinh(t)*sp.cosh(t)) == 0)
check("angular fiber collapses at zero depth",
      same_depth_angular.subs(t, 0) == 1)

# Normalized-gradient route has Frobenius/hypersurface-orthogonal restriction.
px, py, pz, qx, qy, qz = sp.symbols("px py pz qx qy qz", real=True)
pv = sp.Matrix([px, py, pz])
qv = sp.Matrix([qx, qy, qz])
check("normalized-gradient Frobenius triple product vanishes",
      sp.expand(pv.dot(qv.cross(pv))) == 0)

# F. Keep hyperbolic distance chart distinct from live WR-L areal chart.
y = sp.symbols("y", real=True)
A_wr = 1-y
u_from_wr = y/(2-y)
A_h = (1-u)/(1+u)
check("WR-L to hyperbolic-distance chart relation",
      sp.simplify(A_h.subs(u, u_from_wr) - A_wr) == 0)
check("identifying the two dimensionless radii is not valid",
      sp.simplify(A_h.subs(u, y) - A_wr) != 0)
Gamma_wr = (sp.sqrt(A_wr) + 1/sp.sqrt(A_wr))/2
check("reciprocal gamma expressed on WR-L areal radius",
      sp.simplify(Gamma_wr - (2-y)/(2*sp.sqrt(1-y))) == 0)

# G. The c-X-M dimensional statements are only one equation.
G, M, c, beta = sp.symbols("G M c beta", positive=True)
X_expr = beta*G*M/c**2
chi = G*M/(c**2*X_expr)
check("compactness from one dimensional closure", sp.simplify(chi - 1/beta) == 0)
check("c and X forms are algebraic rearrangements",
      sp.solve(sp.Eq(X, beta*G*M/c**2), c**2)[0] == beta*G*M/X)

print(f"\nRESULT: {passed}/{passed + failed} checks pass")
if failed:
    raise SystemExit(1)
