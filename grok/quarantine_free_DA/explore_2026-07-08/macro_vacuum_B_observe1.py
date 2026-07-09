#!/usr/bin/env python3
"""
OBSERVE-1: vacuum field equations under locked option B (W=1), free D, no sources.

  FE-phi:  d/dr( Z D^2 phi' ) = 4 e^{-2 phi} (D')^2
  FE-D:    d/dr( e^{-2 phi} D' ) = -(Z/4) D (phi')^2

Mode: observe what is there. No sky targets. No L_m.
Bounded: small IC grid, scipy IVP, CPU only.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------------------
# Premise tags (echo into results)
# ---------------------------------------------------------------------------
PREMISES = {
    "W": "1 (option B, Charles CHOSE)",
    "Z": "FREE; representative values scanned, not fit",
    "L_m": "0 (vacuum first)",
    "slice": "static spherical diagonal FREE",
    "mode": "OBSERVE not TARGET",
}


def system_rhs(r: float, y: np.ndarray, Z: float) -> list[float]:
    """y = [phi, u, D, v] with u=phi', v=D'."""
    phi, u, D, v = y
    # Guard D
    if D <= 1e-14:
        D = 1e-14
    e2 = np.exp(-2.0 * phi)
    # From FE-phi: Z ( 2 D v u + D^2 u' ) = 4 e2 v^2
    # u' = (4/Z) e2 (v/D)^2 - 2 (v/D) u   if D!=0
    # From FE-D: (e2 v)' = e2 v' - 2 e2 u v = -(Z/4) D u^2
    # v' - 2 u v = -(Z/4) D e^{2 phi} u^2
    # v' = 2 u v - (Z/4) D exp(2 phi) u^2
    up = (4.0 / Z) * e2 * (v / D) ** 2 - 2.0 * (v / D) * u
    vp = 2.0 * u * v - (Z / 4.0) * D * np.exp(2.0 * phi) * u**2
    return [u, up, v, vp]


def residual_check(r, y, Z, eps=1e-6):
    """Finite-diff residual of integrated fluxes (diagnostic)."""
    phi, u, D, v = y
    # need neighbors — used only on dense solution samples
    return None


# ---------------------------------------------------------------------------
# Analytic: regular polar origin power series obstruction
# ---------------------------------------------------------------------------
def analytic_polar_origin_report() -> dict[str, Any]:
    """
    Assume smooth even phi, D ~ d1 r + ..., regular origin.
    Compare leading orders of FE-phi.
    """
    # Documented algebra (also verified symbolically below if sympy available)
    lines = []
    try:
        import sympy as sp

        r = sp.symbols("r", positive=True)
        Z, d1, d3, p0, p2, p4 = sp.symbols("Z d1 d3 p0 p2 p4", real=True)
        # D = d1*r + d3*r**3
        # phi = p0 + p2*r**2 + p4*r**4
        D = d1 * r + d3 * r**3
        phi = p0 + p2 * r**2 + p4 * r**4
        Dp = sp.diff(D, r)
        phip = sp.diff(phi, r)
        LHS = sp.series(sp.diff(Z * D**2 * phip, r), r, 0, 3).removeO()
        RHS = sp.series(4 * sp.exp(-2 * phi) * Dp**2, r, 0, 3).removeO()
        diff = sp.simplify(sp.expand(LHS - RHS))
        # leading constant term in (LHS-RHS)
        const = sp.simplify(diff.subs(r, 0))
        # coeff of r^0
        series_diff = sp.series(LHS - RHS, r, 0, 4)
        lines.append(f"LHS-RHS series = {series_diff}")
        lines.append(f"(LHS-RHS)|_0 = {const}")
        # const should be -4*exp(-2p0)*d1**2
        check = sp.simplify(const + 4 * sp.exp(-2 * p0) * d1**2)
        polar_ok_only_if = "d1=0 (but then higher orders still obstruct smooth phi — see report)"
        d1_zero = sp.series(
            (sp.diff(Z * (d3 * r**3) ** 2 * sp.diff(p0 + p2 * r**2, r), r)
             - 4 * sp.exp(-2 * (p0 + p2 * r**2)) * sp.diff(d3 * r**3, r) ** 2),
            r,
            0,
            5,
        )
        return {
            "CAS": True,
            "const_term_LHS_minus_RHS": str(const),
            "const_equals_minus_4_e_d1sq": bool(check == 0),
            "series": str(series_diff),
            "d1_zero_D_r3_series_diff": str(d1_zero),
            "conclusion": (
                "Smooth polar origin D~d1 r + ..., phi even: FE-phi has "
                "LHS=O(r^2), RHS=4 e^{-2p0} d1^2 + O(r^2). Inconsistent unless d1=0. "
                "With d1=0 and D~r^k, matching forces singular phi'~1/r or fails. "
                "SCOPED: obstruction to SMOOTH REGULAR POLAR ORIGIN under vacuum B."
            ),
        }
    except Exception as e:
        return {"CAS": False, "error": str(e)}


# ---------------------------------------------------------------------------
# First-integral / monotonicity probes
# ---------------------------------------------------------------------------
def analytic_structure_report() -> dict[str, str]:
    return {
        "FE-D_sign": (
            "If Z>0, D>0: (e^{-2phi} D')' = -(Z/4) D (phi')^2 <= 0. "
            "So flux F := e^{-2phi} D' is nonincreasing; strictly decreasing wherever phi'!=0."
        ),
        "FE-phi_sign": (
            "If Z>0: (D^2 phi')' = (4/Z) e^{-2phi} (D')^2 >= 0. "
            "So G := D^2 phi' is nondecreasing; grows wherever D'!=0."
        ),
        "flat_point": (
            "phi'=0 and D'=0 simultaneously: both fluxes stationary; "
            "constant (phi, D) is an exact solution (trivial vacuum)."
        ),
        "Z_scaling": (
            "Z cannot be removed by phi-rescaling alone because of e^{-2phi}. "
            "r-rescaling: if r = a s, D = a Delta, then Z and shape couple; "
            "scan Z as genuine 1-parameter family for now."
        ),
    }


# ---------------------------------------------------------------------------
# Numerics: IVP from interior point (no polar origin assumed)
# ---------------------------------------------------------------------------
@dataclass
class RunResult:
    tag: str
    Z: float
    r0: float
    y0: list[float]
    status: str
    message: str
    r_end: float
    n_points: int
    phi_min: float
    phi_max: float
    D_min: float
    D_max: float
    F_start: float  # e^{-2phi} D'
    F_end: float
    G_start: float  # D^2 phi'
    G_end: float
    hit_D_nonpos: bool
    notes: str


def integrate_case(
    tag: str,
    Z: float,
    r0: float,
    phi0: float,
    u0: float,
    D0: float,
    v0: float,
    r_max: float = 5.0,
    n_eval: int = 400,
) -> RunResult:
    y0 = np.array([phi0, u0, D0, v0], dtype=float)
    F0 = np.exp(-2 * phi0) * v0
    G0 = D0**2 * u0

    def fun(r, y):
        return system_rhs(r, y, Z)

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
        dense_output=True,
        events=hit_D,
        max_step=0.05,
    )

    if sol.t.size < 2:
        return RunResult(
            tag=tag,
            Z=Z,
            r0=r0,
            y0=y0.tolist(),
            status="failed",
            message=sol.message,
            r_end=float(sol.t[-1]) if sol.t.size else r0,
            n_points=int(sol.t.size),
            phi_min=phi0,
            phi_max=phi0,
            D_min=D0,
            D_max=D0,
            F_start=float(F0),
            F_end=float(F0),
            G_start=float(G0),
            G_end=float(G0),
            hit_D_nonpos=False,
            notes="no steps",
        )

    t = sol.t
    Y = sol.y
    phi, u, D, v = Y
    F = np.exp(-2 * phi) * v
    G = D**2 * u
    hit = sol.t_events is not None and len(sol.t_events[0]) > 0
    notes = []
    # Monotonicity checks on F, G (should be mono given theory)
    dF = np.diff(F)
    dG = np.diff(G)
    if np.all(dF <= 1e-8):
        notes.append("F nonincreasing OK")
    else:
        notes.append(f"F mono VIOLATION max dF={dF.max():.2e}")
    if np.all(dG >= -1e-8):
        notes.append("G nondecreasing OK")
    else:
        notes.append(f"G mono VIOLATION min dG={dG.min():.2e}")

    # phi trend
    if phi[-1] > phi[0] + 1e-6:
        notes.append("phi rises")
    elif phi[-1] < phi[0] - 1e-6:
        notes.append("phi falls")
    else:
        notes.append("phi ~ flat")

    if D[-1] > D[0] + 1e-6:
        notes.append("D grows")
    elif D[-1] < D[0] - 1e-6:
        notes.append("D shrinks")
    else:
        notes.append("D ~ flat")

    status = "ok" if sol.success else ("event_D" if hit else "stopped")
    return RunResult(
        tag=tag,
        Z=Z,
        r0=r0,
        y0=y0.tolist(),
        status=status,
        message=str(sol.message),
        r_end=float(t[-1]),
        n_points=int(t.size),
        phi_min=float(phi.min()),
        phi_max=float(phi.max()),
        D_min=float(D.min()),
        D_max=float(D.max()),
        F_start=float(F[0]),
        F_end=float(F[-1]),
        G_start=float(G[0]),
        G_end=float(G[-1]),
        hit_D_nonpos=bool(hit),
        notes="; ".join(notes),
    )


def main() -> None:
    print("=" * 70)
    print("OBSERVE-1 vacuum B (W=1), free D, no sources")
    print("=" * 70)
    print("Premises:", json.dumps(PREMISES, indent=2))

    polar = analytic_polar_origin_report()
    print("\n--- Analytic polar origin ---")
    for k, v in polar.items():
        print(f"  {k}: {v}")

    struct = analytic_structure_report()
    print("\n--- Structure ---")
    for k, v in struct.items():
        print(f"  {k}: {v}")

    # Trivial solution check
    print("\n--- Trivial constant solution ---")
    tr = integrate_case("trivial", Z=1.0, r0=0.1, phi0=0.0, u0=0.0, D0=1.0, v0=0.0, r_max=3.0)
    print(asdict(tr))

    # Small IC survey from r0>0, D0>0 (no polar origin)
    cases = []
    # chart phi0=0; mild slopes
    for Z in (1.0, 4.0, 8.0):
        cases.append(
            ("mild_expand", Z, 0.5, 0.0, 0.05, 1.0, 0.3)
        )
        cases.append(
            ("mild_contract_D", Z, 0.5, 0.0, 0.05, 1.0, -0.2)
        )
        cases.append(
            ("phi_down", Z, 0.5, 0.0, -0.1, 1.0, 0.2)
        )
        cases.append(
            ("near_flat", Z, 0.5, 0.0, 0.01, 1.0, 0.05)
        )

    results: list[RunResult] = []
    print("\n--- IVP survey ---")
    for tag, Z, r0, p0, u0, D0, v0 in cases:
        name = f"{tag}_Z{Z:g}"
        rr = integrate_case(name, Z, r0, p0, u0, D0, v0, r_max=4.0)
        results.append(rr)
        print(
            f"  {rr.tag:24s} status={rr.status:10s} r_end={rr.r_end:.3f} "
            f"phi=[{rr.phi_min:.3f},{rr.phi_max:.3f}] D=[{rr.D_min:.3f},{rr.D_max:.3f}] "
            f"F:{rr.F_start:.3g}->{rr.F_end:.3g} G:{rr.G_start:.3g}->{rr.G_end:.3g} | {rr.notes}"
        )

    # Attempt near-polar: D0 small, v0~1, r0 small — expect stiffness / blow
    print("\n--- Near-polar attempts (expect trouble) ---")
    near = []
    for D0, r0 in ((0.05, 0.05), (0.1, 0.1), (0.2, 0.2)):
        rr = integrate_case(
            f"nearpolar_D{D0}",
            Z=1.0,
            r0=r0,
            phi0=0.0,
            u0=0.0,
            D0=D0,
            v0=1.0,
            r_max=2.0,
        )
        near.append(rr)
        print(
            f"  {rr.tag:24s} status={rr.status:10s} r_end={rr.r_end:.3f} "
            f"phi=[{rr.phi_min:.3f},{rr.phi_max:.3f}] D=[{rr.D_min:.3f},{rr.D_max:.3f}] | {rr.notes}"
        )

    out = {
        "premises": PREMISES,
        "polar_origin": polar,
        "structure": struct,
        "trivial": asdict(tr),
        "survey": [asdict(r) for r in results],
        "near_polar": [asdict(r) for r in near],
    }
    path = "macro_vacuum_B_observe1_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE OBSERVE-1")


if __name__ == "__main__":
    main()
