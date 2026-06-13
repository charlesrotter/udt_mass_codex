#!/usr/bin/env python3
"""W6 FLUX VERIFIER — THE DECISIVE TIME-ROW TEST (deliverable A + the
fold-vs-edge settlement).

The arm established (and I independently confirm in
w6_flux_verifier_curv) that on the STATIC, time-row-OFF metric
  g = [[-f,0,0,0],[0,1/f,q,0],[0,q,r^2 W,0],[0,0,0,r^2 sin^2/W]]
det g4 = -(r sin)^2 D/(1+w)^2 vanishes linearly on D=0 and curvature
invariants diverge there.

THE BRIEF'S CENTRAL UNTESTED QUESTION (A): turn on the same-minus time
row (a,b)=(g_Tr,g_Ttheta). The same-minus theorem is the involution
(a,b)->(-a,-b) (theorem-grade). A surface FIXED under it (only a=b=0)
is the static slice -- a mirror crease.

  (i)  does det g4 STILL vanish on D=0 with (a,b)!=0, or is the
       degeneracy LIFTED?
  (ii) is D=0 the FIXED-POINT SET of (a,b)->(-a,-b)?
  (iii) does curvature still diverge on D=0 with the time row ON?

This is EXACT sympy on the general background, plus an mpmath
high-precision curvature evaluation with a CONCRETE nonzero (a,b) on
the arm's member. Independent engine (Schwarzschild-validated).
"""
import sys
import time
import math
import mpmath as mp
import sympy as sp
from w6_flux_verifier_engine import kretschmann_ricci

t0 = time.time()
PASS, FAIL, NOTE = [], [], []


def ck(tag, cond, note=''):
    (PASS if cond else FAIL).append(tag)
    print(f"{tag}: {'PASS' if cond else 'FAIL'} {note}", flush=True)


def note(tag, n):
    NOTE.append((tag, n))
    print(f"{tag}: NOTE {n}", flush=True)


T, ph = sp.symbols('T phi', real=True)
r = sp.Symbol('r', positive=True)
th = sp.Symbol('theta', real=True)
f, q, w, a, b = sp.symbols('f q w a b', real=True)
W = (1 + w)**2
D = r**2 * W - f * q**2

print("=" * 70)
print("A(i)+A(ii) — DETERMINANT LIFT (exact, general background)")
print("=" * 70)
gfull = sp.Matrix([[-f, a, b, 0],
                   [a, 1 / f, q, 0],
                   [b, q, r**2 * W, 0],
                   [0, 0, 0, r**2 * sp.sin(th)**2 / W]])
detfull = sp.simplify(gfull.det())
# completed-square form:
detform = -(r * sp.sin(th))**2 / (f * (1 + w)**2) \
    * (f * D * (1 + a**2) + (b - f * q * a)**2)
ck("A-detform", sp.simplify(detfull - detform) == 0,
   "det g4 = -(r sin)^2/[f(1+w)^2] * [ f D (1+a^2) + (b - f q a)^2 ]")

# On D=0:
detD0 = sp.simplify(detfull.subs(f * q**2, r**2 * W))
detD0_target = -(r * sp.sin(th))**2 / (f * (1 + w)**2) * (b - f * q * a)**2
ck("A-detD0", sp.simplify(detD0 - detD0_target) == 0,
   "ON D=0: det g4 = -(r sin)^2/[f(1+w)^2] (b - f q a)^2 <= 0; it is "
   "NONZERO (signature held) for any (a,b) with b != f q a")

# A(i): does (a,b)!=0 lift the degeneracy on D=0? Yes unless b=fqa.
note("A(i)", "ON D=0 the determinant is LIFTED to a NONZERO value "
     "-(r sin)^2 (b-fqa)^2/[f(1+w)^2] whenever b != f q a. The static "
     "slice a=b=0 is the SPECIAL case where it vanishes. So D=0 is NOT "
     "a determinant-zero surface of the time-row-on metric generically.")

# A(ii): fixed-point set of (a,b)->(-a,-b). A point is fixed iff the
# metric at (a,b) equals the metric at (-a,-b), i.e. iff a=b=0 (the
# off-diagonal entries are linear in (a,b); only a=b=0 is invariant).
note("A(ii)", "The involution (a,b)->(-a,-b) acts on the metric by "
     "g_Tr->-g_Tr, g_Ttheta->-g_Ttheta. The metric is INVARIANT iff "
     "a=b=0. So the FIXED-POINT SET of the involution is exactly the "
     "STATIC SLICE a=b=0 -- a codim-2 surface in time-row space, NOT "
     "the D=0 surface. D=0 is a surface in (r,theta) for ANY (a,b).")

# Is D=0 mapped to itself by the involution? D = r^2 W - f q^2 does NOT
# involve (a,b), so the involution fixes D=0 SETWISE trivially (it acts
# only on a,b). The decisive reading: the curvature singularity the arm
# found lives ON the a=b=0 fixed slice; off it the determinant is lifted.
note("A(ii)b", "D depends only on (f,q,w), not (a,b); so D=0 is "
     "involution-invariant SETWISE in the trivial sense (the involution "
     "moves only a,b). The substantive content is A(i): the metric "
     "DEGENERACY on D=0 is an artifact of sitting on the a=b=0 fixed "
     "slice. The arm evaluated curvature ONLY on that slice.")

print()
print("=" * 70)
print("A(iii) — CURVATURE ON D=0 WITH THE TIME ROW ON (mpmath 80dps)")
print("=" * 70)
# Concrete member: arm's f, w=0, q = q* (the tangential branch), and a
# CONCRETE constant nonzero (a,b) that does NOT satisfy b=f q a on D=0
# (so the determinant is genuinely lifted). Build full 4-metric with
# time row, compute K,R, evaluate approaching D=0.
mp.mp.dps = 60
ffn = (1 + sp.Rational(1, 10) * sp.cos(th)**2) / r
Wf = sp.Integer(1)
fr, fth = sp.diff(ffn, r), sp.diff(ffn, th)
P = ffn * r**2 * Wf * fr**2 + fth**2
qs = 2 * r**2 * Wf * fr * fth / P
# nonzero time row: pick a=1/3 constant, b=1/4 constant (generic; will
# NOT equal f q a on D=0 except by coincidence -- checked numerically).
aval = sp.Rational(1, 3)
bval = sp.Rational(1, 4)
gtr = sp.Matrix([[-ffn, aval, bval, 0],
                 [aval, 1 / ffn, qs, 0],
                 [bval, qs, r**2 * Wf, 0],
                 [0, 0, 0, r**2 * sp.sin(th)**2 / Wf]])
Dexpr = sp.simplify(r**2 * Wf - ffn * qs**2)
print(f"   [building curvature with time row on {time.time()-t0:.0f}s]",
      flush=True)
K, Rs, _, _, _ = kretschmann_ricci(gtr, [T, r, th, ph])
print(f"   [curvature built {time.time()-t0:.0f}s]", flush=True)
th0 = sp.pi / 3
Rs3 = sp.simplify(Rs.subs(th, th0))
K3 = sp.simplify(K.subs(th, th0))
D3 = sp.simplify(Dexpr.subs(th, th0))
detg3 = sp.simplify(gtr.det().subs(th, th0))
numD = sp.numer(sp.together(D3))
poly = sp.Poly(sp.expand(numD), r)
roots = mp.polyroots([mp.mpf(str(c)) for c in poly.all_coeffs()],
                     maxsteps=300, extraprec=300)
rstar = next(mp.re(rt) for rt in roots
             if abs(mp.im(rt)) < mp.mpf('1e-40') and mp.re(rt) > 0)
print(f"   r*(D=0) = {mp.nstr(rstar, 20)}", flush=True)
Rf = sp.lambdify(r, Rs3, 'mpmath')
Kf = sp.lambdify(r, K3, 'mpmath')
Df = sp.lambdify(r, D3, 'mpmath')
detf = sp.lambdify(r, detg3, 'mpmath')
print(f"{'delta':>8}{'D':>16}{'det g4':>20}{'R':>20}{'K':>20}")
rows = []
for k in range(2, 9):
    dl = mp.mpf(10)**(-k)
    rv = rstar * (1 + dl)
    Dv, dtv, Rv, Kv = Df(rv), detf(rv), Rf(rv), Kf(rv)
    rows.append((float(dl), Dv, Rv, Kv))
    print(f"{mp.nstr(dl,2):>8}{mp.nstr(Dv,4):>16}{mp.nstr(dtv,5):>20}"
          f"{mp.nstr(Rv,5):>20}{mp.nstr(Kv,5):>20}", flush=True)


def fit(rows, idx):
    xs, ys = [], []
    for (_, Dv, Rv, Kv) in rows[-5:]:
        v = Rv if idx == 'R' else Kv
        if Dv != 0 and v != 0:
            xs.append(math.log(abs(float(Dv))))
            ys.append(math.log(abs(float(v))))
    if len(xs) < 3:
        return 0.0, 1.0
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sl = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) \
        / sum((x - mx)**2 for x in xs)
    pred = [my + sl * (x - mx) for x in xs]
    rms = (sum((y - p)**2 for y, p in zip(ys, pred)) / n)**0.5
    return sl, rms


slR, rmsR = fit(rows, 'R')
slK, rmsK = fit(rows, 'K')
print(f"\n   TIME-ROW-ON: R ~ D^{slR:+.4f} (rms {rmsR:.1e}), "
      f"K ~ D^{slK:+.4f} (rms {rmsK:.1e})")
# det g4 should approach a NONZERO constant (lifted), not 0:
detlim = detf(rstar * (1 + mp.mpf(10)**-8))
ck("A(iii)-detlift", abs(detlim) > mp.mpf('1e-6'),
   f"det g4 -> {mp.nstr(detlim,6)} (NONZERO: degeneracy LIFTED by time "
   "row; no signature loss on D=0)")
Kbig = abs(rows[-1][3]) > 1e8
note("A(iii)-K", f"With time row ON, K ~ D^{slK:.3f}, last |K|="
     f"{mp.nstr(abs(rows[-1][3]),4)}. "
     + ("STILL DIVERGES -> divergence is NOT merely the static-slice "
        "det->0 artifact" if Kbig and slK < -0.5 else
        "BOUNDED/MILD -> divergence WAS a static-slice artifact"))

print()
print(f"VERIFIER TIMEROW: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({len(NOTE)} notes, {time.time()-t0:.0f}s)")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0 if not FAIL else 1)
