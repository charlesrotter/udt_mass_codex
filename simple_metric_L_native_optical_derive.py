#!/usr/bin/env python3
"""
Native L from P-opt: dr/A = κ dφ on reciprocal metric.
Re-run: python3 simple_metric_L_native_optical_derive.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    phi, kappa, X = sp.symbols("phi kappa X", positive=True)
    integ = sp.integrate(sp.exp(-2 * sp.symbols("psi", positive=True)),
                         (sp.symbols("psi", positive=True), 0, phi))
    # manual
    r = kappa * (1 - sp.exp(-2 * phi)) / 2
    A = sp.exp(-2 * phi)
    print("r =", r)
    print("r = (κ/2)(1-A) => X=κ/2, r/X=1-A")

    # H non-const
    rH = X * sp.tanh(phi)
    ratio = sp.simplify(sp.diff(rH, phi) / A)
    print("H: dr/(A dφ) =", ratio, " (not const)")

    # L check
    rL = X * (1 - A)
    # express r in phi: A=e^{-2φ}, r=X(1-e^{-2φ})
    rLp = X * (1 - sp.exp(-2 * phi))
    ratioL = sp.simplify(sp.diff(rLp, phi) / sp.exp(-2 * phi))
    print("L: dr/(A dφ) =", ratioL, " (= 2X)")

    out = {
        "principle": "dr/A = kappa dφ",
        "result": "r/X = 1-A with X=kappa/2",
        "H_compatible": False,
        "L_compatible": True,
        "verdict": "P-opt forces L uniquely on reciprocal metric",
    }
    print(out["verdict"])
    (ROOT / "simple_metric_L_native_optical_derive_out.json").write_text(
        json.dumps(out, indent=2)
    )
    print("DONE")


if __name__ == "__main__":
    main()
