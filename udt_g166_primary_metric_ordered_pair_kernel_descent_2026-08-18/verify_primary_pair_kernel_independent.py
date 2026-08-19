#!/usr/bin/env python3
"""Independent stdlib/Fraction verification for G166."""

from __future__ import annotations

import csv
import hashlib
import json
import random
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
getcontext().prec = 60


def dec(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def main() -> None:
    rng = random.Random(166)
    trials = 1200
    for _ in range(trials):
        T = Fraction(rng.randint(2, 17), rng.randint(1, 9))
        L = Fraction(rng.randint(2, 19), rng.randint(1, 9))
        beta = Fraction(rng.randint(-7, 7), rng.randint(2, 11))

        h00 = -(T * T)
        h01 = -(T * T) * beta
        h11 = L * L - T * T * beta * beta
        det = h00 * h11 - h01 * h01
        assert det == -(T * T * L * L)
        assert h01 / h00 == beta
        assert h11 - h01 * h01 / h00 == L * L
        assert h00 * h00 / (-det) == (T / L) ** 2

        scale = Fraction(rng.randint(1, 17), rng.randint(1, 13))
        hs00 = scale * scale * h00
        hs01 = scale * scale * h01
        hs11 = scale * scale * h11
        dets = hs00 * hs11 - hs01 * hs01
        assert hs00 * hs00 / (-dets) == h00 * h00 / (-det)

        q = T / L
        chi = (Fraction(1) - q) / (Fraction(1) + q)
        q_reverse = Fraction(1) / q
        chi_reverse = (Fraction(1) - q_reverse) / (Fraction(1) + q_reverse)
        assert chi_reverse == -chi

        q2 = Fraction(rng.randint(1, 17), rng.randint(1, 17))
        chi2 = (Fraction(1) - q2) / (Fraction(1) + q2)
        chi12 = (Fraction(1) - q * q2) / (Fraction(1) + q * q2)
        assert chi12 == (chi + chi2) / (Fraction(1) + chi * chi2)

        # Independent positive-square-root readout.
        q_decimal = (dec(h00 * h00 / (-det))).sqrt()
        assert abs(q_decimal - dec(T / L)) < Decimal("1e-50")

    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    assert len(rows) == 13
    for row in rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        assert actual == row["sha256"]

    result = {
        "status": "PASS",
        "exact_fraction_trials": trials,
        "source_hashes": len(rows),
        "imports_production": False,
        "checks": [
            "pair determinant and decomposition",
            "terminal ratio",
            "common-scale cancellation",
            "reversal",
            "matched-depth Mobius composition",
            "independent Decimal square-root readout",
        ],
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(f"PASS: {trials} independent exact Fraction trials; {len(rows)} source hashes")


if __name__ == "__main__":
    main()
