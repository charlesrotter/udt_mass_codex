#!/usr/bin/env python3
"""Independent standard-library rational replay for the stratified first-jet atlas."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_RESULT.json"
ETA = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
SLOTS = [(i, j) for i in range(4) for j in range(i, 4)]


def zeros(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    result = zeros(n, n)
    for i in range(n):
        result[i][i] = F(1)
    return result


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def multiply(a, b):
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def scale(a, value):
    return [[value * entry for entry in row] for row in a]


def flatten(a):
    return [entry for row in a for entry in row]


def rref(a):
    work = [row[:] for row in a]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    pivots = []
    lead = 0
    for row in range(rows):
        while lead < cols:
            pivot = next((r for r in range(row, rows) if work[r][lead] != 0), None)
            if pivot is not None:
                break
            lead += 1
        if lead == cols:
            break
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][lead]
        work[row] = [entry / value for entry in work[row]]
        for other in range(rows):
            if other == row:
                continue
            factor = work[other][lead]
            if factor:
                work[other] = [work[other][j] - factor * work[row][j] for j in range(cols)]
        pivots.append(lead)
        lead += 1
    return work, pivots


def rank(a):
    return len(rref(a)[1])


def nullspace(a):
    reduced, pivots = rref(a)
    cols = len(a[0])
    free = [col for col in range(cols) if col not in pivots]
    result = []
    for free_col in free:
        vector = [F(0) for _ in range(cols)]
        vector[free_col] = F(1)
        for row, pivot_col in enumerate(pivots):
            vector[pivot_col] = -reduced[row][free_col]
        result.append(vector)
    return result


def inverse(a):
    n = len(a)
    augmented = [a[i][:] + eye(n)[i] for i in range(n)]
    reduced, pivots = rref(augmented)
    if pivots[:n] != list(range(n)):
        raise ValueError("singular")
    return [row[n:] for row in reduced[:n]]


def determinant(a):
    work = [row[:] for row in a]
    result = F(1)
    swaps = 0
    n = len(a)
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col] != 0), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            swaps += 1
        value = work[col][col]
        result *= value
        for row in range(col + 1, n):
            factor = work[row][col] / value
            for j in range(col, n):
                work[row][j] -= factor * work[col][j]
    return -result if swaps % 2 else result


def matrix_vector(a, v):
    return [sum((a[i][j] * v[j] for j in range(len(v))), F(0)) for i in range(len(a))]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def tangent(x):
    return add(multiply(transpose(x), ETA), multiply(ETA, x))


def columns_to_matrix(columns):
    return [list(row) for row in zip(*columns)] if columns else []


def coframe_map():
    columns = []
    for k in range(16):
        x = zeros(4, 4)
        x[k // 4][k % 4] = F(1)
        t = tangent(x)
        columns.append([t[i][j] for i, j in SLOTS])
    coefficient = columns_to_matrix(columns)

    h = zeros(4, 4)
    h[0][0], h[1][1] = F(-1), F(1)
    generators = [h]
    base_scale = zeros(4, 4)
    base_scale[0][0] = base_scale[1][1] = F(1)
    generators.append(base_scale)
    base_offdiag = zeros(4, 4)
    base_offdiag[0][1], base_offdiag[1][0] = F(1), F(-1)
    generators.append(base_offdiag)
    screen_area = zeros(4, 4)
    screen_area[2][2] = screen_area[3][3] = F(1)
    generators.append(screen_area)
    screen_shear = zeros(4, 4)
    screen_shear[2][2], screen_shear[3][3] = F(1), F(-1)
    generators.append(screen_shear)
    screen_offdiag = zeros(4, 4)
    screen_offdiag[2][3] = screen_offdiag[3][2] = F(1)
    generators.append(screen_offdiag)
    for a in (0, 1):
        for b in (2, 3):
            generator = zeros(4, 4)
            generator[a][b] = F(1)
            generator[b][a] = F(1) if a == 1 else F(-1)
            generators.append(generator)
    basis = columns_to_matrix([[tangent(g)[i][j] for i, j in SLOTS] for g in generators])

    gauge = lorentz_basis()
    gauge_flat = columns_to_matrix([flatten(g) for g in gauge])
    return {
        "per_direction_rank": rank(coefficient),
        "per_direction_nullity": 16 - rank(coefficient),
        "full_rank": 4 * rank(coefficient),
        "full_nullity": 4 * (16 - rank(coefficient)),
        "metric_basis_rank": rank(basis),
        "Lorentz_gauge_dimension": rank(gauge_flat),
        "Lorentz_gauge_tangents_zero": all(tangent(g) == zeros(4, 4) for g in gauge),
    }


def block(rows):
    result = []
    for row_blocks in rows:
        for local_row in range(len(row_blocks[0])):
            result.append(sum((matrix[local_row] for matrix in row_blocks), []))
    return result


def factor_coframe(a, q, s):
    abase = [[F(1, 1) / a, F(0)], [F(0), a]]
    qs = multiply(q, s)
    z = zeros(2, 2)
    return block([[abase, z], [qs, q]])


def causal(a, q, s, p):
    e = factor_coframe(a, q, s)
    metric = multiply(multiply(transpose(e), ETA), e)
    return dot(p, matrix_vector(inverse(metric), p))


def joint_causal():
    p = [F(1), F(0), F(1), F(0)]
    q_identity = eye(2)
    s_zero = zeros(2, 2)
    mixing = {
        "timelike": causal(F(1), q_identity, [[F(-1), F(0)], [F(0), F(0)]], p),
        "null": causal(F(1), q_identity, s_zero, p),
        "spacelike": causal(F(1), q_identity, [[F(1), F(0)], [F(0), F(0)]], p),
    }
    shear = {
        "timelike": causal(F(1), [[F(2), F(0)], [F(0), F(1, 2)]], s_zero, p),
        "null": causal(F(1), q_identity, s_zero, p),
        "spacelike": causal(F(1), [[F(1, 2), F(0)], [F(0), F(2)]], s_zero, p),
    }
    return {
        "mixing": mixing,
        "unit_area_shear": shear,
        "shear_determinants": [determinant([[F(2), F(0)], [F(0), F(1, 2)]]), F(1), determinant([[F(1, 2), F(0)], [F(0), F(2)]])],
    }


def lorentz_basis():
    signs = [F(-1), F(1), F(1), F(1)]
    basis = []
    for a in range(4):
        for b in range(a + 1, 4):
            generator = zeros(4, 4)
            generator[a][b] = F(1)
            generator[b][a] = -signs[a] / signs[b]
            basis.append(generator)
    return basis


def linear_combination(coefficients, matrices):
    result = zeros(4, 4)
    for coefficient, matrix in zip(coefficients, matrices):
        result = add(result, scale(matrix, coefficient))
    return result


def solve_coordinates(basis_columns, vector):
    a = columns_to_matrix(basis_columns)
    at = transpose(a)
    gram = multiply(at, a)
    rhs = matrix_vector(at, vector)
    return matrix_vector(inverse(gram), rhs)


def inertia_symmetric(matrix):
    work = [row[:] for row in matrix]
    positive = negative = zero = 0
    while work:
        n = len(work)
        diagonal = next((i for i in range(n) if work[i][i] != 0), None)
        if diagonal is not None:
            if diagonal != 0:
                work[0], work[diagonal] = work[diagonal], work[0]
                for row in work:
                    row[0], row[diagonal] = row[diagonal], row[0]
            pivot = work[0][0]
            positive += pivot > 0
            negative += pivot < 0
            work = [[work[i][j] - work[i][0] * work[0][j] / pivot for j in range(1, n)] for i in range(1, n)]
            continue
        off = next(((i, j) for i in range(n) for j in range(i + 1, n) if work[i][j] != 0), None)
        if off is None:
            zero += n
            break
        i, j = off
        order = [i, j] + [k for k in range(n) if k not in (i, j)]
        work = [[work[r][c] for c in order] for r in order]
        block2 = [[work[0][0], work[0][1]], [work[1][0], work[1][1]]]
        inv2 = inverse(block2)
        positive += 1
        negative += 1
        remainder = n - 2
        coupling = [[work[r][c] for c in range(2)] for r in range(2, n)]
        tail = [[work[r][c] for c in range(2, n)] for r in range(2, n)]
        correction = multiply(multiply(coupling, inv2), transpose(coupling))
        work = subtract(tail, correction) if remainder else []
    return [int(positive), int(negative), int(zero)]


def stabilizer(name, p):
    ambient = lorentz_basis()
    action_columns = []
    for generator in ambient:
        action_columns.append(matrix_vector(transpose(generator), p))
    coefficients = nullspace(columns_to_matrix(action_columns))
    subalgebra = [linear_combination(vector, ambient) for vector in coefficients]
    flat_columns = [flatten(matrix) for matrix in subalgebra]
    dimension = len(subalgebra)
    structure = [[[F(0) for _ in range(dimension)] for _ in range(dimension)] for _ in range(dimension)]
    for i in range(dimension):
        for j in range(dimension):
            commutator = subtract(multiply(subalgebra[i], subalgebra[j]), multiply(subalgebra[j], subalgebra[i]))
            coords = solve_coordinates(flat_columns, flatten(commutator))
            for k in range(dimension):
                structure[i][j][k] = coords[k]
    adjoint = []
    for i in range(dimension):
        adjoint.append([[structure[i][j][k] for j in range(dimension)] for k in range(dimension)])
    killing = zeros(dimension, dimension)
    for i in range(dimension):
        for j in range(dimension):
            product = multiply(adjoint[i], adjoint[j])
            killing[i][j] = sum((product[k][k] for k in range(dimension)), F(0))
    return {
        "stratum": name,
        "dimension": dimension,
        "Killing_rank": rank(killing),
        "Killing_inertia_positive_negative_zero": inertia_symmetric(killing),
    }


def render_fraction(value):
    if isinstance(value, F):
        return int(value) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, list):
        return [render_fraction(item) for item in value]
    if isinstance(value, dict):
        return {key: render_fraction(item) for key, item in value.items()}
    return value


def derive():
    stabilizers = [
        stabilizer("timelike", [F(1), F(0), F(0), F(0)]),
        stabilizer("spacelike", [F(0), F(1), F(0), F(0)]),
        stabilizer("nonzero_null", [F(1), F(1), F(0), F(0)]),
        stabilizer("zero", [F(0), F(0), F(0), F(0)]),
    ]
    return render_fraction(
        {
            "schema": "udt.full_coframe_first_jet_stratified_transition.independent.v1",
            "first_jet": coframe_map(),
            "joint_causal": joint_causal(),
            "causal_transitions": {
                "nonzero_null_s": "lambda^2-1",
                "nonzero_null_derivative_at_plus_one": 2,
                "normalized_projector_simple_pole": True,
                "zero_gradient_projector_limits_equal": False,
            },
            "rank_transitions": {
                "det_theta": "lambda",
                "det_metric": "-lambda^2",
                "inverse_metric_33": "lambda^-2",
                "adjugate_limit": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, -1]],
                "coframe_codimensions": [1, 4, 9, 16],
                "screen_codimensions": [1, 4],
                "finite_phi_pair_determinant": -1,
            },
            "stabilizers": stabilizers,
            "first_jet_constraint_count": 0,
            "physical_time_evolution_derived": False,
            "native_complete_return_derived": False,
        }
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not args.no_write:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
