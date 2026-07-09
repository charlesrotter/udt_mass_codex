#!/usr/bin/env python3
"""
OBSERVE-5: (b) discrete symmetries / chart conventions for ±u;
           (a) sharper asymptotics on long-lived (u*<0) branch.

Vacuum B only. OBSERVE mode.
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
    "prior": "O4: +u pinches, -u long-lived",
}


# ---------------------------------------------------------------------------
# 5b: symmetries
# ---------------------------------------------------------------------------
def cas_symmetries() -> dict:
    r = sp.symbols("r", positive=True)
    Z = sp.symbols("Z", positive=True)
    phi = sp.Function("phi")
    D = sp.Function("D")
    ph, Dp = phi(r), D(r)
    FE_phi = sp.diff(Z * Dp**2 * sp.diff(ph, r), r) - 4 * sp.exp(-2 * ph) * sp.diff(Dp, r) ** 2
    FE_D = sp.diff(sp.exp(-2 * ph) * sp.diff(Dp, r), r) + (Z / 4) * Dp * sp.diff(ph, r) ** 2

    # Map 1: phi -> -phi (same D, r)
    FE_phi_m = sp.simplify(
        FE_phi.subs(ph, -ph).doit().rewrite(sp.exp)
    )
    # Actually subs on Function: use replace
    FE_phi_flip = FE_phi.xreplace({ph: -ph})
    # better explicit
    phim = -phi(r)
    FE_phi_at_flip = sp.diff(Z * Dp**2 * sp.diff(phim, r), r) - 4 * sp.exp(-2 * phim) * sp.diff(Dp, r) ** 2
    FE_D_at_flip = sp.diff(sp.exp(-2 * phim) * sp.diff(Dp, r), r) + (Z / 4) * Dp * sp.diff(phim, r) ** 2
    FE_phi_at_flip = sp.simplify(FE_phi_at_flip)
    FE_D_at_flip = sp.simplify(FE_D_at_flip)

    # Original FE_phi at phi: L = (Z D^2 phi')' - 4 e^{-2phi} (D')^2
    # At -phi: (Z D^2 (-phi')') - 4 e^{2phi} (D')^2 = -(Z D^2 phi')' - 4 e^{2phi} (D')^2
    # Not proportional to original unless e factors match.

    # Map 2: r -> -s, define Psi(s)=phi(-s), Delta(s)=D(-s)
    # Then d/dr = -d/ds, so phi'_r = -Psi'_s, etc.
    s = sp.symbols("s")
    Psi = sp.Function("Psi")
    Delta = sp.Function("Delta")
    # FE in s: replace d/dr -> -d/ds, phi(r)->Psi(s), D->Delta
    # (Z D^2 phi_r)' _r = 4 e^{-2phi} (D_r)^2
    # Left: d/dr(Z D^2 phi_r) = (-d/ds)(Z Delta^2 (-Psi_s)) = (-d/ds)(-Z Delta^2 Psi_s) = d/ds(Z Delta^2 Psi_s)
    # Right: 4 e^{-2Psi} ( - Delta_s )^2 = 4 e^{-2Psi} (Delta_s)^2
    # So FE-phi form IDENTICAL in s for (Psi, Delta).
    # FE-D: d/dr(e^{-2phi} D_r) = -(Z/4) D (phi_r)^2
    # LHS: (-d/ds)(e^{-2Psi} (-Delta_s)) = (-d/ds)(-e^{-2Psi} Delta_s) = d/ds(e^{-2Psi} Delta_s)
    # RHS: -(Z/4) Delta ( -Psi_s )^2 = -(Z/4) Delta (Psi_s)^2
    # So d/ds(e^{-2Psi} Delta_s) = -(Z/4) Delta (Psi_s)^2 — IDENTICAL form.

    return {
        "phi_to_minus_phi": {
            "invariant": False,
            "reason": (
                "e^{-2phi} in both FE breaks phi -> -phi. "
                "FE-phi at -phi is -(Z D^2 phi')' - 4 e^{+2phi}(D')^2, not a multiple of original residual."
            ),
            "FE_D_note": "FE-D has e^{-2phi} on flux and (phi')^2; (phi')^2 even but weight e^{-2phi} flips to e^{+2phi}.",
        },
        "r_to_minus_r": {
            "invariant": True,
            "reason": (
                "Reparametrization r=-s maps solutions to solutions of the SAME equations. "
                "It flips the sign of both phi' and D' at corresponding points. "
                "A throat with u*>0 integrated to +r is the same geometry as u*<0 if one "
                "reads the chart in the opposite radial direction — BUT only if the GLOBAL "
                "solution is extended both ways; the ASYMMETRIC fate (+pinch vs -long) "
                "is about the TWO SIDES of the throat, not a global phi flip."
            ),
            "careful": (
                "At a throat D'=0, reversing r sends outward to what was inward. "
                "O4 found: from throat, the +r direction with u*>0 pinches, while +r with u*<0 long-lives; "
                "inward (smaller r) was mild for both. So the pinching side is the side toward which "
                "phi INCREASES (G and F dynamics with e^{2phi}). Not removable by global phi->-phi."
            ),
        },
        "combined_phi_flip_and_need_different_eq": (
            "To restore invariance one would need e^{+2phi} weights (different theory), not chart alone."
        ),
    }


def numeric_phi_flip_residual(Z=1.0, u=0.1) -> dict:
    """Take solution with +u; evaluate residual of equations at ( -phi, D )."""
    sol = solve_ivp(
        lambda r, y: system_rhs(r, y, Z),
        (1.0, 6.0),
        [0.0, u, 1.0, 0.0],
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        dense_output=True,
        max_step=0.05,
    )
    rs = np.linspace(1.0, min(5.0, sol.t[-1] - 1e-6), 80)
    Y = sol.sol(rs)
    phi, uu, D, v = Y
    # Original residual via flux derivatives
    F = np.exp(-2 * phi) * v
    G = D**2 * uu
    dF = np.gradient(F, rs)
    dG = np.gradient(G, rs)
    res_F = dF - (-(Z / 4) * D * uu**2)
    res_G = dG - ((4 / Z) * np.exp(2 * phi) * F**2)  # G' = (4/Z) e^{2phi} F^2

    # Flipped field: phi_f = -phi, u_f = -uu, D same, v same
    phi_f, u_f = -phi, -uu
    F_f = np.exp(-2 * phi_f) * v  # e^{2phi} v
    G_f = D**2 * u_f
    dF_f = np.gradient(F_f, rs)
    dG_f = np.gradient(G_f, rs)
    res_F_f = dF_f - (-(Z / 4) * D * u_f**2)
    res_G_f = dG_f - ((4 / Z) * np.exp(2 * phi_f) * F_f**2)

    return {
        "orig_max_rel_res_F": float(np.max(np.abs(res_F)) / (np.max(np.abs(dF)) + 1e-15)),
        "orig_max_rel_res_G": float(np.max(np.abs(res_G)) / (np.max(np.abs(dG)) + 1e-15)),
        "flip_max_rel_res_F": float(np.max(np.abs(res_F_f)) / (np.max(np.abs(dF_f)) + 1e-12)),
        "flip_max_rel_res_G": float(np.max(np.abs(res_G_f)) / (np.max(np.abs(dG_f)) + 1e-12)),
        "conclusion": (
            "Flipped ( -phi, D ) has large residual — not a solution of the same FE."
            if np.max(np.abs(res_F_f)) > 1e-3
            else "unexpected small residual"
        ),
    }


def numeric_r_reverse_match(Z=1.0, u=0.1) -> dict:
    """
    Integrate +u outward from throat; integrate -u inward from throat
    (or +u with decreasing r). Compare D(r) and phi profiles after reflection.
    """
    # Outward +u: r from 1 to 5
    sol_out = solve_ivp(
        lambda r, y: system_rhs(r, y, Z),
        (1.0, 5.0),
        [0.0, u, 1.0, 0.0],
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        dense_output=True,
        max_step=0.05,
    )
    # Inward with same +u: r from 1 to 0.2 — this is the "other side"
    sol_in = solve_ivp(
        lambda r, y: system_rhs(r, y, Z),
        (1.0, 0.2),
        [0.0, u, 1.0, 0.0],
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        dense_output=True,
        max_step=0.05,
    )
    # Outward with -u
    sol_m = solve_ivp(
        lambda r, y: system_rhs(r, y, Z),
        (1.0, 5.0),
        [0.0, -u, 1.0, 0.0],
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        dense_output=True,
        max_step=0.05,
    )

    # Reflection map: profile on inward side at distance x from throat
    # should match outward -u at distance x? 
    # At throat: +u means phi increases with r.
    # Point r = 1+x on +u out: phi > 0.
    # Point r = 1-x on +u in: phi < 0 (if continuous phi'~u).
    # Point r = 1+x on -u out: phi < 0.
    # Compare D(1+x)|_{+u out} vs D(1-x)|_{+u in} — r-reflection of SAME solution
    xs = np.linspace(0.0, 0.8, 40)
    Dout = sol_out.sol(1.0 + xs)[2]
    Din = sol_in.sol(1.0 - xs)[2]
    phi_out = sol_out.sol(1.0 + xs)[0]
    phi_in = sol_in.sol(1.0 - xs)[0]
    # Same connected solution reflected: D should match; phi(1+x) vs -phi(1-x) if odd about throat?
    # For linear phi=u(r-1), phi(1+x)=u x, phi(1-x)=-u x, so phi_out vs -phi_in
    err_D_reflect = float(np.max(np.abs(Dout - Din)))
    err_phi_odd = float(np.max(np.abs(phi_out + phi_in)))

    # Is -u outward the same as +u inward re-labeled?
    # Map inward solution to outward chart: s=2-r maps r=1-x to s=1+x
    # Psi(s) = phi_in(2-s), Delta(s) = D_in(2-s)
    # Compare to -u outward... actually compare +u inward reflected to -u out
    D_m = sol_m.sol(1.0 + xs)[2]
    phi_m = sol_m.sol(1.0 + xs)[0]
    err_D_mu_vs_in = float(np.max(np.abs(D_m - Din)))
    err_phi_mu_vs_neg_in = float(np.max(np.abs(phi_m - (-phi_in))))  # ?

    return {
        "same_solution_D_symmetric_about_throat": err_D_reflect,
        "same_solution_phi_odd_about_throat": err_phi_odd,
        "note_D_symmetry": (
            "If err_D small: D is even about throat on a single +u solution (both sides)."
        ),
        "D_err_+u_out_vs_+u_in_reflected": err_D_reflect,
        "phi_err_odd": err_phi_odd,
        "D_err_-u_out_vs_+u_in": err_D_mu_vs_in,
        "plain": (
            "Single solution with u*>0 has TWO radial sides: one toward increasing phi, one decreasing. "
            "O4 pinch is on the increasing-phi side. The -u outward run is the decreasing-phi side "
            "of an oppositely oriented seed — related by r-reflection of the SAME local jet only if "
            "D is even and phi odd; check errors."
        ),
    }


# ---------------------------------------------------------------------------
# 5a: asymptotics for u* < 0
# ---------------------------------------------------------------------------
@dataclass
class AsymRun:
    Z: float
    u: float
    r_max: float
    r_end: float
    D_end: float
    phi_end: float
    u_end: float
    v_end: float
    F_end: float
    G_end: float
    # late-window averages
    D_mean_last: float
    D_std_last: float
    u_mean_last: float
    v_mean_last: float
    dphi_dr_times_r_mean: float  # if ~const => log
    notes: str


def asym_run(Z: float, u: float, r_max: float = 500.0) -> AsymRun:
    sol = solve_ivp(
        lambda r, y: system_rhs(r, y, Z),
        (1.0, r_max),
        [0.0, u, 1.0, 0.0],
        method="DOP853",
        rtol=1e-8,
        atol=1e-10,
        max_step=0.25,
        dense_output=True,
        events=(
            lambda r, y: y[2] - 1e-8,  # D
        ),
    )
    # fix event attributes
    return _asym_from_sol(Z, u, r_max, sol)


def _asym_from_sol(Z, u, r_max, sol) -> AsymRun:
    # re-integrate with proper events
    def hit_D(r, y):
        return y[2] - 1e-8

    hit_D.terminal = True
    hit_D.direction = -1
    sol = solve_ivp(
        lambda r, y: system_rhs(r, y, Z),
        (1.0, r_max),
        [0.0, u, 1.0, 0.0],
        method="DOP853",
        rtol=1e-8,
        atol=1e-10,
        max_step=0.25,
        dense_output=True,
        events=hit_D,
    )
    if sol.t.size < 10:
        return AsymRun(Z, u, r_max, float(sol.t[-1]), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "short")

    rs = np.linspace(sol.t[0], sol.t[-1], 400)
    Y = sol.sol(rs)
    phi, uu, D, v = Y
    F = np.exp(-2 * phi) * v
    G = D**2 * uu
    # last 20%
    k = int(0.8 * len(rs))
    notes = []
    if sol.t[-1] < r_max - 1e-6:
        notes.append("ended_early")
    D_std = float(np.std(D[k:]))
    if D_std < 1e-3:
        notes.append("D_plateau_numeric")
    elif D_std < 1e-2:
        notes.append("D_nearly_plateau")
    else:
        notes.append("D_still_drifting")
    # phi ~ a + b r ? or b log r?
    # fit phi ~ a + b r on last window
    coef = np.polyfit(rs[k:], phi[k:], 1)
    notes.append(f"phi~{coef[1]:.4f}+{coef[0]:.6f}*r")
    # log fit residual compare
    # u mean
    return AsymRun(
        Z=Z,
        u=u,
        r_max=r_max,
        r_end=float(sol.t[-1]),
        D_end=float(D[-1]),
        phi_end=float(phi[-1]),
        u_end=float(uu[-1]),
        v_end=float(v[-1]),
        F_end=float(F[-1]),
        G_end=float(G[-1]),
        D_mean_last=float(np.mean(D[k:])),
        D_std_last=D_std,
        u_mean_last=float(np.mean(uu[k:])),
        v_mean_last=float(np.mean(v[k:])),
        dphi_dr_times_r_mean=float(np.mean(uu[k:] * rs[k:])),
        notes="; ".join(notes),
    )


def main() -> None:
    print("=" * 70)
    print("OBSERVE-5 symmetries + asymptotics")
    print("=" * 70)

    sym = cas_symmetries()
    print("\n--- 5b CAS symmetries ---")
    print(json.dumps(sym, indent=2))

    print("\n--- 5b numeric phi flip residual ---")
    fr = numeric_phi_flip_residual()
    print(fr)

    print("\n--- 5b r-reflection / sides ---")
    rr = numeric_r_reverse_match()
    print(rr)

    print("\n--- 5a long-lived asymptotics (u*<0, r_max=500) ---")
    asyms = []
    for Z in (1.0, 2.0, 4.0, 8.0):
        for u in (-0.05, -0.1, -0.2):
            a = asym_run(Z, u, r_max=500.0)
            asyms.append(a)
            print(
                f"  Z={Z:g} u={u:g}: r_end={a.r_end:.1f} D_end={a.D_end:.5f} "
                f"D_std_last={a.D_std_last:.2e} u_end={a.u_end:.5f} "
                f"G_end={a.G_end:.5f} | {a.notes}"
            )

    # D_inf vs Z table at fixed u=-0.1
    print("\n--- D_mean_last vs Z (u=-0.1) ---")
    for a in asyms:
        if a.u == -0.1:
            print(f"  Z={a.Z:g}: D≈{a.D_mean_last:.6f}  (1-D)={1-a.D_mean_last:.6f}")

    out = {
        "premises": PREMISES,
        "symmetries": sym,
        "phi_flip_numeric": fr,
        "r_reflection": rr,
        "asym": [asdict(a) for a in asyms],
    }
    path = "macro_vacuum_B_observe5_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE OBSERVE-5")


if __name__ == "__main__":
    main()
