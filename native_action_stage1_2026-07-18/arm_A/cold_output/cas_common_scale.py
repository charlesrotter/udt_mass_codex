#!/usr/bin/env python3
"""Verify common-scale times determinant-one decomposition of a positive diagonal map."""
import sympy as sp

u, v = sp.symbols("u v", positive=True)
phi = sp.log(v/u) / 2
lhs = sp.diag(u, v)
rhs = sp.sqrt(u*v) * sp.diag(sp.exp(-phi), sp.exp(phi))
print("diag(u,v) - proposed decomposition =")
sp.pprint(sp.simplify(lhs-rhs))
print("determinant of reciprocal factor =", sp.simplify(sp.det(sp.diag(sp.exp(-phi), sp.exp(phi)))))
print("recovered phi =", sp.simplify(phi))
