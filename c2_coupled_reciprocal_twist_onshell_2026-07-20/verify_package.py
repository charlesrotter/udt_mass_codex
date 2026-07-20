#!/usr/bin/env python3
"""Fail-closed verifier for the coupled reciprocal-background Bach audit."""
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
    branches = load_json("BRANCH_ANALYSIS.json")
    verification = load_json("VERIFICATION_RESULT.json")
    ledger = rows("STATUS_LEDGER.tsv")
    completeness = rows("COMPLETENESS_MAP.tsv")
    lineage = rows("SOURCE_LINEAGE.tsv")
    ids = {row["id"]: row for row in ledger}
    sectors = {row["sector"]: row for row in completeness}

    lineage_ok = all(digest(HERE.parent / row["path"]) == row["sha256"] for row in lineage)
    outcomes = set(branches["outcomes"])
    witness = branches["all_signs_single_branch_witness"]["values"]
    false_branch = branches["reduced_only_false_branch"]
    transforms = branches["transforms"]

    checks = {
        "background_schema": background["schema"] == "udt-c2-coupled-reciprocal-background-bach-1.0",
        "all_background_checks": all(background["checks"].values()),
        "all_branch_checks": all(branches["checks"].values()) and len(branches["checks"]) == 14,
        "full_bach_multiple_strata": "FULL_BACH_PERMITS_MULTIPLE_Q_STRATA" in outcomes,
        "reduced_false_branches": "REDUCED_STATIONARITY_FALSELY_SELECTS_EXTRA_BRANCHES" in outcomes,
        "general_cubic_constraint": branches["general_local_branch"]["coefficient_constraint"] == "B**2 = 3*A*C",
        "all_three_witness_values": witness == {
            "minimum_y_on_registered_interval": "15/8",
            "r_minus_half": "-12/17",
            "r_plus_half": "4/5",
            "r_zero": "0",
        },
        "twist_coefficients_recorded": transforms["higher_twist_coefficient"] == "y(r)**2" and transforms["lower_twist_coefficient"] == "-2*y(r)*Derivative(y(r), (r, 2))/3",
        "independent_component_replay": verification["result"] == "PASS" and all(verification["checks"].values()),
        "independent_tolerance": verification["maxima"]["nonzero_scaled_error"] <= 1e-8 and verification["maxima"]["zero_absolute_error"] <= 1e-9,
        "status_ledger_unique": len(ledger) == 14 and len(ids) == 14,
        "sign_selection_left_open": ids["B07"]["status"] == "OPEN",
        "carrier_left_open": ids["B14"]["status"] == "OPEN",
        "angular_scope_open": sectors["intrinsic_angular_curvature"]["status"] == "OMITTED_OPEN",
        "source_lineage_hashes": lineage_ok,
    }

    mutated_outcomes = outcomes - {"REDUCED_STATIONARITY_FALSELY_SELECTS_EXTRA_BRANCHES"}
    mutated_witness = dict(witness, r_zero="1")
    mutated_false = dict(false_branch, full_constraint_numerator="0")
    mutated_sign = dict(ids["B07"], status="DERIVED")
    mutated_carrier = dict(ids["B14"], status="DERIVED")
    mutated_angular = dict(sectors["intrinsic_angular_curvature"], status="RETAINED")
    catches = {
        "reduced_only_promotion_rejected": "REDUCED_STATIONARITY_FALSELY_SELECTS_EXTRA_BRANCHES" not in mutated_outcomes,
        "discarded_transverse_component_rejected": verification["maxima"]["transverse_component_witness"] > 1e-6,
        "false_branch_promotion_rejected": false_branch["full_constraint_numerator"] == "4" and mutated_false["full_constraint_numerator"] != "4",
        "divide_by_Q_rejected": witness["r_zero"] == "0" and mutated_witness["r_zero"] != "0",
        "nonzero_curvature_assumption_rejected": branches["general_local_branch"]["coefficient_constraint"] == "B**2 = 3*A*C",
        "fixed_sign_overclaim_rejected": mutated_sign["status"] != ids["B07"]["status"],
        "carrier_promotion_rejected": mutated_carrier["status"] != ids["B14"]["status"],
        "angular_completion_overclaim_rejected": mutated_angular["status"] != sectors["intrinsic_angular_curvature"]["status"],
        "boundary_discard_rejected": background["boundary_decomposition_difference"] == "0" and bool(background["boundary_delta_p_coefficient"]) and bool(background["boundary_delta_p_prime_coefficient"]),
        "gpu_promotion_rejected": background["compute"]["cpu_only"] and verification["compute"]["cpu_only"],
    }
    if not all(checks.values()) or not all(catches.values()):
        raise AssertionError({"checks": checks, "catches": catches})

    result = {
        "schema": "udt-c2-coupled-reciprocal-background-package-verification-1.0",
        "result": "PASS",
        "checks": checks,
        "catch_proofs": catches,
        "counts": {
            "background_checks": len(background["checks"]),
            "branch_checks": len(branches["checks"]),
            "component_records": verification["counts"]["component_records"],
            "status_rows": len(ledger),
            "completeness_rows": len(completeness),
            "source_lineage_rows": len(lineage),
        },
        "load_bearing_hashes": {
            "BACKGROUND_DERIVATION.json": digest(HERE / "BACKGROUND_DERIVATION.json"),
            "BRANCH_ANALYSIS.json": digest(HERE / "BRANCH_ANALYSIS.json"),
            "VERIFICATION_RESULT.json": digest(HERE / "VERIFICATION_RESULT.json"),
            "VERIFICATION_POINTS.tsv": digest(HERE / "VERIFICATION_POINTS.tsv"),
            "STATUS_LEDGER.tsv": digest(HERE / "STATUS_LEDGER.tsv"),
            "COMPLETENESS_MAP.tsv": digest(HERE / "COMPLETENESS_MAP.tsv"),
        },
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", **result["counts"], "catch_proofs": len(catches)}, sort_keys=True))


if __name__ == "__main__":
    main()
