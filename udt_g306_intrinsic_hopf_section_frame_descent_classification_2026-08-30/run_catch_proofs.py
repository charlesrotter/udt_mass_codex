#!/usr/bin/env python3
"""Direct hostile mutations for the preregistered G306 overclaims."""

from __future__ import annotations

import copy
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = HERE / "DERIVATION_RESULT.json"
OUT = HERE / "CATCH_PROOF_RESULT.json"


def validate(d):
    assert d["candidate_landing"] == "A", "landing_class"
    assert d["isotropy_fixed_tangent_dimension"] == 0, "isotropy_fixed_vector"
    assert d["metric_natural_unit_section_exists"] is False, "false_unique_section"
    assert d["constant_curvature_ricci_eigenvalue_multiplicity"] == 3, "false_curvature_axis"
    assert d["radial_map_singular_orbits"] == 2, "false_global_radial_map"
    assert d["component_charge_constant_map"] == 0, "constant_component_charge"
    assert d["component_charge_after_large_frame_rotation"] in (-1, 1), "large_gauge_Hopf_witness"
    assert d["component_charge_after_large_frame_rotation"] != d["component_charge_constant_map"], "component_charge_changed"
    assert d["raw_component_charge_full_frame_invariant"] is False, "false_component_gauge_invariance"
    assert d["oriented_chiral_family_count"] == 2, "chirality_census"
    assert d["individual_member_selected"] is False, "false_member_population"
    assert sorted(d["normalized_helicity_by_chirality"]) == [-1, 1], "helicity_chiralities"
    assert d["normalized_helicity_scale_blind"] is True, "false_scale_attachment"
    assert d["field_or_query_population_selected"] is False, "false_field_population"
    assert d["fixed_cross_history_target_selected"] is False, "false_fixed_target"
    assert d["metric_and_kernel_changed"] is False, "kernel_regression"
    assert "nonspherical_deformations" in d["omitted"], "scope_overexport"
    assert "action" in d["omitted"], "action_import"
    assert "history_selection" in d["omitted"], "history_promotion"
    assert "physical_Xmax" in d["omitted"], "Xmax_promotion"


def mutate(path, value):
    def apply(d):
        if isinstance(path, tuple):
            parent = d
            for key in path[:-1]:
                parent = parent[key]
            before = copy.deepcopy(parent[path[-1]])
            parent[path[-1]] = copy.deepcopy(value)
        else:
            before = copy.deepcopy(d[path])
            d[path] = copy.deepcopy(value)
        return before
    return apply


def remove_omission(name):
    def apply(d):
        before = copy.deepcopy(d["omitted"])
        d["omitted"] = [x for x in d["omitted"] if x != name]
        return before
    return apply


def main():
    baseline = json.loads(BASE.read_text(encoding="utf-8"))
    validate(baseline)
    cases = [
        ("unique_isotropy_fixed_direction", mutate("isotropy_fixed_tangent_dimension", 1), "isotropy_fixed_vector"),
        ("metric_selects_unit_section", mutate("metric_natural_unit_section_exists", True), "false_unique_section"),
        ("curvature_selects_axis", mutate("constant_curvature_ricci_eigenvalue_multiplicity", 1), "false_curvature_axis"),
        ("radial_map_global", mutate("radial_map_singular_orbits", 0), "false_global_radial_map"),
        ("large_gauge_preserves_component_charge", mutate("component_charge_after_large_frame_rotation", 0), "large_gauge_Hopf_witness"),
        ("raw_component_charge_gauge_invariant", mutate("raw_component_charge_full_frame_invariant", True), "false_component_gauge_invariance"),
        ("one_chirality_family", mutate("oriented_chiral_family_count", 1), "chirality_census"),
        ("orientation_selects_member", mutate("individual_member_selected", True), "false_member_population"),
        ("helicity_loses_opposite_chirality", mutate("normalized_helicity_by_chirality", [-1, -1]), "helicity_chiralities"),
        ("helicity_sets_scale", mutate("normalized_helicity_scale_blind", False), "false_scale_attachment"),
        ("family_populates_field", mutate("field_or_query_population_selected", True), "false_field_population"),
        ("metric_selects_fixed_target", mutate("fixed_cross_history_target_selected", True), "false_fixed_target"),
        ("kernel_changed", mutate("metric_and_kernel_changed", True), "kernel_regression"),
        ("export_to_nonspherical", remove_omission("nonspherical_deformations"), "scope_overexport"),
        ("import_old_action", remove_omission("action"), "action_import"),
        ("promote_history", remove_omission("history_selection"), "history_promotion"),
        ("promote_Xmax", remove_omission("physical_Xmax"), "Xmax_promotion"),
    ]
    records = []
    for name, change, expected in cases:
        mutant = copy.deepcopy(baseline)
        before = change(mutant)
        caught = False
        failure = ""
        try:
            validate(mutant)
        except AssertionError as exc:
            caught = True
            failure = str(exc)
        assert caught, name
        assert failure == expected, (name, failure, expected)
        records.append({
            "case": name,
            "caught": caught,
            "expected_failure": expected,
            "actual_failure": failure,
            "before": before,
        })
    result = {
        "status": "PASS",
        "baseline_valid": True,
        "hostile_cases": len(records),
        "direct_computed_or_required_premise_mutations": len(records),
        "records": records,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

