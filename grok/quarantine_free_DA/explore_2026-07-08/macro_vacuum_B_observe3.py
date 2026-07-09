#!/usr/bin/env python3
"""
OBSERVE-3: survival window for vacuum B throat family.

For seeds (Z, u*=phi'*, D*) at throat r*=1, phi*=0, D'=0:
  integrate OUT to r_out and IN to r_in;
  classify SURVIVE (D>D_floor both sides) vs PINCH_OUT / PINCH_IN / BOTH / FAIL.

Also: deeper inward scan (r_in -> small) for mild seeds — does D always hit 0?

Mode: OBSERVE. No sources. No sky.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict

import numpy as np
from scipy.integrate import solve_ivp

from macro_vacuum_B_observe1 import system_rhs

PREMISES = {
    "W": "1 (option B)",
    "L_m": "0",
    "seed": "throat r*=1, phi*=0, D'=0; scan Z, u*, D*",
    "survive_def": "D > D_floor on whole path to r_out and r_in",
    "mode": "OBSERVE not TARGET",
}


@dataclass
class WindowPoint:
    Z: float
    u: float
    D_star: float
    r_out_reached: float
    r_in_reached: float
    D_min_out: float
    D_min_in: float
    phi_max_abs: float
    label: str  # SURVIVE | PINCH_OUT | PINCH_IN | PINCH_BOTH | FAIL
    notes: str


def integrate_to(
    Z: float,
    r0: float,
    y0: np.ndarray,
    r_target: float,
    D_floor: float = 1e-6,
    phi_cap: float = 25.0,
    max_step: float = 0.05,
):
    def fun(r, y):
        return system_rhs(r, y, Z)

    def hit_D(r, y):
        return y[2] - D_floor

    hit_D.terminal = True
    hit_D.direction = -1

    def hit_phi(r, y):
        return phi_cap - abs(y[0])

    hit_phi.terminal = True
    hit_phi.direction = -1

    sol = solve_ivp(
        fun,
        (r0, r_target),
        y0,
        method="DOP853",
        rtol=1e-8,
        atol=1e-10,
        events=(hit_D, hit_phi),
        max_step=max_step,
    )
    if sol.t.size < 1:
        return {
            "ok": False,
            "r_end": r0,
            "D_min": float(y0[2]),
            "phi_abs_max": abs(float(y0[0])),
            "hit_D": False,
            "hit_phi": False,
            "success": False,
        }
    D = sol.y[2]
    phi = sol.y[0]
    hit_d = bool(sol.t_events and len(sol.t_events[0]) > 0)
    hit_p = bool(sol.t_events and len(sol.t_events[1]) > 0)
    return {
        "ok": True,
        "r_end": float(sol.t[-1]),
        "D_min": float(np.min(D)),
        "phi_abs_max": float(np.max(np.abs(phi))),
        "hit_D": hit_d,
        "hit_phi": hit_p,
        "success": bool(sol.success),
    }


def classify_point(
    Z: float,
    u: float,
    D_star: float,
    r_star: float = 1.0,
    r_out: float = 5.0,
    r_in: float = 0.05,
    D_floor: float = 1e-6,
) -> WindowPoint:
    y0 = np.array([0.0, u, D_star, 0.0], dtype=float)
    out = integrate_to(Z, r_star, y0, r_out, D_floor=D_floor)
    inn = integrate_to(Z, r_star, y0, r_in, D_floor=D_floor)

    pinch_out = out["hit_D"] or (out["D_min"] <= D_floor * 10 and not out["success"])
    pinch_in = inn["hit_D"] or (inn["D_min"] <= D_floor * 10 and not inn["success"])
    # stricter: reached target without hit_D
    out_ok = out["success"] and not out["hit_D"] and out["D_min"] > D_floor
    in_ok = inn["success"] and not inn["hit_D"] and inn["D_min"] > D_floor

    if out_ok and in_ok:
        label = "SURVIVE"
    elif (not out_ok) and (not in_ok):
        label = "PINCH_BOTH" if (pinch_out or pinch_in) else "FAIL"
    elif not out_ok:
        label = "PINCH_OUT" if pinch_out or out["hit_D"] else "FAIL_OUT"
    else:
        label = "PINCH_IN" if pinch_in or inn["hit_D"] else "FAIL_IN"

    notes = f"out_r={out['r_end']:.3f},in_r={inn['r_end']:.3f}"
    if out["hit_phi"] or inn["hit_phi"]:
        notes += ";phi_cap"

    return WindowPoint(
        Z=Z,
        u=u,
        D_star=D_star,
        r_out_reached=out["r_end"],
        r_in_reached=inn["r_end"],
        D_min_out=out["D_min"],
        D_min_in=inn["D_min"],
        phi_max_abs=max(out["phi_abs_max"], inn["phi_abs_max"]),
        label=label,
        notes=notes,
    )


def u_critical_bisect(
    Z: float,
    D_star: float,
    r_out: float = 5.0,
    r_in: float = 0.05,
    u_hi: float = 2.0,
    nbit: int = 24,
) -> dict:
    """Largest |u| with SURVIVE for +u branch (phi' > 0)."""
    # check u=0 always survive
    lo, hi = 0.0, u_hi
    # ensure hi pinches
    p_hi = classify_point(Z, hi, D_star, r_out=r_out, r_in=r_in)
    if p_hi.label == "SURVIVE":
        return {
            "Z": Z,
            "D_star": D_star,
            "u_crit_plus": None,
            "note": f"all up to u={u_hi} SURVIVE on window",
            "hi_label": p_hi.label,
        }
    for _ in range(nbit):
        mid = 0.5 * (lo + hi)
        lab = classify_point(Z, mid, D_star, r_out=r_out, r_in=r_in).label
        if lab == "SURVIVE":
            lo = mid
        else:
            hi = mid
    return {
        "Z": Z,
        "D_star": D_star,
        "u_crit_plus": lo,
        "u_first_fail": hi,
        "fail_label": classify_point(Z, hi, D_star, r_out=r_out, r_in=r_in).label,
        "window": f"r in [{r_in},{r_out}]",
    }


def deep_inward_probe(Z: float, u: float, D_star: float, r_star: float = 1.0) -> dict:
    """How far inward before D hits floor (if ever within r_in=1e-4)."""
    y0 = np.array([0.0, u, D_star, 0.0], dtype=float)
    res = integrate_to(Z, r_star, y0, 1e-4, D_floor=1e-6, max_step=0.02)
    return {
        "Z": Z,
        "u": u,
        "D_star": D_star,
        "r_end": res["r_end"],
        "D_min": res["D_min"],
        "hit_D": res["hit_D"],
        "success_to_1e-4": res["success"] and not res["hit_D"],
    }


def main() -> None:
    print("=" * 70)
    print("OBSERVE-3 survival window + deep inward")
    print("=" * 70)

    r_out, r_in = 5.0, 0.05
    Zs = [0.5, 1.0, 2.0, 4.0, 8.0]
    us = [0.0, 0.02, 0.05, 0.08, 0.1, 0.15, 0.2, 0.3, 0.5, -0.1, -0.2]
    Ds = [0.5, 1.0, 2.0]

    grid: list[WindowPoint] = []
    print("\n--- Grid (r window [0.05, 5]) ---")
    for Z in Zs:
        for D_star in Ds:
            for u in us:
                wp = classify_point(Z, u, D_star, r_out=r_out, r_in=r_in)
                grid.append(wp)

    # summary table counts
    from collections import Counter

    print("\nLabel counts by Z (all D*, all u):")
    for Z in Zs:
        c = Counter(p.label for p in grid if p.Z == Z)
        print(f"  Z={Z:g}: {dict(c)}")

    print("\nSURVIVE fraction by |u| (all Z, D*):")
    for u in us:
        pts = [p for p in grid if p.u == u]
        nS = sum(1 for p in pts if p.label == "SURVIVE")
        print(f"  u={u:+g}: {nS}/{len(pts)} SURVIVE")

    print("\n--- u_crit bisect (SURVIVE up to r in [0.05,5], +u) ---")
    crits = []
    for Z in Zs:
        for D_star in Ds:
            cr = u_critical_bisect(Z, D_star, r_out=r_out, r_in=r_in, u_hi=3.0)
            crits.append(cr)
            print(
                f"  Z={Z:g} D*={D_star:g}: u_crit+ ≈ {cr.get('u_crit_plus')} "
                f"(first fail {cr.get('u_first_fail')}, {cr.get('fail_label') or cr.get('note')})"
            )

    # Second window: longer outward only interest r_out=10
    print("\n--- u_crit for longer outward window [0.05, 10] ---")
    crits_long = []
    for Z in [1.0, 4.0, 8.0]:
        for D_star in [1.0]:
            cr = u_critical_bisect(Z, D_star, r_out=10.0, r_in=0.05, u_hi=3.0)
            crits_long.append(cr)
            print(f"  Z={Z:g} D*=1: u_crit+ ≈ {cr.get('u_crit_plus')}")

    print("\n--- Deep inward (to 1e-4) mild seeds ---")
    deep = []
    for Z in [1.0, 4.0, 8.0]:
        for u in [0.05, 0.1, 0.2]:
            d = deep_inward_probe(Z, u, 1.0)
            deep.append(d)
            print(
                f"  Z={Z:g} u={u:g}: r_end={d['r_end']:.4g} D_min={d['D_min']:.4g} "
                f"hit_D={d['hit_D']} ok_to_1e-4={d['success_to_1e-4']}"
            )

    # Scaling check: does u_crit scale with 1/sqrt(Z) or 1/D*?
    print("\n--- Scaling peek: u_crit * sqrt(Z) and u_crit * D* ---")
    for cr in crits:
        uc = cr.get("u_crit_plus")
        if uc is None:
            continue
        Z, Ds_ = cr["Z"], cr["D_star"]
        print(
            f"  Z={Z:g} D*={Ds_:g}: u_c={uc:.5f}  u_c*sqrt(Z)={uc*np.sqrt(Z):.5f}  "
            f"u_c*D*={uc*Ds_:.5f}  u_c*D**sqrt(Z)={uc*Ds_*np.sqrt(Z):.5f}"
        )

    # Compact survive matrix for D*=1
    print("\n--- Matrix label D*=1 (rows Z, cols u) ---")
    u_cols = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5]
    hdr = "Z\\\\u".ljust(8) + "".join(f"{u:+.2f}".center(12) for u in u_cols)
    print(hdr)
    for Z in Zs:
        row = f"{Z:<8g}"
        for u in u_cols:
            lab = next(p.label for p in grid if p.Z == Z and p.D_star == 1.0 and p.u == u)
            short = {
                "SURVIVE": "S",
                "PINCH_OUT": "Po",
                "PINCH_IN": "Pi",
                "PINCH_BOTH": "Pb",
            }.get(lab, lab[:4])
            row += short.center(12)
        print(row)

    out = {
        "premises": PREMISES,
        "window": {"r_in": r_in, "r_out": r_out},
        "grid": [asdict(p) for p in grid],
        "u_crit": crits,
        "u_crit_long": crits_long,
        "deep_inward": deep,
    }
    path = "macro_vacuum_B_observe3_data.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {path}")
    print("DONE OBSERVE-3")


if __name__ == "__main__":
    main()
