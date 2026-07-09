#!/usr/bin/env python3
"""
PHASE 2 — Field-equation restart from the metric (free D_A).
No continuum stand-ins, no G/P labels, no edge targets.
Contract spirit: macro_clean_restart_from_metric_MAP.md Phase 2.

What this script DOES:
  - CAS on the reciprocal metric with free D_A(r)
  - EH / scalar curvature structure; boundary-term check where possible
  - R1-weighted kinetic density; vacuum EL from kinetic ONLY
  - Geometric objects on free D_A (K_cal) — as definitions, not "the" dynamics

What this script does NOT do:
  - Claim a unique full bulk action
  - Introduce matter μ, α, winding, core ICs
  - Solve cosmology
"""
from __future__ import annotations

import sympy as sp

r, th, ps, t, c = sp.symbols("r theta psi t c", positive=True)
Z, q, phiinf = sp.symbols("Z q phi_inf", positive=True)
phi = sp.Function("phi")
DA = sp.Function("D_A")

ph = phi(r)
D = DA(r)
Dp = sp.diff(D, r)
php = sp.diff(ph, r)


def christoffel(g, gi, coords):
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


def ricci_scalar(g, gi, coords):
    Ga = christoffel(g, gi, coords)
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
    R = sum(gi[i, i] * Ric[i, i] for i in range(4))
    return sp.simplify(R), Ric


print("=" * 70)
print("PHASE 2 CAS — metric family free D_A, reciprocal longitudinal block")
print("=" * 70)

# Metric: diag(-e^{-2phi}c^2, e^{2phi}, D_A^2, D_A^2 sin^2 theta)
g = sp.diag(
    -sp.exp(-2 * ph) * c**2,
    sp.exp(2 * ph),
    D**2,
    (D * sp.sin(th)) ** 2,
)
coords = [t, r, th, ps]
gi = g.inv()
detg = sp.simplify(g.det())
sqrtmg = sp.simplify(sp.sqrt(-detg))

print("\n[1] Measure √(-g)")
print("  √(-g) =", sqrtmg)
print("  == c D_A^2 sin(theta) (phi-free)?", sp.simplify(sqrtmg - c * D**2 * sp.sin(th)) == 0)

print("\n[2] Ricci scalar R (free D_A) — compute")
R, Ric = ricci_scalar(g, gi, coords)
R = sp.simplify(R)
print("  R =", R)

# Frozen D_A=r reduction check vs known formula
R_frozen = sp.simplify(R.subs(D, r).doit())
R_known = (
    sp.exp(-2 * ph) * (-4 * php**2 + 2 * sp.diff(ph, r, 2) + 8 * php / r)
    + 2 / r**2
    - 2 * sp.exp(-2 * ph) / r**2
)
# php and ph need to be consistent after sub - use phi(r) derivatives
R_known2 = sp.simplify(
    sp.exp(-2 * phi(r))
    * (
        -4 * sp.diff(phi(r), r) ** 2
        + 2 * sp.diff(phi(r), r, 2)
        + 8 * sp.diff(phi(r), r) / r
    )
    + 2 / r**2
    - 2 * sp.exp(-2 * phi(r)) / r**2
)
print("  R|_(D_A=r) matches founding formula?", sp.simplify(R_frozen - R_known2) == 0)

print("\n[3] EH integrand density √(-g) R — is bulk a total radial derivative?")
# Integrate angles: factor 4π effectively use dens = D_A^2 R  (drop c sin which separates)
# Full: int sin(th) dth dpsi = 4π, dens_r = c * D^2 * R after angular int... use L = D**2 * R
L_eh = sp.simplify(D**2 * R)
# Try to find B such that dB/dr = L_eh (up to terms that vanish on-shell? pure total deriv)
# Symbolic: integrate by parts structure — use sympy rewrite
# For free D_A this is harder; check variational EL of int L_eh w.r.t phi and D_A

def el(L, f):
    fp = sp.diff(f, r)
    fpp = sp.diff(f, r, 2)
    # if L depends on f, f', f''
    dL_df = sp.diff(L, f)
    dL_dfp = sp.diff(L, fp)
    dL_dfpp = sp.diff(L, fpp)
    return sp.simplify(dL_df - sp.diff(dL_dfp, r) + sp.diff(dL_dfpp, r, 2))


# L_eh may depend on phi'', D'', etc.
L_eh_exp = sp.expand(L_eh)
print("  Expanding L_eh = D_A^2 R for EL...")
# substitute derivatives as symbols for EL is messy; use variational with Function

# Use Euler-Lagrange treating phi and D_A as independent
el_phi_eh = el(L_eh, ph)
el_D_eh = el(L_eh, D)
print("  EL_phi[D_A^2 R] simplifies to:", sp.simplify(el_phi_eh))
print("  EL_D  [D_A^2 R] simplifies to:", sp.simplify(el_D_eh))
print("  EL_phi identically 0?", sp.simplify(el_phi_eh) == 0)
print("  EL_D  identically 0?", sp.simplify(el_D_eh) == 0)

# Founding: for D_A=r, r^2 R is total derivative
L_r = sp.simplify((r**2 * R).subs(D, r).doit())
bdy = 2 * r * (1 - sp.exp(-2 * ph)) + 2 * r**2 * sp.exp(-2 * ph) * php
print("\n[3b] Frozen D_A=r: r^2 R - d/dr[bdy] == 0?", sp.simplify(L_r - sp.diff(bdy, r)) == 0)

print("\n[4] R1-weighted kinetic density (shift-invariant)")
# √(-g) * e^{2phi} * g^{rr} * (phi')^2 = √(-g) * (phi')^2
kin_dens = sp.simplify(sqrtmg * sp.exp(2 * ph) * gi[1, 1] * php**2)
print("  √(-g) e^{2φ} g^{rr} (φ')^2 =", kin_dens)
print("  == c D_A^2 sin(theta) (φ')^2 (no explicit φ)?",
      sp.simplify(kin_dens - c * D**2 * sp.sin(th) * php**2) == 0)

print("\n[5] Vacuum dynamics from KINETIC ONLY: L_kin = (Z/2) D_A^2 (φ')^2")
L_kin = (Z / 2) * D**2 * php**2
el_phi_kin = sp.simplify(sp.diff(L_kin, php).diff(r) - sp.diff(L_kin, ph))
el_D_kin = sp.simplify(sp.diff(L_kin, Dp).diff(r) - sp.diff(L_kin, D))
print("  EL_φ =", el_phi_kin)
print("  EL_φ == d/dr(Z D_A^2 φ') ?", sp.simplify(el_phi_kin - sp.diff(Z * D**2 * php, r)) == 0)
print("  EL_D =", el_D_kin)
# On shell Z D^2 phi' = q
el_D_on = sp.simplify(el_D_kin.subs(php, q / (Z * D**2)))
print("  EL_D on Z D_A^2 φ'=q :", el_D_on)
print("  => if only kinetic, EL_D forces q=0 or singular D unless we do NOT vary D_A")
print("  INTERPRETATION: free D_A + pure kinetic => either freeze D_A (gauge/ansatz)")
print("  or add geometric terms that give D_A a kinetic/potential structure.")

print("\n[6] Geometric objects (definitions) — free round D_A")
# K_AB with normal n = e^{-phi} d_r
# K_cal = K_AB K^{AB} - K^2 = -2 e^{-2phi} (D'/D)^2
Kcal = -2 * sp.exp(-2 * ph) * (Dp / D) ** 2
print("  K_cal := K_AB K^{AB}-K^2 =", Kcal)
print("  D_A^2 K_cal =", sp.simplify(D**2 * Kcal))
print("  Compensated density D_A^2 e^{2φ} K_cal =", sp.simplify(D**2 * sp.exp(2 * ph) * Kcal))

print("\n[7] Illustrative reduced Lagrangians (NOT claimed unique theory)")
# A: kinetic + compensated K only (phi-free K piece)
L_A = (Z / 2) * D**2 * php**2 - 2 * Dp**2
elA_phi = sp.simplify(sp.diff(L_A, php).diff(r) - sp.diff(L_A, ph))
elA_D = sp.simplify(sp.diff(L_A, Dp).diff(r) - sp.diff(L_A, D))
print("  (A) L = (Z/2)D^2 φ'^2 - 2 (D')^2  [compensated K density]")
print("      EL_φ: d/dr(Z D^2 φ')=0 ?", sp.simplify(elA_phi - sp.diff(Z * D**2 * php, r)) == 0)
print("      EL_D:", elA_D)
print("      on φ'=q/(Z D^2):", sp.simplify(elA_D.subs(php, q / (Z * D**2))))

L_B = (Z / 2) * D**2 * php**2 - 2 * sp.exp(-2 * ph) * Dp**2
elB_phi = sp.simplify(sp.diff(L_B, php).diff(r) - sp.diff(L_B, ph))
elB_D = sp.simplify(sp.diff(L_B, Dp).diff(r) - sp.diff(L_B, D))
print("  (B) L = (Z/2)D^2 φ'^2 - 2 e^{-2φ}(D')^2  [raw K density]")
print("      EL_φ == d/dr(Z D^2 φ') - 4 e^{-2φ}(D')^2 ?",
      sp.simplify(elB_phi - (sp.diff(Z * D**2 * php, r) - 4 * sp.exp(-2 * ph) * Dp**2)) == 0)
print("      EL_D:", elB_D)

print("\n[8] FREE / FORCED summary print")
print("  FORCED (this CAS): reciprocal metric measure φ-free; R1 kinetic density φ-free;")
print("    pure kinetic EL_φ => d/dr(Z D_A^2 φ')=0; pure kinetic does not determine free D_A alone.")
print("  NOT FORCED: which geometric terms (A vs B vs none vs more) enter the bulk action;")
print("    matter; Z value; static spherical ansatz; edge.")
print("DONE")
