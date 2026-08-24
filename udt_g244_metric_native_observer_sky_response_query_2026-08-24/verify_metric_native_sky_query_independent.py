#!/usr/bin/env python3
"""Independent standard-library exact replay for G244."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "INDEPENDENT_VERIFICATION.json"
LANDING = (
    "METRIC_NATIVE_OBSERVER_SKY_AREA_SHAPE_QUERY_DERIVED_CONDITIONALLY"
    "__NO_FITTED_ANGULAR_COEFFICIENT"
    "__CATALOG_IDENTIFICATION_AND_HISTORY_OPEN"
)


Matrix = tuple[tuple[Fraction, ...], ...]


def mat(rows: list[list[int | Fraction]]) -> Matrix:
    return tuple(tuple(Fraction(value) for value in row) for row in rows)


def eye(n: int) -> Matrix:
    return tuple(tuple(Fraction(int(i == j)) for j in range(n)) for i in range(n))


def transpose(a: Matrix) -> Matrix:
    return tuple(zip(*a))


def multiply(a: Matrix, b: Matrix) -> Matrix:
    bt = transpose(b)
    return tuple(
        tuple(sum((x * y for x, y in zip(row, col)), Fraction(0)) for col in bt)
        for row in a
    )


def scale(c: Fraction, a: Matrix) -> Matrix:
    return tuple(tuple(c * value for value in row) for row in a)


def add(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(x + y for x, y in zip(ra, rb)) for ra, rb in zip(a, b))


def det2(a: Matrix) -> Fraction:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def det4(a: Matrix) -> Fraction:
    total = Fraction(0)
    for column in range(4):
        minor = tuple(
            tuple(row[j] for j in range(4) if j != column)
            for row in a[1:]
        )
        total += (-1 if column % 2 else 1) * a[0][column] * det3(minor)
    return total


def det3(a: Matrix) -> Fraction:
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def trace2(a: Matrix) -> Fraction:
    return a[0][0] + a[1][1]


def block(a: Matrix, row: int, column: int) -> Matrix:
    return tuple(tuple(a[row + i][column + j] for j in range(2)) for i in range(2))


def join_blocks(a: Matrix, b: Matrix, c: Matrix, d: Matrix) -> Matrix:
    return tuple(
        tuple(a[i][j] for j in range(2)) + tuple(b[i][j] for j in range(2))
        for i in range(2)
    ) + tuple(
        tuple(c[i][j] for j in range(2)) + tuple(d[i][j] for j in range(2))
        for i in range(2)
    )


def symmetric(rng: random.Random) -> Matrix:
    a, b, c = (Fraction(rng.randint(-5, 5)) for _ in range(3))
    return ((a, b), (b, c))


def upper_phase(b: Matrix) -> Matrix:
    return join_blocks(eye(2), b, mat([[0, 0], [0, 0]]), eye(2))


def lower_phase(c: Matrix) -> Matrix:
    return join_blocks(eye(2), mat([[0, 0], [0, 0]]), c, eye(2))


def orthogonal(rng: random.Random) -> Matrix:
    triples = ((3, 4, 5), (5, 12, 13), (7, 24, 25), (8, 15, 17), (20, 21, 29))
    x, y, z = rng.choice(triples)
    x *= -1 if rng.randrange(2) else 1
    y *= -1 if rng.randrange(2) else 1
    q = mat([[Fraction(x, z), Fraction(-y, z)],
             [Fraction(y, z), Fraction(x, z)]])
    if rng.randrange(2):
        q = multiply(q, mat([[1, 0], [0, -1]]))
    return q


def invertible(rng: random.Random) -> Matrix:
    while True:
        value = mat([[rng.randint(-9, 9), rng.randint(-9, 9)],
                     [rng.randint(-9, 9), rng.randint(-9, 9)]])
        if det2(value):
            return value


def sign(value: Fraction) -> int:
    return int(value > 0) - int(value < 0)


def normalize(values: list[Fraction]) -> list[Fraction]:
    total = sum(values, Fraction(0))
    return [value / total for value in values]


def bilinear(left: list[Fraction], kernel: Matrix, right: list[Fraction]) -> Fraction:
    return sum(
        (left[i] * kernel[i][j] * right[j] for i in range(len(left)) for j in range(len(right))),
        Fraction(0),
    )


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def compute() -> dict[str, object]:
    rng = random.Random(244002)
    matrix_cases = 5000
    assertion_count = 0
    positive_shear_cases = 0
    parity_flip_cases = 0
    for _ in range(matrix_cases):
        d = invertible(rng)
        h = multiply(transpose(d), d)
        det_d = det2(d)
        det_h = det2(h)
        area = abs(det_d)
        shape = scale(Fraction(1, 1) / area, h)
        shear_numerator = trace2(h) ** 2 - 4 * det_h
        shear_power = shear_numerator / (4 * det_h)
        if det_h != det_d ** 2 or det2(shape) != 1 or shear_numerator < 0 or shear_power < 0:
            raise AssertionError("independent area/shape decomposition failed")
        if shear_power:
            positive_shear_cases += 1

        qs, qo = orthogonal(rng), orthogonal(rng)
        dg = multiply(multiply(transpose(qs), d), qo)
        hg = multiply(transpose(dg), dg)
        expected_hg = multiply(multiply(transpose(qo), h), qo)
        if hg != expected_hg or abs(det2(dg)) != area:
            raise AssertionError("independent screen covariance failed")
        sg = (trace2(hg) ** 2 - 4 * det2(hg)) / (4 * det2(hg))
        if sg != shear_power:
            raise AssertionError("independent shear invariance failed")
        expected_parity = sign(det2(qs)) * sign(det2(qo)) * sign(det_d)
        if sign(det2(dg)) != expected_parity:
            raise AssertionError("independent parity typing failed")
        if sign(det2(dg)) != sign(det_d):
            parity_flip_cases += 1

        factor = Fraction(rng.randint(1, 11), rng.randint(1, 11))
        ds = scale(factor, d)
        hs = multiply(transpose(ds), ds)
        if abs(det2(ds)) != factor ** 2 * area:
            raise AssertionError("independent area scale weight failed")
        if scale(Fraction(1, 1) / abs(det2(ds)), hs) != shape:
            raise AssertionError("independent shape scale invariance failed")
        assertion_count += 10

    if positive_shear_cases == 0 or parity_flip_cases == 0:
        raise AssertionError("independent matrix census missed required cases")

    omega = join_blocks(
        mat([[0, 0], [0, 0]]), eye(2), scale(Fraction(-1), eye(2)), mat([[0, 0], [0, 0]])
    )
    phase_cases = 5000
    nonmultiplicative = 0
    for _ in range(phase_cases):
        m10 = multiply(upper_phase(symmetric(rng)), lower_phase(symmetric(rng)))
        m21 = multiply(lower_phase(symmetric(rng)), upper_phase(symmetric(rng)))
        m20 = multiply(m21, m10)
        for phase in (m10, m21, m20):
            if multiply(multiply(transpose(phase), omega), phase) != omega or det4(phase) != 1:
                raise AssertionError("independent symplectic phase failed")
        b20 = block(m20, 0, 2)
        formula = add(multiply(block(m21, 0, 0), block(m10, 0, 2)),
                      multiply(block(m21, 0, 2), block(m10, 2, 2)))
        if b20 != formula:
            raise AssertionError("independent phase block formula failed")
        if b20 != multiply(block(m21, 0, 2), block(m10, 0, 2)):
            nonmultiplicative += 1
    if nonmultiplicative == 0:
        raise AssertionError("independent phase census missed nonmultiplicativity")

    q = normalize([Fraction(1), Fraction(2), Fraction(3), Fraction(4)])
    area = [Fraction(1), Fraction(2), Fraction(1), Fraction(3)]
    jacobi_maps = [mat([[value, 0], [0, 1]]) for value in area]
    if [abs(det2(value)) for value in jacobi_maps] != area:
        raise AssertionError("independent finite-cell Jacobi-area bridge failed")
    p = normalize([x * y for x, y in zip(q, area)])
    kernel = mat([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]])
    rr = bilinear(q, kernel, q)
    w = (bilinear(p, kernel, p) - 2 * bilinear(p, kernel, q) + rr) / rr
    constant = normalize([Fraction(7) * x for x in q])
    w_constant = (
        bilinear(constant, kernel, constant) - 2 * bilinear(constant, kernel, q) + rr
    ) / rr
    if w != Fraction(-1, 6) or constant != q or w_constant != 0:
        raise AssertionError("independent area projection failed")

    return {
        "audit": "G244_INDEPENDENT_STANDARD_LIBRARY_REPLAY",
        "classification": LANDING,
        "imports_production_code": False,
        "reads_production_output": False,
        "observational_outcomes": "CLOSED_AND_UNREAD",
        "fitted_angular_coefficients": 0,
        "matrix_cases": matrix_cases,
        "matrix_assertions": assertion_count,
        "positive_shear_cases": positive_shear_cases,
        "reflection_parity_flip_cases": parity_flip_cases,
        "phase_cases": phase_cases,
        "nonmultiplicative_position_cases": nonmultiplicative,
        "area_query_w": fraction_payload(w),
        "constant_area_w": fraction_payload(w_constant),
        "caustic_position_inverse_used": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = compute()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
