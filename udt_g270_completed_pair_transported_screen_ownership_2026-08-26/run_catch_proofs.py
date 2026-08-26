#!/usr/bin/env python3
"""G270 shared-validator mutation catches."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"


BASE = {
    "intrinsic_depends_on_w": False,
    "same_pullback_different_w": True,
    "full_realization_evaluates_w": True,
    "completed_det": "-1",
    "gamma_interlock": "cosh_delta_plus_rW2_over_2",
    "frequency_orientation": "omega_A_over_omega_B",
    "mutual_readout": "inverse_gamma",
    "w_channel": "endpoint_clock_transport_projection",
    "w_is_jacobi": False,
    "query_supplied": True,
    "history_selected": False,
}


def validate(candidate: dict[str, object]) -> list[str]:
    failures: list[str] = []
    if candidate["intrinsic_depends_on_w"] is not False:
        failures.append("intrinsic_w_blindness")
    if candidate["same_pullback_different_w"] is not True:
        failures.append("same_pullback_separator")
    if candidate["full_realization_evaluates_w"] is not True:
        failures.append("realization_evaluation")
    if candidate["completed_det"] != "-1":
        failures.append("completed_reciprocity")
    if candidate["gamma_interlock"] != "cosh_delta_plus_rW2_over_2":
        failures.append("g269_interlock")
    if candidate["frequency_orientation"] != "omega_A_over_omega_B":
        failures.append("frequency_orientation")
    if candidate["mutual_readout"] != "inverse_gamma":
        failures.append("inverse_gamma_readout")
    if candidate["w_channel"] != "endpoint_clock_transport_projection":
        failures.append("transported_mismatch_type")
    if candidate["w_is_jacobi"] is not False:
        failures.append("no_jacobi_conflation")
    if candidate["query_supplied"] is not True:
        failures.append("query_status")
    if candidate["history_selected"] is not False:
        failures.append("no_history_promotion")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    mutations = {
        "force_w_zero": ("same_pullback_different_w", False, "same_pullback_separator"),
        "insert_w_into_intrinsic_metric": ("intrinsic_depends_on_w", True, "intrinsic_w_blindness"),
        "deny_realization_evaluation": ("full_realization_evaluates_w", False, "realization_evaluation"),
        "break_completed_determinant": ("completed_det", "-1-W2", "completed_reciprocity"),
        "delete_screen_interlock": ("gamma_interlock", "cosh_delta", "g269_interlock"),
        "reverse_frequency_ratio": ("frequency_orientation", "omega_B_over_omega_A", "frequency_orientation"),
        "drop_inverse_readout": ("mutual_readout", "gamma", "inverse_gamma_readout"),
        "rename_w_as_jacobi_area": ("w_channel", "jacobi_area", "transported_mismatch_type"),
        "conflate_w_with_jacobi": ("w_is_jacobi", True, "no_jacobi_conflation"),
        "delete_query_supply": ("query_supplied", False, "query_status"),
        "promote_history": ("history_selected", True, "no_history_promotion"),
    }

    baseline = validate(BASE)
    results: dict[str, dict[str, object]] = {}
    for name, (key, value, target) in mutations.items():
        candidate = copy.deepcopy(BASE)
        candidate[key] = value
        failures = validate(candidate)
        results[name] = {
            "caught": bool(failures),
            "targeted_caught": target in failures,
            "targeted_failure": target,
            "failures": failures,
        }

    missed = [name for name, item in results.items() if not item["targeted_caught"]]
    result = {
        "status": "PASS" if not baseline and not missed else "FAIL",
        "baseline_failures": baseline,
        "mutations": results,
        "catches": sum(bool(item["targeted_caught"]) for item in results.values()),
        "missed": missed,
        "shared_validator_exercised": True,
    }
    assert result["status"] == "PASS", result
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
