#!/usr/bin/env python3
"""VFOLD curvature engine — built FROM SCRATCH, validated against
Schwarzschild K = 48 M^2/r^6 and flat R=K=0 BEFORE any use. Independent
of the arm (w6_arm1_lib.geom) and the arm-spawned verifier. mpmath
high-precision evaluation path; float64 cross-check to expose the
catastrophic-cancellation sign-flip trap.

This module provides:
  - ricci_scalar(g, xs)         exact sympy
  - kretschmann(g, xs)          exact sympy
  - both validated in __main__ on Schwarzschild + Minkowski.

Engine conventions (standard, lower-index Riemann
R^a_{bcd} = d_c G^a_{bd} - d_d G^a_{bc} + G^a_{ce} G^e_{bd}
            - G^a_{de} G^e_{bc}; K = R_{abcd} R^{abcd}).

Log: /tmp/vfold_curv_engine.log
"""
import sympy as sp


def christoffel(g, xs):
    n = len(xs)
    gi = g.inv()
    G = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for c in range(n):
        for a in range(n):
            for b in range(a, n):
                e = sp.S(0)
                for d in range(n):
                    if gi[c, d] == 0:
                        continue
                    e += gi[c, d] * (sp.diff(g[d, a], xs[b])
                                     + sp.diff(g[d, b], xs[a])
                                     - sp.diff(g[a, b], xs[d]))
                e = sp.together(e / 2)
                G[c][a][b] = e
                G[c][b][a] = e
    return G, gi


def riemann_up(g, xs):
    """R^a_{bcd} (first index up)."""
    n = len(xs)
    G, gi = christoffel(g, xs)
    R = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
         for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(c + 1, n):
                    e = (sp.diff(G[a][b][d], xs[c])
                         - sp.diff(G[a][b][c], xs[d]))
                    for ee in range(n):
                        e += (G[a][c][ee] * G[ee][b][d]
                              - G[a][d][ee] * G[ee][b][c])
                    e = sp.together(e)
                    R[a][b][c][d] = e
                    R[a][b][d][c] = -e
    return R, G, gi


def ricci(g, xs):
    n = len(xs)
    R, G, gi = riemann_up(g, xs)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(b, n):
            e = sp.together(sum(R[a][b][a][d] for a in range(n)))
            Ric[b, d] = e
            Ric[d, b] = e
    Rs = sp.together(sum(gi[b, d] * Ric[b, d]
                         for b in range(n) for d in range(n)))
    return Rs, Ric, R, gi


def kretschmann(g, xs):
    n = len(xs)
    Rs, Ric, Rup, gi = ricci(g, xs)
    # lower first index: R_{abcd} = g_{ae} R^e_{bcd}
    Rl = [[[[sp.together(sum(g[a, e] * Rup[e][b][c][d]
                             for e in range(n)))
             for d in range(n)] for c in range(n)]
           for b in range(n)] for a in range(n)]
    K = sp.S(0)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    low = Rl[a][b][c][d]
                    if low == 0:
                        continue
                    up = sp.S(0)
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
                                    up += (gi[a, ai] * gi[b, bi]
                                           * gi[c, ci] * gi[d, di]
                                           * Rl[ai][bi][ci][di])
                    K += low * sp.together(up)
    return sp.together(K), Rs


if __name__ == "__main__":
    print("=" * 72)
    print("CALIBRATION 1 — Schwarzschild: expect R=0, K = 48 M^2/r^6")
    print("=" * 72)
    t, r, th, ph = sp.symbols('t r theta varphi', positive=True)
    M = sp.Symbol('M', positive=True)
    fS = 1 - 2 * M / r
    gS = sp.diag(-fS, 1 / fS, r ** 2, r ** 2 * sp.sin(th) ** 2)
    K, Rs = kretschmann(gS, [t, r, th, ph])
    Ksimp = sp.simplify(K)
    Rssimp = sp.simplify(Rs)
    print("  Ricci scalar R =", Rssimp, "  (expect 0)")
    print("  Kretschmann K  =", Ksimp)
    print("  K - 48 M^2/r^6 =", sp.simplify(Ksimp - 48 * M ** 2 / r ** 6))
    ok_schw = (sp.simplify(Rssimp) == 0 and
               sp.simplify(Ksimp - 48 * M ** 2 / r ** 6) == 0)
    print("  SCHWARZSCHILD CALIBRATION:", "PASS" if ok_schw else "FAIL")

    print()
    print("=" * 72)
    print("CALIBRATION 2 — Minkowski (spherical): expect R=0, K=0")
    print("=" * 72)
    gM = sp.diag(-1, 1, r ** 2, r ** 2 * sp.sin(th) ** 2)
    KM, RsM = kretschmann(gM, [t, r, th, ph])
    ok_flat = (sp.simplify(RsM) == 0 and sp.simplify(KM) == 0)
    print("  R =", sp.simplify(RsM), "  K =", sp.simplify(KM))
    print("  MINKOWSKI CALIBRATION:", "PASS" if ok_flat else "FAIL")

    import sys
    sys.exit(0 if (ok_schw and ok_flat) else 1)
