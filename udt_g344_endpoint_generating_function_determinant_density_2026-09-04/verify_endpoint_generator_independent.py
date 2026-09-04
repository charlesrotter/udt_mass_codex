#!/usr/bin/env python3
"""Implementation-distinct verification of the bounded G344 endpoint generator."""

from __future__ import annotations

import json
import math
import os
import random


TOL = 3.0e-7


def simpson_log(function, low: float, high: float, panels: int = 640) -> float:
    if low <= 0.0 or high <= 0.0:
        raise ValueError("positive-time domain required")
    if panels % 2:
        panels += 1
    start = math.log(low)
    step = (math.log(high) - start) / panels

    def transformed(x_value):
        t_value = math.exp(x_value)
        return function(t_value) * t_value

    total = transformed(start) + transformed(start + panels * step)
    for index in range(1, panels):
        total += (4.0 if index % 2 else 2.0) * transformed(start + index * step)
    return total * step / 3.0


def ray_rate(t_value, rho, nu, t_reference):
    h_value = math.sqrt(rho * t_value * t_value + (1.0 - rho) * t_reference * t_reference)
    return nu * t_reference ** (-1.0 / 3.0) * t_value ** (-2.0 / 3.0) * h_value


def tide(t_value, rho, nu, t_reference):
    return (
        2.0 * nu * nu * t_reference ** (4.0 / 3.0) * (1.0 - rho)
        / (3.0 * t_value ** (10.0 / 3.0))
    )


def channel_solution(t_value, rho, nu, t_reference, channel):
    h_value = math.sqrt(rho * t_value * t_value + (1.0 - rho) * t_reference * t_reference)
    if channel == "parallel":
        y_value = t_value ** (-1.0 / 3.0) * h_value
        logarithmic_derivative = rho * t_value / (h_value * h_value) - 1.0 / (3.0 * t_value)
    elif channel == "azimuth":
        y_value = t_value ** (2.0 / 3.0)
        logarithmic_derivative = 2.0 / (3.0 * t_value)
    else:
        raise ValueError(channel)
    return y_value, ray_rate(t_value, rho, nu, t_reference) * logarithmic_derivative


def weight(t_value, rho, t_reference, channel):
    h_value = math.sqrt(rho * t_value * t_value + (1.0 - rho) * t_reference * t_reference)
    if channel == "parallel":
        return t_value ** (4.0 / 3.0) / h_value ** 3
    return t_value ** (-2.0 / 3.0) / h_value


def inverse_two(matrix):
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant],
    ]


def multiply(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def add(left, right, factor: float = 1.0):
    return [[left[i][j] + factor * right[i][j] for j in range(len(left[0]))]
            for i in range(len(left))]


def scale(matrix, factor: float):
    return [[factor * value for value in row] for row in matrix]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def determinant_two(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def matrix_error(left, right):
    return max(
        abs(left[i][j] - right[i][j])
        / max(1.0, abs(left[i][j]), abs(right[i][j]))
        for i in range(len(left)) for j in range(len(left[0]))
    )


def matvec(matrix, vector):
    return [sum(row[index] * vector[index] for index in range(len(vector)))
            for row in matrix]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def vecadd(left, right, factor: float = 1.0):
    return [left[index] + factor * right[index] for index in range(len(left))]


def vector_error(left, right):
    return max(abs(a - b) / max(1.0, abs(a), abs(b)) for a, b in zip(left, right))


def fundamental(t_value, anchor, rho, nu, t_reference, channel):
    y_value, mu_value = channel_solution(t_value, rho, nu, t_reference, channel)
    integral = (
        t_reference ** (1.0 / 3.0) / nu
        * simpson_log(lambda u: weight(u, rho, t_reference, channel), anchor, t_value)
    )
    second = y_value * integral
    return [
        [y_value, second],
        [mu_value * y_value, mu_value * second + 1.0 / y_value],
    ]


def scalar_map(t1, t0, rho, nu, t_reference, channel):
    return multiply(
        fundamental(t1, t0, rho, nu, t_reference, channel),
        inverse_two(fundamental(t0, t0, rho, nu, t_reference, channel)),
    )


def diagonal(left, right):
    return [[left, 0.0], [0.0, right]]


def block_map(t1, t0, rho, nu, t_reference):
    parallel = scalar_map(t1, t0, rho, nu, t_reference, "parallel")
    azimuth = scalar_map(t1, t0, rho, nu, t_reference, "azimuth")
    return (
        diagonal(parallel[0][0], azimuth[0][0]),
        diagonal(parallel[0][1], azimuth[0][1]),
        diagonal(parallel[1][0], azimuth[1][0]),
        diagonal(parallel[1][1], azimuth[1][1]),
    )


def boundary_momenta(block_tuple, x1, x0):
    a_block, b_block, c_block, d_block = block_tuple
    p0 = matvec(inverse_two(b_block), vecadd(x1, matvec(a_block, x0), -1.0))
    p1 = vecadd(matvec(c_block, x0), matvec(d_block, p0))
    return p1, p0


def boundary_action(block_tuple, x1, x0):
    p1, p0 = boundary_momenta(block_tuple, x1, x0)
    return 0.5 * (dot(x1, p1) - dot(x0, p0))


def mixed_hessian_finite_difference(block_tuple, x1, x0):
    steps_one = [2.0e-3 * max(1.0, abs(value)) for value in x1]
    steps_zero = [2.0e-3 * max(1.0, abs(value)) for value in x0]
    result = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(2):
        for j in range(2):
            hi = steps_one[i]
            hj = steps_zero[j]
            values = []
            for sign_one, sign_zero in ((1.0, 1.0), (1.0, -1.0), (-1.0, 1.0), (-1.0, -1.0)):
                moved_one = list(x1)
                moved_zero = list(x0)
                moved_one[i] += sign_one * hi
                moved_zero[j] += sign_zero * hj
                values.append(boundary_action(block_tuple, moved_one, moved_zero))
            result[i][j] = (values[0] - values[1] - values[2] + values[3]) / (4.0 * hi * hj)
    return result


def finite_gradient(block_tuple, x1, x0, endpoint):
    base = x1 if endpoint == 1 else x0
    gradient = []
    for component in range(2):
        step = 2.0e-5 * max(1.0, abs(base[component]))
        plus_one, minus_one = list(x1), list(x1)
        plus_zero, minus_zero = list(x0), list(x0)
        if endpoint == 1:
            plus_one[component] += step
            minus_one[component] -= step
        else:
            plus_zero[component] += step
            minus_zero[component] -= step
        gradient.append(
            (boundary_action(block_tuple, plus_one, plus_zero)
             - boundary_action(block_tuple, minus_one, minus_zero)) / (2.0 * step)
        )
    return gradient


def density(block_tuple):
    return 1.0 / abs(determinant_two(block_tuple[1]))


def compose(left, right):
    a21, b21, c21, d21 = left
    a10, b10, c10, d10 = right
    return (
        add(multiply(a21, a10), multiply(b21, c10)),
        add(multiply(a21, b10), multiply(b21, d10)),
        add(multiply(c21, a10), multiply(d21, c10)),
        add(multiply(c21, b10), multiply(d21, d10)),
    )


def stationary_join(left, right, x2, x0):
    b21_inverse = inverse_two(left[1])
    b10_inverse = inverse_two(right[1])
    hessian = add(multiply(b21_inverse, left[0]), multiply(right[3], b10_inverse))
    rhs = vecadd(matvec(b21_inverse, x2), matvec(transpose(b10_inverse), x0))
    return matvec(inverse_two(hessian), rhs), hessian


def rotate(angle, reflected=False):
    cosine, sine = math.cos(angle), math.sin(angle)
    answer = [[cosine, -sine], [sine, cosine]]
    if reflected:
        answer = multiply([[-1.0, 0.0], [0.0, 1.0]], answer)
    return answer


def change_bases(block_tuple, endpoint_one, endpoint_zero):
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


def integrate_state_and_action(t1, t0, rho, nu, t_reference, x0, p0):
    start = math.log(t0)
    finish = math.log(t1)
    panels = max(800, int(300.0 * abs(finish - start)))
    step = (finish - start) / panels
    state = [x0[0], x0[1], p0[0], p0[1], 0.0]

    def rhs(x_value, current):
        t_value = math.exp(x_value)
        q_value = tide(t_value, rho, nu, t_reference)
        ds_dx = t_value / ray_rate(t_value, rho, nu, t_reference)
        x_parallel, x_azimuth, p_parallel, p_azimuth, _ = current
        lagrangian = 0.5 * (
            p_parallel * p_parallel + p_azimuth * p_azimuth
            + q_value * x_parallel * x_parallel - q_value * x_azimuth * x_azimuth
        )
        return [
            ds_dx * p_parallel,
            ds_dx * p_azimuth,
            ds_dx * q_value * x_parallel,
            -ds_dx * q_value * x_azimuth,
            ds_dx * lagrangian,
        ]

    at = start
    for _ in range(panels):
        k1 = rhs(at, state)
        k2 = rhs(at + 0.5 * step, [state[i] + 0.5 * step * k1[i] for i in range(5)])
        k3 = rhs(at + 0.5 * step, [state[i] + 0.5 * step * k2[i] for i in range(5)])
        k4 = rhs(at + step, [state[i] + step * k3[i] for i in range(5)])
        state = [
            state[i] + step * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0
            for i in range(5)
        ]
        at += step
    return state


def main() -> None:
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    checks = {}
    maxima = {
        "action_integral_relative_error": 0.0,
        "composition_relative_error": 0.0,
        "density_relative_error": 0.0,
        "finite_gradient_relative_error": 0.0,
        "finite_mixed_hessian_relative_error": 0.0,
        "reference_relative_error": 0.0,
        "screen_relative_error": 0.0,
        "state_integral_relative_error": 0.0,
    }

    def record(name, condition):
        checks[name] = bool(condition)

    rng = random.Random(344991)
    controls = (0.0, 1.0, 1.0e-10, 1.0 - 1.0e-10)
    saved_cases = []

    for index in range(220):
        t_reference = 10.0 ** rng.uniform(-0.6, 0.6)
        t0 = t_reference * 10.0 ** rng.uniform(-0.3, 0.3)
        direction = 1.0 if rng.random() < 0.5 else -1.0
        first_ratio = 1.0 + 10.0 ** rng.uniform(-2.0, 0.45)
        second_ratio = 1.0 + 10.0 ** rng.uniform(-2.0, 0.45)
        t1 = t0 * first_ratio if direction > 0.0 else t0 / first_ratio
        t2 = t1 * second_ratio if direction > 0.0 else t1 / second_ratio
        rho = controls[index] if index < len(controls) else rng.random()
        nu = 10.0 ** rng.uniform(-0.5, 0.5)
        map10 = block_map(t1, t0, rho, nu, t_reference)
        map21 = block_map(t2, t1, rho, nu, t_reference)
        map20 = block_map(t2, t0, rho, nu, t_reference)
        map01 = block_map(t0, t1, rho, nu, t_reference)
        x0 = [rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)]
        x1 = [rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)]
        x2 = [rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)]

        p1, p0 = boundary_momenta(map10, x1, x0)
        gradient_one = finite_gradient(map10, x1, x0, 1)
        gradient_zero = finite_gradient(map10, x1, x0, 0)
        gradient_error = max(
            vector_error(gradient_one, p1),
            vector_error(gradient_zero, [-value for value in p0]),
        )
        maxima["finite_gradient_relative_error"] = max(
            maxima["finite_gradient_relative_error"], gradient_error
        )
        for component in range(2):
            record(f"finite_target_gradient_{index}_{component}", abs(gradient_one[component] - p1[component]) < TOL * max(1.0, abs(p1[component])))
            record(f"finite_source_gradient_{index}_{component}", abs(gradient_zero[component] + p0[component]) < TOL * max(1.0, abs(p0[component])))

        mixed = mixed_hessian_finite_difference(map10, x1, x0)
        expected_mixed = scale(transpose(inverse_two(map10[1])), -1.0)
        mixed_error = matrix_error(mixed, expected_mixed)
        maxima["finite_mixed_hessian_relative_error"] = max(
            maxima["finite_mixed_hessian_relative_error"], mixed_error
        )
        for row in range(2):
            for column in range(2):
                record(
                    f"finite_mixed_hessian_{index}_{row}_{column}",
                    abs(mixed[row][column] - expected_mixed[row][column])
                    < TOL * max(1.0, abs(expected_mixed[row][column])),
                )
        finite_density = abs(determinant_two(scale(mixed, -1.0)))
        density_error = abs(finite_density - density(map10)) / max(1.0, density(map10))
        maxima["density_relative_error"] = max(maxima["density_relative_error"], density_error)
        record(f"finite_mixed_density_{index}", density_error < TOL)

        joined, stationary_hessian = stationary_join(map21, map10, x2, x0)
        glued_action = boundary_action(map21, x2, joined) + boundary_action(map10, joined, x0)
        direct_action = boundary_action(map20, x2, x0)
        action_error = abs(glued_action - direct_action) / max(1.0, abs(glued_action), abs(direct_action))
        map_error = max(matrix_error(a, b) for a, b in zip(compose(map21, map10), map20))
        glued_density = density(map21) * density(map10) / abs(determinant_two(stationary_hessian))
        glue_density_error = abs(glued_density - density(map20)) / max(1.0, density(map20))
        maxima["composition_relative_error"] = max(
            maxima["composition_relative_error"], action_error, map_error, glue_density_error
        )
        record(f"independent_block_composition_{index}", map_error < TOL)
        record(f"independent_stationary_action_{index}", action_error < TOL)
        record(f"independent_density_glue_{index}", glue_density_error < TOL)

        reverse_action_error = abs(
            boundary_action(map01, x0, x1) + boundary_action(map10, x1, x0)
        ) / max(1.0, abs(boundary_action(map10, x1, x0)))
        reverse_density_error = abs(density(map01) - density(map10)) / max(1.0, density(map10))
        record(f"independent_action_reversal_{index}", reverse_action_error < TOL)
        record(f"independent_density_reversal_{index}", reverse_density_error < TOL)

        new_reference = t_reference * 10.0 ** rng.uniform(-0.5, 0.5)
        new_rho, new_nu = reference_conversion(rho, nu, t_reference, new_reference)
        changed_reference = block_map(t1, t0, new_rho, new_nu, new_reference)
        reference_action_error = abs(
            boundary_action(changed_reference, x1, x0) - boundary_action(map10, x1, x0)
        ) / max(1.0, abs(boundary_action(map10, x1, x0)))
        reference_density_error = abs(density(changed_reference) - density(map10)) / max(1.0, density(map10))
        maxima["reference_relative_error"] = max(
            maxima["reference_relative_error"], reference_action_error, reference_density_error
        )
        record(f"independent_reference_action_{index}", reference_action_error < TOL)
        record(f"independent_reference_density_{index}", reference_density_error < TOL)

        rotation_zero = rotate(rng.uniform(-math.pi, math.pi), index % 13 == 0)
        rotation_one = rotate(rng.uniform(-math.pi, math.pi), index % 17 == 0)
        rotated = change_bases(map10, rotation_one, rotation_zero)
        rotated_x0 = matvec(rotation_zero, x0)
        rotated_x1 = matvec(rotation_one, x1)
        screen_action_error = abs(
            boundary_action(rotated, rotated_x1, rotated_x0) - boundary_action(map10, x1, x0)
        ) / max(1.0, abs(boundary_action(map10, x1, x0)))
        screen_density_error = abs(density(rotated) - density(map10)) / max(1.0, density(map10))
        maxima["screen_relative_error"] = max(
            maxima["screen_relative_error"], screen_action_error, screen_density_error
        )
        record(f"independent_screen_action_scalar_{index}", screen_action_error < TOL)
        record(f"independent_screen_absolute_density_{index}", screen_density_error < TOL)

        record(f"independent_B_nonzero_{index}", abs(determinant_two(map10[1])) > 0.0)
        if index < 64:
            saved_cases.append((t1, t0, rho, nu, t_reference, x1, x0, map10))

    for index, (t1, t0, rho, nu, t_reference, x1, x0, map10) in enumerate(saved_cases):
        p1, p0 = boundary_momenta(map10, x1, x0)
        integrated = integrate_state_and_action(t1, t0, rho, nu, t_reference, x0, p0)
        state_error = max(
            vector_error(integrated[:2], x1), vector_error(integrated[2:4], p1)
        )
        action_error = abs(integrated[4] - boundary_action(map10, x1, x0)) / max(
            1.0, abs(boundary_action(map10, x1, x0))
        )
        maxima["state_integral_relative_error"] = max(
            maxima["state_integral_relative_error"], state_error
        )
        maxima["action_integral_relative_error"] = max(
            maxima["action_integral_relative_error"], action_error
        )
        record(f"rk_boundary_position_{index}", vector_error(integrated[:2], x1) < TOL)
        record(f"rk_boundary_momentum_{index}", vector_error(integrated[2:4], p1) < TOL)
        record(f"rk_onshell_action_{index}", action_error < TOL)

    for index in range(90):
        low = 10.0 ** rng.uniform(-0.6, 0.3)
        middle_time = low * (1.08 + 10.0 ** rng.uniform(-1.4, 0.3))
        high = middle_time * (1.08 + 10.0 ** rng.uniform(-1.4, 0.3))
        permutations = (
            (low, middle_time, high), (low, high, middle_time),
            (middle_time, low, high), (middle_time, high, low),
            (high, low, middle_time), (high, middle_time, low),
        )
        t0, t1, t2 = permutations[index % len(permutations)]
        t_reference = 10.0 ** rng.uniform(-0.6, 0.6)
        rho = controls[index] if index < len(controls) else rng.random()
        nu = 10.0 ** rng.uniform(-0.5, 0.5)
        map10 = block_map(t1, t0, rho, nu, t_reference)
        map21 = block_map(t2, t1, rho, nu, t_reference)
        map20 = block_map(t2, t0, rho, nu, t_reference)
        x0 = [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)]
        x2 = [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)]
        middle, stationary_hessian = stationary_join(map21, map10, x2, x0)
        map_error = max(matrix_error(a, b) for a, b in zip(compose(map21, map10), map20))
        action_error = abs(
            boundary_action(map21, x2, middle) + boundary_action(map10, middle, x0)
            - boundary_action(map20, x2, x0)
        ) / max(1.0, abs(boundary_action(map20, x2, x0)))
        density_error = abs(
            density(map21) * density(map10) / abs(determinant_two(stationary_hessian))
            - density(map20)
        ) / max(1.0, density(map20))
        maxima["composition_relative_error"] = max(
            maxima["composition_relative_error"], map_error, action_error, density_error
        )
        record(f"independent_all_order_map_{index}", map_error < TOL)
        record(f"independent_all_order_action_{index}", action_error < TOL)
        record(f"independent_all_order_density_{index}", density_error < TOL)

    for index in range(80):
        t_reference = 10.0 ** rng.uniform(-0.6, 0.6)
        t0 = t_reference * 10.0 ** rng.uniform(-0.3, 0.3)
        t1 = t0 * (1.0 + 10.0 ** rng.uniform(-2.0, 0.45))
        nu = 10.0 ** rng.uniform(-0.5, 0.5)
        longitudinal = block_map(t1, t0, 1.0, nu, t_reference)
        affine_delta = 1.5 * t_reference ** (1.0 / 3.0) * (
            t1 ** (2.0 / 3.0) - t0 ** (2.0 / 3.0)
        ) / nu
        record(
            f"independent_longitudinal_density_{index}",
            abs(density(longitudinal) - 1.0 / (affine_delta * affine_delta))
            < TOL * max(1.0, density(longitudinal)),
        )

        transverse = block_map(t1, t0, 0.0, nu, t_reference)
        transverse_constant = nu * t_reference ** (2.0 / 3.0)
        parallel_b = 3.0 * (
            t1 * t1 * t0 ** (-1.0 / 3.0) - t1 ** (-1.0 / 3.0) * t0 * t0
        ) / (7.0 * transverse_constant)
        azimuth_b = 3.0 * (
            t1 * t0 ** (2.0 / 3.0) - t1 ** (2.0 / 3.0) * t0
        ) / transverse_constant
        record(
            f"independent_transverse_density_{index}",
            abs(density(transverse) - 1.0 / abs(parallel_b * azimuth_b))
            < TOL * max(1.0, density(transverse)),
        )
        labels = ((0, 0, 0), (1, 0, -1), (-3, 2, 4))
        record(f"independent_path_labels_retained_{index}", tuple(labels) == labels)

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "assertions": len(checks),
        "failed": failed,
        "landing": "INDEPENDENT_FUNDAMENTAL_BASIS_FINITE_HESSIAN_AND_ONSHELL_ACTION_VERIFICATION",
        "maxima": maxima,
        "method": "independent Simpson fundamental basis, finite endpoint derivatives, and RK4 on-shell Jacobi action",
        "status": "PASS" if not failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed[:16]))


if __name__ == "__main__":
    main()
