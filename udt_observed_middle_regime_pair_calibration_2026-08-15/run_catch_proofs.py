#!/usr/bin/env python3
"""Hostile semantic mutations for the G99 calibration contract."""

from __future__ import annotations

import copy
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def validate(contract: dict[str, object]) -> None:
    if contract["object_type"] != "effective_terminal_observer_pair_luminosity_relation":
        raise AssertionError("calibration object was promoted or retyped")
    if contract["complete_metric_history_owned"] is not False:
        raise AssertionError("complete history was promoted")
    if contract["absolute_scale_is_conditional"] is not True:
        raise AssertionError("external luminosity anchor condition was dropped")
    if contract["R_w_is_marginal_measurement"] is not False:
        raise AssertionError("R_w was promoted to a marginal measurement")
    if contract["joint_n_X_eff_covariance_available"] is not False:
        raise AssertionError("unbanked joint covariance was claimed")
    if contract["marginal_intervals_form_independent_box"] is not False:
        raise AssertionError("profile intervals were promoted to an independent box")
    if contract["domain"]["is_Xmax_interval"] is not False:
        raise AssertionError("SNe interval was promoted to Xmax interval")
    if contract["orchestra_correction_appended"] is not False:
        raise AssertionError("unowned orchestra correction was appended")
    if contract["construction"]["holdout_data_read"] is not False:
        raise AssertionError("holdout data contaminated construction")
    if contract["transfer_law_derived"] is not False:
        raise AssertionError("conditional transfer was promoted")
    if contract["c_eff_is_material_signal_speed"] is not False:
        raise AssertionError("pair readout was promoted to material signal speed")
    required = {"BAO", "CMB", "Xmax_endpoint", "micro_mass", "bootstrap"}
    if set(contract["holdouts"]) != required:
        raise AssertionError("holdout set changed")


def main() -> None:
    baseline = json.loads((HERE / "CALIBRATION_CONTRACT.json").read_text(encoding="utf-8"))
    validate(baseline)
    mutations = {
        "promote_complete_history": lambda value: value.__setitem__(
            "complete_metric_history_owned", True
        ),
        "drop_anchor_condition": lambda value: value.__setitem__(
            "absolute_scale_is_conditional", False
        ),
        "promote_Rw_marginal": lambda value: value.__setitem__(
            "R_w_is_marginal_measurement", True
        ),
        "invent_joint_covariance": lambda value: value.__setitem__(
            "joint_n_X_eff_covariance_available", True
        ),
        "independent_interval_box": lambda value: value.__setitem__(
            "marginal_intervals_form_independent_box", True
        ),
        "identify_SNe_domain_with_Xmax": lambda value: value["domain"].__setitem__(
            "is_Xmax_interval", True
        ),
        "append_orchestra_correction": lambda value: value.__setitem__(
            "orchestra_correction_appended", True
        ),
        "read_holdout": lambda value: value["construction"].__setitem__(
            "holdout_data_read", True
        ),
        "promote_transfer": lambda value: value.__setitem__("transfer_law_derived", True),
        "promote_signal_speed": lambda value: value.__setitem__(
            "c_eff_is_material_signal_speed", True
        ),
        "drop_CMB_holdout": lambda value: value.__setitem__(
            "holdouts", [item for item in value["holdouts"] if item != "CMB"]
        ),
    }
    results: dict[str, str] = {}
    for name, mutation in mutations.items():
        candidate = copy.deepcopy(baseline)
        mutation(candidate)
        try:
            validate(candidate)
        except AssertionError:
            results[name] = "PASS_REJECTED"
        else:
            raise AssertionError(f"hostile mutation survived: {name}")
    output = {
        "schema": "udt-observed-middle-regime-pair-calibration-catches-1.0",
        "status": "PASS",
        "baseline": "PASS",
        "mutation_count": len(mutations),
        "results": results,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS G99 catch proofs {len(mutations)}/{len(mutations)}")


if __name__ == "__main__":
    main()
