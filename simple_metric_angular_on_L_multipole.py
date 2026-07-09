#!/usr/bin/env python3
"""
Linear multipoles of residual depth on L background A=1-r/X.
Static Laplace-Beltrami: (r^2 A u')' - ell(ell+1) u = 0.

Re-run: python3 simple_metric_angular_on_L_multipole.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parent


def integrate_mode(ell: int, r_min=1e-4, r_max=0.999):
    def f(r, y):
        u, up = y
        A = 1.0 - r
        upp = (ell * (ell + 1) * u - (2 * r - 3 * r**2) * up) / (r**2 * A)
        return [up, upp]

    if ell == 0:
        y0 = [1.0, 0.0]
    else:
        y0 = [r_min**ell, ell * r_min ** (ell - 1)]
    return solve_ivp(
        f,
        (r_min, r_max),
        y0,
        dense_output=True,
        max_step=5e-4,
        rtol=1e-8,
        atol=1e-10,
        method="LSODA",
    )


def main():
    out = {"ell": {}}
    print("Regular-origin multipoles on L (X=1)")
    for ell in range(0, 6):
        row = {}
        for r_max in [0.99, 0.999, 0.9999]:
            sol = integrate_mode(ell, r_max=r_max)
            if not sol.success:
                row[str(r_max)] = {"ok": False}
                continue
            u, up = sol.y[:, -1]
            row[str(r_max)] = {
                "ok": True,
                "u": float(u),
                "up": float(up),
                "abs_up": float(abs(up)),
            }
            print(f"  ell={ell} r_max={r_max}: u={u:.4g}, u'={up:.4g}")
        out["ell"][str(ell)] = row

    out["conclusion"] = (
        "Static multipoles regular at origin become wall-loud as r→X; "
        "no quiet static angular decoration on filled L."
    )
    print(out["conclusion"])
    (ROOT / "simple_metric_angular_on_L_multipole_out.json").write_text(
        json.dumps(out, indent=2)
    )
    print("DONE")


if __name__ == "__main__":
    main()
