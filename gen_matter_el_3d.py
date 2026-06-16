#!/usr/bin/env python3
"""
gen_matter_el_3d.py -- AUTO-GENERATE the CORRECT full-3-D matter Euler-Lagrange
residual by DIRECT VARIATION of the action (the proven-correct method used for the
verified axisym_matter_el_CORRECT.py -- NOT the buggy off-round codegen).

The matter EL of S = int sqrt(-g)(L2+L4) wrt Theta(r,theta,psi):
  EL = [ d_r(dlag/dTheta_r) + d_th(dlag/dTheta_t) + d_ps(dlag/dTheta_p) - dlag/dTheta ] / rootg
with lag = sqrt(-g)(L2+L4).  This is the literal Euler-Lagrange equation -- exactly
the variation that builds the Hilbert stress (stress-consistent by construction),
hence immune to the L4 codegen bug the verifier found.  Verified machine-zero on the
round soliton and identity-consistent with the stress (div(T) = -EL d Theta).

FIELD: unit S^3 hedgehog, single FREE profile Theta(r,theta,psi), winding m in psi
  n = (sinTheta sin th cos(m psi), sinTheta sin th sin(m psi), sinTheta cos th, cosTheta).
Freeing Theta over ALL THREE coords lets the matter take NON-AXISYMMETRIC / lobed
shape; m sweeps the higher-winding sector.  (ROUND = Theta=Theta(r); axisym = no psi.)

METRIC: diagonal Weyl class, a,b,c,d(r,theta,psi) FREE (B=1/A NOT tied).

EXTENSION over the verified 2-D generator: psi LIVE (a..d,Theta depend on psi);
winding m in psi; the psi Euler term INCLUDED; ps NOT set to 0.

OUTPUT: matter_el_3d_gen.py with matter_el_3d(...) torch/numpy-evaluable.
"""
import sympy as sp
import time

t0 = time.time()
t, r, th, ps = sp.symbols('t r theta psi', real=True)
xi, kap = sp.symbols('xi kappa', positive=True)
m = sp.Symbol('m', positive=True)
coords = [t, r, th, ps]

a = sp.Function('a')(r, th, ps)
b = sp.Function('b')(r, th, ps)
c = sp.Function('c')(r, th, ps)
d = sp.Function('d')(r, th, ps)
Th = sp.Function('Theta')(r, th, ps)

glow = [-sp.exp(2*a), sp.exp(2*b), sp.exp(2*c)*r**2, sp.exp(2*d)*r**2*sp.sin(th)**2]
g = sp.diag(*glow)
ginv = g.inv()

sT, cT = sp.sin(Th), sp.cos(Th)
sth = sp.sin(th)
nA = [sT*sth*sp.cos(m*ps), sT*sth*sp.sin(m*ps), sT*sp.cos(th), cT]


def dmu(e, mu):
    return sp.diff(e, coords[mu])


print("building field metric Gmn...")
Gmn = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        Gmn[i, j] = sum(dmu(nA[A], i)*dmu(nA[A], j) for A in range(4))

print("building L2, L4...")
L2 = -(xi/2)*sum(ginv[i, j]*Gmn[i, j] for i in range(4) for j in range(4))
SS2 = lambda A, nn, B, q: Gmn[A, B]*Gmn[nn, q] - Gmn[A, q]*Gmn[nn, B]
L4 = -(kap/4)*sum(ginv[mm, pp]*ginv[nn, q]*SS2(mm, nn, pp, q)
                  for mm in range(4) for nn in range(4) for pp in range(4) for q in range(4))
L = L2 + L4
rootg = sp.exp(a+b+c+d)*r**2*sth
lag = rootg*L

print("forming Euler-Lagrange (r,theta,psi terms)... t=%.1fs" % (time.time()-t0))
EL = (sp.diff(sp.diff(lag, sp.diff(Th, r)), r)
      + sp.diff(sp.diff(lag, sp.diff(Th, th)), th)
      + sp.diff(sp.diff(lag, sp.diff(Th, ps)), ps)
      - sp.diff(lag, Th)) / rootg

print("simplify... t=%.1fs" % (time.time()-t0))
EL = sp.simplify(EL)

subs = {}
for f, nm in [(a, 'a'), (b, 'b'), (c, 'c'), (d, 'd'), (Th, 'Th')]:
    subs[sp.diff(f, r, 2)] = sp.Symbol(nm+'_rr')
    subs[sp.diff(f, th, 2)] = sp.Symbol(nm+'_tt')
    subs[sp.diff(f, ps, 2)] = sp.Symbol(nm+'_pp')
    subs[sp.diff(f, r, th)] = sp.Symbol(nm+'_rt')
    subs[sp.diff(f, r, ps)] = sp.Symbol(nm+'_rp')
    subs[sp.diff(f, th, ps)] = sp.Symbol(nm+'_tp')
    subs[sp.diff(f, r)] = sp.Symbol(nm+'_r')
    subs[sp.diff(f, th)] = sp.Symbol(nm+'_t')
    subs[sp.diff(f, ps)] = sp.Symbol(nm+'_p')
    subs[f] = sp.Symbol(nm)
ELx = EL.subs(subs, simultaneous=True)

syms = [r, th, ps, m]
for nm in ['a', 'b', 'c', 'd', 'Th']:
    for suf in ['', '_r', '_t', '_p', '_rr', '_tt', '_pp', '_rt', '_rp', '_tp']:
        syms.append(sp.Symbol(nm+suf))
syms += [xi, kap]

from sympy.printing.numpy import NumPyPrinter
code = ("import numpy\nimport numpy as np\nfrom numpy import exp, sin, cos, tan, sqrt\n\n"
        "def matter_el_3d(" + ", ".join(str(s) for s in syms) + "):\n"
        "    return " + NumPyPrinter().doprint(ELx) + "\n")
with open('matter_el_3d_gen.py', 'w') as fo:
    fo.write(code)
print("wrote matter_el_3d_gen.py  (expr len", len(str(ELx)), ") t=%.1fs" % (time.time()-t0))
