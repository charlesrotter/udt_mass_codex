#!/usr/bin/env python3
"""VFOLD TEST C (decisive) + A(iii): TIME-ROW curvature. Does the
curvature divergence at the static-slice surface D=0 SURVIVE turning on
the same-minus time row (a,b)=(g_Tr,g_Ttheta), or is it an ARTIFACT of
the a=b=0 static (fixed) slice?

Established in vfold_det_timerow.py (exact):
  det g4 = -(r^2 sin^2 th / W) (D + E),   E(a,b) = a^2 r^2 W - 2 a b q + b^2/f
  E = ||(a,b)||^2 in the spatial-block metric h=[[1/f,q],[q,r^2 W]] (det=D/f).
So the full 4-metric degeneracy is at D = -E < 0, NOT D=0. On D>0 with the
time row on, the metric is nondegenerate at the static-slice surface D=0.
PREDICTION (fold hypothesis): curvature is FINITE at D=0 once a,b != 0.
PREDICTION (edge hypothesis): curvature still diverges at D=0 regardless.

PRE-REGISTERED CRITERIA:
  TC1: Schwarzschild recalibration of THIS script's engine import (PASS
       required before trusting any number).
  TC2: with a SMALL CONSTANT time row (a0,b0) added to the q* member,
       evaluate K at the static-slice locus r* (where D=0).
       FOLD-PASS: K is FINITE (no divergence) at r* for (a0,b0)!=0.
       EDGE-PASS: K still diverges at r* for (a0,b0)!=0.
       Report whichever; aim hardest at the convenient one.
  TC3: scan |(a,b)| -> 0 and confirm K(r*) -> the static-slice divergence
       continuously (i.e. the static slice is the (a,b)->0 LIMIT, a
       removable codimension-2 degeneracy = a fold crease, like the
       coordinate pole). The divergence is the value AT the fixed slice
       of an otherwise-regular family.
  TC4: the true degeneracy of the time-on metric is at D=-E; confirm K
       diverges THERE (the genuine edge of the enlarged metric), not at
       D=0.

mpmath 50-digit; float64 trap avoided. Log: /tmp/vfold_timerow_curv.log
"""
import sys
import time

import mpmath as mp
import sympy as sp

from vfold_curv_engine import kretschmann

t0 = time.time()
mp.mp.dps = 50

T, ph = sp.symbols('T varphi', real=True)
r = sp.Symbol('r', positive=True)
th = sp.Symbol('theta', real=True)

# --- TC1: recalibrate engine here (cheap, mandatory) -----------------
print("=" * 72)
print("TC1 — Schwarzschild recalibration of imported engine")
print("=" * 72)
Ms = sp.Symbol('M', positive=True)
fSch = 1 - 2 * Ms / r
gSch = sp.diag(-fSch, 1 / fSch, r ** 2, r ** 2 * sp.sin(th) ** 2)
Ksch, Rsch = kretschmann(gSch, [T, r, th, ph])
ok = (sp.simplify(Rsch) == 0 and
      sp.simplify(Ksch - 48 * Ms ** 2 / r ** 6) == 0)
print(f"  R=0, K=48M^2/r^6 reproduced: {ok}")
assert ok, "engine calibration failed"

# --- member: q* branch, w=0, eps=1/10, evaluate at theta=pi/3 --------
eps = sp.Rational(1, 10)
ffun = (1 / r) * (1 + eps * sp.cos(th) ** 2)
W = sp.Integer(1)
fr = sp.diff(ffun, r)
fth = sp.diff(ffun, th)
P = ffun * r ** 2 * W * fr ** 2 + fth ** 2
qstar = 2 * r ** 2 * W * fr * fth / P
D = r ** 2 * W - ffun * qstar ** 2

# small constant time row (frozen background). a,b are metric components,
# CONSTANTS here (a background nonstationary completion needn't have x-dep
# to test whether nonzero (a,b) lifts the determinant degeneracy).
a0, b0 = sp.symbols('a0 b0', real=True)


def build_g4_timerow(aa, bb):
    return sp.Matrix([
        [-ffun, aa, bb, 0],
        [aa, 1 / ffun, qstar, 0],
        [bb, qstar, r ** 2 * W, 0],
        [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / W],
    ])


# locate r* (D=0) at theta=pi/3:
sub3 = {th: sp.pi / 3}
D3 = sp.simplify(D.subs(sub3))
numD = sp.numer(sp.together(D3))
poly = sp.Poly(sp.expand(numD), r)
roots = mp.polyroots([mp.mpf(str(c)) for c in poly.all_coeffs()],
                     maxsteps=300, extraprec=300)
rstar = None
for rt in roots:
    if abs(mp.im(rt)) < mp.mpf('1e-40') and mp.re(rt) > 0:
        rstar = mp.re(rt)
        break
print(f"\n  static-slice surface r* (D=0, theta=pi/3) = {mp.nstr(rstar,20)}")
# evaluate qstar, f at r* to choose a sensible (a0,b0) magnitude:
q_at = float(sp.lambdify(r, qstar.subs(sub3), 'mpmath')(rstar))
f_at = float(sp.lambdify(r, ffun.subs(sub3), 'mpmath')(rstar))
print(f"  at r*: q*={q_at:.4e}, f={f_at:.4e}, r*^2={float(rstar)**2:.2f}")

print()
print("=" * 72)
print("TC2/TC3 — K at the static surface D=0 vs time-row magnitude")
print("=" * 72)
# Build curvature ONCE with symbolic a0,b0 is very expensive. Instead,
# for each numeric (a0,b0) we substitute constants then build curvature.
# To keep cost bounded we evaluate K at a handful of (a0,b0) magnitudes,
# each at r slightly inside the static surface and AT it.
print(f"{'a0=b0':>12} {'r (approach)':>16} {'D':>14} {'K':>22}", flush=True)


def K_at(aa_val, bb_val, rval):
    g4n = build_g4_timerow(sp.nsimplify(aa_val), sp.nsimplify(bb_val))
    g4n = g4n.subs(sub3)
    Kexpr, _ = kretschmann(g4n, [T, r, th, ph])
    Kf = sp.lambdify(r, sp.simplify(Kexpr), 'mpmath')
    return Kf(rval)


# (a0,b0) = (0,0) static control at a few D values, then nonzero rows.
import math
def Dval(rval):
    return sp.lambdify(r, D3, 'mpmath')(rval)

mags = [mp.mpf('0'), mp.mpf('1e-4'), mp.mpf('1e-3'), mp.mpf('1e-2'),
        mp.mpf('1e-1')]
results = {}
for m in mags:
    # approach the static surface: r = r*(1+delta), delta -> small
    Krow = []
    for k in (3, 5, 7):
        delta = mp.mpf(10) ** (-k)
        rv = rstar * (1 + delta)
        try:
            Kv = K_at(m, m, rv)
        except Exception as e:
            Kv = mp.nan
        Dv = Dval(rv)
        Krow.append((float(delta), Dv, Kv))
        print(f"{mp.nstr(m,3):>12} {mp.nstr(rv,12):>16} "
              f"{mp.nstr(Dv,4):>14} {mp.nstr(Kv,6):>22}", flush=True)
    results[float(m)] = Krow
    print()

print("=" * 72)
print("INTERPRETATION")
print("=" * 72)
# For each nonzero magnitude, does K stay BOUNDED as D->0 (fold) or blow
# up (edge)?  Compare K at delta=1e-3 vs 1e-7 for each magnitude.
for m in mags:
    row = results[float(m)]
    Kvals = [abs(float(x[2])) for x in row if mp.isfinite(x[2])]
    if len(Kvals) >= 2:
        ratio = Kvals[-1] / Kvals[0] if Kvals[0] != 0 else float('inf')
        growth = "DIVERGES" if ratio > 1e3 else "BOUNDED"
        print(f"  |a,b|={float(m):.0e}: K(delta=1e-7)/K(delta=1e-3) "
              f"~ {ratio:.2e}  -> {growth}")
print()
print("  FOLD signature: nonzero (a,b) -> K BOUNDED at D=0 (divergence")
print("  was a static-slice/fixed-surface artifact).")
print("  EDGE signature: K DIVERGES at D=0 for all (a,b).")
print(f"\nVFOLD TIMEROW-CURV done ({time.time()-t0:.0f}s)")
sys.exit(0)
