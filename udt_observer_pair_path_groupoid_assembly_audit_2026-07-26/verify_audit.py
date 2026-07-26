#!/usr/bin/env python3
"""Fail-closed verifier for the observer-pair path-groupoid audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def exact_ids(values: list[dict[str, str]], key: str, expected: set[str]) -> None:
    actual = [row[key] for row in values]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise AssertionError(f"identity coverage: {key}")


def validate_sources(corrupt: bool = False) -> None:
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    capability = rows("SOURCE_CAPABILITY_LEDGER.tsv")
    if [row["path"] for row in scope] != [row["path"] for row in manifest]:
        raise AssertionError("source order")
    if {row["path"] for row in capability} != {row["path"] for row in scope} or len(capability) != len(scope):
        raise AssertionError("source capability coverage")
    for index, row in enumerate(manifest):
        expected = "0" * 64 if corrupt and index == 0 else row["sha256"]
        path = ROOT / row["path"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected or path.stat().st_size != int(row["bytes"]):
            raise AssertionError("source identity")


def validate_model(routes, strata, objects, transitions, status, production, independent):
    exact_ids(routes, "route_id", {f"R{i:02d}" for i in range(1, 13)})
    if {row["stratum_id"] for row in strata} != {f"S{i:02d}" for i in range(1, 9)}:
        raise AssertionError("stratum coverage")
    if len(objects) != 11 or len({row["object"] for row in objects}) != 11:
        raise AssertionError("object coverage")
    if len(transitions) != 6 or len({row["prior_object"] for row in transitions}) != 6:
        raise AssertionError("transition coverage")
    if len(status) != 16 or len({row["object"] for row in status}) != 16:
        raise AssertionError("status coverage")

    route = {row["route_id"]: row for row in routes}
    obj = {row["object"]: row for row in objects}
    state = {row["object"]: row for row in status}
    transition = {row["prior_object"]: row for row in transitions}

    if route["R04"]["outcome"] != "EXACT_TYPED_COMPOSITION":
        raise AssertionError("typed composition")
    if state["pair_frame_path_groupoid"]["status"] != "DERIVED_CONDITIONAL_KINEMATICS":
        raise AssertionError("path groupoid promoted")
    if route["R05"]["outcome"] != "VERTICAL_ARROW_REQUIRED_AND_SUFFICIENT" or state["middle_frame_mismatch"]["status"] != "RESOLVED_AS_TYPE_ERROR_WHEN_OMITTED":
        raise AssertionError("vertical arrow")
    if route["R02"]["outcome"] != "AMBIGUITY_DROPS_OUT" or state["screen_SO2_descent"]["status"] != "DERIVED_EXACT":
        raise AssertionError("screen gauge")
    if route["R11"]["outcome"] != "NO_SELECTION" or state["lambda"]["status"] != "OPEN_UNSELECTED":
        raise AssertionError("lambda selected")
    if route["R12"]["outcome"] != "METRIC_NATIVE_SIGNED_DEPTH_COCYCLE" or state["metric_native_signed_depth_cocycle"]["status"] != "OPEN_SMALLEST_KINEMATIC_JOIN":
        raise AssertionError("depth authority")
    if state["Levi_Civita_as_depth_source"]["status"] != "REFUTED_AS_TYPE_MATCH":
        raise AssertionError("transport promoted to depth")
    if route["R07"]["outcome"] != "POTENTIAL_DIFFERENCE" or state["endpoint_only_real_depth"]["status"] != "POTENTIAL_DIFFERENCE_THEOREM":
        raise AssertionError("endpoint potential")
    if route["R09"]["outcome"] != "NONZERO_PERIOD_VISIBLE" or state["nonzero_real_depth_period"]["status"] != "VISIBLE_RECIPROCAL_HOLONOMY":
        raise AssertionError("period erased")
    if route["R10"]["outcome"] != "REQUIRES_SECTION_OR_HOLONOMY_REDUCTION" or state["bare_event_collapse"]["status"] != "OBSTRUCTED_WITHOUT_SECTION_OR_QUOTIENT":
        raise AssertionError("bare event collapse")
    if "vertical_arrow" not in transition["triangle_middle_factor_M_B"]["new_type_resolution"]:
        raise AssertionError("middle transition retyping")
    if "metric_native_signed_depth_assignment" not in transition["smallest_missing_object"]["new_type_resolution"]:
        raise AssertionError("smallest object correction")
    if obj["signed_depth_arrow"]["physical_authority"] != "OPEN_NATIVE_ASSIGNMENT":
        raise AssertionError("inserted depth promoted")
    if obj["bare_event"]["physical_authority"] != "NOT_THE_CORRECT_COMPLETE_OBJECT_BY_ITSELF":
        raise AssertionError("pair data forgotten")
    if state["action_source_carrier_boundary_density_bootstrap_mass_dynamics"]["status"] != "OPEN_UNCHANGED":
        raise AssertionError("physics imported")

    required = {
        "typed_full_comparison_composes_all_lambda",
        "vertical_pair_change_is_sufficient_for_typed_composition",
        "generic_direction_reset_without_vertical_mismatches",
        "finite_character_descends_through_screen_gauge",
        "reciprocal_character_is_Lorentz_only_at_zero_depth",
        "basepoint_reconstructs_endpoint_cocycle",
        "positive_real_character_has_only_zero_identity_period",
        "noncentralizing_two_path_output_differs",
        "symmetric_and_reversal_odd_force_zero",
    }
    if production.get("result") != "PASS" or production.get("check_count") != 51:
        raise AssertionError("production result")
    if not required.issubset(production["checks"]) or set(production["checks"].values()) != {"PASS"}:
        raise AssertionError("production checks")
    counts = independent.get("counts", {})
    if independent.get("result") != "PASS" or independent.get("summary_check_count") != 18:
        raise AssertionError("independent result")
    expected_counts = {
        "lambda_values_tested": 5,
        "screen_gauge_passes": 5,
        "typed_composition_passes": 5,
        "vertical_composition_passes": 5,
        "direction_reset_matches": 1,
        "bare_event_independent_lambda_values": 0,
        "potential_triangles_tested": 125,
        "positive_character_factors_tested": 5,
        "identity_character_factors": 1,
    }
    if counts != expected_counts:
        raise AssertionError("independent counts")


def expect_failure(callback) -> str:
    try:
        callback()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    exact_ids(rows("ROUTE_UNIVERSE.tsv"), "route_id", {f"R{i:02d}" for i in range(1, 13)})
    exact_ids(rows("STRATUM_UNIVERSE.tsv"), "stratum_id", {f"S{i:02d}" for i in range(1, 9)})
    routes = rows("ROUTE_OUTCOMES.tsv")
    strata = rows("STRATUM_OUTCOMES.tsv")
    objects = rows("OBJECT_TYPE_LEDGER.tsv")
    transitions = rows("TRANSITION_REINTERPRETATION.tsv")
    status = rows("STATUS_LEDGER.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    validate_model(routes, strata, objects, transitions, status, production, independent)
    validate_sources()

    def changed(table, key, identity, field, value):
        output = copy.deepcopy(table)
        next(row for row in output if row[key] == identity)[field] = value
        return output

    catches = {}
    bad_production = copy.deepcopy(production)
    del bad_production["checks"]["generic_direction_reset_without_vertical_mismatches"]
    catches["omitted_vertical"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, status, bad_production, independent))
    bad_status = changed(status, "object", "screen_SO2_descent", "status", "OBSTRUCTED")
    catches["screen_gauge"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, bad_status, production, independent))
    bad_status = changed(status, "object", "lambda", "status", "DERIVED_LAMBDA_ONE")
    catches["lambda_selection"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, bad_status, production, independent))
    bad_status = changed(status, "object", "Levi_Civita_as_depth_source", "status", "DERIVED_DEPTH")
    catches["transport_as_depth"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, bad_status, production, independent))
    bad_objects = changed(objects, "object", "signed_depth_arrow", "physical_authority", "DERIVED_FROM_METRIC")
    catches["inserted_depth"] = expect_failure(lambda: validate_model(routes, strata, bad_objects, transitions, status, production, independent))
    bad_routes = changed(routes, "route_id", "R07", "outcome", "GENUINELY_BILOCAL_ADDITIVE_ENDPOINT_COCYCLE")
    catches["endpoint_potential"] = expect_failure(lambda: validate_model(bad_routes, strata, objects, transitions, status, production, independent))
    bad_status = changed(status, "object", "nonzero_real_depth_period", "status", "ERASED")
    catches["period_erasure"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, bad_status, production, independent))
    bad_production = copy.deepcopy(production)
    del bad_production["checks"]["noncentralizing_two_path_output_differs"]
    catches["holonomy_identity"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, status, bad_production, independent))
    bad_status = changed(status, "object", "bare_event_collapse", "status", "AUTOMATIC")
    catches["bare_event"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, bad_status, production, independent))
    bad_status = changed(status, "object", "pair_frame_path_groupoid", "status", "DERIVED_GLOBAL_FLATNESS")
    catches["flatness_promotion"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, bad_status, production, independent))
    bad_production = copy.deepcopy(production)
    del bad_production["checks"]["symmetric_and_reversal_odd_force_zero"]
    catches["symmetric_distance_as_signed"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, status, bad_production, independent))
    bad_status = changed(status, "object", "action_source_carrier_boundary_density_bootstrap_mass_dynamics", "status", "DERIVED")
    catches["physics"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, bad_status, production, independent))
    catches["missing_route"] = expect_failure(lambda: validate_model(routes[:-1], strata, objects, transitions, status, production, independent))
    catches["source_identity"] = expect_failure(lambda: validate_sources(True))
    bad_independent = copy.deepcopy(independent)
    bad_independent["counts"]["typed_composition_passes"] = 4
    catches["independent"] = expect_failure(lambda: validate_model(routes, strata, objects, transitions, status, production, bad_independent))

    if len(catches) != 15 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch count")
    output = {
        "schema": "udt-observer-pair-path-groupoid-verification-1.0",
        "result": "PASS",
        "grade": "VERIFIED_WITH_CAVEATS_BOUNDED_PAIR_FRAME_PATH_GROUPOID_CLASSIFICATION",
        "routes": len(routes),
        "stratum_rows": len(strata),
        "object_types": len(objects),
        "transition_reinterpretations": len(transitions),
        "status_rows": len(status),
        "production_checks": production["check_count"],
        "independent_summary_checks": independent["summary_check_count"],
        "independent_counts": independent["counts"],
        "source_identities": len(rows("SOURCE_MANIFEST.tsv")),
        "catch_count": len(catches),
        "catch_proofs": catches,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
