#!/usr/bin/env python3
"""Exact finite-dimensional checks for the G81 basis-covariance statement."""

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    n = sp.Matrix([12, 3, 4]) / 13
    s1 = sp.Matrix([0, 4, -3]) / 5
    s2 = sp.Matrix([-25, 36, 48]) / 65
    A = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)], [sp.Rational(4, 5), sp.Rational(3, 5)]])
    B = sp.Matrix([[sp.Rational(5, 13), -sp.Rational(12, 13)], [sp.Rational(12, 13), sp.Rational(5, 13)]])
    assert n.dot(n) == s1.dot(s1) == s2.dot(s2) == 1
    assert n.dot(s1) == n.dot(s2) == s1.dot(s2) == 0
    assert s1.cross(s2) == n
    assert A.T * A == B.T * B == sp.eye(2)
    assert A.det() == B.det() == 1
    z = sp.symbols("z", positive=True)
    d11, d12, d21, d22 = sp.symbols("d11 d12 d21 d22", real=True)
    D = sp.Matrix([[d11, d12], [d21, d22]])
    reverse = z * D.T
    rotated = B * reverse * A.T
    prediction = z * B * D.T * A.T
    assert rotated == prediction
    assert sp.factor(rotated.det() - z**2 * D.det()) == 0
    output = {
        "schema": "udt-cmb-g81-exact-algebra-v1",
        "status": "PASS",
        "c1_oriented_orthonormal_triad": True,
        "A_and_B_SO2": True,
        "rotated_covariance_identity": True,
        "area_determinant_identity": True,
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "EXACT_ALGEBRA_RESULT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
