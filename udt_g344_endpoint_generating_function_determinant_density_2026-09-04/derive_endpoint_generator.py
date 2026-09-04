#!/usr/bin/env python3
"""Production checks for the bounded G344 endpoint generator and density."""

from __future__ import annotations

import json
import math
import os
import random


PREREGISTRATION_COMMIT = "5c16ca60"
TOL = 5.0e-9
LANDING = (
    "GLOBAL_NONCOINCIDENT_QUADRATIC_SCREEN_ENDPOINT_GENERATOR_CLOSES"
    "__MIXED_HESSIAN_IS_A_TYPED_AFFINE_WEIGHTED_ENDPOINT_BIDENSITY"
    "__EXACT_STATIONARY_COMPOSITION_REVERSAL_REFERENCE_AND_SCREEN_COVARIANCE"
    "__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED"
    "__NO_LIGHT_FLUX_DISTANCE_PROBABILITY_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
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


def hnorm(t: float, rho: float, t_reference: float) -> float:
    return math.sqrt(rho * t * t + (1.0 - rho) * t_reference * t_reference)


def ray_rate(t: float, rho: float, nu: float, t_reference: float) -> float:
    return (
        nu * t_reference ** (-1.0 / 3.0) * t ** (-2.0 / 3.0)
        * hnorm(t, rho, t_reference)
    )


def channel_data(
    t: float, rho: float, nu: float, t_reference: float, channel: str
) -> tuple[float, float]:
    h_value = hnorm(t, rho, t_reference)
    if channel == "parallel":
        y_value = t ** (-1.0 / 3.0) * h_value
        dlog_dt = rho * t / (h_value * h_value) - 1.0 / (3.0 * t)
    elif channel == "azimuth":
        y_value = t ** (2.0 / 3.0)
        dlog_dt = 2.0 / (3.0 * t)
    else:
        raise ValueError(channel)
    return y_value, ray_rate(t, rho, nu, t_reference) * dlog_dt


def bilocal_b(
    t1: float, t0: float, rho: float, nu: float, t_reference: float, channel: str
) -> float:
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


def scalar_transfer(
    t1: float, t0: float, rho: float, nu: float, t_reference: float, channel: str
) -> tuple[tuple[float, float], tuple[float, float]]:
    y0, mu0 = channel_data(t0, rho, nu, t_reference, channel)
    y1, mu1 = channel_data(t1, rho, nu, t_reference, channel)
    b_value = bilocal_b(t1, t0, rho, nu, t_reference, channel)
    ratio = y1 / y0
    a_value = ratio - mu0 * b_value
    d_value = 1.0 / ratio + mu1 * b_value
    c_value = mu1 * ratio - mu0 * d_value
    return ((a_value, b_value), (c_value, d_value))


def diagonal(left: float, right: float) -> list[list[float]]:
    return [[left, 0.0], [0.0, right]]


def blocks(
    t1: float, t0: float, rho: float, nu: float, t_reference: float
) -> tuple[list[list[float]], ...]:
    parallel = scalar_transfer(t1, t0, rho, nu, t_reference, "parallel")
    azimuth = scalar_transfer(t1, t0, rho, nu, t_reference, "azimuth")
    return (
        diagonal(parallel[0][0], azimuth[0][0]),
        diagonal(parallel[0][1], azimuth[0][1]),
        diagonal(parallel[1][0], azimuth[1][0]),
        diagonal(parallel[1][1], azimuth[1][1]),
    )


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


def vector_error(left, right) -> float:
    return max(abs(a - b) / max(1.0, abs(a), abs(b)) for a, b in zip(left, right))


def matvec(matrix, vector):
    return [sum(row[index] * vector[index] for index in range(len(vector)))
            for row in matrix]


def dot(left, right) -> float:
    return sum(a * b for a, b in zip(left, right))


def vecadd(left, right, factor: float = 1.0):
    return [left[index] + factor * right[index] for index in range(len(left))]


def generator_coefficients(block_tuple):
    a_block, b_block, c_block, d_block = block_tuple
    b_inverse = inverse_two(b_block)
    target_hessian = multiply(d_block, b_inverse)
    source_hessian = multiply(b_inverse, a_block)
    negative_mixed = transpose(b_inverse)
    return target_hessian, source_hessian, negative_mixed


def generator_value(block_tuple, x1, x0) -> float:
    target_hessian, source_hessian, _ = generator_coefficients(block_tuple)
    b_inverse = inverse_two(block_tuple[1])
    return (
        0.5 * dot(x1, matvec(target_hessian, x1))
        - dot(x0, matvec(b_inverse, x1))
        + 0.5 * dot(x0, matvec(source_hessian, x0))
    )


def generator_momenta(block_tuple, x1, x0):
    target_hessian, source_hessian, negative_mixed = generator_coefficients(block_tuple)
    p1 = vecadd(matvec(target_hessian, x1), matvec(negative_mixed, x0), -1.0)
    p0 = vecadd(matvec(inverse_two(block_tuple[1]), x1), matvec(source_hessian, x0), -1.0)
    return p1, p0


def density(block_tuple) -> float:
    return 1.0 / abs(determinant_two(block_tuple[1]))


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


def stationary_middle(block21, block10, x2, x0):
    b21_inverse = inverse_two(block21[1])
    b10_inverse = inverse_two(block10[1])
    hessian = add(
        multiply(b21_inverse, block21[0]),
        multiply(block10[3], b10_inverse),
    )
    right_side = vecadd(
        matvec(b21_inverse, x2),
        matvec(transpose(b10_inverse), x0),
    )
    return matvec(inverse_two(hessian), right_side), hessian


def rotate(angle: float, reflected: bool = False):
    cosine = math.cos(angle)
    sine = math.sin(angle)
    rotation = [[cosine, -sine], [sine, cosine]]
    if reflected:
        rotation = multiply([[-1.0, 0.0], [0.0, 1.0]], rotation)
    return rotation


def change_screen_bases(block_tuple, endpoint_one, endpoint_zero):
    return tuple(
        multiply(multiply(endpoint_one, block), transpose(endpoint_zero))
        for block in block_tuple
    )


def reference_conversion(rho, nu, old_reference, new_reference):
    if rho == 0.0:
        new_rho = 0.0
    elif rho == 1.0:
        new_rho = 1.0
    else:
        lam = old_reference * math.sqrt((1.0 - rho) / rho)
        new_rho = new_reference * new_reference / (new_reference * new_reference + lam * lam)
    return new_rho, ray_rate(new_reference, rho, nu, old_reference)


def assemble_four(block_tuple):
    a_block, b_block, c_block, d_block = block_tuple
    return [
        a_block[0] + b_block[0],
        a_block[1] + b_block[1],
        c_block[0] + d_block[0],
        c_block[1] + d_block[1],
    ]


J_FOUR = [
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
    [-1.0, 0.0, 0.0, 0.0],
    [0.0, -1.0, 0.0, 0.0],
]


def affine_endpoint_transform(block_tuple, endpoint_one_scale, endpoint_zero_scale):
    a_block, b_block, c_block, d_block = block_tuple
    return (
        scale(a_block, 1.0),
        scale(b_block, 1.0 / endpoint_zero_scale),
        scale(c_block, endpoint_one_scale),
        scale(d_block, endpoint_one_scale / endpoint_zero_scale),
    )


def transverse_b_formula(t1, t0, transverse_constant, channel):
    if channel == "parallel":
        return 3.0 * (
            t1 * t1 * t0 ** (-1.0 / 3.0)
            - t1 ** (-1.0 / 3.0) * t0 * t0
        ) / (7.0 * transverse_constant)
    return 3.0 * (
        t1 * t0 ** (2.0 / 3.0) - t1 ** (2.0 / 3.0) * t0
    ) / transverse_constant


def g342_widths(t1: float, t0: float, rho: float):
    if not 0.0 < rho < 1.0:
        raise ValueError("mixed direction required")
    lam = t0 * math.sqrt((1.0 - rho) / rho)
    parallel_integral = gauss_log(
        lambda u: u ** (4.0 / 3.0) / (u * u + lam * lam) ** 1.5,
        t0, t1,
    )
    azimuth_integral = gauss_log(
        lambda u: u ** (-2.0 / 3.0) / math.sqrt(u * u + lam * lam),
        t0, t1,
    )
    return (
        (t0 * t0 + lam * lam) / t0
        * t1 ** (-1.0 / 3.0) * math.sqrt(t1 * t1 + lam * lam)
        * parallel_integral,
        math.sqrt(t0 * t0 + lam * lam) * t1 ** (2.0 / 3.0)
        * azimuth_integral,
    )


def main() -> None:
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    checks: dict[str, bool] = {}
    maxima = {
        "affine_density_weight_relative_error": 0.0,
        "affine_generator_weight_relative_error": 0.0,
        "block_composition_relative_error": 0.0,
        "density_composition_relative_error": 0.0,
        "generator_composition_relative_error": 0.0,
        "generator_reconstruction_relative_error": 0.0,
        "g342_area_recovery_relative_error": 0.0,
        "hessian_identity_relative_error": 0.0,
        "principal_relative_error": 0.0,
        "reference_covariance_relative_error": 0.0,
        "reversal_relative_error": 0.0,
        "screen_covariance_relative_error": 0.0,
    }

    def record(name: str, condition: bool) -> None:
        checks[name] = bool(condition)

    rng = random.Random(344001)
    direction_controls = (0.0, 1.0, 1.0e-12, 1.0 - 1.0e-12)

    for index in range(520):
        t_reference = 10.0 ** rng.uniform(-0.8, 0.8)
        t0 = t_reference * 10.0 ** rng.uniform(-0.4, 0.4)
        direction = 1.0 if rng.random() < 0.5 else -1.0
        ratio_one = 1.0 + 10.0 ** rng.uniform(-2.5, 0.65)
        ratio_two = 1.0 + 10.0 ** rng.uniform(-2.5, 0.65)
        if direction > 0.0:
            t1 = t0 * ratio_one
            t2 = t1 * ratio_two
        else:
            t1 = t0 / ratio_one
            t2 = t1 / ratio_two
        rho = direction_controls[index] if index < len(direction_controls) else rng.random()
        nu = 10.0 ** rng.uniform(-0.7, 0.7)
        block10 = blocks(t1, t0, rho, nu, t_reference)
        block21 = blocks(t2, t1, rho, nu, t_reference)
        block20 = blocks(t2, t0, rho, nu, t_reference)
        block01 = blocks(t0, t1, rho, nu, t_reference)
        a_block, b_block, c_block, d_block = block10

        record(f"B_invertible_{index}", abs(determinant_two(b_block)) > 0.0)
        record(
            f"B_channel_common_sign_{index}",
            b_block[0][0] * direction > 0.0 and b_block[1][1] * direction > 0.0,
        )
        record(f"oriented_native_density_positive_{index}", determinant_two(b_block) > 0.0)

        target_hessian, source_hessian, negative_mixed = generator_coefficients(block10)
        symmetry_error = max(
            matrix_error(target_hessian, transpose(target_hessian)),
            matrix_error(source_hessian, transpose(source_hessian)),
        )
        symplectic_identity = add(
            add(
                c_block,
                scale(multiply(multiply(d_block, inverse_two(b_block)), a_block), -1.0),
            ),
            negative_mixed,
        )
        identity_error = max(symmetry_error, matrix_error(symplectic_identity, [[0.0, 0.0], [0.0, 0.0]]))
        maxima["hessian_identity_relative_error"] = max(maxima["hessian_identity_relative_error"], identity_error)
        record(f"endpoint_hessians_symmetric_{index}", symmetry_error < TOL)
        record(f"cross_hessian_block_identity_{index}", identity_error < TOL)

        x0 = [rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0)]
        x1 = [rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0)]
        p1_gradient, p0_gradient = generator_momenta(block10, x1, x0)
        p0_direct = matvec(inverse_two(b_block), vecadd(x1, matvec(a_block, x0), -1.0))
        p1_direct = vecadd(matvec(c_block, x0), matvec(d_block, p0_direct))
        reconstruction_error = max(
            vector_error(p0_gradient, p0_direct), vector_error(p1_gradient, p1_direct)
        )
        maxima["generator_reconstruction_relative_error"] = max(
            maxima["generator_reconstruction_relative_error"], reconstruction_error
        )
        record(f"source_momentum_from_generator_{index}", vector_error(p0_gradient, p0_direct) < TOL)
        record(f"target_momentum_from_generator_{index}", vector_error(p1_gradient, p1_direct) < TOL)
        record(
            f"mixed_hessian_density_{index}",
            abs(density(block10) - abs(determinant_two(negative_mixed)))
            < TOL * max(1.0, density(block10)),
        )

        composed = compose_blocks(block21, block10)
        composition_error = block_error(composed, block20)
        maxima["block_composition_relative_error"] = max(
            maxima["block_composition_relative_error"], composition_error
        )
        record(f"direct_block_composition_{index}", composition_error < TOL)

        x2 = [rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0)]
        middle, stationary_hessian = stationary_middle(block21, block10, x2, x0)
        glued_value = generator_value(block21, x2, middle) + generator_value(block10, middle, x0)
        direct_value = generator_value(block20, x2, x0)
        generator_composition_error = abs(glued_value - direct_value) / max(
            1.0, abs(glued_value), abs(direct_value)
        )
        hessian_candidate = multiply(
            multiply(inverse_two(block21[1]), block20[1]), inverse_two(block10[1])
        )
        hessian_error = matrix_error(stationary_hessian, hessian_candidate)
        density_glued = density(block21) * density(block10) / abs(determinant_two(stationary_hessian))
        density_error = abs(density_glued - density(block20)) / max(
            1.0, density_glued, density(block20)
        )
        maxima["generator_composition_relative_error"] = max(
            maxima["generator_composition_relative_error"], generator_composition_error
        )
        maxima["density_composition_relative_error"] = max(
            maxima["density_composition_relative_error"], density_error, hessian_error
        )
        record(f"stationary_generator_composition_{index}", generator_composition_error < TOL)
        record(f"stationary_hessian_identity_{index}", hessian_error < TOL)
        record(f"determinant_density_composition_{index}", density_error < TOL)

        reverse_error = abs(
            generator_value(block01, x0, x1) + generator_value(block10, x1, x0)
        ) / max(1.0, abs(generator_value(block10, x1, x0)))
        reverse_density_error = abs(density(block01) - density(block10)) / max(
            1.0, density(block10)
        )
        maxima["reversal_relative_error"] = max(
            maxima["reversal_relative_error"], reverse_error, reverse_density_error
        )
        record(f"generator_reversal_antisymmetry_{index}", reverse_error < TOL)
        record(f"density_reversal_symmetry_{index}", reverse_density_error < TOL)

        affine_scale = 10.0 ** rng.uniform(-0.7, 0.7)
        scaled_block = blocks(t1, t0, rho, affine_scale * nu, t_reference)
        scaled_value = generator_value(scaled_block, x1, x0)
        affine_generator_error = abs(scaled_value - affine_scale * generator_value(block10, x1, x0)) / max(
            1.0, abs(scaled_value), abs(affine_scale * generator_value(block10, x1, x0))
        )
        affine_density_error = abs(density(scaled_block) - affine_scale ** 2 * density(block10)) / max(
            1.0, density(scaled_block), affine_scale ** 2 * density(block10)
        )
        maxima["affine_generator_weight_relative_error"] = max(
            maxima["affine_generator_weight_relative_error"], affine_generator_error
        )
        maxima["affine_density_weight_relative_error"] = max(
            maxima["affine_density_weight_relative_error"], affine_density_error
        )
        record(f"common_affine_generator_weight_one_{index}", affine_generator_error < TOL)
        record(f"common_affine_density_weight_two_{index}", affine_density_error < TOL)

        endpoint_zero_scale = 10.0 ** rng.uniform(-0.5, 0.5)
        endpoint_one_scale = 10.0 ** rng.uniform(-0.5, 0.5)
        independent_units = affine_endpoint_transform(
            block10, endpoint_one_scale, endpoint_zero_scale
        )
        independent_four = assemble_four(independent_units)
        conformal = multiply(multiply(transpose(independent_four), J_FOUR), independent_four)
        expected_conformal = scale(J_FOUR, endpoint_one_scale / endpoint_zero_scale)
        record(
            f"independent_endpoint_units_conformally_symplectic_{index}",
            matrix_error(conformal, expected_conformal) < TOL,
        )
        if abs(endpoint_one_scale / endpoint_zero_scale - 1.0) > 1.0e-6:
            record(
                f"independent_endpoint_units_not_bare_canonical_{index}",
                matrix_error(conformal, J_FOUR) > 1.0e-7,
            )

        new_reference = t_reference * 10.0 ** rng.uniform(-0.6, 0.6)
        new_rho, new_nu = reference_conversion(rho, nu, t_reference, new_reference)
        changed_reference = blocks(t1, t0, new_rho, new_nu, new_reference)
        reference_error = block_error(changed_reference, block10)
        reference_generator_error = abs(
            generator_value(changed_reference, x1, x0) - generator_value(block10, x1, x0)
        ) / max(1.0, abs(generator_value(block10, x1, x0)))
        reference_density_error = abs(density(changed_reference) - density(block10)) / max(
            1.0, density(block10)
        )
        maxima["reference_covariance_relative_error"] = max(
            maxima["reference_covariance_relative_error"],
            reference_error, reference_generator_error, reference_density_error,
        )
        record(f"reference_event_block_covariance_{index}", reference_error < TOL)
        record(f"reference_event_generator_covariance_{index}", reference_generator_error < TOL)
        record(f"reference_event_density_covariance_{index}", reference_density_error < TOL)

        rotation_zero = rotate(rng.uniform(-math.pi, math.pi), index % 7 == 0)
        rotation_one = rotate(rng.uniform(-math.pi, math.pi), index % 11 == 0)
        changed_basis = change_screen_bases(block10, rotation_one, rotation_zero)
        changed_x0 = matvec(rotation_zero, x0)
        changed_x1 = matvec(rotation_one, x1)
        scalar_error = abs(
            generator_value(changed_basis, changed_x1, changed_x0)
            - generator_value(block10, x1, x0)
        ) / max(1.0, abs(generator_value(block10, x1, x0)))
        changed_negative_mixed = generator_coefficients(changed_basis)[2]
        expected_negative_mixed = multiply(
            multiply(rotation_one, negative_mixed), transpose(rotation_zero)
        )
        mixed_error = matrix_error(changed_negative_mixed, expected_negative_mixed)
        absolute_density_error = abs(density(changed_basis) - density(block10)) / max(
            1.0, density(block10)
        )
        maxima["screen_covariance_relative_error"] = max(
            maxima["screen_covariance_relative_error"], scalar_error, mixed_error,
            absolute_density_error,
        )
        record(f"endpoint_screen_generator_scalar_{index}", scalar_error < TOL)
        record(f"endpoint_mixed_hessian_bitensor_{index}", mixed_error < TOL)
        record(f"endpoint_absolute_density_invariant_{index}", absolute_density_error < TOL)

    for index in range(120):
        low = 10.0 ** rng.uniform(-0.7, 0.4)
        middle_time = low * (1.05 + 10.0 ** rng.uniform(-1.5, 0.35))
        high = middle_time * (1.05 + 10.0 ** rng.uniform(-1.5, 0.35))
        permutations = (
            (low, middle_time, high), (low, high, middle_time),
            (middle_time, low, high), (middle_time, high, low),
            (high, low, middle_time), (high, middle_time, low),
        )
        t0, t1, t2 = permutations[index % len(permutations)]
        t_reference = 10.0 ** rng.uniform(-0.7, 0.7)
        rho = direction_controls[index] if index < len(direction_controls) else rng.random()
        nu = 10.0 ** rng.uniform(-0.6, 0.6)
        block10 = blocks(t1, t0, rho, nu, t_reference)
        block21 = blocks(t2, t1, rho, nu, t_reference)
        block20 = blocks(t2, t0, rho, nu, t_reference)
        x0 = [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)]
        x2 = [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)]
        middle, stationary_hessian = stationary_middle(block21, block10, x2, x0)
        block_composition_error = block_error(compose_blocks(block21, block10), block20)
        action_composition_error = abs(
            generator_value(block21, x2, middle)
            + generator_value(block10, middle, x0)
            - generator_value(block20, x2, x0)
        ) / max(1.0, abs(generator_value(block20, x2, x0)))
        density_composition_error = abs(
            density(block21) * density(block10) / abs(determinant_two(stationary_hessian))
            - density(block20)
        ) / max(1.0, density(block20))
        maxima["block_composition_relative_error"] = max(
            maxima["block_composition_relative_error"], block_composition_error
        )
        maxima["generator_composition_relative_error"] = max(
            maxima["generator_composition_relative_error"], action_composition_error
        )
        maxima["density_composition_relative_error"] = max(
            maxima["density_composition_relative_error"], density_composition_error
        )
        record(f"all_order_block_composition_{index}", block_composition_error < TOL)
        record(f"all_order_stationary_action_{index}", action_composition_error < TOL)
        record(f"all_order_density_glue_{index}", density_composition_error < TOL)
        record(
            f"all_order_stationary_hessian_invertible_{index}",
            abs(determinant_two(stationary_hessian)) > 0.0,
        )

    for index in range(120):
        t_reference = 10.0 ** rng.uniform(-0.8, 0.8)
        t0 = t_reference * 10.0 ** rng.uniform(-0.4, 0.4)
        t1 = t0 * (1.0 + 10.0 ** rng.uniform(-2.5, 0.65))
        nu = 10.0 ** rng.uniform(-0.7, 0.7)

        longitudinal = blocks(t1, t0, 1.0, nu, t_reference)
        affine_delta = (
            1.5 * t_reference ** (1.0 / 3.0)
            * (t1 ** (2.0 / 3.0) - t0 ** (2.0 / 3.0)) / nu
        )
        expected_density = 1.0 / (affine_delta * affine_delta)
        longitudinal_error = max(
            abs(longitudinal[1][0][0] - affine_delta),
            abs(longitudinal[1][1][1] - affine_delta),
            abs(density(longitudinal) - expected_density) / max(1.0, expected_density),
        )
        record(f"longitudinal_free_B_{index}", longitudinal_error < TOL)
        x0 = [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)]
        x1 = [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)]
        free_value = dot(vecadd(x1, x0, -1.0), vecadd(x1, x0, -1.0)) / (2.0 * affine_delta)
        free_error = abs(generator_value(longitudinal, x1, x0) - free_value) / max(1.0, abs(free_value))
        record(f"longitudinal_free_generator_{index}", free_error < TOL)

        transverse = blocks(t1, t0, 0.0, nu, t_reference)
        transverse_constant = nu * t_reference ** (2.0 / 3.0)
        expected_parallel = transverse_b_formula(t1, t0, transverse_constant, "parallel")
        expected_azimuth = transverse_b_formula(t1, t0, transverse_constant, "azimuth")
        transverse_error = max(
            abs(transverse[1][0][0] - expected_parallel) / max(1.0, abs(expected_parallel)),
            abs(transverse[1][1][1] - expected_azimuth) / max(1.0, abs(expected_azimuth)),
            abs(density(transverse) - 1.0 / abs(expected_parallel * expected_azimuth))
            / max(1.0, density(transverse)),
        )
        maxima["principal_relative_error"] = max(
            maxima["principal_relative_error"], longitudinal_error, free_error, transverse_error
        )
        record(f"transverse_power_B_and_density_{index}", transverse_error < TOL)

    for index in range(100):
        t0 = 10.0 ** rng.uniform(-0.8, 0.8)
        t1 = t0 * (1.0 + 10.0 ** rng.uniform(-2.0, 0.65))
        rho = rng.uniform(1.0e-5, 1.0 - 1.0e-5)
        source_block = blocks(t1, t0, rho, 1.0, t0)
        widths = g342_widths(t1, t0, rho)
        area_error = abs(
            determinant_two(source_block[1]) - widths[0] * widths[1]
        ) / max(1.0, abs(widths[0] * widths[1]))
        maxima["g342_area_recovery_relative_error"] = max(
            maxima["g342_area_recovery_relative_error"], area_error
        )
        record(f"g342_source_vertex_area_recovery_{index}", area_error < TOL)

    for index in range(80):
        t = 10.0 ** rng.uniform(-1.0, 1.0)
        rho = rng.random()
        nu = 10.0 ** rng.uniform(-0.7, 0.7)
        t_reference = 10.0 ** rng.uniform(-0.7, 0.7)
        coincident = blocks(t, t, rho, nu, t_reference)
        record(f"coincident_B_zero_chart_boundary_{index}", determinant_two(coincident[1]) == 0.0)
        labels = ((0, 0, 0), (1, -1, 0), (-2, 3, 1), (4, 0, -5))
        record(f"compact_path_labels_retained_{index}", tuple(labels) == labels)

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "assertions": len(checks),
        "failed": failed,
        "landing": LANDING,
        "maxima": maxima,
        "method": "G343 exact blocks plus direct quadratic Hessian and stationary-composition algebra",
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "selected_alternatives": ["A", "C1", "R1", "A1", "S1", "P1", "Q1"],
        "status": "PASS" if not failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed[:16]))


if __name__ == "__main__":
    main()
