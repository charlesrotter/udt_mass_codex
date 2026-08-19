#!/usr/bin/env python3
"""Verify the repository-side G172 evidence package before external review."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "7477d8d1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


required = [
    "PONDER_MAP.md",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_smooth_pair_family.py",
    "DERIVATION_RESULT.json",
    "verify_smooth_pair_family_independent.py",
    "INDEPENDENT_VERIFICATION.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "EXACT_DERIVATION.md",
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
    "derive_smooth_pair_family.py",
    "verify_smooth_pair_family_independent.py",
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
    "SMOOTH_FAMILY_CLOSURE"
    "__PRIMARY_METRIC_PULLBACK_GIVES_EXACT_RADIAL_PLUS_ANGULAR_RESPONSE"
    "__STATIC_TIME_ORTHOGONAL_MONOTONE_AREAL_FAMILIES_INTEGRATE"
    "__REVERSAL_AND_TELESCOPING_HOLD_WITHIN_ONE_SUPPLIED_FAMILY"
    "__FIRST_BOUNDARY_IS_CALIBRATION_OR_REGULARITY_LOSS"
    "__NO_PHYSICAL_FAMILY_SELECTION_OR_GLOBAL_COMPLETION"
)
require(production["landing"] == landing, "production landing")
require(production["checks_passed"] == production["checks_total"] == 26, "production checks")
require(independent["landing_supported"] == landing, "independent landing")
require(independent["checks_passed"] == 144000, "independent checks")
require(independent["trials"] == 12000, "independent trials")
require(independent["nonradial_cases"] > 11000, "nonradial coverage")
require(catches["catches_passed"] == catches["catches_total"] == 19, "mutation catches")

manifest = (HERE / "SOURCE_MANIFEST.tsv").read_text()
require(all(f"udt_g{i}" not in manifest for i in range(142, 161)), "scaffold source entered manifest")
ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
require("G142--G160 scaffolded kernel\tEXCLUDED" in ledger, "scaffold guard missing")
require("physical angular-family ownership\tOPEN" in ledger, "physical-family boundary missing")
require("turning and pure-angular strata\tOPEN" in ledger, "turning boundary missing")

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
    "status": "PASS__G172__READY_FOR_FRESH_EXTERNAL_REVIEW",
    "required_files": len(required),
    "source_hashes": len(rows),
    "production_checks": production["checks_total"],
    "independent_checks": independent["checks_passed"],
    "semantic_catches": catches["catches_total"],
    "premise_verifier_returncode": premise.returncode,
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
