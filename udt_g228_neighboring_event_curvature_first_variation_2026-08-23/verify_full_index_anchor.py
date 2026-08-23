#!/usr/bin/env python3
"""Orthogonal 84-slot full-index anchor for G228.

Unlike both 20-slot implementations, this verifier keeps all 21 symmetric
bivector-bilinear entries for every derivative direction.  It imposes the
four algebraic-Bianchi rows and the differential-Bianchi rows simultaneously.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import sympy as sp


BIVECTORS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_INDEX = {pair: i for i, pair in enumerate(BIVECTORS)}
FULL_SLOTS = tuple((i, j) for i in range(6) for j in range(i, 6))
DIRECTIONS = {
    "k": (sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(1)),
    "l": (sp.Rational(1, 2), sp.Integer(0), sp.Integer(0), sp.Rational(-1, 2)),
    "s1": (sp.Integer(0), sp.Integer(1), sp.Integer(0), sp.Integer(0)),
    "s2": (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(0)),
}
ORDER = ("k", "l", "s1", "s2")


def ordered_pair(a: int, b: int) -> tuple[int, int]:
    if a == b:
        return 0, -1
    if a < b:
        return 1, PAIR_INDEX[(a, b)]
    return -1, PAIR_INDEX[(b, a)]


def full_q_basis() -> list[sp.Matrix]:
    answer = []
    for i, j in FULL_SLOTS:
        q = sp.zeros(6, 6)
        q[i, j] = 1
        q[j, i] = 1
        answer.append(q)
    return answer


FULL_BASIS = full_q_basis()


def rcomp(j: int, a: int, b: int, c: int, d: int) -> sp.Expr:
    s1, i = ordered_pair(a, b)
    s2, k = ordered_pair(c, d)
    if not s1 or not s2:
        return sp.Integer(0)
    return s1 * s2 * FULL_BASIS[j][i, k]


def build_full_constraints() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    algebraic_rows = []
    for mu in range(4):
        row = [sp.Integer(0)] * 84
        for j, q in enumerate(FULL_BASIS):
            row[mu * 21 + j] = q[0, 5] - q[1, 4] + q[2, 3]
        algebraic_rows.append(row)

    differential_rows = []
    for e, a, b in itertools.combinations(range(4), 3):
        for c, d in BIVECTORS:
            row = [sp.Integer(0)] * 84
            for j in range(21):
                row[e * 21 + j] += rcomp(j, a, b, c, d)
                row[a * 21 + j] += rcomp(j, b, e, c, d)
                row[b * 21 + j] += rcomp(j, e, a, c, d)
            differential_rows.append(row)
    algebraic = sp.Matrix(algebraic_rows)
    differential = sp.Matrix(differential_rows)
    return algebraic, differential, sp.Matrix.vstack(algebraic, differential)


def projection(names: tuple[str, ...]) -> sp.Matrix:
    rows = []
    for name in names:
        direction = DIRECTIONS[name]
        for component in range(21):
            row = [sp.Integer(0)] * 84
            for mu, coefficient in enumerate(direction):
                row[mu * 21 + component] = coefficient
            rows.append(row)
    return sp.Matrix(rows)


def derive() -> dict[str, object]:
    algebraic, differential, combined = build_full_constraints()
    kernel = sp.Matrix.hstack(*combined.nullspace())
    census = []
    for size in range(1, 5):
        for names in itertools.combinations(ORDER, size):
            image_rank = int((projection(names) * kernel).rank())
            census.append({
                "key": "+".join(names),
                "size": size,
                "intrinsic_target_dimension": 20 * size,
                "image_rank": image_rank,
                "intrinsic_codimension": 20 * size - image_rank,
            })
    return {
        "raw_full_slot_variables": 84,
        "algebraic_bianchi_rank": int(algebraic.rank()),
        "differential_rows_rank_before_combination": int(differential.rank()),
        "combined_constraint_rank": int(combined.rank()),
        "differential_incremental_rank": int(combined.rank()) - int(algebraic.rank()),
        "compatible_module_dimension": 84 - int(combined.rank()),
        "subset_census": census,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "FULL_INDEX_ANCHOR.json")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    if not args.no_write:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
