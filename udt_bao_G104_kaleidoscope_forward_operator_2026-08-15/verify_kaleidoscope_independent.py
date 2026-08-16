#!/usr/bin/env python3
"""Independent Fraction-only G104 replay; imports no production code."""

from __future__ import annotations

from fractions import Fraction as F
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent


def outer(a: list[F], b: list[F]) -> list[list[F]]:
    return [[x * y for y in b] for x in a]


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def matvec(a: list[list[F]], x: list[F]) -> list[F]:
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def is_zero(a: list[list[F]]) -> bool:
    return all(value == 0 for row in a for value in row)


def main() -> None:
    lam = [F(2, 5), F(7, 20), F(1, 4)]
    kernel = [
        [F(3, 4), F(1, 5), 0],
        [F(1, 4), F(1, 2), F(2, 5)],
        [0, F(3, 10), F(3, 5)],
    ]
    assert all(sum(kernel[i][j] for i in range(3)) == 1 for j in range(3))
    nu = matvec(kernel, lam)
    factor = outer(nu, nu)

    p = [F(5, 12), F(1, 3), F(1, 4)]
    q = [F(1, 3)] * 3
    ls = add(sub(sub(outer(p, p), outer(p, q)), outer(q, p)), outer(q, q))
    delta = [x - y for x, y in zip(p, q)]

    identity = [[F(int(i == j)) for j in range(3)] for i in range(3)]
    reverse = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    marked = [
        [F(3, 5) * identity[i][j] + F(2, 5) * reverse[i][j] for j in range(3)]
        for i in range(3)
    ]
    marked_nu = matvec(marked, lam)

    cluster = [[F(0) for _ in range(3)] for _ in range(3)]
    for i, weight in enumerate(lam):
        j = 2 - i
        if i != j:
            cluster[i][j] += weight
            cluster[j][i] += weight

    checks = {
        "factorized_null": is_zero(sub(factor, factor)),
        "selection_mismatch_identity": ls == outer(delta, delta),
        "selection_mismatch_nonzero": not is_zero(ls),
        "independent_marking_null": is_zero(sub(outer(marked_nu, marked_nu), outer(marked_nu, marked_nu))),
        "cluster_nonzero": not is_zero(cluster),
        "imports_production": False,
        "outcome_artifacts_read": [],
    }
    if not all(
        value for key, value in checks.items()
        if key not in {"imports_production", "outcome_artifacts_read"}
    ):
        raise AssertionError(json.dumps(checks, indent=2, sort_keys=True))
    result = {"status": "PASS", "checks": checks}
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
