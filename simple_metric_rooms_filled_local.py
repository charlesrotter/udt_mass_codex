#!/usr/bin/env python3
"""
Rooms + filled hyp J1 character + local C1 stars under reciprocal metric.
Frame: UDT_NATURE_LEAN_FRAME.md
Re-run: python3 simple_metric_rooms_filled_local.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    print("=" * 70)
    print("Rooms / filled / local — metric-led")
    print("=" * 70)
    out = {}

    # Filled hyp
    x, X, u = sp.symbols("x X u", positive=True)
    A = (X - x) / (X + x)
    m = sp.simplify(x * (1 - A) / 2)
    rho = sp.simplify((1 - A - x * sp.diff(A, x)) / (8 * sp.pi * x**2))
    pt = sp.simplify(
        (x * sp.diff(A, x, 2) + 2 * sp.diff(A, x)) / (16 * sp.pi * x)
    )
    xz = (u**2 - 1) / (u**2 + 1)
    out["filled"] = {
        "M": str(sp.limit(m, x, X)),
        "rho": str(rho),
        "pt_over_rho": str(sp.simplify(pt / rho)),
        "dL_over_X": str(sp.simplify(xz * u**2)),
        "DM_over_X": str(sp.simplify(xz * u)),
    }
    print("[filled] M =", out["filled"]["M"])
    print("  d_L/X =", out["filled"]["dL_over_X"])

    # Local C1 theorem + samples
    r, R, alpha = sp.symbols("r R alpha", positive=True)
    beta = 3 * alpha / (5 * R**2)
    A4 = 1 - alpha * r**2 + beta * r**4
    # ρ∝ 3α - 5β r^2 → 0 at R
    dens = sp.simplify(1 - A4 - r * sp.diff(A4, r))
    print("[local] 1-A-rA' =", dens, "at R:", sp.simplify(dens.subs(r, R)))
    out["local_C1_identity"] = "rho(R)=0 ⇔ C1 match to Schw"
    samples = []
    for a in [0.5, 1.0, 1.5, 2.0]:
        RR = 1.0
        b = 3 * a / (5 * RR**2)
        rr = np.linspace(0, RR, 500)
        AA = 1 - a * rr**2 + b * rr**4
        AR = float(AA[-1])
        samples.append(
            {
                "alpha": a,
                "A_R": AR,
                "rs": RR * (1 - AR),
                "A_min": float(AA.min()),
            }
        )
    out["local_samples"] = samples
    print("[local] samples", samples)

    out["verdict"] = (
        "Two rooms; hyp J1 filled character; local C1 ⇔ ρ_s=0; "
        "quartic family exists; no cross-dress."
    )
    print(out["verdict"])
    (ROOT / "simple_metric_rooms_filled_local_out.json").write_text(
        json.dumps(out, indent=2, default=str)
    )
    print("DONE")


if __name__ == "__main__":
    main()
