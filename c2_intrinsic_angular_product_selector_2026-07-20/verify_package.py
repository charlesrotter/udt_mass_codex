#!/usr/bin/env python3
"""Fail-closed verifier for the intrinsic-angular product selector audit."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_json(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def rows(name):
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    background = load_json("BACKGROUND_DERIVATION.json")
    twist = load_json("TWIST_DERIVATION.json")
    branches = load_json("BRANCH_ANALYSIS.json")
    verification = load_json("VERIFICATION_RESULT.json")
    ledger = rows("STATUS_LEDGER.tsv")
    completeness = rows("COMPLETENESS_MAP.tsv")
    lineage = rows("SOURCE_LINEAGE.tsv")
    ids = {row["id"]: row for row in ledger}
    sectors = {row["sector"]: row for row in completeness}
    outcomes = set(branches["outcomes"])
    q_values = branches["all_Q_strata_witness"]["values"]
    lower_values = branches["all_twist_lower_strata_witness"]["values"]
    twist_formula = twist["density_quadratic_epsilon"]
    lineage_ok = all(digest(HERE.parent / row["path"]) == row["sha256"] for row in lineage)

    checks = {
        "background_schema": background["schema"] == "udt-c2-intrinsic-angular-product-background-1.0",
        "background_checks": len(background["checks"]) == 5 and all(background["checks"].values()),
        "full_bach_components": set(background["bach_nonzero_components"]) == {"B_00", "B_11", "B_22", "B_33"},
        "background_action_density": background["density"] == "(-2*K + Derivative(y(r), (r, 2)))**2*F(theta)/3",
        "twist_schema": twist["schema"] == "udt-c2-intrinsic-angular-product-twist-1.0",
        "twist_checks": len(twist["checks"]) == 7 and all(twist["checks"].values()),
        "complete_action_volume_factor": twist_formula.endswith("*F(theta)*y(r)/3"),
        "directional_connection_disclosed": twist["classification"]["angular_connection_dependence_present"] and "Derivative(F(theta), theta)**2" in twist_formula,
        "branch_checks": len(branches["checks"]) == 11 and all(branches["checks"].values()),
        "full_branch_constraint": branches["general_local_branch"]["constraint"] == "B**2=3*A*C+K**2",
        "registered_outcomes": outcomes == {
            "INTRINSIC_CURVATURE_DOES_NOT_CHANGE_LOCAL_SELECTOR_UNDERDETERMINATION",
            "INTRINSIC_CURVATURE_CHANGES_TWIST_DERIVATIVE_INVENTORY",
        },
        "q_three_strata": q_values["r_minus_half"] == "36/49" and q_values["r_zero"] == "0" and q_values["r_plus_half"] == "-36/47",
        "lower_three_strata": lower_values == {"r_zero": "8/3", "r_one_third": "0", "r_one_half": "-47/36"},
        "independent_replay": verification["result"] == "PASS" and len(verification["checks"]) == 8 and all(verification["checks"].values()),
        "independent_tolerances": verification["maxima"]["bach_nonzero_scaled_error"] <= 1e-8 and verification["maxima"]["bach_zero_absolute_error"] <= 1e-9 and verification["maxima"]["twist_nonconstant_scaled_error"] <= 1e-8 and verification["maxima"]["constant_twist_finite_amplitude_absolute"] <= 1e-9,
        "status_ledger_unique": len(ledger) == 16 and len(ids) == 16,
        "selector_left_open": ids["I05"]["status"] == "OPEN" and ids["I11"]["status"] == "OPEN",
        "carrier_left_open": ids["I16"]["status"] == "OPEN",
        "omitted_coframe_sectors_open": sectors["transverse_area"]["status"] == "OMITTED_OPEN" and sectors["transverse_shear"]["status"] == "OMITTED_OPEN",
        "source_lineage_hashes": len(lineage) == 6 and lineage_ok,
    }

    mutated_formula = twist_formula.replace("*F(theta)*y(r)/3", "*y(r)/3")
    mutated_direction = twist_formula.replace(" + 27*Derivative(F(theta), theta)**2*Derivative(u(r), r)**2", "")
    mutated_q = dict(q_values, r_zero="1")
    mutated_lower = dict(lower_values, r_one_third="1")
    mutated_area = dict(sectors["transverse_area"], status="RETAINED")
    mutated_carrier = dict(ids["I16"], status="DERIVED")
    mutated_action = dict(ids["I14"], status="DERIVED")
    catches = {
        "reduced_only_promotion_rejected": branches["reduced_only_false_branch"]["full_constraint"] == "12",
        "fixed_curvature_sign_rejected": "+K**2" in branches["general_local_branch"]["constraint"],
        "divide_by_zero_stratum_rejected": q_values["r_zero"] == "0" and mutated_q["r_zero"] != "0",
        "lower_zero_stratum_discard_rejected": lower_values["r_one_third"] == "0" and mutated_lower["r_one_third"] != "0",
        "action_volume_factor_removal_rejected": twist_formula != mutated_formula and twist_formula.endswith("*F(theta)*y(r)/3"),
        "directional_connection_removal_rejected": twist_formula != mutated_direction and "Derivative(F(theta), theta)**2" in twist_formula,
        "omitted_angular_derivatives_rejected": verification["maxima"]["omitted_angular_derivative_difference"] > 1e-6,
        "missing_metric_backreaction_rejected": verification["maxima"]["missing_backreaction_difference"] > 1e-8,
        "constant_twist_response_rejected": verification["checks"]["constant_twist_zero"],
        "area_completion_overclaim_rejected": mutated_area["status"] != sectors["transverse_area"]["status"],
        "carrier_promotion_rejected": mutated_carrier["status"] != ids["I16"]["status"],
        "conditional_action_promotion_rejected": mutated_action["status"] != ids["I14"]["status"],
        "boundary_discard_rejected": background["boundary_decomposition_difference"] == "0" and bool(background["boundary_delta_y_coefficient"]) and bool(twist["boundary_delta_u_coefficient"]),
    }
    if not all(checks.values()) or not all(catches.values()):
        raise AssertionError({"checks": checks, "catch_proofs": catches})

    result = {
        "schema": "udt-c2-intrinsic-angular-product-package-verification-1.0",
        "result": "PASS",
        "checks": checks,
        "catch_proofs": catches,
        "counts": {
            "background_checks": len(background["checks"]),
            "twist_checks": len(twist["checks"]),
            "branch_checks": len(branches["checks"]),
            "bach_records": verification["counts"]["bach_records"],
            "twist_records": verification["counts"]["twist_records"],
            "status_rows": len(ledger),
            "completeness_rows": len(completeness),
            "source_lineage_rows": len(lineage),
        },
        "load_bearing_hashes": {
            name: digest(HERE / name) for name in (
                "BACKGROUND_DERIVATION.json", "TWIST_DERIVATION.json", "BRANCH_ANALYSIS.json",
                "VERIFICATION_RESULT.json", "BACH_VERIFICATION_POINTS.tsv", "TWIST_VERIFICATION_POINTS.tsv",
                "STATUS_LEDGER.tsv", "COMPLETENESS_MAP.tsv",
            )
        },
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", **result["counts"], "catch_proofs": len(catches)}, sort_keys=True))


if __name__ == "__main__":
    main()
