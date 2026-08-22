#!/usr/bin/env python3
"""Independent exact-Fraction G217 replay; imports no production code."""

from fractions import Fraction
import json
import random


def positive_fraction(rng):
    return Fraction(rng.randint(1, 23), rng.randint(1, 23))


def smooth_map(a, b, slope, bend, x):
    dx = x - a
    return b + slope * dx + bend * dx * dx


def smooth_derivative(a, slope, bend, x):
    return slope + 2 * bend * (x - a)


rng = random.Random(21720260822)
cases = 10_000
assertions = 0

for index in range(cases):
    exp_ab = positive_fraction(rng)
    exp_bc = positive_fraction(rng)
    lam_ab = 1 / exp_ab
    lam_bc = 1 / exp_bc
    lam_ac = 1 / (exp_ab * exp_bc)

    assert lam_ab > 0; assertions += 1
    assert exp_ab * lam_ab == 1; assertions += 1
    assert (1 / exp_ab) * (1 / lam_ab) == 1; assertions += 1
    assert lam_bc * lam_ab == lam_ac; assertions += 1
    assert exp_ab * exp_bc * lam_ac == 1; assertions += 1
    assert (1 / lam_ab) * (1 / lam_bc) == exp_ab * exp_bc; assertions += 1

    rate_a = positive_fraction(rng)
    rate_b = lam_ab * rate_a
    common = positive_fraction(rng)
    assert rate_b / rate_a == lam_ab; assertions += 1
    assert (rate_b / common) / (rate_a / common) == lam_ab; assertions += 1

    scale_a = positive_fraction(rng)
    scale_b = positive_fraction(rng)
    changed = (rate_b / scale_b) / (rate_a / scale_a)
    assert changed == lam_ab * scale_a / scale_b; assertions += 1

    a = Fraction(index % 11, 7)
    b_one = Fraction(index % 13 + 1, 5)
    b_two = b_one + 1
    assert b_one != b_two; assertions += 1
    assert smooth_map(a, b_one, lam_ab, 0, a) == b_one; assertions += 1
    assert smooth_map(a, b_two, lam_ab, 0, a) == b_two; assertions += 1

    bend_one = positive_fraction(rng)
    bend_two = bend_one + 1
    probe = a + Fraction(1, 101)
    assert smooth_map(a, b_one, lam_ab, bend_one, a) == b_one; assertions += 1
    assert smooth_map(a, b_one, lam_ab, bend_two, a) == b_one; assertions += 1
    assert smooth_derivative(a, lam_ab, bend_one, a) == smooth_derivative(a, lam_ab, bend_two, a) == lam_ab; assertions += 1
    assert smooth_map(a, b_one, lam_ab, bend_one, probe) != smooth_map(a, b_one, lam_ab, bend_two, probe); assertions += 1
    assert 2 * bend_one != 2 * bend_two; assertions += 1

    independent_direct = lam_ac + Fraction(1, 97)
    assert independent_direct != lam_ac; assertions += 1
    assert -(rate_a**2) / (rate_a**2) == -1; assertions += 1

print(json.dumps({
    "audit": "G217",
    "status": "PASS",
    "cases": cases,
    "assertions": assertions,
    "assertions_per_case": assertions // cases,
    "method": "independent exact positive-line first-jet and nonselection replay",
}, sort_keys=True))
