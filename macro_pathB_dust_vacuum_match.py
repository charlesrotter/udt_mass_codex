#!/usr/bin/env python3
"""
Match Path B dust interior to vacuum exterior at qualifying turn.
Contract: macro_pathB_dust_vacuum_match_CONTRACT.md
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

Z = 1.0
R_EXP = 3.0
R_SEP = 2.0
EPS_S = 0.02
D_FLOOR = 1e-4
DPHI_BLOW = 10.0


def rho_gauss(r, rho0, rc):
    return rho0 * np.exp(-(r / rc) ** 2)


def rhs_factory(rho0, rc, vacuum=False):
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
        b1 = 2.0 * Z * De * S * Q
        b2 = -Z * De * e2 * Q * Q + 2.0 * De * rh * e2 + 8.0 * De * Q * Q - 8.0 * S * Q
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
    def event_Dfloor(r, y):
        return y[0] - D_FLOOR

    event_Dfloor.terminal = True
    event_Dfloor.direction = -1

    return solve_ivp(
        f,
        (r0, r_max),
        y0,
        method="RK45",
        rtol=1e-7,
        atol=1e-9,
        max_step=0.04,
        events=[event_Dfloor],
    )


def mass_along(sol, rho0, rc):
    r, D = sol.t, sol.y[0]
    if len(r) < 2:
        return 0.0
    dens = 4.0 * np.pi * D**2 * np.array([rho_gauss(ri, rho0, rc) for ri in r])
    return float(np.trapezoid(dens, r))


def find_qualifying_turn(sol, rc):
    """Return index of first qualifying outer turn, or None."""
    r, D, S = sol.t, sol.y[0], sol.y[1]
    D0 = D[0]
    for i in range(1, len(S)):
        if D[i] < 1.05 * D0:
            continue
        Dmax = np.max(D[: i + 1])
        if Dmax / D0 < R_EXP:
            continue
        if r[i] < R_SEP * rc:
            continue
        if S[i - 1] > EPS_S and S[i] <= 0.0:
            return i
    return None


def exterior_health(sol_ext, y_turn):
    if sol_ext is None or len(sol_ext.t) < 2:
        return "FAIL_EMPTY", {}
    D, S, phi, Q = sol_ext.y
    D_t, phi_t = y_turn[0], y_turn[2]
    finite = bool(np.all(np.isfinite(sol_ext.y)))
    Dmin = float(np.min(D))
    dphi = float(np.nanmax(phi) - phi_t)
    drop = Dmin < 0.5 * D_t
    collapsed = Dmin <= 1.5 * D_FLOOR
    blow = dphi >= DPHI_BLOW or not finite
    info = {
        "Dmin_ext": Dmin,
        "Dend_ext": float(D[-1]),
        "Send_ext": float(S[-1]),
        "dphi_ext": dphi,
        "phi_end_ext": float(phi[-1]),
        "r_ext_end": float(sol_ext.t[-1]),
        "ok_int": bool(sol_ext.success),
    }
    if collapsed or blow or not finite:
        return "MATCH_FAIL", info
    if drop and float(S[-1]) < -1.0:
        return "MATCH_FAIL", info
    # healthy: survived
    return "MATCH_OK", info


def process_one(rho0, rc, Q0, r0=0.2, r_int_max=15.0):
    f_dust = rhs_factory(rho0, rc, vacuum=False)
    y0 = [1.0, 0.0, 0.0, Q0]
    sol_i = integrate(f_dust, y0, r0, r_int_max)
    if len(sol_i.t) < 4:
        return {
            "rho0": rho0,
            "rc": rc,
            "Q0": Q0,
            "class": "COLLAPSE_INT",
            "M": 0.0,
        }

    M = mass_along(sol_i, rho0, rc)
    # interior collapse?
    if np.min(sol_i.y[0]) <= 1.5 * D_FLOOR:
        return {
            "rho0": rho0,
            "rc": rc,
            "Q0": Q0,
            "class": "COLLAPSE_INT",
            "M": M,
            "phi_max_int": float(np.nanmax(sol_i.y[2])),
        }

    it = find_qualifying_turn(sol_i, rc)
    if it is None:
        return {
            "rho0": rho0,
            "rc": rc,
            "Q0": Q0,
            "class": "NO_TURN",
            "M": M,
            "phi_max_int": float(np.nanmax(sol_i.y[2])),
            "ratio": float(np.max(sol_i.y[0]) / sol_i.y[0][0]),
        }

    r_t = float(sol_i.t[it])
    y_t = [float(sol_i.y[k, it]) for k in range(4)]
    # Force S slightly <=0 at interface for clean handoff
    if y_t[1] > 0:
        y_t[1] = 0.0

    r_ext = max(r_t + 8.0, 3.0 * r_t)
    f_vac = rhs_factory(0.0, rc, vacuum=True)
    sol_e = integrate(f_vac, y_t, r_t, r_ext)
    status, info = exterior_health(sol_e, y_t)

    return {
        "rho0": rho0,
        "rc": rc,
        "Q0": Q0,
        "class": status,
        "M": M,
        "r_turn": r_t,
        "phi_turn": y_t[2],
        "D_turn": y_t[0],
        "phi_max_int": float(np.nanmax(sol_i.y[2])),
        "ratio": float(np.max(sol_i.y[0]) / sol_i.y[0][0]),
        **info,
    }


def summarize(rows, title):
    print(f"\n=== {title} ===")
    for cl in ("NO_TURN", "MATCH_OK", "MATCH_FAIL", "COLLAPSE_INT"):
        sub = [x for x in rows if x["class"] == cl]
        if not sub:
            print(f"  {cl}: 0")
            continue
        Ms = [x["M"] for x in sub]
        print(
            f"  {cl}: n={len(sub)}  M∈[{min(Ms):.3g}, {max(Ms):.3g}]  "
            f"med M={np.median(Ms):.3g}"
        )
    ok = sorted([x for x in rows if x["class"] == "MATCH_OK"], key=lambda z: z["M"])
    fail = sorted([x for x in rows if x["class"] == "MATCH_FAIL"], key=lambda z: z["M"])
    if ok:
        print("  MATCH_OK samples:")
        for x in ok[:15]:
            print(
                f"    M={x['M']:.4g} ρ0={x['rho0']:.4g} r_t={x['r_turn']:.3g} "
                f"φ_t={x['phi_turn']:.3f} Dend_ext={x.get('Dend_ext', float('nan')):.3g} "
                f"dφ_ext={x.get('dphi_ext', float('nan')):+.3f}"
            )
        Ms = [x["M"] for x in ok]
        print(
            f"  MATCH_OK window: M∈[{min(Ms):.3g}, {max(Ms):.3g}]  "
            f"Δlog10M={np.log10(max(Ms)/min(Ms)):.3f}  n={len(Ms)}"
        )
    if fail:
        print("  MATCH_FAIL samples:")
        for x in fail[:8]:
            print(
                f"    M={x['M']:.4g} ρ0={x['rho0']:.4g} r_t={x.get('r_turn')} "
                f"Dmin_ext={x.get('Dmin_ext')} dφ_ext={x.get('dphi_ext')}"
            )


def main():
    print("=" * 70)
    print("DUST INTERIOR → VACUUM EXTERIOR MATCH AT QUALIFYING TURN")
    print("=" * 70)

    # Dense scan primary family
    rho_list = np.unique(
        np.concatenate(
            [
                np.logspace(-2, 2, 40),
                np.logspace(0.2, 1.4, 35),  # denser mid
            ]
        )
    )

    print("\n[A] gauss rc=1 Q0=0.5")
    rows_a = []
    for rho0 in rho_list:
        o = process_one(float(rho0), 1.0, 0.5)
        rows_a.append(o)
        c = o["class"][0]
        print(
            f"  [{c}] ρ0={rho0:.4g} M={o['M']:.4g} class={o['class']} "
            f"r_t={o.get('r_turn')} φmax_i={o.get('phi_max_int')}"
        )
    summarize(rows_a, "gauss rc=1 Q0=0.5")

    print("\n[B] gauss rc=1 Q0=0")
    rows_b = []
    for rho0 in rho_list:
        o = process_one(float(rho0), 1.0, 0.0)
        rows_b.append(o)
    summarize(rows_b, "gauss rc=1 Q0=0")

    print("\n[C] gauss rc=2 Q0=0.5")
    rows_c = []
    for rho0 in np.logspace(-2, 1.5, 36):
        o = process_one(float(rho0), 2.0, 0.5)
        rows_c.append(o)
    summarize(rows_c, "gauss rc=2 Q0=0.5")

    # Compare MATCH_OK windows
    print("\n" + "=" * 70)
    print("MATCH_OK MASS WINDOWS")
    print("=" * 70)
    for name, rows in [
        ("rc=1 Q0=0.5", rows_a),
        ("rc=1 Q0=0", rows_b),
        ("rc=2 Q0=0.5", rows_c),
    ]:
        ok = [x["M"] for x in rows if x["class"] == "MATCH_OK"]
        fail = [x["M"] for x in rows if x["class"] == "MATCH_FAIL"]
        nt = sum(1 for x in rows if x["class"] == "NO_TURN")
        if ok:
            print(
                f"  {name}: MATCH_OK M∈[{min(ok):.3g},{max(ok):.3g}] n={len(ok)} ; "
                f"MATCH_FAIL n={len(fail)} ; NO_TURN n={nt}"
            )
        else:
            print(f"  {name}: MATCH_OK n=0 ; MATCH_FAIL n={len(fail)} ; NO_TURN n={nt}")

    # Fraction of prior-style CLOSE that match
    # Among runs with a turn (MATCH_OK or MATCH_FAIL)
    print("\n[D] Match success rate among turned interiors")
    for name, rows in [
        ("rc=1 Q0=0.5", rows_a),
        ("rc=1 Q0=0", rows_b),
        ("rc=2 Q0=0.5", rows_c),
    ]:
        turned = [x for x in rows if x["class"] in ("MATCH_OK", "MATCH_FAIL")]
        ok = [x for x in turned if x["class"] == "MATCH_OK"]
        if turned:
            print(
                f"  {name}: {len(ok)}/{len(turned)} = {100*len(ok)/len(turned):.0f}% MATCH_OK "
                f"after turn"
            )
        else:
            print(f"  {name}: no turns")

    print("\nDONE")


if __name__ == "__main__":
    main()
