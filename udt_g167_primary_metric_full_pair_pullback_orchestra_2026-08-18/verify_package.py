#!/usr/bin/env python3
"""Fail-closed package verification for G167."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def main() -> None:
    required = [
        "PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_RESULT.json",
        "CATCH_PROOF_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXTERNAL_ADVERSARIAL_REVIEW.md",
        "EXTERNAL_FOLLOWUP_REVIEW.md",
        "REPAIR_PREREGISTRATION.md",
        "REPOSITORY_GATE_RECORD.json",
        "derive_primary_metric_pair_pullback.py",
        "verify_primary_metric_pair_pullback_independent.py",
        "run_catch_proofs.py",
    ]
    missing = [name for name in required if not (HERE / name).is_file()]

    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    hash_failures = []
    for row in rows:
        if hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() != row["sha256"]:
            hash_failures.append(row["path"])

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    repository_gates = json.loads((HERE / "REPOSITORY_GATE_RECORD.json").read_text())
    exact_text = (HERE / "EXACT_DERIVATION.md").read_text()
    evidence_text = (HERE / "EVIDENCE_GATES.md").read_text()
    review_text = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text()
    followup_text = (HERE / "EXTERNAL_FOLLOWUP_REVIEW.md").read_text()

    checks = {
        "required_files": not missing,
        "ten_sources": len(rows) == 10,
        "source_hashes": not hash_failures,
        "production_19_of_19": derivation.get("checks_passed") == 19
        and derivation.get("checks_total") == 19,
        "independent_pass": independent.get("status") == "PASS"
        and independent.get("fraction_trials") == 1200,
        "catch_proofs_pass": catches.get("status") == "PASS"
        and catches.get("caught") == catches.get("total"),
        "repository_gate_record": repository_gates.get("status") == "PASS"
        and repository_gates.get("premise_rows") == 153
        and repository_gates.get("pytest_passed") == 125
        and repository_gates.get("pytest_xfailed") == 1,
        "first_external_core_verified":
        "VERIFIED_WITH_CAVEATS__BOUNDED_PRIMARY_PAIR_PULLBACK__SOURCE_HASH_REPLAY_BROKEN"
        in review_text,
        "repair_status_consistent":
        "VERIFIED_WITH_CAVEATS__FRESH_EXTERNAL_REPAIR_FOLLOWUP_PASS" in evidence_text
        and "PREREGISTERED__NOT_YET_RUN" not in evidence_text,
        "external_followup_pass":
        "PASS__FIRST_REVIEW_MANDATORY_REPAIRS_CLOSED" in followup_text
        and "Mandatory repairs\n\nNone" in followup_text,
        "displayed_component_sums_repaired":
        "+e^{2\\phi}r_ir_j" in exact_text
        and "+r^2\\theta_i\\theta_j" in exact_text
        and "+e^{2\\phi}r_0r_1" in exact_text,
        "bounded_landing": derivation.get("primary_landing")
        == "PRIMARY_STATIC_SPHERICAL_UDT_METRIC_OWNS_FULL_GENERAL_PAIR_PULLBACK_ORCHESTRA__GENERAL_AMBIENT_EXTENSION_OPEN",
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "missing": missing,
        "source_hash_failures": hash_failures,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if result["status"] != "PASS":
        raise SystemExit(f"FAIL: {result}")
    print("PASS: G167 package verification")


if __name__ == "__main__":
    main()
