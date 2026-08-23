#!/usr/bin/env python3
"""Independent standard-library exact replay for G229.

This verifier does not import the production module and does not use SymPy.
It retains all 21 symmetric-bivector slots (84 slots for D) and imposes the
algebraic and differential Bianchi equations as independent constraint rows.
That representation is intentionally different from the production code's
20/80-slot reduced representation.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parent
SIGNS = (-1, 1, 1, 1)
BIVECTORS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_INDEX = {pair: i for i, pair in enumerate(BIVECTORS)}
FULL_SLOTS = tuple((i, j) for i in range(6) for j in range(i, 6))
SLOT_INDEX = {slot: i for i, slot in enumerate(FULL_SLOTS)}
PAIRS = tuple(itertools.combinations_with_replacement(range(4), 2))
TRIPLES = tuple(itertools.combinations_with_replacement(range(4), 3))
QUADS = tuple(itertools.combinations_with_replacement(range(4), 4))
H_COLS = tuple((ab, cd) for ab in PAIRS for cd in PAIRS)
K_COLS = tuple((ab, cde) for ab in PAIRS for cde in TRIPLES)
A_COLS = tuple((a, bcd) for a in range(4) for bcd in TRIPLES)
B_COLS = tuple((a, bcde) for a in range(4) for bcde in QUADS)
H_INDEX = {label: i for i, label in enumerate(H_COLS)}
K_INDEX = {label: i for i, label in enumerate(K_COLS)}
A_INDEX = {label: i for i, label in enumerate(A_COLS)}
B_INDEX = {label: i for i, label in enumerate(B_COLS)}


def zeros(rows: int, cols: int) -> list[list[F]]:
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(size: int) -> list[list[F]]:
    matrix = zeros(size, size)
    for i in range(size):
        matrix[i][i] = F(1)
    return matrix


def transpose(matrix: Sequence[Sequence[F]]) -> list[list[F]]:
    if not matrix:
        return []
    return [list(column) for column in zip(*matrix)]


def rref(matrix: Sequence[Sequence[F]]) -> tuple[list[list[F]], list[int]]:
    work = [list(map(F, row)) for row in matrix]
    if not work:
        return work, []
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    pivots: list[int] = []
    for column in range(cols):
        selected = next((r for r in range(pivot_row, rows) if work[r][column]), None)
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [value / pivot for value in work[pivot_row]]
        for r in range(rows):
            if r == pivot_row or not work[r][column]:
                continue
            coefficient = work[r][column]
            work[r] = [
                work[r][c] - coefficient * work[pivot_row][c]
                for c in range(cols)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, pivots


def rank(matrix: Sequence[Sequence[F]]) -> int:
    return len(rref(matrix)[1])


def nullspace_columns(matrix: Sequence[Sequence[F]]) -> list[list[F]]:
    reduced, pivots = rref(matrix)
    columns = len(matrix[0]) if matrix else 0
    free = [column for column in range(columns) if column not in pivots]
    basis: list[list[F]] = []
    for free_column in free:
        vector = [F(0)] * columns
        vector[free_column] = F(1)
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        basis.append(vector)
    return transpose(basis)


def matmul(left: Sequence[Sequence[F]], right: Sequence[Sequence[F]]) -> list[list[F]]:
    if not left:
        return []
    if not right:
        return [[] for _ in left]
    right_t = transpose(right)
    return [
        [sum((a * b for a, b in zip(row, column)), F(0)) for column in right_t]
        for row in left
    ]


def is_zero(matrix: Sequence[Sequence[F]]) -> bool:
    return all(not value for row in matrix for value in row)


def equal(left: Sequence[Sequence[F]], right: Sequence[Sequence[F]]) -> bool:
    return [list(row) for row in left] == [list(row) for row in right]


def matrix_hash(matrix: Sequence[Sequence[F]]) -> str:
    def render(value: F) -> str:
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"

    payload = "\n".join(",".join(render(value) for value in row) for row in matrix)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def oriented_pair(a: int, b: int) -> tuple[int, int]:
    if a == b:
        return 0, -1
    if a < b:
        return 1, PAIR_INDEX[(a, b)]
    return -1, PAIR_INDEX[(b, a)]


def full_component(vector: Sequence[F], a: int, b: int, c: int, d: int) -> F:
    sign1, i = oriented_pair(a, b)
    sign2, j = oriented_pair(c, d)
    if not sign1 or not sign2:
        return F(0)
    slot = (i, j) if i <= j else (j, i)
    return F(sign1 * sign2) * vector[SLOT_INDEX[slot]]


def h_entry(column: tuple[tuple[int, int], tuple[int, int]], a: int, b: int, c: int, d: int) -> int:
    return int(column == (tuple(sorted((a, b))), tuple(sorted((c, d)))))


def k_entry(column: tuple[tuple[int, int], tuple[int, int, int]], a: int, b: int, c: int, d: int, e: int) -> int:
    return int(column == (tuple(sorted((a, b))), tuple(sorted((c, d, e)))))


def c2_matrix(last_sign: int = -1) -> list[list[F]]:
    rows = zeros(21, 100)
    for row, (left, right) in enumerate(FULL_SLOTS):
        a, b = BIVECTORS[left]
        c, d = BIVECTORS[right]
        for column_index, column in enumerate(H_COLS):
            rows[row][column_index] = F(
                h_entry(column, a, d, b, c)
                + h_entry(column, b, c, a, d)
                - h_entry(column, b, d, a, c)
                + last_sign * h_entry(column, a, c, b, d),
                2,
            )
    return rows


def c3_matrix(last_sign: int = -1) -> list[list[F]]:
    rows = zeros(84, 200)
    for derivative in range(4):
        for slot_index, (left, right) in enumerate(FULL_SLOTS):
            row = derivative * 21 + slot_index
            a, b = BIVECTORS[left]
            c, d = BIVECTORS[right]
            for column_index, column in enumerate(K_COLS):
                rows[row][column_index] = F(
                    k_entry(column, a, d, b, c, derivative)
                    + k_entry(column, b, c, a, d, derivative)
                    - k_entry(column, b, d, a, c, derivative)
                    + last_sign * k_entry(column, a, c, b, d, derivative),
                    2,
                )
    return rows


def algebraic_bianchi() -> list[list[F]]:
    row = [F(0)] * 21
    row[SLOT_INDEX[(0, 5)]] = F(1)
    row[SLOT_INDEX[(1, 4)]] = F(-1)
    row[SLOT_INDEX[(2, 3)]] = F(1)
    return [row]


def full_d_constraints() -> list[list[F]]:
    rows = zeros(4, 84)
    algebraic = algebraic_bianchi()[0]
    for derivative in range(4):
        for slot, coefficient in enumerate(algebraic):
            rows[derivative][derivative * 21 + slot] = coefficient

    for e, a, b in itertools.combinations(range(4), 3):
        for c, d in BIVECTORS:
            row = [F(0)] * 84
            for derivative, x, y in ((e, a, b), (a, b, e), (b, e, a)):
                sign1, i = oriented_pair(x, y)
                sign2, j = oriented_pair(c, d)
                if not sign1 or not sign2:
                    continue
                slot = (i, j) if i <= j else (j, i)
                row[derivative * 21 + SLOT_INDEX[slot]] += F(sign1 * sign2)
            rows.append(row)
    return rows


def cubic_gauge() -> list[list[F]]:
    matrix = zeros(100, 80)
    for row, ((i, j), (c, d)) in enumerate(H_COLS):
        matrix[row][A_INDEX[(j, tuple(sorted((i, c, d))))]] += F(SIGNS[j])
        matrix[row][A_INDEX[(i, tuple(sorted((j, c, d))))]] += F(SIGNS[i])
    return matrix


def quartic_gauge() -> list[list[F]]:
    matrix = zeros(200, 140)
    for row, ((i, j), (c, d, e)) in enumerate(K_COLS):
        matrix[row][B_INDEX[(j, tuple(sorted((i, c, d, e))))]] += F(SIGNS[j])
        matrix[row][B_INDEX[(i, tuple(sorted((j, c, d, e))))]] += F(SIGNS[i])
    return matrix


def unique_permutations(values: Iterable[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(set(itertools.permutations(tuple(values)))))


def normal2_constraints() -> list[list[F]]:
    matrix = zeros(80, 100)
    row = 0
    for i in range(4):
        for triple in TRIPLES:
            for j, k, l in unique_permutations(triple):
                matrix[row][H_INDEX[(tuple(sorted((i, j))), tuple(sorted((k, l))))]] += F(1)
            row += 1
    return matrix


def normal3_constraints() -> list[list[F]]:
    matrix = zeros(140, 200)
    row = 0
    for i in range(4):
        for quad in QUADS:
            for j, k, l, m in unique_permutations(quad):
                matrix[row][K_INDEX[(tuple(sorted((i, j))), tuple(sorted((k, l, m))))]] += F(1)
            row += 1
    return matrix


def h_inverse(target_basis: Sequence[Sequence[F]]) -> list[list[F]]:
    matrix = zeros(100, len(target_basis[0]))
    for row, ((a, b), (c, d)) in enumerate(H_COLS):
        for basis_index, vector in enumerate(transpose(target_basis)):
            matrix[row][basis_index] = -F(1, 3) * (
                full_component(vector, a, c, b, d)
                + full_component(vector, a, d, b, c)
            )
    return matrix


def d_component(vector: Sequence[F], derivative: int, a: int, b: int, c: int, d: int) -> F:
    return full_component(vector[derivative * 21 : (derivative + 1) * 21], a, b, c, d)


def k_inverse(target_basis: Sequence[Sequence[F]]) -> list[list[F]]:
    columns = transpose(target_basis)
    matrix = zeros(200, len(columns))
    permutations = tuple(itertools.permutations(range(3)))
    for row, ((a, b), derivative_triple) in enumerate(K_COLS):
        labels = tuple(derivative_triple)
        for basis_index, vector in enumerate(columns):
            total = F(0)
            for permutation in permutations:
                c = labels[permutation[0]]
                d = labels[permutation[1]]
                e = labels[permutation[2]]
                total += d_component(vector, e, a, c, b, d)
            matrix[row][basis_index] = -F(1, 6) * total
    return matrix


def run() -> dict[str, object]:
    c2 = c2_matrix()
    c3 = c3_matrix()
    alg = algebraic_bianchi()
    d_constraints = full_d_constraints()
    alg_basis = nullspace_columns(alg)
    d_basis = nullspace_columns(d_constraints)
    gauge2 = cubic_gauge()
    gauge3 = quartic_gauge()
    normal2 = normal2_constraints()
    normal3 = normal3_constraints()
    normal2_basis = nullspace_columns(normal2)
    normal3_basis = nullspace_columns(normal3)
    hinv = h_inverse(alg_basis)
    kinv = k_inverse(d_basis)

    ranks = {
        "c2_full21": rank(c2),
        "algebraic_bianchi": rank(alg),
        "c3_full84": rank(c3),
        "combined_D_constraints": rank(d_constraints),
        "compatible_D_basis": rank(d_basis),
        "cubic_gauge": rank(gauge2),
        "quartic_gauge": rank(gauge3),
        "normal2_constraints": rank(normal2),
        "normal3_constraints": rank(normal3),
        "normal2_slice": rank(normal2_basis),
        "normal3_slice": rank(normal3_basis),
        "normal2_on_cubic_gauge": rank(matmul(normal2, gauge2)),
        "normal3_on_quartic_gauge": rank(matmul(normal3, gauge3)),
        "c2_on_normal2": rank(matmul(c2, normal2_basis)),
        "c3_on_normal3": rank(matmul(c3, normal3_basis)),
    }
    expected = {
        "c2_full21": 20,
        "algebraic_bianchi": 1,
        "c3_full84": 60,
        "combined_D_constraints": 24,
        "compatible_D_basis": 60,
        "cubic_gauge": 80,
        "quartic_gauge": 140,
        "normal2_constraints": 80,
        "normal3_constraints": 140,
        "normal2_slice": 20,
        "normal3_slice": 60,
        "normal2_on_cubic_gauge": 80,
        "normal3_on_quartic_gauge": 140,
        "c2_on_normal2": 20,
        "c3_on_normal3": 60,
    }
    checks = {
        "c2_obeys_algebraic_bianchi": is_zero(matmul(alg, c2)),
        "c3_obeys_all_24_independent_constraints": is_zero(matmul(d_constraints, c3)),
        "cubic_gauge_is_exact_kernel": is_zero(matmul(c2, gauge2)) and rank(gauge2) == 80,
        "quartic_gauge_is_exact_kernel": is_zero(matmul(c3, gauge3)) and rank(gauge3) == 140,
        "h_inverse_complete_basis": equal(matmul(c2, hinv), alg_basis),
        "k_inverse_complete_basis": equal(matmul(c3, kinv), d_basis),
        "h_inverse_normal": is_zero(matmul(normal2, hinv)),
        "k_inverse_normal": is_zero(matmul(normal3, kinv)),
    }
    hashes = {
        "c2_full21": matrix_hash(c2),
        "c3_full84": matrix_hash(c3),
        "combined_D_constraints": matrix_hash(d_constraints),
        "cubic_gauge": matrix_hash(gauge2),
        "quartic_gauge": matrix_hash(gauge3),
        "normal2_constraints": matrix_hash(normal2),
        "normal3_constraints": matrix_hash(normal3),
        "h_inverse_full_basis": matrix_hash(hinv),
        "k_inverse_full_basis": matrix_hash(kinv),
    }
    shared_hash_matches = {
        "cubic_gauge": hashes["cubic_gauge"] == "5b54383c66e5c743852db20fb29184e429a01393885feebbf5c4cf71624a190a",
        "quartic_gauge": hashes["quartic_gauge"] == "fd3ad00323c6f247b9c08bed894673b3330e8e7a8ce7c6594ad6b109cdcc2723",
        "normal2_constraints": hashes["normal2_constraints"] == "8f63ba17f81f4166082dae4c780fc3bf28180b7826389448358ee1cb34376df6",
        "normal3_constraints": hashes["normal3_constraints"] == "82697c076ea6f9995da2cea262b3a49ea17be4cc44db9f436f0669e13a6a1b83",
    }
    all_pass = ranks == expected and all(checks.values()) and all(shared_hash_matches.values())
    return {
        "landing": "INDEPENDENT_FULL_21_84_SLOT_REPLAY_PASS" if all_pass else "INDEPENDENT_REPLAY_FAILURE",
        "all_checks_pass": all_pass,
        "representation": (
            "standard-library Fraction; full 21 symmetric-bivector R slots and 84 D slots; "
            "Bianchi constraints imposed independently"
        ),
        "ranks": ranks,
        "expected_ranks": expected,
        "checks": checks,
        "matrix_sha256": hashes,
        "shared_matrix_hash_matches_production": shared_hash_matches,
        "scope": "independent exact finite-dimensional replay; no history/value generation",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = run()
    if not args.no_write:
        (ROOT / "independent_verification.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
