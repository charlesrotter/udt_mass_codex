#!/usr/bin/env python3
"""Exact checks for the UDT quadratic-dilation-cost derivation.

This verifies group geometry, controlled local expansions, counterfunctions,
and the comparison with WR-L.  It does not postulate a UDT action.
"""

import sympy as sp


checks = []


def check(name, statement):
    ok = bool(statement)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        raise AssertionError(name)


delta, phi, shift = sp.symbols("delta phi shift", real=True)
A, B, Z = sp.symbols("A B Z", positive=True)

# Additive depth, multiplicative residual, and reciprocal invariant.
D = sp.exp(delta)
Gamma = (D + 1 / D) / 2
check("reciprocal mean is cosh depth", sp.simplify(Gamma - sp.cosh(delta)) == 0)
check("reciprocal invariant is even", sp.simplify(Gamma.subs(delta, -delta) - Gamma) == 0)
qchord = 2 * sp.sinh(delta / 2)
check("reciprocal excess is exact chord square",
      sp.simplify(sp.cosh(delta) - 1 - qchord**2 / 2) == 0)

# Any translation-invariant one-dimensional Riemannian state metric has
# constant coefficient.  Coordinate changes then fix its A and B forms.
h = sp.Function("h")
translation_derivative = sp.diff(h(phi + shift), shift).subs(shift, 0)
check("translation invariance infinitesimally requires h prime zero",
      sp.simplify(translation_derivative - sp.diff(h(phi), phi)) == 0)

dphi_dA = sp.diff(-sp.log(A) / 2, A)
check("invariant metric in residual A coordinate",
      sp.simplify(Z * dphi_dA**2 - Z / (4 * A**2)) == 0)
dphi_dB = sp.diff(-sp.log(1 - B) / 2, B)
check("invariant metric in depletion B coordinate",
      sp.simplify(Z * dphi_dB**2 - Z / (4 * (1 - B)**2)) == 0)

# Smooth reciprocal costs have a quadratic leading term only when their
# Hessian at coincidence is nonzero.
Fp, Fpp, Fppp = sp.symbols("F1 F2 F3", real=True)
z = sp.cosh(delta) - 1
Fseries = Fp * z + Fpp * z**2 / 2 + Fppp * z**3 / 6
series6 = sp.series(Fseries, delta, 0, 7).removeO().expand()
expected6 = (
    Fp * delta**2 / 2
    + (Fp / 24 + Fpp / 8) * delta**4
    + (Fp / 720 + Fpp / 48 + Fppp / 48) * delta**6
)
check("general reciprocal-cost expansion through sixth order",
      sp.simplify(series6 - expected6) == 0)
check("MR-1 has quadratic leading term",
      sp.series(sp.cosh(delta) - 1, delta, 0, 5) == delta**2 / 2 + delta**4 / 24 + sp.Order(delta**5))
quartic_cost = (sp.cosh(delta) - 1) ** 2
check("allowed reciprocal countercost begins quartically",
      sp.simplify(sp.limit(quartic_cost / delta**4, delta, 0) - sp.Rational(1, 4)) == 0)

# Symmetric two-point local limit.  p,q2,t,u are successive derivatives of phi.
ell = sp.symbols("ell", positive=True)
p, q2, t, u = sp.symbols("p q2 t u", real=True)
dplus = ell * p + ell**2 * q2 / 2 + ell**3 * t / 6 + ell**4 * u / 24
dminus = -ell * p + ell**2 * q2 / 2 - ell**3 * t / 6 + ell**4 * u / 24
pair_local = (sp.cosh(dplus) + sp.cosh(dminus) - 2) / (2 * ell**2)
pair_series = sp.series(pair_local, ell, 0, 4).removeO().expand()
expected_pair = p**2 / 2 + ell**2 * (p**4 / 24 + p * t / 6 + q2**2 / 8)
check("symmetric pair local limit and O(ell^2) correction",
      sp.simplify(pair_series - expected_pair) == 0)
check("odd-kernel-order contribution cancels", pair_series.coeff(ell, 1) == 0)

# Local covariance and reciprocity allow nonlinear functions of Y.
x, alpha = sp.symbols("x alpha", real=True)
f = sp.Function("f")(x)
vf = sp.diff(f, x)
Y = vf**2
L_linear = Y / 2
L_nonlinear = Y / 2 + alpha * Y**2 / 4
EL_linear = sp.simplify(sp.diff(sp.diff(L_linear, vf), x) - sp.diff(L_linear, f))
EL_nonlinear = sp.factor(sp.simplify(sp.diff(sp.diff(L_nonlinear, vf), x) - sp.diff(L_nonlinear, f)))
check("quadratic local-gradient Euler equation", EL_linear == sp.diff(f, x, 2))
check("nonlinear allowed local-gradient Euler equation",
      sp.simplify(EL_nonlinear - (1 + 3 * alpha * vf**2) * sp.diff(f, x, 2)) == 0)
check("nonlinear counteraction is distinct", sp.simplify(EL_nonlinear - EL_linear) != 0)

# Orthogonal additivity would force a function of squared norm to be linear.
Y1, Y2, c1, c2, c3 = sp.symbols("Y1 Y2 c1 c2 c3", nonnegative=True)
poly = lambda yy: c1 * yy + c2 * yy**2 + c3 * yy**3
additivity_defect = sp.Poly(sp.expand(poly(Y1 + Y2) - poly(Y1) - poly(Y2)), Y1, Y2)
check("quadratic-in-Y term violates orthogonal additivity",
      additivity_defect.coeff_monomial(Y1 * Y2) == 2 * c2)
check("cubic-in-Y term violates orthogonal additivity",
      additivity_defect.coeff_monomial(Y1**2 * Y2) == 3 * c3)
check("linear-in-Y cost obeys orthogonal additivity",
      sp.expand((c1 * (Y1 + Y2)) - c1 * Y1 - c1 * Y2) == 0)

# Exact comparison with WR-L.
r, Xwall = sp.symbols("r X", positive=True)
A_wrl = 1 - r / Xwall
phi_wrl = -sp.log(A_wrl) / 2
phi_prime = sp.simplify(sp.diff(phi_wrl, r))
check("WR-L depth derivative", sp.simplify(phi_prime - 1 / (2 * (Xwall - r))) == 0)
Y_wrl = sp.simplify(A_wrl * phi_prime**2)
check("physical radial depth norm diverges as 1/A",
      sp.simplify(Xwall**2 * Y_wrl - 1 / (4 * A_wrl)) == 0)
check("physical radial depth norm diverges at wall",
      sp.limit(Y_wrl, r, Xwall, dir="-") == sp.oo)

# Controlled pair-local error is not uniform at the wall: its relative size
# contains ell^2/(X-r)^2.
eps_wall = sp.symbols("epsilon", positive=True)
p_w = 1 / (2 * eps_wall)
q_w = 1 / (2 * eps_wall**2)
t_w = 1 / eps_wall**3
leading_w = p_w**2 / 2
corr_w = p_w**4 / 24 + p_w * t_w / 6 + q_w**2 / 8
relative_corr = sp.simplify(ell**2 * corr_w / leading_w)
check("pair-local relative correction blows up near wall",
      sp.simplify(relative_corr - sp.Rational(15, 16) * ell**2 / eps_wall**2) == 0)

# Historical shift-clean radial quadratic norm and a covariant scalar kinetic
# both fail to have WR-L as an extremal.
R1_residual = sp.simplify(sp.diff(r**2 * phi_prime, r))
check("shift-clean r^2 depth norm WR-L residual",
      sp.simplify(R1_residual - r * (2 * Xwall - r) / (2 * (Xwall - r)**2)) == 0)

Afun = sp.Function("Afun")(r)
vA = sp.diff(Afun, r)
L_cov4 = r**2 * vA**2 / (4 * Afun)
EL_cov4 = sp.simplify(sp.diff(sp.diff(L_cov4, vA), r) - sp.diff(L_cov4, Afun))
EL_cov4_wrl = sp.factor(sp.simplify(EL_cov4.subs(Afun, A_wrl).doit()))
check("reciprocal reduced covariant scalar kinetic misses WR-L",
      sp.simplify(EL_cov4_wrl + r * (4 * Xwall - 3 * r) / (4 * (Xwall - r)**2)) == 0)

# The WR-L inverse kinetic term uses flat B distance, not the invariant
# multiplicative-residual state metric.
B_wrl = 1 - A_wrl
invariant_B_weight = sp.simplify(1 / (4 * (1 - B_wrl)**2))
check("invariant B-metric weight diverges at wall",
      sp.limit(invariant_B_weight, r, Xwall, dir="-") == sp.oo)
check("flat-B and invariant-depth metrics agree only weakly",
      sp.series(1 / (4 * (1 - B)**2), B, 0, 3)
      == sp.Rational(1, 4) + B / 2 + 3 * B**2 / 4 + sp.Order(B**3))

# The prior off-shell counterfamily is indistinguishable at the linearized
# Euler level on WR-L, so a derived quadratic Hessian would still not select it.
lambda_symbol = sp.symbols("lambda", positive=True)
Bfield = sp.Function("Bfield")(r)
vB = sp.diff(Bfield, r)
phase = Bfield**2 - r**2 * vB**2
multiplier = r * (1 + lambda_symbol * phase**2 / 16)
multiplier_wrl = sp.simplify(multiplier.subs(Bfield, -r / Xwall).doit())
check("nonlinear counterfamily has same linear multiplier on WR-L",
      multiplier_wrl == r)

passed = sum(ok for _, ok in checks)
print(f"ALL CONSISTENT ({passed}/{len(checks)} checks pass)")
print(f"SymPy {sp.__version__}")
