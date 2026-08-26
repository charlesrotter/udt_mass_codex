#!/usr/bin/env python3
"""Implementation-distinct exact-Fraction verification for G262."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def verify() -> dict[str, object]:
    assertions = 0
    cases = 0

    for i in range(1, 1001):
        r = Fraction((i % 29) + 1, (i % 11) + 2)
        n = Fraction((i % 17) + 2, (i % 13) + 2)
        np = Fraction((i % 19) - 9, (i % 7) + 3)
        npp = Fraction((i % 23) - 11, (i % 5) + 4)

        f = n * n
        fp = 2 * n * np
        fpp = 2 * (np * np + n * npp)
        mu = r * (1 - f) / 2
        mup = (1 - f - r * fp) / 2
        mupp = -fp - r * fpp / 2

        e0 = r * fp + f - 1
        e1 = r * fp + r * r * fpp / 2
        apar = (r * r * fpp - r * fp) / 2
        aperp = 1 - f + r * fp / 2
        ahat = fp / (2 * n)

        checks = (
            ahat == np,
            f == 1 - 2 * mu / r,
            e0 == -2 * mup,
            e1 == -r * mupp,
            apar + aperp == e1 - e0,
            apar == -r * mupp + 3 * mup - 3 * mu / r,
            aperp == 3 * mu / r - mup,
        )
        if not all(checks):
            raise AssertionError(f"metric hierarchy failed at case {i}")
        assertions += len(checks)

        q1 = Fraction((i % 31) + 1, (i % 37) + 2)
        q2 = Fraction((i % 41) + 1, (i % 43) + 2)
        chi = (1 - q1 * q1) / (1 + q1 * q1)
        pair_checks = (
            (1 - chi) == q1 * q1 * (1 + chi),
            q1 * (1 / q1) == 1,
            (q1 * q2) * (1 / q2) == q1,
        )
        if not all(pair_checks):
            raise AssertionError(f"pair hierarchy failed at case {i}")
        assertions += len(pair_checks)
        cases += 1

    # Preregistered profile control at one exact point: a=1/2, r=1.
    r = Fraction(1)
    a = Fraction(1, 2)
    f = 1 + a * r * r / (1 + r * r)
    fp = 2 * a * r / (1 + r * r) ** 2
    mu = r * (1 - f) / 2
    if f <= 0 or fp == 0 or mu == 0:
        raise AssertionError("nontrivial preregistered profile control failed")
    assertions += 3

    return {
        "implementation": "python_standard_library_fraction_no_production_import_no_result_read",
        "case_count": cases,
        "assertion_count": assertions,
        "status": "PASS",
        "scope": "exact point-jet and positive-pair algebra; ownership follows frozen source ledger",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
