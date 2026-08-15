#!/usr/bin/env python3
"""Fail-closed package verification for the uncompressed pair evaluator audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "VERIFICATION_RESULT.json"
LANDING = (
    "FULL_UNCOMPRESSED_TERMINAL_EVALUATOR_DERIVED__NO_SCALAR_MU_OWNED__"
    "PHYSICAL_PAIR_AND_HISTORY_OPEN"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    required = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "MU_TYPE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "derive_uncompressed_pair_evaluator.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "EXACT_DERIVATION.md",
        "SHORTCUT_REGRADE.tsv",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "LAY_REPORT.md",
        "AUDIT_REPORT.md",
    ]
    missing = [name for name in required if not (HERE / name).is_file()]

    source_mismatches = []
    with (HERE / "SOURCE_MANIFEST.tsv").open() as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = HERE.parent / row["path"]
            if not path.is_file() or sha256(path) != row["sha256"]:
                source_mismatches.append(row["path"])

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    prereg = (HERE / "PREREGISTRATION.md").read_text()
    exact = (HERE / "EXACT_DERIVATION.md").read_text()
    report = (HERE / "AUDIT_REPORT.md").read_text()

    checks = {
        "required_files_present": not missing,
        "source_hashes_match": not source_mismatches,
        "preregistered_landing_present": LANDING in prereg,
        "derivation_landing_matches": derivation.get("primary_landing") == LANDING,
        "all_production_checks_pass": all(derivation.get("checks", {}).values()),
        "independent_verification_passes": independent.get("passed") is True,
        "catch_proofs_pass": catches.get("passed") is True,
        "exact_derivation_states_landing": LANDING in exact.replace("\n", ""),
        "report_states_landing": LANDING in report.replace("\n", ""),
        "physical_pair_remains_open": "physical pair assignment\tOPEN" in (HERE / "STATUS_LEDGER.tsv").read_text(),
        "mu_types_separated": "mu_old" in exact and "S in Mat(2,R)" in exact,
        "external_review_not_falsely_claimed_complete": "pending" in (HERE / "EVIDENCE_GATES.md").read_text().lower(),
    }
    passed = all(checks.values())
    result = {
        "schema": "udt.uncompressed_pair_evaluator.package_verification.v1",
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
