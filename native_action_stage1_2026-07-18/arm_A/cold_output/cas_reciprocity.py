#!/usr/bin/env python3
"""Verify the 2x2 dual-pairing algebra and the reciprocal exponential subgroup."""
import sympy as sp

u, v, a, b = sp.symbols("u v a b", positive=True)
K = sp.Matrix([[0, 1], [1, 0]])
P = sp.diag(u, v)
print("P.T*K*P =")
sp.pprint(sp.simplify(P.T * K * P))
print("P.T*K*P-K =")
sp.pprint(sp.simplify(P.T * K * P - K))
print("Solutions of uv=1 for v:", sp.solve(sp.Eq(u*v, 1), v))

Pe = lambda z: sp.diag(sp.exp(-z), sp.exp(z))
print("P(a)P(b)-P(a+b) =")
sp.pprint(sp.simplify(Pe(a) * Pe(b) - Pe(a+b)))
print("P(a).T*K*P(a)-K =")
sp.pprint(sp.simplify(Pe(a).T * K * Pe(a) - K))
