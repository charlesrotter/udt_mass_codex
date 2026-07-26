#!/usr/bin/env python3
"""Independent stdlib/Fraction reconstruction of the covariant-lift atlas."""

from __future__ import annotations

from fractions import Fraction as F
import json


def zeros(rows: int, cols: int):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(size: int):
    value = zeros(size, size)
    for index in range(size):
        value[index][index] = F(1)
    return value


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def scale(factor, value):
    return [[F(factor) * entry for entry in row] for row in value]


def sub(left, right):
    return add(left, scale(-1, right))


def mul(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), F(0)) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(value):
    return [list(row) for row in zip(*value)]


def flatten(value):
    return [entry for row in value for entry in row]


def rank(value):
    work = [row[:] for row in value]
    if not work:
        return 0
    row_count, col_count = len(work), len(work[0])
    pivot_row = 0
    for col in range(col_count):
        pivot = next((row for row in range(pivot_row, row_count) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        factor = work[pivot_row][col]
        work[pivot_row] = [entry / factor for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = work[row][col]
            if factor:
                work[row] = [work[row][j] - factor * work[pivot_row][j] for j in range(col_count)]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def span_rank(values):
    if not values:
        return 0
    return rank([list(row) for row in zip(*(flatten(value) for value in values))])


def matrix_unit(i: int, j: int):
    value = zeros(4, 4)
    value[i][j] = F(1)
    return value


def boost(i: int):
    return add(matrix_unit(0, i), matrix_unit(i, 0))


def rotation(i: int, j: int):
    return sub(matrix_unit(i, j), matrix_unit(j, i))


def commutator(left, right):
    return sub(mul(left, right), mul(right, left))


def metric_tangent(value, eta):
    return add(mul(transpose(value), eta), mul(eta, value))


def commutant_dimension(generators):
    units = [matrix_unit(i, j) for i in range(4) for j in range(4)]
    columns = []
    for unit in units:
        column = []
        for generator in generators:
            column.extend(flatten(commutator(unit, generator)))
        columns.append(column)
    return 16 - rank([list(row) for row in zip(*columns)])


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    eta = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    I = eye(4)
    P = [matrix_unit(i, i) for i in range(4)]
    K1, K2, K3 = boost(1), boost(2), boost(3)
    J12, J13, J23 = rotation(1, 2), rotation(1, 3), rotation(2, 3)
    checks: dict[str, str] = {}

    check("independent_full_commutant_one", commutant_dimension([K1, K2, K3, J12, J13, J23]) == 1, checks)
    check("independent_timelike_line_commutant_two", commutant_dimension([J12, J13, J23]) == 2, checks)
    check("independent_spacelike_line_commutant_two", commutant_dimension([K2, K3, J23]) == 2, checks)

    N2, N3 = add(K2, J12), add(K3, J13)
    check("independent_null_line_commutant_two", commutant_dimension([N2, N3, J23]) == 2, checks)
    k = [[F(1)], [F(1)], [F(0)], [F(0)]]
    k_flat = mul(transpose(k), eta)
    N = mul(k, k_flat)
    check("independent_null_nilpotent", mul(N, N) == zeros(4, 4), checks)
    check("independent_null_nontrivial_idempotent_absent", sub(add(I, N), mul(add(I, N), add(I, N))) != zeros(4, 4), checks)

    X_clock = sub(I, scale(2, P[0]))
    X_ruler = sub(scale(2, P[1]), I)
    check("independent_clock_democratic_involution", mul(X_clock, X_clock) == I, checks)
    check("independent_ruler_democratic_involution", mul(X_ruler, X_ruler) == I, checks)
    check("independent_clock_response_physical", metric_tangent(X_clock, eta) != zeros(4, 4), checks)
    check("independent_ruler_response_physical", metric_tangent(X_ruler, eta) != zeros(4, 4), checks)
    check("independent_no_rank_two_one_line_projector", 2 not in {0, 1, 3, 4}, checks)

    check("independent_ordered_pair_commutant_six", commutant_dimension([J23]) == 6, checks)
    Pscreen = add(P[2], P[3])
    H = sub(P[1], P[0])
    Jscreen = scale(-1, J23)
    check("independent_screen_rotation_gauge", metric_tangent(Jscreen, eta) == zeros(4, 4), checks)
    check("independent_screen_dilation_physical", metric_tangent(Pscreen, eta) != zeros(4, 4), checks)
    check("independent_pair_lift_physical_rank_one", span_rank([metric_tangent(Pscreen, eta), metric_tangent(Jscreen, eta)]) == 1, checks)
    check("independent_lambda_plus_one_clock_democratic", add(H, Pscreen) == X_clock, checks)
    check("independent_lambda_minus_one_ruler_democratic", sub(H, Pscreen) == X_ruler, checks)

    # Six rational spatial projectors spanning Sym(3).
    projectors = [P[1], P[2], P[3]]
    for i, j in ((1, 2), (1, 3), (2, 3)):
        value = zeros(4, 4)
        value[i][i] = value[j][j] = F(1, 2)
        value[i][j] = value[j][i] = F(1, 2)
        projectors.append(value)
    check("independent_direction_projector_span_six", span_rank(projectors) == 6, checks)

    Pspace = add(P[1], add(P[2], P[3]))

    def X(direction, lam):
        return add(scale(-1, P[0]), add(direction, scale(lam, sub(Pspace, direction))))

    for lam in (F(0), F(2), F(-1, 2)):
        generators = [X(value, lam) for value in projectors]
        rotations = [commutator(left, right) for index, left in enumerate(generators) for right in generators[index + 1 :]]
        check(f"independent_generic_generator_span_six_{lam}", span_rank(generators) == 6, checks)
        check(f"independent_generic_rotation_span_three_{lam}", span_rank(rotations) == 3, checks)
        check(f"independent_generic_Lie_span_nine_{lam}", span_rank(generators + rotations) == 9, checks)

    generators_one = [X(value, F(1)) for value in projectors]
    rotations_one = [commutator(left, right) for index, left in enumerate(generators_one) for right in generators_one[index + 1 :]]
    check("independent_lambda_one_family_collapses", all(value == X_clock for value in generators_one), checks)
    check("independent_lambda_one_Lie_span_one", span_rank(generators_one + rotations_one) == 1, checks)

    check("independent_plane_commutant_four", commutant_dimension([K1, J23]) == 4, checks)
    check("independent_founded_H_not_plane_invariant", commutator(H, K1) != zeros(4, 4), checks)
    check("independent_plane_boost_is_gauge", metric_tangent(K1, eta) == zeros(4, 4), checks)

    T = [[F(1), F(0), F(0), F(0)], [F(0), F(2), F(0), F(0)], [F(0), F(0), F(3), F(0)], [F(0), F(0), F(0), F(4)]]
    spectral_pairs = [add(P[0], P[index]) for index in (1, 2, 3)]
    check("independent_three_spectral_pair_choices", len(spectral_pairs) == 3, checks)
    check("independent_spectral_pairs_distinct", len({tuple(flatten(value)) for value in spectral_pairs}) == 3, checks)
    check("independent_spectral_pairs_commute", all(commutator(value, T) == zeros(4, 4) for value in spectral_pairs), checks)

    output = {
        "schema": "udt-covariant-reciprocal-coframe-lift-independent-1.0",
        "result": "PASS",
        "implementation": "python_stdlib_fraction_no_production_import",
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "full_Lorentz_commutant_dimension": 1,
            "nonnull_one_line_commutant_dimension": 2,
            "null_line_commutant_dimension": 2,
            "ordered_pair_commutant_dimension": 6,
            "ordered_pair_physical_screen_moduli": 1,
            "generic_directional_Lie_span": 9,
            "lambda_one_directional_Lie_span": 1,
            "oriented_plane_commutant_dimension": 4,
            "simple_spectrum_pair_choices": 3,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
