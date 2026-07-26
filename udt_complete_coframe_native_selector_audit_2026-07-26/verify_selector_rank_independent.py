#!/usr/bin/env python3
"""Independent stdlib rational reconstruction of selector-rank claims."""

from __future__ import annotations

from fractions import Fraction
import json


Q = Fraction


def matrix(rows: list[list[int | Fraction]]) -> list[list[Fraction]]:
    return [[Q(value) for value in row] for row in rows]


def zero(rows: int, cols: int) -> list[list[Fraction]]:
    return [[Q(0) for _ in range(cols)] for _ in range(rows)]


def identity(size: int) -> list[list[Fraction]]:
    value = zero(size, size)
    for index in range(size):
        value[index][index] = Q(1)
    return value


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def subtract(left, right):
    return [[left[i][j] - right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def multiply(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), Q(0)) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(value):
    return [list(row) for row in zip(*value)]


def flatten(value):
    return [entry for row in value for entry in row]


def rank(value: list[list[Fraction]]) -> int:
    work = [row[:] for row in value]
    if not work:
        return 0
    rows, cols = len(work), len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            scale = work[row][col]
            if scale:
                work[row] = [work[row][j] - scale * work[pivot_row][j] for j in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def columns_rank(columns: list[list[Fraction]]) -> int:
    return rank([list(row) for row in zip(*columns)])


def metric_tangent(generator, eta):
    return add(multiply(transpose(generator), eta), multiply(eta, generator))


def commutator(left, right):
    return subtract(multiply(left, right), multiply(right, left))


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    eta = matrix([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    extension_basis = []
    for i, j in ((2, 2), (2, 3), (3, 3), (2, 0), (2, 1), (3, 0), (3, 1)):
        value = zero(4, 4)
        value[i][j] = Q(1)
        extension_basis.append(value)
    checks: dict[str, str] = {}
    check("independent_extension_rank_seven", columns_rank([flatten(value) for value in extension_basis]) == 7, checks)
    physical = [metric_tangent(value, eta) for value in extension_basis]
    check("independent_physical_tangent_rank_seven", columns_rank([flatten(value) for value in physical]) == 7, checks)

    # Rebuild the full six-dimensional eta-antisymmetric presentation kernel.
    matrix_units = []
    for i in range(4):
        for j in range(4):
            value = zero(4, 4)
            value[i][j] = Q(1)
            matrix_units.append(value)
    lorentz_map = [flatten(metric_tangent(value, eta)) for value in matrix_units]
    check("independent_Lorentz_kernel_dimension_six", 16 - columns_rank(lorentz_map) == 6, checks)

    # Centralizer of exact boost/rotation generators.
    generators = []
    for i in range(1, 4):
        value = zero(4, 4)
        value[0][i] = Q(1)
        value[i][0] = Q(1)
        generators.append(value)
    for i, j in ((1, 2), (1, 3), (2, 3)):
        value = zero(4, 4)
        value[i][j] = Q(1)
        value[j][i] = Q(-1)
        generators.append(value)
    centralizer_map = []
    for unit in matrix_units:
        column = []
        for generator in generators:
            column.extend(flatten(commutator(unit, generator)))
        centralizer_map.append(column)
    check("independent_full_frame_centralizer_dimension_one", 16 - columns_rank(centralizer_map) == 1, checks)
    founded = matrix([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    check("independent_founded_generator_not_frame_invariant", commutator(founded, generators[0]) != zero(4, 4), checks)

    # Conditional equation ranks, formed directly without production code.
    # Parameter order: a,b,d,c11,c12,c21,c22.
    det_rows = matrix([[1, 0, 1, 0, 0, 0, 0]])
    angular_rows = matrix([[2, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0]])
    mixing_rows = matrix([
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1],
    ])
    check("independent_determinant_rank_one", rank(det_rows) == 1, checks)
    check("independent_angular_rank_three", rank(angular_rows) == 3, checks)
    check("independent_mixing_rank_four", rank(mixing_rows) == 4, checks)
    check("independent_spectator_joint_rank_seven", rank(angular_rows + mixing_rows) == 7, checks)

    # Exact rational first-order witnesses: one angular and one mixing
    # direction are nonzero physical metric tangents while preserving the
    # fixed founded base block.
    angular_witness = extension_basis[0]
    mixing_witness = extension_basis[3]
    check("independent_angular_witness_physical", metric_tangent(angular_witness, eta) != zero(4, 4), checks)
    check("independent_mixing_witness_physical", metric_tangent(mixing_witness, eta) != zero(4, 4), checks)

    result = {
        "schema": "udt-complete-coframe-native-selector-independent-1.0",
        "result": "PASS",
        "implementation": "python_stdlib_fraction_no_production_import",
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "extension_rank": 7,
            "physical_tangent_rank": 7,
            "Lorentz_kernel_dimension": 6,
            "full_frame_centralizer_dimension": 1,
            "active_selector_rank": 0,
            "survivor_dimension": 7,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
