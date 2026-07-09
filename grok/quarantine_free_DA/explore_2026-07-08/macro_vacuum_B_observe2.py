#!/usr/bin/env python3
"""
OBSERVE-2: vacuum B throat family — no polar origin.

Seed at r = r_* with D > 0, D' = 0 (throat), free phi, phi'.
Integrate both outward (r > r_*) and inward (r < r_*) while D stays positive.

Equations (locked W=1):
  d/dr( Z D^2 phi' ) = 4 e^{-2 phi} (D')^2
  d/dr( e^{-2 phi} D' ) = -(Z/4) D (phi')^2

Mode: OBSERVE. No sources. No sky fit.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp

from macro_vacuum_B_observe1 import system_rhs, analytic_structure_report

PREMISES = {
    "W": "1 (option B)",
    "Z": "FREE; representatives {1,4,8}",
    "L_m": "0",
    "seed": "throat D>0, D'=0 at r_*; two-sided IVP",
    "mode": "OBSERVE not TARGET",
    "inherits": "macro_vacuum_B_observe1_results.md polar obstruction",
}


@dataclass
class SideResult:
    direction: str
    status: str
    message: str
    r_start: float
    r_end: float
    n_points: int
    phi_start: float
    phi_end: float
    phi_min: float
    phi_max: float
    D_start: float
    D_end: float
    D_min: float
    D_max: float
    F_start: float
    F_end: float
    G_start: float
    G_end: float
    hit_D_nonpos: bool
    notes: str


@dataclass
class ThroatCase:
    tag: str
    Z: float
    r_star: float
    phi_star: float
    u_star: float  # phi'
    D_star: float
    outward: dict
    inward: dict
    summary: str


def integrate_side(
    Z: float,
    r0: float,
    y0: np.ndarray,
    r_target: float,
    direction: str,
) -> SideResult:
    phi0, u0, D0, v0 = y0
    F0 = float(np.exp(-2 * phi0) * v0)
    G0 = float(D0**2 * u0)

    def fun(r, y):
        return system_rhs(r, y, Z)

    def hit_D(r, y):
        return y[2] - 1e-8

    hit_D.terminal = True
    hit_D.direction = -1

    # also stop if |phi| huge (blow)
    def hit_phi(r, y):
        return 20.0 - abs(y[0])

    hit_phi.terminal = True
    hit_phi.direction = -1

    sol = solve_ivp(
        fun,
        (r0, r_target),
        y0,
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        events=(hit_D, hit_phi),
        max_step=0.05,
        dense_output=False,
    )

    if sol.t.size < 2:
        return SideResult(
            direction=direction,
            status="failed",
            message=str(sol.message),
            r_start=r0,
            r_end=r0,
            n_points=int(sol.t.size),
            phi_start=float(phi0),
            phi_end=float(phi0),
            phi_min=float(phi0),
            phi_max=float(phi0),
            D_start=float(D0),
            D_end=float(D0),
            D_min=float(D0),
            D_max=float(D0),
            F_start=F0,
            F_end=F0,
            G_start=G0,
            G_end=G0,
            hit_D_nonpos=False,
            notes="no steps",
        )

    # Raw solver order (out: r increasing; in: r decreasing)
    t_raw = sol.t
    phi_raw, u_raw, D_raw, v_raw = sol.y
    r_start_raw = float(t_raw[0])
    r_end_raw = float(t_raw[-1])

    # r-increasing order for mono checks and min/max
    if t_raw[0] > t_raw[-1]:
        phi = phi_raw[::-1]
        u = u_raw[::-1]
        D = D_raw[::-1]
        v = v_raw[::-1]
    else:
        phi, u, D, v = phi_raw, u_raw, D_raw, v_raw

    F = np.exp(-2 * phi) * v
    G = D**2 * u
    hit_d = len(sol.t_events[0]) > 0 if sol.t_events else False
    hit_p = len(sol.t_events[1]) > 0 if sol.t_events else False

    notes = []
    dF = np.diff(F)
    dG = np.diff(G)
    if np.all(dF <= 1e-7):
        notes.append("F nonincreasing OK")
    else:
        notes.append(f"F mono viol maxdF={dF.max():.1e}")
    if np.all(dG >= -1e-7):
        notes.append("G nondecreasing OK")
    else:
        notes.append(f"G mono viol mindG={dG.min():.1e}")

    # Trends along increasing r
    if D[-1] > D[0] + 1e-6:
        notes.append("D grows with r")
    elif D[-1] < D[0] - 1e-6:
        notes.append("D shrinks with r")
    else:
        notes.append("D ~flat")

    if phi[-1] > phi[0] + 1e-6:
        notes.append("phi rises with r")
    elif phi[-1] < phi[0] - 1e-6:
        notes.append("phi falls with r")
    else:
        notes.append("phi ~flat")

    # Relative to throat seed: does this side leave with D < D_start?
    if float(np.min(D_raw)) < float(D_raw[0]) - 1e-6:
        notes.append("D drops away from seed")
    if float(np.max(D_raw)) > float(D_raw[0]) + 1e-6:
        notes.append("D rises away from seed")

    if hit_d:
        notes.append("hit D~0")
    if hit_p:
        notes.append("hit |phi| cap")

    if sol.success:
        status = "ok"
    elif hit_d:
        status = "event_D"
    elif hit_p:
        status = "event_phi"
    else:
        status = "stopped"

    return SideResult(
        direction=direction,
        status=status,
        message=str(sol.message),
        r_start=r_start_raw,
        r_end=r_end_raw,
        n_points=int(sol.t.size),
        phi_start=float(phi_raw[0]),
        phi_end=float(phi_raw[-1]),
        phi_min=float(phi.min()),
        phi_max=float(phi.max()),
        D_start=float(D_raw[0]),
        D_end=float(D_raw[-1]),
        D_min=float(D.min()),
        D_max=float(D.max()),
        F_start=float(np.exp(-2 * phi_raw[0]) * v_raw[0]),
        F_end=float(np.exp(-2 * phi_raw[-1]) * v_raw[-1]),
        G_start=float(D_raw[0] ** 2 * u_raw[0]),
        G_end=float(D_raw[-1] ** 2 * u_raw[-1]),
        hit_D_nonpos=bool(hit_d),
        notes="; ".join(notes),
    )


def run_throat(
    tag: str,
    Z: float,
    r_star: float,
    phi_star: float,
    u_star: float,
    D_star: float,
    r_out: float = 5.0,
    r_in: float = 0.05,
) -> ThroatCase:
    # throat: v = D' = 0
    y_star = np.array([phi_star, u_star, D_star, 0.0], dtype=float)

    out = integrate_side(Z, r_star, y_star, r_out, "out")
    inn = integrate_side(Z, r_star, y_star, r_in, "in")

    # summary classification
    bits = []
    if abs(u_star) < 1e-15:
        bits.append("u*=0 exact throat+flat-phi seed")
    else:
        bits.append(f"u*={u_star:g}")

    # At throat with v=0: F=0. FE-D => F' = -(Z/4) D u^2 <= 0
    # So immediately F becomes negative for u!=0 => D' becomes negative (since e^{-2phi}>0)
    # both sides: D decreases away from throat in r? 
    # Actually F' < 0 at throat means as r increases F goes negative => D'<0 outward.
    # Inward (r decreases): integrating opposite — D behavior from notes.

    if out.hit_D_nonpos or out.status == "event_D":
        bits.append("OUT hits D~0")
    elif out.status == "ok":
        bits.append("OUT reaches r_max")
    else:
        bits.append(f"OUT {out.status}")

    if inn.hit_D_nonpos or inn.status == "event_D":
        bits.append("IN hits D~0")
    elif inn.status == "ok":
        bits.append("IN reaches r_min")
    else:
        bits.append(f"IN {inn.status}")

    # D max location
    if out.D_max <= D_star * 1.001 and inn.D_max <= D_star * 1.001:
        bits.append("D*=local max (both sides D drops or flat)")
    elif out.D_max > D_star * 1.01 or inn.D_max > D_star * 1.01:
        bits.append("D exceeds D* on a side")

    return ThroatCase(
        tag=tag,
        Z=Z,
        r_star=r_star,
        phi_star=phi_star,
        u_star=u_star,
        D_star=D_star,
        outward=asdict(out),
        inward=asdict(inn),
        summary="; ".join(bits),
    )


def residual_spotcheck_throat(Z=1.0, r_star=1.0, u_star=0.1, D_star=1.0) -> dict[str, float]:
    y0 = np.array([0.0, u_star, D_star, 0.0])
    sol = solve_ivp(
        lambda r, y: system_rhs(r, y, Z),
        (r_star, r_star + 2.0),
        y0,
        method="DOP853",
        rtol=1e-10,
        atol=1e-12,
        max_step=0.02,
        dense_output=True,
    )
    rs = np.linspace(r_star, sol.t[-1], 150)
    Y = sol.sol(rs)
    phi, u, D, v = Y
    F = np.exp(-2 * phi) * v
    G = D**2 * u
    dF = np.gradient(F, rs)
    dG = np.gradient(G, rs)
    rhs_F = -(Z / 4) * D * u**2
    rhs_G = (4 / Z) * np.exp(-2 * phi) * v**2
    return {
        "max_abs_F_resid": float(np.max(np.abs(dF - rhs_F))),
        "max_abs_G_resid": float(np.max(np.abs(dG - rhs_G))),
        "rel_F": float(np.max(np.abs(dF - rhs_F)) / (np.max(np.abs(rhs_F)) + 1e-15)),
        "rel_G": float(np.max(np.abs(dG - rhs_G)) / (np.max(np.abs(rhs_G)) + 1e-15)),
    }


def throat_series_cas() -> dict[str, Any]:
    """Local expansion at throat: D=D0 + (1/2)D2 (r-r*)^2 + ..., phi = p0 + u0 (r-r*) + ..."""
    import sympy as sp

    s = sp.symbols("s")  # s = r - r*
    Z, D0, p0, u0, D2, p2 = sp.symbols("Z D0 p0 u0 D2 p2", real=True)
    # D = D0 + (1/2) D2 s^2 + ...
    # phi = p0 + u0 s + (1/2) p2 s^2 + ...
    D = D0 + sp.Rational(1, 2) * D2 * s**2
    phi = p0 + u0 * s + sp.Rational(1, 2) * p2 * s**2
    Dp = sp.diff(D, s)
    phip = sp.diff(phi, s)
    # FE-D at s=0: d/ds(e^{-2phi} D') = -(Z/4) D (phi')^2
    F = sp.exp(-2 * phi) * Dp
    lhs_D = sp.series(sp.diff(F, s), s, 0, 1).removeO()
    rhs_D = sp.series(-(Z / 4) * D * phip**2, s, 0, 1).removeO()
    # at s=0: F' = e^{-2p0} D2  (since D'(0)=0, D''(0)=D2) wait
    # D' = D2 s, F = e^{-2phi} D2 s, F'(0) = e^{-2p0} D2
    # rhs(0) = -(Z/4) D0 u0^2
    eq_D2 = sp.simplify(lhs_D.subs(s, 0) - rhs_D.subs(s, 0))
    # FE-phi: (Z D^2 phi')' = 4 e^{-2phi} (D')^2
    Gz = Z * D**2 * phip
    lhs_p = sp.series(sp.diff(Gz, s), s, 0, 2).removeO()
    rhs_p = sp.series(4 * sp.exp(-2 * phi) * Dp**2, s, 0, 2).removeO()
    return {
        "FE-D_at_throat": str(eq_D2),
        "implies_D2": str(sp.solve(eq_D2, D2)),
        "plain": (
            "At throat D'=0: D''(r*) = -(Z/4) D* e^{2 phi*} (phi')^2 <= 0 for Z,D>0. "
            "So if phi'!=0 at throat, D has a LOCAL MAXIMUM (D''<0). "
            "If phi'=0 too, D''=0 (need higher order / trivial)."
        ),
        "FE-phi_series_diff_O_s": str(sp.simplify(lhs_p - rhs_p)),
    }


def main() -> None:
    print("=" * 70)
    print("OBSERVE-2 vacuum B throat family")
    print("=" * 70)
    print(json.dumps(PREMISES, indent=2))

    cas = throat_series_cas()
    print("\n--- Throat local expansion ---")
    for k, v in cas.items():
        print(f"  {k}: {v}")

    print("\n--- Residual spot-check ---")
    print(residual_spotcheck_throat())

    cases: list[ThroatCase] = []
    r_star = 1.0
    D_star = 1.0
    phi_star = 0.0

    grid = []
    for Z in (1.0, 4.0, 8.0):
        grid.append((f"flat_u0_Z{Z:g}", Z, 0.0))
        for u in (0.05, 0.1, 0.2, -0.1):
            grid.append((f"u{u:g}_Z{Z:g}", Z, u))

    print("\n--- Two-sided throat IVPs ---")
    for tag, Z, u in grid:
        tc = run_throat(tag, Z, r_star, phi_star, u, D_star, r_out=5.0, r_in=0.05)
        cases.append(tc)
        o, i = tc.outward, tc.inward
        print(
            f"  {tc.tag:16s} | {tc.summary}\n"
            f"      OUT: {o['status']:10s} r->{o['r_end']:.3f} "
            f"phi[{o['phi_min']:.3f},{o['phi_max']:.3f}] D[{o['D_min']:.3f},{o['D_max']:.3f}] | {o['notes']}\n"
            f"      IN:  {i['status']:10s} r->{i['r_end']:.3f} "
            f"phi[{i['phi_min']:.3f},{i['phi_max']:.3f}] D[{i['D_min']:.3f},{i['D_max']:.3f}] | {i['notes']}"
        )

    # Extra: vary D_star
    print("\n--- D_star variation (Z=1, u=0.1) ---")
    dvar = []
    for Ds in (0.5, 1.0, 2.0):
        tc = run_throat(f"Ds{Ds:g}", 1.0, r_star, 0.0, 0.1, Ds, r_out=4.0, r_in=0.05)
        dvar.append(tc)
        print(f"  {tc.tag}: {tc.summary}")

    out = {
        "premises": PREMISES,
        "structure": analytic_structure_report(),
        "throat_cas": cas,
        "residual": residual_spotcheck_throat(),
        "cases": [asdict(c) for c in cases],
        "D_star_var": [asdict(c) for c in dvar],
    }
    path = "macro_vacuum_B_observe2_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE OBSERVE-2")


if __name__ == "__main__":
    main()
