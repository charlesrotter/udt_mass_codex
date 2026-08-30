#!/usr/bin/env python3
"""Evidence-driven hostile-promotion catches for the bounded G305 result."""

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
        "promotions": set(),
    }


def validate(state):
    """Return named contradictions between proposed promotions and computed evidence."""
    violations = []
    production = state["production"]
    independent = state["independent"]
    topology = state["topology"]
    requirements = state["requirements"]
    statuses = state["statuses"]
    promotions = state["promotions"]
    categories = independent.get("checks_by_category", {})

    # Baseline integrity is derived from saved computations, not claim labels.
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

    if "static_zero_is_material_edge" in promotions:
        if (
            categories.get("positive_overlap", 0) > 0
            and statuses["positive_static_zero_is_observer_horizon_not_material_boundary"]["status"]
            == "DERIVED_CONDITIONAL"
        ):
            violations.append("material_edge_contradicts_regular_global_overlap")

    if "compact_domain_supplies_physical_target_field" in promotions:
        if requirements["fixed_physical_S2_target"]["status_after_G305"] == "OPEN":
            violations.append("physical_target_has_no_owned_prerequisite")

    if "hopf_existence_selects_history" in promotions:
        if requirements["physical_history_selection"]["status_after_G305"] == "OPEN":
            violations.append("history_selection_not_implied_by_map_class_existence")

    if "hopf_integer_fixes_curvature_magnitude" in promotions:
        if (
            requirements["curvature_magnitude_mass_or_Xmax"]["status_after_G305"] == "OPEN"
            and production.get("hopf_number_frozen_orientation") == -1
            and independent.get("checks_by_category", {}).get("hopf_and_scale_time", 0) > 0
        ):
            violations.append("scale_blind_integer_cannot_fix_curvature_magnitude")

    if "ordinary_R3_has_Hopf_integer_without_basepoint" in promotions:
        if (
            topology["R0_zero"]["ordinary_map_class_to_S2"] == "trivial_on_contractible_domain"
            and topology["R0_zero"]["extra_condition_for_Hopf_class"]
            == "asymptotic_basepoint_or_other_compactification"
        ):
            violations.append("ordinary_R3_requires_extra_basepoint_or_compactification")

    if "old_Hopf_action_is_metric_derived" in promotions:
        if requirements["covariant_action"]["status_after_G305"] == "OPEN":
            violations.append("no_metric_owned_action_in_requirement_ledger")

    if "covers_all_global_quotients_and_topology_change" in promotions:
        if production.get("scope") == "smooth_center_G304_family_standard_simply_connected_completions_only":
            violations.append("promotion_exceeds_standard_simply_connected_scope")

    if "algebraic_radius_is_physical_Xmax" in promotions:
        if statuses["curvature_magnitude_mass_or_physical_Xmax"]["status"] == "OPEN":
            violations.append("physical_Xmax_ownership_absent")

    if "kinematic_persistence_is_dynamical_conservation" in promotions:
        if requirements["time_live_dynamics_or_conservation"]["status_after_G305"] == "OPEN":
            violations.append("kinematic_product_slicing_is_not_dynamical_conservation")

    if "celestial_screen_is_historical_internal_target" in promotions:
        if (
            requirements["fixed_physical_S2_target"]["status_after_G305"] == "OPEN"
            and requirements["local_frame_gauge_descent"]["status_after_G305"] == "OPEN_FOR_ACTUAL_FIELD"
        ):
            violations.append("celestial_screen_lacks_internal_target_and_gauge_descent")

    return violations


def main():
    baseline = load_state()
    baseline_violations = validate(baseline)
    assert not baseline_violations, baseline_violations

    hostile_promotions = (
        "static_zero_is_material_edge",
        "compact_domain_supplies_physical_target_field",
        "hopf_existence_selects_history",
        "hopf_integer_fixes_curvature_magnitude",
        "ordinary_R3_has_Hopf_integer_without_basepoint",
        "old_Hopf_action_is_metric_derived",
        "covers_all_global_quotients_and_topology_change",
        "algebraic_radius_is_physical_Xmax",
        "kinematic_persistence_is_dynamical_conservation",
        "celestial_screen_is_historical_internal_target",
    )
    catches = {}
    for promotion in hostile_promotions:
        candidate = copy.deepcopy(baseline)
        candidate["promotions"].add(promotion)
        violations = validate(candidate)
        assert violations, promotion
        catches[promotion] = {
            "caught": True,
            "violations": violations,
        }

    corrupted = copy.deepcopy(baseline)
    corrupted["independent"]["status"] = "CORRUPTED_CONTROL"
    corruption_violations = validate(corrupted)
    assert "independent_replay_not_pass" in corruption_violations

    result = {
        "status": "PASS",
        "caught": len(catches),
        "total": len(hostile_promotions),
        "baseline_valid": True,
        "corrupted_baseline_detected": True,
        "corrupted_baseline_violations": corruption_violations,
        "catches": catches,
        "method": "mutate_computed_evidence_state_then_require_named_invariant_provenance_topology_or_ownership_failure",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
