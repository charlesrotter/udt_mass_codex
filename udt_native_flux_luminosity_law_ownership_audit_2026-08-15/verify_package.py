#!/usr/bin/env python3
"""Verify the native flux/luminosity ownership package and semantic guards."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_statuses():
    with (ROOT / "STATUS_LEDGER.tsv").open(encoding="utf-8") as handle:
        return {row["object"]: row for row in csv.DictReader(handle, delimiter="\t")}


def main():
    required = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_CENSUS.tsv",
        "EXACT_DERIVATION.md",
        "STATUS_LEDGER.tsv",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "SOURCE_MANIFEST.tsv",
        "REVIEW_DISPATCH.md",
        "EXTERNAL_ADVERSARIAL_REVIEW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
    ]
    checks = {f"exists:{name}": (ROOT / name).is_file() for name in required}

    derivation = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    statuses = read_statuses()
    census = (ROOT / "SOURCE_CENSUS.tsv").read_text(encoding="utf-8")
    report = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")

    checks.update(
        {
            "wronskian_exact": derivation["wronskian_derivative_zero"] is True,
            "screen_factor_exact": derivation["reverse_determinant_factor"] == "Z**2",
            "composition_nonselection": (
                derivation["composition_selects_p_or_q"] is False
            ),
            "independent_pass": independent["all_pass"] is True,
            "three_catches": len(independent["catch_proofs"]) == 3
            and all(independent["catch_proofs"].values()),
            "eta_open": statuses["radiative_survival_eta"]["status"] == "OPEN",
            "epsilon_open": statuses["energy_conversion_epsilon"]["status"] == "OPEN",
            "historical_law_conditional": (
                statuses["historical_dL_Z2_dA"]["status"]
                == "COMPATIBLE_CONDITIONAL_CLOSURE"
            ),
            "fresh_review_banked": (
                statuses["overall"]["status"]
                == "EXTERNALLY_VERIFIED_WITH_CAVEATS__Z3_GEOMETRIC_CLOCK_FACTOR__TRANSFER_PRODUCT_OPEN"
                and "EXTERNALLY_VERIFIED_WITH_CAVEATS" in report
            ),
            "regular_character_scope_repaired": (
                "power laws exhaust the positive character family" in report
            ),
            "maxwell_regression_caught": (
                "claims minimal Maxwell and photon conservation derived conflict"
                in census
            ),
            "no_full_validation": "No SNe fit" in report,
        }
    )

    result = {
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "all_pass": all(checks.values()),
    }
    (ROOT / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
