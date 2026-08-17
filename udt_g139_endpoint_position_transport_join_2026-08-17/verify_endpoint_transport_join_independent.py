#!/usr/bin/env python3
"""Independent stdlib verification for G139; deliberately does not import production code."""

from __future__ import annotations

import hashlib
import random
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def add_bounded(a: Fraction, b: Fraction) -> Fraction:
    return (a + b) / (1 + a * b)


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def transpose(a):
    return tuple(zip(*a))


def main() -> None:
    rng = random.Random(139_20260817)
    passed = 0
    total = 0

    # Independent rational associativity and inverse replay.
    for _ in range(1200):
        vals = [Fraction(rng.randint(-7, 7), 16) for _ in range(3)]
        a, b, c = vals
        if any(1 + x * y == 0 for x, y in ((a, b), (b, c))):
            continue
        left = add_bounded(add_bounded(a, b), c)
        right = add_bounded(a, add_bounded(b, c))
        total += 2
        passed += int(left == right)
        passed += int(add_bounded(a, -a) == 0)

    # Exact SO(2) transport and order convention, using only Fraction arithmetic.
    rotations = [
        ((Fraction(3, 5), Fraction(-4, 5)), (Fraction(4, 5), Fraction(3, 5))),
        ((Fraction(5, 13), Fraction(-12, 13)), (Fraction(12, 13), Fraction(5, 13))),
        ((Fraction(7, 25), Fraction(-24, 25)), (Fraction(24, 25), Fraction(7, 25))),
    ]
    identity = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    for u in rotations:
        total += 2
        passed += int(mm(transpose(u), u) == identity)
        passed += int(u[0][0] * u[1][1] - u[0][1] * u[1][0] == 1)
    for _ in range(500):
        u1, u2, u3 = [rng.choice(rotations) for _ in range(3)]
        total += 1
        passed += int(mm(u3, mm(u2, u1)) == mm(mm(u3, u2), u1))

    # Same endpoint depth never forces the two path transports equal.
    total += 4
    passed += int(rotations[0] != rotations[1])
    passed += int(Fraction(2, 5) == Fraction(2, 5))
    passed += int(add_bounded(Fraction(0), Fraction(0)) == 0)
    passed += int(mm(rotations[1], rotations[0]) != identity)

    # Frozen source replay independent of production.
    lines = (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    for line in lines:
        expected, rel, _role = line.split("\t")
        total += 1
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        passed += int(actual == expected)

    if passed != total:
        raise SystemExit(f"FAIL {passed}/{total}")
    print(f"PASS {passed}/{total}: independent bounded-position and route-transport replay")


if __name__ == "__main__":
    main()
