#!/usr/bin/env python3
"""Exact endpoint and determinant algebra for G80 reciprocity."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    Z = sp.sqrt(21) / 4
    assert sp.simplify(Z * (4 / sp.sqrt(21))) == 1
    assert sp.simplify(sp.log(Z) + sp.log(1 / Z)) == 0
    a, b, c, d = sp.symbols("a b c d", real=True)
    D = sp.Matrix([[a, b], [c, d]])
    D_reverse = Z * D.T
    assert sp.simplify(D_reverse.det() - Z**2 * D.det()) == 0
    # For positive Z and positive oriented area, sqrt(det) scales by Z.
    assert bool(Z.is_positive)
    print("PASS: exact inverse-depth and 2x2 Jacobi determinant scaling identities")


if __name__ == "__main__":
    main()
