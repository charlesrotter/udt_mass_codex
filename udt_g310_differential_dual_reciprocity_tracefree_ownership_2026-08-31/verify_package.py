#!/usr/bin/env python3
"""No-write live package verification for G310."""

from __future__ import annotations

import json
from pathlib import Path

from derive_ddr_tracefree import LANDING, build_result as build_production
from run_catch_proofs import build_result as build_catches
from verify_ddr_independent import build_result as build_independent


ROOT = Path(__file__).resolve().parent


def main() -> None:
    required = (
        "AUDIT_REPORT.md",
        "COMMANDS.md",
        "CATCH_PROOF_RESULT.json",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md",
        "EXTERNAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_RESPONSE.md",
        "EXTERNAL_REVIEW_TRANSCRIPT.txt",
        "EXTERNAL_REVIEW_TRANSMISSION.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "PONDER.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "PREREGISTRATION_ANCESTRY.md",
        "REPAIR_IMPLEMENTATION.md",
        "RUN_RECORD.md",
        "SOURCE_SCOPE.tsv",
        "STATUS_LEDGER.tsv",
        "EXTERNAL_REVIEW_REPAIR_REQUEST.md",
    )
    for name in required:
        assert (ROOT / name).is_file(), name

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert production == build_production()
    assert independent == build_independent()
    assert catches == build_catches()
    assert production["landing"] == LANDING
    assert production["reciprocal_shape_rank"] == 9
    assert production["reciprocal_tangent_normalization"].startswith("H=2*")
    assert production["annihilator_nullity"] == 1
    assert production["nondegenerate_gate"] == "a!=0"
    assert production["scale_status"] == "not fixed by DDR"
    assert independent["status"] == "PASS"
    assert independent["constructive_shape_rank"] == 9
    assert independent["tangent_normalization"].startswith("H=2*")
    assert independent["lorentz_pairing_rank"] == 9
    assert independent["annihilator_nullity"] == 1
    assert independent["annihilator_derived_from_balance_rows"] is True
    assert catches["status"] == "PASS"
    assert catches["hostile_cases"] == 7

    print(json.dumps({
        "status": "PASS",
        "required_files": len(required),
        "production_checks": production["production_checks"],
        "independent_checks": independent["independent_checks"],
        "hostile_cases": catches["hostile_cases"],
        "landing": LANDING,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
