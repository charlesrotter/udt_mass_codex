#!/usr/bin/env python3
"""Repository outer gate for G175, with sealed read-only delegation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "6df732bd"

if (ROOT / "REVIEW_SCOPE.json").is_file():
    completed = subprocess.run(
        [sys.executable, str(HERE / "verify_sealed_intake.py"), str(ROOT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    raise SystemExit(completed.returncode)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


required = (
    "PONDER_MAP.md",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "EXACT_DERIVATION.md",
    "derive_calibration_equivalence.py",
    "DERIVATION_RESULT.json",
    "CALIBRATION_EQUIVALENCE_ATLAS.tsv",
    "verify_calibration_equivalence_independent.py",
    "INDEPENDENT_VERIFICATION.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "STATUS_LEDGER.tsv",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "EVIDENCE_GATES.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "REVIEW_EXECUTION_BOUNDARY.md",
    "verify_sealed_intake.py",
    "build_review_intake.py",
)
for name in required:
    require((HERE / name).is_file(), f"missing {name}")

rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
require(len(rows) == 8, "source count")
for row in rows:
    frozen = subprocess.run(
        ["git", "show", f"{FROZEN_SOURCE_COMMIT}:{row['path']}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    require(hashlib.sha256(frozen).hexdigest() == row["sha256"], row["path"])

for script in (
    "derive_calibration_equivalence.py",
    "verify_calibration_equivalence_independent.py",
    "run_catch_proofs.py",
):
    completed = subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    require(completed.returncode == 0, f"{script}\n{completed.stdout}\n{completed.stderr}")

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
require(production["checks_passed"] == production["checks_total"] == 12, "production checks")
require(independent["checks_passed"] == 144_000, "independent checks")
require(independent["anchored_changed"] == 2_000, "anchored counterfamily")
require(catches["catches_passed"] == catches["catches_total"] == 18, "semantic catches")

manifest_text = (HERE / "SOURCE_MANIFEST.tsv").read_text()
require(all(f"udt_g{i}" not in manifest_text for i in range(142, 161)), "scaffold entered source")
ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
require("physical carry owner\tOPEN" in ledger, "physical carry guard")
require("pointwise metric-unit ruler\tDERIVED_OPTION_NOT_SELECTED" in ledger, "unit-ruler guard")

premise = subprocess.run(
    [sys.executable, str(ROOT / "verify_current_scientific_premises.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
require(premise.returncode == 0, premise.stdout + premise.stderr)

external = HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md"
external_status = "PENDING"
if external.is_file():
    require(external.read_text().startswith("G175_ACCEPTED_WITH_STATED_BOUNDS\n"), "external verdict")
    external_status = "ACCEPTED_WITH_STATED_BOUNDS"

result = {
    "gate": "REPOSITORY_OUTER_GATE",
    "status": f"PASS__G175__EXTERNAL_{external_status}",
    "required_files": len(required),
    "source_hashes": len(rows),
    "production_checks": production["checks_total"],
    "independent_checks": independent["checks_passed"],
    "anchored_counterfamilies": independent["anchored_changed"],
    "semantic_catches": catches["catches_total"],
    "premise_verifier_returncode": premise.returncode,
}
(HERE / "VERIFICATION_RESULT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(result, sort_keys=True))
