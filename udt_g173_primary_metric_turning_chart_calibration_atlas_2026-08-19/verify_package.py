#!/usr/bin/env python3
"""Repository-side outer verifier for the G173 package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "d1f2e6f5"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


required = [
    "PONDER_MAP.md",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_turning_chart_atlas.py",
    "DERIVATION_RESULT.json",
    "verify_turning_chart_independent.py",
    "INDEPENDENT_VERIFICATION.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "EXACT_DERIVATION.md",
    "WITNESS_ATLAS.tsv",
    "CALIBRATION_ATLAS.tsv",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "REVIEW_EXECUTION_BOUNDARY.md",
    "verify_sealed_intake.py",
    "build_review_intake.py",
    "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
    "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
    "TRANSMISSION_RECORD.md",
]
for name in required:
    require((HERE / name).is_file(), f"missing {name}")

rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
require(len(rows) == 11, "source manifest count")
for row in rows:
    frozen = subprocess.run(
        ["git", "show", f"{FROZEN_SOURCE_COMMIT}:{row['path']}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    require(hashlib.sha256(frozen).hexdigest() == row["sha256"], f"source hash {row['path']}")

for script in (
    "derive_turning_chart_atlas.py",
    "verify_turning_chart_independent.py",
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
    "PULLBACK_EXTENDS__CALIBRATION_ATLAS_NONUNIQUE"
    "__RADIAL_TURN_WITH_ANGULAR_MOTION_IS_REGULAR"
    "__RAW_TERMINAL_PHI_IS_AN_AFFINE_LOG_DENSITY"
    "__ANY_POSITIVE_WEIGHT_ONE_CALIBRATION_GIVES_AN_INVARIANT_SCALAR_CHART"
    "__TWO_METRIC_BUILT_CALIBRATIONS_SURVIVE_AND_DISAGREE"
    "__NO_FINITE_CALIBRATION_CAN_EQUAL_G172_ON_EVERY_PUNCTURED_MONOTONE_NEIGHBORHOOD"
    "__TRUE_FIRST_RANK_BOUNDARY_IS_ZERO_COMPLETE_SPATIAL_TANGENT"
    "__NO_PHYSICAL_CALIBRATION_OR_GLOBAL_SELECTION"
)
require(production["landing"] == landing, "production landing")
require(production["checks_passed"] == production["checks_total"] == 32, "production checks")
require(independent["landing_supported"] == landing, "independent landing")
require(independent["checks_passed"] == 144000, "independent checks")
require(independent["trials"] == 12000, "independent trials")
require(independent["turning_cases"] >= 1000, "turning coverage")
require(catches["catches_passed"] == catches["catches_total"] == 19, "mutation catches")
review = (HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").read_text()
require(review.startswith("G173_ACCEPTED_WITH_STATED_BOUNDS\n"), "external review verdict")
require("Banking judgment: `VERIFIED_WITH_CAVEATS`" in review, "external review grade")
require(
    hashlib.sha256((HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").read_bytes()).hexdigest()
    == "6328b1d416f03870661185e9d3da4d4c49fa2be9c00131a6bcbc40ba0271a9aa",
    "banked external review hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz").read_bytes()).hexdigest()
    == "fe0b04caa336cb7234c267d4d80172b851b65074a95e896091bf3024347bcf3b",
    "compressed external transcript hash",
)

manifest = (HERE / "SOURCE_MANIFEST.tsv").read_text()
require(all(f"udt_g{i}" not in manifest for i in range(142, 161)), "scaffold source entered manifest")
ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
require("unique turning calibration\tREFUTED_UNDER_ACTIVE_GATES" in ledger, "nonuniqueness grade missing")
require("physical calibration or family ownership\tOPEN" in ledger, "physical ownership guard missing")
require("cross-calibration carry\tOPEN" in ledger, "carry boundary missing")
require("non-scalar transport closure\tOPEN" in ledger, "transport boundary missing")

premise = subprocess.run(
    [sys.executable, str(ROOT / "verify_current_scientific_premises.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
require(premise.returncode == 0, f"premise verifier\n{premise.stdout}\n{premise.stderr}")

result = {
    "gate": "REPOSITORY_OUTER_GATE",
    "status": "PASS__G173__EXTERNAL_GPT54_ACCEPTED_WITH_STATED_BOUNDS",
    "required_files": len(required),
    "source_hashes": len(rows),
    "production_checks": production["checks_total"],
    "independent_checks": independent["checks_passed"],
    "turning_cases": independent["turning_cases"],
    "semantic_catches": catches["catches_total"],
    "premise_verifier_returncode": premise.returncode,
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
