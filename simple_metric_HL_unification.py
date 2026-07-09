#!/usr/bin/env python3
"""H/L unification: multiplicative A; chart embeddings."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    phi = sp.symbols("phi", positive=True)
    A = sp.exp(-2 * phi)
    lhs = sp.simplify(sp.tanh(phi))
    rhs = sp.simplify((1 - A) / (1 + A))
    print("tanh φ =", lhs)
    print("(1-A)/(1+A) =", rhs)
    print("equal", sp.simplify(lhs - rhs) == 0)

    out = {
        "spine": [
            "A=e^{-2φ}",
            "φ additive",
            "A multiplies under composition",
            "wall A→0",
        ],
        "H_embedding": "r/X=tanh φ=(1-A)/(1+A)",
        "L_embedding": "r/X=1-A",
        "L_composition": "r1+r2-r1*r2/X",
        "H_composition": "(r1+r2)/(1+r1*r2/X**2)",
        "pt_half": "equivalent to L embedding + Einstein",
        "verdict": "Same spine; fork is f(A) embedding into areal radius",
    }
    print(out["verdict"])
    (ROOT / "simple_metric_HL_unification_out.json").write_text(
        json.dumps(out, indent=2)
    )
    print("DONE")


if __name__ == "__main__":
    main()
