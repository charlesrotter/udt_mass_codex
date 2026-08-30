#!/usr/bin/env python3
"""Direct evidence-mutation hostile catches for the bounded G305 result."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "CATCH_PROOF_RESULT.json"


def read_tsv(name, key):
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle, delimiter="\t")}


def load_state():
    return {
        "production": json.loads((HERE / "DERIVATION_RESULT.json").read_text()),
        "independent": json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text()),
        "topology": read_tsv("TOPOLOGY_CENSUS.tsv", "sector"),
        "requirements": read_tsv("HOPF_REQUIREMENT_LEDGER.tsv", "requirement"),
        "statuses": read_tsv("STATUS_LEDGER.tsv", "claim"),
    }


def validate(state):
    """Return named contradictions in the computed evidence and premise state."""
    violations = []
    production = state["production"]
    independent = state["independent"]
    topology = state["topology"]
    requirements = state["requirements"]
    statuses = state["statuses"]
    categories = independent.get("checks_by_category", {})

    if independent.get("status") != "PASS":
        violations.append("independent_replay_not_pass")
    if categories.get("positive_overlap", 0) <= 0:
        violations.append("positive_overlap_not_independently_checked")
    if categories.get("negative_global_relation", 0) <= 0:
        violations.append("negative_global_relation_not_independently_checked")
    if abs(independent.get("normalized_hopf_number", 99.0) + 1.0) >= 2.0e-9:
        violations.append("normalized_Hopf_integral_failed")
    if production.get("hopf_number_frozen_orientation") != -1:
        violations.append("production_Hopf_witness_failed")
    if topology["R0_positive"]["compact_without_boundary"] != "yes":
        violations.append("positive_compact_domain_missing")
    if topology["R0_zero"]["compact_without_boundary"] != "no":
        violations.append("zero_domain_compactness_corrupted")
    if topology["R0_negative_causal_cover"]["compact_without_boundary"] != "no":
        violations.append("negative_cover_compactness_corrupted")

    horizon_status = statuses[
        "positive_static_zero_is_observer_horizon_not_material_boundary"
    ]["status"]
    if horizon_status != "DERIVED_CONDITIONAL":
        violations.append("material_edge_contradicts_regular_global_overlap")

    target_status = requirements["fixed_physical_S2_target"]["status_after_G305"]
    frame_status = requirements["local_frame_gauge_descent"]["status_after_G305"]
    celestial_target = (
        target_status == "DERIVED_FROM_CELESTIAL_SCREEN"
        or frame_status == "DERIVED_FROM_CELESTIAL_SCREEN"
    )
    if celestial_target:
        violations.append("celestial_screen_lacks_internal_target_and_gauge_descent")
    elif target_status != "OPEN":
        violations.append("physical_target_has_no_owned_prerequisite")
    if frame_status != "OPEN_FOR_ACTUAL_FIELD" and not celestial_target:
        violations.append("local_frame_gauge_descent_not_owned")

    if requirements["physical_history_selection"]["status_after_G305"] != "OPEN":
        violations.append("history_selection_not_implied_by_map_class_existence")
    if requirements["curvature_magnitude_mass_or_Xmax"]["status_after_G305"] != "OPEN":
        violations.append("scale_blind_integer_cannot_fix_curvature_magnitude")
    if topology["R0_zero"]["ordinary_map_class_to_S2"] != "trivial_on_contractible_domain":
        violations.append("ordinary_R3_requires_extra_basepoint_or_compactification")
    if requirements["covariant_action"]["status_after_G305"] != "OPEN":
        violations.append("no_metric_owned_action_in_requirement_ledger")
    if production.get("scope") != "smooth_center_G304_family_standard_simply_connected_completions_only":
        violations.append("promotion_exceeds_standard_simply_connected_scope")
    if statuses["curvature_magnitude_mass_or_physical_Xmax"]["status"] != "OPEN":
        violations.append("physical_Xmax_ownership_absent")
    if requirements["time_live_dynamics_or_conservation"]["status_after_G305"] != "OPEN":
        violations.append("kinematic_product_slicing_is_not_dynamical_conservation")

    return violations


MUTATION_CASES = {
    "static_zero_is_material_edge": {
        "changes": [("statuses", "positive_static_zero_is_observer_horizon_not_material_boundary", "status", "MATERIAL_EDGE")],
        "expected_failure": "material_edge_contradicts_regular_global_overlap",
    },
    "compact_domain_supplies_physical_target_field": {
        "changes": [("requirements", "fixed_physical_S2_target", "status_after_G305", "DERIVED_FROM_COMPACT_DOMAIN")],
        "expected_failure": "physical_target_has_no_owned_prerequisite",
    },
    "hopf_existence_selects_history": {
        "changes": [("requirements", "physical_history_selection", "status_after_G305", "DERIVED_FROM_HOPF_EXISTENCE")],
        "expected_failure": "history_selection_not_implied_by_map_class_existence",
    },
    "hopf_integer_fixes_curvature_magnitude": {
        "changes": [("requirements", "curvature_magnitude_mass_or_Xmax", "status_after_G305", "DERIVED_FROM_HOPF_INTEGER")],
        "expected_failure": "scale_blind_integer_cannot_fix_curvature_magnitude",
    },
    "ordinary_R3_has_Hopf_integer_without_basepoint": {
        "changes": [("topology", "R0_zero", "ordinary_map_class_to_S2", "Z_WITHOUT_BASEPOINT")],
        "expected_failure": "ordinary_R3_requires_extra_basepoint_or_compactification",
    },
    "old_Hopf_action_is_metric_derived": {
        "changes": [("requirements", "covariant_action", "status_after_G305", "DERIVED_FROM_METRIC")],
        "expected_failure": "no_metric_owned_action_in_requirement_ledger",
    },
    "covers_all_global_quotients_and_topology_change": {
        "changes": [("production", None, "scope", "ALL_QUOTIENTS_AND_TOPOLOGY_CHANGE")],
        "expected_failure": "promotion_exceeds_standard_simply_connected_scope",
    },
    "algebraic_radius_is_physical_Xmax": {
        "changes": [("statuses", "curvature_magnitude_mass_or_physical_Xmax", "status", "DERIVED_PHYSICAL_XMAX")],
        "expected_failure": "physical_Xmax_ownership_absent",
    },
    "kinematic_persistence_is_dynamical_conservation": {
        "changes": [("requirements", "time_live_dynamics_or_conservation", "status_after_G305", "DERIVED_DYNAMICAL_CONSERVATION")],
        "expected_failure": "kinematic_product_slicing_is_not_dynamical_conservation",
    },
    "celestial_screen_is_historical_internal_target": {
        "changes": [
            ("requirements", "fixed_physical_S2_target", "status_after_G305", "DERIVED_FROM_CELESTIAL_SCREEN"),
            ("requirements", "local_frame_gauge_descent", "status_after_G305", "DERIVED_FROM_CELESTIAL_SCREEN"),
        ],
        "expected_failure": "celestial_screen_lacks_internal_target_and_gauge_descent",
    },
}


def apply_changes(state, changes):
    records = []
    for section, row_key, field, after in changes:
        target = state[section] if row_key is None else state[section][row_key]
        before = target[field]
        assert before != after, (section, row_key, field, before, after)
        target[field] = after
        records.append({
            "path": ".".join(part for part in (section, row_key, field) if part is not None),
            "before": before,
            "after": after,
        })
    return records


def main():
    baseline = load_state()
    baseline_violations = validate(baseline)
    assert not baseline_violations, baseline_violations

    catches = {}
    for case_name, specification in MUTATION_CASES.items():
        candidate = copy.deepcopy(baseline)
        mutation_records = apply_changes(candidate, specification["changes"])
        violations = validate(candidate)
        expected_failure = specification["expected_failure"]
        assert expected_failure in violations, (case_name, expected_failure, violations)
        catches[case_name] = {
            "caught": True,
            "expected_failure": expected_failure,
            "violations": violations,
            "mutations": mutation_records,
        }

    corrupted = copy.deepcopy(baseline)
    corruption_records = apply_changes(
        corrupted,
        [("independent", None, "status", "CORRUPTED_CONTROL")],
    )
    corruption_violations = validate(corrupted)
    assert "independent_replay_not_pass" in corruption_violations

    mutation_count = sum(len(row["mutations"]) for row in catches.values())
    assert mutation_count == 11
    result = {
        "status": "PASS",
        "caught": len(catches),
        "total": len(MUTATION_CASES),
        "actual_evidence_mutations": mutation_count,
        "baseline_valid": True,
        "corrupted_baseline_detected": True,
        "corrupted_baseline_mutations": corruption_records,
        "corrupted_baseline_violations": corruption_violations,
        "catches": catches,
        "method": "directly_mutate_computed_evidence_or_required_premise_fields_then_require_preregistered_named_failure",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
