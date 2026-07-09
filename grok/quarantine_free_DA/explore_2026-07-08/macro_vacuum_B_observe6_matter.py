#!/usr/bin/env python3
"""
OBSERVE-6: option B + continuum dust (dilated vs blind vs vacuum).

  Dilated:
    (Z D^2 phi')' = 4 e^{-2phi} (D')^2 + 2 rho D^2 e^{-2phi}
    (e^{-2phi} D')' = -(Z/4) D (phi')^2 + (1/2) rho D e^{-2phi}

  Blind: same FE-phi vacuum; FE-D with +(1/2) rho D (no e^{-2phi} on rho)

Throat seeds: D'=0, D>0, scan u*=phi'*, rho amplitude.
Mode: OBSERVE — does matter tame hard/soft? Not sky-fit.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
from scipy.integrate import solve_ivp

PREMISES = {
    "W": "1",
    "L_m": "dilated -rho D^2 e^{-2phi}; blind control; vacuum control",
    "rho": "prescribed gaussian FREE profile",
    "mode": "OBSERVE not TARGET",
}


def rho_gauss(r, rho0, rc, r_cen=1.0):
    return rho0 * np.exp(-(((r - r_cen) / rc) ** 2))


def rhs(r, y, Z, rho0, rc, mode: str):
    """y = [phi, u, D, v]; mode in vacuum|dilated|blind."""
    phi, u, D, v = y
    D = max(D, 1e-14)
    em2 = np.exp(-2.0 * phi)
    ep2 = np.exp(2.0 * phi)
    rh = 0.0 if mode == "vacuum" else float(rho_gauss(r, rho0, rc))

    # u' from FE-phi: Z(2 D v u + D^2 u') = 4 em2 v^2 + matter
    # u' = (4/Z) em2 (v/D)^2 - 2 (v/D) u + matter_phi
    if mode == "dilated":
        mat_phi = (2.0 / Z) * rh * em2  # (2 rho D^2 em2) / (Z D^2)
        mat_F = 0.5 * rh * D * em2
    elif mode == "blind":
        mat_phi = 0.0
        mat_F = 0.5 * rh * D
    else:
        mat_phi = 0.0
        mat_F = 0.0

    up = (4.0 / Z) * em2 * (v / D) ** 2 - 2.0 * (v / D) * u + mat_phi
    # F = em2 v; F' = - (Z/4) D u^2 + mat_F
    # em2 v' - 2 em2 u v = F'
    # v' = 2 u v + ep2 * F'
    Fp = -(Z / 4.0) * D * u**2 + mat_F
    vp = 2.0 * u * v + ep2 * Fp
    return [u, up, v, vp]


@dataclass
class Run:
    tag: str
    mode: str
    Z: float
    u: float
    rho0: float
    side: str
    status: str
    r_end: float
    phi_end: float
    D_end: float
    D_min: float
    D_max: float
    notes: str


def integrate_side(
    mode: str,
    Z: float,
    u: float,
    rho0: float,
    rc: float,
    side: str,
    r_star: float = 1.0,
    D_star: float = 1.0,
    r_out: float = 40.0,
    r_in: float = 0.05,
) -> Run:
    y0 = np.array([0.0, u, D_star, 0.0], dtype=float)
    r_target = r_out if side == "out" else r_in

    def fun(r, y):
        return rhs(r, y, Z, rho0, rc, mode)

    def hit_D(r, y):
        return y[2] - 1e-8

    hit_D.terminal = True
    hit_D.direction = -1

    def hit_phi(r, y):
        return 30.0 - abs(y[0])

    hit_phi.terminal = True
    hit_phi.direction = -1

    sol = solve_ivp(
        fun,
        (r_star, r_target),
        y0,
        method="DOP853",
        rtol=1e-8,
        atol=1e-10,
        events=(hit_D, hit_phi),
        max_step=0.08,
    )
    if sol.t.size < 2:
        return Run(
            f"{mode}_u{u:g}_{side}",
            mode,
            Z,
            u,
            rho0,
            side,
            "failed",
            r_star,
            0.0,
            D_star,
            D_star,
            D_star,
            sol.message,
        )

    phi, uu, D, v = sol.y
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
    if D[-1] < D[0] - 1e-4:
        notes.append("D_down")
    elif D[-1] > D[0] + 1e-4:
        notes.append("D_up")
    else:
        notes.append("D_flatish")
    if phi[-1] > 0.05:
        notes.append("phi_up")
    elif phi[-1] < -0.05:
        notes.append("phi_down")
    # late D std if long
    if status == "ok" and len(D) > 20:
        k = int(0.8 * len(D))
        if np.std(D[k:]) < 1e-3:
            notes.append("D_plateau")
        elif np.min(D) > 0.5 * D_star and status == "ok":
            notes.append("D_survives")

    return Run(
        tag=f"{mode}_Z{Z:g}_u{u:g}_r{rho0:g}_{side}",
        mode=mode,
        Z=Z,
        u=u,
        rho0=rho0,
        side=side,
        status=status,
        r_end=float(sol.t[-1]),
        phi_end=float(phi[-1]),
        D_end=float(D[-1]),
        D_min=float(np.min(D)),
        D_max=float(np.max(D)),
        notes="; ".join(notes),
    )


def main() -> None:
    print("=" * 70)
    print("OBSERVE-6 matter on B (dilated / blind / vacuum)")
    print("=" * 70)
    print(json.dumps(PREMISES, indent=2))

    Z = 1.0
    rc = 0.5  # gaussian width about throat
    us = [0.05, 0.1, 0.2, -0.1, -0.2]
    rho0s = [0.0, 0.1, 0.5, 1.0, 2.0, 5.0]
    modes = ["vacuum", "dilated", "blind"]

    runs: list[Run] = []
    print("\n--- Outward throat, Z=1, rc=0.5 ---")
    for mode in modes:
        for u in us:
            for rho0 in rho0s:
                if mode == "vacuum" and rho0 != 0.0:
                    continue
                if mode != "vacuum" and rho0 == 0.0:
                    continue
                rr = integrate_side(mode, Z, u, rho0 if mode != "vacuum" else 0.0, rc, "out")
                runs.append(rr)

    # Compact table: for each (mode,u) list fate vs rho0
    print("\n--- Fate matrix OUT (status @ r_end): mode × u × rho0 ---")
    for mode in modes:
        print(f"\n  [{mode}]")
        for u in us:
            bits = []
            for rho0 in rho0s:
                if mode == "vacuum":
                    if rho0 != 0.0:
                        continue
                    match = [r for r in runs if r.mode == mode and r.u == u and r.side == "out"]
                else:
                    match = [
                        r
                        for r in runs
                        if r.mode == mode and r.u == u and r.rho0 == rho0 and r.side == "out"
                    ]
                if not match:
                    continue
                r = match[0]
                bits.append(f"ρ{rho0:g}:{r.status[:1]}@{r.r_end:.1f}/D{r.D_end:.2f}")
            print(f"    u={u:+g}: " + " | ".join(bits))

    # Focus: does dilated delay/prevent pinch for +u?
    print("\n--- Pinch radius vs rho0 for +u dilated (Z=1) ---")
    for u in [0.05, 0.1, 0.2]:
        row = []
        # vacuum
        rv = integrate_side("vacuum", Z, u, 0.0, rc, "out", r_out=40.0)
        row.append(f"vac:{rv.status}@{rv.r_end:.2f}")
        for rho0 in [0.5, 1.0, 2.0, 5.0, 10.0]:
            rd = integrate_side("dilated", Z, u, rho0, rc, "out", r_out=40.0)
            runs.append(rd)
            row.append(f"ρ{rho0:g}:{rd.status}@{rd.r_end:.2f}")
        print(f"  u={u:g}: " + " | ".join(row))

    print("\n--- Same for blind +u=0.1 ---")
    row = []
    for rho0 in [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]:
        mode = "vacuum" if rho0 == 0 else "blind"
        rb = integrate_side(mode, Z, 0.1, rho0, rc, "out", r_out=40.0)
        runs.append(rb)
        row.append(f"ρ{rho0:g}:{rb.status}@{rb.r_end:.2f}/D{rb.D_end:.2f}")
    print("  " + " | ".join(row))

    # Soft side: does dilated change D_inf?
    print("\n--- Soft side u=-0.1 to r=100: D_end vs mode/rho ---")
    for mode, rho0 in [
        ("vacuum", 0.0),
        ("dilated", 0.5),
        ("dilated", 2.0),
        ("dilated", 5.0),
        ("blind", 2.0),
        ("blind", 5.0),
    ]:
        rs = integrate_side(mode, Z, -0.1, rho0, rc, "out", r_out=100.0)
        runs.append(rs)
        print(
            f"  {mode:8s} ρ={rho0:g}: {rs.status} r_end={rs.r_end:.1f} "
            f"D_end={rs.D_end:.4f} phi_end={rs.phi_end:.3f} | {rs.notes}"
        )

    # Matter centered OFF throat (outer lump) mild probe
    print("\n--- Dilated lump off-throat (r_cen=3) u=0.1 ---")
    # quick custom: modify by temporary monkey — integrate with shifted rho via rc wrapper
    def rhs_shift(r, y, Z, rho0, rc, r_cen):
        phi, u, D, v = y
        D = max(D, 1e-14)
        em2 = np.exp(-2.0 * phi)
        ep2 = np.exp(2.0 * phi)
        rh = float(rho_gauss(r, rho0, rc, r_cen=r_cen))
        mat_phi = (2.0 / Z) * rh * em2
        mat_F = 0.5 * rh * D * em2
        up = (4.0 / Z) * em2 * (v / D) ** 2 - 2.0 * (v / D) * u + mat_phi
        Fp = -(Z / 4.0) * D * u**2 + mat_F
        vp = 2.0 * u * v + ep2 * Fp
        return [u, up, v, vp]

    for rho0 in [1.0, 5.0, 10.0]:
        sol = solve_ivp(
            lambda r, y: rhs_shift(r, y, 1.0, rho0, 0.5, 3.0),
            (1.0, 40.0),
            [0.0, 0.1, 1.0, 0.0],
            method="DOP853",
            rtol=1e-8,
            atol=1e-10,
            max_step=0.08,
            events=[lambda r, y: y[2] - 1e-8],
        )
        sol.t_events  # noqa
        # set event terminal
        print(
            f"  ρ0={rho0:g} r_cen=3: success={sol.success} r_end={sol.t[-1]:.2f} "
            f"D_end={sol.y[2,-1]:.4f} phi_end={sol.y[0,-1]:.3f}"
        )

    # redo off-throat with terminal event
    print("\n--- Off-throat dilated pinch check (proper events) ---")
    for rho0 in [1.0, 5.0, 20.0]:

        def hit(r, y):
            return y[2] - 1e-8

        hit.terminal = True
        hit.direction = -1
        sol = solve_ivp(
            lambda r, y: rhs_shift(r, y, 1.0, rho0, 0.5, 3.0),
            (1.0, 40.0),
            [0.0, 0.1, 1.0, 0.0],
            method="DOP853",
            rtol=1e-8,
            atol=1e-10,
            max_step=0.08,
            events=hit,
        )
        st = "ok" if sol.success else ("pinch" if sol.t[-1] < 39 else "stopped")
        print(
            f"  ρ0={rho0:g}: {st} r_end={sol.t[-1]:.2f} D_min={sol.y[2].min():.4f} "
            f"phi_end={sol.y[0,-1]:.3f}"
        )

    out = {
        "premises": PREMISES,
        "runs": [asdict(r) for r in runs],
    }
    path = "macro_vacuum_B_observe6_matter_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE OBSERVE-6")


if __name__ == "__main__":
    main()
