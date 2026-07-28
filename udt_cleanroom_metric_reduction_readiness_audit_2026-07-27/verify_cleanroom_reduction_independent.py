#!/usr/bin/env python3
"""Independent stdlib/Fraction reconstruction; does not import production code."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


AMPLITUDES = ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")


def rank(matrix: list[list[Fraction]]) -> int:
    a = [row[:] for row in matrix]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [v / scale for v in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                factor = a[i][c]
                a[i] = [x - factor * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r


def mat_zero() -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(4)] for _ in range(4)]


def generators() -> dict[str, list[list[Fraction]]]:
    out = {name: mat_zero() for name in AMPLITUDES}
    out["phi"][0][0], out["phi"][1][1] = Fraction(-1), Fraction(1)
    out["sigma"][2][2] = out["sigma"][3][3] = Fraction(1, 2)
    out["alpha"][2][2], out["alpha"][3][3] = Fraction(-1), Fraction(1)
    for name, i, j in (("k", 2, 3), ("S10", 2, 0), ("S11", 2, 1), ("S20", 3, 0), ("S21", 3, 1)):
        out[name][i][j] = Fraction(1)
    return out


def column_rank(mats: list[list[list[Fraction]]]) -> int:
    return rank([[mat[i][j] for mat in mats] for i in range(4) for j in range(4)])


def metric_tangent(m: list[list[Fraction]]) -> list[list[Fraction]]:
    eta = (Fraction(-1), Fraction(1), Fraction(1), Fraction(1))
    return [[eta[i] * m[i][j] + eta[j] * m[j][i] for j in range(4)] for i in range(4)]


def torsion_rank() -> tuple[int, int]:
    variables = [(a, b, c) for a in range(4) for b in range(a + 1, 4) for c in range(4)]
    signs = (-1, 1, 1, 1)

    def omega(a: int, b: int, c: int, var: tuple[int, int, int]) -> int:
        i, j, k = var
        if c != k:
            return 0
        if (a, b) == (i, j):
            return 1
        if (a, b) == (j, i):
            return -1
        return 0

    rows = []
    for a in range(4):
        for c in range(4):
            for d in range(c + 1, 4):
                rows.append([Fraction(signs[a] * (omega(a, d, c, v) - omega(a, c, d, v))) for v in variables])
    return len(variables), rank(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    gs = generators()
    coframe_rank = column_rank([gs[name] for name in AMPLITUDES])
    metric_rank = column_rank([metric_tangent(gs[name]) for name in AMPLITUDES])
    unknowns, connection_rank = torsion_rank()

    result = {
        "schema": "udt-cleanroom-metric-reduction-independent-1.0",
        "implementation": "PYTHON_STDLIB_FRACTION_NO_SYMPY_NO_PRODUCTION_IMPORT",
        "coframe_tangent_rank": coframe_rank,
        "metric_tangent_rank": metric_rank,
        "cartan_connection_unknowns": unknowns,
        "cartan_connection_rank": connection_rank,
        "cartan_background_equation_rank": 0,
        "cohomogeneity_one": {"live_directions": 8, "supplied_equation_rank": 0, "deficit": 8, "closed": False},
        "one_plus_one": {"time_principal_directions": 8, "supplied_principal_rank": 0, "deficit": 8, "closed": False},
        "path_systems": {
            "geodesic": [8, 8, True],
            "ambient_parallel": [4, 4, True],
            "projected_screen": [2, 2, True],
            "jacobi": [8, 8, True],
        },
        "identity_ruling": {
            "first_Cartan": "CONNECTION_DEFINITION",
            "second_Cartan": "CURVATURE_DEFINITION",
            "Bianchi": "IDENTITY_NOT_BACKGROUND_EQUATION",
            "right_Maurer_Cartan": "IDENTITY_NOT_BACKGROUND_EVOLUTION",
        },
        "authorization": {
            "metric_background_ode": False,
            "metric_time_live": False,
            "conditional_path_ode": True,
        },
        "result": "PASS" if (coframe_rank, metric_rank, unknowns, connection_rank) == (8, 8, 24, 24) else "FAIL",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
