#!/usr/bin/env python3
"""Fail-closed package verifier for G169."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


required = [
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "STATUS_LEDGER.tsv",
    "PONDER_MAP.md",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "OUTCOME_PREMISE_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "derive_bidirectional_distance.py",
    "verify_bidirectional_distance_independent.py",
    "run_catch_proofs.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
    "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
    "REPAIR_PREREGISTRATION.md",
    "TRANSMISSION_RECORD.md",
    "EXTERNAL_FOLLOWUP_REVIEW_RAW.md",
    "EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt",
    "FOLLOWUP_REVIEW_ADJUDICATION.md",
    "SECOND_REPAIR_PREREGISTRATION.md",
]
for name in required:
    require((HERE / name).is_file(), f"missing {name}")

manifest_count = 0
for line in (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
    expected, relative, _role = line.split("\t")
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    require(actual == expected, f"source hash {relative}")
    manifest_count += 1
require(manifest_count == 12, "manifest count")

derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
landing = (
    "CONDITIONAL_REVERSAL_QUOTIENT_ON_SUPPLIED_TWO_ENDED_RELATION"
    "__NOT_YET_PHYSICAL_UDT_DISTANCE"
    "__PURE_RECIPROCAL_SCALAR_REVERSAL_DERIVED"
    "__MATCHED_CHAIN_COMPOSITION_DERIVED"
    "__ARBITRARY_TRIANGLE_ADDITIVITY_NOT_REQUIRED_OR_DERIVED"
    "__PHYSICAL_TWO_ENDED_GERM_AND_CARRY_OWNERSHIP_OPEN"
)
require(derivation["landing"] == landing, "production landing")
require(derivation["checks_passed"] == derivation["checks_total"] == 36, "production checks")
require(independent["checks_passed"] == 12005, "independent count")
require(independent["landing_supported"] == landing, "independent landing")
require(catches["catches_passed"] == catches["catches_total"] == 12, "mutation catches")

audit = (HERE / "AUDIT_REPORT.md").read_text()
exact = (HERE / "EXACT_DERIVATION.md").read_text()
ledger = (HERE / "OUTCOME_PREMISE_LEDGER.tsv").read_text()
status_ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
require("FINAL_REPAIR_FOLLOWUP_OPEN" in audit, "external followup status")
require(
    "physical co-present relation owns both endpoint germs and inverse carry\tOPEN_NOT_DERIVED" in ledger,
    "outcome ownership boundary",
)
require(
    "physical two-ended germ and carry ownership\tOPEN_NOT_DERIVED" in status_ledger,
    "status ownership boundary",
)
require("NOT_DERIVED_TYPE_FAILURE" in ledger, "physical distance boundary")
require("surface reversal or endpoint exchange alone does not generate UDT Reciprocity" in exact, "counterexample boundary")
require("arbitrary" in audit and "one-dimensional additive rule" in audit, "triangle category guard")
require(
    hashlib.sha256((HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").read_bytes()).hexdigest()
    == "722a1013b5f221e3c15cc843c1efda058375a25927e595108b6d775c12265762",
    "external raw hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt").read_bytes()).hexdigest()
    == "e3fd11474760c1885260352c76a839fe410acaceeea7355926c089375627ef2e",
    "external transcript hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_FOLLOWUP_REVIEW_RAW.md").read_bytes()).hexdigest()
    == "ffa4e6ceb1164102b223607d2eacc984b65546f45f46175cb051b42d62ec7e2a",
    "external followup raw hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt").read_bytes()).hexdigest()
    == "ce0260faea817b6adba97cada472b497e532cd7f25a3bf8c86c870590c7c97f4",
    "external followup transcript hash",
)

premise = subprocess.run(
    [sys.executable, str(ROOT / "verify_current_scientific_premises.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
require(premise.returncode == 0, "current premise verifier")

result = {
    "status": "PASS__SECOND_LEDGER_REPAIR_INTERNAL_GATES__FINAL_REPAIR_FOLLOWUP_OPEN",
    "required_files": len(required),
    "source_hashes": manifest_count,
    "production_checks": derivation["checks_total"],
    "independent_checks": independent["checks_passed"],
    "semantic_catches": catches["catches_total"],
    "premise_verifier_returncode": premise.returncode,
    "premise_verifier_stdout": premise.stdout.strip(),
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
