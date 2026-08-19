#!/usr/bin/env python3
"""Independent Fraction replay for G167; imports no production implementation."""

from __future__ import annotations

import csv
import hashlib
import json
import random
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def pullback(diagonal: list[F], jacobian: list[list[F]]) -> list[list[F]]:
    return [
        [
            sum(diagonal[a] * jacobian[a][i] * jacobian[a][j] for a in range(4))
            for j in range(2)
        ]
        for i in range(2)
    ]


def add2(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]


def det2(h: list[list[F]]) -> F:
    return h[0][0] * h[1][1] - h[0][1] * h[1][0]


def q2(h: list[list[F]]) -> F:
    return h[0][0] ** 2 / (-det2(h))


def dot_pullback(
    diagonal: list[F],
    dot_diagonal: list[F],
    jacobian: list[list[F]],
    dot_jacobian: list[list[F]],
) -> list[list[F]]:
    return [
        [
            sum(
                dot_diagonal[a] * jacobian[a][i] * jacobian[a][j]
                + diagonal[a]
                * (
                    dot_jacobian[a][i] * jacobian[a][j]
                    + jacobian[a][i] * dot_jacobian[a][j]
                )
                for a in range(4)
            )
            for j in range(2)
        ]
        for i in range(2)
    ]


def phi_dot_from_h(h: list[list[F]], dot_h: list[list[F]]) -> F:
    determinant = det2(h)
    dot_det = (
        dot_h[0][0] * h[1][1]
        + h[0][0] * dot_h[1][1]
        - 2 * h[0][1] * dot_h[0][1]
    )
    return dot_det / (4 * determinant) - dot_h[0][0] / (2 * h[0][0])


def source_hashes() -> tuple[int, list[str]]:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures: list[str] = []
    for row in rows:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            failures.append(row["path"])
    return len(rows), failures


def main() -> None:
    rng = random.Random(167)
    trials = 1200
    regular = 0
    for _ in range(trials):
        ce = F(rng.randint(1, 5), rng.randint(1, 5))
        u = F(rng.randint(1, 5), rng.randint(1, 5))
        radius = F(rng.randint(1, 5), rng.randint(1, 5))
        sine = F(rng.randint(1, 5), rng.randint(5, 9))
        diagonal = [-(ce / u) ** 2, u**2, radius**2, (radius * sine) ** 2]
        jacobian = [
            [F(rng.randint(-4, 4), rng.randint(1, 5)) for _ in range(2)]
            for _ in range(4)
        ]
        h = pullback(diagonal, jacobian)
        y = jacobian[:2]
        z = jacobian[2:]
        h_base = pullback(diagonal[:2] + [F(0), F(0)], y + [[F(0), F(0)], [F(0), F(0)]])
        p = pullback([F(0), F(0)] + diagonal[2:], [[F(0), F(0)], [F(0), F(0)]] + z)
        if h != add2(h_base, p):
            raise SystemExit("FAIL: pullback assembly")

        dot_diagonal = [
            F(rng.randint(-5, 5), rng.randint(1, 5)) for _ in range(4)
        ]
        dot_jacobian = [
            [F(rng.randint(-4, 4), rng.randint(1, 5)) for _ in range(2)]
            for _ in range(4)
        ]
        dot_h = dot_pullback(diagonal, dot_diagonal, jacobian, dot_jacobian)
        if h[0][0] != 0 and det2(h) != 0:
            # Independent identity: phi_dot equals -1/4 d log(q^2).
            determinant = det2(h)
            dot_det = (
                dot_h[0][0] * h[1][1]
                + h[0][0] * dot_h[1][1]
                - 2 * h[0][1] * dot_h[0][1]
            )
            dot_log_q2 = 2 * dot_h[0][0] / h[0][0] - dot_det / determinant
            if phi_dot_from_h(h, dot_h) != -dot_log_q2 / 4:
                raise SystemExit("FAIL: live terminal identity")
        if h[0][0] < 0 and det2(h) < 0:
            regular += 1

    diagonal = [-F(1, 4), F(4), F(9), F(144, 25)]
    witness_j = [
        [F(4), F(0)],
        [F(0), F(1, 2)],
        [F(1, 10), F(1, 5)],
        [F(0), F(1, 3)],
    ]
    witness = pullback(diagonal, witness_j)
    expected = [[-F(391, 100), F(9, 50)], [F(9, 50), F(2)]]
    if witness != expected:
        raise SystemExit(f"FAIL: witness {witness}")
    if det2(witness) != -F(19631, 2500):
        raise SystemExit("FAIL: witness determinant")
    if q2(witness) != F(152881, 78524):
        raise SystemExit(f"FAIL: witness q2 {q2(witness)}")

    count, failures = source_hashes()
    result = {
        "status": "PASS" if count == 10 and not failures else "FAIL",
        "fraction_trials": trials,
        "regular_lorentzian_trials": regular,
        "source_count": count,
        "source_failures": failures,
        "witness_h": [[str(value) for value in row] for row in witness],
        "witness_det": str(det2(witness)),
        "witness_q_squared": str(q2(witness)),
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if result["status"] != "PASS":
        raise SystemExit(f"FAIL: source hashes {failures}")
    print(f"PASS: {trials} independent Fraction trials; {regular} regular; 10 sources")


if __name__ == "__main__":
    main()
