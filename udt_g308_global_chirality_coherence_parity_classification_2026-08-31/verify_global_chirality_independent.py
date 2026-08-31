#!/usr/bin/env python3
"""Implementation-distinct numerical verification of the bounded G308 result."""

from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_VERIFICATION.json"
SEED = 3080831


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def norm(a):
    return math.sqrt(dot(a, a))


def normalize(a):
    length = norm(a)
    if length < 1e-12:
        raise ValueError("degenerate vector")
    return scale(1.0 / length, a)


def outer(a, b):
    return tuple(tuple(a[i] * b[j] for j in range(4)) for i in range(4))


def matadd(*matrices):
    return tuple(
        tuple(sum(matrix[i][j] for matrix in matrices) for j in range(4))
        for i in range(4)
    )


def matscale(c, matrix):
    return tuple(tuple(c * value for value in row) for row in matrix)


def matvec(matrix, vector):
    return tuple(sum(matrix[i][j] * vector[j] for j in range(4)) for i in range(4))


def matmul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4))
        for i in range(4)
    )


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in range(4)) for i in range(4))


def determinant(matrix):
    result = 0.0
    for permutation in itertools.permutations(range(4)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(4)
            for j in range(i + 1, 4)
        )
        term = 1.0 if inversions % 2 == 0 else -1.0
        for i in range(4):
            term *= matrix[i][permutation[i]]
        result += term
    return result


def determinant3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def columns(vectors):
    return tuple(tuple(vectors[j][i] for j in range(4)) for i in range(4))


def orthogonal_fourth(p, v, w):
    rows = (p, v, w)
    cofactors = []
    for excluded in range(4):
        minor = tuple(
            tuple(row[j] for j in range(4) if j != excluded)
            for row in rows
        )
        cofactors.append(((-1.0) ** excluded) * determinant3(minor))
    z = normalize(tuple(cofactors))
    if determinant(columns((p, v, w, z))) < 0.0:
        z = scale(-1.0, z)
    return z


def random_unit(rng):
    return normalize(tuple(rng.gauss(0.0, 1.0) for _ in range(4)))


def random_frame(rng):
    while True:
        try:
            p = random_unit(rng)
            raw_v = tuple(rng.gauss(0.0, 1.0) for _ in range(4))
            v = normalize(add(raw_v, scale(-dot(raw_v, p), p)))
            raw_w = tuple(rng.gauss(0.0, 1.0) for _ in range(4))
            w = normalize(
                add(
                    add(raw_w, scale(-dot(raw_w, p), p)),
                    scale(-dot(raw_w, v), v),
                )
            )
            z = orthogonal_fourth(p, v, w)
            return p, v, w, z
        except ValueError:
            continue


def complex_structure(p, v, w, z, sign):
    route = matadd(outer(v, p), matscale(-1.0, outer(p, v)))
    screen = matadd(outer(z, w), matscale(-1.0, outer(w, z)))
    return matadd(route, matscale(sign, screen))


def reflection(p, v, w, z):
    return matadd(outer(p, p), outer(v, v), outer(w, w), matscale(-1.0, outer(z, z)))


def pfaffian(matrix):
    return (
        matrix[0][1] * matrix[2][3]
        - matrix[0][2] * matrix[1][3]
        + matrix[0][3] * matrix[1][2]
    )


def maximum_vector_error(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def maximum_matrix_error(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(4) for j in range(4))


def main():
    rng = random.Random(SEED)
    identity = tuple(tuple(1.0 if i == j else 0.0 for j in range(4)) for i in range(4))
    minus_identity = matscale(-1.0, identity)
    checks = 0
    maximum_error = 0.0

    def check(condition, error=0.0):
        nonlocal checks, maximum_error
        assert condition
        checks += 1
        maximum_error = max(maximum_error, abs(error))

    sample_cases = 1200
    global_points_per_case = 4
    for _ in range(sample_cases):
        p, v, w, z = random_frame(rng)
        left = complex_structure(p, v, w, z, 1.0)
        right = complex_structure(p, v, w, z, -1.0)
        mirror = reflection(p, v, w, z)

        for candidate in (left, right):
            skew_error = maximum_matrix_error(transpose(candidate), matscale(-1.0, candidate))
            complex_error = maximum_matrix_error(matmul(candidate, candidate), minus_identity)
            orthogonal_error = maximum_matrix_error(matmul(transpose(candidate), candidate), identity)
            check(skew_error < 2e-12, skew_error)
            check(complex_error < 2e-12, complex_error)
            check(orthogonal_error < 2e-12, orthogonal_error)
            check(abs(abs(pfaffian(candidate)) - 1.0) < 2e-12, abs(abs(pfaffian(candidate)) - 1.0))

        check(abs(pfaffian(left) + pfaffian(right)) < 2e-12, pfaffian(left) + pfaffian(right))
        check(abs(determinant(mirror) + 1.0) < 2e-12, determinant(mirror) + 1.0)
        check(maximum_matrix_error(matmul(mirror, mirror), identity) < 2e-12, maximum_matrix_error(matmul(mirror, mirror), identity))
        check(maximum_vector_error(matvec(mirror, p), p) < 2e-12, maximum_vector_error(matvec(mirror, p), p))
        check(maximum_vector_error(matvec(mirror, v), v) < 2e-12, maximum_vector_error(matvec(mirror, v), v))
        check(maximum_vector_error(matvec(mirror, w), w) < 2e-12, maximum_vector_error(matvec(mirror, w), w))
        check(maximum_vector_error(matvec(mirror, z), scale(-1.0, z)) < 2e-12, maximum_vector_error(matvec(mirror, z), scale(-1.0, z)))
        conjugated = matmul(matmul(mirror, left), transpose(mirror))
        check(maximum_matrix_error(conjugated, right) < 3e-12, maximum_matrix_error(conjugated, right))

        reversed_left = matscale(-1.0, left)
        reversed_right = matscale(-1.0, right)
        check(abs(pfaffian(reversed_left) - pfaffian(left)) < 2e-12, pfaffian(reversed_left) - pfaffian(left))
        check(abs(pfaffian(reversed_right) - pfaffian(right)) < 2e-12, pfaffian(reversed_right) - pfaffian(right))
        check(maximum_vector_error(matvec(reversed_left, p), scale(-1.0, v)) < 2e-12, maximum_vector_error(matvec(reversed_left, p), scale(-1.0, v)))

        midpoint = matscale(0.5, matadd(left, right))
        check(abs(determinant(midpoint)) < 2e-12, determinant(midpoint))
        check(maximum_matrix_error(matmul(midpoint, midpoint), minus_identity) > 0.5)

        rotation_frame = random_frame(rng)
        rotation = columns(rotation_frame)
        check(abs(determinant(rotation) - 1.0) < 2e-12, determinant(rotation) - 1.0)
        rotated_left = matmul(matmul(rotation, left), transpose(rotation))
        rotated_right = matmul(matmul(rotation, right), transpose(rotation))
        check(abs(pfaffian(rotated_left) - pfaffian(left)) < 3e-12, pfaffian(rotated_left) - pfaffian(left))
        check(abs(pfaffian(rotated_right) - pfaffian(right)) < 3e-12, pfaffian(rotated_right) - pfaffian(right))

        radius = 10.0 ** rng.uniform(-2.0, 2.0)
        radius_rate = rng.uniform(-3.0, 3.0)
        first_carry_term = -radius_rate / (radius * radius)
        second_carry_term = (1.0 / radius) * (radius_rate / radius)
        carry = first_carry_term + second_carry_term
        carry_scale = max(1.0, abs(first_carry_term) + abs(second_carry_term))
        normalized_carry_error = carry / carry_scale
        check(abs(normalized_carry_error) < 2e-12, normalized_carry_error)
        if abs(radius_rate) > 1e-8:
            check(abs(radius_rate / radius) > 0.0)

        for _ in range(global_points_per_case):
            q = random_unit(rng)
            for candidate, other in ((left, right), (right, left)):
                field = matvec(candidate, q)
                check(abs(dot(q, field)) < 2e-12, dot(q, field))
                check(abs(dot(field, field) - 1.0) < 3e-12, dot(field, field) - 1.0)
                equivariance_error = maximum_vector_error(
                    matvec(mirror, field),
                    matvec(other, matvec(mirror, q)),
                )
                check(equivariance_error < 3e-12, equivariance_error)
                unit_field = scale(1.0 / radius, field)
                check(abs(radius * radius * dot(unit_field, unit_field) - 1.0) < 4e-12, radius * radius * dot(unit_field, unit_field) - 1.0)

            raw_tangent = random_unit(rng)
            spatial = add(raw_tangent, scale(-dot(raw_tangent, q), q))
            dt = rng.uniform(-2.0, 2.0)
            before = -dt * dt + radius * radius * dot(spatial, spatial)
            reflected_spatial = matvec(mirror, spatial)
            after = -dt * dt + radius * radius * dot(reflected_spatial, reflected_spatial)
            causal_scale = max(1.0, abs(before) + abs(after))
            causal_error = (before - after) / causal_scale
            check(abs(causal_error) < 3e-12, causal_error)
            check((before > 0.0) == (after > 0.0) and (before < 0.0) == (after < 0.0))

    result = {
        "status": "PASS",
        "implementation": "random_oriented_frame_outer_product_and_pfaffian_no_production_import",
        "imports_production_code": False,
        "random_seed": SEED,
        "sample_cases": sample_cases,
        "global_points_per_case": global_points_per_case,
        "independent_checks": checks,
        "maximum_error": maximum_error,
        "both_global_fields_verified": True,
        "det_minus_one_exchange_verified": True,
        "det_plus_one_chirality_preservation_verified": True,
        "pair_reversal_chirality_preservation_verified": True,
        "connected_switch_degeneracy_verified": True,
        "causal_quadratic_form_preserved": True,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
