#!/usr/bin/env python3
"""Independent Fraction replay for G247; imports no production code or output."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction
from pathlib import Path


EXPECTED = (
    "REGULAR_DIRECTION_ROUTE_LABELLED_NULL_BRANCH_ATLAS_DESCENDS_GLOBALLY"
    "__DIRECT_FUTURE_NULL_LINKS_FORM_A_QUIVER_NOT_A_CATEGORY_OR_GROUPOID"
    "__FREE_MATCHED_NULL_CHAIN_CATEGORY_CARRIES_ADDITIVE_DEPTH_AND_PATH_LABELLED_PHASE"
    "__CAUSTIC_BRANCH_AGGREGATION_GLOBAL_SELECTION_AND_PHYSICAL_HISTORY_REMAIN_OPEN"
)


def mul(a, b):
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(4)), Fraction(0))
                       for j in range(4)) for i in range(4))


def tr(a):
    return tuple(tuple(a[j][i] for j in range(4)) for i in range(4))


O = (
    (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
    (Fraction(-1), Fraction(0), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(-1), Fraction(0), Fraction(0)),
)


def scaled(a, q):
    return tuple(tuple(q * x for x in row) for row in a)


def phase(q, x, y, z):
    # Independently write out diag(I,qI) times a symmetric upper shear.
    return (
        (Fraction(1), Fraction(0), x, y),
        (Fraction(0), Fraction(1), y, z),
        (Fraction(0), Fraction(0), q, Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0), q),
    )


L = (
    (Fraction(0), Fraction(-1), Fraction(0), Fraction(0)),
    (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(0), Fraction(-1)),
    (Fraction(0), Fraction(0), Fraction(1), Fraction(0)),
)


def csp(a, q):
    return mul(tr(a), mul(O, a)) == scaled(O, q)


def run(cases, seed):
    checks = 0

    def yes(value, label):
        nonlocal checks
        checks += 1
        if not value:
            raise AssertionError(label)

    # Independent interval check, written directly rather than calling a helper.
    for dt, dx, wanted in ((1, 1, 0), (1, -1, 0), (2, 0, -4)):
        yes(-Fraction(dt) ** 2 + Fraction(dx) ** 2 == wanted, "causal interval")
    yes(csp(L, Fraction(1)), "vertex phase")

    rng = random.Random(seed)
    reordered_differences = 0
    for _ in range(cases):
        q1 = Fraction(rng.randrange(1, 151), rng.randrange(1, 151))
        q2 = Fraction(rng.randrange(1, 151), rng.randrange(1, 151))
        v = [Fraction(rng.randrange(-13, 14), rng.randrange(1, 17)) for _ in range(6)]
        a = phase(q1, v[0], v[1], v[2])
        b = phase(q2, v[3], v[4], v[5])
        chain = mul(b, mul(L, a))
        q = q2 * q1

        yes(q1 > 0, "positive first ratio")
        yes(q2 > 0, "positive second ratio")
        yes(csp(a, q1), "first CSp law")
        yes(csp(b, q2), "second CSp law")
        yes(csp(chain, q), "chain CSp law")
        yes(Fraction(1, 1) / q == (Fraction(1, 1) / q2) * (Fraction(1, 1) / q1),
            "ruler inverse law")
        yes(q / q1 == q2, "middle ratio cancels")
        yes(mul(b, L) != mul(L, b) or v[3] == v[5] == 0,
            "ordered vertex carry")
        yes(mul(chain, L) != mul(L, chain) or chain == L,
            "matrix phase is not a scalar")
        yes(csp(mul(L, chain), q), "further vertex composition")
        yes(csp(mul(chain, L), q), "opposite ordered composition remains CSp")
        if mul(b, L) != mul(L, b):
            reordered_differences += 1

    yes(reordered_differences > 0, "noncommuting samples required")

    # Route-label and caustic checks by a second construction.
    labels = tuple((n, abs(2 + 9 * n)) for n in range(-12, 13))
    yes(len(labels) == 25, "winding count")
    yes(len(set(labels)) == 25, "winding labels")
    yes(len({delay for _, delay in labels}) > 1, "winding delays")
    singular_b_phase = phase(Fraction(1), Fraction(0), Fraction(0), Fraction(5))
    yes(singular_b_phase[0][2] * singular_b_phase[1][3]
        - singular_b_phase[0][3] * singular_b_phase[1][2] == 0, "singular B block")
    yes(csp(singular_b_phase, Fraction(1)), "full phase survives caustic")

    return {
        "expected_landing": EXPECTED,
        "cases": cases,
        "assertions": checks,
        "reordered_phase_differences": reordered_differences,
        "implementation": "independent_standard_library_fraction_no_production_import",
        "status": "PASS",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cases", type=int, default=5000)
    p.add_argument("--seed", type=int, default=247001)
    p.add_argument("--output", type=Path)
    ns = p.parse_args()
    result = run(ns.cases, ns.seed)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if ns.output:
        ns.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()

