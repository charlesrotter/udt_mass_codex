#!/usr/bin/env python3
"""
phase1_geon_reduce_fast.py -- PHASE-1c step 1 (FAST variant): same O(A^2) coupled
geon reduction as phase1_geon_reduce.py but polynomialized up front (exp -> O(A^2)
Taylor) so the symbolic series/simplify is tractable in minutes.

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. OBSERVE. c=1.

This is the Taylor-function-replacement sanctioned by the charter (machine-exact to
the working order O(A^2); keeps the quadratic content that IS the geon source). The
metric exponentials e^{+-2 A^2 F} are replaced by 1 +- 2 A^2 F (exact to O(A^2),
since higher terms are O(A^4) and do not enter the O(A^2) source or the O(A^2)
frequency shift). h enters linearly in the metric so it is already polynomial.

Same reduction CHOICES C1-C4 as phase1_geon_reduce.py (see that file's header).
"""
import sympy as sp

t, r, th, ps = sp.symbols('t r theta psi', real=True)
A = sp.symbols('A')
w = sp.symbols('w', positive=True)
X = [t, r, th, ps]
H = sp.Function('H')(r)
F = sp.Function('F')(r)
P2 = (3 * sp.cos(th)**2 - 1) / 2
h = A * H * sp.cos(w * t)
# exp(-2 phi) with phi=A^2 F -> 1 - 2 A^2 F (+O(A^4)); exp(2 phi)->1+2 A^2 F
gtt = -(1 - 2 * A**2 * F)
grr = (1 + 2 * A**2 * F)
g = sp.Matrix([
    [gtt, 0, 0, 0],
    [0, grr, 0, 0],
    [0, 0, r**2 * (1 + h * P2), 0],
    [0, 0, 0, r**2 * sp.sin(th)**2 * (1 - h * P2)],
])


def einstein_tensor(g, X):
    n = len(X)
    ginv = g.inv()
    Gamma = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    if ginv[a, d] == 0:
                        continue
                    s += ginv[a, d] * (sp.diff(g[d, c], X[b])
                                       + sp.diff(g[d, b], X[c])
                                       - sp.diff(g[b, c], X[d]))
                Gamma[a][b][c] = sp.Rational(1, 2) * s
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            s = sp.S(0)
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], X[a]) - sp.diff(Gamma[a][b][a], X[d])
                for e in range(n):
                    s += Gamma[a][a][e] * Gamma[e][b][d] - Gamma[a][d][e] * Gamma[e][b][a]
            Ric[b, d] = sp.expand(s)
    Rs = sp.S(0)
    for a in range(n):
        Rs += ginv[a, a] * Ric[a, a]
    Rs = sp.expand(Rs)
    G = sp.zeros(n, n)
    for a in range(n):
        for b in range(n):
            G[a, b] = sp.expand(Ric[a, b] - sp.Rational(1, 2) * g[a, b] * Rs)
    return G, ginv


def coeffA(expr, order):
    p = sp.Poly(sp.expand(expr), A)
    return p.coeff_monomial(A**order)


def time_avg(expr):
    e = sp.expand(expr)
    c = sp.cos(w * t)
    if not e.has(c):
        return e.subs({sp.cos(2 * w * t): 0, sp.sin(2 * w * t): 0,
                       sp.sin(w * t): 0}).doit()
    poly = sp.Poly(e, c)
    out = sp.S(0)
    from sympy import binomial, Rational
    for (deg,), coeff in poly.terms():
        coeff = coeff.subs({sp.cos(2 * w * t): 0, sp.sin(2 * w * t): 0, sp.sin(w * t): 0})
        if deg == 0:
            out += coeff
        elif deg % 2 == 0:
            out += coeff * Rational(int(binomial(deg, deg // 2)), 2**deg)
    return sp.expand(out)


def ang_avg(expr):
    """(1/2) int_{-1}^{1} f d(cos th), axisymmetric l=0 projection."""
    u = sp.Symbol('u')
    e = expr.rewrite(sp.cos)
    e = e.subs(sp.sin(th)**2, 1 - sp.cos(th)**2).subs(sp.cos(th), u)
    e = sp.expand(e)
    if e.has(th):
        e = e.subs(sp.sin(th), sp.sqrt(1 - u**2)).subs(sp.cos(th), u)
    return sp.simplify(sp.integrate(sp.expand(e), (u, -1, 1)) / 2)


if __name__ == "__main__":
    print("=" * 78)
    print("PHASE-1c step 1 FAST: O(A^2) coupled geon reduction (polynomialized)")
    print("=" * 78)
    G, ginv = einstein_tensor(g, X)

    # ---- O(A^1) wave operator: traceless G^th_th - G^ps_ps ----
    Cwave = sp.expand(ginv[2, 2] * G[2, 2] - ginv[3, 3] * G[3, 3])
    C1 = sp.expand(coeffA(Cwave, 1))
    C1c = sp.simplify(C1 / sp.cos(w * t))
    Hrr = sp.diff(H, r, 2); Hr = sp.diff(H, r)
    a2 = sp.simplify(C1c.coeff(Hrr)); a1 = sp.simplify(C1c.coeff(Hr))
    a0 = sp.simplify((C1c - a2 * Hrr - a1 * Hr).coeff(H))
    print("\n[O(A^1) WAVE]  a2 H'' + a1 H' + a0 H = 0")
    print("  a2 =", a2)
    print("  a1 =", a1)
    print("  a0 =", a0)
    if a2 != 0:
        print("  normalized -H'' + (%s) H' + (%s) H = 0" %
              (sp.simplify(-a1 / a2), sp.simplify(-a0 / a2)))

    # ---- O(A^1) l=0 tadpole (must vanish) ----
    Gtt1 = coeffA(G[0, 0], 1)
    tad = ang_avg(time_avg(Gtt1))
    print("\n[O(A^1) TADPOLE]  <G_tt^(1)>_{t,ang} =", sp.simplify(tad), " (must be 0)")

    # ---- O(A^2) l=0 phi source from G_tt ----
    Gtt2 = coeffA(G[0, 0], 2)
    Gtt2a = ang_avg(time_avg(Gtt2))
    Frr = sp.diff(F, r, 2); Fr = sp.diff(F, r)
    b2 = sp.simplify(Gtt2a.coeff(Frr)); b1 = sp.simplify(Gtt2a.coeff(Fr))
    b0 = sp.simplify((Gtt2a - b2 * Frr - b1 * Fr).coeff(F))
    Src = sp.simplify(Gtt2a - b2 * Frr - b1 * Fr - b0 * F)
    print("\n[O(A^2) PHI-SRC from G_tt]  b2 F'' + b1 F' + b0 F + Src[H] = 0")
    print("  b2 =", b2)
    print("  b1 =", b1)
    print("  b0 =", b0)
    print("  Src[H] =", Src)

    # ---- O(A^2) l=0 from G_rr (second relation / check) ----
    Grr2 = coeffA(G[1, 1], 2)
    Grr2a = ang_avg(time_avg(Grr2))
    c2 = sp.simplify(Grr2a.coeff(Frr)); c1 = sp.simplify(Grr2a.coeff(Fr))
    c0 = sp.simplify((Grr2a - c2 * Frr - c1 * Fr).coeff(F))
    Src_rr = sp.simplify(Grr2a - c2 * Frr - c1 * Fr - c0 * F)
    print("\n[O(A^2) from G_rr]  c2 F'' + c1 F' + c0 F + Src_rr[H] = 0")
    print("  c2 =", c2)
    print("  c1 =", c1)
    print("  c0 =", c0)
    print("  Src_rr[H] =", Src_rr)

    print("\n" + "=" * 78)
    print("These exact coefficients feed phase1_geon_solve.py.")
    print("=" * 78)
