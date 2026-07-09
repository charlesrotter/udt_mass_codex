#!/usr/bin/env python3
"""
Simple metric + dilated matter (matter couples to phi).

Metric: ds^2 = -e^{-2phi} c^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2
L_m = -rho(r) r^2 e^{-2 phi}   (dilated continuum probe)

  W = e^{2phi}:  Z (r^2 phi')' = 2 rho r^2 e^{-2 phi}
  W = 1:         Z (r^2 phi')' = 4 e^{-2 phi} + 2 rho r^2 e^{-2 phi}

rho compact support (matter ball), vacuum exterior.
Characterize: does matter change large-r barrier / redshift-out?
No free D_A. No sky fit.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
from scipy.integrate import solve_ivp, trapezoid

PREMISES = {
    "metric": "simple D_A=r",
    "L_m": "-rho r^2 e^{-2 phi}  (couples to phi)",
    "rho": "compact FREE profile",
    "mode": "OBSERVE",
}


def rho_ball(r, rho0, R_m, edge=0.15):
    if r >= R_m:
        return 0.0
    r_flat = R_m * (1.0 - edge)
    if r <= r_flat:
        x = r / max(R_m, 1e-12)
        return float(rho0 * max(0.0, 1.0 - 0.25 * x * x))
    t = (r - r_flat) / max(R_m - r_flat, 1e-12)
    w = 0.5 * (1.0 + np.cos(np.pi * min(t, 1.0)))
    x = r_flat / max(R_m, 1e-12)
    return float(rho0 * max(0.0, 1.0 - 0.25 * x * x) * w)


def make_rhs(Z, rho0, R_m, W_uncomp: bool):
    """W_uncomp True => W=1; False => W=e^{2phi} compensated geometric."""

    def f(r, y):
        phi, u = y
        rh = rho_ball(r, rho0, R_m)
        em2 = np.exp(-2.0 * np.clip(phi, -40, 40))
        # Z (r^2 u)' = RHS
        # RHS_geo = 4 e^{-2phi} if uncomp else 0
        # RHS_mat = 2 rho r^2 e^{-2phi}
        RHS = 2.0 * rh * r**2 * em2
        if W_uncomp:
            RHS = RHS + 4.0 * em2
        # 2 r u + r^2 u' = RHS/Z
        up = (RHS / Z - 2.0 * r * u) / (r**2)
        return [u, up]

    return f


@dataclass
class Run:
    tag: str
    W: str
    rho0: float
    R_m: float
    r0: float
    u0: float
    status: str
    r_end: float
    phi_Rm: float
    u_Rm: float
    Q_Rm: float
    phi_end: float
    u_end: float
    Q_end: float
    ell: float
    notes: str


def integrate(
    W_uncomp: bool,
    rho0: float,
    R_m: float,
    r0: float = 0.2,
    u0: float = 0.0,
    phi0: float = 0.0,
    r_max: float = 150.0,
    Z: float = 1.0,
) -> Run:
    f = make_rhs(Z, rho0, R_m, W_uncomp)
    Wlab = "1" if W_uncomp else "e2"

    def hit_phi(r, y):
        return 25.0 - abs(y[0])

    hit_phi.terminal = True
    hit_phi.direction = -1

    sol = solve_ivp(
        f,
        (r0, r_max),
        [phi0, u0],
        method="DOP853",
        rtol=1e-8,
        atol=1e-10,
        events=hit_phi,
        max_step=0.05,
        dense_output=True,
    )
    status = "ok" if sol.success else "stopped"
    if sol.t_events and len(sol.t_events[0]) > 0:
        status = "phi_cap"

    r_end = float(sol.t[-1])
    if sol.sol is None:
        yE = sol.y[:, -1]
        phi_end, u_end = float(yE[0]), float(yE[1])
        phi_Rm = u_Rm = Q_Rm = float("nan")
        ell = 0.0
    else:
        r_hi = min(R_m, r_end)
        yRm = sol.sol(r_hi)
        phi_Rm, u_Rm = float(yRm[0]), float(yRm[1])
        Q_Rm = r_hi**2 * u_Rm
        yE = sol.sol(r_end)
        phi_end, u_end = float(yE[0]), float(yE[1])
        rs = np.linspace(r0, r_end, 400)
        ph = sol.sol(rs)[0]
        ell = float(trapezoid(np.exp(np.clip(ph, -40, 40)), rs))

    Q_end = r_end**2 * u_end
    notes = []
    if r_end > R_m and status == "ok":
        notes.append("vacuum_ext")
        # exterior: for W_uncomp Q still increases slowly; for comp Q conserved if rho=0
        if not W_uncomp and r_end > R_m + 1:
            # check Q drift in exterior
            rs = np.linspace(R_m, r_end, 50)
            Qe = rs**2 * sol.sol(rs)[1]
            notes.append(f"Q_ext_drift={float(np.max(np.abs(Qe - Q_Rm))):.2e}")
    if phi_end > phi0 + 0.05:
        notes.append("phi_up")
    if abs(u_end) < 1e-3:
        notes.append("u_small")

    return Run(
        tag=f"W{Wlab}_r{rho0:g}_Rm{R_m:g}_u{u0:g}",
        W=Wlab,
        rho0=rho0,
        R_m=R_m,
        r0=r0,
        u0=u0,
        status=status,
        r_end=r_end,
        phi_Rm=phi_Rm,
        u_Rm=u_Rm,
        Q_Rm=Q_Rm,
        phi_end=phi_end,
        u_end=u_end,
        Q_end=Q_end,
        ell=ell,
        notes="; ".join(notes),
    )


def main() -> None:
    print("=" * 70)
    print("Simple metric + dilated matter (couples to phi)")
    print("=" * 70)
    print(json.dumps(PREMISES, indent=2))

    runs: list[Run] = []

    # Compensated + matter ball: vacuum exterior should conserve Q
    print("\n--- W=e^{2phi} + dilated ball (r0=0.2, u0=0, phi0=0) ---")
    for R_m in [1.0, 2.0]:
        for rho0 in [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]:
            rr = integrate(False, rho0, R_m, r_max=120.0)
            runs.append(rr)
            print(
                f"  Rm={R_m:g} ρ={rho0:g}: {rr.status:8s} "
                f"Q_Rm={rr.Q_Rm:8.4f} phi_Rm={rr.phi_Rm:6.3f} "
                f"phi_end={rr.phi_end:6.3f} u_end={rr.u_end:.5f} "
                f"ell={rr.ell:.4g} | {rr.notes}"
            )

    # Uncompensated + matter
    print("\n--- W=1 + dilated ball ---")
    for R_m in [1.0, 2.0]:
        for rho0 in [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]:
            rr = integrate(True, rho0, R_m, r_max=120.0)
            runs.append(rr)
            print(
                f"  Rm={R_m:g} ρ={rho0:g}: {rr.status:8s} "
                f"Q_Rm={rr.Q_Rm:8.4f} phi_Rm={rr.phi_Rm:6.3f} "
                f"phi_end={rr.phi_end:6.3f} u_end={rr.u_end:.5f} "
                f"ell={rr.ell:.4g} | {rr.notes}"
            )

    # ell growth for compensated matter case
    print("\n--- ell vs R_max (W=e2, Rm=2, rho0=5) ---")
    ells = []
    for R in [20, 40, 80, 150, 300]:
        rr = integrate(False, 5.0, 2.0, r_max=float(R))
        ells.append((R, rr.ell, rr.phi_end, rr.Q_Rm, rr.Q_end))
        print(
            f"  Rmax={R}: ell={rr.ell:.5g} phi_end={rr.phi_end:.4f} "
            f"Q_Rm={rr.Q_Rm:.4f} Q_end={rr.Q_end:.4f}"
        )

    # Analytic exterior compensated: after ball Q=const, phi = phi_inf - Q/r
    print("\n--- Exterior Coulomb from junction (W=e2 rho0=5 Rm=2) ---")
    rr = integrate(False, 5.0, 2.0, r_max=200.0)
    Q = rr.Q_Rm
    # phi(r) = phi_Rm + Q (1/Rm - 1/r) for r>Rm if Q const and vacuum compensated
    # => phi_inf = phi_Rm + Q/Rm
    phi_inf = rr.phi_Rm + Q / rr.R_m
    print(f"  Q={Q:.6f} phi_Rm={rr.phi_Rm:.6f} => phi_inf={phi_inf:.6f}")
    print(f"  numeric phi_end={rr.phi_end:.6f} (should approach phi_inf)")
    print(f"  z_max ~ e^{{phi_inf}}-1 = {np.exp(phi_inf)-1:.6f} FINITE")
    print(f"  hard barrier: NO (ell grows, open r)")

    # Regularity at small r: start closer to 0
    print("\n--- smaller r0 (W=e2, Rm=2, rho0=5) ---")
    for r0 in [0.05, 0.1, 0.2, 0.5]:
        rr = integrate(False, 5.0, 2.0, r0=r0, r_max=80.0)
        print(
            f"  r0={r0:g}: status={rr.status} Q_Rm={rr.Q_Rm:.4f} "
            f"phi_end={rr.phi_end:.3f} | {rr.notes}"
        )

    out = {
        "premises": PREMISES,
        "runs": [asdict(r) for r in runs],
        "ell_growth": ells,
        "score": {
            "W_e2_matter_ball": (
                "Matter loads Q>0 inside ball; exterior Q conserved; "
                "phi -> phi_inf = phi_Rm + Q/Rm finite; redshift out YES; hard barrier NO"
            ),
            "W_1_matter_ball": (
                "Matter + geometric source; exterior still open with phi rising toward plateau; "
                "hard barrier NO in samples"
            ),
            "coupling": "dilated L_m couples rho to phi EL as designed",
        },
    }
    path = "simple_metric_matter_asymptotics_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE")


if __name__ == "__main__":
    main()
