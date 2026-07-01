#!/usr/bin/env python3
"""W6 FLUX-TEST — INDEPENDENT BLIND VERIFIER (main-loop pass of record).

Agent: independent verifier (NOT the arm, NOT a66894d1a78df7b1a).
This module is my OWN curvature engine, built from scratch, validated
against Schwarzschild K = 48 M^2/r^6 BEFORE it is trusted anywhere.
NO machinery is imported from w6_arm1_lib, w6_flux_*, or w_alg_*.
Everything below (Christoffel, Riemann, Ricci, Kretschmann, the metric)
is re-implemented here.

CONVENTION (mine, fixed once):
  Christoffel  Gam^c_ab = (1/2) g^{cd}(d_a g_db + d_b g_da - d_d g_ab)
  Riemann      R^a_bcd  = d_c Gam^a_bd - d_d Gam^a_bc
                          + Gam^a_ce Gam^e_bd - Gam^a_de Gam^e_bc
  Ricci        R_bd = R^a_bad
  scalar       R   = g^{bd} R_bd
  Kretschmann  K   = R_{abcd} R^{abcd}   (R_{abcd}=g_ae R^e_bcd)

The UDT metric under test (re-typed from the ansatz in w6_arm1_lib,
NOT imported):
  g = [[-f,      0,     0,                 0              ],
       [0,       1/f,   q,                 0              ],
       [0,       q,     r^2 W,             0              ],
       [0,       0,     0,                 r^2 sin^2 / W ]]
  W = (1+w)^2,   D = r^2 W - f q^2.
Same-minus time-row enlargement (tested in part A): add g_Tr=a,
g_Tth=b (symmetric).  Involution (a,b)->(-a,-b).

Log: /tmp/w6_flux_verifier2_engine.log
"""
import sys
import time

import sympy as sp

t0 = time.time()
PASS, FAIL, NOTE = [], [], []


def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"V2-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)


def note(tag, msg):
    NOTE.append((tag, msg))
    print(f"V2-{tag}: NOTE  {msg}", flush=True)


# ---------------------------------------------------------------------
# MY curvature engine (from scratch)
# ---------------------------------------------------------------------
def christoffel(g, gi, xs):
    n = len(xs)
    G = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for c in range(n):
        for a in range(n):
            for b in range(a, n):
                s = sp.S(0)
                for d in range(n):
                    if gi[c, d] == 0:
                        continue
                    s += gi[c, d] * (sp.diff(g[d, a], xs[b])
                                     + sp.diff(g[d, b], xs[a])
                                     - sp.diff(g[a, b], xs[d]))
                s = sp.cancel(sp.together(s / 2))
                G[c][a][b] = s
                G[c][b][a] = s
    return G


def riemann_mixed(G, xs):
    n = len(xs)
    R = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
         for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(c + 1, n):
                    e = sp.diff(G[a][b][d], xs[c]) - sp.diff(G[a][b][c], xs[d])
                    for ee in range(n):
                        e += G[a][c][ee] * G[ee][b][d] \
                            - G[a][d][ee] * G[ee][b][c]
                    e = sp.cancel(sp.together(e))
                    R[a][b][c][d] = e
                    R[a][b][d][c] = -e
    return R


def ricci_and_scalar(Rm, gi, xs):
    n = len(xs)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            Ric[b, d] = sp.cancel(sp.together(
                sum(Rm[a][b][a][d] for a in range(n))))
    Rs = sp.cancel(sp.together(
        sum(gi[b, d] * Ric[b, d] for b in range(n) for d in range(n))))
    return Ric, Rs


def kretschmann(Rm, g, gi, xs):
    n = len(xs)
    # lower first index
    Rl = [[[[sp.cancel(sp.together(
        sum(g[a, e] * Rm[e][b][c][d] for e in range(n))))
        for d in range(n)] for c in range(n)] for b in range(n)]
        for a in range(n)]
    K = sp.S(0)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    low = Rl[a][b][c][d]
                    if low == 0:
                        continue
                    up = sum(gi[a, ai] * gi[b, bi] * gi[c, ci] * gi[d, di]
                             * Rl[ai][bi][ci][di]
                             for ai in range(n) for bi in range(n)
                             for ci in range(n) for di in range(n))
                    K += low * up
    return sp.cancel(sp.together(K))


def all_invariants(g, xs, do_K=True):
    gi = g.inv()
    G = christoffel(g, gi, xs)
    Rm = riemann_mixed(G, xs)
    Ric, Rs = ricci_and_scalar(Rm, gi, xs)
    K = kretschmann(Rm, g, gi, xs) if do_K else None
    return gi, G, Rm, Ric, Rs, K


# ---------------------------------------------------------------------
# CALIBRATION 1: Schwarzschild  K = 48 M^2/r^6,  R = 0
# ---------------------------------------------------------------------
print("=" * 72)
print("CALIBRATION — Schwarzschild (K = 48 M^2/r^6, Ricci = 0)")
print("=" * 72)
tt, rr, thh, pph = sp.symbols('t r theta varphi', real=True)
M = sp.Symbol('M', positive=True)
fSch = 1 - 2 * M / rr
gSch = sp.diag(-fSch, 1 / fSch, rr ** 2, rr ** 2 * sp.sin(thh) ** 2)
xs = [tt, rr, thh, pph]
_, _, _, RicSch, RsSch, KSch = all_invariants(gSch, xs, do_K=True)
RsSch = sp.simplify(RsSch)
KSch = sp.simplify(KSch)
Kexpect = 48 * M ** 2 / rr ** 6
check("CAL-Ricci", sp.simplify(RsSch) == 0
      and all(sp.simplify(RicSch[i, j]) == 0 for i in range(4)
              for j in range(4)),
      "Schwarzschild Ricci tensor + scalar identically zero (vacuum).")
check("CAL-K", sp.simplify(KSch - Kexpect) == 0,
      f"Schwarzschild Kretschmann = {sp.simplify(KSch)} == 48 M^2/r^6.")

# CALIBRATION 2: flat space in spherical coords -> R = K = 0
gFlat = sp.diag(-1, 1, rr ** 2, rr ** 2 * sp.sin(thh) ** 2)
_, _, _, RicF, RsF, KF = all_invariants(gFlat, xs, do_K=True)
check("CAL-Flat", sp.simplify(RsF) == 0 and sp.simplify(KF) == 0,
      "Flat spherical: R = K = 0 (engine adds no spurious curvature).")

cal_ok = all(t in PASS for t in ('CAL-Ricci', 'CAL-K', 'CAL-Flat'))
print(f"\n   [calibration {'OK — engine TRUSTED' if cal_ok else 'FAILED'} "
      f"{time.time()-t0:.0f}s]\n", flush=True)
if not cal_ok:
    print("ENGINE NOT VALIDATED — ABORT.")
    sys.exit(2)

# ---------------------------------------------------------------------
# UDT metric builders (mine)
# ---------------------------------------------------------------------
Tt = sp.Symbol('T', real=True)
rv = sp.Symbol('r', positive=True)
thv = sp.Symbol('theta', real=True)
phv = sp.Symbol('varphi', real=True)
UXS = [Tt, rv, thv, phv]


def udt_metric(f, q, w, a=sp.S(0), b=sp.S(0)):
    """Full UDT 4-metric.  a=g_Tr, b=g_Tth time-row (same-minus)."""
    W = (1 + w) ** 2
    return sp.Matrix([
        [-f,    a,      b,             0],
        [a,     1 / f,  q,             0],
        [b,     q,      rv ** 2 * W,   0],
        [0,     0,      0,             rv ** 2 * sp.sin(thv) ** 2 / W]])


def det4(g):
    return sp.simplify(g.det())


print("=" * 72)
print("PART D (re-derive) — det g4 and the signature eigenvalue")
print("=" * 72)
fG, qG, wG, aG, bG = sp.symbols('f q w a b', real=True)
g_static = udt_metric(fG, qG, wG)            # a=b=0
W = (1 + wG) ** 2
Dexpr = rv ** 2 * W - fG * qG ** 2
det_static = det4(g_static)
target_det = -(rv * sp.sin(thv)) ** 2 * Dexpr / (1 + wG) ** 2
check("D-det",
      sp.simplify(det_static - target_det) == 0,
      f"det g4 (a=b=0) = -(r sin)^2 D/(1+w)^2 EXACTLY -> vanishes "
      f"LINEARLY in D. [det={sp.simplify(det_static)}]")

# Spatial (r,theta) block determinant and its small eigenvalue.
hblk = sp.Matrix([[1 / fG, qG], [qG, rv ** 2 * W]])
det_h = sp.simplify(hblk.det())
check("D-blockdet", sp.simplify(det_h - Dexpr / fG) == 0,
      "spatial (r,theta) block det = D/f -> 0 linearly at D=0.")
tr_h = sp.simplify(hblk.trace())
# small eigenvalue ~ det_h / tr_h as det_h -> 0:
note("D-eig", f"block eigenvalues product = D/f, sum = {tr_h}; "
     f"so lam_- = (D/f)/lam_+ -> 0 LINEARLY in D (one spatial "
     f"eigenvalue collapses; signature (-,+,+,+)->(-,0,+) at D=0).")

print(f"\n[engine + det part done {time.time()-t0:.0f}s]\n", flush=True)
print(f"V2 ENGINE: {len(PASS)} PASS / {len(FAIL)} FAIL")
for x in FAIL:
    print("FAILED:", x)

# export the engine + symbols for the other verifier scripts via import
if __name__ == '__main__':
    sys.exit(0 if not FAIL else 1)
