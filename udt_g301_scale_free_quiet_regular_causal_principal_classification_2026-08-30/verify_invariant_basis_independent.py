#!/usr/bin/env python3
"""Independent exact Lorentz-intertwiner census for the load-bearing G301 basis."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 4
ETA = (-1, 1, 1, 1)
BIVECTORS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
BIV_INDEX = {pair: i for i, pair in enumerate(BIVECTORS)}
S2_POSITIONS = tuple((i, j) for i in range(N) for j in range(i, N))
M_POSITIONS = tuple(
    (i, j)
    for i in range(len(BIVECTORS))
    for j in range(i, len(BIVECTORS))
    if (i, j) != (0, 5)
)


def zero4():
    return [[[[0 for _ in range(N)] for _ in range(N)] for _ in range(N)] for _ in range(N)]


def canonical_pair(a, b):
    if a == b:
        return None, 0
    if a < b:
        return BIV_INDEX[(a, b)], 1
    return BIV_INDEX[(b, a)], -1


def tensor_from_bivector_matrix(matrix):
    tensor = zero4()
    for a in range(N):
        for b in range(N):
            left, sl = canonical_pair(a, b)
            if sl == 0:
                continue
            for c in range(N):
                for d in range(N):
                    right, sr = canonical_pair(c, d)
                    if sr:
                        tensor[a][b][c][d] = sl * sr * matrix[left][right]
    return tensor


def algebraic_curvature_basis():
    basis = []
    for i, j in M_POSITIONS:
        matrix = [[0 for _ in BIVECTORS] for _ in BIVECTORS]
        matrix[i][j] = 1
        matrix[j][i] = 1
        if i == j:
            matrix[i][j] = 1
        if (i, j) == (1, 4):
            matrix[0][5] = matrix[5][0] = 1
        if (i, j) == (2, 3):
            matrix[0][5] = matrix[5][0] = -1
        basis.append(tensor_from_bivector_matrix(matrix))
    assert len(basis) == 20
    return basis


def curvature_coordinates(tensor):
    values = []
    for i, j in M_POSITIONS:
        a, b = BIVECTORS[i]
        c, d = BIVECTORS[j]
        values.append(tensor[a][b][c][d])
    return values


def assert_algebraic(tensor):
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    assert tensor[a][b][c][d] == -tensor[b][a][c][d]
                    assert tensor[a][b][c][d] == -tensor[a][b][d][c]
                    assert tensor[a][b][c][d] == tensor[c][d][a][b]
                    assert (
                        tensor[a][b][c][d]
                        + tensor[a][c][d][b]
                        + tensor[a][d][b][c]
                        == 0
                    )


def s2_basis():
    basis = []
    for i, j in S2_POSITIONS:
        tensor = [[0 for _ in range(N)] for _ in range(N)]
        tensor[i][j] = tensor[j][i] = 1
        basis.append(tensor)
    return basis


def s2_coordinates(tensor):
    return [tensor[i][j] for i, j in S2_POSITIONS]


def lorentz_generators():
    generators = []
    for i in range(1, N):
        boost = [[0 for _ in range(N)] for _ in range(N)]
        boost[0][i] = 1
        boost[i][0] = 1
        generators.append(boost)
    for i in range(1, N):
        for j in range(i + 1, N):
            rotation = [[0 for _ in range(N)] for _ in range(N)]
            rotation[i][j] = 1
            rotation[j][i] = -1
            generators.append(rotation)
    assert len(generators) == 6
    for x in generators:
        for a in range(N):
            for b in range(N):
                lhs = sum(x[p][a] * (ETA[p] if p == b else 0) for p in range(N))
                lhs += ETA[a] * x[a][b]
                assert lhs == 0
    return generators


def act_covariant2(generator, tensor):
    out = [[0 for _ in range(N)] for _ in range(N)]
    for a in range(N):
        for b in range(N):
            out[a][b] = -sum(generator[p][a] * tensor[p][b] for p in range(N))
            out[a][b] -= sum(generator[p][b] * tensor[a][p] for p in range(N))
    return out


def act_curvature(generator, tensor):
    out = zero4()
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    value = -sum(generator[p][a] * tensor[p][b][c][d] for p in range(N))
                    value -= sum(generator[p][b] * tensor[a][p][c][d] for p in range(N))
                    value -= sum(generator[p][c] * tensor[a][b][p][d] for p in range(N))
                    value -= sum(generator[p][d] * tensor[a][b][c][p] for p in range(N))
                    out[a][b][c][d] = value
    return out


def representation_matrix(basis, act, coordinates, generator):
    columns = [coordinates(act(generator, tensor)) for tensor in basis]
    return [[columns[j][i] for j in range(len(columns))] for i in range(len(columns[0]))]


def linear_combination_curvature(values, basis):
    out = zero4()
    for coefficient, tensor in zip(values, basis):
        for a in range(N):
            for b in range(N):
                for c in range(N):
                    for d in range(N):
                        out[a][b][c][d] += coefficient * tensor[a][b][c][d]
    return out


def same_curvature(left, right):
    return all(
        left[a][b][c][d] == right[a][b][c][d]
        for a in range(N)
        for b in range(N)
        for c in range(N)
        for d in range(N)
    )


def ricci_tensor(curvature):
    ricci = [[0 for _ in range(N)] for _ in range(N)]
    for b in range(N):
        for d in range(N):
            ricci[b][d] = sum(ETA[a] * curvature[a][b][a][d] for a in range(N))
    return ricci


def scalar_times_metric(curvature):
    ricci = ricci_tensor(curvature)
    scalar = sum(ETA[a] * ricci[a][a] for a in range(N))
    tensor = [[0 for _ in range(N)] for _ in range(N)]
    for a in range(N):
        tensor[a][a] = scalar * ETA[a]
    return tensor


def intertwiner_vector(curvature_basis, mapping):
    # Unknown ordering is output-coordinate-major, then input-coordinate.
    columns = [s2_coordinates(mapping(tensor)) for tensor in curvature_basis]
    return [columns[j][i] for i in range(10) for j in range(20)]


def equivariance_rows(rep_s2, rep_curvature):
    rows = []
    for i in range(10):
        for j in range(20):
            row = [0 for _ in range(200)]
            for p in range(10):
                row[p * 20 + j] += rep_s2[i][p]
            for q in range(20):
                row[i * 20 + q] -= rep_curvature[q][j]
            rows.append(row)
    return rows


def modular_rank(rows, prime):
    matrix = [[value % prime for value in row] for row in rows if any(value % prime for value in row)]
    pivot_row = 0
    columns = len(matrix[0])
    for column in range(columns):
        selected = next((r for r in range(pivot_row, len(matrix)) if matrix[r][column]), None)
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], prime - 2, prime)
        matrix[pivot_row] = [(x * inverse) % prime for x in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r == pivot_row or matrix[r][column] == 0:
                continue
            factor = matrix[r][column]
            matrix[r] = [
                (matrix[r][c] - factor * matrix[pivot_row][c]) % prime
                for c in range(columns)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def dot(row, vector):
    return sum(a * b for a, b in zip(row, vector))


def main():
    curvature_basis = algebraic_curvature_basis()
    symmetric_basis = s2_basis()
    generators = lorentz_generators()
    assertions = 0

    for tensor in curvature_basis:
        assert_algebraic(tensor)
        assertions += N ** 4 * 4

    all_rows = []
    for generator in generators:
        rep_k = representation_matrix(
            curvature_basis, act_curvature, curvature_coordinates, generator
        )
        rep_s = representation_matrix(symmetric_basis, act_covariant2, s2_coordinates, generator)
        for column, tensor in enumerate(curvature_basis):
            rebuilt = linear_combination_curvature(
                [rep_k[row][column] for row in range(20)], curvature_basis
            )
            assert same_curvature(rebuilt, act_curvature(generator, tensor))
            assertions += N ** 4
        all_rows.extend(equivariance_rows(rep_s, rep_k))

    ricci_map = intertwiner_vector(curvature_basis, ricci_tensor)
    scalar_metric_map = intertwiner_vector(curvature_basis, scalar_times_metric)
    assert any(ricci_map)
    assert any(scalar_metric_map)
    independent = any(
        ricci_map[i] * scalar_metric_map[j] != ricci_map[j] * scalar_metric_map[i]
        for i in range(200)
        for j in range(i + 1, 200)
    )
    assert independent
    assertions += 3
    for row in all_rows:
        assert dot(row, ricci_map) == 0
        assert dot(row, scalar_metric_map) == 0
        assertions += 2

    ranks = {prime: modular_rank(all_rows, prime) for prime in (1000003, 1000033)}
    assert set(ranks.values()) == {198}
    assertions += len(ranks)
    # Modular rank 198 is a lower bound on rational rank. Two exact independent null vectors give
    # rational nullity at least two, hence rank at most 198. Therefore rational rank is exactly 198.

    result = {
        "verdict": "INDEPENDENT_FULL_SPACE_BASIS_CERTIFIED",
        "algebraic_curvature_dimension": 20,
        "symmetric_two_tensor_dimension": 10,
        "lorentz_generators": 6,
        "intertwiner_unknowns": 200,
        "equivariance_rows": len(all_rows),
        "modular_ranks": {str(key): value for key, value in ranks.items()},
        "rational_rank": 198,
        "rational_nullity": 2,
        "exact_null_vectors": ["RICCI", "SCALAR_TIMES_METRIC"],
        "exact_null_vectors_independent": independent,
        "production_imported": False,
        "assertions": assertions,
    }
    (HERE / "INVARIANT_BASIS_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
