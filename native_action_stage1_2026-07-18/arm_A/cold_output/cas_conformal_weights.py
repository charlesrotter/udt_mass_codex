#!/usr/bin/env python3
"""Verify four-dimensional Weyl weights of sqrt(-g) X^2 and of the S2 quadratic/quartic densities."""
import sympy as sp

Omega = sp.symbols("Omega", positive=True)
d = sp.symbols("d", integer=True, positive=True)
# Weight exponents under g_ab -> Omega^2 g_ab.
sqrtg_w = d
X_w = -2
F2_w = -4
print("weight exponent of sqrt(g)*X^2 in d dimensions =", sp.simplify(sqrtg_w+2*X_w))
print("in d=4 =", sp.simplify((sqrtg_w+2*X_w).subs(d, 4)))
print("weight exponent of sqrt(g)*F_mn F^mn in d=4 =", 4+F2_w)
print("weight exponent of sqrt(g)*g^mn dn.dn in d=4 =", 4-2)
chi2_w = -2
print("with a weight -1 compensator chi, quadratic term weight =", 4-2+chi2_w)
print("explicit invariant factors:", sp.simplify(Omega**4*(Omega**-2)**2), sp.simplify(Omega**4*Omega**-4))
