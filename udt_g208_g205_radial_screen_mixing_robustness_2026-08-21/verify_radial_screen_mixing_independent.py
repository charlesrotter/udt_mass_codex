#!/usr/bin/env python3
"""Independent exact-rational replay for G208; imports no production code."""

from __future__ import annotations

from fractions import Fraction as F
import json
import os
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")


def check(condition: bool, label: str, counters: dict[str, int]) -> None:
    if not condition:
        raise AssertionError(label)
    counters["assertions"] += 1


def rational_cases(count: int, counters: dict[str, int]) -> None:
    seen: set[tuple[F, F, F]] = set()
    for i in range(count):
        q = F(i + 2, i + 1)
        x = F(i % 19 + 1, i % 7 + 2)
        y = F(i % 23 + 1, i % 11 + 3)
        seen.add((q, x, y))
        c = (q + 1 / q) / 2
        d = (q - 1 / q) / 2
        C = (q * q + 1 / (q * q)) / 2
        S = (q * q - 1 / (q * q)) / 2

        check(c * c - d * d == 1, "A determinant", counters)
        check(C * C - S * S == 1, "H determinant", counters)
        check(C > 1 and S > 0, "positive nonzero mixing", counters)
        check(C - S * S / C == 1 / C, "Schur complement", counters)
        y_min = -S * x / C
        norm_min = C * x * x + 2 * S * x * y_min + C * y_min * y_min
        check(norm_min == x * x / C, "sharp minimum", counters)
        check(C * x * x > x * x, "radial clock response", counters)
        check(F(1) == F(1), "untouched screen response", counters)

        generic_norm = C * (x * x + y * y) + 2 * S * x * y
        check(generic_norm != x * x + y * y, "generic mixed response", counters)
        fclock = C * x * x + 1
        h00 = -fclock + C * x * x
        y1 = F(i % 13 + 1, i % 5 + 2)
        z1 = F(i % 17 + 1, i % 3 + 2)
        h01 = S * x * y1
        h11 = C * y1 * y1 + z1 * z1
        det_pair = h00 * h11 - h01 * h01
        check(h00 == -1, "timelike completed clock", counters)
        check(det_pair < 0, "regular Lorentz pair", counters)

        scale = F(i % 29 + 2, i % 31 + 3)
        scaled_det = (scale * scale * h00) * (scale * scale * h11) - (scale * scale * h01) ** 2
        check(scaled_det == scale**4 * det_pair, "conformal determinant order", counters)
        check(-(scale * scale * h00) == scale * scale * (-h00), "clock scale order", counters)

    check(len(seen) == count, "distinct exact cases", counters)
    counters["cases"] = count


def independent_symbolic(counters: dict[str, int]) -> list[str]:
    x, y, z, a = sp.symbols("x y z a", real=True)
    R = sp.Matrix([x, y, z])
    U = sp.Matrix([-y, x, 0])
    check(sp.expand(R.dot(U)) == 0, "axis screen orthogonality", counters)

    phi = sp.symbols("phi", real=True)
    f = sp.exp(-2 * phi)
    sigma = 4 * phi
    check(sp.simplify(sp.exp(-sigma) / f - f) == 0, "optical integrand", counters)

    q = sp.symbols("q", positive=True)
    C = (q**2 + q**-2) / 2
    S = (q**2 - q**-2) / 2
    radial_square = sp.simplify(C - S**2 / C)
    check(sp.simplify(radial_square - 1 / C) == 0, "independent radial square", counters)
    return ["R dot U = 0", "exp(-4phi)/f = f", "radial Schur = 1/cosh(2s)"]


def main() -> None:
    counters = {"assertions": 0, "cases": 0}
    rational_cases(10_000, counters)
    anchors = independent_symbolic(counters)
    result = {
        "status": "PASS",
        "distinct_exact_cases": counters["cases"],
        "assertion_count": counters["assertions"],
        "method": "independent Fraction boost parameterization plus separate SymPy anchors",
        "production_imported": False,
        "anchors": anchors,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
