"""Arbitrate the factor 2: evaluate the FULL generic K (Schwarzschild-
validated) at moderate theta with mpmath dps=60, Richardson-extrapolate
theta->0, compare against my exact axis formula
   K_axis = a''^2 + 4a'^2/y^2 + 4(a-1)^2/y^4 + 16 b^2/(y^4 a^2)
and the audit/banked law (which implies the b-term would be 8 b^2/...)."""
import sympy as sp
import numpy as np
from mpmath import mp
mp.dps = 60

T, y, th, ph = sp.symbols('T y theta phi')
fF = sp.Function('f')(y, th)
gdd = sp.diag(-fF, 1/fF, y**2, y**2*sp.sin(th)**2)
xs = [T, y, th, ph]
guu = sp.diag(-1/fF, fF, 1/y**2, 1/(y**2*sp.sin(th)**2))
Gam = [[[sum(guu[a, d]*(sp.diff(gdd[d, b], xs[c]) + sp.diff(gdd[d, c],
        xs[b]) - sp.diff(gdd[b, c], xs[d])) for d in range(4))/2
        for c in range(4)] for b in range(4)] for a in range(4)]
Riem = [[[[sp.diff(Gam[a][b][d], xs[c]) - sp.diff(Gam[a][b][c], xs[d])
           + sum(Gam[a][e][c]*Gam[e][b][d] - Gam[a][e][d]*Gam[e][b][c]
                 for e in range(4))
           for d in range(4)] for c in range(4)] for b in range(4)]
        for a in range(4)]
Rdddd = [[[[sum(gdd[a, e]*Riem[e][b][c][d] for e in range(4))
            for d in range(4)] for c in range(4)] for b in range(4)]
         for a in range(4)]
K = sp.Integer(0)
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                t1 = Rdddd[a][b][c][d]
                if t1 == 0:
                    continue
                K += t1**2*guu[a, a]*guu[b, b]*guu[c, c]*guu[d, d]

f0s, fys, fths, fyys, fthths, fyths = sp.symbols(
    'f0 fy fth fyy fthth fyth', real=True)
def dmap(d):
    cnt = {y: 0, th: 0}
    for v, n in d.variable_count:
        cnt[v] += n
    return {(1, 0): fys, (2, 0): fyys, (0, 1): fths, (0, 2): fthths,
            (1, 1): fyths}[(cnt[y], cnt[th])]
repl = {d: dmap(d) for d in K.atoms(sp.Derivative)}
repl[fF] = f0s
Ksym = K.xreplace(repl)
Kfun = sp.lambdify((y, th, f0s, fys, fths, fyys, fthths, fyths),
                   Ksym, 'mpmath')

def K_full(yv, A, A1, A2, B, B1, thv):
    """exact metric f = a(y) + b(y) theta^2 at finite theta (mpmath)."""
    fv = A + B*thv**2
    return Kfun(mp.mpf(yv), mp.mpf(thv), fv, A1 + B1*thv**2,
                2*B*thv, A2, 2*B, 2*B1*thv)

def K_axis_mine(yv, A, A1, A2, B, B1):
    return A2**2 + 4*A1**2/yv**2 + 4*(A-1)**2/yv**4 + 16*B**2/(yv**4*A**2)

cases = [
    ("const a,b", 1.5, 0.0, 0.0, 0.7, 0.0, 1.3),
    ("generic", 0.8, -2.1, 3.3, 0.9, 1.7, 0.9),
    ("seal-ish", 0.002, -50.0, 4000.0, 2.5, 30.0, 0.03),
]
for name, A, A1, A2, B, B1, yv in cases:
    A, A1, A2, B, B1, yv = map(mp.mpf, (A, A1, A2, B, B1, yv))
    k1 = K_full(yv, A, A1, A2, B, B1, mp.mpf('1e-2'))
    k2 = K_full(yv, A, A1, A2, B, B1, mp.mpf('5e-3'))
    kext = (4*k2 - k1)/3      # O(th^2) Richardson
    kmine = K_axis_mine(yv, A, A1, A2, B, B1)
    kclaim = kmine - 8*B**2/(yv**4*A**2)   # if the b-coeff were 8 not 16
    print(f"{name}: K(extrap) = {mp.nstr(kext, 12)}")
    print(f"   mine(16b^2) = {mp.nstr(kmine, 12)}   rel.dev "
          f"{mp.nstr(abs(kext-kmine)/abs(kext), 3)}")
    print(f"   claim(8b^2) = {mp.nstr(kclaim, 12)}   rel.dev "
          f"{mp.nstr(abs(kext-kclaim)/abs(kext), 3)}")
