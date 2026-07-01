#!/usr/bin/env python3
"""W6 FLUX-TEST — PHASE 0 ADJUDICATION 2: IS THE D=0 CURVATURE
SINGULARITY A METRIC FACT OR A q* ARTIFACT?

Date: 2026-06-12.  Driver: W6 FLUX-TEST agent.  w6_flux_curv.py found a
GENUINE curvature singularity (R~D^{-3/2}, K~D^{-3}, 80-digit clean) at
D=0 -- but ON the q = q* eliminated configuration. The brief's NON-
NEGOTIABLE (1) warns: the q-eliminated form is singular at Delta_w BY
CONSTRUCTION. So the decisive question for the INVARIANT character:

  Does the curvature singularity at D=0 depend on q being the SPECIFIC
  eliminated branch q* = 2 r^2 W f_r f_th/P, or does ANY smooth metric
  whose (r,theta) block determinant D = r^2 W - f q^2 passes through 0
  carry a curvature singularity there?

If singular for a GENERIC smooth q(r,theta) reaching D=0 -> the
singularity is a property of the METRIC at D=0 (a real wall: the
spacetime is geodesically/curvature singular on that surface; the
cell-partition reading is then SUPERSEDED by a stronger statement --
the surface is a curvature edge), INDEPENDENT of the elimination.

If FINITE for a generic smooth q (singular only for q=q*) -> the
divergence is tied to the q*-branch field configuration (the
elimination's own breakdown, W5 L_qq~Delta_w^{-3}), i.e. it lives in
the ELIMINATED dynamics, not the bare metric -- pushing back toward a
chart/elimination artifact and the unreduced-3-field Phase 1.

TEST: same f=(1/r)(1+eps cos^2), w=0 background. Replace q* by a GENERIC
smooth field q_gen(r,theta) = alpha(theta) (r - r0(theta)) + q0 chosen
so that D = r^2 - f q_gen^2 has a SIMPLE ZERO at a chosen (r*,theta*)
with q_gen, dq_gen FINITE and generic there (NOT the q* branch, whose
own derivatives carry P, Delta_w structure). Compute R, K at 80 digits
approaching that D=0.

Log: /tmp/w6_flux_curv_generic.log
"""
import sys
import time
import math

import mpmath as mp
import sympy as sp

t0 = time.time()
mp.mp.dps = 80

T, ph = sp.symbols('T varphi', real=True)
r = sp.Symbol('r', positive=True)
th = sp.Symbol('theta', real=True)

eps = sp.Rational(1, 10)
ffun = 1 / r * (1 + eps * sp.cos(th) ** 2)
Wf = sp.Integer(1)

# GENERIC smooth q reaching D=0. Pick a target latitude theta*=pi/3 and
# a target radius r0; set q_gen so that at (r0, pi/3) we have
# D = r0^2 - f(r0) q_gen^2 = 0 with q_gen a SMOOTH generic function.
# Simplest generic smooth choice: q_gen = c0 + c1*(r) + c2*cos^2(th),
# constants, NOT the q* combination. Then D(r,th) = r^2 - f q_gen^2 is a
# smooth function with (generically) a simple zero surface. We just need
# q_gen, its r- and theta-derivatives to be O(1) and NOT carry the
# 1/P, 1/Delta_w structure of q*.
r0 = sp.Rational(10)
# choose constants so D(r0, pi/3)=0: f(r0,pi/3) = (1/r0)(1+eps/4).
f0 = (1 / r0) * (1 + eps * sp.Rational(1, 4))
# want r0^2 - f0 q_gen0^2 = 0 -> q_gen0 = r0/sqrt(f0)
q_gen0 = r0 / sp.sqrt(f0)
# make q_gen depend smoothly on r and theta so the metric is curved and
# the zero is a generic simple zero (nonzero gradient of D):
qfun = q_gen0 + sp.Rational(1, 7) * (r - r0) \
    + sp.Rational(1, 5) * (sp.cos(th) ** 2 - sp.Rational(1, 4))
# this q is a smooth, generic field (linear in r, quadratic in cos th),
# NOT q*. Verify it is finite & smooth and reaches D=0 at (r0, pi/3).

g4f = sp.Matrix([[-ffun, 0, 0, 0],
                 [0, 1 / ffun, qfun, 0],
                 [0, qfun, r ** 2 * Wf, 0],
                 [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / Wf]])
Df = sp.simplify(r ** 2 * Wf - ffun * qfun ** 2)
xs4 = [T, r, th, ph]
n = 4

print("=" * 72)
print("GENERIC (NON-q*) smooth q reaching D=0 at (r0=10, theta=pi/3)")
print("=" * 72)
Dcheck = sp.nsimplify(Df.subs({r: r0, th: sp.pi / 3}))
print(f"   D(r0,pi/3) = {sp.simplify(Dcheck)}  (should be 0)")
print(f"   q_gen(r0,pi/3) = {sp.nsimplify(qfun.subs({r: r0, th: sp.pi/3}))} "
      f"(finite, generic)")
print(f"   dq/dr = {sp.diff(qfun, r)} (const, O(1)), "
      f"dq/dth carries only cos*sin (smooth)", flush=True)


def christoffel(g, xs):
    gi = g.inv()
    nn = len(xs)
    Gam = [[[sp.S(0)] * nn for _ in range(nn)] for _ in range(nn)]
    for c in range(nn):
        for a in range(nn):
            for b in range(nn):
                e = sum(gi[c, d] * (sp.diff(g[d, a], xs[b])
                                    + sp.diff(g[d, b], xs[a])
                                    - sp.diff(g[a, b], xs[d]))
                        for d in range(nn)) / 2
                Gam[c][a][b] = sp.together(e)
    return Gam, gi


Gam, gi4 = christoffel(g4f, xs4)
print(f"   [Christoffels {time.time()-t0:.0f}s]", flush=True)
Riem = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
        for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(c + 1, n):
                e = (sp.diff(Gam[a][b][d], xs4[c])
                     - sp.diff(Gam[a][b][c], xs4[d]))
                for ee in range(n):
                    e += (Gam[a][c][ee] * Gam[ee][b][d]
                          - Gam[a][d][ee] * Gam[ee][b][c])
                Riem[a][b][c][d] = sp.together(e)
                Riem[a][b][d][c] = -Riem[a][b][c][d]
print(f"   [Riemann {time.time()-t0:.0f}s]", flush=True)
Rlow = [[[[sum(g4f[a, e] * Riem[e][b][c][d] for e in range(n))
           for d in range(n)] for c in range(n)]
         for b in range(n)] for a in range(n)]
Ric = sp.zeros(n, n)
for b in range(n):
    for d in range(n):
        Ric[b, d] = sum(Riem[a][b][a][d] for a in range(n))
Rsc = sp.together(sum(gi4[b, d] * Ric[b, d]
                      for b in range(n) for d in range(n)))
K = sp.S(0)
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                Rl = Rlow[a][b][c][d]
                if Rl == 0:
                    continue
                Rup = sum(gi4[a, ai] * gi4[b, bi] * gi4[c, ci]
                          * gi4[d, di] * Rlow[ai][bi][ci][di]
                          for ai in range(n) for bi in range(n)
                          for ci in range(n) for di in range(n))
                K += Rl * Rup
print(f"   [curvature scalars assembled {time.time()-t0:.0f}s]",
      flush=True)
Rsc3 = sp.simplify(Rsc.subs(th, sp.pi / 3))
K3 = sp.simplify(K.subs(th, sp.pi / 3))
Df3 = sp.simplify(Df.subs(th, sp.pi / 3))
print(f"   [theta=pi/3 specialization {time.time()-t0:.0f}s]", flush=True)
Rsc3_f = sp.lambdify(r, Rsc3, modules='mpmath')
K3_f = sp.lambdify(r, K3, modules='mpmath')
Df3_f = sp.lambdify(r, Df3, modules='mpmath')

# r* = 10 exactly (by construction). Approach from above.
rstar_mp = mp.mpf(10)
print()
print("=" * 72)
print("HIGH-PRECISION APPROACH D->0  (80-digit)")
print("=" * 72)
print(f"{'delta':>10} {'D':>22} {'R':>26} {'K':>26}")
rows = []
for k in range(2, 11):
    delta = mp.mpf(10) ** (-k)
    rv = rstar_mp * (1 + delta)
    Dv = Df3_f(rv)
    Rv = Rsc3_f(rv)
    Kv = K3_f(rv)
    rows.append((float(delta), Dv, Rv, Kv))
    print(f"{mp.nstr(delta, 4):>10} {mp.nstr(Dv, 6):>22} "
          f"{mp.nstr(Rv, 8):>26} {mp.nstr(Kv, 8):>26}", flush=True)


def fit_exponent(rows, which):
    xs, ys = [], []
    for (_, Dv, Rv, Kv) in rows[-6:]:
        val = (Rv if which == 'R' else Kv)
        if Dv != 0 and val != 0:
            xs.append(math.log(abs(float(Dv))))
            ys.append(math.log(abs(float(val))))
    nn = len(xs)
    mx, my = sum(xs) / nn, sum(ys) / nn
    sl = (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
          / sum((x - mx) ** 2 for x in xs))
    pred = [my + sl * (x - mx) for x in xs]
    rms = (sum((y - p) ** 2 for y, p in zip(ys, pred)) / nn) ** 0.5
    return sl, rms


slR, rmsR = fit_exponent(rows, 'R')
slK, rmsK = fit_exponent(rows, 'K')
print()
print(f"   R ~ D^({slR:+.4f})   (RMS {rmsR:.2e})")
print(f"   K ~ D^({slK:+.4f})   (RMS {rmsK:.2e})")
diverges = (slR < -0.3 or slK < -0.5)
bounded = (abs(slR) < 0.2 and abs(slK) < 0.2)
print()
print("=" * 72)
print("VERDICT: q* artifact vs metric fact")
print("=" * 72)
if diverges:
    print("  >>> The curvature DIVERGES even for a GENERIC smooth q at")
    print("  >>> D=0 (not just q*). => D=0 is a CURVATURE SINGULARITY of")
    print("  >>> the METRIC itself (the q^2 off-diagonal sends the block")
    print("  >>> determinant -> 0; curvature ~ 1/D powers). The")
    print("  >>> singularity is a METRIC FACT, not a q*-elimination")
    print("  >>> artifact. Phase-0 verdict (a) stands and STRENGTHENS.")
elif bounded:
    print("  >>> The curvature is BOUNDED for a generic smooth q at D=0.")
    print("  >>> => the singularity found on q* is tied to the q*")
    print("  >>> ELIMINATED configuration (its derivatives carry P,")
    print("  >>> Delta_w), i.e. an elimination/chart artifact, NOT a")
    print("  >>> bare-metric singularity. Pushes toward (c)/Phase 1.")
else:
    print("  >>> INCONCLUSIVE.")
print(f"\nW6 FLUX CURV GENERIC: ({time.time()-t0:.0f}s)")
sys.exit(0)
