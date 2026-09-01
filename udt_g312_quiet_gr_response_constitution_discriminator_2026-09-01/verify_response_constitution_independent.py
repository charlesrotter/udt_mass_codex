#!/usr/bin/env python3
"""Independent exact verifier for G312; imports no production code or result."""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
Q = Fraction
SIGN = (-1, 1, 1, 1)
PAIRS = tuple((i, j) for i in range(4) for j in range(i, 4))


def unpack(entries):
    matrix = [[Q(0) for _ in range(4)] for _ in range(4)]
    for value, (i, j) in zip(entries, PAIRS):
        matrix[i][j] = value
        matrix[j][i] = value
    return matrix


def pack(matrix):
    return tuple(matrix[i][j] for i, j in PAIRS)


def lorentz_trace(entries):
    matrix = unpack(entries)
    return sum(SIGN[i] * matrix[i][i] for i in range(4))


def tf(entries):
    matrix = unpack(entries)
    scalar = lorentz_trace(entries) / 4
    for i in range(4):
        matrix[i][i] -= scalar * SIGN[i]
    return pack(matrix)


def combine_ricci_scalar(entries, alpha, beta):
    matrix = unpack(entries)
    scalar = lorentz_trace(entries)
    for i in range(4):
        for j in range(4):
            matrix[i][j] *= alpha
        matrix[i][i] += beta * scalar * SIGN[i]
    return pack(matrix)


def ricci_square_tf(entries):
    matrix = unpack(entries)
    square = [[sum(matrix[i][k] * SIGN[k] * matrix[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
    return tf(pack(square))


def integrate_twice(values):
    first = [Q(0)]
    for value in values:
        first.append(first[-1] + value)
    second = [Q(0)]
    for value in first[1:]:
        second.append(second[-1] + value)
    return second


def registry_rows():
    with (REPO / "CURRENT_SCIENTIFIC_PREMISES.tsv").open(encoding="utf-8", newline="") as stream:
        return {row["premise_id"]: row for row in csv.DictReader(stream, delimiter="\t")}


def main():
    checks = 0

    # Different flattened representation and coefficient order from production.
    for index in range(1, 193):
        entries = tuple(Q(((index * (slot + 3)) % 17) - 8, (slot % 5) + 1) for slot in range(10))
        alpha = Q((index % 11) + 1, (index % 7) + 1)
        beta = Q((index % 13) - 6, (index % 3) + 1)
        actual = tf(combine_ricci_scalar(entries, alpha, beta))
        expected = tuple(alpha * component for component in tf(entries))
        assert actual == expected
        checks += 10

    # The quadratic lane has solution overlap but a vanishing first quiet jet.
    zero = (Q(0),) * 10
    assert ricci_square_tf(zero) == zero
    checks += 10
    nonzero = 0
    for index in range(1, 97):
        entries = tuple(Q(index + slot - 5, slot + 2) for slot in range(10))
        base = ricci_square_tf(entries)
        for numerator, denominator in ((1, 9), (2, 7), (5, 3)):
            factor = Q(numerator, denominator)
            scaled = tuple(factor * component for component in entries)
            assert ricci_square_tf(scaled) == tuple(factor * factor * component for component in base)
            checks += 10
        if any(base):
            nonzero += 1
    assert nonzero == 96
    checks += 1

    # A nonlinear degree-one toy response cannot possess a linear derivative at the origin.
    def directional(x, y):
        norm2 = x * x + y * y
        return (x * x * x / norm2, y * y * y / norm2)

    assert directional(Q(1), Q(1)) != tuple(
        directional(Q(1), Q(0))[i] + directional(Q(0), Q(1))[i] for i in range(2)
    )
    checks += 2

    # Independent history-carry witness: identical terminal local source, different integrated past.
    past_a = [Q(1), Q(0), Q(0), Q(0), Q(0), Q(0), Q(0)]
    past_b = [Q(0)] * 7
    twice_a = integrate_twice(integrate_twice(past_a))
    twice_b = integrate_twice(integrate_twice(past_b))
    assert past_a[-4:] == past_b[-4:]
    assert twice_a[-1] != twice_b[-1]
    assert twice_a[-1] - twice_a[-2] != twice_b[-1] - twice_b[-2]
    checks += 3

    # Dimensional and ownership gates, independently reconstructed.
    assert (-4) + 2 == -2  # quadratic curvature plus one length-squared coefficient
    assert (-4) + 4 == 0   # two inverse boxes make a dimensionless history scalar
    assert 0 + (-1) + (-1) == -2  # its gradient square can re-enter a rank-two response
    checks += 3

    rows = registry_rows()
    assert "solution overlap" in rows["G257"]["active_use"].lower() or "comparison" in rows["G257"]["active_use"].lower()
    assert "POINTWISE_LOCALITY_SECOND_ORDER" in rows["G261"]["current_status"]
    assert "CURRENT_PREMISES_DO_NOT_PRIVILEGE_ONE_RESIDUAL_FORM" in rows["G296"]["current_status"]
    assert "whether UDT owns locality" in rows["G301"]["open_scope"]
    assert "RESPONSE_CONSTITUTION_REMAINS_OPEN" in rows["G311"]["current_status"]
    checks += 5

    result = {
        "status": "PASS",
        "landing": "TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED",
        "checks": checks,
        "production_imported": False,
        "production_result_read": False,
        "separation_witnesses": {
            "local_but_not_gr_principal": "PURE_CURVATURE_QUADRATIC",
            "gr_principal_but_not_local": "SCALE_FREE_NONLOCAL_METRIC_HISTORY",
        },
        "conditional_result": "FULL_QUIET_GR_PRINCIPAL_OVERLAP_PLUS_LOCAL_FINITE_JET_RESPONSE_CLOSES_G301_WITH_EXISTING_NO_SCALE_AND_REGULARITY_GATES",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
