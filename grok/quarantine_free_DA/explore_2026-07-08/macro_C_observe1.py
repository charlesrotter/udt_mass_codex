#!/usr/bin/env python3
"""
OBSERVE-C1: fallback C vacuum + dilated matter.

Vacuum:
  (Z D^2 phi')' = 0
  D'' = -(Z/4) D (phi')^2

Matter dilated:
  (Z D^2 phi')' = 2 rho D^2 e^{-2phi}
  D'' = -(Z/4) D (phi')^2 + (1/2) rho D e^{-2phi}

Mode: OBSERVE. No sky fit.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp

PREMISES = {
    "packaging": "C: W=e^{2phi} vacuum; dilated L_m sources phi",
    "Z": "FREE representative 1",
    "mode": "OBSERVE",
    "B": "parked",
}


def cas_checks() -> dict:
    r = sp.symbols("r", positive=True)
    Z, q, D0 = sp.symbols("Z q D0", positive=True)
    # Coulomb frozen D=r: phi = -q/r (phi_inf=0)
    phi = -q / r
    chk = sp.simplify(sp.diff(Z * r**2 * sp.diff(phi, r), r))
    # Constant G: D^2 phi' = K
    # Trivial flat
    return {
        "coulomb_frozen_EL": str(chk),
        "coulomb_ok": chk == 0,
    }


def rho_gauss(r, rho0, rc, r_cen=0.0):
    return rho0 * np.exp(-(((r - r_cen) / max(rc, 1e-12)) ** 2))


def rhs_C(r, y, Z, rho0, rc, r_cen, matter: bool, dilated: bool = True):
    """y = [phi, u, D, v]"""
    phi, u, D, v = y
    D = max(float(D), 1e-14)
    rh = float(rho_gauss(r, rho0, rc, r_cen)) if matter else 0.0
    em2 = np.exp(-2.0 * phi)

    # (Z D^2 u)' = 2 rho D^2 em2  (dilated) or 0
    # Z (2 D v u + D^2 u') = RHS
    if matter and dilated:
        RHS = 2.0 * rh * D**2 * em2
    else:
        RHS = 0.0
    up = (RHS / Z - 2.0 * D * v * u) / (D**2)

    # D'' = -(Z/4) D u^2 + (1/2) rho D em2  (dilated)
    if matter and dilated:
        vp = -(Z / 4.0) * D * u**2 + 0.5 * rh * D * em2
    elif matter and not dilated:
        vp = -(Z / 4.0) * D * u**2 + 0.5 * rh * D
    else:
        vp = -(Z / 4.0) * D * u**2

    return [u, up, v, vp]


@dataclass
class Run:
    tag: str
    kind: str
    Z: float
    u0: float
    D0: float
    v0: float
    rho0: float
    status: str
    r_end: float
    phi_end: float
    D_end: float
    D_min: float
    D_max: float
    G_start: float
    G_end: float
    notes: str


def integrate(
    tag: str,
    kind: str,
    Z: float,
    r0: float,
    y0: np.ndarray,
    r_max: float,
    rho0: float = 0.0,
    rc: float = 1.0,
    r_cen: float = 0.0,
    matter: bool = False,
    dilated: bool = True,
) -> Run:
    phi0, u0, D0, v0 = y0
    G0 = D0**2 * u0

    def fun(r, y):
        return rhs_C(r, y, Z, rho0, rc, r_cen, matter, dilated)

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
        (r0, r_max),
        y0,
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        events=(hit_D, hit_phi),
        max_step=0.1,
    )
    if sol.t.size < 2:
        return Run(tag, kind, Z, u0, D0, v0, rho0, "failed", r0, phi0, D0, D0, D0, G0, G0, sol.message)

    phi, u, D, v = sol.y
    G = D**2 * u
    hit_d = bool(sol.t_events and len(sol.t_events[0]) > 0)
    if sol.success:
        status = "ok"
    elif hit_d:
        status = "pinch"
    else:
        status = "stopped"

    notes = []
    # vacuum: G should be constant
    if not matter:
        dG = np.max(np.abs(G - G[0]))
        notes.append(f"max|dG|={dG:.2e}")
    if D[-1] > D[0] + 1e-3:
        notes.append("D_up")
    elif D[-1] < D[0] - 1e-3:
        notes.append("D_down")
    else:
        notes.append("D_flatish")
    if abs(u[-1]) < 1e-4 and abs(v[-1]) < 1e-4:
        notes.append("slopes_small")
    if status == "ok" and len(D) > 30:
        k = int(0.8 * len(D))
        if np.std(D[k:]) < 1e-3:
            notes.append("D_plateau")

    return Run(
        tag=tag,
        kind=kind,
        Z=Z,
        u0=float(u0),
        D0=float(D0),
        v0=float(v0),
        rho0=float(rho0),
        status=status,
        r_end=float(sol.t[-1]),
        phi_end=float(phi[-1]),
        D_end=float(D[-1]),
        D_min=float(np.min(D)),
        D_max=float(np.max(D)),
        G_start=float(G[0]),
        G_end=float(G[-1]),
        notes="; ".join(notes),
    )


def main() -> None:
    print("=" * 70)
    print("OBSERVE-C1 fallback C")
    print("=" * 70)
    print("CAS:", cas_checks())

    Z = 1.0
    runs: list[Run] = []

    # --- Vacuum ---
    print("\n--- C vacuum ---")
    # flat
    runs.append(
        integrate("vac_flat", "vac", Z, 0.5, np.array([0.0, 0.0, 1.0, 0.0]), 20.0)
    )
    # throat D'=0, small u
    for u in [0.0, 0.05, 0.1, 0.2, -0.1, -0.2]:
        rr = integrate(
            f"vac_throat_u{u:g}",
            "vac",
            Z,
            1.0,
            np.array([0.0, u, 1.0, 0.0]),
            50.0,
        )
        runs.append(rr)
        print(
            f"  {rr.tag:22s} {rr.status:6s} r_end={rr.r_end:6.2f} "
            f"D[{rr.D_min:.3f},{rr.D_max:.3f}] phi_end={rr.phi_end:7.3f} "
            f"G {rr.G_start:.4f}->{rr.G_end:.4f} | {rr.notes}"
        )

    # both directions from throat u=0.1
    print("\n--- C vacuum throat two-sided u=0.1 ---")
    for side, rmax in [("out", 50.0), ("in", 0.05)]:
        rr = integrate(
            f"vac_u0.1_{side}",
            "vac",
            Z,
            1.0,
            np.array([0.0, 0.1, 1.0, 0.0]),
            rmax,
        )
        runs.append(rr)
        print(
            f"  {side}: {rr.status} r_end={rr.r_end:.3f} D_end={rr.D_end:.4f} "
            f"phi_end={rr.phi_end:.4f} G={rr.G_end:.4f} | {rr.notes}"
        )

    # expand D' > 0
    print("\n--- C vacuum mild expand D'=0.3, u=0.05 ---")
    rr = integrate(
        "vac_expand",
        "vac",
        Z,
        0.5,
        np.array([0.0, 0.05, 1.0, 0.3]),
        30.0,
    )
    runs.append(rr)
    print(f"  {rr.status} r_end={rr.r_end:.2f} D_end={rr.D_end:.3f} phi_end={rr.phi_end:.3f} | {rr.notes}")

    # --- Matter dilated: ball-ish gaussian at center, start outside center ---
    print("\n--- C dilated matter: throat seed + rho at r_cen=1 ---")
    for u in [0.0, 0.05, 0.1, -0.05]:
        for rho0 in [0.2, 1.0, 3.0, 10.0]:
            rr = integrate(
                f"mat_u{u:g}_r{rho0:g}",
                "mat_dil",
                Z,
                1.0,
                np.array([0.0, u, 1.0, 0.0]),
                40.0,
                rho0=rho0,
                rc=0.6,
                r_cen=1.0,
                matter=True,
                dilated=True,
            )
            runs.append(rr)
            print(
                f"  u={u:+g} ρ={rho0:g}: {rr.status:6s} r_end={rr.r_end:6.2f} "
                f"D[{rr.D_min:.3f},{rr.D_max:.3f}] phi_end={rr.phi_end:7.3f} "
                f"G {rr.G_start:.3f}->{rr.G_end:.3f} | {rr.notes}"
            )

    # Matter from small r with D~r-like: D0 small, v0=1, u0=0, rho centered 0
    print("\n--- C dilated: near-center seed D0=0.2 v0=1 u0=0 rho at 0 ---")
    for rho0 in [0.0, 0.5, 2.0, 5.0, 20.0]:
        rr = integrate(
            f"near_c_r{rho0:g}",
            "mat_dil" if rho0 else "vac",
            Z,
            0.2,
            np.array([0.0, 0.0, 0.2, 1.0]),
            30.0,
            rho0=rho0,
            rc=0.8,
            r_cen=0.0,
            matter=(rho0 > 0),
            dilated=True,
        )
        runs.append(rr)
        print(
            f"  ρ={rho0:g}: {rr.status:6s} r_end={rr.r_end:6.2f} "
            f"D_end={rr.D_end:.3f} phi_end={rr.phi_end:.3f} "
            f"G {rr.G_start:.3f}->{rr.G_end:.3f} | {rr.notes}"
        )

    # Blind contrast few
    print("\n--- C blind control throat u=0 rho=3 ---")
    rr = integrate(
        "blind_u0_r3",
        "mat_blind",
        Z,
        1.0,
        np.array([0.0, 0.0, 1.0, 0.0]),
        40.0,
        rho0=3.0,
        rc=0.6,
        r_cen=1.0,
        matter=True,
        dilated=False,
    )
    runs.append(rr)
    print(f"  {rr.status} r_end={rr.r_end:.2f} D_end={rr.D_end:.3f} phi_end={rr.phi_end:.3f} G {rr.G_start}->{rr.G_end}")

    # Analytic vacuum: if G=D^2 phi' = K const, D'' = -(Z/4) D (K/D^2)^2 = -(Z/4) K^2 / D^3
    print("\n--- Vacuum identity: D'' + (Z/4) K^2 / D^3 = 0 for K=G ---")
    sol = solve_ivp(
        lambda r, y: rhs_C(r, y, 1.0, 0, 1, 0, False),
        (1.0, 20.0),
        [0.0, 0.1, 1.0, 0.0],
        dense_output=True,
        rtol=1e-10,
        max_step=0.05,
    )
    rs = np.linspace(1.0, sol.t[-1], 100)
    Y = sol.sol(rs)
    phi, u, D, v = Y
    K = D**2 * u
    resid = np.gradient(v, rs) + (1.0 / 4.0) * (K**2) / (D**3)
    # also check K constant
    print(f"  max|K-K0|={np.max(np.abs(K-K[0])):.3e}, max|D''+(Z/4)K^2/D^3|={np.max(np.abs(resid)):.3e}")

    out = {"premises": PREMISES, "runs": [asdict(r) for r in runs]}
    path = "macro_C_observe1_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE OBSERVE-C1")


if __name__ == "__main__":
    main()
