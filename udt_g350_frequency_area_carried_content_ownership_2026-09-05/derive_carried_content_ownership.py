#!/usr/bin/env python3
"""Dependency-free G350 production checks for the preregistered character problem."""

import json
import math
import os
import random
from pathlib import Path


TOL = 2.0e-11
SEED = 3500509
CASES = 12000


def transfer(p, q, ratio_frequency, ratio_area):
    return math.exp(p * math.log(ratio_frequency) + q * math.log(ratio_area))


def relative_error(left, right):
    return abs(left - right) / max(1.0, abs(left), abs(right))


def main():
    rng = random.Random(SEED)
    checks = 0
    max_error = 0.0

    def check_close(left, right):
        nonlocal checks, max_error
        err = relative_error(left, right)
        max_error = max(max_error, err)
        checks += 1
        if err > TOL:
            raise AssertionError((left, right, err))

    def check_true(value):
        nonlocal checks
        checks += 1
        if not value:
            raise AssertionError("registered boolean check failed")

    for _ in range(CASES):
        log_omega = [rng.uniform(-3.0, 3.0) for _ in range(3)]
        log_area = [rng.uniform(-3.0, 3.0) for _ in range(3)]
        omega = [math.exp(value) for value in log_omega]
        area = [math.exp(value) for value in log_area]
        p = rng.uniform(-2.5, 2.5)
        q = rng.uniform(-2.5, 2.5)

        r10 = omega[1] / omega[0]
        r21 = omega[2] / omega[1]
        r20 = omega[2] / omega[0]
        a10 = area[1] / area[0]
        a21 = area[2] / area[1]
        a20 = area[2] / area[0]

        check_close(r20, r21 * r10)
        check_close(a20, a21 * a10)
        check_close(
            transfer(p, q, r20, a20),
            transfer(p, q, r21, a21) * transfer(p, q, r10, a10),
        )
        check_close(
            transfer(p, q, 1.0 / r10, 1.0 / a10),
            1.0 / transfer(p, q, r10, a10),
        )
        check_close(transfer(p, q, 1.0, 1.0), 1.0)

        d0 = math.exp(rng.uniform(-1.2, 1.2))
        d1 = math.exp(rng.uniform(-1.2, 1.2))
        content0 = math.exp(rng.uniform(-2.0, 2.0))
        content1 = transfer(p, q, r10, a10) * content0
        transformed0 = d0**p * content0
        transformed1 = d1**p * content1
        transformed_t = transfer(p, q, (d1 / d0) * r10, a10)
        check_close(transformed1, transformed_t * transformed0)

        conserved1 = transfer(p, -1.0, r10, a10) * content0
        invariant0 = content0 * area[0] / omega[0] ** p
        invariant1 = conserved1 * area[1] / omega[1] ** p
        check_close(invariant1, invariant0)

        states = [rng.uniform(-2.0, 2.0) for _ in range(3)]
        beta = rng.uniform(-1.5, 1.5)
        weights = [math.exp(beta * state) for state in states]
        tw10 = (weights[1] / weights[0]) * transfer(p, q, r10, a10)
        tw21 = (weights[2] / weights[1]) * transfer(p, q, r21, a21)
        tw20 = (weights[2] / weights[0]) * transfer(p, q, r20, a20)
        check_close(tw20, tw21 * tw10)
        check_close(
            (weights[0] / weights[1]) * transfer(p, q, 1.0 / r10, 1.0 / a10),
            1.0 / tw10,
        )

        check_true(transfer(p, q, r10, a10) * 0.0 == 0.0)

    ratio_frequency = 1.7
    ratio_area = 2.3
    named = {
        "T_00": transfer(0.0, 0.0, ratio_frequency, ratio_area),
        "T_10": transfer(1.0, 0.0, ratio_frequency, ratio_area),
        "T_01": transfer(0.0, 1.0, ratio_frequency, ratio_area),
        "T_0m1": transfer(0.0, -1.0, ratio_frequency, ratio_area),
        "T_1m1": transfer(1.0, -1.0, ratio_frequency, ratio_area),
        "T_2m1": transfer(2.0, -1.0, ratio_frequency, ratio_area),
    }
    check_true(len({round(value, 14) for value in named.values()}) == len(named))

    p_probe, q_probe = 1.25, -0.75
    check_close(math.log(transfer(p_probe, q_probe, math.e, 1.0)), p_probe)
    check_close(math.log(transfer(p_probe, q_probe, 1.0, math.e)), q_probe)
    check_close(
        math.log(transfer(p_probe, q_probe, math.exp(0.37), math.exp(-0.29))),
        p_probe * 0.37 + q_probe * -0.29,
    )

    nonlinear_left = math.exp((0.8 + -0.3) ** 2 + (0.2 + 0.4))
    nonlinear_right = math.exp(0.8**2 + 0.2) * math.exp((-0.3) ** 2 + 0.4)
    check_true(relative_error(nonlinear_left, nonlinear_right) > 1.0e-4)

    epsilons = [1.0e-2, 1.0e-4, 1.0e-6, 1.0e-8]
    positive_limits = [transfer(0.0, 1.0, 1.3, eps) for eps in epsilons]
    zero_limits = [transfer(0.0, 0.0, 1.3, eps) for eps in epsilons]
    negative_limits = [transfer(0.0, -1.0, 1.3, eps) for eps in epsilons]
    check_true(all(b < a for a, b in zip(positive_limits, positive_limits[1:])))
    check_true(all(value == 1.0 for value in zero_limits))
    check_true(all(b > a for a, b in zip(negative_limits, negative_limits[1:])))
    check_close(positive_limits[-1] * negative_limits[-1], 1.0)

    t_probe = transfer(0.4, -0.6, 1.8, 0.7)
    source_a, source_b = 1.0, 7.0
    check_true(t_probe * source_a != t_probe * source_b)

    selected = (
        "B__CONTINUOUS_LOCAL_MULTIPLICATIVE_TRANSFERS_FORM_A_NONUNIQUE_CHARACTER_FAMILY"
    )
    result = {
        "all_passed": True,
        "checks_passed": checks,
        "checks_total": checks,
        "selected_primary_alternative": selected,
        "selected_secondary_alternatives": [
            "K1__LOG_T_IS_LINEAR_P_LOG_R_PLUS_Q_LOG_A",
            "R1__IDENTITY_AND_SEWING_IMPLY_RECIPROCAL_REVERSAL",
            "O1__COVARIANCE_TYPES_P_BUT_DOES_NOT_SELECT_IT",
            "S1__Q_MINUS_ONE_FOLLOWS_ONLY_AFTER_A_NEW_CONSERVATION_PREMISE",
            "Z1__METRIC_FREQUENCY_EXISTS_BUT_CARRIED_FREQUENCY_WEIGHT_IS_OPEN",
            "N1__HOMOGENEOUS_TRANSFER_PRESERVES_ZERO_AND_NEEDS_SOURCE_DATA",
            "E1__ENDPOINT_COBOUNDARIES_WIDEN_THE_CANDIDATE_CLASS",
            "C1__POSITIVE_RATIO_TRANSFER_IS_REGULAR_STRATUM_ONLY",
            "L1__PER_LABEL_ONLY_WITH_NO_METRIC_WEIGHT_OR_SUM",
            "P1__OWNERSHIP_BOUNDARY_ONLY",
        ],
        "character_family": "T_(p,q)(R,A)=R^p A^q",
        "named_counterfamily": named,
        "candidate_weights_selected": False,
        "nonzero_source_selected": False,
        "sheet_conservation_derived": False,
        "caustic_extension_selected": False,
        "max_relative_error": max_error,
        "seed": SEED,
        "cases": CASES,
        "tolerance": TOL,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") == "1":
        print(rendered, end="")
    else:
        Path("DERIVATION_RESULT.json").write_text(rendered, encoding="utf-8")
        print(rendered, end="")


if __name__ == "__main__":
    main()
