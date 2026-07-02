"""bv2_g_transv_toy.py — C6 third check: nontrivial toy with constant in L.
L = v^2/2 - a*q + c0 on [0,s]; q(0)=0; free endpoint value AND free s.
Direct dS/ds of the on-shell family must equal -H(s) evaluated with the constant INCLUDED.
"""
import sympy as sp
t, s, a, c0 = sp.symbols('t s a c0', positive=True)
# EOM q'' = -a? EL: q'' = dL/dq = -a. Natural BC at s: q'(s)=0. q(0)=0.
# q = -a t^2/2 + b t; q'(s) = -a s + b = 0 -> b = a s. q = a s t - a t^2/2.
q = a*s*t - a*t**2/2
v = sp.diff(q, t)
L = v**2/2 - a*q + c0
S = sp.integrate(L, (t, 0, s))
dS = sp.simplify(sp.diff(S, s))
H = sp.simplify((v**2/2 + a*q - c0).subs(t, s))   # H = v dL/dv - L = v^2/2 + a q - c0
print("S(s) =", sp.simplify(S))
print("dS/ds =", dS, "   -H(s) =", sp.simplify(-H))
print("dS/ds == -H(s):", sp.simplify(dS + H) == 0)
# closure dS/ds=0 <-> H(s)=0, and the constant c0 enters H with weight -1: check
print("solve dS/ds=0 for c0:", sp.solve(sp.Eq(dS,0), c0))
