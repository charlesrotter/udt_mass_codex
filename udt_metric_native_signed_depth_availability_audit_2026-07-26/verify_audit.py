#!/usr/bin/env python3
"""Fail-closed verifier for the signed-depth availability audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_IDS = {f"D{i:02d}" for i in range(1, 9)}


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def exact_ids(values: list[dict[str, str]], key: str, expected: set[str]) -> None:
    actual = [row[key] for row in values]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise AssertionError(f"identity coverage:{key}")


def validate_sources(corrupt: bool = False) -> None:
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    capability = rows("SOURCE_CAPABILITY_LEDGER.tsv")
    if [row["path"] for row in scope] != [row["path"] for row in manifest]:
        raise AssertionError("source order")
    if len(capability) != len(scope) or {row["path"] for row in capability} != {row["path"] for row in scope}:
        raise AssertionError("source capability coverage")
    for index, row in enumerate(manifest):
        expected = "0" * 64 if corrupt and index == 0 else row["sha256"]
        path = ROOT / row["path"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected or path.stat().st_size != int(row["size"]):
            raise AssertionError("source identity")


def validate_model(candidates, properties, outcomes, references, status, production, independent) -> None:
    exact_ids(candidates, "id", EXPECTED_IDS)
    exact_ids(properties, "id", EXPECTED_IDS)
    exact_ids(outcomes, "id", EXPECTED_IDS)
    if len(references) != 12 or len({row["object"] for row in references}) != 12:
        raise AssertionError("reference ledger coverage")
    if len(status) != 18 or len({row["object"] for row in status}) != 18:
        raise AssertionError("status coverage")

    prop = {row["id"]: row for row in properties}
    outcome = {row["id"]: row for row in outcomes}
    state = {row["object"]: row for row in status}
    ref = {row["object"]: row for row in references}

    expected_outcomes = {
        "D01": "AVAILABLE_CONDITIONAL_SECTION",
        "D02": "AVAILABLE_CONDITIONAL_ONE_FORM",
        "D03": "DERIVED_READOUT_GIVEN_RECIPROCAL_MAP__NONADDITIVE_OUTSIDE_SUBGROUP",
        "D04": "AVAILABLE_CONDITIONAL_PROFILE_AND_TRANSITIONS__NONADDITIVE_BILOCAL",
        "D05": "METRIC_NATIVE_MAGNITUDE_NOT_SIGNED_COCYCLE",
        "D06": "DERIVED_READOUT_GIVEN_SIGNAL_DATA_NOT_FOUNDED_IDENTITY",
        "D07": "EXACT_COCYCLE_GIVEN_SELECTED_INVARIANT__NONUNIQUE_UNSELECTED",
        "D08": "ZERO_BY_METRIC_COMPATIBILITY",
    }
    if {key: outcome[key]["outcome"] for key in EXPECTED_IDS} != expected_outcomes:
        raise AssertionError("candidate outcome")
    if prop["D05"]["signed_reversal_odd"] != "FAIL_SYMMETRIC_MAGNITUDE" or prop["D05"]["additive_on_typed_arrows"] != "FAIL_FOR_GENERIC_TRIANGLES":
        raise AssertionError("bilocal promotion")
    if prop["D08"]["nontrivial"] != "FAIL_NONTRIVIAL" or prop["D08"]["metric_native"] != "PASS_LEVI_CIVITA_FROM_METRIC":
        raise AssertionError("Levi-Civita promotion")
    if prop["D06"]["founding_aligned"] != "OPEN_SOLDER_TO_FOUNDED_DEPTH":
        raise AssertionError("clock ratio promotion")
    if prop["D07"]["founding_aligned"] != "FAIL_NO_FOUNDED_IDENTIFICATION":
        raise AssertionError("invariant potential promotion")
    if ref["raw_coframe_projection"]["status"] != "REFERENCE_DEPENDENT":
        raise AssertionError("raw reference")
    if ref["Levi_Civita_reciprocal_projection"]["status"] != "ZERO_EXACT":
        raise AssertionError("LC reference")
    if ref["general_complete_relative_map"]["status"] != "NOT_SCALAR_HOMOMORPHISM":
        raise AssertionError("general log")
    if state["founded_phi_identity"]["status"] != "DERIVED_UNCHANGED":
        raise AssertionError("phi demoted")
    if state["candidate_routes_passing_all_six_requirements"]["status"] != "ZERO_IN_FROZEN_UNIVERSE":
        raise AssertionError("all-six count")
    if state["smallest_remaining_kinematic_join"]["status"] != "OPEN_METRIC_NATIVE_NORMALIZED_RECIPROCAL_COCYCLE_OR_EQUIVALENT_REFERENCE_CONNECTION":
        raise AssertionError("smallest join")
    if state["lambda_complete_branch_path_Xmax_action_matter_density_bootstrap_source_boundary_mass_dynamics"]["status"] != "OPEN_UNCHANGED":
        raise AssertionError("physics imported")

    required_production = {
        "section_Maurer_Cartan_equals_X_dphi",
        "endpoint_basepoint_reconstruction",
        "self_adjoint_skew_trace_pairing_zero",
        "nonconstant_reference_change_shifts_raw_depth",
        "reciprocal_subgroup_depth_adds",
        "general_log_projection_nonadditive",
        "symmetric_and_reversal_odd_force_zero",
        "observer_chart_generic_overlap_not_scalar_cocycle",
        "real_reciprocal_character_identity_only_zero_period",
        "invariant_potentials_are_nonunique",
        "clock_log_ratio_adds",
        "clock_ratio_not_algebraically_identical_to_free_founded_depth",
    }
    if production.get("result") != "PASS" or production.get("summary_check_count") != 35 or production.get("census_check_count") != 86 or production.get("total_check_count") != 121:
        raise AssertionError("production result")
    if not required_production.issubset(production["checks"]) or set(production["checks"].values()) != {"PASS"}:
        raise AssertionError("production checks")
    expected_production_counts = {
        "candidate_types": 8,
        "endpoint_reversal_checks": 16,
        "endpoint_triangle_checks": 64,
        "invariant_potential_checks": 6,
        "routes_passing_all_six_requirements": 0,
        "Levi_Civita_nonzero_reciprocal_components": 0,
        "conditional_exact_signed_additive_constructions": 5,
    }
    if production.get("counts") != expected_production_counts:
        raise AssertionError("production counts")

    expected_independent_counts = {
        "endpoint_triangles": 125,
        "endpoint_reversals": 125,
        "metric_skew_samples": 135,
        "reference_change_samples": 25,
        "reciprocal_subgroup_compositions": 25,
        "clock_ratio_compositions": 27,
        "invariant_cocycles": 375,
        "identity_character_factors": 1,
    }
    if independent.get("result") != "PASS" or independent.get("summary_check_count") != 9 or independent.get("census_check_count") != 973:
        raise AssertionError("independent result")
    if independent.get("counts") != expected_independent_counts or set(independent["checks"].values()) != {"PASS"}:
        raise AssertionError("independent counts")


def changed(table, key, identity, field, value):
    output = copy.deepcopy(table)
    next(row for row in output if row[key] == identity)[field] = value
    return output


def expect_failure(callback) -> str:
    try:
        callback()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    candidates = rows("CANDIDATE_UNIVERSE.tsv")
    properties = rows("PROPERTY_MATRIX.tsv")
    outcomes = rows("CANDIDATE_OUTCOMES.tsv")
    references = rows("REFERENCE_AND_CONNECTION_LEDGER.tsv")
    status = rows("STATUS_LEDGER.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    validate_model(candidates, properties, outcomes, references, status, production, independent)
    validate_sources()

    def model(c=candidates, p=properties, o=outcomes, r=references, s=status, d=production, i=independent):
        return lambda: validate_model(c, p, o, r, s, d, i)

    catches = {}
    catches["missing_candidate"] = expect_failure(model(c=candidates[:-1]))
    catches["duplicate_candidate"] = expect_failure(model(c=candidates + [copy.deepcopy(candidates[0])]))
    catches["false_Levi_Civita_depth"] = expect_failure(model(p=changed(properties, "id", "D08", "nontrivial", "PASS_NONZERO")))
    catches["false_bilocal_cocycle"] = expect_failure(model(p=changed(properties, "id", "D05", "signed_reversal_odd", "PASS")))
    bad_production = copy.deepcopy(production)
    del bad_production["checks"]["nonconstant_reference_change_shifts_raw_depth"]
    catches["reference_invariance_deleted"] = expect_failure(model(d=bad_production))
    bad_production = copy.deepcopy(production)
    del bad_production["checks"]["general_log_projection_nonadditive"]
    catches["general_log_additivity"] = expect_failure(model(d=bad_production))
    catches["clock_ratio_founding_promotion"] = expect_failure(model(p=changed(properties, "id", "D06", "founding_aligned", "PASS")))
    catches["invariant_formula_promotion"] = expect_failure(model(p=changed(properties, "id", "D07", "founding_aligned", "PASS")))
    catches["section_selection_promotion"] = expect_failure(model(o=changed(outcomes, "id", "D01", "outcome", "DERIVED_METRIC_NATIVE_SIGNED_DEPTH")))
    catches["one_form_selection_promotion"] = expect_failure(model(o=changed(outcomes, "id", "D02", "outcome", "DERIVED_METRIC_NATIVE_SIGNED_DEPTH")))
    catches["phi_demotion"] = expect_failure(model(s=changed(status, "object", "founded_phi_identity", "status", "OPEN_PLACEHOLDER")))
    catches["physics_promotion"] = expect_failure(model(s=changed(status, "object", "lambda_complete_branch_path_Xmax_action_matter_density_bootstrap_source_boundary_mass_dynamics", "status", "DERIVED")))
    bad_production = copy.deepcopy(production)
    bad_production["counts"]["routes_passing_all_six_requirements"] = 1
    catches["all_six_count"] = expect_failure(model(d=bad_production))
    bad_independent = copy.deepcopy(independent)
    bad_independent["counts"]["metric_skew_samples"] = 134
    catches["independent_replay"] = expect_failure(model(i=bad_independent))
    catches["source_identity"] = expect_failure(lambda: validate_sources(True))

    if len(catches) != 15 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch count")
    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch", "result"])
        writer.writerows(sorted(catches.items()))
    output = {
        "schema": "udt-metric-native-signed-depth-verification-1.0",
        "result": "PASS",
        "grade": "VERIFIED_WITH_CAVEATS_BOUNDED_AVAILABILITY_CLASSIFICATION",
        "candidate_types": len(candidates),
        "property_rows": len(properties),
        "outcome_rows": len(outcomes),
        "reference_rows": len(references),
        "status_rows": len(status),
        "source_identities": len(rows("SOURCE_MANIFEST.tsv")),
        "production_checks": production["total_check_count"],
        "independent_checks": independent["summary_check_count"] + independent["census_check_count"],
        "routes_passing_all_six_requirements": 0,
        "catch_count": len(catches),
        "catch_proofs": catches,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
