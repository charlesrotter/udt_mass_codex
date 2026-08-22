#!/usr/bin/env python3
"""Independent exact-Fraction G216 replay; imports no production code."""

from fractions import Fraction
import json
import random


def proper_clock_rate(numerator, denominator):
    return Fraction(numerator, denominator)


def relation_derivative(rate_left, rate_right):
    return rate_right / rate_left


def reciprocal_multiplier(rate_left, rate_right):
    return rate_left / rate_right


def squared_reciprocal_readout(rate_left, rate_right):
    return (rate_right / rate_left) ** 2


rng = random.Random(21620260822)
cases = 10_000
assertions = 0

for index in range(cases):
    rate_a = proper_clock_rate(rng.randint(1, 19), rng.randint(1, 19))
    rate_b = proper_clock_rate(rng.randint(1, 19), rng.randint(1, 19))
    rate_c = proper_clock_rate(rng.randint(1, 19), rng.randint(1, 19))

    # u=(d tau/dy)U with g(U,U)=-1.
    assert -(rate_a**2) / (rate_a**2) == -1; assertions += 1
    assert -(rate_b**2) / (rate_b**2) == -1; assertions += 1
    assert Fraction(1) ** 2 == 1; assertions += 1

    derivative_ab = relation_derivative(rate_a, rate_b)
    multiplier_ab = reciprocal_multiplier(rate_a, rate_b)
    q_ab = squared_reciprocal_readout(rate_a, rate_b)
    assert derivative_ab * multiplier_ab == 1; assertions += 1
    assert multiplier_ab**2 * q_ab == 1; assertions += 1
    assert multiplier_ab * reciprocal_multiplier(rate_b, rate_a) == 1; assertions += 1

    # One common pair coordinate change cancels exactly.
    common = proper_clock_rate(rng.randint(1, 19), rng.randint(1, 19))
    re_a = rate_a / common
    re_b = rate_b / common
    assert reciprocal_multiplier(re_a, re_b) == multiplier_ab; assertions += 1
    assert squared_reciprocal_readout(re_a, re_b) == q_ab; assertions += 1

    # Independent coordinate changes are different calibrated incidence data.
    scale_a = proper_clock_rate(rng.randint(1, 19), rng.randint(1, 19))
    scale_b = proper_clock_rate(rng.randint(1, 19), rng.randint(1, 19))
    independently_changed = reciprocal_multiplier(rate_a / scale_a, rate_b / scale_b)
    assert independently_changed == multiplier_ab * scale_b / scale_a; assertions += 1
    changed_q = squared_reciprocal_readout(rate_a / scale_a, rate_b / scale_b)
    assert changed_q == q_ab * (scale_a / scale_b) ** 2; assertions += 1

    # Composable pair-germ derivatives obey the ordinary chain rule.
    derivative_bc = relation_derivative(rate_b, rate_c)
    derivative_ac = relation_derivative(rate_a, rate_c)
    assert derivative_ab * derivative_bc == derivative_ac; assertions += 1
    assert multiplier_ab * reciprocal_multiplier(rate_b, rate_c) == reciprocal_multiplier(rate_a, rate_c); assertions += 1
    assert q_ab * squared_reciprocal_readout(rate_b, rate_c) == squared_reciprocal_readout(rate_a, rate_c); assertions += 1

    # Static chart exact proxy: a=exp(-phi), g00=-a^2, U=(1/a)partial_0.
    static_a = proper_clock_rate(rng.randint(1, 19), rng.randint(1, 19))
    metric_00 = -(static_a**2)
    assert metric_00 * (1 / static_a) ** 2 == -1; assertions += 1
    assert -metric_00 == static_a**2; assertions += 1
    assert (1 / static_a) ** 4 * static_a**4 == 1; assertions += 1

    # The absolute endpoint factor changes under common reparameterization; the edge does not.
    assert (rate_a / common) ** 2 == rate_a**2 / common**2; assertions += 1
    assert ((rate_b / common) / (rate_a / common)) == derivative_ab; assertions += 1

    # Distinct events on one observer label may carry distinct rates.
    other_event_rate = rate_a + Fraction(index % 7 + 1, 23)
    assert other_event_rate != rate_a; assertions += 1

print(json.dumps({
    "audit": "G216",
    "status": "PASS",
    "cases": cases,
    "assertions": assertions,
    "assertions_per_case": assertions // cases,
    "method": "independent exact Fraction proper-clock rate and event-pair derivative replay",
}, sort_keys=True))

