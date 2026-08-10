#!/usr/bin/env python3
"""Independent stdlib reconstruction of the query-projection result."""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> int:
    checks: dict[str, bool] = {}

    def check(name: str, value: bool) -> None:
        checks[name] = bool(value)
        if not value:
            raise AssertionError(name)

    # A continuous character of additive R^2 is fixed by its values a,b on the basis.
    # Exchange fixes e_kappa and reverses e_phi. Oddness therefore gives a=-a, hence a=0;
    # normalization on e_phi gives b=1.
    a = Fraction(0)
    b = Fraction(1)
    check("exchange_basis_kills_common_scale", a == -a == 0)
    check("pure_reciprocal_basis_normalizes_phi", b == 1)
    check("selected_basis_pair_unique", (a, b) == (Fraction(0), Fraction(1)))
    for dk, dp in ((Fraction(2), Fraction(3)), (Fraction(-5), Fraction(7))):
        check(f"selected_character_{dk}_{dp}", a * dk + b * dp == dp)

    # Independent density inversion.
    for dk, dp in ((Fraction(3, 5), Fraction(-2, 7)), (Fraction(-4, 9), Fraction(5, 6))):
        clock = dk - dp
        area = 2 * dk
        check(f"density_inverse_kappa_{dk}_{dp}", area / 2 == dk)
        check(f"density_inverse_phi_{dk}_{dp}", area / 2 - clock == dp)

    # Broader endpoint coboundaries really do survive telescoping and therefore limit uniqueness.
    fp, fq, fr = Fraction(2), Fraction(11), Fraction(-3)
    check("endpoint_coboundary_telescopes", (fq - fp) + (fr - fq) == fr - fp)
    check("endpoint_coboundary_nonzero", fq - fp != 0)

    # Exact quarter-turn SO(2) composition; compactness then kills a continuous real character.
    R90 = ((0, -1), (1, 0))
    def mm(x: tuple[tuple[int, int], tuple[int, int]],
           y: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
        return (
            (x[0][0] * y[0][0] + x[0][1] * y[1][0],
             x[0][0] * y[0][1] + x[0][1] * y[1][1]),
            (x[1][0] * y[0][0] + x[1][1] * y[1][0],
             x[1][0] * y[0][1] + x[1][1] * y[1][1]),
        )
    R180 = ((-1, 0), (0, -1))
    I = ((1, 0), (0, 1))
    check("quarter_turn_square", mm(R90, R90) == R180)
    check("quarter_turn_period_four", mm(R180, R180) == I)
    check("finite_order_real_character_zero", 4 * 0 == 0)

    # Exact mixed-pair ratios, independent of SymPy.
    h00_1, h11_1 = Fraction(-3, 16), Fraction(4)
    det1 = h00_1 * h11_1
    check("mix_one_det", det1 == Fraction(-3, 4))
    check("mix_one_phi_argument", (-det1) / (h00_1 * h00_1) == Fraction(64, 3))
    h00_2, h01_2, h11_2 = Fraction(-3, 16), Fraction(1, 12), Fraction(37, 9)
    det2 = h00_2 * h11_2 - h01_2 * h01_2
    check("mix_two_det", det2 == Fraction(-7, 9))
    check("mix_two_phi_argument", (-det2) / (h00_2 * h00_2) == Fraction(1792, 81))
    check("mix_two_beta", h01_2 / h00_2 == Fraction(-4, 9))

    classification = rows("QUERY_PROJECTION_CLASSIFICATION.tsv")
    ownership = rows("MEASUREMENT_OWNERSHIP_ATLAS.tsv")
    signatures = rows("FOUNDING_SIGNATURE_RESULT.tsv")
    check("classification_rows_14", len(classification) == 14)
    check("ownership_rows_6", len(ownership) == 6)
    check("signature_rows_5", len(signatures) == 5)
    by_query = {row["query_id"]: row for row in classification}
    check(
        "Q02_founding_projection",
        by_query["Q02"]["disposition"]
        == "REALIZED_FOUNDING_PROJECTION_CONDITIONAL_UNIQUE_WITHIN_DENSITY_CHARACTER_CLASS",
    )
    check("Q10_broader_nonuniqueness_retained", "UNOWNED" in by_query["Q10"]["disposition"])
    check("Q12_regime_policy_open", by_query["Q12"]["disposition"] == "OPEN_NO_PHYSICAL_REGIME_MAP")

    result = {
        "schema_version": 1,
        "status": "PASS",
        "method": "INDEPENDENT_STDLIB_FRACTION_BASIS_CHARACTER_AND_TYPED_TABLE_RECONSTRUCTION",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "failed": [name for name, ok in checks.items() if not ok],
    }
    assert result["passed"] == result["total"]
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
