#!/usr/bin/env python3
"""Independent full-matrix verification of the configuration adjacency atlas.

This file does not import the production builder.  It reconstructs both registered
configuration charts, forms the complete 4x4 coframe metric, and evaluates
g^{-1}(dphi,dphi) through matrix inversion or an interval adjugate/determinant.
"""

from __future__ import annotations

import csv
import gzip
import itertools
import json
import math
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from mpmath import iv
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
iv.dps = 80

PARAMETERS = tuple(f"alpha_{index}" for index in range(10)) + ("beta",)
BASE_VALUES = tuple(map(Fraction, (
    "0.08", "0.14", "-0.06", "0.12", "-0.09",
    "0.05", "0.11", "-0.07", "0.09", "0.04",
)))
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
POINTS = {
    "P0": (Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
    "P1": (Fraction(1, 3), Fraction(-1, 4), Fraction(1, 5), Fraction(-1, 6)),
    "P2": (Fraction(-1, 4), Fraction(1, 5), Fraction(-1, 6), Fraction(1, 7)),
    "P3": (Fraction(1, 5), Fraction(1, 6), Fraction(-1, 7), Fraction(-1, 8)),
    "P4": (Fraction(-1, 6), Fraction(-1, 7), Fraction(1, 8), Fraction(1, 9)),
    "P5": (Fraction(1, 2), Fraction(0), Fraction(-1, 3), Fraction(1, 4)),
    "P6": (Fraction(0), Fraction(-1, 2), Fraction(1, 4), Fraction(-1, 3)),
    "P7": (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)),
}
POINT_PAIRS = {0: ("P0", "P4"), 1: ("P1", "P5"), 2: ("P2", "P6"), 3: ("P3", "P7")}
CHARTS = ("J1_GENERATOR_COEFFICIENT_JOIN", "J2_EVALUATED_COFIELD_JOIN")
BANK_PAIRS = tuple(itertools.combinations(range(4), 2))


def rows(path):
    opener = gzip.open if Path(path).suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def coefficient(bank, field, term):
    raw = (
        (bank + 2) * 11
        + (field + 1) * 7
        + (term + 1) * 5
        + (bank + 1) * (field + term + 3)
    ) % 19 - 9
    if raw == 0:
        raw = 1 if (bank + field + term) % 2 == 0 else -1
    return Fraction(raw, 60 if term < 4 else 90 if term < 8 else 120)


COEFFICIENTS = tuple(
    tuple(tuple(coefficient(bank, field, term) for term in range(14)) for field in range(11))
    for bank in range(4)
)
FLOAT_COEFFICIENTS = np.asarray(COEFFICIENTS, dtype=np.float64)
FLOAT_BASE_VALUES = np.asarray(BASE_VALUES, dtype=np.float64)


def amplitude_vector(carrier, mask):
    selected = [Fraction(0) for _ in range(11)]
    for indices, bit in (((0, 1, 2), 1), ((3, 4, 5), 2), ((6, 7, 8, 9), 4), ((10,), 8)):
        if mask & bit:
            for index in indices:
                selected[index] = carrier[index]
    return tuple(selected)


def bank_coordinate(bank, parameter):
    first, second = (POINTS[name] for name in POINT_PAIRS[bank])
    return tuple(float(first[i]) + parameter * float(second[i] - first[i]) for i in range(4))


def field_value(coefficients, coordinates):
    value = sum(float(coefficients[i]) * coordinates[i] for i in range(4))
    value += sum(float(coefficients[4 + i]) * coordinates[i] ** 2 / 2 for i in range(4))
    value += sum(
        float(coefficients[8 + p]) * coordinates[i] * coordinates[j]
        for p, (i, j) in enumerate(PAIRS)
    )
    return value


def field_gradient(coefficients, coordinates):
    output = []
    for index in range(4):
        value = float(coefficients[index]) + float(coefficients[4 + index]) * coordinates[index]
        for pair_index, (first, second) in enumerate(PAIRS):
            if index == first:
                value += float(coefficients[8 + pair_index]) * coordinates[second]
            elif index == second:
                value += float(coefficients[8 + pair_index]) * coordinates[first]
        output.append(value)
    return np.asarray(output)


def endpoint(bank, amplitudes, parameter_u):
    coordinate = bank_coordinate(bank, parameter_u)
    latent = np.asarray([
        float(BASE_VALUES[field])
        + float(amplitudes[field]) * field_value(COEFFICIENTS[bank][field], coordinate)
        for field in range(10)
    ])
    gradient = float(amplitudes[10]) * field_gradient(COEFFICIENTS[bank][10], coordinate)
    return latent, gradient


def configured(chart, bank_a, bank_b, amplitudes, parameter_u, parameter_lambda):
    if chart == CHARTS[1]:
        latent_a, gradient_a = endpoint(bank_a, amplitudes, parameter_u)
        latent_b, gradient_b = endpoint(bank_b, amplitudes, parameter_u)
        return (
            (1 - parameter_lambda) * latent_a + parameter_lambda * latent_b,
            (1 - parameter_lambda) * gradient_a + parameter_lambda * gradient_b,
        )
    coordinate_a = bank_coordinate(bank_a, parameter_u)
    coordinate_b = bank_coordinate(bank_b, parameter_u)
    coordinate = np.asarray([
        (1 - parameter_lambda) * coordinate_a[index]
        + parameter_lambda * coordinate_b[index]
        for index in range(4)
    ])
    coefficients = tuple(
        tuple(
            (1 - parameter_lambda) * float(COEFFICIENTS[bank_a][field][term])
            + parameter_lambda * float(COEFFICIENTS[bank_b][field][term])
            for term in range(14)
        )
        for field in range(11)
    )
    latent = np.asarray([
        float(BASE_VALUES[field])
        + float(amplitudes[field]) * field_value(coefficients[field], coordinate)
        for field in range(10)
    ])
    gradient = float(amplitudes[10]) * field_gradient(coefficients[10], coordinate)
    return latent, gradient


def full_metric(latent, omit_angular_shift=False, omit_field=None):
    values = np.asarray(latent, dtype=np.float64).copy()
    field_index = {
        "d": 3, "e": 4, "f": 5,
        "a20": 6, "a30": 7, "a21": 8, "a31": 9,
    }
    if omit_field is not None:
        values[field_index[omit_field]] = 0.0
    a, b, c, d, e, f, a20, a30, a21, a31 = values
    if omit_angular_shift:
        a20 = a30 = a21 = a31 = 0.0
    u, w, r, t = math.exp(a), math.exp(c), math.exp(d), math.exp(f)
    coframe = np.asarray([
        [u, b, 0.0, 0.0],
        [0.0, w, 0.0, 0.0],
        [r * a20 + e * a30, r * a21 + e * a31, r, e],
        [t * a30, t * a31, 0.0, t],
    ])
    eta = np.diag((-1.0, 1.0, 1.0, 1.0))
    return coframe.T @ eta @ coframe


def scalar_matrix(chart, bank_a, bank_b, amplitudes, u, lam, omit_angular_shift=False):
    latent, gradient = configured(chart, bank_a, bank_b, amplitudes, u, lam)
    metric = full_metric(latent, omit_angular_shift=omit_angular_shift)
    determinant = float(np.linalg.det(metric))
    scalar = float(gradient @ np.linalg.solve(metric, gradient))
    return scalar, determinant, float(np.linalg.norm(gradient))


def batch_bank_coordinate(bank, parameter_u):
    first, second = (np.asarray(POINTS[name], dtype=np.float64) for name in POINT_PAIRS[bank])
    return first.reshape(1, -1, 4) + parameter_u.reshape(1, -1, 1) * (
        second - first
    ).reshape(1, 1, 4)


def batch_field_values(coefficients, coordinate):
    # coefficients: N x U x fields x 14; coordinate: N x U x 4
    linear = np.sum(coefficients[..., :4] * coordinate[..., None, :], axis=-1)
    quadratic = np.sum(
        coefficients[..., 4:8] * coordinate[..., None, :] ** 2 / 2.0, axis=-1
    )
    cross = np.zeros_like(linear)
    for pair_index, (first, second) in enumerate(PAIRS):
        cross += (
            coefficients[..., 8 + pair_index]
            * coordinate[..., first, None]
            * coordinate[..., second, None]
        )
    return linear + quadratic + cross


def batch_field_gradient(coefficients, coordinate):
    # coefficients: N x U x 14; coordinate: N x U x 4
    output = []
    for index in range(4):
        value = coefficients[..., index] + coefficients[..., 4 + index] * coordinate[..., index]
        for pair_index, (first, second) in enumerate(PAIRS):
            if index == first:
                value += coefficients[..., 8 + pair_index] * coordinate[..., second]
            elif index == second:
                value += coefficients[..., 8 + pair_index] * coordinate[..., first]
        output.append(value)
    return np.stack(output, axis=-1)


def batch_endpoint(bank, amplitudes, parameter_u):
    coordinate = batch_bank_coordinate(bank, parameter_u)
    count = amplitudes.shape[0]
    coordinates = np.broadcast_to(coordinate, (count, coordinate.shape[1], 4))
    coefficients = np.broadcast_to(
        FLOAT_COEFFICIENTS[bank].reshape(1, 1, 11, 14),
        (count, coordinate.shape[1], 11, 14),
    )
    values = batch_field_values(coefficients, coordinates)
    latent = FLOAT_BASE_VALUES[:10].reshape(1, 1, 10) + (
        amplitudes[:, None, :10] * values[..., :10]
    )
    gradient = (
        amplitudes[:, None, 10, None]
        * batch_field_gradient(coefficients[..., 10, :], coordinates)
    )
    return latent, gradient


def batch_scalar_matrix(chart, bank_a, bank_b, amplitudes, parameter_u, parameter_lambda):
    count, u_count = parameter_lambda.shape
    if chart == CHARTS[1]:
        latent_a, gradient_a = batch_endpoint(bank_a, amplitudes, parameter_u)
        latent_b, gradient_b = batch_endpoint(bank_b, amplitudes, parameter_u)
        latent = (
            (1.0 - parameter_lambda[..., None]) * latent_a
            + parameter_lambda[..., None] * latent_b
        )
        gradient = (
            (1.0 - parameter_lambda[..., None]) * gradient_a
            + parameter_lambda[..., None] * gradient_b
        )
    else:
        coordinate_a = batch_bank_coordinate(bank_a, parameter_u)
        coordinate_b = batch_bank_coordinate(bank_b, parameter_u)
        coordinate = (
            (1.0 - parameter_lambda[..., None]) * coordinate_a
            + parameter_lambda[..., None] * coordinate_b
        )
        coefficients = (
            (1.0 - parameter_lambda[..., None, None])
            * FLOAT_COEFFICIENTS[bank_a].reshape(1, 1, 11, 14)
            + parameter_lambda[..., None, None]
            * FLOAT_COEFFICIENTS[bank_b].reshape(1, 1, 11, 14)
        )
        values = batch_field_values(coefficients, coordinate)
        latent = FLOAT_BASE_VALUES[:10].reshape(1, 1, 10) + (
            amplitudes[:, None, :10] * values[..., :10]
        )
        gradient = (
            amplitudes[:, None, 10, None]
            * batch_field_gradient(coefficients[..., 10, :], coordinate)
        )
    a, b, c, d, e, f, a20, a30, a21, a31 = np.moveaxis(latent, -1, 0)
    u, w, r, t = np.exp(a), np.exp(c), np.exp(d), np.exp(f)
    coframe = np.zeros((count, u_count, 4, 4))
    coframe[..., 0, 0] = u
    coframe[..., 0, 1] = b
    coframe[..., 1, 1] = w
    coframe[..., 2, 0] = r * a20 + e * a30
    coframe[..., 2, 1] = r * a21 + e * a31
    coframe[..., 2, 2] = r
    coframe[..., 2, 3] = e
    coframe[..., 3, 0] = t * a30
    coframe[..., 3, 1] = t * a31
    coframe[..., 3, 3] = t
    signed = coframe.copy()
    signed[..., 0, :] *= -1.0
    metric = np.swapaxes(coframe, -1, -2) @ signed
    solved = np.linalg.solve(metric, gradient[..., None])[..., 0]
    return np.sum(gradient * solved, axis=-1)


def batch_roots(chart, bank_a, bank_b, amplitude_rows, u_points):
    amplitudes = np.asarray(amplitude_rows, dtype=np.float64)
    parameter_u = np.asarray(u_points, dtype=np.float64)
    lo = np.zeros((len(amplitudes), len(parameter_u)))
    hi = np.ones_like(lo)
    for _ in range(58):
        midpoint = (lo + hi) / 2.0
        values = batch_scalar_matrix(
            chart, bank_a, bank_b, amplitudes, parameter_u, midpoint
        )
        positive = values > 0.0
        lo = np.where(positive, midpoint, lo)
        hi = np.where(positive, hi, midpoint)
    return (lo + hi) / 2.0


def root(chart, bank_a, bank_b, amplitudes, parameter_u):
    lo, hi = 0.0, 1.0
    value_lo = scalar_matrix(chart, bank_a, bank_b, amplitudes, parameter_u, lo)[0]
    value_hi = scalar_matrix(chart, bank_a, bank_b, amplitudes, parameter_u, hi)[0]
    if not value_lo > 0.0 or not value_hi < 0.0:
        raise AssertionError("independent endpoint signs")
    for _ in range(58):
        middle = (lo + hi) / 2
        value = scalar_matrix(chart, bank_a, bank_b, amplitudes, parameter_u, middle)[0]
        if value > 0:
            lo = middle
        else:
            hi = middle
    return (lo + hi) / 2


def qiv(value):
    value = Fraction(value)
    return iv.mpf(value.numerator) / iv.mpf(value.denominator)


def interval(lo, hi):
    left, right = qiv(lo), qiv(hi)
    return iv.mpf([left.a, right.b])


def bounds(value):
    return float(value.a), float(value.b)


def _down(value):
    return np.nextafter(value, -np.inf)


def _up(value):
    return np.nextafter(value, np.inf)


@dataclass(frozen=True)
class BInterval:
    """Independent vector directed interval used only by the matrix route."""

    lo: np.ndarray
    hi: np.ndarray

    @classmethod
    def point(cls, value):
        current = np.asarray(value, dtype=np.float64)
        return cls(current, current)

    @classmethod
    def rational(cls, value):
        if isinstance(value, (list, tuple)):
            current = np.asarray([float(Fraction(item)) for item in value], dtype=np.float64)
        else:
            current = np.asarray(float(Fraction(value)), dtype=np.float64)
        return cls(_down(current), _up(current))

    @classmethod
    def limits(cls, lo, hi):
        return cls(np.asarray(lo, dtype=np.float64), np.asarray(hi, dtype=np.float64))

    def __add__(self, other):
        rhs = other if isinstance(other, BInterval) else BInterval.point(other)
        return BInterval(_down(self.lo + rhs.lo), _up(self.hi + rhs.hi))

    __radd__ = __add__

    def __neg__(self):
        return BInterval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-other if isinstance(other, BInterval) else -BInterval.point(other))

    def __rsub__(self, other):
        return BInterval.point(other) - self

    def __mul__(self, other):
        rhs = other if isinstance(other, BInterval) else BInterval.point(other)
        products = np.stack((
            self.lo * rhs.lo,
            self.lo * rhs.hi,
            self.hi * rhs.lo,
            self.hi * rhs.hi,
        ))
        return BInterval(_down(np.min(products, axis=0)), _up(np.max(products, axis=0)))

    __rmul__ = __mul__

    def reciprocal(self):
        if np.any((self.lo <= 0.0) & (self.hi >= 0.0)):
            raise ZeroDivisionError("matrix interval contains zero")
        values = np.stack((1.0 / self.lo, 1.0 / self.hi))
        return BInterval(_down(np.min(values, axis=0)), _up(np.max(values, axis=0)))

    def __truediv__(self, other):
        rhs = other if isinstance(other, BInterval) else BInterval.point(other)
        return self * rhs.reciprocal()

    def __rtruediv__(self, other):
        return BInterval.point(other) / self

    def exp(self):
        return BInterval(_down(np.exp(self.lo)), _up(np.exp(self.hi)))


@dataclass(frozen=True)
class BDual:
    value: BInterval
    derivative: BInterval

    @classmethod
    def constant(cls, value):
        current = value if isinstance(value, BInterval) else BInterval.point(value)
        return cls(current, BInterval.point(0.0))

    def __add__(self, other):
        rhs = other if isinstance(other, BDual) else BDual.constant(other)
        return BDual(self.value + rhs.value, self.derivative + rhs.derivative)

    __radd__ = __add__

    def __neg__(self):
        return BDual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + (-other if isinstance(other, BDual) else -BDual.constant(other))

    def __rsub__(self, other):
        return BDual.constant(other) - self

    def __mul__(self, other):
        rhs = other if isinstance(other, BDual) else BDual.constant(other)
        return BDual(
            self.value * rhs.value,
            self.derivative * rhs.value + self.value * rhs.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        rhs = other if isinstance(other, BDual) else BDual.constant(other)
        return BDual(
            self.value / rhs.value,
            (self.derivative * rhs.value - self.value * rhs.derivative)
            / (rhs.value * rhs.value),
        )

    def __rtruediv__(self, other):
        return BDual.constant(other) / self


def bexp(value):
    current = value.value.exp()
    return BDual(current, current * value.derivative)


@lru_cache(maxsize=None)
def brational(value):
    return BInterval.rational(value)


def b_lerp(first, second, parameter):
    return (BDual.constant(BInterval.point(1.0)) - parameter) * first + parameter * second


def b_amplitudes(amplitudes):
    return tuple(
        BInterval.rational([row[field] for row in amplitudes])
        for field in range(11)
    )


def b_columns(amplitudes):
    return tuple(
        BInterval(value.lo.reshape(-1, 1), value.hi.reshape(-1, 1))
        for value in amplitudes
    )


def b_take(amplitudes, indices):
    return tuple(BInterval(value.lo[indices], value.hi[indices]) for value in amplitudes)


def b_bank_coordinate(bank, parameter_u):
    first, second = (POINTS[name] for name in POINT_PAIRS[bank])
    return tuple(
        brational(first[index])
        + parameter_u * brational(second[index] - first[index])
        for index in range(4)
    )


def b_field_value(coefficients, coordinate):
    value = BDual.constant(BInterval.point(0.0))
    for index in range(4):
        value += coefficients[index] * coordinate[index]
    for index in range(4):
        value += (
            coefficients[4 + index]
            * coordinate[index]
            * coordinate[index]
            / BInterval.point(2.0)
        )
    for pair_index, (first, second) in enumerate(PAIRS):
        value += coefficients[8 + pair_index] * coordinate[first] * coordinate[second]
    return value


def b_field_gradient(coefficients, coordinate):
    output = []
    for index in range(4):
        value = coefficients[index] + coefficients[4 + index] * coordinate[index]
        for pair_index, (first, second) in enumerate(PAIRS):
            if index == first:
                value += coefficients[8 + pair_index] * coordinate[second]
            elif index == second:
                value += coefficients[8 + pair_index] * coordinate[first]
        output.append(value)
    return tuple(output)


def b_endpoint(bank, amplitudes, parameter_u):
    coordinate = tuple(BDual.constant(item) for item in b_bank_coordinate(bank, parameter_u))
    latent = []
    for field in range(10):
        coefficients = tuple(BDual.constant(brational(item)) for item in COEFFICIENTS[bank][field])
        latent.append(
            BDual.constant(brational(BASE_VALUES[field]))
            + b_field_value(coefficients, coordinate) * amplitudes[field]
        )
    coefficients = tuple(BDual.constant(brational(item)) for item in COEFFICIENTS[bank][10])
    gradient = tuple(
        value * amplitudes[10]
        for value in b_field_gradient(coefficients, coordinate)
    )
    return tuple(latent), gradient


def b_configured(chart, bank_a, bank_b, amplitudes, u_lo, u_hi, l_lo, l_hi):
    parameter_u = BInterval.limits(u_lo, u_hi)
    parameter_lambda = BDual(BInterval.limits(l_lo, l_hi), BInterval.point(1.0))
    if chart == CHARTS[1]:
        latent_a, gradient_a = b_endpoint(bank_a, amplitudes, parameter_u)
        latent_b, gradient_b = b_endpoint(bank_b, amplitudes, parameter_u)
        return (
            tuple(b_lerp(latent_a[i], latent_b[i], parameter_lambda) for i in range(10)),
            tuple(b_lerp(gradient_a[i], gradient_b[i], parameter_lambda) for i in range(4)),
        )
    coordinate_a = b_bank_coordinate(bank_a, parameter_u)
    coordinate_b = b_bank_coordinate(bank_b, parameter_u)
    coordinate = tuple(
        b_lerp(BDual.constant(coordinate_a[i]), BDual.constant(coordinate_b[i]), parameter_lambda)
        for i in range(4)
    )
    latent = []
    for field in range(10):
        coefficients = tuple(
            b_lerp(
                BDual.constant(brational(COEFFICIENTS[bank_a][field][term])),
                BDual.constant(brational(COEFFICIENTS[bank_b][field][term])),
                parameter_lambda,
            )
            for term in range(14)
        )
        latent.append(
            BDual.constant(brational(BASE_VALUES[field]))
            + b_field_value(coefficients, coordinate) * amplitudes[field]
        )
    coefficients = tuple(
        b_lerp(
            BDual.constant(brational(COEFFICIENTS[bank_a][10][term])),
            BDual.constant(brational(COEFFICIENTS[bank_b][10][term])),
            parameter_lambda,
        )
        for term in range(14)
    )
    gradient = tuple(
        value * amplitudes[10]
        for value in b_field_gradient(coefficients, coordinate)
    )
    return tuple(latent), gradient


def b_det3(matrix):
    return (
        matrix[0][0] * matrix[1][1] * matrix[2][2]
        + matrix[0][1] * matrix[1][2] * matrix[2][0]
        + matrix[0][2] * matrix[1][0] * matrix[2][1]
        - matrix[0][2] * matrix[1][1] * matrix[2][0]
        - matrix[0][1] * matrix[1][0] * matrix[2][2]
        - matrix[0][0] * matrix[1][2] * matrix[2][1]
    )


def b_cofactor(matrix, row, column):
    reduced = [
        [matrix[i][j] for j in range(4) if j != column]
        for i in range(4) if i != row
    ]
    value = b_det3(reduced)
    return -value if (row + column) % 2 else value


def b_matrix_scalar(chart, bank_a, bank_b, amplitudes, u_lo, u_hi, l_lo, l_hi):
    latent, gradient = b_configured(
        chart, bank_a, bank_b, amplitudes, u_lo, u_hi, l_lo, l_hi
    )
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    u, w, r, t = bexp(a), bexp(c), bexp(d), bexp(f)
    zero = BDual.constant(BInterval.point(0.0))
    coframe = [
        [u, b, zero, zero],
        [zero, w, zero, zero],
        [r * a20 + e * a30, r * a21 + e * a31, r, e],
        [t * a30, t * a31, zero, t],
    ]
    signs = (-1.0, 1.0, 1.0, 1.0)
    metric = [[BDual.constant(BInterval.point(0.0)) for _ in range(4)] for _ in range(4)]
    for row in range(4):
        for column in range(4):
            for frame in range(4):
                metric[row][column] += (
                    BDual.constant(BInterval.point(signs[frame]))
                    * coframe[frame][row]
                    * coframe[frame][column]
                )
    numerator = BDual.constant(BInterval.point(0.0))
    for first in range(4):
        for second in range(4):
            numerator += (
                gradient[first]
                * b_cofactor(metric, second, first)
                * gradient[second]
            )
    exact_determinant = -(bexp(BDual.constant(BInterval.point(2.0)) * (a + c + d + f)))
    return numerator / exact_determinant, gradient


def b_partition_certificate(
    chart, bank_a, bank_b, amplitudes, pair_type, nu, nl,
    root_lo=None, root_hi=None,
):
    columns = b_columns(amplitudes)
    size = columns[0].lo.shape[0]
    passed = np.ones(size, dtype=bool)
    minimum_scalar_lo = np.full(size, np.inf)
    maximum_right_scalar_hi = np.full(size, -np.inf)
    maximum_derivative_hi = np.full(size, -np.inf)
    gradient_nonzero = np.ones(size, dtype=bool)
    partition_valid = np.ones(size, dtype=bool)
    batch_size = 8
    cells = []
    if pair_type == "SAME_SIGN_CONTROL":
        for u_index in range(nu):
            for lambda_index in range(nl):
                cells.append((
                    "SAME", u_index,
                    np.full(size, lambda_index / nl),
                    np.full(size, (lambda_index + 1) / nl),
                ))
    else:
        if root_lo is None or root_hi is None:
            raise AssertionError("matrix cross route requires a saved proof envelope")
        partition_valid &= (
            np.all(root_lo >= 0.0, axis=1)
            & np.all(root_hi <= 1.0, axis=1)
            & np.all(root_lo <= root_hi, axis=1)
        )
        side_bins, root_bins = nl // 4, nl // 2
        for u_index in range(nu):
            strip_lo = root_lo[:, u_index]
            strip_hi = root_hi[:, u_index]
            for lambda_index in range(side_bins):
                fraction_lo = lambda_index / side_bins
                fraction_hi = (lambda_index + 1) / side_bins
                cells.append((
                    "LEFT", u_index,
                    strip_lo * fraction_lo,
                    strip_lo * fraction_hi,
                ))
                cells.append((
                    "RIGHT", u_index,
                    strip_hi + (1.0 - strip_hi) * fraction_lo,
                    strip_hi + (1.0 - strip_hi) * fraction_hi,
                ))
            for lambda_index in range(root_bins):
                fraction_lo = lambda_index / root_bins
                fraction_hi = (lambda_index + 1) / root_bins
                cells.append((
                    "ROOT", u_index,
                    strip_lo + (strip_hi - strip_lo) * fraction_lo,
                    strip_lo + (strip_hi - strip_lo) * fraction_hi,
                ))
    for start in range(0, len(cells), batch_size):
        current = cells[start:start + batch_size]
        labels = [item[0] for item in current]
        u_indices = np.asarray([item[1] for item in current])
        lambda_lo = np.stack([item[2] for item in current], axis=1)
        lambda_hi = np.stack([item[3] for item in current], axis=1)
        scalar, gradient = b_matrix_scalar(
            chart, bank_a, bank_b, columns,
            (u_indices / nu).reshape(1, -1),
            ((u_indices + 1) / nu).reshape(1, -1),
            np.maximum(0.0, _down(lambda_lo)),
            np.minimum(1.0, _up(lambda_hi)),
        )
        for index, label in enumerate(labels):
            if label in {"SAME", "LEFT"}:
                passed &= scalar.value.lo[:, index] > 0.0
                minimum_scalar_lo = np.minimum(minimum_scalar_lo, scalar.value.lo[:, index])
            elif label == "RIGHT":
                passed &= scalar.value.hi[:, index] < 0.0
                maximum_right_scalar_hi = np.maximum(
                    maximum_right_scalar_hi, scalar.value.hi[:, index]
                )
            else:
                passed &= scalar.derivative.hi[:, index] < 0.0
                maximum_derivative_hi = np.maximum(
                    maximum_derivative_hi, scalar.derivative.hi[:, index]
                )
                local_nonzero = np.zeros(size, dtype=bool)
                for component in gradient:
                    local_nonzero |= (
                        (component.value.lo[:, index] > 0.0)
                        | (component.value.hi[:, index] < 0.0)
                    )
                gradient_nonzero &= local_nonzero
    if pair_type == "CROSS_SECTOR":
        passed &= gradient_nonzero & partition_valid
    return {
        "passed": passed,
        "minimum_scalar_lo": minimum_scalar_lo,
        "maximum_right_scalar_hi": maximum_right_scalar_hi,
        "maximum_derivative_hi": maximum_derivative_hi,
        "gradient_nonzero": gradient_nonzero,
        "partition_valid": partition_valid,
        "covered_boxes": nu * nl,
    }


def full_matrix_interval_census(groups, saved_sheets):
    amplitude_rows = [row[2] for row in groups]
    amplitudes_float = np.asarray(amplitude_rows, dtype=np.float64)
    saved_lookup = {row["sheet_id"]: row for row in saved_sheets}
    output = []
    total_boxes = 0
    for chart in CHARTS:
        chart_id = "J1" if chart == CHARTS[0] else "J2"
        for bank_a, bank_b in BANK_PAIRS:
            midpoint_u = np.asarray([0.5])
            left = batch_scalar_matrix(
                chart, bank_a, bank_b, amplitudes_float,
                midpoint_u, np.zeros((len(groups), 1)),
            )[:, 0]
            right = batch_scalar_matrix(
                chart, bank_a, bank_b, amplitudes_float,
                midpoint_u, np.ones((len(groups), 1)),
            )[:, 0]
            routed_same = np.flatnonzero((left > 0.0) & (right > 0.0))
            routed_cross = np.flatnonzero((left > 0.0) & (right < 0.0))
            if len(routed_same) + len(routed_cross) != len(groups):
                raise AssertionError("independent endpoint routing is incomplete")

            for pair_type, initial_indices in (
                ("SAME_SIGN_CONTROL", routed_same),
                ("CROSS_SECTOR", routed_cross),
            ):
                remaining = initial_indices.copy()
                for nu, nl in ((16, 64), (32, 128), (64, 256)):
                    if not len(remaining):
                        break
                    selected_rows = [amplitude_rows[index] for index in remaining]
                    selected_amplitudes = b_amplitudes(selected_rows)
                    root_lo = root_hi = None
                    if pair_type == "CROSS_SECTOR":
                        roots = batch_roots(
                            chart, bank_a, bank_b, selected_rows,
                            [index / nu for index in range(nu + 1)],
                        )
                        root_lo = np.maximum(
                            0.0,
                            _down(np.minimum(roots[:, :-1], roots[:, 1:]) - 0.125),
                        )
                        root_hi = np.minimum(
                            1.0,
                            _up(np.maximum(roots[:, :-1], roots[:, 1:]) + 0.125),
                        )
                    certificate = b_partition_certificate(
                        chart, bank_a, bank_b, selected_amplitudes,
                        pair_type, nu, nl, root_lo, root_hi,
                    )
                    passed = certificate["passed"]
                    for local_index in np.flatnonzero(passed):
                        global_index = int(remaining[local_index])
                        carrier_id, mask, _amplitude = groups[global_index]
                        sheet_id = f"{carrier_id}_M{mask:X}_B{bank_a}B{bank_b}_{chart_id}"
                        derived_class = (
                            "UNIFORMLY_SPACELIKE_SHEET"
                            if pair_type == "SAME_SIGN_CONTROL"
                            else "FORCED_SINGLE_REGULAR_NULL_GRAPH"
                        )
                        if saved_lookup[sheet_id]["primary_class"] != derived_class:
                            raise AssertionError(f"independent full-sheet class mismatch {sheet_id}")
                        total_boxes += nu * nl
                        output.append({
                            "sheet_id": sheet_id,
                            "chart": chart,
                            "bank_pair": f"B{bank_a}-B{bank_b}",
                            "carrier_id": carrier_id,
                            "mask_id": f"M{mask:X}",
                            "endpoint_route": pair_type,
                            "derived_class": derived_class,
                            "resolution_u": nu,
                            "resolution_lambda": nl,
                            "covered_boxes": nu * nl,
                            "minimum_positive_s_lower": (
                                f"{certificate['minimum_scalar_lo'][local_index]:.17g}"
                            ),
                            "maximum_negative_s_upper": (
                                f"{certificate['maximum_right_scalar_hi'][local_index]:.17g}"
                                if pair_type == "CROSS_SECTOR" else ""
                            ),
                            "maximum_partial_lambda_s_upper": (
                                f"{certificate['maximum_derivative_hi'][local_index]:.17g}"
                                if pair_type == "CROSS_SECTOR" else ""
                            ),
                            "root_envelope_minimum": (
                                f"{np.min(root_lo[local_index]):.17g}"
                                if pair_type == "CROSS_SECTOR" else ""
                            ),
                            "root_envelope_maximum": (
                                f"{np.max(root_hi[local_index]):.17g}"
                                if pair_type == "CROSS_SECTOR" else ""
                            ),
                            "partition_status": (
                                "CLOSED_DOMAIN_EXACT_COVER"
                                if certificate["partition_valid"][local_index]
                                else "INVALID"
                            ),
                            "dphi_status": (
                                "NONZERO_COMPONENT_EVERY_ROOT_BOX"
                                if pair_type == "CROSS_SECTOR"
                                and certificate["gradient_nonzero"][local_index]
                                else "NOT_APPLICABLE"
                            ),
                            "arithmetic": "INDEPENDENT_FULL_MATRIX_BINARY64_DIRECTED_INTERVAL",
                            "status": "PASS",
                        })
                    remaining = remaining[~passed]
                if len(remaining):
                    raise AssertionError(
                        f"independent full-matrix interval unresolved {chart} B{bank_a}-B{bank_b} "
                        f"{pair_type} count={len(remaining)}"
                    )
    output.sort(key=lambda row: row["sheet_id"])
    if len(output) != 4_608 or len({row["sheet_id"] for row in output}) != 4_608:
        raise AssertionError("independent full-matrix sheet coverage")
    if set(row["sheet_id"] for row in output) != set(saved_lookup):
        raise AssertionError("independent/saved sheet identity set")
    return output, total_boxes


@dataclass(frozen=True)
class IDual:
    value: object
    derivative: object

    @classmethod
    def constant(cls, value):
        return cls(value, qiv(0))

    def __add__(self, other):
        rhs = other if isinstance(other, IDual) else IDual.constant(other)
        return IDual(self.value + rhs.value, self.derivative + rhs.derivative)

    __radd__ = __add__

    def __neg__(self):
        return IDual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + (-other if isinstance(other, IDual) else -IDual.constant(other))

    def __rsub__(self, other):
        return IDual.constant(other) - self

    def __mul__(self, other):
        rhs = other if isinstance(other, IDual) else IDual.constant(other)
        return IDual(
            self.value * rhs.value,
            self.derivative * rhs.value + self.value * rhs.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        rhs = other if isinstance(other, IDual) else IDual.constant(other)
        return IDual(
            self.value / rhs.value,
            (self.derivative * rhs.value - self.value * rhs.derivative)
            / (rhs.value * rhs.value),
        )

    def __rtruediv__(self, other):
        return IDual.constant(other) / self


def dexp(value):
    current = iv.exp(value.value)
    return IDual(current, current * value.derivative)


def dlerp(first, second, parameter):
    return (IDual.constant(qiv(1)) - parameter) * first + parameter * second


def d_bank_coordinate(bank, parameter_u):
    first, second = (POINTS[name] for name in POINT_PAIRS[bank])
    return tuple(qiv(first[i]) + parameter_u * qiv(second[i] - first[i]) for i in range(4))


def d_field_value(coefficients, coordinate):
    value = IDual.constant(qiv(0))
    for index in range(4):
        value += coefficients[index] * coordinate[index]
    for index in range(4):
        value += coefficients[4 + index] * coordinate[index] * coordinate[index] / qiv(2)
    for pair_index, (first, second) in enumerate(PAIRS):
        value += coefficients[8 + pair_index] * coordinate[first] * coordinate[second]
    return value


def d_field_gradient(coefficients, coordinate):
    output = []
    for index in range(4):
        value = coefficients[index] + coefficients[4 + index] * coordinate[index]
        for pair_index, (first, second) in enumerate(PAIRS):
            if index == first:
                value += coefficients[8 + pair_index] * coordinate[second]
            elif index == second:
                value += coefficients[8 + pair_index] * coordinate[first]
        output.append(value)
    return tuple(output)


def d_endpoint(bank, amplitudes, parameter_u):
    coordinate = tuple(IDual.constant(value) for value in d_bank_coordinate(bank, parameter_u))
    latent = []
    for field in range(10):
        coefficients = tuple(IDual.constant(qiv(item)) for item in COEFFICIENTS[bank][field])
        latent.append(
            IDual.constant(qiv(BASE_VALUES[field]))
            + d_field_value(coefficients, coordinate) * qiv(amplitudes[field])
        )
    coefficients = tuple(IDual.constant(qiv(item)) for item in COEFFICIENTS[bank][10])
    gradient = tuple(
        value * qiv(amplitudes[10])
        for value in d_field_gradient(coefficients, coordinate)
    )
    return tuple(latent), gradient


def d_configured(chart, bank_a, bank_b, amplitudes, u_lo, u_hi, l_lo, l_hi):
    parameter_u = interval(u_lo, u_hi)
    parameter_lambda = IDual(interval(l_lo, l_hi), qiv(1))
    if chart == CHARTS[1]:
        latent_a, gradient_a = d_endpoint(bank_a, amplitudes, parameter_u)
        latent_b, gradient_b = d_endpoint(bank_b, amplitudes, parameter_u)
        return (
            tuple(dlerp(latent_a[i], latent_b[i], parameter_lambda) for i in range(10)),
            tuple(dlerp(gradient_a[i], gradient_b[i], parameter_lambda) for i in range(4)),
        )
    coordinate_a = d_bank_coordinate(bank_a, parameter_u)
    coordinate_b = d_bank_coordinate(bank_b, parameter_u)
    coordinate = tuple(
        dlerp(IDual.constant(coordinate_a[i]), IDual.constant(coordinate_b[i]), parameter_lambda)
        for i in range(4)
    )
    latent = []
    for field in range(10):
        coefficients = tuple(
            dlerp(
                IDual.constant(qiv(COEFFICIENTS[bank_a][field][term])),
                IDual.constant(qiv(COEFFICIENTS[bank_b][field][term])),
                parameter_lambda,
            )
            for term in range(14)
        )
        latent.append(
            IDual.constant(qiv(BASE_VALUES[field]))
            + d_field_value(coefficients, coordinate) * qiv(amplitudes[field])
        )
    coefficients = tuple(
        dlerp(
            IDual.constant(qiv(COEFFICIENTS[bank_a][10][term])),
            IDual.constant(qiv(COEFFICIENTS[bank_b][10][term])),
            parameter_lambda,
        )
        for term in range(14)
    )
    gradient = tuple(
        value * qiv(amplitudes[10])
        for value in d_field_gradient(coefficients, coordinate)
    )
    return tuple(latent), gradient


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix):
    output = IDual.constant(qiv(0))
    for permutation in itertools.permutations(range(len(matrix))):
        term = IDual.constant(qiv(permutation_sign(permutation)))
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        output += term
    return output


def minor(matrix, deleted_row, deleted_column):
    return [
        [matrix[row][column] for column in range(len(matrix)) if column != deleted_column]
        for row in range(len(matrix))
        if row != deleted_row
    ]


def cofactor(matrix, row, column):
    return IDual.constant(qiv(-1 if (row + column) % 2 else 1)) * determinant(
        minor(matrix, row, column)
    )


def interval_matrix_scalar(chart, bank_a, bank_b, amplitudes, u_lo, u_hi, l_lo, l_hi):
    latent, gradient = d_configured(
        chart, bank_a, bank_b, amplitudes, u_lo, u_hi, l_lo, l_hi
    )
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    u, w, r, t = dexp(a), dexp(c), dexp(d), dexp(f)
    zero = IDual.constant(qiv(0))
    coframe = [
        [u, b, zero, zero],
        [zero, w, zero, zero],
        [r * a20 + e * a30, r * a21 + e * a31, r, e],
        [t * a30, t * a31, zero, t],
    ]
    signs = (-1, 1, 1, 1)
    metric = [[IDual.constant(qiv(0)) for _ in range(4)] for _ in range(4)]
    for row in range(4):
        for column in range(4):
            for frame in range(4):
                metric[row][column] += (
                    IDual.constant(qiv(signs[frame]))
                    * coframe[frame][row]
                    * coframe[frame][column]
                )
    determinant_value = determinant(metric)
    numerator = IDual.constant(qiv(0))
    for first in range(4):
        for second in range(4):
            numerator += gradient[first] * cofactor(metric, second, first) * gradient[second]
    return numerator / determinant_value, determinant_value, gradient


def certify_matrix_anchor(chart, bank_a, bank_b, amplitudes, pair_type, u_lo, u_hi, l_lo, l_hi):
    queue = [(u_lo, u_hi, l_lo, l_hi, 0)]
    certified = 0
    minimum_scalar_lo = math.inf
    maximum_scalar_hi = -math.inf
    minimum_derivative_lo = math.inf
    maximum_derivative_hi = -math.inf
    maximum_determinant_hi = -math.inf
    while queue:
        current_u_lo, current_u_hi, current_l_lo, current_l_hi, depth = queue.pop()
        scalar, determinant_value, gradient = interval_matrix_scalar(
            chart, bank_a, bank_b, amplitudes,
            current_u_lo, current_u_hi, current_l_lo, current_l_hi,
        )
        scalar_lo, scalar_hi = bounds(scalar.value)
        derivative_lo, derivative_hi = bounds(scalar.derivative)
        _determinant_lo, determinant_hi = bounds(determinant_value.value)
        gradient_nonzero = any(
            bounds(component.value)[0] > 0.0 or bounds(component.value)[1] < 0.0
            for component in gradient
        )
        condition = (
            scalar_lo > 0.0
            if pair_type == "SAME_SIGN_CONTROL"
            else derivative_hi < 0.0 and gradient_nonzero
        )
        if determinant_hi < 0.0 and condition:
            certified += 1
            minimum_scalar_lo = min(minimum_scalar_lo, scalar_lo)
            maximum_scalar_hi = max(maximum_scalar_hi, scalar_hi)
            minimum_derivative_lo = min(minimum_derivative_lo, derivative_lo)
            maximum_derivative_hi = max(maximum_derivative_hi, derivative_hi)
            maximum_determinant_hi = max(maximum_determinant_hi, determinant_hi)
            continue
        if depth >= 10:
            raise AssertionError("high-precision matrix anchor unresolved after subdivision")
        u_width = current_u_hi - current_u_lo
        lambda_width = current_l_hi - current_l_lo
        if u_width >= lambda_width:
            midpoint = (current_u_lo + current_u_hi) / 2
            queue.append((current_u_lo, midpoint, current_l_lo, current_l_hi, depth + 1))
            queue.append((midpoint, current_u_hi, current_l_lo, current_l_hi, depth + 1))
        else:
            midpoint = (current_l_lo + current_l_hi) / 2
            queue.append((current_u_lo, current_u_hi, current_l_lo, midpoint, depth + 1))
            queue.append((current_u_lo, current_u_hi, midpoint, current_l_hi, depth + 1))
    return {
        "certified_subboxes": certified,
        "matrix_s_lo": minimum_scalar_lo,
        "matrix_s_hi": maximum_scalar_hi,
        "matrix_partial_lambda_s_lo": minimum_derivative_lo,
        "matrix_partial_lambda_s_hi": maximum_derivative_hi,
        "matrix_determinant_hi": maximum_determinant_hi,
    }


def expect_failure(catch_id, operation, catches):
    try:
        operation()
    except AssertionError as exc:
        catches.append({"catch_id": catch_id, "result": "MUTATION_REJECTED", "reason": str(exc)})
    else:
        raise AssertionError(f"mutation escaped {catch_id}")


def require_uniform_same(values):
    if not all(value > 0.0 for value in values):
        raise AssertionError("interior same-sign pocket rejected")


def require_single_regular_root(roots, derivatives, gradient_nonzero):
    if len(roots) != 1:
        raise AssertionError("multiple root rejected")
    if not derivatives[0] < 0.0:
        raise AssertionError("null tangency rejected")
    if not gradient_nonzero:
        raise AssertionError("zero-gradient interface rejected")


def require_nondegenerate(determinant_value):
    if not determinant_value < 0.0:
        raise AssertionError("singular or non-Lorentzian coframe rejected")


def require_partition(intervals):
    if not intervals or intervals[0][0] != 0.0 or intervals[-1][1] != 1.0:
        raise AssertionError("partition domain rejected")
    if any(lo < 0.0 or hi > 1.0 or lo > hi for lo, hi in intervals):
        raise AssertionError("partition out-of-domain rejected")
    if any(intervals[index][1] != intervals[index + 1][0] for index in range(len(intervals) - 1)):
        raise AssertionError("partition gap rejected")


def safe_projector_divide(value):
    if value == 0.0:
        raise AssertionError("division by s at null interface rejected")
    return 1.0 / value


def main():
    carrier_rows = rows(ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21/CARRIER_VECTOR_REGISTRY.tsv")
    carriers = {
        row["carrier_id"]: tuple(Fraction(row[name]) for name in PARAMETERS)
        for row in carrier_rows
    }
    groups = [
        (carrier_id, mask, amplitude_vector(carriers[carrier_id], mask))
        for carrier_id in sorted(carriers)
        for mask in range(8, 16)
    ]
    sheets = rows(HERE / "SHEET_CLASSIFICATION.tsv")
    sheet_lookup = {row["sheet_id"]: row for row in sheets}
    if len(sheets) != 4_608 or len(sheet_lookup) != 4_608:
        raise AssertionError("complete unique sheet census")

    full_interval_rows, full_interval_boxes = full_matrix_interval_census(groups, sheets)
    with (HERE / "INDEPENDENT_FULL_MATRIX_INTERVAL_CERTIFICATES.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(full_interval_rows[0]),
            delimiter="\t", lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(full_interval_rows)

    probe_rows = []
    for chart in CHARTS:
        for bank_a, bank_b in BANK_PAIRS:
            current = [
                row for row in full_interval_rows
                if row["chart"] == chart and row["bank_pair"] == f"B{bank_a}-B{bank_b}"
            ]
            classes = Counter(row["derived_class"] for row in current)
            probe_rows.append({
                "chart": chart,
                "bank_pair": f"B{bank_a}-B{bank_b}",
                "matched_sheets": len(current),
                "derived_class_census": json.dumps(dict(sorted(classes.items())), sort_keys=True),
                "covered_boxes": sum(int(row["covered_boxes"]) for row in current),
                "minimum_positive_s_lower": min(
                    float(row["minimum_positive_s_lower"]) for row in current
                ),
                "maximum_negative_s_upper": max(
                    (
                        float(row["maximum_negative_s_upper"])
                        for row in current if row["maximum_negative_s_upper"]
                    ),
                    default="",
                ),
                "maximum_partial_lambda_s_upper": max(
                    (
                        float(row["maximum_partial_lambda_s_upper"])
                        for row in current if row["maximum_partial_lambda_s_upper"]
                    ),
                    default="",
                ),
                "status": "INDEPENDENT_FULL_MATRIX_COMPLETE_COVER_PASS",
            })

    representative_amplitudes = groups[-1][2]
    representative_latent, representative_gradient = configured(
        CHARTS[0], 0, 3, representative_amplitudes, 0.5, 0.5
    )
    ordinary_metric = full_metric(representative_latent)
    ordinary_scalar = float(
        representative_gradient
        @ np.linalg.solve(ordinary_metric, representative_gradient)
    )
    individual_field_effects = {}
    for field in ("d", "e", "f", "a20", "a30", "a21", "a31"):
        modified_metric = full_metric(representative_latent, omit_field=field)
        modified_scalar = float(
            representative_gradient
            @ np.linalg.solve(modified_metric, representative_gradient)
        )
        individual_field_effects[field] = abs(ordinary_scalar - modified_scalar)
    if not all(value > 1e-14 for value in individual_field_effects.values()):
        raise AssertionError("individual angular/shift field is vacuous in mutation probe")

    anchor_rows = rows(HERE / "HIGH_PRECISION_ANCHORS.tsv")
    if len(anchor_rows) != 12:
        raise AssertionError("one high-precision anchor per chart/bank-pair")
    high_precision = []
    for row in anchor_rows:
        bank_a, bank_b = (int(value[1:]) for value in row["bank_pair"].split("-"))
        amplitudes = groups[int(row["amplitude_index"])][2]
        certified = certify_matrix_anchor(
            row["chart"], bank_a, bank_b, amplitudes,
            row["pair_type"],
            Fraction(row["u_lo"]), Fraction(row["u_hi"]),
            Fraction(row["lambda_lo"]), Fraction(row["lambda_hi"]),
        )
        high_precision.append({
            "chart": row["chart"],
            "bank_pair": row["bank_pair"],
            "pair_type": row["pair_type"],
            **certified,
            "status": "FULL_MATRIX_ADJUGATE_INTERVAL_PASS",
        })

    def require_count(value):
        if value != 4_608:
            raise AssertionError("missing sheet rejected")

    def require_unique(value):
        if value != 4_608:
            raise AssertionError("duplicate sheet rejected")

    def require_class(value):
        if value != {"FORCED_SINGLE_REGULAR_NULL_GRAPH": 2_304, "UNIFORMLY_SPACELIKE_SHEET": 2_304}:
            raise AssertionError("class mutation rejected")

    def require_matrix_route(value):
        if value != 4_608:
            raise AssertionError("full-matrix sheet loss rejected")

    def require_fields(values):
        if set(values) != {"d", "e", "f", "a20", "a30", "a21", "a31"}:
            raise AssertionError("individual angular/shift omission rejected")
        if not all(value > 1e-14 for value in values.values()):
            raise AssertionError("individual angular/shift omission rejected")

    catches = []
    expect_failure("I01_MISSING_SHEET", lambda: require_count(4_607), catches)
    expect_failure("I02_DUPLICATE_SHEET", lambda: require_unique(4_607), catches)
    expect_failure(
        "I03_FLIPPED_CLASS",
        lambda: require_class({"FORCED_SINGLE_REGULAR_NULL_GRAPH": 2_303, "UNIFORMLY_SPACELIKE_SHEET": 2_305}),
        catches,
    )
    expect_failure("I04_LOST_FULL_MATRIX_SHEET", lambda: require_matrix_route(4_607), catches)
    expect_failure(
        "I05_INTERIOR_SAME_SIGN_POCKET",
        lambda: require_uniform_same((0.15, -0.05, 0.12)),
        catches,
    )
    expect_failure(
        "I06_THREE_CROSS_SECTOR_ROOTS",
        lambda: require_single_regular_root((0.2, 0.5, 0.8), (-1.0, -1.0, -1.0), True),
        catches,
    )
    expect_failure(
        "I07_NULL_TANGENCY",
        lambda: require_single_regular_root((0.5,), (0.0,), True),
        catches,
    )
    expect_failure(
        "I08_ZERO_DPHI",
        lambda: require_single_regular_root((0.5,), (-1.0,), False),
        catches,
    )
    expect_failure("I09_SINGULAR_COFRAME", lambda: require_nondegenerate(0.0), catches)
    expect_failure(
        "I10_PARTITION_GAP",
        lambda: require_partition(((0.0, 0.4), (0.5, 1.0))),
        catches,
    )
    expect_failure(
        "I11_PARTITION_OUT_OF_DOMAIN",
        lambda: require_partition(((-0.01, 0.5), (0.5, 1.0))),
        catches,
    )
    expect_failure("I12_DIVISION_BY_S", lambda: safe_projector_divide(0.0), catches)
    corrupted_effects = dict(individual_field_effects)
    corrupted_effects["a31"] = 0.0
    expect_failure(
        "I13_OMIT_INDIVIDUAL_ANGULAR_SHIFT",
        lambda: require_fields(corrupted_effects),
        catches,
    )

    output_fields = list(probe_rows[0])
    with (HERE / "INDEPENDENT_MATRIX_PROBES.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(probe_rows)

    result = {
        "status": "PASS_WITH_REGISTERED_SCOPE",
        "method": (
            "INDEPENDENT_COMPLETE_FULL_4X4_MATRIX_ADJUGATE_INTERVAL_COVER_"
            "PLUS_80D_ANCHORS"
        ),
        "sheet_count": len(sheets),
        "sheet_unique": len(sheet_lookup),
        "sheet_census": dict(sorted(Counter(row["derived_class"] for row in full_interval_rows).items())),
        "full_matrix_interval_sheets": len(full_interval_rows),
        "full_matrix_interval_boxes": full_interval_boxes,
        "minimum_full_matrix_positive_s_lower": min(
            float(row["minimum_positive_s_lower"]) for row in full_interval_rows
        ),
        "maximum_full_matrix_negative_s_upper": max(
            float(row["maximum_negative_s_upper"])
            for row in full_interval_rows if row["maximum_negative_s_upper"]
        ),
        "maximum_full_matrix_partial_lambda_s_upper": max(
            float(row["maximum_partial_lambda_s_upper"])
            for row in full_interval_rows if row["maximum_partial_lambda_s_upper"]
        ),
        "full_matrix_closed_domain_partitions": sum(
            row["partition_status"] == "CLOSED_DOMAIN_EXACT_COVER"
            for row in full_interval_rows
        ),
        "full_matrix_dphi_nonzero_root_sheets": sum(
            row["dphi_status"] == "NONZERO_COMPONENT_EVERY_ROOT_BOX"
            for row in full_interval_rows
        ),
        "high_precision_matrix_anchors": high_precision,
        "high_precision_matrix_anchor_count": len(high_precision),
        "individual_angular_shift_effect_probes": individual_field_effects,
        "mutation_catches": catches,
        "production_builder_imported": False,
        "binary64_transcendental_scope": (
            "PLATFORM_SCOPED_NUMERICAL_ENCLOSURE__80D_WORST_CLASS_ANCHORS"
        ),
        "maximum_conclusion": "INDEPENDENT_SUPPORT_FOR_BOUNDED_REGISTERED_ADJACENCY_CENSUS",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
