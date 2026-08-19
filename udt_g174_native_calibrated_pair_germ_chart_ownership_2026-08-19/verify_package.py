#!/usr/bin/env python3
"""Repository-side outer verifier for the G174 package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "9e40a840"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


required = [
    "PONDER_MAP.md",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_calibrated_germ_ownership.py",
    "DERIVATION_RESULT.json",
    "verify_calibrated_germ_independent.py",
    "INDEPENDENT_VERIFICATION.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "EXACT_DERIVATION.md",
    "WITNESS_ATLAS.tsv",
    "CALIBRATION_CLASS_ATLAS.tsv",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "REVIEW_EXECUTION_BOUNDARY.md",
    "verify_sealed_intake.py",
    "build_review_intake.py",
]
for name in required:
    require((HERE / name).is_file(), f"missing {name}")

rows = [
    row
    for row in csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t")
    if row.get("path")
]
require(len(rows) == 12, "source manifest count")
for row in rows:
    frozen = subprocess.run(
        ["git", "show", f"{FROZEN_SOURCE_COMMIT}:{row['path']}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    require(hashlib.sha256(frozen).hexdigest() == row["sha256"], f"source hash {row['path']}")

for script in (
    "derive_calibrated_germ_ownership.py",
    "verify_calibrated_germ_independent.py",
    "run_catch_proofs.py",
):
    completed = subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    require(completed.returncode == 0, f"command failed: {script}\n{completed.stdout}\n{completed.stderr}")

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
landing = (
    "CALIBRATED_GERM_OWNS_UNIQUE_SCALAR__UNCALIBRATED_LINE_RETAINS_ATLAS"
    "__G173_TENSOR_AND_RANK_THEOREM_RETAINED"
    "__M_IS_THE_JACOBIAN_FROM_AUXILIARY_PARAMETER_TO_SUPPLIED_RULER_COORDINATE"
    "__DISTINCT_M_DEFINE_DISTINCT_CALIBRATED_GERMS_UNLESS_IDENTICAL"
    "__CONSTANT_UNIT_RESCALE_CANCELS_FROM_ENDPOINT_DEPTH"
    "__PHYSICAL_CALIBRATION_AND_CARRY_OWNER_REMAIN_OPEN"
)
require(production["landing"] == landing, "production landing")
require(production["checks_passed"] == production["checks_total"] == 32, "production checks")
require(independent["landing_supported"] == landing, "independent landing")
require(independent["checks_passed"] == 156000, "independent checks")
require(independent["trials"] == 12000, "independent trials")
require(independent["turning_cases"] == 2000, "turning coverage")
require(independent["candidate_difference_cases"] > 0, "candidate distinction coverage")
require(catches["catches_passed"] == catches["catches_total"] == 18, "mutation catches")

manifest = (HERE / "SOURCE_MANIFEST.tsv").read_text()
require(all(f"udt_g{i}" not in manifest for i in range(142, 161)), "scaffold source entered manifest")
ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
require("physical calibration owner\tOPEN" in ledger, "physical ownership guard missing")
require("G173 calibration nonuniqueness\tRECLASSIFIED" in ledger, "G173 regrade missing")
require("G173 tensor and rank theorem\tRETAINED_DERIVED_BOUNDED" in ledger, "G173 tensor retention missing")

premise = subprocess.run(
    [sys.executable, str(ROOT / "verify_current_scientific_premises.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
require(premise.returncode == 0, f"premise verifier\n{premise.stdout}\n{premise.stderr}")

external = HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md"
external_status = "PENDING"
if external.is_file():
    review = external.read_text()
    require(review.startswith("G174_ACCEPTED_WITH_STATED_BOUNDS\n"), "external review verdict")
    external_status = "ACCEPTED_WITH_STATED_BOUNDS"

result = {
    "gate": "REPOSITORY_OUTER_GATE",
    "status": f"PASS__G174__EXTERNAL_{external_status}",
    "required_files": len(required),
    "source_hashes": len(rows),
    "production_checks": production["checks_total"],
    "independent_checks": independent["checks_passed"],
    "turning_cases": independent["turning_cases"],
    "candidate_difference_cases": independent["candidate_difference_cases"],
    "semantic_catches": catches["catches_total"],
    "premise_verifier_returncode": premise.returncode,
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
