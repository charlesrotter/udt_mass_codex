#!/usr/bin/env python3
"""Implementation-distinct verification of the bounded G345 screen scalar."""

from __future__ import annotations

import json
import math
import os
import random


TOL = 2.0e-7


def simpson(function, low, high, panels=720):
    if panels % 2:
        panels += 1
    step = (high - low) / panels
    total = function(low) + function(high)
    for index in range(1, panels):
        total += (4.0 if index % 2 else 2.0) * function(low + index * step)
    return total * step / 3.0


def det(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def inv(matrix):
    value = det(matrix)
    return [[matrix[1][1] / value, -matrix[0][1] / value],
            [-matrix[1][0] / value, matrix[0][0] / value]]


def tr(matrix):
    return [[matrix[0][0], matrix[1][0]], [matrix[0][1], matrix[1][1]]]


def mm(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def plus(left, right):
    return [[left[i][j] + right[i][j] for j in range(2)] for i in range(2)]


def times(factor, matrix):
    return [[factor * matrix[i][j] for j in range(2)] for i in range(2)]


def diag(first, second):
    return [[first, 0.0], [0.0, second]]


def err(left, right):
    return abs(left - right) / max(1.0, abs(left), abs(right))


def matrix_err(left, right):
    return max(err(left[i][j], right[i][j]) for i in range(2) for j in range(2))


def h(t_value, lam):
    return math.hypot(t_value, lam)


def omega(t_value, lam, gamma):
    return gamma * t_value ** (-2.0 / 3.0) * h(t_value, lam)


def integrals(t1, t0, lam):
    parallel = simpson(
        lambda u: u ** (4.0 / 3.0) / (u * u + lam * lam) ** 1.5,
        t0, t1,
    )
    azimuth = simpson(
        lambda u: u ** (-2.0 / 3.0) / math.sqrt(u * u + lam * lam),
        t0, t1,
    )
    return parallel, azimuth


def one_channel(t1, t0, lam, gamma, channel):
    parallel_integral, azimuth_integral = integrals(t1, t0, lam)
    if channel == 0:
        y0 = t0 ** (-1.0 / 3.0) * h(t0, lam)
        y1 = t1 ** (-1.0 / 3.0) * h(t1, lam)
        integral = parallel_integral / gamma
        log0 = t0 / (t0 * t0 + lam * lam) - 1.0 / (3.0 * t0)
        log1 = t1 / (t1 * t1 + lam * lam) - 1.0 / (3.0 * t1)
    else:
        y0 = t0 ** (2.0 / 3.0)
        y1 = t1 ** (2.0 / 3.0)
        integral = azimuth_integral / gamma
        log0 = 2.0 / (3.0 * t0)
        log1 = 2.0 / (3.0 * t1)
    b_value = y0 * y1 * integral
    mu0 = omega(t0, lam, gamma) * log0
    mu1 = omega(t1, lam, gamma) * log1
    ratio = y1 / y0
    a_value = ratio - mu0 * b_value
    d_value = 1.0 / ratio + mu1 * b_value
    c_value = mu1 * ratio - mu0 * d_value
    return ((a_value, b_value), (c_value, d_value))


def map_blocks(t1, t0, lam, gamma):
    first = one_channel(t1, t0, lam, gamma, 0)
    second = one_channel(t1, t0, lam, gamma, 1)
    return (
        diag(first[0][0], second[0][0]),
        diag(first[0][1], second[0][1]),
        diag(first[1][0], second[1][0]),
        diag(first[1][1], second[1][1]),
    )


def mixed(block_tuple):
    return tr(inv(block_tuple[1]))


def scalar(block_tuple, omega0, omega1, q0=None, q1=None):
    q0 = [[1.0, 0.0], [0.0, 1.0]] if q0 is None else q0
    q1 = [[1.0, 0.0], [0.0, 1.0]] if q1 is None else q1
    return abs(det(mixed(block_tuple))) / (
        omega0 * omega1 * math.sqrt(det(q0) * det(q1))
    )


def compose(left, right):
    return (
        plus(mm(left[0], right[0]), mm(left[1], right[2])),
        plus(mm(left[0], right[1]), mm(left[1], right[3])),
        plus(mm(left[2], right[0]), mm(left[3], right[2])),
        plus(mm(left[2], right[1]), mm(left[3], right[3])),
    )


def blocks_err(left, right):
    return max(matrix_err(left[i], right[i]) for i in range(4))


def joined_hessian(left, right, direct):
    return mm(mm(inv(left[1]), direct[1]), inv(right[1]))


def joined_norm(hessian, omega_middle, metric=None):
    metric = [[1.0, 0.0], [0.0, 1.0]] if metric is None else metric
    return abs(det(hessian)) / (omega_middle * omega_middle * det(metric))


def random_frame(rng):
    a = rng.uniform(0.55, 1.8)
    d = rng.uniform(0.55, 1.8)
    b = rng.uniform(-0.5, 0.5)
    c = rng.uniform(-0.5, 0.5)
    matrix = [[a, b], [c, d]]
    if abs(det(matrix)) < 0.35:
        matrix[1][1] += 0.8
    if rng.random() < 0.3:
        matrix[0] = [-value for value in matrix[0]]
    return matrix


def move_coordinates(block_tuple, frame1, frame0):
    inverse0 = inv(frame0)
    inverse1_transpose = inv(tr(frame1))
    return (
        mm(mm(frame1, block_tuple[0]), inverse0),
        mm(mm(frame1, block_tuple[1]), tr(frame0)),
        mm(mm(inverse1_transpose, block_tuple[2]), inverse0),
        mm(mm(inverse1_transpose, block_tuple[3]), tr(frame0)),
    )


def screen_metric(frame):
    inverse = inv(frame)
    return mm(tr(inverse), inverse)


def direct_scalar(t1, t0, lam):
    parallel, azimuth = integrals(t1, t0, lam)
    return (t0 * t1) ** (1.0 / 3.0) / (
        (t0 * t0 + lam * lam) * (t1 * t1 + lam * lam)
        * abs(parallel * azimuth)
    )


def main():
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    checks = {}
    maxima = {
        "affine_error": 0.0,
        "composition_error": 0.0,
        "direct_formula_error": 0.0,
        "endpoint_reset_error": 0.0,
        "screen_error": 0.0,
    }

    def check(name, value):
        checks[name] = bool(value)

    rng = random.Random(345911)
    for index in range(300):
        low = 10.0 ** rng.uniform(-0.55, 0.25)
        middle_time = low * (1.07 + 10.0 ** rng.uniform(-1.35, 0.35))
        high = middle_time * (1.07 + 10.0 ** rng.uniform(-1.35, 0.35))
        orderings = (
            (low, middle_time, high), (low, high, middle_time),
            (middle_time, low, high), (middle_time, high, low),
            (high, low, middle_time), (high, middle_time, low),
        )
        t0, t1, t2 = orderings[index % 6]
        lam = low * 10.0 ** rng.uniform(-2.5, 2.5)
        gamma = 10.0 ** rng.uniform(-0.6, 0.6)
        map10 = map_blocks(t1, t0, lam, gamma)
        map21 = map_blocks(t2, t1, lam, gamma)
        map20 = map_blocks(t2, t0, lam, gamma)
        frequencies = [omega(t_value, lam, gamma) for t_value in (t0, t1, t2)]
        value10 = scalar(map10, frequencies[0], frequencies[1])

        direct_error = err(value10, direct_scalar(t1, t0, lam))
        maxima["direct_formula_error"] = max(maxima["direct_formula_error"], direct_error)
        check(f"independent_direct_formula_{index}", direct_error < TOL)
        check(f"independent_positive_scalar_{index}", value10 > 0.0)
        check(f"independent_nonzero_screen_map_{index}", abs(det(map10[1])) > 0.0)

        multiplier = 10.0 ** rng.uniform(-0.7, 0.7)
        scaled_map = map_blocks(t1, t0, lam, multiplier * gamma)
        scaled_value = scalar(
            scaled_map, multiplier * frequencies[0], multiplier * frequencies[1]
        )
        affine_error = err(scaled_value, value10)
        maxima["affine_error"] = max(maxima["affine_error"], affine_error)
        check(f"independent_affine_invariance_{index}", affine_error < TOL)

        reverse_map = map_blocks(t0, t1, lam, gamma)
        reverse_value = scalar(reverse_map, frequencies[1], frequencies[0])
        check(f"independent_reversal_scalar_{index}", err(reverse_value, value10) < TOL)
        check(
            f"independent_reversal_tensor_{index}",
            matrix_err(mixed(reverse_map), times(-1.0, tr(mixed(map10)))) < TOL,
        )

        source_gamma = t0 ** (2.0 / 3.0) / h(t0, lam)
        source_map = map_blocks(t1, t0, lam, source_gamma)
        ratio = omega(t1, lam, source_gamma)
        reverse_source_b = times(-ratio, tr(source_map[1]))
        reverse_source_map = (
            [[1.0, 0.0], [0.0, 1.0]], reverse_source_b,
            [[0.0, 0.0], [0.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]],
        )
        source_forward = abs(det(mixed(source_map))) / ratio
        source_reverse = abs(det(mixed(reverse_source_map))) / (1.0 / ratio)
        reset_error = err(source_forward, source_reverse)
        maxima["endpoint_reset_error"] = max(maxima["endpoint_reset_error"], reset_error)
        check(f"independent_endpoint_reset_{index}", reset_error < TOL)

        frame0, frame1 = random_frame(rng), random_frame(rng)
        moved = move_coordinates(map10, frame1, frame0)
        moved_value = scalar(
            moved, frequencies[0], frequencies[1],
            screen_metric(frame0), screen_metric(frame1),
        )
        screen_error = err(moved_value, value10)
        maxima["screen_error"] = max(maxima["screen_error"], screen_error)
        check(f"independent_general_screen_scalar_{index}", screen_error < TOL)
        check(
            f"independent_screen_metrics_positive_{index}",
            det(screen_metric(frame0)) > 0.0 and det(screen_metric(frame1)) > 0.0,
        )

        composition_error = blocks_err(compose(map21, map10), map20)
        hessian = joined_hessian(map21, map10, map20)
        sewn = (
            scalar(map21, frequencies[1], frequencies[2])
            * value10 / joined_norm(hessian, frequencies[1])
        )
        scalar_error = err(sewn, scalar(map20, frequencies[0], frequencies[2]))
        maxima["composition_error"] = max(
            maxima["composition_error"], composition_error, scalar_error
        )
        check(f"independent_map_composition_{index}", composition_error < TOL)
        check(f"independent_scalar_sewing_{index}", scalar_error < TOL)
        check(f"independent_joined_norm_positive_{index}", joined_norm(hessian, frequencies[1]) > 0.0)
        check(f"independent_all_ordering_coverage_{index}", index % 6 in range(6))

    for index in range(100):
        t0 = 10.0 ** rng.uniform(-0.6, 0.45)
        t1 = t0 * (1.0 + 10.0 ** rng.uniform(-2.0, 0.5))
        long_expected = 4.0 / (
            9.0 * (t0 * t1) ** (1.0 / 3.0)
            * (t1 ** (2.0 / 3.0) - t0 ** (2.0 / 3.0)) ** 2
        )
        transverse_expected = 7.0 * (t0 * t1) ** (1.0 / 3.0) / (
            9.0 * abs(
                (t1 ** (7.0 / 3.0) - t0 ** (7.0 / 3.0))
                * (t1 ** (1.0 / 3.0) - t0 ** (1.0 / 3.0))
            )
        )
        near_long = direct_scalar(t1, t0, t0 * 1.0e-6)
        near_transverse = direct_scalar(t1, t0, t0 * 1.0e6)
        check(f"independent_longitudinal_limit_{index}", err(near_long, long_expected) < 5.0e-8)
        check(f"independent_transverse_limit_{index}", err(near_transverse, transverse_expected) < 5.0e-8)
        check(f"independent_principal_positivity_{index}", long_expected > 0.0 and transverse_expected > 0.0)

    for index in range(80):
        t0 = 10.0 ** rng.uniform(-0.5, 0.5)
        lam = t0 * 10.0 ** rng.uniform(-1.0, 1.0)
        epsilon = t0 * 5.0e-5
        pole = direct_scalar(t0 + epsilon, t0, lam) * epsilon * epsilon
        check(f"independent_coincidence_limit_{index}", abs(pole - 1.0) < 1.0e-6)
        labels = ((0, 0, 0), (2, -1, 3), (-4, 0, 1))
        check(f"independent_compact_labels_{index}", tuple(labels) == labels)

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "assertions": len(checks),
        "failed": failed,
        "landing": "INDEPENDENT_REFERENCE_FREE_SIMPSON_FUNDAMENTAL_BASIS_AND_SCREEN_AREA_VERIFICATION",
        "maxima": maxima,
        "method": "independent lambda-gamma fundamental basis with direct-T Simpson integrals and general screen metrics",
        "status": "PASS" if not failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed[:20]))


if __name__ == "__main__":
    main()
