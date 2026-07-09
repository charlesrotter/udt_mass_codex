#!/usr/bin/env python3
"""
Skeleton: hyperbolic reach + MS critical closure under J1.
Frame: UDT_NATURE_LEAN_FRAME.md

Re-run: python3 simple_metric_skeleton_reach_closure.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parent


def main():
    x, X = sp.symbols("x X", positive=True)
    out = {}

    print("=" * 70)
    print("Skeleton reach + critical closure (J1 hyperbolic)")
    print("=" * 70)

    A_h = (X - x) / (X + x)
    m_h = sp.simplify(x * (1 - A_h) / 2)
    rho_h = sp.simplify(
        (1 - A_h - x * sp.diff(A_h, x)) / (8 * sp.pi * x**2)
    )
    pt_h = sp.simplify(
        (x * sp.diff(A_h, x, 2) + 2 * sp.diff(A_h, x)) / (16 * sp.pi * x)
    )

    print("m =", m_h, "→", sp.limit(m_h, x, X))
    print("ρ =", rho_h)
    print("p_t/ρ =", sp.simplify(pt_h / rho_h))
    out["m"] = str(m_h)
    out["M_crit"] = "X/2"
    out["rho"] = str(rho_h)
    out["pt_over_rho"] = str(sp.simplify(pt_h / rho_h))

    # d_L
    u = sp.symbols("u", positive=True)
    xz = (u**2 - 1) / (u**2 + 1)
    dL_over_X = sp.simplify(xz * u**2)
    print("d_L/X =", dL_over_X)
    out["dL_over_X"] = str(dL_over_X)

    # proper distance numeric
    def ell_num(xv, Xv=1.0):
        return quad(
            lambda s: np.sqrt((Xv + s) / (Xv - s)), 0, xv, epsabs=1e-14
        )[0]

    ells = {str(a): ell_num(a) for a in [0.5, 0.9, 0.99, 0.999, 0.9999]}
    print("ell(x) for X=1:", ells)
    print("analytic limit X(1+π/2) =", 1 + 0.5 * np.pi)
    out["ell_samples_X1"] = ells
    out["ell_wall"] = "X(1+pi/2) finite"
    out["unattainable"] = "compositional (x never = X), not infinite proper distance"

    # linear contrast
    r = sp.symbols("r", positive=True)
    A_l = 1 - r / X
    m_l = sp.simplify(r * (1 - A_l) / 2)
    out["linear_M"] = str(sp.limit(m_l, r, X))
    print("linear ceiling also M→X/2")

    out["verdict"] = (
        "J1 hyperbolic reach = critical fill M=X/2; "
        "proper distance to wall finite; compositional unattainability."
    )
    print("\n" + out["verdict"])
    path = ROOT / "simple_metric_skeleton_reach_closure_out.json"
    path.write_text(json.dumps(out, indent=2, default=str))
    print(f"Wrote {path.name}")
    print("DONE")


if __name__ == "__main__":
    main()
