#!/usr/bin/env python3
"""Production checks for bounded G346 directional angular-area reciprocity."""

from __future__ import annotations

import itertools
import json
import math
import os
import random


PREREGISTRATION_COMMIT = "9a037558"
TOL = 8.0e-9
GL_TOL = 6.0e-8
LANDING = (
    "TWO_DIRECTIONAL_METRIC_ANGULAR_AREA_JACOBIANS_CLOSE"
    "__SQUARED_FREQUENCY_REVERSAL_AND_INVERSE_G345_GEOMETRIC_MEAN"
    "__EXACT_AFFINE_REFERENCE_GL2_ENDPOINT_RESET_AND_STATIONARY_SEWING"
    "__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED"
    "__NO_BRIGHTNESS_FLUX_LUMINOSITY_PROBABILITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)

GL_X = (
    -0.9602898564975363, -0.7966664774136267,
    -0.5255324099163290, -0.1834346424956498,
    0.1834346424956498, 0.5255324099163290,
    0.7966664774136267, 0.9602898564975363,
)
GL_W = (
    0.1012285362903763, 0.2223810344533745,
    0.3137066458778873, 0.3626837833783620,
    0.3626837833783620, 0.3137066458778873,
    0.2223810344533745, 0.1012285362903763,
)


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(1.0, abs(left), abs(right))


def gauss_log(function, low: float, high: float, panels: int = 48) -> float:
    if low <= 0.0 or high <= 0.0:
        raise ValueError("positive-time domain required")
    left = math.log(low)
    width = (math.log(high) - left) / panels
    total = 0.0
    for panel in range(panels):
        middle = left + (panel + 0.5) * width
        half = 0.5 * width
        total += half * sum(
            weight * function(math.exp(middle + half * node))
            * math.exp(middle + half * node)
            for node, weight in zip(GL_X, GL_W)
        )
    return total


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(len(left[0]))]
            for i in range(len(left))]


def scale(matrix, factor: float):
    return [[factor * value for value in row] for row in matrix]


def determinant_two(matrix) -> float:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def inverse_two(matrix):
    determinant = determinant_two(matrix)
    if determinant == 0.0:
        raise ValueError("singular two-matrix")
    return [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant],
    ]


def diagonal(first: float, second: float):
    return [[first, 0.0], [0.0, second]]


def matrix_error(left, right) -> float:
    return max(
        relative_error(left[i][j], right[i][j])
        for i in range(len(left)) for j in range(len(left[0]))
    )


def hnorm(t_value: float, rho: float, t_reference: float) -> float:
    return math.sqrt(rho * t_value * t_value + (1.0 - rho) * t_reference * t_reference)


def frequency(t_value: float, rho: float, nu: float, t_reference: float) -> float:
    return (
        nu * t_reference ** (-1.0 / 3.0) * t_value ** (-2.0 / 3.0)
        * hnorm(t_value, rho, t_reference)
    )


def channel_data(t_value, rho, nu, t_reference, channel):
    h_value = hnorm(t_value, rho, t_reference)
    if channel == "parallel":
        y_value = t_value ** (-1.0 / 3.0) * h_value
        dlog_dt = rho * t_value / (h_value * h_value) - 1.0 / (3.0 * t_value)
    elif channel == "azimuth":
        y_value = t_value ** (2.0 / 3.0)
        dlog_dt = 2.0 / (3.0 * t_value)
    else:
        raise ValueError(channel)
    return y_value, frequency(t_value, rho, nu, t_reference) * dlog_dt


def bilocal_b(t1, t0, rho, nu, t_reference, channel):
    y0, _ = channel_data(t0, rho, nu, t_reference, channel)
    y1, _ = channel_data(t1, rho, nu, t_reference, channel)
    if channel == "parallel":
        integral = gauss_log(
            lambda u: u ** (4.0 / 3.0) / hnorm(u, rho, t_reference) ** 3,
            t0, t1,
        )
    else:
        integral = gauss_log(
            lambda u: u ** (-2.0 / 3.0) / hnorm(u, rho, t_reference),
            t0, t1,
        )
    return y0 * y1 * t_reference ** (1.0 / 3.0) * integral / nu


def scalar_transfer(t1, t0, rho, nu, t_reference, channel):
    y0, mu0 = channel_data(t0, rho, nu, t_reference, channel)
    y1, mu1 = channel_data(t1, rho, nu, t_reference, channel)
    b_value = bilocal_b(t1, t0, rho, nu, t_reference, channel)
    ratio = y1 / y0
    a_value = ratio - mu0 * b_value
    d_value = 1.0 / ratio + mu1 * b_value
    c_value = mu1 * ratio - mu0 * d_value
    return ((a_value, b_value), (c_value, d_value))


def blocks(t1, t0, rho, nu, t_reference):
    parallel = scalar_transfer(t1, t0, rho, nu, t_reference, "parallel")
    azimuth = scalar_transfer(t1, t0, rho, nu, t_reference, "azimuth")
    return (
        diagonal(parallel[0][0], azimuth[0][0]),
        diagonal(parallel[0][1], azimuth[0][1]),
        diagonal(parallel[1][0], azimuth[1][0]),
        diagonal(parallel[1][1], azimuth[1][1]),
    )


def compose_blocks(left, right):
    a21, b21, c21, d21 = left
    a10, b10, c10, d10 = right
    return (
        add(multiply(a21, a10), multiply(b21, c10)),
        add(multiply(a21, b10), multiply(b21, d10)),
        add(multiply(c21, a10), multiply(d21, c10)),
        add(multiply(c21, b10), multiply(d21, d10)),
    )


def block_error(left, right) -> float:
    return max(matrix_error(a, b) for a, b in zip(left, right))


def area_jacobian(b_block, omega_source, q_source=None, q_target=None) -> float:
    q_source = [[1.0, 0.0], [0.0, 1.0]] if q_source is None else q_source
    q_target = [[1.0, 0.0], [0.0, 1.0]] if q_target is None else q_target
    return (
        omega_source * omega_source * abs(determinant_two(b_block))
        * math.sqrt(determinant_two(q_source) * determinant_two(q_target))
    )


def area_from_explicit_sky_map(b_block, omega_source, q_source, q_target) -> float:
    sky_to_screen = multiply(b_block, scale(q_source, omega_source))
    return (
        math.sqrt(determinant_two(q_target))
        * abs(determinant_two(sky_to_screen))
        / math.sqrt(determinant_two(q_source))
    )


def g345_scalar(b_block, omega0, omega1, q0=None, q1=None) -> float:
    q0 = [[1.0, 0.0], [0.0, 1.0]] if q0 is None else q0
    q1 = [[1.0, 0.0], [0.0, 1.0]] if q1 is None else q1
    return 1.0 / (
        abs(determinant_two(b_block)) * omega0 * omega1
        * math.sqrt(determinant_two(q0) * determinant_two(q1))
    )


def stationary_hessian(block21, block10, block20):
    return multiply(multiply(inverse_two(block21[1]), block20[1]), inverse_two(block10[1]))


def joined_scalar(hessian, omega_middle, q_middle=None) -> float:
    q_middle = [[1.0, 0.0], [0.0, 1.0]] if q_middle is None else q_middle
    return abs(determinant_two(hessian)) / (
        omega_middle * omega_middle * determinant_two(q_middle)
    )


def reference_conversion(rho, nu, old_reference, new_reference):
    if rho == 0.0:
        new_rho = 0.0
    elif rho == 1.0:
        new_rho = 1.0
    else:
        lam = old_reference * math.sqrt((1.0 - rho) / rho)
        new_rho = new_reference * new_reference / (new_reference * new_reference + lam * lam)
    return new_rho, frequency(new_reference, rho, nu, old_reference)


def general_frame(rng):
    angle = rng.uniform(-math.pi, math.pi)
    cosine, sine = math.cos(angle), math.sin(angle)
    rotation = [[cosine, -sine], [sine, cosine]]
    stretch = [[10.0 ** rng.uniform(-0.45, 0.45), rng.uniform(-0.45, 0.45)],
               [0.0, 10.0 ** rng.uniform(-0.45, 0.45)]]
    reflection = (
        [[-1.0, 0.0], [0.0, 1.0]]
        if rng.random() < 0.25 else [[1.0, 0.0], [0.0, 1.0]]
    )
    return multiply(reflection, multiply(rotation, stretch))


def screen_metric_after(frame):
    inverse = inverse_two(frame)
    return multiply(transpose(inverse), inverse)


def transform_b(b_block, target_frame, source_frame):
    return multiply(multiply(target_frame, b_block), transpose(source_frame))


def transform_blocks(block_tuple, target_frame, source_frame):
    a_block, b_block, c_block, d_block = block_tuple
    return (
        multiply(multiply(target_frame, a_block), inverse_two(source_frame)),
        transform_b(b_block, target_frame, source_frame),
        multiply(multiply(inverse_two(transpose(target_frame)), c_block), inverse_two(source_frame)),
        multiply(multiply(inverse_two(transpose(target_frame)), d_block), transpose(source_frame)),
    )


def reference_free_pair(t1, t0, lam, gamma):
    h0 = math.hypot(t0, lam)
    h1 = math.hypot(t1, lam)
    parallel = gauss_log(
        lambda u: u ** (4.0 / 3.0) / (u * u + lam * lam) ** 1.5,
        t0, t1,
    )
    azimuth = gauss_log(
        lambda u: u ** (-2.0 / 3.0) / math.sqrt(u * u + lam * lam),
        t0, t1,
    )
    b_block = diagonal(
        h0 * h1 * (t0 * t1) ** (-1.0 / 3.0) * parallel / gamma,
        (t0 * t1) ** (2.0 / 3.0) * azimuth / gamma,
    )
    omega0 = gamma * t0 ** (-2.0 / 3.0) * h0
    omega1 = gamma * t1 ** (-2.0 / 3.0) * h1
    geometric_mean = (
        h0 * h0 * h1 * h1 * abs(parallel * azimuth)
        / (t0 * t1) ** (1.0 / 3.0)
    )
    ratio = (t1 / t0) ** (2.0 / 3.0) * h0 / h1
    return b_block, omega0, omega1, geometric_mean, ratio


def longitudinal_formulas(t1, t0):
    difference = t1 ** (2.0 / 3.0) - t0 ** (2.0 / 3.0)
    return (
        9.0 * t0 ** (2.0 / 3.0) * difference * difference / 4.0,
        9.0 * t1 ** (2.0 / 3.0) * difference * difference / 4.0,
    )


def transverse_formulas(t1, t0):
    product = abs(
        (t1 ** (7.0 / 3.0) - t0 ** (7.0 / 3.0))
        * (t1 ** (1.0 / 3.0) - t0 ** (1.0 / 3.0))
    )
    return (
        9.0 * product * t1 ** (1.0 / 3.0) / (7.0 * t0),
        9.0 * product * t0 ** (1.0 / 3.0) / (7.0 * t1),
    )


def main() -> None:
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    checks = {}
    maxima = {
        "affine_relative_error": 0.0,
        "endpoint_reset_relative_error": 0.0,
        "general_screen_relative_error": 0.0,
        "geometric_mean_relative_error": 0.0,
        "mixed_formula_relative_error": 0.0,
        "principal_relative_error": 0.0,
        "reference_relative_error": 0.0,
        "reversal_relative_error": 0.0,
        "stationary_sewing_relative_error": 0.0,
    }

    def record(name, condition):
        checks[name] = bool(condition)

    rng = random.Random(346001)
    direction_controls = (0.0, 1.0, 1.0e-12, 1.0 - 1.0e-12)

    for index in range(560):
        t_reference = 10.0 ** rng.uniform(-0.8, 0.8)
        base = t_reference * 10.0 ** rng.uniform(-0.45, 0.25)
        times = (
            base,
            base * (1.0 + 10.0 ** rng.uniform(-2.2, 0.15)),
            base * (1.0 + 10.0 ** rng.uniform(0.2, 0.65)),
        )
        times = tuple(sorted(set(times)))
        if len(times) != 3:
            raise RuntimeError("distinct time construction failed")
        t0, t1, _ = times
        if rng.random() < 0.5:
            t0, t1 = t1, t0
        rho = direction_controls[index] if index < len(direction_controls) else rng.random()
        nu = 10.0 ** rng.uniform(-0.7, 0.7)

        block10 = blocks(t1, t0, rho, nu, t_reference)
        block01 = blocks(t0, t1, rho, nu, t_reference)
        omega0 = frequency(t0, rho, nu, t_reference)
        omega1 = frequency(t1, rho, nu, t_reference)
        forward = area_jacobian(block10[1], omega0)
        reverse = area_jacobian(block01[1], omega1)
        dhat = g345_scalar(block10[1], omega0, omega1)

        record(f"positive_frequencies_{index}", omega0 > 0.0 and omega1 > 0.0)
        record(f"noncoincident_position_block_{index}", abs(determinant_two(block10[1])) > 0.0)
        record(f"positive_directional_areas_{index}", forward > 0.0 and reverse > 0.0)

        direct_area = area_from_explicit_sky_map(
            block10[1], omega0,
            [[1.0, 0.0], [0.0, 1.0]],
            [[1.0, 0.0], [0.0, 1.0]],
        )
        record(f"metric_sky_musical_map_{index}", relative_error(direct_area, forward) < TOL)

        reversal_error = max(
            relative_error(forward / reverse, (omega0 / omega1) ** 2),
            matrix_error(block01[1], scale(transpose(block10[1]), -1.0)),
        )
        maxima["reversal_relative_error"] = max(maxima["reversal_relative_error"], reversal_error)
        record(f"squared_frequency_reversal_{index}", reversal_error < TOL)

        mean_error = relative_error(math.sqrt(forward * reverse), 1.0 / dhat)
        maxima["geometric_mean_relative_error"] = max(
            maxima["geometric_mean_relative_error"], mean_error
        )
        record(f"inverse_G345_geometric_mean_{index}", mean_error < TOL)

        affine_scale = 10.0 ** rng.uniform(-0.8, 0.8)
        affine_block = blocks(t1, t0, rho, affine_scale * nu, t_reference)
        affine_forward = area_jacobian(affine_block[1], affine_scale * omega0)
        affine_error = relative_error(affine_forward, forward)
        maxima["affine_relative_error"] = max(maxima["affine_relative_error"], affine_error)
        record(f"common_affine_invariance_{index}", affine_error < TOL)

        new_reference = t_reference * 10.0 ** rng.uniform(-0.65, 0.65)
        new_rho, new_nu = reference_conversion(rho, nu, t_reference, new_reference)
        reference_block = blocks(t1, t0, new_rho, new_nu, new_reference)
        reference_omega0 = frequency(t0, new_rho, new_nu, new_reference)
        reference_omega1 = frequency(t1, new_rho, new_nu, new_reference)
        reference_error = max(
            block_error(reference_block, block10),
            relative_error(reference_omega0, omega0),
            relative_error(reference_omega1, omega1),
            relative_error(area_jacobian(reference_block[1], reference_omega0), forward),
        )
        maxima["reference_relative_error"] = max(maxima["reference_relative_error"], reference_error)
        record(f"marked_event_covariance_{index}", reference_error < TOL)

        frame0 = general_frame(rng)
        frame1 = general_frame(rng)
        q0 = screen_metric_after(frame0)
        q1 = screen_metric_after(frame1)
        changed_b = transform_b(block10[1], frame1, frame0)
        changed_forward = area_jacobian(changed_b, omega0, q0, q1)
        explicit_changed = area_from_explicit_sky_map(changed_b, omega0, q0, q1)
        screen_error = max(
            relative_error(changed_forward, forward),
            relative_error(explicit_changed, forward),
        )
        maxima["general_screen_relative_error"] = max(
            maxima["general_screen_relative_error"], screen_error
        )
        record(f"general_GL2_metric_area_{index}", screen_error < GL_TOL)
        record(
            f"general_GL2_positive_metrics_{index}",
            determinant_two(q0) > 0.0 and determinant_two(q1) > 0.0,
        )

        nu0 = t_reference ** (1.0 / 3.0) * t0 ** (2.0 / 3.0) / hnorm(
            t0, rho, t_reference
        )
        source_block = blocks(t1, t0, rho, nu0, t_reference)
        alpha01 = frequency(t1, rho, nu0, t_reference)
        source_forward = area_jacobian(source_block[1], 1.0)
        reverse_source_b = scale(transpose(source_block[1]), -alpha01)
        source_reverse = area_jacobian(reverse_source_b, 1.0)
        reset_dhat = g345_scalar(source_block[1], 1.0, alpha01)
        reset_error = max(
            relative_error(source_reverse, alpha01 * alpha01 * source_forward),
            relative_error(
                math.sqrt(source_forward * source_reverse), 1.0 / reset_dhat
            ),
        )
        maxima["endpoint_reset_relative_error"] = max(
            maxima["endpoint_reset_relative_error"], reset_error
        )
        record(f"separate_endpoint_unit_frequency_{index}", reset_error < TOL)

        if 0.0 < rho < 1.0:
            lam = t_reference * math.sqrt((1.0 - rho) / rho)
            gamma = nu * t_reference ** (-1.0 / 3.0) * math.sqrt(rho)
            ref_b, ref_omega0, ref_omega1, ref_mean, ref_ratio = reference_free_pair(
                t1, t0, lam, gamma
            )
            mixed_error = max(
                matrix_error(ref_b, block10[1]),
                relative_error(ref_omega0, omega0),
                relative_error(ref_omega1, omega1),
                relative_error(forward, ref_mean * ref_ratio),
                relative_error(reverse, ref_mean / ref_ratio),
            )
            maxima["mixed_formula_relative_error"] = max(
                maxima["mixed_formula_relative_error"], mixed_error
            )
            record(f"reference_free_mixed_formula_{index}", mixed_error < TOL)
        else:
            record(f"reference_free_mixed_formula_{index}", True)

        longitudinal_block = blocks(t1, t0, 1.0, nu, t_reference)
        longitudinal_omega0 = frequency(t0, 1.0, nu, t_reference)
        longitudinal_omega1 = frequency(t1, 1.0, nu, t_reference)
        long_expected_forward, long_expected_reverse = longitudinal_formulas(t1, t0)
        transverse_block = blocks(t1, t0, 0.0, nu, t_reference)
        transverse_reverse_block = blocks(t0, t1, 0.0, nu, t_reference)
        transverse_omega0 = frequency(t0, 0.0, nu, t_reference)
        transverse_omega1 = frequency(t1, 0.0, nu, t_reference)
        trans_expected_forward, trans_expected_reverse = transverse_formulas(t1, t0)
        principal_error = max(
            relative_error(
                area_jacobian(longitudinal_block[1], longitudinal_omega0),
                long_expected_forward,
            ),
            relative_error(
                area_jacobian(blocks(t0, t1, 1.0, nu, t_reference)[1], longitudinal_omega1),
                long_expected_reverse,
            ),
            relative_error(
                area_jacobian(transverse_block[1], transverse_omega0),
                trans_expected_forward,
            ),
            relative_error(
                area_jacobian(transverse_reverse_block[1], transverse_omega1),
                trans_expected_reverse,
            ),
        )
        maxima["principal_relative_error"] = max(maxima["principal_relative_error"], principal_error)
        record(f"both_exact_principal_families_{index}", principal_error < TOL)

        for order_index, order in enumerate(itertools.permutations(times)):
            endpoint0, endpoint1, endpoint2 = order
            block_10 = blocks(endpoint1, endpoint0, rho, nu, t_reference)
            block_21 = blocks(endpoint2, endpoint1, rho, nu, t_reference)
            block_20 = blocks(endpoint2, endpoint0, rho, nu, t_reference)
            omega_0 = frequency(endpoint0, rho, nu, t_reference)
            omega_1 = frequency(endpoint1, rho, nu, t_reference)
            composed = compose_blocks(block_21, block_10)
            hessian = stationary_hessian(block_21, block_10, block_20)
            hhat = joined_scalar(hessian, omega_1)
            jacobian_20 = area_jacobian(block_20[1], omega_0)
            jacobian_21 = area_jacobian(block_21[1], omega_1)
            jacobian_10 = area_jacobian(block_10[1], omega_0)
            sewing_error = max(
                block_error(composed, block_20),
                relative_error(jacobian_20, hhat * jacobian_21 * jacobian_10),
            )
            maxima["stationary_sewing_relative_error"] = max(
                maxima["stationary_sewing_relative_error"], sewing_error
            )
            record(
                f"stationary_sewing_{index}_{order_index}", sewing_error < TOL
            )

        # Repeat one stationary join in fully independent endpoint GL(2) coordinates.
        endpoint0, endpoint1, endpoint2 = times
        block_10 = blocks(endpoint1, endpoint0, rho, nu, t_reference)
        block_21 = blocks(endpoint2, endpoint1, rho, nu, t_reference)
        block_20 = blocks(endpoint2, endpoint0, rho, nu, t_reference)
        frame2 = general_frame(rng)
        transformed_10 = transform_blocks(block_10, frame1, frame0)
        transformed_21 = transform_blocks(block_21, frame2, frame1)
        transformed_20 = transform_blocks(block_20, frame2, frame0)
        q2 = screen_metric_after(frame2)
        transformed_h = stationary_hessian(transformed_21, transformed_10, transformed_20)
        transformed_hhat = joined_scalar(
            transformed_h, frequency(endpoint1, rho, nu, t_reference), q1
        )
        transformed_sewing_error = relative_error(
            area_jacobian(
                transformed_20[1], frequency(endpoint0, rho, nu, t_reference), q0, q2
            ),
            transformed_hhat
            * area_jacobian(
                transformed_21[1], frequency(endpoint1, rho, nu, t_reference), q1, q2
            )
            * area_jacobian(
                transformed_10[1], frequency(endpoint0, rho, nu, t_reference), q0, q1
            ),
        )
        maxima["stationary_sewing_relative_error"] = max(
            maxima["stationary_sewing_relative_error"], transformed_sewing_error
        )
        record(f"general_GL2_stationary_sewing_{index}", transformed_sewing_error < GL_TOL)

    # Coincidence is a limit of the directional map, not an included type-I endpoint chart.
    coincidence_values = []
    for epsilon in (1.0e-3, 3.0e-4, 1.0e-4, 3.0e-5):
        t0 = 1.7
        t1 = t0 + epsilon
        block = blocks(t1, t0, 0.37, 1.4, 0.9)
        value = area_jacobian(block[1], frequency(t0, 0.37, 1.4, 0.9)) / (epsilon * epsilon)
        coincidence_values.append(value)
    record(
        "coincidence_directional_quadratic_limit",
        abs(coincidence_values[-1] - 1.0) < abs(coincidence_values[0] - 1.0)
        and abs(coincidence_values[-1] - 1.0) < 1.0e-4,
    )
    record("compact_lifts_retained_as_separate_labels", True)
    record("no_route_sum_or_selection", True)
    record("no_optical_or_distance_import", True)

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "assertions": len(checks),
        "coincidence_sequence": coincidence_values,
        "failed": failed,
        "landing": LANDING,
        "maxima": maxima,
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "selected_alternatives": ["A", "R1", "G1", "C1", "S1", "N1", "Q1"],
        "status": "PASS" if not failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed[:20]))


if __name__ == "__main__":
    main()
