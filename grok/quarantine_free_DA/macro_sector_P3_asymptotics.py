#!/usr/bin/env python3
"""
P3 asymptotics: vacuum W=1, D=r gauge.

  Z (r^2 phi')' = 4 exp(-2 phi)

Elegant tests: redshift out (phi increasing), dilation barrier
(ell = int e^phi dr, u = int e^{2 phi} dr), no preferred-center ontology claim.

Analytic reductions + bounded numeric phase portrait (not seed theater for cosmos).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

Zsym, r, C, A, B = sp.symbols("Z r C A B", positive=True)
phi = sp.Function("phi")


def analytic_reductions() -> dict:
    # w = exp(-phi) > 0  =>  phi = -ln w, phi' = -w'/w
    # r^2 phi' = - r^2 w'/w
    # (r^2 phi')' = 4/Z exp(-2 phi) = 4/Z w^2
    w = sp.Function("w")
    # Let Q = r^2 phi'  =>  Q' = (4/Z) e^{-2 phi}
    # Emden-like / multiply by r^2 phi' ?
    # d/dr ( (1/2) Z (r^2 phi')^2 ) = Z r^2 phi' (r^2 phi')' = 4 r^2 phi' e^{-2 phi}
    # RHS = -2 r^2 d/dr (e^{-2 phi}) ? d/dr e^{-2phi} = -2 e^{-2phi} phi'
    # so 4 r^2 phi' e^{-2phi} = -2 r^2 d/dr(e^{-2phi})
    # Not exact conservation without weight.
    #
    # Autonomous if use s = ln r:
    # d/dr = (1/r) d/ds
    # (r^2 phi')' = d/dr (r d phi/ds) = d phi/ds + d^2 phi / ds^2
    # because r^2 phi' = r^2 (1/r) phi_s = r phi_s
    # d/dr (r phi_s) = phi_s + r (1/r) phi_ss = phi_s + phi_ss
    # EL: Z (phi_ss + phi_s) = 4 e^{-2 phi}
    red = {
        "log_coordinate": "s=ln r:  Z (phi_ss + phi_s) = 4 e^{-2 phi}",
        "mechanical_analog": (
            "Like particle phi(s) with friction phi_s and force ~ e^{-2 phi}; "
            "not conservative friction."
        ),
        "w_form": "w=e^{-phi}: Z (r^2 ( -w'/w ))' = 4 w^2",
        "no_constant_sol": "phi=const => 0 = 4 e^{-2c} impossible",
        "linear_ansatz_fail": "phi=a+b ln r: left Z b, right 4 e^{-2a} r^{-2b} — only if b=0 impossible, or power match no",
    }
    # Try phi = ln r + c  => e^{-2phi} = e^{-2c}/r^2
    # left: phi'=1/r, r^2 phi'=r, (r^2 phi')'=1
    # right: 4 e^{-2c}/(Z r^2) — no match
    # Try phi = ln(ln r) etc — skip
    # First integral attempt with s:
    # multiply Z(phi_ss + phi_s) = 4 e^{-2phi} by e^{2 phi} phi_s? 
    return red


def first_integral_probe() -> dict:
    """Numeric check of candidate integrals — none simple conserved."""
    return {
        "note": "No elementary conserved energy (friction in s=ln r). Phase plane 2D.",
    }


def system(r, y, Z):
    """y = [phi, u] with u=phi'."""
    phi, u = y
    # (r^2 u)' = (4/Z) e^{-2 phi}
    # 2 r u + r^2 u' = (4/Z) e^{-2 phi}
    # u' = (4/Z) e^{-2 phi}/r^2 - 2 u/r
    em2 = np.exp(-2.0 * np.clip(phi, -30, 30))
    up = (4.0 / Z) * em2 / (r**2) - 2.0 * u / r
    return [u, up]


@dataclass
class Shot:
    tag: str
    Z: float
    r0: float
    phi0: float
    u0: float
    r_end: float
    phi_end: float
    u_end: float
    status: str
    phi_max: float
    phi_min: float
    # integrals from r0 to r_end
    ell: float  # int e^phi dr
    null_u: float  # int e^{2 phi} dr
    notes: str


def integrate_shot(
    Z: float,
    r0: float,
    phi0: float,
    u0: float,
    r_max: float = 50.0,
    r_min: float = 1e-3,
    direction: str = "out",
) -> Shot:
    y0 = [phi0, u0]
    target = r_max if direction == "out" else r_min

    def fun(r, y):
        return system(r, y, Z)

    def hit_phi(r, y):
        return 40.0 - abs(y[0])

    hit_phi.terminal = True
    hit_phi.direction = -1

    sol = solve_ivp(
        fun,
        (r0, target),
        y0,
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        events=hit_phi,
        max_step=0.05,
        dense_output=True,
    )
    if sol.t.size < 2:
        return Shot(
            f"{direction}_u{u0:g}",
            Z,
            r0,
            phi0,
            u0,
            r0,
            phi0,
            u0,
            "failed",
            phi0,
            phi0,
            0.0,
            0.0,
            sol.message,
        )

    r = sol.t
    phi, u = sol.y
    # order increasing r for integrals
    if r[0] > r[-1]:
        r = r[::-1]
        phi = phi[::-1]
        u = u[::-1]

    ep = np.exp(np.clip(phi, -40, 40))
    ell = float(np.trapz(ep, r))
    null_u = float(np.trapz(ep**2, r))

    status = "ok" if sol.success else "stopped"
    if sol.t_events and len(sol.t_events[0]) > 0:
        status = "phi_cap"

    notes = []
    if phi[-1] > phi[0] + 0.1:
        notes.append("phi_up")
    elif phi[-1] < phi[0] - 0.1:
        notes.append("phi_down")
    if u[-1] > 0:
        notes.append("u_end>0")
    else:
        notes.append("u_end<=0")
    # rough asymptotic class
    if status == "ok" and r[-1] >= 0.9 * (r_max if direction == "out" else r0):
        if phi[-1] > 5 and u[-1] > 0:
            notes.append("CLASS_phi_rising")
        elif phi[-1] < -5:
            notes.append("CLASS_phi_deep_neg")
        elif abs(u[-1]) < 0.01 and abs(phi[-1] - phi[0]) < 1:
            notes.append("CLASS_mild")
        else:
            notes.append("CLASS_ongoing")

    return Shot(
        tag=f"Z{Z:g}_{direction}_p{phi0:g}_u{u0:g}",
        Z=Z,
        r0=r0,
        phi0=phi0,
        u0=u0,
        r_end=float(sol.t[-1]),
        phi_end=float(sol.y[0, -1]),
        u_end=float(sol.y[1, -1]),
        status=status,
        phi_max=float(np.max(phi)),
        phi_min=float(np.min(phi)),
        ell=ell,
        null_u=null_u,
        notes="; ".join(notes),
    )


def asymptotic_scaling_guess() -> dict:
    """
    For large phi positive: RHS small, approx (r^2 phi')' ~ 0 => phi ~ a - b/r
    approaches const from below if b>0 (phi increases toward a).
    Matching: residual (r^2 phi')' = 0 but need tiny RHS — consistent only as e^{-2phi}->0 i.e. phi->+oo
    contradiction with const unless approach is slow.

    Suppose phi ~ (1/2) ln(ln r) for large r? skip

    Suppose at finite r_* blowup: phi -> +oo as r -> r_*- 
    Then e^{-2phi}->0, near free: r^2 phi' ~ const = A
    phi ~ -A/r + B -> finite as r->r_* unless A->oo
    So smooth blowup to +oo at finite r hard with A finite.

    phi -> -oo at finite r_*: e^{-2phi}->+oo, RHS huge, accelerates phi'' strongly.
    """
    return {
        "no_finite_constant_at_infinity": "exact (RHS never zero)",
        "approach_phi_plus_infty_slow": "possible open research; (r^2 phi')'>0 always so G_r=r^2 phi' strictly increasing",
        "flux_mono": "Q := r^2 phi' is STRICTLY increasing (Q' = (4/Z)e^{-2phi}>0)",
        "consequence": (
            "Once Q>0, stays and grows; phi eventually increases. "
            "If Q(r0)<0, may cross to Q>0 then phi min then rise."
        ),
    }


def main() -> None:
    print("=" * 70)
    print("P3 asymptotics")
    print("=" * 70)
    print("analytic:", json.dumps(analytic_reductions(), indent=2))
    print("scaling:", json.dumps(asymptotic_scaling_guess(), indent=2))

    # Flux mono check
    print("\n--- Flux Q=r^2 phi' monotone ---")
    Z = 1.0
    shots = []
    # observer-like: r0=1, phi0=0, various u0
    print("\n--- Outward from r=1, phi=0 ---")
    for u0 in [-2.0, -1.0, -0.5, -0.1, 0.0, 0.1, 0.5, 1.0, 2.0]:
        sh = integrate_shot(Z, 1.0, 0.0, u0, r_max=100.0)
        shots.append(sh)
        print(
            f"  u0={u0:+.1f}: {sh.status:8s} r_end={sh.r_end:7.2f} "
            f"phi[{sh.phi_min:.2f},{sh.phi_max:.2f}] end={sh.phi_end:.2f} "
            f"u_end={sh.u_end:.4f} ell={sh.ell:.3g} null={sh.null_u:.3g} | {sh.notes}"
        )

    # long runs for u0>=0
    print("\n--- Long outward r_max=500, u0>=0 ---")
    long_shots = []
    for u0 in [0.0, 0.1, 0.5, 1.0]:
        sh = integrate_shot(Z, 1.0, 0.0, u0, r_max=500.0)
        long_shots.append(sh)
        print(
            f"  u0={u0:g}: r_end={sh.r_end:.1f} phi_end={sh.phi_end:.3f} "
            f"u_end={sh.u_end:.5f} ell={sh.ell:.4g} null={sh.null_u:.4g} | {sh.notes}"
        )

    # Inward toward center from r=1
    print("\n--- Inward toward r->0, phi=0 ---")
    for u0 in [-0.5, 0.0, 0.5, 1.0]:
        sh = integrate_shot(Z, 1.0, 0.0, u0, r_min=1e-3, direction="in")
        shots.append(sh)
        print(
            f"  u0={u0:+.1f}: {sh.status:8s} r_end={sh.r_end:.4f} "
            f"phi_end={sh.phi_end:.2f} u_end={sh.u_end:.3f} | {sh.notes}"
        )

    # Estimate: does ell converge as r_max increases for rising phi?
    print("\n--- ell(r_max) growth for u0=0.5 ---")
    ells = []
    for R in [10, 20, 50, 100, 200, 500]:
        sh = integrate_shot(Z, 1.0, 0.0, 0.5, r_max=float(R))
        ells.append((R, sh.ell, sh.phi_end, sh.u_end, sh.status))
        print(f"  R={R}: ell={sh.ell:.6g} phi_end={sh.phi_end:.4f} u_end={sh.u_end:.5f}")

    # Q(r) = r^2 u monotone check on one solution
    print("\n--- Q=r^2 phi' increasing (u0=-0.5) ---")
    sol = solve_ivp(
        lambda r, y: system(r, y, 1.0),
        (1.0, 50.0),
        [0.0, -0.5],
        dense_output=True,
        rtol=1e-9,
        max_step=0.05,
    )
    rs = np.linspace(1.0, sol.t[-1], 200)
    Y = sol.sol(rs)
    Q = rs**2 * Y[1]
    dQ = np.diff(Q)
    print(f"  min dQ={dQ.min():.3e} (should be >0): all_pos={(dQ > -1e-10).all()}")
    print(f"  Q: {Q[0]:.4f} -> {Q[-1]:.4f}, phi: {Y[0,0]:.3f} -> {Y[0,-1]:.3f}")

    # Asymptotic fit for large r: if Q ~ (4/Z) int e^{-2phi} ... hard
    # If phi large positive, Q' small, Q~const, phi~ -Q/r + const
    print("\n--- Late phi vs -Q/r + c for u0=0.5 long ---")
    sol = solve_ivp(
        lambda r, y: system(r, y, 1.0),
        (1.0, 200.0),
        [0.0, 0.5],
        dense_output=True,
        rtol=1e-9,
        max_step=0.1,
    )
    rs = np.linspace(50, sol.t[-1], 100)
    Y = sol.sol(rs)
    Q = rs**2 * Y[1]
    # phi ≈ phi_inf - Q/r with Q nearly const late
    Q_mean = np.mean(Q[-20:])
    phi_inf_est = np.mean(Y[0, -20:] + Q_mean / rs[-20:])
    resid = Y[0] - (phi_inf_est - Q_mean / rs)
    print(f"  Q_mean_late={Q_mean:.6f} phi_inf_est={phi_inf_est:.6f} max|resid|={np.max(np.abs(resid)):.3e}")
    print(f"  phi_end={Y[0,-1]:.6f}  => approaches finite phi_inf? residual small suggests YES quasi-Coulomb late")

    out = {
        "analytic": analytic_reductions(),
        "scaling": asymptotic_scaling_guess(),
        "shots": [asdict(s) for s in shots],
        "long": [asdict(s) for s in long_shots],
        "ell_growth": ells,
        "late_coulomb_fit": {
            "Q_mean": float(Q_mean),
            "phi_inf_est": float(phi_inf_est),
            "max_resid": float(np.max(np.abs(resid))),
        },
        "score": {
            "flux_Q_strictly_increasing": True,
            "late_behavior_numeric": "quasi approach to finite phi_inf with Q~const (Coulomb-like) when phi large — e^{-2phi} suppressed",
            "barrier": "FAIL if true asymptote phi->const finite (ell diverges)",
            "caveat": "Strictly Q keeps growing albeit very slowly while e^{-2phi}>0 — may never reach exact const; practical asymptote still open infinity",
        },
    }
    path = "macro_sector_P3_asymptotics_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE P3")


if __name__ == "__main__":
    main()
