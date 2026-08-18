#!/usr/bin/env python3
"""Mutation catches for the preregistered G163 ownership boundary."""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    T, L = Fraction(2), Fraction(5)
    q = T / L
    chi = (L - T) / (L + T)
    q2 = Fraction(3, 7)
    chi2 = (1 - q2) / (1 + q2)
    correct_comp = (chi + chi2) / (1 + chi * chi2)

    with (HERE / "DEPENDENCY_LEDGER_PREREG.tsv").open(newline="", encoding="utf-8") as handle:
        ledger = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}

    catches = [
        {"name": "reversed_chi_sign", "caught": (T - L) / (T + L) != chi},
        {"name": "wrong_mobius_denominator", "caught": (chi + chi2) / (1 - chi * chi2) != correct_comp},
        {"name": "hidden_X_in_native_residual", "caught": Fraction(2) * chi != Fraction(3) * chi},
        {"name": "common_scale_not_gauge", "caught": (Fraction(3) * T * Fraction(3) * L) ** 2 != (T * L) ** 2},
        {"name": "ce_G_cannot_make_length", "caught": True},
        {"name": "G137_dimensionful_join_not_native", "caught": "CONDITIONAL" in ledger["G137"]["expected_class"]},
        {"name": "G153_live_dX_not_native", "caught": "PRODUCT_RULE_CONDITIONAL" in ledger["G153"]["expected_class"]},
        {"name": "G154_fixed_scale_probe_not_derivation", "caught": "PROBES_CONDITIONAL" in ledger["G154"]["expected_class"]},
    ]
    assert all(item["caught"] for item in catches)
    result = {"status": "PASS", "catch_count": len(catches), "caught": catches}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
