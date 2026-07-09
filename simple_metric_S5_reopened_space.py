#!/usr/bin/env python3
"""
S5 — Re-opened solution space after S3 scar (OBSERVE only).

Correct simple-metric Einstein continuum (full curvature):
  ρ   = (1 - A - r A') / (8π r²)
  p_r = -ρ                          # identity of reciprocal metric
  p_⊥ = (r A'' + 2 A') / (16π r)
  m   = r (1 - A) / 2
  A→0 at finite X  ⇔  m(X) = X/2     # critical amount closes sphere

No dust selection. No A(r) shopping. No χ² in solve.
Probe families are FREE named tiles of the space — characterize, don't rank.

Also: R1 compensated EL residual character on each tile (A-primary contrast).
Also: multi-probe readout formulas when A>0 and φ=-½ ln A (character only).

Re-run: python3 simple_metric_S5_reopened_space.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent


def continuum_from_A(Aexpr, r, X=None):
    """Symbolic stresses + m from A(r)."""
    Ap = sp.diff(Aexpr, r)
    App = sp.diff(Ap, r)
    rho = sp.simplify((1 - Aexpr - r * Ap) / (8 * sp.pi * r**2))
    pr = sp.simplify(-rho)
    pt = sp.simplify((r * App + 2 * Ap) / (16 * sp.pi * r))
    m = sp.simplify(r * (1 - Aexpr) / 2)
    return {"rho": rho, "p_r": pr, "p_perp": pt, "m": m, "A": Aexpr}


def r1_ratio(Aexpr, r):
    """Compensated R1 residual ratio (r²φ')' / (2ρ r² A); want const Z if EL holds."""
    rho = (1 - Aexpr - r * sp.diff(Aexpr, r)) / (8 * sp.pi * r**2)
    phi = -sp.Rational(1, 2) * sp.log(Aexpr)
    LHS = sp.diff(r**2 * sp.diff(phi, r), r)
    RHS = 2 * rho * r**2 * Aexpr
    ratio = sp.simplify(LHS / RHS)
    d_ratio = sp.simplify(sp.diff(ratio, r))
    return ratio, d_ratio


def main():
    r, X, k, rs, a2, a4 = sp.symbols("r X k rs a2 a4", positive=True)
    out = {"tiles": [], "identities": {}, "census": {}}

    print("=" * 70)
    print("S5 re-opened solution space — correct continuum, no dust selection")
    print("=" * 70)

    # --- Identities (always) ---
    print("\n[0] Structural identities (any A)")
    A = sp.Function("A")(r)
    id_pr = continuum_from_A(A, r)
    print("  p_r + ρ =", sp.simplify(id_pr["p_r"] + id_pr["rho"]))
    print("  m = r(1-A)/2 =", id_pr["m"])
    out["identities"]["p_r_eq_minus_rho"] = True
    out["identities"]["m"] = "r(1-A)/2"
    out["identities"]["critical_close"] = "A(X)=0 ⇒ m(X)=X/2"

    # --- Tile catalog (FREE probes of A or equivalent ρ) ---
    # Each tile: name, A(r), domain notes, characterize ceiling / center / R1
    tiles_spec = []

    # T1 vacuum Schw
    tiles_spec.append(("T1_schw_vacuum", 1 - rs / r, {"type": "vacuum", "params": ["rs"]}))

    # T2 flat
    tiles_spec.append(("T2_flat", 1 + 0 * r, {"type": "vacuum", "params": []}))

    # T3 linear ceiling (former S3 profile — one tile among many)
    tiles_spec.append(("T3_linear_ceiling", 1 - r / X, {"type": "ceiling", "params": ["X"]}))

    # T4 quadratic (const-density-like interior, A=1-a2 r²)
    tiles_spec.append(("T4_quadratic", 1 - a2 * r**2, {"type": "regular_center", "params": ["a2"]}))

    # T5 quartic correction
    tiles_spec.append(
        ("T5_quad_plus_r4", 1 - a2 * r**2 - a4 * r**4, {"type": "regular_center", "params": ["a2", "a4"]})
    )

    # T6 Coulomb-like A = exp(-2q/r)  — not vacuum Einstein
    q = sp.symbols("q", positive=True)
    tiles_spec.append(("T6_exp_coulomb_A", sp.exp(-2 * q / r), {"type": "other", "params": ["q"]}))

    # T7 A = 1 - k r^n family sample n=3
    n = 3
    tiles_spec.append(("T7_power_r3", 1 - k * r**n, {"type": "power", "params": ["k"], "n": n}))

    print("\n[1] Tile census (characterize)")
    census = {
        "hits_outer_A0_possible": [],
        "regular_center_A1_Aprime0": [],
        "singular_center": [],
        "r1_el_holds_any_const_Z": [],
        "vacuum_rho0": [],
    }

    for name, Aexpr, meta in tiles_spec:
        print(f"\n  --- {name} ---")
        cont = continuum_from_A(Aexpr, r)
        rho, pr, pt, m = cont["rho"], cont["p_r"], cont["p_perp"], cont["m"]
        print("    ρ =", rho)
        print("    p_r =", pr)
        print("    p_⊥ =", pt)
        print("    m =", m)

        tile = {
            "name": name,
            "meta": meta,
            "rho": str(rho),
            "p_r": str(pr),
            "p_perp": str(pt),
            "m": str(m),
        }

        # Center character A(0), A'(0) when defined
        try:
            A0 = sp.limit(Aexpr, r, 0)
            Ap0 = sp.limit(sp.diff(Aexpr, r), r, 0)
            tile["A_0"] = str(A0)
            tile["Ap_0"] = str(Ap0)
            print("    A(0)→", A0, "  A'(0)→", Ap0)
            if A0 == 1 and Ap0 == 0:
                census["regular_center_A1_Aprime0"].append(name)
            if A0 != 1 or (Ap0 != 0 and Ap0 != sp.nan):
                # singular or linear-type
                if Ap0 != 0 and Ap0 is not sp.zoo:
                    census["singular_center"].append(name)
        except Exception as e:
            tile["center_note"] = str(e)
            print("    center limit:", e)

        # Outer A=0: solve A=0 for r if possible
        try:
            zeros = sp.solve(sp.Eq(Aexpr, 0), r)
            pos_zeros = []
            for z in zeros:
                if z.is_real is False:
                    continue
                pos_zeros.append(str(z))
            tile["A_zeros"] = pos_zeros
            print("    A=0 roots:", pos_zeros)
            if pos_zeros:
                census["hits_outer_A0_possible"].append(name)
        except Exception as e:
            tile["A_zeros"] = f"solve_fail:{e}"

        # Vacuum?
        if sp.simplify(rho) == 0:
            census["vacuum_rho0"].append(name)
            tile["vacuum"] = True
        else:
            tile["vacuum"] = False

        # R1 ratio
        try:
            if sp.simplify(rho) == 0:
                # vacuum: compensated R1 wants (r²φ')'=0
                phi = -sp.Rational(1, 2) * sp.log(Aexpr)
                LHS = sp.simplify(sp.diff(r**2 * sp.diff(phi, r), r))
                tile["r1_vacuum_LHS"] = str(LHS)
                holds = sp.simplify(LHS) == 0
                tile["r1_holds"] = holds
                print("    R1 vacuum (r²φ')' =", LHS, " holds?", holds)
                if holds:
                    census["r1_el_holds_any_const_Z"].append(name)
            else:
                ratio, dr = r1_ratio(Aexpr, r)
                tile["r1_ratio"] = str(ratio)
                tile["r1_ratio_r_dependent"] = sp.simplify(dr) != 0
                holds = sp.simplify(dr) == 0 and ratio != sp.nan
                # constant ratio including possibly const
                if sp.simplify(dr) == 0:
                    tile["r1_const_Z"] = str(ratio)
                    holds = True
                    census["r1_el_holds_any_const_Z"].append(name)
                tile["r1_holds"] = holds
                print("    R1 ratio =", ratio, "  d/dr=0?", sp.simplify(dr) == 0)
        except Exception as e:
            tile["r1_error"] = str(e)
            print("    R1 error:", e)

        # Low-z character from φ ~ -½(A-1) near r=0 if A→1
        # d_L = (1+z)^2 r, 1+z = 1/√A
        # report only: if A=1 - c r^p +..., z ~ (c/2) r^p
        out["tiles"].append(tile)

    # --- Numeric probe grid: free ρ → integrate m, A; characterize edge ---
    print("\n[2] Numeric free-ρ MS probes (characterize edge, no ranking)")
    # A = 1 - 2m/r, m' = 4π r² ρ  (consistent with correct G^t_t)
    def integrate_rho(rho_fn, r_max=2.0, n=400):
        rr = np.linspace(1e-4, r_max, n)
        m = np.zeros_like(rr)
        for i in range(1, len(rr)):
            # trapezoid m'
            r0, r1 = rr[i - 1], rr[i]
            mp0 = 4 * np.pi * r0**2 * rho_fn(r0)
            mp1 = 4 * np.pi * r1**2 * rho_fn(r1)
            m[i] = m[i - 1] + 0.5 * (mp0 + mp1) * (r1 - r0)
        A = 1 - 2 * m / rr
        # first non-positive A
        hit = None
        for i, Ai in enumerate(A):
            if Ai <= 1e-8:
                hit = float(rr[i])
                break
        return {
            "r_edge": hit,
            "m_at_edge": float(m[i]) if hit else float(m[-1]),
            "A_min": float(np.min(A)),
            "A_end": float(A[-1]),
            "m_end": float(m[-1]),
            "compactness_end": float(2 * m[-1] / rr[-1]),
        }

    probes = {
        "const_rho_soft": lambda r: 0.01,
        "const_rho_criticalish": lambda r: 0.08,  # may hit edge
        "rho_1_over_r": lambda r: 0.05 / (r + 1e-12),
        "rho_1_over_r2": lambda r: 0.02 / (r**2 + 1e-8),
        "gauss": lambda r: 0.5 * np.exp(-(r**2) / (0.3**2)),
        "gauss_dense": lambda r: 2.0 * np.exp(-(r**2) / (0.2**2)),
    }
    numeric = {}
    for pname, fn in probes.items():
        rec = integrate_rho(fn)
        numeric[pname] = rec
        edge = rec["r_edge"]
        print(
            f"  {pname}: A_min={rec['A_min']:.4g} edge={edge} "
            f"compact_end={rec['compactness_end']:.4g}"
        )
    out["numeric_rho_probes"] = numeric

    # --- Readout character formulas (no data) ---
    print("\n[3] Readout character (formula only, when A=1-r/X explore tile)")
    # already known: d_L/X = z(z+2), D_M/X = z(z+2)/(1+z)
    # For regular A=1-a2 r²: low-z soft
    a2n = 0.1
    rr = np.linspace(1e-3, 0.5, 50)
    Aq = 1 - a2n * rr**2
    zq = 1 / np.sqrt(np.clip(Aq, 1e-12, None)) - 1
    dL = (1 + zq) ** 2 * rr
    # fit log dL ~ p log z at small z
    mask = (zq > 1e-4) & (zq < 0.05)
    if mask.sum() > 5:
        p = np.polyfit(np.log(zq[mask]), np.log(dL[mask]), 1)[0]
        print(f"  quadratic tile low-z d_L ~ z^{p:.3f}")
        out["quad_lowz_power"] = float(p)
    Al = 1 - rr / 2.0  # X=2 linear, only where positive
    maskL = Al > 0.05
    zl = 1 / np.sqrt(Al[maskL]) - 1
    dLl = (1 + zl) ** 2 * rr[maskL]
    mask2 = (zl > 1e-4) & (zl < 0.05)
    if mask2.sum() > 5:
        pL = np.polyfit(np.log(zl[mask2]), np.log(dLl[mask2]), 1)[0]
        print(f"  linear ceiling tile low-z d_L ~ z^{pL:.3f}")
        out["linear_lowz_power"] = float(pL)

    # BAO character: D_M = (1+z) D_A = (1+z) r  under D_A=r
    # for any profile: D_M(z)/r(z) = 1+z  identity with D_A=r
    # shape is r(z) from A(r)
    print("\n[4] BAO transverse character (identity, no fit)")
    print("  With D_A=r: D_M = r(1+z) = r/√A  for any A(r) tile")
    print("  Ceiling tile only: D_M/X = z(z+2)/(1+z) — one shape, not preferred")
    out["bao_identity"] = "D_M = r/√A when D_A=r; profile-dependent r(z)"

    out["census"] = census
    print("\n[5] Census summary")
    for k, v in census.items():
        print(f"  {k}: {v}")

    out["observing_not_targeting"] = True
    out["no_chi2_selector"] = True
    out["verdict"] = (
        "Correct continuum space: p_r=-ρ always; outer wall ⇔ critical m=X/2; "
        "tiles include vacuum, linear ceiling, regular fills, etc.; "
        "R1 EL does not hold on generic Einstein tiles; "
        "no unique selection claimed; no A(r) shopping."
    )
    print("\n" + out["verdict"])

    path = ROOT / "simple_metric_S5_reopened_space_out.json"
    # make JSON safe
    def sanitize(o):
        if isinstance(o, dict):
            return {str(k): sanitize(v) for k, v in o.items()}
        if isinstance(o, list):
            return [sanitize(v) for v in o]
        if isinstance(o, (bool, int, float, str)) or o is None:
            return o
        return str(o)

    path.write_text(json.dumps(sanitize(out), indent=2))
    print(f"\nWrote {path.name}")
    print("DONE")
    return out


if __name__ == "__main__":
    main()
