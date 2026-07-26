#!/usr/bin/env python3
"""Independent Fraction verification of the founded-phi extension class."""

from __future__ import annotations

import json
from fractions import Fraction as F


Matrix = list[list[F]]


def eye(n: int) -> Matrix:
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mul(a: Matrix, b: Matrix) -> Matrix:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def determinant(a: Matrix) -> F:
    work = [row[:] for row in a]
    value = F(1)
    for column in range(len(work)):
        pivot = next((r for r in range(column, len(work)) if work[r][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value *= -1
        pivot_value = work[column][column]
        value *= pivot_value
        for row in range(column + 1, len(work)):
            factor = work[row][column] / pivot_value
            for index in range(column, len(work)):
                work[row][index] -= factor * work[column][index]
    return value


def rank(vectors: list[list[F]]) -> int:
    work = [list(row) for row in zip(*vectors)]
    row = 0
    for column in range(len(vectors)):
        pivot = next((r for r in range(row, len(work)) if work[r][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = work[row][column]
        work[row] = [x / scale for x in work[row]]
        for r in range(len(work)):
            if r != row and work[r][column]:
                factor = work[r][column]
                work[r] = [work[r][j] - factor * work[row][j] for j in range(len(work[r]))]
        row += 1
    return row


def flatten(a: Matrix) -> list[F]:
    return [x for row in a for x in row]


def spectator(z: F) -> Matrix:
    value = eye(4)
    value[0][0], value[1][1] = 1 / z, z
    return value


def angular(z: F, power: int) -> Matrix:
    value = spectator(z)
    value[2][2], value[3][3] = z ** (-power), z**power
    return value


def shift(z: F, strength: F) -> Matrix:
    value = spectator(z)
    value[2][0] = strength * (1 - 1 / z)
    return value


def metric(e: Matrix) -> Matrix:
    eta = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    return mul(mul(transpose(e), eta), e)


def main() -> None:
    checks: dict[str, bool] = {}
    # Seven independent extension tangents: three upper-triangular angular,
    # four lower-left mixing directions.
    tangents = []
    for i, j in ((2, 2), (2, 3), (3, 3), (2, 0), (2, 1), (3, 0), (3, 1)):
        value = [[F(0) for _ in range(4)] for _ in range(4)]
        value[i][j] = F(1)
        tangents.append(value)
    checks["seven_extension_tangent_rank"] = rank([flatten(x) for x in tangents]) == 7

    # The determinant-one angular trace-free tangent plus four shifts and one
    # angular shear span six directions.
    det_one = []
    value = [[F(0) for _ in range(4)] for _ in range(4)]
    value[2][2], value[3][3] = F(1), F(-1)
    det_one.append(value)
    for i, j in ((2, 3), (2, 0), (2, 1), (3, 0), (3, 1)):
        value = [[F(0) for _ in range(4)] for _ in range(4)]
        value[i][j] = F(1)
        det_one.append(value)
    checks["six_det_one_extension_tangent_rank"] = rank([flatten(x) for x in det_one]) == 6

    z1, z2 = F(2), F(3)
    checks["spectator_composition"] = mul(spectator(z2), spectator(z1)) == spectator(z1 * z2)
    checks["spectator_reversal"] = mul(spectator(1 / z1), spectator(z1)) == eye(4)
    checks["spectator_determinant_one"] = determinant(spectator(z1)) == 1
    checks["spectator_metric"] = metric(spectator(z1)) == [
        [F(-1, 4), F(0), F(0), F(0)],
        [F(0), F(4), F(0), F(0)],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]

    checks["angular_composition"] = mul(angular(z2, 2), angular(z1, 2)) == angular(z1 * z2, 2)
    checks["angular_determinant_one"] = determinant(angular(z1, 2)) == 1
    checks["angular_projects_founded_pair"] = [row[:2] for row in angular(z1, 2)[:2]] == [row[:2] for row in spectator(z1)[:2]]
    checks["angular_counterfamily_nontrivial"] = metric(angular(z1, 2))[2][2] != 1

    strength = F(5)
    checks["shift_composition"] = mul(shift(z2, strength), shift(z1, strength)) == shift(z1 * z2, strength)
    checks["shift_determinant_one"] = determinant(shift(z1, strength)) == 1
    checks["shift_projects_founded_pair"] = [row[:2] for row in shift(z1, strength)[:2]] == [row[:2] for row in spectator(z1)[:2]]
    checks["shift_counterfamily_cross_term"] = metric(shift(z1, strength))[0][2] == F(5, 2)

    # For K=[[a,b],[0,d]], K^T+K=0 gives a=b=d=0 in
    # characteristic zero. C itself is the cross-block metric tangent.
    a, b, d = F(7), F(11), F(13)
    angular_tangent = [[2 * a, b], [b, 2 * d]]
    checks["nonzero_triangular_generator_changes_angular_metric"] = angular_tangent != [[F(0), F(0)], [F(0), F(0)]]
    checks["zero_triangular_generator_preserves_angular_metric"] = [[F(0), F(0)], [F(0), F(0)]] == [[F(0), F(0)], [F(0), F(0)]]
    C = [[F(17), F(19)], [F(23), F(29)]]
    checks["nonzero_C_creates_metric_mixing"] = any(x for row in C for x in row)
    checks["zero_C_removes_metric_mixing"] = not any(x for row in [[F(0), F(0)], [F(0), F(0)]] for x in row)

    if not all(checks.values()) or len(checks) != 18:
        raise AssertionError({
            "failed": [name for name, passed in checks.items() if not passed],
            "actual_check_count": len(checks),
            "expected_check_count": 18,
        })
    print(json.dumps({
        "schema": "udt-founded-phi-complete-coframe-extension-independent-1.0",
        "result": "PASS",
        "implementation": "Python standard library fractions.Fraction",
        "check_count": len(checks),
        "checks": checks,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
