#!/usr/bin/env python3
"""Independent exact-rational G210 replay; imports no production code."""

from __future__ import annotations

from fractions import Fraction as F
import json
import os
from pathlib import Path


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")


def determinant(a: list[list[F]]) -> F:
    m = [row[:] for row in a]
    value = F(1)
    sign = 1
    for col in range(len(m)):
        pivot = next(i for i in range(col, len(m)) if m[i][col] != 0)
        if pivot != col:
            m[pivot], m[col] = m[col], m[pivot]
            sign *= -1
        p = m[col][col]
        value *= p
        for i in range(col + 1, len(m)):
            factor = m[i][col] / p
            for j in range(col + 1, len(m)):
                m[i][j] -= factor * m[col][j]
    return sign * value


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    m = [a[i][:] + [F(int(i == j)) for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if m[i][col] != 0)
        m[pivot], m[col] = m[col], m[pivot]
        p = m[col][col]
        m[col] = [x / p for x in m[col]]
        for i in range(n):
            if i == col:
                continue
            q = m[i][col]
            m[i] = [m[i][j] - q * m[col][j] for j in range(2 * n)]
    return [row[n:] for row in m]


def mmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def matvec(a: list[list[F]], x: list[F]) -> list[F]:
    return [sum((a[i][j] * x[j] for j in range(len(x))), F(0)) for i in range(len(a))]


def dot(x: list[F], y: list[F]) -> F:
    return sum((a * b for a, b in zip(x, y)), F(0))


def make_spd(i: int) -> list[list[F]]:
    p = F(i % 17 - 8, i % 7 + 2)
    q = F(i % 19 - 9, i % 11 + 3)
    r = F(i % 23 - 11, i % 13 + 4)
    d = (F(i % 29 + 1, i % 5 + 1), F(i % 31 + 2, i % 7 + 1), F(i % 37 + 3, i % 11 + 1))
    l = [[F(1), F(0), F(0)], [p, F(1), F(0)], [q, r, F(1)]]
    return [[sum((l[a][k] * d[k] * l[b][k] for k in range(3)), F(0)) for b in range(3)] for a in range(3)]


def check(ok: bool, label: str, state: dict[str, int]) -> None:
    if not ok:
        raise AssertionError(label)
    state["assertions"] += 1


def main() -> None:
    state = {"assertions": 0}
    seen: set[tuple[F, ...]] = set()
    for i in range(10_000):
        H = make_spd(i)
        Hinv = inverse(H)
        u = F(i % 97 + 1, i % 43 + 2)
        f = F(i % 41 + 1, i % 13 + 2)
        b = [F(i % 43 - 21, i % 17 + 3), F(i % 47 - 23, i % 19 + 4), F(i % 53 - 26, i % 23 + 5)]
        v = [F(i % 59 - 29, i % 29 + 6), F(i % 61 - 30, i % 31 + 7), F(i % 67 - 33, i % 37 + 8)]
        seen.add(tuple(sum(H, [])) + (u, f) + tuple(b) + tuple(v))

        K = [[u * H[a][c] for c in range(3)] for a in range(3)]
        Kinv = [[Hinv[a][c] / u for c in range(3)] for a in range(3)]
        Kb = matvec(K, b)
        g = [[F(0) for _ in range(4)] for _ in range(4)]
        g[0][0] = -f + dot(b, Kb)
        for j in range(3):
            g[0][j + 1] = Kb[j]
            g[j + 1][0] = Kb[j]
            for k in range(3):
                g[j + 1][k + 1] = K[j][k]
        gi = [[F(0) for _ in range(4)] for _ in range(4)]
        gi[0][0] = -1 / f
        for j in range(3):
            gi[0][j + 1] = b[j] / f
            gi[j + 1][0] = b[j] / f
            for k in range(3):
                gi[j + 1][k + 1] = Kinv[j][k] - b[j] * b[k] / f

        check(determinant(K) == u**3 * determinant(H), "spatial determinant", state)
        Kbar = [[K[a][c] / u for c in range(3)] for a in range(3)]
        check(determinant(Kbar) == determinant(H), "determinant-one remainder", state)
        check(determinant(g) == -f * u**3 * determinant(H), "ambient determinant", state)
        product = mmul(g, gi)
        for a in range(4):
            for c in range(4):
                check(product[a][c] == F(int(a == c)), "block inverse", state)
        check(gi[0][0] == -1 / f, "temporal dt", state)

        shifted = [v[j] + b[j] for j in range(3)]
        X = [F(1)] + v
        gx = dot(X, matvec(g, X))
        check(gx == -f + u * dot(shifted, matvec(H, shifted)), "scaled translated cone", state)
        center = [F(1)] + [-x for x in b]
        check(dot(center, matvec(g, center)) == -f, "cone center", state)

        a0 = F(i % 71 + 1, i % 41 + 2)
        w0 = [F(i % 73 - 36, i % 43 + 3), F(i % 79 - 39, i % 47 + 4), F(i % 83 - 41, i % 53 + 5)]
        J0 = [a0] + w0
        T2_direct = -dot(J0, matvec(g, J0))
        shifted_clock = [w0[j] + a0 * b[j] for j in range(3)]
        T2_expected = f * a0**2 - u * dot(shifted_clock, matvec(H, shifted_clock))
        check(T2_direct == T2_expected, "completed clock", state)
        euler = [a0] + [-a0 * x for x in b]
        check(-dot(euler, matvec(g, euler)) == f * a0**2, "Eulerian blind stratum", state)

        # Radial null algebra with u=a^2 represented rationally.
        energy = F(i % 101 + 1, i % 67 + 2)
        rdot2 = energy**2 / u
        check(-energy**2 / f + u * rdot2 / f == 0, "radial null identity", state)

    check(len(seen) == 10_000, "distinct exact cases", state)
    result = {
        "status": "PASS",
        "distinct_exact_cases": len(seen),
        "assertion_count": state["assertions"],
        "method": "independent Fraction SPD volume split, ADM inverse, translated cone, pair clock, and radial null replay",
        "production_imported": False,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
