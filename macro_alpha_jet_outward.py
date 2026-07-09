#!/usr/bin/env python3
"""
Outward IVP from α<0 regular center jet — clean-core macro observe.
Contract: macro_alpha_jet_outward_CONTRACT.md
Framing:  macro_no_GP_framing.md  (no G/P labels)

Characterize only. No SNe / cosine / 1101.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

Z = 1.0


def p2_of(alpha, rc, c3, Z=Z):
    den = rc**2 * (3 * Z + 2 * alpha + 4)
    if abs(den) < 1e-14:
        return None
    return 2.0 * (6.0 * c3 * rc**2 + 1.0) / den


def sigma0_of(alpha):
    if alpha >= 0:
        return None
    return -4.0 / alpha


def ic_at_eps(alpha, rc, c3, eps=1e-3):
    """Regular jet ICs at r=eps."""
    s0 = sigma0_of(alpha)
    p2 = p2_of(alpha, rc, c3)
    if s0 is None or p2 is None:
        return None
    D = eps + c3 * eps**3
    Dp = 1.0 + 3.0 * c3 * eps**2
    phi = p2 * eps**2
    php = 2.0 * p2 * eps  # d/dr (p2 r^2) at eps
    pi = Z * D**2 * php
    return dict(D=D, Dp=Dp, phi=phi, pi=pi, p2=p2, s0=s0, php=php)


def rhs_factory(alpha, rc, s0, rho_eff_mode="zero"):
    """
    y = [D, Dp, phi, pi]
    pi' = 4 e^{-2phi} (Dp)^2 + alpha e^{alpha phi} sigma
    phi' = pi / (Z D^2)
    D'' from EL_DA of L=(Z/2)D^2 phi'^2 - 2 e^{-2phi}(Dp)^2 - D^2 rho_eff
      D'' = 2 phi' Dp - e^{2phi}(Z/4) D phi'^2 + e^{2phi}(1/2) D rho_eff
    rho_eff: 'zero' or 'sigma' (optional cross-check)
    """

    def f(r, y):
        D, Dp, phi, pi = y
        De = max(abs(D), 1e-16)
        php = pi / (Z * De**2)
        sig = s0 * np.exp(-(r / rc) ** 2)
        pip = 4.0 * np.exp(-2.0 * phi) * (Dp**2) + alpha * np.exp(alpha * phi) * sig
        if rho_eff_mode == "sigma":
            rh = sig  # FREE: not a derived identity
        else:
            rh = 0.0
        Dpp = (
            2.0 * php * Dp
            - np.exp(2.0 * phi) * (Z / 4.0) * De * (php**2)
            + np.exp(2.0 * phi) * 0.5 * De * rh
        )
        # soft clips for stiffness reporting (not physics)
        if not np.isfinite(Dpp):
            Dpp = 0.0
        if not np.isfinite(pip):
            pip = 0.0
        Dpp = float(np.clip(Dpp, -1e8, 1e8))
        pip = float(np.clip(pip, -1e8, 1e8))
        return [Dp, Dpp, php, pip]

    return f


def integrate(alpha, rc, c3, eps=1e-3, r_max=8.0, rho_eff_mode="zero"):
    ic = ic_at_eps(alpha, rc, c3, eps=eps)
    if ic is None:
        return None, "bad_ic"
    y0 = [ic["D"], ic["Dp"], ic["phi"], ic["pi"]]
    f = rhs_factory(alpha, rc, ic["s0"], rho_eff_mode=rho_eff_mode)
    sol = solve_ivp(
        f,
        (eps, r_max),
        y0,
        method="RK45",
        rtol=1e-7,
        atol=1e-9,
        max_step=0.02,
        dense_output=False,
    )
    return sol, ic


def summarize(label, sol, ic, eps, r_max):
    if sol is None:
        print(f"  [{label}] no sol ({ic})")
        return None
    if not sol.success and len(sol.t) < 5:
        print(f"  [{label}] FAIL early: {sol.message}")
        return {
            "label": label,
            "ok": False,
            "msg": sol.message,
            "r_end": float(sol.t[-1]) if len(sol.t) else eps,
        }
    r = sol.t
    D, Dp, phi, pi = sol.y
    php = pi / (Z * np.maximum(np.abs(D), 1e-16) ** 2)
    # diagnostics
    i_turn = None
    if len(D) > 3:
        # first local max of D if any (turnover)
        for i in range(1, len(D) - 1):
            if D[i] >= D[i - 1] and D[i] >= D[i + 1] and Dp[i] * Dp[i - 1] <= 0:
                i_turn = i
                break
    out = {
        "label": label,
        "ok": bool(sol.success),
        "msg": sol.message,
        "n": len(r),
        "r_end": float(r[-1]),
        "reached_max": bool(sol.success and r[-1] >= r_max - 1e-6),
        "D_start": float(D[0]),
        "D_end": float(D[-1]),
        "D_min": float(np.min(D)),
        "D_max": float(np.max(D)),
        "Dp_end": float(Dp[-1]),
        "phi_start": float(phi[0]),
        "phi_end": float(phi[-1]),
        "dphi": float(phi[-1] - phi[0]),
        "php_start": float(php[0]),
        "php_max": float(np.nanmax(np.abs(php))),
        "php_end": float(php[-1]),
        "finite": bool(np.all(np.isfinite(sol.y))),
        "p2": float(ic["p2"]),
        "s0": float(ic["s0"]),
        "turn_r": float(r[i_turn]) if i_turn is not None else None,
        "turn_D": float(D[i_turn]) if i_turn is not None else None,
    }
    turn_s = (
        f" turn@r={out['turn_r']:.3g} D={out['turn_D']:.3g}"
        if out["turn_r"] is not None
        else ""
    )
    print(
        f"  [{label}] r→{out['r_end']:.3g} ok={out['ok']} finite={out['finite']}  "
        f"D:{out['D_start']:.3g}→{out['D_end']:.3g} (max {out['D_max']:.3g})  "
        f"Δφ={out['dphi']:+.4f} |φ'|max={out['php_max']:.3e} φ'(ε)={out['php_start']:.3e}"
        f"{turn_s}"
    )
    return out


def residual_check(sol, alpha, rc, s0):
    if sol is None or len(sol.t) < 10:
        return None
    r = sol.t
    D, Dp, phi, pi = sol.y
    pip_num = np.gradient(pi, r)
    sig = s0 * np.exp(-(r / rc) ** 2)
    pip_rhs = 4.0 * np.exp(-2.0 * phi) * Dp**2 + alpha * np.exp(alpha * phi) * sig
    res = pip_num[2:-2] - pip_rhs[2:-2]
    med = float(np.median(np.abs(res)))
    mx = float(np.max(np.abs(res)))
    print(f"    residual median|pi'-RHS|={med:.3e}  max={mx:.3e}")
    return med, mx


def main():
    print("=" * 70)
    print("MACRO α-jet outward OBSERVE (no G/P labels)")
    print("=" * 70)

    rows = []

    # J0 control alpha=0 — expect singular IC path (use old 1/r seed contrast)
    print("\n[J0] alpha=0 control (no regular jet; phi'~4/(Z r) at eps):")
    eps = 1e-3
    for eps0 in (1e-2, 1e-3, 1e-4):
        php = 4.0 / (Z * eps0)
        print(f"  eps={eps0:.0e}  implied |phi'|~{php:.3e}  (diverges as eps->0)")

    print("\n[J1–J5] alpha<0 regular jet outward (rho_eff=0 primary):")
    grid = []
    for alpha in (-2.0, -1.0, -0.5):
        for rc in (0.5, 1.0, 2.0):
            for c3 in (0.0, 0.05, -0.05):
                grid.append((alpha, rc, c3))

    for alpha, rc, c3 in grid:
        lab = f"a={alpha:g} rc={rc:g} c3={c3:g}"
        sol, ic = integrate(alpha, rc, c3, eps=eps, r_max=8.0, rho_eff_mode="zero")
        if isinstance(ic, str):
            print(f"  [{lab}] skip ({ic})")
            continue
        row = summarize(lab, sol, ic, eps, 8.0)
        if row and row.get("ok"):
            residual_check(sol, alpha, rc, ic["s0"])
        if row:
            rows.append(row)

    print("\n[cross] sample with rho_eff=sigma (FREE, not derived):")
    for alpha, rc, c3 in [(-1.0, 1.0, 0.0), (-2.0, 1.0, 0.0)]:
        lab = f"a={alpha:g} rc={rc:g} c3={c3:g} rho=sig"
        sol, ic = integrate(alpha, rc, c3, eps=eps, r_max=8.0, rho_eff_mode="sigma")
        if isinstance(ic, str):
            continue
        row = summarize(lab, sol, ic, eps, 8.0)
        if row and row.get("ok"):
            residual_check(sol, alpha, rc, ic["s0"])
        if row:
            rows.append(row)

    # Classification
    print("\n" + "=" * 70)
    print("CLASSIFICATION")
    print("=" * 70)
    ok_rows = [r for r in rows if r.get("ok") and r.get("finite")]
    reached = [r for r in ok_rows if r.get("reached_max")]
    turned = [r for r in ok_rows if r.get("turn_r") is not None]
    failed = [r for r in rows if not r.get("ok")]

    print(f"  J0 alpha=0: singular center law (analytic) — control only")
    print(f"  J1 regular start: all alpha<0 ICs constructed with finite phi'(eps)~O(eps)")
    if ok_rows:
        phps = [r["php_start"] for r in ok_rows if "php_start" in r]
        print(f"      sample |phi'(eps)| max among OK runs = {max(phps):.3e} (should be << 1/eps)")
    print(f"  J2 reached r_max=8 with finite fields: {len(reached)} / {len(rows)} listed runs")
    print(f"  J6 failed/stiff before useful length: {len(failed)}")
    if ok_rows:
        dphis = [r["dphi"] for r in ok_rows]
        Dends = [r["D_end"] for r in ok_rows]
        print(f"  J4 Delta-phi among OK: min={min(dphis):+.4f} max={max(dphis):+.4f}")
        print(f"  J3 D_end among OK: min={min(Dends):.3g} max={max(Dends):.3g}")
    print(f"  J3/J5 turnover (local D max in-box): {len(turned)} runs")
    if turned:
        for r in turned[:8]:
            print(f"      {r['label']}: turn r={r['turn_r']:.3g} D={r['turn_D']:.3g} Δφ={r['dphi']:+.4f}")

    # Highlight a few representative OK trajectories
    print("\nRepresentative OK trajectories:")
    for key in ["a=-1 rc=1 c3=0", "a=-2 rc=1 c3=0", "a=-0.5 rc=1 c3=0", "a=-1 rc=2 c3=0"]:
        hit = next((r for r in rows if r.get("label") == key), None)
        if hit:
            print(
                f"  {key}: ok={hit.get('ok')} r_end={hit.get('r_end'):.3g} "
                f"D_end={hit.get('D_end'):.3g} Δφ={hit.get('dphi'):+.4f} "
                f"|φ'|max={hit.get('php_max'):.3e}"
            )

    print("\nDONE")
    return rows


if __name__ == "__main__":
    main()
