#!/usr/bin/env python3
"""Independent exact-Fraction replay for G211; imports no production code."""

from __future__ import annotations

from fractions import Fraction as F
import json
import os
from pathlib import Path


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def matvec(a: list[list[F]], x: list[F]) -> list[F]:
    return [sum((a[i][j] * x[j] for j in range(len(x))), F(0)) for i in range(len(a))]


def dot(x: list[F], y: list[F]) -> F:
    return sum((a * b for a, b in zip(x, y)), F(0))


def determinant(a: list[list[F]]) -> F:
    m = [row[:] for row in a]
    out = F(1)
    for col in range(len(m)):
        pivot = next(i for i in range(col, len(m)) if m[i][col] != 0)
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            out = -out
        p = m[col][col]
        out *= p
        for i in range(col + 1, len(m)):
            factor = m[i][col] / p
            for j in range(col + 1, len(m)):
                m[i][j] -= factor * m[col][j]
    return out


def inverse3(a: list[list[F]]) -> list[list[F]]:
    aug = [a[i][:] + [F(int(i == j)) for j in range(3)] for i in range(3)]
    for col in range(3):
        pivot = next(i for i in range(col, 3) if aug[i][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        p = aug[col][col]
        aug[col] = [x / p for x in aug[col]]
        for i in range(3):
            if i == col:
                continue
            factor = aug[i][col]
            aug[i] = [aug[i][j] - factor * aug[col][j] for j in range(6)]
    return [row[3:] for row in aug]


def check(condition: bool, message: str, state: dict[str, int]) -> None:
    if not condition:
        raise AssertionError(message)
    state["assertions"] += 1


def main() -> None:
    state = {"assertions": 0}
    seen: set[tuple[F, ...]] = set()

    # Independent fixed-basis checks.
    check(F(1) * F(-1) - F(0) * F(3) == -1, "common-relative rank", state)
    check(F(1) * F(-1) - F(3) * F(1) == -4, "volume-width rank", state)

    for i in range(10_000):
        den = i % 89 + 3
        f = F(i % 97 + 1, den)
        u = F(i % 101 + 2, i % 43 + 2)
        z = F(i % 103 + 3, i % 47 + 3)
        c = u
        r = z / u

        L = [
            [F(i % 11 + 1, 7), F(0), F(0)],
            [F(i % 13 - 6, 17), F(i % 17 + 2, 11), F(0)],
            [F(i % 19 - 9, 23), F(i % 23 - 11, 29), F(i % 29 + 3, 13)],
        ]
        H = matmul(L, transpose(L))
        Hinv = inverse3(H)
        b = [F(i % 31 - 15, 19), F(i % 37 - 18, 23), F(i % 41 - 20, 29)]
        v = [F(i % 43 - 21, 31), F(i % 47 - 23, 37), F(i % 53 - 26, 41)]
        a0 = F(i % 59 + 1, i % 31 + 2)
        w0 = [F(i % 61 - 30, 43), F(i % 67 - 33, 47), F(i % 71 - 35, 53)]

        key = (f, u, z, *b, *v, a0, *w0)
        seen.add(key)

        Hb = matvec(H, b)
        bHb = dot(b, Hb)
        g = [[-u * f + z * bHb] + [z * x for x in Hb]]
        for row in range(3):
            g.append([z * Hb[row]] + [z * H[row][col] for col in range(3)])

        det_expected = -u * f * z**3 * determinant(H)
        check(determinant(g) == det_expected, "ADM determinant", state)

        gi = [[-1 / (u * f)] + [x / (u * f) for x in b]]
        for row in range(3):
            gi.append(
                [b[row] / (u * f)]
                + [Hinv[row][col] / z - b[row] * b[col] / (u * f) for col in range(3)]
            )
        product = matmul(g, gi)
        for row in range(4):
            for col in range(4):
                check(product[row][col] == F(int(row == col)), "ADM inverse", state)

        check(gi[0][0] == -1 / (u * f), "temporal dt", state)
        shifted = [v[j] + b[j] for j in range(3)]
        X = [F(1)] + v
        check(dot(X, matvec(g, X)) == -u * f + z * dot(shifted, matvec(H, shifted)), "cone", state)
        center = [F(1)] + [-x for x in b]
        check(dot(center, matvec(g, center)) == -u * f, "cone center", state)
        check(u / z == 1 / r, "common factor cancels width", state)
        check(u * z**3 == c**4 * r**3, "four-volume factor", state)

        relative_g = [[entry / c for entry in row] for row in g]
        check(relative_g[0][0] == -f + r * bHb, "common-relative factor", state)
        check(z == c * r, "basis reconstruction", state)

        J0 = [a0] + w0
        T2_direct = -dot(J0, matvec(g, J0))
        shifted_clock = [w0[j] + a0 * b[j] for j in range(3)]
        T2_expected = u * f * a0**2 - z * dot(shifted_clock, matvec(H, shifted_clock))
        check(T2_direct == T2_expected, "completed clock", state)
        check(T2_expected == c * (f * a0**2 - r * dot(shifted_clock, matvec(H, shifted_clock))), "pair factor", state)
        euler = [a0] + [-a0 * x for x in b]
        check(-dot(euler, matvec(g, euler)) == u * f * a0**2, "Eulerian relative blind", state)

        energy = F(i % 73 + 1, i % 37 + 2)
        rdot2 = energy**2 / (u * z)
        check(-energy**2 / (u * f) + z * rdot2 / f == 0, "radial null", state)

    check(len(seen) == 10_000, "distinct exact cases", state)
    result = {
        "status": "PASS",
        "distinct_exact_cases": len(seen),
        "assertion_count": state["assertions"],
        "method": "independent Fraction ADM determinant/inverse, scalar basis, cone, pair, and radial-null replay",
        "production_imported": False,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
