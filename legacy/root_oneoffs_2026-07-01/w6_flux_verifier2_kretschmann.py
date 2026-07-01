#!/usr/bin/env python3
"""W6 FLUX-TEST VERIFIER — PART A/C: KRETSCHMANN with the time row ON,
and the chart-invariance cross-check.

Hostile self-check on my OWN convenient Ricci result: the arm's HEADLINE
invariant was the KRETSCHMANN K (R~D^-3/2, K~D^-3 on q*).  Ricci can be
bounded while K diverges.  So I recompute the FULL Kretschmann (my own
Schwarzschild-validated engine) on:
  (1) the static slice (a=b=0)  -> must reproduce the arm's K~D^-3 blow-up
      (this CALIBRATES my engine against the arm's claim independently);
  (2) the SAME member with the same-minus time row (a,b)!=0 ON -> if K
      stays BOUNDED, the divergence is a static-slice artifact (FOLD);
      if K still diverges, the edge survives the time row (EDGE).

Also: confirm the float64 catastrophic-cancellation sign-flip near
D ~ 1e-7 (mpmath clean, float64 erratic), per the brief.

Engine: imported from w6_flux_verifier2_engine (Schwarzschild K=48M^2/r^6
validated).  mpmath 80 digits.

Log: /tmp/w6_flux_verifier2_kretschmann.log
"""
import sys
import time
import math

import mpmath as mp
import sympy as sp

from w6_flux_verifier2_engine import (udt_metric, christoffel,
                                       riemann_mixed, kretschmann,
                                       UXS, rv, thv)

t0 = time.time()
mp.mp.dps = 80
PASS, FAIL, NOTE = [], [], []


def check(tag, cond, n=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"K-{tag}: {'PASS' if ok else 'FAIL'}  {n}", flush=True)


def note(tag, msg):
    NOTE.append((tag, msg))
    print(f"K-{tag}: NOTE  {msg}", flush=True)


# member (same as arm / my part A)
eps = sp.Rational(1, 10)
ffun = 1 / rv * (1 + eps * sp.cos(thv) ** 2)
Wf = sp.Integer(1)
fr = sp.diff(ffun, rv)
fth = sp.diff(ffun, thv)
Pf = ffun * rv ** 2 * Wf * fr ** 2 + fth ** 2
qfun = 2 * rv ** 2 * Wf * fr * fth / Pf
Df = sp.simplify(rv ** 2 * Wf - ffun * qfun ** 2)
th0 = sp.pi / 3
Df3 = sp.simplify(Df.subs(thv, th0))


def build_K(metric):
    gi = metric.inv()
    G = christoffel(metric, gi, UXS)
    Rm = riemann_mixed(G, UXS)
    return kretschmann(Rm, metric, gi, UXS)


print("=" * 72)
print("PART (1) — Kretschmann on the STATIC slice (reproduce arm K~D^-3)")
print("=" * 72)
print(f"   [building K (static, a=b=0) ... {time.time()-t0:.0f}s]",
      flush=True)
g_static = udt_metric(ffun, qfun, sp.S(0), sp.S(0), sp.S(0))
K_static = build_K(g_static)
print(f"   [K_static assembled {time.time()-t0:.0f}s]", flush=True)
K_static3 = K_static.subs(thv, th0)
Df3f = sp.lambdify(rv, Df3, 'mpmath')
K_static_f = sp.lambdify(rv, K_static3, 'mpmath')

# high-precision root of D=0:
numDf = sp.Poly(sp.expand(sp.numer(sp.together(Df3))), rv)
rmp = None
for rt in mp.polyroots([mp.mpf(str(c)) for c in numDf.all_coeffs()],
                       maxsteps=400, extraprec=400):
    if abs(mp.im(rt)) < mp.mpf('1e-50') and mp.re(rt) > 0:
        rmp = mp.re(rt)
        break
note("rstar", f"r*_mp = {mp.nstr(rmp, 25)}")

print(f"\n{'delta':>8} {'D':>18} {'K(static,80dps)':>26} {'K(float64)':>20}")
rows = []
for k in range(2, 11):
    delta = mp.mpf(10) ** (-k)
    rval = rmp * (1 + delta)
    Dv = Df3f(rval)
    Kv = K_static_f(rval)
    # float64 path: evaluate the same expression in double precision
    try:
        Kf64 = complex(K_static3.subs(rv, float(rval)).evalf(17)).real
    except Exception:
        Kf64 = float('nan')
    rows.append((float(delta), Dv, Kv, Kf64))
    print(f"{mp.nstr(delta,2):>8} {mp.nstr(Dv,4):>18} "
          f"{mp.nstr(Kv,6):>26} {Kf64:>20.4e}", flush=True)

# fit K ~ D^p on the clean mpmath data
xs = [math.log(abs(float(Dv))) for (_, Dv, Kv, _) in rows if Kv != 0]
ys = [math.log(abs(float(Kv))) for (_, Dv, Kv, _) in rows if Kv != 0]
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) \
    / sum((x - mx) ** 2 for x in xs)
pred = [my + slope * (x - mx) for x in xs]
rms = (sum((y - p) ** 2 for y, p in zip(ys, pred)) / len(xs)) ** 0.5
note("static-exp", f"K(static) ~ D^({slope:+.4f}) (RMS {rms:.1e}) "
     "[arm claims K~D^-3 on q*]")
check("static-diverges", slope < -1.0 and rms < 0.05,
      f"static-slice K DIVERGES as clean power law D^{slope:.2f} "
      "(reproduces arm's q* singularity claim on MY engine).")

# float64 sign-flip trap
f64_signs = [math.copysign(1, x[3]) for x in rows if not math.isnan(x[3])]
mp_signs = [1 if mp.re(x[2]) > 0 else -1 for x in rows]
f64_erratic = len(set(f64_signs)) > 1
mp_clean = len(set(mp_signs)) == 1
check("float64-trap", f64_erratic and mp_clean,
      f"CONFIRMED: float64 K sign {'FLIPS' if f64_erratic else 'stable'} "
      f"near D~1e-7 (catastrophic cancellation) while mpmath sign "
      f"{'STABLE' if mp_clean else 'flips'} -> the divergence is real, "
      "the float64 sign-flip is the cancellation artifact (brief's trap).")

# ---------------------------------------------------------------------
print()
print("=" * 72)
print("PART (2) — KRETSCHMANN with the SAME-MINUS TIME ROW ON")
print("=" * 72)
print(f"   [building K (time row a,b != 0) ... {time.time()-t0:.0f}s]",
      flush=True)
aval = sp.Rational(1, 5)
bval = sp.Rational(1, 7)
g_ab = udt_metric(ffun, qfun, sp.S(0), aval, bval)
K_ab = build_K(g_ab)
print(f"   [K(a,b) assembled {time.time()-t0:.0f}s]", flush=True)
K_ab3 = K_ab.subs(thv, th0)
K_ab_f = sp.lambdify(rv, K_ab3, 'mpmath')

print(f"\n{'delta':>8} {'D':>18} {'K(a,b ON, 80dps)':>26}")
ab_rows = []
for k in range(2, 11):
    delta = mp.mpf(10) ** (-k)
    rval = rmp * (1 + delta)
    Dv = Df3f(rval)
    Kv = K_ab_f(rval)
    ab_rows.append((float(delta), Dv, Kv))
    print(f"{mp.nstr(delta,2):>8} {mp.nstr(Dv,4):>18} "
          f"{mp.nstr(Kv,8):>26}", flush=True)

K_ab_first = abs(float(ab_rows[0][2]))
K_ab_last = abs(float(ab_rows[-1][2]))
ab_bounded = K_ab_last < K_ab_first * 100      # within 2 orders = bounded
note("ab-range", f"K(a,b ON): {mp.nstr(ab_rows[0][2],6)} -> "
     f"{mp.nstr(ab_rows[-1][2],6)} as D: {mp.nstr(ab_rows[0][1],3)} -> "
     f"{mp.nstr(ab_rows[-1][1],3)}")
check("ab-bounded", ab_bounded,
      f"K with the same-minus TIME ROW ON STAYS BOUNDED through D->0 "
      f"(|K|: {K_ab_first:.3e} -> {K_ab_last:.3e}). The static-slice "
      "K~D^-3 blow-up is LIFTED by the time row -> the curvature "
      "divergence was an artifact of the a=b=0 fixed-point slice "
      "through a MIRROR surface, NOT a true edge.")

print()
print("=" * 72)
print("VERDICT (Kretschmann)")
print("=" * 72)
if ('static-diverges' in PASS) and ('ab-bounded' in PASS):
    print("  >>> K DIVERGES on the static slice but is BOUNDED with the")
    print("  >>> same-minus time row ON. The arm's curvature singularity")
    print("  >>> is a STATIC-SLICE ARTIFACT. ==> MIRROR FOLD.")
elif ('static-diverges' in PASS) and ('ab-bounded' not in PASS):
    print("  >>> K diverges BOTH on the static slice and with the time")
    print("  >>> row ON. ==> TRUE EDGE (arm Phase-0 stands).")
else:
    print("  >>> inconclusive (static K did not reproduce) -- inspect.")

print(f"\nK PART: {len(PASS)} PASS / {len(FAIL)} FAIL ({time.time()-t0:.0f}s)")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0 if not FAIL else 1)
