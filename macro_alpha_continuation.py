#!/usr/bin/env python3
"""
Macro continuation: larger-box jet + action-consistent L_m + finite-core probe.
Contract: macro_alpha_continuation_CONTRACT.md
Framing:  macro_no_GP_framing.md
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

Z = 1.0


# ----- shared helpers -----
def p2_jet(alpha, rc, c3):
    den = rc**2 * (3 * Z + 2 * alpha + 4)
    if abs(den) < 1e-14:
        return None
    return 2.0 * (6.0 * c3 * rc**2 + 1.0) / den


def integrate(f, y0, r0, r_max, max_step=0.05):
    return solve_ivp(
        f,
        (r0, r_max),
        y0,
        method="RK45",
        rtol=1e-7,
        atol=1e-9,
        max_step=max_step,
        dense_output=False,
    )


def diag(sol, label, r_max):
    if sol is None or len(sol.t) < 2:
        print(f"  [{label}] empty")
        return None
    r = sol.t
    D, Dp, phi, pi = sol.y
    php = pi / (Z * np.maximum(np.abs(D), 1e-16) ** 2)
    # turnover: D' changes + to -
    i_turn = None
    for i in range(1, len(Dp)):
        if Dp[i - 1] > 0 and Dp[i] <= 0:
            i_turn = i
            break
    # D'->0 soft edge signal
    i_flat = None
    if len(Dp) > 5:
        thr = 0.05 * max(1e-12, np.max(np.abs(Dp)))
        for i in range(len(Dp) // 5, len(Dp)):
            if abs(Dp[i]) < thr and D[i] > D[0]:
                i_flat = i
                break
    out = {
        "label": label,
        "ok": bool(sol.success),
        "msg": sol.message,
        "r_end": float(r[-1]),
        "reached": bool(sol.success and r[-1] >= r_max - 1e-6),
        "D0": float(D[0]),
        "Dend": float(D[-1]),
        "Dmax": float(np.max(D)),
        "Dpend": float(Dp[-1]),
        "dphi": float(phi[-1] - phi[0]),
        "phi_end": float(phi[-1]),
        "php0": float(php[0]),
        "php_max": float(np.nanmax(np.abs(php))),
        "finite": bool(np.all(np.isfinite(sol.y))),
        "turn_r": float(r[i_turn]) if i_turn is not None else None,
        "turn_D": float(D[i_turn]) if i_turn is not None else None,
        "flat_r": float(r[i_flat]) if i_flat is not None else None,
    }
    extra = ""
    if out["turn_r"] is not None:
        extra += f" TURN@r={out['turn_r']:.3g}"
    if out["flat_r"] is not None:
        extra += f" flatDp@r={out['flat_r']:.3g}"
    print(
        f"  [{label}] r→{out['r_end']:.4g} ok={out['ok']} fin={out['finite']} "
        f"D:{out['D0']:.3g}→{out['Dend']:.3g} (max{out['Dmax']:.3g}) "
        f"Δφ={out['dphi']:+.4f} |φ'|max={out['php_max']:.3e}{extra}"
    )
    return out


# =============================================================================
# PART A — prior jet model, larger box
# =============================================================================
def jet_rhs(alpha, rc, s0):
    def f(r, y):
        D, Dp, phi, pi = y
        De = max(abs(D), 1e-16)
        php = pi / (Z * De**2)
        sig = s0 * np.exp(-(r / rc) ** 2)
        pip = 4.0 * np.exp(-2.0 * phi) * Dp**2 + alpha * np.exp(alpha * phi) * sig
        Dpp = 2.0 * php * Dp - np.exp(2.0 * phi) * (Z / 4.0) * De * php**2
        Dpp = float(np.clip(Dpp if np.isfinite(Dpp) else 0.0, -1e8, 1e8))
        pip = float(np.clip(pip if np.isfinite(pip) else 0.0, -1e8, 1e8))
        return [Dp, Dpp, php, pip]

    return f


def run_jet_box(alpha, rc, c3, r_max, eps=1e-3):
    if alpha >= 0:
        return None, None
    s0 = -4.0 / alpha
    p2 = p2_jet(alpha, rc, c3)
    if p2 is None:
        return None, None
    D = eps + c3 * eps**3
    Dp = 1.0 + 3.0 * c3 * eps**2
    phi = p2 * eps**2
    php = 2.0 * p2 * eps
    pi = Z * D**2 * php
    sol = integrate(jet_rhs(alpha, rc, s0), [D, Dp, phi, pi], eps, r_max)
    return sol, dict(s0=s0, p2=p2)


# =============================================================================
# PART B — action-consistent L = (Z/2)D^2 phi'^2 - 2 e^{-2phi}(D')^2 - D^2 mu e^{alpha phi}
# =============================================================================
def action_mu_rhs(alpha, rc, mu0):
    """
    L = (Z/2) D^2 php^2 - 2 e^{-2phi} Dp^2 - D^2 mu(r) e^{alpha phi}
    EL_phi: d/dr(Z D^2 php) = 4 e^{-2phi} Dp^2 - alpha D^2 mu e^{alpha phi}
    EL_DA:  d/dr(-4 e^{-2phi} Dp) = Z D php^2 - 2 D mu e^{alpha phi}
         => D'' = 2 php Dp - e^{2phi}(Z/4) D php^2 + e^{2phi}(1/2) D mu e^{alpha phi}
    """

    def f(r, y):
        D, Dp, phi, pi = y
        De = max(abs(D), 1e-16)
        php = pi / (Z * De**2)
        mu = mu0 * np.exp(-(r / rc) ** 2)
        w = np.exp(alpha * phi)
        pip = 4.0 * np.exp(-2.0 * phi) * Dp**2 - alpha * De**2 * mu * w
        Dpp = (
            2.0 * php * Dp
            - np.exp(2.0 * phi) * (Z / 4.0) * De * php**2
            + np.exp(2.0 * phi) * 0.5 * De * mu * w
        )
        Dpp = float(np.clip(Dpp if np.isfinite(Dpp) else 0.0, -1e8, 1e8))
        pip = float(np.clip(pip if np.isfinite(pip) else 0.0, -1e8, 1e8))
        return [Dp, Dpp, php, pip]

    return f


def run_action_point_center(alpha, rc, mu0, eps=1e-3, r_max=8.0):
    """Point-center attempt with action mu — expect pi'(0)=4 still (matter~D^2)."""
    # series-like seed D=eps, Dp=1, phi=0, pi from vacuum-like int ~ 4*eps (matter negligible)
    D, Dp, phi = eps, 1.0, 0.0
    pi = 4.0 * eps  # leading geometric only
    sol = integrate(action_mu_rhs(alpha, rc, mu0), [D, Dp, phi, pi], eps, r_max)
    return sol


def run_finite_core(alpha, rc, mu0, Dc, r_max=30.0, eps=1e-4):
    """
    Finite core: start at r=eps with D=Dc, Dp=0, phi=0, pi=0 (regular even core).
    Domain is r>=0 with mirror symmetry at r=0.
    """
    y0 = [Dc, 0.0, 0.0, 0.0]
    sol = integrate(action_mu_rhs(alpha, rc, mu0), y0, eps, r_max, max_step=0.05)
    return sol


def analytic_action_center_note():
    print("\n[L3 analytic] action L_m = -D_A^2 mu e^{alpha phi}:")
    print("  pi' = 4 e^{-2phi}(D')^2 - alpha D_A^2 mu e^{alpha phi}")
    print("  at D_A=0, D'=1: pi'(0) = 4  (matter term vanishes) => same 1/r jet problem as alpha=0")
    print("  => finite-at-origin prescribed sigma is NOT the same as bulk mu with D^2 measure")


def main():
    print("=" * 70)
    print("MACRO CONTINUATION (larger box + action matter + finite core)")
    print("=" * 70)

    rows = []

    # ----- A: larger box jet -----
    print("\n=== PART A: jet model larger box (rho_eff=0, sigma stand-in) ===")
    cases = [
        (-1.0, 1.0, 0.0),
        (-2.0, 1.0, 0.0),
        (-0.5, 1.0, 0.0),
        (-1.0, 2.0, 0.0),
        (-1.0, 0.5, 0.0),
    ]
    for r_max in (8.0, 30.0, 80.0):
        print(f"\n-- r_max={r_max:g} --")
        for alpha, rc, c3 in cases:
            lab = f"jet a={alpha:g} rc={rc:g} R={r_max:g}"
            sol, ic = run_jet_box(alpha, rc, c3, r_max)
            row = diag(sol, lab, r_max)
            if row:
                row["family"] = "jet"
                rows.append(row)

    # asymptotic trend for one case: D and phi at sample radii
    print("\n-- sample jet a=-1 rc=1 profile (r_max=80) --")
    sol, _ = run_jet_box(-1.0, 1.0, 0.0, 80.0)
    if sol is not None and len(sol.t) > 10:
        r, D, Dp, phi = sol.t, sol.y[0], sol.y[1], sol.y[2]
        for rt in (1, 2, 5, 10, 20, 40, 80):
            if r[-1] < rt:
                break
            i = np.searchsorted(r, rt)
            i = min(i, len(r) - 1)
            print(
                f"  r={r[i]:6.2f}  D={D[i]:10.4g}  D'={Dp[i]:10.4g}  "
                f"phi={phi[i]:+.4f}  1+z=e^phi={np.exp(phi[i]):.4g}"
            )

    # ----- B: action-consistent -----
    analytic_action_center_note()

    print("\n=== PART B: action-consistent mu e^{alpha phi} — point-center attempt ===")
    for alpha in (-2.0, -1.0, -0.5):
        for mu0 in (0.0, 1.0, 4.0, 10.0):
            lab = f"act-pt a={alpha:g} mu0={mu0:g}"
            sol = run_action_point_center(alpha, 1.0, mu0, eps=1e-3, r_max=8.0)
            row = diag(sol, lab, 8.0)
            if row:
                row["family"] = "action_point"
                # php0 should be large ~ 4/eps if singular
                rows.append(row)

    print("\n=== PART C: finite core D(0)=Dc>0, D'(0)=0 + action mu ===")
    for alpha in (-2.0, -1.0, -0.5, 0.0):
        for Dc in (0.5, 1.0, 2.0):
            for mu0 in (0.0, 0.5, 1.0, 2.0, 5.0):
                for rc in (1.0, 2.0):
                    lab = f"core a={alpha:g} Dc={Dc:g} mu0={mu0:g} rc={rc:g}"
                    sol = run_finite_core(alpha, rc, mu0, Dc, r_max=30.0)
                    row = diag(sol, lab, 30.0)
                    if row:
                        row["family"] = "core"
                        rows.append(row)

    # ----- summary -----
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    jets = [r for r in rows if r.get("family") == "jet"]
    for R in (8.0, 30.0, 80.0):
        sub = [r for r in jets if f"R={R:g}" in r["label"] or r["label"].endswith(f"R={R:g}")]
        # labels are like jet a=-1 rc=1 R=8
        sub = [r for r in jets if f"R={R:g}" in r["label"]]
        ok = [r for r in sub if r.get("ok") and r.get("finite")]
        turns = [r for r in ok if r.get("turn_r") is not None]
        print(f"  L1/L2 jet r_max={R:g}: {len(ok)}/{len(sub)} OK finite; turnovers={len(turns)}")
        if ok:
            print(
                f"      Δφ range [{min(r['dphi'] for r in ok):+.3f}, {max(r['dphi'] for r in ok):+.3f}]  "
                f"Dend range [{min(r['Dend'] for r in ok):.3g}, {max(r['Dend'] for r in ok):.3g}]"
            )

    pts = [r for r in rows if r.get("family") == "action_point"]
    if pts:
        php0s = [r["php0"] for r in pts if "php0" in r]
        print(f"  L3 action point-center: |phi'(eps)| among runs ~ "
              f"{min(php0s):.3e} .. {max(php0s):.3e}  (expect O(1/eps)~4e3 if singular)")

    cores = [r for r in rows if r.get("family") == "core"]
    cok = [r for r in cores if r.get("ok") and r.get("finite") and r.get("reached")]
    cturn = [r for r in cok if r.get("turn_r") is not None]
    cdphi = [r for r in cok if abs(r["dphi"]) > 0.05]
    print(f"  L4 finite-core reached r=30 OK: {len(cok)}/{len(cores)}")
    print(f"      with |Δφ|>0.05: {len(cdphi)}; with D turnover: {len(cturn)}")
    # highlight best nontrivial cores
    if cdphi:
        cdphi_sorted = sorted(cdphi, key=lambda r: -abs(r["dphi"]))[:8]
        print("      largest |Δφ| finite-core successes:")
        for r in cdphi_sorted:
            print(
                f"        {r['label']}: Δφ={r['dphi']:+.4f} Dend={r['Dend']:.3g} "
                f"turn={r['turn_r']}"
            )

    print("\nDONE")


if __name__ == "__main__":
    main()
