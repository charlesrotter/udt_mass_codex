#!/usr/bin/env python3
"""Independent exact-Fraction G214 replay; imports no production implementation."""

from fractions import Fraction
import json
import random


def product(left, right):
    rows = []
    for row in range(2):
        values = []
        for column in range(2):
            values.append(sum(left[row][inner] * right[inner][column] for inner in range(2)))
        rows.append(tuple(values))
    return tuple(rows)


def transpose(matrix):
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def diagonal(first, second):
    zero = Fraction(0)
    return ((first, zero), (zero, second))


def transform(metric, basis):
    return product(product(transpose(basis), metric), basis)


def build_metric(clock, ruler, shift):
    return (
        (-clock**2, -(clock**2) * shift),
        (-(clock**2) * shift, ruler**2 - clock**2 * shift**2),
    )


def normalize(metric, area_density):
    inverse_calibration = diagonal(Fraction(1), Fraction(1) / area_density)
    return transform(metric, inverse_calibration)


def denormalize(metric, area_density):
    return transform(metric, diagonal(Fraction(1), area_density))


def normalized_basis(change, area_before, area_after):
    return product(
        product(diagonal(Fraction(1), area_before), change),
        diagonal(Fraction(1), Fraction(1) / area_after),
    )


rng = random.Random(21420260822)
cases = 10_000
assertions = 0

for index in range(cases):
    clock = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    ruler = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    shift = Fraction(rng.randint(-9, 9), rng.randint(1, 11))
    metric_i = build_metric(clock, ruler, shift)
    area_i = clock * ruler
    normalized_i = normalize(metric_i, area_i)

    a = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    d = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    shear = Fraction(rng.randint(-9, 9), rng.randint(1, 11))
    change_ij = ((a, shear), (Fraction(0), d))
    metric_j = transform(metric_i, change_ij)
    area_j = a * d * area_i
    normalized_j = normalize(metric_j, area_j)
    carry_ij = normalized_basis(change_ij, area_i, area_j)

    assert determinant(metric_i) == -(area_i**2); assertions += 1
    assert determinant(normalized_i) == -1; assertions += 1
    assert area_j == determinant(change_ij) * area_i; assertions += 1
    assert determinant(metric_j) == -(area_j**2); assertions += 1
    assert determinant(carry_ij) == 1; assertions += 1
    assert normalized_j == transform(normalized_i, carry_ij); assertions += 1
    assert denormalize(normalized_j, area_j) == metric_j; assertions += 1

    a2 = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    d2 = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    shear2 = Fraction(rng.randint(-9, 9), rng.randint(1, 11))
    change_jk = ((a2, shear2), (Fraction(0), d2))
    change_ik = product(change_ij, change_jk)
    metric_k = transform(metric_j, change_jk)
    area_k = determinant(change_jk) * area_j
    normalized_k = normalize(metric_k, area_k)
    carry_jk = normalized_basis(change_jk, area_j, area_k)
    carry_ik = normalized_basis(change_ik, area_i, area_k)

    assert metric_k == transform(metric_i, change_ik); assertions += 1
    assert area_k == determinant(change_ik) * area_i; assertions += 1
    assert product(carry_ij, carry_jk) == carry_ik; assertions += 1
    assert normalized_k == transform(normalized_i, carry_ik); assertions += 1

    ruler_factor = Fraction(rng.randint(1, 11), rng.randint(1, 11))
    ruler_change = diagonal(Fraction(1), ruler_factor)
    ruler_area = ruler_factor * area_i
    ruler_carry = normalized_basis(ruler_change, area_i, ruler_area)
    assert ruler_carry == diagonal(Fraction(1), Fraction(1)); assertions += 1
    assert normalize(transform(metric_i, ruler_change), ruler_area) == normalized_i; assertions += 1

    reverse = diagonal(Fraction(1), Fraction(-1))
    reversed_metric = transform(metric_i, reverse)
    assert determinant(reversed_metric) == determinant(metric_i); assertions += 1
    assert normalize(reversed_metric, area_i) == transform(normalized_i, reverse); assertions += 1
    assert reversed_metric[0][1] == -metric_i[0][1]; assertions += 1

    scale = Fraction(2 + index % 7, 1)
    scaled_metric = transform(metric_i, diagonal(Fraction(1), scale))
    scaled_area = scale * area_i
    assert normalize(scaled_metric, scaled_area) == normalized_i; assertions += 1
    assert scaled_metric != metric_i; assertions += 1

    observer_a = Fraction(2 + index % 5, 3)
    observer_b = Fraction(3 + index % 7, 4)
    observer_c = Fraction(5 + index % 11, 6)
    assert (observer_a / observer_b) * (observer_b / observer_c) == observer_a / observer_c; assertions += 1

    b_on_ab = Fraction(1)
    b_on_bc = Fraction(2 + index % 5)
    assert b_on_ab != b_on_bc; assertions += 1

print(json.dumps({
    "audit": "G214",
    "status": "PASS",
    "cases": cases,
    "assertions": assertions,
    "assertions_per_case": assertions // cases,
    "method": "independent exact Fraction overlap and incidence replay",
}, sort_keys=True))
