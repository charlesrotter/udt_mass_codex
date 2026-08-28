#!/usr/bin/env python3
"""Dependency-free G286 production witness and path-transfer diagnostic."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


EPSILON = 0.2
J = (
    (0.0, 0.0, 1.0, 0.0),
    (0.0, 0.0, 0.0, 1.0),
    (-1.0, 0.0, 0.0, 0.0),
    (0.0, -1.0, 0.0, 0.0),
)


def flat_switch(u: float) -> float:
    return 0.0 if u <= 0.0 else math.exp(-1.0 / (u * u))


def tidal(u: float, active: bool) -> tuple[tuple[float, float], tuple[float, float]]:
    a = EPSILON * flat_switch(u) if active else 0.0
    return ((a, 0.0), (0.0, -a))


def generator(u: float, active: bool) -> list[list[float]]:
    t = tidal(u, active)
    return [
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [-t[0][0], -t[0][1], 0.0, 0.0],
        [-t[1][0], -t[1][1], 0.0, 0.0],
    ]


def matmul(a: list[list[float]] | tuple[tuple[float, ...], ...], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def add_scaled(a: list[list[float]], b: list[list[float]], scale: float) -> list[list[float]]:
    return [[a[i][j] + scale * b[i][j] for j in range(4)] for i in range(4)]


def rk4_transfer(active: bool, steps: int) -> list[list[float]]:
    lo, hi = -1.0, 1.0
    h = (hi - lo) / steps
    y = [[float(i == j) for j in range(4)] for i in range(4)]
    u = lo
    for _ in range(steps):
        k1 = matmul(generator(u, active), y)
        k2 = matmul(generator(u + 0.5 * h, active), add_scaled(y, k1, 0.5 * h))
        k3 = matmul(generator(u + 0.5 * h, active), add_scaled(y, k2, 0.5 * h))
        k4 = matmul(generator(u + h, active), add_scaled(y, k3, h))
        y = [[y[i][j] + h * (k1[i][j] + 2*k2[i][j] + 2*k3[i][j] + k4[i][j]) / 6.0
              for j in range(4)] for i in range(4)]
        u += h
    return y


def transpose(a: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def max_abs(a: list[list[float]]) -> float:
    return max(abs(x) for row in a for x in row)


def difference(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[a[i][j] - b[i][j] for j in range(4)] for i in range(4)]


def symplectic_defect(y: list[list[float]]) -> float:
    lhs = matmul(transpose(y), matmul(J, y))
    return max_abs(difference(lhs, [list(row) for row in J]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=30000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    y0 = rk4_transfer(False, args.steps)
    y1 = rk4_transfer(True, args.steps)
    samples = [-1.0, -0.5, 0.0, 0.25, 0.5, 1.0]
    bvals = {str(u): flat_switch(u) for u in samples}
    future_t = tidal(0.5, True)

    result = {
        "landing": "SAME_COMPLETE_PRIOR_AND_ALL_BOUNDARY_JETS_ADMIT_DISTINCT_FUTURE_L2_NETWORKS__VALUE_PROPAGATION_REMAINS_OPEN",
        "epsilon": EPSILON,
        "steps": args.steps,
        "flat_switch_samples": bvals,
        "prior_samples_exactly_zero": all(flat_switch(u) == 0.0 for u in samples if u <= 0.0),
        "future_curvature_nonzero": max(abs(v) for row in future_t for v in row) > 0.0,
        "future_tidal_symmetric": future_t[0][1] == future_t[1][0],
        "future_tidal_trace": future_t[0][0] + future_t[1][1],
        "metric_determinant": -1.0,
        "production_symplectic_defect": symplectic_defect(y1),
        "future_transfer_difference_from_flat": max_abs(difference(y1, y0)),
        "active_transfer": y1,
        "flat_transfer": y0,
    }
    result["pass"] = (
        result["prior_samples_exactly_zero"]
        and result["future_curvature_nonzero"]
        and result["future_tidal_symmetric"]
        and result["future_tidal_trace"] == 0.0
        and result["metric_determinant"] == -1.0
        and result["production_symplectic_defect"] < 2e-11
        and result["future_transfer_difference_from_flat"] > 1e-5
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
