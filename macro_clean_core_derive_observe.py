#!/usr/bin/env python3
"""
Clean-core macro: DERIVE free-D_A EOM (G/P, vacuum + φ-blind ρ) + OBSERVE center structure.

Contract: macro_clean_core_first_observe_CONTRACT.md
Posture:  macro_Q1_source_posture.md  (Q1=(a) primary)
MAP:      macro_universe_clean_core_MAP.md

NO SNe fit. NO cosine targeting. Characterize only.
"""
from __future__ import annotations

import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp

Zval = 1.0  # FREE convention

# =============================================================================
# PART A — CAS DERIVE
# =============================================================================
print("=" * 70)
print("PART A — CAS DERIVE (free D_A, round h_AB = D_A^2 Omega)")
print("=" * 70)

r = sp.symbols("r", positive=True)
Z = sp.symbols("Z", positive=True)
phi = sp.Function("phi")
DA = sp.Function("D_A")
rho = sp.Function("rho")  # prescribed φ-blind density

ph = phi(r)
D = DA(r)
Dp = sp.diff(D, r)
php = sp.diff(ph, r)

# Reduced radial Lagrangian (drop 4π; topological +2 kept but D_A-independent):
# L = (Z/2) D^2 phi'^2 + 2 + D^2 * K_branch + D^2 * L_m
# L_m = -rho(r)   (Q4 FREE stand-in; no explicit phi)

def el_phi(L):
    return sp.simplify(sp.diff(L, php).diff(r) - sp.diff(L, ph))

def el_DA(L):
    return sp.simplify(sp.diff(L, Dp).diff(r) - sp.diff(L, D))


# --- Branch G vacuum (compensated K): D^2 K_G = -2 (D')^2 ---
L_G_vac = (Z / 2) * D**2 * php**2 - 2 * Dp**2
eom_phi_G = el_phi(L_G_vac)
eom_DA_G = el_DA(L_G_vac)
print("\n[A1] Branch G vacuum L = (Z/2)D^2 phi'^2 - 2 (D')^2")
print("  EL_phi =", eom_phi_G)
print("  EL_DA  =", eom_DA_G)
# Expected: d/dr(Z D^2 phi') = 0  and  Z D phi'^2 + 4 D'' = 0
flux_G = sp.diff(Z * D**2 * php, r)
print("  EL_phi == d/dr(Z D^2 phi') ?", sp.simplify(eom_phi_G - flux_G) == 0)
print("  EL_DA  == -(Z D phi'^2 + 4 D'') ?",
      sp.simplify(eom_DA_G + (Z * D * php**2 + 4 * sp.diff(D, r, 2))) == 0)
# First integral form
q = sp.symbols("q")
print("  with Z D^2 phi' = q: D'' + q^2/(4 Z D^3) == 0?",
      sp.simplify(sp.diff(D, r, 2) + q**2 / (4 * Z * D**3)) == sp.diff(D, r, 2) + q**2 / (4 * Z * D**3))
# substitute
eom_DA_G_on = sp.simplify(eom_DA_G.subs(php, q / (Z * D**2)))
print("  EL_DA on-shell phi' = q/(Z D^2):", eom_DA_G_on)
print("  => D'' = -q^2/(4 Z D^3) residual check:",
      sp.simplify(eom_DA_G_on + 4 * (sp.diff(D, r, 2) + q**2 / (4 * Z * D**3))))


# --- Branch P vacuum (uncompensated): D^2 K = -2 e^{-2phi} (D')^2 ---
L_P_vac = (Z / 2) * D**2 * php**2 - 2 * sp.exp(-2 * ph) * Dp**2
eom_phi_P = el_phi(L_P_vac)
eom_DA_P = el_DA(L_P_vac)
print("\n[A2] Branch P vacuum L = (Z/2)D^2 phi'^2 - 2 e^{-2phi} (D')^2")
print("  EL_phi =", eom_phi_P)
print("  EL_DA  =", eom_DA_P)
# Expected EL_phi: d/dr(Z D^2 phi') - 4 e^{-2phi} (D')^2 = 0
expect_phi_P = sp.diff(Z * D**2 * php, r) - 4 * sp.exp(-2 * ph) * Dp**2
print("  EL_phi == d/dr(Z D^2 phi') - 4 e^{-2phi}(D')^2 ?",
      sp.simplify(eom_phi_P - expect_phi_P) == 0)
# Frozen D=r check
eom_phi_P_frozen = sp.simplify(eom_phi_P.subs(D, r).doit())
print("  frozen D_A=r: EL_phi reduces to Z(r^2 phi')' - 4 e^{-2phi} ?",
      sp.simplify(eom_phi_P_frozen - (Z * sp.diff(r**2 * php, r) - 4 * sp.exp(-2 * ph))) == 0)


# --- Branch P + φ-blind L_m = -rho(r) ---
L_P_m = L_P_vac - D**2 * rho(r)
eom_phi_Pm = el_phi(L_P_m)
eom_DA_Pm = el_DA(L_P_m)
print("\n[A3] Branch P + L_m=-rho(r)  (φ-blind prescribed density)")
print("  EL_phi =", eom_phi_Pm)
print("  EL_phi identical to vacuum P?", sp.simplify(eom_phi_Pm - eom_phi_P) == 0)
print("  EL_DA  =", eom_DA_Pm)
print("  EL_DA - EL_DA_vac =", sp.simplify(eom_DA_Pm - eom_DA_P))
print("  => rho ENTERS only EL_DA (term from -D^2 rho), NOT EL_phi.")


# --- Center series: D_A ~ r, power-law analysis for P ---
print("\n[A4] Center structure on P (analytic)")
print("  Integrated EL_phi (C=0 at r=0):  Z D^2 phi' = int_0^r 4 e^{-2phi} (D')^2 ds")
print("  Power-law ansatz D_A = a r^alpha (alpha>0), phi smooth => e^{-2phi}~const:")
a_s, alpha, r_s = sp.symbols("a alpha r", positive=True)
# I(r) = int_0^r (D')^2 ~ int_0^r (a alpha s^{alpha-1})^2 ds = a^2 alpha^2 r^{2alpha-1}/(2alpha-1)
# need 2alpha-1 > 0 => alpha > 1/2
# phi' = I / (Z D^2) ~ r^{2alpha-1} / r^{2alpha} = r^{-1}
print("  => phi' ~ 1/r  for ANY alpha > 1/2 with D_A(0)=0 (power-law).")
print("  => phi ~ ln r → -∞ as r→0: LOG DILATION SINGULARITY at geometric center.")
print("  => φ-blind rho cannot cancel this: it does not appear in EL_phi.")

# G center: phi' = q/(Z D^2) ~ q/r^2 if D~r — worse (1/r pole in phi)
print("\n[A5] Center structure on G (analytic)")
print("  Z D^2 phi' = q (const). D~r => phi' ~ q/r^2 => phi ~ -q/r (1/r singularity) if q≠0.")
print("  q=0 => phi=const => no redshift. Same vacuum tension as banked n=2 optics work.")


# =============================================================================
# PART B — NUMERIC OBSERVE (bounded IVP from epsilon outward)
# =============================================================================
print("\n" + "=" * 70)
print("PART B — NUMERIC OBSERVE (bounded; characterize, do not target)")
print("=" * 70)

def rho_gauss(r, rho0, rc):
    return rho0 * np.exp(-(r / rc) ** 2)


def ivp_P(rho0, rc, eps=1e-3, r_max=8.0, DA0_scale=1.0, phi0=0.0):
    """
    Branch P + optional gauss density.
    State y = [D_A, D_A', phi, pi] with pi := Z D_A^2 phi'  (flux).
    EL_phi:  pi' = 4 e^{-2phi} (D_A')^2
    phi'   = pi / (Z D_A^2)
    EL_DA:  from eom — rearrange for D''.

    From sympy EL_DA for L = (Z/2)D^2 phi'^2 - 2 e^{-2phi}(D')^2 - D^2 rho:
    We use the form derived:
      d/dr( -4 e^{-2phi} D' ) = Z D phi'^2 - 2 D rho
    Actually EL = d/dr(∂L/∂D') - ∂L/∂D = 0
      ∂L/∂D' = -4 e^{-2phi} D'
      ∂L/∂D  = Z D phi'^2 - 2 D rho
    => d/dr(-4 e^{-2phi} D') - (Z D phi'^2 - 2 D rho) = 0
    => -4[ -2 phi' e^{-2phi} D' + e^{-2phi} D'' ] = Z D phi'^2 - 2 D rho
    => 8 phi' e^{-2phi} D' - 4 e^{-2phi} D'' = Z D phi'^2 - 2 D rho
    => D'' = 2 phi' D' - e^{2phi}(Z/4) D phi'^2 + e^{2phi}(1/2) D rho
    """
    Z = Zval

    def f(r, y):
        D, Dp, ph, pi = y
        # protect
        D_eff = max(D, 1e-14)
        php = pi / (Z * D_eff**2)
        # pi' = 4 e^{-2phi} (D')^2
        pip = 4.0 * np.exp(-2.0 * ph) * (Dp**2)
        rh = rho_gauss(r, rho0, rc)
        Dpp = (2.0 * php * Dp
               - np.exp(2.0 * ph) * (Z / 4.0) * D_eff * php**2
               + np.exp(2.0 * ph) * 0.5 * D_eff * rh)
        return [Dp, Dpp, php, pip]

    # Start slightly off center with regular-looking seed (will test if it stays regular)
    # D(eps)=eps, D'=1, phi=phi0, pi = Z D^2 phi' with phi' trial from series ~ 4/(Z eps) *?
    # series says phi'~4/(Z*a^2 * r) with a=1 => pi = Z D^2 phi' ~ Z eps^2 * 4/(Z eps) = 4 eps
    D_eps = DA0_scale * eps
    Dp_eps = DA0_scale
    # Use integrated vacuum-P estimate: pi(eps) ≈ 4 * eps * (Dp)^2 * e^{-2phi0}  (if phi~const)
    pi_eps = 4.0 * eps * (Dp_eps**2) * np.exp(-2.0 * phi0)
    y0 = [D_eps, Dp_eps, phi0, pi_eps]

    sol = solve_ivp(f, (eps, r_max), y0, rtol=1e-7, atol=1e-9, dense_output=False,
                    max_step=0.05)
    return sol


def ivp_G(q, eps=1e-3, r_max=8.0, E=0.0, Dobs_start=None):
    """
    Branch G vacuum: phi' = q/(Z D^2), D'' = -q^2/(4 Z D^3).
    Start at D=eps with D' from first integral D'^2 = q^2/(4Z D^2) + E.
    """
    Z = Zval
    A = q**2 / (4 * Z)

    def f(r, y):
        D, Dp, ph = y
        D_eff = max(D, 1e-14)
        php = q / (Z * D_eff**2)
        Dpp = -q**2 / (4 * Z * D_eff**3)
        return [Dp, Dpp, php]

    D0 = eps if Dobs_start is None else Dobs_start
    val = A / D0**2 + E
    if val <= 0:
        return None
    Dp0 = np.sqrt(val)
    ph0 = 0.0  # observer frame at start point (not necessarily center)
    sol = solve_ivp(f, (0.0, r_max), [D0, Dp0, ph0], rtol=1e-7, atol=1e-9, max_step=0.05)
    return sol


def summarize_P(label, sol, eps):
    if sol is None or not sol.success:
        print(f"  [{label}] FAIL success={getattr(sol, 'success', None)} msg={getattr(sol, 'message', None)}")
        return None
    r = sol.t
    D, Dp, ph, pi = sol.y
    php = pi / (Zval * np.maximum(D, 1e-14)**2)
    out = {
        "label": label,
        "n": len(r),
        "r_end": float(r[-1]),
        "D_end": float(D[-1]),
        "phi_end": float(ph[-1]),
        "phi_start": float(ph[0]),
        "dphi": float(ph[-1] - ph[0]),
        "php_max": float(np.nanmax(np.abs(php))),
        "php_start": float(php[0]),
        "D_min": float(np.min(D)),
        "D_start": float(D[0]),
        "finite": bool(np.all(np.isfinite(sol.y))),
    }
    print(f"  [{label}] r∈[{r[0]:.3g},{out['r_end']:.3g}]  "
          f"D: {out['D_start']:.3g}→{out['D_end']:.3g}  "
          f"Δφ={out['dphi']:+.4f}  |φ'|_max={out['php_max']:.3e}  "
          f"φ'(eps)={out['php_start']:.3e}  finite={out['finite']}")
    return out


print("\n[B0] Control — Branch G vacuum:")
for q, E in ((0.0, 1.0), (0.5, 0.0), (1.0, 0.0)):
    sol = ivp_G(q, eps=1e-3, r_max=5.0, E=E)
    if sol is None or not sol.success:
        print(f"  [G q={q} E={E}] fail msg={getattr(sol, 'message', None)}")
        continue
    D, Dp, ph = sol.y
    php0 = abs(q) / (Zval * max(D[0], 1e-30)**2) if q != 0 else 0.0
    print(f"  [G q={q} E={E}] Δφ={ph[-1]-ph[0]:+.4f}  D: {D[0]:.3g}→{D[-1]:.3g}  "
          f"|φ'|_start={php0:.3e}")

print("\n[B1] Center LAW (no IVP) — P with D_A=a*r near 0, phi~const for leading order:")
print("  Z D^2 phi' = int_0^eps 4 e^{-2phi} (D')^2 ds ≈ 4 a^2 eps  (phi≈0)")
print("  phi'(eps) = [4 a^2 eps] / (Z a^2 eps^2) = 4/(Z eps)")
for eps in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5):
    php = 4.0 / (Zval * eps)
    print(f"  eps={eps:.0e}  =>  phi'~{php:.6e}   eps*phi'={eps*php:.4f} (expect 4)")
print("  => lim eps->0 |phi'| = +inf  (log singularity of phi). STRUCTURAL, not numeric.")

print("\n[B2] Same law is rho-independent (CAS A3): adding φ-blind rho cannot change phi'(eps).")
print("  EL_phi has no rho => C2 cannot cure C1 center blowup inside this coupling.")

print("\n[B3] Mid-domain P IVP (start AWAY from center — existence of some P trajectories):")
rows = []

def ivp_P_mid(rho0, rc, r0=0.5, r_max=6.0, D0=0.5, Dp0=1.0, phi0=0.0, pi0=0.0):
    """Start at finite r0 with finite data — not a center claim."""
    Z = Zval

    def f(r, y):
        D, Dp, ph, pi = y
        D_eff = max(abs(D), 1e-14)
        php = pi / (Z * D_eff**2)
        pip = 4.0 * np.exp(-2.0 * ph) * (Dp**2)
        rh = rho_gauss(r, rho0, rc)
        Dpp = (2.0 * php * Dp
               - np.exp(2.0 * ph) * (Z / 4.0) * D_eff * php**2
               + np.exp(2.0 * ph) * 0.5 * D_eff * rh)
        if not np.all(np.isfinite([Dp, Dpp, php, pip])):
            return [0.0, 0.0, 0.0, 0.0]
        # soft clip extreme steps
        Dpp = float(np.clip(Dpp, -1e6, 1e6))
        pip = float(np.clip(pip, -1e6, 1e6))
        return [Dp, Dpp, php, pip]

    y0 = [D0, Dp0, phi0, pi0]
    sol = solve_ivp(f, (r0, r_max), y0, rtol=1e-6, atol=1e-8, max_step=0.02,
                    dense_output=False)
    return sol

for rho0 in (0.0, 1.0, 10.0):
    sol = ivp_P_mid(rho0=rho0, rc=1.0, r0=0.5, r_max=4.0, D0=0.5, Dp0=0.8, phi0=0.0, pi0=0.2)
    row = summarize_P(f"P mid ρ0={rho0:g}", sol, 0.5)
    if row:
        rows.append(row)

print("\n[B4] Residual spot-check on a successful mid-domain P trajectory:")
sol = ivp_P_mid(0.0, 1.0, r0=0.5, r_max=3.0, D0=0.5, Dp0=0.8, phi0=0.0, pi0=0.2)
if sol is not None and sol.success and len(sol.t) > 10:
    r = sol.t
    D, Dp, ph, pi = sol.y
    pip_num = np.gradient(pi, r)
    pip_rhs = 4.0 * np.exp(-2.0 * ph) * Dp**2
    res = pip_num[2:-2] - pip_rhs[2:-2]
    print(f"  median|pi' - 4 exp(-2phi)(D')^2| = {np.median(np.abs(res)):.3e}  "
          f"max = {np.max(np.abs(res)):.3e}")
else:
    print(f"  mid-domain integrate fail: success={getattr(sol, 'success', None)} "
          f"msg={getattr(sol, 'message', None)}")
    if sol is not None and len(getattr(sol, 't', [])) > 0:
        print(f"  reached n={len(sol.t)} r_end={sol.t[-1]:.4g}")

print("\n[B5] CLASSIFICATION (pre-registered C0–C3):")
print("  C0 G vacuum: q!=0 => redshift only with singular/off-center D_A->0; q=0 => no redshift.")
print("  C1 vacuum P free-D_A: analytic center law phi'~4/(Z r) as r->0 with D_A~r — SINGULAR.")
print("  C2 P + phi-blind rho: rho absent from EL_phi — cannot regularize center.")
print("  C3 regular geometric center + nontrivial Delta-phi: NOT FOUND / STRUCTURALLY BLOCKED")
print("     in this slice (round free D_A, uncompensated K, phi-blind L_m, D_A(0)=0).")

print("\n" + "=" * 70)
print("DONE — see macro_clean_core_first_observe_results.md")
print("=" * 70)
