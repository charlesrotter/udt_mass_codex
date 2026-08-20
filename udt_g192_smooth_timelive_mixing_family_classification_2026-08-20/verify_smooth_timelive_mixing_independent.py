#!/usr/bin/env python3
"""Independent standard-library replay for G192.

This verifier does not import the production module and does not read its output.
It integrates the affine Jacobi system directly in eta and compares it with a
separately evaluated exact factorized quadrature.
"""

from __future__ import annotations

import json
import math
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


SEED = 19220260820
RANDOM_CASES = 256
RK4_STEPS = 5000
SIMPSON_STEPS = 20000
TOLERANCE = 2.0e-9
SQRT2 = math.sqrt(2.0)


@dataclass(frozen=True)
class History:
    name: str
    endpoint: float
    L: Callable[[float], float]
    Lp: Callable[[float], float]
    Lpp: Callable[[float], float]
    mu: Callable[[float], float]
    mup: Callable[[float], float]
    I: Callable[[float], float]


def simpson(function, endpoint, steps=SIMPSON_STEPS):
    if steps % 2:
        raise ValueError("Simpson steps must be even")
    step = endpoint / steps
    total = function(0.0) + function(endpoint)
    for index in range(1, steps):
        total += (4.0 if index % 2 else 2.0) * function(index * step)
    return total * step / 3.0


def exact_factorized(history):
    endpoint = history.endpoint
    I_end = history.I(endpoint)
    J_end = simpson(lambda value: math.exp(4.0 * history.I(value)), endpoint)
    scale = math.exp(history.L(endpoint))
    plus = scale * math.exp(-2.0 * I_end) * J_end
    minus = scale * endpoint
    frequency = math.exp(-history.L(endpoint))
    lam = simpson(lambda value: math.exp(2.0 * history.L(value)), endpoint)
    return frequency, plus, minus, plus * minus, lam


def rhs_eta(history, eta, state):
    frequency, plus, plus_velocity, minus, minus_velocity, lam = state
    log_scale = history.L(eta)
    scale = math.exp(log_scale)
    lp = history.Lp(eta)
    lpp = history.Lpp(eta)
    mixing = history.mu(eta)
    mixing_prime = history.mup(eta)
    inverse_scale_four = math.exp(-4.0 * log_scale)
    isotropic_tide = (lp * lp - lpp) * inverse_scale_four
    mixing_tide = (2.0 * SQRT2 * mixing_prime - 8.0 * mixing * mixing) * inverse_scale_four
    scale_squared = scale * scale
    return [
        -lp * frequency,
        scale_squared * plus_velocity,
        -scale_squared * (isotropic_tide + mixing_tide) * plus,
        scale_squared * minus_velocity,
        -scale_squared * isotropic_tide * minus,
        scale_squared,
    ]


def add_scaled(state, slope, scale):
    return [value + scale * change for value, change in zip(state, slope)]


def rk4(history):
    step = history.endpoint / RK4_STEPS
    state = [1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
    eta = 0.0
    for _ in range(RK4_STEPS):
        k1 = rhs_eta(history, eta, state)
        k2 = rhs_eta(history, eta + step / 2.0, add_scaled(state, k1, step / 2.0))
        k3 = rhs_eta(history, eta + step / 2.0, add_scaled(state, k2, step / 2.0))
        k4 = rhs_eta(history, eta + step, add_scaled(state, k3, step))
        state = [
            value + step * (one + 2.0 * two + 2.0 * three + four) / 6.0
            for value, one, two, three, four in zip(state, k1, k2, k3, k4)
        ]
        eta += step
    return state


def named_histories():
    return [
        History(
            "C01_G191",
            1.2,
            lambda e: 0.35 * e,
            lambda e: 0.35,
            lambda e: 0.0,
            lambda e: 0.22,
            lambda e: 0.0,
            lambda e: SQRT2 * 0.22 * e,
        ),
        History(
            "C02_G190_nonconstant",
            1.1,
            lambda e: 0.20 * e + 0.08 * e * e,
            lambda e: 0.20 + 0.16 * e,
            lambda e: 0.16,
            lambda e: 0.0,
            lambda e: 0.0,
            lambda e: 0.0,
        ),
        History(
            "C03_single_turn",
            1.2,
            lambda e: 0.55 * e - 0.55 * e * e,
            lambda e: 0.55 - 1.10 * e,
            lambda e: -1.10,
            lambda e: 0.15 + 0.08 * math.sin(2.0 * e),
            lambda e: 0.16 * math.cos(2.0 * e),
            lambda e: SQRT2 * (0.15 * e + 0.04 * (1.0 - math.cos(2.0 * e))),
        ),
        History(
            "C04_multiple_turns_signed_mix",
            1.5,
            lambda e: 0.12 * math.sin(4.0 * e),
            lambda e: 0.48 * math.cos(4.0 * e),
            lambda e: -1.92 * math.sin(4.0 * e),
            lambda e: 0.18 * math.sin(3.0 * e),
            lambda e: 0.54 * math.cos(3.0 * e),
            lambda e: SQRT2 * 0.06 * (1.0 - math.cos(3.0 * e)),
        ),
        History(
            "C05_increasing_frequency_signed_mix",
            1.3,
            lambda e: -0.18 * e + 0.04 * e * e,
            lambda e: -0.18 + 0.08 * e,
            lambda e: 0.08,
            lambda e: 0.28 * math.cos(2.5 * e) - 0.12,
            lambda e: -0.70 * math.sin(2.5 * e),
            lambda e: SQRT2 * (0.112 * math.sin(2.5 * e) - 0.12 * e),
        ),
        History(
            "C06_zero_crossing_mix",
            1.2,
            lambda e: 0.10 * e,
            lambda e: 0.10,
            lambda e: 0.0,
            lambda e: 0.30 * (e - 0.5),
            lambda e: 0.30,
            lambda e: SQRT2 * 0.30 * (0.5 * e * e - 0.5 * e),
        ),
        History(
            "C07_small_regular_scale",
            1.5,
            lambda e: -1.40 * e,
            lambda e: -1.40,
            lambda e: 0.0,
            lambda e: 0.35 * math.exp(-0.5 * e),
            lambda e: -0.175 * math.exp(-0.5 * e),
            lambda e: SQRT2 * 0.70 * (1.0 - math.exp(-0.5 * e)),
        ),
        History(
            "C08_nonzero_mix_zero_tracefree_tide",
            1.4,
            lambda e: 0.25 * e,
            lambda e: 0.25,
            lambda e: 0.0,
            lambda e: -1.0 / (SQRT2 * (2.0 * e + 3.0)),
            lambda e: SQRT2 / ((2.0 * e + 3.0) ** 2),
            lambda e: -0.5 * math.log((2.0 * e + 3.0) / 3.0),
        ),
        History(
            "C09_negative_cross_response",
            1.2,
            lambda e: 0.15 * e,
            lambda e: 0.15,
            lambda e: 0.0,
            lambda e: 0.25 * e / SQRT2,
            lambda e: 0.25 / SQRT2,
            lambda e: 0.125 * e * e,
        ),
        History(
            "C10_G188",
            1.1,
            lambda e: 0.0,
            lambda e: 0.0,
            lambda e: 0.0,
            lambda e: 0.31,
            lambda e: 0.0,
            lambda e: SQRT2 * 0.31 * e,
        ),
    ]


def random_histories(rng):
    histories = []
    coefficients = []
    for index in range(RANDOM_CASES):
        c1 = rng.uniform(-0.5, 0.7)
        c2 = rng.uniform(-0.3, 0.3)
        c3 = rng.uniform(-0.15, 0.15)
        w = rng.uniform(0.5, 4.0)
        m0 = rng.uniform(-0.4, 0.4)
        m1 = rng.uniform(-0.35, 0.35)
        m2 = rng.uniform(-0.3, 0.3)
        v = rng.uniform(0.5, 4.0)
        endpoint = rng.uniform(0.2, 1.5)
        coefficients.append([c1, c2, c3, w, m0, m1, m2, v, endpoint])
        histories.append(
            History(
                f"R{index:03d}",
                endpoint,
                lambda e, c1=c1, c2=c2, c3=c3, w=w: c1 * e + c2 * e * e + c3 * math.sin(w * e),
                lambda e, c1=c1, c2=c2, c3=c3, w=w: c1 + 2.0 * c2 * e + c3 * w * math.cos(w * e),
                lambda e, c2=c2, c3=c3, w=w: 2.0 * c2 - c3 * w * w * math.sin(w * e),
                lambda e, m0=m0, m1=m1, m2=m2, v=v: m0 + m1 * e + m2 * math.sin(v * e),
                lambda e, m1=m1, m2=m2, v=v: m1 + m2 * v * math.cos(v * e),
                lambda e, m0=m0, m1=m1, m2=m2, v=v: SQRT2
                * (m0 * e + 0.5 * m1 * e * e + m2 * (1.0 - math.cos(v * e)) / v),
            )
        )
    return histories, coefficients


def turn_count(history, samples=4096):
    previous = history.Lp(0.0)
    count = 0
    for index in range(1, samples + 1):
        current = history.Lp(history.endpoint * index / samples)
        if previous * current < 0.0:
            count += 1
        previous = current
    return count


def main():
    rng = random.Random(SEED)
    random_cases, coefficients = random_histories(rng)
    histories = named_histories() + random_cases
    maximum_frequency_error = 0.0
    maximum_plus_error = 0.0
    maximum_minus_error = 0.0
    maximum_lambda_error = 0.0
    minimum_determinant = math.inf
    assertions = 0
    summaries = {}

    for history in histories:
        exact_frequency, exact_plus, exact_minus, exact_det, exact_lambda = exact_factorized(history)
        numeric = rk4(history)
        frequency_error = abs(numeric[0] - exact_frequency)
        plus_error = abs(numeric[1] - exact_plus)
        minus_error = abs(numeric[3] - exact_minus)
        lambda_error = abs(numeric[5] - exact_lambda)
        maximum_frequency_error = max(maximum_frequency_error, frequency_error)
        maximum_plus_error = max(maximum_plus_error, plus_error)
        maximum_minus_error = max(maximum_minus_error, minus_error)
        maximum_lambda_error = max(maximum_lambda_error, lambda_error)
        minimum_determinant = min(minimum_determinant, exact_det)

        assert frequency_error < TOLERANCE
        assert plus_error < TOLERANCE
        assert minus_error < TOLERANCE
        assert lambda_error < TOLERANCE
        assert exact_frequency > 0.0
        assert exact_plus > 0.0
        assert exact_minus > 0.0
        assert exact_det > 0.0
        assertions += 8

        if history.name.startswith("C"):
            summaries[history.name] = {
                "frequency": exact_frequency,
                "plus_mode": exact_plus,
                "minus_mode": exact_minus,
                "cross_response": 0.5 * (exact_plus - exact_minus),
                "determinant": exact_det,
                "lambda": exact_lambda,
                "turn_count": turn_count(history),
            }

    # Named classification controls fixed before this implementation.
    assert summaries["C03_single_turn"]["turn_count"] == 1
    assert summaries["C04_multiple_turns_signed_mix"]["turn_count"] >= 2
    assert summaries["C05_increasing_frequency_signed_mix"]["frequency"] > 1.0
    assert summaries["C01_G191"]["cross_response"] > 0.0
    assert summaries["C09_negative_cross_response"]["cross_response"] < 0.0
    assert abs(summaries["C08_nonzero_mix_zero_tracefree_tide"]["cross_response"]) < 5.0e-12
    assertions += 6

    result = {
        "status": "PASS",
        "seed": SEED,
        "imports_production_module": False,
        "reads_production_artifact": False,
        "named_cases": 10,
        "random_cases": RANDOM_CASES,
        "rk4_steps_per_case": RK4_STEPS,
        "simpson_steps_per_case": SIMPSON_STEPS,
        "registered_tolerance": TOLERANCE,
        "maximum_frequency_error": maximum_frequency_error,
        "maximum_plus_mode_error": maximum_plus_error,
        "maximum_minus_mode_error": maximum_minus_error,
        "maximum_lambda_error": maximum_lambda_error,
        "minimum_endpoint_determinant": minimum_determinant,
        "assertions": assertions,
        "named_summaries": summaries,
        "random_coefficients": coefficients,
    }
    if os.environ.get("G192_NO_WRITE") != "1":
        output = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
