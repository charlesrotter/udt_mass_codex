"""
S2: Symbolic Born-Oppenheimer (adiabatic/rigid-tracking) reduction of the
m=0 static quadratic form, and Liouville reduction to standard SL form.

Quadratic form around the demanded background (u = dF, b = da orthonormal):
  Q = int dy [ pi y^2 u'^2 + (1/4) y^2 b'^2 + (1/2) P_aa (b - ktil u)^2 ]
  ktil = a0/F0 = sqrt(4pi/3) kappa(y);  rank-1 exactness verified in S1.

BO level: substitute the rigid pointwise response b = ktil u (the exact
pointwise-static minimizer, ie. the scaling direction), keep radial
gradients of the response. Then Liouville-transform to kinetic pi y^2 w'^2
and read off mu_eff^BO(y) in the SL normalization
  (y^2 w')' = (lambda y^q + mu_eff) w.
Compare against N1's claim: mu_eff^W = 3 y^2 kappa'^2 / (3+kappa^2)^2.
"""
import sympy as sp

y = sp.Symbol('y', positive=True)
kap = sp.Function('kappa')(y)
u = sp.Function('u')(y)
w = sp.Function('w')(y)

ktil = sp.sqrt(4*sp.pi/3)*kap

# BO integrand: pi y^2 u'^2 + (1/4) y^2 ((ktil u)')^2
L_BO = sp.pi*y**2*sp.diff(u, y)**2 + sp.Rational(1,4)*y**2*sp.diff(ktil*u, y)**2
L_BO = sp.expand(L_BO)

# Liouville: u = w / sqrt(ptil), ptil = 1 + kappa^2/3  (so kinetic -> pi ptil y^2 u'^2 = pi y^2 w'^2 + ...)
ptil = 1 + kap**2/3
L_BO_w = L_BO.subs(u, w/sp.sqrt(ptil)).doit()
L_BO_w = sp.expand(sp.simplify(L_BO_w))

# Collect into  alpha(y) w'^2 + beta(y) w w' + gamma(y) w^2 ; then IBP: beta w w' -> -(1/2) beta' w^2
wp = sp.diff(w, y)
poly = sp.Poly(L_BO_w, wp, w)
alpha = poly.coeff_monomial(wp**2)
beta = poly.coeff_monomial(wp*w)
gamma = poly.coeff_monomial(w**2)
alpha = sp.simplify(alpha); beta = sp.simplify(beta); gamma = sp.simplify(gamma)
print("alpha (w'^2 coeff):", alpha)
print("  alpha - pi y^2 =", sp.simplify(alpha - sp.pi*y**2), "  [must be 0 for correct Liouville]")
gamma_eff = sp.simplify(gamma - sp.Rational(1,2)*sp.diff(beta, y))
print("gamma_eff (w^2 coeff after IBP):", sp.simplify(gamma_eff))

# SL normalization: L = pi[ y^2 w'^2 + mu_eff w^2 ]  =>  mu_eff = gamma_eff/pi
mu_BO = sp.simplify(gamma_eff/sp.pi)
mu_BO = sp.simplify(sp.expand(mu_BO))
print()
print("mu_eff^BO(y) =", mu_BO)

# N1's claim
kp = sp.diff(kap, y)
mu_N1 = 3*y**2*kp**2/(3+kap**2)**2
diff = sp.simplify(mu_BO - mu_N1)
print()
print("mu_eff^BO - mu_N1 =", diff)
print("N1 closed form exact at BO level:", diff == 0)
