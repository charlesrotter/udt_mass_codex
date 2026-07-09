#!/usr/bin/env python3
"""
J1 honesty under nature lean: forced vs CHOSE joins.
Re-run: python3 simple_metric_J1_honesty_skeleton.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parent


def main():
    X = sp.symbols("X", positive=True)
    out = {"forced": [], "joins": {}}

    print("=" * 70)
    print("J1 honesty — skeleton joins")
    print("=" * 70)

    out["forced"] = [
        "A=e^{-2φ}, D_A=r, dℓ=e^φ dr",
        "1+z=e^Δφ; d_L=(1+z)^2 r",
        "composition x=X tanh φ if finite bound postulate",
        "MS: A=0 ⇒ m=r_wall/2",
        "p_r=-ρ on reciprocal Einstein continuum",
    ]
    print("[forced]")
    for line in out["forced"]:
        print(" ", line)

    # P_ell r_max/X
    I = quad(lambda ph: np.exp(-ph) / np.cosh(ph) ** 2, 0, 40)[0]
    print("\n[P_ell] r_max/X =", I, " = π/2-1?", abs(I - (np.pi / 2 - 1)) < 1e-9)
    out["joins"]["P_ell"] = {
        "r_max_over_X": float(I),
        "M_over_X": float(I / 2),
        "tag": "CHOSE explore",
    }

    out["joins"]["J1"] = {
        "r_max_over_X": 1.0,
        "M_over_X": 0.5,
        "tag": "CHOSE working (Charles sphere-size)",
        "dL_form": "(1+z)^2 * ((1+z)^2-1)/((1+z)^2+1) * X",
    }

    out["joins"]["free_r_of_x"] = {
        "M_wall": "r(X)/2",
        "tag": "free-and-explored class",
    }

    out["verdict"] = (
        "J1 not forced; working lean default; "
        "join-free skeleton keeps reach + M=r_wall/2 + areal light."
    )
    print("\n" + out["verdict"])
    path = ROOT / "simple_metric_J1_honesty_skeleton_out.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {path.name}")
    print("DONE")


if __name__ == "__main__":
    main()
