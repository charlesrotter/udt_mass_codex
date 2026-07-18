#!/usr/bin/env python3
"""Verify reciprocal metric-block identity, inverse, determinant, and spherical lapse-volume cancellation."""
import sympy as sp

phi, th = sp.symbols("phi theta", real=True)
c, r = sp.symbols("c r", positive=True)
g2 = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi))
print("g2 =")
sp.pprint(g2)
print("g2 inverse =")
sp.pprint(sp.simplify(g2.inv()))
print("(-g_tt/c^2)*g_rr =", sp.simplify((-g2[0, 0]/c**2)*g2[1, 1]))
print("det(g2) =", sp.simplify(g2.det()))

N = sp.exp(-phi)
hdet = sp.exp(2*phi)*r**4*sp.sin(th)**2
print("N*sqrt(det h) (positive angular chart) =", sp.simplify(N*sp.sqrt(hdet)))
