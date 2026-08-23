#!/usr/bin/env python3
"""Independent exact-Fraction replay for G225; imports no production code."""

from __future__ import annotations

import json
import random
from fractions import Fraction as F


LANDING = (
    "METRIC_AND_SHARED_CLOCK_DEFINE_POSITIVE_INCIDENT_SCREEN_PLANES"
    "__CANONICAL_LEAST_TURNING_DIRECT_SCREEN_ISOMETRY_EXISTS_OFF_ANTIPODES"
    "__THREE_DIRECTION_COMPOSITION_RETAINS_FINITE_O2_HOLONOMY_AND_NO_GLOBAL_ENDPOINT_ONLY_FLAT_SCREEN_CARRY_EXISTS"
    "__G188_JACOBI_TRANSPORT_REMAINS_SEPARATE"
)

Vector = tuple[F, F, F]
Matrix = tuple[tuple[F, F, F], tuple[F, F, F], tuple[F, F, F]]


def dot(left: Vector, right: Vector) -> F:
    return sum((left[i] * right[i] for i in range(3)), F(0))


def cross(left: Vector, right: Vector) -> Vector:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def identity() -> Matrix:
    return ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[j][i] for j in range(3)) for i in range(3))  # type: ignore[return-value]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(sum((left[i][k] * right[k][j] for k in range(3)), F(0)) for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(sum((matrix[i][j] * vector[j] for j in range(3)), F(0)) for i in range(3))  # type: ignore[return-value]


def add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(tuple(left[i][j] + right[i][j] for j in range(3)) for i in range(3))  # type: ignore[return-value]


def scale(value: F, matrix: Matrix) -> Matrix:
    return tuple(tuple(value * matrix[i][j] for j in range(3)) for i in range(3))  # type: ignore[return-value]


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(left[i] * right[j] for j in range(3)) for i in range(3))  # type: ignore[return-value]


def subtract(left: Matrix, right: Matrix) -> Matrix:
    return add(left, scale(F(-1), right))


def determinant(matrix: Matrix) -> F:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def rotation(source: Vector, target: Vector) -> Matrix:
    cosine = dot(source, target)
    if cosine == -1:
        raise ValueError("antipodal")
    skew = subtract(outer(target, source), outer(source, target))
    return add(add(identity(), skew), scale(F(1, 1) / (1 + cosine), matmul(skew, skew)))


def unit_from_stereographic(p: int, q: int) -> Vector:
    denominator = F(1 + p * p + q * q)
    return (
        F(1 - p * p - q * q, 1) / denominator,
        F(2 * p, 1) / denominator,
        F(2 * q, 1) / denominator,
    )


def signed_permutation(rng: random.Random) -> Matrix:
    order = [0, 1, 2]
    rng.shuffle(order)
    signs = [F(rng.choice((-1, 1))) for _ in range(3)]
    rows = [[F(0) for _ in range(3)] for _ in range(3)]
    for row, column in enumerate(order):
        rows[row][column] = signs[row]
    return tuple(tuple(row) for row in rows)  # type: ignore[return-value]


def nonzero_screen_vector(direction: Vector) -> Vector:
    trial: Vector = (F(1), F(0), F(0))
    value = cross(direction, trial)
    if value == (F(0), F(0), F(0)):
        trial = (F(0), F(1), F(0))
        value = cross(direction, trial)
    return value


def main() -> None:
    rng = random.Random(2250822)
    cases = 20_000
    assertions = 0
    nontrivial_defects = 0

    def check(condition: bool, label: str) -> None:
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(label)

    completed = 0
    while completed < cases:
        directions = tuple(
            unit_from_stereographic(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(3)
        )
        if len(set(directions)) != 3:
            continue
        a, b, c = directions
        if dot(a, b) == -1 or dot(b, c) == -1 or dot(a, c) == -1:
            continue

        for direction in directions:
            check(dot(direction, direction) == 1, "unit direction")

        pair_data = ((a, b), (b, c), (a, c))
        rotations: list[Matrix] = []
        for source, target in pair_data:
            candidate = rotation(source, target)
            rotations.append(candidate)
            check(matvec(candidate, source) == target, "direction mapping")
            check(matmul(transpose(candidate), candidate) == identity(), "orthogonality")
            check(determinant(candidate) == 1, "properness")
            check(rotation(target, source) == transpose(candidate), "inverse")
            screen = nonzero_screen_vector(source)
            carried = matvec(candidate, screen)
            check(dot(screen, source) == 0, "source screen")
            check(dot(carried, target) == 0, "target screen")
            check(dot(carried, carried) == dot(screen, screen), "screen norm")

        q = signed_permutation(rng)
        check(
            rotation(matvec(q, a), matvec(q, b))
            == matmul(matmul(q, rotations[0]), transpose(q)),
            "passive orthogonal covariance",
        )

        defect = matmul(transpose(rotations[2]), matmul(rotations[1], rotations[0]))
        check(matmul(transpose(defect), defect) == identity(), "defect orthogonal")
        check(determinant(defect) == 1, "defect proper")
        check(matvec(defect, a) == a, "defect fixes start direction")
        if defect != identity():
            nontrivial_defects += 1

        q_ab = F(rng.randint(1, 11), rng.randint(1, 11))
        q_bc = F(rng.randint(1, 11), rng.randint(1, 11))
        check((q_bc * q_ab) == (q_ab * q_bc), "scalar carry composition")
        completed += 1

    # Fixed coplanar, noncoplanar, antipodal, and projection controls.
    ex: Vector = (F(1), F(0), F(0))
    ey: Vector = (F(0), F(1), F(0))
    ez: Vector = (F(0), F(0), F(1))
    middle: Vector = (F(3, 5), F(4, 5), F(0))
    check(matmul(rotation(middle, ey), rotation(ex, middle)) == rotation(ex, ey), "great-circle control")

    octant = matmul(transpose(rotation(ex, ez)), matmul(rotation(ey, ez), rotation(ex, ey)))
    expected: Matrix = ((F(1), F(0), F(0)), (F(0), F(0), F(-1)), (F(0), F(1), F(0)))
    check(octant == expected, "octant holonomy")
    check(octant != identity(), "octant nontrivial")
    check(matmul(transpose(octant), octant) == identity(), "octant orthogonal")
    check(matvec(octant, ex) == ex, "octant fixes direction")

    antipodal_one: Matrix = ((F(-1), F(0), F(0)), (F(0), F(-1), F(0)), (F(0), F(0), F(1)))
    antipodal_two: Matrix = ((F(-1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(-1)))
    for candidate in (antipodal_one, antipodal_two):
        check(matvec(candidate, ex) == (-ex[0], -ex[1], -ex[2]), "antipodal mapping")
        check(matmul(transpose(candidate), candidate) == identity(), "antipodal orthogonal")
        check(determinant(candidate) == 1, "antipodal proper")
    check(antipodal_one != antipodal_two, "antipodal nonunique")
    check(nontrivial_defects > 0, "nontrivial random holonomy present")

    result = {
        "status": "PASS",
        "seed": 2250822,
        "cases": cases,
        "exact_rational_assertions": assertions,
        "nontrivial_composition_defects": nontrivial_defects,
        "production_code_imported": False,
        "sympy_imported": False,
        "fixed_great_circle_control": True,
        "fixed_octant_holonomy": True,
        "antipodal_least_turning_nonuniqueness": True,
        "passive_O3_covariance": True,
        "G224_scalar_composition": True,
        "landing": LANDING,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
