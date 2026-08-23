#!/usr/bin/env python3
"""Independent direct-product verification of the G238 exact witness and ledger."""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent


def as_fraction(record: dict[str, object]) -> Fraction:
    return Fraction(int(record["numerator"]), int(record["denominator"]))


def main() -> None:
    result = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    roots = [Fraction(index, 11) for index in range(12)]
    point = Fraction(1, 22)

    # This route does not construct polynomial coefficients. It uses the exact product and
    # logarithmic-derivative identities at a point that is not a root.
    q = Fraction(1)
    for root in roots:
        q *= point - root
    reciprocal_sum = sum((Fraction(1, point - root) for root in roots), Fraction(0))
    reciprocal_square_sum = sum(
        (Fraction(1, (point - root) ** 2) for root in roots), Fraction(0)
    )
    q_prime = q * reciprocal_sum
    q_second = q * (reciprocal_sum**2 - reciprocal_square_sum)

    counterfamily = result["counterfamily"]
    assert q == as_fraction(counterfamily["q"])
    assert q_prime == as_fraction(counterfamily["q_prime"])
    assert q_second == as_fraction(counterfamily["q_second"])
    assert q != 0 and q_prime != 0 and q_second != 0

    rows = list(csv.DictReader((PACKAGE / "OPERATOR_TYPE_LEDGER.tsv").open(), delimiter="\t"))
    by_stage = {row["stage"]: row for row in rows}
    assert len(rows) == 15 and len(by_stage) == 15
    for stage in ("Q02", "Q03", "Q04", "Q09", "Q10", "Q11"):
        assert by_stage[stage]["status"] == "OPEN"
    assert by_stage["Q15"]["status"] == "QUERY_TYPING_INCOMPLETE"
    for stage in ("Q05", "Q06", "Q07"):
        assert "DERIVED_CONDITIONAL" in by_stage[stage]["status"]

    forbidden = ("P1", "X_max", "LCDM", "Lambda-CDM", "preferred_feature")
    assert not any(token in json.dumps(result) for token in forbidden)
    assert result["boss_outcomes_opened"] is False
    assert result["profile_or_feature_fit_performed"] is False

    print(
        "PASS: independent direct-product witness, 15-row operator typing, "
        "conditional evaluator ownership, and no-outcome/no-fit gates"
    )


if __name__ == "__main__":
    main()
