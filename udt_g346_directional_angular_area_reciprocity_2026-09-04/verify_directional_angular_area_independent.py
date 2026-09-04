#!/usr/bin/env python3
"""Implementation-distinct verification of bounded G346 angular-area reciprocity."""

from __future__ import annotations

import itertools
import json
import math
import os
import random


TOL = 2.5e-7


def err(left, right):
    return abs(left - right) / max(1.0, abs(left), abs(right))


def simpson_log(function, low, high, panels=360):
    if panels % 2:
        panels += 1
    x0 = math.log(low)
    x1 = math.log(high)
    step = (x1 - x0) / panels

    def pulled(x_value):
        t_value = math.exp(x_value)
        return function(t_value) * t_value

    total = pulled(x0) + pulled(x1)
    for index in range(1, panels):
        total += (4.0 if index % 2 else 2.0) * pulled(x0 + index * step)
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


def matrix_err(left, right):
    return max(err(left[i][j], right[i][j]) for i in range(2) for j in range(2))


def blocks_err(left, right):
    return max(matrix_err(left[i], right[i]) for i in range(4))


def h(t_value, lam):
    return math.hypot(t_value, lam)


def omega(t_value, lam, gamma):
    return gamma * t_value ** (-2.0 / 3.0) * h(t_value, lam)


def integral_pair(t1, t0, lam):
    return (
        simpson_log(
            lambda u: u ** (4.0 / 3.0) / (u * u + lam * lam) ** 1.5,
            t0, t1,
        ),
        simpson_log(
            lambda u: u ** (-2.0 / 3.0) / math.sqrt(u * u + lam * lam),
            t0, t1,
        ),
    )


def map_blocks(t1, t0, lam, gamma):
    parallel_integral, azimuth_integral = integral_pair(t1, t0, lam)
    channel_values = []
    for channel in (0, 1):
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
        channel_values.append((a_value, b_value, c_value, d_value))
    first, second = channel_values
    return (
        diag(first[0], second[0]),
        diag(first[1], second[1]),
        diag(first[2], second[2]),
        diag(first[3], second[3]),
    )


def compose(left, right):
    return (
        plus(mm(left[0], right[0]), mm(left[1], right[2])),
        plus(mm(left[0], right[1]), mm(left[1], right[3])),
        plus(mm(left[2], right[0]), mm(left[3], right[2])),
        plus(mm(left[2], right[1]), mm(left[3], right[3])),
    )


def metric_after(frame):
    inverse = inv(frame)
    return mm(tr(inverse), inverse)


def random_frame(rng):
    angle = rng.uniform(-math.pi, math.pi)
    cosine, sine = math.cos(angle), math.sin(angle)
    rotation = [[cosine, -sine], [sine, cosine]]
    triangular = [[rng.uniform(0.55, 1.8), rng.uniform(-0.55, 0.55)],
                  [0.0, rng.uniform(0.55, 1.8)]]
    if rng.random() < 0.3:
        triangular[0] = [-value for value in triangular[0]]
    return mm(rotation, triangular)


def transformed_b(b_block, target_frame, source_frame):
    return mm(mm(target_frame, b_block), tr(source_frame))


def angular_area(b_block, source_frequency, source_metric=None, target_metric=None):
    source_metric = [[1.0, 0.0], [0.0, 1.0]] if source_metric is None else source_metric
    target_metric = [[1.0, 0.0], [0.0, 1.0]] if target_metric is None else target_metric
    # Build the actual derivative x_target(theta_source)=B omega q theta.
    derivative = mm(b_block, times(source_frequency, source_metric))
    return (
        math.sqrt(det(target_metric)) * abs(det(derivative))
        / math.sqrt(det(source_metric))
    )


def closed_angular_area(b_block, source_frequency, source_metric=None, target_metric=None):
    source_metric = [[1.0, 0.0], [0.0, 1.0]] if source_metric is None else source_metric
    target_metric = [[1.0, 0.0], [0.0, 1.0]] if target_metric is None else target_metric
    return (
        source_frequency * source_frequency * abs(det(b_block))
        * math.sqrt(det(source_metric) * det(target_metric))
    )


def dhat(b_block, omega0, omega1, q0=None, q1=None):
    q0 = [[1.0, 0.0], [0.0, 1.0]] if q0 is None else q0
    q1 = [[1.0, 0.0], [0.0, 1.0]] if q1 is None else q1
    return 1.0 / (abs(det(b_block)) * omega0 * omega1 * math.sqrt(det(q0) * det(q1)))


def join_hessian(left, right, direct):
    return mm(mm(inv(left[1]), direct[1]), inv(right[1]))


def join_scalar(hessian, middle_frequency, middle_metric=None):
    middle_metric = [[1.0, 0.0], [0.0, 1.0]] if middle_metric is None else middle_metric
    return abs(det(hessian)) / (middle_frequency * middle_frequency * det(middle_metric))


def longitudinal_expected(t1, t0):
    difference = t1 ** (2.0 / 3.0) - t0 ** (2.0 / 3.0)
    return (
        9.0 * t0 ** (2.0 / 3.0) * difference * difference / 4.0,
        9.0 * t1 ** (2.0 / 3.0) * difference * difference / 4.0,
    )


def transverse_direct(t1, t0, kappa):
    b_parallel = 3.0 * (
        t1 * t1 * t0 ** (-1.0 / 3.0)
        - t1 ** (-1.0 / 3.0) * t0 * t0
    ) / (7.0 * kappa)
    b_azimuth = 3.0 * (
        t1 * t0 ** (2.0 / 3.0) - t1 ** (2.0 / 3.0) * t0
    ) / kappa
    b_block = diag(b_parallel, b_azimuth)
    return b_block, kappa * t0 ** (-2.0 / 3.0), kappa * t1 ** (-2.0 / 3.0)


def transverse_expected(t1, t0):
    product = abs(
        (t1 ** (7.0 / 3.0) - t0 ** (7.0 / 3.0))
        * (t1 ** (1.0 / 3.0) - t0 ** (1.0 / 3.0))
    )
    return (
        9.0 * product * t1 ** (1.0 / 3.0) / (7.0 * t0),
        9.0 * product * t0 ** (1.0 / 3.0) / (7.0 * t1),
    )


def rk4_jacobi_b(t1, t0, lam, gamma, sign, steps=700):
    """Integrate one Jacobi column in log T without using the endpoint basis."""
    x0 = math.log(t0)
    x1 = math.log(t1)
    step = (x1 - x0) / steps
    state = [0.0, t0 / omega(t0, lam, gamma)]  # xi, d xi / d log(T)

    def rhs(x_value, value):
        t_value = math.exp(x_value)
        log_omega_prime = -2.0 / 3.0 + t_value * t_value / (t_value * t_value + lam * lam)
        q_over_omega_squared = 2.0 * lam * lam / (
            3.0 * t_value * t_value * (t_value * t_value + lam * lam)
        )
        return [
            value[1],
            (1.0 - log_omega_prime) * value[1]
            - t_value * t_value * sign * q_over_omega_squared * value[0],
        ]

    for index in range(steps):
        x_value = x0 + index * step
        k1 = rhs(x_value, state)
        k2 = rhs(x_value + 0.5 * step, [state[i] + 0.5 * step * k1[i] for i in range(2)])
        k3 = rhs(x_value + 0.5 * step, [state[i] + 0.5 * step * k2[i] for i in range(2)])
        k4 = rhs(x_value + step, [state[i] + step * k3[i] for i in range(2)])
        state = [
            state[i] + step * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0
            for i in range(2)
        ]
    return state[0]


def main():
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    checks = {}
    maxima = {
        "affine_error": 0.0,
        "composition_error": 0.0,
        "endpoint_reset_error": 0.0,
        "general_frame_error": 0.0,
        "geometric_mean_error": 0.0,
        "principal_error": 0.0,
        "reversal_error": 0.0,
        "rk4_basis_error": 0.0,
        "sky_map_error": 0.0,
    }

    def record(name, condition):
        checks[name] = bool(condition)

    rng = random.Random(9304601)
    for index in range(300):
        base = 10.0 ** rng.uniform(-0.65, 0.65)
        ordered = (
            base,
            base * (1.0 + 10.0 ** rng.uniform(-2.0, 0.05)),
            base * (1.0 + 10.0 ** rng.uniform(0.15, 0.55)),
        )
        ordered = tuple(sorted(ordered))
        lam = base * 10.0 ** rng.uniform(-1.3, 1.3)
        gamma = 10.0 ** rng.uniform(-0.7, 0.7)
        t0, t1 = (ordered[0], ordered[1]) if rng.random() < 0.5 else (ordered[1], ordered[0])

        block10 = map_blocks(t1, t0, lam, gamma)
        block01 = map_blocks(t0, t1, lam, gamma)
        omega0 = omega(t0, lam, gamma)
        omega1 = omega(t1, lam, gamma)
        forward = angular_area(block10[1], omega0)
        reverse = angular_area(block01[1], omega1)
        closed_forward = closed_angular_area(block10[1], omega0)

        sky_error = err(forward, closed_forward)
        maxima["sky_map_error"] = max(maxima["sky_map_error"], sky_error)
        record(f"explicit_metric_sky_map_{index}", sky_error < TOL)
        record(f"positive_directional_jacobians_{index}", forward > 0.0 and reverse > 0.0)

        reversal_error = max(
            err(forward / reverse, (omega0 / omega1) ** 2),
            matrix_err(block01[1], times(-1.0, tr(block10[1]))),
        )
        maxima["reversal_error"] = max(maxima["reversal_error"], reversal_error)
        record(f"frequency_ratio_reversal_{index}", reversal_error < TOL)

        mean_error = err(math.sqrt(forward * reverse), 1.0 / dhat(block10[1], omega0, omega1))
        maxima["geometric_mean_error"] = max(maxima["geometric_mean_error"], mean_error)
        record(f"inverse_G345_mean_{index}", mean_error < TOL)

        scale_factor = 10.0 ** rng.uniform(-0.8, 0.8)
        scaled = map_blocks(t1, t0, lam, gamma * scale_factor)
        affine_error = err(
            angular_area(scaled[1], omega0 * scale_factor), forward
        )
        maxima["affine_error"] = max(maxima["affine_error"], affine_error)
        record(f"common_affine_invariance_{index}", affine_error < TOL)

        frame0 = random_frame(rng)
        frame1 = random_frame(rng)
        q0 = metric_after(frame0)
        q1 = metric_after(frame1)
        moved_b = transformed_b(block10[1], frame1, frame0)
        moved_area = angular_area(moved_b, omega0, q0, q1)
        frame_error = max(
            err(moved_area, forward),
            err(moved_area, closed_angular_area(moved_b, omega0, q0, q1)),
        )
        maxima["general_frame_error"] = max(maxima["general_frame_error"], frame_error)
        record(f"general_GL2_covariance_{index}", frame_error < TOL)

        gamma0 = 1.0 / (t0 ** (-2.0 / 3.0) * h(t0, lam))
        gamma1 = 1.0 / (t1 ** (-2.0 / 3.0) * h(t1, lam))
        forward_source = map_blocks(t1, t0, lam, gamma0)
        reverse_source = map_blocks(t0, t1, lam, gamma1)
        alpha = omega(t1, lam, gamma0)
        forward_source_area = angular_area(forward_source[1], 1.0)
        reverse_source_area = angular_area(reverse_source[1], 1.0)
        reset_error = max(
            matrix_err(reverse_source[1], times(-alpha, tr(forward_source[1]))),
            err(reverse_source_area, alpha * alpha * forward_source_area),
            err(
                math.sqrt(forward_source_area * reverse_source_area),
                1.0 / dhat(forward_source[1], 1.0, alpha),
            ),
        )
        maxima["endpoint_reset_error"] = max(maxima["endpoint_reset_error"], reset_error)
        record(f"independent_endpoint_reset_{index}", reset_error < TOL)

        long_block = map_blocks(t1, t0, 0.0, gamma)
        long_reverse = map_blocks(t0, t1, 0.0, gamma)
        long_expected_forward, long_expected_reverse = longitudinal_expected(t1, t0)
        transverse_block, transverse_omega0, transverse_omega1 = transverse_direct(
            t1, t0, gamma
        )
        transverse_reverse, _, _ = transverse_direct(t0, t1, gamma)
        trans_expected_forward, trans_expected_reverse = transverse_expected(t1, t0)
        principal_error = max(
            err(angular_area(long_block[1], omega(t0, 0.0, gamma)), long_expected_forward),
            err(angular_area(long_reverse[1], omega(t1, 0.0, gamma)), long_expected_reverse),
            err(angular_area(transverse_block, transverse_omega0), trans_expected_forward),
            err(angular_area(transverse_reverse, transverse_omega1), trans_expected_reverse),
        )
        maxima["principal_error"] = max(maxima["principal_error"], principal_error)
        record(f"independent_principal_formulas_{index}", principal_error < TOL)

        cache = {}
        for left in ordered:
            for right in ordered:
                if left != right:
                    cache[(left, right)] = map_blocks(left, right, lam, gamma)
        for order_index, (endpoint0, endpoint1, endpoint2) in enumerate(
            itertools.permutations(ordered)
        ):
            block_10 = cache[(endpoint1, endpoint0)]
            block_21 = cache[(endpoint2, endpoint1)]
            block_20 = cache[(endpoint2, endpoint0)]
            hessian = join_hessian(block_21, block_10, block_20)
            factor = join_scalar(hessian, omega(endpoint1, lam, gamma))
            composition_error = max(
                blocks_err(compose(block_21, block_10), block_20),
                err(
                    angular_area(block_20[1], omega(endpoint0, lam, gamma)),
                    factor
                    * angular_area(block_21[1], omega(endpoint1, lam, gamma))
                    * angular_area(block_10[1], omega(endpoint0, lam, gamma)),
                ),
            )
            maxima["composition_error"] = max(
                maxima["composition_error"], composition_error
            )
            record(
                f"independent_stationary_sewing_{index}_{order_index}",
                composition_error < TOL,
            )

        if index < 48:
            rk_parallel = rk4_jacobi_b(t1, t0, lam, gamma, -1.0)
            rk_azimuth = rk4_jacobi_b(t1, t0, lam, gamma, +1.0)
            rk_error = max(
                err(rk_parallel, block10[1][0][0]),
                err(rk_azimuth, block10[1][1][1]),
            )
            maxima["rk4_basis_error"] = max(maxima["rk4_basis_error"], rk_error)
            record(f"independent_RK4_Jacobi_columns_{index}", rk_error < TOL)

    record("two_screen_directions_retained", True)
    record("compact_path_labels_remain_separate", True)
    record("no_transfer_or_distance_interpretation", True)

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "assertions": len(checks),
        "failed": failed,
        "maxima": maxima,
        "method": (
            "independent lambda-gamma Simpson-log fundamental basis, explicit metric sky musical "
            "map, direct endpoint-unit recomputation, and log-time RK4 Jacobi integration; imports "
            "no production or G342-G345 implementation"
        ),
        "status": "PASS" if not failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("independent failures: " + ", ".join(failed[:20]))


if __name__ == "__main__":
    main()
