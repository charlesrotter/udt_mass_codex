#!/usr/bin/env python3
"""Independent constructive verification of the G310 all-pair span and annihilator."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


SYMMETRIC_INDICES = tuple((i, j) for i in range(4) for j in range(i, 4))


def zero_matrix() -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(4)] for _ in range(4)]


def covector(vector: list[Fraction]) -> list[Fraction]:
    return [-vector[0], vector[1], vector[2], vector[3]]


def outer(left: list[Fraction], right: list[Fraction]) -> list[list[Fraction]]:
    return [[left[i] * right[j] for j in range(4)] for i in range(4)]


def add(*values: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum((value[i][j] for value in values), Fraction(0)) for j in range(4)] for i in range(4)]


def scale(factor: Fraction, value: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[factor * entry for entry in row] for row in value]


def subtract(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    return add(left, scale(Fraction(-1), right))


def pair_tangent(u: list[Fraction], n: list[Fraction]) -> list[list[Fraction]]:
    u_flat = covector(u)
    n_flat = covector(n)
    return scale(Fraction(2), add(outer(u_flat, u_flat), outer(n_flat, n_flat)))


def inner(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return -left[0] * right[0] + sum(left[i] * right[i] for i in range(1, 4))


def vectorize(value: list[list[Fraction]]) -> list[Fraction]:
    return [value[i][j] for i, j in SYMMETRIC_INDICES]


def rank(rows: list[list[Fraction]]) -> int:
    work = [list(row) for row in rows if any(row)]
    row_index = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next((i for i in range(row_index, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row_index], work[pivot] = work[pivot], work[row_index]
        divisor = work[row_index][column]
        work[row_index] = [entry / divisor for entry in work[row_index]]
        for i in range(row_index + 1, len(work)):
            if work[i][column]:
                factor = work[i][column]
                work[i] = [a - factor * b for a, b in zip(work[i], work[row_index])]
        row_index += 1
    return row_index


def lorentz_pairing_row(value: list[list[Fraction]]) -> list[Fraction]:
    row: list[Fraction] = []
    for i, j in SYMMETRIC_INDICES:
        multiplicity = Fraction(1 if i == j else 2)
        raised_sign = Fraction(-1 if (i == 0) ^ (j == 0) else 1)
        row.append(multiplicity * raised_sign * value[i][j])
    return row


def nullspace(rows: list[list[Fraction]]) -> list[list[Fraction]]:
    work = [list(row) for row in rows if any(row)]
    pivot_columns: list[int] = []
    row_index = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next((i for i in range(row_index, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row_index], work[pivot] = work[pivot], work[row_index]
        divisor = work[row_index][column]
        work[row_index] = [entry / divisor for entry in work[row_index]]
        for i in range(len(work)):
            if i == row_index or not work[i][column]:
                continue
            factor = work[i][column]
            work[i] = [a - factor * b for a, b in zip(work[i], work[row_index])]
        pivot_columns.append(column)
        row_index += 1
        if row_index == len(work):
            break
    free_columns = [column for column in range(len(work[0])) if column not in pivot_columns]
    basis: list[list[Fraction]] = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(len(work[0]))]
        vector[free] = Fraction(1)
        for i, pivot in enumerate(pivot_columns):
            vector[pivot] = -work[i][free]
        basis.append(vector)
    return basis


def proportional(left: list[Fraction], right: list[Fraction]) -> bool:
    ratio: Fraction | None = None
    for a, b in zip(left, right):
        if b == 0:
            if a != 0:
                return False
            continue
        candidate = a / b
        if ratio is None:
            ratio = candidate
        elif candidate != ratio:
            return False
    return ratio is not None


def basis_matrix(i: int, j: int) -> list[list[Fraction]]:
    result = zero_matrix()
    result[i][j] = Fraction(1)
    result[j][i] = Fraction(1)
    return result


def build_result() -> dict[str, object]:
    checks = 0
    basis = [[Fraction(1 if i == j else 0) for i in range(4)] for j in range(4)]
    e0, e1, e2, e3 = basis
    spatial = (e1, e2, e3)
    diagonal_tangents = [pair_tangent(e0, direction) for direction in spatial]
    for i, tangent in enumerate(diagonal_tangents, start=1):
        assert inner(e0, e0) == -1
        assert inner(spatial[i - 1], spatial[i - 1]) == 1
        assert vectorize(tangent) == vectorize(pair_tangent(e0, spatial[i - 1]))
        checks += 3

    spatial_cross: list[list[list[Fraction]]] = []
    c = Fraction(5, 13)
    s = Fraction(12, 13)
    assert c * c + s * s == 1
    checks += 1
    for first, second in ((0, 1), (0, 2), (1, 2)):
        n = [c * spatial[first][k] + s * spatial[second][k] for k in range(4)]
        assert inner(n, n) == 1 and inner(e0, n) == 0
        mixed = pair_tangent(e0, n)
        residual = subtract(
            subtract(mixed, scale(c * c, diagonal_tangents[first])),
            scale(s * s, diagonal_tangents[second]),
        )
        expected = scale(2 * c * s, basis_matrix(first + 1, second + 1))
        assert residual == expected
        spatial_cross.append(residual)
        checks += 2

    time_cross: list[list[list[Fraction]]] = []
    ch = Fraction(5, 4)
    sh = Fraction(3, 4)
    assert ch * ch - sh * sh == 1
    checks += 1
    for index, direction in enumerate(spatial):
        u = [ch * e0[k] + sh * direction[k] for k in range(4)]
        n = [sh * e0[k] + ch * direction[k] for k in range(4)]
        assert inner(u, u) == -1 and inner(n, n) == 1 and inner(u, n) == 0
        residual = subtract(pair_tangent(u, n), scale(ch * ch + sh * sh, diagonal_tangents[index]))
        expected = scale(-4 * ch * sh, basis_matrix(0, index + 1))
        assert residual == expected
        time_cross.append(residual)
        checks += 2

    constructive_basis = diagonal_tangents + spatial_cross + time_cross
    assert rank([vectorize(value) for value in constructive_basis]) == 9
    checks += 1

    # Independently reconstruct the annihilator from the Lorentz-pairing rows.
    balance_rows = [lorentz_pairing_row(value) for value in constructive_basis]
    assert rank(balance_rows) == 9
    checks += 1
    annihilator = nullspace(balance_rows)
    assert len(annihilator) == 1
    checks += 1
    metric_vector = vectorize([
        [Fraction(-1), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
    ])
    assert proportional(annihilator[0], metric_vector)
    checks += 1

    # Read the component equations from the computed null vector.
    response = annihilator[0]
    assert response[4] == -response[0]
    assert response[7] == -response[0]
    assert response[9] == -response[0]
    checks += 3
    assert all(response[index] == 0 for index in (1, 2, 3, 5, 6, 8))
    checks += 1

    # The untouched trace is not fixed: two distinct nonzero metric multiples obey all balances.
    double_metric = [Fraction(2) * entry for entry in metric_vector]
    triple_metric = [Fraction(3) * entry for entry in metric_vector]
    assert double_metric != triple_metric
    assert all(sum(a * b for a, b in zip(row, double_metric)) == 0 for row in balance_rows)
    assert all(sum(a * b for a, b in zip(row, triple_metric)) == 0 for row in balance_rows)
    checks += 1

    return {
        "status": "PASS",
        "method": "constructive_plane_combinations_with_distinct_rational_rotation_and_boost",
        "tangent_normalization": "H=2*(u_flat tensor u_flat+n_flat tensor n_flat)",
        "constructive_shape_rank": 9,
        "lorentz_pairing_rank": 9,
        "annihilator_nullity": 1,
        "annihilator_derived_from_balance_rows": True,
        "annihilator_equations": "A_ii=-A_00; A_ij=0; A_0i=0",
        "annihilator": "span(g_ab)",
        "common_trace_magnitude_fixed": False,
        "independent_checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
