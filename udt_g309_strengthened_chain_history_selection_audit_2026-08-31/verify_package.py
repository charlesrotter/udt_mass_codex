#!/usr/bin/env python3
"""No-write package verification for G309."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LANDING = (
    "FOUNDED_STRENGTHENED_CHAIN_REMAINS_COMPATIBILITY_ONLY"
    "__ROUND_HOPF_TIME_LIVE_COUNTERFAMILY_SURVIVES"
    "__CONDITIONAL_TRACEFREE_RESIDUAL_CLOSES_POSITIVE_STANDARD_COMPLETION_TO_ONE_SCALE"
    "__HOPF_STRUCTURE_DOES_NOT_OWN_OR_CALIBRATE_THAT_RESIDUAL"
)


def main() -> None:
    required = [
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
    ]
    for name in required:
        assert (ROOT / name).is_file(), name

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))

    assert production["landing"] == LANDING
    assert production["candidate"] == "B"
    assert production["base_q"] == "0"
    assert abs(float(production["deformed_q_numeric"])) > 1e-3
    assert independent["status"] == "PASS"
    assert independent["independent_checks"] == 28
    assert catches["status"] == "PASS"
    assert catches["hostile_cases"] == 4

    print(json.dumps({
        "status": "PASS",
        "required_files": len(required),
        "production_checks": production["symbolic_checks"],
        "independent_checks": independent["independent_checks"],
        "hostile_cases": catches["hostile_cases"],
        "landing": LANDING,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
