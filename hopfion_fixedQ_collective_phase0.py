#!/usr/bin/env python3
"""Phase 0 DEMO: fixed-Q collective scale energy E_Q(R) from H3-banked virial ratio.

NOT a PDE solve. Moments I2,I4 are order-1 CHOSE-normalized (see ledger) so only
ratios R_Q(Q)/R_0 and signs of curvature are claimed. Bank E2/E4 from H3.

Usage: python3 hopfion_fixedQ_collective_phase0.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

# --- H3 banked (node_H3_hopfion_solve_results.md) ---
E2_OVER_E4 = 0.9995  # ~virial; continuum Derrick wants 1
# Gauge ξ=κ=1 free data-blind; set E4=1, E2=ratio
E4 = 1.0
E2 = E2_OVER_E4 * E4

# Collective inertia moments: dimensionless CHOSE normalization (Phase 0).
# True I2,I4 need profile integrals on n_0; for DEMO set I4=1, I2=1 so
# charge term competes at O(1) with E2,E4 near R~1.
I2 = 1.0  # CHOSE-norm
I4 = 1.0  # CHOSE-norm


def E_Q(R: np.ndarray, Q: float) -> np.ndarray:
    R = np.asarray(R, dtype=float)
    pot = E2 * R + E4 / R
    inert = I2 * R**3 + I4 * R
    return pot + (Q**2) / (2.0 * inert)


def scan_Q(Q: float, rmin=0.2, rmax=8.0, n=4000):
    R = np.linspace(rmin, rmax, n)
    E = E_Q(R, Q)
    i = int(np.argmin(E))
    # numerical second derivative at min
    h = R[1] - R[0]
    if 0 < i < n - 1:
        curv = (E[i + 1] - 2 * E[i] + E[i - 1]) / h**2
    else:
        curv = float("nan")
    return {
        "Q": Q,
        "R_Q": float(R[i]),
        "E_min": float(E[i]),
        "E_pp": float(curv),
        "stable": bool(curv > 0),
    }


def main():
    qs = [0.0, 0.5, 1.0, 2.0, 5.0]
    rows = [scan_Q(q) for q in qs]
    # P0-T3: Q->0 should approach R* = sqrt(E4/E2) for pure pot
    R_star = float(np.sqrt(E4 / E2))
    out = {
        "grade": "DEMO",
        "E2": E2,
        "E4": E4,
        "E2_over_E4": E2_OVER_E4,
        "I2_norm": I2,
        "I4_norm": I4,
        "I_note": "CHOSE order-1 normalization; absolute R_Q not physical until I from H3 profile",
        "R_star_Derrick": R_star,
        "rows": rows,
        "P0_T1_finite_min_Qgt0": all(r["R_Q"] > 0.25 and r["R_Q"] < 7.5 for r in rows if r["Q"] > 0),
        "P0_T2_stable": all(r["stable"] for r in rows),
        "P0_T3_Q0_near_Derrick": abs(rows[0]["R_Q"] - R_star) / R_star < 0.02,
    }
    path = Path("hopfion_fixedQ_collective_phase0_out.json")
    path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    print("wrote", path)


if __name__ == "__main__":
    main()
