#!/usr/bin/env python3
"""
Asymptotics on the SIMPLE metric only (D_A = r, field = phi only).

  W = e^{2phi}:  (r^2 phi')' = 0  ->  phi = phi_inf - q/r
  W = 1:         Z (r^2 phi')' = 4 e^{-2 phi}

Elegant probes: redshift out (phi increasing with r), hard barrier
(ell = int e^phi dr, null = int e^{2phi} dr finite?), relational note.

No free D_A. Provenance: SIMPLE_METRIC_MACRO.md
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
from scipy.integrate import solve_ivp, trapezoid

Z_DEFAULT = 1.0


def system_W1(r, y, Z):
    phi, u = y
    em2 = np.exp(-2.0 * np.clip(phi, -40, 40))
    # (r^2 u)' = (4/Z) e^{-2 phi}
    up = (4.0 / Z) * em2 / (r**2) - 2.0 * u / r
    return [u, up]


@dataclass
class Shot:
    tag: str
    W: str
    r0: float
    phi0: float
    u0: float
    r_end: float
    phi_end: float
    u_end: float
    status: str
    ell: float
    null_int: float
    phi_min: float
    phi_max: float
    notes: str


def integrate_W1(
    r0: float,
    phi0: float,
    u0: float,
    r_max: float = 200.0,
    Z: float = Z_DEFAULT,
    direction: str = "out",
) -> Shot:
    target = r_max if direction == "out" else max(1e-4, r0 * 1e-4)

    def hit_phi(r, y):
        return 30.0 - abs(y[0])

    hit_phi.terminal = True
    hit_phi.direction = -1

    sol = solve_ivp(
        lambda r, y: system_W1(r, y, Z),
        (r0, target),
        [phi0, u0],
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        events=hit_phi,
        max_step=0.05 if direction == "out" else 0.01,
        dense_output=True,
    )
    if sol.t.size < 2:
        return Shot(
            f"W1_{direction}_u{u0:g}",
            "1",
            r0,
            phi0,
            u0,
            r0,
            phi0,
            u0,
            "failed",
            0.0,
            0.0,
            phi0,
            phi0,
            sol.message,
        )

    r = sol.t.copy()
    phi, u = sol.y.copy()
    if r[0] > r[-1]:
        r, phi, u = r[::-1], phi[::-1], u[::-1]

    ep = np.exp(np.clip(phi, -40, 40))
    ell = float(trapezoid(ep, r))
    null_int = float(trapezoid(ep**2, r))

    status = "ok" if sol.success else "stopped"
    if sol.t_events and len(sol.t_events[0]) > 0:
        status = "phi_cap"

    notes = []
    if phi[-1] > phi[0] + 0.05:
        notes.append("phi_up")
    elif phi[-1] < phi[0] - 0.05:
        notes.append("phi_down")
    if status == "ok" and direction == "out":
        # growth of ell with window suggests open
        notes.append("reached_rmax")
    return Shot(
        tag=f"W1_{direction}_r{r0:g}_u{u0:g}",
        W="1",
        r0=r0,
        phi0=phi0,
        u0=u0,
        r_end=float(sol.t[-1]),
        phi_end=float(sol.y[0, -1]),
        u_end=float(sol.y[1, -1]),
        status=status,
        ell=ell,
        null_int=null_int,
        phi_min=float(np.min(phi)),
        phi_max=float(np.max(phi)),
        notes="; ".join(notes),
    )


def coulomb_analytics() -> dict:
    """W = e^{2phi}: phi = phi_inf - q/r. Observer at r0 with phi(r0)=0 => phi_inf = q/r0."""
    # For r > r0, phi = q (1/r0 - 1/r) > 0 if q>0 — redshift out
    # As r->oo, phi -> q/r0 finite, 1+z_max = e^{q/r0}
    # ell = int_{r0}^oo e^{phi} dr = e^{q/r0} int e^{-q/r} dr DIVERGES
    return {
        "solution": "phi = phi_inf - q/r",
        "observer_phi_r0_0": "phi_inf = q/r0 for q>0 => phi increases to phi_inf as r increases",
        "z_max": "e^{q/r0} - 1  FINITE",
        "ell_to_infty": "DIVERGES (e^phi -> e^{phi_inf} > 0)",
        "null_to_infty": "DIVERGES",
        "hard_barrier": "FAIL",
        "redshift_out": "YES (for q>0, looking outward from r0)",
        "center": "singular at r=0 if q!=0 (chart origin)",
    }


def Q_mono_check(Z=1.0) -> dict:
    sol = solve_ivp(
        lambda r, y: system_W1(r, y, Z),
        (1.0, 50.0),
        [0.0, -0.5],
        dense_output=True,
        rtol=1e-9,
        max_step=0.05,
    )
    rs = np.linspace(1.0, sol.t[-1], 300)
    Y = sol.sol(rs)
    Q = rs**2 * Y[1]
    return {
        "Q_start": float(Q[0]),
        "Q_end": float(Q[-1]),
        "min_dQ": float(np.min(np.diff(Q))),
        "strictly_increasing": bool(np.min(np.diff(Q)) > -1e-12),
    }


def main() -> None:
    print("=" * 70)
    print("Simple-metric asymptotics (phi only)")
    print("=" * 70)

    W_comp = coulomb_analytics()
    print("\n--- W = e^{2phi} (exact) ---")
    for k, v in W_comp.items():
        print(f"  {k}: {v}")

    print("\n--- W = 1: Q = r^2 phi' monotone ---")
    qm = Q_mono_check()
    print(f"  {qm}")

    shots = []
    print("\n--- W = 1 outward r0=1 phi0=0 ---")
    for u0 in [-1.0, -0.5, 0.0, 0.1, 0.5, 1.0, 2.0]:
        sh = integrate_W1(1.0, 0.0, u0, r_max=200.0)
        shots.append(sh)
        print(
            f"  u0={u0:+.1f}: {sh.status:8s} r_end={sh.r_end:7.1f} "
            f"phi_end={sh.phi_end:6.3f} u_end={sh.u_end:.5f} "
            f"ell={sh.ell:.4g} | {sh.notes}"
        )

    print("\n--- W = 1 ell growth u0=0.5 ---")
    ell_growth = []
    for R in [10, 20, 50, 100, 200, 500]:
        sh = integrate_W1(1.0, 0.0, 0.5, r_max=float(R))
        ell_growth.append((R, sh.ell, sh.phi_end, sh.u_end))
        print(f"  R={R:4d}: ell={sh.ell:.6g} phi_end={sh.phi_end:.4f} u_end={sh.u_end:.6f}")

    print("\n--- W = 1 late Coulomb fit u0=0.5 R=300 ---")
    sol = solve_ivp(
        lambda r, y: system_W1(r, y, 1.0),
        (1.0, 300.0),
        [0.0, 0.5],
        dense_output=True,
        rtol=1e-9,
        max_step=0.1,
    )
    rs = np.linspace(80, sol.t[-1], 120)
    Y = sol.sol(rs)
    Q = rs**2 * Y[1]
    Qm = float(np.mean(Q[-30:]))
    phi_inf = float(np.mean(Y[0, -30:] + Qm / rs[-30:]))
    resid = float(np.max(np.abs(Y[0] - (phi_inf - Qm / rs))))
    print(f"  Q_mean={Qm:.6f} phi_inf_est={phi_inf:.6f} max|resid|={resid:.3e}")

    print("\n--- W = 1 inward toward r=0 ---")
    for u0 in [0.0, 0.5, -0.5]:
        sh = integrate_W1(1.0, 0.0, u0, direction="in")
        shots.append(sh)
        print(
            f"  u0={u0:+.1f}: {sh.status:8s} r_end={sh.r_end:.5f} "
            f"phi_end={sh.phi_end:.2f} | {sh.notes}"
        )

    # Observer at r0 with Coulomb: analytic z and ell sample
    print("\n--- W compensated numeric check q=1 r0=1 ---")
    # phi = 1 - 1/r for r>=1, phi(1)=0
    rr = np.linspace(1.0, 100.0, 500)
    phi_c = 1.0 - 1.0 / rr
    ell_c = float(trapezoid(np.exp(phi_c), rr))
    print(f"  phi(100)={phi_c[-1]:.4f} phi_inf=1 ell_to_100={ell_c:.4f} (grows ~e*Delta r)")

    out = {
        "W_compensated": W_comp,
        "Q_mono": qm,
        "W1_shots": [asdict(s) for s in shots],
        "ell_growth": ell_growth,
        "late_fit": {"Q_mean": Qm, "phi_inf_est": phi_inf, "max_resid": resid},
        "scoreboard": {
            "W_e2phi_vacuum": {
                "redshift_out": "YES (q>0)",
                "hard_barrier": "FAIL",
                "z_max": "FINITE",
                "note": "exact Coulomb; open infinity",
            },
            "W_1_vacuum": {
                "redshift_out": "YES (from sample r0=1 after any u0 eventually phi rises)",
                "hard_barrier": "FAIL (ell grows with R; phi approaches finite plateau-ish)",
                "Q_strictly_increasing": True,
                "center": "phi blows as r->0 in samples",
            },
            "provenance": "phi-only on simple metric; not free-D freeze",
        },
    }
    path = "simple_metric_asymptotics_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE")


if __name__ == "__main__":
    main()
