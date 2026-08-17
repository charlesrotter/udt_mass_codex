#!/usr/bin/env python3
"""Independent stdlib numerical/source replay for G137."""

from __future__ import annotations

import hashlib
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def close(a: float, b: float, tol: float = 2.0e-13) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def frozen_source_bytes(path: str) -> bytes:
    payload = (ROOT / path).read_bytes()
    if path != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return payload
    frozen = []
    for line in payload.splitlines(keepends=True):
        frozen.append(line)
        if line.startswith(b"G136\t"):
            return b"".join(frozen)
    raise AssertionError("G136 row absent from append-only premise registry")


def main() -> None:
    passed = 0
    total = 0

    def check(condition: bool) -> None:
        nonlocal passed, total
        total += 1
        if not condition:
            raise AssertionError(f"independent check {total} failed")
        passed += 1

    depths = (-8.0, -1.25, -0.1, 0.0, 0.1, 1.25, 8.0)
    for p in depths:
        q = math.exp(-2.0 * p)
        xi = math.tanh(p)
        check(close(xi, (1.0 - q) / (1.0 + q)))
        check(abs(xi) < 1.0)

    for p, r in ((-1.2, 0.4), (0.1, 0.7), (2.0, -0.3)):
        a, b = math.tanh(p), math.tanh(r)
        check(close(math.tanh(p + r), (a + b) / (1.0 + a * b)))

    for p in (-3.0, -0.2, 0.2, 3.0):
        xi = math.tanh(p)
        check(close(math.atanh(xi), p))
        check(close(math.tanh(-p), -xi))

    a = 1.0 / 3.0
    same = abs((a + a) / (1.0 + a * a))
    opposite = abs((a - a) / (1.0 - a * a))
    check(close(same, 3.0 / 5.0))
    check(close(opposite, 0.0))
    check(not close(same, opposite))

    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        path, expected, _ = line.split("\t", 2)
        check(hashlib.sha256(frozen_source_bytes(path)).hexdigest() == expected)

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    check("CANON.md` canonization" in prereg)
    check("proper_length_areal_radius_signal_distance\tOPEN" in ledger)
    check("pair_realization_and_history\tOPEN" in ledger)
    print(f"PASS {passed}/{total}: independent numerical/source replay and ownership guards")


if __name__ == "__main__":
    main()
