#!/usr/bin/env python3
"""Implementation-distinct smooth-profile verification for G348."""

from __future__ import annotations

import json
import math
import random


TOL = 2.0e-7
ZERO_TOL = 2.0e-6


def ident(size):
    return [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]


def trans(value):
    return [list(row) for row in zip(*value)]


def product(left, right):
    columns = trans(right)
    return [[sum(a * b for a, b in zip(row, column)) for column in columns] for row in left]


def plus(left, right):
    return [[a + b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(left, right)]


def times(number, value):
    return [[number * item for item in row] for row in value]


def determinant2(value):
    return value[0][0] * value[1][1] - value[0][1] * value[1][0]


def subblock(value, row, column):
    return [[value[2 * row + i][2 * column + j] for j in range(2)] for i in range(2)]


def phase_generator(tide):
    return [
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [-tide[0][0], -tide[0][1], 0.0, 0.0],
        [-tide[1][0], -tide[1][1], 0.0, 0.0],
    ]


def smooth_tide(parameters, value):
    a0, a1, d0, d1, b0, b1, frequency = parameters
    return [
        [a0 + a1 * math.sin(frequency * value), b0 + b1 * math.cos(0.7 * frequency * value)],
        [b0 + b1 * math.cos(0.7 * frequency * value), d0 + d1 * math.cos(frequency * value)],
    ]


def derivative(parameters, location, state):
    return product(phase_generator(smooth_tide(parameters, location)), state)


def rk4(parameters, start, stop, steps):
    state = ident(4)
    step = (stop - start) / steps
    location = start
    for _ in range(steps):
        k1 = derivative(parameters, location, state)
        k2 = derivative(parameters, location + 0.5 * step, plus(state, times(0.5 * step, k1)))
        k3 = derivative(parameters, location + 0.5 * step, plus(state, times(0.5 * step, k2)))
        k4 = derivative(parameters, location + step, plus(state, times(step, k3)))
        increment = plus(plus(k1, times(2.0, k2)), plus(times(2.0, k3), k4))
        state = plus(state, times(step / 6.0, increment))
        location += step
    return state


J = [
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
    [-1.0, 0.0, 0.0, 0.0],
    [0.0, -1.0, 0.0, 0.0],
]


class Audit:
    def __init__(self):
        self.count = 0
        self.failures = []
        self.maxima = {}

    def scalar(self, label, actual, expected, tolerance=TOL):
        self.count += 1
        error = abs(actual - expected) / max(1.0, abs(actual), abs(expected))
        self.maxima[label] = max(error, self.maxima.get(label, 0.0))
        if not math.isfinite(error) or error > tolerance:
            self.failures.append({"label": label, "error": error})

    def matrix(self, label, actual, expected, tolerance=TOL):
        for row_a, row_e in zip(actual, expected):
            for a, e in zip(row_a, row_e):
                self.scalar(label, a, e, tolerance)

    def require(self, label, condition):
        self.count += 1
        if not condition:
            self.failures.append({"label": label, "condition": False})


def lorentz(left, right):
    return -left[0] * right[0] + sum(left[i] * right[i] for i in range(1, 4))


def dot3(left, right):
    return sum(a * b for a, b in zip(left, right))


def unit3(value):
    length = math.sqrt(dot3(value, value))
    return tuple(item / length for item in value)


def cross3(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def basis_for(direction):
    trial = (0.0, 0.0, 1.0) if abs(direction[2]) < 0.8 else (0.0, 1.0, 0.0)
    first = unit3(cross3(direction, trial))
    second = unit3(cross3(direction, first))
    return (0.0,) + first, (0.0,) + second


def rapidity_observer(rapidity, direction):
    return (math.cosh(rapidity),) + tuple(math.sinh(rapidity) * item for item in direction)


def change_screen(vector, observer, ray, frequency):
    amount = lorentz(vector, observer) / frequency
    return tuple(vector[i] + amount * ray[i] for i in range(4))


def sky_area(first, second):
    value = lorentz(first, first) * lorentz(second, second) - lorentz(first, second) ** 2
    return math.sqrt(max(0.0, value))


def main():
    rng = random.Random(843201)
    audit = Audit()
    smooth_cases = 0
    near_null_cases = 0

    for index in range(150):
        parameters = (
            rng.uniform(-1.2, 1.8), rng.uniform(-0.8, 0.8),
            rng.uniform(-1.2, 1.8), rng.uniform(-0.8, 0.8),
            rng.uniform(-0.5, 0.5), rng.uniform(-0.8, 0.8), rng.uniform(0.7, 2.4),
        )
        stop = rng.uniform(0.35, 1.05)
        middle = stop * rng.uniform(0.3, 0.7)
        whole = rk4(parameters, 0.0, stop, 360)
        reverse = rk4(parameters, stop, 0.0, 360)
        first = rk4(parameters, 0.0, middle, 190)
        second = rk4(parameters, middle, stop, 190)
        audit.matrix("smooth_symplectic", product(product(trans(whole), J), whole), J)
        audit.matrix("smooth_reversal", product(reverse, whole), ident(4))
        audit.matrix("smooth_composition", product(second, first), whole)
        b_forward = subblock(whole, 0, 1)
        b_reverse = subblock(reverse, 0, 1)
        audit.matrix("smooth_B_adjoint", b_reverse, times(-1.0, trans(b_forward)))
        bprime = subblock(whole, 1, 1)
        wronskian = plus(product(trans(b_forward), bprime),
                         times(-1.0, product(trans(bprime), b_forward)))
        audit.matrix("smooth_B_Wronskian", wronskian, [[0.0, 0.0], [0.0, 0.0]])

        omega0 = math.exp(rng.uniform(-0.8, 0.8))
        omega1 = math.exp(rng.uniform(-0.8, 0.8))
        forward_area = omega0 * omega0 * abs(determinant2(b_forward))
        reverse_area = omega1 * omega1 * abs(determinant2(b_reverse))
        audit.scalar("smooth_directional_reversal", forward_area / reverse_area,
                     (omega0 / omega1) ** 2)

        direction = unit3((rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0),
                           rng.uniform(-1.0, 1.0)))
        ray = (1.0,) + direction
        rapidity = rng.uniform(-4.2, 4.2)
        if abs(rapidity) > 3.5:
            near_null_cases += 1
        velocity_direction = unit3((rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0),
                                    rng.uniform(-1.0, 1.0)))
        endpoint_observer = rapidity_observer(rapidity, velocity_direction)
        frequency = -lorentz(ray, endpoint_observer)
        original_basis = basis_for(direction)
        moved = [change_screen(vector, endpoint_observer, ray, frequency)
                 for vector in original_basis]
        for old, new in zip(original_basis, moved):
            audit.scalar("rapidity_target_orthogonal", lorentz(new, endpoint_observer), 0.0)
            audit.scalar("rapidity_ray_orthogonal", lorentz(new, ray), 0.0)
            audit.scalar("rapidity_isometry", lorentz(new, new), lorentz(old, old))
        moved_sky = [tuple(item / frequency for item in vector) for vector in moved]
        audit.scalar("rapidity_sky_area", sky_area(*moved_sky), 1.0 / frequency ** 2)
        audit.scalar("rapidity_source_factor", forward_area / sky_area(*moved_sky),
                     frequency ** 2 * forward_area)
        smooth_cases += 1

    epsilon = 1.0e-4
    for offset in (-epsilon, 0.0, epsilon):
        length = math.pi + offset
        rank_one_det = math.sin(length) * math.sinh(length)
        rank_zero_det = math.sin(length) ** 2
        if offset == 0.0:
            audit.scalar("rank_one_exact_zero", rank_one_det, 0.0, ZERO_TOL)
            audit.scalar("rank_zero_exact_zero", rank_zero_det, 0.0, ZERO_TOL)
    rank_one_minus = math.sin(math.pi - epsilon) * math.sinh(math.pi - epsilon)
    rank_one_plus = math.sin(math.pi + epsilon) * math.sinh(math.pi + epsilon)
    rank_zero_minus = math.sin(math.pi - epsilon) ** 2
    rank_zero_plus = math.sin(math.pi + epsilon) ** 2
    audit.require("independent_rank_one_flip", rank_one_minus * rank_one_plus < 0.0)
    audit.require("independent_rank_zero_no_flip", rank_zero_minus * rank_zero_plus > 0.0)
    audit.scalar("independent_simple_order",
                 (rank_one_plus - rank_one_minus) / (2.0 * epsilon),
                 -math.sinh(math.pi), ZERO_TOL)
    audit.scalar("independent_double_order",
                 (rank_zero_plus + rank_zero_minus) / epsilon ** 2, 2.0, ZERO_TOL)
    audit.require("smooth_cases", smooth_cases == 150)
    audit.require("near_null_cases", near_null_cases >= 20)
    audit.require("at_least_7500_checks", audit.count + 1 >= 7500)

    result = {
        "assertions": audit.count,
        "failed": audit.failures[:30],
        "maxima": audit.maxima,
        "method": "independent smooth-variable-tide RK4 and rapidity observer reconstruction; imports no production or G343-G347 code",
        "near_null_cases": near_null_cases,
        "smooth_variable_tide_cases": smooth_cases,
        "status": "PASS" if not audit.failures else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if audit.failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
