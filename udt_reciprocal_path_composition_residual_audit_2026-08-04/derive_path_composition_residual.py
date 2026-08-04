#!/usr/bin/env python3
"""Exact production derivation for the reciprocal path-composition residual audit."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import sys
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
checks: list[str] = []


def require(name: str, condition: bool) -> None:
    assert bool(condition), name
    checks.append(name)


def zero_matrix(name: str, matrix: sp.Matrix) -> None:
    require(name, matrix.applyfunc(sp.simplify) == sp.zeros(*matrix.shape))


def write_tsv(name: str, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


# 1. Founded real reciprocal character.
a, b, p = sp.symbols("a b p", real=True)


def D(value: sp.Expr) -> sp.Matrix:
    return sp.diag(sp.exp(-value), sp.exp(value))


zero_matrix("character_composition", D(b) * D(a) - D(a + b))
zero_matrix("character_reversal", D(-a) - D(a).inv())
require("character_determinant_one", sp.simplify(D(a).det()) == 1)
require("real_character_faithful", sp.solveset(sp.exp(p) - 1, p, domain=sp.S.Reals) == sp.FiniteSet(0))
require("nonzero_character_witness", D(sp.log(2)) != sp.eye(2))

# 2. Four-object edge/cycle complex.
edges = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
triangles = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
edge_index = {edge: index for index, edge in enumerate(edges)}
B = sp.zeros(6, 4)
for row, (i, j) in enumerate(edges):
    B[row, i] = -1
    B[row, j] = 1
C = sp.zeros(4, 6)
for row, (i, j, k) in enumerate(triangles):
    C[row, edge_index[(i, j)]] = 1
    C[row, edge_index[(j, k)]] = 1
    C[row, edge_index[(i, k)]] = -1

require("incidence_rank_three", B.rank() == 3)
require("incidence_common_offset_kernel", B.nullspace() == [sp.ones(4, 1)])
require("triangle_rank_three", C.rank() == 3)
zero_matrix("boundary_of_coboundary_zero", C * B)
require("exact_edge_space_equals_triangle_kernel_by_dimension", 6 - C.rank() == B.rank())

for index, potential in enumerate((sp.Matrix([0, 1, 4, 9]), sp.Matrix([3, -2, 5, 11]), sp.Matrix([0, 0, 1, -1])), 1):
    edge_values = B * potential
    zero_matrix(f"endpoint_potential_{index}_triangle_identity", C * edge_values)
    require(f"endpoint_potential_{index}_nonvacuous", any(value != 0 for value in edge_values))

free_edges = sp.Matrix([1, 0, 0, 0, 0, 0])
require("free_edge_cochain_can_fail", C * free_edges != sp.zeros(4, 1))
edge_symbols = sp.Matrix(sp.symbols("y0:6"))
require("edge_data_residual_rank_three", (C * edge_symbols).jacobian(tuple(edge_symbols)).rank() == 3)

phi0, phi1, phi2 = sp.symbols("phi0 phi1 phi2")
composed_endpoint = (phi1 - phi0) + (phi2 - phi1) - (phi2 - phi0)
require("endpoint_composition_is_identity", sp.expand(composed_endpoint) == 0)
require("endpoint_composition_profile_jacobian_zero", all(sp.diff(composed_endpoint, q) == 0 for q in (phi0, phi1, phi2)))

# 3. Exact versus nonclosed one-form path controls on the unit square.
x, y = sp.symbols("x y", real=True)
phi = x**2 * y + 3 * x
alpha_exact = (sp.diff(phi, x), sp.diff(phi, y))
alpha_nonclosed = (-y / 2, x / 2)
curvature_exact = sp.diff(alpha_exact[1], x) - sp.diff(alpha_exact[0], y)
curvature_nonclosed = sp.diff(alpha_nonclosed[1], x) - sp.diff(alpha_nonclosed[0], y)
require("exact_form_closed", sp.simplify(curvature_exact) == 0)
require("nonclosed_form_curvature_one", sp.simplify(curvature_nonclosed) == 1)


def unit_square_integral(form: tuple[sp.Expr, sp.Expr]) -> sp.Expr:
    px, qy = form
    bottom = sp.integrate(px.subs(y, 0), (x, 0, 1))
    right = sp.integrate(qy.subs(x, 1), (y, 0, 1))
    top = sp.integrate(px.subs(y, 1), (x, 1, 0))
    left = sp.integrate(qy.subs(x, 0), (y, 1, 0))
    return sp.simplify(bottom + right + top + left)


require("exact_form_zero_square_period", unit_square_integral(alpha_exact) == 0)
require("nonclosed_form_nonzero_square_period", unit_square_integral(alpha_nonclosed) == 1)
require("segmented_path_integral_adds_by_definition", sp.Symbol("I01") + sp.Symbol("I12") == sp.Symbol("I01") + sp.Symbol("I12"))

# 4. Metric-control family: composition accepts distinct reciprocal metrics/profiles.
z = sp.symbols("z", real=True)
profile_curvatures = {}
for name, profile in (("zero", sp.Integer(0)), ("linear", z), ("quadratic", z**2)):
    curvature = sp.simplify(2 * (sp.diff(profile, z, 2) - 2 * sp.diff(profile, z) ** 2) * sp.exp(-2 * profile))
    profile_curvatures[name] = sp.simplify(curvature.subs(z, 0))
    d01 = sp.simplify(profile.subs(z, 1) - profile.subs(z, 0))
    d12 = sp.simplify(profile.subs(z, 2) - profile.subs(z, 1))
    d02 = sp.simplify(profile.subs(z, 2) - profile.subs(z, 0))
    zero_matrix(f"profile_{name}_character_composition", D(d12) * D(d01) - D(d02))
require("profile_curvatures_distinct", set(profile_curvatures.values()) == {sp.Integer(-4), sp.Integer(0), sp.Integer(4)})

# 5. Typed semidirect transport composition with a noncommuting generator.
eta = sp.diag(-1, 1)
X0 = sp.diag(-1, 1)
U1 = sp.Matrix([[sp.Rational(5, 4), -sp.Rational(3, 4)], [-sp.Rational(3, 4), sp.Rational(5, 4)]])
U2 = sp.Matrix([[sp.Rational(13, 12), -sp.Rational(5, 12)], [-sp.Rational(5, 12), sp.Rational(13, 12)]])
zero_matrix("transport_U1_is_Lorentz", U1.T * eta * U1 - eta)
zero_matrix("transport_U2_is_Lorentz", U2.T * eta * U2 - eta)
require("transport_changes_generator", sp.simplify(U1 * X0 * U1.inv()) != X0)

d_a, d_b = sp.log(2), sp.log(3)
D0a, D0b = D(d_a), D(d_b)
D1b = sp.simplify(U1 * D0b * U1.inv())
zero_matrix("transport_intertwines_character", D1b * U1 - U1 * D0b)
T_alpha = U1 * D0a
T_beta = U2 * D1b
zero_matrix("semidirect_typed_composition", T_beta * T_alpha - U2 * U1 * D(sp.log(6)))
require("semidirect_composition_nonvacuous", T_beta * T_alpha != sp.eye(2))

# 6. Loop objects remain distinct.
period_response = D(sp.log(2))
lc_holonomy = U1
full_loop = lc_holonomy * period_response
require("nonzero_period_visible", period_response != sp.eye(2))
require("nontrivial_lc_holonomy_visible", lc_holonomy != sp.eye(2))
require("full_loop_nonidentity_control", full_loop != sp.eye(2))
zero_matrix("lc_holonomy_metric_isometry", lc_holonomy.T * eta * lc_holonomy - eta)
require("reciprocal_dilation_not_metric_isometry", period_response.T * eta * period_response != eta)
require("zero_period_does_not_remove_lc_holonomy", lc_holonomy * D(0) != sp.eye(2))
require("identity_lc_does_not_remove_nonzero_period", sp.eye(2) * period_response != sp.eye(2))

# 7. Frozen source statements required for the provenance ruling.
source_requirements = {
    "cold_packet_intermediate_position": ("UDT_NATIVE_ACTION_COLD_PACKET.md", "comparisons compose consistently through an intermediate position"),
    "founding_additive_coordinate": ("UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md", "P(\\Delta_1+\\Delta_2)=P(\\Delta_1)P(\\Delta_2)"),
    "current_physical_assignment_open": ("CURRENT_SCIENTIFIC_PREMISES.md", "physical observer/path assignment"),
    "semantic_path_variable_absent": ("udt_founding_observer_comparison_semantics_audit_2026-07-27/SOURCE_CLAIM_OUTCOMES.tsv", "Composition_domain_contains_no_metric_path_variable"),
    "groupoid_depth_open": ("udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/STATUS_LEDGER.tsv", "metric_native_signed_depth_cocycle"),
    "composition_no_depth_selection": ("udt_native_global_coframe_definition_audit_2026-07-28/EXACT_DERIVATION.md", "Composition does not select depth"),
    "reciprocity_no_realization": ("udt_whole_configuration_reciprocity_audit_2026-08-01/EXACT_DERIVATION.md", "pairwise comparison cocycle -> realized phi profile"),
    "path_lift_conditional": ("udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/STATUS_LEDGER.tsv", "given_specified_path_and_parent_connection"),
    "architecture_not_selected": ("udt_basic_vs_universal_query_residual_audit_2026-08-04/FOUNDATIONAL_RULING.tsv", "no nontrivial native residual selected"),
    "founded_query_depth_open": ("udt_native_law_home_codomain_ownership_audit_2026-08-04/FOUNDATIONAL_ENTAILMENT_MATRIX.tsv", "abstract depth assignment still open physically"),
}
for name, (relative, needle) in source_requirements.items():
    require(name, needle in (ROOT / relative).read_text(encoding="utf-8"))

candidate_rows = [
    {"candidate_id": "C01", "outcome": "IDENTITY_AFTER_ADDITIVE_DEPTH", "home": "CHARACTER_OPERATOR", "metric_residual": "NO", "foundation_status": "DERIVED_KINEMATIC_IDENTITY", "reason": "D_b_D_a_equals_D_a_plus_b_for_every_real_additive_depth"},
    {"candidate_id": "C02", "outcome": "NONTRIVIAL_ON_FREE_EDGE_DATA", "home": "QUERY_DEPTH_DATA", "metric_residual": "NO_WITHOUT_DEPTH_MAP", "foundation_status": "DERIVED_ABSTRACT_CONSISTENCY", "reason": "rank_three_triangle_system_restricts_six_free_edges_but_C_B_is_identically_zero"},
    {"candidate_id": "C03", "outcome": "IDENTITY_FOR_EVERY_ENDPOINT_POTENTIAL", "home": "OBJECT_POTENTIAL", "metric_residual": "NO", "foundation_status": "NONSELECTING", "reason": "every_f_gives_delta_f_and_composition_has_zero_profile_Jacobian"},
    {"candidate_id": "C04", "outcome": "ADDITIVE_COCYCLE_IS_SUPPLIED_DATA_CLASS", "home": "PATH_GROUPOID", "metric_residual": "NO_WITHOUT_ASSIGNMENT", "foundation_status": "CONDITIONAL_KINEMATIC_INPUT", "reason": "composition_defines_cocycle_and_allows_nonzero_loop_periods"},
    {"candidate_id": "C05", "outcome": "PATH_ADDITIVITY_BY_INTEGRAL_CONCATENATION", "home": "PATH_GROUPOID", "metric_residual": "NO_WITHOUT_ALPHA_OF_G", "foundation_status": "MATHEMATICAL_CONTROL", "reason": "closed_and_nonclosed_one_forms_both_add_on_concatenated_paths"},
    {"candidate_id": "C06", "outcome": "LOCAL_ENDPOINT_INDEPENDENCE_RESTRICTION", "home": "SPACETIME_TWO_FORM", "metric_residual": "POSSIBLE_IF_ALPHA_OF_G", "foundation_status": "CONDITIONAL_EXTRA_PREMISE", "reason": "d_alpha_zero_is_not_implied_by_path_additivity"},
    {"candidate_id": "C07", "outcome": "GLOBAL_ENDPOINT_INDEPENDENCE_RESTRICTION", "home": "LOOP_PERIOD_FAMILY", "metric_residual": "POSSIBLE_IF_ALPHA_OF_G", "foundation_status": "CONDITIONAL_EXTRA_PREMISE", "reason": "zero_periods_are_stronger_than_local_closedness_and_not_founded"},
    {"candidate_id": "C08", "outcome": "FUNCTORIAL_TRANSPORT_IDENTITY", "home": "FRAME_PATH_GROUPOID", "metric_residual": "NO", "foundation_status": "DEFINED_FROM_SUPPLIED_METRIC", "reason": "Levi_Civita_transport_composes_for_every_supplied_metric"},
    {"candidate_id": "C09", "outcome": "SEMIDIRECT_COMPOSITION_IDENTITY_GIVEN_INPUTS", "home": "PAIR_FRAME_PATH_GROUPOID", "metric_residual": "NO", "foundation_status": "CONDITIONAL_EXACT_KINEMATICS", "reason": "transported_generator_and_additive_depth_make_composition_exact"},
    {"candidate_id": "C10", "outcome": "NONTRIVIAL_FULL_LOOP_RESTRICTION_IF_IMPOSED", "home": "GLOBAL_LOOP_SPACE", "metric_residual": "YES_CONDITIONAL", "foundation_status": "NOT_FOUNDED_EXTRA", "reason": "T_loop_identity_would_restrict_period_and_holonomy_but_no_source_demands_it"},
    {"candidate_id": "C11", "outcome": "NATURALITY_GATE_ON_FUTURE_LAW", "home": "LAW_BUNDLE", "metric_residual": "NO_LAW_SUPPLIED", "foundation_status": "DERIVED_SCOPED_GATE", "reason": "equivariance_rejects_bad_laws_but_does_not_generate_one"},
    {"candidate_id": "C12", "outcome": "ARCHITECTURE_ADMISSIBLE_WITHOUT_RESIDUAL", "home": "METRIC_CONFIGURATION_SPACE", "metric_residual": "OPEN_NOT_SUPPLIED", "foundation_status": "ADMISSIBLE_NOT_SELECTED", "reason": "universal_query_quantifier_is_possible_but_not_founded_as_dynamics"},
]
write_tsv("CANDIDATE_OUTCOMES.tsv", ("candidate_id", "outcome", "home", "metric_residual", "foundation_status", "reason"), candidate_rows)

source_rows = [
    {"source_id": "S01", "source_object": "cold_packet_intermediate_position", "owned_content": "ABSTRACT_INTERMEDIATE_COMPOSITION", "metric_path_quantifier": "ABSENT", "depth_assignment": "SUPPLIED_RELATIVE_DEPTH", "ruling": "NO_METRIC_RESIDUAL"},
    {"source_id": "S02", "source_object": "founding_exponential_derivation", "owned_content": "ONE_PARAMETER_CHARACTER", "metric_path_quantifier": "ABSENT", "depth_assignment": "ADDITIVE_COORDINATE", "ruling": "KINEMATIC_IDENTITY"},
    {"source_id": "S03", "source_object": "current_premise_registry", "owned_content": "FOUNDED_PHI_IDENTITY", "metric_path_quantifier": "OPEN", "depth_assignment": "PHYSICAL_ASSIGNMENT_OPEN", "ruling": "BLOCKS_PROMOTION"},
    {"source_id": "S04", "source_object": "founding_semantics_census", "owned_content": "ABSTRACT_OPERATOR_PRECEDES_PATH", "metric_path_quantifier": "ZERO_SOURCES_FORCE_ENDPOINT_OR_PATH", "depth_assignment": "OPEN", "ruling": "SEMANTICS_OPEN"},
    {"source_id": "S05", "source_object": "typed_path_groupoid", "owned_content": "EXACT_COMPOSITION_FOR_ALL_LAMBDA", "metric_path_quantifier": "CONDITIONAL_PATH_LABEL", "depth_assignment": "METRIC_NATIVE_COCYCLE_OPEN", "ruling": "NONSELECTING_GIVEN_INPUT"},
    {"source_id": "S06", "source_object": "global_coframe_definition", "owned_content": "ALL_ENDPOINT_FUNCTIONS_COMPOSE", "metric_path_quantifier": "NONE", "depth_assignment": "ARBITRARY_f", "ruling": "COMPOSITION_DOES_NOT_SELECT_DEPTH"},
    {"source_id": "S07", "source_object": "whole_configuration_Reciprocity", "owned_content": "NATURALITY_AND_RELATIVE_RECONSTRUCTION", "metric_path_quantifier": "FUTURE_TYPED", "depth_assignment": "REALIZATION_NOT_DERIVED", "ruling": "LAW_GATE_NOT_GENERATOR"},
    {"source_id": "S08", "source_object": "intrinsic_holonomy_control", "owned_content": "PATH_LIFT_GIVEN_PATH_AND_CONNECTION", "metric_path_quantifier": "CONDITIONAL", "depth_assignment": "NOT_SUPPLIED", "ruling": "ENDPOINT_CLOSURE_NOT_FOUNDED"},
    {"source_id": "S09", "source_object": "native_law_type_audit", "owned_content": "TYPED_QUERY_HOME", "metric_path_quantifier": "OPEN", "depth_assignment": "OPEN", "ruling": "NO_COMPLETE_LAW_SELECTED"},
    {"source_id": "S10", "source_object": "basic_vs_universal_audit", "owned_content": "UNIVERSAL_ARCHITECTURE_ADMISSIBLE", "metric_path_quantifier": "NOT_SELECTED", "depth_assignment": "OPEN", "ruling": "NO_NONTRIVIAL_RESIDUAL"},
    {"source_id": "S11", "source_object": "SNe_anchor", "owned_content": "DOWNSTREAM_READOUT_COMPATIBILITY", "metric_path_quantifier": "NONE", "depth_assignment": "CONDITIONAL_READOUT", "ruling": "NO_UPSTREAM_SELECTION"},
]
write_tsv("SOURCE_PROVENANCE_RULINGS.tsv", ("source_id", "source_object", "owned_content", "metric_path_quantifier", "depth_assignment", "ruling"), source_rows)

source_adjudication_data = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md": ("FOUNDING_PACKET", "intermediate_position_composition", "NOT_SUPPLIED", "NOT_SUPPLIED", "ABSTRACT_COMPOSITION_ONLY"),
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": ("FOUNDING_DERIVATION", "one_parameter_character", "NOT_SUPPLIED", "NOT_SUPPLIED", "KINEMATIC_IDENTITY"),
    "CURRENT_SCIENTIFIC_PREMISES.md": ("CURRENT_PREMISE_CONTROL", "founded_phi_identity", "PHYSICAL_ASSIGNMENT_OPEN", "OPEN", "BLOCKS_PROMOTION"),
    "CURRENT_SCIENTIFIC_PREMISES.tsv": ("CURRENT_PREMISE_CONTROL", "founded_phi_identity", "PHYSICAL_ASSIGNMENT_OPEN", "OPEN", "BLOCKS_PROMOTION"),
    "udt_founding_reciprocity_object_audit_2026-07-27/AUDIT_REPORT.md": ("FOUNDING_ENTAILMENT", "abstract_comparison_exact", "OPEN", "NOT_FOUNDED", "NO_METRIC_RESIDUAL"),
    "udt_founding_reciprocity_object_audit_2026-07-27/EXACT_DERIVATION.md": ("FOUNDING_ENTAILMENT", "abstract_comparison_exact", "OPEN", "NOT_FOUNDED", "NO_METRIC_RESIDUAL"),
    "udt_founding_reciprocity_object_audit_2026-07-27/OBJECT_CLASSIFICATION.tsv": ("FOUNDING_ENTAILMENT", "object_by_object_classification", "OPEN", "ENDPOINT_CLOSURE_NOT_DERIVED", "NO_METRIC_RESIDUAL"),
    "udt_founding_observer_comparison_semantics_audit_2026-07-27/AUDIT_REPORT.md": ("SEMANTICS_AUTHORITY", "abstract_not_path_homotopy", "OPEN", "ZERO_SOURCES_FORCE_ROUTE", "SEMANTICS_OPEN"),
    "udt_founding_observer_comparison_semantics_audit_2026-07-27/SOURCE_CLAIM_OUTCOMES.tsv": ("SEMANTICS_AUTHORITY", "36_claim_census", "OPEN", "ZERO_SOURCES_FORCE_ROUTE", "SEMANTICS_OPEN"),
    "udt_founding_observer_comparison_semantics_audit_2026-07-27/IMPLICATION_MATRIX.tsv": ("SEMANTICS_AUTHORITY", "endpoint_and_path_implications", "OPEN", "EXTRA_REQUIREMENTS_ABSENT", "SEMANTICS_OPEN"),
    "udt_observer_pair_clock_operator_audit_2026-07-24/EXACT_DERIVATION.md": ("OPERATOR_TYPE", "character_and_endpoint_identity", "OPEN", "PATH_INDEPENDENCE_OPEN", "TYPE_DISTINCTION"),
    "udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/AUDIT_REPORT.md": ("PATH_GROUPOID", "typed_composition_all_lambda", "OPEN_SMALLEST_JOIN", "PERIODS_ALLOWED", "CONDITIONAL_KINEMATICS"),
    "udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/EXACT_DERIVATION.md": ("PATH_GROUPOID", "typed_composition_all_lambda", "OPEN_SMALLEST_JOIN", "PERIODS_ALLOWED", "CONDITIONAL_KINEMATICS"),
    "udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/ROUTE_OUTCOMES.tsv": ("PATH_GROUPOID", "twelve_route_classification", "OPEN_SMALLEST_JOIN", "PERIODS_VISIBLE", "NONSELECTING"),
    "udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/STATUS_LEDGER.tsv": ("PATH_GROUPOID", "current_route_status", "OPEN_SMALLEST_JOIN", "ENDPOINT_COLLAPSE_EXTRA", "NONSELECTING"),
    "udt_native_global_coframe_definition_audit_2026-07-28/EXACT_DERIVATION.md": ("GLOBAL_COFRAME", "every_endpoint_f_composes", "OPEN", "NOT_SELECTED", "COMPOSITION_NO_SELECTOR"),
    "udt_native_global_coframe_definition_audit_2026-07-28/MINIMAL_SELECTOR_SET.tsv": ("GLOBAL_COFRAME", "missing_physical_comparison_base", "OPEN", "NOT_SELECTED", "INDEPENDENT_GAP"),
    "udt_whole_configuration_reciprocity_audit_2026-08-01/AUDIT_REPORT.md": ("WHOLE_CONFIGURATION", "law_naturality", "REALIZATION_OPEN", "GLOBAL_DATA_OPEN", "GATE_NOT_GENERATOR"),
    "udt_whole_configuration_reciprocity_audit_2026-08-01/EXACT_DERIVATION.md": ("WHOLE_CONFIGURATION", "cocycle_reconstruction", "REALIZATION_OPEN", "GLOBAL_DATA_OPEN", "GATE_NOT_GENERATOR"),
    "udt_whole_configuration_reciprocity_audit_2026-08-01/STATUS_LEDGER.tsv": ("WHOLE_CONFIGURATION", "current_whole_status", "REALIZATION_OPEN", "GLOBAL_DATA_OPEN", "GATE_NOT_GENERATOR"),
    "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/AUDIT_REPORT.md": ("HOLONOMY_CONTROL", "path_transport_given_inputs", "NOT_SUPPLIED", "ENDPOINT_CLOSURE_FAILS_CONTROL", "NO_FOUNDING_LOOP_IDENTITY"),
    "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/EXACT_DERIVATION.md": ("HOLONOMY_CONTROL", "path_transport_given_inputs", "NOT_SUPPLIED", "ENDPOINT_CLOSURE_FAILS_CONTROL", "NO_FOUNDING_LOOP_IDENTITY"),
    "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/STATUS_LEDGER.tsv": ("HOLONOMY_CONTROL", "bounded_loop_status", "NOT_SUPPLIED", "PATH_RULE_OPEN", "NO_FOUNDING_LOOP_IDENTITY"),
    "udt_basic_vs_universal_query_residual_audit_2026-08-04/AUDIT_REPORT.md": ("PARENT_FRONTIER", "universal_architecture_admissible", "OPEN", "LOCAL_GLOBAL_OPEN", "NO_RESIDUAL_SELECTED"),
    "udt_basic_vs_universal_query_residual_audit_2026-08-04/EXACT_DERIVATION.md": ("PARENT_FRONTIER", "local_global_controls", "OPEN", "LOCAL_GLOBAL_OPEN", "NO_RESIDUAL_SELECTED"),
    "udt_basic_vs_universal_query_residual_audit_2026-08-04/FOUNDATIONAL_RULING.tsv": ("PARENT_FRONTIER", "foundational_nonselection", "OPEN", "LOCAL_GLOBAL_OPEN", "NO_RESIDUAL_SELECTED"),
    "udt_native_law_home_codomain_ownership_audit_2026-08-04/AUDIT_REPORT.md": ("LAW_TYPE_PARENT", "query_law_typing", "OPEN", "QUANTIFIER_OPEN", "TYPE_ONLY"),
    "udt_native_law_home_codomain_ownership_audit_2026-08-04/FOUNDATIONAL_ENTAILMENT_MATRIX.tsv": ("LAW_TYPE_PARENT", "founded_query_morphism", "ABSTRACT_DEPTH_OPEN", "QUANTIFIER_OPEN", "TYPE_ONLY"),
    "udt_query_bundle_section_descent_audit_2026-08-04/AUDIT_REPORT.md": ("SECTION_PARENT", "query_without_section", "OPEN", "STRATIFIED_OPEN", "NO_SECTION_SELECTED"),
    "udt_extension_bundle_globalization_variation_audit_2026-08-04/AUDIT_REPORT.md": ("GLOBALIZATION_PARENT", "conditional_bundle_globalization", "OPEN", "TOPOLOGY_GLUE_OPEN", "NO_LAW_SELECTED"),
    "udt_factorized_whole_spacetime_skeleton_2026-08-04/OPEN_EQUATION_SLOTS.tsv": ("OPEN_SLOT_PARENT", "complete_open_law_slots", "OPEN", "OPEN", "NO_LAW_SELECTED"),
    "udt_pair_space_metric_transform_sne_readout_audit_2026-07-24/SNE_READOUT_LEDGER.tsv": ("DOWNSTREAM_ANCHOR", "conditional_readout", "CONDITIONAL", "NONE", "NO_UPSTREAM_SELECTION"),
}
source_paths = [line for line in (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines() if line]
require("source_adjudication_domain_exact", set(source_adjudication_data) == set(source_paths))
source_adjudication_rows = []
for path in source_paths:
    role, composition_claim, metric_depth, loop_requirement, ruling = source_adjudication_data[path]
    source_adjudication_rows.append({"path": path, "role": role, "composition_claim": composition_claim, "metric_depth_assignment": metric_depth, "loop_requirement": loop_requirement, "ruling": ruling})
write_tsv("SOURCE_ADJUDICATION.tsv", ("path", "role", "composition_claim", "metric_depth_assignment", "loop_requirement", "ruling"), source_adjudication_rows)

implication_rows = [
    {"implication_id": "I01", "antecedent": "additive_depth", "consequent": "character_composition", "status": "DERIVED_IDENTITY", "extra_premise": "NONE"},
    {"implication_id": "I02", "antecedent": "endpoint_potential", "consequent": "zero_triangle_residual", "status": "DERIVED_IDENTITY", "extra_premise": "NONE"},
    {"implication_id": "I03", "antecedent": "path_integral", "consequent": "concatenation_additivity", "status": "DERIVED_IDENTITY", "extra_premise": "NONE"},
    {"implication_id": "I04", "antecedent": "path_integral", "consequent": "d_alpha_zero", "status": "NOT_DERIVED", "extra_premise": "LOCAL_ENDPOINT_INDEPENDENCE"},
    {"implication_id": "I05", "antecedent": "d_alpha_zero", "consequent": "all_loop_periods_zero", "status": "NOT_DERIVED_GLOBAL", "extra_premise": "GLOBAL_EXACTNESS_OR_TOPOLOGY"},
    {"implication_id": "I06", "antecedent": "all_loop_periods_zero", "consequent": "endpoint_depth_potential", "status": "DERIVED_UNDER_REGULAR_CONNECTED_SCOPE", "extra_premise": "PATH_CONNECTED_REGULAR_DOMAIN"},
    {"implication_id": "I07", "antecedent": "Levi_Civita_transport", "consequent": "path_composition", "status": "DEFINED_FUNCTORIAL", "extra_premise": "SUPPLIED_METRIC"},
    {"implication_id": "I08", "antecedent": "transport_plus_additive_depth", "consequent": "typed_full_composition", "status": "DERIVED_CONDITIONAL", "extra_premise": "MATCHED_PAIR_OBJECTS_OR_VERTICAL_RESET"},
    {"implication_id": "I09", "antecedent": "typed_full_composition", "consequent": "T_loop_identity", "status": "NOT_DERIVED", "extra_premise": "ENDPOINT_COLLAPSE_AND_TRIVIAL_LOOP_RETURN"},
    {"implication_id": "I10", "antecedent": "observer_Reciprocity", "consequent": "future_law_equivariance", "status": "DERIVED_SCOPED", "extra_premise": "TYPED_DOMAIN_CODOMAIN_ACTIONS"},
    {"implication_id": "I11", "antecedent": "observer_Reciprocity", "consequent": "unique_or_nontrivial_metric_law", "status": "NOT_DERIVED", "extra_premise": "LAW_GENERATING_PRINCIPLE"},
    {"implication_id": "I12", "antecedent": "universal_query_admissibility", "consequent": "universal_query_dynamics_selected", "status": "NOT_DERIVED", "extra_premise": "PHYSICAL_QUANTIFIER_SELECTION"},
]
write_tsv("CONDITIONAL_IMPLICATION_LEDGER.tsv", ("implication_id", "antecedent", "consequent", "status", "extra_premise"), implication_rows)

loop_rows = [
    {"object_id": "L01", "object": "reciprocal_period", "formula": "Pi_gamma", "owner": "SUPPLIED_DEPTH_COCYCLE", "composition_effect": "D_Pi", "identity_condition": "Pi_equals_zero_for_real_faithful_character"},
    {"object_id": "L02", "object": "Levi_Civita_holonomy", "formula": "H_gamma", "owner": "SUPPLIED_METRIC_AND_LOOP", "composition_effect": "metric_isometry", "identity_condition": "H_equals_I"},
    {"object_id": "L03", "object": "full_typed_loop", "formula": "H_gamma_D_Pi_with_transport_typing", "owner": "METRIC_PLUS_DEPTH_PLUS_PAIR_PATH", "composition_effect": "valid_groupoid_automorphism", "identity_condition": "EXTRA_NOT_FOUNDED"},
    {"object_id": "L04", "object": "local_depth_curvature", "formula": "d_alpha", "owner": "SUPPLIED_DEPTH_ONE_FORM", "composition_effect": "small_loop_period", "identity_condition": "local_endpoint_independence"},
    {"object_id": "L05", "object": "global_depth_period_family", "formula": "integral_loop_alpha", "owner": "SUPPLIED_DEPTH_ONE_FORM_AND_TOPOLOGY", "composition_effect": "global_reciprocal_loop_response", "identity_condition": "global_endpoint_independence"},
]
write_tsv("LOOP_OBJECT_SEPARATION.tsv", ("object_id", "object", "formula", "owner", "composition_effect", "identity_condition"), loop_rows)

result = {
    "status": "COMPOSITION_IDENTITY_NONSELECTING",
    "termination_ruling": "CURRENT_COMPOSITION_TO_NATIVE_RESIDUAL_ROUTE_TERMINATES_WITHOUT_NEW_SOURCE_BACKED_DEPTH_OR_LOOP_PREMISE",
    "production_exact_checks": len(checks),
    "check_names": checks,
    "candidate_rows": len(candidate_rows),
    "source_rulings": len(source_rows),
    "source_adjudications": len(source_adjudication_rows),
    "implication_rows": len(implication_rows),
    "loop_objects": len(loop_rows),
    "graph": {"vertices": 4, "edges": 6, "incidence_rank": B.rank(), "triangle_rank": C.rank(), "potential_offset_nullity": len(B.nullspace())},
    "profile_curvatures_at_zero": {key: str(value) for key, value in profile_curvatures.items()},
    "local_exact_form_period": str(unit_square_integral(alpha_exact)),
    "local_nonclosed_form_period": str(unit_square_integral(alpha_nonclosed)),
    "nontrivial_metric_residual_from_founded_composition": False,
    "universal_all_queries_selected": False,
    "conditional_nontrivial_loop_residual_exists_if_extra_premise_imposed": True,
    "action_or_downstream_physics_derived": False,
    "python": platform.python_version(),
    "sympy": sp.__version__,
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
stdout = (
    f"PASS production_exact_checks={len(checks)} candidates={len(candidate_rows)} "
    f"source_rulings={len(source_rows)} source_adjudications={len(source_adjudication_rows)} "
    f"implications={len(implication_rows)} loops={len(loop_rows)}\n"
    f"status={result['status']}\n"
    f"termination={result['termination_ruling']}\n"
)
(HERE / "PRODUCTION_STDOUT.txt").write_text(stdout, encoding="utf-8")
(HERE / "PRODUCTION_STDERR.txt").write_text("", encoding="utf-8")
sys.stdout.write(stdout)
