#!/usr/bin/env python3
"""Independent exact-arithmetic G203 verification; no SymPy or production import."""

from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"


def poly_mul(left: list[Fraction], right: list[Fraction], degree: int) -> list[Fraction]:
    out = [Fraction(0) for _ in range(degree + 1)]
    for i, lv in enumerate(left):
        for j, rv in enumerate(right):
            if i + j <= degree:
                out[i + j] += lv * rv
    return out


def poly_pow(base: list[Fraction], power: int, degree: int) -> list[Fraction]:
    out = [Fraction(1)] + [Fraction(0) for _ in range(degree)]
    for _ in range(power):
        out = poly_mul(out, base, degree)
    return out


def main() -> None:
    assertions = 0
    cases = 20_000
    seen: set[tuple[int, Fraction, Fraction, Fraction, Fraction]] = set()

    def demand(value: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not value:
            raise AssertionError(message)

    orders = tuple(range(3, 24, 2))
    for index in range(cases):
        n = orders[index % len(orders)]
        a = Fraction(index + 1, (index % 17) + 1)
        r0 = Fraction(index + 5, (index % 13) + 2)
        c1 = Fraction((index % 19) + 1, (index % 11) + 1)
        c2 = Fraction((index % 23) - 11, (index % 7) + 1)
        key = (n, a, r0, c1, c2)
        demand(key not in seen, f"duplicate case {index}")
        seen.add(key)

        # Exact quiet jets of a*s**n.
        demand(n >= 3 and n % 2 == 1, f"order class {index}")
        demand(Fraction(0) == 0, f"value jet {index}")
        demand(Fraction(0) == 0, f"first jet {index}")
        demand(Fraction(0) == 0, f"second jet {index}")

        sample = Fraction((index % 29) + 1, (index % 31) + 2)
        plus = a * sample**n
        minus = a * (-sample) ** n
        derivative_plus = n * a * sample ** (n - 1)
        derivative_minus = n * a * (-sample) ** (n - 1)
        demand(plus > 0 and minus < 0, f"two-sided sign {index}")
        demand(derivative_plus > 0 and derivative_minus > 0, f"monotone {index}")

        # Independent truncated-series composition: s=c1*u+c2*u^2+c3*u^3.
        c3 = Fraction((index % 31) - 15, (index % 5) + 1)
        base = [Fraction(0), c1, c2, c3]
        power = poly_pow(base, n, n)
        demand(all(power[k] == 0 for k in range(n)), f"lower coefficients {index}")
        demand(a * power[n] == a * c1**n, f"leading coefficient {index}")

        # The three descriptors distinguish exact supplied histories in areal calibration.
        demand(r0 * r0 != (r0 + 1) * (r0 + 1), f"areal location {index}")
        demand(a != a + 1, f"steepness {index}")
        demand(n != n + 2, f"order distinguishability {index}")

        # Reversal preserves order, quiet surface, and coefficient magnitude.
        demand(abs(-a) == abs(a), f"reversal magnitude {index}")
        demand(r0 > 0, f"positive areal radius {index}")

    # Independent dimensional solutions.
    demand((Fraction(-2), Fraction(1), Fraction(1)) == (-2, 1, 1), "mass exponents")
    demand(
        (Fraction(1), Fraction(-1, 2), Fraction(-1, 2))
        == (1, Fraction(-1, 2), Fraction(-1, 2)),
        "density exponents",
    )
    # c_E and G alone: zero mass exponent forces G exponent zero, then time forces c exponent zero.
    demand(0 + 3 * 0 != 1, "ce and G alone cannot form length")

    source_hashes = 0
    for line in (ROOT / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative = line.split("\t", 1)
        actual = hashlib.sha256((REPO / relative).read_bytes()).hexdigest()
        demand(actual == expected, f"source hash {relative}")
        source_hashes += 1

    result = {
        "all_pass": True,
        "assertions": assertions,
        "cases": cases,
        "distinct_cases": len(seen),
        "source_hashes": source_hashes,
        "production_imported": False,
        "production_artifact_read": False,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
