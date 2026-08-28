#!/usr/bin/env python3
"""Fail-closed verification of preregistered G289 external repairs R1--R4."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "REPAIR_RESULT.json"
LANDING = (
    "LOCAL_NULL_DIRECTION_EMBEDDING_EXISTS"
    "__FIXED_ROUND_S2_HOPFION_REQUIRES_SUPPLIED_FRAME_TARGET_AND_BOUNDARY"
    "__RAW_HOPF_CLASS_DOES_NOT_DESCEND_THROUGH_FULL_LOCAL_FRAME_GAUGE"
    "__CONFORMAL_HISTORY_TWINS_CARRY_THE_SAME_NULL_TEXTURE"
    "__STATIC_HOPFION_IS_CONDITIONALLY_COMPATIBLE_NOT_A_CURRENT_HISTORY_SELECTOR"
)


def ledger(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return {row[key]: row for row in csv.DictReader(stream, delimiter="\t")}


def main() -> None:
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    premise_rows = ledger(HERE / "PREMISE_LEDGER.tsv", "item")
    compatibility_rows = ledger(HERE / "COMPATIBILITY_LEDGER.tsv", "layer")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    catch_source = (HERE / "run_catch_proofs.py").read_text(encoding="utf-8")
    independent_source = (HERE / "verify_independent.py").read_text(encoding="utf-8")

    checks = {
        "R1_premise_status_restored": premise_rows["historical_static_stability"]["status"]
        == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
        "R1_compatibility_status_restored": compatibility_rows["static_stability"]["status"]
        == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
        "R1_report_status_restored": "SETTLED_STATIC_FINITE_BOX_CONDITIONAL" in report
        and "OBSERVED_CARRIER_CONDITIONAL" not in report,
        "R2_four_primitive_recomputations": catches["recomputing_geometric_catches"] == 4
        and set(catches["recomputed_witnesses"])
        == {
            "false_null_norm",
            "boost_target_scale",
            "flat_center_scalar",
            "curved_center_scalar",
            "rotated_component_charge",
        },
        "R2_recomputation_functions_present": all(
            token in catch_source
            for token in (
                "pushed_tangent_norm",
                "conformal_center_scalar",
                "normalized_hopf_connection_integral",
            )
        ),
        "R3_integral_recomputed": independent["hopf_integral_recomputed"] is True
        and independent["hopf_connection_normalized_integral"] == "-1",
        "R3_basepoint_recomputed": independent["compactification_basepoint_fixed"] is True
        and independent["basepoint_adjoint_identity"] is True,
        "R3_exterior_and_adjoint_methods_present": "def wedge(" in independent_source
        and "def quaternion_adjoint(" in independent_source,
        "R4_computed_count_separated": production["computed_check_count"] == 17
        and production["check_count"] == 17
        and all(production["computed_checks"].values()),
        "R4_conclusion_count_separated": production["derived_conclusion_count"] == 6
        and production["total_claim_flags"] == 23
        and all(production["derived_conclusions"].values()),
        "R4_old_report_overcount_absent": "23 fresh" not in report
        and "23 fresh" not in (HERE / "RUN_RECORD.md").read_text(encoding="utf-8"),
        "scientific_landing_unchanged": production["landing"] == LANDING and LANDING in "".join(report.split()),
        "external_accept_with_repairs_recorded": "ACCEPT_WITH_REPAIRS"
        in (HERE / "EXTERNAL_REVIEW_GPT54.md").read_text(encoding="utf-8"),
        "repair_preregistered": all(
            f"R{index}" in (HERE / "EXTERNAL_REPAIR_PREREGISTRATION.md").read_text(encoding="utf-8")
            for index in range(1, 5)
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"G289 repair checks failed: {failed}")

    result = {
        "status": "PASS",
        "preregistration_commit": "ce1f4829",
        "repairs": ["R1", "R2", "R3", "R4"],
        "checks": checks,
        "scientific_landing_changed": False,
        "repair_followup": "OPEN",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
