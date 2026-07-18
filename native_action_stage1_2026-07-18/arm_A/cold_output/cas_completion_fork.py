#!/usr/bin/env python3
"""Verify that arbitrary time-sector coefficients leave the supplied static S2 energy unchanged."""
import sympy as sp

xi, kappa, a2, a4 = sp.symbols("xi kappa a2 a4", real=True)
Dt2, Di2, Fti2, Fij2 = sp.symbols("Dt2 Di2 Fti2 Fij2", nonnegative=True)
# Exact flat-foliation Lagrangian; a2 and a4 are deliberately independent.
L = a2*Dt2/2-xi*Di2/2+a4*Fti2/2-kappa*Fij2/4
print("General flat-foliation L =", L)
L_static = sp.simplify(L.subs({Dt2: 0, Fti2: 0}))
E = xi*Di2/2+kappa*Fij2/4
print("Static L =", L_static)
print("Static L + supplied E =", sp.simplify(L_static+E))
print("d(static L)/d(a2) =", sp.diff(L_static, a2))
print("d(static L)/d(a4) =", sp.diff(L_static, a4))
