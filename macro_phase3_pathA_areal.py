#!/usr/bin/env python3
"""
PHASE 3 — Path A (chosen): areal gauge D_A=r, EH empty, vacuum bulk from R1 kinetic.
No matter stand-ins, no G/P, no edge IVP.
"""
from __future__ import annotations

import sympy as sp

r, th, ps, t, c = sp.symbols("r theta psi t c", positive=True)
Z, q, phiinf = sp.symbols("Z q phi_inf", real=True)
Z = sp.symbols("Z", positive=True)
phi = sp.Function("phi")
ph = phi(r)
php = sp.diff(ph, r)

print("=" * 70)
print("PATH A — areal gauge D_A ≡ r")
print("=" * 70)

# Metric
g = sp.diag(
    -sp.exp(-2 * ph) * c**2,
    sp.exp(2 * ph),
    r**2,
    (r * sp.sin(th)) ** 2,
)
gi = g.inv()
coords = [t, r, th, ps]
sqrtmg = sp.simplify(sp.sqrt(-g.det()))
print("\n[1] √(-g) =", sqrtmg)
print("    phi-free?", "phi" not in str(sqrtmg).lower() or sp.simplify(sqrtmg - c * r**2 * sp.sin(th)) == 0)

# Ricci + EH boundary
def christ(g, gi, coords):
    n = 4
    Ga = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = 0
                for d in range(n):
                    s += gi[a, d] * (
                        sp.diff(g[d, b], coords[cc])
                        + sp.diff(g[d, cc], coords[b])
                        - sp.diff(g[b, cc], coords[d])
                    )
                Ga[a][b][cc] = sp.simplify(s / 2)
    return Ga


def ricci_R(g, gi, coords):
    Ga = christ(g, gi, coords)
    n = 4
    Ric = sp.zeros(n)
    for b in range(n):
        for d in range(n):
            s = 0
            for a in range(n):
                s += sp.diff(Ga[a][b][d], coords[a]) - sp.diff(Ga[a][b][a], coords[d])
                for e in range(n):
                    s += Ga[a][a][e] * Ga[e][b][d] - Ga[a][d][e] * Ga[e][b][a]
            Ric[b, d] = sp.simplify(s)
    return sp.simplify(sum(gi[i, i] * Ric[i, i] for i in range(4)))


R = ricci_R(g, gi, coords)
bdy = 2 * r * (1 - sp.exp(-2 * ph)) + 2 * r**2 * sp.exp(-2 * ph) * php
print("\n[2] EH empty: r^2 R - d(bdy)/dr == 0?", sp.simplify(r**2 * R - sp.diff(bdy, r)) == 0)

# R1 kinetic
kin = sp.simplify(sqrtmg * sp.exp(2 * ph) * gi[1, 1] * php**2)
print("\n[3] R1 kinetic density =", kin)
print("    == c r^2 sinθ (φ')^2?", sp.simplify(kin - c * r**2 * sp.sin(th) * php**2) == 0)

# Vacuum EL from L = (Z/2) r^2 (phi')^2  (angular integral dropped)
L = (Z / 2) * r**2 * php**2
el = sp.simplify(sp.diff(L, php).diff(r) - sp.diff(L, ph))
print("\n[4] Vacuum EL from kinetic only: EL =", el)
print("    == d/dr(Z r^2 φ')?", sp.simplify(el - sp.diff(Z * r**2 * php, r)) == 0)

phi_sol = phiinf - q / r
print("\n[5] Coulomb vacuum φ = φ_∞ - q/r")
print("    satisfies (r^2 φ')'=0?", sp.simplify(sp.diff(r**2 * sp.diff(phi_sol, r), r)) == 0)
print("    g_tt =", sp.simplify(-sp.exp(-2 * phi_sol) * c**2))

# Unweighted kinetic contrast (not adopted)
print("\n[6] Contrast: UNWEIGHTED kinetic g^{rr}(φ')^2 is NOT R1-shift clean")
kin_uw = sp.simplify(sqrtmg * gi[1, 1] * php**2)
print("    density =", kin_uw, " (explicit e^{-2φ})")

print("\n[7] What Path A does NOT fix")
print("    - value of Z (normalization)")
print("    - matter sector")
print("    - free D_A / EH re-entry (Path B generalization)")
print("    - edge/x_max existence")
print("    - time dependence / non-spherical")
print("DONE")
