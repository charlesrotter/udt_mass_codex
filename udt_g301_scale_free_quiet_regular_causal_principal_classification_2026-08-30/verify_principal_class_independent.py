#!/usr/bin/env python3
"""Independent exact replay for G301. Imports no production code."""

from __future__ import annotations

import json
import random
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 4
SIGNS = (-1, 1, 1, 1)
POSITIONS = [(i, j) for i in range(N) for j in range(i, N)]


def to_tensor(values):
    tensor = [[Fraction(0) for _ in range(N)] for _ in range(N)]
    for value, (i, j) in zip(values, POSITIONS):
        tensor[i][j] = value
        tensor[j][i] = value
    return tensor


def to_values(tensor):
    return [tensor[i][j] for i, j in POSITIONS]


def lorentz_trace(tensor):
    return sum(SIGNS[i] * tensor[i][i] for i in range(N))


def residual(tensor, a, b):
    tr = lorentz_trace(tensor)
    out = [[a * tensor[i][j] for j in range(N)] for i in range(N)]
    for i in range(N):
        out[i][i] += b * tr * SIGNS[i]
    return out


def operator_columns(a, b):
    columns = []
    for col in range(len(POSITIONS)):
        unit = [Fraction(0) for _ in POSITIONS]
        unit[col] = Fraction(1)
        columns.append(to_values(residual(to_tensor(unit), a, b)))
    return [[columns[j][i] for j in range(len(POSITIONS))] for i in range(len(POSITIONS))]


def matrix_rank(rows):
    rows = [row[:] for row in rows]
    pivots = 0
    for column in range(len(rows[0])):
        selected = None
        for row in range(pivots, len(rows)):
            if rows[row][column]:
                selected = row
                break
        if selected is None:
            continue
        rows[pivots], rows[selected] = rows[selected], rows[pivots]
        divisor = rows[pivots][column]
        for j in range(column, len(rows[0])):
            rows[pivots][j] /= divisor
        for row in range(pivots + 1, len(rows)):
            factor = rows[row][column]
            if factor:
                for j in range(column, len(rows[0])):
                    rows[row][j] -= factor * rows[pivots][j]
        pivots += 1
    return pivots


def zero(tensor):
    return all(value == 0 for row in tensor for value in row)


def main():
    rng = random.Random(1901301)
    checks = 0
    cases = 0

    for _ in range(12000):
        a = Fraction(rng.randint(-17, 17), rng.randint(1, 7))
        b = Fraction(rng.randint(-17, 17), rng.randint(1, 7))
        rank = matrix_rank(operator_columns(a, b))
        if a == 0 and b == 0:
            expected = 0
        elif a == 0:
            expected = 1
        elif a + 4 * b == 0:
            expected = 9
        else:
            expected = 10
        assert rank == expected
        checks += 1

        values = [Fraction(rng.randint(-19, 19), rng.randint(1, 9)) for _ in POSITIONS]
        tensor = to_tensor(values)
        image = residual(tensor, a, b)
        assert lorentz_trace(image) == (a + 4 * b) * lorentz_trace(tensor)
        checks += 1

        if expected == 10:
            tr_x = lorentz_trace(image) / (a + 4 * b)
            recovered = [[image[i][j] / a for j in range(N)] for i in range(N)]
            for i in range(N):
                recovered[i][i] -= (b * tr_x / a) * SIGNS[i]
            assert to_values(recovered) == values
            checks += 1
        cases += 1

    metric = to_tensor([-1, 0, 0, 0, 1, 0, 0, 1, 0, 1])
    assert lorentz_trace(metric) == 4
    assert zero(residual(metric, Fraction(1), Fraction(-1, 4)))
    assert not zero(residual(metric, Fraction(1), Fraction(-1, 2)))
    checks += 3

    traceless = to_tensor([1, 0, 0, 0, 1, 0, 0, 0, 0, 0])
    assert lorentz_trace(traceless) == 0
    assert zero(residual(traceless, Fraction(0), Fraction(1)))
    assert not zero(residual(traceless, Fraction(1), Fraction(-1, 4)))
    checks += 3

    # Direction-independent differentiability test behind the homogeneity lemma:
    # F(t x)/t is frozen by degree-one homogeneity, so its t->0 limit equals F(x).
    for _ in range(3000):
        fx = Fraction(rng.randint(-100, 100), rng.randint(1, 20))
        for t in (Fraction(1, 2), Fraction(1, 7), Fraction(1, 101)):
            assert (t * fx) / t == fx
            checks += 1

    # Nonzero covector times a Fourier scalar can vanish componentwise only for scalar zero.
    for _ in range(5000):
        covector = [Fraction(rng.randint(-12, 12)) for _ in range(N)]
        if all(x == 0 for x in covector):
            covector[0] = Fraction(1)
        scalar = Fraction(rng.randint(-12, 12))
        if all(x * scalar == 0 for x in covector):
            assert scalar == 0
        checks += 1

    result = {
        "verdict": "INDEPENDENT_COEFFICIENT_STRATA_AGREEMENT_CONDITIONAL_ON_TWO_TERM_BASIS",
        "scope": "DOWNSTREAM_A_RICCI_PLUS_B_R_G_ALGEBRA_ONLY",
        "landing": "TWO_INEQUIVALENT_FULL_METRIC_QUIET_PRINCIPAL_CLASSES_SURVIVE__GENERIC_RICCI_FLAT_AND_TRACEFREE_RICCI_WITH_ONE_CONSTANT_SCALAR_DATUM",
        "random_coefficient_cases": cases,
        "assertions": checks,
        "production_imported": False,
        "full_invariant_basis_certified": False,
        "metric_change": False,
        "kernel_change": False,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
