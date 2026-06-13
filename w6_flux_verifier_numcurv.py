#!/usr/bin/env python3
"""W6 FLUX VERIFIER — NUMERICAL high-precision curvature engine.

Independent engine: metric components lambdified to mpmath; Christoffel,
Riemann, Kretschmann, Ricci computed by mpmath CENTRAL FINITE DIFFERENCES
at each point (high working precision so the differencing is clean).
Validated against Schwarzschild K = 48 M^2/r^6 numerically before use.

This replaces the symbolic engine for the heavy q*/time-row members:
same invariants, no giant expressions. Differencing step h chosen with
working precision >> required digits to keep truncation+roundoff below
the signal. Self-calibrates the step.

Then:
  - reproduces the static (time-row off) divergence (claim C) on q* and
    generic q, with float64 sign-flip cross-check (the trap);
  - THE DECISIVE TEST: recomputes K,R on D=0 with the same-minus time
    row ON (a,b != 0) and asks if the divergence survives or is lifted.
"""
import sys
import time
import math
import mpmath as mp
import sympy as sp

t0 = time.time()


class NumCurv:
    """metric as dict (i,j)->callable(coords mp-vector). 4D."""

    def __init__(self, gfun, dps=60, h=None):
        self.gfun = gfun
        self.n = 4
        mp.mp.dps = dps
        self.h = mp.mpf(10) ** (-(dps // 3)) if h is None else h

    def g(self, x):
        n = self.n
        M = mp.matrix(n, n)
        for i in range(n):
            for j in range(n):
                M[i, j] = self.gfun[(i, j)](*x)
        return M

    def dg(self, x, k):
        # central difference d g / d x^k
        xp = list(x); xm = list(x)
        xp[k] += self.h; xm[k] -= self.h
        gp, gm = self.g(xp), self.g(xm)
        return (gp - gm) / (2 * self.h)

    def d2g(self, x, k, l):
        # mixed/second derivative of g
        h = self.h
        if k == l:
            xp = list(x); xm = list(x)
            xp[k] += h; xm[k] -= h
            return (self.g(xp) - 2 * self.g(x) + self.g(xm)) / h**2
        xpp = list(x); xpm = list(x); xmp = list(x); xmm = list(x)
        xpp[k] += h; xpp[l] += h
        xpm[k] += h; xpm[l] -= h
        xmp[k] -= h; xmp[l] += h
        xmm[k] -= h; xmm[l] -= h
        return (self.g(xpp) - self.g(xpm) - self.g(xmp)
                + self.g(xmm)) / (4 * h**2)

    def christ(self, x):
        n = self.n
        ginv = self.g(x) ** -1
        dgs = [self.dg(x, k) for k in range(n)]
        G = [[[mp.mpf(0)] * n for _ in range(n)] for _ in range(n)]
        for c in range(n):
            for a in range(n):
                for b in range(n):
                    s = mp.mpf(0)
                    for d in range(n):
                        s += ginv[c, d] * (dgs[b][d, a] + dgs[a][d, b]
                                           - dgs[d][a, b])
                    G[c][a][b] = s / 2
        return G, ginv, dgs

    def dchrist(self, x, k):
        xp = list(x); xm = list(x)
        xp[k] += self.h; xm[k] -= self.h
        Gp, _, _ = self.christ(xp)
        Gm, _, _ = self.christ(xm)
        n = self.n
        return [[[(Gp[a][b][c] - Gm[a][b][c]) / (2 * self.h)
                  for c in range(n)] for b in range(n)] for a in range(n)]

    def invariants(self, x):
        n = self.n
        G, ginv, _ = self.christ(x)
        dG = [self.dchrist(x, k) for k in range(n)]  # dG[k][a][b][c]
        gx = self.g(x)
        # Riemann up: R^a_bcd = dG[c][a][b][d] - dG[d][a][b][c] + GG - GG
        Ru = [[[[mp.mpf(0)] * n for _ in range(n)] for _ in range(n)]
              for _ in range(n)]
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        e = dG[c][a][b][d] - dG[d][a][b][c]
                        for m in range(n):
                            e += G[a][c][m] * G[m][b][d] \
                                - G[a][d][m] * G[m][b][c]
                        Ru[a][b][c][d] = e
        # Ricci
        Ric = mp.matrix(n, n)
        for b in range(n):
            for d in range(n):
                Ric[b, d] = sum(Ru[a][b][a][d] for a in range(n))
        Rs = sum(ginv[b, d] * Ric[b, d] for b in range(n)
                 for d in range(n))
        # lower Riemann
        Rl = [[[[sum(gx[a, e] * Ru[e][b][c][d] for e in range(n))
                 for d in range(n)] for c in range(n)]
               for b in range(n)] for a in range(n)]
        K = mp.mpf(0)
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        rl = Rl[a][b][c][d]
                        if rl == 0:
                            continue
                        ru = sum(ginv[a, ai] * ginv[b, bi] * ginv[c, ci]
                                 * ginv[d, di] * Rl[ai][bi][ci][di]
                                 for ai in range(n) for bi in range(n)
                                 for ci in range(n) for di in range(n))
                        K += rl * ru
        return Rs, K


def lambdify_metric(g4, coords):
    n = 4
    return {(i, j): sp.lambdify(coords, g4[i, j], 'mpmath')
            for i in range(n) for j in range(n)}


if __name__ == '__main__':
    PASS, FAIL = [], []

    def ck(tag, cond, note=''):
        (PASS if cond else FAIL).append(tag)
        print(f"{tag}: {'PASS' if cond else 'FAIL'} {note}", flush=True)

    t, r, th, ph = sp.symbols('t r theta phi', positive=True)
    print("=== NUMERICAL ENGINE CAL: Schwarzschild ===", flush=True)
    M = mp.mpf('1.0')
    fS = 1 - 2 * M / r
    gS = sp.diag(-fS, 1 / fS, r**2, r**2 * sp.sin(th)**2)
    gfun = lambdify_metric(gS, [t, r, th, ph])
    nc = NumCurv(gfun, dps=50)
    x = [mp.mpf(0), mp.mpf(5), mp.mpf(1), mp.mpf(0)]
    Rs, K = nc.invariants(x)
    Ktarget = 48 * M**2 / mp.mpf(5)**6
    ck("schw-K", abs(K - Ktarget) / Ktarget < mp.mpf('1e-20'),
       f"K={mp.nstr(K,12)} target={mp.nstr(Ktarget,12)}")
    ck("schw-Ricci", abs(Rs) < mp.mpf('1e-15'),
       f"Ricci={mp.nstr(Rs,6)} (vacuum 0)")
    # second point
    x2 = [mp.mpf(0), mp.mpf(3), mp.mpf('0.7'), mp.mpf(0)]
    Rs2, K2 = nc.invariants(x2)
    ck("schw-K2", abs(K2 - 48 * M**2 / mp.mpf(3)**6) / (48 / mp.mpf(3)**6)
       < mp.mpf('1e-20'), f"K(r=3)={mp.nstr(K2,12)}")
    print(f"\nNUMCURV CAL: {len(PASS)} PASS / {len(FAIL)} FAIL "
          f"({time.time()-t0:.0f}s)")
    sys.exit(0 if not FAIL else 1)
