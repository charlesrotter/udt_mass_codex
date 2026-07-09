#!/usr/bin/env python3
"""
WP2 — Path B + dust: bracket mass/amount, hunt closure-like behavior.
MAP: macro_native_matter_edge_MAP.md
WP1: macro_pathB_dust_WP1_results.md

Gravity: free D_A + EH + R1 kinetic (Path B).
Matter: FREE alpha=0 dust L_m = -rho D_A^2; rho profile FREE (amount scan).
Charles: universe may bootstrap — only narrow mass range closes.

Characterize; no SNe; no claim dust is fundamental UDT matter.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

Z = 1.0


def rho_gauss(r, rho0, rc):
    return rho0 * np.exp(-(r / rc) ** 2)


def rho_tophat(r, rho0, rc, soft=0.05):
    # soft edge for numerics
    return rho0 / (1.0 + np.exp((r - rc) / (soft * rc + 1e-12)))


def make_rhs(rho0, rc, profile="gauss"):
    def rho_of(r):
        if profile == "gauss":
            return rho_gauss(r, rho0, rc)
        return rho_tophat(r, rho0, rc)

    def f(r, y):
        D, S, phi, Q = y
        De = max(float(D), 1e-14)
        rh = float(rho_of(r))
        e2 = np.exp(np.clip(2.0 * phi, -40, 40))
        em2 = np.exp(np.clip(-2.0 * phi, -40, 40))
        # Linear system for (S', Q') from EL_phi, EL_D
        # EL_phi: 4 D em2 S' - Z D^2 Q' = 2 Z D S Q
        # EL_D:  -4 S' + 4 D Q' = -Z D e2 Q^2 + 2 D rh e2 + 8 D Q^2 - 8 S Q
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
        if not np.isfinite(Sp):
            Sp = 0.0
        if not np.isfinite(Qp):
            Qp = 0.0
        return [
            S,
            float(np.clip(Sp, -1e6, 1e6)),
            Q,
            float(np.clip(Qp, -1e6, 1e6)),
        ]

    return f, rho_of


def integrate(rho0, rc, y0, r0, r_max, profile="gauss"):
    f, rho_of = make_rhs(rho0, rc, profile)

    def event_Dfloor(r, y):
        return y[0] - 1e-5

    event_Dfloor.terminal = True
    event_Dfloor.direction = -1

    sol = solve_ivp(
        f,
        (r0, r_max),
        y0,
        method="RK45",
        rtol=1e-7,
        atol=1e-9,
        max_step=0.05,
        events=[event_Dfloor],
    )
    return sol, rho_of


def mass_proxy(sol, rho_of):
    """M ~ int 4 pi D^2 rho dr  (geometric G=c=1)."""
    r = sol.t
    D = sol.y[0]
    if len(r) < 2:
        return 0.0
    dens = 4.0 * np.pi * D**2 * np.array([rho_of(ri) for ri in r])
    return float(np.trapezoid(dens, r))


def classify_run(sol, rho_of, label):
    if sol is None or len(sol.t) < 3:
        return None
    r, D, S, phi, Q = sol.t, sol.y[0], sol.y[1], sol.y[2], sol.y[3]
    M = mass_proxy(sol, rho_of)
    # turnover: S was >0 then crosses to <=0
    i_turn = None
    for i in range(1, len(S)):
        if S[i - 1] > 0.02 and S[i] <= 0.0 and D[i] > D[0]:
            i_turn = i
            break
    # expansion then slow: S drops a lot from max while still positive
    Smax = float(np.max(S))
    Slow = float(S[-1])
    phi_max = float(np.nanmax(phi))
    out = {
        "label": label,
        "ok": bool(sol.success),
        "r_end": float(r[-1]),
        "phi_max": phi_max,
        "phi_end": float(phi[-1]),
        "dphi": float(phi[-1] - phi[0]),
        "D0": float(D[0]),
        "Dend": float(D[-1]),
        "Dmax": float(np.max(D)),
        "S_end": Slow,
        "S_max": Smax,
        "M": M,
        "turn_r": float(r[i_turn]) if i_turn is not None else None,
        "turn_D": float(D[i_turn]) if i_turn is not None else None,
        "turn_phi": float(phi[i_turn]) if i_turn is not None else None,
        "ceil_break": phi_max > 2.15,  # vacuum ceiling was ~2.04
        "finite": bool(np.all(np.isfinite(sol.y))),
    }
    return out


def print_row(o):
    if o is None:
        return
    t = ""
    if o["turn_r"] is not None:
        t = f" TURN@r={o['turn_r']:.3g} φ={o['turn_phi']:.3f}"
    cb = " CEIL↑" if o["ceil_break"] else ""
    print(
        f"  [{o['label']}] φmax={o['phi_max']:.3f} Δφ={o['dphi']:+.3f} "
        f"D:{o['D0']:.3g}→{o['Dend']:.3g} S_end={o['S_end']:+.3g} "
        f"M~{o['M']:.3g}{t}{cb} ok={o['ok']}"
    )


def main():
    print("=" * 70)
    print("WP2 Path B + dust — mass bracket / closure hunt")
    print("=" * 70)

    r0, r_max = 0.2, 12.0
    # Seeds: vacuum-like flat core + mild Q0; also pure rest
    seeds = [
        ("Q0=0", [1.0, 0.0, 0.0, 0.0]),
        ("Q0=0.1", [1.0, 0.0, 0.0, 0.1]),
        ("Q0=0.5", [1.0, 0.0, 0.0, 0.5]),
        ("Q0=1", [1.0, 0.0, 0.0, 1.0]),
    ]

    rows = []

    # ----- Vacuum control -----
    print("\n[0] Vacuum control rho0=0")
    for name, y0 in seeds:
        sol, rho_of = integrate(0.0, 1.0, y0, r0, r_max)
        o = classify_run(sol, rho_of, f"vac {name}")
        print_row(o)
        if o:
            rows.append(o)

    # ----- Mass bracket: rho0 log scan -----
    print("\n[1] Gauss rho0 bracket (rc=1), seed Q0=0.5")
    rho0_grid = np.logspace(-3, 2, 36)  # 0.001 .. 100
    for rho0 in rho0_grid:
        sol, rho_of = integrate(float(rho0), 1.0, [1.0, 0.0, 0.0, 0.5], r0, r_max)
        o = classify_run(sol, rho_of, f"g rc=1 ρ0={rho0:.3g} Q0=0.5")
        print_row(o)
        if o:
            rows.append({**o, "rho0": float(rho0), "rc": 1.0, "prof": "gauss", "Q0": 0.5})

    print("\n[2] Gauss rho0 bracket, seed Q0=0 (matter-driven only)")
    for rho0 in rho0_grid:
        sol, rho_of = integrate(float(rho0), 1.0, [1.0, 0.0, 0.0, 0.0], r0, r_max)
        o = classify_run(sol, rho_of, f"g rc=1 ρ0={rho0:.3g} Q0=0")
        if o and (o["phi_max"] > 0.05 or o["turn_r"] is not None or o["S_max"] > 0.1):
            print_row(o)
        if o:
            rows.append({**o, "rho0": float(rho0), "rc": 1.0, "prof": "gauss", "Q0": 0.0})

    print("\n[3] Vary rc at fixed rho0 (shape/amount)")
    for rc in [0.3, 0.5, 1.0, 2.0, 3.0]:
        for rho0 in [0.1, 1.0, 10.0]:
            sol, rho_of = integrate(float(rho0), float(rc), [1.0, 0.0, 0.0, 0.5], r0, r_max)
            o = classify_run(sol, rho_of, f"g rc={rc:g} ρ0={rho0:g} Q0=0.5")
            print_row(o)
            if o:
                rows.append({**o, "rho0": float(rho0), "rc": float(rc), "prof": "gauss", "Q0": 0.5})

    print("\n[4] Top-hat profile bracket")
    for rho0 in np.logspace(-2, 1.5, 16):
        sol, rho_of = integrate(float(rho0), 1.5, [1.0, 0.0, 0.0, 0.5], r0, r_max, profile="tophat")
        o = classify_run(sol, rho_of, f"th rc=1.5 ρ0={rho0:.3g} Q0=0.5")
        print_row(o)
        if o:
            rows.append({**o, "rho0": float(rho0), "rc": 1.5, "prof": "tophat", "Q0": 0.5})

    # ----- Look for narrow windows -----
    print("\n" + "=" * 70)
    print("WINDOW ANALYSIS")
    print("=" * 70)

    def subset(pred):
        return [x for x in rows if pred(x)]

    ceil = subset(lambda x: x.get("ceil_break"))
    turns = subset(lambda x: x.get("turn_r") is not None)
    highphi = subset(lambda x: x.get("phi_max", 0) > 2.1)
    # "slowing expansion": S_end < 0.2 * S_max and S_max > 0.5 and S_end > 0
    slow = subset(
        lambda x: x.get("S_max", 0) > 0.5
        and x.get("S_end", 1) > 0
        and x["S_end"] < 0.25 * x["S_max"]
        and x.get("Dend", 0) > x.get("D0", 1)
    )

    print(f"  total recorded: {len(rows)}")
    print(f"  ceil_break (φmax>2.15): {len(ceil)}")
    print(f"  E-turn (D' +→− after growth): {len(turns)}")
    print(f"  φmax>2.1: {len(highphi)}")
    print(f"  expansion slowing (S_end<0.25 S_max): {len(slow)}")

    if turns:
        print("\n  TURN examples:")
        for x in turns[:15]:
            print(
                f"    {x['label']}: r_t={x['turn_r']:.3g} D_t={x['turn_D']:.3g} "
                f"φ_t={x['turn_phi']:.3f} φmax={x['phi_max']:.3f} M~{x['M']:.3g}"
            )

    if ceil:
        print("\n  CEILING BREAK examples:")
        for x in sorted(ceil, key=lambda z: -z["phi_max"])[:12]:
            print(f"    {x['label']}: φmax={x['phi_max']:.3f} M~{x['M']:.3g} S_end={x['S_end']:+.3g}")

    # phi_max vs log10(rho0) for fixed family
    fam = [x for x in rows if x.get("prof") == "gauss" and x.get("rc") == 1.0 and x.get("Q0") == 0.5 and "rho0" in x]
    if fam:
        fam = sorted(fam, key=lambda z: z["rho0"])
        print("\n  [gauss rc=1 Q0=0.5] φmax vs ρ0 (bracket curve):")
        for x in fam:
            mark = ""
            if x.get("turn_r") is not None:
                mark += " T"
            if x.get("ceil_break"):
                mark += " C"
            print(f"    ρ0={x['rho0']:.3e}  M~{x['M']:.3e}  φmax={x['phi_max']:.4f}  S_end={x['S_end']:+.3e}{mark}")

    # Fine bracket where something changes
    print("\n[5] Fine bracket where φmax or S_end changes most (gauss rc=1 Q0=0.5)")
    if len(fam) > 3:
        dphi = np.diff([x["phi_max"] for x in fam])
        i_star = int(np.argmax(np.abs(dphi))) if len(dphi) else 0
        rho_lo = fam[max(0, i_star - 1)]["rho0"]
        rho_hi = fam[min(len(fam) - 1, i_star + 2)]["rho0"]
        if rho_lo > rho_hi:
            rho_lo, rho_hi = rho_hi, rho_lo
        print(f"  refining ρ0 ∈ [{rho_lo:.3e}, {rho_hi:.3e}]")
        for rho0 in np.geomspace(max(rho_lo, 1e-4), rho_hi * 3, 20):
            sol, rho_of = integrate(float(rho0), 1.0, [1.0, 0.0, 0.0, 0.5], r0, r_max)
            o = classify_run(sol, rho_of, f"fine ρ0={rho0:.4g}")
            print_row(o)

    # Shoot S(r_out)=0 over rho0 for fixed Q0
    print("\n[6] Shoot S(r_out=6)=0 vs ρ0 (Q0=0.5, gauss rc=1)")
    r_out = 6.0

    def S_out(rho0):
        sol, _ = integrate(float(rho0), 1.0, [1.0, 0.0, 0.0, 0.5], r0, r_out)
        if len(sol.t) < 2:
            return 1e3
        return float(sol.y[1][-1])

    rhos = np.logspace(-3, 2, 50)
    Ss = [S_out(rh) for rh in rhos]
    for rh, s in zip(rhos[::5], Ss[::5]):
        print(f"  ρ0={rh:.3e}  S(6)={s:+.4f}")
    roots = []
    for i in range(len(rhos) - 1):
        if np.isfinite(Ss[i]) and np.isfinite(Ss[i + 1]) and Ss[i] * Ss[i + 1] < 0:
            if abs(Ss[i]) < 500 and abs(Ss[i + 1]) < 500:
                try:
                    rt = brentq(S_out, rhos[i], rhos[i + 1])
                    roots.append(rt)
                except Exception:
                    pass
    print(f"  roots S(6)=0: {roots if roots else 'none'}")
    for rt in roots:
        sol, rho_of = integrate(rt, 1.0, [1.0, 0.0, 0.0, 0.5], r0, r_out)
        o = classify_run(sol, rho_of, f"root ρ0={rt:.4g}")
        print_row(o)
        if o:
            print(f"    M~{o['M']:.4g}  φmax={o['phi_max']:.4f}  Dend={o['Dend']:.4g}")

    # Also Q0=0 shoot
    print("\n[7] Shoot S(r_out=6)=0 vs ρ0 (Q0=0 pure matter kick)")

    def S_out0(rho0):
        sol, _ = integrate(float(rho0), 1.0, [1.0, 0.0, 0.0, 0.0], r0, r_out)
        if len(sol.t) < 2:
            return 1e3
        return float(sol.y[1][-1])

    Ss0 = [S_out0(rh) for rh in rhos]
    for rh, s in zip(rhos[::5], Ss0[::5]):
        print(f"  ρ0={rh:.3e}  S(6)={s:+.4f}")
    roots0 = []
    for i in range(len(rhos) - 1):
        if np.isfinite(Ss0[i]) and np.isfinite(Ss0[i + 1]) and Ss0[i] * Ss0[i + 1] < 0:
            if abs(Ss0[i]) < 500 and abs(Ss0[i + 1]) < 500:
                try:
                    roots0.append(brentq(S_out0, rhos[i], rhos[i + 1]))
                except Exception:
                    pass
    print(f"  roots S(6)=0 (Q0=0): {roots0 if roots0 else 'none'}")

    print("\nDONE WP2")


if __name__ == "__main__":
    main()
