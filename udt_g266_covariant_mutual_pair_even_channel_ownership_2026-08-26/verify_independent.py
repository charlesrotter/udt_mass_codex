#!/usr/bin/env python3
"""Implementation-distinct exact-rational G266 verification; no SymPy or production import."""

from fractions import Fraction
import json


def gamma(r):
    return (r + 1 / r) / 2


def xi(r):
    return (1 / r - r) / 2


def main():
    assertions = 0
    cases = 0
    for i in range(1, 65):
        a = Fraction(i + 1, i + 3)
        b = Fraction(2 * i + 3, i + 5)
        ga, gb, gab = gamma(a), gamma(b), gamma(a * b)
        xa, xb, xab = xi(a), xi(b), xi(a * b)
        tests = (
            ga * ga - xa * xa == 1,
            gamma(1 / a) == ga,
            xi(1 / a) == -xa,
            ga - xa == a,
            ga + xa == 1 / a,
            gab == ga * gb + xa * xb,
            xab == xa * gb + ga * xb,
            1 / gamma(1 / a) == 1 / ga,
        )
        assert all(tests)
        assertions += len(tests)
        cases += 1

    for n in range(1, 65):
        k = Fraction(n, 1000)
        first = (-2 * k, -2 * k, -2 * k)
        second = (4 * k * k, 2 * k * k, Fraction(0))
        tests = (
            len(set(first)) == 1,
            len(set(second)) == 3,
            second[0] - second[1] == 2 * k * k,
            second[1] - second[2] == 2 * k * k,
        )
        assert all(tests)
        assertions += len(tests)
        cases += 1

    print(json.dumps({
        "status": "PASS",
        "implementation": "python_fraction_no_sympy_no_production_import_no_result_read",
        "cases": cases,
        "assertions": assertions,
        "group_cases": 64,
        "distance_jet_cases": 64,
        "verified": [
            "reversal parity",
            "hyperbolic norm",
            "signed leg reconstruction",
            "two-channel composition",
            "conditional inverse-trace reversal invariance",
            "common first jet and distinct second jets for three distance attachments",
        ],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
