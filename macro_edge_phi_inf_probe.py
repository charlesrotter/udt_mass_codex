#!/usr/bin/env python3
"""
Probe: finite-core continuum matter — does φ→+∞ develop at finite chart radius?
Contract: macro_edge_phi_inf_CONTRACT.md
Frame:    macro_xmax_limit_FRAME.md  (x_max ~ limit edge)
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

Z = 1.0
G = 1.0  # geometric units
C = 1.0


def action_rhs(alpha, rc, mu0):
    def f(r, y):
        D, Dp, phi, pi = y
        De = max(abs(D), 1e-16)
        php = pi / (Z * De**2)
        mu = mu0 * np.exp(-(r / rc) ** 2)
        w = np.exp(alpha * phi)
        # soft cap exp(2phi) to avoid pure overflow noise; still allows large phi
        e2 = np.exp(min(2.0 * phi, 40.0))
        em2 = np.exp(min(-2.0 * phi, 40.0)) if phi < 0 else np.exp(-2.0 * phi)
        # when phi large positive, e^{-2phi} tiny
        if phi > 20:
            em2 = 0.0
        pip = 4.0 * em2 * Dp**2 - alpha * De**2 * mu * w
        Dpp = 2.0 * php * Dp - e2 * (Z / 4.0) * De * php**2 + e2 * 0.5 * De * mu * w
        if not np.isfinite(Dpp):
            Dpp = 0.0
        if not np.isfinite(pip):
            pip = 0.0
        return [Dp, float(np.clip(Dpp, -1e10, 1e10)), php, float(np.clip(pip, -1e10, 1e10))]

    return f


def jet_rhs(alpha, rc, s0):
    def f(r, y):
        D, Dp, phi, pi = y
        De = max(abs(D), 1e-16)
        php = pi / (Z * De**2)
        sig = s0 * np.exp(-(r / rc) ** 2)
        em2 = np.exp(-2.0 * phi) if phi < 20 else 0.0
        e2 = np.exp(min(2.0 * phi, 40.0))
        pip = 4.0 * em2 * Dp**2 + alpha * np.exp(alpha * phi) * sig
        Dpp = 2.0 * php * Dp - e2 * (Z / 4.0) * De * php**2
        if not np.isfinite(Dpp):
            Dpp = 0.0
        if not np.isfinite(pip):
            pip = 0.0
        return [Dp, float(np.clip(Dpp, -1e10, 1e10)), php, float(np.clip(pip, -1e10, 1e10))]

    return f


def event_phi_cut(phi_cut):
    def ev(r, y):
        return y[2] - phi_cut

    ev.terminal = True
    ev.direction = 1
    return ev


def event_D_collapse(D_floor=1e-6):
    def ev(r, y):
        return y[0] - D_floor

    ev.terminal = True
    ev.direction = -1
    return ev


def mass_proxy(sol, alpha, rc, mu0):
    """Crude M ~ int 4π D^2 μ e^{αφ} dr  (stand-in energy density weight)."""
    r = sol.t
    D, _, phi, _ = sol.y
    if len(r) < 2:
        return 0.0
    mu = mu0 * np.exp(-(r / rc) ** 2)
    dens = 4.0 * np.pi * D**2 * mu * np.exp(alpha * phi)
    return float(np.trapz(dens, r))


def integrate_core(alpha, rc, mu0, Dc, r_max=50.0, phi_cut=8.0):
    y0 = [Dc, 0.0, 0.0, 0.0]
    f = action_rhs(alpha, rc, mu0)
    sol = solve_ivp(
        f,
        (1e-6, r_max),
        y0,
        method="RK45",
        rtol=1e-6,
        atol=1e-8,
        max_step=0.05,
        events=[event_phi_cut(phi_cut), event_D_collapse(1e-6)],
    )
    return sol


def integrate_jet(alpha, rc, c3, r_max=50.0, phi_cut=8.0, eps=1e-3):
    if alpha >= 0:
        return None
    s0 = -4.0 / alpha
    den = rc**2 * (3 * Z + 2 * alpha + 4)
    if abs(den) < 1e-14:
        return None
    p2 = 2.0 * (6.0 * c3 * rc**2 + 1.0) / den
    D = eps + c3 * eps**3
    Dp = 1.0 + 3.0 * c3 * eps**2
    phi = p2 * eps**2
    php = 2.0 * p2 * eps
    pi = Z * D**2 * php
    sol = solve_ivp(
        jet_rhs(alpha, rc, s0),
        (eps, r_max),
        [D, Dp, phi, pi],
        method="RK45",
        rtol=1e-6,
        atol=1e-8,
        max_step=0.05,
        events=[event_phi_cut(phi_cut), event_D_collapse(1e-6)],
    )
    return sol


def classify(sol, phi_cut, r_max, label, M=None):
    if sol is None or len(sol.t) < 2:
        print(f"  [{label}] empty")
        return None
    r = sol.t
    D, Dp, phi, pi = sol.y
    phi_max = float(np.nanmax(phi))
    r_end = float(r[-1])
    D_end = float(D[-1])
    D_min = float(np.min(D))
    # events
    hit_phi = sol.t_events is not None and len(sol.t_events) > 0 and len(sol.t_events[0]) > 0
    hit_D = sol.t_events is not None and len(sol.t_events) > 1 and len(sol.t_events[1]) > 0
    r_phi = float(sol.t_events[0][0]) if hit_phi else None
    r_D = float(sol.t_events[1][0]) if hit_D else None

    mode = "saturated_or_box"
    if hit_D and (not hit_phi or (r_D is not None and r_phi is not None and r_D <= r_phi)):
        mode = "D_collapse"
    elif hit_phi:
        mode = "phi_cut_candidate"
    elif not sol.success and phi_max > 0.5 * phi_cut:
        mode = "stiff_high_phi"
    elif not sol.success and D_min < 0.1 * abs(D[0]):
        mode = "stiff_collapse"
    elif sol.success and r_end >= r_max - 1e-6:
        mode = "reached_box"
        if phi_max < 0.5:
            mode = "trivial_or_flat"

    # proper distance proxy int e^phi dr (truncated)
    try:
        prop = float(np.trapz(np.exp(np.clip(phi, -5, 20)), r))
    except Exception:
        prop = float("nan")

    scale = None
    if M is not None and M > 0 and r_phi is not None:
        scale = r_phi / M  # geometric G=c=1
    elif M is not None and M > 0:
        scale = r_end / M

    out = {
        "label": label,
        "mode": mode,
        "ok": bool(sol.success),
        "r_end": r_end,
        "phi_max": phi_max,
        "phi_end": float(phi[-1]),
        "D_end": D_end,
        "D_min": D_min,
        "r_phi": r_phi,
        "r_D": r_D,
        "prop_proxy": prop,
        "M_proxy": M,
        "r_over_M": scale,
        "n": len(r),
    }
    extra = f" mode={mode}"
    if r_phi is not None:
        extra += f" r_φ={r_phi:.4g}"
    if r_D is not None:
        extra += f" r_D={r_D:.4g}"
    if scale is not None:
        extra += f" r/M~{scale:.3g}"
    print(
        f"  [{label}] r→{r_end:.4g} φmax={phi_max:.3f} Dend={D_end:.3g} "
        f"M~{M if M is not None else float('nan'):.3g}{extra}"
    )
    return out


def main():
    print("=" * 70)
    print("EDGE PROBE: φ→∞ at finite chart radius? (finite-core + jet control)")
    print("=" * 70)

    rows = []
    phi_cuts = (5.0, 8.0, 12.0)
    # use one primary cut for scan; mention others in a few spots
    phi_cut = 8.0
    r_max = 50.0

    print("\n=== A. Finite-core + action μ (primary) φ_cut=8, r_max=50 ===")
    grid = []
    for alpha in (-1.0, -0.5, 0.0, 0.5):
        for Dc in (0.5, 1.0, 2.0):
            for rc in (0.5, 1.0, 2.0):
                for mu0 in (0.0, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0):
                    grid.append((alpha, Dc, rc, mu0))

    for alpha, Dc, rc, mu0 in grid:
        lab = f"core a={alpha:g} Dc={Dc:g} rc={rc:g} mu0={mu0:g}"
        sol = integrate_core(alpha, rc, mu0, Dc, r_max=r_max, phi_cut=phi_cut)
        M = mass_proxy(sol, alpha, rc, mu0) if sol is not None else 0.0
        row = classify(sol, phi_cut, r_max, lab, M=M)
        if row:
            row["family"] = "core"
            rows.append(row)

    print("\n=== B. Jet control (expect no φ edge; Δφ saturates) ===")
    for alpha in (-2.0, -1.0, -0.5):
        for rc in (1.0, 2.0):
            lab = f"jet a={alpha:g} rc={rc:g}"
            sol = integrate_jet(alpha, rc, 0.0, r_max=r_max, phi_cut=phi_cut)
            row = classify(sol, phi_cut, r_max, lab, M=None)
            if row:
                row["family"] = "jet"
                rows.append(row)

    print("\n=== C. High φ_cut stress on a few cores that hit cut=8 ===")
    candidates = [r for r in rows if r.get("mode") == "phi_cut_candidate"]
    # re-run top candidates at higher cut if any; else pick high phi_max cores
    if not candidates:
        print("  (no phi_cut_candidate at 8 — sampling highest phi_max cores)")
        cores = [r for r in rows if r.get("family") == "core"]
        cores_sorted = sorted(cores, key=lambda x: -x["phi_max"])[:6]
        for r0 in cores_sorted:
            # parse label
            parts = r0["label"].split()
            kv = {p.split("=")[0]: float(p.split("=")[1]) for p in parts[1:]}
            for pc in (12.0, 20.0):
                sol = integrate_core(kv["a"], kv["rc"], kv["mu0"], kv["Dc"], r_max=80.0, phi_cut=pc)
                M = mass_proxy(sol, kv["a"], kv["rc"], kv["mu0"])
                row = classify(sol, pc, 80.0, r0["label"] + f" cut={pc:g}", M=M)
                if row:
                    row["family"] = "core_hi"
                    rows.append(row)
    else:
        for r0 in candidates[:8]:
            parts = r0["label"].split()
            kv = {p.split("=")[0]: float(p.split("=")[1]) for p in parts[1:]}
            for pc in (12.0, 20.0):
                sol = integrate_core(kv["a"], kv["rc"], kv["mu0"], kv["Dc"], r_max=80.0, phi_cut=pc)
                M = mass_proxy(sol, kv["a"], kv["rc"], kv["mu0"])
                row = classify(sol, pc, 80.0, r0["label"] + f" cut={pc:g}", M=M)
                if row:
                    row["family"] = "core_hi"
                    rows.append(row)

    # Summary
    print("\n" + "=" * 70)
    print("CLASSIFICATION")
    print("=" * 70)
    cores = [r for r in rows if r.get("family") == "core"]
    jets = [r for r in rows if r.get("family") == "jet"]
    by_mode = {}
    for r in cores:
        by_mode.setdefault(r["mode"], []).append(r)

    print(f"  Core runs (primary): {len(cores)}")
    for m, lst in sorted(by_mode.items(), key=lambda x: -len(x[1])):
        print(f"    {m}: {len(lst)}")

    cand = by_mode.get("phi_cut_candidate", [])
    coll = by_mode.get("D_collapse", [])
    box = [r for r in cores if r["mode"] in ("reached_box", "saturated_or_box", "trivial_or_flat")]
    print(f"\n  X1 phi_cut candidates: {len(cand)}")
    print(f"  X3 D_collapse failures: {len(coll)}")
    print(f"  X0/box-like (no large φ): {len(box)}")

    if cand:
        print("  sample candidates:")
        for r in sorted(cand, key=lambda x: -x["phi_max"])[:10]:
            print(
                f"    {r['label']}: r_φ={r['r_phi']:.4g} φmax={r['phi_max']:.2f} "
                f"Dend={r['D_end']:.3g} M~{r['M_proxy']:.3g} r/M~{r['r_over_M']}"
            )
    else:
        print("  No φ_cut candidates in primary core grid.")
        top = sorted(cores, key=lambda x: -x["phi_max"])[:8]
        print("  highest φ_max cores:")
        for r in top:
            print(
                f"    {r['label']}: φmax={r['phi_max']:.3f} r_end={r['r_end']:.3g} mode={r['mode']}"
            )

    print(f"\n  Jet controls: {len(jets)}")
    for r in jets:
        print(f"    {r['label']}: φmax={r['phi_max']:.3f} mode={r['mode']} r_end={r['r_end']:.3g}")

    # X4: r/M for candidates
    scales = [r["r_over_M"] for r in cand if r.get("r_over_M") is not None]
    if scales:
        print(f"\n  X4 r_φ/M_proxy among candidates: min={min(scales):.3g} max={max(scales):.3g} med={np.median(scales):.3g}")

    print("\nDONE")
    return rows


if __name__ == "__main__":
    main()
