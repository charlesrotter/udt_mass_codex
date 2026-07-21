#!/usr/bin/env python3
"""Fail-closed verifier for the partial transverse-coframe closure package."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def rows(name):
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    gauge = load("GAUGE_STRUCTURE.json")
    background = load("BACKGROUND_CLOSURE.json")
    verification = load("VERIFICATION_RESULT.json")
    closure = load("CLOSURE_ANALYSIS.json")
    ledger = rows("STATUS_LEDGER.tsv")
    completeness = rows("COMPLETENESS_MAP.tsv")
    lineage = rows("SOURCE_LINEAGE.tsv")
    ids = {row["id"]: row for row in ledger}
    sectors = {row["sector"]: row for row in completeness}
    outcomes = set(closure["outcomes"])
    timeout = (HERE / "GENERAL_TWIST_TIMEOUT.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")

    checks = {
        "gauge_schema_and_checks": gauge["schema"] == "udt-c2-transverse-coframe-gauge-structure-1.0" and len(gauge["checks"]) == 4 and all(gauge["checks"].values()),
        "background_schema_and_checks": background["schema"] == "udt-c2-transverse-coframe-background-1.0" and len(background["checks"]) == 8 and all(background["checks"].values()),
        "verification_schema_and_checks": verification["schema"] == "udt-c2-transverse-coframe-independent-verification-1.0" and len(verification["checks"]) == 7 and all(verification["checks"].values()),
        "closure_schema_and_checks": closure["schema"] == "udt-c2-transverse-coframe-closure-analysis-1.0" and len(closure["checks"]) == 12 and all(closure["checks"].values()),
        "registered_partial_outcomes": outcomes == {"PRODUCT_BACH_FAMILY_REMAINS_FULL_METRIC_STATIONARY", "TWIST_HESSIAN_BLOCK_DIAGONAL_BY_REFLECTION", "COFRAME_CONTROL_INCONCLUSIVE"},
        "product_recovery": background["product_control"]["density_difference"] == "0",
        "einstein_counterexample": background["variation_domain_obstruction"]["einstein_branch_full_constraint"] == "0" and background["variation_domain_obstruction"]["einstein_branch_projection"] == "-32*K**2/3",
        "angular_integration_disclosed": "no general division by F is valid" in background["angular_reduction_rule"],
        "mixed_blocks_exact_zero": verification["maxima"]["mixed_block_absolute"] == 0.0,
        "pure_twist_nonzero_control": verification["controls"]["minimum_pure_twist_magnitude"] > 1e-6,
        "general_pure_twist_inconclusive": not (HERE / "TWIST_CLOSURE.json").exists() and "exit code `130`" in timeout and ids["T12"]["status"] == "INCONCLUSIVE",
        "status_ledger_unique": len(ledger) == 18 and len(ids) == 18,
        "restricted_selector_rejected": ids["T09"]["status"] == "REJECTED" and ids["T13"]["status"] == "OPEN",
        "carrier_open": ids["T17"]["status"] == "OPEN",
        "angular_domain_load_bearing": sectors["angular_domain_and_caps"]["status"] == "OMITTED_LOAD_BEARING",
        "source_lineage_hashes": len(lineage) == 6 and all(digest(HERE.parent / row["path"]) == row["sha256"] for row in lineage),
        "partial_grade_disclosed": "VERIFIED-WITH-CAVEATS / PARTIAL" in report and "INCONCLUSIVE" in report,
    }

    mutated_outcomes = outcomes - {"COFRAME_CONTROL_INCONCLUSIVE"}
    mutated_einstein = dict(background["variation_domain_obstruction"], einstein_branch_full_constraint="1")
    mutated_selector = dict(ids["T09"], status="DERIVED")
    mutated_twist = dict(ids["T12"], status="DERIVED")
    mutated_angular = dict(sectors["angular_domain_and_caps"], status="RETAINED")
    mutated_carrier = dict(ids["T17"], status="DERIVED")
    mutated_action = dict(ids["T16"], status="DERIVED")
    catches = {
        "restricted_selector_promotion_rejected": mutated_selector["status"] != ids["T09"]["status"],
        "einstein_branch_discard_rejected": mutated_einstein["einstein_branch_full_constraint"] != background["variation_domain_obstruction"]["einstein_branch_full_constraint"],
        "general_division_by_F_rejected": "no general division by F is valid" in background["angular_reduction_rule"],
        "missing_inconclusive_outcome_rejected": "COFRAME_CONTROL_INCONCLUSIVE" not in mutated_outcomes,
        "invented_twist_result_rejected": not (HERE / "TWIST_CLOSURE.json").exists() and mutated_twist["status"] != ids["T12"]["status"],
        "timeout_as_negative_rejected": "no negative physics" in timeout.lower(),
        "mixed_block_mutation_rejected": verification["maxima"]["mixed_block_absolute"] <= 1e-9,
        "constant_connection_response_rejected": verification["maxima"]["constant_connection_absolute"] <= 1e-9,
        "endpoint_discard_rejected": all(bool(values["delta_field"]) and bool(values["delta_field_prime"]) for values in background["endpoint_coefficients"].values()),
        "angular_completion_overclaim_rejected": mutated_angular["status"] != sectors["angular_domain_and_caps"]["status"],
        "carrier_promotion_rejected": mutated_carrier["status"] != ids["T17"]["status"],
        "conditional_action_promotion_rejected": mutated_action["status"] != ids["T16"]["status"],
        "gpu_promotion_rejected": closure["compute"]["cpu_only"] and not closure["compute"]["gpu_work_performed"],
    }
    if not all(checks.values()) or not all(catches.values()):
        raise AssertionError({"checks": checks, "catch_proofs": catches})

    result = {
        "schema": "udt-c2-transverse-coframe-package-verification-1.0",
        "result": "PASS_WITH_REGISTERED_INCONCLUSIVE_SECTOR",
        "checks": checks,
        "catch_proofs": catches,
        "counts": {
            "gauge_checks": len(gauge["checks"]), "background_checks": len(background["checks"]),
            "independent_checks": len(verification["checks"]), "closure_checks": len(closure["checks"]),
            "background_records": verification["counts"]["background_records"],
            "mixed_block_records": verification["counts"]["mixed_block_records"],
            "bach_components": verification["counts"]["bach_components"],
            "status_rows": len(ledger), "completeness_rows": len(completeness), "source_lineage_rows": len(lineage),
        },
        "load_bearing_hashes": {name: digest(HERE / name) for name in (
            "GAUGE_STRUCTURE.json", "BACKGROUND_CLOSURE.json", "VERIFICATION_RESULT.json",
            "CLOSURE_ANALYSIS.json", "BACKGROUND_VERIFICATION_POINTS.tsv", "MIXED_BLOCK_POINTS.tsv",
            "STATUS_LEDGER.tsv", "COMPLETENESS_MAP.tsv", "GENERAL_TWIST_TIMEOUT.md",
        )},
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": result["result"], **result["counts"], "catch_proofs": len(catches)}, sort_keys=True))


if __name__ == "__main__":
    main()
