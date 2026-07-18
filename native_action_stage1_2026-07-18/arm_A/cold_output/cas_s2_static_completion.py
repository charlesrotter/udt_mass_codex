#!/usr/bin/env python3
"""Verify that the chosen Lorentz-covariant S2 completion reduces to minus the supplied static energy."""
import sympy as sp

xi, kappa = sp.symbols("xi kappa", real=True)
nt2, ns2 = sp.symbols("nt2 ns2", nonnegative=True)
f0i2, fij_sum = sp.symbols("f0i2 fij_sum", nonnegative=True)
# Signature (-,+,+,+): Y=-|dot n|^2+sum_i|d_i n|^2.
Y = -nt2 + ns2
# Ordered-index contraction F_mn F^mn = -2 sum_i F_0i^2 + sum_{i,j}F_ij^2.
F2 = -2*f0i2 + fij_sum
L = -xi*Y/2-kappa*F2/4
print("Four-dimensional Lagrangian in components =")
sp.pprint(sp.expand(L))
L_static = sp.simplify(L.subs({nt2: 0, f0i2: 0}))
E_supplied = xi*ns2/2+kappa*fij_sum/4
print("Static L =", L_static)
print("Supplied static energy density =", E_supplied)
print("L_static + E_supplied =", sp.simplify(L_static+E_supplied))
