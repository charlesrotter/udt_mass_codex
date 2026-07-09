#!/usr/bin/env python3
"""
Path B + DILATED dust: L_m = -rho(r) D_A^2 e^{-2 phi}
(Charles: matter dilated toward the edge; T_tt ~ rho e^{-2 phi})
Compare to phi-blind dust; M-bracket + turn + vacuum match.
Frame: macro_matter_dilation_edge_FRAME.md
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

Z = 1.0
R_EXP, R_SEP, EPS_S = 3.0, 2.0, 0.02
D_FLOOR = 1e-4


def rho_gauss(r, rho0, rc):
    return rho0 * np.exp(-(r / rc) ** 2)


def make_rhs(rho0, rc, dilated=True, vacuum=False):
    def f(r, y):
        D, S, phi, Q = y
        De = max(float(D), 1e-14)
        rh = 0.0 if vacuum else float(rho_gauss(r, rho0, rc))
        e2 = np.exp(np.clip(2.0 * phi, -40, 40))
        em2 = np.exp(np.clip(-2.0 * phi, -40, 40))
        A11 = 4.0 * De * em2
        A12 = -Z * De * De
        A21 = -4.0
        A22 = 4.0 * De
        if dilated and not vacuum:
            # b1: 2 Z D S Q - 2 D^2 rho e^{-2phi}
            b1 = 2.0 * Z * De * S * Q - 2.0 * De * De * rh * em2
            # b2: vac + 2 D rho
            b2 = -Z * De * e2 * Q * Q + 8.0 * De * Q * Q - 8.0 * S * Q + 2.0 * De * rh
        else:
            # phi-blind: b1 vac; b2 vac + 2 D rho e2
            b1 = 2.0 * Z * De * S * Q
            b2 = (
                -Z * De * e2 * Q * Q
                + 2.0 * De * rh * e2
                + 8.0 * De * Q * Q
                - 8.0 * S * Q
            )
        det = A11 * A22 - A12 * A21
        if abs(det) < 1e-30:
            return [S, 0.0, Q, 0.0]
        Sp = (b1 * A22 - A12 * b2) / det
        Qp = (A11 * b2 - b1 * A21) / det
        Sp = float(np.clip(Sp if np.isfinite(Sp) else 0.0, -1e6, 1e6))
        Qp = float(np.clip(Qp if np.isfinite(Qp) else 0.0, -1e6, 1e6))
        return [S, Sp, Q, Qp]

    return f


def integrate(f, y0, r0, r_max):
    def ev(r, y):
        return y[0] - D_FLOOR

    ev.terminal = True
    ev.direction = -1
    return solve_ivp(
        f, (r0, r_max), y0, method="RK45", rtol=1e-7, atol=1e-9, max_step=0.04, events=[ev]
    )


def mass_M(sol, rho0, rc):
    r, D = sol.t, sol.y[0]
    dens = 4.0 * np.pi * D**2 * np.array([rho_gauss(ri, rho0, rc) for ri in r])
    return float(np.trapezoid(dens, r)) if len(r) > 1 else 0.0


def find_turn(sol, rc):
    r, D, S = sol.t, sol.y[0], sol.y[1]
    D0 = D[0]
    for i in range(1, len(S)):
        if np.max(D[: i + 1]) / D0 < R_EXP:
            continue
        if r[i] < R_SEP * rc:
            continue
        if S[i - 1] > EPS_S and S[i] <= 0.0:
            return i
    return None


def run_case(rho0, rc, Q0, dilated, r0=0.2, r_max=15.0):
    f = make_rhs(rho0, rc, dilated=dilated, vacuum=False)
    sol = integrate(f, [1.0, 0.0, 0.0, Q0], r0, r_max)
    if len(sol.t) < 4:
        return {"class": "COLLAPSE_INT", "M": 0.0, "rho0": rho0, "dilated": dilated}
    M = mass_M(sol, rho0, rc)
    phi_max = float(np.nanmax(sol.y[2]))
    if np.min(sol.y[0]) <= 1.5 * D_FLOOR:
        return {
            "class": "COLLAPSE_INT",
            "M": M,
            "rho0": rho0,
            "phi_max": phi_max,
            "dilated": dilated,
        }
    it = find_turn(sol, rc)
    if it is None:
        return {
            "class": "NO_TURN",
            "M": M,
            "rho0": rho0,
            "phi_max": phi_max,
            "ratio": float(np.max(sol.y[0]) / sol.y[0][0]),
            "dilated": dilated,
        }
    y_t = [float(sol.y[k, it]) for k in range(4)]
    if y_t[1] > 0:
        y_t[1] = 0.0
    r_t = float(sol.t[it])
    f_vac = make_rhs(0.0, rc, dilated=True, vacuum=True)
    sol_e = integrate(f_vac, y_t, r_t, max(r_t + 8.0, 3 * r_t))
    Dmin = float(np.min(sol_e.y[0])) if len(sol_e.t) else 0.0
    dphi = float(np.nanmax(sol_e.y[2]) - y_t[2]) if len(sol_e.t) else 99.0
    ok = (
        len(sol_e.t) > 2
        and np.all(np.isfinite(sol_e.y))
        and Dmin > 1.5 * D_FLOOR
        and dphi < 10.0
    )
    return {
        "class": "MATCH_OK" if ok else "MATCH_FAIL",
        "M": M,
        "rho0": rho0,
        "phi_max": phi_max,
        "r_turn": r_t,
        "phi_turn": y_t[2],
        "ratio": float(np.max(sol.y[0]) / sol.y[0][0]),
        "dphi_ext": dphi,
        "Dend_ext": float(sol_e.y[0, -1]) if len(sol_e.t) else 0.0,
        "dilated": dilated,
    }


def summarize(rows, title):
    print(f"\n=== {title} ===")
    for cl in ("NO_TURN", "MATCH_OK", "MATCH_FAIL", "COLLAPSE_INT"):
        sub = [x for x in rows if x["class"] == cl]
        if not sub:
            print(f"  {cl}: 0")
            continue
        Ms = [x["M"] for x in sub]
        ph = [x.get("phi_max", 0) for x in sub]
        print(
            f"  {cl}: n={len(sub)} M∈[{min(Ms):.3g},{max(Ms):.3g}] "
            f"φmax∈[{min(ph):.2f},{max(ph):.2f}]"
        )
    ok = sorted([x for x in rows if x["class"] == "MATCH_OK"], key=lambda z: z["M"])
    if ok:
        print(
            f"  MATCH_OK window M∈[{ok[0]['M']:.3g},{ok[-1]['M']:.3g}] "
            f"Δlog10={np.log10(ok[-1]['M']/ok[0]['M']):.3f} n={len(ok)}"
        )
        for x in ok[:10]:
            print(
                f"    M={x['M']:.4g} ρ0={x['rho0']:.4g} r_t={x['r_turn']:.3g} "
                f"φmax={x['phi_max']:.3f} dφ_ext={x['dphi_ext']:+.3f}"
            )


def main():
    print("=" * 70)
    print("DILATED dust (e^{-2φ}) vs φ-blind — Path B")
    print("=" * 70)

    rho_list = np.unique(np.concatenate([np.logspace(-2, 2, 36), np.logspace(0.3, 1.3, 28)]))

    for dilated, tag in [(True, "DILATED e^{-2φ}"), (False, "φ-BLIND")]:
        print(f"\n[scan] {tag}  rc=1 Q0=0.5")
        rows = []
        for rho0 in rho_list:
            o = run_case(float(rho0), 1.0, 0.5, dilated=dilated)
            rows.append(o)
            print(
                f"  [{o['class'][0]}] ρ0={rho0:.4g} M={o['M']:.4g} class={o['class']} "
                f"φmax={o.get('phi_max', float('nan')):.3f}"
            )
        summarize(rows, tag + " rc=1 Q0=0.5")

    print("\n[scan] DILATED rc=1 Q0=0")
    rows0 = [run_case(float(rho0), 1.0, 0.0, dilated=True) for rho0 in rho_list]
    summarize(rows0, "DILATED rc=1 Q0=0")

    print("\n[scan] DILATED rc=2 Q0=0.5")
    rows2 = [
        run_case(float(rho0), 2.0, 0.5, dilated=True)
        for rho0 in np.logspace(-2, 1.5, 32)
    ]
    summarize(rows2, "DILATED rc=2 Q0=0.5")

    # Vacuum control dilated engine
    print("\n[control] vacuum Q0=0.5")
    o = run_case(0.0, 1.0, 0.5, dilated=True)
    print(o)

    print("\nDONE")


if __name__ == "__main__":
    main()
