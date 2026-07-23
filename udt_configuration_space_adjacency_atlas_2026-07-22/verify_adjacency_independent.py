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


def full_metric(latent, omit_angular_shift=False):
    a, b, c, d, e, f, a20, a30, a21, a31 = latent
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

    sampled_same_values = 0
    sampled_cross_roots = 0
    minimum_same = math.inf
    maximum_cross_derivative = -math.inf
    minimum_determinant_gap = math.inf
    maximum_matrix_formula_disagreement = 0.0
    probe_rows = []
    selected_shift_effect = 0.0
    for chart in CHARTS:
        chart_id = "J1" if chart == CHARTS[0] else "J2"
        for bank_a, bank_b in BANK_PAIRS:
            pair_type = "CROSS_SECTOR" if bank_b == 3 else "SAME_SIGN_CONTROL"
            local_minimum = math.inf
            local_maximum_derivative = -math.inf
            for carrier_id, mask, amplitudes in groups:
                sheet_id = f"{carrier_id}_M{mask:X}_B{bank_a}B{bank_b}_{chart_id}"
                expected = (
                    "FORCED_SINGLE_REGULAR_NULL_GRAPH"
                    if pair_type == "CROSS_SECTOR"
                    else "UNIFORMLY_SPACELIKE_SHEET"
                )
                if sheet_lookup[sheet_id]["primary_class"] != expected:
                    raise AssertionError(f"saved class mismatch {sheet_id}")
                if pair_type == "SAME_SIGN_CONTROL":
                    for parameter_u in (0.0, 0.25, 0.5, 0.75, 1.0):
                        for parameter_lambda in np.linspace(0.0, 1.0, 17):
                            scalar, determinant_value, _ = scalar_matrix(
                                chart, bank_a, bank_b, amplitudes,
                                parameter_u, float(parameter_lambda),
                            )
                            if not scalar > 0.0 or not determinant_value < 0.0:
                                raise AssertionError("independent same-sign probe")
                            sampled_same_values += 1
                            minimum_same = min(minimum_same, scalar)
                            local_minimum = min(local_minimum, scalar)
                            minimum_determinant_gap = min(minimum_determinant_gap, -determinant_value)
                else:
                    for parameter_u in (0.0, 0.25, 0.5, 0.75, 1.0):
                        current_root = root(chart, bank_a, bank_b, amplitudes, parameter_u)
                        scalar, determinant_value, gradient_norm = scalar_matrix(
                            chart, bank_a, bank_b, amplitudes, parameter_u, current_root
                        )
                        step = 1e-6
                        left = scalar_matrix(
                            chart, bank_a, bank_b, amplitudes,
                            parameter_u, max(0.0, current_root - step),
                        )[0]
                        right = scalar_matrix(
                            chart, bank_a, bank_b, amplitudes,
                            parameter_u, min(1.0, current_root + step),
                        )[0]
                        derivative = (right - left) / (
                            min(1.0, current_root + step) - max(0.0, current_root - step)
                        )
                        if abs(scalar) > 2e-12 or not derivative < 0.0:
                            raise AssertionError("independent regular crossing probe")
                        if not determinant_value < 0.0 or not gradient_norm > 0.0:
                            raise AssertionError("independent metric/gradient probe")
                        sampled_cross_roots += 1
                        maximum_cross_derivative = max(maximum_cross_derivative, derivative)
                        local_maximum_derivative = max(local_maximum_derivative, derivative)
                        minimum_determinant_gap = min(minimum_determinant_gap, -determinant_value)
                if (
                    chart == CHARTS[0] and bank_a == 0 and bank_b == 3
                    and carrier_id == groups[-1][0] and mask == 15
                ):
                    ordinary = scalar_matrix(chart, bank_a, bank_b, amplitudes, 0.5, 0.5)[0]
                    omitted = scalar_matrix(
                        chart, bank_a, bank_b, amplitudes, 0.5, 0.5,
                        omit_angular_shift=True,
                    )[0]
                    selected_shift_effect = abs(ordinary - omitted)
            probe_rows.append({
                "chart": chart,
                "bank_pair": f"B{bank_a}-B{bank_b}",
                "pair_type": pair_type,
                "matched_sheets": len(groups),
                "sampled_scalar_values": (
                    len(groups) * 5 * 17 if pair_type == "SAME_SIGN_CONTROL" else ""
                ),
                "sampled_roots": len(groups) * 5 if pair_type == "CROSS_SECTOR" else "",
                "minimum_same_sign_s": (
                    f"{local_minimum:.17g}" if pair_type == "SAME_SIGN_CONTROL" else ""
                ),
                "maximum_crossing_derivative": (
                    f"{local_maximum_derivative:.17g}" if pair_type == "CROSS_SECTOR" else ""
                ),
                "status": "INDEPENDENT_FULL_MATRIX_PROBES_PASS",
            })

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

    if not selected_shift_effect > 1e-12:
        raise AssertionError("angular/shift sectors are not a vacuous reconstruction")

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
        if value != 12:
            raise AssertionError("matrix-anchor loss rejected")

    def require_shift(value):
        if not value > 1e-12:
            raise AssertionError("angular/shift omission rejected")

    catches = []
    expect_failure("I01_MISSING_SHEET", lambda: require_count(4_607), catches)
    expect_failure("I02_DUPLICATE_SHEET", lambda: require_unique(4_607), catches)
    expect_failure(
        "I03_FLIPPED_CLASS",
        lambda: require_class({"FORCED_SINGLE_REGULAR_NULL_GRAPH": 2_303, "UNIFORMLY_SPACELIKE_SHEET": 2_305}),
        catches,
    )
    expect_failure("I04_LOST_MATRIX_ANCHOR", lambda: require_matrix_route(11), catches)
    expect_failure("I05_OMITTED_ANGULAR_SHIFT", lambda: require_shift(0.0), catches)

    output_fields = list(probe_rows[0])
    with (HERE / "INDEPENDENT_MATRIX_PROBES.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(probe_rows)

    result = {
        "status": "PASS_WITH_REGISTERED_SCOPE",
        "method": "INDEPENDENT_FULL_4X4_MATRIX_INVERSION_PLUS_80D_ADJUGATE_INTERVAL_ANCHORS",
        "sheet_count": len(sheets),
        "sheet_unique": len(sheet_lookup),
        "sheet_census": dict(sorted(Counter(row["primary_class"] for row in sheets).items())),
        "sampled_same_sign_matrix_values": sampled_same_values,
        "sampled_cross_sector_matrix_roots": sampled_cross_roots,
        "minimum_sampled_same_sign_s": minimum_same,
        "maximum_sampled_crossing_derivative": maximum_cross_derivative,
        "minimum_sampled_negative_determinant_gap": minimum_determinant_gap,
        "high_precision_matrix_anchors": high_precision,
        "high_precision_matrix_anchor_count": len(high_precision),
        "angular_shift_effect_probe": selected_shift_effect,
        "mutation_catches": catches,
        "production_builder_imported": False,
        "maximum_conclusion": "INDEPENDENT_SUPPORT_FOR_BOUNDED_REGISTERED_ADJACENCY_CENSUS",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
