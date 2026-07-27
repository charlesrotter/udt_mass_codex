#!/usr/bin/env python3
"""Exact total-degree jets for the frozen twisted-S3 curvature certificates."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product

F = Fraction
DEGREE = 3
ZERO = (0, 0, 0)


@dataclass(frozen=True)
class Jet:
    coefficients: dict[tuple[int, int, int], F]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "coefficients",
            {key: F(value) for key, value in self.coefficients.items()
             if value and sum(key) <= DEGREE},
        )

    @staticmethod
    def constant(value: int | F = 0) -> "Jet":
        value = F(value)
        return Jet({ZERO: value} if value else {})

    def __add__(self, other: object) -> "Jet":
        rhs = as_jet(other)
        result = dict(self.coefficients)
        for key, value in rhs.coefficients.items():
            result[key] = result.get(key, F(0)) + value
        return Jet(result)

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet({key: -value for key, value in self.coefficients.items()})

    def __sub__(self, other: object) -> "Jet":
        return self + (-as_jet(other))

    def __rsub__(self, other: object) -> "Jet":
        return as_jet(other) - self

    def __mul__(self, other: object) -> "Jet":
        rhs = as_jet(other)
        result: dict[tuple[int, int, int], F] = {}
        for left_key, left_value in self.coefficients.items():
            for right_key, right_value in rhs.coefficients.items():
                key = tuple(left_key[index] + right_key[index] for index in range(3))
                if sum(key) <= DEGREE:
                    result[key] = result.get(key, F(0)) + left_value * right_value
        return Jet(result)

    __rmul__ = __mul__

    def inverse(self) -> "Jet":
        constant = self.coefficient(ZERO)
        assert constant
        reduced = self / constant - 1
        result = Jet.constant(1)
        term = Jet.constant(1)
        for _ in range(1, DEGREE + 1):
            term = term * (-reduced)
            result += term
        return result / constant

    def __truediv__(self, other: object) -> "Jet":
        if isinstance(other, (int, F)):
            return Jet({key: value / F(other) for key, value in self.coefficients.items()})
        return self * as_jet(other).inverse()

    def __rtruediv__(self, other: object) -> "Jet":
        return as_jet(other) * self.inverse()

    def exponential_zero_constant(self) -> "Jet":
        assert self.coefficient(ZERO) == 0
        result = Jet.constant(1)
        term = Jet.constant(1)
        factorial = 1
        for order in range(1, DEGREE + 1):
            term *= self
            factorial *= order
            result += term / factorial
        return result

    def derivative(self, axis: int) -> "Jet":
        result: dict[tuple[int, int, int], F] = {}
        for key, value in self.coefficients.items():
            if key[axis]:
                lowered = list(key)
                lowered[axis] -= 1
                result[tuple(lowered)] = value * key[axis]
        return Jet(result)

    def truncate(self, degree: int) -> "Jet":
        return Jet({key: value for key, value in self.coefficients.items() if sum(key) <= degree})

    def coefficient(self, key: tuple[int, int, int]) -> F:
        return self.coefficients.get(key, F(0))


def as_jet(value: object) -> Jet:
    return value if isinstance(value, Jet) else Jet.constant(value)  # type: ignore[arg-type]


X = Jet({(1, 0, 0): F(1)})
Y = Jet({(0, 1, 0): F(1)})
Z = Jet({(0, 0, 1): F(1)})


def matrix_inverse(matrix: list[list[Jet]]) -> list[list[Jet]]:
    size = len(matrix)
    augmented = [
        [matrix[row][column] for column in range(size)]
        + [Jet.constant(int(row == column)) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size)
                     if augmented[row][column].coefficient(ZERO))
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][index] - factor * augmented[column][index]
                for index in range(2 * size)
            ]
    return [row[size:] for row in augmented]


def complete_metric(lambda_value: F, epsilon: F, twist: F) -> list[list[Jet]]:
    radius_squared = X * X + Y * Y + Z * Z
    denominator = (1 + radius_squared).inverse()
    quaternion = [
        (1 - radius_squared) * denominator,
        2 * X * denominator,
        2 * Y * denominator,
        2 * Z * denominator,
    ]
    differentials = [
        [quaternion[index].derivative(axis) for axis in range(3)] for index in range(4)
    ]
    sigma = [[Jet.constant() for _ in range(3)] for _ in range(3)]
    for axis in range(3):
        sigma[0][axis] = (
            quaternion[0] * differentials[1][axis]
            - quaternion[1] * differentials[0][axis]
            - quaternion[2] * differentials[3][axis]
            + quaternion[3] * differentials[2][axis]
        )
        sigma[1][axis] = (
            quaternion[0] * differentials[2][axis]
            - quaternion[2] * differentials[0][axis]
            - quaternion[3] * differentials[1][axis]
            + quaternion[1] * differentials[3][axis]
        )
        sigma[2][axis] = (
            quaternion[0] * differentials[3][axis]
            - quaternion[3] * differentials[0][axis]
            - quaternion[1] * differentials[2][axis]
            + quaternion[2] * differentials[1][axis]
        )

    _, q1, q2, q3 = quaternion
    profile = (
        q1 + 2 * q2 + 3 * q3
        + q1 * q2 + 2 * q2 * q3 + 3 * q3 * q1
        + 2 * q1 * q1 - 3 * q2 * q2 + 5 * q3 * q3
        + q1 * q2 * q3 + 2 * q1 * q1 * q1 - q2 * q2 * q2 + 3 * q3 * q3 * q3
    )
    phi = epsilon * profile
    clock_weight = (-phi).exponential_zero_constant()
    ruler_weight = phi.exponential_zero_constant()
    screen_weight = (lambda_value * phi).exponential_zero_constant()

    coframe = [[Jet.constant() for _ in range(4)] for _ in range(4)]
    coframe[0][0] = clock_weight
    for axis in range(3):
        coframe[0][axis + 1] = clock_weight * twist * sigma[2][axis]
        coframe[1][axis + 1] = ruler_weight * sigma[2][axis]
        coframe[2][axis + 1] = screen_weight * sigma[0][axis]
        coframe[3][axis + 1] = screen_weight * sigma[1][axis]

    signs = (-1, 1, 1, 1)
    return [[
        sum((signs[leg] * coframe[leg][row] * coframe[leg][column]
             for leg in range(4)), Jet.constant())
        for column in range(4)
    ] for row in range(4)]


def coordinate_derivative(value: Jet, coordinate: int) -> Jet:
    return Jet.constant() if coordinate == 0 else value.derivative(coordinate - 1)


def determinant_3(matrix: list[list[F]]) -> F:
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def invariant_gradient_certificate(lambda_value: F, epsilon: F, twist: F) -> dict[str, object]:
    metric = complete_metric(lambda_value, epsilon, twist)
    inverse = matrix_inverse(metric)

    # Exact inverse and signature checks at every retained jet order.
    for row, column in product(range(4), repeat=2):
        identity = sum((metric[row][middle] * inverse[middle][column]
                        for middle in range(4)), Jet.constant())
        assert (identity - int(row == column)).coefficients == {}
    assert metric[0][0].coefficient(ZERO) == -1

    christoffel = [[[
        (sum((
            inverse[upper][other] * (
                coordinate_derivative(metric[other][right], left)
                + coordinate_derivative(metric[other][left], right)
                - coordinate_derivative(metric[left][right], other)
            ) for other in range(4)
        ), Jet.constant()) / 2).truncate(2)
        for right in range(4)] for left in range(4)] for upper in range(4)]
    for upper, left, right in product(range(4), repeat=3):
        assert (christoffel[upper][left][right] - christoffel[upper][right][left]).coefficients == {}

    riemann = [[[[Jet.constant() for _ in range(4)] for _ in range(4)]
                for _ in range(4)] for _ in range(4)]
    for upper, lower, left, right in product(range(4), repeat=4):
        value = (
            coordinate_derivative(christoffel[upper][right][lower], left)
            - coordinate_derivative(christoffel[upper][left][lower], right)
        )
        for middle in range(4):
            value += (
                christoffel[upper][left][middle] * christoffel[middle][right][lower]
                - christoffel[upper][right][middle] * christoffel[middle][left][lower]
            )
        riemann[upper][lower][left][right] = value.truncate(1)
    for upper, lower, left, right in product(range(4), repeat=4):
        assert (riemann[upper][lower][left][right]
                + riemann[upper][lower][right][left]).coefficients == {}

    ricci = [[
        sum((riemann[upper][left][upper][right] for upper in range(4)), Jet.constant()).truncate(1)
        for right in range(4)
    ] for left in range(4)]
    for left, right in product(range(4), repeat=2):
        assert (ricci[left][right] - ricci[right][left]).coefficients == {}

    scalar = sum((inverse[left][right] * ricci[left][right]
                  for left, right in product(range(4), repeat=2)), Jet.constant()).truncate(1)
    ricci_operator = [[
        sum((inverse[row][middle] * ricci[middle][column] for middle in range(4)),
            Jet.constant()).truncate(1)
        for column in range(4)
    ] for row in range(4)]
    ricci_squared = sum((
        ricci_operator[row][column] * ricci_operator[column][row]
        for row, column in product(range(4), repeat=2)
    ), Jet.constant()).truncate(1)

    lowered = [[[[
        sum((metric[first][upper] * riemann[upper][second][third][fourth]
             for upper in range(4)), Jet.constant()).truncate(1)
        for fourth in range(4)] for third in range(4)]
        for second in range(4)] for first in range(4)]
    for first, second, third, fourth in product(range(4), repeat=4):
        assert (lowered[first][second][third][fourth]
                + lowered[second][first][third][fourth]).coefficients == {}
        assert (lowered[first][second][third][fourth]
                - lowered[third][fourth][first][second]).coefficients == {}

    pairs = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    bivector_inverse = [[
        (inverse[a][c] * inverse[b][d] - inverse[a][d] * inverse[b][c]).truncate(1)
        for c, d in pairs
    ] for a, b in pairs]
    paired_riemann = [[lowered[a][b][c][d] for c, d in pairs] for a, b in pairs]
    kretschmann = Jet.constant()
    for first, second, raised_first, raised_second in product(range(6), repeat=4):
        kretschmann += (
            4 * paired_riemann[first][second]
            * bivector_inverse[first][raised_first]
            * bivector_inverse[second][raised_second]
            * paired_riemann[raised_first][raised_second]
        )
    kretschmann = kretschmann.truncate(1)

    invariants = (scalar, ricci_squared, kretschmann)
    gradients = [[
        invariant.coefficient((1, 0, 0)),
        invariant.coefficient((0, 1, 0)),
        invariant.coefficient((0, 0, 1)),
    ] for invariant in invariants]
    determinant = determinant_3(gradients)
    return {
        "gradients": gradients,
        "determinant": determinant,
        "rank_three": determinant != 0,
    }
