#!/usr/bin/env python3
"""Hostile semantic/algebraic catches for the bounded G80 result."""

from __future__ import annotations

import copy
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def valid(data: dict) -> None:
    assert data["status"] == "PASS"
    assert data["profile_id"] == "G75_AM_S01_E05"
    assert data["query_type"] == "past_directed_mathematical_reversal_of_same_null_curve_not_future_signal"
    assert data["reciprocity"]["Z_times_inverse_Z_minus_one"] < 1.0e-10
    assert data["reciprocity"]["phi_sum_absolute"] < 1.0e-10
    assert data["reciprocity"]["D_relative"] < 1.0e-8
    assert data["reciprocity"]["dA_ratio_minus_Z"] < 1.0e-8
    assert data["authority"]["past_directed_reversal_only"] is True
    assert data["authority"]["future_signal_derived"] is False
    assert data["authority"]["physical_profile_or_endpoint_selected"] is False
    assert data["authority"]["Xmax_identified"] is False
    assert data["authority"]["cmb_temp_activated"] is False


def caught(base: dict, path: tuple[str, ...], value: object) -> bool:
    trial = copy.deepcopy(base)
    target = trial
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    try:
        valid(trial)
    except AssertionError:
        return True
    return False


def main() -> None:
    base = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    valid(base)
    cases = {
        "spatial_only_or_future_reversal_rejected": caught(base, ("query_type",), "future_directed_spatial_flip"),
        "wrong_source_normalization_rejected": caught(base, ("reciprocity", "Z_times_inverse_Z_minus_one"), 0.1),
        "wrong_redshift_sign_rejected": caught(base, ("reciprocity", "phi_sum_absolute"), 0.1),
        "missing_transpose_or_map_error_rejected": caught(base, ("reciprocity", "D_relative"), 0.1),
        "missing_Z_area_factor_rejected": caught(base, ("reciprocity", "dA_ratio_minus_Z"), 0.1),
        "different_profile_rejected": caught(base, ("profile_id",), "G75_AM_S01_E10"),
        "future_signal_promotion_rejected": caught(base, ("authority", "future_signal_derived"), True),
        "physical_profile_promotion_rejected": caught(base, ("authority", "physical_profile_or_endpoint_selected"), True),
        "Xmax_promotion_rejected": caught(base, ("authority", "Xmax_identified"), True),
        "cmb_temp_activation_rejected": caught(base, ("authority", "cmb_temp_activated"), True),
    }
    output = {
        "schema": "udt-cmb-g80-catch-proofs-v1",
        "status": "PASS" if all(cases.values()) else "FAIL",
        "catch_count": len(cases),
        "catches": cases,
    }
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    assert output["status"] == "PASS"


if __name__ == "__main__":
    main()
