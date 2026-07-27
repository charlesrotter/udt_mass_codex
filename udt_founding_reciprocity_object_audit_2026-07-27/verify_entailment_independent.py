#!/usr/bin/env python3
"""Independent algebra/source-free replay of the load-bearing entailment distinction."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def main() -> int:
    # Rational pointwise version of the local model at x=0: g=diag(-1,1), dg_x=diag(2,2).
    ginv = [[Fraction(-1), Fraction(0)], [Fraction(0), Fraction(1)]]
    dg = [[[Fraction(0) for _ in range(2)] for _ in range(2)] for _ in range(2)]
    dg[1][0][0] = Fraction(2)
    dg[1][1][1] = Fraction(2)
    gamma = [[[Fraction(0) for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for a in range(2):
        for b in range(2):
            for c in range(2):
                gamma[a][b][c] = sum(
                    Fraction(1, 2) * ginv[a][d] * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                    for d in range(2)
                )
    X = [[Fraction(-1), Fraction(0)], [Fraction(0), Fraction(1)]]
    nabla_t_X_t_x = sum(gamma[0][0][d] * X[d][1] - gamma[d][0][1] * X[0][d] for d in range(2))
    assert gamma[0][0][1] == -1 and nabla_t_X_t_x == -2

    # Independent finite character check at rational positive diagonal values.
    # D(log 2)=diag(1/2,2), D(log 3)=diag(1/3,3), so composition is D(log 6).
    d2 = [[Fraction(1, 2), 0], [0, Fraction(2)]]
    d3 = [[Fraction(1, 3), 0], [0, Fraction(3)]]
    d6 = [[Fraction(1, 6), 0], [0, Fraction(6)]]
    K = [[0, 1], [1, 0]]
    assert matmul(d2, d3) == d6
    assert matmul([[d2[j][i] for j in range(2)] for i in range(2)], matmul(K, d2)) == K

    result = {
        "schema": "udt-founding-reciprocity-object-independent-1.0",
        "status": "PASS",
        "method": "stdlib_fraction_coordinate_connection_plus_finite_character",
        "Gamma_t_t_x_at_origin": str(gamma[0][0][1]),
        "nabla_dt_X_t_x_at_origin": str(nabla_t_X_t_x),
        "founding_character_composes": True,
        "founding_character_preserves_pairing": True,
        "founding_packet_entails_parallelism": False,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
