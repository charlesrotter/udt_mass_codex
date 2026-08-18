#!/usr/bin/env python3
"""Package-level G155 verification."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REQUIRED = {
    "WHITEBOARD_SYNTHESIS.md",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "SOURCE_FREEZE.md",
    "EQUATION_ROLE_LEDGER.tsv",
    "derive_scale_sector_closure.py",
    "DERIVATION_RESULT.json",
    "verify_scale_sector_independent.py",
    "INDEPENDENT_RESULT.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "EVIDENCE_GATES.md",
    "RUN_RECORD.md",
    "INTERNAL_ADVERSARIAL_REVIEW.md",
    "INTERNAL_REPAIR_FOLLOWUP.md",
    "REVIEW_ADJUDICATION.md",
    "PREMISE_VERIFIER_OUTPUT.txt",
    "verify_package.py",
}


def main() -> None:
    present = {p.name for p in HERE.iterdir() if p.is_file()}
    missing = sorted(REQUIRED - present)
    assert not missing, missing
    for script in (
        "derive_scale_sector_closure.py",
        "verify_scale_sector_independent.py",
        "run_catch_proofs.py",
    ):
        subprocess.run([sys.executable, str(HERE / script)], check=True, stdout=subprocess.DEVNULL)
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == "RANK_ZERO"
    assert production["common_scale_physical_history_principal_rank"] == 0
    assert independent["common_scale_physical_history_principal_rank"] == 0
    assert production["source_count"] == independent["manifest_files"] == 41
    assert production["exact_checks"] == len(production["exact_check_names"]) == 9
    assert independent["three_observer_conformal_triangle_trials"] == 500
    assert catches["catch_count"] == 6
    assert all(item["caught"] for item in catches["caught"])
    report = (HERE / "AUDIT_REPORT.md").read_text()
    assert "RANK_ZERO__NO_ACTIVE_NONIDENTITY_COMMON_SCALE_HISTORY_EQUATION" in report
    assert "No canonization" in report
    assert "PASS: G155-extended premise guards" in (HERE / "PREMISE_VERIFIER_OUTPUT.txt").read_text()
    result = {
        "status": "PASS",
        "required_files": len(REQUIRED),
        "source_count": 41,
        "ledger_count": 41,
        "landing": "RANK_ZERO",
        "principal_rank": 0,
        "catch_count": 6,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
