#!/usr/bin/env python3
"""Independent exact-rational G209 replay; imports no production code."""

from __future__ import annotations

from fractions import Fraction as F
import json
import os
from pathlib import Path


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")


def det3(a: list[list[F]]) -> F:
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def matvec(a: list[list[F]], x: list[F]) -> list[F]:
    return [sum((a[i][j] * x[j] for j in range(3)), F(0)) for i in range(3)]


def dot(x: list[F], y: list[F]) -> F:
    return sum((u * v for u, v in zip(x, y)), F(0))


def check(condition: bool, label: str, counters: dict[str, int]) -> None:
    if not condition:
        raise AssertionError(label)
    counters["assertions"] += 1


def make_spd(i: int) -> list[list[F]]:
    # H=L D L^T with rational unit-lower L and positive diagonal D.
    p = F(i % 17 - 8, i % 7 + 2)
    q = F(i % 19 - 9, i % 11 + 3)
    r = F(i % 23 - 11, i % 13 + 4)
    d1 = F(i % 29 + 1, i % 5 + 1)
    d2 = F(i % 31 + 2, i % 7 + 1)
    d3 = F(i % 37 + 3, i % 11 + 1)
    l = [[F(1), F(0), F(0)], [p, F(1), F(0)], [q, r, F(1)]]
    return [
        [sum((l[a][k] * (d1, d2, d3)[k] * l[b][k] for k in range(3)), F(0)) for b in range(3)]
        for a in range(3)
    ]


def exact_cases(count: int, counters: dict[str, int]) -> None:
    seen: set[tuple[F, ...]] = set()
    for i in range(count):
        H = make_spd(i)
        f = F(i % 41 + 1, i % 13 + 2)
        b = [F(i % 43 - 21, i % 17 + 3), F(i % 47 - 23, i % 19 + 4), F(i % 53 - 26, i % 23 + 5)]
        v = [F(i % 59 - 29, i % 29 + 6), F(i % 61 - 30, i % 31 + 7), F(i % 67 - 33, i % 37 + 8)]
        seen.add(tuple(sum(H, [])) + tuple(b) + tuple(v) + (f, F(i)))
        Hb = matvec(H, b)
        Hv = matvec(H, v)
        shifted = [v[j] + b[j] for j in range(3)]
        Hshifted = matvec(H, shifted)

        check(H[0][0] > 0, "first Sylvester minor", counters)
        check(H[0][0] * H[1][1] - H[0][1] ** 2 > 0, "second Sylvester minor", counters)
        check(det3(H) > 0, "third Sylvester minor", counters)
        check(-f * det3(H) != 0, "Lorentz determinant", counters)
        expanded = -f + dot(v, Hv) + 2 * dot(v, Hb) + dot(b, Hb)
        check(expanded == -f + dot(shifted, Hshifted), "translated cone", counters)
        check(-f + dot([-x for x in b], matvec(H, [-x for x in b])) + 2 * dot([-x for x in b], Hb) + dot(b, Hb) == -f, "cone center", counters)

        a0 = F(i % 71 + 1, i % 41 + 2)
        w0 = [F(i % 73 - 36, i % 43 + 3), F(i % 79 - 39, i % 47 + 4), F(i % 83 - 41, i % 53 + 5)]
        pair_clock = f * a0 * a0 - dot([w0[j] + a0 * b[j] for j in range(3)], matvec(H, [w0[j] + a0 * b[j] for j in range(3)]))
        coordinate_clock = a0 * a0 * (f - dot(b, Hb))
        euler_clock = f * a0 * a0
        check(pair_clock == f * a0 * a0 - dot([w0[j] + a0 * b[j] for j in range(3)], matvec(H, [w0[j] + a0 * b[j] for j in range(3)])), "generic pair clock", counters)
        check(coordinate_clock == f * a0 * a0 - dot([a0 * b[j] for j in range(3)], matvec(H, [a0 * b[j] for j in range(3)])), "coordinate clock", counters)
        check(euler_clock == f * a0 * a0 - dot([F(0), F(0), F(0)], matvec(H, [F(0), F(0), F(0)])), "Eulerian clock", counters)

        # Independently parameterized radial Hamiltonian identity.
        fr = F(i % 89 + 2, i % 59 + 3)
        br = F(i % 97 - 48, i % 61 + 4)
        radius = F(i % 101 + 2, i % 67 + 5)
        energy = F(i % 103 + 1, i % 71 + 6)
        angular = F(i % 107 + 1, i % 73 + 7)
        momentum = F(i % 109 - 54, i % 79 + 8)
        A = fr - br * br / fr
        constraint = A * momentum * momentum - 2 * br * energy * momentum / fr - energy * energy / fr + angular * angular / (radius * radius)
        radial_velocity = A * momentum - br * energy / fr
        check(radial_velocity * radial_velocity - (energy * energy - A * angular * angular / (radius * radius)) == A * constraint, "radial Hamiltonian identity", counters)

    check(len(seen) == count, "distinct exact cases", counters)
    counters["cases"] = count


def main() -> None:
    counters = {"assertions": 0, "cases": 0}
    exact_cases(10_000, counters)
    result = {
        "status": "PASS",
        "distinct_exact_cases": counters["cases"],
        "assertion_count": counters["assertions"],
        "method": "independent Fraction SPD factorization, translated cones, pair clocks, and radial Hamiltonian",
        "production_imported": False,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
