#!/usr/bin/env python3
"""VFOLD TEST C (part 1): reproduce the arm's STATIC-SLICE (a=b=0)
curvature divergence with MY OWN engine, then re-derive the exponents
independently at >=50 digits on the q* branch member. Confirm the float64
catastrophic-cancellation sign-flip trap near D~1e-7.

PRE-REGISTERED CRITERIA:
  C1: my engine, on the arm's exact member (f=(1/r)(1+eps cos^2 th),
      eps=1/10, w=0, q=q*, theta=pi/3), must show R,K DIVERGING as clean
      power laws at >=50-digit mpmath. Expect (arm) R~D^{-3/2}, K~D^{-3}
      on the q* tangential branch.  PASS if I independently reproduce
      divergence with stable exponents; FAIL if bounded.
  C2: float64 evaluation of K must go ERRATIC / SIGN-FLIP near D~1e-7
      while mpmath stays a clean power law -> confirms the trap is real
      and the arm correctly avoided it.
  C3: generic transversal q (NOT q*) -> R~D^{-2}, K~D^{-4} (steeper),
      independent reproduction.

This establishes my engine reproduces the arm's STATIC-SLICE result, so
the time-row lift test (vfold_timerow_curv.py) is a like-for-like attack,
not a machinery disagreement.

Log: /tmp/vfold_static_slice.log
"""
import math
import sys
import time

import mpmath as mp
import sympy as sp

from vfold_curv_engine import kretschmann

t0 = time.time()
mp.mp.dps = 60

r = sp.Symbol('r', positive=True)
th = sp.Symbol('theta', real=True)
T, ph = sp.symbols('T varphi', real=True)

eps = sp.Rational(1, 10)
ffun = (1 / r) * (1 + eps * sp.cos(th) ** 2)
W = sp.Integer(1)              # w=0
fr = sp.diff(ffun, r)
fth = sp.diff(ffun, th)
P = ffun * r ** 2 * W * fr ** 2 + fth ** 2
qstar = 2 * r ** 2 * W * fr * fth / P
D = r ** 2 * W - ffun * qstar ** 2


def build_g4(qval):
    return sp.Matrix([
        [-ffun, 0, 0, 0],
        [0, 1 / ffun, qval, 0],
        [0, qval, r ** 2 * W, 0],
        [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / W],
    ])


def approach_fit(K3_f, R3_f, D3_f, rstar_mp, label):
    print(f"\n--- {label} ---")
    print(f"{'k':>4} {'D':>20} {'R':>24} {'K':>24}")
    rows = []
    for k in range(2, 11):
        delta = mp.mpf(10) ** (-k)
        rv = rstar_mp * (1 + delta)
        Dv, Rv, Kv = D3_f(rv), R3_f(rv), K3_f(rv)
        rows.append((Dv, Rv, Kv))
        print(f"{k:>4} {mp.nstr(Dv, 4):>20} {mp.nstr(Rv, 6):>24} "
              f"{mp.nstr(Kv, 6):>24}", flush=True)
    # fit
    def fit(idx):
        xs, ys = [], []
        for (Dv, Rv, Kv) in rows[-6:]:
            v = Rv if idx == 'R' else Kv
            if Dv != 0 and v != 0:
                xs.append(math.log(abs(float(Dv))))
                ys.append(math.log(abs(float(v))))
        nn = len(xs)
        mx, my = sum(xs) / nn, sum(ys) / nn
        sl = (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
              / sum((x - mx) ** 2 for x in xs))
        pred = [my + sl * (x - mx) for x in xs]
        rms = (sum((y - p) ** 2 for y, p in zip(ys, pred)) / nn) ** 0.5
        return sl, rms
    sR, rR = fit('R')
    sK, rK = fit('K')
    print(f"  R ~ D^({sR:+.3f}) RMS {rR:.1e};  K ~ D^({sK:+.3f}) RMS {rK:.1e}")
    return sR, sK, rows


print("=" * 72)
print("C1 — q* branch, static slice (a=b=0), MY engine, 60-digit")
print("=" * 72)
g4q = build_g4(qstar)
K_q, R_q = kretschmann(g4q, [T, r, th, ph])
print(f"  [curvature built {time.time()-t0:.0f}s]", flush=True)
sub3 = {th: sp.pi / 3}
Rq3 = sp.simplify(R_q.subs(sub3))
Kq3 = sp.simplify(K_q.subs(sub3))
Dq3 = sp.simplify(D.subs(sub3))
print(f"  [specialized theta=pi/3 {time.time()-t0:.0f}s]", flush=True)
numD = sp.numer(sp.together(Dq3))
poly = sp.Poly(sp.expand(numD), r)
roots = mp.polyroots([mp.mpf(str(c)) for c in poly.all_coeffs()],
                     maxsteps=300, extraprec=300)
rstar = None
for rt in roots:
    if abs(mp.im(rt)) < mp.mpf('1e-40') and mp.re(rt) > 0:
        rstar = mp.re(rt)
        break
print(f"  r* (60-digit) = {mp.nstr(rstar, 25)}", flush=True)
Rq3f = sp.lambdify(r, Rq3, 'mpmath')
Kq3f = sp.lambdify(r, Kq3, 'mpmath')
Dq3f = sp.lambdify(r, Dq3, 'mpmath')
sR, sK, rows = approach_fit(Kq3f, Rq3f, Dq3f, rstar, "q* branch (60-dps)")
c1 = (sR < -0.5 and sK < -1.0 and
      abs(sR - (-1.5)) < 0.4 and abs(sK - (-3.0)) < 0.6)
print(f"\n  C1 q* exponents R~{sR:.2f} (arm -1.5), K~{sK:.2f} (arm -3.0): "
      f"{'PASS' if c1 else 'CHECK'}")

print()
print("=" * 72)
print("C2 — float64 SIGN-FLIP TRAP near D~1e-7 (q*, theta=pi/3)")
print("=" * 72)
Kq3f64 = sp.lambdify(r, Kq3, 'numpy')
Dq3f64 = sp.lambdify(r, Dq3, 'numpy')
import numpy as np
flip = False
prev_sign = None
print(f"{'k':>4} {'D(f64)':>16} {'K(f64)':>20} {'K(mpmath)':>22}")
for k in range(2, 13):
    rv64 = float(rstar) * (1 + 10.0 ** (-k))
    try:
        Kf64 = Kq3f64(rv64)
        Df64 = Dq3f64(rv64)
    except Exception as e:
        Kf64 = float('nan'); Df64 = float('nan')
    rvmp = rstar * (1 + mp.mpf(10) ** (-k))
    Kmp = Kq3f(rvmp)
    s = (1 if (isinstance(Kf64, float) and Kf64 > 0) else
         -1 if (isinstance(Kf64, float) and Kf64 < 0) else 0)
    if prev_sign is not None and s != 0 and s != prev_sign:
        flip = True
    if s != 0:
        prev_sign = s
    print(f"{k:>4} {Df64:>16.3e} {Kf64:>20.4e} {mp.nstr(Kmp, 6):>22}",
          flush=True)
print(f"\n  C2 float64 K sign-flips/erratic while mpmath clean power law: "
      f"{'PASS (trap confirmed)' if flip else 'no flip seen in range'}")

print()
print("=" * 72)
print("C3 — GENERIC transversal q (q = q*/2, NOT the branch), 60-digit")
print("=" * 72)
qgen = qstar / 2          # smooth non-q* off-diagonal: crosses D=0 linearly
Dgen = r ** 2 * W - ffun * qgen ** 2
g4g = build_g4(qgen)
K_g, R_g = kretschmann(g4g, [T, r, th, ph])
print(f"  [generic curvature built {time.time()-t0:.0f}s]", flush=True)
Rg3 = sp.simplify(R_g.subs(sub3))
Kg3 = sp.simplify(K_g.subs(sub3))
Dg3 = sp.simplify(Dgen.subs(sub3))
numDg = sp.numer(sp.together(Dg3))
polyg = sp.Poly(sp.expand(numDg), r)
rootsg = mp.polyroots([mp.mpf(str(c)) for c in polyg.all_coeffs()],
                      maxsteps=300, extraprec=300)
rstarg = None
for rt in rootsg:
    if abs(mp.im(rt)) < mp.mpf('1e-40') and mp.re(rt) > 0:
        rstarg = mp.re(rt)
        break
print(f"  r*_gen = {mp.nstr(rstarg, 25)}", flush=True)
Rg3f = sp.lambdify(r, Rg3, 'mpmath')
Kg3f = sp.lambdify(r, Kg3, 'mpmath')
Dg3f = sp.lambdify(r, Dg3, 'mpmath')
sRg, sKg, _ = approach_fit(Kg3f, Rg3f, Dg3f, rstarg, "generic q (60-dps)")
c3 = (sKg < -2.0 and abs(sKg - (-4.0)) < 0.7 and abs(sRg - (-2.0)) < 0.6)
print(f"\n  C3 generic exponents R~{sRg:.2f} (arm -2), K~{sKg:.2f} (arm -4): "
      f"{'PASS' if c3 else 'CHECK'}")

print(f"\nVFOLD STATIC-SLICE done ({time.time()-t0:.0f}s). "
      f"q*:R{sR:.2f}/K{sK:.2f}  gen:R{sRg:.2f}/K{sKg:.2f}  trap={flip}")
sys.exit(0)
