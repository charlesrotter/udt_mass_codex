#!/usr/bin/env python3
"""Independent standard-library G231 exterior-symbol replay."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ETA = (-1, 1, 1, 1)
PAIRS = tuple(itertools.combinations(range(4), 2))
PAIR_POS = {pair: i for i, pair in enumerate(PAIRS)}
TRIPLES = tuple(itertools.combinations(range(4), 3))
TRIPLE_POS = {triple: i for i, triple in enumerate(TRIPLES)}
Q_SLOTS = tuple((i, j) for i in range(6) for j in range(i, 6))
Q_INDEX = {slot: i for i, slot in enumerate(Q_SLOTS)}
FULL_E_ROWS = tuple((f, e, q) for f in range(4) for e in range(4) for q in Q_SLOTS)
FULL_E_INDEX = {item: i for i, item in enumerate(FULL_E_ROWS)}


def pair_slot(a: int, b: int):
    if a == b:
        return None
    return (PAIR_POS[(a, b)], 1) if a < b else (PAIR_POS[(b, a)], -1)


def wedge_sign(indices):
    if len(set(indices)) != len(indices):
        return 0, None
    inv = sum(indices[i] > indices[j] for i in range(len(indices)) for j in range(i + 1, len(indices)))
    return (-1 if inv % 2 else 1), tuple(sorted(indices))


def add(row: dict[int, int], col: int, value: int) -> None:
    if value:
        row[col] = row.get(col, 0) + value
        if row[col] == 0:
            del row[col]


def rank_mod(rows: list[dict[int, int]], ncols: int, prime: int) -> int:
    work = [{c: v % prime for c, v in row.items() if v % prime} for row in rows]
    pivot_row = 0
    for col in range(ncols):
        pivot = next((r for r in range(pivot_row, len(work)) if work[r].get(col, 0)), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][col], prime - 2, prime)
        work[pivot_row] = {c: (v * inverse) % prime for c, v in work[pivot_row].items()}
        for r in range(len(work)):
            if r == pivot_row:
                continue
            factor = work[r].get(col, 0)
            if not factor:
                continue
            for c, v in work[pivot_row].items():
                new = (work[r].get(c, 0) - factor * v) % prime
                if new:
                    work[r][c] = new
                elif c in work[r]:
                    del work[r][c]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def b1_rows() -> list[dict[int, int]]:
    rows = [dict() for _ in range(16)]
    for p, (m, n) in enumerate(PAIRS):
        for q, (c, d) in enumerate(PAIRS):
            col = 6 * p + q
            for a in range(4):
                for b in range(4):
                    slot = pair_slot(a, b)
                    if slot is None or slot[0] != p:
                        continue
                    sign, triple = wedge_sign((c, d, b))
                    if sign:
                        add(rows[4 * a + TRIPLE_POS[triple]], col, ETA[a] * slot[1] * sign)
    return rows


def explicit_curvature_basis() -> list[list[int]]:
    symmetric = [(i, j) for i in range(6) for j in range(i, 6)]
    parameters = [pair for pair in symmetric if pair != (0, 5)]
    columns = []
    for selected in parameters:
        q = [[0 for _ in range(6)] for _ in range(6)]
        i, j = selected
        q[i][j] = 1
        q[j][i] = 1
        if selected == (1, 4):
            q[0][5] += 1
            q[5][0] += 1
        if selected == (2, 3):
            q[0][5] -= 1
            q[5][0] -= 1
        columns.append([q[p][r] for p in range(6) for r in range(6)])
    return columns


def mat_vec(rows: list[dict[int, int]], vector: list[int]) -> list[int]:
    return [sum(value * vector[col] for col, value in row.items()) for row in rows]


def b2_rows(basis: list[list[int]]) -> list[dict[int, int]]:
    rows = [dict() for _ in range(24)]
    for e in range(4):
        for j, column in enumerate(basis):
            source = 20 * e + j
            for raw, coefficient in enumerate(column):
                if not coefficient:
                    continue
                p, q = divmod(raw, 6)
                c, d = PAIRS[q]
                sign, triple = wedge_sign((e, c, d))
                if sign:
                    add(rows[4 * p + TRIPLE_POS[triple]], source, sign * coefficient)
    return rows


def db_rows(b2: list[dict[int, int]]) -> list[dict[int, int]]:
    rows = [dict() for _ in range(96)]
    for f in range(4):
        for r, base in enumerate(b2):
            target = rows[24 * f + r]
            for inner, value in base.items():
                e, j = divmod(inner, 20)
                add(target, (4 * f + e) * 20 + j, value)
    return rows


def comm_rows() -> list[dict[int, int]]:
    rows = []
    for f, e in PAIRS:
        for j in range(20):
            row = {}
            add(row, (4 * f + e) * 20 + j, 1)
            add(row, (4 * e + f) * 20 + j, -1)
            rows.append(row)
    return rows


def component(vector, a, b, c, d):
    left = pair_slot(a, b)
    right = pair_slot(c, d)
    if left is None or right is None:
        return Fraction(0)
    return Fraction(left[1] * right[1]) * vector[6 * left[0] + right[0]]


def ricci_rhs_raw(vector, f, e):
    result = [Fraction(0) for _ in range(36)]
    for p1, (a, b) in enumerate(PAIRS):
        for p2, (c, d) in enumerate(PAIRS):
            value = Fraction(0)
            for p in range(4):
                value -= ETA[p] * component(vector, p, a, f, e) * component(vector, p, b, c, d)
                value -= ETA[p] * component(vector, p, b, f, e) * component(vector, a, p, c, d)
                value -= ETA[p] * component(vector, p, c, f, e) * component(vector, a, b, p, d)
                value -= ETA[p] * component(vector, p, d, f, e) * component(vector, a, b, c, p)
            result[6 * p1 + p2] = value
    return result


def witness_vector():
    vector = [Fraction(0) for _ in range(36)]
    p01, p02 = PAIR_POS[(0, 1)], PAIR_POS[(0, 2)]
    vector[6 * p01 + p02] = 1
    vector[6 * p02 + p01] = 1
    return vector


def constant_vector():
    vector = [Fraction(0) for _ in range(36)]
    metric = lambda i, j: ETA[i] if i == j else 0
    for p1, (a, b) in enumerate(PAIRS):
        for p2, (c, d) in enumerate(PAIRS):
            vector[6 * p1 + p2] = metric(a, c) * metric(b, d) - metric(a, d) * metric(b, c)
    return vector


def curvature_locator(a, b, c, d):
    left = pair_slot(a, b)
    right = pair_slot(c, d)
    if left is None or right is None:
        return 0, -1
    sign = left[1] * right[1]
    return sign, Q_INDEX[tuple(sorted((left[0], right[0])))]


def full_r_value(q, a, b, c, d):
    sign, slot = curvature_locator(a, b, c, d)
    return Fraction(sign) * q[slot] if sign else Fraction(0)


def full_h_value(q, a, b, c, d):
    return -Fraction(1, 3) * (
        full_r_value(q, a, c, b, d) + full_r_value(q, a, d, b, c)
    )


def direct_dgamma(q, derivative, upper, b, c):
    return Fraction(ETA[upper], 2) * (
        full_h_value(q, upper, c, b, derivative)
        + full_h_value(q, upper, b, c, derivative)
        - full_h_value(q, b, c, upper, derivative)
    )


def direct_second_component(q, f, e, a, b, c, d):
    product = Fraction(0)
    for p in range(4):
        product += ETA[p] * (
            direct_dgamma(q, e, p, b, c) * direct_dgamma(q, f, p, a, d)
            + direct_dgamma(q, f, p, b, c) * direct_dgamma(q, e, p, a, d)
            - direct_dgamma(q, e, p, b, d) * direct_dgamma(q, f, p, a, c)
            - direct_dgamma(q, f, p, b, d) * direct_dgamma(q, e, p, a, c)
        )
    covariant = Fraction(0)
    for p in range(4):
        covariant -= direct_dgamma(q, f, p, e, a) * full_r_value(q, p, b, c, d)
        covariant -= direct_dgamma(q, f, p, e, b) * full_r_value(q, a, p, c, d)
        covariant -= direct_dgamma(q, f, p, e, c) * full_r_value(q, a, b, p, d)
        covariant -= direct_dgamma(q, f, p, e, d) * full_r_value(q, a, b, c, p)
    return product + covariant


def direct_second_vector(q):
    return [
        direct_second_component(q, f, e, *PAIRS[left], *PAIRS[right])
        for f, e, (left, right) in FULL_E_ROWS
    ]


def full_db_rows():
    rows = []
    for f in range(4):
        for e, a, b in itertools.combinations(range(4), 3):
            for c, d in PAIRS:
                row = {}
                for derivative, x, y in ((e, a, b), (a, b, e), (b, e, a)):
                    sign, slot = curvature_locator(x, y, c, d)
                    if sign:
                        add(row, FULL_E_INDEX[(f, derivative, Q_SLOTS[slot])], sign)
                rows.append(row)
    return rows


def full_comm_rows():
    rows = []
    for f, e in PAIRS:
        for q in Q_SLOTS:
            row = {}
            add(row, FULL_E_INDEX[(f, e, q)], 1)
            add(row, FULL_E_INDEX[(e, f, q)], -1)
            rows.append(row)
    return rows


def direct_rhs(q):
    values = []
    for f, e in PAIRS:
        for left, right in Q_SLOTS:
            a, b = PAIRS[left]
            c, d = PAIRS[right]
            value = Fraction(0)
            for p in range(4):
                value -= ETA[p] * full_r_value(q, p, a, f, e) * full_r_value(q, p, b, c, d)
                value -= ETA[p] * full_r_value(q, p, b, f, e) * full_r_value(q, a, p, c, d)
                value -= ETA[p] * full_r_value(q, p, c, f, e) * full_r_value(q, a, b, p, d)
                value -= ETA[p] * full_r_value(q, p, d, f, e) * full_r_value(q, a, b, c, p)
            values.append(value)
    return values


def lorentz_generators():
    generators = []
    for a, b in PAIRS:
        matrix = [[Fraction(0) for _ in range(4)] for _ in range(4)]
        matrix[a][b] = Fraction(ETA[a])
        matrix[b][a] = Fraction(-ETA[b])
        generators.append(matrix)
    return generators


def vertical_action_raw(generator, tensor):
    values = [Fraction(0) for _ in range(36)]
    for raw, (ab, cd) in enumerate((x, y) for x in PAIRS for y in PAIRS):
        a, b = ab
        c, d = cd
        value = Fraction(0)
        for p in range(4):
            value += generator[p][a] * component(tensor, p, b, c, d)
            value += generator[p][b] * component(tensor, a, p, c, d)
            value += generator[p][c] * component(tensor, a, b, p, d)
            value += generator[p][d] * component(tensor, a, b, c, p)
        values[raw] = value
    return values


def explicit_frame_transform_derivative(generator, tensor):
    # Coefficient of epsilon in R(e_a+eps A^p_a e_p, ..., e_d+eps A^p_d e_p).
    values = [Fraction(0) for _ in range(36)]
    for raw, (ab, cd) in enumerate((x, y) for x in PAIRS for y in PAIRS):
        indices = list(ab + cd)
        coefficient = Fraction(0)
        for position in range(4):
            old = indices[position]
            for replacement in range(4):
                mutated = list(indices)
                mutated[position] = replacement
                coefficient += generator[replacement][old] * component(tensor, *mutated)
        values[raw] = coefficient
    return values


def derive() -> dict[str, object]:
    first = b1_rows()
    basis = explicit_curvature_basis()
    second = b2_rows(basis)
    third = db_rows(second)
    comm = comm_rows()
    combined = third + comm
    primes = (1000000007, 1000000009)
    ranks = {}
    for prime in primes:
        ranks[str(prime)] = {
            "algebraic_bianchi": rank_mod(first, 36, prime),
            "explicit_curvature_basis": rank_mod(
                [{j: basis[j][i] for j in range(20) if basis[j][i]} for i in range(36)], 20, prime
            ),
            "differential_bianchi": rank_mod(second, 80, prime),
            "differentiated_bianchi": rank_mod(third, 320, prime),
            "commutator": rank_mod(comm, 320, prime),
            "combined_second_prolongation": rank_mod(combined, 320, prime),
        }
    basis_in_kernel = all(not any(mat_vec(first, column)) for column in basis)
    witness = witness_vector()
    constant = constant_vector()
    witness_rhs = [value for f, e in PAIRS for value in ricci_rhs_raw(witness, f, e)]
    constant_rhs = [value for f, e in PAIRS for value in ricci_rhs_raw(constant, f, e)]
    direct_q = [Fraction(0) for _ in range(21)]
    direct_q[Q_INDEX[(0, 1)]] = Fraction(1)
    direct_second = direct_second_vector(direct_q)
    direct_db = mat_vec(full_db_rows(), direct_second)
    direct_comm = mat_vec(full_comm_rows(), direct_second)
    direct_comm_rhs = direct_rhs(direct_q)
    direct_sign_residual = [a - b for a, b in zip(direct_comm, direct_comm_rhs)]
    reversed_sign_residual = [a + b for a, b in zip(direct_comm, direct_comm_rhs)]
    generators = lorentz_generators()
    eta_skew = []
    for generator in generators:
        eta_skew.append(
            all(
                ETA[i] * generator[i][j] + generator[j][i] * ETA[j] == 0
                for i in range(4)
                for j in range(4)
            )
        )
    basis_vertical_preserved = all(
        not any(mat_vec(first, vertical_action_raw(generator, column)))
        for generator in generators
        for column in basis
    )
    constant_vertical_zero = all(
        not any(vertical_action_raw(generator, constant)) for generator in generators
    )
    witness_vertical_counts = [
        sum(bool(value) for value in vertical_action_raw(generator, witness))
        for generator in generators
    ]
    explicit_transform_matches = all(
        vertical_action_raw(generator, witness)
        == explicit_frame_transform_derivative(generator, witness)
        for generator in generators
    )
    expected = {
        "algebraic_bianchi": 16,
        "explicit_curvature_basis": 20,
        "differential_bianchi": 20,
        "differentiated_bianchi": 80,
        "commutator": 120,
        "combined_second_prolongation": 194,
    }
    checks = {
        "two_prime_ranks_match": all(row == expected for row in ranks.values()),
        "explicit_20_basis_is_in_b1_kernel": basis_in_kernel,
        "witness_passes_algebraic_bianchi": not any(mat_vec(first, witness)),
        "witness_R_squared_is_nonzero": any(witness_rhs),
        "witness_first_nonzero_is_minus_one": next(v for v in witness_rhs if v) == -1,
        "constant_passes_algebraic_bianchi": not any(mat_vec(first, constant)),
        "constant_R_squared_is_zero": not any(constant_rhs),
        "direct_polynomial_metric_differentiated_Bianchi": not any(direct_db),
        "direct_polynomial_metric_Ricci_sign": not any(direct_sign_residual),
        "reversed_Ricci_sign_fails_direct_metric_witness": any(reversed_sign_residual),
        "all_six_generators_are_eta_skew": all(eta_skew),
        "vertical_action_preserves_full_20_basis_B1_kernel": basis_vertical_preserved,
        "vertical_action_annihilates_constant_curvature": constant_vertical_zero,
        "vertical_action_nonzero_on_offdiagonal_witness": all(
            count > 0 for count in witness_vertical_counts
        ),
        "vertical_action_matches_explicit_infinitesimal_frame_transform": explicit_transform_matches,
    }
    return {
        "landing": "INDEPENDENT_EXPLICIT_BIVECTOR_TWO_PRIME_AND_FRACTION_REPLAY_PASS",
        "representation": "explicit symmetric 6x6 bivector matrix with q05=q14-q23",
        "ranks_by_prime": ranks,
        "witness": {
            "description": "q_(01,02)=q_(02,01)=1",
            "commutator_nonzero_count": sum(bool(v) for v in witness_rhs),
            "first_nonzero": str(next(v for v in witness_rhs if v)),
        },
        "constant_curvature": {
            "commutator_nonzero_count": sum(bool(v) for v in constant_rhs),
            "vertical_action_nonzero_count": sum(
                sum(bool(value) for value in vertical_action_raw(generator, constant))
                for generator in generators
            ),
        },
        "direct_polynomial_metric_sign_anchor": {
            "differentiated_Bianchi_residual_nonzero_count": sum(bool(v) for v in direct_db),
            "correct_sign_residual_nonzero_count": sum(bool(v) for v in direct_sign_residual),
            "reversed_sign_residual_nonzero_count": sum(bool(v) for v in reversed_sign_residual),
        },
        "independent_vertical_action": {
            "eta_skew_generators": eta_skew,
            "witness_nonzero_counts": witness_vertical_counts,
            "basis_kernel_preserved": basis_vertical_preserved,
            "constant_annihilated": constant_vertical_zero,
            "explicit_transform_matches": explicit_transform_matches,
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if not args.no_write:
        (ROOT / "independent_results.json").write_text(text + "\n", encoding="utf-8")
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
