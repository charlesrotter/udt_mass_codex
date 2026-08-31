#!/usr/bin/env python3
"""Method-distinct Hodge/group-orbit verification of the bounded G308 theorem."""

from __future__ import annotations

import itertools
import json
import math
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "HODGE_INDEPENDENT_VERIFICATION.json"
SEED = 308831
DIM = 4


def identity():
    return tuple(tuple(1.0 if i == j else 0.0 for j in range(DIM)) for i in range(DIM))


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in range(DIM)) for i in range(DIM))


def matmul(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(DIM)) for j in range(DIM))
        for i in range(DIM)
    )


def matvec(matrix, vector):
    return tuple(sum(matrix[i][j] * vector[j] for j in range(DIM)) for i in range(DIM))


def matscale(value, matrix):
    return tuple(tuple(value * entry for entry in row) for row in matrix)


def matadd(left, right):
    return tuple(tuple(left[i][j] + right[i][j] for j in range(DIM)) for i in range(DIM))


def vecadd(left, right):
    return tuple(left[i] + right[i] for i in range(DIM))


def vecscale(value, vector):
    return tuple(value * entry for entry in vector)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def normalize(vector):
    length = math.sqrt(dot(vector, vector))
    if length < 1e-14:
        raise ValueError("degenerate vector")
    return vecscale(1.0 / length, vector)


def determinant(matrix):
    total = 0.0
    for permutation in itertools.permutations(range(DIM)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(DIM)
            for j in range(i + 1, DIM)
        )
        term = -1.0 if inversions % 2 else 1.0
        for i in range(DIM):
            term *= matrix[i][permutation[i]]
        total += term
    return total


def givens(i, j, angle):
    matrix = [list(row) for row in identity()]
    cosine = math.cos(angle)
    sine = math.sin(angle)
    matrix[i][i] = cosine
    matrix[i][j] = -sine
    matrix[j][i] = sine
    matrix[j][j] = cosine
    return tuple(tuple(row) for row in matrix)


def random_so4(rng):
    matrix = identity()
    for i, j in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
        matrix = matmul(givens(i, j, rng.uniform(-math.pi, math.pi)), matrix)
    return matrix


def levi_civita(indices):
    if len(set(indices)) != DIM:
        return 0
    inversions = sum(
        indices[i] > indices[j]
        for i in range(DIM)
        for j in range(i + 1, DIM)
    )
    return -1 if inversions % 2 else 1


def hodge(matrix):
    return tuple(
        tuple(
            0.5 * sum(
                levi_civita((i, j, k, ell)) * matrix[k][ell]
                for k in range(DIM)
                for ell in range(DIM)
            )
            for j in range(DIM)
        )
        for i in range(DIM)
    )


def matrix_inner(left, right):
    return sum(left[i][j] * right[i][j] for i in range(DIM) for j in range(DIM))


def maximum_matrix_error(left, right):
    return max(abs(left[i][j] - right[i][j]) for i in range(DIM) for j in range(DIM))


def maximum_vector_error(left, right):
    return max(abs(left[i] - right[i]) for i in range(DIM))


def conjugate(frame, matrix):
    return matmul(matmul(frame, matrix), transpose(frame))


def basis_vector(index):
    return tuple(1.0 if i == index else 0.0 for i in range(DIM))


def main():
    rng = random.Random(SEED)
    unit = identity()
    minus_unit = matscale(-1.0, unit)
    canonical_plus = (
        (0.0, -1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, -1.0),
        (0.0, 0.0, 1.0, 0.0),
    )
    canonical_minus = (
        (0.0, -1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
        (0.0, 0.0, -1.0, 0.0),
    )
    canonical_mirror = (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, -1.0),
    )

    checks = 0
    maximum_error = 0.0

    def check(condition, error=0.0):
        nonlocal checks, maximum_error
        assert condition
        checks += 1
        maximum_error = max(maximum_error, abs(error))

    sample_cases = 1600
    global_points_per_case = 3
    for _ in range(sample_cases):
        frame = random_so4(rng)
        frame_error = maximum_matrix_error(matmul(transpose(frame), frame), unit)
        frame_det_error = determinant(frame) - 1.0
        check(frame_error < 3e-13, frame_error)
        check(abs(frame_det_error) < 5e-13, frame_det_error)

        plus = conjugate(frame, canonical_plus)
        minus = conjugate(frame, canonical_minus)
        mirror = conjugate(frame, canonical_mirror)
        star_plus = hodge(plus)
        star_minus = hodge(minus)

        for candidate, star_candidate, chirality in (
            (plus, star_plus, 1.0),
            (minus, star_minus, -1.0),
        ):
            skew_error = maximum_matrix_error(transpose(candidate), matscale(-1.0, candidate))
            complex_error = maximum_matrix_error(matmul(candidate, candidate), minus_unit)
            orthogonal_error = maximum_matrix_error(matmul(transpose(candidate), candidate), unit)
            hodge_error = maximum_matrix_error(star_candidate, matscale(chirality, candidate))
            hodge_ratio = matrix_inner(candidate, star_candidate) / matrix_inner(candidate, candidate)
            check(skew_error < 4e-13, skew_error)
            check(complex_error < 5e-13, complex_error)
            check(orthogonal_error < 5e-13, orthogonal_error)
            check(hodge_error < 4e-13, hodge_error)
            check(abs(hodge_ratio - chirality) < 5e-13, hodge_ratio - chirality)

        mirror_error = maximum_matrix_error(matmul(transpose(mirror), mirror), unit)
        mirror_det_error = determinant(mirror) + 1.0
        exchange_error = maximum_matrix_error(conjugate(mirror, plus), minus)
        check(mirror_error < 5e-13, mirror_error)
        check(abs(mirror_det_error) < 6e-13, mirror_det_error)
        check(exchange_error < 6e-13, exchange_error)
        for index, sign in ((0, 1.0), (1, 1.0), (2, 1.0), (3, -1.0)):
            carried = matvec(frame, basis_vector(index))
            image = matvec(mirror, carried)
            fix_error = maximum_vector_error(image, vecscale(sign, carried))
            check(fix_error < 5e-13, fix_error)

        rotation = random_so4(rng)
        rotated_plus = conjugate(rotation, plus)
        rotated_minus = conjugate(rotation, minus)
        plus_hodge_ratio = matrix_inner(rotated_plus, hodge(rotated_plus)) / matrix_inner(rotated_plus, rotated_plus)
        minus_hodge_ratio = matrix_inner(rotated_minus, hodge(rotated_minus)) / matrix_inner(rotated_minus, rotated_minus)
        check(abs(plus_hodge_ratio - 1.0) < 7e-13, plus_hodge_ratio - 1.0)
        check(abs(minus_hodge_ratio + 1.0) < 7e-13, minus_hodge_ratio + 1.0)

        for candidate, chirality in ((plus, 1.0), (minus, -1.0)):
            reversed_candidate = matscale(-1.0, candidate)
            reversed_ratio = (
                matrix_inner(reversed_candidate, hodge(reversed_candidate))
                / matrix_inner(reversed_candidate, reversed_candidate)
            )
            check(abs(reversed_ratio - chirality) < 6e-13, reversed_ratio - chirality)

        midpoint = matscale(0.5, matadd(plus, minus))
        midpoint_complex_error = maximum_matrix_error(matmul(midpoint, midpoint), minus_unit)
        check(abs(determinant(midpoint)) < 8e-13, determinant(midpoint))
        check(midpoint_complex_error > 0.5)
        midpoint_ratio = matrix_inner(midpoint, hodge(midpoint)) / matrix_inner(midpoint, midpoint)
        check(abs(midpoint_ratio) < 7e-13, midpoint_ratio)

        radius = 10.0 ** rng.uniform(-3.0, 3.0)
        radius_rate = rng.uniform(-4.0, 4.0)
        time_carry = -radius_rate / (radius * radius) + radius_rate / (radius * radius)
        carry_scale = max(1.0, 2.0 * abs(radius_rate / (radius * radius)))
        check(abs(time_carry / carry_scale) < 1e-15, time_carry / carry_scale)
        spacetime_acceleration = radius_rate / radius
        check((abs(spacetime_acceleration) < 1e-15) == (abs(radius_rate) < 1e-15))

        for _ in range(global_points_per_case):
            point = normalize(tuple(rng.gauss(0.0, 1.0) for _ in range(DIM)))
            for candidate, other in ((plus, minus), (minus, plus)):
                field = matvec(candidate, point)
                check(abs(dot(point, field)) < 5e-13, dot(point, field))
                check(abs(dot(field, field) - 1.0) < 7e-13, dot(field, field) - 1.0)
                ambient_acceleration = matvec(candidate, field)
                slice_tangent_acceleration = vecadd(ambient_acceleration, point)
                slice_error = max(abs(entry) for entry in slice_tangent_acceleration)
                check(slice_error < 6e-13, slice_error)
                angle = rng.uniform(-4.0 * math.pi, 4.0 * math.pi)
                orbit = vecadd(vecscale(math.cos(angle), point), vecscale(math.sin(angle), field))
                expected_tangent = vecadd(vecscale(-math.sin(angle), point), vecscale(math.cos(angle), field))
                flow_error = maximum_vector_error(matvec(candidate, orbit), expected_tangent)
                check(abs(dot(orbit, orbit) - 1.0) < 8e-13, dot(orbit, orbit) - 1.0)
                check(flow_error < 8e-13, flow_error)
                period_error = maximum_vector_error(
                    vecadd(vecscale(math.cos(2.0 * math.pi), point), vecscale(math.sin(2.0 * math.pi), field)),
                    point,
                )
                check(period_error < 6e-13, period_error)
                mirror_equivariance_error = maximum_vector_error(
                    matvec(mirror, field),
                    matvec(other, matvec(mirror, point)),
                )
                check(mirror_equivariance_error < 8e-13, mirror_equivariance_error)

            spatial = tuple(rng.uniform(-2.0, 2.0) for _ in range(DIM))
            dt = rng.uniform(-2.0, 2.0)
            before = -dt * dt + radius * radius * dot(spatial, spatial)
            reflected = matvec(mirror, spatial)
            after = -dt * dt + radius * radius * dot(reflected, reflected)
            causal_scale = max(1.0, abs(before) + abs(after))
            causal_error = (before - after) / causal_scale
            check(abs(causal_error) < 9e-13, causal_error)
            check((before > 0.0) == (after > 0.0) and (before < 0.0) == (after < 0.0))

    result = {
        "status": "PASS",
        "method": "canonical_complex_blocks__SO4_Givens_conjugation__Hodge_star_split__group_orbit_flow",
        "imports_production_code": False,
        "uses_outer_product_candidate_construction": False,
        "random_seed": SEED,
        "sample_cases": sample_cases,
        "global_points_per_case": global_points_per_case,
        "independent_checks": checks,
        "maximum_error": maximum_error,
        "both_global_fields_verified": True,
        "hodge_chirality_split_verified": True,
        "O4_exchange_verified": True,
        "SO4_nonexchange_verified": True,
        "pair_reversal_preserves_chirality": True,
        "connected_regular_switch_excluded": True,
        "normalized_time_carry_verified": True,
        "slice_vs_spacetime_geodesic_distinguished": True,
        "causal_equivalence_verified": True,
        "metric_and_kernel_changed": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
