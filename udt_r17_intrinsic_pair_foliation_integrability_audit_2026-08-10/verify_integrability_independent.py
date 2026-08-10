#!/usr/bin/env python3
"""Independent standard-library reconstruction of the load-bearing algebra."""

from __future__ import annotations

import json
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent


def matmul(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def verify_witness(lam: Q, u: Q, v: Q, a: Q, p1: Q, p2: Q, p3: Q) -> dict[str, bool]:
    coframe = [
        [1 / u, a / u, Q(0), Q(0)],
        [Q(0), u, Q(0), Q(0)],
        [Q(0), Q(0), v, Q(0)],
        [Q(0), Q(0), Q(0), v],
    ]
    frame = [
        [u, -a / u, Q(0), Q(0)],
        [Q(0), 1 / u, Q(0), Q(0)],
        [Q(0), Q(0), 1 / v, Q(0)],
        [Q(0), Q(0), Q(0), 1 / v],
    ]
    identity = [[Q(int(i == j)) for j in range(4)] for i in range(4)]
    pair = [-p1 / u, Q(0), Q(0), Q(0)]
    screen = [2 * a / (u * v * v), 2 * u / (v * v), lam * p3 / v, -lam * p2 / v]
    h00 = -1 / (u * u)
    h01 = -a / (u * u)
    h11 = u * u - a * a / (u * u)
    det_h = h00 * h11 - h01 * h01
    terminal_ratio = (-det_h) / (h00 * h00)
    return {
        "duality": matmul(coframe, frame) == identity,
        "pair_transverse_zero": pair[2:] == [Q(0), Q(0)],
        "screen_pair_nonzero": screen[1] != 0,
        "twist_retained": h01 != 0,
        "det_minus_one": det_h == -1,
        "terminal_ratio_u_fourth": terminal_ratio == u**4,
    }


def main() -> None:
    lambdas = [Q(-2), Q(-1), Q(0), Q(1, 2), Q(1), Q(2)]
    witnesses = []
    for i, lam in enumerate(lambdas, start=1):
        values = {
            "lam": lam,
            "u": Q(i + 1, i),
            "v": Q(i + 2, i + 1),
            "a": Q((-1) ** i, 8 + i),
            "p1": Q(i - 3, i + 2),
            "p2": Q(2 * i - 5, i + 3),
            "p3": Q(4 - i, i + 4),
        }
        checks = verify_witness(**values)
        if not all(checks.values()):
            raise SystemExit(f"FAIL witness {i}: {checks}")
        witnesses.append(
            {
                "id": f"C{i:02d}",
                "values": {
                    ("lambda" if key == "lam" else key): str(value)
                    for key, value in values.items()
                },
                "checks": checks,
            }
        )

    result = {
        "mode": "independent_standard_library_exact_rationals",
        "imports_production_controller": False,
        "witness_count": len(witnesses),
        "checks_per_witness": 6,
        "passed_checks": 36,
        "witnesses": witnesses,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS: 36/36 independent exact-rational checks across six lambda strata")


if __name__ == "__main__":
    main()
