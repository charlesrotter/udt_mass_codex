#!/usr/bin/env python3
"""Mechanical closure gate for the bounded G99 package."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition: bool, label: str, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks[label] = "PASS"


def main() -> None:
    contract = json.loads((HERE / "CALIBRATION_CONTRACT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    holdout = (HERE / "HOLDOUT_LEDGER.tsv").read_text(encoding="utf-8")
    caveats = (HERE / "RESULT_CAVEAT_LEDGER.tsv").read_text(encoding="utf-8")
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    checks: dict[str, str] = {}

    require(
        contract["status"] == "OBSERVED_CONDITIONAL_TERMINAL_CALIBRATION_FROZEN",
        "registered_status",
        checks,
    )
    require(contract["construction"]["optimizer_run"] is False, "no_optimizer", checks)
    require(contract["construction"]["holdout_data_read"] is False, "no_holdout_read", checks)
    require(contract["construction"]["source_count"] == 10, "source_count", checks)
    require(contract["complete_metric_history_owned"] is False, "history_open", checks)
    require(contract["physical_pair_realization_owned"] is False, "pair_open", checks)
    require(contract["transfer_law_derived"] is False, "transfer_conditional", checks)
    require(contract["absolute_scale_is_conditional"] is True, "anchor_conditional", checks)
    require(contract["R_w_is_marginal_measurement"] is False, "Rw_joint_only", checks)
    require(
        contract["joint_n_X_eff_covariance_available"] is False,
        "joint_covariance_unavailable",
        checks,
    )
    require(
        contract["marginal_intervals_form_independent_box"] is False,
        "interval_box_forbidden",
        checks,
    )
    require(contract["domain"]["is_Xmax_interval"] is False, "not_Xmax_interval", checks)
    require(len(contract["nodes"]) == 6, "node_count", checks)
    require(independent["status"] == "PASS", "independent_pass", checks)
    require(independent["imports_production_extractor"] is False, "independent_codepath", checks)
    require(catches["status"] == "PASS", "catch_status", checks)
    require(catches["mutation_count"] == 11, "catch_count", checks)
    require("no new fit" in prereg, "prereg_no_fit", checks)
    require("strict forward holdout" in prereg, "prereg_holdout", checks)
    require("effective dL_cal(z)" in ledger, "object_type_ledger", checks)
    require("BAO\tNONE" in holdout and "CMB\tNONE" in holdout, "holdout_ledger", checks)
    require("NOT_PRESENT_IN_FROZEN_G65_ARTIFACTS" in caveats, "covariance_caveat", checks)
    require("INTERNALLY_VERIFIED_WITH_CAVEATS" in audit, "audit_grade", checks)
    require("dr_cal/dz = 2 X_eff" in exact, "exact_origin_slope", checks)
    require("not yet a spacetime model" in lay, "lay_scope", checks)

    result = {
        "schema": "udt-observed-middle-regime-pair-calibration-package-1.0",
        "status": "PASS",
        "check_count": len(checks),
        "checks": checks,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS G99 package {len(checks)}/{len(checks)}")


if __name__ == "__main__":
    main()
