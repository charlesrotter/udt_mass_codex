#!/usr/bin/env python3
"""Production checks for bounded G347 endpoint-observer covariance."""

from __future__ import annotations

import json
import math
import os
import random


PREREGISTRATION_COMMIT = "c80d2666"
LOCAL_TOL = 8.0e-10
BILOCAL_TOL = 8.0e-9
BOUNDARY_TOL = 8.0e-8
LANDING = (
    "EXACT_FINITE_TIMELIKE_ENDPOINT_OBSERVER_COVARIANCE_CLOSES"
    "__QUOTIENT_SCREEN_ISOMETRY_AND_INVERSE_FREQUENCY_SKY_CONFORMALITY"
    "__SOURCE_DOPPLER_SQUARED_DIRECTIONAL_AREAS"
    "__SQUARED_FREQUENCY_REVERSAL_INVERSE_G345_MEAN_AND_STATIONARY_SEWING_RETAIN_COVARIANT_FORM"
    "__NO_PREFERRED_OBSERVER_LIGHT_DISTANCE_POPULATION_SCALE_OR_XMAX_SELECTED"
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


def relerr(left, right):
    return abs(left - right) / max(1.0, abs(left), abs(right))


def vadd(left, right):
    return tuple(a + b for a, b in zip(left, right))


def vscale(value, vector):
    return tuple(value * item for item in vector)


def minkowski(left, right):
    return -left[0] * right[0] + sum(left[i] * right[i] for i in range(1, 4))


def spatial_dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def spatial_norm(vector):
    return math.sqrt(spatial_dot(vector, vector))


def spatial_unit(vector):
    value = spatial_norm(vector)
    if value == 0.0:
        raise ValueError("zero spatial vector")
    return tuple(item / value for item in vector)


def cross(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def screen_basis(direction):
    seeds = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    seed = min(seeds, key=lambda value: abs(spatial_dot(direction, value)))
    first = spatial_unit(cross(direction, seed))
    second = spatial_unit(cross(direction, first))
    return (0.0,) + first, (0.0,) + second


def boost_observer(beta):
    beta2 = spatial_dot(beta, beta)
    if not 0.0 <= beta2 < 1.0:
        raise ValueError("finite timelike boost required")
    gamma = 1.0 / math.sqrt(1.0 - beta2)
    return (gamma,) + tuple(gamma * item for item in beta)


def screen_representative(vector, observer, ray):
    omega = -minkowski(ray, observer)
    return vadd(vector, vscale(minkowski(vector, observer) / omega, ray))


def sky_tangent(vector, old_omega, new_observer, ray):
    delta_ray = vscale(old_omega, vector)
    new_omega = -minkowski(ray, new_observer)
    delta_omega = -minkowski(delta_ray, new_observer)
    return vadd(
        vscale(1.0 / new_omega, delta_ray),
        vscale(-delta_omega / (new_omega * new_omega), ray),
    )


def det2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def mm(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def inverse2(matrix):
    value = det2(matrix)
    if value == 0.0:
        raise ValueError("singular matrix")
    return [
        [matrix[1][1] / value, -matrix[0][1] / value],
        [-matrix[1][0] / value, matrix[0][0] / value],
    ]


def diagonal(first, second):
    return [[first, 0.0], [0.0, second]]


def metric_after(frame):
    inverse = inverse2(frame)
    return mm(transpose(inverse), inverse)


def transform_b(block, target_frame, source_frame):
    return mm(mm(target_frame, block), transpose(source_frame))


def random_frame(rng):
    angle = rng.uniform(-math.pi, math.pi)
    cosine, sine = math.cos(angle), math.sin(angle)
    rotation = [[cosine, -sine], [sine, cosine]]
    triangular = [
        [10.0 ** rng.uniform(-0.45, 0.45), rng.uniform(-0.5, 0.5)],
        [0.0, 10.0 ** rng.uniform(-0.45, 0.45)],
    ]
    if rng.random() < 0.25:
        triangular[0] = [-item for item in triangular[0]]
    return mm(rotation, triangular)


def gauss_log(function, low, high, panels=28):
    x0, x1 = math.log(low), math.log(high)
    width = (x1 - x0) / panels
    total = 0.0
    for panel in range(panels):
        middle = x0 + (panel + 0.5) * width
        half = 0.5 * width
        for node, weight in zip(GL_X, GL_W):
            x_value = middle + half * node
            t_value = math.exp(x_value)
            total += half * weight * function(t_value) * t_value
    return total


def hnorm(t_value, rho, t_reference):
    return math.sqrt(rho * t_value * t_value + (1.0 - rho) * t_reference * t_reference)


def normal_frequency(t_value, rho, nu, t_reference):
    return (
        nu * t_reference ** (-1.0 / 3.0) * t_value ** (-2.0 / 3.0)
        * hnorm(t_value, rho, t_reference)
    )


def bilocal_b(t1, t0, rho, nu, t_reference):
    h0 = hnorm(t0, rho, t_reference)
    h1 = hnorm(t1, rho, t_reference)
    yp0, yp1 = t0 ** (-1.0 / 3.0) * h0, t1 ** (-1.0 / 3.0) * h1
    yz0, yz1 = t0 ** (2.0 / 3.0), t1 ** (2.0 / 3.0)
    ip = gauss_log(
        lambda value: value ** (4.0 / 3.0)
        / hnorm(value, rho, t_reference) ** 3,
        t0, t1,
    )
    iz = gauss_log(
        lambda value: value ** (-2.0 / 3.0)
        / hnorm(value, rho, t_reference),
        t0, t1,
    )
    factor = t_reference ** (1.0 / 3.0) / nu
    return diagonal(factor * yp0 * yp1 * ip, factor * yz0 * yz1 * iz)


def ray_direction(t_value, rho, t_reference):
    if rho == 1.0:
        return (1.0, 0.0, 0.0)
    if rho == 0.0:
        return (0.0, 1.0, 0.0)
    lam = t_reference * math.sqrt((1.0 - rho) / rho)
    value = math.hypot(t_value, lam)
    return (t_value / value, lam / value, 0.0)


def angular_area(block, source_frequency, source_metric=None, target_metric=None):
    identity = [[1.0, 0.0], [0.0, 1.0]]
    source_metric = identity if source_metric is None else source_metric
    target_metric = identity if target_metric is None else target_metric
    return (
        source_frequency * source_frequency * abs(det2(block))
        * math.sqrt(det2(source_metric) * det2(target_metric))
    )


def dhat(block, omega0, omega1, q0=None, q1=None):
    identity = [[1.0, 0.0], [0.0, 1.0]]
    q0 = identity if q0 is None else q0
    q1 = identity if q1 is None else q1
    return 1.0 / (
        abs(det2(block)) * omega0 * omega1
        * math.sqrt(det2(q0) * det2(q1))
    )


def stationary_hessian(block21, block10, block20):
    return mm(mm(inverse2(block21), block20), inverse2(block10))


def join_scalar(hessian, middle_frequency, middle_metric=None):
    identity = [[1.0, 0.0], [0.0, 1.0]]
    middle_metric = identity if middle_metric is None else middle_metric
    return abs(det2(hessian)) / (
        middle_frequency * middle_frequency * det2(middle_metric)
    )


def random_beta(rng, index):
    direction = spatial_unit((rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)))
    if index % 4 != 0:
        speed = 1.0 - 10.0 ** rng.uniform(-6.0, -2.05)
    elif index % 8 == 0:
        speed = rng.uniform(0.0, 0.82)
    else:
        speed = 0.0
    return tuple(speed * item for item in direction)


class Recorder:
    def __init__(self):
        self.assertions = 0
        self.failed = []
        self.maxima = {}

    def check(self, name, left, right, tolerance):
        error = relerr(left, right)
        self.assertions += 1
        self.maxima[name] = max(self.maxima.get(name, 0.0), error)
        if error > tolerance:
            self.failed.append({"name": name, "error": error, "left": left, "right": right})

    def vector(self, name, left, right, tolerance):
        for a, b in zip(left, right):
            self.check(name, a, b, tolerance)

    def truth(self, name, condition):
        self.assertions += 1
        if not condition:
            self.failed.append({"name": name, "error": 1.0})


def observer_checks(recorder, ray, old_omega, direction, beta, beta_third):
    old = (1.0, 0.0, 0.0, 0.0)
    new = boost_observer(beta)
    third = boost_observer(beta_third)
    omega_new = -minkowski(ray, new)
    gamma = new[0]
    doppler = omega_new / old_omega
    expected_doppler = gamma * (1.0 - spatial_dot(beta, direction))
    recorder.check("observer_unit", minkowski(new, new), -1.0, LOCAL_TOL)
    recorder.check("frequency_doppler", doppler, expected_doppler, BOUNDARY_TOL)
    recorder.truth("frequency_positive", omega_new > 0.0)
    basis = screen_basis(direction)
    mapped = [screen_representative(item, new, ray) for item in basis]
    for item in mapped:
        recorder.check("screen_orthogonal_observer", minkowski(item, new), 0.0, BOUNDARY_TOL)
        recorder.check("screen_orthogonal_ray", minkowski(item, ray), 0.0, BOUNDARY_TOL)
    for row in range(2):
        for column in range(2):
            recorder.check(
                "screen_isometry",
                minkowski(mapped[row], mapped[column]),
                1.0 if row == column else 0.0,
                BOUNDARY_TOL,
            )
    for original, changed in zip(basis, mapped):
        returned = screen_representative(changed, old, ray)
        recorder.vector("screen_inverse", returned, original, BOUNDARY_TOL)
        through = screen_representative(changed, third, ray)
        direct = screen_representative(original, third, ray)
        recorder.vector("screen_transitivity", through, direct, BOUNDARY_TOL)
    sky = [sky_tangent(item, old_omega, new, ray) for item in basis]
    expected_sky = [vscale(1.0 / doppler, item) for item in mapped]
    for actual, expected in zip(sky, expected_sky):
        recorder.vector("sky_tangent", actual, expected, BOUNDARY_TOL)
        recorder.check("sky_tangent_observer", minkowski(actual, new), 0.0, BOUNDARY_TOL)
    gram = [[minkowski(sky[i], sky[j]) for j in range(2)] for i in range(2)]
    solid_factor = math.sqrt(max(0.0, det2(gram)))
    recorder.check("sky_solid_angle", solid_factor, 1.0 / (doppler * doppler), BOUNDARY_TOL)
    return doppler


def main():
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")
    rng = random.Random(3470904)
    recorder = Recorder()
    near_null_boosts = 0
    principal_longitudinal = 0
    principal_transverse = 0
    noninvariant_examples = 0

    for index in range(800):
        base = 10.0 ** rng.uniform(-0.35, 0.45)
        t0 = base
        t1 = t0 * 10.0 ** rng.uniform(0.035, 0.42)
        t2 = t1 * 10.0 ** rng.uniform(0.035, 0.35)
        t_reference = 10.0 ** rng.uniform(-0.3, 0.5)
        nu = 10.0 ** rng.uniform(-0.5, 0.6)
        mode = index % 10
        if mode == 0:
            rho = 1.0
            principal_longitudinal += 1
        elif mode == 1:
            rho = 0.0
            principal_transverse += 1
        else:
            lam = 10.0 ** rng.uniform(-2.8, 2.8) * t_reference
            rho = t_reference * t_reference / (t_reference * t_reference + lam * lam)

        omega0 = normal_frequency(t0, rho, nu, t_reference)
        omega1 = normal_frequency(t1, rho, nu, t_reference)
        omega2 = normal_frequency(t2, rho, nu, t_reference)
        direction0 = ray_direction(t0, rho, t_reference)
        direction1 = ray_direction(t1, rho, t_reference)
        direction2 = ray_direction(t2, rho, t_reference)
        ray0 = vscale(omega0, (1.0,) + direction0)
        ray1 = vscale(omega1, (1.0,) + direction1)
        ray2 = vscale(omega2, (1.0,) + direction2)
        recorder.check("ray0_null", minkowski(ray0, ray0), 0.0, LOCAL_TOL)
        recorder.check("ray1_null", minkowski(ray1, ray1), 0.0, LOCAL_TOL)
        recorder.check("ray2_null", minkowski(ray2, ray2), 0.0, LOCAL_TOL)

        beta0 = random_beta(rng, 2 * index)
        beta1 = random_beta(rng, 2 * index + 1)
        beta2 = random_beta(rng, 2 * index + 1601)
        third0 = random_beta(rng, 4 * index + 3203)
        third1 = random_beta(rng, 4 * index + 3205)
        if spatial_norm(beta0) > 0.99:
            near_null_boosts += 1
        if spatial_norm(beta1) > 0.99:
            near_null_boosts += 1
        d0 = observer_checks(recorder, ray0, omega0, direction0, beta0, third0)
        d1 = observer_checks(recorder, ray1, omega1, direction1, beta1, third1)
        v2 = boost_observer(beta2)
        d2 = -minkowski(ray2, v2) / omega2

        b10 = bilocal_b(t1, t0, rho, nu, t_reference)
        b01 = [[-value for value in row] for row in transpose(b10)]
        b21 = bilocal_b(t2, t1, rho, nu, t_reference)
        b20 = bilocal_b(t2, t0, rho, nu, t_reference)
        area10 = angular_area(b10, omega0)
        area01 = angular_area(b01, omega1)
        changed10 = angular_area(b10, d0 * omega0)
        changed01 = angular_area(b01, d1 * omega1)
        recorder.check("forward_source_doppler_squared", changed10, d0 * d0 * area10, BOUNDARY_TOL)
        recorder.check("reverse_source_doppler_squared", changed01, d1 * d1 * area01, BOUNDARY_TOL)
        recorder.check(
            "changed_frequency_reversal",
            changed10 / changed01,
            (d0 * omega0 / (d1 * omega1)) ** 2,
            BOUNDARY_TOL,
        )
        old_dhat = dhat(b10, omega0, omega1)
        new_dhat = dhat(b10, d0 * omega0, d1 * omega1)
        recorder.check("changed_G345", new_dhat, old_dhat / (d0 * d1), BOUNDARY_TOL)
        recorder.check(
            "changed_geometric_mean",
            math.sqrt(changed10 * changed01),
            1.0 / new_dhat,
            BOUNDARY_TOL,
        )
        if abs(d0 - 1.0) > 1.0e-4 and relerr(changed10, area10) > 1.0e-6:
            noninvariant_examples += 1

        affine = 10.0 ** rng.uniform(-4.0, 4.0)
        affine_b = [[value / affine for value in row] for row in b10]
        recorder.check(
            "common_affine_area",
            angular_area(affine_b, affine * d0 * omega0),
            changed10,
            BOUNDARY_TOL,
        )
        recorder.check(
            "common_affine_doppler",
            (affine * d0 * omega0) / (affine * omega0),
            d0,
            LOCAL_TOL,
        )

        frame0, frame1 = random_frame(rng), random_frame(rng)
        q0, q1 = metric_after(frame0), metric_after(frame1)
        transformed = transform_b(b10, frame1, frame0)
        recorder.check(
            "observer_plus_GL2_forward_area",
            angular_area(transformed, d0 * omega0, q0, q1),
            changed10,
            BOUNDARY_TOL,
        )
        transformed_reverse = transform_b(b01, frame0, frame1)
        recorder.check(
            "observer_plus_GL2_reverse_area",
            angular_area(transformed_reverse, d1 * omega1, q1, q0),
            changed01,
            BOUNDARY_TOL,
        )
        recorder.check(
            "observer_plus_GL2_G345",
            dhat(transformed, d0 * omega0, d1 * omega1, q0, q1),
            new_dhat,
            BOUNDARY_TOL,
        )

        hessian = stationary_hessian(b21, b10, b20)
        hhat = join_scalar(hessian, omega1)
        area20 = angular_area(b20, omega0)
        area21 = angular_area(b21, omega1)
        recorder.check("baseline_stationary_sewing", area20, hhat * area21 * area10, BILOCAL_TOL)
        changed20 = d0 * d0 * area20
        changed21 = d1 * d1 * area21
        changed_hhat = hhat / (d1 * d1)
        recorder.check(
            "changed_stationary_sewing",
            changed20,
            changed_hhat * changed21 * changed10,
            BOUNDARY_TOL,
        )
        recorder.check(
            "changed_join_factor",
            join_scalar(hessian, d1 * omega1),
            changed_hhat,
            BOUNDARY_TOL,
        )

        if rho == 1.0:
            difference = t1 ** (2.0 / 3.0) - t0 ** (2.0 / 3.0)
            expected10 = 2.25 * t0 ** (2.0 / 3.0) * difference * difference
            expected01 = 2.25 * t1 ** (2.0 / 3.0) * difference * difference
            recorder.check("longitudinal_forward", area10, expected10, BILOCAL_TOL)
            recorder.check("longitudinal_reverse", area01, expected01, BILOCAL_TOL)
        elif rho == 0.0:
            product = abs(
                (t1 ** (7.0 / 3.0) - t0 ** (7.0 / 3.0))
                * (t1 ** (1.0 / 3.0) - t0 ** (1.0 / 3.0))
            )
            expected10 = 9.0 * product * t1 ** (1.0 / 3.0) / (7.0 * t0)
            expected01 = 9.0 * product * t0 ** (1.0 / 3.0) / (7.0 * t1)
            recorder.check("transverse_forward", area10, expected10, BILOCAL_TOL)
            recorder.check("transverse_reverse", area01, expected01, BILOCAL_TOL)

    recorder.truth("at_least_1000_near_null_boosts", near_null_boosts >= 1000)
    recorder.truth("both_principal_families", principal_longitudinal > 0 and principal_transverse > 0)
    recorder.truth("observer_dependence_exhibited", noninvariant_examples >= 500)
    recorder.truth("at_least_12000_checks", recorder.assertions + 1 >= 12000)

    result = {
        "assertions": recorder.assertions,
        "failed": recorder.failed[:20],
        "landing": LANDING,
        "maxima": recorder.maxima,
        "near_null_boosts": near_null_boosts,
        "noninvariant_examples": noninvariant_examples,
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "principal_cases": {
            "longitudinal": principal_longitudinal,
            "transverse": principal_transverse,
        },
        "selected_alternatives": ["A", "Q1", "S1", "A1", "R1", "G1", "N1", "B1", "P1"],
        "status": "PASS" if not recorder.failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if recorder.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
