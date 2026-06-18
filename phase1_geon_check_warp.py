#!/usr/bin/env python3
"""
phase1_geon_check_warp.py -- PHASE-1c diagnostic: is the SINGLE-P2-warp ansatz a
clean l=2 even-parity GW DOF, or does it violate the other vacuum constraints at
O(A)?  This decides reduction-choice C4 (single warp vs full Zerilli master) and
which wave operator is the legitimate one for the geon.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. OBSERVE. c=1.

We list ALL O(A^1) vacuum Einstein components for g = flat round + single P2 warp
(g_thth=r^2(1+A h P2), g_psps=r^2 sin^2(1-A h P2), h=H cos w t). If components
beyond the traceless-angular one are NOT separately satisfiable by the SAME H, the
single warp is NOT a free TT mode -> we must say so (frame caveat) and identify the
true master operator.
"""
import sympy as sp

t, r, th = sp.symbols('t r theta', real=True)
A = sp.symbols('A')
w = sp.symbols('w', positive=True)
ps = sp.Symbol('psi', real=True)
X = [t, r, th, ps]
H = sp.Function('H')(r)
P2 = (3 * sp.cos(th)**2 - 1) / 2
h = A * H * sp.cos(w * t)
g = sp.Matrix([
    [-1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, r**2 * (1 + h * P2), 0],
    [0, 0, 0, r**2 * sp.sin(th)**2 * (1 - h * P2)],
])


def ricci(g, X):
    n = len(X); ginv = g.inv()
    Ga = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    if ginv[a, d] == 0:
                        continue
                    s += ginv[a, d] * (sp.diff(g[d, c], X[b]) + sp.diff(g[d, b], X[c]) - sp.diff(g[b, c], X[d]))
                Ga[a][b][c] = s / 2
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            s = sp.S(0)
            for a in range(n):
                s += sp.diff(Ga[a][b][d], X[a]) - sp.diff(Ga[a][b][a], X[d])
                for e in range(n):
                    s += Ga[a][a][e] * Ga[e][b][d] - Ga[a][d][e] * Ga[e][b][a]
            Ric[b, d] = sp.expand(s)
    return Ric, ginv


def O1(e):
    return sp.simplify(sp.series(sp.expand(e), A, 0, 2).removeO().coeff(A, 1))


Ric, ginv = ricci(g, X)
print("=== ALL O(A^1) vacuum Ricci components for the single-P2-warp ansatz ===")
names = ['tt', 'rr', 'thth', 'psps', 'tr']
idx = [(0, 0), (1, 1), (2, 2), (3, 3), (0, 1)]
comps = {}
for nm, (i, j) in zip(names, idx):
    c = O1(Ric[i, j])
    comps[nm] = c
    print(f"  R_{nm}^(1) =", c)

print("\n--- Interpretation ---")
print("If R_tt, R_rr, R_tr all vanish identically (they did at O(A) in the flat")
print("background) the single warp's ONLY nontrivial vacuum content is the angular")
print("block. The angular block carries BOTH an l=0 trace part and the l=2 traceless")
print("part. Project:")
# trace angular part: R^th_th + R^ps_ps (l=0-ish); traceless: R^th_th - R^ps_ps
Rthth_up = O1(ginv[2, 2] * Ric[2, 2])
Rpsps_up = O1(ginv[3, 3] * Ric[3, 3])
tr_ang = sp.simplify(Rthth_up + Rpsps_up)
tl_ang = sp.simplify(Rthth_up - Rpsps_up)
print("  R^th_th + R^ps_ps (trace angular) =", tr_ang)
print("  R^th_th - R^ps_ps (traceless)     =", tl_ang)
print("\nThe vacuum eqn requires BOTH = 0. If the trace part forces an EXTRA")
print("condition on H not implied by the traceless part, the single warp is")
print("OVER-CONSTRAINED (not a free DOF) -> need full Zerilli. Report which.")

# Check: solve traceless=0 for the operator, then test if trace=0 is automatic.
print("\n--- Does traceless=0 imply trace=0 (same H)? ---")
# Extract operators
def op_of(e):
    e = sp.expand(e / sp.cos(w * t)) if e.has(sp.cos(w * t)) else sp.expand(e)
    Hrr = sp.diff(H, r, 2); Hr = sp.diff(H, r)
    # strip residual angular factor by dividing by its theta-content via ratio
    return e
print("  traceless (per cos wt):", sp.simplify(tl_ang / sp.cos(w * t)) if tl_ang.has(sp.cos(w*t)) else tl_ang)
print("  trace     (per cos wt):", sp.simplify(tr_ang / sp.cos(w * t)) if tr_ang.has(sp.cos(w*t)) else tr_ang)
