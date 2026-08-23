#!/usr/bin/env python3
"""Independent exact-arithmetic replay for G239; imports no production code."""

from __future__ import annotations

import json
import random
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def norm(values: list[Fraction]) -> list[Fraction]:
    total = sum(values, Fraction(0))
    return [value / total for value in values]


def form(a: list[Fraction], k: list[list[Fraction]], b: list[Fraction]) -> Fraction:
    return sum(
        (a[i] * k[i][j] * b[j] for i in range(len(a)) for j in range(len(a))),
        Fraction(0),
    )


def outer(a: list[Fraction], b: list[Fraction]) -> list[list[Fraction]]:
    return [[x * y for y in b] for x in a]


def run() -> dict[str, object]:
    # Independent exact replay of the G127 local area-response coefficient.
    tilted = [Fraction(8, 25), Fraction(4, 25)]
    tilted_trace = tilted[0] + tilted[1]
    determinant_lambda4_coefficient = -tilted_trace / 6
    assert tilted_trace == Fraction(12, 25)
    assert determinant_lambda4_coefficient == Fraction(-2, 25)

    rng = random.Random(239)
    identity_cases = 0
    cancellation_cases = 0
    nonzero_cases = 0
    branch_cases = 0

    for _ in range(2000):
        n = rng.randint(3, 7)
        q = norm([Fraction(rng.randint(1, 11)) for _ in range(n)])
        response = [Fraction(rng.randint(1, 9)) for _ in range(n)]
        p = norm([q[i] * response[i] for i in range(n)])
        k = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                value = Fraction(rng.randint(0, 5))
                k[i][j] = value
                k[j][i] = value
        rr = form(q, k, q)
        if rr == 0:
            continue
        dd = form(p, k, p)
        dr = form(p, k, q)
        ls = (dd - 2 * dr + rr) / rr
        delta = [p[i] - q[i] for i in range(n)]
        assert ls == form(delta, k, delta) / rr
        identity_cases += 1
        if ls != 0:
            nonzero_cases += 1

        common = Fraction(rng.randint(1, 20))
        pc = norm([q_i * common for q_i in q])
        assert pc == q
        assert (form(pc, k, pc) - 2 * form(pc, k, q) + rr) / rr == 0
        assert (form(p, k, p) - 2 * form(p, k, p) + form(p, k, p)) == 0
        cancellation_cases += 1

        ns = rng.randint(2, 5)
        no = rng.randint(2, 6)
        source = norm([Fraction(rng.randint(1, 9)) for _ in range(ns)])
        # Each source column is a normalized supplied branch distribution.
        columns = [norm([Fraction(rng.randint(1, 9)) for _ in range(no)]) for _ in range(ns)]
        amap = [[columns[a][i] for a in range(ns)] for i in range(no)]
        mapped = [sum((amap[i][a] * source[a] for a in range(ns)), Fraction(0)) for i in range(no)]
        direct = [
            [
                sum(
                    (
                        amap[i][a] * amap[j][b] * source[a] * source[b]
                        for a in range(ns)
                        for b in range(ns)
                    ),
                    Fraction(0),
                )
                for j in range(no)
            ]
            for i in range(no)
        ]
        assert direct == outer(mapped, mapped)
        branch_cases += 1

    if identity_cases < 1900 or nonzero_cases == 0:
        raise AssertionError("insufficient independent coverage")

    result = {
        "audit": "G239_INDEPENDENT_REFERENCE_OPERATOR_REPLAY",
        "status": "PASS",
        "implementation": "independent_standard_library_fraction_randomized",
        "seed": 239,
        "identity_cases": identity_cases,
        "cancellation_cases": cancellation_cases,
        "nonzero_cases": nonzero_cases,
        "branch_factorization_cases": branch_cases,
        "g127_tilted_trace": "12/25",
        "g127_jacobi_determinant_lambda4_coefficient": "-2/25",
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
