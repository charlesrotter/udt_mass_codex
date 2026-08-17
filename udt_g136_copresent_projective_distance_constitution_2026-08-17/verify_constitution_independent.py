#!/usr/bin/env python3
"""Independent stdlib numerical/source replay for G136; no SymPy imports."""

from __future__ import annotations

import hashlib
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def close(a: float, b: float, tol: float = 2.0e-13) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def mobius(a: float, b: float) -> float:
    return (a + b) / (1.0 + a * b)


def main() -> None:
    passed = 0
    total = 0

    def check(condition: bool) -> None:
        nonlocal passed, total
        total += 1
        if not condition:
            raise AssertionError(f"independent check {total} failed")
        passed += 1

    for k in (0.25, 1.0, 3.0):
        for a, b in ((-1.2, 0.4), (0.1, 0.7), (2.0, -0.3)):
            check(close(math.tanh(k * (a + b)), mobius(math.tanh(k * a), math.tanh(k * b))))

    for k in (0.25, 1.0, 3.0):
        h = 1.0e-6
        slope = (math.tanh(k * h) - math.tanh(-k * h)) / (2.0 * h)
        check(close(slope, k, 2.0e-10))

    for value in (-4.0, -0.5, 0.0, 0.5, 4.0):
        check(close(math.atanh(math.tanh(value)), value))

    manifest = {}
    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        path, digest, _ = line.split("\t", 2)
        manifest[path] = digest
    for path, expected in manifest.items():
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        check(actual == expected)

    check("physical_position_equals_chi\tOPEN" in (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8"))
    check("No canonization follows" in (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8"))
    print(f"PASS {passed}/{total}: independent numerical/source replay of composition, normalization, inverse, hashes, and guards")


if __name__ == "__main__":
    main()
