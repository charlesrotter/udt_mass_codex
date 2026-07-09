#!/usr/bin/env python3
"""
OBSERVE-4: nondimensional reduction + outer asymptotics (vacuum B).

A) Analytic / CAS: rewrite FE in (phi, d=ln D), show D* scale-out.
B) Optional first-integral probes.
C) Long outward runs on SURVIVE seeds — what does (phi, D) do as r grows?

Mode: OBSERVE. No sources. No sky.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

from macro_vacuum_B_observe1 import system_rhs

PREMISES = {
    "W": "1",
    "L_m": "0",
    "mode": "OBSERVE",
    "prior": "O1-O3 throat survival band",
}


def cas_nondim() -> dict:
    r = sp.symbols("r", positive=True)
    Z = sp.symbols("Z", positive=True)
    phi = sp.Function("phi")
    D = sp.Function("D")
    ph, Dp = phi(r), D(r)
    # Original FE
    FE_phi = sp.diff(Z * Dp**2 * sp.diff(ph, r), r) - 4 * sp.exp(-2 * ph) * sp.diff(Dp, r) ** 2
    FE_D = sp.diff(sp.exp(-2 * ph) * sp.diff(Dp, r), r) + (Z / 4) * Dp * sp.diff(ph, r) ** 2

    # d = ln D,  D = exp(d), D' = d' exp(d)
    d = sp.Function("d")
    dd = d(r)
    Dsub = sp.exp(dd)
    # substitute
    FE_phi_d = sp.simplify(FE_phi.subs(Dp, Dsub).doit())
    FE_D_d = sp.simplify(FE_D.subs(Dp, Dsub).doit())
    # Factor e^{2d} etc
    FE_phi_red = sp.simplify(FE_phi_d / sp.exp(2 * dd))
    FE_D_red = sp.simplify(FE_D_d / sp.exp(dd))

    # Scale D -> lam D: already known independent for phi
    # First integral candidates: try energy-like
    # From fluxes F = e^{-2phi} D', G = D^2 phi'
    F = sp.exp(-2 * ph) * sp.diff(Dp, r)
    G = Dp**2 * sp.diff(ph, r)
    # F' = -(Z/4) D (phi')^2 = -(Z/4) G^2 / D^3
    # G' = (4/Z) e^{-2phi} (D')^2 = (4/Z) e^{2phi} F^2
    # wait e^{-2phi} (D')^2 = e^{-2phi} (F e^{2phi})^2 = e^{2phi} F^2
    # G' = (4/Z) e^{2phi} F^2

    return {
        "FE_phi_in_d": str(FE_phi_red),
        "FE_D_in_d": str(FE_D_red),
        "flux_form": {
            "F": "e^{-2phi} D'",
            "G": "D^2 phi'",
            "F_prime": "-(Z/4) D (phi')^2 = -(Z/4) G^2 / D^3",
            "G_prime": "(4/Z) e^{2phi} F^2",
        },
        "D_star_independence": (
            "D -> lam D leaves phi equation invariant; "
            "d = ln D shifts by const; derivatives of d unchanged. "
            "u_crit independent of D* (O3) is structural."
        ),
        "plain_d_system": (
            "With d=ln D: "
            "G = e^{2d} phi', F = e^{-2phi} e^{d} d'. "
            "System is autonomous in (phi, d, phi', d') with no explicit D scale."
        ),
    }


def cas_first_integral_probe() -> dict:
    """Probe whether a simple polynomial conserved quantity exists (local symbolic)."""
    # Use flux ODE: dF/dr = -(Z/4) G^2 / D^3, dG/dr = (4/Z) e^{2phi} F^2
    # Need D, phi evolution too — hard. Try in terms of F,G,phi,D as state.
    # Autonomic: dF/dG = F'/G' = [-(Z/4) G^2/D^3] / [(4/Z) e^{2phi} F^2]
    # = -(Z^2/16) G^2 / (D^3 e^{2phi} F^2)
    # Still involves D, phi.
    # From G = D^2 phi', F = e^{-2phi} D':
    # d phi / d ln D = phi' / (D'/D) = (G/D^2) / (F e^{2phi}/D) = G/(D F) e^{-2phi} wait
    # phi'/(d') = G/D^2 / (F e^{2phi}/D) wait D' = F e^{2phi}, d'=D'/D = F e^{2phi}/D
    # phi'/d' = (G/D^2) / (F e^{2phi}/D) = G/(D F e^{2phi})
    return {
        "simple_F_G_conserved": (
            "No elementary conserved H(F,G) independent of phi,D found; "
            "dF/dG still depends on D and phi. OPEN — not claimed absent."
        ),
        "monotonic_pair": "F nonincreasing, G nondecreasing remain the structural controls.",
    }


@dataclass
class OuterRun:
    tag: str
    Z: float
    u: float
    r_max: float
    status: str
    r_end: float
    phi_end: float
    D_end: float
    D_min: float
    F_end: float
    G_end: float
    # trend diagnostics
    D_slope_end: float
    phi_slope_end: float
    dlnD_dr_end: float
    notes: str


def long_outward(Z: float, u: float, D_star: float = 1.0, r_star: float = 1.0, r_max: float = 50.0) -> OuterRun:
    y0 = np.array([0.0, u, D_star, 0.0], dtype=float)

    def fun(r, y):
        return system_rhs(r, y, Z)

    def hit_D(r, y):
        return y[2] - 1e-8

    hit_D.terminal = True
    hit_D.direction = -1

    def hit_phi(r, y):
        return 40.0 - abs(y[0])

    hit_phi.terminal = True
    hit_phi.direction = -1

    sol = solve_ivp(
        fun,
        (r_star, r_max),
        y0,
        method="DOP853",
        rtol=1e-8,
        atol=1e-10,
        events=(hit_D, hit_phi),
        max_step=0.1,
        dense_output=False,
    )
    if sol.t.size < 2:
        return OuterRun(
            tag=f"Z{Z:g}_u{u:g}",
            Z=Z,
            u=u,
            r_max=r_max,
            status="failed",
            r_end=r_star,
            phi_end=0.0,
            D_end=D_star,
            D_min=D_star,
            F_end=0.0,
            G_end=0.0,
            D_slope_end=0.0,
            phi_slope_end=u,
            dlnD_dr_end=0.0,
            notes=str(sol.message),
        )

    phi, uu, D, v = sol.y
    F = np.exp(-2 * phi) * v
    G = D**2 * uu
    hit_d = bool(sol.t_events and len(sol.t_events[0]) > 0)
    hit_p = bool(sol.t_events and len(sol.t_events[1]) > 0)
    if sol.success:
        status = "ok"
    elif hit_d:
        status = "pinch"
    elif hit_p:
        status = "phi_cap"
    else:
        status = "stopped"

    notes = []
    # late trend: last 10% of samples
    n = len(sol.t)
    k = max(2, n // 10)
    # D decreasing?
    if D[-1] < D[0] - 1e-8:
        notes.append("D drops from throat")
    if abs(v[-1]) < 1e-4 and abs(uu[-1]) < 1e-4:
        notes.append("near_static_end")
    elif abs(v[-1]) < 1e-3:
        notes.append("D_slope_small")
    if phi[-1] > phi[0] + 0.01:
        notes.append("phi_up")
    elif phi[-1] < phi[0] - 0.01:
        notes.append("phi_down")
    # asymptotic class heuristic
    if status == "pinch":
        notes.append("CLASS: finite-r pinch")
    elif D[-1] > 0.5 * D_star and abs(v[-1]) < 0.01 and abs(uu[-1]) < 0.02:
        notes.append("CLASS: approach plateau?")
    elif D[-1] < 0.2 * D_star and status == "ok":
        notes.append("CLASS: slow drain D (still >0 at r_max)")
    elif status == "ok":
        notes.append("CLASS: ongoing evolution at r_max")

    dln = v[-1] / max(D[-1], 1e-15)
    return OuterRun(
        tag=f"Z{Z:g}_u{u:g}",
        Z=Z,
        u=u,
        r_max=r_max,
        status=status,
        r_end=float(sol.t[-1]),
        phi_end=float(phi[-1]),
        D_end=float(D[-1]),
        D_min=float(np.min(D)),
        F_end=float(F[-1]),
        G_end=float(G[-1]),
        D_slope_end=float(v[-1]),
        phi_slope_end=float(uu[-1]),
        dlnD_dr_end=float(dln),
        notes="; ".join(notes),
    )


def main() -> None:
    print("=" * 70)
    print("OBSERVE-4 nondim + outer asymptotics")
    print("=" * 70)

    nd = cas_nondim()
    print("\n--- Nondim / flux form ---")
    for k, v in nd.items():
        print(f"  {k}: {v}")

    fi = cas_first_integral_probe()
    print("\n--- First integral probe ---")
    for k, v in fi.items():
        print(f"  {k}: {v}")

    # Verify D* independence numerically: same u,Z, two D*, compare phi(r) and D/D*
    print("\n--- Numeric scale-out check ---")
    Z, u = 1.0, 0.1
    r_max = 8.0
    curves = {}
    for Ds in (0.5, 1.0, 2.0):
        sol = solve_ivp(
            lambda r, y: system_rhs(r, y, Z),
            (1.0, r_max),
            [0.0, u, Ds, 0.0],
            method="DOP853",
            rtol=1e-9,
            atol=1e-11,
            dense_output=True,
            max_step=0.05,
        )
        rs = np.linspace(1.0, sol.t[-1], 100)
        Y = sol.sol(rs)
        curves[Ds] = (rs, Y[0], Y[2] / Ds)
    # compare phi and D/D* at common r
    r_common = curves[1.0][0]
    phi1 = curves[1.0][1]
    dhat1 = curves[1.0][2]
    for Ds in (0.5, 2.0):
        rs, phi, dhat = curves[Ds]
        # interp to r_common
        phi_i = np.interp(r_common, rs, phi)
        dhat_i = np.interp(r_common, rs, dhat)
        err_phi = np.max(np.abs(phi_i - phi1))
        err_d = np.max(np.abs(dhat_i - dhat1))
        print(f"  D*={Ds} vs 1: max|dphi|={err_phi:.3e}, max|d(D/D*)|={err_d:.3e}")

    # Outer runs: grid of mild/critical-ish u
    print("\n--- Long outward (r_max=50) ---")
    runs = []
    for Z in (1.0, 4.0, 8.0):
        for u in (0.0, 0.05, 0.1, 0.15, 0.2, -0.1, -0.2):
            rr = long_outward(Z, u, r_max=50.0)
            runs.append(rr)
            print(
                f"  {rr.tag:14s} {rr.status:7s} r_end={rr.r_end:7.3f} "
                f"phi_end={rr.phi_end:8.3f} D_end={rr.D_end:8.4f} "
                f"F={rr.F_end:10.3g} G={rr.G_end:10.3g} | {rr.notes}"
            )

    # Even longer for one mild survive seed
    print("\n--- Ultra outward Z=1 u=0.05 r_max=200 ---")
    ultra = long_outward(1.0, 0.05, r_max=200.0)
    print(
        f"  {ultra.status} r_end={ultra.r_end:.3f} phi_end={ultra.phi_end:.4f} "
        f"D_end={ultra.D_end:.6f} F={ultra.F_end:.4g} G={ultra.G_end:.4g} | {ultra.notes}"
    )

    print("\n--- Ultra outward Z=1 u=-0.1 r_max=200 ---")
    ultra_m = long_outward(1.0, -0.1, r_max=200.0)
    print(
        f"  {ultra_m.status} r_end={ultra_m.r_end:.3f} phi_end={ultra_m.phi_end:.4f} "
        f"D_end={ultra_m.D_end:.6f} F={ultra_m.F_end:.4g} G={ultra_m.G_end:.4g} | {ultra_m.notes}"
    )

    out = {
        "premises": PREMISES,
        "nondim": nd,
        "first_integral": fi,
        "outer_r50": [asdict(r) for r in runs],
        "ultra_u0.05": asdict(ultra),
        "ultra_u-0.1": asdict(ultra_m),
    }
    path = "macro_vacuum_B_observe4_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE OBSERVE-4")


if __name__ == "__main__":
    main()
