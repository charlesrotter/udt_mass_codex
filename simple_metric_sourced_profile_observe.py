#!/usr/bin/env python3
"""
OBSERVE — sourced φ profiles on the SIMPLE metric only (D_A = r fixed).

Upstream #1 (simple_metric_root_upstream_MAP.md): what r(z) / d_L emerges
under true optics d_L = r (1+z)^2, from φ solved with a matter probe.

Held:
  ds^2 = -e^{-2φ} c^2 dt^2 + e^{2φ} dr^2 + r^2 dΩ^2
  1+z = e^φ (observer φ=0 at r=0)
  D_A = r  (native, chart origin)
  d_L = r (1+z)^2   (n=2)

Operator fork used here (SIMPLE_METRIC_MACRO.md):
  Compensated geometric W=e^{2φ} + dilated dust L_m = -ρ r^2 e^{-2φ}
    =>  (r^2 φ')' = (2/Z) ρ r^2 e^{-2φ}
  Uncompensated vacuum (r^2 φ')' = (4/Z) e^{-2φ} is NOT regular at origin
  (included only as a note / failed regular launch).

ρ = FREE probe profiles (gauss / tophat amount+width) — NOT fundamental matter.
Z = 1 CHOSE units. No SNe tuning of shape params. Characterize; optional
shape score vs Pantheon is DEMO of residual, not a fit campaign.

Also report hyperbolic J1 and locked-cubic as FIXED comparison shapes (not solved).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import cho_factor, cho_solve

ROOT = Path(__file__).resolve().parent
Z_PHI = 1.0  # CHOSE units


def rho_gauss(r, rho0, rc):
    return rho0 * np.exp(-((r / max(rc, 1e-12)) ** 2))


def rho_tophat(r, rho0, rc, soft=0.08):
    return rho0 / (1.0 + np.exp((r - rc) / (soft * rc + 1e-12)))


def integrate_compensated_dust(rho0, rc, profile="gauss", r_max=30.0, n_eval=800):
    """
    Q = φ',  Q' = (2/Z) ρ e^{-2φ} - 2Q/r
    IC: φ(0)=0, Q(0)=0; series start at r_eps.
    """

    def rho_of(r):
        if profile == "gauss":
            return rho_gauss(r, rho0, rc)
        return rho_tophat(r, rho0, rc)

    # series at small r: φ ≈ a r^2, a = ρ(0)/(3Z)
    r0 = 1e-4
    a = rho_of(0.0) / (3.0 * Z_PHI)
    y0 = [a * r0 * r0, 2.0 * a * r0]  # phi, Q

    def f(r, y):
        phi, Q = y
        rh = rho_of(r)
        em2 = np.exp(np.clip(-2.0 * phi, -40, 40))
        # regularized 2Q/r
        Qp = (2.0 / Z_PHI) * rh * em2 - 2.0 * Q / max(r, 1e-14)
        if not np.isfinite(Qp):
            Qp = 0.0
        return [Q, Qp]

    sol = solve_ivp(
        f,
        (r0, r_max),
        y0,
        method="RK45",
        rtol=1e-8,
        atol=1e-10,
        dense_output=True,
        max_step=0.05,
    )
    if not sol.success:
        return None
    r = np.linspace(r0, min(sol.t[-1], r_max), n_eval)
    y = sol.sol(r)
    phi, Q = y[0], y[1]
    # mass proxy M = ∫ 4π r^2 ρ dr (probe units)
    dens = 4.0 * np.pi * r**2 * np.array([rho_of(ri) for ri in r])
    M = float(np.trapezoid(dens, r))
    return {
        "r": r,
        "phi": phi,
        "Q": Q,
        "M": M,
        "phi_max": float(np.max(phi)),
        "rho0": rho0,
        "rc": rc,
        "profile": profile,
        "r_end": float(r[-1]),
        "ok": bool(sol.success and np.all(np.isfinite(phi))),
    }


def integrate_MS_uniform(rho0, R_ball, n_eval=800):
    """
    Geometric MS continuum on simple metric (GR-form MS as geometric identity):
      m' = 4π r^2 ρ,  A = 1 - 2m/r  (G=c=1 units),  φ = -0.5 ln A for A>0.
    Uniform ball ρ=ρ0 for r<R, 0 outside; exterior Schwarzschild.
    CHARACTERIZE only — Category-A / geometric reference on this metric.
    """
    # interior: m = (4π/3) ρ r^3, A = 1 - (8π/3) ρ r^2
    # need A>0 in interior: (8π/3)ρ R^2 < 1
    crit = (8.0 * np.pi / 3.0) * rho0 * R_ball**2
    if crit >= 0.999:
        return None  # trapped / horizon inside ball
    r = np.linspace(1e-4, R_ball * 3.0, n_eval)
    m = np.where(
        r <= R_ball,
        (4.0 * np.pi / 3.0) * rho0 * r**3,
        (4.0 * np.pi / 3.0) * rho0 * R_ball**3,
    )
    A = 1.0 - 2.0 * m / np.maximum(r, 1e-14)
    if np.any(A <= 1e-12):
        return None
    phi = -0.5 * np.log(A)
    # shift so φ(0)=0: interior A(0)=1 => φ(0)=0 already
    return {
        "r": r,
        "phi": phi,
        "M": float(m[-1]),
        "phi_max": float(np.max(phi)),
        "rho0": rho0,
        "rc": R_ball,
        "profile": "MS_uniform",
        "r_end": float(r[-1]),
        "compactness": float(2.0 * m[r <= R_ball][-1] / R_ball),
        "ok": True,
    }


def r_of_z_from_profile(r, phi, z_query):
    """Invert 1+z = e^φ for r(z); φ must be increasing."""
    one_plus = np.exp(phi)
    # require monotonic
    if not np.all(np.diff(one_plus) >= -1e-12):
        # allow tiny noise; use cumulative max
        one_plus = np.maximum.accumulate(one_plus)
    z_prof = one_plus - 1.0
    z_max = float(z_prof[-1])
    out = np.full_like(z_query, np.nan, dtype=float)
    mask = (z_query >= z_prof[0]) & (z_query <= z_max * 0.999)
    if mask.any():
        out[mask] = np.interp(z_query[mask], z_prof, r)
    return out, z_max


def dL_n2(r, z):
    return r * (1.0 + z) ** 2


def dL_hyp_over_X(z):
    ez = 1.0 + z
    return (ez**2) * (ez**2 - 1.0) / (ez**2 + 1.0)


def locked_cubic_r_of_z(z, mu_g=0.2473):
    def phi_c(rr):
        return (
            1.5 * mu_g * rr
            - np.cos(np.pi / 5) * mu_g**2 * rr**2
            + (2.0 / 3.0) * mu_g**3 * rr**3
        )

    out = np.empty_like(z, float)
    for i, zi in enumerate(z):
        lo, hi = 0.0, 80.0
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            if np.exp(phi_c(mid)) - 1.0 < zi:
                lo = mid
            else:
                hi = mid
        out[i] = 0.5 * (lo + hi)
    return out


def dL_lcdm(z, Om=0.3):
    z = np.atleast_1d(z)
    out = np.empty_like(z, float)
    for i, zi in enumerate(z):
        g = np.linspace(0.0, float(zi), 1024)
        E = np.sqrt(Om * (1 + g) ** 3 + (1 - Om))
        out[i] = (1 + zi) * np.trapezoid(1.0 / E, g)
    return out


def load_pantheon():
    dat = ROOT / "Data" / "Pantheon+SH0ES.dat"
    covp = ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov"
    if not dat.is_file():
        return None
    d = np.genfromtxt(dat, names=True, dtype=None, encoding=None)
    mask = (d["IS_CALIBRATOR"].astype(int) == 0) & (d["zHD"] > 0.01)
    idx = np.where(mask)[0]
    z = np.asarray(d["zHD"][mask], float)
    m = np.asarray(d["m_b_corr"][mask], float)
    if not covp.is_file():
        s = np.asarray(d["m_b_corr_err_DIAG"][mask], float)
        return {"z": z, "m": m, "mode": "diag", "w": 1.0 / s**2, "cf": None}
    with open(covp) as f:
        Nall = int(f.readline())
    C = np.loadtxt(covp, skiprows=1).reshape(Nall, Nall)
    C = 0.5 * (C + C.T)
    C = C[np.ix_(idx, idx)]
    cf = cho_factor(C, lower=True, check_finite=False)
    return {"z": z, "m": m, "mode": "full", "cf": cf, "w": None}


def score_shape(dL, pan):
    """One offset only; shape demo."""
    z, m = pan["z"], pan["m"]
    mu = 5.0 * np.log10(np.maximum(dL, 1e-30))
    dv = m - mu
    if pan["mode"] == "full":
        cf = pan["cf"]
        ones = np.ones_like(dv)
        O = float((ones @ cho_solve(cf, dv)) / (ones @ cho_solve(cf, ones)))
        res = dv - O
        chi2 = float(res @ cho_solve(cf, res))
    else:
        w = pan["w"]
        O = float(np.sum(w * dv) / np.sum(w))
        res = dv - O
        chi2 = float(np.sum(w * res**2))
    dof = len(z) - 1
    rms = float(np.sqrt(np.mean(res**2)))
    return {"chi2_dof": chi2 / dof, "rms": rms, "chi2": chi2, "offset": O}


def shape_ratio_grid(dL_fun, z_grid=None):
    if z_grid is None:
        z_grid = np.array([0.05, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0])
    L = dL_lcdm(z_grid)
    H = np.array([dL_fun(z) for z in z_grid], float)
    # normalize at z=0.05
    Hn = H / H[0]
    Ln = L / L[0]
    ratio = Hn / Ln
    return [
        {"z": float(z), "ratio_to_LCDM": float(r), "dmu": float(5 * np.log10(r))}
        for z, r in zip(z_grid, ratio)
    ]


def main():
    print("=" * 70)
    print("OBSERVE: simple-metric sourced φ → r(z) → d_L = r(1+z)^2")
    print("Compensated + dilated dust probe; MS uniform reference")
    print("=" * 70)

    pan = load_pantheon()
    results = {"profiles": [], "comparisons": {}, "premise": {
        "metric": "simple D_A=r",
        "optics": "d_L=r(1+z)^2",
        "operator": "compensated + dilated dust (FREE rho probe)",
        "Z": Z_PHI,
        "not": "free D_A, SNe-tuned cubic, fundamental matter claim",
    }}

    # --- scan compensated dust ---
    scan = []
    for profile in ("gauss", "tophat"):
        for rc in (1.0, 2.0, 5.0):
            for rho0 in np.geomspace(0.01, 50.0, 16):
                sol = integrate_compensated_dust(rho0, rc, profile=profile, r_max=40.0)
                if sol is None or not sol["ok"]:
                    continue
                z_grid = np.array([0.05, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0])
                r_at_z, z_max = r_of_z_from_profile(sol["r"], sol["phi"], z_grid)
                row = {
                    "profile": profile,
                    "rho0": float(rho0),
                    "rc": float(rc),
                    "M": sol["M"],
                    "phi_max": sol["phi_max"],
                    "z_max": float(z_max),
                    "reaches_z2": bool(z_max >= 2.0),
                    "r_at_z": {
                        f"{z:.2f}": (None if not np.isfinite(r) else float(r))
                        for z, r in zip(z_grid, r_at_z)
                    },
                }
                # low-z slope: d_L ~ r z^0 ... d_L/z at small z ≈ r/(z/(1+z)...) 
                # φ ~ a r^2 near 0 for compensated dust → 1+z ~ 1+a r^2, not linear in r
                # characterize dL shape if z_max sufficient
                if z_max >= 0.5 and pan is not None:
                    zq = pan["z"]
                    rq, _ = r_of_z_from_profile(sol["r"], sol["phi"], zq)
                    if np.isfinite(rq).sum() > 0.9 * len(zq):
                        # only score if covers almost all SNe z
                        dL = dL_n2(rq, zq)
                        if np.all(np.isfinite(dL)) and np.all(dL > 0):
                            sc = score_shape(dL, pan)
                            row["sne_demo"] = sc
                scan.append(row)
                if sol["phi_max"] > 0.05:
                    print(
                        f"  {profile:6s} rc={rc:.1f} rho0={rho0:8.3g}  "
                        f"M={sol['M']:8.3g}  phi_max={sol['phi_max']:.3f}  "
                        f"z_max={z_max:.3f}"
                        + (
                            f"  chi2/dof={row['sne_demo']['chi2_dof']:.3f}"
                            if "sne_demo" in row
                            else ""
                        )
                    )

    results["profiles"] = scan

    # best by phi_max / z coverage among those with sne_demo
    scored = [s for s in scan if "sne_demo" in s]
    if scored:
        best = min(scored, key=lambda s: s["sne_demo"]["chi2_dof"])
        worst = max(scored, key=lambda s: s["sne_demo"]["chi2_dof"])
        print("\n--- among FULL z-coverage dust probes (demo scores) ---")
        print(
            f"  best  chi2/dof={best['sne_demo']['chi2_dof']:.4f}  "
            f"RMS={best['sne_demo']['rms']:.4f}  {best['profile']} rc={best['rc']} rho0={best['rho0']:.4g}"
        )
        print(
            f"  worst chi2/dof={worst['sne_demo']['chi2_dof']:.4f}  "
            f"RMS={worst['sne_demo']['rms']:.4f}"
        )
        results["best_dust_demo"] = best
        results["n_scored"] = len(scored)
    else:
        print("\n--- no dust probe covered full Pantheon z (z_max too small or invert fail) ---")
        results["best_dust_demo"] = None
        results["n_scored"] = 0

    # z_max distribution
    zm = [s["z_max"] for s in scan]
    pm = [s["phi_max"] for s in scan]
    print(f"\n  scan N={len(scan)}  phi_max range [{min(pm):.3f},{max(pm):.3f}]  "
          f"z_max range [{min(zm):.3f},{max(zm):.3f}]")
    print(f"  reaches z>=2: {sum(1 for s in scan if s['reaches_z2'])} / {len(scan)}")

    # --- MS uniform reference (few points) ---
    print("\n--- MS uniform ball (geometric A=1-2m/r) ---")
    ms_rows = []
    for R in (1.0, 2.0, 5.0):
        for comp in (0.1, 0.3, 0.5, 0.8, 0.95):
            # compactness C = 2M/R = (8π/3) ρ R^2  => ρ = C / ((8π/3) R^2)
            rho0 = comp / ((8.0 * np.pi / 3.0) * R**2)
            sol = integrate_MS_uniform(rho0, R)
            if sol is None:
                print(f"  R={R} C={comp}: horizon/fail")
                continue
            z_grid = np.array([0.05, 0.1, 0.3, 0.5, 1.0])
            r_at_z, z_max = r_of_z_from_profile(sol["r"], sol["phi"], z_grid)
            print(
                f"  R={R} C={comp:.2f}  phi_max={sol['phi_max']:.3f}  z_max={z_max:.3f}  "
                f"M={sol['M']:.4g}"
            )
            ms_rows.append(
                {
                    "R": R,
                    "compactness": comp,
                    "phi_max": sol["phi_max"],
                    "z_max": float(z_max),
                    "M": sol["M"],
                }
            )
    results["MS_uniform"] = ms_rows

    # --- fixed comparisons on Pantheon ---
    if pan is not None:
        print("\n--- FIXED shape comparisons (true n=2 or historical) ---")
        z = pan["z"]
        # hyp n=2 shape
        sc_hyp = score_shape(dL_hyp_over_X(z), pan)
        print(f"  hyp J1 n=2:     chi2/dof={sc_hyp['chi2_dof']:.4f}  RMS={sc_hyp['rms']:.4f}")
        # cubic n=2
        rcub = locked_cubic_r_of_z(z)
        sc_c2 = score_shape(dL_n2(rcub, z), pan)
        print(f"  cubic n=2:      chi2/dof={sc_c2['chi2_dof']:.4f}  RMS={sc_c2['rms']:.4f}")
        sc_c1 = score_shape(rcub * (1 + z), pan)
        print(f"  cubic n=1 old:  chi2/dof={sc_c1['chi2_dof']:.4f}  RMS={sc_c1['rms']:.4f}")
        sc_L = score_shape(dL_lcdm(z), pan)
        print(f"  LCDM Om=0.3:    chi2/dof={sc_L['chi2_dof']:.4f}  RMS={sc_L['rms']:.4f}")
        results["comparisons"] = {
            "hyp_n2": sc_hyp,
            "cubic_n2": sc_c2,
            "cubic_n1": sc_c1,
            "lcdm": sc_L,
        }

    # --- structural note: near-origin of compensated dust ---
    # φ ~ a r^2 => 1+z ~ exp(a r^2) => at low z, z ~ a r^2 => r ~ sqrt(z/a)
    # d_L = r (1+z)^2 ~ sqrt(z)  — WRONG low-z Hubble (should be d_L ~ z)
    print("\n--- STRUCTURE: compensated dust near origin ---")
    print("  φ ≈ a r²  (a=ρ0/(3Z))  =>  z ≈ a r² at low z  =>  r ~ sqrt(z/a)")
    print("  d_L = r(1+z)² ~ sqrt(z)  — NOT linear in z (bad low-z distance law)")
    print("  Cubic had φ~k r linear leading term (irregular origin) to get z~k r.")
    results["structure_note"] = {
        "compensated_dust_low_z": "d_L ~ sqrt(z) — fails linear Hubble",
        "needs_for_linear_low_z": "φ'(0)≠0 or φ~k r leading (conflicts regular origin)",
    }

    # thin J1 reminder
    results["J1_thin"] = {
        "statement": "D_A=r forced at chart origin; hyp x=X tanh φ is compositional",
        "J1": "r≡x is CHOSE join; not required by D_A=r alone",
        "if_not_J1": "need derived r(x); not free D_A(r)",
    }

    outp = ROOT / "simple_metric_sourced_profile_observe_out.json"
    # trim r arrays from profiles if any
    outp.write_text(json.dumps(results, indent=2, default=float))
    print(f"\nWrote {outp}")
    return results


if __name__ == "__main__":
    main()
