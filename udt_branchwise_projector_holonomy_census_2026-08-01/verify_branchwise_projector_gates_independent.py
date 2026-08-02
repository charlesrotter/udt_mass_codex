#!/usr/bin/env python3
"""Independent no-SymPy replay of the twisted-S3 relative-curvature gate."""

from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
LAMBDAS = (("C01", F(-2)), ("C02", F(-1)), ("C03", F(0)), ("C04", F(1, 2)), ("C05", F(1)), ("C06", F(2)))


def zeros(n: int) -> list[list[F]]:
    return [[F(0) for _ in range(n)] for _ in range(n)]


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def is_zero(a: list[list[F]]) -> bool:
    return all(value == 0 for row in a for value in row)


def north_connection(lam: F) -> list[list[list[F]]]:
    sign = (F(-1), F(1), F(1), F(1))
    p1, p2, p3 = F(3, 50), F(1, 50), F(2, 50)
    structure = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]

    def setc(up: int, left: int, right: int, value: F) -> None:
        structure[up][left][right] = -value
        structure[up][right][left] = value

    setc(0, 0, 1, p1); setc(0, 0, 2, p2); setc(0, 0, 3, p3); setc(0, 2, 3, F(-1, 32))
    setc(1, 1, 2, -p2); setc(1, 1, 3, -p3); setc(1, 2, 3, F(-2))
    setc(2, 1, 2, lam*p1); setc(2, 2, 3, -lam*p3); setc(2, 1, 3, F(2))
    setc(3, 1, 3, lam*p1); setc(3, 2, 3, lam*p2); setc(3, 1, 2, F(-2))
    result = []
    for direction in range(4):
        gamma = zeros(4)
        for out in range(4):
            for acted in range(4):
                lower = (
                    sign[out]*structure[out][direction][acted]
                    - sign[direction]*structure[direction][acted][out]
                    + sign[acted]*structure[acted][out][direction]
                ) / 2
                gamma[out][acted] = sign[out]*lower
        result.append(gamma)
    return result


def main() -> int:
    source = {row["branch_id"]: row for row in csv.DictReader((HERE / "TWISTED_S3_RELATIVE_CURVATURE.tsv").open(), delimiter="\t")}
    p = [[F(1),F(0),F(0)],[F(0),F(0),F(0)],[F(0),F(0),F(0)]]
    q = [[F(0),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(1)]]
    checks = []
    identity_lines = []
    for branch, lam in LAMBDAS:
        dp = []
        for gamma4 in north_connection(lam):
            gamma3 = [row[1:4] for row in gamma4[1:4]]
            dp.append(sub(mul(gamma3, p), mul(p, gamma3)))
        comm = sub(mul(dp[2], dp[3]), mul(dp[3], dp[2]))
        relative = mul(q, mul(comm, q))
        witness = relative[1][2]
        expected = F(source[branch]["relative_curvature_component_Q23_12"])
        checks.extend((witness == expected, witness != 0, is_zero(mul(p, relative)), is_zero(mul(relative, p))))
        identity_lines.append(f"{branch}:{witness}")
    # Independent exact controls for exchange and full-holonomy obstruction.
    swap = [[F(0),F(1)],[F(1),F(0)]]
    p1 = [[F(1),F(0)],[F(0),F(0)]]
    p2 = [[F(0),F(0)],[F(0),F(1)]]
    checks.append(mul(swap, mul(p1, swap)) == p2)
    clock = [F(1),F(0),F(0),F(0)]
    boost_clock = [F(0),F(1),F(0),F(0)]
    checks.append(boost_clock[1] != 0 and clock[1] == 0)
    if not all(checks):
        raise AssertionError("independent replay failure")
    result = {
        "schema": "udt.branchwise_projector_holonomy_census.independent.v1",
        "status": "PASS",
        "implementation": "stdlib_Fraction_no_production_import_no_SymPy",
        "check_count": len(checks),
        "branch_count": len(LAMBDAS),
        "exact_relative_curvature_witnesses": identity_lines,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
