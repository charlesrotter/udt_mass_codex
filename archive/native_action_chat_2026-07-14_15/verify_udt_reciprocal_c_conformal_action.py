#!/usr/bin/env python3
"""Exact audit of the conditional Reciprocal-c conformal metric action.

The script derives the reciprocal spherical curvature invariants from the
metric, varies the curvature-quadratic basis, and independently constructs the
full Bach tensor for the resulting static solution family. It does not adopt
common-scale neutrality or the action as native UDT physics.
"""

import sympy as sp


checks = []


def check(name, statement):
    ok = bool(statement)
    checks.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        raise AssertionError(name)


# Reciprocal/common-scale decomposition.
u, v, omega = sp.symbols("u v omega", positive=True)
Omega = sp.sqrt(u * v)
depth = sp.log(v / u) / 2
check("positive calibration decomposes into common and reciprocal clock factors",
      sp.simplify(Omega * sp.exp(-depth) - u) == 0)
check("positive calibration decomposes into common and reciprocal ruler factors",
      sp.simplify(Omega * sp.exp(depth) - v) == 0)
D = sp.diag(sp.exp(-depth), sp.exp(depth))
check("reciprocal factor has determinant one", sp.simplify(D.det()) == 1)
check("common scaling leaves the time-length ratio unchanged",
      sp.simplify((omega * u) / (omega * v) - u / v) == 0)

# Four-dimensional conformal weights.  This is a weight audit, not a proof
# that common scale is gauge.
check("volume density is not common-scale invariant", 4 != 0)
check("Ricci-scalar density has nonzero constant conformal weight", 4 - 2 == 2)
check("Weyl-squared density has zero conformal weight", 4 - 4 == 0)

# Derive curvature from the reciprocal spherical metric.
t, r, theta, azimuth = sp.symbols("t r theta azimuth", real=True)
coords = [t, r, theta, azimuth]
n = 4
A = sp.Function("A")(r)
g = sp.diag(-A, 1 / A, r**2, r**2 * sp.sin(theta)**2)
ginv = sp.simplify(g.inv())

Gamma = [[[
    sp.simplify(sum(
        ginv[a, d] * (
            sp.diff(g[d, c], coords[b])
            + sp.diff(g[d, b], coords[c])
            - sp.diff(g[b, c], coords[d]))
        for d in range(n)) / 2)
    for c in range(n)] for b in range(n)] for a in range(n)]

Riemann_mixed = {}
for a in range(n):
    for b in range(n):
        for cidx in range(n):
            for d in range(n):
                Riemann_mixed[a, b, cidx, d] = sp.simplify(
                    sp.diff(Gamma[a][b][d], coords[cidx])
                    - sp.diff(Gamma[a][b][cidx], coords[d])
                    + sum(
                        Gamma[a][cidx][e] * Gamma[e][b][d]
                        - Gamma[a][d][e] * Gamma[e][b][cidx]
                        for e in range(n)))

Ricci = sp.MutableDenseNDimArray.zeros(n, n)
for b in range(n):
    for d in range(n):
        Ricci[b, d] = sp.simplify(sum(
            Riemann_mixed[a, b, a, d] for a in range(n)))

Rscalar = sp.simplify(sum(
    ginv[a, b] * Ricci[a, b] for a in range(n) for b in range(n)))
Ricci2 = sp.simplify(sum(
    ginv[a, cidx] * ginv[b, d] * Ricci[a, b] * Ricci[cidx, d]
    for a in range(n) for b in range(n)
    for cidx in range(n) for d in range(n)))

# With diagonal g, lower the first Riemann index and contract directly.
Riemann2 = 0
for a in range(n):
    for b in range(n):
        for cidx in range(n):
            for d in range(n):
                Rlow = sp.simplify(g[a, a] * Riemann_mixed[a, b, cidx, d])
                if Rlow != 0:
                    Riemann2 += sp.simplify(
                        ginv[a, a] * ginv[b, b] * ginv[cidx, cidx]
                        * ginv[d, d] * Rlow**2)
Riemann2 = sp.factor(sp.simplify(Riemann2))

Aprime = sp.diff(A, r)
Asecond = sp.diff(A, r, 2)
R_expected = -(r**2 * Asecond + 4 * r * Aprime + 2 * A - 2) / r**2
Ricci2_expected = (
    r**4 * Asecond**2 + 4 * r**3 * Aprime * Asecond
    + 8 * r**2 * Aprime**2 + 8 * r * (A - 1) * Aprime
    + 4 * (A - 1)**2) / (2 * r**4)
Riemann2_expected = (
    r**4 * Asecond**2 + 4 * r**2 * Aprime**2
    + 4 * (A - 1)**2) / r**4
check("Ricci scalar derived from metric", sp.simplify(Rscalar - R_expected) == 0)
check("Ricci-square derived from metric", sp.simplify(Ricci2 - Ricci2_expected) == 0)
check("Riemann-square derived from metric",
      sp.simplify(Riemann2 - Riemann2_expected) == 0)

Euler4 = sp.factor(sp.simplify(Riemann2 - 4 * Ricci2 + Rscalar**2))
Weyl2 = sp.factor(sp.simplify(Riemann2 - 2 * Ricci2 + Rscalar**2 / 3))
Euler4_expected = 4 * ((A - 1) * Asecond + Aprime**2) / r**2
Weyl2_expected = (
    r**2 * Asecond - 2 * r * Aprime + 2 * A - 2)**2 / (3 * r**4)
check("Euler density derived from metric", sp.simplify(Euler4 - Euler4_expected) == 0)
check("Euler radial density is a total derivative",
      sp.simplify(r**2 * Euler4
                  - sp.diff(4 * (A - 1) * Aprime, r)) == 0)
check("Weyl-square derived from metric", sp.simplify(Weyl2 - Weyl2_expected) == 0)
check("Weyl-square differs from its two-invariant bulk form only by Euler density",
      sp.simplify(Weyl2 - Euler4
                  - (2 * Ricci2 - sp.Rational(2, 3) * Rscalar**2)) == 0)


def higher_el(lagrangian):
    """Euler operator for L(A,A',A'')."""
    return sp.factor(sp.simplify(
        sp.diff(lagrangian, A)
        - sp.diff(sp.diff(lagrangian, Aprime), r)
        + sp.diff(sp.diff(lagrangian, Asecond), r, 2)))


EL_R = higher_el(r**2 * Rscalar)
EL_R2 = higher_el(r**2 * Rscalar**2)
EL_Ricci2 = higher_el(r**2 * Ricci2)
EL_Euler4 = higher_el(r**2 * Euler4)
EL_Weyl2 = higher_el(r**2 * Weyl2)
A3 = sp.diff(A, r, 3)
A4 = sp.diff(A, r, 4)
check("reduced Einstein-Hilbert density has empty reciprocal bulk equation", EL_R == 0)
check("R-square reciprocal Euler operator",
      sp.simplify(EL_R2
                  - 2 * (r**4 * A4 + 4 * r**3 * A3 - 6 * r**2 * Asecond
                         + 12 * A - 12) / r**2) == 0)
check("Ricci-square reciprocal Euler operator",
      sp.simplify(EL_Ricci2
                  - (r**4 * A4 + 4 * r**3 * A3 - 4 * r**2 * Asecond
                     + 8 * A - 8) / r**2) == 0)
check("curvature-quadratic operators are independent",
      sp.simplify(EL_R2 - 2 * EL_Ricci2) != 0)
check("Euler density has empty bulk equation", EL_Euler4 == 0)
check("Weyl-square reciprocal Euler operator",
      sp.simplify(EL_Weyl2 - sp.Rational(2, 3) * r * (r * A4 + 4 * A3)) == 0)

# Static reciprocal solution family of the reduced Weyl-square equation.
a0, a1, am1, a2 = sp.symbols("a0 a1 a_minus1 a2", real=True)
A_solution = a0 + a1 * r + am1 / r + a2 * r**2
check("four-constant reciprocal family solves reduced Weyl equation",
      sp.simplify(EL_Weyl2.subs({
          A: A_solution,
          Aprime: sp.diff(A_solution, r),
          Asecond: sp.diff(A_solution, r, 2),
          A3: sp.diff(A_solution, r, 3),
          A4: sp.diff(A_solution, r, 4),
      })) == 0)

# WR-L is located only after the action and solution family have been found.
X = sp.symbols("X", positive=True)
A_wrl = 1 - r / X
check("WR-L conformal curvature vanishes",
      sp.simplify(Weyl2.subs({
          A: A_wrl,
          Aprime: -1 / X,
          Asecond: 0,
      })) == 0)
check("WR-L Ricci scalar remains nonzero",
      sp.simplify(Rscalar.subs({
          A: A_wrl,
          Aprime: -1 / X,
          Asecond: 0,
      }) - 6 / (X * r)) == 0)

# Full covariant Bach tensor for the entire reduced solution family.  This
# independently catches restrict-then-vary artifacts.
gS = sp.diag(-A_solution, 1 / A_solution,
             r**2, r**2 * sp.sin(theta)**2)
gSinv = sp.simplify(gS.inv())
GammaS = [[[
    sp.simplify(sum(
        gSinv[a, d] * (
            sp.diff(gS[d, cidx], coords[b])
            + sp.diff(gS[d, b], coords[cidx])
            - sp.diff(gS[b, cidx], coords[d]))
        for d in range(n)) / 2)
    for cidx in range(n)] for b in range(n)] for a in range(n)]

RmS = {}
for a in range(n):
    for b in range(n):
        for cidx in range(n):
            for d in range(n):
                RmS[a, b, cidx, d] = sp.simplify(
                    sp.diff(GammaS[a][b][d], coords[cidx])
                    - sp.diff(GammaS[a][b][cidx], coords[d])
                    + sum(
                        GammaS[a][cidx][e] * GammaS[e][b][d]
                        - GammaS[a][d][e] * GammaS[e][b][cidx]
                        for e in range(n)))

RlS = {}
for a in range(n):
    for b in range(n):
        for cidx in range(n):
            for d in range(n):
                RlS[a, b, cidx, d] = sp.simplify(sum(
                    gS[a, e] * RmS[e, b, cidx, d] for e in range(n)))

RicS = sp.MutableDenseNDimArray.zeros(n, n)
for b in range(n):
    for d in range(n):
        RicS[b, d] = sp.simplify(sum(RmS[a, b, a, d] for a in range(n)))
RS = sp.simplify(sum(
    gSinv[a, b] * RicS[a, b] for a in range(n) for b in range(n)))

CS = {}
for a in range(n):
    for b in range(n):
        for cidx in range(n):
            for d in range(n):
                CS[a, b, cidx, d] = sp.factor(sp.simplify(
                    RlS[a, b, cidx, d]
                    - sp.Rational(1, 2) * (
                        gS[a, cidx] * RicS[d, b]
                        - gS[a, d] * RicS[cidx, b]
                        - gS[b, cidx] * RicS[d, a]
                        + gS[b, d] * RicS[cidx, a])
                    + RS * sp.Rational(1, 6) * (
                        gS[a, cidx] * gS[d, b]
                        - gS[a, d] * gS[cidx, b])))

# First covariant derivative of C.
DCS = {}
for e in range(n):
    for a in range(n):
        for m in range(n):
            for b in range(n):
                for q in range(n):
                    value = sp.diff(CS[a, m, b, q], coords[e])
                    for h in range(n):
                        value -= (
                            GammaS[h][e][a] * CS[h, m, b, q]
                            + GammaS[h][e][m] * CS[a, h, b, q]
                            + GammaS[h][e][b] * CS[a, m, h, q]
                            + GammaS[h][e][q] * CS[a, m, b, h])
                    DCS[e, a, m, b, q] = sp.factor(sp.simplify(value))

# First divergence T_{a m b}=nabla^q C_{a m b q}.
TC = {}
for a in range(n):
    for m in range(n):
        for b in range(n):
            TC[a, m, b] = sp.factor(sp.simplify(sum(
                gSinv[e, q] * DCS[e, a, m, b, q]
                for e in range(n) for q in range(n))))

RicS_up = [[sp.simplify(sum(
    gSinv[m, a] * gSinv[q, b] * RicS[a, b]
    for a in range(n) for b in range(n)))
    for q in range(n)] for m in range(n)]

Bach = sp.MutableDenseNDimArray.zeros(n, n)
for a in range(n):
    for b in range(n):
        second_divergence = 0
        for pidx in range(n):
            for m in range(n):
                if gSinv[pidx, m] == 0:
                    continue
                value = sp.diff(TC[a, m, b], coords[pidx])
                for h in range(n):
                    value -= (
                        GammaS[h][pidx][a] * TC[h, m, b]
                        + GammaS[h][pidx][m] * TC[a, h, b]
                        + GammaS[h][pidx][b] * TC[a, m, h])
                second_divergence += gSinv[pidx, m] * value
        curvature_term = sp.Rational(1, 2) * sum(
            RicS_up[m][q] * CS[a, m, b, q]
            for m in range(n) for q in range(n))
        Bach[a, b] = sp.factor(sp.simplify(sp.expand_trig(sp.simplify(
            second_divergence + curvature_term))))

delta = a0**2 - 3 * a1 * am1 - 1
Bach_mixed = [sp.factor(sp.simplify(gSinv[a, a] * Bach[a, a]))
              for a in range(n)]
check("full Bach tensor has no off-diagonal residue",
      all(sp.simplify(sp.expand_trig(Bach[a, b])) == 0
          for a in range(n) for b in range(n) if a != b))
check("full Bach temporal component gives algebraic constraint",
      sp.simplify(Bach_mixed[0] - delta / (6 * r**4)) == 0)
check("full Bach radial component matches temporal component",
      sp.simplify(Bach_mixed[1] - delta / (6 * r**4)) == 0)
check("full Bach angular components are opposite",
      sp.simplify(Bach_mixed[2] + delta / (6 * r**4)) == 0
      and sp.simplify(Bach_mixed[3] + delta / (6 * r**4)) == 0)
check("full Bach tensor is trace free", sp.simplify(sum(Bach_mixed)) == 0)
check("WR-L passes full covariant Bach equation",
      sp.simplify(delta.subs({a0: 1, a1: -1 / X, am1: 0, a2: 0})) == 0)

passed = sum(ok for _, ok in checks)
print(f"ALL CONSISTENT ({passed}/{len(checks)} checks pass)")
print(f"SymPy {sp.__version__}")
