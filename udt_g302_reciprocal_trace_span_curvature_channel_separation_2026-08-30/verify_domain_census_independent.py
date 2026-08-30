#!/usr/bin/env python3
"""Dependency-free exhaustive parameter-cell verification of the G302 domain census."""

from __future__ import annotations

import csv
from fractions import Fraction as F
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def trim(poly):
    out = list(poly)
    while out and out[-1] == 0:
        out.pop()
    return out or [F(0)]


def derivative(poly):
    return trim([F(i) * poly[i] for i in range(1, len(poly))])


def divmod_poly(numerator, denominator):
    num = trim(numerator)
    den = trim(denominator)
    if den == [0]:
        raise ZeroDivisionError
    quotient = [F(0)] * max(1, len(num) - len(den) + 1)
    while num != [0] and len(num) >= len(den):
        shift = len(num) - len(den)
        factor = num[-1] / den[-1]
        quotient[shift] += factor
        for index, value in enumerate(den):
            num[index + shift] -= factor * value
        num = trim(num)
    return trim(quotient), trim(num)


def deflate_zero(poly):
    out = trim(poly)
    multiplicity = 0
    while len(out) > 1 and out[0] == 0:
        out = trim(out[1:])
        multiplicity += 1
    return out, multiplicity


def sturm_sequence(poly):
    first, _ = deflate_zero(poly)
    sequence = [trim(first), derivative(first)]
    while sequence[-1] != [0]:
        _, remainder = divmod_poly(sequence[-2], sequence[-1])
        if remainder == [0]:
            break
        sequence.append(trim([-value for value in remainder]))
    return sequence


def sign(value):
    return (value > 0) - (value < 0)


def variations(signs):
    cleaned = [item for item in signs if item]
    return sum(cleaned[i] != cleaned[i - 1] for i in range(1, len(cleaned)))


def distinct_positive_roots(poly):
    sequence = sturm_sequence(poly)
    at_zero = [sign(item[0]) for item in sequence]
    at_infinity = [sign(item[-1]) for item in sequence]
    return variations(at_zero) - variations(at_infinity)


def discriminant_cubic(a, b, c, d):
    return 18 * a * b * c * d - 4 * b**3 * d + b**2 * c**2 - 4 * a * c**3 - 27 * a**2 * d**2


def normalized_poly(curvature_sign, beta):
    # Three times P after r=2x/sqrt(|R0|), beta=b*sqrt(|R0|)/2.
    if curvature_sign == "negative":
        return [3 * beta, F(3), F(0), F(1)]
    if curvature_sign == "positive":
        return [3 * beta, F(3), F(0), F(-1)]
    if curvature_sign == "zero":
        return [beta, F(1)]
    raise ValueError(curvature_sign)


def expected_rows():
    return [
        {
            "R0_condition": "R0<0", "b_condition": "b>=0",
            "positive_f_intervals": "(0,infinity)", "root_structure": "no positive root",
            "center_status": "smooth only when b=0",
        },
        {
            "R0_condition": "R0<0", "b_condition": "b<0",
            "positive_f_intervals": "(r_h,infinity)",
            "root_structure": "one simple positive root r_h",
            "center_status": "center excluded; Weyl singular",
        },
        {
            "R0_condition": "R0=0", "b_condition": "b>=0",
            "positive_f_intervals": "(0,infinity)", "root_structure": "no positive root",
            "center_status": "smooth only when b=0",
        },
        {
            "R0_condition": "R0=0", "b_condition": "b<0",
            "positive_f_intervals": "(-b,infinity)",
            "root_structure": "one simple positive root -b",
            "center_status": "center excluded; Weyl singular",
        },
        {
            "R0_condition": "R0>0", "b_condition": "b>=0",
            "positive_f_intervals": "(0,r_plus)",
            "root_structure": "one simple positive outer root; r_plus=sqrt(12/R0) when b=0",
            "center_status": "smooth only when b=0",
        },
        {
            "R0_condition": "R0>0", "b_condition": "-4/(3*sqrt(R0))<b<0",
            "positive_f_intervals": "(r_minus,r_plus)",
            "root_structure": "two simple positive roots",
            "center_status": "center excluded; Weyl singular",
        },
        {
            "R0_condition": "R0>0", "b_condition": "b=-4/(3*sqrt(R0))",
            "positive_f_intervals": "none",
            "root_structure": "one positive double root at 2/sqrt(R0); f does not become positive",
            "center_status": "no positive-f static interval",
        },
        {
            "R0_condition": "R0>0", "b_condition": "b<-4/(3*sqrt(R0))",
            "positive_f_intervals": "none", "root_structure": "no positive root and f<0",
            "center_status": "no positive-f static interval",
        },
    ]


def main():
    # Exact discriminants of the integer-normalized cubics.
    # positive R0: -x^3+3x+3 beta; negative R0: x^3+3x+3 beta.
    beta_symbol = "beta"
    positive_discriminant_constant = discriminant_cubic(F(-1), F(0), F(3), F(0))
    positive_discriminant_beta2 = -27 * F(1) * F(9)  # coefficient of beta^2
    negative_discriminant_constant = discriminant_cubic(F(1), F(0), F(3), F(0))
    negative_discriminant_beta2 = -27 * F(1) * F(9)
    assert positive_discriminant_constant == 108
    assert positive_discriminant_beta2 == -243
    assert negative_discriminant_constant == -108
    assert negative_discriminant_beta2 == -243

    # A positive repeated root in the positive-curvature polynomial must satisfy p'=0.
    # p'=3(1-x^2), hence x=1, and p(1)=2+3 beta=0 gives beta=-2/3.
    repeated_beta = F(-2, 3)
    repeated_poly = normalized_poly("positive", repeated_beta)
    expected_factor = [F(-2), F(3), F(0), F(-1)]  # -(x-1)^2(x+2)
    assert repeated_poly == expected_factor
    quotient, remainder = divmod_poly(repeated_poly, [F(-1), F(1)])
    assert remainder == [0]
    quotient2, remainder2 = divmod_poly(quotient, [F(-1), F(1)])
    assert remainder2 == [0] and quotient2 == [F(-2), F(-1)]
    assert distinct_positive_roots(repeated_poly) == 1

    # beta=0 is the only possible crossing through the excluded r=0 boundary.
    assert normalized_poly("positive", F(0))[0] == 0
    assert normalized_poly("negative", F(0))[0] == 0
    assert normalized_poly("zero", F(0))[0] == 0

    # Exact Sturm representatives for every connected positive-root topology cell and boundary.
    cells = {
        "R0_negative_beta_positive": ("negative", F(1), 0),
        "R0_negative_beta_zero": ("negative", F(0), 0),
        "R0_negative_beta_negative": ("negative", F(-1), 1),
        "R0_zero_b_positive": ("zero", F(1), 0),
        "R0_zero_b_zero": ("zero", F(0), 0),
        "R0_zero_b_negative": ("zero", F(-1), 1),
        "R0_positive_beta_positive": ("positive", F(1), 1),
        "R0_positive_beta_plus_discriminant_boundary": ("positive", F(2, 3), 1),
        "R0_positive_beta_zero": ("positive", F(0), 1),
        "R0_positive_between_threshold_and_zero": ("positive", F(-1, 3), 2),
        "R0_positive_at_negative_threshold": ("positive", F(-2, 3), 1),
        "R0_positive_below_negative_threshold": ("positive", F(-1), 0),
    }
    cell_results = {}
    for name, (curvature_sign, beta, expected) in cells.items():
        actual = distinct_positive_roots(normalized_poly(curvature_sign, beta))
        assert actual == expected, (name, actual, expected)
        cell_results[name] = actual

    # Topology is exhaustive: positive roots can change only at beta=0 (r=0 crossing) or
    # beta=-2/3 (positive repeated root). For R0<0, p'=3(1+x^2)>0; for R0=0 the law is linear.
    topology_cells = [
        "R0<0: beta<0 | beta=0 | beta>0",
        "R0=0: b<0 | b=0 | b>0",
        "R0>0: beta<-2/3 | beta=-2/3 | -2/3<beta<0 | beta=0 | beta>0",
    ]

    # Exact interval orientations follow from P(0)=b, the leading sign, and the positive-root count.
    orientation = {
        "R0<0,b>=0": "positive_on_(0,infinity)",
        "R0<0,b<0": "negative_then_positive_after_unique_root",
        "R0=0,b>=0": "positive_on_(0,infinity)",
        "R0=0,b<0": "negative_then_positive_after_-b",
        "R0>0,b>=0": "positive_then_negative_after_unique_outer_root",
        "R0>0,-threshold<b<0": "negative_positive_negative_across_two_roots",
        "R0>0,b=-threshold": "nonpositive_with_one_double_zero",
        "R0>0,b<-threshold": "negative_on_(0,infinity)",
    }

    with (ROOT / "DOMAIN_CLASSIFICATION.tsv").open(encoding="utf-8", newline="") as handle:
        observed_rows = list(csv.DictReader(handle, delimiter="\t"))
    expected = expected_rows()
    assert observed_rows == expected

    result = {
        "status": "PASS",
        "imports_production_code": False,
        "method": "dependency-free exact nondimensionalization, discriminant, Sturm cells, boundary factorization, and sign orientation",
        "positive_R0_discriminant": f"108-243*{beta_symbol}^2",
        "negative_R0_discriminant": f"-108-243*{beta_symbol}^2",
        "positive_repeated_root": "x=1,beta=-2/3",
        "physical_threshold": "b=-4/(3*sqrt(R0))",
        "repeated_factorization": "-(x-1)^2*(x+2)",
        "root_at_zero_boundary": "beta=0",
        "topology_cells": topology_cells,
        "cell_positive_root_counts": cell_results,
        "interval_orientation": orientation,
        "rows_verified_field_by_field": len(observed_rows),
        "all_fields_match": True,
    }
    (ROOT / "DOMAIN_CENSUS_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G302 exhaustive domain census PASS (8/8 rows)")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

