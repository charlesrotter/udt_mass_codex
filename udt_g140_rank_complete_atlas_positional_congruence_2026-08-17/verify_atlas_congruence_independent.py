#!/usr/bin/env python3
"""Independent stdlib replay of the G140 witnesses."""

from __future__ import annotations

import hashlib
import itertools
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
FACES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))


def rank_float(matrix, tolerance=1e-12):
    a = [list(map(float, row)) for row in matrix]
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = max(range(pivot_row, rows), key=lambda r: abs(a[r][col]), default=pivot_row)
        if abs(a[pivot][col]) <= tolerance:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        lead = a[pivot_row][col]
        a[pivot_row] = [x / lead for x in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row and abs(a[r][col]) > tolerance:
                factor = a[r][col]
                a[r] = [a[r][j] - factor * a[pivot_row][j] for j in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def rank_fraction(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col] != 0), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        lead = a[pivot_row][col]
        a[pivot_row] = [x / lead for x in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row and a[r][col] != 0:
                factor = a[r][col]
                a[r] = [a[r][j] - factor * a[pivot_row][j] for j in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def design(vertices):
    rows = []
    lengths2 = {}
    for i, j in EDGES:
        r = tuple(vertices[j][k] - vertices[i][k] for k in range(3))
        x, y, z = r
        lengths2[(i, j)] = x*x + y*y + z*z
        rows.extend([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, x, y, z, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, x*x, 2*x*y, 2*x*z, y*y, 2*y*z, z*z],
        ])
    return rows, lengths2


def cycle_residuals_from_supplied_lift(lengths2):
    bar_phi = {edge: 0.25 * math.log(float(value)) for edge, value in lengths2.items()}
    delta = dict(bar_phi)  # independent replay of the registered increasing-label lift
    return [delta[(i, j)] + delta[(j, k)] - delta[(i, k)] for i, j, k in FACES]


def main() -> None:
    passed = 0
    total = 0

    right = (
        (Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    )
    regular = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.5, math.sqrt(3) / 2, 0.0),
        (0.5, math.sqrt(3) / 6, math.sqrt(2 / 3)),
    )
    right_design, right_l2 = design(right)
    regular_design, regular_l2 = design(regular)

    tests = [
        rank_float(right_design) == 10,
        rank_float(regular_design) == 10,
        list(right_l2.values()) == [Fraction(1), Fraction(1), Fraction(1), Fraction(2), Fraction(2), Fraction(2)],
        all(abs(float(v) - 1.0) < 1e-13 for v in regular_l2.values()),
        all(abs(r - math.log(2) / 4) < 1e-13 for r in cycle_residuals_from_supplied_lift(right_l2)),
        all(abs(r) < 1e-13 for r in cycle_residuals_from_supplied_lift(regular_l2)),
        abs(math.exp(-2 * (math.log(2) / 4)) - 1 / math.sqrt(2)) < 1e-13,
        all(
            not all(abs(value) < 1e-13 for value in (
                signs[0] * math.log(2) / 4,
                signs[1] * math.log(2) / 4,
                signs[2] * math.log(2) / 4,
                (signs[0] + signs[2] - signs[1]) * math.log(2) / 4,
            ))
            for signs in itertools.product((-1, 1), repeat=3)
        ),
    ]
    total += len(tests)
    passed += sum(tests)

    # Exact Fraction elimination independently confirms the rational witness rank.
    total += 1
    passed += int(rank_fraction(right_design) == 10)

    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, rel, _role = line.split("\t")
        total += 1
        passed += int(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == expected)

    if passed != total:
        raise SystemExit(f"FAIL {passed}/{total}")
    print(f"PASS {passed}/{total}: independent rank, geometry, cycle, and source replay")


if __name__ == "__main__":
    main()
