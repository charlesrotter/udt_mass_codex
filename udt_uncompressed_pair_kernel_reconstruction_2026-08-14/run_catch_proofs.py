#!/usr/bin/env python3
"""Fail-closed hostile mutations for omitted live channels and a reciprocal sign."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "CATCH_PROOF_RESULT.json"


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(2)] for i in range(2)]


def scale(c, a):
    return [[c * a[i][j] for j in range(2)] for i in range(2)]


def tr(a):
    return [[a[j][i] for j in range(2)] for i in range(2)]


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(2)), F(0)) for j in range(2)] for i in range(2)]


def zero():
    return [[F(0), F(0)], [F(0), F(0)]]


ETA = [[F(-1), F(0)], [F(0), F(1)]]


def h(B, Q, S, Y, Z):
    U = mul(B, Y)
    A = mul(Q, add(mul(S, Y), Z))
    return add(mul(mul(tr(U), ETA), U), mul(tr(A), A))


def line(base, direction, t):
    return h(*[add(base[i], scale(t, direction[i])) for i in range(5)])


def centered_exact_for_one_channel(base, direction):
    # With exactly one matrix live, h(t) is quadratic, so this centered derivative is exact.
    return scale(F(1, 2), sub(line(base, direction, F(1)), line(base, direction, F(-1))))


def nonzero(a):
    return any(x != 0 for row in a for x in row)


def main():
    B = [[F(2), F(1, 3)], [F(0), F(3, 2)]]
    Q = [[F(3, 2), F(1, 5)], [F(0), F(4, 3)]]
    S = [[F(1, 5), -F(1, 7)], [F(2, 9), F(1, 6)]]
    Y = [[F(1), F(1, 10)], [-F(1, 8), F(1)]]
    Z = [[F(1, 12), -F(1, 11)], [F(1, 13), F(1, 14)]]
    base = [B, Q, S, Y, Z]
    E00 = [[F(1), F(0)], [F(0), F(0)]]
    names = ["dB_sign_flip", "omit_dQ", "omit_dS", "omit_dY", "omit_dZ"]
    caught = {}
    residuals = {}
    for idx, name in enumerate(names):
        direction = [zero(), zero(), zero(), zero(), zero()]
        direction[idx] = E00
        truth = centered_exact_for_one_channel(base, direction)
        if idx == 0:
            mutant = scale(F(-1), truth)
        else:
            mutant = zero()
        residual = sub(truth, mutant)
        caught[name] = nonzero(residual)
        residuals[name] = [[str(x) for x in row] for row in residual]

    passed = all(caught.values())
    result = {
        "schema": "udt.uncompressed_pair_evaluator.catch.v1",
        "method": "exact Fraction centered derivatives with one live matrix channel",
        "caught": caught,
        "residuals": residuals,
        "passed": passed,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
