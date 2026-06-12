#!/usr/bin/env python3
"""
VERIFIER EPSILON — independent symbolic reproduction for D-RECYCLING-COUPLING-ACTION-1.
Written from scratch (not a rerun of dispatch scripts). Canonical Form-T (CG §4.4):
  R1: G' + (kappa/r - phi') G - (m e^{phi} + E e^{2phi}) F = 0
  R2: F' + (-kappa/r - phi') F - (m e^{phi} - E e^{2phi}) G = 0
Perturb phi -> phi + eps*dphi (G,F,E,m,kappa fixed). First order in eps.
"""
import sympy as sp

r = sp.symbols('r', positive=True)
kap, m, E, eps = sp.symbols('kappa m E eps', real=True)
phi = sp.Function('phi')
dphi = sp.Function('dphi')
G = sp.Function('G')
F = sp.Function('F')

ph  = phi(r)
php = sp.diff(ph, r)
dp  = dphi(r)
dpp = sp.diff(dp, r)
g, f = G(r), F(r)
gp, fp = sp.diff(g, r), sp.diff(f, r)

# Residuals (LHS - RHS = 0 form)
R1 = gp + (kap/r - php)*g - (m*sp.exp(ph) + E*sp.exp(2*ph))*f
R2 = fp + (-kap/r - php)*f - (m*sp.exp(ph) - E*sp.exp(2*ph))*g

# First-order variation: substitute phi -> phi + eps*dphi, differentiate in eps at 0
def first_order(R):
    Rp = R.subs(ph, ph + eps*dp)
    return sp.expand(sp.diff(Rp, eps).subs(eps, 0).doit())

dR1 = first_order(R1)
dR2 = first_order(R2)
print("delta R1 =", sp.simplify(dR1))
print("delta R2 =", sp.simplify(dR2))

# ============ TASK 1: diagonal contraction -(G dR1 + F dR2) ============
diag = sp.expand(-(g*dR1 + f*dR2))
diag = sp.expand(sp.simplify(diag))
print("\n--- TASK 1: diagonal contraction -(G dR1 + F dR2) ---")
print("diag =", diag)

coeff_dpp = sp.simplify(diag.coeff(dpp))
print("coeff of dphi'(r):", coeff_dpp)
print("  == (G^2+F^2)?  ", sp.simplify(coeff_dpp - (g**2 + f**2)) == 0)

remainder = sp.simplify(sp.expand(diag - coeff_dpp*dpp))
print("non-derivative (dphi) remainder:", remainder)
print("  == 2 m e^{phi} dphi G F ?  ",
      sp.simplify(remainder - 2*m*sp.exp(ph)*dp*g*f) == 0)

# ============ TASK 2: the two E e^{2phi} pieces equal & opposite ============
print("\n--- TASK 2: E e^{2phi} channel cancellation in diagonal contraction ---")
# extract the E-dependent part of each contracted residual piece
piece1 = sp.expand(-g*dR1)   # contribution to diag from eq1
piece2 = sp.expand(-f*dR2)   # contribution to diag from eq2
# isolate the coefficient of E in each (the e^{2phi} eigenvalue-coupling channel)
E1 = sp.expand(piece1.coeff(E))*E
E2 = sp.expand(piece2.coeff(E))*E
print("E-piece from eq1 (in -G dR1):", sp.simplify(E1))
print("E-piece from eq2 (in -F dR2):", sp.simplify(E2))
print("sum of E-pieces:", sp.simplify(E1 + E2))
print("  equal & opposite (sum==0)?  ", sp.simplify(E1 + E2) == 0)

# Also confirm magnitude of each is 2 E e^{2phi} GF (up to sign)
print("E1 == -2 E e^{2phi} G F dphi ?", sp.simplify(E1 - (-2*E*sp.exp(2*ph)*g*f*dp)) == 0)
print("E2 == +2 E e^{2phi} G F dphi ?", sp.simplify(E2 - (+2*E*sp.exp(2*ph)*g*f*dp)) == 0)

# ============ TASK 3: genuine first-order eigenvalue shift (off-diagonal/Rayleigh) ============
print("\n--- TASK 3: genuine eigenvalue shift (Hellmann-Feynman / Rayleigh) ---")
# Off-diagonal contraction F*dR1 - G*dR2 isolates the energy response.
offdiag = sp.expand(sp.simplify(f*dR1 - g*dR2))
print("F dR1 - G dR2 =", offdiag)
# coefficient of dphi (non-derivative): the energy-shift density
coeff_off_dpp = sp.simplify(offdiag.coeff(dpp))
print("coeff of dphi' in offdiag:", coeff_off_dpp)
off_rem = sp.simplify(sp.expand(offdiag - coeff_off_dpp*dpp))
print("offdiag dphi-coefficient (energy-shift density):", off_rem)

# Rayleigh route: from R1*F - R2*G isolate E:
#   E e^{2phi}(G^2+F^2) = 2 kappa GF/r + F G' - G F' - m e^{phi}(F^2-G^2)
N = 2*kap*g*f/r + f*gp - g*fp - m*sp.exp(ph)*(f**2 - g**2)
D = sp.exp(2*ph)*(g**2 + f**2)
def fo(expr):
    e = expr.subs(ph, ph + eps*dp)
    return sp.simplify(sp.diff(e, eps).subs(eps, 0).doit())
dN = fo(N)
dD = fo(D)
dE_density = sp.expand(sp.simplify(dN - E*dD))   # numerator integrand of delta E
print("\nRayleigh dE density integrand (dN - E dD):", dE_density)
# check it is density-weighted (proportional to (G^2+F^2)) not bare GF
factored = sp.factor(dE_density)
print("factored:", factored)
print("contains (G^2+F^2) factor?  ", sp.simplify(factored / (g**2 + f**2)).is_polynomial(g, f) or
      ((g**2 + f**2) in sp.Mul.make_args(factored)))
