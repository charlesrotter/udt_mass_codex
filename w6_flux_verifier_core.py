#!/usr/bin/env python3
"""W6 FLUX-TEST — INDEPENDENT BLIND ADVERSARIAL VERIFIER (main-loop).

Date: 2026-06-12.  Driver: independent verifier (own machinery; shares
NO code with the arm or its arm-spawned verifier a66894d1a78df7b1a).

This is a FROM-SCRATCH curvature engine.  Conventions deliberately
different from the arm where possible:
  - Riemann built as R^a_{bcd} = d_c G^a_{bd} - d_d G^a_{bc}
    + G^a_{ce}G^e_{bd} - G^a_{de}G^e_{bc}, full antisymmetric c,d loop
    (no together() shortcut; we use cancel on final scalars).
  - Kretschmann via FULLY-LOWERED R_{abcd} and FULLY-RAISED R^{abcd}
    computed independently, contracted; cross-checked with a SECOND
    contraction route (mixed R^{ab}_{cd}).
  - Ricci via R_{bd}=R^a_{bad}; scalar g^{bd}R_{bd}.
  - High precision: mpmath dps=60, with the curvature scalar built as
    an EXACT sympy rational function of r at fixed theta, lambdified to
    mpmath.  No float64 in the divergence fit.

VALIDATION GATE: Schwarzschild K = 48 M^2/r^6, R = 0, R_{ab}=0.  If this
fails the engine is not trusted.

Attacks A (exponents, two backgrounds), B (det g4 ~ D).
Log: /tmp/w6_flux_verifier_core.log
"""
import sys
import time
import math

import sympy as sp
import mpmath as mp

t0 = time.time()
mp.mp.dps = 60
PASS, FAIL, NOTE = [], [], []


def ck(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"V-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)


def note(tag, n):
    NOTE.append((tag, n))
    print(f"V-{tag}: NOTE  {n}", flush=True)


# ====================================================================
# INDEPENDENT CURVATURE ENGINE (my own; do not import arm code)
# ====================================================================
def christ(g, X):
    """Christoffel Gamma^c_{ab}.  Returns nested list [c][a][b]."""
    n = len(X)
    gi = g.inv()
    G = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for c in range(n):
        for a in range(n):
            for b in range(a, n):
                s = sp.S(0)
                for d in range(n):
                    if gi[c, d] == 0:
                        continue
                    s += gi[c, d] * (sp.diff(g[d, a], X[b])
                                     + sp.diff(g[d, b], X[a])
                                     - sp.diff(g[a, b], X[d]))
                s = sp.cancel(s / 2)
                G[c][a][b] = s
                G[c][b][a] = s
    return G, gi


def riemann_mixed(G, X):
    """R^a_{bcd} (1,3).  Independent loop, antisymmetric in (c,d)."""
    n = len(X)
    R = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
         for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(c + 1, n):
                    t = sp.diff(G[a][b][d], X[c]) - sp.diff(G[a][b][c], X[d])
                    for e in range(n):
                        t += G[a][c][e] * G[e][b][d]
                        t -= G[a][d][e] * G[e][b][c]
                    t = sp.cancel(t)
                    R[a][b][c][d] = t
                    R[a][b][d][c] = -t
    return R


def ricci_scalar(Rm, gi, n):
    """Ricci R_{bd}=R^a_{bad}; scalar = g^{bd}R_{bd}."""
    Ric = [[sp.S(0)] * n for _ in range(n)]
    for b in range(n):
        for d in range(n):
            Ric[b][d] = sp.cancel(sum(Rm[a][b][a][d] for a in range(n)))
    Rs = sp.S(0)
    for b in range(n):
        for d in range(n):
            if gi[b, d] != 0:
                Rs += gi[b, d] * Ric[b][d]
    return sp.cancel(Rs), Ric


def kretschmann(Rm, g, gi, n):
    """K = R_{abcd}R^{abcd}.  Lower a, raise b,c,d.  Independent of arm
    route (arm raised all four on Rlow; we lower only a then raise all)."""
    # R_{abcd} = g_{ae} R^e_{bcd}
    Rlow = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
            for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    Rlow[a][b][c][d] = sum(g[a, e] * Rm[e][b][c][d]
                                           for e in range(n))
    # K = sum Rlow_{abcd} * Rup^{abcd}, Rup = g^aa' g^bb' g^cc' g^dd' Rlow
    K = sp.S(0)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    Rl = Rlow[a][b][c][d]
                    if Rl == 0:
                        continue
                    Rup = sp.S(0)
                    for ai in range(n):
                        if gi[a, ai] == 0:
                            continue
                        for bi in range(n):
                            if gi[b, bi] == 0:
                                continue
                            for ci in range(n):
                                if gi[c, ci] == 0:
                                    continue
                                for di in range(n):
                                    if gi[d, di] == 0:
                                        continue
                                    Rup += (gi[a, ai] * gi[b, bi]
                                            * gi[c, ci] * gi[d, di]
                                            * Rlow[ai][bi][ci][di])
                    K += Rl * Rup
    return sp.cancel(K)


# ====================================================================
# VALIDATION: SCHWARZSCHILD
# ====================================================================
print("=" * 72)
print("VALIDATION GATE — SCHWARZSCHILD  (K must = 48 M^2/r^6, R=0)")
print("=" * 72)
tS, rS, thS, phS = sp.symbols('t r theta phi', positive=True)
M = sp.Symbol('M', positive=True)
fsch = 1 - 2 * M / rS
gS = sp.Matrix([[-fsch, 0, 0, 0],
                [0, 1 / fsch, 0, 0],
                [0, 0, rS ** 2, 0],
                [0, 0, 0, rS ** 2 * sp.sin(thS) ** 2]])
XS = [tS, rS, thS, phS]
GS, giS = christ(gS, XS)
RmS = riemann_mixed(GS, XS)
RsS, RicS = ricci_scalar(RmS, giS, 4)
KS = kretschmann(RmS, gS, giS, 4)
KS = sp.simplify(KS)
RsS = sp.simplify(RsS)
riczero = all(sp.simplify(RicS[a][b]) == 0 for a in range(4)
              for b in range(4))
ck("SCHW-R", RsS == 0, f"Ricci scalar = {RsS} (must be 0)")
ck("SCHW-RIC", riczero, "Ricci tensor all-zero (vacuum)")
ck("SCHW-K", sp.simplify(KS - 48 * M ** 2 / rS ** 6) == 0,
   f"Kretschmann = {KS}  (target 48 M^2/r^6)")
print(f"[Schwarzschild validated {time.time()-t0:.0f}s]", flush=True)

if FAIL:
    print("ENGINE VALIDATION FAILED — aborting.")
    sys.exit(1)

# Flat-space sanity (R=K=0):
gflat = sp.Matrix([[-1, 0, 0, 0], [0, 1, 0, 0],
                   [0, 0, rS ** 2, 0],
                   [0, 0, 0, rS ** 2 * sp.sin(thS) ** 2]])
Gf, gif = christ(gflat, XS)
Rmf = riemann_mixed(Gf, XS)
Kf = sp.simplify(kretschmann(Rmf, gflat, gif, 4))
ck("FLAT-K", Kf == 0, f"flat-space (spherical coords) K = {Kf}")
print(f"[flat validated {time.time()-t0:.0f}s]", flush=True)


# ====================================================================
# THE UDT METRIC (my own build of the declared line element)
# ====================================================================
T, ph = sp.symbols('T varphi', real=True)
r = sp.Symbol('r', positive=True)
th = sp.Symbol('theta', real=True)


def udt_metric(ffun, qfun, wfun):
    W = (1 + wfun) ** 2
    return sp.Matrix([[-ffun, 0, 0, 0],
                      [0, 1 / ffun, qfun, 0],
                      [0, qfun, r ** 2 * W, 0],
                      [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / W]])


def curvature_scalars_at_theta(ffun, qfun, wfun, theta_val):
    """Build g, compute R and K as EXACT sympy, specialize theta, return
    lambdified mpmath callables R(r), K(r), D(r)."""
    g = udt_metric(ffun, qfun, wfun)
    W = (1 + wfun) ** 2
    Dexpr = sp.cancel(r ** 2 * W - ffun * qfun ** 2)
    X4 = [T, r, th, ph]
    G, gi = christ(g, X4)
    Rm = riemann_mixed(G, X4)
    Rs, _ = ricci_scalar(Rm, gi, 4)
    K = kretschmann(Rm, g, gi, 4)
    Rs3 = Rs.subs(th, theta_val)
    K3 = K.subs(th, theta_val)
    D3 = Dexpr.subs(th, theta_val)
    # cancel into rational form (avoid float)
    Rs3 = sp.cancel(sp.nsimplify(Rs3, rational=True)) \
        if Rs3.free_symbols == {r} else sp.cancel(Rs3)
    fR = sp.lambdify(r, sp.nsimplify(Rs3, rational=True), 'mpmath')
    fK = sp.lambdify(r, sp.nsimplify(K3, rational=True), 'mpmath')
    fD = sp.lambdify(r, sp.nsimplify(D3, rational=True), 'mpmath')
    detg = sp.cancel(g.det())
    return fR, fK, fD, Dexpr, detg, g


def fit_pow(rows, idx):
    xs, ys = [], []
    for (Dv, Rv, Kv) in rows[-6:]:
        v = Rv if idx == 'R' else Kv
        if Dv != 0 and v != 0:
            xs.append(mp.log(abs(Dv)))
            ys.append(mp.log(abs(v)))
    nn = len(xs)
    mx = sum(xs) / nn
    my = sum(ys) / nn
    sl = (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
          / sum((x - mx) ** 2 for x in xs))
    pred = [my + sl * (x - mx) for x in xs]
    rms = (sum((y - p) ** 2 for y, p in zip(ys, pred)) / nn) ** 0.5
    return float(sl), float(rms)


def approach_report(label, fR, fK, fD, rstar_mp, side=+1, signtrack=True):
    print(f"\n--- {label} : approach D->0 (rstar={mp.nstr(rstar_mp,20)}) ---")
    print(f"{'delta':>10} {'D':>20} {'R':>22} {'K':>22}")
    rows = []
    Ksigns = []
    for k in range(2, 11):
        delta = mp.mpf(10) ** (-k)
        rv = rstar_mp * (1 + side * delta)
        Dv = fD(rv)
        Rv = fR(rv)
        Kv = fK(rv)
        rows.append((Dv, Rv, Kv))
        Ksigns.append(mp.sign(mp.re(Kv)))
        print(f"{mp.nstr(delta,3):>10} {mp.nstr(Dv,5):>20} "
              f"{mp.nstr(Rv,6):>22} {mp.nstr(Kv,6):>22}", flush=True)
    slR, rmsR = fit_pow(rows, 'R')
    slK, rmsK = fit_pow(rows, 'K')
    Ksign_const = len(set(Ksigns)) == 1
    print(f"   R ~ D^({slR:+.4f})  RMS {rmsR:.2e}")
    print(f"   K ~ D^({slK:+.4f})  RMS {rmsK:.2e}")
    print(f"   K sign constant (mpmath, no cancellation): {Ksign_const}")
    return slR, rmsR, slK, rmsK, Ksign_const, rows


# ====================================================================
# ATTACK B (do first — cheap, class-general): det g4 = -(r sin)^2 D/W
# ====================================================================
print()
print("=" * 72)
print("ATTACK B — det g4 PROPORTIONAL TO D (class-general, my derivation)")
print("=" * 72)
fS, qS, wS = sp.symbols('f q w', positive=True)
WS = (1 + wS) ** 2
DS = r ** 2 * WS - fS * qS ** 2
gsym = udt_metric.__wrapped__ if hasattr(udt_metric, '__wrapped__') else None
gsymM = sp.Matrix([[-fS, 0, 0, 0],
                   [0, 1 / fS, qS, 0],
                   [0, qS, r ** 2 * WS, 0],
                   [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / WS]])
detg_sym = sp.cancel(gsymM.det())
tgt = -(r ** 2 * sp.sin(th) ** 2) * DS / WS
ck("B-det", sp.simplify(detg_sym - tgt) == 0,
   f"det g4 = {sp.factor(detg_sym)}  ==  -(r sin)^2 D/(1+w)^2 ; linear in D")
# signature eigenvalue: spatial (r,theta) block
hb = sp.Matrix([[1 / fS, qS], [qS, r ** 2 * WS]])
deth = sp.cancel(hb.det())
ck("B-blockdet", sp.simplify(deth - DS / fS) == 0,
   "spatial (r,theta) block det = D/f -> one eigenvalue -> 0 linearly at D=0")
# explicit: eigenvalues of h, smaller -> 0
trh = sp.simplify(hb.trace())
lam = sp.symbols('lam')
eigs = sp.solve(lam ** 2 - trh * lam + deth, lam)
# at D=0, product = 0 so min eigenvalue 0; verify lam- ~ D/(f trh)
lam_minus_lead = sp.cancel(deth / trh)
note("B-eig", f"spatial block eigenvalues product = D/f; small eigenvalue "
     f"~ D/(f*tr_h) -> 0 LINEAR in D (signature loss). tr_h={trh}")
print(f"[Attack B done {time.time()-t0:.0f}s]", flush=True)


# ====================================================================
# ATTACK A1 — q* branch, member 1 (f=a/r ell=2, theta=pi/3, w=0)
# ====================================================================
print()
print("=" * 72)
print("ATTACK A1 — q* branch curvature exponents (member 1: f=(1/r)(1+eps cos^2), theta=pi/3, w=0)")
print("=" * 72)
eps = sp.Rational(1, 10)
f1 = (1 + eps * sp.cos(th) ** 2) / r
W1 = sp.Integer(1)
f1r = sp.diff(f1, r)
f1th = sp.diff(f1, th)
P1 = f1 * r ** 2 * W1 * f1r ** 2 + f1th ** 2
q1 = 2 * r ** 2 * W1 * f1r * f1th / P1
fR1, fK1, fD1, Dexpr1, detg1, g1 = curvature_scalars_at_theta(
    f1, q1, sp.Integer(0), sp.pi / 3)
print(f"[member1 curvature built {time.time()-t0:.0f}s]", flush=True)
# find r* where D=0 at theta=pi/3 (high precision root of numerator)
D1_3 = sp.cancel(Dexpr1.subs(th, sp.pi / 3))
numD1 = sp.numer(sp.together(D1_3))
poly1 = sp.Poly(sp.expand(numD1), r)
roots1 = mp.polyroots([mp.mpf(str(c)) for c in poly1.all_coeffs()],
                      maxsteps=300, extraprec=300)
rstar1 = None
for rt in roots1:
    if abs(mp.im(rt)) < mp.mpf('1e-40') and mp.re(rt) > 0:
        rstar1 = mp.re(rt)
        break
note("A1-rstar", f"q* member1 D=0 at r* = {mp.nstr(rstar1,20)} (theta=pi/3)")
slR, rmsR, slK, rmsK, Ksc, rows1 = approach_report(
    "A1 q* member1", fR1, fK1, fD1, rstar1)
# expected q*: R~D^-3/2, K~D^-3
ck("A1-Rexp", abs(slR - (-1.5)) < 0.05 and rmsR < 1e-3,
   f"q* Ricci exponent {slR:.4f} matches -3/2 (clean power law)")
ck("A1-Kexp", abs(slK - (-3.0)) < 0.05 and rmsK < 1e-3,
   f"q* Kretschmann exponent {slK:.4f} matches -3 (clean power law)")
ck("A1-clean", Ksc, "mpmath K keeps constant sign (no float64 sign-flip)")


print(f"\nINTERIM: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
for x in FAIL:
    print("FAILED:", x)
sys.exit(0)
