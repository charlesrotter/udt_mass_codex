#!/usr/bin/env python3
"""Verify that T_00 of the chosen covariant S2 completion equals the supplied static energy density."""
import sympy as sp

xi, kappa, ns2, fij_sum = sp.symbols("xi kappa ns2 fij_sum", real=True)
# For static fields in Minkowski: d_0 n=F_0a=0, g_00=-1.
Y = ns2
F2 = fij_sum
T00_sigma = sp.simplify(xi*(0-sp.Rational(1, 2)*(-1)*Y))
T00_F = sp.simplify(kappa*(0-sp.Rational(1, 4)*(-1)*F2))
E = xi*ns2/2+kappa*fij_sum/4
print("T00 sigma =", T00_sigma)
print("T00 quartic =", T00_F)
print("T00 total - supplied energy =", sp.simplify(T00_sigma+T00_F-E))
