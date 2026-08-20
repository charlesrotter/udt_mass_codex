#!/usr/bin/env python3
"""Independent standard-library replay for G191.

This module does not import the production derivation and does not read its output artifact.
"""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path


SEED = 19120260820
PAIR_TRIALS = 20000
JACOBI_TRIALS = 256
RK4_STEPS = 800
TOLERANCE = 2.0e-9


def matmul(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def determinant(matrix):
    work = [row[:] for row in matrix]
    value = 1.0
    for pivot in range(len(work)):
        choice = max(range(pivot, len(work)), key=lambda row: abs(work[row][pivot]))
        if choice != pivot:
            work[pivot], work[choice] = work[choice], work[pivot]
            value *= -1.0
        diagonal = work[pivot][pivot]
        if abs(diagonal) < 1.0e-300:
            return 0.0
        value *= diagonal
        for row in range(pivot + 1, len(work)):
            ratio = work[row][pivot] / diagonal
            for col in range(pivot + 1, len(work)):
                work[row][col] -= ratio * work[pivot][col]
    return value


def coframe(H, mu, eta, x, y):
    a = math.exp(H * eta)
    mixing = mu * (x + y) / math.sqrt(2.0)
    return [
        [a, 0.0, 0.0, 0.0],
        [0.0, a, 0.0, 0.0],
        [a * mixing, a * mixing, a, 0.0],
        [a * mixing, a * mixing, 0.0, a],
    ]


def metric_from_coframe(frame):
    eta4 = [[-1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    return matmul(transpose(frame), matmul(eta4, frame))


def exact_response(H, mu, endpoint):
    q = 1.0 + 2.0 * H * endpoint
    root = math.sqrt(q)
    logq = math.log1p(2.0 * H * endpoint)
    symmetric = root * math.sinh(math.sqrt(2.0) * mu * logq / H) / (2.0 * math.sqrt(2.0) * mu)
    antisymmetric = root * logq / (2.0 * H)
    diagonal = 0.5 * (symmetric + antisymmetric)
    cross = 0.5 * (symmetric - antisymmetric)
    return 1.0 / root, [diagonal, cross, cross, diagonal], symmetric * antisymmetric


def rhs(H, mu, parameter, state):
    q = 1.0 + 2.0 * H * parameter
    diagonal_tide = (H * H - 4.0 * mu * mu) / (q * q)
    cross_tide = -4.0 * mu * mu / (q * q)
    zfreq = state[0]
    d = state[1:5]
    velocity = state[5:9]
    acceleration = [
        -(diagonal_tide * d[0] + cross_tide * d[2]),
        -(diagonal_tide * d[1] + cross_tide * d[3]),
        -(cross_tide * d[0] + diagonal_tide * d[2]),
        -(cross_tide * d[1] + diagonal_tide * d[3]),
    ]
    return [-H * zfreq**3] + velocity + acceleration


def add_scaled(state, slope, scale):
    return [value + scale * change for value, change in zip(state, slope)]


def rk4(H, mu, endpoint):
    step = endpoint / RK4_STEPS
    state = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0]
    parameter = 0.0
    for _ in range(RK4_STEPS):
        k1 = rhs(H, mu, parameter, state)
        k2 = rhs(H, mu, parameter + step / 2.0, add_scaled(state, k1, step / 2.0))
        k3 = rhs(H, mu, parameter + step / 2.0, add_scaled(state, k2, step / 2.0))
        k4 = rhs(H, mu, parameter + step, add_scaled(state, k3, step))
        state = [
            value + step * (one + 2.0 * two + 2.0 * three + four) / 6.0
            for value, one, two, three, four in zip(state, k1, k2, k3, k4)
        ]
        parameter += step
    return state


def main():
    rng = random.Random(SEED)
    assertions = 0
    maximum_metric_error = 0.0
    maximum_frequency_error = 0.0
    maximum_jacobi_error = 0.0

    for _ in range(PAIR_TRIALS):
        H = rng.uniform(0.05, 1.5)
        mu = rng.uniform(0.02, 1.4)
        eta = rng.uniform(-0.5, 1.2)
        x = rng.uniform(-1.0, 1.0)
        y = rng.uniform(-1.0, 1.0)
        frame = coframe(H, mu, eta, x, y)
        metric = metric_from_coframe(frame)
        a = math.exp(H * eta)
        frame_error = abs(determinant(frame) - a**4)
        metric_error = abs(determinant(metric) + a**8)
        maximum_metric_error = max(maximum_metric_error, frame_error, metric_error)
        assert frame_error < 5.0e-9
        assert metric_error < 5.0e-8 * max(1.0, a**8)
        assert determinant(frame) > 0.0
        assertions += 3

        central = coframe(H, mu, eta, 0.0, 0.0)
        central_metric = metric_from_coframe(central)
        expected = [-a * a, a * a, a * a, a * a]
        for row in range(4):
            for col in range(4):
                target = expected[row] if row == col else 0.0
                error = abs(central_metric[row][col] - target)
                maximum_metric_error = max(maximum_metric_error, error)
                assert error < 2.0e-12 * max(1.0, a * a)
                assertions += 1

    for _ in range(JACOBI_TRIALS):
        H = rng.uniform(0.15, 1.5)
        mu = rng.uniform(0.03, 1.2)
        endpoint = rng.uniform(0.05, 2.0)
        exact_z, exact_d, exact_det = exact_response(H, mu, endpoint)
        numeric = rk4(H, mu, endpoint)
        frequency_error = abs(numeric[0] - exact_z)
        jacobi_errors = [abs(numeric[index + 1] - exact_d[index]) for index in range(4)]
        maximum_frequency_error = max(maximum_frequency_error, frequency_error)
        maximum_jacobi_error = max(maximum_jacobi_error, *jacobi_errors)
        assert frequency_error < TOLERANCE
        assert max(jacobi_errors) < TOLERANCE
        assert exact_z < 1.0
        assert exact_d[1] > 0.0
        assert exact_det > 0.0
        assert abs(numeric[2] - numeric[3]) < TOLERANCE
        assert abs(numeric[1] - numeric[4]) < TOLERANCE
        assertions += 10

    # Independent exact limit checks.
    for _ in range(1024):
        H = rng.uniform(0.1, 1.5)
        mu = rng.uniform(0.02, 1.2)
        endpoint = rng.uniform(0.02, 1.5)
        q = 1.0 + 2.0 * H * endpoint
        g190 = math.sqrt(q) * math.log(q) / (2.0 * H)
        zfreq, d_mu_small, _ = exact_response(H, 1.0e-8, endpoint)
        assert abs(d_mu_small[0] - g190) < 2.0e-8
        assert abs(d_mu_small[1]) < 2.0e-8
        h_zero_symmetric = math.sinh(2.0 * math.sqrt(2.0) * mu * endpoint) / (2.0 * math.sqrt(2.0) * mu)
        _, d_h_small, _ = exact_response(1.0e-10, mu, endpoint)
        assert abs(d_h_small[0] - 0.5 * (h_zero_symmetric + endpoint)) < 2.0e-7
        assert abs(d_h_small[1] - 0.5 * (h_zero_symmetric - endpoint)) < 2.0e-7
        assert zfreq < 1.0
        assertions += 5

    result = {
        "status": "PASS",
        "seed": SEED,
        "imports_production_module": False,
        "reads_production_artifact": False,
        "pair_trials": PAIR_TRIALS,
        "jacobi_trials": JACOBI_TRIALS,
        "rk4_steps_per_trial": RK4_STEPS,
        "assertions": assertions,
        "registered_tolerance": TOLERANCE,
        "maximum_metric_error": maximum_metric_error,
        "maximum_frequency_error": maximum_frequency_error,
        "maximum_jacobi_error": maximum_jacobi_error,
    }
    if os.environ.get("G191_NO_WRITE") != "1":
        output = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
