#!/usr/bin/env python3
"""Independent exact-Fraction G215 replay; imports no production code."""

from fractions import Fraction
import json
import random


def multiply(left, right):
    return tuple(tuple(sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def transpose(matrix):
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def transform(metric, basis):
    return multiply(multiply(transpose(basis), metric), basis)


def pair(clock, ruler, shear):
    return (
        (-clock**2, -(clock**2) * shear),
        (-(clock**2) * shear, ruler**2 - clock**2 * shear**2),
    )


def completed(metric, density):
    inverse = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1) / density))
    return transform(metric, inverse)


def k_value(metric):
    return -determinant(metric) / metric[0][0] ** 2


rng = random.Random(21520260822)
cases = 10_000
assertions = 0

for index in range(cases):
    clock = Fraction(rng.randint(1, 13), rng.randint(1, 13))
    ruler_one = Fraction(rng.randint(1, 13), rng.randint(1, 13))
    ruler_two = Fraction(rng.randint(1, 13), rng.randint(1, 13))
    shear_one = Fraction(rng.randint(-11, 11), rng.randint(1, 13))
    # Force beta_two/L_two to differ from beta_one/L_one. Merely changing raw
    # ruler data can describe the same completed tuple after density normalization.
    shear_two = ruler_two * (shear_one / ruler_one + Fraction(index % 5 + 1, 7))

    raw_one = pair(clock, ruler_one, shear_one)
    raw_two = pair(clock, ruler_two, shear_two)
    density_one = clock * ruler_one
    density_two = clock * ruler_two
    done_one = completed(raw_one, density_one)
    done_two = completed(raw_two, density_two)

    assert determinant(raw_one) == -(density_one**2); assertions += 1
    assert determinant(raw_two) == -(density_two**2); assertions += 1
    assert determinant(done_one) == -1; assertions += 1
    assert determinant(done_two) == -1; assertions += 1
    assert done_one[0][0] == done_two[0][0] == -(clock**2); assertions += 1
    assert k_value(done_one) == k_value(done_two) == 1 / clock**4; assertions += 1
    assert done_one != done_two; assertions += 1
    assert done_one[0][1] != done_two[0][1]; assertions += 1
    assert density_one != 0 and density_two != 0; assertions += 1

    ruler_change = Fraction(rng.randint(1, 13), rng.randint(1, 13))
    rechart_shear = Fraction(rng.randint(-11, 11), rng.randint(1, 13))
    clock_fixed_change = ((Fraction(1), rechart_shear), (Fraction(0), ruler_change))
    clock_fixed_raw = transform(raw_one, clock_fixed_change)
    assert 1 / ((-clock_fixed_raw[0][0]) ** 2) == 1 / clock**4; assertions += 1

    clock_change = Fraction(rng.randint(1, 13), rng.randint(1, 13))
    general_change = ((clock_change, rechart_shear), (Fraction(0), ruler_change))
    general_raw = transform(raw_one, general_change)
    assert 1 / ((-general_raw[0][0]) ** 2) == 1 / ((clock_change * clock) ** 4); assertions += 1

    clocks = [Fraction(rng.randint(1, 13), rng.randint(1, 13)) for _ in range(4)]
    edge_q = [clocks[(i + 1) % 4] ** 2 / clocks[i] ** 2 for i in range(4)]
    product = Fraction(1)
    for value in edge_q:
        product *= value
    assert product == 1; assertions += 1
    assert edge_q[0] * (1 / edge_q[0]) == 1; assertions += 1

    scale = Fraction(index % 9 + 2, index % 7 + 1)
    if scale == 1:
        scale = Fraction(3, 2)
    broken_second = clocks[2] ** 2 / ((scale * clocks[1]) ** 2)
    broken_cycle = edge_q[0] * broken_second * (clocks[0] ** 2 / clocks[2] ** 2)
    assert broken_cycle == 1 / scale**2; assertions += 1
    assert broken_cycle != 1; assertions += 1

    # Same scalar never implies full pair-metric equality.
    assert k_value(done_one) == k_value(done_two) and done_one != done_two; assertions += 1

    # G171's fixed rational witness is completed on every pass as a regression anchor.
    g171_one = ((Fraction(-1), Fraction(-1, 2)), (Fraction(-1, 2), Fraction(3, 4)))
    g171_two = ((Fraction(-1), Fraction(-1, 2)), (Fraction(-1, 2), Fraction(211, 100)))
    assert k_value(g171_one) == 1; assertions += 1
    assert k_value(g171_two) == Fraction(59, 25); assertions += 1
    assert 1 / ((-g171_one[0][0]) ** 2) == 1 / ((-g171_two[0][0]) ** 2) == 1; assertions += 1

print(json.dumps({
    "audit": "G215",
    "status": "PASS",
    "cases": cases,
    "assertions": assertions,
    "assertions_per_case": assertions // cases,
    "method": "independent exact Fraction completed-incidence and network-cycle replay",
}, sort_keys=True))
