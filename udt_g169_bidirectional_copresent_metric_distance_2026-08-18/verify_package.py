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
    "CONDITIONAL_RELATIONAL_DISTANCE_OBJECT"
    "__RECIPROCAL_SCALAR_REVERSAL_DERIVED_ON_ONE_SUPPLIED_RELATION"
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
require("FRESH_ADVERSARIAL_REVIEW_OPEN" in audit, "external review status")
require("PROPOSED_WORKING_FOUNDATIONAL_CLARIFICATION_NOT_DERIVED" in ledger, "ownership boundary")
require("surface reversal or endpoint exchange alone does not generate UDT Reciprocity" in exact, "counterexample boundary")
require("arbitrary" in audit and "one-dimensional additive rule" in audit, "triangle category guard")

premise = subprocess.run(
    [sys.executable, str(ROOT / "verify_current_scientific_premises.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
require(premise.returncode == 0, "current premise verifier")

result = {
    "status": "PASS__INTERNAL_GATES__FRESH_ADVERSARIAL_REVIEW_OPEN",
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
