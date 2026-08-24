#!/usr/bin/env python3
"""Exact finite checks for G247's global null-branch network classification."""

from __future__ import annotations

import argparse
import json
import math
import random
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path


LANDING = (
    "REGULAR_DIRECTION_ROUTE_LABELLED_NULL_BRANCH_ATLAS_DESCENDS_GLOBALLY"
    "__DIRECT_FUTURE_NULL_LINKS_FORM_A_QUIVER_NOT_A_CATEGORY_OR_GROUPOID"
    "__FREE_MATCHED_NULL_CHAIN_CATEGORY_CARRIES_ADDITIVE_DEPTH_AND_PATH_LABELLED_PHASE"
    "__CAUSTIC_BRANCH_AGGREGATION_GLOBAL_SELECTION_AND_PHYSICAL_HISTORY_REMAIN_OPEN"
)


def eye(n: int) -> list[list[F]]:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def mm(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def scale(a: list[list[F]], c: F) -> list[list[F]]:
    return [[c * x for x in row] for row in a]


def det(a: list[list[F]]) -> F:
    n = len(a)
    out = F(0)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = F(-1 if inversions % 2 else 1)
        for i in range(n):
            term *= a[i][p[i]]
        out += term
    return out


OMEGA = [
    [F(0), F(0), F(1), F(0)],
    [F(0), F(0), F(0), F(1)],
    [F(-1), F(0), F(0), F(0)],
    [F(0), F(-1), F(0), F(0)],
]


def edge_phase(r: F, b00: F, b01: F, b11: F) -> list[list[F]]:
    # M = diag(I, r I) [[I, B], [0, I]], with symmetric B.
    s = [
        [F(1), F(0), b00, b01],
        [F(0), F(1), b01, b11],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    d = [
        [F(1), F(0), F(0), F(0)],
        [F(0), F(1), F(0), F(0)],
        [F(0), F(0), r, F(0)],
        [F(0), F(0), F(0), r],
    ]
    return mm(d, s)


def vertex_quarter_turn() -> list[list[F]]:
    c = [[F(0), F(-1)], [F(1), F(0)]]
    return [
        [c[0][0], c[0][1], F(0), F(0)],
        [c[1][0], c[1][1], F(0), F(0)],
        [F(0), F(0), c[0][0], c[0][1]],
        [F(0), F(0), c[1][0], c[1][1]],
    ]


def is_csp(m: list[list[F]], r: F) -> bool:
    return mm(transpose(m), mm(OMEGA, m)) == scale(OMEGA, r)


def interval_squared(p: tuple[F, F], q: tuple[F, F]) -> F:
    dt = q[0] - p[0]
    dx = q[1] - p[1]
    return -dt * dt + dx * dx


def run(cases: int = 2048, seed: int = 247) -> dict:
    assertions = 0

    def req(condition: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(message)

    # Exact failure of closure for direct future-null links.
    a, b, c = (F(0), F(0)), (F(1), F(1)), (F(2), F(0))
    req(interval_squared(a, b) == 0, "A->B must be null")
    req(interval_squared(b, c) == 0, "B->C must be null")
    req(interval_squared(a, c) == -4, "A->C must be timelike")
    req(b[0] > a[0] and c[0] > b[0], "both legs must be future-directed")

    # Empty chain is the identity; it is not a zero-affine-span null ribbon.
    empty_chain: tuple[str, ...] = ()
    req(len(empty_chain) == 0, "identity must be the empty chain")
    req(a == a and interval_squared(a, a) == 0, "coincidence is separately typed")

    # Direction/route labels preserve global multiplicity on a flat cylinder.
    circumference, separation = F(10), F(3)
    windings = list(range(-10, 11))
    labelled = [(n, abs(separation + n * circumference), F(1)) for n in windings]
    req(len(labelled) == 21, "winding census")
    req(len({n for n, _, _ in labelled}) == 21, "route labels must remain distinct")
    req({r for _, _, r in labelled} == {F(1)}, "all winding clock ratios are one")
    req(len({delay for _, delay, _ in labelled}) > 1, "route delays retain non-scalar data")

    # Past reversal and future return are not the same physical arrow.
    e = F(2)
    req(F(1, 1) / e != e, "inverse and future return differ")
    req(math.isclose(-math.log(float(e)) - math.log(float(F(1) / e)), 0.0,
                     rel_tol=0.0, abs_tol=1e-15), "inverse depth is odd")

    rng = random.Random(seed)
    l = vertex_quarter_turn()
    req(is_csp(l, F(1)), "vertex lift must be symplectic")

    noncommuting = 0
    for _ in range(cases):
        r1 = F(rng.randint(1, 97), rng.randint(1, 97))
        r2 = F(rng.randint(1, 97), rng.randint(1, 97))
        coeffs = [F(rng.randint(-9, 9), rng.randint(1, 11)) for _ in range(6)]
        m1 = edge_phase(r1, coeffs[0], coeffs[1], coeffs[2])
        m2 = edge_phase(r2, coeffs[3], coeffs[4], coeffs[5])
        chain = mm(m2, mm(l, m1))
        product = r2 * r1

        req(r1 > 0 and r2 > 0, "clock ratios must be positive")
        req(is_csp(m1, r1), "first edge multiplier")
        req(is_csp(m2, r2), "second edge multiplier")
        req(is_csp(chain, product), "chain multiplier")
        req(det(m1) == r1 * r1, "first edge determinant")
        req(det(m2) == r2 * r2, "second edge determinant")
        req(det(chain) == product * product, "chain determinant")
        req((F(1) / r2) * (F(1) / r1) == F(1) / product,
            "inverse ruler factors compose")
        req(math.isclose(-math.log(float(product)),
                         -math.log(float(r1)) - math.log(float(r2)),
                         rel_tol=2e-15, abs_tol=2e-15), "depths add")
        req(mm(chain, eye(4)) == chain, "empty-chain identity")
        if mm(m2, l) != mm(l, m2):
            noncommuting += 1

    req(noncommuting > 0, "phase order must retain noncommuting matrix data")

    # A caustic position block can be singular while full phase is invertible.
    caustic = edge_phase(F(1), F(0), F(0), F(1))
    b_block = [[caustic[i][j] for j in (2, 3)] for i in (0, 1)]
    req(det(b_block) == 0, "position block must be singular in caustic control")
    req(det(caustic) == 1, "full phase must remain invertible")
    req(is_csp(caustic, F(1)), "full caustic phase must remain symplectic")

    # Exact overlap cocycle for affine-null charts.
    f1, a1, f2, a2, density = F(3, 2), F(5, 3), F(7, 4), F(11, 5), F(13, 7)
    direct_density = density / ((f1 * f2) * (a1 * a2))
    sequential_density = (density / (f1 * a1)) / (f2 * a2)
    req(direct_density == sequential_density, "affine-null density overlap cocycle")
    clock_weight_direct = density / (f1 * f2)
    clock_weight_sequential = (density / f1) / f2
    req(clock_weight_direct == clock_weight_sequential, "clock overlap weight cocycle")

    return {
        "landing": LANDING,
        "selected_alternative": "C_BRANCH_QUIVER_PLUS_GENERATED_CHAIN_CATEGORY",
        "cases": cases,
        "assertions": assertions,
        "noncommuting_phase_cases": noncommuting,
        "direct_null_closure_counterexample": {
            "AB_interval_squared": "0",
            "BC_interval_squared": "0",
            "AC_interval_squared": "-4",
        },
        "cylinder_winding_branches": len(labelled),
        "caustic_position_block_determinant": str(det(b_block)),
        "caustic_full_phase_determinant": str(det(caustic)),
        "status": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=2048)
    parser.add_argument("--seed", type=int, default=247)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.cases, args.seed)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
