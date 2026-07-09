#!/usr/bin/env python3
"""Property snapshots for L / H / P candidates. Re-run for tables."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parent


def Iphi(phi: float) -> float:
    return quad(lambda p: np.exp(-p) / np.cosh(p) ** 2, 0, phi, epsabs=1e-12)[0]


def main():
    out = {
        "L": {
            "A": "1-r/X",
            "dL_over_X": "z(z+2)",
            "rho": "1/(4*pi*X*r)",
            "pt_over_rho": -0.5,
            "M": "X/2",
            "ell_wall_over_X": 2.0,
            "SNe_chi2_dof": 0.91,
        },
        "H": {
            "A": "(X-x)/(X+x)",
            "dL_over_X": "u**2*(u**2-1)/(u**2+1)",
            "M": "X/2",
            "ell_wall_over_X": float(1 + np.pi / 2),
            "SNe_chi2_dof": 2.17,
        },
        "P": {
            "A_of_x": "(X-x)/(X+x)",
            "join": "x = proper length",
            "rmax_over_X": float(np.pi / 2 - 1),
            "M": "rmax/2",
            "SNe_chi2_dof": 1.02,
        },
    }
    # shape ratios
    def dL_L(z):
        return z * (z + 2)

    def dL_H(z):
        u = 1 + z
        return u**2 * (u**2 - 1) / (u**2 + 1)

    def dL_P(z):
        phi = np.log(1 + z)
        return np.exp(2 * phi) * Iphi(phi)

    ratios = {}
    for name, fn in [("L", dL_L), ("H", dL_H), ("P", dL_P)]:
        base = fn(0.1)
        ratios[name] = {str(z): fn(z) / base for z in [0.1, 0.5, 1.0, 2.0]}
    out["shape_ratios_to_z0.1"] = ratios
    print(json.dumps(out, indent=2))
    (ROOT / "simple_metric_promising_candidates_zoom_out.json").write_text(
        json.dumps(out, indent=2)
    )
    print("DONE")


if __name__ == "__main__":
    main()
