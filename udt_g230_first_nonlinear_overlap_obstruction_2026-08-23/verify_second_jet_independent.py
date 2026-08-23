#!/usr/bin/env python3
"""Independent G230 replay using full 21-slot curvature and modular ranks.

This implementation does not import the production derivation or SymPy.  It
keeps all symmetric 6x6 bivector slots, imposes algebraic Bianchi explicitly,
and computes ranks over two finite fields.  Exact Fraction arithmetic checks
the nonlinear witness and commutator sign.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ETA = (-1, 1, 1, 1)
BIVECTORS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_INDEX = {pair: i for i, pair in enumerate(BIVECTORS)}
Q_SLOTS = tuple((i, j) for i in range(6) for j in range(i, 6))
Q_INDEX = {slot: i for i, slot in enumerate(Q_SLOTS)}
PAIRS = tuple(itertools.combinations_with_replacement(range(4), 2))
QUADS = tuple(itertools.combinations_with_replacement(range(4), 4))
QUINTS = tuple(itertools.combinations_with_replacement(range(4), 5))
L_COLUMNS = tuple((ab, q) for ab in PAIRS for q in QUADS)
G_COLUMNS = tuple((a, q) for a in range(4) for q in QUINTS)
E_ROWS = tuple((f, e, q) for f in range(4) for e in range(4) for q in Q_SLOTS)
D_ROWS = tuple((e, q) for e in range(4) for q in Q_SLOTS)
L_INDEX = {item: i for i, item in enumerate(L_COLUMNS)}
G_INDEX = {item: i for i, item in enumerate(G_COLUMNS)}
E_INDEX = {item: i for i, item in enumerate(E_ROWS)}
D_INDEX = {item: i for i, item in enumerate(D_ROWS)}

assert len(Q_SLOTS) == 21
assert len(L_COLUMNS) == 350
assert len(G_COLUMNS) == 224
assert len(E_ROWS) == 336
assert len(D_ROWS) == 84


def add(row: dict[int, int], column: int, value: int) -> None:
    if value:
        row[column] = row.get(column, 0) + value
        if row[column] == 0:
            del row[column]


def pair_locator(a: int, b: int) -> tuple[int, int]:
    if a == b:
        return 0, -1
    if a < b:
        return 1, PAIR_INDEX[(a, b)]
    return -1, PAIR_INDEX[(b, a)]


def curvature_locator(a: int, b: int, c: int, d: int) -> tuple[int, int]:
    s1, i = pair_locator(a, b)
    s2, j = pair_locator(c, d)
    if not s1 or not s2:
        return 0, -1
    return s1 * s2, Q_INDEX[tuple(sorted((i, j)))]


def build_c4_twice() -> list[dict[int, int]]:
    rows: list[dict[int, int]] = []
    for f, e, (left, right) in E_ROWS:
        a, b = BIVECTORS[left]
        c, d = BIVECTORS[right]
        row: dict[int, int] = {}
        add(row, L_INDEX[(tuple(sorted((a, d))), tuple(sorted((b, c, e, f))))], 1)
        add(row, L_INDEX[(tuple(sorted((b, c))), tuple(sorted((a, d, e, f))))], 1)
        add(row, L_INDEX[(tuple(sorted((b, d))), tuple(sorted((a, c, e, f))))], -1)
        add(row, L_INDEX[(tuple(sorted((a, c))), tuple(sorted((b, d, e, f))))], -1)
        rows.append(row)
    return rows


def build_algebraic_bianchi() -> list[dict[int, int]]:
    rows: list[dict[int, int]] = []
    q05 = Q_INDEX[(0, 5)]
    q14 = Q_INDEX[(1, 4)]
    q23 = Q_INDEX[(2, 3)]
    for f in range(4):
        for e in range(4):
            row: dict[int, int] = {}
            add(row, E_INDEX[(f, e, Q_SLOTS[q05])], 1)
            add(row, E_INDEX[(f, e, Q_SLOTS[q14])], -1)
            add(row, E_INDEX[(f, e, Q_SLOTS[q23])], 1)
            rows.append(row)
    return rows


def add_curvature_term(
    row: dict[int, int], f: int, derivative: int, a: int, b: int, c: int, d: int
) -> None:
    sign, slot = curvature_locator(a, b, c, d)
    if sign:
        add(row, E_INDEX[(f, derivative, Q_SLOTS[slot])], sign)


def build_differentiated_bianchi() -> list[dict[int, int]]:
    rows: list[dict[int, int]] = []
    for f in range(4):
        for e, a, b in itertools.combinations(range(4), 3):
            for c, d in BIVECTORS:
                row: dict[int, int] = {}
                add_curvature_term(row, f, e, a, b, c, d)
                add_curvature_term(row, f, a, b, e, c, d)
                add_curvature_term(row, f, b, e, a, c, d)
                rows.append(row)
    return rows


def build_first_derivative_constraints() -> list[dict[int, int]]:
    rows: list[dict[int, int]] = []
    q05 = Q_INDEX[(0, 5)]
    q14 = Q_INDEX[(1, 4)]
    q23 = Q_INDEX[(2, 3)]
    for e in range(4):
        row: dict[int, int] = {}
        add(row, D_INDEX[(e, Q_SLOTS[q05])], 1)
        add(row, D_INDEX[(e, Q_SLOTS[q14])], -1)
        add(row, D_INDEX[(e, Q_SLOTS[q23])], 1)
        rows.append(row)
    for e, a, b in itertools.combinations(range(4), 3):
        for c, d in BIVECTORS:
            row = {}
            for derivative, x, y in ((e, a, b), (a, b, e), (b, e, a)):
                sign, slot = curvature_locator(x, y, c, d)
                if sign:
                    add(row, D_INDEX[(derivative, Q_SLOTS[slot])], sign)
            rows.append(row)
    return rows


def build_commutator() -> list[dict[int, int]]:
    rows: list[dict[int, int]] = []
    for f, e in itertools.combinations(range(4), 2):
        for q in Q_SLOTS:
            row: dict[int, int] = {}
            add(row, E_INDEX[(f, e, q)], 1)
            add(row, E_INDEX[(e, f, q)], -1)
            rows.append(row)
    return rows


def build_gauge() -> list[dict[int, int]]:
    rows: list[dict[int, int]] = []
    for (i, j), (c, d, e, f) in L_COLUMNS:
        row: dict[int, int] = {}
        add(row, G_INDEX[(j, tuple(sorted((i, c, d, e, f))))], ETA[j])
        add(row, G_INDEX[(i, tuple(sorted((j, c, d, e, f))))], ETA[i])
        rows.append(row)
    return rows


def build_normal() -> list[dict[int, int]]:
    rows: list[dict[int, int]] = []
    for i in range(4):
        for quint in QUINTS:
            row: dict[int, int] = {}
            for j, k, l, m, n in sorted(set(itertools.permutations(quint))):
                add(
                    row,
                    L_INDEX[(tuple(sorted((i, j))), tuple(sorted((k, l, m, n))))],
                    1,
                )
            rows.append(row)
    return rows


def rank_mod(rows: list[dict[int, int]], ncols: int, prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for original in rows:
        row = {c: v % prime for c, v in original.items() if v % prime}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                inverse = pow(row[pivot], prime - 2, prime)
                row = {c: (v * inverse) % prime for c, v in row.items() if v % prime}
                pivots[pivot] = row
                break
            factor = row[pivot]
            base = pivots[pivot]
            for c, value in base.items():
                updated = (row.get(c, 0) - factor * value) % prime
                if updated:
                    row[c] = updated
                elif c in row:
                    del row[c]
    return len(pivots)


def multiply_rows(
    left: list[dict[int, int]], right: list[dict[int, int]]
) -> list[dict[int, int]]:
    result: list[dict[int, int]] = []
    for row in left:
        out: dict[int, int] = {}
        for middle, coefficient in row.items():
            for column, value in right[middle].items():
                add(out, column, coefficient * value)
        result.append(out)
    return result


def sparse_hash(rows: list[dict[int, int]]) -> str:
    text = "\n".join(
        ",".join(f"{column}:{row[column]}" for column in sorted(row)) for row in rows
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def q_from_g229_coefficient_one() -> list[F]:
    # G229 independent coordinate 1 is symmetric bivector slot (01,02).
    q = [F(0)] * 21
    q[Q_INDEX[(0, 1)]] = F(1)
    return q


def r_value(q: list[F], a: int, b: int, c: int, d: int) -> F:
    sign, slot = curvature_locator(a, b, c, d)
    return F(sign) * q[slot] if sign else F(0)


def h_value(q: list[F], a: int, b: int, c: int, d: int) -> F:
    return -F(1, 3) * (r_value(q, a, c, b, d) + r_value(q, a, d, b, c))


def dgamma(q: list[F], derivative: int, upper: int, b: int, c: int) -> F:
    return F(ETA[upper], 2) * (
        h_value(q, upper, c, b, derivative)
        + h_value(q, upper, b, c, derivative)
        - h_value(q, b, c, upper, derivative)
    )


def split_q_component(q: list[F], f: int, e: int, a: int, b: int, c: int, d: int) -> tuple[F, F]:
    product = F(0)
    for p in range(4):
        product += ETA[p] * (
            dgamma(q, e, p, b, c) * dgamma(q, f, p, a, d)
            + dgamma(q, f, p, b, c) * dgamma(q, e, p, a, d)
            - dgamma(q, e, p, b, d) * dgamma(q, f, p, a, c)
            - dgamma(q, f, p, b, d) * dgamma(q, e, p, a, c)
        )
    covariant = F(0)
    for p in range(4):
        covariant -= dgamma(q, f, p, e, a) * r_value(q, p, b, c, d)
        covariant -= dgamma(q, f, p, e, b) * r_value(q, a, p, c, d)
        covariant -= dgamma(q, f, p, e, c) * r_value(q, a, b, p, d)
        covariant -= dgamma(q, f, p, e, d) * r_value(q, a, b, c, p)
    return product, covariant


def q_second_vector(q: list[F], mode: str = "full") -> list[F]:
    values: list[F] = []
    for f, e, (left, right) in E_ROWS:
        a, b = BIVECTORS[left]
        c, d = BIVECTORS[right]
        product, covariant = split_q_component(q, f, e, a, b, c, d)
        if mode == "product":
            values.append(product)
        elif mode == "covariant":
            values.append(covariant)
        else:
            values.append(product + covariant)
    return values


def commutator_rhs(q: list[F]) -> list[F]:
    values: list[F] = []
    for f, e in itertools.combinations(range(4), 2):
        for left, right in Q_SLOTS:
            a, b = BIVECTORS[left]
            c, d = BIVECTORS[right]
            value = F(0)
            for p in range(4):
                value -= ETA[p] * r_value(q, p, a, f, e) * r_value(q, p, b, c, d)
                value -= ETA[p] * r_value(q, p, b, f, e) * r_value(q, a, p, c, d)
                value -= ETA[p] * r_value(q, p, c, f, e) * r_value(q, a, b, p, d)
                value -= ETA[p] * r_value(q, p, d, f, e) * r_value(q, a, b, c, p)
            values.append(value)
    return values


def matvec(rows: list[dict[int, int]], vector: list[F]) -> list[F]:
    return [sum((F(value) * vector[column] for column, value in row.items()), F(0)) for row in rows]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    c4 = build_c4_twice()
    algebraic = build_algebraic_bianchi()
    db2 = build_differentiated_bianchi()
    comm = build_commutator()
    constraints = algebraic + db2 + comm
    gauge = build_gauge()
    normal = build_normal()
    primes = (1_000_000_007, 1_000_000_009)

    ranks = {
        str(prime): {
            "c4": rank_mod(c4, 350, prime),
            "algebraic_bianchi": rank_mod(algebraic, 336, prime),
            "differentiated_bianchi": rank_mod(db2, 336, prime),
            "commutator": rank_mod(comm, 336, prime),
            "combined_constraints": rank_mod(constraints, 336, prime),
            "quintic_gauge": rank_mod(gauge, 224, prime),
            "normal4": rank_mod(normal, 350, prime),
            "normal4_on_gauge": rank_mod(multiply_rows(normal, gauge), 224, prime),
            "stacked_normal4_c4": rank_mod(normal + c4, 350, prime),
        }
        for prime in primes
    }
    expected = {
        "c4": 126,
        "algebraic_bianchi": 16,
        "differentiated_bianchi": 96,
        "commutator": 126,
        "combined_constraints": 210,
        "quintic_gauge": 224,
        "normal4": 224,
        "normal4_on_gauge": 224,
        "stacked_normal4_c4": 350,
    }

    constraint_on_c4 = multiply_rows(constraints, c4)
    c4_on_gauge = multiply_rows(c4, gauge)
    q = q_from_g229_coefficient_one()
    second = q_second_vector(q)
    rhs = commutator_rhs(q)
    full_residual = [a - b for a, b in zip(matvec(comm, second), rhs)]
    db_residual = matvec(db2, second)
    alg_residual = matvec(algebraic, second)
    zero_fails = any(value for value in rhs)
    g227_residuals = [
        r_value(q, a, b, c, d) + r_value(q, a, c, d, b) + r_value(q, a, d, b, c)
        for a, b, c, d in itertools.product(range(4), repeat=4)
    ]
    first_constraints = build_first_derivative_constraints()
    zero_d_residual = matvec(first_constraints, [F(0)] * 84)
    zero_e_db_residual = matvec(db2, [F(0)] * 336)
    zero_e_comm_residual = [F(0) - value for value in rhs]

    checks = {
        "two_prime_ranks_match": all(value == expected for value in ranks.values()),
        "constraints_annihilate_c4_exactly": all(not row for row in constraint_on_c4),
        "c4_annihilates_quintic_gauge_exactly": all(not row for row in c4_on_gauge),
        "direct_fraction_witness_algebraic_bianchi": not any(alg_residual),
        "direct_fraction_witness_differentiated_bianchi": not any(db_residual),
        "direct_fraction_witness_commutator_sign": not any(full_residual),
        "direct_fraction_witness_rhs_nonzero": zero_fails,
        "g227_witness_explicit_algebraic_bianchi_pass": not any(g227_residuals),
        "g228_zero_D_explicit_constraints_pass": not any(zero_d_residual),
        "zero_E_explicit_differentiated_bianchi_pass": not any(zero_e_db_residual),
        "zero_E_explicit_commutator_failure": any(zero_e_comm_residual),
    }
    result = {
        "landing": "INDEPENDENT_FULL_21_SLOT_TWO_PRIME_AND_FRACTION_REPLAY_PASS"
        if all(checks.values())
        else "INDEPENDENT_REPLAY_FAILURE",
        "representation": "full 21 symmetric bivector slots; algebraic Bianchi imposed explicitly",
        "ranks_by_prime": ranks,
        "expected_ranks": expected,
        "checks": checks,
        "witness": {
            "q_slot": "(01,02)=1",
            "commutator_rhs_nonzero_count": sum(bool(value) for value in rhs),
            "first_nonzero": str(next(value for value in rhs if value)),
            "product_only_commutator_residual_nonzero": any(
                a - b for a, b in zip(matvec(comm, q_second_vector(q, "product")), rhs)
            ),
            "product_only_differentiated_bianchi_residual_nonzero": any(
                matvec(db2, q_second_vector(q, "product"))
            ),
            "covariantization_only_commutator_residual_nonzero": any(
                a - b for a, b in zip(matvec(comm, q_second_vector(q, "covariant")), rhs)
            ),
            "covariantization_only_differentiated_bianchi_residual_nonzero": any(
                matvec(db2, q_second_vector(q, "covariant"))
            ),
            "g227_algebraic_bianchi_nonzero": sum(bool(value) for value in g227_residuals),
            "g228_zero_D_constraint_nonzero": sum(bool(value) for value in zero_d_residual),
            "g230_zero_E_differentiated_bianchi_nonzero": sum(
                bool(value) for value in zero_e_db_residual
            ),
            "g230_zero_E_commutator_residual_nonzero": sum(
                bool(value) for value in zero_e_comm_residual
            ),
        },
        "hashes": {
            "c4_full21_sparse": sparse_hash(c4),
            "constraints_full21_sparse": sparse_hash(constraints),
            "gauge_sparse": sparse_hash(gauge),
            "normal_sparse": sparse_hash(normal),
        },
    }
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if not args.no_write:
        (ROOT / "independent_results.json").write_text(text + "\n", encoding="utf-8")
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
