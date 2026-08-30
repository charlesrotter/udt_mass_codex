#!/usr/bin/env python3
"""Implementation-distinct exact Fraction verifier for G299."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent


def mdot(x: tuple[F, F, F], y: tuple[F, F, F]) -> F:
    return -x[0] * y[0] + x[1] * y[1] + x[2] * y[2]


def det3(columns: tuple[tuple[F, F, F], ...]) -> F:
    a, b, c = columns
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def projective(a: list[list[F]]) -> tuple[F, F, F]:
    return tuple(a[i][0] / a[0][0] for i in range(1, 4))


def main() -> None:
    rng = random.Random(2990829)
    cases = 20_000
    assertions = 0
    for _ in range(cases):
        rn = rng.randint(1, 500)
        rd = rng.randint(1, 500)
        wn = rng.choice([i for i in range(-50, 51) if i])
        wd = rng.randint(1, 100)
        r = F(rn, rd)
        w = F(wn, wd)
        gamma = (1 + r * r + r * r * w * w) / (2 * r)
        a = (-1 + r * r + r * r * w * w) / (2 * r)
        U = (gamma, a, w)
        clock = tuple(r * x for x in U)
        nT = (F(0), F(1), F(0))
        nL = (r - gamma, r - a, -w)

        assert mdot(U, U) == -1
        assert r * (gamma - a) == 1
        assert mdot(U, nL) == 0
        assert mdot(nL, nL) == 1
        assert mdot(clock, clock) == -r * r
        assert det3((clock, nT, nL)) == -r * r * w
        assert det3((clock, nT, nL)) != 0

        hT00, hT01, hT11 = mdot(clock, clock), mdot(clock, nT), mdot(nT, nT)
        hL00, hL01, hL11 = mdot(clock, clock), mdot(clock, nL), mdot(nL, nL)
        assert hT00 == hL00 == -r * r
        assert hT00 * hT11 - hT01 * hT01 < 0
        assert hL00 * hL11 - hL01 * hL01 == -r * r
        assertions += 10

    Bx = [[F(5, 4), F(3, 4), F(0), F(0)], [F(3, 4), F(5, 4), F(0), F(0)],
          [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    Bs = [[F(441, 359), F(0), F(200, 359), F(160, 359)], [F(0), F(1), F(0), F(0)],
          [F(200, 359), F(0), F(409, 359), F(40, 359)],
          [F(160, 359), F(0), F(40, 359), F(391, 359)]]
    rot = [[F(1), F(0), F(0), F(0)], [F(0), F(0), F(-1), F(0)],
           [F(0), F(1), F(0), F(0)], [F(0), F(0), F(0), F(1)]]
    BsR = matmul(Bs, rot)
    assert projective(Bs) == projective(BsR)
    assert projective(matmul(Bs, Bx)) != projective(matmul(BsR, Bx))
    assertions += 2

    result = {
        "status": "PASS",
        "method": "stdlib Fraction arithmetic with independent component formulas",
        "cases": cases,
        "assertions": assertions,
        "active_screen_planes_distinct": True,
        "registered_W1_clock_entry_shared": True,
        "projective_vector_not_composition_complete": True,
        "scope": "algebraic and factorization witnesses only; physical ownership is source-audited separately",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
