#!/usr/bin/env python3
"""Independent Fraction-only G248 replay; imports no production implementation or output."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction
from pathlib import Path


LANDING = (
    "METRIC_OWNS_ORDERED_REGULAR_INCIDENCE_COAREA_DENSITY_R_OVER_A"
    "__SKY_PHASE_COUNTING_AND_INCIDENCE_MEASURES_ARE_DISTINCT_TYPED_OBJECTS"
    "__CSP4_COMPOSITION_LEAVES_REAL_CHARACTER_FAMILY_R_TO_ALPHA"
    "__UNIVERSAL_PHYSICAL_BRANCH_MEASURE_SOURCE_POPULATION_AND_CRITICAL_COMPLETION_REMAIN_OPEN"
)


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*a)]


def scale_matrix(c: Fraction, a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[c * value for value in row] for row in a]


def subtract(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def determinant(a: list[list[Fraction]]) -> Fraction:
    work = [row[:] for row in a]
    value = Fraction(1)
    n = len(work)
    for column in range(n):
        pivot = next((row for row in range(column, n) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        pivot_value = work[column][column]
        value *= pivot_value
        for row in range(column + 1, n):
            factor = work[row][column] / pivot_value
            for k in range(column + 1, n):
                work[row][k] -= factor * work[column][k]
    return value


def inverse2(a: list[list[Fraction]]) -> list[list[Fraction]]:
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0:
        raise ZeroDivisionError("singular 2x2 matrix")
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def block(a: list[list[Fraction]], b: list[list[Fraction]],
          c: list[list[Fraction]], d: list[list[Fraction]]) -> list[list[Fraction]]:
    return [a[i] + b[i] for i in range(2)] + [c[i] + d[i] for i in range(2)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=10000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    assertions = 0

    def check(value: bool) -> None:
        nonlocal assertions
        assertions += 1
        if not value:
            raise AssertionError(f"independent exact check {assertions} failed")

    zero = Fraction(0)
    one = Fraction(1)
    eye2 = [[one, zero], [zero, one]]
    zero2 = [[zero, zero], [zero, zero]]
    omega4 = block(zero2, eye2, scale_matrix(Fraction(-1), eye2), zero2)
    eye4 = [[one if i == j else zero for j in range(4)] for i in range(4)]
    rng = random.Random(824248)
    separated = 0
    inverse_density_changes = 0

    for _ in range(args.cases):
        while True:
            g = [[Fraction(rng.randint(1, 9), rng.randint(1, 7)),
                  Fraction(rng.randint(-5, 5), rng.randint(1, 7))],
                 [Fraction(rng.randint(-5, 5), rng.randint(1, 7)),
                  Fraction(rng.randint(1, 9), rng.randint(1, 7))]]
            if determinant(g) != 0:
                break
        g_inv_t = transpose(inverse2(g))
        # Independent symplectic construction: Fourier exchange times diag(g,g^-T).
        symplectic = block(zero2, g_inv_t, scale_matrix(Fraction(-1), g), zero2)
        q = Fraction(rng.randint(1, 11), rng.randint(1, 9))
        r = q * q
        phase = scale_matrix(q, symplectic)

        residual = subtract(matmul(matmul(transpose(phase), omega4), phase), scale_matrix(r, omega4))
        for row in residual:
            for value in row:
                check(value == 0)
        check(determinant(phase) == r * r)

        a_block = [row[:2] for row in phase[:2]]
        b_block = [row[2:] for row in phase[:2]]
        c_block = [row[:2] for row in phase[2:]]
        d_block = [row[2:] for row in phase[2:]]
        inverse_formula = scale_matrix(
            one / r,
            block(transpose(d_block), scale_matrix(Fraction(-1), transpose(b_block)),
                  scale_matrix(Fraction(-1), transpose(c_block)), transpose(a_block)),
        )
        product = matmul(phase, inverse_formula)
        for i in range(4):
            for j in range(4):
                check(product[i][j] == eye4[i][j])

        inverse_b = [row[2:] for row in inverse_formula[:2]]
        expected_inverse_b = scale_matrix(Fraction(-1, 1) / r, transpose(b_block))
        check(inverse_b == expected_inverse_b)
        area = abs(determinant(b_block))
        inverse_area = abs(determinant(inverse_b))
        check(area > 0)
        check(inverse_area == area / (r * r))
        coarea = r / area
        check((one / r) / inverse_area == coarea)

        # Independent Lorentz determinant calculation in (t,x,y,z).
        omega_b = one / r
        gauge1 = Fraction(rng.randint(-7, 7), rng.randint(1, 9))
        gauge2 = Fraction(rng.randint(-7, 7), rng.randint(1, 9))
        k = [omega_b, zero, zero, omega_b]
        j1 = [gauge1 * k[0], b_block[0][0], b_block[1][0], gauge1 * k[3]]
        j2 = [gauge2 * k[0], b_block[0][1], b_block[1][1], gauge2 * k[3]]
        u = [one, zero, zero, zero]
        columns = [j1, j2, k, u]
        lorentz_matrix = [[columns[j][i] for j in range(4)] for i in range(4)]
        jacobian = abs(determinant(lorentz_matrix))
        check(jacobian == area / r)
        check(one / jacobian == coarea)

        q2 = Fraction(rng.randint(1, 11), rng.randint(1, 9))
        r2 = q2 * q2
        for alpha in (-4, -2, -1, 0, 1, 2, 4):
            check((r * r2) ** alpha == r**alpha * r2**alpha)
            check((one / r) ** alpha == one / (r**alpha))

        counting = one
        symmetric_clock = q
        if len({counting, symmetric_clock, coarea}) > 1:
            separated += 1
        if r != 1:
            # Same inverse coefficient, but the rebuilt inverse ordered query is based on d_tau_B.
            inverse_density_changes += 1

        check((one / (r * r)) == one / determinant(phase))

    check(separated > 0)
    check(inverse_density_changes > 0)

    result = {
        "assertions": assertions,
        "cases": args.cases,
        "expected_landing": LANDING,
        "implementation": "independent_fraction_fourier_symplectic_no_production_import_or_output_read",
        "inverse_density_changes": inverse_density_changes,
        "measure_separation_cases": separated,
        "observational_outcomes": "CLOSED_AND_UNREAD",
        "status": "PASS",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
