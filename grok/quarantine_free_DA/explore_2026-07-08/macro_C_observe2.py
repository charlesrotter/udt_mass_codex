#!/usr/bin/env python3
"""
OBSERVE-C2: matter ball -> vacuum exterior under fallback C.

Packaging (LOCKED C):
  Inside / with rho:  (Z D^2 phi')' = 2 rho D^2 e^{-2 phi}
                      D'' = -(Z/4) D (phi')^2 + (1/2) rho D e^{-2 phi}
  Vacuum (rho=0):     (Z D^2 phi')' = 0   =>  G = D^2 phi' = const
                      D'' = -(Z/4) D (phi')^2

rho: compact support (smooth bump on [0, R_m]), zero outside.
Integrate from near-center seed outward through matter into vacuum exterior.

Mode: OBSERVE — structure of solutions, not sky fit.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
from scipy.integrate import solve_ivp

PREMISES = {
    "packaging": "C",
    "rho": "compact bump FREE profile",
    "mode": "OBSERVE not TARGET",
    "Z": "FREE representative scan",
}


def rho_compact(r, rho0, R_m, edge=0.15):
    """C^infty-like bump: positive on r < R_m, ~0 for r >= R_m.
    edge = transition width fraction of R_m.
    """
    if r >= R_m:
        return 0.0
    # raised cosine from 0 to R_m*(1-edge) flat-ish then smooth to 0
    r_flat = R_m * (1.0 - edge)
    if r <= r_flat:
        # mild center: 1 - a (r/R_m)^2
        x = r / max(R_m, 1e-12)
        return float(rho0 * (1.0 - 0.3 * x * x))
    # smooth to zero
    t = (r - r_flat) / max(R_m - r_flat, 1e-12)  # 0..1
    w = 0.5 * (1.0 + np.cos(np.pi * t))  # 1->0
    x = r_flat / max(R_m, 1e-12)
    rho_edge = rho0 * (1.0 - 0.3 * x * x)
    return float(rho_edge * w)


def rhs_C(r, y, Z, rho0, R_m):
    phi, u, D, v = y
    D = max(float(D), 1e-14)
    rh = rho_compact(r, rho0, R_m)
    em2 = np.exp(np.clip(-2.0 * phi, -50, 50))

    RHS = 2.0 * rh * D**2 * em2  # 0 in vacuum
    up = (RHS / Z - 2.0 * D * v * u) / (D**2)
    vp = -(Z / 4.0) * D * u**2 + 0.5 * rh * D * em2
    return [u, up, v, vp]


@dataclass
class BallRun:
    tag: str
    Z: float
    rho0: float
    R_m: float
    status: str
    r_end: float
    # at matter edge R_m
    phi_Rm: float
    u_Rm: float
    D_Rm: float
    v_Rm: float
    G_Rm: float
    # at end
    phi_end: float
    D_end: float
    G_end: float
    G_drift_vac: float  # max |G - G_Rm| for r > R_m
    pinched: bool
    notes: str


def integrate_ball(
    Z: float,
    rho0: float,
    R_m: float,
    r0: float = 0.05,
    r_max: float = 40.0,
    D0: float | None = None,
    v0: float = 1.0,
    phi0: float = 0.0,
    u0: float = 0.0,
) -> BallRun:
    if D0 is None:
        D0 = r0  # near polar-like areal
    y0 = np.array([phi0, u0, D0, v0], dtype=float)

    def fun(r, y):
        return rhs_C(r, y, Z, rho0, R_m)

    def hit_D(r, y):
        return y[2] - 1e-8

    hit_D.terminal = True
    hit_D.direction = -1

    sol = solve_ivp(
        fun,
        (r0, r_max),
        y0,
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        events=hit_D,
        max_step=0.05,
        dense_output=True,
    )

    pinched = bool(sol.t_events and len(sol.t_events[0]) > 0)
    status = "ok" if sol.success else ("pinch" if pinched else "stopped")

    # sample at R_m and exterior
    r_end = float(sol.t[-1])
    if sol.sol is None:
        Y_end = sol.y[:, -1]
        phi_Rm = u_Rm = D_Rm = v_Rm = G_Rm = float("nan")
        G_drift = float("nan")
        phi_end, D_end = float(Y_end[0]), float(Y_end[2])
        G_end = float(Y_end[2] ** 2 * Y_end[1])
    else:
        # Rm may be beyond pinch
        r_Rm = min(R_m, r_end)
        yRm = sol.sol(r_Rm)
        phi_Rm, u_Rm, D_Rm, v_Rm = map(float, yRm)
        G_Rm = D_Rm**2 * u_Rm
        yE = sol.sol(r_end)
        phi_end, D_end = float(yE[0]), float(yE[2])
        G_end = float(yE[2] ** 2 * yE[1])
        if r_end > R_m + 1e-6 and not pinched:
            rs = np.linspace(R_m, r_end, 80)
            Y = sol.sol(rs)
            G = Y[2] ** 2 * Y[1]
            G_drift = float(np.max(np.abs(G - G_Rm)))
        else:
            G_drift = float("nan")

    notes = []
    if r_end > R_m and not pinched:
        notes.append("reached_vacuum_ext")
        if G_drift == G_drift and G_drift < 1e-6:
            notes.append("G_conserved_ext")
        elif G_drift == G_drift:
            notes.append(f"G_drift={G_drift:.2e}")
    if pinched:
        notes.append("pinched")
    if D_end > D_Rm if D_Rm == D_Rm else False:
        notes.append("D_grew_in_ext")
    elif D_end < (D_Rm if D_Rm == D_Rm else D_end) - 1e-3:
        notes.append("D_fell_in_ext")

    return BallRun(
        tag=f"Z{Z:g}_r{rho0:g}_Rm{R_m:g}",
        Z=Z,
        rho0=rho0,
        R_m=R_m,
        status=status,
        r_end=r_end,
        phi_Rm=phi_Rm,
        u_Rm=u_Rm,
        D_Rm=D_Rm,
        v_Rm=v_Rm,
        G_Rm=G_Rm,
        phi_end=phi_end,
        D_end=D_end,
        G_end=G_end,
        G_drift_vac=G_drift,
        pinched=pinched,
        notes="; ".join(notes),
    )


def main() -> None:
    print("=" * 70)
    print("OBSERVE-C2 matter ball -> vacuum exterior")
    print("=" * 70)

    runs: list[BallRun] = []

    # Baseline grid
    print("\n--- Grid Z=1, r0=0.05, D0=r0, v0=1, u0=0 ---")
    for R_m in (1.0, 2.0, 3.0):
        for rho0 in (0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0):
            rr = integrate_ball(1.0, rho0, R_m, r_max=40.0)
            runs.append(rr)
            print(
                f"  Rm={R_m:g} ρ={rho0:g}: {rr.status:6s} r_end={rr.r_end:6.2f} "
                f"G_Rm={rr.G_Rm:8.4f} G_end={rr.G_end:8.4f} drift={rr.G_drift_vac} "
                f"D_Rm={rr.D_Rm:.3f} D_end={rr.D_end:.3f} phi_end={rr.phi_end:.3f} | {rr.notes}"
            )

    # Z scan at fixed Rm=2, rho0=5
    print("\n--- Z scan Rm=2 rho0=5 ---")
    for Z in (0.5, 1.0, 2.0, 4.0, 8.0):
        rr = integrate_ball(Z, 5.0, 2.0, r_max=40.0)
        runs.append(rr)
        print(
            f"  Z={Z:g}: {rr.status:6s} r_end={rr.r_end:6.2f} G_Rm={rr.G_Rm:.4f} "
            f"D_end={rr.D_end:.3f} phi_end={rr.phi_end:.3f} drift={rr.G_drift_vac} | {rr.notes}"
        )

    # Longer exterior for survivors
    print("\n--- Long exterior r_max=100, survivors-ish ---")
    for rho0, R_m in [(1.0, 2.0), (5.0, 2.0), (10.0, 2.0), (5.0, 3.0), (0.5, 2.0)]:
        rr = integrate_ball(1.0, rho0, R_m, r_max=100.0)
        runs.append(rr)
        print(
            f"  ρ={rho0:g} Rm={R_m:g}: {rr.status:6s} r_end={rr.r_end:7.2f} "
            f"G_Rm={rr.G_Rm:.4f} drift={rr.G_drift_vac} D_end={rr.D_end:.3f} "
            f"phi_end={rr.phi_end:.3f} | {rr.notes}"
        )

    # Vacuum exterior analytic check: G const, integrate D from junction
    print("\n--- Exterior-only check from saved junction (rho0=5 Rm=2) ---")
    rr = integrate_ball(1.0, 5.0, 2.0, r_max=50.0)
    print(
        f"  full: status={rr.status} G_Rm={rr.G_Rm:.6f} drift={rr.G_drift_vac} "
        f"D_Rm={rr.D_Rm:.4f} v_Rm={rr.v_Rm:.4f} phi_Rm={rr.phi_Rm:.4f}"
    )

    # Class summary
    n_ok = sum(1 for r in runs if r.status == "ok")
    n_pin = sum(1 for r in runs if r.pinched)
    n_vac = sum(1 for r in runs if "reached_vacuum_ext" in r.notes)
    n_G = sum(1 for r in runs if "G_conserved_ext" in r.notes)
    print(f"\n--- Counts: ok={n_ok} pinch={n_pin} reached_ext={n_vac} G_conserved_tag={n_G} ---")

    # Coulomb-like exterior phi: for frozen D would be -q/r; free D different
    # Report G_Rm vs rho0 for Rm=2
    print("\n--- G_Rm vs rho0 (Z=1 Rm=2) ---")
    for r in runs:
        if r.R_m == 2.0 and r.Z == 1.0 and r.r_end >= 2.0 - 1e-6:
            # first occurrence per rho0 from main grid (r_max 40)
            pass
    seen = set()
    for r in runs:
        if r.Z == 1.0 and r.R_m == 2.0 and abs(r.rho0) >= 0 and r.tag not in seen:
            # filter long runs duplicate by tag
            if "Z1_r" in r.tag and r.r_end <= 40.5:
                print(f"  ρ={r.rho0:g}: G_Rm={r.G_Rm:.5f} status={r.status} D_Rm={r.D_Rm:.3f}")
                seen.add(r.rho0)

    out = {"premises": PREMISES, "runs": [asdict(r) for r in runs]}
    path = "macro_C_observe2_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE OBSERVE-C2")


if __name__ == "__main__":
    main()
