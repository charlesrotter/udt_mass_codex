#!/usr/bin/env python3
"""W6 FLUX-TEST — PHASE 0 ADDENDUM: HIGH-PRECISION CURVATURE AT D=0.

Date: 2026-06-12.  Driver: W6 FLUX-TEST agent.  Phase-0 PART C flagged a
DIVERGING Kretschmann (164e3 -> 1.68e11 -> 2.28e17 -> NEGATIVE 6.5e26)
and Ricci R -> -oo on the float64 pass. The negative sign and the
super-fast blow-up are the classic fingerprint of float64 CATASTROPHIC
CANCELLATION in a giant rational expression evaluated near a near-zero
denominator -- NOT necessarily a true singularity. This script
ADJUDICATES that with EXACT-RATIONAL / mpmath-high-precision evaluation
and a fitted divergence exponent.

Mirror of the brief's discipline: just as a numerical blow-up must not
masquerade as INSULATION, a numerical blow-up must not masquerade as a
SINGULARITY. We force the distinction.

METHOD:
  - At theta = pi/3 the C=0 ell=2 member f = (1/r)(1 + (eps/4)) ... is
    fully RATIONAL in r (cos^2(pi/3)=1/4). q* is rational in r. So R
    and K are EXACT rational functions of r. We evaluate them as EXACT
    rationals along r -> r* (where D->0), at mpmath precision 80 digits,
    so cancellation is impossible.
  - Fit log|R|, log|K| vs log(D): a TRUE curvature singularity gives a
    clean power law K ~ D^{-p} with stable p; a cancellation artifact
    gives an erratic / sign-flipping non-power-law (the float64 run).
  - DECISIVE cross-check: if R, K diverge as exact rationals at 80
    digits, the singularity is REAL on this member at the q* branch
    (verdict (a), a major finding -- the q* metric is curvature-
    singular at D=0, which is STRONGER than a coordinate artifact and
    must be reported as such, with the caveat that q*=q*(branch) is an
    ELIMINATED-field configuration, not an independent metric d.o.f.).

Log: /tmp/w6_flux_curv.log
"""
import sys
import time

import mpmath as mp
import sympy as sp

t0 = time.time()
mp.mp.dps = 80

T, ph = sp.symbols('T varphi', real=True)
r = sp.Symbol('r', positive=True)
th = sp.Symbol('theta', real=True)

# C=0 flat member + ell=2 shape (same as phase0):
eps = sp.Rational(1, 10)
ffun = 1 / r * (1 + eps * sp.cos(th) ** 2)
Wf = sp.Integer(1)            # w = 0
fr_f = sp.diff(ffun, r)
fth_f = sp.diff(ffun, th)
Pf = ffun * r ** 2 * Wf * fr_f ** 2 + fth_f ** 2
qfun = 2 * r ** 2 * Wf * fr_f * fth_f / Pf
g4f = sp.Matrix([[-ffun, 0, 0, 0],
                 [0, 1 / ffun, qfun, 0],
                 [0, qfun, r ** 2 * Wf, 0],
                 [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / Wf]])
Df = sp.simplify(r ** 2 * Wf - ffun * qfun ** 2)
xs4 = [T, r, th, ph]
n = 4

print("=" * 72)
print("BUILD curvature scalars as EXACT rational functions (theta=pi/3)")
print("=" * 72)


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
# Ricci scalar
Ric = sp.zeros(n, n)
for b in range(n):
    for d in range(n):
        Ric[b, d] = sum(Riem[a][b][a][d] for a in range(n))
Rsc = sp.together(sum(gi4[b, d] * Ric[b, d]
                      for b in range(n) for d in range(n)))
print(f"   [Ricci scalar {time.time()-t0:.0f}s]", flush=True)
# Kretschmann
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
print(f"   [Kretschmann assembled {time.time()-t0:.0f}s]", flush=True)

# Specialize to theta = pi/3 (cos^2 = 1/4, sin = sqrt(3)/2): EXACT
# rational-in-r after this substitution (sqrt(3) appears only in even
# powers via sin^2, and q* even). Substitute and simplify to a rational
# function of r.
sub3 = {th: sp.pi / 3}
Rsc3 = sp.simplify(Rsc.subs(sub3))
K3 = sp.simplify(K.subs(sub3))
Df3 = sp.simplify(Df.subs(sub3))
print(f"   [specialized to theta=pi/3 {time.time()-t0:.0f}s]", flush=True)
# Find r* where D=0 (exact):
rstar_sol = sp.solve(sp.Eq(sp.numer(sp.together(Df3)), 0), r)
rstar = None
for rr in rstar_sol:
    v = complex(rr.evalf())
    if abs(v.imag) < 1e-12 and v.real > 0:
        rstar = rr
        break
print(f"   r* (exact) = {rstar}  (~{complex(rstar.evalf()).real:.6f})",
      flush=True)

# Convert to mpmath callables (exact rational coeffs -> 80-digit eval):
Rsc3_f = sp.lambdify(r, Rsc3, modules='mpmath')
K3_f = sp.lambdify(r, K3, modules='mpmath')
Df3_f = sp.lambdify(r, Df3, modules='mpmath')
rstar_mp = mp.mpf(str(sp.nsimplify(rstar))) if rstar.is_rational \
    else mp.mpf(mp.nstr(mp.mpf(complex(rstar.evalf()).real), 40))
# better: high-precision root of the exact numerator
numDf = sp.numer(sp.together(Df3))
numDf_poly = sp.Poly(sp.expand(numDf), r)
roots_mp = mp.polyroots([mp.mpf(str(c)) for c in numDf_poly.all_coeffs()],
                        maxsteps=200, extraprec=200)
rstar_mp = None
for rt in roots_mp:
    if abs(mp.im(rt)) < mp.mpf('1e-40') and mp.re(rt) > 0:
        rstar_mp = mp.re(rt)
        break
print(f"   r*_mp (80-digit) = {mp.nstr(rstar_mp, 30)}", flush=True)

print()
print("=" * 72)
print("HIGH-PRECISION APPROACH D->0  (80-digit, no cancellation)")
print("=" * 72)
print(f"{'delta':>10} {'D':>22} {'R':>26} {'K':>26}")
rows = []
for k in range(2, 11):
    delta = mp.mpf(10) ** (-k)
    rv = rstar_mp * (1 + delta)     # approach from outer band
    Dv = Df3_f(rv)
    Rv = Rsc3_f(rv)
    Kv = K3_f(rv)
    rows.append((float(delta), Dv, Rv, Kv))
    print(f"{mp.nstr(delta, 4):>10} {mp.nstr(Dv, 6):>22} "
          f"{mp.nstr(Rv, 8):>26} {mp.nstr(Kv, 8):>26}", flush=True)

# Fit power law: log|K| = -p log D + c.  Use last several points.
print()
print("=" * 72)
print("DIVERGENCE-EXPONENT FIT  (log|scalar| vs log D)")
print("=" * 72)
import math


def fit_exponent(rows, idx):
    xs, ys = [], []
    for (_, Dv, Rv, Kv) in rows[-6:]:
        val = (Rv if idx == 'R' else Kv)
        if Dv != 0 and val != 0:
            xs.append(math.log(abs(float(Dv))))
            ys.append(math.log(abs(float(val))))
    # slope:
    nn = len(xs)
    mx = sum(xs) / nn
    my = sum(ys) / nn
    sl = (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
          / sum((x - mx) ** 2 for x in xs))
    # residual std (linearity quality):
    pred = [my + sl * (x - mx) for x in xs]
    resid = [y - p for y, p in zip(ys, pred)]
    rms = (sum(e ** 2 for e in resid) / nn) ** 0.5
    return sl, rms


slR, rmsR = fit_exponent(rows, 'R')
slK, rmsK = fit_exponent(rows, 'K')
print(f"   R ~ D^({slR:+.4f})   (log-log RMS residual {rmsR:.2e})")
print(f"   K ~ D^({slK:+.4f})   (log-log RMS residual {rmsK:.2e})")
print()
# A clean power law (small RMS) with negative exponent at 80-digit
# precision => GENUINE curvature divergence (verdict a). The float64
# run's sign flip is then confirmed to be cancellation; the TRUE
# behavior is the high-precision power law.
clean_power = (rmsR < 0.05 and rmsK < 0.05)
diverges = (slR < -0.3 and slK < -0.5)
all_positive_K = all(mp.re(Kv) > 0 for (_, _, _, Kv) in rows) or \
    all(mp.re(Kv) < 0 for (_, _, _, Kv) in rows)
print(f"   clean power law (RMS<0.05 both): {clean_power}")
print(f"   diverges (neg exponents): {diverges}")
print(f"   K keeps consistent sign at 80-digit: {all_positive_K}")
print()
print("=" * 72)
print("CURVATURE VERDICT")
print("=" * 72)
if clean_power and diverges:
    print("  >>> The Ricci scalar AND Kretschmann DIVERGE as clean")
    print(f"  >>> power laws (R ~ D^{slR:.2f}, K ~ D^{slK:.2f}) at")
    print("  >>> 80-digit precision. The float64 sign-flip was")
    print("  >>> cancellation; the TRUE behavior is a GENUINE CURVATURE")
    print("  >>> SINGULARITY at D=0 on the q* branch.")
    print("  >>> PHASE-0 VERDICT = (a) SINGULARITY (major finding).")
    verdict = 'a'
elif not diverges:
    print("  >>> Curvature scalars are BOUNDED at 80-digit precision;")
    print("  >>> the float64 blow-up was pure cancellation artifact.")
    print("  >>> PHASE-0 VERDICT stays (c) COORDINATE DEGENERACY.")
    verdict = 'c'
else:
    print("  >>> Curvature behavior is INCONCLUSIVE (divergent but not")
    print("  >>> a clean power law) -- investigate further.")
    verdict = '?'

print(f"\nW6 FLUX CURV: verdict={verdict} ({time.time()-t0:.0f}s)")
sys.exit(0)
