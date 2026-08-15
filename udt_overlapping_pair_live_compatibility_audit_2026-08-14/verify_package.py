#!/usr/bin/env python3
"""Fail-closed verifier for the overlapping-pair live compatibility package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "VERIFICATION_RESULT.json"
PRIMARY = "OVERLAP_SUPPLIES_NONIDENTITY_SIMULTANEOUS_COMPATIBILITY_BUT_NOT_LIVE_REGIME_SELECTION"
SECONDARY = "LOUD_ENDS_QUIET_MIDDLE_CONDITIONAL_SURVIVOR_NOT_SELECTED"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    required = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "SOURCE_MANIFEST.tsv",
        "SOURCE_SCOPE_CORRECTION.md",
        "derive_overlap_compatibility.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "EXACT_DERIVATION.md",
        "WITNESS_ATLAS.tsv",
        "STATUS_LEDGER.tsv",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "AUDIT_REPORT.md",
        "REVIEW_DISPATCH.md",
        "build_review_intake.py",
    ]
    missing = [name for name in required if not (HERE / name).is_file()]

    source_mismatches = []
    with (HERE / "SOURCE_MANIFEST.tsv").open() as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["path"]
            if not path.is_file() or sha256(path) != row["sha256"]:
                source_mismatches.append(row["path"])

    prereg = (HERE / "PREREGISTRATION.md").read_text()
    exact = (HERE / "EXACT_DERIVATION.md").read_text()
    report = (HERE / "AUDIT_REPORT.md").read_text()
    evidence = (HERE / "EVIDENCE_GATES.md").read_text()
    status = (HERE / "STATUS_LEDGER.tsv").read_text()
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())

    checks = {
        "required_files_present": not missing,
        "source_hashes_match": not source_mismatches,
        "preregistered_before_outcome": "NOT YET EVALUATED" in prereg and "aa810251" in evidence,
        "primary_landing_preregistered": PRIMARY in prereg,
        "secondary_landing_preregistered": SECONDARY in prereg,
        "derivation_primary_matches": derivation.get("primary_landing") == PRIMARY,
        "derivation_secondary_matches": derivation.get("secondary_landing") == SECONDARY,
        "all_production_checks_pass": all(derivation.get("checks", {}).values()),
        "independent_verification_passes": independent.get("passed") is True,
        "catch_proofs_pass": catches.get("passed") is True,
        "exact_derivation_states_primary": PRIMARY in exact,
        "exact_derivation_states_secondary": SECONDARY in exact,
        "report_states_primary": PRIMARY in report,
        "report_states_secondary": SECONDARY in report,
        "physical_history_remains_open": "physical pair family and history\tOPEN" in status,
        "quiet_middle_not_promoted": "universal overlap-derived quiet middle\tFALSIFIED WITHIN DECLARED LIVE CLASS" in status,
        "external_review_not_falsely_claimed_complete": "PENDING" in evidence,
    }
    passed = all(checks.values())
    result = {
        "schema": "udt.overlapping_pair_live_compatibility.package_verification.v1",
        "checks": checks,
        "missing": missing,
        "source_mismatches": source_mismatches,
        "passed": passed,
        "banking_grade": "VERIFIED-WITH-CAVEATS__FRESH_EXTERNAL_SEMANTIC_REVIEW_PENDING",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
