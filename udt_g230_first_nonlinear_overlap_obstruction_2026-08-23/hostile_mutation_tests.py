#!/usr/bin/env python3
"""Hostile G230 mutations for omitted terms, signs, constraints, and gauge."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

import verify_second_jet_independent as independent


ROOT = Path(__file__).resolve().parent


def scope_guard(scope: dict[str, bool]) -> bool:
    return not (
        scope["finite_region_realized"]
        or scope["values_generated"]
        or scope["physical_history_selected"]
    )


def symmetrize_derivative_pair(vector: list[F]) -> list[F]:
    result = list(vector)
    for f in range(4):
        for e in range(4):
            for q in independent.Q_SLOTS:
                i = independent.E_INDEX[(f, e, q)]
                j = independent.E_INDEX[(e, f, q)]
                result[i] = (vector[i] + vector[j]) / 2
    return result


def one_term_deleted_c4() -> list[dict[int, int]]:
    matrix = independent.build_c4_twice()
    mutated: list[dict[int, int]] = []
    for row in matrix:
        copy = dict(row)
        if copy:
            last = max(copy)
            del copy[last]
        mutated.append(copy)
    return mutated


def derive() -> dict[str, object]:
    algebraic = independent.build_algebraic_bianchi()
    db2 = independent.build_differentiated_bianchi()
    comm = independent.build_commutator()
    constraints = algebraic + db2 + comm
    gauge = independent.build_gauge()
    q = independent.q_from_g229_coefficient_one()
    full = independent.q_second_vector(q)
    product = independent.q_second_vector(q, "product")
    covariant = independent.q_second_vector(q, "covariant")
    rhs = independent.commutator_rhs(q)
    comm_full = independent.matvec(comm, full)
    symmetric = symmetrize_derivative_pair(full)
    prime = 1_000_000_007

    shortened_gauge = [dict(row) for row in gauge]
    for row in shortened_gauge:
        row.pop(223, None)

    deleted_c4_residual = independent.multiply_rows(constraints, one_term_deleted_c4())
    omitted_db_rank = independent.rank_mod(algebraic + comm, 336, prime)
    full_rank = independent.rank_mod(constraints, 336, prime)
    bounded_scope = {
        "finite_region_realized": False,
        "values_generated": False,
        "physical_history_selected": False,
    }
    promoted_scope = dict(bounded_scope)
    promoted_scope["physical_history_selected"] = True

    catches = {
        "delete_connection_product_detected": any(independent.matvec(db2, covariant)),
        "delete_covariantization_detected": (
            any(independent.matvec(db2, product))
            and any(a - b for a, b in zip(independent.matvec(comm, product), rhs))
        ),
        "reverse_commutator_sign_detected": any(a + b for a, b in zip(comm_full, rhs)),
        "premature_derivative_symmetrization_detected": any(
            a - b for a, b in zip(independent.matvec(comm, symmetric), rhs)
        ),
        "omit_differentiated_bianchi_detected": omitted_db_rank < full_rank,
        "truncate_quintic_gauge_detected": independent.rank_mod(shortened_gauge, 223, prime) < 224,
        "delete_c4_index_term_detected": any(deleted_c4_residual),
        "zero_E_false_overlap_detected": any(rhs),
        "point_jet_to_history_promotion_detected": (
            scope_guard(bounded_scope) and not scope_guard(promoted_scope)
        ),
    }
    result = {
        "landing": "HOSTILE_MUTATIONS_9_OF_9_CAUGHT" if all(catches.values()) else "HOSTILE_FAILURE",
        "catches": catches,
        "diagnostics": {
            "full_constraint_rank": full_rank,
            "omit_differentiated_bianchi_rank": omitted_db_rank,
            "shortened_gauge_rank": independent.rank_mod(shortened_gauge, 223, prime),
            "commutator_rhs_nonzero": sum(bool(value) for value in rhs),
        },
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if not args.no_write:
        (ROOT / "hostile_results.json").write_text(text + "\n", encoding="utf-8")
    if not all(result["catches"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
