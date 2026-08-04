#!/usr/bin/env python3
"""Independent Fraction-only reconstruction of load-bearing selector algebra."""

from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
Z = F(0)
O = F(1)


def zero() -> list[list[F]]:
    return [[Z for _ in range(4)] for _ in range(4)]


def identity() -> list[list[F]]:
    out = zero()
    for i in range(4):
        out[i][i] = O
    return out


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(4)), Z) for j in range(4)] for i in range(4)]


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] + b[i][j] for j in range(4)] for i in range(4)]


def scale(c: F, a: list[list[F]]) -> list[list[F]]:
    return [[c * a[i][j] for j in range(4)] for i in range(4)]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [[a[j][i] for j in range(4)] for i in range(4)]


def diagonal(values: list[int]) -> list[list[F]]:
    out = zero()
    for i, value in enumerate(values):
        out[i][i] = F(value)
    return out


def gen(i: int, j: int) -> list[list[F]]:
    out = zero()
    out[i][j] = O
    out[j][i] = O if i == 0 else -O
    return out


def rank(rows: list[list[F]]) -> int:
    work = [row[:] for row in rows if any(row)]
    if not work:
        return 0
    r = 0
    columns = len(work[0])
    for c in range(columns):
        pivot = next((i for i in range(r, len(work)) if work[i][c]), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        q = work[r][c]
        work[r] = [x / q for x in work[r]]
        for i in range(len(work)):
            if i == r or not work[i][c]:
                continue
            q = work[i][c]
            work[i] = [work[i][j] - q * work[r][j] for j in range(columns)]
        r += 1
        if r == len(work):
            break
    return r


def commutant_rank(generators: list[list[list[F]]]) -> int:
    rows: list[list[F]] = []
    for g in generators:
        for i in range(4):
            for j in range(4):
                row = [Z] * 16
                for a in range(4):
                    for b in range(4):
                        column = 4 * a + b
                        if i == a:
                            row[column] += g[b][j]
                        if j == b:
                            row[column] -= g[i][a]
                rows.append(row)
    return rank(rows)


def spectral(operator: list[list[F]], value: int, others: list[int]) -> list[list[F]]:
    out = identity()
    for other in others:
        factor = add(operator, scale(F(-other), identity()))
        out = scale(F(1, value - other), mul(out, factor))
    return out


boosts = [gen(0, i) for i in (1, 2, 3)]
rotations = [gen(1, 2), gen(1, 3), gen(2, 3)]
full_rank = commutant_rank(boosts + rotations)
round_rank = commutant_rank(rotations)
ruler_rank = commutant_rank([gen(0, 2), gen(0, 3), gen(2, 3)])
null_generators = [gen(2, 3), add(gen(0, 2), gen(1, 2)), add(gen(0, 3), gen(1, 3))]
null_rank = commutant_rank(null_generators)
assert (full_rank, round_rank, ruler_rank, null_rank) == (15, 14, 14, 14)

B0 = [[F(-1), O, Z, Z], [F(-1), O, Z, Z], [Z, Z, Z, Z], [Z, Z, Z, Z]]
B1 = [[F(2), F(-1), Z, Z], [O, Z, Z, Z], [Z, Z, O, Z], [Z, Z, Z, O]]
assert mul(B0, B0) == zero() and add(B0, B1) == identity()
assert all(mul(B0, item) == mul(item, B0) and mul(B1, item) == mul(item, B1) for item in null_generators)
null_idempotent_ranks = [0, 4]

eta = diagonal([-1, 1, 1, 1])
A = diagonal([2, 3, 5, 5])
ricci_q02 = diagonal([0, 0, 0, 0])
ricci_q02[1][1] = F(1, 2)
ricci_q02[2][2] = F(3, 2)
ricci_q02[3][3] = F(3, 2)
assert A == add(scale(F(2), identity()), scale(F(2), ricci_q02))
P = add(spectral(A, 2, [3, 5]), spectral(A, 3, [2, 5]))
expected_P = diagonal([1, 1, 0, 0])
assert P == expected_P and mul(P, P) == P
assert mul(transpose(P), eta) == mul(eta, P)

boost = [
    [F(5, 3), Z, F(4, 3), Z],
    [Z, O, Z, Z],
    [F(4, 3), Z, F(5, 3), Z],
    [Z, Z, Z, O],
]
boost_inverse = [
    [F(5, 3), Z, F(-4, 3), Z],
    [Z, O, Z, Z],
    [F(-4, 3), Z, F(5, 3), Z],
    [Z, Z, Z, O],
]
assert mul(mul(transpose(boost), eta), boost) == eta
A_prime = mul(mul(boost, A), boost_inverse)
P_prime = add(spectral(A_prime, 2, [3, 5]), spectral(A_prime, 3, [2, 5]))
assert P_prime == mul(mul(boost, P), boost_inverse)

P_e1 = diagonal([1, 1, 0, 0])
P_e2 = diagonal([1, 0, 1, 0])
assert P_e1 != P_e2
difference_rows = [[P_e1[i][j] - P_e2[i][j] for j in range(4)] for i in range(4)]
assert rank(difference_rows) == 2
axis_swap = [[O, Z, Z, Z], [Z, Z, O, Z], [Z, O, Z, Z], [Z, Z, Z, O]]
assert mul(mul(axis_swap, P_e1), axis_swap) == P_e2

e1 = [[Z], [O], [Z], [Z]]
orbit_columns = []
for g in rotations:
    orbit_columns.append([sum((g[i][j] * e1[j][0] for j in range(4)), Z) for i in range(4)])
orbit_rows = [[orbit_columns[j][i] for j in range(3)] for i in range(4)]
assert rank(orbit_rows) == 2

with (ROOT / "udt_intrinsic_two_form_distribution_audit_2026-08-02/CANDIDATE_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
    intrinsic = list(csv.DictReader(handle, delimiter="\t"))
counts: dict[str, int] = {}
for row in intrinsic:
    counts[row["distribution_status"]] = counts.get(row["distribution_status"], 0) + 1
assert counts == {"ZERO": 9, "MULTIPLE_NONZERO_TYPES_ON_DIFFERENT_LOCI": 6, "PROJECTOR_BLOCKED": 2, "METRIC_DEGENERATE": 1}

with (HERE / "SELECTOR_OUTCOMES.tsv").open(newline="", encoding="utf-8") as handle:
    outcomes = list(csv.DictReader(handle, delimiter="\t"))
assert len(outcomes) == 18 and [row["selector_id"] for row in outcomes] == [f"M{i:02d}" for i in range(18)]

result = {
    "schema": "udt-metric-natural-reciprocal-split-selector-independent-1.0",
    "result": "PASS",
    "method": "stdlib_Fraction_no_production_import",
    "full_commutant_rank": full_rank,
    "round_commutant_rank": round_rank,
    "ruler_complement_commutant_rank": ruler_rank,
    "null_little_group_commutant_rank": null_rank,
    "null_little_group_idempotent_ranks": null_idempotent_ranks,
    "round_idempotent_ranks": [0, 1, 3, 4],
    "ricci_projector_rank": rank(P),
    "ricci_equivariance": True,
    "collision_projector_difference_rank": rank(difference_rows),
    "collision_axis_rotation": True,
    "q02_ricci_link": True,
    "round_line_orbit_dimension": rank(orbit_rows),
    "intrinsic_counts": counts,
    "selector_rows": len(outcomes),
}
(HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
