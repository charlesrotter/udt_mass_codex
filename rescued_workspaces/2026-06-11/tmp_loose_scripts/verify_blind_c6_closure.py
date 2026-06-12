"""BLIND VERIFIER C6: closure selector theorem.

Claims: (i) static vacuum in radial class: f = A + B/y (general?);
(ii) action density B^2/(4y^2), non-integrable at y->0 unless B=0;
(iii) closure + finite action + f(phi0)=1 => f === 1; so nontrivial => sigma != 0;
(iv) annular cells evade; (v) pointwise f>=1 at interface forces a(phi0)=0,
surviving datum p_source = (1/2) y^2 a'.
Hostile additions: does the ANGULAR sector admit other finite-action vacua that
evade the spherical f=A+B/y argument? (energy/positivity audit in Galerkin class)
"""
import numpy as np
import sympy as sp

y = sp.Symbol('y', positive=True); f = sp.Function('f')
print("(i) spherical static vacuum: solve (y^2 f')' = 0")
sol = sp.dsolve(sp.Derivative(y**2*sp.Derivative(f(y), y), y), f(y))
print("   ", sol)

A, B = sp.symbols('A B')
fv = A + B/y
dens = sp.simplify(sp.Rational(1,4)*y**2*sp.diff(fv, y)**2)
print("(ii) action density (1/4) y^2 f'^2 =", dens)
eps = sp.Symbol('epsilon', positive=True)
I = sp.integrate(dens, (y, eps, 1))
print("    Int_eps^1 =", sp.simplify(I), " -> diverges as eps->0 unless B=0:",
      sp.limit(I, eps, 0))

print("\n(iii') HOSTILE: angular-sector vacua in the ell<=1 Galerkin class")
print("  a-equation: (y^2 a')' = P_a/2, with a*P_a >= 0 (check positivity):")
k = sp.Symbol('k')
L = sp.log((1+k)/(1-k))
hp = (1 + 1/k**2)*L - 2/k          # h'(kappa); P_a = 2 pi c h'(k); sign(h')=sign(k)
ser = sp.series(hp, k, 0, 6)
print("   h'(k) small-k series:", ser)
kk = np.linspace(1e-4, 0.999, 50)
hpn = (1+1/kk**2)*np.log((1+kk)/(1-kk)) - 2/kk
print("   min h'(k)/k on (0,1):", (hpn/kk).min(), " (>0 => a*P_a >= 0 everywhere)")
print("   => energy identity: [y^2 a' a]_0^1 = Int (y^2 a'^2 + a P_a/2) dy >= 0,")
print("      equality iff a==0.  With a(1)=0 (pointwise interface) and finite")
print("      action regularity at y->0, boundary term -> 0  => a == 0.")
print("   => closure theorem CONCLUSION survives the angular sector in the")
print("      Galerkin class, but the agent's stated PROOF (f=A+B/y) covers the")
print("      spherical sector only.")

print("\n(v) pointwise f>=1 + monopole f(phi0)=1 => Int (f-1) dOmega = 0 with")
print("    f-1>=0 pointwise => f==1 on the sphere => a(phi0)=0.  SOUND.")
print("    boundary momentum: vary (1/4) Int y^2 a'^2: delta S_bdy = (1/2) y^2 a' da")
asym = sp.Function('a')
S = sp.Rational(1,4)*y**2*sp.Derivative(asym(y), y)**2
print("    dL/da' =", sp.diff(S, sp.Derivative(asym(y), y)), " => p = (1/2) y^2 a'  OK")
