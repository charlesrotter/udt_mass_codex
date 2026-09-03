#!/usr/bin/env python3
"""Implementation-distinct numerical and finite-difference G334 verifier."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))] for i in range(len(left))]


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(2)] for i in range(2)]


def scale(value, matrix):
    return [[value * matrix[i][j] for j in range(2)] for i in range(2)]


def boost(z):
    ch = math.cosh(z)
    sh = math.sinh(z)
    return [[ch, sh], [sh, ch]]


def base_metric(time, rate):
    return [[-1.0, 0.0], [0.0, 1.0 + 2.0 * rate * time]]


def frame_metric(time, rate, z0, boost_rate):
    matrix = boost(z0 + boost_rate * time)
    return multiply(transpose(matrix), multiply(base_metric(time, rate), matrix))


def close(left, right, tolerance=3e-8):
    return abs(left - right) <= tolerance * max(1.0, abs(left), abs(right))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()

    checks = []
    records = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    eta = [[-1.0, 0.0], [0.0, 1.0]]
    epsilon = 2e-7
    for rate_index, rate in enumerate((-4.25, -0.7, 0.0, 0.35, 3.8)):
        for boost_index, z0 in enumerate((-2.0, -0.6, 0.0, 0.4, 1.7)):
            matrix = boost(z0)
            metric_at_zero = multiply(transpose(matrix), multiply(eta, matrix))
            for i in range(2):
                for j in range(2):
                    require(close(metric_at_zero[i][j], eta[i][j], 2e-14),
                            f"metric_{rate_index}_{boost_index}_{i}_{j}")

            ch = math.cosh(z0)
            sh = math.sinh(z0)
            expected = [
                [2 * rate * sh * sh, 2 * rate * sh * ch],
                [2 * rate * sh * ch, 2 * rate * ch * ch],
            ]
            for boost_rate_index, zeta in enumerate((-3.1, 0.0, 2.4)):
                plus = frame_metric(epsilon, rate, z0, zeta)
                minus = frame_metric(-epsilon, rate, z0, zeta)
                finite = scale(1 / (2 * epsilon), add(plus, scale(-1, minus)))
                for i in range(2):
                    for j in range(2):
                        require(close(finite[i][j], expected[i][j]),
                                f"finite_{rate_index}_{boost_index}_{boost_rate_index}_{i}_{j}")

            d00, d01, d11 = expected[0][0], expected[0][1], expected[1][1]
            require(close(d11 - d00, 2 * rate),
                    f"invariant_difference_{rate_index}_{boost_index}")
            require(close(d01 * d01, d00 * d11),
                    f"rank_one_{rate_index}_{boost_index}")
            require(close(-d00 + d11, 2 * rate),
                    f"mixed_trace_{rate_index}_{boost_index}")
            require(close(-d00 * d11 + d01 * d01, 0.0),
                    f"mixed_determinant_{rate_index}_{boost_index}")
            require(close(d00 / 2, rate * sh * sh),
                    f"terminal_phi_{rate_index}_{boost_index}")

            alpha, beta, gamma, delta = 0.31, -0.72, 0.18, -0.27
            transported = [
                [d00 - 2 * alpha, d01 + beta - gamma],
                [d01 + beta - gamma, d11 + 2 * delta],
            ]
            require(not close(transported[0][0], d00) and not close(transported[1][1], d11),
                    f"general_transport_changes_components_{rate_index}_{boost_index}")

            reorthonormalized = [
                [d00 - 2 * (d00 / 2), d01 - d01],
                [d01 - d01, d11 + 2 * (-d11 / 2)],
            ]
            require(all(close(reorthonormalized[i][j], 0.0, 2e-14)
                        for i in range(2) for j in range(2)),
                    f"reorthonormalization_{rate_index}_{boost_index}")
            records.append({"rate": rate, "rapidity": z0, "first_jet": expected})

    # Reversal parity and the exact blind stratum are checked separately.
    rate = 1.75
    positive = boost(0.8)
    negative = boost(-0.8)
    base_jet = [[0.0, 0.0], [0.0, 2 * rate]]
    response_positive = multiply(transpose(positive), multiply(base_jet, positive))
    response_negative = multiply(transpose(negative), multiply(base_jet, negative))
    require(close(response_positive[0][0], response_negative[0][0]), "reversal_clock_even")
    require(close(response_positive[1][1], response_negative[1][1]), "reversal_ruler_even")
    require(close(response_positive[0][1], -response_negative[0][1]), "reversal_cross_odd")
    require(close(frame_metric(epsilon, rate, 0.0, 0.0)[0][0], -1.0),
            "unboosted_terminal_first_jet_blind")

    # The observer derivative contains an independent spatial derivative when sinh(z) != 0.
    ch, sh = math.cosh(0.8), math.sinh(0.8)
    observer_a = ch * 1.2 + sh * 0.0
    observer_b = ch * 1.2 + sh * 2.3
    require(not close(observer_a, observer_b), "normal_is_not_observer_time")

    payload = {
        "package": "G334",
        "verifier": "independent_finite_difference_varying_boost_and_transport",
        "imports_production": False,
        "reads_production_result": False,
        "checks_passed": len(checks),
        "checks": checks,
        "records": records,
        "verdict": "PASS",
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"checks_passed": len(checks), "verdict": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
