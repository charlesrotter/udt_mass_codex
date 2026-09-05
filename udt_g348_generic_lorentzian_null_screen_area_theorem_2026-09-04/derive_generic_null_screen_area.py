#!/usr/bin/env python3
"""Production checks for the preregistered G348 generic null-screen theorem."""

from __future__ import annotations

import json
import math
import random


PREREGISTRATION_COMMIT = "23e50369"
ALG_TOL = 2.0e-9
ZERO_TOL = 2.0e-6
LANDING = (
    "GENERIC_METRIC_NULL_SCREEN_AREA_THEOREM_CLOSES_WITH_SINGULAR_STRATA"
    "__LEVI_CIVITA_QUOTIENT_CONNECTION_SELF_ADJOINT_TIDE_AND_SYMPLECTIC_FLOW"
    "__SOURCE_FREQUENCY_SQUARED_DIRECTIONAL_AREAS_AND_GENERIC_OBSERVER_COVARIANCE"
    "__WRONSKIAN_FORCES_CONJUGATE_ZERO_ORDER_EQUAL_TO_KERNEL_DIMENSION"
    "__TYPE_I_GENERATOR_INVERSE_SCALAR_AND_STATIONARY_SEWING_ARE_CHARTWISE"
    "__NO_LIGHT_DISTANCE_POPULATION_HISTORY_SCALE_OR_XMAX_SELECTED"
)


def eye(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matsub(a, b):
    return [[x - y for x, y in zip(arow, brow)] for arow, brow in zip(a, b)]


def matscale(value, a):
    return [[value * item for item in row] for row in a]


def maxabs(a):
    return max(abs(item) for row in a for item in row)


def inverse(a):
    n = len(a)
    work = [row[:] + unit[:] for row, unit in zip(a, eye(n))]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(work[row][col]))
        if abs(work[pivot][col]) < 1.0e-14:
            raise ValueError("singular matrix")
        work[col], work[pivot] = work[pivot], work[col]
        value = work[col][col]
        work[col] = [item / value for item in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            work[row] = [x - factor * y for x, y in zip(work[row], work[col])]
    return [row[n:] for row in work]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def block(a, b, c, d):
    return [a[0] + b[0], a[1] + b[1], c[0] + d[0], c[1] + d[1]]


def getblock(a, row, col):
    return [[a[2 * row + i][2 * col + j] for j in range(2)] for i in range(2)]


def rotation(theta):
    c = math.cos(theta)
    s = math.sin(theta)
    return [[c, -s], [s, c]]


def spectral_pair(tide):
    a, b, d = tide[0][0], tide[0][1], tide[1][1]
    theta = 0.5 * math.atan2(2.0 * b, a - d)
    radius = math.hypot(0.5 * (a - d), b)
    middle = 0.5 * (a + d)
    return rotation(theta), (middle + radius, middle - radius)


def scalar_cs(value, length):
    if value > 1.0e-12:
        root = math.sqrt(value)
        return math.cos(root * length), math.sin(root * length) / root
    if value < -1.0e-12:
        root = math.sqrt(-value)
        return math.cosh(root * length), math.sinh(root * length) / root
    return 1.0, length


def constant_tide_step(tide, length):
    rot, values = spectral_pair(tide)
    rt = transpose(rot)
    cs = [scalar_cs(value, length) for value in values]
    cdiag = [[cs[0][0], 0.0], [0.0, cs[1][0]]]
    sdiag = [[cs[0][1], 0.0], [0.0, cs[1][1]]]
    kdiag = [[-values[0] * cs[0][1], 0.0], [0.0, -values[1] * cs[1][1]]]
    cmat = matmul(matmul(rot, cdiag), rt)
    smat = matmul(matmul(rot, sdiag), rt)
    kmat = matmul(matmul(rot, kdiag), rt)
    return block(cmat, smat, kmat, cmat)


def flow(segments):
    result = eye(4)
    for tide, length in segments:
        result = matmul(constant_tide_step(tide, length), result)
    return result


J4 = [
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
    [-1.0, 0.0, 0.0, 0.0],
    [0.0, -1.0, 0.0, 0.0],
]


class Recorder:
    def __init__(self):
        self.assertions = 0
        self.failed = []
        self.maxima = {}

    def check(self, name, left, right, tolerance=ALG_TOL):
        self.assertions += 1
        error = abs(left - right) / max(1.0, abs(left), abs(right))
        self.maxima[name] = max(self.maxima.get(name, 0.0), error)
        if not math.isfinite(error) or error > tolerance:
            self.failed.append({"name": name, "error": error, "left": left, "right": right})

    def matrix(self, name, left, right, tolerance=ALG_TOL):
        for i in range(len(left)):
            for j in range(len(left[0])):
                self.check(name, left[i][j], right[i][j], tolerance)

    def truth(self, name, condition):
        self.assertions += 1
        if not condition:
            self.failed.append({"name": name, "condition": False})


def random_tide(rng):
    a = rng.uniform(-2.0, 3.0)
    d = rng.uniform(-2.0, 3.0)
    b = rng.uniform(-1.4, 1.4)
    return [[a, b], [b, d]]


def random_gl2(rng, allow_reflection=False):
    while True:
        angle = rng.uniform(-math.pi, math.pi)
        rot = rotation(angle)
        scales = [math.exp(rng.uniform(-0.7, 0.7)), math.exp(rng.uniform(-0.7, 0.7))]
        shear = rng.uniform(-0.5, 0.5)
        core = [[scales[0], shear], [0.0, scales[1]]]
        value = matmul(rot, core)
        if allow_reflection and rng.random() < 0.5:
            value[0][0] *= -1.0
            value[1][0] *= -1.0
        if abs(det2(value)) > 0.1:
            return value


def canonical_frame(r):
    zero = [[0.0, 0.0], [0.0, 0.0]]
    return block(r, zero, zero, transpose(inverse(r)))


def metric_in_new_frame(r):
    rinv = inverse(r)
    return matmul(transpose(rinv), rinv)


def area_from_components(bmat, omega, q0, q1):
    return omega * omega * abs(det2(bmat)) * math.sqrt(det2(q0) * det2(q1))


def minkowski(left, right):
    return -left[0] * right[0] + sum(left[i] * right[i] for i in range(1, 4))


def spatial_dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def normalize_spatial(value):
    norm = math.sqrt(spatial_dot(value, value))
    return tuple(item / norm for item in value)


def cross(left, right):
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def screen_basis(direction):
    seed = min(((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
               key=lambda item: abs(spatial_dot(item, direction)))
    first = normalize_spatial(cross(direction, seed))
    second = normalize_spatial(cross(direction, first))
    return (0.0,) + first, (0.0,) + second


def observer(beta):
    beta2 = spatial_dot(beta, beta)
    gamma = 1.0 / math.sqrt(1.0 - beta2)
    return (gamma,) + tuple(gamma * item for item in beta)


def screen_change(vector, target, kvec, omega_target):
    coefficient = minkowski(vector, target) / omega_target
    return tuple(vector[i] + coefficient * kvec[i] for i in range(4))


def gram_area(first, second):
    determinant = (
        minkowski(first, first) * minkowski(second, second)
        - minkowski(first, second) ** 2
    )
    return math.sqrt(max(0.0, determinant))


def main():
    rng = random.Random(34820260904)
    recorder = Recorder()
    noncommuting_profiles = 0
    sewing_cases = 0
    reflected_frames = 0
    observer_cases = 0

    for case in range(420):
        segments = []
        for _ in range(3 + case % 4):
            segments.append((random_tide(rng), rng.uniform(0.025, 0.16)))
        if any(abs(tide[0][1]) > 0.05 for tide, _ in segments):
            noncommuting_profiles += 1
        forward = flow(segments)
        backward = flow([(tide, -length) for tide, length in reversed(segments)])

        recorder.matrix("symplectic", matmul(matmul(transpose(forward), J4), forward), J4)
        recorder.matrix("direct_reversal", matmul(backward, forward), eye(4))
        recorder.matrix("inverse_reversal", backward, inverse(forward))
        b10 = getblock(forward, 0, 1)
        b01 = getblock(backward, 0, 1)
        recorder.matrix("B_reverse_adjoint", b01, matscale(-1.0, transpose(b10)))
        recorder.check("absolute_determinant_reversal", abs(det2(b01)), abs(det2(b10)))

        r0 = random_gl2(rng, allow_reflection=True)
        r1 = random_gl2(rng, allow_reflection=True)
        if det2(r0) * det2(r1) < 0.0:
            reflected_frames += 1
        p0 = canonical_frame(r0)
        p1 = canonical_frame(r1)
        changed = matmul(matmul(p1, forward), inverse(p0))
        bchanged = getblock(changed, 0, 1)
        expected_b = matmul(matmul(r1, b10), transpose(r0))
        recorder.matrix("GL2_B", bchanged, expected_b)
        q0 = metric_in_new_frame(r0)
        q1 = metric_in_new_frame(r1)

        omega0 = math.exp(rng.uniform(-1.0, 1.0))
        omega1 = math.exp(rng.uniform(-1.0, 1.0))
        area10 = area_from_components(b10, omega0, eye(2), eye(2))
        area01 = area_from_components(b01, omega1, eye(2), eye(2))
        area_changed_coordinates = area_from_components(bchanged, omega0, q0, q1)
        recorder.check("GL2_unsigned_area", area_changed_coordinates, area10)
        if det2(b10) != 0.0:
            oriented_ratio = det2(bchanged) / det2(b10)
            recorder.check("GL2_oriented_density", oriented_ratio, det2(r1) * det2(r0))
        recorder.check("directional_reversal", area10 / area01, (omega0 / omega1) ** 2)

        affine = math.exp(rng.uniform(-1.5, 1.5))
        sa = block(eye(2), [[0.0, 0.0], [0.0, 0.0]],
                   [[0.0, 0.0], [0.0, 0.0]], matscale(affine, eye(2)))
        affine_map = matmul(matmul(sa, forward), inverse(sa))
        baffine = getblock(affine_map, 0, 1)
        recorder.matrix("affine_B", baffine, matscale(1.0 / affine, b10))
        recorder.check(
            "affine_area",
            area_from_components(baffine, affine * omega0, eye(2), eye(2)),
            area10,
        )

        d0 = math.exp(rng.uniform(-1.2, 1.2))
        d1 = math.exp(rng.uniform(-1.2, 1.2))
        area10_new = d0 * d0 * area10
        area01_new = d1 * d1 * area01
        recorder.check(
            "observer_changed_reversal",
            area10_new / area01_new,
            (d0 * omega0 / (d1 * omega1)) ** 2,
        )
        if abs(det2(b10)) > 1.0e-10:
            dhat = 1.0 / (abs(det2(b10)) * omega0 * omega1)
            dhat_new = dhat / (d0 * d1)
            recorder.check(
                "observer_changed_geometric_mean",
                math.sqrt(area10_new * area01_new),
                1.0 / dhat_new,
            )

        split = len(segments) // 2
        m10 = flow(segments[:split])
        m21 = flow(segments[split:])
        m20 = matmul(m21, m10)
        recorder.matrix("composition", m20, forward)
        b10s = getblock(m10, 0, 1)
        b21s = getblock(m21, 0, 1)
        b20s = getblock(m20, 0, 1)
        if min(abs(det2(b10s)), abs(det2(b21s)), abs(det2(b20s))) > 1.0e-9:
            hessian = matmul(matmul(inverse(b21s), b20s), inverse(b10s))
            recorder.check(
                "stationary_determinant_sewing",
                abs(det2(b20s)),
                abs(det2(hessian) * det2(b21s) * det2(b10s)),
            )
            area20 = omega0 * omega0 * abs(det2(b20s))
            area21 = omega1 * omega1 * abs(det2(b21s))
            area10s = omega0 * omega0 * abs(det2(b10s))
            hhat = abs(det2(hessian)) / (omega1 * omega1)
            recorder.check("stationary_area_sewing", area20, hhat * area21 * area10s)
            sewing_cases += 1

        direction = normalize_spatial((rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0),
                                       rng.uniform(-1.0, 1.0)))
        basis = screen_basis(direction)
        if case % 7 == 0:
            speed = 1.0 - 10.0 ** rng.uniform(-5.0, -3.0)
        else:
            speed = rng.uniform(0.0, 0.97)
        beta_direction = normalize_spatial((rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0),
                                            rng.uniform(-1.0, 1.0)))
        beta = tuple(speed * item for item in beta_direction)
        target = observer(beta)
        kvec = (1.0,) + direction
        doppler = -minkowski(kvec, target)
        changed_basis = [screen_change(item, target, kvec, doppler) for item in basis]
        for original, updated in zip(basis, changed_basis):
            recorder.check("observer_screen_target_orthogonal", minkowski(updated, target), 0.0)
            recorder.check("observer_screen_null_orthogonal", minkowski(updated, kvec), 0.0)
            recorder.check("observer_screen_norm", minkowski(updated, updated),
                           minkowski(original, original))
        recorder.check("observer_screen_inner", minkowski(changed_basis[0], changed_basis[1]), 0.0)
        sky_basis = [tuple(item / doppler for item in vector) for vector in changed_basis]
        recorder.check("observer_sky_area", gram_area(*sky_basis), 1.0 / (doppler * doppler))
        recorder.check("observer_source_area", doppler * doppler * area10,
                       area10 / gram_area(*sky_basis))
        observer_cases += 1

    pi = math.pi
    rank_one = constant_tide_step([[1.0, 0.0], [0.0, -1.0]], pi)
    rank_zero = constant_tide_step([[1.0, 0.0], [0.0, 1.0]], pi)
    coincidence = constant_tide_step([[2.0, 0.3], [0.3, -0.7]], 0.0)
    negative = constant_tide_step([[-1.0, 0.0], [0.0, -4.0]], 0.8)
    b_rank_one = getblock(rank_one, 0, 1)
    b_rank_zero = getblock(rank_zero, 0, 1)
    d_rank_one = getblock(rank_one, 1, 1)
    recorder.truth("rank_one_witness", abs(det2(b_rank_one)) < ZERO_TOL
                   and maxabs(b_rank_one) > 1.0)
    recorder.truth("rank_zero_witness", maxabs(b_rank_zero) < ZERO_TOL)
    recorder.matrix("rank_one_full_flow_regular", matmul(inverse(rank_one), rank_one), eye(4))
    recorder.matrix("rank_zero_full_flow_regular", matmul(inverse(rank_zero), rank_zero), eye(4))
    recorder.matrix("coincidence_full_flow", coincidence, eye(4))
    recorder.truth("negative_tide_nonconjugate", det2(getblock(negative, 0, 1)) > 0.0)
    recorder.check("rank_one_kernel_derivative_nonzero", abs(d_rank_one[0][0]), 1.0, ZERO_TOL)
    recorder.check("rank_one_derivative_orthogonal_to_image", d_rank_one[1][0], 0.0, ZERO_TOL)

    epsilon = 1.0e-4
    r1_before = det2(getblock(constant_tide_step([[1.0, 0.0], [0.0, -1.0]], pi - epsilon), 0, 1))
    r1_after = det2(getblock(constant_tide_step([[1.0, 0.0], [0.0, -1.0]], pi + epsilon), 0, 1))
    r0_before = det2(getblock(constant_tide_step([[1.0, 0.0], [0.0, 1.0]], pi - epsilon), 0, 1))
    r0_after = det2(getblock(constant_tide_step([[1.0, 0.0], [0.0, 1.0]], pi + epsilon), 0, 1))
    recorder.truth("rank_one_sign_flip", r1_before * r1_after < 0.0)
    recorder.truth("rank_zero_no_sign_flip", r0_before * r0_after > 0.0)
    recorder.check(
        "rank_one_centered_first_derivative",
        (r1_after - r1_before) / (2.0 * epsilon),
        -math.sinh(pi),
        ZERO_TOL,
    )
    recorder.check(
        "rank_zero_centered_second_derivative",
        (r0_after + r0_before) / (epsilon * epsilon),
        2.0,
        ZERO_TOL,
    )

    recorder.truth("noncommuting_profiles_covered", noncommuting_profiles >= 400)
    recorder.truth("stationary_cases_covered", sewing_cases >= 400)
    recorder.truth("reflected_frames_covered", reflected_frames >= 150)
    recorder.truth("observer_cases_covered", observer_cases == 420)
    recorder.truth("at_least_20000_checks", recorder.assertions + 1 >= 20000)

    result = {
        "assertions": recorder.assertions,
        "failed": recorder.failed[:30],
        "landing": LANDING,
        "maxima": recorder.maxima,
        "noncommuting_profiles": noncommuting_profiles,
        "observer_cases": observer_cases,
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "reflected_frames": reflected_frames,
        "selected_alternatives": ["A", "Q1", "J1", "R1", "A1", "O1", "C1", "X1", "S1", "W1", "P1"],
        "sewing_cases": sewing_cases,
        "status": "PASS" if not recorder.failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if recorder.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
