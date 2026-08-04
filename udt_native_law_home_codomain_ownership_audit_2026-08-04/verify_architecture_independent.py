#!/usr/bin/env python3
"""Independent stdlib/Fraction replay; does not import production code or SymPy."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return sum(a[i][i] for i in range(len(a)))


def transpose(a):
    return [list(row) for row in zip(*a)]


def main() -> None:
    zero = F(0)
    one = F(1)
    P01 = [[one, zero, zero, zero], [zero, one, zero, zero], [zero, zero, zero, zero], [zero, zero, zero, zero]]
    P02 = [[one, zero, zero, zero], [zero, zero, zero, zero], [zero, zero, one, zero], [zero, zero, zero, zero]]
    R = [[one, zero, zero, zero], [zero, zero, one, zero], [zero, one, zero, zero], [zero, zero, zero, one]]
    A = [[F(2), zero, zero, zero], [zero, F(3), zero, zero], [zero, zero, F(5), zero], [zero, zero, zero, F(7)]]
    Ac = [[F(2), zero, zero, zero], [zero, F(4), zero, zero], [zero, zero, F(4), zero], [zero, zero, zero, F(7)]]
    Pp = [[zero] * 4 for _ in range(4)]
    Pp[1][2] = Pp[2][1] = F(-1, 2)
    B = [[zero] * 4 for _ in range(4)]
    B[1][2] = B[2][1] = one
    checks = []
    checks.append(mm(P01, P01) == P01)
    checks.append(mm(P02, P02) == P02)
    checks.append(transpose(P01) == P01)
    checks.append(transpose(P02) == P02)
    checks.append(mm(mm(R, P01), R) == P02)
    checks.append(P01 != P02)
    checks.append([tr(mm(P01, A)), tr(mm(P02, A))] == [F(5), F(7)])
    checks.append(tr(A) == F(17))
    checks.append(tr(mm(mm(mm(R, P01), R), mm(mm(R, A), R))) == tr(mm(P01, A)))
    checks.append(tr(mm(mm(R, A), R)) == tr(A))
    checks.append(tr(mm(Pp, B)) == F(-1))
    checks.append(tr(Pp) == zero)
    checks.append((A[1][1] - A[2][2]) * Pp[1][2] == one)
    checks.append(mm(mm(R, Ac), R) == Ac)
    checks.append(mm(mm(R, P01), R) == P02 and P01 != P02)
    # Polynomial identity for the registered conditional SNe shape:
    # (1+z)^2 [1-(1+z)^-2] = z(z+2), checked at exact rational probes.
    for z in (F(0), F(1, 3), F(1), F(7, 2)):
        u = one + z
        checks.append(u * u * (one - one / (u * u)) == z * (z + 2))
    checks.append(len({"clock", "areal", "optical", "proper_pair"}) == 4)
    checks.append(tr(mm(P01, A)) != tr(mm(P02, A)))
    checks.append(tr(mm(Pp, B)) != zero)
    failed = [index for index, value in enumerate(checks, start=1) if not value]
    assert not failed, failed
    result = {
        "status": "PASS",
        "exact_checks": len(checks),
        "reciprocal_pair_query_values": ["5", "7"],
        "basic_trace": "17",
        "branch_selector_chain_term": "-1",
        "collision_limits_distinct": True,
        "sne_conditional_shape": "z*(z + 2)",
        "sne_readout_slots": ["clock", "areal", "optical", "proper_pair"],
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
