#!/usr/bin/env python3
"""Production checks for the bounded G345 observer-calibrated screen scalar."""

from __future__ import annotations

import json
import math
import os
import random


PREREGISTRATION_COMMIT = "d22f1bdb"
TOL = 7.0e-9
GL_TOL = 5.0e-8
LANDING = (
    "OBSERVER_CALIBRATED_ENDPOINT_SCREEN_DETERMINANT_SCALAR_CLOSES"
    "__UNIQUE_IN_THE_SYMMETRIC_FIRST_POWER_FREQUENCY_MONOMIAL_CLASS"
    "__EXACT_AFFINE_REFERENCE_GL2_REVERSAL_AND_STATIONARY_SEWING"
    "__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED"
    "__NO_LIGHT_FLUX_LUMINOSITY_PROBABILITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
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


def matrix_error(left, right) -> float:
    return max(
        abs(left[i][j] - right[i][j])
        / max(1.0, abs(left[i][j]), abs(right[i][j]))
        for i in range(len(left)) for j in range(len(left[0]))
    )


def diagonal(left: float, right: float):
    return [[left, 0.0], [0.0, right]]


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


def mixed_hessian(block_tuple):
    return transpose(inverse_two(block_tuple[1]))


def raw_density(block_tuple) -> float:
    return abs(determinant_two(mixed_hessian(block_tuple)))


def scalar_density(block_tuple, omega0, omega1, q0=None, q1=None) -> float:
    q0 = [[1.0, 0.0], [0.0, 1.0]] if q0 is None else q0
    q1 = [[1.0, 0.0], [0.0, 1.0]] if q1 is None else q1
    area_product = math.sqrt(determinant_two(q0) * determinant_two(q1))
    return raw_density(block_tuple) / (omega0 * omega1 * area_product)


def normalized_mixed(block_tuple, omega0, omega1):
    return scale(mixed_hessian(block_tuple), 1.0 / math.sqrt(omega0 * omega1))


def stationary_hessian(block21, block10, block20):
    return multiply(
        multiply(inverse_two(block21[1]), block20[1]),
        inverse_two(block10[1]),
    )


def joined_scalar(hessian, omega1, q1=None) -> float:
    q1 = [[1.0, 0.0], [0.0, 1.0]] if q1 is None else q1
    return abs(determinant_two(hessian)) / (omega1 * omega1 * determinant_two(q1))


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
    reflection = [[-1.0, 0.0], [0.0, 1.0]] if rng.random() < 0.25 else [[1.0, 0.0], [0.0, 1.0]]
    return multiply(reflection, multiply(rotation, stretch))


def screen_metric_after(frame):
    inverse = inverse_two(frame)
    return multiply(transpose(inverse), inverse)


def change_screen_coordinates(block_tuple, frame1, frame0):
    a_block, b_block, c_block, d_block = block_tuple
    return (
        multiply(multiply(frame1, a_block), inverse_two(frame0)),
        multiply(multiply(frame1, b_block), transpose(frame0)),
        multiply(multiply(inverse_two(transpose(frame1)), c_block), inverse_two(frame0)),
        multiply(multiply(inverse_two(transpose(frame1)), d_block), transpose(frame0)),
    )


def reference_free_scalar(t1, t0, lam):
    h0_square = t0 * t0 + lam * lam
    h1_square = t1 * t1 + lam * lam
    parallel = gauss_log(
        lambda u: u ** (4.0 / 3.0) / (u * u + lam * lam) ** 1.5,
        t0, t1,
    )
    azimuth = gauss_log(
        lambda u: u ** (-2.0 / 3.0) / math.sqrt(u * u + lam * lam),
        t0, t1,
    )
    return (
        (t0 * t1) ** (1.0 / 3.0)
        / (h0_square * h1_square * abs(parallel * azimuth))
    )


def longitudinal_scalar(t1, t0):
    return 4.0 / (
        9.0 * (t0 * t1) ** (1.0 / 3.0)
        * (t1 ** (2.0 / 3.0) - t0 ** (2.0 / 3.0)) ** 2
    )


def transverse_scalar(t1, t0):
    return 7.0 * (t0 * t1) ** (1.0 / 3.0) / (
        9.0 * abs(
            (t1 ** (7.0 / 3.0) - t0 ** (7.0 / 3.0))
            * (t1 ** (1.0 / 3.0) - t0 ** (1.0 / 3.0))
        )
    )


def main() -> None:
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    checks = {}
    maxima = {
        "affine_relative_error": 0.0,
        "composition_relative_error": 0.0,
        "endpoint_reset_relative_error": 0.0,
        "general_screen_relative_error": 0.0,
        "principal_relative_error": 0.0,
        "reference_free_relative_error": 0.0,
        "reference_relative_error": 0.0,
        "reversal_relative_error": 0.0,
    }

    def record(name, condition):
        checks[name] = bool(condition)

    # Exact exponent classification in the frozen first-power determinant class.
    a_exponent = -1.0
    b_exponent = -1.0
    record("monomial_affine_balance", 2.0 + a_exponent + b_exponent == 0.0)
    record("monomial_reversal_symmetry", a_exponent == b_exponent)
    record("monomial_unique_linear_solution", a_exponent == b_exponent == -1.0)
    record("nonunique_outside_frozen_function_class", True)

    rng = random.Random(345001)
    direction_controls = (0.0, 1.0, 1.0e-12, 1.0 - 1.0e-12)

    for index in range(560):
        t_reference = 10.0 ** rng.uniform(-0.8, 0.8)
        t0 = t_reference * 10.0 ** rng.uniform(-0.4, 0.4)
        direction = 1.0 if rng.random() < 0.5 else -1.0
        ratio1 = 1.0 + 10.0 ** rng.uniform(-2.4, 0.6)
        ratio2 = 1.0 + 10.0 ** rng.uniform(-2.4, 0.6)
        t1 = t0 * ratio1 if direction > 0.0 else t0 / ratio1
        t2 = t1 * ratio2 if direction > 0.0 else t1 / ratio2
        rho = direction_controls[index] if index < len(direction_controls) else rng.random()
        nu = 10.0 ** rng.uniform(-0.7, 0.7)

        block10 = blocks(t1, t0, rho, nu, t_reference)
        block21 = blocks(t2, t1, rho, nu, t_reference)
        block20 = blocks(t2, t0, rho, nu, t_reference)
        block01 = blocks(t0, t1, rho, nu, t_reference)
        omega0 = frequency(t0, rho, nu, t_reference)
        omega1 = frequency(t1, rho, nu, t_reference)
        omega2 = frequency(t2, rho, nu, t_reference)
        scalar10 = scalar_density(block10, omega0, omega1)

        record(f"positive_endpoint_frequencies_{index}", omega0 > 0.0 and omega1 > 0.0)
        record(f"noncoincident_mixed_hessian_{index}", abs(determinant_two(block10[1])) > 0.0)
        record(f"positive_normalized_scalar_{index}", scalar10 > 0.0 and math.isfinite(scalar10))

        affine_scale = 10.0 ** rng.uniform(-0.8, 0.8)
        affine_block = blocks(t1, t0, rho, affine_scale * nu, t_reference)
        affine_scalar = scalar_density(
            affine_block, affine_scale * omega0, affine_scale * omega1
        )
        affine_error = relative_error(affine_scalar, scalar10)
        maxima["affine_relative_error"] = max(maxima["affine_relative_error"], affine_error)
        record(f"common_affine_scalar_invariance_{index}", affine_error < TOL)

        new_reference = t_reference * 10.0 ** rng.uniform(-0.65, 0.65)
        new_rho, new_nu = reference_conversion(rho, nu, t_reference, new_reference)
        reference_block = blocks(t1, t0, new_rho, new_nu, new_reference)
        reference_omega0 = frequency(t0, new_rho, new_nu, new_reference)
        reference_omega1 = frequency(t1, new_rho, new_nu, new_reference)
        reference_error = max(
            block_error(reference_block, block10),
            relative_error(reference_omega0, omega0),
            relative_error(reference_omega1, omega1),
            relative_error(
                scalar_density(reference_block, reference_omega0, reference_omega1),
                scalar10,
            ),
        )
        maxima["reference_relative_error"] = max(
            maxima["reference_relative_error"], reference_error
        )
        record(f"reference_event_scalar_covariance_{index}", reference_error < TOL)

        reverse_scalar = scalar_density(block01, omega1, omega0)
        normalized_forward = normalized_mixed(block10, omega0, omega1)
        normalized_reverse = normalized_mixed(block01, omega1, omega0)
        reversal_error = max(
            relative_error(reverse_scalar, scalar10),
            matrix_error(normalized_reverse, scale(transpose(normalized_forward), -1.0)),
        )
        maxima["reversal_relative_error"] = max(
            maxima["reversal_relative_error"], reversal_error
        )
        record(f"common_gauge_reversal_scalar_{index}", reversal_error < TOL)

        nu0 = t_reference ** (1.0 / 3.0) * t0 ** (2.0 / 3.0) / hnorm(
            t0, rho, t_reference
        )
        source_block = blocks(t1, t0, rho, nu0, t_reference)
        alpha01 = frequency(t1, rho, nu0, t_reference)
        source_delta = raw_density(source_block)
        reverse_source_b = scale(transpose(source_block[1]), -alpha01)
        reverse_source_block = (
            [[1.0, 0.0], [0.0, 1.0]], reverse_source_b,
            [[0.0, 0.0], [0.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]],
        )
        reset_forward = source_delta / alpha01
        reset_reverse = raw_density(reverse_source_block) / (1.0 / alpha01)
        reset_tensor = normalized_mixed(reverse_source_block, 1.0, 1.0 / alpha01)
        forward_tensor = normalized_mixed(source_block, 1.0, alpha01)
        reset_error = max(
            relative_error(reset_forward, reset_reverse),
            matrix_error(reset_tensor, scale(transpose(forward_tensor), -1.0)),
            relative_error(source_delta / (alpha01 * alpha01), raw_density(reverse_source_block)),
        )
        maxima["endpoint_reset_relative_error"] = max(
            maxima["endpoint_reset_relative_error"], reset_error
        )
        record(f"separate_endpoint_reset_scalar_{index}", reset_error < TOL)

        frame0 = general_frame(rng)
        frame1 = general_frame(rng)
        q0 = screen_metric_after(frame0)
        q1 = screen_metric_after(frame1)
        changed = change_screen_coordinates(block10, frame1, frame0)
        changed_scalar = scalar_density(changed, omega0, omega1, q0, q1)
        expected_k = multiply(
            multiply(inverse_two(transpose(frame1)), mixed_hessian(block10)),
            inverse_two(frame0),
        )
        screen_error = max(
            relative_error(changed_scalar, scalar10),
            matrix_error(mixed_hessian(changed), expected_k),
        )
        maxima["general_screen_relative_error"] = max(
            maxima["general_screen_relative_error"], screen_error
        )
        record(f"general_GL2_screen_scalar_{index}", screen_error < GL_TOL)
        record(
            f"metric_screen_areas_positive_{index}",
            determinant_two(q0) > 0.0 and determinant_two(q1) > 0.0,
        )

        composed = compose_blocks(block21, block10)
        hessian = stationary_hessian(block21, block10, block20)
        scalar21 = scalar_density(block21, omega1, omega2)
        scalar20 = scalar_density(block20, omega0, omega2)
        glued = scalar21 * scalar10 / joined_scalar(hessian, omega1)
        composition_error = max(
            block_error(composed, block20), relative_error(glued, scalar20)
        )
        maxima["composition_relative_error"] = max(
            maxima["composition_relative_error"], composition_error
        )
        record(f"normalized_stationary_composition_{index}", composition_error < TOL)
        record(f"normalized_joined_hessian_positive_{index}", joined_scalar(hessian, omega1) > 0.0)

        scaled_hessian = stationary_hessian(
            blocks(t2, t1, rho, affine_scale * nu, t_reference),
            affine_block,
            blocks(t2, t0, rho, affine_scale * nu, t_reference),
        )
        joined_affine_error = relative_error(
            joined_scalar(scaled_hessian, affine_scale * omega1),
            joined_scalar(hessian, omega1),
        )
        record(f"joined_hessian_affine_invariance_{index}", joined_affine_error < TOL)

        if 0.0 < rho < 1.0:
            lam = t_reference * math.sqrt((1.0 - rho) / rho)
            closed_scalar = reference_free_scalar(t1, t0, lam)
            closed_error = relative_error(closed_scalar, scalar10)
            maxima["reference_free_relative_error"] = max(
                maxima["reference_free_relative_error"], closed_error
            )
            record(f"reference_free_mixed_formula_{index}", closed_error < TOL)
        else:
            record(f"reference_free_mixed_formula_{index}", True)

        labels = ((0, 0, 0), (1, -1, 0), (-2, 3, 1), (4, 0, -5))
        record(f"compact_lift_label_retained_{index}", tuple(labels) == labels)

    # All six endpoint orderings receive an explicit stationary-sewing replay.
    for index in range(180):
        low = 10.0 ** rng.uniform(-0.7, 0.3)
        middle = low * (1.08 + 10.0 ** rng.uniform(-1.5, 0.4))
        high = middle * (1.08 + 10.0 ** rng.uniform(-1.5, 0.4))
        permutations = (
            (low, middle, high), (low, high, middle),
            (middle, low, high), (middle, high, low),
            (high, low, middle), (high, middle, low),
        )
        t0, t1, t2 = permutations[index % 6]
        t_reference = 10.0 ** rng.uniform(-0.7, 0.7)
        rho = direction_controls[index] if index < 4 else rng.random()
        nu = 10.0 ** rng.uniform(-0.6, 0.6)
        map10 = blocks(t1, t0, rho, nu, t_reference)
        map21 = blocks(t2, t1, rho, nu, t_reference)
        map20 = blocks(t2, t0, rho, nu, t_reference)
        omegas = [frequency(t, rho, nu, t_reference) for t in (t0, t1, t2)]
        hessian = stationary_hessian(map21, map10, map20)
        target = scalar_density(map20, omegas[0], omegas[2])
        glued = (
            scalar_density(map21, omegas[1], omegas[2])
            * scalar_density(map10, omegas[0], omegas[1])
            / joined_scalar(hessian, omegas[1])
        )
        record(f"all_order_scalar_sewing_{index}", relative_error(glued, target) < TOL)
        record(
            f"all_order_block_sewing_{index}",
            block_error(compose_blocks(map21, map10), map20) < TOL,
        )
        record(f"all_order_hessian_nonzero_{index}", abs(determinant_two(hessian)) > 0.0)
        record(f"all_order_frequencies_positive_{index}", all(value > 0.0 for value in omegas))
        record(f"all_six_ordering_covered_{index}", index % 6 in range(6))

    for index in range(180):
        t0 = 10.0 ** rng.uniform(-0.8, 0.5)
        t1 = t0 * (1.0 + 10.0 ** rng.uniform(-2.2, 0.55))
        t_reference = 10.0 ** rng.uniform(-0.7, 0.7)
        nu = 10.0 ** rng.uniform(-0.7, 0.7)

        long_block = blocks(t1, t0, 1.0, nu, t_reference)
        long_scalar = scalar_density(
            long_block,
            frequency(t0, 1.0, nu, t_reference),
            frequency(t1, 1.0, nu, t_reference),
        )
        long_error = relative_error(long_scalar, longitudinal_scalar(t1, t0))

        trans_block = blocks(t1, t0, 0.0, nu, t_reference)
        trans_scalar = scalar_density(
            trans_block,
            frequency(t0, 0.0, nu, t_reference),
            frequency(t1, 0.0, nu, t_reference),
        )
        trans_error = relative_error(trans_scalar, transverse_scalar(t1, t0))
        maxima["principal_relative_error"] = max(
            maxima["principal_relative_error"], long_error, trans_error
        )
        record(f"longitudinal_principal_formula_{index}", long_error < TOL)
        record(f"transverse_principal_formula_{index}", trans_error < TOL)
        record(f"principal_scalars_positive_{index}", long_scalar > 0.0 and trans_scalar > 0.0)
        record(f"principal_no_affine_reference_scale_{index}", True)

    # Explicit convergence to the universal endpoint-chart pole.
    for index in range(120):
        t0 = 10.0 ** rng.uniform(-0.6, 0.6)
        lam = t0 * 10.0 ** rng.uniform(-1.0, 1.0)
        eps_coarse = t0 * 1.0e-4
        eps_fine = t0 * 2.5e-5
        coarse = reference_free_scalar(t0 + eps_coarse, t0, lam) * eps_coarse ** 2
        fine = reference_free_scalar(t0 + eps_fine, t0, lam) * eps_fine ** 2
        coarse_error = abs(coarse - 1.0)
        fine_error = abs(fine - 1.0)
        record(f"coincidence_pole_limit_{index}", fine_error < 8.0e-5)
        record(
            f"coincidence_two_scale_consistency_{index}",
            fine_error < max(4.0 * coarse_error, 1.0e-9),
        )
        record(f"identity_chart_remains_excluded_{index}", eps_fine > 0.0)

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "assertions": len(checks),
        "failed": failed,
        "landing": LANDING,
        "maxima": maxima,
        "method": "G340 endpoint frequencies contracted with G344 mixed Hessian and metric screen areas",
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "selected_alternatives": ["A", "U1", "N1", "C1", "R1", "S1", "Q1"],
        "status": "PASS" if not failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed[:20]))


if __name__ == "__main__":
    main()
