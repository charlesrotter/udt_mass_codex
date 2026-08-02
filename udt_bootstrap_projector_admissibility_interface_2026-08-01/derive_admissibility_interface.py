#!/usr/bin/env python3
"""Derive the bootstrap/projector type interface and exact implication controls."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    x, o, r = sp.symbols("x o r", real=True)
    graph = sp.Matrix([o - r * x])
    j_graph = graph.jacobian([x, o])
    graph_rank = int(j_graph.rank())
    graph_nullity = 2 - graph_rank
    assert graph_rank == 1 and graph_nullity == 1

    local_only = sp.Matrix([o - r * x, x])
    global_only = sp.Matrix([o - r * x, o])
    coupled = sp.Matrix([o - r * x, x - o])
    ranks = {
        "graph_only": int(j_graph.rank()),
        "local_only_plus_graph": int(local_only.jacobian([x, o]).rank()),
        "global_only_plus_graph": int(global_only.jacobian([x, o]).rank()),
        "coupled_plus_graph_generic_r": int(coupled.jacobian([x, o]).rank()),
    }
    assert ranks == {
        "graph_only": 1,
        "local_only_plus_graph": 2,
        "global_only_plus_graph": 2,
        "coupled_plus_graph_generic_r": 2,
    }

    # Finite fiber controls distinguish a global on/off window, a separable local+global filter,
    # and a genuinely O-dependent family of nonempty local fibers.
    xs = ("x0", "x1", "x2", "x3")
    os = ("o0", "o1", "o2")
    readout = {"x0": "o0", "x1": "o1", "x2": "o1", "x3": "o2"}
    global_window = {"o0": set(), "o1": set(xs), "o2": set()}
    projector = {"x1", "x2"}
    separable = {key: (projector if key == "o1" else set()) for key in os}
    modulated = {"o0": {"x0"}, "o1": {"x1"}, "o2": {"x0", "x2"}}

    def graph_intersection(fibers: dict[str, set[str]]) -> set[str]:
        return {state for state in xs if state in fibers[readout[state]]}

    finite = {
        "readout_graph_projection": list(xs),
        "global_window_graph_intersection": sorted(graph_intersection(global_window)),
        "separable_graph_intersection": sorted(graph_intersection(separable)),
        "modulated_graph_intersection": sorted(graph_intersection(modulated)),
        "global_window_nonempty_fiber_shapes": len({frozenset(v) for v in global_window.values() if v}),
        "separable_nonempty_fiber_shapes": len({frozenset(v) for v in separable.values() if v}),
        "modulated_nonempty_fiber_shapes": len({frozenset(v) for v in modulated.values() if v}),
    }
    assert finite == {
        "readout_graph_projection": ["x0", "x1", "x2", "x3"],
        "global_window_graph_intersection": ["x1", "x2"],
        "separable_graph_intersection": ["x1", "x2"],
        "modulated_graph_intersection": ["x0", "x1"],
        "global_window_nonempty_fiber_shapes": 1,
        "separable_nonempty_fiber_shapes": 1,
        "modulated_nonempty_fiber_shapes": 3,
    }

    candidates = [
        {"candidate_id": "C01", "candidate_join": "PROJECTOR_NEIGHBORHOOD_ALONE", "independent_X_O": "NO_O_ARGUMENT", "X_dependence": "YES", "O_dependence": "NO", "complete_R": "NO", "native_on_shell_domain": "NO", "observer_naturality": "INTRINSIC_LOCAL_GEOMETRY_ONLY", "proper_graph_intersection": "NOT_DEFINED", "premise_firewall": "PASS", "ruling": "OFFSHELL_LOCAL_FILTER_NOT_BOOTSTRAP"},
        {"candidate_id": "C02", "candidate_join": "READOUT_GRAPH_ALONE", "independent_X_O": "YES_AS_GRAPH_ARGUMENTS", "X_dependence": "FORWARD_READOUT_ONLY", "O_dependence": "EQUALITY_ONLY", "complete_R": "NO_PARTIAL", "native_on_shell_domain": "NO", "observer_naturality": "PARTIAL_CONDITIONAL", "proper_graph_intersection": "NO_PROJECTION_IS_ALL_X", "premise_firewall": "PASS", "ruling": "READOUT_NOT_RETURN"},
        {"candidate_id": "C03", "candidate_join": "GLOBAL_DENSITY_WINDOW", "independent_X_O": "YES", "X_dependence": "NO_BEFORE_SUBSTITUTION", "O_dependence": "YES_WINDOW", "complete_R": "NO_NATIVE_MASS_DENSITY", "native_on_shell_domain": "NO", "observer_naturality": "IF_NATIVE_SCALAR_DEFINED", "proper_graph_intersection": "UNCOMPUTABLE", "premise_firewall": "PASS", "ruling": "WORKING_ONE_WAY_SURVIVAL_FILTER_TYPE"},
        {"candidate_id": "C04", "candidate_join": "PROJECTOR_RESPONSE_AS_RETURN", "independent_X_O": "NO_O_ARGUMENT", "X_dependence": "YES", "O_dependence": "NO", "complete_R": "NO", "native_on_shell_domain": "NO", "observer_naturality": "LOCAL_GEOMETRIC_RESPONSE", "proper_graph_intersection": "NOT_DEFINED", "premise_firewall": "PASS", "ruling": "PROJECTOR_RESPONSE_CANNOT_BE_BOOTSTRAP_RETURN_ALONE"},
        {"candidate_id": "C05", "candidate_join": "GLOBAL_CURVATURE_READOUT", "independent_X_O": "YES_AS_GRAPH_ARGUMENTS", "X_dependence": "FORWARD_READOUT_ONLY", "O_dependence": "EQUALITY_ONLY", "complete_R": "PARTIAL_METRIC_READOUT", "native_on_shell_domain": "NO", "observer_naturality": "POSSIBLE_FOR_SPECIFIED_SCALARS", "proper_graph_intersection": "NO_FOR_GRAPH_ALONE", "premise_firewall": "PASS", "ruling": "CURVATURE_READOUT_NOT_RETURN_RELATION"},
        {"candidate_id": "C06", "candidate_join": "CONDITIONAL_STABILITY_BASIN", "independent_X_O": "NO_COMPLETE_O_ARGUMENT", "X_dependence": "CONDITIONAL", "O_dependence": "NO_NATIVE_MAP", "complete_R": "NO", "native_on_shell_domain": "CONDITIONAL_CARRIER_ACTION_ONLY", "observer_naturality": "NOT_COMPLETE", "proper_graph_intersection": "NOT_DEFINED", "premise_firewall": "FAIL_IF_PROMOTED", "ruling": "CONDITIONAL_MODEL_CANNOT_DEFINE_NATIVE_MEMBERSHIP"},
        {"candidate_id": "C07", "candidate_join": "ABSTRACT_TWO_ARROW_RELATION", "independent_X_O": "REQUIRED_BY_TYPE", "X_dependence": "REQUIRED_NOT_DEFINED", "O_dependence": "REQUIRED_NOT_DEFINED", "complete_R": "NO", "native_on_shell_domain": "NO", "observer_naturality": "REQUIRED_NOT_INSTANTIATED", "proper_graph_intersection": "REQUIRED_NOT_COMPUTABLE", "premise_firewall": "PASS", "ruling": "TYPE_INCOMPLETE"},
        {"candidate_id": "C08", "candidate_join": "COMPLETE_SAME_SOLUTION_INTERSECTION", "independent_X_O": "REQUIRED", "X_dependence": "A_OPEN", "O_dependence": "A_OPEN", "complete_R": "OPEN", "native_on_shell_domain": "OPEN", "observer_naturality": "CONSTRAINT_KNOWN_ACTIONS_INCOMPLETE", "proper_graph_intersection": "UNCOMPUTABLE", "premise_firewall": "PASS", "ruling": "OPEN_MISSING_E_NATIVE_R_AND_A"},
    ]
    write_tsv("INTERFACE_GATE_MATRIX.tsv", candidates)

    hierarchy = [
        {"level": "L0", "name": "FORWARD_READOUT", "formal_object": "O=R[X]", "fiber_behavior": "one_graph_point_per_X", "what_it_can_do": "recompute_global_data", "what_it_cannot_do": "select_X_or_feed_back"},
        {"level": "L1", "name": "GLOBAL_SURVIVAL_WINDOW", "formal_object": "O_in_I", "fiber_behavior": "all_X_or_empty", "what_it_can_do": "one_way_on_shell_filter_after_R_exists", "what_it_cannot_do": "distinguish_local_shapes_at_fixed_O"},
        {"level": "L2", "name": "SEPARABLE_MUTUAL_FILTER", "formal_object": "P(X)_and_O_in_I", "fiber_behavior": "same_nonempty_P_through_window", "what_it_can_do": "depend_on_both_arguments_as_membership", "what_it_cannot_do": "show_global_modulation_of_local_family"},
        {"level": "L3", "name": "FAMILY_TUNING", "formal_object": "X_in_F_O_with_F_O1_not_equal_F_O2", "fiber_behavior": "nonempty_local_fiber_shape_changes_with_O", "what_it_can_do": "encode_chicken_and_egg_admissibility", "what_it_cannot_do": "supply_derivative_dynamics_or_action"},
        {"level": "L4", "name": "DIFFERENTIABLE_RESPONSE", "formal_object": "A(X,O)=0_with_D_O_A_nontrivial", "fiber_behavior": "tangent_response_changes_with_O", "what_it_can_do": "pose_linear_response_and_coupled_Jacobian", "what_it_cannot_do": "derive_pairing_action_or_stability_by_itself"},
        {"level": "L5", "name": "COMPLETE_ON_SHELL_CLOSURE", "formal_object": "N_intersection_Sol(E_native)_intersection_pi_X[Z(A)_intersection_Graph(R)]", "fiber_behavior": "same_complete_solution", "what_it_can_do": "define_the_requested_intersection", "what_it_cannot_do": "exist_until_E_native_R_A_and_domain_are_defined"},
    ]
    write_tsv("ADMISSIBILITY_HIERARCHY.tsv", hierarchy)

    missing = [
        {"slot": "M01", "object": "N_projector", "status": "DERIVED_CONDITIONAL_BOUNDED", "current_content": "open_C3_neighborhoods_around_C01_C06", "needed_for_intersection": "available_local_geometric_antecedent"},
        {"slot": "M02", "object": "complete_native_configuration_domain", "status": "DERIVED_TYPED_NOT_SELECTED", "current_content": "off_shell_parent_arena", "needed_for_intersection": "one_selected_completion_and_variation_domain"},
        {"slot": "M03", "object": "E_native", "status": "OPEN", "current_content": "no_complete_native_equation_or_persistence_rule", "needed_for_intersection": "Sol(E_native)"},
        {"slot": "M04", "object": "R_geometric", "status": "PARTIAL", "current_content": "curvature_Cartan_boundary_transport_topology_branch_readouts", "needed_for_intersection": "one_complete_same_solution_map_for_claimed_channels"},
        {"slot": "M05", "object": "R_mass_energy_density", "status": "OPEN", "current_content": "no_native_total_mass_energy_or_same_solution_density", "needed_for_intersection": "lawful_density_window_or_mass_energy_feedback"},
        {"slot": "M06", "object": "A_global_to_local", "status": "OPEN", "current_content": "two_arrow_type_only", "needed_for_intersection": "nonidentity_membership_fibers_F_O"},
        {"slot": "M07", "object": "observer_action_on_complete_X_O_and_codomain", "status": "PARTIAL_CONSTRAINT", "current_content": "equivariance_and_zero_preservation_required", "needed_for_intersection": "verify_actual_A_is_natural"},
        {"slot": "M08", "object": "boundary_corner_global_modulus_channels", "status": "OPEN_REQUIRED", "current_content": "partial_geometry_operator_dependent_response", "needed_for_intersection": "complete_domain_and_variation"},
        {"slot": "M09", "object": "same_solution_witness", "status": "OPEN", "current_content": "no_member_satisfying_all_slots", "needed_for_intersection": "nonempty_certification"},
    ]
    write_tsv("MISSING_INPUT_LEDGER.tsv", missing)

    intersection = [
        {"object": "projector_neighborhood", "formula": "N_projector", "current_status": "DEFINED_BOUNDED_OFFSHELL", "selection_status": "NO"},
        {"object": "readout_graph", "formula": "Graph(R)={(X,O):O=R[X]}", "current_status": "R_PARTIAL", "selection_status": "PROJECTION_ALL_X_WHEN_DEFINED"},
        {"object": "bootstrap_membership", "formula": "Z(A)={(X,O):A(X,O)=0}", "current_status": "A_OPEN", "selection_status": "UNCOMPUTABLE"},
        {"object": "on_shell_set", "formula": "Sol(E_native)", "current_status": "E_NATIVE_OPEN", "selection_status": "UNCOMPUTABLE"},
        {"object": "requested_intersection", "formula": "N_projector_intersection_Sol(E_native)_intersection_pi_X[Z(A)_intersection_Graph(R)]", "current_status": "OPEN_MISSING_E_R_A", "selection_status": "NOT_RUN_NOT_EMPTY_OR_NEGATIVE"},
    ]
    write_tsv("INTERSECTION_STATUS.tsv", intersection)

    algebra = {
        "schema": "udt.bootstrap_projector_admissibility_interface.algebra.v1",
        "graph_equation": "o-r*x=0",
        "graph_jacobian_rank": graph_rank,
        "graph_jacobian_nullity": graph_nullity,
        "jacobian_ranks": ranks,
        "finite_controls": finite,
        "same_solution_intersection": "N_projector ∩ Sol(E_native) ∩ pi_X[Z(A) ∩ Graph(R)]",
        "operational_minimum": "independent_X_O_nontrivial_both_arguments_nonempty_proper_graph_intersection_observer_natural",
        "tuning_refinement": "nonempty_membership_fibers_F_O_change_with_independent_O",
    }
    (HERE / "ALGEBRA_RESULT.json").write_text(json.dumps(algebra, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = {
        "schema": "udt.bootstrap_projector_admissibility_interface.result.v1",
        "status": "PASS",
        "outcome": "PROJECTOR_ANTECEDENT_ROBUST__BOOTSTRAP_INTERSECTION_OPEN_MISSING_E_NATIVE_R_AND_A",
        "candidate_count": len(candidates),
        "passing_complete_intersections": 0,
        "hierarchy_levels": len(hierarchy),
        "missing_slots": len(missing),
        "density_window_ruling": "WORKING_ONE_WAY_SURVIVAL_FILTER_TYPE_NOT_TWO_WAY_TUNING_BY_ITSELF",
        "projector_ruling": "AVAILABLE_LOCAL_GEOMETRIC_ANTECEDENT_NOT_ON_SHELL_MEMBERSHIP",
        "maximum_conclusion": "EXACT_INTERFACE_AND_MISSING_INPUT_LEDGER_ONLY_NO_BOOTSTRAP_LAW_OR_STABILITY",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
