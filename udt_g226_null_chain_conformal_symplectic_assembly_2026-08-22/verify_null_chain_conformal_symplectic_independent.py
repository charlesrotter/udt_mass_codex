#!/usr/bin/env python3
"""Independent exact-Fraction replay for G226; imports no production code."""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction as F
from pathlib import Path


Matrix = list[list[F]]
I2: Matrix = [[F(1), F(0)], [F(0), F(1)]]
Z2: Matrix = [[F(0), F(0)], [F(0), F(0)]]
OMEGA: Matrix = [
    [F(0), F(0), F(1), F(0)],
    [F(0), F(0), F(0), F(1)],
    [F(-1), F(0), F(0), F(0)],
    [F(0), F(-1), F(0), F(0)],
]


def mm(a: Matrix, b: Matrix) -> Matrix:
    rows, inner, cols = len(a), len(b), len(b[0])
    return [[sum((a[i][k] * b[k][j] for k in range(inner)), F(0)) for j in range(cols)] for i in range(rows)]


def mt(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def madd(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def msub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def msmul(s: F, a: Matrix) -> Matrix:
    return [[s * x for x in row] for row in a]


def eye(n: int) -> Matrix:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def block(a: Matrix, b: Matrix, c: Matrix, d: Matrix) -> Matrix:
    return [ar + br for ar, br in zip(a, b)] + [cr + dr for cr, dr in zip(c, d)]


def diag_phase(q: Matrix) -> Matrix:
    return block(q, Z2, Z2, q)


def free(b: Matrix) -> Matrix:
    return block(I2, b, Z2, I2)


def lens(c: Matrix) -> Matrix:
    return block(I2, Z2, c, I2)


def clock_scale(w: F) -> Matrix:
    return [[F(1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), w, F(0)], [F(0), F(0), F(0), w]]


def clock_scale_inv(w: F) -> Matrix:
    return clock_scale(F(1, 1) / w)


def rotation(t: F, reflect: bool = False) -> Matrix:
    d = F(1) + t * t
    q = [[(F(1) - t * t) / d, -F(2) * t / d], [F(2) * t / d, (F(1) - t * t) / d]]
    if reflect:
        q = mm(q, [[F(-1), F(0)], [F(0), F(1)]])
    return q


def det(a: Matrix) -> F:
    work = [row[:] for row in a]
    out = F(1)
    n = len(work)
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col] != 0), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            out = -out
        p = work[col][col]
        out *= p
        for row in range(col + 1, n):
            if work[row][col] == 0:
                continue
            factor = work[row][col] / p
            for j in range(col, n):
                work[row][j] -= factor * work[col][j]
    return out


def symplectic_defect(m: Matrix, multiplier: F = F(1)) -> Matrix:
    return msub(mm(mm(mt(m), OMEGA), m), msmul(multiplier, OMEGA))


def is_zero(a: Matrix) -> bool:
    return all(x == 0 for row in a for x in row)


def symmetric_random(rng: random.Random) -> Matrix:
    def rf() -> F:
        return F(rng.randint(-4, 4), rng.randint(1, 5))

    a, b, c = rf(), rf(), rf()
    return [[a, b], [b, c]]


def random_rotation(rng: random.Random) -> Matrix:
    num = rng.choice([i for i in range(-5, 6) if i != 0])
    den = rng.randint(1, 6)
    return rotation(F(num, den), reflect=bool(rng.getrandbits(1)))


def require(condition: bool, label: str) -> int:
    if not condition:
        raise AssertionError(label)
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=226_822)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("INDEPENDENT_VERIFICATION.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    assertions = 0
    noncommuting = 0
    for case in range(args.cases):
        f1 = mm(lens(symmetric_random(rng)), mm(free(symmetric_random(rng)), lens(symmetric_random(rng))))
        f2 = mm(free(symmetric_random(rng)), mm(lens(symmetric_random(rng)), free(symmetric_random(rng))))
        assertions += require(is_zero(symplectic_defect(f1)), f"affine_symplectic_1_{case}")
        assertions += require(is_zero(symplectic_defect(f2)), f"affine_symplectic_2_{case}")

        wa, wbi = F(rng.randint(1, 9)), F(rng.randint(10, 18))
        wbo, wc = F(rng.randint(2, 10)), F(rng.randint(11, 19))
        r1, r2 = wa / wbi, wbo / wc
        m1 = mm(clock_scale_inv(wbi), mm(f1, clock_scale(wa)))
        m2 = mm(clock_scale_inv(wc), mm(f2, clock_scale(wbo)))
        assertions += require(is_zero(symplectic_defect(m1, r1)), f"edge_multiplier_1_{case}")
        assertions += require(is_zero(symplectic_defect(m2, r2)), f"edge_multiplier_2_{case}")

        cv = random_rotation(rng)
        vertex = diag_phase(cv)
        assertions += require(is_zero(symplectic_defect(vertex)), f"vertex_symplectic_{case}")
        chain = mm(m2, mm(vertex, m1))
        rchain = r2 * r1
        assertions += require(is_zero(symplectic_defect(chain, rchain)), f"chain_multiplier_{case}")
        assertions += require(det(chain) == rchain * rchain, f"chain_det_{case}")

        qa, qbi, qbo, qc = (random_rotation(rng) for _ in range(4))
        ga, gbi, gbo, gc = map(diag_phase, (qa, qbi, qbo, qc))
        m1g = mm(mt(gbi), mm(m1, ga))
        vg = mm(mt(gbo), mm(vertex, gbi))
        m2g = mm(mt(gc), mm(m2, gbo))
        chain_g = mm(m2g, mm(vg, m1g))
        assertions += require(chain_g == mm(mt(gc), mm(chain, ga)), f"middle_gauge_{case}")
        assertions += require(is_zero(symplectic_defect(chain_g, rchain)), f"gauged_multiplier_{case}")

        gamma = F(rng.randint(2, 9), rng.randint(1, 7))
        rg, rgi = clock_scale(gamma), clock_scale_inv(gamma)
        f1s = mm(rg, mm(f1, rgi))
        m1s = mm(clock_scale_inv(gamma * wbi), mm(f1s, clock_scale(gamma * wa)))
        assertions += require(m1s == m1, f"affine_rescale_{case}")

        if chain != mm(vertex, mm(m2, m1)):
            noncommuting += 1

    a = [[F(-1), F(0)], [F(0), F(1)]]
    b = [[F(0), F(0)], [F(0), F(1)]]
    caustic = block(a, b, Z2, a)
    assertions += require(is_zero(symplectic_defect(caustic)), "caustic_symplectic")
    assertions += require(det(b) == 0, "caustic_position_singular")
    assertions += require(det(caustic) == 1, "caustic_full_invertible")

    h2 = [[F(0), F(-1)], [F(1), F(0)]]
    hphase = diag_phase(h2)
    assertions += require(is_zero(symplectic_defect(hphase)), "octant_phase_symplectic")
    assertions += require(hphase != eye(4), "octant_phase_nonidentity")
    assertions += require(h2[0][1] != 0 and h2[1][0] != 0, "octant_not_scalar")
    assertions += require(noncommuting > 0, "ordered_products_noncommute")

    result = {
        "package": "G226",
        "implementation": "independent_standard_library_fraction",
        "seed": args.seed,
        "cases": args.cases,
        "assertions": assertions,
        "noncommuting_cases": noncommuting,
        "status": "PASS",
        "claims": [
            "affine edge phases symplectic",
            "clock-normalized edge multiplier equals r",
            "two-edge multiplier composes",
            "independent middle O(2) gauges cancel",
            "affine-generator rescaling cancels",
            "singular position block does not destroy full phase",
            "G225 octant holonomy embeds nontrivially in phase",
        ],
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
