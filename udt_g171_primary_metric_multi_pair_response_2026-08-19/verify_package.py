#!/usr/bin/env python3
"""Verify the internal G171 primary-metric multi-pair evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "d9e2d54f"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


required = [
    "PONDER_MAP.md",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_multi_pair_response.py",
    "DERIVATION_RESULT.json",
    "verify_multi_pair_independent.py",
    "INDEPENDENT_VERIFICATION.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "verify_sealed_intake.py",
    "build_review_intake.py",
    "REPAIR_PREREGISTRATION.md",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
    "TRANSMISSION_RECORD.md",
    "REVIEW_EXECUTION_BOUNDARY.md",
    "FOLLOWUP_REVIEW_REQUEST.md",
    "EXTERNAL_FOLLOWUP_REVIEW_RAW.md",
    "EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt",
    "FOLLOWUP_REVIEW_ADJUDICATION.md",
]
for name in required:
    require((HERE / name).is_file(), f"missing {name}")

rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
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
    "derive_multi_pair_response.py",
    "verify_multi_pair_independent.py",
    "run_catch_proofs.py",
):
    command = [sys.executable, str(HERE / script)]
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    require(completed.returncode == 0, f"command failed: {script}\n{completed.stdout}\n{completed.stderr}")

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
landing = (
    "PRIMARY_METRIC_PAIR_GERM_RELATIVE_NETWORK"
    "__EACH_ORDERED_PAIR_RESPONSE_NATIVE_FROM_ITS_COMPLETE_PULLBACK"
    "__SAME_PAIR_REVERSAL_AUTOMATIC"
    "__SHARED_OBSERVER_DOES_NOT_FORCE_PAIR_INDEPENDENT_ENDPOINT_DENSITY"
    "__GENERAL_TRIANGLE_ADDITIVITY_NOT_DERIVED_OR_REQUIRED"
    "__MATCHED_ENDPOINT_READOUT_SUBFAMILY_TELESCOPES"
    "__NO_SCAFFOLDED_CARRY_KERNEL"
)
require(production["landing"] == landing, "production landing")
require(production["checks_passed"] == production["checks_total"] == 31, "production checks")
require(independent["landing_supported"] == landing, "independent landing")
require(independent["checks_passed"] == 108000, "independent checks")
require(independent["trials"] == 12000, "independent trial count")
require(independent["different_pair_readouts"] == 12000, "pair readout coverage")
require(independent["unmatched_triangle_nonzero"] == 12000, "nonadditive coverage")
require(catches["catches_passed"] == catches["catches_total"] == 14, "mutation catches")

manifest = (HERE / "SOURCE_MANIFEST.tsv").read_text()
require(all(f"udt_g{i}" not in manifest for i in range(142, 161)), "scaffold source entered manifest")
audit = (HERE / "AUDIT_REPORT.md").read_text()
ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
require("PACKAGING_REPAIR_FOLLOWUP_PASS" in audit, "repair-followup pass grade missing")
require("scaffolded carrier carry score kernel\tEXCLUDED_BY_GATE" in ledger, "scaffold guard missing")
require("arbitrary triangle additivity\tNOT_DERIVED_NOT_REQUIRED" in ledger, "triangle boundary missing")
require("positive metric-space distance\tNOT_CLAIMED" in ledger, "distance boundary missing")

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
    "status": "PASS__G171__EXTERNAL_AND_SEALED_REPAIR_FOLLOWUP_COMPLETE",
    "required_files": len(required),
    "source_hashes": len(rows),
    "production_checks": production["checks_total"],
    "independent_checks": independent["checks_passed"],
    "semantic_catches": catches["catches_total"],
    "premise_verifier_returncode": premise.returncode,
    "sealed_replay": "RUN_VERIFY_SEALED_INTAKE_INSIDE_SEAL",
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
