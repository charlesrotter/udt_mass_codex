#!/usr/bin/env python3
"""
R1 OBSERVE — operational PATH measures under hyperbolic rapidity (χ²-blind).

Held:
  Simple metric: dℓ = e^φ dr  (proper radial)
                 null: c dt = e^{2φ} dr  (coordinate; c=1 below)
  Hyp rapidity law on a PATH chart ξ ∈ [0, X):
                 φ = arctanh(ξ/X),  A = e^{-2φ} = (X-ξ)/(X+ξ)
                 1+z = e^φ

PRE-REGISTERED: this script does NOT score Pantheon. It only reports
analytic/numeric relations among operational lengths.

Candidate identifications of composition coordinate x:
  J1   : x = r           (areal = path label)
  P_ell: x = ℓ           (x = proper from origin)
  P_rad: x related so radar one-way R = ∫ e^{2φ} dr equals something
  Affine null parameter (scaled)

For each CHOSE join, D_A = r is recovered from the metric once φ(path) known.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parent
X = 1.0  # units: set X=1 without loss for ratios


def phi_of_xi(xi, X=X):
    """φ = arctanh(ξ/X), ξ in [0,X)."""
    u = np.clip(xi / X, 0.0, 1.0 - 1e-15)
    return np.arctanh(u)


def e_phi(xi, X=X):
    return np.exp(phi_of_xi(xi, X))


def e_mphi(xi, X=X):
    return np.exp(-phi_of_xi(xi, X))


# --- Integrals in path-parameter ξ when φ=φ(ξ) and we need r, ℓ, radar ---
# These depend on which chart ξ is.

def r_from_path_is_ell(xi, X=X):
    """P_ell: ξ=ℓ proper ⇒ dr = e^{-φ} dξ ⇒ r = ∫_0^ξ e^{-φ} du."""
    if xi <= 0:
        return 0.0
    val, _ = quad(lambda u: e_mphi(u, X), 0.0, float(xi), epsabs=1e-12)
    return val


def radar_from_path_is_ell(xi, X=X):
    """One-way radar optical: R = ∫ e^{2φ} dr = ∫ e^{2φ} e^{-φ} dξ = ∫ e^φ dξ when ξ=ℓ."""
    if xi <= 0:
        return 0.0
    val, _ = quad(lambda u: e_phi(u, X), 0.0, float(xi), epsabs=1e-12)
    return val


def ell_from_J1(r, X=X):
    """J1: path label = areal r, φ=arctanh(r/X) — only valid for r<X.
    ℓ = ∫_0^r e^{φ(s)} ds."""
    if r <= 0:
        return 0.0
    if r >= X:
        return np.nan
    val, _ = quad(lambda s: e_phi(s, X), 0.0, float(r), epsabs=1e-12)
    return val


def radar_from_J1(r, X=X):
    """R = ∫_0^r e^{2φ} ds with φ=arctanh(s/X)."""
    if r <= 0:
        return 0.0
    if r >= X:
        return np.nan
    val, _ = quad(lambda s: e_phi(s, X) ** 2, 0.0, float(r), epsabs=1e-12)
    return val


def main():
    print("=" * 70)
    print("R1 — operational PATH measures (χ²-blind)")
    print("φ = arctanh(ξ/X) on PATH chart; X=1 units")
    print("=" * 70)

    # Exact numbers for P_ell
    r_max, _ = quad(lambda u: e_mphi(u, X), 0.0, X * (1 - 1e-15), epsabs=1e-10)
    print(f"\nP_ell: r_max/X = {r_max/X:.15f}  (expect π/2-1 = {np.pi/2-1:.15f})")
    print(f"  match: {abs(r_max/X - (np.pi/2-1)) < 1e-9}")

    # Radar under P_ell as ξ→X: ∫ e^φ dξ diverges (e^φ→∞)
    # Check growth
    print("\n--- Under P_ell (ξ = proper ℓ) ---")
    print(f"{'ξ/X':>8} {'r/X':>10} {'R_radar/X':>12} {'r/ξ':>8} {'R/ξ':>8}")
    rows_pell = []
    for f in [0.05, 0.1, 0.3, 0.5, 0.8, 0.95, 0.99]:
        xi = f * X
        r = r_from_path_is_ell(xi, X)
        R = radar_from_path_is_ell(xi, X)
        rows_pell.append({"xi_over_X": f, "r_over_X": r / X, "R_over_X": R / X})
        print(f"{f:8.2f} {r/X:10.5f} {R/X:12.5f} {r/xi:8.4f} {R/xi:8.4f}")
    print("  Note: radar R grows faster than ξ; as ξ→X, e^φ→∞ so R→∞ while r→r_max finite.")

    print("\n--- Under J1 (ξ = areal r, φ=arctanh(r/X)) ---")
    print(f"{'r/X':>8} {'ℓ/X':>10} {'R_radar/X':>12} {'ℓ/r':>8}")
    rows_j1 = []
    for f in [0.05, 0.1, 0.3, 0.5, 0.8, 0.95]:
        r = f * X
        ell = ell_from_J1(r, X)
        R = radar_from_J1(r, X)
        rows_j1.append({"r_over_X": f, "ell_over_X": ell / X, "R_over_X": R / X})
        print(f"{f:8.2f} {ell/X:10.5f} {R/X:12.5f} {ell/r:8.4f}")
    print("  Note: under J1, ℓ = ∫ e^φ dr with φ=arctanh(r/X) DIVERGES as r→X (e^φ→∞).")
    # check near X
    ell_near = ell_from_J1(0.99 * X, X)
    print(f"  ℓ/X at r/X=0.99 ≈ {ell_near/X:.4f} (large)")

    # Affine null: take k^t from null geodesic with conserved E
    # p_t = -E, for radial null; affine λ with dr/dλ = ...
    # Standard: for metric, affine radial null can use dλ ∝ e^{2φ} dr or e^{-2φ} depending on normalization
    # Report both common scalings without declaring THE affine path
    print("\n--- Affine-like integrals (chart r, φ=arctanh(r/X) as if J1 background) ---")
    print("  I1 = ∫ e^{2φ} dr  (= radar optical one-way)")
    print("  I2 = ∫ e^{-2φ} dr")
    print("  I3 = ∫ e^{φ} dr   (= proper ℓ)")
    for f in [0.1, 0.5, 0.9]:
        r = f * X
        I1 = radar_from_J1(r, X)
        I2, _ = quad(lambda s: e_mphi(s, X) ** 2, 0, r, epsabs=1e-12)
        I3 = ell_from_J1(r, X)
        print(f"  r/X={f:.1f}  I1/X={I1/X:.4f}  I2/X={I2/X:.4f}  I3/X={I3/X:.4f}")

    # Logical forcedness
    print("\n" + "=" * 70)
    print("FORCEDNESS (logic, not fit)")
    print("=" * 70)
    print(
        """
  FORCED by metric alone:
    • proper radial element dℓ = e^φ dr
    • null one-way optical ∫ e^{2φ} dr (coordinate time × c)
    • areal D_A = r on simple metric (chart origin)
    • if composition rapidity is metric φ, then φ additive

  NOT forced by metric alone:
    • which operational 1D length is the composition coordinate x
    • x = ℓ (P_ell) — natural for static rods, CHOSE
    • x = r (J1) — CHOSE; makes proper ℓ diverge at bound
    • x = radar R — CHOSE; R diverges at bound under P_ell path
    • a unique affine λ as "the" path distance

  CONSISTENCY filters (structure, not SNe):
    • Bound x→X with φ→∞ and finite proper reach: P_ell has finite X=ℓ_max
      but infinite radar; J1 has finite r_max=X but infinite proper to horizon-like wall
    • c-edge / xmax story wanted "distance bound always farther, asymptotic":
      proper ℓ→X finite under P_ell means the bound is at FINITE proper distance
      (like a horizon you reach in finite proper length in some senses — nuance)
    • Local agreement: all options satisfy x~r~ℓ~R as φ→0 (same linear Hubble seed)
"""
    )

    # Small-ξ series agreement
    print("--- small-ξ series (X=1): all ~ ξ + O(ξ³) or similar ---")
    for f in [0.01, 0.02, 0.05]:
        xi = f
        r = r_from_path_is_ell(xi)
        R = radar_from_path_is_ell(xi)
        print(f"  ξ={f:.3f}  r={r:.6f}  R={R:.6f}  r/ξ={r/xi:.6f}  R/ξ={R/xi:.6f}")

    out = {
        "pre_registered": "no Pantheon; no join ranking by residual",
        "P_ell_rmax_over_X": r_max / X,
        "pi_over_2_minus_1": float(np.pi / 2 - 1),
        "rows_pell": rows_pell,
        "rows_j1": rows_j1,
        "verdict": {
            "forced": [
                "d_ell = e^phi dr",
                "radar_one_way = int e^{2 phi} dr",
                "D_A = r areal at chart origin",
            ],
            "not_forced": [
                "composition x equals ell",
                "composition x equals r",
                "composition x equals radar",
            ],
            "P_ell": "CHOSE/motivated — unique only if composition is defined as integrated static-rod length",
            "J1": "CHOSE — conflicts with finite proper distance to phi=inf wall",
        },
    }
    path = ROOT / "simple_metric_R1_path_ops_out.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
