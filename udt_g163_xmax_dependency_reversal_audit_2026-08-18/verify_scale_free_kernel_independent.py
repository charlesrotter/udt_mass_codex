#!/usr/bin/env python3
"""Independent stdlib exact replay for G163; no SymPy imports."""

from __future__ import annotations

import csv
import hashlib
import json
import random
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTCOME = "SCALE_FREE_KERNEL_CLOSES__XMAX_IS_DIMENSIONAL_NULL_DIRECTION__DEPENDENCY_REVERSAL_REQUIRED"


def chi_from_ratio(q: Fraction) -> Fraction:
    return (1 - q) / (1 + q)


def main() -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 26
    for row in sources:
        payload = (ROOT / row["path"]).read_bytes()
        assert len(payload) == int(row["bytes"])
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]

    rng = random.Random(163)
    trials = 1200
    for _ in range(trials):
        T = Fraction(rng.randint(1, 1000), rng.randint(1, 1000))
        L = Fraction(rng.randint(1, 1000), rng.randint(1, 1000))
        q = T / L
        chi = (L - T) / (L + T)
        assert chi == chi_from_ratio(q)
        assert (1 - chi) / (1 + chi) == q
        assert -1 < chi < 1

        q2 = Fraction(rng.randint(1, 1000), rng.randint(1, 1000))
        c2 = chi_from_ratio(q2)
        assert chi_from_ratio(q * q2) == (chi + c2) / (1 + chi * c2)
        assert chi_from_ratio(1 / q) == -chi

        scale = Fraction(rng.randint(1, 1000), rng.randint(1, 1000))
        Ts, Ls = scale * T, scale * L
        assert (Ls - Ts) / (Ls + Ts) == chi
        assert Ts / Ls == q
        assert (Ts * Ls) ** 2 == scale**4 * (T * L) ** 2

        # This only confirms the independently encoded algebra omits the after-the-fact X label.
        native = (q, chi, chi_from_ratio(q * q2), -chi)
        for X in (Fraction(1), Fraction(2), Fraction(17, 3)):
            assert (q, chi, chi_from_ratio(q * q2), -chi) == native

    with (HERE / "DEPENDENCY_LEDGER_PREREG.tsv").open(newline="", encoding="utf-8") as handle:
        prereg_ledger = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "DEPENDENCY_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        final_ledger = list(csv.DictReader(handle, delimiter="\t"))
    expected_ids = [f"G{i}" for i in range(135, 155)]
    assert [row["id"] for row in prereg_ledger] == expected_ids
    assert [row["id"] for row in final_ledger] == expected_ids
    assert all(row["scale_free_survivor"] and row["xmax_dependent_content"] for row in prereg_ledger)
    assert all(row["final_class"] and row["conditional_or_open_dimensional_content"] for row in final_ledger)

    result = {
        "status": "PASS",
        "registered_outcome_class": OUTCOME,
        "source_count": len(sources),
        "fraction_trials": trials,
        "dependency_rows": len(final_ledger),
        "xmax_absent_from_independently_encoded_algebra": True,
        "xmax_absence_is_structural_not_independent_identifiability_evidence": True,
        "dimensionless_bound_derived": True,
        "dimensionful_xmax_derived": False,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
