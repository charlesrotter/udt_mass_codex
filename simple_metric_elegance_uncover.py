#!/usr/bin/env python3
"""
UDT elegance uncover: kinematic reach → A → Einstein continuum → light.
Re-run: python3 simple_metric_elegance_uncover.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    x, X, u, z = sp.symbols("x X u z", positive=True)
    A = (X - x) / (X + x)
    rho = sp.simplify((1 - A - x * sp.diff(A, x)) / (8 * sp.pi * x**2))
    pt = sp.simplify(
        (x * sp.diff(A, x, 2) + 2 * sp.diff(A, x)) / (16 * sp.pi * x)
    )
    m = sp.simplify(x * (1 - A) / 2)
    xX = (u**2 - 1) / (u**2 + 1)
    dL_X = sp.simplify(xX * u**2)
    ser = sp.series(dL_X.subs(u, 1 + z), z, 0, 4).removeO()

    out = {
        "rho": str(rho),
        "pt": str(pt),
        "pt_over_rho": str(sp.simplify(pt / rho)),
        "M": str(sp.limit(m, x, X)),
        "dL_over_X": str(dL_X),
        "dL_series": str(ser),
        "free": ["X", "observer_zero"],
        "fixed_by_kinematics": ["A(x)", "rho", "p_r", "p_t", "d_L(z)", "relational"],
        "verdict": (
            "Kinematics fix A; Einstein reads continuum; light fixed; "
            "one scale X; no EOS menu."
        ),
    }
    print("ρ =", out["rho"])
    print("p_t =", out["pt"])
    print("M =", out["M"])
    print("d_L/X =", out["dL_over_X"])
    print("series", out["dL_series"])
    print(out["verdict"])
    (ROOT / "simple_metric_elegance_uncover_out.json").write_text(
        json.dumps(out, indent=2)
    )
    print("DONE")


if __name__ == "__main__":
    main()
