#!/usr/bin/env python3
"""
S6 — Deeper free continuum census (OBSERVE only).

Correct MS on simple metric:
  m' = 4π r² ρ,  A = 1 - 2m/r
  ⇒ p_r = -ρ, p_⊥ from A (when A smooth)
  edge when A→0 ⇔ m→r/2 (critical close)

Scans:
  (A) free power-law ρ ∝ r^α  (α free grid)
  (B) free A = 1 - c r^p       (p free grid)
  (C) BAO/SNe readout *character* on survivors — ratios of shapes, no data fit

No χ² selector. No preferred profile. No mechanism.

Re-run: python3 simple_metric_S6_deeper_census.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent


def integrate_ms(rho_fn, r_max=3.0, n=800, r_min=1e-4):
    """Integrate m' = 4π r² ρ from near 0; return grids + edge if any."""
    rr = np.linspace(r_min, r_max, n)
    m = np.zeros_like(rr)
    for i in range(1, len(rr)):
        r0, r1 = rr[i - 1], rr[i]
        mp0 = 4 * np.pi * r0**2 * max(rho_fn(r0), 0.0)
        mp1 = 4 * np.pi * r1**2 * max(rho_fn(r1), 0.0)
        m[i] = m[i - 1] + 0.5 * (mp0 + mp1) * (r1 - r0)
    A = 1.0 - 2.0 * m / rr
    edge_i = None
    for i, Ai in enumerate(A):
        if Ai <= 1e-10:
            edge_i = i
            break
    return rr, m, A, edge_i


def lowz_dL_power(rr, A, z_lo=1e-4, z_hi=0.05):
    """Estimate d_L ~ z^p near low z (where A>0)."""
    ok = A > 0.05
    if ok.sum() < 20:
        return None
    r = rr[ok]
    z = 1.0 / np.sqrt(A[ok]) - 1.0
    dL = (1.0 + z) ** 2 * r
    mask = (z > z_lo) & (z < z_hi) & (dL > 0)
    if mask.sum() < 8:
        return None
    p = np.polyfit(np.log(z[mask]), np.log(dL[mask]), 1)[0]
    return float(p)


def anisotropy_at(rr, A, m, frac=0.3):
    """
    p_⊥/ρ from finite differences on A (correct continuum).
    ρ = m'/(4πr²), p_r=-ρ,
    p_⊥ = (r A'' + 2 A')/(16π r)
    """
    # pick interior index
    i = int(frac * (len(rr) - 1))
    i = max(2, min(i, len(rr) - 3))
    if A[i] <= 0:
        return None
    # derivatives
    Ap = np.gradient(A, rr)
    App = np.gradient(Ap, rr)
    r = rr[i]
    rho = (1 - A[i] - r * Ap[i]) / (8 * np.pi * r**2)
    if abs(rho) < 1e-30:
        return None
    pt = (r * App[i] + 2 * Ap[i]) / (16 * np.pi * r)
    return float(pt / rho)


def bao_shape_vector(rr, A, z_anchors=(0.2, 0.5, 1.0, 1.5)):
    """
    Character only: D_M(z) at anchor redshifts, normalized by D_M(z=0.5).
    D_M = r/√A = r(1+z). Build r(z) by invert z(r).
    """
    ok = A > 0.02
    r = rr[ok]
    z = 1.0 / np.sqrt(A[ok]) - 1.0
    # monotonic z?
    if len(z) < 10 or np.any(np.diff(z) <= 0):
        # allow weak non-mono by sort unique
        order = np.argsort(z)
        z, r = z[order], r[order]
        # drop duplicates
        _, idx = np.unique(np.round(z, 8), return_index=True)
        z, r = z[idx], r[idx]
    if len(z) < 10:
        return None
    zmax = float(z[-1])
    # D_M = r (1+z) with D_A = r
    DM = r * (1.0 + z)
    # normalize at z=0.5 if reachable
    out = {"z_max": zmax, "ratios": {}}
    z_ref = 0.5
    if zmax < z_ref:
        return {"z_max": zmax, "ratios": None, "note": "z_max < 0.5"}
    DM_ref = float(np.interp(z_ref, z, DM))
    if DM_ref <= 0:
        return None
    for za in z_anchors:
        if za > zmax * 0.98:
            out["ratios"][str(za)] = None
        else:
            out["ratios"][str(za)] = float(np.interp(za, z, DM) / DM_ref)
    return out


def main():
    out = {
        "mode": "OBSERVE",
        "power_law_rho": [],
        "power_A": [],
        "bao_characters": {},
        "structure_notes": [],
    }

    print("=" * 70)
    print("S6 deeper free continuum census — observe only")
    print("=" * 70)

    # ----- (A) free ρ = ρ0 r^α -----
    print("\n[A] Power-law density ρ = ρ0 · r^α")
    # choose ρ0 so that a range of α can hit edge; scan ρ0 too lightly
    alphas = [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
    rho0s = [0.02, 0.05, 0.1, 0.2]

    for alpha in alphas:
        for rho0 in rho0s:
            # avoid non-integrable mess at 0 for α ≤ -3; our α ≥ -1.5 OK with r_min
            def rho_fn(r, a=alpha, c=rho0):
                return c * (r ** a)

            rr, m, A, edge_i = integrate_ms(rho_fn, r_max=4.0, n=1000)
            rec = {
                "alpha": alpha,
                "rho0": rho0,
                "edge": None if edge_i is None else float(rr[edge_i]),
                "M_at_edge": None if edge_i is None else float(m[edge_i]),
                "half_edge": None if edge_i is None else float(0.5 * rr[edge_i]),
                "A_min": float(np.min(A)),
                "lowz_p": lowz_dL_power(rr, A),
                "pt_over_rho@0.3": anisotropy_at(rr, A, m, 0.3),
            }
            if edge_i is not None:
                # critical check: m(edge) ≈ edge/2
                rec["critical_ratio_m_over_rhalf"] = float(
                    m[edge_i] / (0.5 * rr[edge_i])
                )
            out["power_law_rho"].append(rec)

    # summary table: for each α, fraction that hit edge + typical lowz_p when edged
    print(f"  {'α':>6} {'ρ0':>6} {'edge':>8} {'lowz_p':>8} {'p⊥/ρ':>8} {'m/(X/2)':>8}")
    for rec in out["power_law_rho"]:
        if rec["rho0"] not in (0.05, 0.1):
            continue  # print subset
        e = f"{rec['edge']:.3f}" if rec["edge"] else "—"
        p = f"{rec['lowz_p']:.3f}" if rec["lowz_p"] else "—"
        an = f"{rec['pt_over_rho@0.3']:.3f}" if rec["pt_over_rho@0.3"] is not None else "—"
        cr = (
            f"{rec['critical_ratio_m_over_rhalf']:.4f}"
            if rec.get("critical_ratio_m_over_rhalf")
            else "—"
        )
        print(f"  {rec['alpha']:6.1f} {rec['rho0']:6.2f} {e:>8} {p:>8} {an:>8} {cr:>8}")

    # aggregate by alpha
    by_a = {}
    for rec in out["power_law_rho"]:
        by_a.setdefault(rec["alpha"], []).append(rec)
    print("\n  By α: #edge / n, mean lowz_p (edged only)")
    alpha_summary = {}
    for a, rows in sorted(by_a.items()):
        edged = [x for x in rows if x["edge"] is not None]
        ps = [x["lowz_p"] for x in edged if x["lowz_p"] is not None]
        alpha_summary[str(a)] = {
            "n": len(rows),
            "n_edge": len(edged),
            "mean_lowz_p_edged": float(np.mean(ps)) if ps else None,
        }
        print(
            f"    α={a:+.1f}: edge {len(edged)}/{len(rows)}, "
            f"mean lowz_p={np.mean(ps) if ps else float('nan'):.3f}"
        )
    out["alpha_summary"] = alpha_summary

    # ----- (B) free A = 1 - c r^p -----
    print("\n[B] Free lapse family A = 1 - c r^p  (c>0, p>0)")
    # edge at r_edge = c^{-1/p}, m = (c/2) r^{p+1} wait m = r(1-A)/2 = (c/2) r^{p+1}
    # At edge m = c/2 * c^{-(p+1)/p} = (1/2) c^{-1/p} = r_edge/2 ✓ always critical
    ps = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
    for p in ps:
        c = 0.2  # edge at (1/c)^{1/p}
        r_edge = c ** (-1.0 / p)

        def A_of_r(r, pp=p, cc=c):
            return 1.0 - cc * r**pp

        rr = np.linspace(1e-4, 0.98 * r_edge, 600)
        A = A_of_r(rr)
        m = rr * (1 - A) / 2
        # rho from formula
        # Ap = -c p r^{p-1}
        Ap = -c * p * rr ** (p - 1)
        rho = (1 - A - rr * Ap) / (8 * np.pi * rr**2)
        rec = {
            "p": p,
            "c": c,
            "r_edge": float(r_edge),
            "M": float(r_edge / 2),
            "lowz_p": lowz_dL_power(rr, A),
            "rho_center_class": (
                "singular_or_divergent"
                if p < 2
                else "finite"
                if p == 2
                else "rho→0 at center"
            ),
            "pt_over_rho_mid": None,
        }
        # analytic ρ ∝ r^{p-2} for A=1-c r^p
        # mid anisotropy
        mid = len(rr) // 2
        App = -c * p * (p - 1) * rr[mid] ** (p - 2)
        pt = (rr[mid] * App + 2 * Ap[mid]) / (16 * np.pi * rr[mid])
        if abs(rho[mid]) > 1e-30:
            rec["pt_over_rho_mid"] = float(pt / rho[mid])
        # ρ exponent
        rec["rho_scaling"] = f"∝ r^{p-2}"
        out["power_A"].append(rec)
        print(
            f"  p={p:.1f}: edge={r_edge:.3f}, lowz_p={rec['lowz_p']}, "
            f"ρ~r^{p-2}, p⊥/ρ_mid={rec['pt_over_rho_mid']}"
        )

    out["structure_notes"].append(
        "For A=1-c r^p, edge always critical m=X/2; ρ∝r^{p-2}; "
        "p=1 → ρ∝1/r linear-center; p=2 → const ρ regular; p>2 → ρ→0 at center."
    )

    # ----- (C) BAO shape characters (normalized), no data -----
    print("\n[C] BAO D_M shape character (normalized to z=0.5), no survey fit")
    characters = {}
    # build a few named tiles
    tiles = {}
    # linear ceiling X=1
    X = 1.0
    rr = np.linspace(1e-4, 0.98 * X, 800)
    A = 1 - rr / X
    tiles["linear_X1"] = (rr, A)
    # quadratic edge at 1
    a2 = 1.0
    rr2 = np.linspace(1e-4, 0.98, 800)
    tiles["quad_edge1"] = (rr2, 1 - a2 * rr2**2)
    # p=3
    c3 = 1.0
    re = c3 ** (-1 / 3)
    rr3 = np.linspace(1e-4, 0.98 * re, 800)
    tiles["power3"] = (rr3, 1 - c3 * rr3**3)
    # soft const rho no edge in box — skip if zmax small
    rr4, m4, A4, e4 = integrate_ms(lambda r: 0.05, r_max=2.0, n=800)
    tiles["const_rho_0p05"] = (rr4, A4)

    print(f"  {'tile':<18} zmax   DM(0.2)/DM0.5  DM(1)/DM0.5  DM(1.5)/DM0.5")
    for name, (rrt, At) in tiles.items():
        sh = bao_shape_vector(rrt, At)
        characters[name] = sh
        if sh is None or sh.get("ratios") is None:
            print(f"  {name:<18} (no full shape)")
            continue
        rats = sh["ratios"]
        print(
            f"  {name:<18} {sh['z_max']:.3f}  "
            f"{rats.get('0.2')!s:>12}  {rats.get('1.0')!s:>10}  {rats.get('1.5')!s:>10}"
        )
    out["bao_characters"] = characters

    # analytic T3 ratios for check
    # D_M/X = z(z+2)/(1+z); ratio to z=0.5
    def dm_t3(z):
        return z * (z + 2) / (1 + z)

    t3 = {str(z): dm_t3(z) / dm_t3(0.5) for z in (0.2, 0.5, 1.0, 1.5)}
    out["bao_T3_analytic_norm"] = t3
    print("  T3 analytic norms:", t3)

    # ----- structure synthesis (characterize, not rank) -----
    print("\n[D] Structure map (what the space is doing)")
    notes = [
        "Center type ↔ low-z light: regular (A'=0, ρ finite) → d_L~z^0.5; "
        "linear-type (ρ~1/r, A'≠0) → d_L~z; p>2 fills → ρ→0 center, soft-ish.",
        "Every outer A=0 wall is critical: m=X/2 identity (numeric ratio ~1).",
        "Anisotropy p⊥/ρ is profile-dependent (not free fluid with independent p).",
        "BAO D_M(z) shape differs across tiles when normalized — multi-probe can "
        "characterize, not yet used to pick a tile.",
        "Still no unique selection; still no R1 glue; still no mechanism.",
    ]
    for n in notes:
        print("  •", n)
        out["structure_notes"].append(n)

    out["verdict"] = (
        "Deeper census: power-law ρ and A=1-c r^p families show a continuous "
        "character map (center type, edge yes/no, low-z power, BAO shape ratios). "
        "Critical closure universal at walls. No winner selected."
    )
    print("\n" + out["verdict"])

    path = ROOT / "simple_metric_S6_deeper_census_out.json"

    def san(o):
        if isinstance(o, dict):
            return {str(k): san(v) for k, v in o.items()}
        if isinstance(o, list):
            return [san(v) for v in o]
        if isinstance(o, (float, np.floating)):
            if np.isnan(o) or np.isinf(o):
                return str(o)
            return float(o)
        if isinstance(o, (int, np.integer)):
            return int(o)
        if isinstance(o, (bool, str)) or o is None:
            return o
        return str(o)

    path.write_text(json.dumps(san(out), indent=2))
    print(f"Wrote {path.name}")
    print("DONE")
    return out


if __name__ == "__main__":
    main()
