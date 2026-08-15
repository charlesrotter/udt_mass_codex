#!/usr/bin/env python3
"""Verify the native radiative-current/energy ownership package."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def table(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main():
    required = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_CENSUS.tsv",
        "CANDIDATE_OWNER_ATLAS.tsv",
        "EXACT_DERIVATION.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "STATUS_LEDGER.tsv",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "SOURCE_MANIFEST.tsv",
        "EXTERNAL_ADVERSARIAL_REVIEW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
    ]
    checks = {f"exists:{name}": (ROOT / name).is_file() for name in required}
    primary = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    statuses = {row["object"]: row for row in table("STATUS_LEDGER.tsv")}
    candidates = {row["candidate_id"]: row for row in table("CANDIDATE_OWNER_ATLAS.tsv")}
    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    checks.update(
        {
            "candidate_count_13": len(candidates) == 13,
            "dF_identity": primary["homogeneous_identity_dF_zero"] is True,
            "dJ_identity": primary["response_conservation_dJ3_zero"] is True,
            "source_free_not_identity": primary["source_free_dstarF_zero_is_identity"] is False,
            "phase_volume_preserved": primary["hamiltonian_phase_volume_preserved"] is True,
            "distribution_not_selected": primary["distribution_transport_selected_by_metric"] is False,
            "carrier_not_selected": primary["physical_carrier_identification_selected"] is False,
            "independent_pass": independent["all_pass"] is True,
            "independent_no_sympy": "no_SymPy" in independent["implementation"],
            "eta_open": statuses["eta"]["status"] == "OPEN",
            "epsilon_conditional": statuses["epsilon"]["status"] == "CONDITIONAL_ONE_CARRIER_COVECTOR_PREMISE",
            "source_free_open": statuses["source_free_equation"]["status"] == "OPEN_NOT_IDENTITY",
            "pair_normal_type_guard": candidates["C04"]["status"] == "PATH_CHANNEL_NOT_4D_RADIATIVE_CURRENT",
            "smallest_missing_carrier": candidates["C13"]["status"] == "SMALLEST_MISSING_CARRIER_OBJECT",
            "no_planck_needed_for_ratio": "Planck-scale" in exact,
            "external_status": statuses["overall"]["status"].startswith("EXTERNALLY_VERIFIED_WITH_CAVEATS"),
            "review_landing": "VERIFIED_WITH_CAVEATS__GEOMETRIC_RESPONSE_AND_PHASESPACE_TRANSPORT_ONLY" in (ROOT / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8"),
            "consistency_gate_not_independence": "consistency-only" in (ROOT / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8"),
            "no_full_maxwell_claim": "__PHYSICAL_TRANSFER_OPEN" in report,
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
