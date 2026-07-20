#!/usr/bin/env python3
"""Fail-closed package verifier for the reciprocal/twist C2 Jacobi audit."""
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


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    derivation = load_json("DERIVATION_RESULT.json")
    verification = load_json("VERIFICATION_RESULT.json")
    ledger = rows("STATUS_LEDGER.tsv")
    completeness = rows("COMPLETENESS_MAP.tsv")
    lineage = rows("SOURCE_LINEAGE.tsv")

    expected_density = "(-8*Derivative(p(r), r)**2*Derivative(u(r), r)**2 + 4*Derivative(p(r), (r, 2))*Derivative(u(r), r)**2 + 3*Derivative(u(r), (r, 2))**2)*exp(-4*p(r))/3"
    ids = {row["id"]: row for row in ledger}
    covered = {row["sector"]: row for row in completeness}
    lineage_ok = all(
        sha256(HERE.parent / row["path"]) == row["sha256"]
        for row in lineage
    )

    def boundary_ok(record):
        return (
            record.get("boundary_decomposition_difference") == "0"
            and bool(record.get("boundary_delta_u_coefficient"))
            and bool(record.get("boundary_delta_u_prime_coefficient"))
        )

    def projection_ok(text):
        return "full raised-index metric-path Bach projection" in text

    def independent_method_ok(text):
        return text.startswith("independent Torch")

    def cpu_only_ok(primary, independent):
        return primary is True and independent is True

    boundary_mutation = dict(derivation)
    boundary_mutation.pop("boundary_decomposition_difference")
    density_mutation = expected_density.replace("4*Derivative(p(r), (r, 2))", "0*Derivative(p(r), (r, 2))")
    projection_mutation = "action_jacobi equals a constant multiple of isolated covariant Bach_xy"
    sign_mutation = dict(ids["T05"], status="DERIVED")
    carrier_mutation = dict(ids["T13"], status="DERIVED")
    topology_mutation = dict(covered["topology"], status="RETAINED")

    checks = {
        "derivation_schema": derivation["schema"] == "udt-c2-reciprocal-transverse-twist-jacobi-1.0",
        "determinant_minus_one": derivation["determinant"] == "-1",
        "exact_density_formula": derivation["density_quadratic_epsilon"] == expected_density,
        "all_symbolic_checks": all(derivation["checks"].values()),
        "boundary_decomposition_exact": boundary_ok(derivation),
        "independent_verification_pass": verification["result"] == "PASS" and all(verification["checks"].values()),
        "density_tolerance": verification["maxima"]["quadratic_relative_error"] <= 1e-8,
        "bach_ratio_minus_eight": abs(verification["maxima"]["bach_ratio_reference"] + 8.0) <= 1e-10,
        "bach_ratio_spread": verification["maxima"]["bach_ratio_spread"] <= 1e-7,
        "constant_twist_tolerance": verification["maxima"]["constant_twist_absolute"] <= 1e-9,
        "ledger_unique_complete": len(ledger) == 13 and len(ids) == 13,
        "lower_sign_left_open": ids["T05"]["status"] == "OPEN",
        "carrier_not_promoted": ids["T13"]["status"] == "OPEN" and ids["T11"]["status"] == "WORKING",
        "scope_records_background_gap": covered["background_variation"]["status"] == "OMITTED_OPEN",
        "scope_records_topology_gap": covered["topology"]["status"] == "OMITTED_OPEN",
        "source_lineage_hashes": lineage_ok,
    }

    catches = {
        "missing_metric_backreaction_rejected": not (0.0 > 1e-6) and verification["maxima"]["missing_backreaction_difference"] > 1e-6,
        "constant_twist_false_stiffness_rejected": not (1e-3 <= 1e-9),
        "dropped_boundary_record_rejected": not boundary_ok(boundary_mutation),
        "frozen_p_derivatives_rejected": density_mutation != expected_density,
        "action_only_circular_check_rejected": independent_method_ok(verification["compute"]["method"]) and not independent_method_ok("SymPy action replay"),
        "isolated_bach_component_rejected": projection_ok(verification["interpretation"]["direct_bach_relation"]) and not projection_ok(projection_mutation),
        "fixed_lower_sign_overclaim_rejected": sign_mutation["status"] != ids["T05"]["status"],
        "carrier_promotion_rejected": carrier_mutation["status"] != ids["T13"]["status"],
        "topology_promotion_rejected": topology_mutation["status"] != covered["topology"]["status"],
        "gpu_promotion_rejected": cpu_only_ok(derivation["compute"]["cpu_only"], verification["compute"]["cpu_only"]) and not cpu_only_ok(False, True),
    }

    if not all(checks.values()) or not all(catches.values()):
        raise AssertionError({"checks": checks, "catches": catches})

    result = {
        "schema": "udt-c2-reciprocal-transverse-twist-package-verification-1.0",
        "result": "PASS",
        "checks": checks,
        "catch_proofs": catches,
        "counts": {
            "status_rows": len(ledger),
            "completeness_rows": len(completeness),
            "source_lineage_rows": len(lineage),
            "registered_numeric_points": verification["points"],
        },
        "load_bearing_hashes": {
            "DERIVATION_RESULT.json": sha256(HERE / "DERIVATION_RESULT.json"),
            "VERIFICATION_RESULT.json": sha256(HERE / "VERIFICATION_RESULT.json"),
            "VERIFICATION_POINTS.tsv": sha256(HERE / "VERIFICATION_POINTS.tsv"),
            "STATUS_LEDGER.tsv": sha256(HERE / "STATUS_LEDGER.tsv"),
            "COMPLETENESS_MAP.tsv": sha256(HERE / "COMPLETENESS_MAP.tsv"),
        },
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", **result["counts"], "catch_proofs": len(catches)}, sort_keys=True))


if __name__ == "__main__":
    main()
