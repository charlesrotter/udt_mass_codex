#!/usr/bin/env python3
"""
HUNT (free D_A unquarantined for this tile only) — low-z asymptotics.

Question: with free D_A + Path-B-style EL + dilated dust, can we get
  d_L ~ z   (linear Hubble)
at low z under true n=2  d_L = (1+z)^2 D_A,  1+z = e^φ,
with a regular center?

Structural expectation (pre-registered):
  Regular center: D_A ~ r (odd), φ ~ a r^2 (even) near r=0
  => z ~ a r^2, d_L ~ D_A ~ r ~ sqrt(z)   SAME sqrt problem as D_A=r
  Free D_A alone does NOT evade that parity unless φ'(0)≠0 or D_A'(0)=0.

OBSERVE: integrate Path B + dilated dust; measure effective power
  d_L ∝ z^p  in a low-z window; report p, and φ/D series coefficients.

No SNe tuning of free functions. Full-cov score only as optional demo on a
few solutions that cover z.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.stats import linregress

ROOT = Path(__file__).resolve().parent
Z = 1.0


def rho_gauss(r, rho0, rc):
    return rho0 * np.exp(-((r / max(rc, 1e-12)) ** 2))


def make_rhs(rho0, rc, dilated=True):
    """Path B + dust (from macro_pathB_dilated_dust_observe.py)."""

    def f(r, y):
        D, S, phi, Q = y
        De = max(float(D), 1e-14)
        rh = float(rho_gauss(r, rho0, rc))
        e2 = np.exp(np.clip(2.0 * phi, -40, 40))
        em2 = np.exp(np.clip(-2.0 * phi, -40, 40))
        A11 = 4.0 * De * em2
        A12 = -Z * De * De
        A21 = -4.0
        A22 = 4.0 * De
        if dilated:
            b1 = 2.0 * Z * De * S * Q - 2.0 * De * De * rh * em2
            b2 = -Z * De * e2 * Q * Q + 8.0 * De * Q * Q - 8.0 * S * Q + 2.0 * De * rh
        else:
            b1 = 2.0 * Z * De * S * Q
            b2 = (
                -Z * De * e2 * Q * Q
                + 2.0 * De * rh * e2
                + 8.0 * De * Q * Q
                - 8.0 * S * Q
            )
        det = A11 * A22 - A12 * A21
        if abs(det) < 1e-30:
            return [S, 0.0, Q, 0.0]
        Sp = (b1 * A22 - A12 * b2) / det
        Qp = (A11 * b2 - b1 * A21) / det
        Sp = float(np.clip(Sp if np.isfinite(Sp) else 0.0, -1e6, 1e6))
        Qp = float(np.clip(Qp if np.isfinite(Qp) else 0.0, -1e6, 1e6))
        return [S, Sp, Q, Qp]

    return f


def integrate(rho0, rc, Q0=0.0, r_max=25.0, dilated=True):
    """
    IC near center: D=r_eps, S=1 (areal-like), phi=0, Q=Q0.
    Q0=0 is regular-ish; Q0≠0 probes φ'(0)≠0 (irregular).
    """
    r0 = 1e-3
    y0 = [r0, 1.0, 0.0, Q0]
    f = make_rhs(rho0, rc, dilated=dilated)

    def hit_floor(r, y):
        return y[0] - 1e-4

    hit_floor.terminal = True
    hit_floor.direction = -1

    sol = solve_ivp(
        f,
        (r0, r_max),
        y0,
        method="RK45",
        rtol=1e-7,
        atol=1e-9,
        max_step=0.03,
        dense_output=True,
        events=[hit_floor],
    )
    if sol.t[-1] <= r0 * 2:
        return None
    r = np.linspace(r0, sol.t[-1], 1200)
    try:
        Y = sol.sol(r)
    except Exception:
        return None
    D, S, phi, Q = Y
    if not np.all(np.isfinite(D)) or np.any(D <= 0):
        return None
    return {"r": r, "D": D, "S": S, "phi": phi, "Q": Q, "r_end": float(r[-1])}


def lowz_power(r, D, phi, z_lo=1e-3, z_hi=5e-2):
    """
    Fit log d_L vs log z in a low-z window -> effective power p in d_L ∝ z^p.
    Linear Hubble => p≈1.  sqrt law => p≈0.5.
    """
    z = np.exp(phi) - 1.0
    dL = np.exp(2.0 * phi) * D
    m = (z >= z_lo) & (z <= z_hi) & np.isfinite(dL) & (dL > 0) & (z > 0)
    if m.sum() < 8:
        # try wider if phi small
        m = (z >= z_lo) & (z <= max(z_hi, 0.2)) & np.isfinite(dL) & (dL > 0)
    if m.sum() < 8:
        return None
    lz, ld = np.log(z[m]), np.log(dL[m])
    reg = linregress(lz, ld)
    return {
        "p": float(reg.slope),
        "intercept": float(reg.intercept),
        "rvalue": float(reg.rvalue),
        "n": int(m.sum()),
        "z_lo": float(z[m].min()),
        "z_hi": float(z[m].max()),
        "dL_over_z_mean": float(np.mean(dL[m] / z[m])),
        "dL_over_sqrtz_mean": float(np.mean(dL[m] / np.sqrt(z[m]))),
    }


def series_coeffs(r, D, phi, Q):
    """Crude near-origin coefficients from first points."""
    # D ≈ d1 r + d3 r^3; phi ≈ a r^2
    i = min(30, len(r) - 1)
    rr, DD, pp, QQ = r[:i], D[:i], phi[:i], Q[:i]
    # phi / r^2
    a_est = float(np.median(pp[5:] / rr[5:] ** 2)) if np.all(rr[5:] > 0) else float("nan")
    d1_est = float(np.median(DD[5:] / rr[5:]))
    Q0_est = float(QQ[0])
    return {"a_phi_r2": a_est, "D_over_r": d1_est, "Q_at_start": Q0_est}


def main():
    print("=" * 70)
    print("FREE D_A HUNT — low-z power of d_L=(1+z)^2 D_A")
    print("Unquarantined for this hunt only (Charles 2026-07-09)")
    print("=" * 70)

    rows = []
    # Q0=0 regular-ish; also small Q0 probes
    for dilated in (True, False):
        for Q0 in (0.0, 0.05, 0.2):
            for rc in (1.0, 2.0):
                for rho0 in np.geomspace(0.05, 20.0, 10):
                    sol = integrate(rho0, rc, Q0=Q0, dilated=dilated)
                    if sol is None:
                        continue
                    powr = lowz_power(sol["r"], sol["D"], sol["phi"])
                    ser = series_coeffs(sol["r"], sol["D"], sol["phi"], sol["Q"])
                    z = np.exp(sol["phi"]) - 1.0
                    row = {
                        "dilated": dilated,
                        "Q0": Q0,
                        "rc": rc,
                        "rho0": float(rho0),
                        "phi_max": float(np.nanmax(sol["phi"])),
                        "z_max": float(np.nanmax(z)),
                        "D_max": float(np.nanmax(sol["D"])),
                        "series": ser,
                        "lowz": powr,
                    }
                    rows.append(row)

    # summarize powers
    def collect(pred):
        ps = [
            r["lowz"]["p"]
            for r in rows
            if r["lowz"] is not None and pred(r) and np.isfinite(r["lowz"]["p"])
        ]
        return ps

    print("\n--- low-z effective power p in d_L ∝ z^p ---")
    for label, pred in [
        ("dilated Q0=0", lambda r: r["dilated"] and r["Q0"] == 0),
        ("dilated Q0>0", lambda r: r["dilated"] and r["Q0"] > 0),
        ("phi-blind Q0=0", lambda r: (not r["dilated"]) and r["Q0"] == 0),
        ("phi-blind Q0>0", lambda r: (not r["dilated"]) and r["Q0"] > 0),
        ("ALL with lowz", lambda r: True),
    ]:
        ps = collect(pred)
        if not ps:
            print(f"  {label:20s}  n=0")
            continue
        print(
            f"  {label:20s}  n={len(ps):3d}  p median={np.median(ps):.3f}  "
            f"p range=[{np.min(ps):.3f},{np.max(ps):.3f}]"
        )

    # show a few explicit examples
    print("\n--- examples (dilated, Q0=0) ---")
    ex = [r for r in rows if r["dilated"] and r["Q0"] == 0 and r["lowz"]]
    ex = sorted(ex, key=lambda r: r["rho0"])[:6] + sorted(ex, key=lambda r: -r["phi_max"])[:3]
    seen = set()
    for r in ex:
        key = (r["rc"], r["rho0"])
        if key in seen:
            continue
        seen.add(key)
        p = r["lowz"]["p"] if r["lowz"] else None
        print(
            f"  rc={r['rc']} rho0={r['rho0']:.3g}  phi_max={r['phi_max']:.3f}  "
            f"z_max={r['z_max']:.3f}  p={p}  D/r~{r['series']['D_over_r']:.3f}  "
            f"a=phi/r^2~{r['series']['a_phi_r2']:.3g}"
        )

    print("\n--- examples (dilated, Q0=0.2 irregular launch) ---")
    for r in [x for x in rows if x["dilated"] and x["Q0"] == 0.2 and x["lowz"]][:8]:
        p = r["lowz"]["p"]
        print(
            f"  rc={r['rc']} rho0={r['rho0']:.3g}  phi_max={r['phi_max']:.3f}  "
            f"p={p:.3f}  Q_start={r['series']['Q_at_start']:.3f}"
        )

    # Analytic parity note printed
    print("\n--- STRUCTURAL (pre-registered) ---")
    print("  Regular: D~r, phi~a r^2 => d_L~r, z~a r^2 => d_L ~ z^{1/2}")
    print("  Target linear Hubble: p=1.  sqrt law: p=0.5")
    print("  Free D_A does not change the parity of a smooth center.")

    # Optional: freeze D=r (S=1 forced) is simple metric — already done elsewhere
    out = {
        "hunt": "free_DA_lowz",
        "unquarantine": "Charles 2026-07-09 scoped",
        "n_rows": len(rows),
        "summary_p": {},
        "rows_sample": rows[:: max(1, len(rows) // 40)],
    }
    for label, pred in [
        ("dilated_Q0_0", lambda r: r["dilated"] and r["Q0"] == 0),
        ("dilated_Q0_pos", lambda r: r["dilated"] and r["Q0"] > 0),
        ("blind_Q0_0", lambda r: (not r["dilated"]) and r["Q0"] == 0),
    ]:
        ps = collect(pred)
        if ps:
            out["summary_p"][label] = {
                "n": len(ps),
                "p_median": float(np.median(ps)),
                "p_min": float(np.min(ps)),
                "p_max": float(np.max(ps)),
            }

    # full list of p for dilated Q0=0
    out["all_p_dilated_Q0_0"] = [
        {
            "rho0": r["rho0"],
            "rc": r["rc"],
            "p": r["lowz"]["p"],
            "phi_max": r["phi_max"],
            "z_max": r["z_max"],
        }
        for r in rows
        if r["dilated"] and r["Q0"] == 0 and r["lowz"]
    ]

    path = ROOT / "simple_metric_freeDA_lowz_observe_out.json"
    path.write_text(json.dumps(out, indent=2, default=float))
    print(f"\nWrote {path}  (N rows={len(rows)})")


if __name__ == "__main__":
    main()
