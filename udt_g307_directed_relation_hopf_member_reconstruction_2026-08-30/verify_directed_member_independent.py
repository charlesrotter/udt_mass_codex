#!/usr/bin/env python3
"""Implementation-distinct numerical replay using oriented two-plane operators."""

from __future__ import annotations

import json
import math
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_VERIFICATION.json"
SEED = 3070830


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def scale(c, a):
    return [c * x for x in a]


def add(*vectors):
    return [sum(values) for values in zip(*vectors)]


def norm(a):
    return math.sqrt(dot(a, a))


def unit(a):
    n = norm(a)
    if n < 1e-10:
        raise ValueError("degenerate vector")
    return scale(1.0 / n, a)


def project_out(a, basis):
    out = list(a)
    for vector in basis:
        out = add(out, scale(-dot(out, vector), vector))
    return out


def qmul(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return [
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    ]


def qconj(q):
    return [q[0], -q[1], -q[2], -q[3]]


def determinant(a):
    matrix = [list(row) for row in a]
    value = 1.0
    for column in range(4):
        pivot = max(range(column, 4), key=lambda row: abs(matrix[row][column]))
        if pivot != column:
            matrix[pivot], matrix[column] = matrix[column], matrix[pivot]
            value *= -1.0
        p = matrix[column][column]
        value *= p
        for row in range(column + 1, 4):
            factor = matrix[row][column] / p
            for j in range(column + 1, 4):
                matrix[row][j] -= factor * matrix[column][j]
    return value


def outer(a, b):
    return [[x * y for y in b] for x in a]


def madd(*matrices):
    return [[sum(matrix[i][j] for matrix in matrices) for j in range(4)] for i in range(4)]


def mscale(c, a):
    return [[c * x for x in row] for row in a]


def matvec(a, v):
    return [dot(row, v) for row in a]


def action_matrix(action):
    basis = (
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    )
    columns = [action(vector) for vector in basis]
    return [[columns[j][i] for j in range(4)] for i in range(4)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def transpose(a):
    return [[a[j][i] for j in range(4)] for i in range(4)]


def maxerr(a, b):
    if isinstance(a[0], list):
        return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))
    return max(abs(x - y) for x, y in zip(a, b))


def complex_operator(q, v, w, z, sign):
    route = madd(outer(v, q), mscale(-1.0, outer(q, v)))
    screen = madd(outer(z, w), mscale(-1.0, outer(w, z)))
    return madd(route, mscale(sign, screen))


def main():
    rng = random.Random(SEED)
    checks = 0
    worst = 0.0

    def check_error(actual, expected, label):
        nonlocal checks, worst
        error = maxerr(actual, expected)
        worst = max(worst, error)
        assert error < 2e-10, (label, error)
        checks += 1

    def check_scalar(actual, expected, label):
        nonlocal checks, worst
        error = abs(actual - expected)
        worst = max(worst, error)
        assert error < 2e-10, (label, error)
        checks += 1

    identity = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    imag_basis = (
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    )
    samples = 1000
    radii = (0.125, 0.5, 1.0, 3.25, 11.0)
    for case in range(samples):
        q = unit([rng.gauss(0.0, 1.0) for _ in range(4)])
        v = unit(project_out([rng.gauss(0.0, 1.0) for _ in range(4)], [q]))
        w = unit(project_out([rng.gauss(0.0, 1.0) for _ in range(4)], [q, v]))
        z = unit(project_out([rng.gauss(0.0, 1.0) for _ in range(4)], [q, v, w]))
        frame_rows = [[q[j], v[j], w[j], z[j]] for j in range(4)]
        if determinant(frame_rows) < 0.0:
            z = scale(-1.0, z)

        plus = complex_operator(q, v, w, z, 1.0)
        minus = complex_operator(q, v, w, z, -1.0)

        # Reconstruct each family member from (q,v) through the two independent
        # imaginary-quaternion evaluation maps, not from the route/screen operators.
        left_images = [qmul(axis, q) for axis in imag_basis]
        right_images = [qmul(q, axis) for axis in imag_basis]
        gram_identity = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
        left_gram = [[dot(left_images[i], left_images[j]) for j in range(3)] for i in range(3)]
        right_gram = [[dot(right_images[i], right_images[j]) for j in range(3)] for i in range(3)]
        check_error(left_gram, gram_identity, "left evaluation isometry")
        check_error(right_gram, gram_identity, "right evaluation isometry")

        left_coefficients = [dot(v, image) for image in left_images]
        right_coefficients = [dot(v, image) for image in right_images]
        reconstructed_left_v = [sum(left_coefficients[j] * left_images[j][i] for j in range(3)) for i in range(4)]
        reconstructed_right_v = [sum(right_coefficients[j] * right_images[j][i] for j in range(3)) for i in range(4)]
        check_error(reconstructed_left_v, v, "left unique coefficient solve")
        check_error(reconstructed_right_v, v, "right unique coefficient solve")

        u_left = [0.0] + left_coefficients
        u_right = [0.0] + right_coefficients
        check_scalar(u_left[0], 0.0, "left pure imaginary")
        check_scalar(u_right[0], 0.0, "right pure imaginary")
        check_scalar(dot(u_left, u_left), 1.0, "left unit coefficient")
        check_scalar(dot(u_right, u_right), 1.0, "right unit coefficient")
        check_error(qmul(u_left, q), v, "left reconstructed field value")
        check_error(qmul(q, u_right), v, "right reconstructed field value")
        check_error(u_left, qmul(v, qconj(q)), "left closed reconstruction formula")
        check_error(u_right, qmul(qconj(q), v), "right closed reconstruction formula")

        reconstructed_left = action_matrix(lambda x, u=u_left: qmul(u, x))
        reconstructed_right = action_matrix(lambda x, u=u_right: qmul(x, u))
        left_twist = dot(z, matvec(reconstructed_left, w))
        right_twist = dot(z, matvec(reconstructed_right, w))
        check_scalar(left_twist + right_twist, 0.0, "reconstructed opposite chirality")
        left_sign = 1.0 if left_twist > 0.0 else -1.0
        right_sign = 1.0 if right_twist > 0.0 else -1.0
        check_error(reconstructed_left, complex_operator(q, v, w, z, left_sign), "left full operator reconstruction")
        check_error(reconstructed_right, complex_operator(q, v, w, z, right_sign), "right full operator reconstruction")

        for operator, sign in ((plus, 1.0), (minus, -1.0)):
            check_error(madd(transpose(operator), operator), [[0.0] * 4 for _ in range(4)], "skew")
            check_error(matmul(operator, operator), mscale(-1.0, identity), "square")
            check_error(matvec(operator, q), v, "point tangent")
            check_error(matvec(operator, v), scale(-1.0, q), "route plane")
            check_error(matvec(operator, w), scale(sign, z), "screen sign")
            check_error(matvec(operator, z), scale(-sign, w), "screen closure")

        angle = rng.uniform(-math.pi, math.pi)
        c, s = math.cos(angle), math.sin(angle)
        route_point = add(scale(c, q), scale(s, v))
        route_tangent = add(scale(c, v), scale(-s, q))
        check_error(matvec(plus, route_point), route_tangent, "plus common route")
        check_error(matvec(minus, route_point), route_tangent, "minus common route")
        check_error(matvec(plus, w), scale(-1.0, matvec(minus, w)), "opposite transverse data")

        radius = radii[case % len(radii)]
        check_scalar(dot(z, scale(1.0 / radius, matvec(plus, w))), 1.0 / radius, "plus twist")
        check_scalar(dot(z, scale(1.0 / radius, matvec(minus, w))), -1.0 / radius, "minus twist")

    result = {
        "status": "PASS",
        "implementation": "oriented_two_plane_outer_product_no_production_import",
        "random_seed": SEED,
        "sample_cases": samples,
        "independent_checks": checks,
        "maximum_error": worst,
        "directed_germ_member_count": 2,
        "signed_screen_member_count": 1,
        "path_only_distinguishes_chirality": False,
        "imports_production_code": False,
        "reconstructs_members_from_pv": True,
        "evaluation_maps_verified_injective": True,
        "closed_quaternion_formulas_independently_recovered": True,
    }
    assert checks >= 30000
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
