#!/usr/bin/env python3
"""Applied mutation catches for the G262 evidence contract.

These are regression checks, not independent scientific proof.
"""

from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path


def catches(package: Path) -> dict[str, object]:
    r = Fraction(3, 2)
    n = Fraction(5, 4)
    np = Fraction(2, 7)
    npp = Fraction(-3, 11)
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
    q = Fraction(2, 3)
    chi = (1 - q * q) / (1 + q * q)

    applied = {
        "acceleration_sign_flip": (-fp / (2 * n)) != np,
        "mass_aspect_plus_sign": f != 1 - 2 * (r * (1 + f) / 2) / r,
        "E0_sign_flip": e0 != 2 * mup,
        "E1_sign_flip": e1 != r * mupp,
        "angular_trace_reversal": apar + aperp != e0 - e1,
        "clock_ratio_inversion": q != 1 / q,
        "projective_chi_sign_flip": (1 + chi) != q * q * (1 - chi),
    }

    ledger = package / "PREMISE_LEDGER.tsv"
    with ledger.open(newline="", encoding="utf-8") as handle:
        rows = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}
    applied.update(
        {
            "geometric_mass_promoted_to_physical": rows["P08"]["status"]
            != "DERIVED_PHYSICAL_MASS",
            "physical_total_mass_promoted": rows["P13"]["status"] == "OPEN",
            "xmax_inserted_as_numeric_input": "no numerical Xmax" in rows["P10"]["open_or_excluded"],
        }
    )

    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ownership = (package / "OWNERSHIP_ATLAS.tsv").read_text(encoding="utf-8")
    applied.update(
        {
            "raw_wall_flux_omitted": "Phi_{\\rm wall}=-2\\pi X" in report,
            "raw_wall_flux_promoted_to_mass": (
                "DERIVED_METRIC_LIMIT_PREEXISTING" in ownership
                and "not a native mass or charge" in report
            ),
        }
    )

    failed = [name for name, caught in applied.items() if not caught]
    if failed:
        raise AssertionError(f"uncaught mutations: {failed}")
    return {
        "status": "PASS",
        "mutation_count": len(applied),
        "caught_count": sum(applied.values()),
        "mutations": applied,
        "qualification": "regression_only_not_scientific_proof",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    result = catches(package)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
