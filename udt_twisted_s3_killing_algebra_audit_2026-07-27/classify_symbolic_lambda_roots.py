#!/usr/bin/env python3
"""Classify real roots of the exact symbolic-lambda rank determinant."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    source = json.loads((HERE / "SYMBOLIC_LAMBDA_RESULT.json").read_text(encoding="utf-8"))
    symbol = sp.symbols("L", real=True)
    determinant = sp.sympify(source["invariant_gradient_determinant"].replace("lambda", "L"), locals={"L": symbol})
    numerator, denominator = sp.fraction(sp.together(determinant))
    polynomial = sp.Poly(numerator, symbol)
    roots = sp.nroots(polynomial, maxsteps=200)
    real_roots = [float(sp.re(root)) for root in roots if abs(float(sp.im(root))) < 1e-10]
    result = {
        "schema": "udt.twisted_s3_killing_algebra.symbolic_lambda_roots.v1",
        "polynomial_degree": polynomial.degree(),
        "denominator": str(denominator),
        "real_root_count": len(real_roots),
        "real_root_approximations": real_roots,
        "semantics": "certificate_inconclusive_at_roots_not_extra_symmetry",
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "SYMBOLIC_LAMBDA_ROOTS.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    assert polynomial.degree() == 9
    assert len(real_roots) == 7


if __name__ == "__main__":
    main()
