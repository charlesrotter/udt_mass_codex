#!/usr/bin/env python3
"""Independent implicit-midpoint transfer check for the G286 witness."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


EPSILON = 0.2
J = [[0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0],
     [-1.0, 0.0, 0.0, 0.0], [0.0, -1.0, 0.0, 0.0]]


def switch(u: float) -> float:
    if u <= 0.0:
        return 0.0
    return math.exp(-(u ** -2))


def eye() -> list[list[float]]:
    return [[float(i == j) for j in range(4)] for i in range(4)]


def mul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(x*y for x, y in zip(a[i], (b[k][j] for k in range(4))))
             for j in range(4)] for i in range(4)]


def inv(a: list[list[float]]) -> list[list[float]]:
    aug = [row[:] + e for row, e in zip(a, eye())]
    for col in range(4):
        pivot = max(range(col, 4), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        p = aug[col][col]
        if abs(p) < 1e-15:
            raise ArithmeticError("singular midpoint matrix")
        aug[col] = [x/p for x in aug[col]]
        for r in range(4):
            if r == col:
                continue
            f = aug[r][col]
            aug[r] = [aug[r][j] - f*aug[col][j] for j in range(8)]
    return [row[4:] for row in aug]


def a_matrix(u: float, active: bool) -> list[list[float]]:
    q = EPSILON * switch(u) if active else 0.0
    return [[0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0],
            [-q, 0.0, 0.0, 0.0], [0.0, q, 0.0, 0.0]]


def midpoint(active: bool, steps: int) -> list[list[float]]:
    h = 2.0 / steps
    y = eye()
    for k in range(steps):
        u = -1.0 + (k + 0.5)*h
        a = a_matrix(u, active)
        minus = [[float(i == j) - 0.5*h*a[i][j] for j in range(4)] for i in range(4)]
        plus = [[float(i == j) + 0.5*h*a[i][j] for j in range(4)] for i in range(4)]
        y = mul(mul(inv(minus), plus), y)
    return y


def trans(a: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def normdiff(a: list[list[float]], b: list[list[float]]) -> float:
    return max(abs(a[i][j]-b[i][j]) for i in range(4) for j in range(4))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--production", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=40000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    production = json.loads(args.production.read_text(encoding="utf-8"))
    active = midpoint(True, args.steps)
    flat = midpoint(False, args.steps)
    defect = normdiff(mul(trans(active), mul(J, active)), J)
    cross = normdiff(active, production["active_transfer"])
    separation = normdiff(active, flat)
    result = {
        "method": "implicit_midpoint_cayley",
        "steps": args.steps,
        "independent_symplectic_defect": defect,
        "production_independent_transfer_difference": cross,
        "independent_future_transfer_difference_from_flat": separation,
    }
    result["pass"] = defect < 2e-8 and cross < 2e-6 and separation > 1e-5
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
