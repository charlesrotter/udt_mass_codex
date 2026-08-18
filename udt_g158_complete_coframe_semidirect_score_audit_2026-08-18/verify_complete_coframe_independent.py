#!/usr/bin/env python3
"""Independent stdlib replay of G158; imports neither SymPy nor production code."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import random
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "f26c7ace"
LANDING = (
    "GAUGE_FIXED_COMPLETE_COFRAME_SEMIDIRECT_SCORE_DERIVED__"
    "TEN_CHANNEL_REGULAR_GROUP_CLOSES__BASE_AND_SCREEN_BPLUS2_CHANNELS_"
    "ACT_ON_FOUR_MIXING_COMPONENTS__Y_Z_ARE_QUERY_REPRESENTATION_DATA_"
    "NOT_GROUP_COORDINATES__CHANGING_BALANCE_ALLOWED__PHYSICAL_CARRY_"
    "HISTORY_SCORE_AND_GLOBAL_COMPLETION_OPEN"
)


def mm(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def neg(a):
    return [[-value for value in row] for row in a]


def eq(a, b):
    return a == b


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def inv2(a):
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert determinant != 0
    return [
        [a[1][1] / determinant, -a[0][1] / determinant],
        [-a[1][0] / determinant, a[0][0] / determinant],
    ]


def block(b, q, s):
    qs = mm(q, s)
    return [
        [b[0][0], b[0][1], F(0), F(0)],
        [b[1][0], b[1][1], F(0), F(0)],
        [qs[0][0], qs[0][1], q[0][0], q[0][1]],
        [qs[1][0], qs[1][1], q[1][0], q[1][1]],
    ]


def split(e):
    b = [e[0][:2], e[1][:2]]
    q = [e[2][2:], e[3][2:]]
    lower = [e[2][:2], e[3][:2]]
    return b, q, mm(inv2(q), lower)


def product(g2, g1):
    b2, q2, s2 = g2
    b1, q1, s1 = g1
    return mm(b2, b1), mm(q2, q1), add(s1, mm(mm(inv2(q1), s2), b1))


def inverse(g):
    b, q, s = g
    return inv2(b), inv2(q), neg(mm(mm(q, s), inv2(b)))


def determinant(a):
    work = [row[:] for row in a]
    result = F(1)
    n = len(work)
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col] != 0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result = -result
        value = work[col][col]
        result *= value
        for row in range(col + 1, n):
            factor = work[row][col] / value
            for j in range(col, n):
                work[row][j] -= factor * work[col][j]
    return result


def random_upper(rng):
    return [[F(rng.randint(1, 9)), F(rng.randint(-5, 5))], [F(0), F(rng.randint(1, 9))]]


def random_m2(rng):
    return [[F(rng.randint(-5, 5)), F(rng.randint(-5, 5))],
            [F(rng.randint(-5, 5)), F(rng.randint(-5, 5))]]


def random_group(rng):
    return random_upper(rng), random_upper(rng), random_m2(rng)


def verify_manifest():
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 10
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"])
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
    return len(rows)


def main():
    source_count = verify_manifest()
    rng = random.Random(158)
    trials = 500
    for _ in range(trials):
        g1, g2, g3 = random_group(rng), random_group(rng), random_group(rng)
        e1, e2, e3 = block(*g1), block(*g2), block(*g3)
        gp = product(g2, g1)
        assert eq(mm(e2, e1), block(*gp))
        assert eq(block(*split(e1)), e1)
        gi = inverse(g1)
        assert eq(mm(block(*gi), e1), eye(4))
        assert eq(mm(e1, block(*gi)), eye(4))
        assert eq(mm(mm(e3, e2), e1), mm(e3, mm(e2, e1)))
        assert determinant(e1) == determinant(g1[0]) * determinant(g1[1])

        j = [[F(rng.randint(-3, 3)), F(rng.randint(-3, 3))] for _ in range(4)]
        assert eq(mm(e2, mm(e1, j)), mm(block(*gp), j))

        # Differential identity using independently assembled tangent blocks.
        db, dq, ds = random_upper(rng), random_upper(rng), random_m2(rng)
        lower_de = add(mm(dq, g1[2]), mm(g1[1], ds))
        de = [
            [db[0][0], db[0][1], F(0), F(0)],
            [db[1][0], db[1][1], F(0), F(0)],
            [lower_de[0][0], lower_de[0][1], dq[0][0], dq[0][1]],
            [lower_de[1][0], lower_de[1][1], dq[1][0], dq[1][1]],
        ]
        right = mm(de, block(*gi))
        right_expected = [
            mm(db, inv2(g1[0]))[0] + [F(0), F(0)],
            mm(db, inv2(g1[0]))[1] + [F(0), F(0)],
            mm(mm(g1[1], ds), inv2(g1[0]))[0] + mm(dq, inv2(g1[1]))[0],
            mm(mm(g1[1], ds), inv2(g1[0]))[1] + mm(dq, inv2(g1[1]))[1],
        ]
        assert eq(right, right_expected)
        dj = [[F(rng.randint(-3, 3)), F(rng.randint(-3, 3))] for _ in range(4)]
        v = mm(e1, j)
        dv = add(mm(de, j), mm(e1, dj))
        assert eq(dv, add(mm(right, v), mm(e1, dj)))

    # Registered changing-balance witness.
    def frame(t):
        return block(
            [[F(1 + t), F(t * t)], [F(0), F(1 + t * t)]],
            [[F(1 + t * t), F(t)], [F(0), F(1 + 2 * t)]],
            [[F(t), F(t * t)], [F(t**3), F(-t)]],
        )

    f0, f1, f2 = frame(0), frame(1), frame(2)
    c10 = mm(f1, block(*inverse(split(f0))))
    c21 = mm(f2, block(*inverse(split(f1))))
    c20 = mm(f2, block(*inverse(split(f0))))
    assert eq(mm(c21, c10), c20)
    assert not eq(f2, mm(f1, f1))
    # Independent exact score-balance check for the polynomial witness.
    b0 = [[F(1), F(0)], [F(0), F(1)]]
    db0 = [[F(1), F(0)], [F(0), F(0)]]
    b1 = [[F(2), F(1)], [F(0), F(2)]]
    db1 = [[F(1), F(2)], [F(0), F(2)]]
    omega_bb_0 = mm(db0, inv2(b0))
    omega_bb_1 = mm(db1, inv2(b1))
    assert omega_bb_0 == [[F(1), F(0)], [F(0), F(0)]]
    assert omega_bb_1 == [[F(1, 2), F(3, 4)], [F(0), F(1)]]
    assert omega_bb_0[1][1] == 0 and omega_bb_1[1][1] != 0

    # Independent floating fixed-generator control.
    subgroup_trials = 200
    subgroup_attempts = 0
    subgroup_executed = 0
    while subgroup_executed < subgroup_trials:
        subgroup_attempts += 1
        aa = [rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)]
        cc = [rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)]
        # Avoid near-resonance only to keep the direct quotient well-conditioned.
        if min(abs(aa[j] - cc[i]) for i, j in itertools.product(range(2), repeat=2)) < 0.05:
            continue
        m = [[rng.uniform(-1.0, 1.0) for _ in range(2)] for _ in range(2)]
        t, u = rng.uniform(-0.8, 0.8), rng.uniform(-0.8, 0.8)

        def fg(x):
            b = [[math.exp(aa[0] * x), 0.0], [0.0, math.exp(aa[1] * x)]]
            q = [[math.exp(cc[0] * x), 0.0], [0.0, math.exp(cc[1] * x)]]
            s = [[m[i][j] * (math.exp((aa[j] - cc[i]) * x) - 1.0) /
                  (aa[j] - cc[i]) for j in range(2)] for i in range(2)]
            return b, q, s

        lhs = block(*product(fg(t), fg(u)))
        rhs = block(*fg(t + u))
        assert all(math.isclose(lhs[i][j], rhs[i][j], rel_tol=3e-11, abs_tol=3e-11)
                   for i in range(4) for j in range(4))
        subgroup_executed += 1

    result = {
        "status": "PASS",
        "method": "stdlib_fraction_exact_plus_independent_float_fixed_generator",
        "registered_outcome_class": "COMPLETE_COFRAME_SEMIDIRECT_SCORE_DERIVED",
        "landing": LANDING,
        "source_count": source_count,
        "exact_fraction_trials": trials,
        "fixed_generator_trials": subgroup_executed,
        "fixed_generator_attempts": subgroup_attempts,
        "changing_balance_witnesses": 1,
        "changing_score_witness_noncollinear": True,
        "coordinate_count": 10,
        "query_blocks_are_group_coordinates": False,
        "physical_score_derived": False,
        "physical_cross_query_carry_derived": False,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
