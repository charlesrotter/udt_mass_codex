#!/usr/bin/env python3
"""Build the preregistered UDT configuration-space bank-edge adjacency atlas."""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import itertools
import json
import math
import subprocess
from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from mpmath import iv
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
IV_DPS = 80
MAX_CONTROL_DEPTH = 18
MAX_CROSS_U_DEPTH = 12
MAX_DERIVATIVE_LAMBDA_DEPTH = 10

SOURCE_DIR = ROOT / "udt_motif_hopf_correspondence_audit_2026-07-22"
PHI_DIR = ROOT / "udt_phi_causal_interface_atlas_2026-07-22"
CARRIER_FILE = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21/CARRIER_VECTOR_REGISTRY.tsv"
IDENTITY_FILE = SOURCE_DIR / "COHERENT_IDENTITY_REGISTRY.tsv"
CAUSAL_FILE = PHI_DIR / "IDENTITY_CAUSAL_CERTIFICATES.tsv"

PARAMETERS = tuple(f"alpha_{index}" for index in range(10)) + ("beta",)
BASE_VALUES = tuple(map(Fraction, ("0.08", "0.14", "-0.06", "0.12", "-0.09", "0.05", "0.11", "-0.07", "0.09", "0.04")))
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


def read_tsv(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path, fieldnames, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_tsv_gz(path, fieldnames, rows):
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=0) as compressed:
        with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    Path(path).write_bytes(buffer.getvalue())


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def coefficient(bank, field, term):
    raw = ((bank + 2) * 11 + (field + 1) * 7 + (term + 1) * 5 + (bank + 1) * (field + term + 3)) % 19 - 9
    if raw == 0:
        raw = 1 if (bank + field + term) % 2 == 0 else -1
    return Fraction(raw, 60 if term < 4 else 90 if term < 8 else 120)


COEFFICIENTS = tuple(
    tuple(tuple(coefficient(bank, field, term) for term in range(14)) for field in range(11))
    for bank in range(4)
)


def qiv(value):
    value = Fraction(value)
    return iv.mpf(value.numerator) / iv.mpf(value.denominator)


def make_interval(lo, hi):
    left, right = qiv(lo), qiv(hi)
    return iv.mpf([left.a, right.b])


def bounds(value):
    return float(value.a), float(value.b)


def fmt(value):
    return f"{value:.17g}"


@dataclass(frozen=True)
class Dual:
    value: object
    derivative: object

    @classmethod
    def constant(cls, value):
        return cls(value, qiv(0))

    def __add__(self, other):
        rhs = other if isinstance(other, Dual) else Dual.constant(other)
        return Dual(self.value + rhs.value, self.derivative + rhs.derivative)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Dual) else -Dual.constant(other))

    def __rsub__(self, other):
        return Dual.constant(other) - self

    def __mul__(self, other):
        rhs = other if isinstance(other, Dual) else Dual.constant(other)
        return Dual(
            self.value * rhs.value,
            self.derivative * rhs.value + self.value * rhs.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        rhs = other if isinstance(other, Dual) else Dual.constant(other)
        return Dual(
            self.value / rhs.value,
            (self.derivative * rhs.value - self.value * rhs.derivative) / (rhs.value * rhs.value),
        )

    def __rtruediv__(self, other):
        return Dual.constant(other) / self


def dual_exp(value):
    current = iv.exp(value.value)
    return Dual(current, current * value.derivative)


def _down(value):
    return np.nextafter(value, -np.inf)


def _up(value):
    return np.nextafter(value, np.inf)


@dataclass(frozen=True)
class VInterval:
    """Vectorized binary64 interval with explicit outward rounding."""

    lo: np.ndarray
    hi: np.ndarray

    @classmethod
    def point(cls, value):
        array = np.asarray(value, dtype=np.float64)
        return cls(array, array)

    @classmethod
    def enclosing_fraction(cls, value):
        if isinstance(value, np.ndarray):
            center = value.astype(np.float64)
        elif isinstance(value, (list, tuple)):
            center = np.asarray([float(Fraction(item)) for item in value], dtype=np.float64)
        else:
            center = np.asarray(float(Fraction(value)), dtype=np.float64)
        return cls(_down(center), _up(center))

    @classmethod
    def bounds(cls, lo, hi):
        return cls(np.asarray(lo, dtype=np.float64), np.asarray(hi, dtype=np.float64))

    def __add__(self, other):
        rhs = other if isinstance(other, VInterval) else VInterval.point(other)
        return VInterval(_down(self.lo + rhs.lo), _up(self.hi + rhs.hi))

    __radd__ = __add__

    def __neg__(self):
        return VInterval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-other if isinstance(other, VInterval) else -VInterval.point(other))

    def __rsub__(self, other):
        return VInterval.point(other) - self

    def __mul__(self, other):
        rhs = other if isinstance(other, VInterval) else VInterval.point(other)
        products = np.stack(
            (
                self.lo * rhs.lo,
                self.lo * rhs.hi,
                self.hi * rhs.lo,
                self.hi * rhs.hi,
            )
        )
        return VInterval(_down(np.min(products, axis=0)), _up(np.max(products, axis=0)))

    __rmul__ = __mul__

    def reciprocal(self):
        if np.any((self.lo <= 0.0) & (self.hi >= 0.0)):
            raise ZeroDivisionError("interval contains zero")
        values = np.stack((1.0 / self.lo, 1.0 / self.hi))
        return VInterval(_down(np.min(values, axis=0)), _up(np.max(values, axis=0)))

    def __truediv__(self, other):
        rhs = other if isinstance(other, VInterval) else VInterval.point(other)
        return self * rhs.reciprocal()

    def __rtruediv__(self, other):
        return VInterval.point(other) / self

    def exp(self):
        return VInterval(_down(np.exp(self.lo)), _up(np.exp(self.hi)))


@dataclass(frozen=True)
class VDual:
    value: VInterval
    derivative: VInterval

    @classmethod
    def constant(cls, value):
        interval = value if isinstance(value, VInterval) else VInterval.point(value)
        return cls(interval, VInterval.point(0.0))

    def __add__(self, other):
        rhs = other if isinstance(other, VDual) else VDual.constant(other)
        return VDual(self.value + rhs.value, self.derivative + rhs.derivative)

    __radd__ = __add__

    def __neg__(self):
        return VDual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + (-other if isinstance(other, VDual) else -VDual.constant(other))

    def __rsub__(self, other):
        return VDual.constant(other) - self

    def __mul__(self, other):
        rhs = other if isinstance(other, VDual) else VDual.constant(other)
        return VDual(
            self.value * rhs.value,
            self.derivative * rhs.value + self.value * rhs.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        rhs = other if isinstance(other, VDual) else VDual.constant(other)
        return VDual(
            self.value / rhs.value,
            (self.derivative * rhs.value - self.value * rhs.derivative)
            / (rhs.value * rhs.value),
        )

    def __rtruediv__(self, other):
        return VDual.constant(other) / self


def vdual_exp(value):
    current = value.value.exp()
    return VDual(current, current * value.derivative)


def v_lerp(first, second, parameter):
    return (VDual.constant(VInterval.point(1.0)) - parameter) * first + parameter * second


@lru_cache(maxsize=None)
def _v_fraction_cached(value):
    return VInterval.enclosing_fraction(value)


def v_fraction(value):
    return _v_fraction_cached(Fraction(value))


def v_bank_coordinate(bank, parameter_u):
    start_name, end_name = POINT_PAIRS[bank]
    return tuple(
        v_fraction(POINTS[start_name][index])
        + parameter_u * v_fraction(POINTS[end_name][index] - POINTS[start_name][index])
        for index in range(4)
    )


def v_field_value(coefficients, coordinates):
    output = VDual.constant(VInterval.point(0.0))
    for index in range(4):
        output += coefficients[index] * coordinates[index]
    for index in range(4):
        output += coefficients[4 + index] * coordinates[index] * coordinates[index] / VInterval.point(2.0)
    for pair_index, (first, second) in enumerate(PAIRS):
        output += coefficients[8 + pair_index] * coordinates[first] * coordinates[second]
    return output


def v_field_gradient(coefficients, coordinates):
    output = []
    for index in range(4):
        current = coefficients[index] + coefficients[4 + index] * coordinates[index]
        for pair_index, (first, second) in enumerate(PAIRS):
            if index == first:
                current += coefficients[8 + pair_index] * coordinates[second]
            elif index == second:
                current += coefficients[8 + pair_index] * coordinates[first]
        output.append(current)
    return tuple(output)


def v_endpoint(bank, amplitude_intervals, parameter_u):
    coordinates = tuple(VDual.constant(value) for value in v_bank_coordinate(bank, parameter_u))
    latent = []
    for field in range(10):
        coefficients = tuple(VDual.constant(v_fraction(item)) for item in COEFFICIENTS[bank][field])
        latent.append(
            VDual.constant(v_fraction(BASE_VALUES[field]))
            + v_field_value(coefficients, coordinates) * amplitude_intervals[field]
        )
    phi_coefficients = tuple(VDual.constant(v_fraction(item)) for item in COEFFICIENTS[bank][10])
    gradient = tuple(
        item * amplitude_intervals[10]
        for item in v_field_gradient(phi_coefficients, coordinates)
    )
    return tuple(latent), gradient


def v_configured_fields(chart, bank_a, bank_b, amplitude_intervals, u_lo, u_hi, lambda_lo, lambda_hi):
    parameter_u = VInterval.bounds(u_lo, u_hi)
    parameter_lambda = VDual(VInterval.bounds(lambda_lo, lambda_hi), VInterval.point(1.0))
    if chart == "J2_EVALUATED_COFIELD_JOIN":
        latent_a, gradient_a = v_endpoint(bank_a, amplitude_intervals, parameter_u)
        latent_b, gradient_b = v_endpoint(bank_b, amplitude_intervals, parameter_u)
        latent = tuple(v_lerp(latent_a[index], latent_b[index], parameter_lambda) for index in range(10))
        gradient = tuple(v_lerp(gradient_a[index], gradient_b[index], parameter_lambda) for index in range(4))
        return latent, gradient

    coordinates_a = v_bank_coordinate(bank_a, parameter_u)
    coordinates_b = v_bank_coordinate(bank_b, parameter_u)
    coordinates = tuple(
        v_lerp(VDual.constant(coordinates_a[index]), VDual.constant(coordinates_b[index]), parameter_lambda)
        for index in range(4)
    )
    latent = []
    for field in range(10):
        coefficients = tuple(
            v_lerp(
                VDual.constant(v_fraction(COEFFICIENTS[bank_a][field][term])),
                VDual.constant(v_fraction(COEFFICIENTS[bank_b][field][term])),
                parameter_lambda,
            )
            for term in range(14)
        )
        latent.append(
            VDual.constant(v_fraction(BASE_VALUES[field]))
            + v_field_value(coefficients, coordinates) * amplitude_intervals[field]
        )
    phi_coefficients = tuple(
        v_lerp(
            VDual.constant(v_fraction(COEFFICIENTS[bank_a][10][term])),
            VDual.constant(v_fraction(COEFFICIENTS[bank_b][10][term])),
            parameter_lambda,
        )
        for term in range(14)
    )
    gradient = tuple(
        item * amplitude_intervals[10]
        for item in v_field_gradient(phi_coefficients, coordinates)
    )
    return tuple(latent), gradient


def v_sheet_interval(chart, bank_a, bank_b, amplitude_intervals, u_lo, u_hi, lambda_lo, lambda_hi):
    latent, gradient = v_configured_fields(
        chart, bank_a, bank_b, amplitude_intervals, u_lo, u_hi, lambda_lo, lambda_hi
    )
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    scale_u, scale_w, scale_r, scale_t = vdual_exp(a), vdual_exp(c), vdual_exp(d), vdual_exp(f)
    first = gradient[0] - a20 * gradient[2] - a30 * gradient[3]
    second = gradient[1] - a21 * gradient[2] - a31 * gradient[3]
    scalar = (
        -((first / scale_u) * (first / scale_u))
        + ((second - b * first / scale_u) / scale_w)
        * ((second - b * first / scale_u) / scale_w)
        + (gradient[2] / scale_r) * (gradient[2] / scale_r)
        + ((gradient[3] - e * gradient[2] / scale_r) / scale_t)
        * ((gradient[3] - e * gradient[2] / scale_r) / scale_t)
    )
    return scalar, gradient


def lerp(first, second, parameter):
    return (Dual.constant(qiv(1)) - parameter) * first + parameter * second


def bank_coordinate(bank, parameter_u):
    start_name, end_name = POINT_PAIRS[bank]
    start, end = POINTS[start_name], POINTS[end_name]
    return tuple(qiv(start[index]) + parameter_u * qiv(end[index] - start[index]) for index in range(4))


def field_value(coefficients, coordinates):
    output = Dual.constant(qiv(0))
    for index in range(4):
        output += coefficients[index] * coordinates[index]
    for index in range(4):
        output += coefficients[4 + index] * coordinates[index] * coordinates[index] / qiv(2)
    for pair_index, (first, second) in enumerate(PAIRS):
        output += coefficients[8 + pair_index] * coordinates[first] * coordinates[second]
    return output


def field_gradient(coefficients, coordinates):
    output = []
    for index in range(4):
        current = coefficients[index] + coefficients[4 + index] * coordinates[index]
        for pair_index, (first, second) in enumerate(PAIRS):
            if index == first:
                current += coefficients[8 + pair_index] * coordinates[second]
            elif index == second:
                current += coefficients[8 + pair_index] * coordinates[first]
        output.append(current)
    return tuple(output)


def endpoint_dual(bank, amplitudes, parameter_u):
    coordinates = tuple(Dual.constant(value) for value in bank_coordinate(bank, parameter_u))
    latent = []
    for field in range(10):
        coefficients = tuple(Dual.constant(qiv(item)) for item in COEFFICIENTS[bank][field])
        latent.append(Dual.constant(qiv(BASE_VALUES[field])) + field_value(coefficients, coordinates) * qiv(amplitudes[field]))
    phi_coefficients = tuple(Dual.constant(qiv(item)) for item in COEFFICIENTS[bank][10])
    gradient = tuple(item * qiv(amplitudes[10]) for item in field_gradient(phi_coefficients, coordinates))
    return tuple(latent), gradient


def configured_fields(chart, bank_a, bank_b, amplitudes, u_lo, u_hi, lambda_lo, lambda_hi):
    parameter_u = make_interval(u_lo, u_hi)
    parameter_lambda = Dual(make_interval(lambda_lo, lambda_hi), qiv(1))
    if chart == "J2_EVALUATED_COFIELD_JOIN":
        latent_a, gradient_a = endpoint_dual(bank_a, amplitudes, parameter_u)
        latent_b, gradient_b = endpoint_dual(bank_b, amplitudes, parameter_u)
        latent = tuple(lerp(latent_a[index], latent_b[index], parameter_lambda) for index in range(10))
        gradient = tuple(lerp(gradient_a[index], gradient_b[index], parameter_lambda) for index in range(4))
        return latent, gradient

    coordinates_a = bank_coordinate(bank_a, parameter_u)
    coordinates_b = bank_coordinate(bank_b, parameter_u)
    coordinates = tuple(
        lerp(Dual.constant(coordinates_a[index]), Dual.constant(coordinates_b[index]), parameter_lambda)
        for index in range(4)
    )
    latent = []
    for field in range(10):
        coefficients = tuple(
            lerp(
                Dual.constant(qiv(COEFFICIENTS[bank_a][field][term])),
                Dual.constant(qiv(COEFFICIENTS[bank_b][field][term])),
                parameter_lambda,
            )
            for term in range(14)
        )
        latent.append(Dual.constant(qiv(BASE_VALUES[field])) + field_value(coefficients, coordinates) * qiv(amplitudes[field]))
    phi_coefficients = tuple(
        lerp(
            Dual.constant(qiv(COEFFICIENTS[bank_a][10][term])),
            Dual.constant(qiv(COEFFICIENTS[bank_b][10][term])),
            parameter_lambda,
        )
        for term in range(14)
    )
    gradient = tuple(item * qiv(amplitudes[10]) for item in field_gradient(phi_coefficients, coordinates))
    return tuple(latent), gradient


def sheet_interval(chart, bank_a, bank_b, amplitudes, u_lo, u_hi, lambda_lo, lambda_hi):
    latent, gradient = configured_fields(chart, bank_a, bank_b, amplitudes, u_lo, u_hi, lambda_lo, lambda_hi)
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    scale_u, scale_w, scale_r, scale_t = dual_exp(a), dual_exp(c), dual_exp(d), dual_exp(f)
    first = gradient[0] - a20 * gradient[2] - a30 * gradient[3]
    second = gradient[1] - a21 * gradient[2] - a31 * gradient[3]
    time_component = first / scale_u
    base_space_component = (second - b * first / scale_u) / scale_w
    angular_first = gradient[2] / scale_r
    angular_second = (gradient[3] - e * gradient[2] / scale_r) / scale_t
    scalar = (
        -(time_component * time_component)
        + base_space_component * base_space_component
        + angular_first * angular_first
        + angular_second * angular_second
    )
    return scalar, gradient


def float_coefficients(bank_a, bank_b, parameter_lambda):
    return tuple(
        tuple(
            (1.0 - parameter_lambda) * float(COEFFICIENTS[bank_a][field][term])
            + parameter_lambda * float(COEFFICIENTS[bank_b][field][term])
            for term in range(14)
        )
        for field in range(11)
    )


def float_bank_coordinate(bank, parameter_u):
    start_name, end_name = POINT_PAIRS[bank]
    return tuple(
        float(POINTS[start_name][index] + (POINTS[end_name][index] - POINTS[start_name][index]) * parameter_u)
        for index in range(4)
    )


def float_field_value(coefficients, coordinates):
    value = sum(coefficients[index] * coordinates[index] for index in range(4))
    value += sum(coefficients[4 + index] * coordinates[index] ** 2 / 2.0 for index in range(4))
    value += sum(coefficients[8 + pair_index] * coordinates[first] * coordinates[second]
                 for pair_index, (first, second) in enumerate(PAIRS))
    return value


def float_field_gradient(coefficients, coordinates):
    output = []
    for index in range(4):
        value = coefficients[index] + coefficients[4 + index] * coordinates[index]
        for pair_index, (first, second) in enumerate(PAIRS):
            if index == first:
                value += coefficients[8 + pair_index] * coordinates[second]
            elif index == second:
                value += coefficients[8 + pair_index] * coordinates[first]
        output.append(value)
    return tuple(output)


def float_endpoint(bank, amplitudes, parameter_u):
    coordinates = float_bank_coordinate(bank, parameter_u)
    latent = tuple(
        float(BASE_VALUES[field]) + float(amplitudes[field]) * float_field_value(
            tuple(map(float, COEFFICIENTS[bank][field])), coordinates
        )
        for field in range(10)
    )
    gradient = tuple(
        float(amplitudes[10]) * item
        for item in float_field_gradient(tuple(map(float, COEFFICIENTS[bank][10])), coordinates)
    )
    return latent, gradient


def float_scalar(chart, bank_a, bank_b, amplitudes, parameter_u, parameter_lambda):
    if chart == "J2_EVALUATED_COFIELD_JOIN":
        latent_a, gradient_a = float_endpoint(bank_a, amplitudes, parameter_u)
        latent_b, gradient_b = float_endpoint(bank_b, amplitudes, parameter_u)
        latent = tuple((1 - parameter_lambda) * latent_a[index] + parameter_lambda * latent_b[index] for index in range(10))
        gradient = tuple((1 - parameter_lambda) * gradient_a[index] + parameter_lambda * gradient_b[index] for index in range(4))
    else:
        coordinates_a = float_bank_coordinate(bank_a, parameter_u)
        coordinates_b = float_bank_coordinate(bank_b, parameter_u)
        coordinates = tuple((1 - parameter_lambda) * coordinates_a[index] + parameter_lambda * coordinates_b[index] for index in range(4))
        coefficients = float_coefficients(bank_a, bank_b, parameter_lambda)
        latent = tuple(
            float(BASE_VALUES[field]) + float(amplitudes[field]) * float_field_value(coefficients[field], coordinates)
            for field in range(10)
        )
        gradient = tuple(
            float(amplitudes[10]) * item for item in float_field_gradient(coefficients[10], coordinates)
        )
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
    scale_u, scale_w, scale_r, scale_t = math.exp(a), math.exp(c), math.exp(d), math.exp(f)
    first = gradient[0] - a20 * gradient[2] - a30 * gradient[3]
    second = gradient[1] - a21 * gradient[2] - a31 * gradient[3]
    return (
        -(first / scale_u) ** 2
        + ((second - b * first / scale_u) / scale_w) ** 2
        + (gradient[2] / scale_r) ** 2
        + ((gradient[3] - e * gradient[2] / scale_r) / scale_t) ** 2
    )


def float_root(chart, bank_a, bank_b, amplitudes, parameter_u):
    lo, hi = 0.0, 1.0
    value_lo = float_scalar(chart, bank_a, bank_b, amplitudes, parameter_u, lo)
    value_hi = float_scalar(chart, bank_a, bank_b, amplitudes, parameter_u, hi)
    if not value_lo > 0.0 or not value_hi < 0.0:
        raise AssertionError("cross-sector endpoint signs")
    for _ in range(70):
        midpoint = (lo + hi) / 2
        value_mid = float_scalar(chart, bank_a, bank_b, amplitudes, parameter_u, midpoint)
        if value_mid > 0:
            lo, value_lo = midpoint, value_mid
        else:
            hi, value_hi = midpoint, value_mid
    return (lo + hi) / 2


def amplitude_vector(carrier, mask):
    output = [Fraction(0) for _ in range(11)]
    for indices, bit in (((0, 1, 2), 1), ((3, 4, 5), 2), ((6, 7, 8, 9), 4), ((10,), 8)):
        if mask & bit:
            for index in indices:
                output[index] = carrier[index]
    return tuple(output)


def certify_derivative_negative(chart, bank_a, bank_b, amplitudes, u_lo, u_hi):
    queue = deque([(Fraction(0), Fraction(1), 0)])
    lower_bound = float("inf")
    upper_bound = -float("inf")
    boxes = 0
    while queue:
        lambda_lo, lambda_hi, depth = queue.popleft()
        scalar, _gradient = sheet_interval(
            chart, bank_a, bank_b, amplitudes, u_lo, u_hi, lambda_lo, lambda_hi
        )
        derivative_lo, derivative_hi = bounds(scalar.derivative)
        if derivative_hi < 0.0:
            boxes += 1
            lower_bound = min(lower_bound, derivative_lo)
            upper_bound = max(upper_bound, derivative_hi)
        elif depth >= MAX_DERIVATIVE_LAMBDA_DEPTH:
            return None
        else:
            midpoint = (lambda_lo + lambda_hi) / 2
            queue.append((lambda_lo, midpoint, depth + 1))
            queue.append((midpoint, lambda_hi, depth + 1))
    return boxes, lower_bound, upper_bound


def certify_cross_sheet(sheet_id, chart, bank_a, bank_b, amplitudes):
    queue = deque([(Fraction(0), Fraction(1), 0)])
    certificates = []
    unresolved = []
    while queue:
        u_lo, u_hi, depth = queue.popleft()
        derivative = certify_derivative_negative(chart, bank_a, bank_b, amplitudes, u_lo, u_hi)
        roots = [
            float_root(chart, bank_a, bank_b, amplitudes, float(point))
            for point in (u_lo, (u_lo + u_hi) / 2, u_hi)
        ]
        padding = max(1.0 / 512.0, 2.0 * (max(roots) - min(roots)) + 1.0 / 1024.0)
        lambda_lo = Fraction(max(0.0, min(roots) - padding)).limit_denominator(2**24)
        lambda_hi = Fraction(min(1.0, max(roots) + padding)).limit_denominator(2**24)
        left_scalar, _ = sheet_interval(chart, bank_a, bank_b, amplitudes, u_lo, u_hi, lambda_lo, lambda_lo)
        right_scalar, _ = sheet_interval(chart, bank_a, bank_b, amplitudes, u_lo, u_hi, lambda_hi, lambda_hi)
        left_lo, _left_hi = bounds(left_scalar.value)
        _right_lo, right_hi = bounds(right_scalar.value)
        root_scalar, root_gradient = sheet_interval(
            chart, bank_a, bank_b, amplitudes, u_lo, u_hi, lambda_lo, lambda_hi
        )
        nonzero_component = None
        for index, component in enumerate(root_gradient):
            component_lo, component_hi = bounds(component.value)
            if component_lo > 0.0 or component_hi < 0.0:
                nonzero_component = index
                break
        if derivative is not None and left_lo > 0.0 and right_hi < 0.0 and nonzero_component is not None:
            derivative_boxes, derivative_lo, derivative_hi = derivative
            scalar_lo, scalar_hi = bounds(root_scalar.value)
            certificates.append({
                "sheet_id": sheet_id,
                "u_lo": str(u_lo),
                "u_hi": str(u_hi),
                "u_depth": depth,
                "lambda_lo": str(lambda_lo),
                "lambda_hi": str(lambda_hi),
                "s_left_lower": fmt(left_lo),
                "s_right_upper": fmt(right_hi),
                "root_box_s_lo": fmt(scalar_lo),
                "root_box_s_hi": fmt(scalar_hi),
                "partial_lambda_s_lo": fmt(derivative_lo),
                "partial_lambda_s_hi": fmt(derivative_hi),
                "derivative_lambda_boxes": derivative_boxes,
                "nonzero_dphi_component": str(nonzero_component),
                "interface_class": "REGULAR_NULL_GRAPH_SEGMENT",
                "dyad_status": "NONZERO_RANK_ONE_NILPOTENT_AT_S_ZERO",
                "metric_status": "LORENTZIAN_NONDEGENERATE_EXACT_COFRAME",
            })
        elif depth >= MAX_CROSS_U_DEPTH:
            unresolved.append({
                "sheet_id": sheet_id,
                "u_lo": str(u_lo),
                "u_hi": str(u_hi),
                "u_depth": depth,
                "lambda_lo": str(lambda_lo),
                "lambda_hi": str(lambda_hi),
                "reason": "INTERVAL_REGULARITY_OR_ROOT_ENVELOPE_UNRESOLVED",
            })
        else:
            midpoint = (u_lo + u_hi) / 2
            queue.append((u_lo, midpoint, depth + 1))
            queue.append((midpoint, u_hi, depth + 1))
    certificates.sort(key=lambda row: Fraction(row["u_lo"]))
    return certificates, unresolved


def certify_positive_sheet(sheet_id, chart, bank_a, bank_b, amplitudes):
    queue = deque([(Fraction(0), Fraction(1), Fraction(0), Fraction(1), 0)])
    certificates = []
    unresolved = []
    negative = []
    while queue:
        u_lo, u_hi, lambda_lo, lambda_hi, depth = queue.popleft()
        scalar, _gradient = sheet_interval(
            chart, bank_a, bank_b, amplitudes, u_lo, u_hi, lambda_lo, lambda_hi
        )
        scalar_lo, scalar_hi = bounds(scalar.value)
        if scalar_lo > 0.0:
            certificates.append({
                "sheet_id": sheet_id,
                "u_lo": str(u_lo),
                "u_hi": str(u_hi),
                "lambda_lo": str(lambda_lo),
                "lambda_hi": str(lambda_hi),
                "depth": depth,
                "s_lower": fmt(scalar_lo),
                "s_upper": fmt(scalar_hi),
                "certificate": "STRICTLY_SPACELIKE_BOX",
            })
        elif scalar_hi < 0.0:
            negative.append((u_lo, u_hi, lambda_lo, lambda_hi, depth, scalar_lo, scalar_hi))
        elif depth >= MAX_CONTROL_DEPTH:
            unresolved.append((u_lo, u_hi, lambda_lo, lambda_hi, depth, scalar_lo, scalar_hi))
        else:
            u_width = u_hi - u_lo
            lambda_width = lambda_hi - lambda_lo
            if u_width >= lambda_width:
                midpoint = (u_lo + u_hi) / 2
                queue.append((u_lo, midpoint, lambda_lo, lambda_hi, depth + 1))
                queue.append((midpoint, u_hi, lambda_lo, lambda_hi, depth + 1))
            else:
                midpoint = (lambda_lo + lambda_hi) / 2
                queue.append((u_lo, u_hi, lambda_lo, midpoint, depth + 1))
                queue.append((u_lo, u_hi, midpoint, lambda_hi, depth + 1))
    return certificates, negative, unresolved


def vector_amplitude_intervals(amplitudes):
    """Transpose N exact amplitude vectors into eleven outward vector intervals."""
    return tuple(
        VInterval.enclosing_fraction([row[field] for row in amplitudes])
        for field in range(11)
    )


def column_amplitude_intervals(amplitude_intervals):
    return tuple(
        VInterval(item.lo.reshape(-1, 1), item.hi.reshape(-1, 1))
        for item in amplitude_intervals
    )


def take_amplitude_intervals(amplitude_intervals, indices):
    return tuple(VInterval(item.lo[indices], item.hi[indices]) for item in amplitude_intervals)


def vector_point_roots(chart, bank_a, bank_b, amplitude_intervals, u_points):
    """Diagnostic roots at fixed-u fibers; interval boxes certify the enclosing graph."""
    columns = column_amplitude_intervals(amplitude_intervals)
    u_values = np.asarray(u_points, dtype=np.float64).reshape(1, -1)
    size = columns[0].lo.shape[0]
    lo = np.zeros((size, len(u_points)))
    hi = np.ones((size, len(u_points)))
    for _ in range(58):
        midpoint = (lo + hi) / 2.0
        scalar, _gradient = v_sheet_interval(
            chart, bank_a, bank_b, columns,
            u_values, u_values, midpoint, midpoint,
        )
        values = (scalar.value.lo + scalar.value.hi) / 2.0
        positive = values > 0.0
        lo = np.where(positive, midpoint, lo)
        hi = np.where(positive, hi, midpoint)
    return (lo + hi) / 2.0


def fixed_partition_certificate(chart, bank_a, bank_b, amplitude_intervals, pair_type, nu, nl):
    if pair_type != "SAME_SIGN_CONTROL":
        raise AssertionError("fixed full-sheet partition is the same-sign control route")
    size = len(np.atleast_1d(amplitude_intervals[0].lo))
    columns = column_amplitude_intervals(amplitude_intervals)
    minimum_s_lower = np.full(size, np.inf)
    maximum_s_upper = np.full(size, -np.inf)
    all_positive = np.ones(size, dtype=bool)
    worst_flat_index = np.zeros(size, dtype=int)
    u_indices = np.repeat(np.arange(nu), nl)
    lambda_indices = np.tile(np.arange(nl), nu)
    batch_size = 32
    for start in range(0, len(u_indices), batch_size):
        stop = min(start + batch_size, len(u_indices))
        current_u = u_indices[start:stop]
        current_lambda = lambda_indices[start:stop]
        scalar, _gradient = v_sheet_interval(
            chart, bank_a, bank_b, columns,
            (current_u / nu).reshape(1, -1),
            ((current_u + 1) / nu).reshape(1, -1),
            (current_lambda / nl).reshape(1, -1),
            ((current_lambda + 1) / nl).reshape(1, -1),
        )
        scalar_lo, scalar_hi = scalar.value.lo, scalar.value.hi
        local_index = np.argmin(scalar_lo, axis=1)
        local_minimum = scalar_lo[np.arange(size), local_index]
        replace = local_minimum < minimum_s_lower
        worst_flat_index = np.where(replace, start + local_index, worst_flat_index)
        minimum_s_lower = np.minimum(minimum_s_lower, local_minimum)
        maximum_s_upper = np.maximum(maximum_s_upper, np.max(scalar_hi, axis=1))
        all_positive &= np.all(scalar_lo > 0.0, axis=1)

    output = {
        "nu": nu,
        "nl": nl,
        "covered_boxes": nu * nl,
        "minimum_s_lower": minimum_s_lower,
        "maximum_s_upper": maximum_s_upper,
        "all_positive": all_positive,
        "worst_u_index": worst_flat_index // nl,
        "worst_lambda_index": worst_flat_index % nl,
    }
    return output


def cross_partition_certificate(chart, bank_a, bank_b, amplitude_intervals, nu, nl):
    """Certify positive/root/negative lambda regions on every complete u strip."""
    if nl % 4:
        raise AssertionError("cross partition requires four-way lambda budget")
    columns = column_amplitude_intervals(amplitude_intervals)
    size = columns[0].lo.shape[0]
    roots = vector_point_roots(
        chart, bank_a, bank_b, amplitude_intervals,
        [index / nu for index in range(nu + 1)],
    )
    # Fixed preregistered implementation envelope: broad enough that interval
    # dependency on a complete u strip cannot substitute for a sampled root.
    padding = 0.125
    local_root_lo = np.maximum(
        0.0, _down(np.minimum(roots[:, :-1], roots[:, 1:]) - padding)
    )
    local_root_hi = np.minimum(
        1.0, _up(np.maximum(roots[:, :-1], roots[:, 1:]) + padding)
    )

    endpoint_signs = np.ones(size, dtype=bool)
    outside_signs = np.ones(size, dtype=bool)
    derivative_negative = np.ones(size, dtype=bool)
    gradient_nonzero = np.ones(size, dtype=bool)
    root_left_minimum = np.full(size, np.inf)
    root_right_maximum = np.full(size, -np.inf)
    maximum_derivative_upper = np.full(size, -np.inf)
    minimum_derivative_lower = np.full(size, np.inf)
    derivative_u_index = np.zeros(size, dtype=int)
    derivative_lambda_index = np.zeros(size, dtype=int)
    derivative_lambda_lo = np.zeros(size)
    derivative_lambda_hi = np.ones(size)

    side_bins = nl // 4
    root_bins = nl // 2
    batch_size = 16

    # Exact endpoint signs on complete u strips.
    u_index = np.arange(nu)
    for endpoint, expected_positive in ((0.0, True), (1.0, False)):
        scalar, _gradient = v_sheet_interval(
            chart, bank_a, bank_b, columns,
            (u_index / nu).reshape(1, -1),
            ((u_index + 1) / nu).reshape(1, -1),
            endpoint, endpoint,
        )
        if expected_positive:
            endpoint_signs &= np.all(scalar.value.lo > 0.0, axis=1)
        else:
            endpoint_signs &= np.all(scalar.value.hi < 0.0, axis=1)

    region_cells = []
    for current_u in range(nu):
        for current_lambda in range(side_bins):
            fraction_lo = current_lambda / side_bins
            fraction_hi = (current_lambda + 1) / side_bins
            region_cells.append(("LEFT", current_u, fraction_lo, fraction_hi))
            region_cells.append(("RIGHT", current_u, fraction_lo, fraction_hi))
        for current_lambda in range(root_bins):
            region_cells.append((
                "ROOT", current_u,
                current_lambda / root_bins,
                (current_lambda + 1) / root_bins,
            ))

    for start in range(0, len(region_cells), batch_size):
        current = region_cells[start:start + batch_size]
        labels = [item[0] for item in current]
        us = np.asarray([item[1] for item in current])
        fraction_lo = np.asarray([item[2] for item in current]).reshape(1, -1)
        fraction_hi = np.asarray([item[3] for item in current]).reshape(1, -1)
        base_lo = local_root_lo[:, us]
        base_hi = local_root_hi[:, us]
        lambda_lo = np.empty_like(base_lo)
        lambda_hi = np.empty_like(base_hi)
        for index, label in enumerate(labels):
            if label == "LEFT":
                lambda_lo[:, index] = base_lo[:, index] * fraction_lo[0, index]
                lambda_hi[:, index] = base_lo[:, index] * fraction_hi[0, index]
            elif label == "ROOT":
                width = base_hi[:, index] - base_lo[:, index]
                lambda_lo[:, index] = base_lo[:, index] + width * fraction_lo[0, index]
                lambda_hi[:, index] = base_lo[:, index] + width * fraction_hi[0, index]
            else:
                width = 1.0 - base_hi[:, index]
                lambda_lo[:, index] = base_hi[:, index] + width * fraction_lo[0, index]
                lambda_hi[:, index] = base_hi[:, index] + width * fraction_hi[0, index]
        bounded_lambda_lo = np.maximum(0.0, _down(lambda_lo))
        bounded_lambda_hi = np.minimum(1.0, _up(lambda_hi))
        scalar, gradient = v_sheet_interval(
            chart, bank_a, bank_b, columns,
            (us / nu).reshape(1, -1),
            ((us + 1) / nu).reshape(1, -1),
            bounded_lambda_lo, bounded_lambda_hi,
        )
        for index, label in enumerate(labels):
            if label == "LEFT":
                outside_signs &= scalar.value.lo[:, index] > 0.0
                root_left_minimum = np.minimum(root_left_minimum, scalar.value.lo[:, index])
            elif label == "RIGHT":
                outside_signs &= scalar.value.hi[:, index] < 0.0
                root_right_maximum = np.maximum(root_right_maximum, scalar.value.hi[:, index])
            else:
                derivative_hi = scalar.derivative.hi[:, index]
                derivative_lo = scalar.derivative.lo[:, index]
                replace = derivative_hi > maximum_derivative_upper
                derivative_u_index = np.where(replace, us[index], derivative_u_index)
                derivative_lambda_index = np.where(
                    replace,
                    int(round(fraction_lo[0, index] * root_bins)),
                    derivative_lambda_index,
                )
                derivative_lambda_lo = np.where(replace, lambda_lo[:, index], derivative_lambda_lo)
                derivative_lambda_hi = np.where(replace, lambda_hi[:, index], derivative_lambda_hi)
                maximum_derivative_upper = np.maximum(maximum_derivative_upper, derivative_hi)
                minimum_derivative_lower = np.minimum(minimum_derivative_lower, derivative_lo)
                derivative_negative &= derivative_hi < 0.0
                current_nonzero = np.zeros(size, dtype=bool)
                for component in gradient:
                    current_nonzero |= (
                        (component.value.lo[:, index] > 0.0)
                        | (component.value.hi[:, index] < 0.0)
                    )
                gradient_nonzero &= current_nonzero

    return {
        "nu": nu,
        "nl": nl,
        "covered_boxes": nu * nl,
        "endpoint_signs": endpoint_signs,
        "outside_signs": outside_signs,
        "all_derivative_negative": derivative_negative,
        "all_gradient_nonzero": gradient_nonzero,
        "root_side_certified": outside_signs,
        "root_sample_minimum": np.min(roots, axis=1),
        "root_sample_maximum": np.max(roots, axis=1),
        "root_envelope_lo": np.min(local_root_lo, axis=1),
        "root_envelope_hi": np.max(local_root_hi, axis=1),
        "root_left_minimum": root_left_minimum,
        "root_right_maximum": root_right_maximum,
        "maximum_derivative_upper": maximum_derivative_upper,
        "minimum_derivative_lower": minimum_derivative_lower,
        "derivative_u_index": derivative_u_index,
        "derivative_lambda_index": derivative_lambda_index,
        "derivative_lambda_lo": derivative_lambda_lo,
        "derivative_lambda_hi": derivative_lambda_hi,
    }


def certify_vector_group(chart, bank_a, bank_b, amplitude_intervals, pair_type):
    combined = None
    remaining = np.arange(len(np.atleast_1d(amplitude_intervals[0].lo)))
    for nu, nl in ((16, 64), (32, 128), (64, 256)):
        current_amplitudes = take_amplitude_intervals(amplitude_intervals, remaining)
        if pair_type == "SAME_SIGN_CONTROL":
            current = fixed_partition_certificate(
                chart, bank_a, bank_b, current_amplitudes, pair_type, nu, nl
            )
            passed = current["all_positive"]
        else:
            current = cross_partition_certificate(
                chart, bank_a, bank_b, current_amplitudes, nu, nl
            )
            passed = (
                current["endpoint_signs"]
                & current["outside_signs"]
                & current["all_derivative_negative"]
                & current["all_gradient_nonzero"]
            )
        if combined is None:
            combined = current
            combined["passed"] = passed.copy()
            combined["resolution_nu"] = np.full(len(passed), nu, dtype=int)
            combined["resolution_nl"] = np.full(len(passed), nl, dtype=int)
            combined["covered_boxes_per_sheet"] = np.full(len(passed), nu * nl, dtype=int)
        else:
            for key, value in current.items():
                if isinstance(value, np.ndarray) and value.shape[0] == len(remaining):
                    combined[key][remaining] = value
            combined["passed"][remaining] = passed
            combined["resolution_nu"][remaining] = nu
            combined["resolution_nl"][remaining] = nl
            combined["covered_boxes_per_sheet"][remaining] = nu * nl
        next_remaining = remaining[~passed]
        if not len(next_remaining):
            return combined
        remaining = next_remaining
    return combined


def high_precision_anchor(chart, bank_a, bank_b, amplitudes, pair_type, certificate, index):
    if pair_type == "SAME_SIGN_CONTROL":
        u_index = int(certificate["worst_u_index"][index])
        lambda_index = int(certificate["worst_lambda_index"][index])
    else:
        u_index = int(certificate["derivative_u_index"][index])
        lambda_index = int(certificate["derivative_lambda_index"][index])
    nu = int(certificate["resolution_nu"][index])
    nl = int(certificate["resolution_nl"][index])
    u_lo, u_hi = Fraction(u_index, nu), Fraction(u_index + 1, nu)
    if pair_type == "SAME_SIGN_CONTROL":
        lambda_lo, lambda_hi = Fraction(lambda_index, nl), Fraction(lambda_index + 1, nl)
    else:
        lambda_lo = Fraction.from_float(float(certificate["derivative_lambda_lo"][index]))
        lambda_hi = Fraction.from_float(float(certificate["derivative_lambda_hi"][index]))
    scalar, _gradient = sheet_interval(
        chart, bank_a, bank_b, amplitudes,
        u_lo, u_hi, lambda_lo, lambda_hi,
    )
    scalar_lo, scalar_hi = bounds(scalar.value)
    derivative_lo, derivative_hi = bounds(scalar.derivative)
    if pair_type == "SAME_SIGN_CONTROL" and scalar_lo <= 0.0:
        raise AssertionError("high-precision positive anchor")
    if pair_type == "CROSS_SECTOR" and derivative_hi >= 0.0:
        raise AssertionError("high-precision derivative anchor")
    return {
        "chart": chart,
        "bank_pair": f"B{bank_a}-B{bank_b}",
        "pair_type": pair_type,
        "amplitude_index": index,
        "u_lo": str(u_lo),
        "u_hi": str(u_hi),
        "lambda_lo": str(lambda_lo),
        "lambda_hi": str(lambda_hi),
        "binary64_s_lo": (
            fmt(certificate["minimum_s_lower"][index])
            if pair_type == "SAME_SIGN_CONTROL" else ""
        ),
        "binary64_derivative_hi": (
            fmt(certificate["maximum_derivative_upper"][index])
            if pair_type == "CROSS_SECTOR" else ""
        ),
        "mpmath80_s_lo": fmt(scalar_lo),
        "mpmath80_s_hi": fmt(scalar_hi),
        "mpmath80_partial_lambda_s_lo": fmt(derivative_lo),
        "mpmath80_partial_lambda_s_hi": fmt(derivative_hi),
        "status": "HIGH_PRECISION_SIGN_AGREEMENT",
    }


def main():
    iv.dps = IV_DPS
    carrier_rows = read_tsv(CARRIER_FILE)
    carriers = {
        row["carrier_id"]: tuple(Fraction(row[name]) for name in PARAMETERS)
        for row in carrier_rows
    }
    if len(carriers) != 48:
        raise AssertionError("carrier universe")
    identities = read_tsv(IDENTITY_FILE)
    causal_rows = read_tsv(CAUSAL_FILE)
    causal = {row["identity_id"]: row["causal_status"] for row in causal_rows}
    active = [row for row in identities if int(row["mask_id"][1:], 16) & 8]
    if len(active) != 1_536 or len(causal) != 3_072:
        raise AssertionError("active endpoint universe")
    identity_lookup = {
        (int(row["bank"][1:]), row["carrier_id"], int(row["mask_id"][1:], 16)): row["identity_id"]
        for row in active
    }
    if len(identity_lookup) != 1_536:
        raise AssertionError("active identity uniqueness")

    group_rows = []
    amplitude_rows = []
    for carrier_id in sorted(carriers):
        for mask in range(8, 16):
            amplitudes = amplitude_vector(carriers[carrier_id], mask)
            group_rows.append({
                "carrier_id": carrier_id,
                "mask": mask,
                "mask_id": f"M{mask:X}",
            })
            amplitude_rows.append(amplitudes)
    if len(group_rows) != 384:
        raise AssertionError("matched group universe")
    amplitude_intervals = vector_amplitude_intervals(amplitude_rows)

    endpoint_pairs = []
    pair_lookup = {}
    for group_index, group in enumerate(group_rows):
        carrier_id, mask = group["carrier_id"], group["mask"]
        for bank_a, bank_b in BANK_PAIRS:
            identity_a = identity_lookup[(bank_a, carrier_id, mask)]
            identity_b = identity_lookup[(bank_b, carrier_id, mask)]
            status_a, status_b = causal[identity_a], causal[identity_b]
            endpoint_pair_id = f"{carrier_id}_M{mask:X}_B{bank_a}B{bank_b}"
            row = {
                "endpoint_pair_id": endpoint_pair_id,
                "carrier_id": carrier_id,
                "mask_id": f"M{mask:X}",
                "bank_a": f"B{bank_a}",
                "bank_b": f"B{bank_b}",
                "identity_a": identity_a,
                "identity_b": identity_b,
                "causal_a": status_a,
                "causal_b": status_b,
                "pair_type": "CROSS_SECTOR" if status_a != status_b else "SAME_SIGN_CONTROL",
            }
            endpoint_pairs.append(row)
            pair_lookup[(group_index, bank_a, bank_b)] = row

    sheets = []
    null_segments = []
    positive_boxes = []
    unresolved_rows = []
    high_precision_rows = []
    for chart in CHARTS:
        chart_id = "J1" if chart.startswith("J1") else "J2"
        for bank_a, bank_b in BANK_PAIRS:
            pair_type = "CROSS_SECTOR" if bank_b == 3 else "SAME_SIGN_CONTROL"
            certificate = certify_vector_group(
                chart, bank_a, bank_b, amplitude_intervals, pair_type
            )
            if pair_type == "SAME_SIGN_CONTROL":
                anchor_index = int(np.argmin(certificate["minimum_s_lower"]))
            else:
                anchor_index = int(np.argmax(certificate["maximum_derivative_upper"]))
            high_precision_rows.append(high_precision_anchor(
                chart, bank_a, bank_b, amplitude_rows[anchor_index],
                pair_type, certificate, anchor_index,
            ))
            for group_index, group in enumerate(group_rows):
                pair = pair_lookup[(group_index, bank_a, bank_b)]
                sheet_id = f"{pair['endpoint_pair_id']}_{chart_id}"
                passed = bool(certificate["passed"][group_index])
                resolution_nu = int(certificate["resolution_nu"][group_index])
                resolution_nl = int(certificate["resolution_nl"][group_index])
                covered_boxes = int(certificate["covered_boxes_per_sheet"][group_index])
                if pair_type == "SAME_SIGN_CONTROL":
                    primary = (
                        "UNIFORMLY_SPACELIKE_SHEET"
                        if passed else "UNRESOLVED_INTERVAL_GEOMETRY"
                    )
                    positive_boxes.append({
                        "sheet_id": sheet_id,
                        "chart": chart,
                        "bank_pair": f"B{bank_a}-B{bank_b}",
                        "carrier_id": group["carrier_id"],
                        "mask_id": group["mask_id"],
                        "resolution_u": resolution_nu,
                        "resolution_lambda": resolution_nl,
                        "covered_boxes": covered_boxes,
                        "minimum_s_lower": fmt(certificate["minimum_s_lower"][group_index]),
                        "maximum_s_upper": fmt(certificate["maximum_s_upper"][group_index]),
                        "worst_u_index": int(certificate["worst_u_index"][group_index]),
                        "worst_lambda_index": int(certificate["worst_lambda_index"][group_index]),
                        "certificate": (
                            "COMPLETE_SHEET_STRICTLY_SPACELIKE"
                            if passed else "UNRESOLVED_COMPLETE_SHEET"
                        ),
                        "arithmetic": "BINARY64_DIRECTED_NEXTAFTER",
                    })
                    root_lo = root_hi = derivative_upper = ""
                    null_components = 0 if passed else "UNRESOLVED"
                else:
                    primary = (
                        "FORCED_SINGLE_REGULAR_NULL_GRAPH"
                        if passed else "UNRESOLVED_INTERVAL_GEOMETRY"
                    )
                    null_segments.append({
                        "sheet_id": sheet_id,
                        "chart": chart,
                        "bank_pair": f"B{bank_a}-B{bank_b}",
                        "carrier_id": group["carrier_id"],
                        "mask_id": group["mask_id"],
                        "resolution_u": resolution_nu,
                        "resolution_lambda": resolution_nl,
                        "covered_boxes": covered_boxes,
                        "lambda_root_sample_minimum": fmt(certificate["root_sample_minimum"][group_index]),
                        "lambda_root_sample_maximum": fmt(certificate["root_sample_maximum"][group_index]),
                        "lambda_root_envelope_lo": fmt(certificate["root_envelope_lo"][group_index]),
                        "lambda_root_envelope_hi": fmt(certificate["root_envelope_hi"][group_index]),
                        "left_region_s_lower": fmt(certificate["root_left_minimum"][group_index]),
                        "right_region_s_upper": fmt(certificate["root_right_maximum"][group_index]),
                        "partial_lambda_s_lower": fmt(certificate["minimum_derivative_lower"][group_index]),
                        "partial_lambda_s_upper": fmt(certificate["maximum_derivative_upper"][group_index]),
                        "endpoint_signs": "CERTIFIED" if certificate["endpoint_signs"][group_index] else "UNRESOLVED",
                        "outer_region_signs": "CERTIFIED" if certificate["outside_signs"][group_index] else "UNRESOLVED",
                        "root_band_derivative": "STRICTLY_NEGATIVE" if certificate["all_derivative_negative"][group_index] else "UNRESOLVED",
                        "root_band_dphi": "NONZERO_COMPONENT_CERTIFIED" if certificate["all_gradient_nonzero"][group_index] else "UNRESOLVED",
                        "interface_class": (
                            "SINGLE_REGULAR_NULL_GRAPH"
                            if passed else "UNRESOLVED_INTERVAL_GEOMETRY"
                        ),
                        "dyad_status": (
                            "NONZERO_RANK_ONE_NILPOTENT_AT_S_ZERO"
                            if passed else "NOT_GRADED"
                        ),
                        "metric_status": "LORENTZIAN_NONDEGENERATE_EXACT_COFRAME",
                        "arithmetic": "BINARY64_DIRECTED_NEXTAFTER",
                    })
                    root_lo = fmt(certificate["root_envelope_lo"][group_index])
                    root_hi = fmt(certificate["root_envelope_hi"][group_index])
                    derivative_upper = fmt(certificate["maximum_derivative_upper"][group_index])
                    null_components = 1 if passed else "UNRESOLVED"
                if not passed:
                    unresolved_rows.append({
                        "sheet_id": sheet_id,
                        "chart": chart,
                        "pair_type": pair_type,
                        "resolution_u": resolution_nu,
                        "resolution_lambda": resolution_nl,
                        "reason": "PREREGISTERED_INTERVAL_LADDER_EXHAUSTED",
                    })
                sheets.append({
                    "sheet_id": sheet_id,
                    "endpoint_pair_id": pair["endpoint_pair_id"],
                    "chart": chart,
                    "pair_type": pair_type,
                    "primary_class": primary,
                    "certified_boxes_or_segments": covered_boxes if passed else 0,
                    "unresolved_boxes": 0 if passed else 1,
                    "null_components": null_components,
                    "lambda_root_envelope_lo": root_lo,
                    "lambda_root_envelope_hi": root_hi,
                    "largest_partial_lambda_s_upper": derivative_upper,
                    "metric_degeneracies": 0,
                    "physical_label": "NONE",
                })

    if len(endpoint_pairs) != 2_304 or len(sheets) != 4_608:
        raise AssertionError("sheet universe")
    write_tsv(HERE / "ENDPOINT_PAIR_REGISTRY.tsv", list(endpoint_pairs[0]), endpoint_pairs)
    write_tsv(HERE / "SHEET_CLASSIFICATION.tsv", list(sheets[0]), sheets)
    write_tsv_gz(HERE / "NULL_GRAPH_CERTIFICATES.tsv.gz", list(null_segments[0]), null_segments)
    write_tsv_gz(HERE / "SAME_SIGN_BOX_CERTIFICATES.tsv.gz", list(positive_boxes[0]), positive_boxes)
    unresolved_fields = (
        "sheet_id", "chart", "pair_type", "resolution_u", "resolution_lambda", "reason"
    )
    write_tsv(HERE / "UNRESOLVED_BOXES.tsv", unresolved_fields, unresolved_rows)
    write_tsv(HERE / "HIGH_PRECISION_ANCHORS.tsv", list(high_precision_rows[0]), high_precision_rows)

    comparison = []
    sheet_lookup = {(row["endpoint_pair_id"], row["chart"]): row for row in sheets}
    for pair in endpoint_pairs:
        if pair["pair_type"] != "CROSS_SECTOR":
            continue
        j1 = sheet_lookup[(pair["endpoint_pair_id"], CHARTS[0])]
        j2 = sheet_lookup[(pair["endpoint_pair_id"], CHARTS[1])]
        comparison.append({
            "endpoint_pair_id": pair["endpoint_pair_id"],
            "J1_class": j1["primary_class"],
            "J2_class": j2["primary_class"],
            "topological_separator_agreement": "YES" if j1["null_components"] == j2["null_components"] == 1 else "NO_OR_UNRESOLVED",
            "J1_lambda_lo": j1["lambda_root_envelope_lo"],
            "J1_lambda_hi": j1["lambda_root_envelope_hi"],
            "J2_lambda_lo": j2["lambda_root_envelope_lo"],
            "J2_lambda_hi": j2["lambda_root_envelope_hi"],
            "shape_status": "CHART_DEPENDENT_ENVELOPES__EXISTENCE_INVARIANT",
        })
    write_tsv(HERE / "CHART_COMPARISON.tsv", list(comparison[0]), comparison)

    graph_rows = [
        {
            "graph_object": "SPACELIKE_BANK_TRIANGLE",
            "vertices": "B0;B1;B2",
            "registered_edge_sheets_per_chart": 1_152,
            "status": "CONSTRUCTIVELY_CONNECTED_WITHIN_MATCHED_BANK_EDGE_ATLAS"
            if all(row["primary_class"] == "UNIFORMLY_SPACELIKE_SHEET" for row in sheets if row["pair_type"] == "SAME_SIGN_CONTROL")
            else "UNRESOLVED_OR_POCKET_PRESENT",
            "scope_guard": "FIXED_CARRIER_MASK_BANK_EDGES_ONLY",
        },
        {
            "graph_object": "TIMELIKE_BANK_VERTEX",
            "vertices": "B3",
            "registered_edge_sheets_per_chart": 0,
            "status": "SINGLE_REGISTERED_TIMELIKE_BANK__INTERNAL_CONNECTEDNESS_NOT_TESTED",
            "scope_guard": "NO_SECOND_TIMELIKE_BANK_VERTEX",
        },
        {
            "graph_object": "CROSS_SECTOR_JOIN",
            "vertices": "B0-B3;B1-B3;B2-B3",
            "registered_edge_sheets_per_chart": 1_152,
            "status": "NULL_SEPARATOR_REQUIRED_ON_EVERY_REGISTERED_EDGE",
            "scope_guard": "NO_PHYSICAL_REGIME_OR_SIMPLEX_INTERIOR_CLAIM",
        },
    ]
    write_tsv(HERE / "ADJACENCY_COMPONENT_GRAPH.tsv", list(graph_rows[0]), graph_rows)

    exact_rows = [
        {
            "identity": "E01_CONTINUOUS_CAUSAL_SEPARATOR",
            "status": "DERIVED_EXACT",
            "statement": "continuous s with opposite endpoint signs has at least one zero",
            "scope": "ANY_CONTINUOUS_NONDEGENERATE_LORENTZIAN_CONFIGURATION_PATH",
        },
        {
            "identity": "E02_COFRAME_NONDEGENERACY",
            "status": "DERIVED_EXACT",
            "statement": "det(g)=-exp(2*(a+c+d+f))<0",
            "scope": "J1_AND_J2_ALL_FINITE_CONFIGURATION_POINTS",
        },
        {
            "identity": "E03_NULL_DYAD",
            "status": "DERIVED_EXACT",
            "statement": "at regular s=0 with dphi nonzero, D is nonzero rank-one and D^2=0",
            "scope": "CERTIFIED_REGULAR_NULL_GRAPH",
        },
        {
            "identity": "E04_CSN_SEPARATOR",
            "status": "DERIVED_EXACT",
            "statement": "positive common scale preserves sign and zero set of s",
            "scope": "POSITIVE_COMMON_SCALE_TRANSFORMATIONS",
        },
    ]
    write_tsv(HERE / "EXACT_TOPOLOGY_LEDGER.tsv", list(exact_rows[0]), exact_rows)

    source_paths = [
        CARRIER_FILE,
        IDENTITY_FILE,
        SOURCE_DIR / "verify_correspondence_independent.py",
        PHI_DIR / "MANIFEST.sha256",
        CAUSAL_FILE,
        PHI_DIR / "RESULT.json",
        PHI_DIR / "INDEPENDENT_VERIFICATION.json",
        PHI_DIR / "POST_CORRECTION_ADVERSARIAL_CLOSURE.md",
    ]
    source_rows = []
    for path in source_paths:
        relative = path.relative_to(ROOT).as_posix()
        blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{relative}"], cwd=ROOT, text=True).strip()
        source_rows.append({
            "path": relative,
            "sha256": digest(path),
            "base_blob": blob,
            "role": "FROZEN_LOAD_BEARING_SOURCE",
        })
    write_tsv(HERE / "SOURCE_LEDGER.tsv", list(source_rows[0]), source_rows)

    sheet_census = Counter(row["primary_class"] for row in sheets)
    result = {
        "status": "PASS_WITH_REGISTERED_SCOPE" if not unresolved_rows else "UNRESOLVED_INTERVAL_GEOMETRY_RETAINED",
        "base": BASE,
        "matched_carrier_mask_groups": 384,
        "endpoint_pairs": len(endpoint_pairs),
        "chart_sheet_presentations": len(sheets),
        "same_sign_endpoint_pairs": 1_152,
        "cross_sector_endpoint_pairs": 1_152,
        "sheet_class_census": dict(sorted(sheet_census.items())),
        "null_graph_segments": len(null_segments),
        "positive_certificate_boxes": len(positive_boxes),
        "unresolved_boxes": len(unresolved_rows),
        "metric_degeneracies": 0,
        "signature_transitions": 0,
        "actions_loaded": 0,
        "matter_carriers_loaded": 0,
        "atlas_deformation_vectors_loaded": 48,
        "physical_regime_labels_assigned": 0,
        "simplex_interiors_covered": 0,
        "gpu_runs": 0,
        "maximum_conclusion": "BOUNDED_REGISTERED_CONFIGURATION-SPACE_BANK-EDGE_ADJACENCY_CHARACTERIZED",
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
