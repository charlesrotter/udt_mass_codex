#!/usr/bin/env python3
"""
P1 free-D, W=1 vacuum — asymptotics for elegant macro test.

  (Z D^2 phi')' = 4 e^{-2 phi} (D')^2
  (e^{-2 phi} D')' = -(Z/4) D (phi')^2

  G = D^2 phi',  F = e^{-2 phi} D'
  G' = (4/Z) e^{-2 phi} (D')^2 >= 0
  F' = -(Z/4) D (phi')^2 <= 0

Question: any class with phi increasing outward AND hard barrier
(ell or null converge / finite-r end with z->oo), without inventing terms?
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
from scipy.integrate import solve_ivp, trapezoid

PREMISES = {
    "packaging": "P1 vacuum W=1 free D",
    "mode": "OBSERVE asymptotics",
    "frame": "elegant macro: redshift out + barrier",
}


def rhs(r, y, Z):
    phi, u, D, v = y
    D = max(float(D), 1e-14)
    em2 = np.exp(-2.0 * np.clip(phi, -40, 40))
    ep2 = np.exp(2.0 * np.clip(phi, -40, 40))
    # u' from (Z D^2 u)' = 4 em2 v^2
    up = (4.0 / Z) * em2 * (v / D) ** 2 - 2.0 * (v / D) * u
    # F = em2 v; F' = -(Z/4) D u^2
    Fp = -(Z / 4.0) * D * u**2
    vp = 2.0 * u * v + ep2 * Fp
    return [u, up, v, vp]


@dataclass
class Run:
    tag: str
    Z: float
    r0: float
    y0: list
    status: str
    r_end: float
    phi_end: float
    D_end: float
    u_end: float
    v_end: float
    phi_min: float
    phi_max: float
    D_min: float
    ell: float
    null_u: float
    G0: float
    G_end: float
    F0: float
    F_end: float
    notes: str


def run_ivp(
    tag: str,
    y0: list,
    r0: float = 1.0,
    r_max: float = 80.0,
    Z: float = 1.0,
) -> Run:
    phi0, u0, D0, v0 = y0
    G0 = D0**2 * u0
    F0 = np.exp(-2 * phi0) * v0

    def hit_D(r, y):
        return y[2] - 1e-8

    hit_D.terminal = True
    hit_D.direction = -1

    def hit_phi(r, y):
        return 25.0 - abs(y[0])

    hit_phi.terminal = True
    hit_phi.direction = -1

    sol = solve_ivp(
        lambda r, y: rhs(r, y, Z),
        (r0, r_max),
        y0,
        method="DOP853",
        rtol=1e-8,
        atol=1e-10,
        events=(hit_D, hit_phi),
        max_step=0.05,
        dense_output=True,
    )
    pinched = bool(sol.t_events and len(sol.t_events[0]) > 0)
    phi_cap = bool(sol.t_events and len(sol.t_events[1]) > 0)
    if sol.success:
        status = "ok"
    elif pinched:
        status = "pinch_D"
    elif phi_cap:
        status = "phi_cap"
    else:
        status = "stopped"

    r = sol.t
    phi, u, D, v = sol.y
    ep = np.exp(np.clip(phi, -40, 40))
    ell = float(trapezoid(ep, r)) if len(r) > 1 else 0.0
    null_u = float(trapezoid(ep**2, r)) if len(r) > 1 else 0.0
    G_end = float(D[-1] ** 2 * u[-1])
    F_end = float(np.exp(-2 * phi[-1]) * v[-1])

    notes = []
    if phi[-1] > phi[0] + 0.05:
        notes.append("phi_up")
    elif phi[-1] < phi[0] - 0.05:
        notes.append("phi_down")
    if status == "pinch_D":
        notes.append("FINITE_R_END")
        if phi[-1] > phi[0]:
            notes.append("redshift_out_to_pinch")
    if status == "ok":
        if D[-1] > D[0] * 1.2:
            notes.append("D_grew")
        if abs(u[-1]) < 1e-3 and phi[-1] > 1:
            notes.append("phi_flat_high")
        # ell growth proxy: if ok to r_max, likely open
        notes.append("open_to_rmax")

    return Run(
        tag=tag,
        Z=Z,
        r0=r0,
        y0=list(map(float, y0)),
        status=status,
        r_end=float(r[-1]),
        phi_end=float(phi[-1]),
        D_end=float(D[-1]),
        u_end=float(u[-1]),
        v_end=float(v[-1]),
        phi_min=float(np.min(phi)),
        phi_max=float(np.max(phi)),
        D_min=float(np.min(D)),
        ell=ell,
        null_u=null_u,
        G0=float(G0),
        G_end=G_end,
        F0=float(F0),
        F_end=F_end,
        notes="; ".join(notes),
    )


def analytic_notes() -> dict:
    return {
        "G_mono": "G=D^2 phi' nondecreasing (G'>=0); phi-gradient charge only grows",
        "F_mono": "F=e^{-2phi} D' nonincreasing (F'<=0)",
        "phi_up_needs_G_gt_0": "for D>0, phi'>0 iff G>0",
        "barrier_with_phi_to_plus_infty_at_infty": (
            "ell=int e^phi dr: if phi->+oo as r->oo, e^phi grows — typically ell DIVERGES "
            "(harder barrier, not easier). Infinite redshift with infinite proper distance = weak."
        ),
        "barrier_with_phi_to_plus_infty_at_finite_r": (
            "Possible if geometry ends (D->0) at finite r_*; ell=int e^phi dr may be finite. "
            "That is the 'hard/pinch' class — finite reach + redshift if phi rose."
        ),
        "barrier_with_phi_to_minus_infty": (
            "ell can converge but 1+z=e^{phi_far} ->0 blueshift out — fail macro look-out"
        ),
        "no_new_terms": "only classify existing EL system",
    }


def main() -> None:
    print("=" * 70)
    print("P1 free-D W=1 asymptotics")
    print("=" * 70)
    print(json.dumps(analytic_notes(), indent=2))

    Z = 1.0
    runs: list[Run] = []

    # A) Expand seeds: D0=1, v0>0, phi0=0, u0>=0 (redshift-out candidates)
    print("\n--- A expand seeds u0>=0 v0>0 ---")
    for u0 in [0.0, 0.05, 0.1, 0.2, 0.5]:
        for v0 in [0.1, 0.3, 0.5, 1.0]:
            rr = run_ivp(f"exp_u{u0:g}_v{v0:g}", [0.0, u0, 1.0, v0], r_max=60.0)
            runs.append(rr)
            print(
                f"  u0={u0:g} v0={v0:g}: {rr.status:8s} r_end={rr.r_end:6.2f} "
                f"phi[{rr.phi_min:.2f},{rr.phi_max:.2f}] D_end={rr.D_end:.3f} "
                f"ell={rr.ell:.3g} | {rr.notes}"
            )

    # B) Mild contract v0<0 with u0>0 — classic hard path
    print("\n--- B contract v0<0 u0>0 ---")
    for u0 in [0.05, 0.1, 0.2]:
        for v0 in [-0.1, -0.3, -0.5]:
            rr = run_ivp(f"con_u{u0:g}_v{v0:g}", [0.0, u0, 1.0, v0], r_max=40.0)
            runs.append(rr)
            print(
                f"  u0={u0:g} v0={v0:g}: {rr.status:8s} r_end={rr.r_end:6.2f} "
                f"phi_end={rr.phi_end:.2f} D_min={rr.D_min:.4f} ell={rr.ell:.3g} | {rr.notes}"
            )

    # C) Throat D'=0 u0>0 (hard family from explore)
    print("\n--- C throat v0=0 u0>0 ---")
    for u0 in [0.05, 0.1, 0.2, 0.5]:
        rr = run_ivp(f"thr_u{u0:g}", [0.0, u0, 1.0, 0.0], r_max=40.0)
        runs.append(rr)
        print(
            f"  u0={u0:g}: {rr.status:8s} r_end={rr.r_end:6.2f} "
            f"phi_end={rr.phi_end:.2f} ell={rr.ell:.3g} | {rr.notes}"
        )

    # D) ell to pinch for hard class — is proper distance finite?
    print("\n--- D ell at pinch vs u0 (throat) ---")
    pinch_table = []
    for u0 in [0.05, 0.1, 0.15, 0.2, 0.3]:
        rr = run_ivp(f"pinch_u{u0:g}", [0.0, u0, 1.0, 0.0], r_max=100.0)
        pinch_table.append(rr)
        print(
            f"  u0={u0:g}: {rr.status} r_end={rr.r_end:.3f} phi_end={rr.phi_end:.3f} "
            f"ell={rr.ell:.6g} null={rr.null_u:.6g} G_end={rr.G_end:.4f}"
        )

    # E) expand: does phi keep rising or level? ell vs r_max
    print("\n--- E expand u0=0.1 v0=0.5 ell vs R ---")
    for R in [10, 20, 40, 80]:
        rr = run_ivp(f"R{R}", [0.0, 0.1, 1.0, 0.5], r_max=float(R))
        print(
            f"  R={R}: status={rr.status} phi_end={rr.phi_end:.3f} "
            f"D_end={rr.D_end:.3f} ell={rr.ell:.4g} u_end={rr.u_end:.5f}"
        )

    # Summary classes
    n_pinch = sum(1 for r in runs if r.status == "pinch_D")
    n_ok = sum(1 for r in runs if r.status == "ok")
    n_phi_up_pinch = sum(
        1 for r in runs if r.status == "pinch_D" and "redshift_out_to_pinch" in r.notes
    )
    print(f"\n--- counts: ok={n_ok} pinch={n_pinch} pinch+phi_up={n_phi_up_pinch} ---")

    # Matter dilated brief asymptotics on expand (same action L_m)
    # (Z D^2 phi')' = 4 e^{-2phi}(D')^2 + 2 rho D^2 e^{-2phi}
    # F' = -(Z/4)D u^2 + (1/2) rho D e^{-2phi}
    print("\n--- F matter ball asymptote sketch (dilated rho compact) ---")
    print(
        "  Outside ball vacuum P1 laws resume: G frozen only if W compensated; "
        "here W=1 vacuum exterior G still increases if D'!=0. "
        "Same classes: open expand or pinch — matter loads G then vacuum dynamics."
    )

    out = {
        "premises": PREMISES,
        "analytic": analytic_notes(),
        "runs": [asdict(r) for r in runs],
        "pinch_table": [asdict(r) for r in pinch_table],
        "score": {
            "expand_G_gt_0": "typically open: D grows, phi rises then may slow; ell grows with R — no hard barrier in window",
            "pinch_G_gt_0": "finite r_end, finite ell, phi rose — BARRIER YES + redshift out YES; ontology = preferred pinch structure in chart",
            "elegant_cosmos": "pinch class is only vacuum P1 pass of barrier+redshift-out, but fails no-preferred-center as THE macro",
            "matter": "does not invent new exterior law under W=1; loads initial G",
        },
    }
    path = "macro_sector_P1_freeD_asymptotics_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE P1 freeD")


if __name__ == "__main__":
    main()
