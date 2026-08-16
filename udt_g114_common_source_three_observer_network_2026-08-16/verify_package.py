#!/usr/bin/env python3
"""Verify G114 source hashes, saved results, and scope guards."""

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
pkg = Path(__file__).resolve().parent
preregistration_commit = "38f7b665"

required = [
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "AUDIT_REPORT.md",
    "EXACT_DERIVATION.md",
    "LAY_REPORT.md",
    "NEXT_GATE.md",
    "TYPE_AND_PREMISE_LEDGER.tsv",
    "STATUS_LEDGER.tsv",
    "SYMBOLIC_VERIFICATION_RESULT.json",
    "INDEPENDENT_VERIFICATION_RESULT.json",
    "EVIDENCE_GATES.md",
    "STATUS.md",
    "CORRECTION_RECORD.md",
    "BLIND_REVIEW_ADJUDICATION.md",
    "PACKAGE_VERIFICATION_RESULT.json",
    "verify_common_source_network.py",
    "verify_common_source_independent.py",
]
missing = [name for name in required if not (pkg / name).is_file()]

hash_ok = True
rows = []
with (pkg / "SOURCE_MANIFEST.tsv").open(newline="") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        p = root / row["path"]
        if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.md":
            frozen = subprocess.check_output(
                ["git", "show", f"{preregistration_commit}:{row['path']}"], cwd=root
            )
            actual = hashlib.sha256(frozen).hexdigest()
        else:
            actual = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        ok = actual == row["sha256"]
        rows.append({"path": row["path"], "ok": ok})
        hash_ok &= ok

symbolic = json.loads((pkg / "SYMBOLIC_VERIFICATION_RESULT.json").read_text())
independent = json.loads((pkg / "INDEPENDENT_VERIFICATION_RESULT.json").read_text())
fresh_symbolic = json.loads(subprocess.check_output(
    [sys.executable, str(pkg / "verify_common_source_network.py")], text=True
))
fresh_independent = json.loads(subprocess.check_output(
    [sys.executable, str(pkg / "verify_common_source_independent.py")], text=True
))
audit = (pkg / "AUDIT_REPORT.md").read_text()
exact = (pkg / "EXACT_DERIVATION.md").read_text()
ledger = (pkg / "TYPE_AND_PREMISE_LEDGER.tsv").read_text()
review = (pkg / "BLIND_REVIEW_ADJUDICATION.md").read_text()

guards = {
    "no_missing_files": not missing,
    "all_source_hashes": hash_ok,
    "symbolic_pass": symbolic.get("status") == "PASS",
    "independent_pass": independent.get("status") == "PASS",
    "fresh_symbolic_exactly_matches_saved": fresh_symbolic == symbolic,
    "fresh_independent_exactly_matches_saved": fresh_independent == independent,
    "caustic_scope": "inverse-`D` filtering" in audit,
    "beam_compatibility_explicit": "beam-intersection rank" in audit,
    "history_open": "physical complete metric history" in audit,
    "source_transfer_open": "source transfer" in audit,
    "scalar_reduction_conditional": "common reciprocal calibration" in audit,
    "no_signalling_claim": "not a signal" in exact,
    "premise_ledger_open_slots": all(x in ledger for x in ["source transfer", "physical history", "X_max"]),
    "blind_followup_pass": "PASS" in review and "No required repair remains" in review,
}

result = {
    "status": "PASS" if all(guards.values()) else "FAIL",
    "guards": guards,
    "manifest_rows": len(rows),
    "missing": missing,
    "preregistration_commit": preregistration_commit,
}
print(json.dumps(result, indent=2, sort_keys=True))
if result["status"] != "PASS":
    raise SystemExit(1)
