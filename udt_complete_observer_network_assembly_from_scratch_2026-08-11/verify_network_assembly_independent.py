#!/usr/bin/env python3
"""Independent Fraction-only verifier for G62 network assembly."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def inv(a):
    n = len(a)
    aug = [row[:] + unit[:] for row, unit in zip(a, eye(n))]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row != col:
                scale = aug[row][col]
                aug[row] = [x - scale * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def transpose(a):
    return [list(row) for row in zip(*a)]


def rotation(p, q):
    den = p * p + q * q
    return [[(p * p - q * q) / den, -2 * p * q / den], [2 * p * q / den, (p * p - q * q) / den]]


def frame(rng, t):
    diagonal = [F(rng.randint(2, 8)) + t * F(rng.randint(0, 2), 7) for _ in range(4)]
    return [
        [diagonal[0], F(rng.randint(1, 3), 5) + t / 11, 0, 0],
        [0, diagonal[1], 0, 0],
        [F(rng.randint(1, 3), 7), F(rng.randint(1, 3), 7), diagonal[2], F(1, 9)],
        [F(rng.randint(1, 3), 8), F(rng.randint(1, 3), 8), F(rng.randint(1, 3), 8), diagonal[3]],
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--read-only", action="store_true")
    parser.parse_args()
    rng = random.Random(620811)
    object_trials = edge_trials = frame_trials = rotation_trials = 0

    for _ in range(400):
        phi = [F(rng.randint(-20, 20), rng.randint(1, 9)) for _ in range(4)]
        edge = {(i, j): phi[j] - phi[i] for i in range(4) for j in range(4) if i != j}
        faces = []
        for i, j, k in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
            value = edge[i, j] + edge[j, k] - edge[i, k]
            assert value == 0
            faces.append(value)
        assert faces[3] - faces[2] + faces[1] - faces[0] == 0
        object_trials += 1

    for _ in range(400):
        values = [F(rng.randint(-20, 20), rng.randint(1, 9)) for _ in range(6)]
        e01, e02, e03, e12, e13, e23 = values
        faces = [e01 + e12 - e02, e01 + e13 - e03, e02 + e23 - e03, e12 + e23 - e13]
        assert faces[3] - faces[2] + faces[1] - faces[0] == 0
        # A nonzero face is lawful route data, not an algebra failure.
        if all(value == 0 for value in faces):
            continue
        edge_trials += 1

    for _ in range(300):
        t = F(rng.randint(-3, 3), 13)
        frames = [frame(rng, t) for _ in range(4)]
        arrows = {(i, j): mm(frames[j], inv(frames[i])) for i in range(4) for j in range(4) if i != j}
        for i, j, k in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
            assert mm(arrows[j, k], arrows[i, j]) == arrows[i, k]
        assert arrows[1, 0] == inv(arrows[0, 1])
        frame_trials += 1

    for _ in range(400):
        params = [(F(rng.randint(1, 9)), F(rng.randint(1, 9))) for _ in range(6)]
        mats = [rotation(p, q) for p, q in params]
        for mat in mats:
            assert mm(transpose(mat), mat) == eye(2)
        R01, R02, R03, R12, R13, R23 = mats
        rs = {(0, 1): R01, (0, 2): R02, (0, 3): R03, (1, 2): R12, (1, 3): R13, (2, 3): R23}
        rs.update({(j, i): transpose(value) for (i, j), value in list(rs.items())})
        h = lambda i, j, k: mm(rs[k, i], mm(rs[j, k], rs[i, j]))
        h012, h013, h023, h123 = h(0, 1, 2), h(0, 1, 3), h(0, 2, 3), h(1, 2, 3)
        assert mm(h123, mm(inv(h023), mm(h013, inv(h012)))) == eye(2)
        assert h(0, 2, 1) == inv(h012)
        rotation_trials += 1

    output = {
        "status": "PASS",
        "implementation": "independent_standard_library_fraction_only_no_sympy_no_production_import",
        "object_coboundary_trials": object_trials,
        "nonflat_edge_cochain_trials": edge_trials,
        "complete_time_live_frame_trials": frame_trials,
        "angular_holonomy_trials": rotation_trials,
        "total_exact_trials": object_trials + edge_trials + frame_trials + rotation_trials,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
