#!/usr/bin/env python3
"""Verify trace and static energy density of the four-dimensional X^2 scalar stress tensor."""
import sympy as sp

a, X = sp.symbols("a X", real=True)
d = sp.symbols("d", integer=True, positive=True)
# T_ab = a X phi_a phi_b - a/4 g_ab X^2, and g^ab phi_a phi_b=X.
trace_d = sp.simplify(a*X**2 - d*a*X**2/4)
print("Trace in d dimensions =", trace_d)
print("Trace in d=4 =", sp.simplify(trace_d.subs(d, 4)))

p2 = sp.symbols("p2", nonnegative=True)
# In a static orthonormal frame X=p2 and phi_0=0; T_00=-(a/4)g_00 X^2.
T00_static = sp.simplify(a*p2**2/4)
print("Static orthonormal T_00 =", T00_static)
print("Hamiltonian density -L =", sp.simplify(-(-a*p2**2/4)))
print("Difference =", sp.simplify(T00_static-a*p2**2/4))
