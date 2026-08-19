#!/usr/bin/env python3
"""Verify the repository-side, repair-ready G170 endpoint-relative evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "f9a6d1e6"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


required = [
    "PREREGISTRATION.md",
    "PONDER_MAP.md",
    "SOURCE_MANIFEST.tsv",
    "derive_endpoint_relative_response.py",
    "DERIVATION_RESULT.json",
    "verify_endpoint_relative_independent.py",
    "INDEPENDENT_VERIFICATION.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "EXECUTION_NOTE.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
    "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
    "TRANSMISSION_RECORD.md",
    "REPAIR_PREREGISTRATION.md",
    "EXTERNAL_FOLLOWUP_REVIEW_RAW.md",
    "EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt",
    "FOLLOWUP_REVIEW_ADJUDICATION.md",
    "SECOND_REPAIR_PREREGISTRATION.md",
    "EXTERNAL_FINAL_FOLLOWUP_REVIEW_RAW.md",
    "EXTERNAL_FINAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt",
    "FINAL_FOLLOWUP_REVIEW_ADJUDICATION.md",
    "THIRD_REPAIR_PREREGISTRATION.md",
    "verify_sealed_intake.py",
    "EXTERNAL_MECHANICAL_CLOSURE_REVIEW_RAW.md",
    "EXTERNAL_MECHANICAL_CLOSURE_REVIEW_TRANSCRIPT.txt",
    "MECHANICAL_CLOSURE_ADJUDICATION.md",
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

commands = [
    [sys.executable, str(HERE / "derive_endpoint_relative_response.py")],
    [sys.executable, str(HERE / "verify_endpoint_relative_independent.py")],
    [sys.executable, str(HERE / "run_catch_proofs.py")],
]
for command in commands:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    require(completed.returncode == 0, f"command failed: {' '.join(command)}\n{completed.stdout}\n{completed.stderr}")

production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
landing = (
    "ENDPOINT_RELATIVE_RECIPROCAL_DEPTH_DERIVED_FROM_TERMINAL_CEFF_RATIOS"
    "__WITHIN_ONE_CONSISTENT_RECIPROCAL_CALIBRATION_CLASS"
    "__BIDIRECTIONAL_REVERSAL_AND_MATCHED_COMPOSITION_AUTOMATIC"
    "__G169_SINGLE_ENDPOINT_REVERSAL_COUNTEREXAMPLE_RECLASSIFIED"
    "__COPRESENCE_NOT_LOAD_BEARING"
    "__CROSS_QUERY_AND_FULL_NONSCALAR_CARRY_REMAIN_OPEN"
)
require(production["landing"] == landing, "production landing")
require(production["checks_passed"] == production["checks_total"] == 40, "production checks")
require(independent["landing_supported"] == landing, "independent landing")
require(independent["checks_passed"] == 21600, "independent count")
require(independent["angular_trials"] == independent["angular_shift_live"] == 1200, "angular shift coverage")
require(independent["angular_trials"] == independent["angular_readout_changed"] == 1200, "angular readout coverage")
require(catches["catches_passed"] == catches["catches_total"] == 13, "mutation catches")

require(
    hashlib.sha256((HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").read_bytes()).hexdigest()
    == "082b9207559f9e412b0f6ec595f051a9b2831776fca5adb72868bbd0fff937a3",
    "external raw hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt").read_bytes()).hexdigest()
    == "b72071d46b9ab44d4db90e2c30b621b4378063bba02882ad11ff42dcbf966d80",
    "external transcript hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_FOLLOWUP_REVIEW_RAW.md").read_bytes()).hexdigest()
    == "2d3be594fcbf0c2330d495606b4f3c19db0215131a6f5b99d10f8495abbf943f",
    "follow-up raw hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt").read_bytes()).hexdigest()
    == "00b93696d1f71390a7f15bdc70eb5211a4440d5c94ca60ab5af8ca6f0088bf9b",
    "follow-up transcript hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_FINAL_FOLLOWUP_REVIEW_RAW.md").read_bytes()).hexdigest()
    == "867bba598174b7f54bad4248a65910c6404692c48f530a74596e6411c63f1b93",
    "final follow-up raw hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_FINAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt").read_bytes()).hexdigest()
    == "0258aa802d3cf60a8c55ec088f80e07e41edac93c5e131f4d22b802f40fefa12",
    "final follow-up transcript hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_MECHANICAL_CLOSURE_REVIEW_RAW.md").read_bytes()).hexdigest()
    == "5a84ac9536436712d0bc13eb990fdeaa0be82f8bf92af72ce03993a2958b69cd",
    "mechanical closure raw hash",
)
require(
    hashlib.sha256((HERE / "EXTERNAL_MECHANICAL_CLOSURE_REVIEW_TRANSCRIPT.txt").read_bytes()).hexdigest()
    == "52e7a0bd0bfee304478673ddd51047d6569aa309588230b88f5496fc52748363",
    "mechanical closure transcript hash",
)

audit = (HERE / "AUDIT_REPORT.md").read_text()
exact = (HERE / "EXACT_DERIVATION.md").read_text()
ledger = (HERE / "STATUS_LEDGER.tsv").read_text()
exact_normalized = " ".join(exact.split())
require("ENDPOINT_RELATIVE_REPAIR_VALID_BUT_CALIBRATION_CARRY_STILL_LOAD_BEARING" in audit, "external landing")
require(r"\Phi_B-\Phi_A" in exact, "endpoint-difference theorem")
require("one consistently calibrated pair surface" in exact_normalized, "calibration-class scope")
require("co-presence premise\tNOT_LOAD_BEARING" in ledger, "co-presence boundary")
require("positive metric-space distance\tNOT_CLAIMED" in ledger, "distance boundary")
require("full non-scalar carry\tOPEN_SEPARATE" in ledger, "carry boundary")
require("reciprocal calibration carry\tOPEN_LOAD_BEARING" in ledger, "reciprocal carry boundary")
mechanical = (HERE / "EXTERNAL_MECHANICAL_CLOSURE_REVIEW_RAW.md").read_text()
require("passes final mechanical closure" in mechanical, "mechanical closure landing")
require("observed child `no_site` flags `true/true`" in mechanical, "child no-site evidence")

premise = subprocess.run(
    [sys.executable, str(ROOT / "verify_current_scientific_premises.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
require(premise.returncode == 0, f"premise verifier\n{premise.stdout}\n{premise.stderr}")

result = {
    "status": "PASS__VERIFIED_WITH_CAVEATS__ENDPOINT_RELATIVE_THEOREM__CROSS_QUERY_CARRY_OPEN",
    "required_files": len(required),
    "source_hashes": len(rows),
    "production_checks": production["checks_total"],
    "independent_checks": independent["checks_passed"],
    "semantic_catches": catches["catches_total"],
    "premise_verifier_returncode": premise.returncode,
    "premise_verifier_stdout": premise.stdout.strip(),
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
