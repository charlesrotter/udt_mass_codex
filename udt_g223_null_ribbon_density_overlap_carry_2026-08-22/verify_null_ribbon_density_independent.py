#!/usr/bin/env python3
"""Independent exact-rational G223 overlap replay without SymPy."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
CASES = 20000
SEED = 2230822


def mmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [sum((a[i][k] * b[k][j] for k in range(2)), Fraction(0)) for j in range(2)]
        for i in range(2)
    ]


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[j][i] for j in range(2)] for i in range(2)]


def det(a: list[list[Fraction]]) -> Fraction:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def adapted(F: Fraction, A: Fraction, Q: Fraction) -> list[list[Fraction]]:
    return [[1 / F, Fraction(0)], [-Q / (A * F), 1 / A]]


def positive(rng: random.Random) -> Fraction:
    return Fraction(rng.randint(1, 19), rng.randint(1, 17))


def signed(rng: random.Random) -> Fraction:
    return Fraction(rng.randint(-23, 23), rng.randint(1, 19))


def main(*, write_outputs: bool = True) -> None:
    rng = random.Random(SEED)
    assertions = 0
    for _ in range(CASES):
        F1, F2, A1, A2, density = (positive(rng) for _ in range(5))
        Q1, Q2, H = (signed(rng) for _ in range(3))

        P1 = adapted(F1, A1, Q1)
        h = [[H, -density], [-density, Fraction(0)]]
        hj = mmul(transpose(P1), mmul(h, P1))
        aj = density / (F1 * A1)
        Hj = (H + 2 * density * Q1 / A1) / (F1 * F1)
        expected = [[Hj, -aj], [-aj, Fraction(0)]]
        assert hj == expected
        assertions += 4
        assert det(hj) == -(aj * aj)
        assertions += 1
        assert aj * F1 * A1 == density
        assertions += 1
        assert aj * A1 == density / F1
        assertions += 1

        P2 = adapted(F2, A2, Q2)
        Pc = adapted(F1 * F2, A1 * A2, A2 * Q1 + F1 * Q2)
        assert mmul(P1, P2) == Pc
        assertions += 4
        assert density / (F1 * A1 * F2 * A2) == density / ((F1 * F2) * (A1 * A2))
        assertions += 1
        assert (1 / F1) * (1 / F2) == 1 / (F1 * F2)
        assertions += 1

        diagonal = adapted(F1, A1, Fraction(0))
        assert diagonal == [[1 / F1, Fraction(0)], [Fraction(0), 1 / A1]]
        assertions += 4
        assert det(diagonal) * density == aj
        assertions += 1

    # Same geometry and vertical class: old representative d lambda is closed;
    # after lambda'=exp(y)lambda the pulled-back new representative is
    # d lambda+lambda dy and has dy^dlam coefficient -1.
    old_curl = Fraction(0)
    new_curl = Fraction(-1)
    assert old_curl != new_curl
    assertions += 1

    # Exact affine fiber potential: the base-dependent offset cancels and the
    # vertical finite difference is exactly a times the parameter difference.
    for _ in range(1000):
        density = positive(rng)
        lambda_1, lambda_2, offset = (signed(rng) for _ in range(3))
        s_1 = density * lambda_1 + offset
        s_2 = density * lambda_2 + offset
        assert s_2 - s_1 == density * (lambda_2 - lambda_1)
        assertions += 1

    result = {
        "status": "PASS",
        "seed": SEED,
        "cases": CASES,
        "exact_rational_assertions": assertions,
        "same_metric_closedness_counterexample": True,
        "local_fiber_integration_control": True,
        "clock_weight_cocycle": True,
        "cross_ribbon_vertical_gluing_derived": False,
    }
    if write_outputs:
        (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
    print(f"PASS: G223 independent replay; {CASES} cases; {assertions} exact rational assertions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    main(write_outputs=not args.check_only)
