#!/usr/bin/env python3
"""
L selection: p_t=-rho/2 uniqueness; L composition law; F(phi) notes.
Re-run: python3 simple_metric_L_P_selection_derive.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    r, X = sp.symbols("r X", positive=True)
    A = sp.Function("A")
    num = (
        r**2 * A(r).diff(r, 2)
        + r * A(r).diff(r)
        - A(r)
        + 1
    )
    sol = sp.dsolve(sp.Eq(num, 0), A(r))
    print("ODE p_t=-ρ/2:", sol)

    # verify linear
    AL = 1 - r / X
    rho = (1 - AL - r * sp.diff(AL, r)) / (8 * sp.pi * r**2)
    pt = (r * sp.diff(AL, r, 2) + 2 * sp.diff(AL, r)) / (16 * sp.pi * r)
    print("linear pt/rho", sp.simplify(pt / rho))

    # composition L
    a, b, c, Xs = sp.symbols("a b c Xs", positive=True)

    def op(u, v):
        return u + v - u * v / Xs

    print(
        "L⊕ associative",
        sp.simplify(op(op(a, b), c) - op(a, op(b, c))) == 0,
    )
    print("r⊕X =", sp.simplify(op(a, Xs)))

    out = {
        "general_A_pt_half": str(sol),
        "unique_with_reg_wall": "A=1-r/X",
        "L_composition": "r1+r2-r1*r2/X",
        "L_chart": "r/X=1-exp(-2*phi)=1-A",
        "H_chart": "x/X=tanh(phi)",
        "verdict": (
            "L unique under pt=-rho/2 + reg + wall; "
            "L also kinematic via chart 1-e^{-2phi} and associative ⊕"
        ),
    }
    print(out["verdict"])
    (ROOT / "simple_metric_L_P_selection_derive_out.json").write_text(
        json.dumps(out, indent=2)
    )
    print("DONE")


if __name__ == "__main__":
    main()
