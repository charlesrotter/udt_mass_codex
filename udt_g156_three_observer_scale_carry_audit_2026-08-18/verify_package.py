#!/usr/bin/env python3
"""Package-level verifier for G156."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
QUALIFIED_LANDING = (
    "PAIR_METRIC_CANONICALLY_SUPPLIES_POSITIVE_HALF_DENSITY_SECTION__"
    "ANY_SUPPLIED_TYPED_CARRY_INDUCES_GAUGE_INVARIANT_LOG_DETERMINANT_CHARACTER__"
    "FULL_CLOSURE_IMPLIES_BUT_IS_NOT_IMPLIED_BY_SCALE_CLOSURE__"
    "OWNED_CHART_OVERLAP_AND_LEVI_CIVITA_CARRIES_ARE_SCALE_FLAT__"
    "ARBITRARY_SUPPLIED_NONISOMETRIC_CARRIES_NEED_NOT_BE_FLAT__"
    "NO_METRIC_OWNED_CROSS_QUERY_CARRY_OR_KAPPA_HISTORY"
)
REQUIRED = {
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "SOURCE_FREEZE.md",
    "derive_three_observer_scale_carry.py",
    "DERIVATION_RESULT.json",
    "verify_scale_carry_independent.py",
    "INDEPENDENT_RESULT.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "EXACT_DERIVATION.md",
    "CLAIM_LEDGER.tsv",
    "STATUS_LEDGER.tsv",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "EVIDENCE_GATES.md",
    "RUN_RECORD.md",
    "INTERNAL_ADVERSARIAL_REVIEW.md",
    "INTERNAL_REPAIR_FOLLOWUP.md",
    "PREMISE_VERIFIER_OUTPUT.txt",
    "verify_package.py",
}


def main() -> None:
    present = {path.name for path in HERE.iterdir() if path.is_file()}
    assert not (REQUIRED - present), sorted(REQUIRED - present)
    for script in (
        "derive_three_observer_scale_carry.py",
        "verify_scale_carry_independent.py",
        "run_catch_proofs.py",
    ):
        subprocess.run([sys.executable, str(HERE / script)], check=True, stdout=subprocess.DEVNULL)

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == QUALIFIED_LANDING
    assert production["registered_outcome_class"] == "CONDITIONAL_FLAT_SCALE_CARRY"
    assert independent["registered_outcome_class"] == "CONDITIONAL_FLAT_SCALE_CARRY"
    assert production["source_count"] == independent["source_count"] == 19
    assert production["exact_checks"] == len(production["exact_check_names"]) == 12
    assert independent["randomized_exact_trials"] == 500
    assert independent["sl2_kernel_counterexample"] is True
    assert catches["catch_count"] == 8 and all(item["caught"] for item in catches["caught"])
    report = (HERE / "AUDIT_REPORT.md").read_text()
    assert "CONDITIONAL_FLAT_SCALE_CARRY" in report and "NEED_NOT_BE_FLAT" in report
    assert "No canonization" in report
    premise = (HERE / "PREMISE_VERIFIER_OUTPUT.txt").read_text()
    assert "PASS: G156-extended premise guards" in premise
    assert "Status: `FOLLOWUP_PASS`" in (HERE / "INTERNAL_REPAIR_FOLLOWUP.md").read_text()
    result = {
        "status": "PASS",
        "required_files": len(REQUIRED),
        "source_count": 19,
        "exact_checks": 12,
        "independent_trials": 500,
        "catch_count": 8,
        "landing": QUALIFIED_LANDING,
        "registered_outcome_class": "CONDITIONAL_FLAT_SCALE_CARRY",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
