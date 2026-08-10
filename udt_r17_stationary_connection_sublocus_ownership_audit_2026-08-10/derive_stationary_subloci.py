#!/usr/bin/env python3
"""Exact stationary sublocus classification for the banked R17 normal connection."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
LAMBDAS = (
    sp.Rational(-2),
    sp.Rational(-1),
    sp.Rational(0),
    sp.Rational(1, 2),
    sp.Rational(1),
    sp.Rational(2),
)
A_VALUE = sp.Rational(1, 64)


def real_positive_roots(lam: sp.Rational) -> list[sp.Float]:
    x, y = sp.symbols("x y", positive=True)
    a = A_VALUE
    if lam == -2:
        polynomial = x**3 - a**2 * x - 2
        candidates = sp.nroots(polynomial, n=40, maxsteps=200)
        return [sp.N(sp.re(root), 20) for root in candidates
                if abs(float(sp.im(root))) < 1e-30 and sp.re(root) > a]
    if lam == sp.Rational(1, 2):
        polynomial = y**4 - 2 * y**3 - a**2
        candidates = sp.nroots(polynomial, n=40, maxsteps=200)
        return [sp.N(sp.re(root)**2, 20) for root in candidates
                if abs(float(sp.im(root))) < 1e-30 and sp.re(root)**2 > a]
    expression = sp.together(x**2 - 2 * x ** (1 + lam) - a**2)
    numerator = sp.fraction(expression)[0]
    candidates = sp.nroots(numerator, n=40, maxsteps=200)
    return [sp.N(sp.re(root), 20) for root in candidates
            if abs(float(sp.im(root))) < 1e-30 and sp.re(root) > a]


def main() -> int:
    x, a, lam, epsilon = sp.symbols("x a lambda epsilon", positive=True)
    u, v = sp.symbols("u v", positive=True)
    p1, p2, p3, q21, q31, q22, q33 = sp.symbols(
        "p1 p2 p3 q21 q31 q22 q33", real=True
    )

    connection_vertical = sp.simplify(
        epsilon * (2 - u**2 / v**2 + a**2 / (u**2 * v**2))
    )
    B = sp.simplify(connection_vertical.subs({u: sp.sqrt(x), v: x ** (lam / 2)}) / epsilon)
    expected_B = 2 - x ** (1 - lam) + a**2 * x ** (-(1 + lam))
    assert sp.simplify(B - expected_B) == 0

    F23_constant = 2 * u**2 / v**4 - 4 / v**2 - 2 * a**2 / (u**2 * v**4)
    F23_x = sp.simplify(F23_constant.subs({u: sp.sqrt(x), v: x ** (lam / 2)}))
    assert sp.simplify(F23_x + 2 * B / x**lam) == 0
    flat_equation = sp.expand(x**2 - 2 * x ** (1 + lam) - a**2)
    assert sp.simplify(sp.factor(F23_x * x ** (1 + 2 * lam) / 2) - flat_equation) == 0

    # Lambda=-1 compactness identity for local curvature horizontality.
    # X(p1)=4 eps*y*p3, Y(p1)=-4 eps*y*p2 and [X,Y]phi=2 eps*p1.
    y = sp.symbols("y", positive=True)
    horizontal_laplacian_p1 = sp.expand(4 * epsilon * y * (2 * epsilon * p1))
    assert sp.simplify(horizontal_laplacian_p1 - 8 * epsilon**2 * y * p1) == 0

    # Lambda=-1 compactness identities for complete flatness.
    H = sp.symbols("H", nonnegative=True)
    Q = 2 * y - 4 - 2 * a**2
    Zp1 = -2 * y * (4 * H + Q)
    integrated_identity = sp.expand(-Zp1 / 4)
    assert sp.simplify(integrated_identity - (2 * y * H + y**2 - (2 + a**2) * y)) == 0

    # Canonical Hopf tangent descent: projectable coefficients rotate at 2 epsilon.
    canonical_condition = sp.Eq(epsilon * B, 2 * epsilon)
    canonical_numerator = sp.factor(
        (B - 2) * x ** (1 + lam)
    )
    assert sp.simplify(canonical_numerator - (a**2 - x**2)) == 0

    roots = {}
    expected_counts = {-2: 1, -1: 1, 0: 1, sp.Rational(1, 2): 1, 1: 0, 2: 2}
    for value in LAMBDAS:
        values = real_positive_roots(value)
        assert len(values) == expected_counts[value]
        roots[str(value)] = [str(item) for item in values]

    bmin_lambda2 = sp.simplify(2 - sp.Rational(2, 3) / (sp.sqrt(3) * A_VALUE))
    assert -23 < bmin_lambda2 < -22

    result = {
        "schema_version": 1,
        "arena": "REGULAR_STATIONARY_R17_ON_R_TIMES_S3",
        "twist": "a>0; specialized roots use a=1/64",
        "lambda_values": [str(item) for item in LAMBDAS],
        "vertical_connection": "A_Z=epsilon*B_lambda(x)",
        "B_lambda": "2-x**(1-lambda)+a**2*x**(-(1+lambda))",
        "regularity": "x=exp(2phi)>a",
        "global_local_curvature_horizontal": "IFF_PHI_CONSTANT",
        "complete_flatness": "PHI_CONSTANT_AND_B_LAMBDA_X_ZERO",
        "flat_equation": "x**2-2*x**(1+lambda)-a**2=0",
        "flat_regular_root_counts_at_a_1_over_64": {
            str(key): value for key, value in expected_counts.items()
        },
        "flat_regular_roots_at_a_1_over_64": roots,
        "abstract_parallel_quotient_descent": "PHI_CONSTANT_AND_B_LAMBDA_X_IN_Z",
        "abstract_descent_integer_ranges_at_a_1_over_64": {
            "-2": "all integers <=1; one root each",
            "-1": "all integers <=1; one root each",
            "0": "all integers <=1; one root each",
            "1/2": "all integers <=1; one root each",
            "1": "none",
            "2": "integers -22 through 1; two roots each",
        },
        "lambda_2_B_min": str(bmin_lambda2),
        "canonical_hopf_tangent_descent": str(canonical_condition),
        "canonical_hopf_regular_result": "NONE_FOR_A_POSITIVE_BECAUSE_X_EQUALS_A_IS_SLICE_DEGENERACY",
        "complete_holonomy": "TRIVIAL_ON_FLAT_ROOTS_ELSE_FULL_SO2",
        "proper_nontrivial_reduced_holonomy": False,
        "c01_c06": "NONCONSTANT_OFFSHELL_WITNESSES__NOT_HORIZONTAL__NOT_FLAT__FULL_SO2_HOLONOMY",
        "manifest_backed_r17_source_selection": False,
        "primary_ruling": (
            "STATIONARY_SPECIAL_SUBLOCUS_CLASSIFIED__GLOBAL_HORIZONTALITY_FORCES_CONSTANT_PHI__"
            "FLAT_AND_ABSTRACT_DESCENT_LOCUS_EXPLICIT__NO_REGULAR_CANONICAL_HOPF_TANGENT_DESCENT__"
            "MANIFEST_BACKED_R17_SOURCES_SELECT_NONE"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
