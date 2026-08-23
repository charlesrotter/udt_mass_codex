#!/usr/bin/env python3
"""Hostile semantic mutations for G239."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from derive_reference_operator import LANDING, compute


ROOT = Path(__file__).resolve().parent


def exact(payload: dict[str, object]) -> str:
    return str(payload["exact"])


def validate(result: dict[str, object]) -> None:
    if result["landing"] != LANDING:
        raise AssertionError("landing changed")
    if result["boss_outcomes_opened"] is not False:
        raise AssertionError("outcome gate opened")
    if result["feature_or_scale_used"] is not False or result["profile_fit_performed"] is not False:
        raise AssertionError("feature, scale, or fit inserted")
    if not str(result["source_status"]).startswith("CHOSE_OBSERVATIONAL_HYPOTHESIS"):
        raise AssertionError("source hypothesis promoted")
    if "NOT_PHYSICAL_SOURCE_LAW" not in str(result["reference_status"]):
        raise AssertionError("reference promoted to source law")
    if "postreadout_coefficient" in result:
        raise AssertionError("post-readout coefficient inserted")

    witness = result["factorized_witness"]
    if exact(witness["landy_szalay"]) != "-1/6":
        raise AssertionError("LS sign or normalization changed")
    if exact(witness["mismatch_form"]) != exact(witness["landy_szalay"]):
        raise AssertionError("quadratic mismatch identity changed")
    if witness["nonzero"] is not True:
        raise AssertionError("survival witness disabled")

    cancellations = result["cancellation_controls"]
    if cancellations["constant_response_p_equals_q"] is not True:
        raise AssertionError("common response no longer cancels")
    if exact(cancellations["constant_response_landy_szalay"]) != "0/1":
        raise AssertionError("common response has spurious signal")
    if exact(cancellations["matched_reference_landy_szalay"]) != "0/1":
        raise AssertionError("matched reference has spurious signal")

    connected = result["connected_control"]
    if connected["decomposition_exact"] is not True:
        raise AssertionError("connected term omitted")
    if exact(connected["connected_term"]) != "-1/240":
        raise AssertionError("connected term changed")
    if connected["pair_measure_nonnegative"] is not True:
        raise AssertionError("connected witness left measure cone")

    metric = result["metric_local_jacobi_liveness"]
    if exact(metric["tilted_trace"]) != "12/25":
        raise AssertionError("metric tidal trace changed")
    if exact(metric["jacobi_determinant_lambda4_coefficient"]) != "-2/25":
        raise AssertionError("metric Jacobi area coefficient changed")
    if result["branch_factorization"]["direct_product_equals_product_pushforward"] is not True:
        raise AssertionError("Poisson branch factorization changed")

    required_absent = {
        "P1",
        "X_max",
        "Lambda-CDM distance",
        "BOSS curve value",
        "feature location",
        "fitted coefficient",
        "post-readout orchestra",
        "protected package",
    }
    if set(result["forbidden_inputs_absent"]) != required_absent:
        raise AssertionError("forbidden-input guard changed")


def mutate(base: dict[str, object], name: str) -> dict[str, object]:
    result = copy.deepcopy(base)
    if name == "ls_sign_or_normalization":
        result["factorized_witness"]["landy_szalay"]["exact"] = "1/6"
    elif name == "matched_reference_nonzero":
        result["cancellation_controls"]["matched_reference_landy_szalay"]["exact"] = "1/100"
    elif name == "common_response_nonzero":
        result["cancellation_controls"]["constant_response_landy_szalay"]["exact"] = "1/100"
    elif name == "connected_term_omission":
        result["connected_control"]["decomposition_exact"] = False
    elif name == "metric_liveness_deletion":
        result["metric_local_jacobi_liveness"]["jacobi_determinant_lambda4_coefficient"]["exact"] = "0/1"
    elif name == "source_promotion":
        result["source_status"] = "DERIVED_NATIVE_UDT_SOURCE_LAW"
    elif name == "reference_promotion":
        result["reference_status"] = "PHYSICAL_SOURCE_LAW"
    elif name == "outcome_opening":
        result["boss_outcomes_opened"] = True
    elif name == "feature_or_scale_insertion":
        result["feature_or_scale_used"] = True
    elif name == "postreadout_coefficient":
        result["postreadout_coefficient"] = 0.7
    elif name == "forbidden_guard_removal":
        result["forbidden_inputs_absent"].remove("X_max")
    else:
        raise KeyError(name)
    return result


def main() -> None:
    base = compute()
    validate(base)
    names = (
        "ls_sign_or_normalization",
        "matched_reference_nonzero",
        "common_response_nonzero",
        "connected_term_omission",
        "metric_liveness_deletion",
        "source_promotion",
        "reference_promotion",
        "outcome_opening",
        "feature_or_scale_insertion",
        "postreadout_coefficient",
        "forbidden_guard_removal",
    )
    cases = []
    for name in names:
        caught = False
        try:
            validate(mutate(base, name))
        except AssertionError:
            caught = True
        cases.append({"mutation": name, "caught": caught})
    result = {
        "audit": "G239_CATCH_PROOFS",
        "status": "PASS" if all(case["caught"] for case in cases) else "FAIL",
        "cases": cases,
    }
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

