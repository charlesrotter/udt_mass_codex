#!/usr/bin/env python3
"""Implementation-distinct verification of bounded G347 observer covariance."""

from __future__ import annotations

import json
import math
import os
import random


TOL = 2.0e-7


def error(left, right):
    return abs(left - right) / max(1.0, abs(left), abs(right))


def inner(left, right):
    return -left[0] * right[0] + left[1] * right[1] + left[2] * right[2] + left[3] * right[3]


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def times(factor, vector):
    return tuple(factor * item for item in vector)


def dot3(left, right):
    return sum(a * b for a, b in zip(left, right))


def unit3(vector):
    length = math.sqrt(dot3(vector, vector))
    return tuple(item / length for item in vector)


def cross3(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def transverse_basis(direction):
    seed = (0.0, 0.0, 1.0) if abs(direction[2]) < 0.75 else (0.0, 1.0, 0.0)
    first = unit3(cross3(direction, seed))
    second = unit3(cross3(direction, first))
    return (0.0,) + first, (0.0,) + second


def rapidity_observer(rapidity, axis):
    return (math.cosh(rapidity),) + tuple(math.sinh(rapidity) * item for item in axis)


def project_screen(vector, observer, ray):
    # Orthogonal representative of the quotient class, written without using production code.
    return add(vector, times(-inner(vector, observer) / inner(ray, observer), ray))


def seen_direction(ray, observer):
    measured = -inner(ray, observer)
    return add(times(1.0 / measured, ray), times(-1.0, observer))


def observed_sky_derivative(theta, normal_frequency, ray, observer):
    varied_ray = times(normal_frequency, theta)
    measured = -inner(ray, observer)
    measured_derivative = -inner(varied_ray, observer)
    return add(
        times(1.0 / measured, varied_ray),
        times(-measured_derivative / (measured * measured), ray),
    )


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def inverse(matrix):
    value = determinant(matrix)
    return [
        [matrix[1][1] / value, -matrix[0][1] / value],
        [-matrix[1][0] / value, matrix[0][0] / value],
    ]


def transpose(matrix):
    return [[matrix[0][0], matrix[1][0]], [matrix[0][1], matrix[1][1]]]


def multiply(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def diagonal(first, second):
    return [[first, 0.0], [0.0, second]]


def simpson_log(function, low, high, panels=240):
    if panels % 2:
        panels += 1
    x0, x1 = math.log(low), math.log(high)
    step = (x1 - x0) / panels

    def pull(value):
        t_value = math.exp(value)
        return function(t_value) * t_value

    total = pull(x0) + pull(x1)
    for index in range(1, panels):
        total += (4.0 if index % 2 else 2.0) * pull(x0 + index * step)
    return total * step / 3.0


def reference_free_data(t1, t0, lam, affine):
    if lam is None:
        kappa = affine
        bp = 3.0 * (
            t1 * t1 * t0 ** (-1.0 / 3.0)
            - t1 ** (-1.0 / 3.0) * t0 * t0
        ) / (7.0 * kappa)
        bz = 3.0 * (
            t1 * t0 ** (2.0 / 3.0)
            - t1 ** (2.0 / 3.0) * t0
        ) / kappa
        return diagonal(bp, bz), kappa * t0 ** (-2.0 / 3.0), kappa * t1 ** (-2.0 / 3.0)
    h0, h1 = math.hypot(t0, lam), math.hypot(t1, lam)
    jp = simpson_log(lambda value: value ** (4.0 / 3.0) / math.hypot(value, lam) ** 3, t0, t1)
    jz = simpson_log(lambda value: value ** (-2.0 / 3.0) / math.hypot(value, lam), t0, t1)
    bp = h0 * h1 * (t0 * t1) ** (-1.0 / 3.0) * jp / affine
    bz = (t0 * t1) ** (2.0 / 3.0) * jz / affine
    omega0 = affine * t0 ** (-2.0 / 3.0) * h0
    omega1 = affine * t1 ** (-2.0 / 3.0) * h1
    return diagonal(bp, bz), omega0, omega1


def angular_area(block, frequency, source_metric=None, target_metric=None):
    identity = [[1.0, 0.0], [0.0, 1.0]]
    source_metric = identity if source_metric is None else source_metric
    target_metric = identity if target_metric is None else target_metric
    derivative = multiply(block, [[frequency * source_metric[i][j] for j in range(2)] for i in range(2)])
    return math.sqrt(determinant(target_metric)) * abs(determinant(derivative)) / math.sqrt(determinant(source_metric))


def scalar_dhat(block, frequency0, frequency1, metric0=None, metric1=None):
    identity = [[1.0, 0.0], [0.0, 1.0]]
    metric0 = identity if metric0 is None else metric0
    metric1 = identity if metric1 is None else metric1
    return 1.0 / (
        abs(determinant(block)) * frequency0 * frequency1
        * math.sqrt(determinant(metric0) * determinant(metric1))
    )


def frame_metric(frame):
    inv = inverse(frame)
    return multiply(transpose(inv), inv)


def frame_change(block, target, source):
    return multiply(multiply(target, block), transpose(source))


def random_frame(rng):
    return [
        [rng.uniform(0.65, 1.55), rng.uniform(-0.4, 0.4)],
        [rng.uniform(-0.35, 0.35), rng.uniform(0.7, 1.6)],
    ]


def finite_difference_sky(direction, basis_vector, normal_frequency, observer, step=2.0e-4):
    def value(parameter):
        rotated = tuple(
            math.cos(parameter) * direction[index]
            + math.sin(parameter) * basis_vector[index + 1]
            for index in range(3)
        )
        ray = times(normal_frequency, (1.0,) + rotated)
        return seen_direction(ray, observer)

    m2, m1, p1, p2 = value(-2.0 * step), value(-step), value(step), value(2.0 * step)
    return tuple((m2[i] - 8.0 * m1[i] + 8.0 * p1[i] - p2[i]) / (12.0 * step) for i in range(4))


class Checks:
    def __init__(self):
        self.count = 0
        self.failures = []
        self.maxima = {}

    def same(self, label, left, right, tolerance=TOL):
        value = error(left, right)
        self.count += 1
        self.maxima[label] = max(self.maxima.get(label, 0.0), value)
        if value > tolerance:
            self.failures.append({"label": label, "error": value})

    def vector(self, label, left, right, tolerance=TOL):
        for a, b in zip(left, right):
            self.same(label, a, b, tolerance)

    def true(self, label, condition):
        self.count += 1
        if not condition:
            self.failures.append({"label": label, "error": 1.0})


def main():
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")
    rng = random.Random(743471)
    checks = Checks()
    finite_difference_cases = 0
    near_null_cases = 0

    for index in range(320):
        t0 = 10.0 ** rng.uniform(-0.25, 0.35)
        t1 = t0 * 10.0 ** rng.uniform(0.04, 0.38)
        t2 = t1 * 10.0 ** rng.uniform(0.04, 0.3)
        affine = 10.0 ** rng.uniform(-0.4, 0.5)
        mode = index % 12
        if mode == 0:
            lam = 0.0
        elif mode == 1:
            lam = None
        else:
            lam = t0 * 10.0 ** rng.uniform(-2.5, 2.5)
        b10, omega0, omega1 = reference_free_data(t1, t0, lam, affine)
        b20, omega0_again, omega2 = reference_free_data(t2, t0, lam, affine)
        b21, omega1_again, omega2_again = reference_free_data(t2, t1, lam, affine)
        checks.same("shared_omega0", omega0_again, omega0)
        checks.same("shared_omega1", omega1_again, omega1)
        checks.same("shared_omega2", omega2_again, omega2)
        if lam is None:
            directions = ((0.0, 1.0, 0.0),) * 3
        else:
            directions = tuple(
                unit3((t_value, lam, 0.0))
                for t_value in (t0, t1, t2)
            )
        normal_frequencies = (omega0, omega1, omega2)
        observers = []
        dopplers = []
        for endpoint, (direction, normal_frequency) in enumerate(zip(directions, normal_frequencies)):
            axis = unit3((rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)))
            rapidity = rng.uniform(-5.1, 5.1) if endpoint < 2 else rng.uniform(-3.0, 3.0)
            observer = rapidity_observer(rapidity, axis)
            observers.append(observer)
            beta_speed = abs(math.tanh(rapidity))
            if beta_speed > 0.99:
                near_null_cases += 1
            ray = times(normal_frequency, (1.0,) + direction)
            measured = -inner(ray, observer)
            doppler = measured / normal_frequency
            dopplers.append(doppler)
            expected = math.cosh(rapidity) - math.sinh(rapidity) * dot3(axis, direction)
            checks.same("rapidity_frequency", doppler, expected)
            checks.same("rapidity_unit", inner(observer, observer), -1.0)
            checks.true("positive_frequency", measured > 0.0)
            basis = transverse_basis(direction)
            projected = [project_screen(item, observer, ray) for item in basis]
            derivatives = [observed_sky_derivative(item, normal_frequency, ray, observer) for item in basis]
            for item, projection, derivative in zip(basis, projected, derivatives):
                checks.same("projected_observer_orthogonality", inner(projection, observer), 0.0)
                checks.same("projected_ray_orthogonality", inner(projection, ray), 0.0)
                checks.same("projected_length", inner(projection, projection), inner(item, item))
                checks.vector("sky_derivative_scale", derivative, times(1.0 / doppler, projection))
            projected_gram = [[inner(projected[i], projected[j]) for j in range(2)] for i in range(2)]
            sky_gram = [[inner(derivatives[i], derivatives[j]) for j in range(2)] for i in range(2)]
            checks.same("projected_area", math.sqrt(determinant(projected_gram)), 1.0)
            checks.same("sky_area_factor", math.sqrt(determinant(sky_gram)), 1.0 / (doppler * doppler))
            if index % 8 == 0 and abs(rapidity) < 4.0:
                for item, derivative in zip(basis, derivatives):
                    numerical = finite_difference_sky(direction, item, normal_frequency, observer)
                    checks.vector("finite_difference_aberration", numerical, derivative, 3.0e-7)
                    finite_difference_cases += 1

        d0, d1, d2 = dopplers
        reverse = [[-value for value in row] for row in transpose(b10)]
        area10 = angular_area(b10, omega0)
        area01 = angular_area(reverse, omega1)
        changed10 = angular_area(b10, d0 * omega0)
        changed01 = angular_area(reverse, d1 * omega1)
        checks.same("independent_forward_factor", changed10, d0 * d0 * area10)
        checks.same("independent_reverse_factor", changed01, d1 * d1 * area01)
        checks.same("independent_reversal", changed10 / changed01, (d0 * omega0 / (d1 * omega1)) ** 2)
        old_scalar = scalar_dhat(b10, omega0, omega1)
        new_scalar = scalar_dhat(b10, d0 * omega0, d1 * omega1)
        checks.same("independent_scalar_change", new_scalar, old_scalar / (d0 * d1))
        checks.same("independent_mean", math.sqrt(changed10 * changed01), 1.0 / new_scalar)

        frame0, frame1 = random_frame(rng), random_frame(rng)
        while abs(determinant(frame0)) < 0.25:
            frame0 = random_frame(rng)
        while abs(determinant(frame1)) < 0.25:
            frame1 = random_frame(rng)
        q0, q1 = frame_metric(frame0), frame_metric(frame1)
        changed_block = frame_change(b10, frame1, frame0)
        checks.same("independent_GL2_area", angular_area(changed_block, d0 * omega0, q0, q1), changed10)
        checks.same("independent_GL2_scalar", scalar_dhat(changed_block, d0 * omega0, d1 * omega1, q0, q1), new_scalar)

        hessian = multiply(multiply(inverse(b21), b20), inverse(b10))
        hhat = abs(determinant(hessian)) / (omega1 * omega1)
        area20 = angular_area(b20, omega0)
        area21 = angular_area(b21, omega1)
        checks.same("independent_baseline_sewing", area20, hhat * area21 * area10)
        checks.same(
            "independent_changed_sewing",
            d0 * d0 * area20,
            (hhat / (d1 * d1)) * (d1 * d1 * area21) * (d0 * d0 * area10),
        )
        checks.same(
            "independent_join_frequency",
            abs(determinant(hessian)) / ((d1 * omega1) ** 2),
            hhat / (d1 * d1),
        )
        common_affine = 10.0 ** rng.uniform(-3.0, 3.0)
        scaled_b = [[item / common_affine for item in row] for row in b10]
        checks.same(
            "independent_affine_area",
            angular_area(scaled_b, common_affine * d0 * omega0),
            changed10,
        )

    checks.true("at_least_4500_checks", checks.count + 1 >= 4500)
    checks.true("near_null_independent_coverage", near_null_cases > 300)
    checks.true("finite_difference_coverage", finite_difference_cases >= 50)
    result = {
        "assertions": checks.count,
        "failed": checks.failures[:20],
        "maxima": checks.maxima,
        "method": (
            "independent rapidity-chart Lorentz reconstruction, quotient projection, five-point "
            "celestial finite differences, reference-free Simpson bilocal blocks, and explicit "
            "determinant sewing; imports no production or G340/G343/G345/G346 implementation"
        ),
        "near_null_cases": near_null_cases,
        "finite_difference_cases": finite_difference_cases,
        "status": "PASS" if not checks.failures else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if checks.failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
