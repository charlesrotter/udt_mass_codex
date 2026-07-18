#!/usr/bin/env python3
"""Check the reduced Euler-Lagrange expression and boundary momentum for L=-(a/4)(phi')^4."""
import sympy as sp

x, a = sp.symbols("x a", real=True)
f = sp.Function("f")(x)
fp = sp.diff(f, x)
L = -a*fp**4/4
momentum = sp.diff(L, fp)
EL = sp.diff(L, f) - sp.diff(momentum, x)
print("L =", L)
print("dL/d(phi') =", momentum)
print("Euler-Lagrange coefficient dL/dphi-d_x(dL/dphi') =")
sp.pprint(sp.factor(EL))
print("Expected a*d_x((phi')^3), difference =", sp.simplify(EL-a*sp.diff(fp**3, x)))
print("Boundary coefficient from integration by parts is dL/d(phi') =", momentum)
