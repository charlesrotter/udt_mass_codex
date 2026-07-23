#!/usr/bin/env python3
"""Deterministic complete-metric realization layer map."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAXIMUM = (
    "REGISTERED_COMPLETE_METRIC_REALIZATION_LAYERS_MAPPED__ANY_EXISTING_"
    "NATIVE_JOIN_IDENTIFIED_WITH_EXACT_SCOPE__MISSING_JOINS_REMAIN_OPEN"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def verify_sources() -> int:
    rows = []
    for line in (HERE / "SOURCE_MANIFEST.sha256").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        path = ROOT / relative
        if not path.is_file() or digest(path) != expected:
            raise AssertionError(f"source mismatch: {relative}")
        rows.append(relative)
    if len(rows) != 47 or len(set(rows)) != 47:
        raise AssertionError("source identity/count")
    return len(rows)


def write_tsv(name: str, records: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(records[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(records)


def exact_controls() -> dict[str, object]:
    # Two coframes related by an exact Lorentz boost give the same metric,
    # while a tensor built by privileging coframe leg zero changes.
    eta = sp.diag(-1, 1, 1, 1)
    boost = sp.Matrix(
        [
            [sp.Rational(5, 4), sp.Rational(3, 4), 0, 0],
            [sp.Rational(3, 4), sp.Rational(5, 4), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    metric_residual = sp.simplify(boost.T * eta * boost - eta)
    selected = sp.diag(1, 0, 0, 0)
    selected_after = sp.simplify(boost.T * selected * boost)
    selected_residual = sp.simplify(selected_after - selected)
    if metric_residual != sp.zeros(4) or selected_residual == sp.zeros(4):
        raise AssertionError("Lorentz descent control")

    # A conformal Lorentzian metric supplies the entire projective null
    # sphere, not a preferred point of that sphere.
    n1, n2, n3, omega = sp.symbols(
        "n1 n2 n3 Omega", real=True, nonzero=True
    )
    ray = sp.Matrix([1, n1, n2, n3])
    null_form = sp.expand((ray.T * eta * ray)[0])
    conformal_null_form = sp.expand((ray.T * (omega**2 * eta) * ray)[0])
    if sp.simplify(conformal_null_form - omega**2 * null_form) != 0:
        raise AssertionError("conformal null-cone control")

    # Universal frame-dependence control used by the registered null-section
    # audit: a winding spatial frame turns constant component data into the
    # standard Hopf map. This replays an obstruction; it is not new UDT
    # physics and does not identify the carrier.
    x1, x2, x3, x4 = sp.symbols("x1 x2 x3 x4", real=True)
    radius2 = x1**2 + x2**2 + x3**2 + x4**2
    hopf = sp.Matrix(
        [
            2 * (x1 * x3 + x2 * x4),
            2 * (x2 * x3 - x1 * x4),
            x1**2 + x2**2 - x3**2 - x4**2,
        ]
    )
    hopf_norm_residual = sp.factor(hopf.dot(hopf) - radius2**2)
    if hopf_norm_residual != 0:
        raise AssertionError("winding-frame Hopf control")

    return {
        "lorentz_descent": {
            "metric_residual": "ZERO_4X4",
            "selected_leg_tensor_residual": [
                [str(item) for item in row] for row in selected_residual.tolist()
            ],
            "same_metric_different_labeled_leg": True,
        },
        "celestial_fiber": {
            "null_form": str(null_form),
            "conformal_null_form": str(conformal_null_form),
            "projectivized_future_null_rays": "S2_CONDITIONAL_ON_4D_LORENTZIAN_READOUT",
            "preferred_ray_selected": False,
        },
        "winding_frame_control": {
            "hopf_norm_residual": str(hopf_norm_residual),
            "constant_components_can_acquire_hopf_map_under_winding_frame": True,
            "new_udt_physics_claimed": False,
        },
    }


LAYERS = [
    {
        "id": "L01",
        "layer": "FOUNDATIONAL_RELATION",
        "object": "positional_dilation_and_reciprocal_clock_ruler_pair",
        "transformation_type": "FOUNDING_RELATION",
        "survival": "REGISTERED_FOUNDATIONAL",
        "scope": "exact_C0_C1_only",
        "missing": "physical_complete_configuration_owner",
    },
    {
        "id": "L02",
        "layer": "COFRAME_CHART",
        "object": "two_additive_upper_triangular_depth_characters",
        "transformation_type": "COFRAME_COMPONENT_CHARACTER",
        "survival": "DERIVED_CHART_STRUCTURE",
        "scope": "complete_registered_triangular_chart_group",
        "missing": "frame_independent_ownership_and_scalar_phi_identification",
    },
    {
        "id": "L03",
        "layer": "LOCAL_METRIC",
        "object": "conformal_causal_structure_and_celestial_null_direction_fiber",
        "transformation_type": "ASSOCIATED_PROJECTIVE_NULL_BUNDLE",
        "survival": "DERIVED_CONDITIONAL",
        "scope": "conditional_4D_Lorentzian_readout",
        "missing": "selected_section_round_target_transport_and_action",
    },
    {
        "id": "L04",
        "layer": "LOCAL_METRIC",
        "object": "distinguished_reciprocal_rank_two_plane_or_projector",
        "transformation_type": "TANGENT_SUBBUNDLE_REDUCTION",
        "survival": "OPEN",
        "scope": "full_connected_local_stabilizer",
        "missing": "registered_reduction_or_equivariant_intrinsic_definition",
    },
    {
        "id": "L05",
        "layer": "COFRAME_TO_TOPOLOGY",
        "object": "component_Hopf_number_of_unframed_null_or_tangent_section",
        "transformation_type": "FRAME_COMPONENT_MAP",
        "survival": "NOT_FRAME_INVARIANT",
        "scope": "exact_winding_frame_counterexample",
        "missing": "physical_trivialization_connection_or_intrinsic_bundle_invariant",
    },
    {
        "id": "L06",
        "layer": "COFRAME_TO_TOPOLOGY",
        "object": "angular_depth_to_Hopf_weight_and_latitude_crosswalk",
        "transformation_type": "CHART_LEVEL_CONDITIONAL_CROSSWALK",
        "survival": "EXACT_CONDITIONAL",
        "scope": "reciprocal_diagonal_angular_subgroup_plus_supplied_toric_readout",
        "missing": "frame_independent_owner_phase_global_completion_and_carrier",
    },
    {
        "id": "L07",
        "layer": "GLOBAL_COMPLETION",
        "object": "toric_connection_and_integer_class",
        "transformation_type": "GLOBAL_BUNDLE_DATA",
        "survival": "UNIQUE_CONDITIONAL",
        "scope": "supplied_transverse_torus_primitive_caps_periods_orientation",
        "missing": "native_selection_of_those_global_inputs",
    },
    {
        "id": "L08",
        "layer": "GLOBAL_COMPLETION",
        "object": "finite_cell_completion_class",
        "transformation_type": "COMPLETED_GEOMETRY_TOPOLOGY",
        "survival": "CATALOGUED_NOT_SELECTED",
        "scope": "registered_completion_atlas",
        "missing": "native_quotient_seam_cap_or_boundary_selection",
    },
    {
        "id": "L09",
        "layer": "REALIZATION",
        "object": "bootstrap_admissibility_language",
        "transformation_type": "ON_SHELL_GLOBAL_ACCEPTANCE_HYPOTHESIS",
        "survival": "WORKING",
        "scope": "registered_universe_self_consistency_and_density_window_language",
        "missing": "typed_operation_response_boundary_problem_and_uniqueness",
    },
    {
        "id": "L10",
        "layer": "REALIZATION",
        "object": "map_from_admissible_complete_geometries_to_realized_solution",
        "transformation_type": "REALIZATION_OPERATOR_OR_RELATION",
        "survival": "OPEN",
        "scope": "audited_registered_sources",
        "missing": "operator_relation_functional_or_fixed_point_with_domain_codomain",
    },
    {
        "id": "L11",
        "layer": "DYNAMICS_AND_MATTER",
        "object": "static_finite_box_Hopfion_in_no_null_L2_plus_L4_carrier",
        "transformation_type": "CONDITIONAL_CARRIER_SOLUTION",
        "survival": "SETTLED_WITHIN_STATED_PREMISES",
        "scope": "positive_round_S2_carrier_finite_box_corrected_functional",
        "missing": "native_carrier_emergence_time_live_persistence_and_unconditional_mass",
    },
    {
        "id": "L12",
        "layer": "DYNAMICS_AND_MATTER",
        "object": "complete_native_action_source_boundary_charge_and_mass",
        "transformation_type": "PHYSICAL_DYNAMICAL_COMPLETION",
        "survival": "OPEN",
        "scope": "final_A_B_C_adjudication",
        "missing": "native_action_matter_source_boundary_completion_and_bridge",
    },
]


JOINS = [
    {
        "id": "J01",
        "source": "foundational_reciprocal_pair",
        "target": "additive_coframe_depth_characters",
        "edge_status": "DERIVED_CHART_STRUCTURE",
        "exact_scope": "registered_triangular_coframe_group",
        "independent_open_requirement": "none_within_chart",
    },
    {
        "id": "J02",
        "source": "coframe_depth_character",
        "target": "frame_independent_reciprocal_geometric_object",
        "edge_status": "OPEN",
        "exact_scope": "local_Lorentz_equivalence",
        "independent_open_requirement": "equivariant_reduction_section_or_intrinsic_definition",
    },
    {
        "id": "J03",
        "source": "conditional_conformal_Lorentzian_metric",
        "target": "celestial_null_direction_S2_fiber",
        "edge_status": "DERIVED_CONDITIONAL",
        "exact_scope": "projectivized_future_null_cone",
        "independent_open_requirement": "none_for_fiber_only",
    },
    {
        "id": "J04",
        "source": "celestial_S2_fiber",
        "target": "physical_global_section_or_carrier_map",
        "edge_status": "OPEN",
        "exact_scope": "associated_bundle",
        "independent_open_requirement": "section_transport_trivialization_or_intrinsic_bundle_observable",
    },
    {
        "id": "J05",
        "source": "unframed_section_components",
        "target": "frame_independent_Hopf_charge",
        "edge_status": "OBSTRUCTED_AS_BARE_COMPONENT_CLAIM",
        "exact_scope": "winding_local_spatial_frame",
        "independent_open_requirement": "physical_connection_trivialization_or_intrinsic_reformulation",
    },
    {
        "id": "J06",
        "source": "reciprocal_diagonal_angular_character",
        "target": "Hopf_weight_and_latitude",
        "edge_status": "EXACT_CONDITIONAL_CHART_CROSSWALK",
        "exact_scope": "supplied_toric_phase_and_subgroup",
        "independent_open_requirement": "physical_descent_and_global_inputs",
    },
    {
        "id": "J07",
        "source": "supplied_toric_fibration_caps_periods_orientation",
        "target": "global_integer_Hopf_class",
        "edge_status": "UNIQUE_CONDITIONAL",
        "exact_scope": "registered_toric_closure_theorem",
        "independent_open_requirement": "native_selection_of_global_inputs",
    },
    {
        "id": "J08",
        "source": "completion_atlas",
        "target": "one_realized_finite_cell_quotient",
        "edge_status": "OPEN",
        "exact_scope": "all_registered_completion_classes",
        "independent_open_requirement": "selection_or_realization_relation",
    },
    {
        "id": "J09",
        "source": "complete_admissible_geometry_class",
        "target": "physically_realized_solution",
        "edge_status": "OPEN_NO_OPERATION",
        "exact_scope": "registered_bootstrap_wording",
        "independent_open_requirement": "typed_domain_codomain_operation_acceptance_and_uniqueness",
    },
    {
        "id": "J10",
        "source": "selected_global_geometry",
        "target": "metric_deformation_or_action",
        "edge_status": "OPEN",
        "exact_scope": "global_atlas_stage_gate",
        "independent_open_requirement": "native_variation_domain_and_dynamical_rule",
    },
    {
        "id": "J11",
        "source": "conditional_internal_round_S2_carrier_and_L2_plus_L4_action",
        "target": "finite_box_static_stable_Hopfion",
        "edge_status": "SETTLED_CONDITIONAL",
        "exact_scope": "audited_no_null_functional_and_finite_box",
        "independent_open_requirement": "none_within_stated_static_premises",
    },
    {
        "id": "J12",
        "source": "conditional_stable_Hopfion",
        "target": "native_matter_and_unconditional_mass",
        "edge_status": "OPEN",
        "exact_scope": "complete_native_theory",
        "independent_open_requirement": "carrier_emergence_source_action_scale_and_time_live_law",
    },
]


BOOTSTRAP = [
    {
        "ingredient": "input_class",
        "registered_supply": "PARTIAL",
        "exact_evidence": "complete_universe_or_realized_metric_language",
        "missing": "typed_off_shell_configuration_class",
    },
    {
        "ingredient": "equivalence_relation",
        "registered_supply": "PARTIAL",
        "exact_evidence": "pre_scale_CSN_and_metric_local_Lorentz_equivalence",
        "missing": "complete_physical_configuration_equivalence_and_global_identifications",
    },
    {
        "ingredient": "operation_or_relation",
        "registered_supply": "ABSENT_IN_AUDITED_SOURCES",
        "exact_evidence": "no_R_of_g_fixed_point_variation_or_response_map",
        "missing": "explicit_native_operation",
    },
    {
        "ingredient": "boundary_domain",
        "registered_supply": "PARTIAL",
        "exact_evidence": "static_phi_odd_seal_and_finite_cell_language",
        "missing": "complete_boundary_fields_variation_response_and_charge",
    },
    {
        "ingredient": "output_class",
        "registered_supply": "ABSENT_IN_AUDITED_SOURCES",
        "exact_evidence": "no_typed_selected_solution_codomain",
        "missing": "realized_geometry_or_equivalence_class_output",
    },
    {
        "ingredient": "acceptance_condition",
        "registered_supply": "WORKING_QUALITATIVE",
        "exact_evidence": "global_self_consistency_and_narrow_total_density_window",
        "missing": "native_computable_predicate_and_density_center_width",
    },
    {
        "ingredient": "existence_criterion",
        "registered_supply": "ABSENT_IN_AUDITED_SOURCES",
        "exact_evidence": "no_solution_theorem_or_constructive_operator",
        "missing": "existence_test",
    },
    {
        "ingredient": "uniqueness_or_ranking",
        "registered_supply": "ABSENT_IN_AUDITED_SOURCES",
        "exact_evidence": "no_selector_score_order_or_uniqueness_theorem",
        "missing": "selection_criterion",
    },
]


STATUSES = [
    {
        "id": "S01",
        "claim": "registered_reciprocal_skeleton",
        "status": "REGISTERED_FOUNDATIONAL",
        "scope": "exact_C0_C1",
    },
    {
        "id": "S02",
        "claim": "chart_depth_character_is_already_physical_phi_owner",
        "status": "OPEN",
        "scope": "blocked_by_local_frame_equivalence_and_subbundle_ownership",
    },
    {
        "id": "S03",
        "claim": "celestial_null_direction_S2_fiber",
        "status": "DERIVED_CONDITIONAL",
        "scope": "conditional_4D_conformal_Lorentzian_readout",
    },
    {
        "id": "S04",
        "claim": "fiber_selects_section_or_round_internal_target",
        "status": "OPEN",
        "scope": "no_selector_transport_action_or_boundary_completion",
    },
    {
        "id": "S05",
        "claim": "bare_component_Hopf_charge_is_frame_independent",
        "status": "REFUTED_IN_REGISTERED_SCOPE",
        "scope": "exact_winding_frame_counterexample",
    },
    {
        "id": "S06",
        "claim": "angular_depth_Hopf_weight_latitude_crosswalk",
        "status": "EXACT_CONDITIONAL_CHART_LEVEL",
        "scope": "reciprocal_diagonal_angular_subgroup_and_supplied_toric_readout",
    },
    {
        "id": "S07",
        "claim": "registered_rules_select_global_completion",
        "status": "OPEN",
        "scope": "completion_classes_catalogued_not_ranked",
    },
    {
        "id": "S08",
        "claim": "registered_bootstrap_is_a_complete_realization_operator",
        "status": "OPEN",
        "scope": "working_admissibility_language_lacks_operation_and_codomain",
    },
    {
        "id": "S09",
        "claim": "physical_descent_global_completion_and_realization_are_identical_join",
        "status": "NOT_DERIVED",
        "scope": "different_mathematical_types_and_independent_missing_inputs",
    },
    {
        "id": "S10",
        "claim": "one_future_native_law_could_close_multiple_joins",
        "status": "OPEN_POSSIBILITY",
        "scope": "no_current_law_supplies_all_edges",
    },
    {
        "id": "S11",
        "claim": "metric_native_Hopf_carrier_emergence",
        "status": "OPEN",
        "scope": "fiber_crosswalk_and_conditional_toric_bundle_do_not_select_carrier",
    },
    {
        "id": "S12",
        "claim": "complete_action_source_boundary_charge_scale_and_mass",
        "status": "OPEN",
        "scope": "final_native_action_adjudication",
    },
    {
        "id": "S13",
        "claim": "unresolved_metric_representation_join",
        "status": "LOCALIZED",
        "scope": "frame_independent_physical_configuration_object_type_distinct_from_realization_operator",
    },
    {
        "id": "S14",
        "claim": "next_bounded_metric_representation_question_after_source_only_realization_audit",
        "status": "OPEN_BOUNDED",
        "scope": "whether_complete_metric_defines_intrinsic_reduction_section_or_bundle_invariant_without_frame_choice",
    },
]


def main() -> None:
    source_count = verify_sources()
    controls = exact_controls()
    write_tsv("LAYER_SURVIVAL_LEDGER.tsv", LAYERS)
    write_tsv("JOIN_GRAPH.tsv", JOINS)
    write_tsv("BOOTSTRAP_REALIZATION_MATRIX.tsv", BOOTSTRAP)
    write_tsv("STATUS_LEDGER.tsv", STATUSES)
    result = {
        "schema": "udt-complete-metric-realization-zoomout-v1",
        "source_count": source_count,
        "cpu_only": True,
        "new_physical_premises": 0,
        "controls": controls,
        "counts": {
            "layers": len(LAYERS),
            "joins": len(JOINS),
            "bootstrap_ingredients": len(BOOTSTRAP),
            "status_rows": len(STATUSES),
            "open_or_obstructed_joins": sum(
                row["edge_status"]
                in {
                    "OPEN",
                    "OPEN_NO_OPERATION",
                    "OBSTRUCTED_AS_BARE_COMPONENT_CLAIM",
                }
                for row in JOINS
            ),
            "native_end_to_end_bridges": 0,
        },
        "unification_tests": {
            "single_frame_independent_reciprocal_object_supplies_all_joins": False,
            "reason_one": "global_completion_realization_and_dynamics_require_independent_typed_data",
            "single_registered_realization_rule_supplies_all_joins": False,
            "reason_two": "registered_bootstrap_has_no operation_output_existence_or_uniqueness",
        },
        "dependency_layers": [
            "REPRESENTATION_DESCENT",
            "GLOBAL_COMPLETION",
            "REALIZATION",
            "DEFORMATION_DYNAMICS_AND_MATTER",
        ],
        "ordering_ruling": {
            "different_mathematical_types": True,
            "strict_total_order_derived": False,
            "one_future_law_may_close_multiple_joins_jointly": True,
            "controlling_first_conceptual_priority": "SOURCE_ONLY_REALIZATION_OPERATOR_AUDIT",
            "this_package_completed_that_source_census": True,
        },
        "next_bounded_metric_representation_question": (
            "Does the complete metric define an intrinsic frame-independent "
            "reduction, section, or bundle invariant carrying reciprocal/Hopf "
            "data, without choosing a coframe or carrier?"
        ),
        "maximum_conclusion": MAXIMUM,
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
