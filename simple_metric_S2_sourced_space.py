#!/usr/bin/env python3
"""
S2 — Sourced solution-space observe on the simple metric (MS continuum).

Arena: D_A = r, A = e^{-2φ} = 1 - 2m/r  (c=G=1),  m' = 4π r² ρ
       1+z = e^φ = 1/sqrt(A)   (where A>0)
       full light readout: d_L = (1+z)^2 r

Source: NAMED probe densities (FREE amount/scale) — not fundamental matter,
not residual-fitted free A(r).

PRE-REGISTERED:
  - No χ² inside the integrator
  - No imposed A(X)=0 BC (except critical const-ρ analytic check)
  - Report who DEVELOPS A→0 at finite r
  - Optional residual demo AFTER inventory (separate, clearly labeled)

Anti-hang: 1D ODE, modest grids, one process.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parent


def integrate_ms(rho_fn, r_max=20.0, n_out=800, r0=1e-4):
    """
    dm/dr = 4π r² ρ, A = 1 - 2m/r, stop if A<=eps or m/r >= 0.5 - eps.
    Returns dict with r, m, A, phi, characters.
    """

    def f(r, y):
        (m,) = y
        rh = float(rho_fn(r))
        return [4.0 * np.pi * r**2 * rh]

    def hit_horizon(r, y):
        m = y[0]
        # A = 1 - 2m/r
        return 1.0 - 2.0 * m / max(r, 1e-30) - 1e-8

    hit_horizon.terminal = True
    hit_horizon.direction = -1

    # start near 0 with m~0
    sol = solve_ivp(
        f,
        (r0, r_max),
        [0.0],
        method="RK45",
        rtol=1e-7,
        atol=1e-10,
        max_step=0.02,
        dense_output=True,
        events=[hit_horizon],
    )
    r_end = float(sol.t[-1])
    r = np.linspace(r0, r_end, n_out)
    m = sol.sol(r)[0]
    A = 1.0 - 2.0 * m / np.maximum(r, 1e-30)
    A = np.maximum(A, 1e-15)
    phi = -0.5 * np.log(A)
    hit = len(sol.t_events[0]) > 0 if sol.t_events else False
    # proper length
    ell = float(np.trapezoid(np.exp(phi), r))
    # low-z class: phi near r0
    # dphi/dr at start
    if len(r) > 5:
        dphi0 = (phi[5] - phi[0]) / (r[5] - r[0])
    else:
        dphi0 = np.nan
    return {
        "r": r,
        "m": m,
        "A": A,
        "phi": phi,
        "r_end": r_end,
        "m_end": float(m[-1]),
        "A_min": float(np.min(A)),
        "phi_max": float(np.max(phi)),
        "hit_A0": bool(hit or A[-1] < 1e-4),
        "ell": ell,
        "dphi0_est": float(dphi0),
        "success": bool(sol.success or hit),
    }


def characters(sol, name, params):
    r, phi, A = sol["r"], sol["phi"], sol["A"]
    # redshift from center-like: φ(0+)~φ[0], source at r
    # use φ - φ[0] if φ[0] small
    phi0 = float(phi[0])
    z = np.exp(phi - phi0) - 1.0
    dL = (1.0 + z) ** 2 * r
    # low-z: first points with z in (1e-3, 5e-2) if available
    low_z_class = "unknown"
    sel = (z > 1e-3) & (z < 5e-2)
    if sel.sum() > 10:
        # fit log dL vs log z
        coef = np.polyfit(np.log(z[sel]), np.log(np.maximum(dL[sel], 1e-30)), 1)
        p = float(coef[0])
        if p < 0.7:
            low_z_class = f"~z^{p:.2f} (soft/sqrt-like)"
        elif p < 1.3:
            low_z_class = f"~z^{p:.2f} (near-linear)"
        else:
            low_z_class = f"~z^{p:.2f} (steep)"
    elif sol["dphi0_est"] == sol["dphi0_est"]:
        # phi ~ a r^2 => dphi/dr ~ 2a r → 0 at center
        if abs(sol["dphi0_est"]) < 0.05:
            low_z_class = "phi'~0 near start → expect soft low-z if center"
        else:
            low_z_class = f"phi'~{sol['dphi0_est']:.3g} near start"

    return {
        "name": name,
        "params": params,
        "hit_A0": sol["hit_A0"],
        "r_end": sol["r_end"],
        "m_end": sol["m_end"],
        "A_min": sol["A_min"],
        "phi_max": sol["phi_max"],
        "z_max": float(np.max(z)),
        "ell": sol["ell"],
        "low_z_class": low_z_class,
        "compactness_end": float(2 * sol["m_end"] / sol["r_end"]) if sol["r_end"] > 0 else None,
        "ceiling_like": bool(sol["hit_A0"] and sol["r_end"] > 0.5),
    }


def main():
    print("=" * 70)
    print("S2 sourced MS solution-space (characters; no χ² in loop)")
    print("=" * 70)

    rows = []

    # --- probe families ---
    # 1) constant density
    print("\n--- const ρ ---")
    for rho0 in [0.01, 0.05, 0.1, 0.2, 0.5]:
        sol = integrate_ms(lambda r, rho0=rho0: rho0, r_max=30.0)
        ch = characters(sol, "const_rho", {"rho0": rho0})
        rows.append(ch)
        print(
            f"  ρ0={rho0:5.3f}  hit_A0={ch['hit_A0']}  r_end={ch['r_end']:.3f}  "
            f"z_max={ch['z_max']:.3f}  low_z={ch['low_z_class']}"
        )

    # 2) gaussian
    print("\n--- gaussian ρ=ρ0 exp(-(r/rc)^2) ---")
    for rc in [1.0, 2.0]:
        for rho0 in [0.1, 0.5, 1.0, 2.0, 5.0]:
            sol = integrate_ms(
                lambda r, rho0=rho0, rc=rc: rho0 * np.exp(-((r / rc) ** 2)),
                r_max=40.0,
            )
            ch = characters(sol, "gauss", {"rho0": rho0, "rc": rc})
            rows.append(ch)
            if ch["hit_A0"] or rho0 in (0.1, 1.0, 5.0):
                print(
                    f"  rc={rc} ρ0={rho0:5.2f}  hit_A0={ch['hit_A0']}  r_end={ch['r_end']:.3f}  "
                    f"z_max={ch['z_max']:.2f}  {ch['low_z_class']}"
                )

    # 3) ρ ∝ 1/r  (the A=1-r/X continuum) — analytic family
    print("\n--- ρ = k/(4π r)  (MS ⇒ m=k r²/2, A=1-k r) ---")
    # A=1-k r → zero at r=1/k. Matches A=1-r/X with X=1/k
    for k in [0.2, 0.5, 1.0]:
        # ρ = k/(4π r) so m' = 4π r² * k/(4π r) = k r ⇒ m = k r²/2
        sol = integrate_ms(lambda r, k=k: k / (4.0 * np.pi * max(r, 1e-6)), r_max=10.0)
        ch = characters(sol, "rho_1_over_r", {"k": k})
        rows.append(ch)
        print(
            f"  k={k:.2f}  hit_A0={ch['hit_A0']}  r_end={ch['r_end']:.3f}  "
            f"(expect ~{1/k:.3f})  z_max={ch['z_max']:.2f}  {ch['low_z_class']}"
        )

    # 4) ρ ∝ 1/r^2 soft
    print("\n--- ρ = k/(4π r^2) ---")
    for k in [0.1, 0.3, 0.5]:
        sol = integrate_ms(lambda r, k=k: k / (4.0 * np.pi * max(r, 1e-6) ** 2), r_max=20.0)
        ch = characters(sol, "rho_1_over_r2", {"k": k})
        rows.append(ch)
        print(
            f"  k={k:.2f}  hit_A0={ch['hit_A0']}  r_end={ch['r_end']:.3f}  "
            f"z_max={ch['z_max']:.2f}  {ch['low_z_class']}"
        )

    # summary counts
    n_hit = sum(1 for r in rows if r["hit_A0"])
    n_ceil = sum(1 for r in rows if r.get("ceiling_like"))
    print("\n" + "=" * 70)
    print(f"SUMMARY: {len(rows)} runs, hit_A0={n_hit}, ceiling_like={n_ceil}")
    print(
        """
  Characters that EMERGED:
  • Const ρ: can hit A=0 at finite r (critical ball) — low-z soft (regular center)
  • Gauss: high enough central density → A→0 at finite r_end
  • ρ∝1/r: hits A=0 at r=1/k (A=1-r/X family) — linear-type low-z (phi'≠0)
  • ρ∝1/r²: m∝r → A=1-2k constant shift — may not hit 0 if 2k<1

  Implication:
  • Outer A→0 at finite r APPEARS once continuum mass is enough (solver-first: source on)
  • Regular-center fills give soft low-z under full light readout
  • 1/r continuum reproduces sphere-ceiling linear lapse as a MS solution — not invented A(r)
"""
    )

    # Optional residual demo AFTER (not in solve)
    print("--- optional residual DEMO (after inventory; not selector) ---")
    try:
        from scipy.linalg import cho_factor, cho_solve

        d = np.genfromtxt(ROOT / "Data" / "Pantheon+SH0ES.dat", names=True, dtype=None, encoding=None)
        mask = (d["IS_CALIBRATOR"].astype(int) == 0) & (d["zHD"] > 0.01)
        idx = np.where(mask)[0]
        zobs = np.asarray(d["zHD"][mask], float)
        mobs = np.asarray(d["m_b_corr"][mask], float)
        with open(ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov") as f:
            N = int(f.readline())
        C = np.loadtxt(ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov", skiprows=1).reshape(N, N)
        C = 0.5 * (C + C.T)
        C = C[np.ix_(idx, idx)]
        cf = cho_factor(C, lower=True, check_finite=False)

        def score_from_sol(sol, label):
            r, phi = sol["r"], sol["phi"]
            phi0 = float(phi[0])
            # map z_obs → r by invert z(r)=exp(phi-phi0)-1
            z_path = np.exp(phi - phi0) - 1.0
            # require increasing
            if not np.all(np.diff(z_path) >= -1e-12):
                z_path = np.maximum.accumulate(z_path)
            if z_path[-1] < zobs.max():
                print(f"  [{label:40s}] incomplete z coverage z_max={z_path[-1]:.3f}")
                return None
            r_at = np.interp(zobs, z_path, r)
            dL = (1.0 + zobs) ** 2 * r_at
            # shape only
            mu = 5 * np.log10(np.maximum(dL / dL[0] if dL[0] > 0 else dL, 1e-30))
            # better: free scale via offset on 5log10(dL)
            mu = 5 * np.log10(np.maximum(dL, 1e-30))
            dv = mobs - mu
            ones = np.ones_like(dv)
            O = float((ones @ cho_solve(cf, dv)) / (ones @ cho_solve(cf, ones)))
            res = dv - O
            chi2 = float(res @ cho_solve(cf, res))
            dof = len(zobs) - 1
            print(f"  [{label:40s}] chi2/dof={chi2/dof:.4f} RMS={np.sqrt(np.mean(res**2)):.4f}")
            return chi2 / dof

        # analytic A=1-r/X from rho 1/r
        score_from_sol(
            integrate_ms(lambda r: 1.0 / (4.0 * np.pi * max(r, 1e-8)), r_max=5.0),
            "DEMO MS ρ∝1/r → A=1-r/X",
        )
        # critical const dens: rho such that R_crit with A(R)=0: (8π/3)ρ R^2=1
        # integrate until hit — pick rho0 so r_end ~ few
        score_from_sol(
            integrate_ms(lambda r: 0.05, r_max=30.0),
            "DEMO MS const ρ=0.05",
        )
        # gauss that hits
        score_from_sol(
            integrate_ms(lambda r: 2.0 * np.exp(-(r**2)), r_max=20.0),
            "DEMO MS gauss ρ0=2 rc=1",
        )
    except Exception as e:
        print("  residual demo skipped:", e)

    out = {
        "n_runs": len(rows),
        "n_hit_A0": n_hit,
        "rows": rows,
        "implication": "outer A→0 emerges with enough continuum mass; vacuum lacked it",
    }
    path = ROOT / "simple_metric_S2_sourced_space_out.json"

    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items()}
        if isinstance(o, list):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, float)):
            return float(o)
        if isinstance(o, (np.bool_, bool)):
            return bool(o)
        if isinstance(o, (np.integer, int)):
            return int(o)
        return o

    path.write_text(json.dumps(clean(out), indent=2))
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
