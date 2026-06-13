#!/usr/bin/env python3
"""W6 FLUX VERIFIER — INDEPENDENT CURVATURE ENGINE + SCHWARZSCHILD CAL.

Blind adversarial verifier (main-loop pass). Built from scratch, shares
NO machinery with the arm or the arm-spawned verifier. Validates against
Schwarzschild K = 48 M^2/r^6 EXACTLY before trusting any result.

Engine convention: Riemann R^a_{bcd} = d_c G^a_{bd} - d_d G^a_{bc}
 + G^a_{ce} G^e_{bd} - G^a_{de} G^e_{bc}; Ricci R_{bd}=R^a_{bad};
 K = R_{abcd} R^{abcd}.
"""
import sys
import time
import sympy as sp

t0 = time.time()


def christoffel(g, xs):
    n = len(xs)
    gi = g.inv()
    G = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for c in range(n):
        for a in range(n):
            for b in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += gi[c, d] * (sp.diff(g[d, a], xs[b])
                                     + sp.diff(g[d, b], xs[a])
                                     - sp.diff(g[a, b], xs[d]))
                G[c][a][b] = sp.cancel(sp.together(s / 2))
    return G, gi


def riemann_up(G, xs):
    n = len(xs)
    R = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
         for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    e = sp.diff(G[a][b][d], xs[c]) - sp.diff(G[a][b][c],
                                                             xs[d])
                    for k in range(n):
                        e += G[a][c][k] * G[k][b][d] \
                            - G[a][d][k] * G[k][b][c]
                    R[a][b][c][d] = sp.cancel(sp.together(e))
    return R


def kretschmann_ricci(g, xs):
    n = len(xs)
    G, gi = christoffel(g, xs)
    Ru = riemann_up(G, xs)
    # lower: R_{abcd} = g_{ae} R^e_{bcd}
    Rl = [[[[sum(g[a, e] * Ru[e][b][c][d] for e in range(n))
             for d in range(n)] for c in range(n)]
           for b in range(n)] for a in range(n)]
    # Ricci R_{bd} = R^a_{bad}
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            Ric[b, d] = sp.cancel(sp.together(
                sum(Ru[a][b][a][d] for a in range(n))))
    Rs = sp.cancel(sp.together(
        sum(gi[b, d] * Ric[b, d] for b in range(n) for d in range(n))))
    # raise Riemann fully for K
    K = sp.S(0)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    rl = Rl[a][b][c][d]
                    if rl == 0:
                        continue
                    ru = sum(gi[a, ai] * gi[b, bi] * gi[c, ci] * gi[d, di]
                             * Rl[ai][bi][ci][di]
                             for ai in range(n) for bi in range(n)
                             for ci in range(n) for di in range(n))
                    K += rl * ru
    return sp.cancel(sp.together(K)), Rs, Ric, Rl, gi


if __name__ == '__main__':
    PASS, FAIL = [], []

    def ck(tag, cond, note=''):
        (PASS if cond else FAIL).append(tag)
        print(f"{tag}: {'PASS' if cond else 'FAIL'} {note}", flush=True)

    print("=== SCHWARZSCHILD CALIBRATION ===")
    t, rr, th, ph = sp.symbols('t r theta phi', positive=True)
    M = sp.Symbol('M', positive=True)
    ffn = 1 - 2 * M / rr
    gS = sp.diag(-ffn, 1 / ffn, rr**2, rr**2 * sp.sin(th)**2)
    K, Rs, Ric, _, _ = kretschmann_ricci(gS, [t, rr, th, ph])
    Ktarget = 48 * M**2 / rr**6
    ck("schwarzschild-K", sp.simplify(K - Ktarget) == 0,
       f"K={sp.simplify(K)} (target 48 M^2/r^6)")
    ck("schwarzschild-Ricci", sp.simplify(Rs) == 0,
       "Ricci scalar = 0 (vacuum)")

    print("\n=== FLAT SPACE ===")
    gF = sp.diag(-1, 1, rr**2, rr**2 * sp.sin(th)**2)
    Kf, Rsf, _, _, _ = kretschmann_ricci(gF, [t, rr, th, ph])
    ck("flat-K", sp.simplify(Kf) == 0, "flat K=0")
    ck("flat-Ricci", sp.simplify(Rsf) == 0, "flat Ricci=0")

    print(f"\nENGINE CAL: {len(PASS)} PASS / {len(FAIL)} FAIL "
          f"({time.time()-t0:.0f}s)")
    sys.exit(0 if not FAIL else 1)
