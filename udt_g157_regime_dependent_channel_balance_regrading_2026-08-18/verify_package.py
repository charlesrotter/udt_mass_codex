#!/usr/bin/env python3
"""Package-level verification for G157."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "MIXED_REGRADING__BPLUS2_NO_FIXED_CHANNEL_RATIO_DERIVED__"
    "REGIME_DEPENDENT_BASE_BALANCE_ALLOWED_BY_NATIVE_SEMIDIRECT_COMPOSITION__"
    "SUPPLIED_VALUED_HISTORY_CAN_CARRY_CHANGING_SCORE__FULL_SCREEN_MIXING_"
    "COMPOSITION_PHYSICAL_CROSS_QUERY_CARRY_AND_HISTORY_EVOLUTION_REMAIN_OPEN"
)
REQUIRED = {
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "SOURCE_FREEZE.md",
    "REGRADING_LEDGER.tsv",
    "derive_regime_balance.py",
    "DERIVATION_RESULT.json",
    "verify_regime_balance_independent.py",
    "INDEPENDENT_RESULT.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "EXACT_DERIVATION.md",
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
        "derive_regime_balance.py",
        "verify_regime_balance_independent.py",
        "run_catch_proofs.py",
    ):
        subprocess.run([sys.executable, str(HERE / script)], check=True, stdout=subprocess.DEVNULL)
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == LANDING
    assert production["registered_outcome_class"] == independent["registered_outcome_class"] == "MIXED_REGRADING"
    assert production["source_count"] == independent["source_count"] == 20
    assert production["ledger_count"] == independent["ledger_count"] == 20
    assert production["exact_checks"] == len(production["exact_check_names"]) == 10
    assert independent["semidirect_exact_trials"] == 500
    assert independent["one_parameter_subgroup_trials"] == 300
    assert independent["one_parameter_subgroup_nonzero_q_trials"] == 200
    assert independent["one_parameter_subgroup_zero_q_trials"] == 100
    assert catches["catch_count"] == 6 and all(item["caught"] for item in catches["caught"])
    assert production["active_depth_only_lockstep_sources"] == 0
    assert production["regime_dependent_balance_kinematically_allowed"] is True
    assert production["physical_regime_score_derived"] is False
    assert "FOLLOWUP_PASS" in (HERE / "INTERNAL_REPAIR_FOLLOWUP.md").read_text()
    assert "PASS: G157-extended premise guards" in (HERE / "PREMISE_VERIFIER_OUTPUT.txt").read_text()
    report = (HERE / "AUDIT_REPORT.md").read_text()
    assert LANDING in report and "No canonization" in report
    result = {
        "status": "PASS",
        "required_files": len(REQUIRED),
        "source_count": 20,
        "ledger_count": 20,
        "exact_checks": 10,
        "independent_semidirect_trials": 500,
        "independent_subgroup_trials": 300,
        "catch_count": 6,
        "landing": LANDING,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
