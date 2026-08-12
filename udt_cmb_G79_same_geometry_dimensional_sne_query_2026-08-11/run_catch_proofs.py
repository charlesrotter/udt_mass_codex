#!/usr/bin/env python3
"""Exercise the preregistered G79 fail-closed semantic catches."""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent


def validate(result: dict) -> None:
    assert result["status"] == "PASS"
    assert result["selected_profile"]["profile_id"] == "G75_AM_S01_E05"
    assert result["selected_profile"]["q_of_s"] == "s**2/20"
    assert result["q_coefficients_c0_c1_c2"] == [0.0, 0.0, 0.05]
    assert result["query"]["mixing_and_angular_sectors"] == "LIVE"
    assert result["query"]["source_control_sphere_x"] == 1.0
    assert result["distance"]["R_power"] == 1
    assert result["distance"]["physical_relation"] == "d_A=R*(dA_over_R)"
    assert result["distance"]["P1_type_match"].startswith("CONDITIONAL_REGISTERED_MATCH")
    assert result["redshift"]["one_plus_z_direct"] > 1.0
    assert result["redshift"]["absolute_direct_analytic_difference"] < 1.0e-10
    assert len(result["refinement"]) == 3
    assert [row["step_count"] for row in result["refinement"]] == [1024, 2048, 4096]
    assert math.isfinite(result["distance"]["dA_over_R"])
    authority = result["authority"]
    assert authority["maximum_conclusion"] == "DERIVED_CONDITIONAL_ON_ONE_FROZEN_GEOMETRY_AND_ONE_CHOSEN_STATIONARY_QUERY"
    assert authority["physical_profile_selected"] is False
    assert authority["R_selected"] is False
    assert authority["Xmax_identified"] is False
    assert authority["SNe_fit_performed"] is False
    assert authority["CMB_temperature_or_spectrum_derived"] is False


def caught(result: dict, mutation) -> bool:
    trial = copy.deepcopy(result)
    mutation(trial)
    try:
        validate(trial)
    except (AssertionError, KeyError, TypeError, ValueError):
        return True
    return False


def main() -> None:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    validate(result)
    catches = {
        "different_profile_rejected": caught(result, lambda r: r["selected_profile"].__setitem__("profile_id", "OTHER")),
        "zeroed_mixing_rejected": caught(result, lambda r: r.__setitem__("q_coefficients_c0_c1_c2", [0.0, 0.0, 0.0])),
        "dead_angular_mixing_label_rejected": caught(result, lambda r: r["query"].__setitem__("mixing_and_angular_sectors", "ZEROED")),
        "x1_to_Xmax_promotion_rejected": caught(result, lambda r: r["authority"].__setitem__("Xmax_identified", True)),
        "P1_metric_insertion_rejected": caught(result, lambda r: r["distance"].__setitem__("P1_type_match", "P1_DERIVED_METRIC_PROFILE")),
        "hidden_numeric_R_rejected": caught(result, lambda r: r["distance"].__setitem__("R_power", 0)),
        "redshift_sign_reversal_rejected": caught(result, lambda r: r["redshift"].__setitem__("one_plus_z_direct", 1.0 / r["redshift"]["one_plus_z_direct"])),
        "missing_refinement_rejected": caught(result, lambda r: r.__setitem__("refinement", r["refinement"][:2])),
        "SNe_fit_promotion_rejected": caught(result, lambda r: r["authority"].__setitem__("SNe_fit_performed", True)),
        "CMB_temperature_promotion_rejected": caught(result, lambda r: r["authority"].__setitem__("CMB_temperature_or_spectrum_derived", True)),
        "physical_profile_promotion_rejected": caught(result, lambda r: r["authority"].__setitem__("physical_profile_selected", True)),
        "R_selection_promotion_rejected": caught(result, lambda r: r["authority"].__setitem__("R_selected", True)),
    }
    assert all(catches.values())
    output = {
        "schema": "udt-cmb-g79-catch-proofs-v1",
        "status": "PASS",
        "catch_count": len(catches),
        "catches": catches,
    }
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

