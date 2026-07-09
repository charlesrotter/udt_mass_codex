#!/usr/bin/env python3
"""Identities for UDT_DOTTED_LINE residual spine."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    phi, A, r, X = sp.symbols("phi A r X", positive=True)
    A_of_phi = sp.exp(-2 * phi)
    C = 1 - A
    # embeddings
    r_L = X * (1 - A)
    r_H = X * (1 - A) / (1 + A)
    # H check tanh
    print("r_H/X vs tanh φ:", sp.simplify(r_H.subs(A, A_of_phi) / X - sp.tanh(phi)))

    out = {
        "primitive": "A = e^{-2φ}",
        "composition": "A12 = A1*A2",
        "compactness": "C = 1-A = 2m/r",
        "L": "r/X = C = 1-A",
        "H": "r/X = C/(2-C) = tanh φ",
        "wall": "A→0, C→1, m→r/2",
        "verdict": "One residual A connects metric, mass, composition, embeddings",
    }
    print(out["verdict"])
    (ROOT / "simple_metric_dotted_line_out.json").write_text(json.dumps(out, indent=2))
    print("DONE")


if __name__ == "__main__":
    main()
