#!/usr/bin/env python3
"""
WP1 — Path B + dust probe: write EL (CAS). No solve.
Gravity: free D_A + EH + R1 kinetic.
Matter: static spherical dust, alpha=0 (no direct phi coupling), FREE temporary probe.
MAP: macro_native_matter_edge_MAP.md
"""
from __future__ import annotations

import sympy as sp

r, th, c = sp.symbols("r theta c", positive=True)
Z = sp.symbols("Z", positive=True)
phi = sp.Function("phi")
DA = sp.Function("D_A")
rho = sp.Function("rho")  # dust energy density (rest)

ph = phi(r)
D = DA(r)
php = sp.diff(ph, r)
phpp = sp.diff(ph, r, 2)
Dp = sp.diff(D, r)
Dpp = sp.diff(D, r, 2)

print("=" * 70)
print("WP1 Path B + dust — structure and EL")
print("=" * 70)

# Metric factors
# g_tt = -e^{-2phi} c^2, g_rr = e^{2phi}, g_thth = D^2
# Static dust u^t only: u_t u^t = -1 => u^t = e^{phi}/c  (future-directed)
# T^t_t = -rho (energy density in rest frame), other components 0 for dust pressureless
# Hilbert: vary sqrt(-g) R gives Einstein tensor; matter couples via T_mu nu
# Equivalent reduced approach for spherical static:
# For dust, Lagrangian density often L_m = -rho with constraint, or use
#   int sqrt(-g) (-rho) with rho conserved appropriately.
#
# With sqrt(-g) = c D^2 sin(th) (phi-free), L_m density ~ -rho * D^2
# if rho is coordinate scalar density of rest mass per proper volume carefully:
# Proper energy density rho_proper; for static dust
#   S_m = -int rho_proper c^2 sqrt(-g) d^4x  with u^mu u_mu=-1
# Since sqrt(-g) is phi-free, delta S_m / delta phi = 0 from measure alone;
# residual coupling can appear if rho_proper is defined with metric projections.
#
# Channel-blind static dust probe (FREE): take reduced radial matter density
#   L_m = - rho(r) * D_A^2
# so matter does not depend on phi explicitly (alpha=0). Conservation will relate rho and D, phi.

L_m = -rho(r) * D**2
print("\n[1] FREE dust probe reduced L_m = -rho(r) D_A^2  (alpha=0, no explicit phi)")
print("    Tag: FREE temporary; not UDT-fundamental.")

# Gravity L as before
R = (
    2
    * sp.exp(-2 * ph)
    / D**2
    * (
        -2 * D**2 * php**2
        + D**2 * phpp
        + 4 * D * Dp * php
        - 2 * D * Dpp
        + sp.exp(2 * ph)
        - Dp**2
    )
)
L_eh = sp.simplify(D**2 * R)
L_kin = (Z / 2) * D**2 * php**2
L_g = sp.simplify(L_eh + L_kin)
L = sp.simplify(L_g + L_m)


def el(L, f):
    fp = sp.diff(f, r)
    fpp = sp.diff(f, r, 2)
    return sp.simplify(
        sp.diff(L, f) - sp.diff(sp.diff(L, fp), r) + sp.diff(sp.diff(L, fpp), r, 2)
    )


el_phi = el(L, ph)
el_D = el(L, D)

print("\n[2] EL_phi (full) =", el_phi)
print("    EL_phi vacuum part + matter: matter contrib to EL_phi =", sp.simplify(el(L_m, ph)))
print("    => explicit phi-blind L_m does not source EL_phi directly:", sp.simplify(el(L_m, ph)) == 0)

print("\n[3] EL_D (full) =", el_D)
print("    matter piece el(L_m, D) =", sp.simplify(el(L_m, D)))

# Conservation for static spherical dust on this metric
# nabla_mu T^mu_r = 0 for dust => pressureless: either rho=0 or flow; static dust
# T^t_t = -rho, and hydrostatic: for p=0, d p /dr = 0 automatically, but
# continuity: (rho u^mu);_mu = 0
# u^t = e^{phi}/c, u_t = -c e^{-phi}
# sqrt(-g) rho u^r = 0 for static; only constraint is consistency of Einstein G_tt ~ rho
# For p=0 static: Euler says partial_r p = 0 OK; density free radial profile
# OR for free-fall dust not static.
# FREE probe: allow rho=rho(r) prescribed OR from G_tt Einstein equation once solved.
print("\n[4] Static dust conservation note:")
print("    p=0 static: hydrostatic identity trivial; rho(r) is NOT fixed by continuity alone.")
print("    rho is FREE profile OR solved algebraically from Einstein G_{tt} ~ rho if that eq is used.")
print("    Tag: rho profile FREE in probe; or on-shell from EL/Einstein.")

# Einstein G_tt style: vary or use known structure
# Compare vacuum EL_D matter shift: el(L_m,D) = 2 rho D  (since L_m=-rho D^2, d/dr terms 0)
print("\n[5] Matter contribution to EL_D:")
print("    el(-rho D^2, D) =", sp.simplify(el(-rho(r) * D**2, D)))
print("    = +2 rho D   (sign: L_m=-rho D^2 => tends to act like pressureless source in D eq)")

# Full system summary
print("\n[6] System summary (WP1):")
print("    Unknowns: phi(r), D_A(r), and either free rho(r) or rho from constraint.")
print("    EL_phi: same as vacuum Path B (matter phi-blind in this L_m).")
print("    EL_D:  vacuum Path B EL_D + 2 rho D_A  (with this reduced L_m).")
print("    Dust does NOT directly raise phi; it only reshapes D_A, which couples back via EH.")
print("    That is the only legal channel for this FREE alpha=0 probe.")

# Contrast: if someone puts L_m = -rho D^2 e^{alpha phi}
alpha = sp.symbols("alpha", real=True)
L_ma = -rho(r) * D**2 * sp.exp(alpha * ph)
print("\n[7] FORBIDDEN-as-default contrast L_m ∝ e^{alpha phi}:")
print("    el_phi matter =", sp.simplify(el(L_ma, ph)))
print("    (only for separate tagged fork; default WP2 uses alpha=0)")

print("\nDONE WP1")
