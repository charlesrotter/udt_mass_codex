#!/usr/bin/env python3
"""Administrative and evidence gate for G168."""

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
    "EXECUTION_NOTE.md",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "OUTCOME_PREMISE_LEDGER.tsv",
    "derive_pair_plane_ownership.py",
    "verify_pair_plane_independent.py",
    "run_catch_proofs.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "EXTERNAL_FOLLOWUP_REVIEW_RAW.md",
    "EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_FOLLOWUP_REVIEW.md",
]
for name in required:
    require((HERE / name).is_file(), f"missing {name}")

derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
landing = "SUPPLIED_ORDERED_COPRESENT_PAIR_GERM_DERIVES_LOCAL_CALIBRATED_PAIR_PLANE__NO_PATH_REQUIRED__PHYSICAL_GERM_OWNERSHIP_IS_ADDITIONAL_WORKING_POSTULATE"
require(derivation["landing"] == landing, "production landing mismatch")
require(derivation["checks_passed"] == derivation["checks_total"] == 36, "production checks")
require(independent["checks_passed"] == 6012, "independent checks")
require(independent["landing_supported"] == landing, "independent landing")
require(catches["catches_passed"] == catches["catches_total"], "semantic catches")

manifest_count = 0
for line in (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
    expected, rel, _role = line.split("\t")
    actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    require(actual == expected, f"source hash {rel}")
    manifest_count += 1
require(manifest_count == 10, "manifest count")

audit = (HERE / "AUDIT_REPORT.md").read_text()
exact = (HERE / "EXACT_DERIVATION.md").read_text()
require(landing.split("__")[0] in audit, "audit landing")
require(
    "VERIFIED_WITH_CAVEATS__FRESH_EXTERNAL_REPAIR_FOLLOWUP_PASS" in audit,
    "repair follow-up pass absent",
)
require(
    "does not derive that a physical relation supplies the germ" in exact
    and "event-pairing rule" in exact,
    "scope ceiling",
)
require("PROPOSED_WORKING_POSTULATE_NOT_DERIVED" in exact, "germ ownership regrade absent")

followup = (HERE / "EXTERNAL_FOLLOWUP_REVIEW_RAW.md").read_text().strip()
require(
    followup == "FOLLOWUP_PASS__OWNERSHIP_REGRADE_COMPLETE__CONDITIONAL_LOCAL_THEOREM_RETAINED",
    "external follow-up landing mismatch",
)

premise = subprocess.run(
    [sys.executable, str(ROOT / "verify_current_scientific_premises.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
require(premise.returncode == 0, "current premise verifier failed")

result = {
    "status": "PASS__FRESH_EXTERNAL_REPAIR_FOLLOWUP_PASS",
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
