#!/usr/bin/env python3
"""Adjudicate preregistered complete-metric observer-separation candidates."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
BASE = "566686f0d05b149792b4e266e78d112830a77579"


GATE_FIELDS = [
    "native_input",
    "observer_domain",
    "event_pairing",
    "nonnegative",
    "pair_exchange",
    "identity",
    "chart_coframe_invariant",
    "angular_path_complete",
    "CSN_representative_honest",
    "causal_scope_honest",
    "global_descent",
    "no_hidden_premise",
]


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def g(
    native: str,
    domain: str,
    pairing: str,
    nonnegative: str,
    exchange: str,
    identity: str,
    invariant: str,
    angular: str,
    csn: str,
    causal: str,
    global_descent: str,
    hidden: str,
) -> dict[str, str]:
    values = [
        native, domain, pairing, nonnegative, exchange, identity,
        invariant, angular, csn, causal, global_descent, hidden,
    ]
    return dict(zip(GATE_FIELDS, values))


OUTCOMES: dict[str, tuple[dict[str, str], str, str]] = {
    "C01": (
        g("PASS", "FAIL", "FAIL", "FAIL", "PASS_LOCAL", "FAIL", "PASS_LOCAL", "FAIL", "CONDITIONAL", "ALL_LOCAL_TANGENTS", "FAIL", "FAIL"),
        "REJECT_AS_OBSERVER_DISTANCE",
        "pointwise_indefinite_bilinear_form_is_not_a_two_point_nonnegative_distance",
    ),
    "C02": (
        g("PASS", "FAIL", "FAIL", "FAIL_SIGNED", "PASS_LOCAL_BRANCH", "FAIL_NULL", "PASS_LOCAL_NORMAL_NEIGHBORHOOD", "CONDITIONAL_GEODESIC", "CONDITIONAL", "EVENT_CAUSAL_TYPES", "FAIL_MULTIGEODESIC_OR_CUT_LOCUS", "FAIL"),
        "CONDITIONAL_EVENT_INTERVAL_NOT_OBSERVER_DISTANCE",
        "world_function_is_local_event_geometry_not_a_nonnegative_paired_worldline_distance",
    ),
    "C03": (
        g("PASS", "FAIL", "FAIL", "PASS", "PASS", "FAIL_NULL", "PASS_LOCAL_NORMAL_NEIGHBORHOOD", "CONDITIONAL_GEODESIC", "CONDITIONAL", "EVENT_CAUSAL_TYPES", "FAIL_MULTIGEODESIC_OR_CUT_LOCUS", "FAIL"),
        "REJECT_AS_PHYSICAL_DISTANCE",
        "absolute_value_still_assigns_zero_to_noncoincident_null_events",
    ),
    "C04": (
        g("PASS", "FAIL", "FAIL", "PASS", "FAIL_DIRECTED", "FAIL_SPACELIKE_ZERO", "PASS_CAUSAL", "FAIL_SPATIAL", "CONDITIONAL", "CAUSAL_ONLY", "CONDITIONAL_GLOBAL_HYPERBOLICITY", "FAIL"),
        "REJECT_AS_SYMMETRIC_OBSERVER_SEPARATION",
        "causal_time_separation_is_directed_and_not_spatial_distance",
    ),
    "C05": (
        g("PASS", "FAIL", "FAIL", "PASS_PER_CURVE", "PASS_REVERSED_CURVE", "PASS_PER_REGULAR_CURVE", "PASS", "FAIL_PATH_CHOICE", "CONDITIONAL", "SPACELIKE_CURVES_ONLY", "OPEN", "FAIL"),
        "CONDITIONAL_PATH_LENGTH_NOT_SELECTED_DISTANCE",
        "same_endpoints_admit_different_spacelike_curve_lengths",
    ),
    "C06": (
        g("PASS", "FAIL_SLICE", "FAIL_SLICE_PAIRING", "PASS_ON_RIEMANNIAN_SLICE", "PASS", "PASS_CONNECTED_SLICE", "PASS", "PASS", "FAIL_REPRESENTATIVE", "SPACELIKE_SLICE_ONLY", "OPEN_COMPLETENESS", "FAIL"),
        "CONDITIONAL_IF_SPATIAL_SLICE_AND_REPRESENTATIVE_SUPPLIED",
        "intrinsic_distance_is_exact_after_unselected_slice_and_scale_choices",
    ),
    "C07": (
        g("PASS", "FAIL_U_SELECTION", "FAIL_RESTSPACE_INTEGRABILITY", "PASS_LOCAL_SCREEN", "PASS", "CONDITIONAL", "PASS", "PASS_LOCAL", "FAIL_REPRESENTATIVE", "TIMELIKE_U_ONLY", "OPEN", "FAIL"),
        "CONDITIONAL_IF_OBSERVER_CONGRUENCE_AND_INTEGRABLE_QUOTIENT_SUPPLIED",
        "metric_does_not_select_u_and_local_rest_spaces_need_not_form_global_slices",
    ),
    "C08": (
        g("PASS", "CONDITIONAL_ALL_FUTURE_TIMELIKE_HISTORIES", "DERIVED_CONDITIONAL_EQUAL_PHI_COMMON_RANGE", "PASS_ON_CONNECTED_LEVEL_SET", "PASS", "PASS_ON_SLICE", "PASS", "PASS_INTRINSIC_SLICE", "CONDITIONAL_H0_VS_HF_AND_PHYSICAL_SCALE", "TIMELIKE_NONNULL_ONLY", "OPEN_NO_COMPLETE_BRANCH", "FAIL_GLOBAL_TEMPORAL_BRANCH_AND_REPRESENTATIVE"),
        "DERIVED_CONDITIONAL_TEMPORAL_PHI_SEPARATION_FAMILY__NOT_UNIVERSAL_PHYSICAL_DG",
        "strongest_native_candidate_preserves_observer_equivalence_but_needs_global_temporal_phi_branch_and_scale",
    ),
    "C09": (
        g("PASS", "FAIL_OBSERVER", "FAIL", "PASS_MAGNITUDE", "PASS", "FAIL_LEVEL_SETS", "PASS_LOCAL", "FAIL_ANGULAR", "CONDITIONAL", "SPACELIKE_NONNULL_ONLY", "OPEN", "FAIL"),
        "CONDITIONAL_ONE_DIMENSIONAL_DEPTH_ONLY",
        "spacelike_gradient_supplies_a_line_not_complete_observer_pair_distance",
    ),
    "C10": (
        g("PASS", "FAIL", "FAIL", "FAIL_DEGENERATE", "CONDITIONAL", "FAIL", "PASS_TENSORIAL_NILPOTENT", "FAIL", "FAIL_H0_DEGENERATE", "NULL_ONLY", "FAIL_INTERFACE", "FAIL"),
        "REJECT_ON_NULL_STRATUM",
        "normalized_projector_and_positive_screen_metric_degenerate",
    ),
    "C11": (
        g("PASS", "FAIL", "FAIL", "FAIL_NO_OBJECT", "FAIL", "FAIL", "FAIL_NO_REDUCTION", "FAIL", "FAIL", "ZERO_DPHI_ONLY", "FAIL", "FAIL"),
        "NO_INTRINSIC_REDUCTION",
        "zero_dphi_selects_no_line_slice_or_pairing",
    ),
    "C12": (
        g("PASS", "FAIL", "FAIL", "PASS_ABSOLUTE_VALUE", "PASS", "FAIL_SAME_LEVEL", "PASS_SCALAR", "FAIL_ANGULAR", "PASS_NEUTRAL", "ALL", "PASS_AS_SCALAR", "FAIL_DISTANCE_INTERPRETATION"),
        "REJECT_AS_COMPLETE_DISTANCE",
        "distinct_angular_or_same_level_points_collapse_to_zero",
    ),
    "C13": (
        g("CONDITIONAL_RECIPROCAL_REALIZATION", "FAIL_GENERAL_OBSERVER_SET", "CONDITIONAL_ORDERED_COMPARISON", "PASS_MAGNITUDE_ONLY", "PASS_AFTER_MAGNITUDE", "FAIL_ANGULAR", "PASS_IN_1D_CLASS", "FAIL_ANGULAR", "PASS_SCALE_WEIGHT_ZERO", "NOT_DPHI_COMPLETE", "OPEN_JOIN", "FAIL_PROJECTIVE_AND_POSITION_JOINS"),
        "RETAIN_UNIQUE_CONDITIONAL_1D_PROJECTIVE_COORDINATE",
        "not_general_metric_distance",
    ),
    "C14": (
        g("CONDITIONAL_WRL", "STATIC_CHART_OBSERVERS_ONLY", "STATIC_T_PAIRING", "PASS_COORDINATE_RANGE", "PASS", "PASS_CHART_POINTS", "FAIL_CHART_LABEL", "FAIL_RADIAL_ONLY", "FAIL_GLOBAL_REPRESENTATIVE", "STATIC_SPACELIKE_DPHI", "FAIL_COMPLETE_FRAME", "FAIL"),
        "REJECT_AS_INVARIANT_COMPLETE_DISTANCE",
        "coordinate_r_is_local_WRL_chart_label",
    ),
    "C15": (
        g("CONDITIONAL_WRL", "STATIC_WRL_CONGRUENCE", "STATIC_T_PAIRING", "PASS_RADIAL_SLICE", "PASS", "PASS_RADIAL_RAY", "PASS_WITHIN_SLICE", "FAIL_ANGULAR_AND_PATH", "CONDITIONAL_REPRESENTATIVE", "STATIC_SPACELIKE_DPHI", "FAIL_COMPLETE_FRAME", "FAIL"),
        "RETAIN_CONDITIONAL_WRL_RADIAL_PROPER_LENGTH",
        "exact_local_radial_length_not_complete_observer_pair_distance",
    ),
    "C16": (
        g("CONDITIONAL_WRL", "STATIC_WRL_CONGRUENCE", "SIGNAL_OR_STATIONARY_T_PAIRING", "PASS", "PASS_RADIAL_CONTROL", "PASS_RADIAL_RAY", "PASS_WITHIN_STATIC_CHART", "FAIL_GENERAL_PATH", "CONDITIONAL_REPRESENTATIVE", "STATIC_SPACELIKE_DPHI", "FAIL_COMPLETE_FRAME", "FAIL_SIGNAL_OR_OPTICAL_ROLE"),
        "RETAIN_CONDITIONAL_OPTICAL_COMPARISON",
        "optical_distance_requires_stationary_threading_and_is_not_native_physical_separation",
    ),
    "C17": (
        g("PASS", "FAIL_OBSERVER_POLARIZATION", "FAIL", "PASS_PER_SPACELIKE_PATH", "PASS_PATH_REVERSE", "PASS_PER_PATH", "PASS_COVARIANT", "CONDITIONAL_FULL_COFRAME", "FAIL_PHYSICAL_REPRESENTATIVE", "PATH_DEPENDENT", "OPEN_HOLONOMY_AND_GLUING", "FAIL_PATH_SELECTION"),
        "CONDITIONAL_COFRAME_PATH_FUNCTIONAL",
        "complete_coframe_supplies_integrands_not_a_selected_path_or_spatial_polarization",
    ),
    "C18": (
        g("PASS_IF_COMPLETE_CELL", "FAIL_SPATIAL_QUOTIENT", "FAIL", "PASS_IF_RIEMANNIAN_QUOTIENT", "PASS", "PASS_IF_CONNECTED", "PASS", "PASS_IF_COMPLETE", "FAIL_REPRESENTATIVE", "COMPLETION_DEPENDENT", "FAIL_NO_SELECTED_COMPLETE_BRANCH", "FAIL"),
        "OPEN_COMPLETE_CELL_DISTANCE",
        "no_selected_complete_on_shell_cell_spatial_metric_or topology",
    ),
    "C19": (
        g("CONDITIONAL_SEAL", "FAIL_OBSERVER", "FAIL", "CONDITIONAL_NORMAL_DISTANCE", "PASS", "CONDITIONAL", "PASS_IF_SURFACE", "FAIL_GENERAL", "FAIL_REPRESENTATIVE", "BOUNDARY_TYPE_DEPENDENT", "FAIL_SEAL_TYPE_OPEN", "FAIL_BOUNDARY_PREMISE"),
        "OPEN_SEAL_DISTANCE",
        "seal_is_not_selected_as_physical_boundary_or observer-pair locus",
    ),
    "C20": (
        g("PASS_ON_FIBER", "FAIL_BASE_OBSERVERS", "FAIL", "PASS_FIBER", "PASS", "PASS_FIBER", "PASS_LATTICE_CHART_QUALIFIED", "PASS_FIBER", "PASS_NORMALIZED_SHAPE", "TORIC_FIBER_ONLY", "CONDITIONAL_TORIC_DESCENT", "FAIL_TYPE_MISMATCH"),
        "TYPE_MISMATCH_FIBER_NOT_OBSERVER_BASE",
        "angular_fiber_distance_does_not_measure_separation_of spacetime observers",
    ),
    "C21": (
        g("PASS_ON_TORIC_FIBER", "FAIL_BASE_OBSERVERS", "FAIL", "PASS_CHARACTER_LENGTH", "PASS_SIGN_CLASS", "FAIL_MULTIPLE_CHARACTERS_TIES", "PASS_SET_VALUED", "PASS_FIBER", "PASS_NORMALIZED_H", "TORIC_ONLY", "CONDITIONAL_MONODROMY", "FAIL_TYPE_MISMATCH"),
        "TYPE_MISMATCH_CHARACTER_LENGTH_NOT_OBSERVER_DISTANCE",
        "dual_systole_is_intrinsic_fiber_character_data",
    ),
    "C22": (
        g("PASS_IF_SIMPLE_TIMELIKE_EIGENLINE", "CONDITIONAL_EIGENLINE_AS_OBSERVER", "FAIL_PAIRING", "CONDITIONAL_SLICE", "PASS", "CONDITIONAL", "PASS", "CONDITIONAL", "FAIL_REPRESENTATIVE", "GENERIC_BRANCH_ONLY", "FAIL_DEGENERACIES_AND_HOLONOMY", "FAIL_PHYSICALITY"),
        "CONDITIONAL_BRANCH_SELECTOR_NOT_UNIVERSAL",
        "registered_curvature_ensemble_has_full_irreducible_or flat ambiguous cases",
    ),
    "C23": (
        g("PASS", "FAIL_OBSERVER_HISTORIES", "CONDITIONAL_EVENT_ORDER", "FAIL_BOOLEAN_ONLY", "PASS_OR_DIRECTED", "FAIL_NULL_EQUIVALENCE", "PASS", "FAIL_MAGNITUDE", "PASS_CONFORMAL", "ALL_CAUSAL", "CONDITIONAL_CAUSAL_COMPLETION", "FAIL_DISTANCE_INFERENCE"),
        "RELATION_NOT_DISTANCE",
        "null_cone_and_causal_accessibility_supply order_or_incidence_not magnitude",
    ),
    "C24": (
        g("PASS_PRINCIPLES", "FAIL_CONSTRUCTION", "FAIL_CONSTRUCTION", "FAIL_CONSTRUCTION", "CONSTRAINS", "FAIL_CONSTRUCTION", "CONSTRAINS", "CONSTRAINS", "CONSTRAINS", "NO_OBJECT", "NO_OBJECT", "FAIL_PROMOTION"),
        "CONSTRAINS_NOT_SELECTS",
        "registered_principles_supply_symmetry_scale_neutrality_completion_and_admissibility_not_Dg",
    ),
}


PRINCIPLES = [
    ("P01", "complete_Lorentzian_metric", "cones_inner_products_path_integrands", "no_preferred_observer_or_spatial_quotient", "CONSTRAINS_NOT_SELECTS"),
    ("P02", "phi_and_dphi", "signed_scalar_and_causal_stratified_line_where_nonnull", "observer_physicality_and_global_causal_type", "CONDITIONAL_GEOMETRIC_REDUCTION"),
    ("P03", "Reciprocity", "pair_exchange_and_reciprocal_character_with_exact_stamps", "observer_domain_pairing_and_distance_magnitude", "CONSTRAINS_NOT_SELECTS"),
    ("P04", "CSN", "conformal_cones_normalized_shapes_h0_and_hf_pre_scale_families", "physical_representative_and_absolute_length", "CONSTRAINS_NOT_SELECTS"),
    ("P05", "finite_cell", "finite_completion_requirement_and_taxonomy", "completion_topology_spatial_slice_and_metric", "CONSTRAINS_NOT_SELECTS"),
    ("P06", "static_seal", "phi_value_parity_and_one_tangent_condition", "observer_pairing_surface_type_and_complete_boundary", "CONSTRAINS_NOT_SELECTS"),
    ("P07", "co_presence", "events_belong_to_one_complete_solution", "simultaneity_event_pairing_or_information_access", "NOT_A_SELECTOR"),
    ("P08", "bootstrap", "after_solution_admissibility_and_future_global_fork", "local_pairing_metric_or_response_operator", "NOT_EXECUTABLE_SELECTOR"),
    ("P09", "angular_coframe_H_S", "full_angular_shape_shift_and_holonomy_data_on_supplied_branch", "spatial_base_slice_observer_section_and_completion", "NECESSARY_NOT_SUFFICIENT"),
    ("P10", "connector_lapse_shift", "exact_distance_and_optical_integrands_after_path_threading", "physical_threading_path_and_global connector", "OPEN_SELECTOR"),
    ("P11", "Xmax_owner_meaning", "target_global_supremum_type", "Dg_definition", "TARGET_NOT_CONSTRUCTOR"),
    ("P12", "c_E_anchor", "local_clock_length_conversion_after calibration", "global_pairing_or_absolute_Xmax", "CALIBRATES_NOT_SELECTS"),
]


CAUSAL_ROWS = [
    {"causal_class": "TIMELIKE_NONNULL", "dphi_object": "temporal_function_and_spacelike_kernel", "h0_status": "NONDEGENERATE_LORENTZIAN", "candidate_distance": "intrinsic_Riemannian_distance_between_equal_phi_events", "observer_status": "ALL_FUTURE_TIMELIKE_HISTORIES_WITH_COMMON_PHI_RANGE", "global_status": "OPEN_COMPLETE_TEMPORAL_BRANCH"},
    {"causal_class": "SPACELIKE_NONNULL", "dphi_object": "spacelike_line_and_Lorentzian_kernel", "h0_status": "NONDEGENERATE_LORENTZIAN", "candidate_distance": "no_positive_three_space_on_phi_level", "observer_status": "NO_OBSERVER_LINE_FROM_DPHI", "global_status": "OPEN_OTHER_CONSTRUCTION"},
    {"causal_class": "NULL_NONNULL", "dphi_object": "rank1_nilpotent", "h0_status": "DEGENERATE", "candidate_distance": "normalized_slice_metric_undefined", "observer_status": "NO_UNIT_TIMELIKE_LINE", "global_status": "BLOCKS_C08_EXTENSION"},
    {"causal_class": "ZERO_DPHI", "dphi_object": "no_line_or_split", "h0_status": "ZERO", "candidate_distance": "no_dphi_selected_distance", "observer_status": "NO_SELECTION", "global_status": "BLOCKS_C08_EXTENSION"},
    {"causal_class": "TYPE_CHANGING", "dphi_object": "must_cross_null_or_zero", "h0_status": "SINGULAR_AT_INTERFACE", "candidate_distance": "piecewise_only_without_interface_rule", "observer_status": "NO_GLOBAL_CONGRUENCE_DERIVED", "global_status": "OPEN_INTERFACE_SELECTOR"},
]


COMPLETION_ROWS = [
    ("FC01_BOUNDARY_BOUNDARY", "allows_nonnull_submersion_but_does_not_force_profile", "OPEN"),
    ("FC02_ONE_CAP_BOUNDARY", "static_orbit_depth_cap_forces_criticality_time_live_open", "OPEN"),
    ("FC03_TWO_CAP_P0", "compact_static_real_phi_forces_zero_dphi_time_live_open", "OPEN"),
    ("FC04_TWO_CAP_P1", "compact_static_real_phi_forces_zero_dphi_time_live_open", "OPEN"),
    ("FC05_TWO_CAP_P_GT1", "compact_static_real_phi_forces_zero_dphi_time_live_open", "OPEN"),
    ("FC06_NONPRIMITIVE_CAP", "singular_stratum_blocks_global_metric_construction", "BLOCKED_REGULAR_COMPLEMENT_ONLY"),
    ("FC07_PERIODIC_TORUS_BUNDLE", "periodic_static_real_phi_forces_critical_point_time_live_open", "OPEN"),
    ("FC08_MIRROR_DOUBLE", "parity_or_sign_twist_requires_unsupplied_seam_lift", "OPEN"),
    ("FC09_NONORIENTABLE_GLUE", "line_may_descend_but_time_orientation_and_slice_glue_unproved", "OPEN"),
    ("FC10_STRATIFIED_PROJECTOR", "other_projector_strata_do_not_select_dphi_strata", "OPEN"),
    ("FC11_NONINTEGRABLE_DISTRIBUTION", "kernel_dphi_is_integrable_but_no_complete_metric_or observer quotient", "OPEN"),
    ("FC12_RECIPROCAL_TORIC_DIAGONAL", "open_nonnull_control_without_complete_endpoints", "CONDITIONAL_LOCAL_ONLY"),
]


def source_role(path: str) -> tuple[str, str]:
    if "xmax_observer_separation" in path:
        return "CONTROLLING_TYPE_CORRECTION", "supremum_schema_and_open_Dg"
    if "metric_pure_frame" in path or "frame_bivector" in path:
        return "LOCAL_OBSERVER_GEOMETRY", "no_universal_u_local_gamma_only"
    if "dphi" in path or "cartan_transport" in path or "intrinsic_object" in path:
        return "DPHI_CAUSAL_GEOMETRY", "nonnull_local_reduction_null_zero_obstruction"
    if "phi_metric_ontology" in path:
        return "PHI_ONTOLOGY", "phi_not_distance_and_metric_ownership_open"
    if "solution_space_map" in path or "global_metric_assembly" in path or "finite_cell_completion" in path:
        return "COMPLETE_SPACE_AND_COMPLETION", "all_branches_visible_none_selected"
    if "complete_connector" in path or "clock_anchor" in path:
        return "CONNECTOR_AND_THREADING", "path_lapse_shift_observer_threading_open"
    if "observer_centered" in path or "projective_position" in path:
        return "RELATIONAL_CORRECTION", "local_depth_not_complete_distance"
    if "three_reciprocity" in path:
        return "RECIPROCITY_SCOPE", "symmetry_and_conditional_1D_group_not_Dg"
    if "global_reciprocal" in path or "pre_p06" in path or "seal_boundary" in path:
        return "PRINCIPLE_AND_BOUNDARY_SCOPE", "principles_constrain_without_complete_selector"
    if "dual_systole" in path:
        return "ANGULAR_FIBER_GEOMETRY", "fiber_character_data_not_base_observer_distance"
    if "bootstrap_substrate" in path:
        return "BOOTSTRAP_SCOPE", "global_channels_exist_pairing_operator_absent"
    raise AssertionError(f"unclassified source: {path}")


def main() -> None:
    candidates = read_tsv("CANDIDATE_LEDGER.tsv")
    if len(candidates) != 24 or set(OUTCOMES) != {
        row["candidate_id"] for row in candidates
    }:
        raise AssertionError("candidate universe mismatch")
    gate_rows = []
    outcome_rows = []
    for row in candidates:
        candidate_id = row["candidate_id"]
        gates, outcome, reason = OUTCOMES[candidate_id]
        gate_rows.append(
            {"candidate_id": candidate_id, "candidate": row["candidate"], **gates}
        )
        outcome_rows.append(
            {
                "candidate_id": candidate_id,
                "candidate": row["candidate"],
                "final_ruling": outcome,
                "load_bearing_reason": reason,
                "universal_pass": "NO",
            }
        )
    write_tsv(
        "CANDIDATE_GATE_MATRIX.tsv",
        ["candidate_id", "candidate", *GATE_FIELDS],
        gate_rows,
    )
    write_tsv(
        "CANDIDATE_OUTCOMES.tsv",
        ["candidate_id", "candidate", "final_ruling", "load_bearing_reason", "universal_pass"],
        outcome_rows,
    )
    write_tsv(
        "PRINCIPLE_CAPABILITY_MATRIX.tsv",
        ["principle_id", "structure", "supplies", "does_not_supply", "ruling"],
        [
            {
                "principle_id": row[0],
                "structure": row[1],
                "supplies": row[2],
                "does_not_supply": row[3],
                "ruling": row[4],
            }
            for row in PRINCIPLES
        ],
    )
    write_tsv(
        "DPHI_CAUSAL_DISTANCE_ATLAS.tsv",
        ["causal_class", "dphi_object", "h0_status", "candidate_distance", "observer_status", "global_status"],
        CAUSAL_ROWS,
    )
    write_tsv(
        "COMPLETION_DESCENT_ATLAS.tsv",
        ["completion", "C08_timelike_dphi_constraint", "descent_ruling"],
        [
            {
                "completion": row[0],
                "C08_timelike_dphi_constraint": row[1],
                "descent_ruling": row[2],
            }
            for row in COMPLETION_ROWS
        ],
    )

    manifest = read_tsv("SOURCE_MANIFEST.tsv")
    if len(manifest) != 50 or len({row["path"] for row in manifest}) != 50:
        raise AssertionError("source manifest mismatch")
    source_rows = []
    for row in manifest:
        role, ruling = source_role(row["path"])
        source_rows.append(
            {
                "source_id": row["source_id"],
                "path": row["path"],
                "role": role,
                "audit_use": ruling,
                "base_git_blob": row["git_blob"],
                "base_sha256": row["sha256"],
            }
        )
    write_tsv(
        "SOURCE_ADJUDICATION.tsv",
        ["source_id", "path", "role", "audit_use", "base_git_blob", "base_sha256"],
        source_rows,
    )

    # Exact local controls.
    beta, L, lam, phi0, omega = sp.symbols(
        "beta L lambda phi0 Omega", real=True, positive=True
    )
    eta = sp.diag(-1, 1, 1, 1)
    alpha_t = sp.Matrix([1, 0, 0, 0])
    alpha_x = sp.Matrix([0, 1, 0, 0])
    alpha_null = sp.Matrix([1, -1, 0, 0])
    eta_inv = eta.inv()
    s_t = (alpha_t.T * eta_inv * alpha_t)[0]
    s_x = (alpha_x.T * eta_inv * alpha_x)[0]
    s_null = (alpha_null.T * eta_inv * alpha_null)[0]
    h0_t = abs(int(s_t)) * eta
    n_t = h0_t.inv() * alpha_t
    q_t = h0_t + alpha_t * alpha_t.T
    boosted_slice_distance = sp.simplify(L * sp.sqrt(1 - beta**2))
    h_family_scale = sp.exp(lam * phi0**2)
    null_interval = (
        sp.Matrix([1, 1, 0, 0]).T
        * eta
        * sp.Matrix([1, 1, 0, 0])
    )[0]
    same_phi_difference = sp.Integer(0)
    angular_chord = sp.simplify(
        2 * L * sp.sin(sp.Symbol("theta", positive=True) / 2)
    )
    csn_length_ratio = sp.simplify((omega * L) / (omega * sp.Symbol("X", positive=True)))

    exact = {
        "Minkowski_signature": [-1, 1, 1, 1],
        "timelike_dphi_s": str(s_t),
        "spacelike_dphi_s": str(s_x),
        "null_dphi_s": str(s_null),
        "timelike_h0": str(h0_t.tolist()),
        "timelike_n": str(n_t.T.tolist()),
        "timelike_n_phi": str((alpha_t.T * n_t)[0]),
        "timelike_slice_q": str(q_t.tolist()),
        "noncoincident_null_interval": str(null_interval),
        "lab_slice_distance": str(L),
        "boosted_pairing_slice_distance": str(boosted_slice_distance),
        "beta_3_over_5_distance_ratio": str(
            sp.simplify(boosted_slice_distance.subs(beta, sp.Rational(3, 5)) / L)
        ),
        "h_f_slice_distance_scale": str(h_family_scale),
        "same_phi_distinct_point_difference": str(same_phi_difference),
        "same_radius_angular_chord": str(angular_chord),
        "constant_CSN_distance_fraction": str(csn_length_ratio),
        "straight_vs_L_path_lengths": ["sqrt(2)", "2"],
    }

    results = {
        "schema": "udt-two-observer-separation-selector-audit-v1",
        "base": BASE,
        "candidate_count": len(candidates),
        "source_count": len(manifest),
        "principle_count": len(PRINCIPLES),
        "causal_class_count": len(CAUSAL_ROWS),
        "completion_count": len(COMPLETION_ROWS),
        "universal_candidate_count": sum(
            row["universal_pass"] == "YES" for row in outcome_rows
        ),
        "strongest_candidate": {
            "candidate_id": "C08",
            "ruling": OUTCOMES["C08"][1],
            "derived_geometry": (
                "on_timelike_nonnull_dphi_regions_phi_is_temporal_equal_phi_"
                "pairs_future_observer_histories_and_level_sets_are_Riemannian"
            ),
            "open_physics": (
                "global_temporal_phi_branch_common_range_physical_representative_"
                "hf_selection_null_zero_interface_and_complete_global_descent"
            ),
        },
        "exact_controls": exact,
        "maximum_ruling": "OPEN_SELECTOR",
        "scoped_no_go": (
            "NO_REGISTERED_CANDIDATE_DEFINES_ONE_UNIVERSAL_PHYSICAL_TWO_OBSERVER_"
            "SEPARATION_ACROSS_ALL_CAUSAL_AND_COMPLETION_CLASSES"
        ),
        "smallest_missing_object": (
            "native selection of a complete globally temporal phi branch with "
            "physical spatial representative, or an equivalent threading and "
            "pairing rule on the other causal branches"
        ),
        "downstream": {
            "global_diameter": "NOT_EVALUATED_GATE_NOT_PASSED",
            "WRL_X_to_global_Xmax_join": "NOT_EVALUATED_GATE_NOT_PASSED",
            "numerical_Xmax": "OPEN_UNCHANGED",
            "action_source_boundary_mass": "OPEN_UNCHANGED",
        },
        "authority_boundary": {
            "external_mechanics_imported": False,
            "topology_selected": False,
            "physical_observer_selected": False,
            "physical_representative_selected": False,
            "signal_law_adopted": False,
            "matter_or_time_live_solve": False,
            "gpu_used": False,
            "canon_changed": False,
            "historical_or_frozen_changed": False,
        },
        "source_identity_sha256": hashlib.sha256(
            "\n".join(row["path"] for row in manifest).encode()
        ).hexdigest(),
    }
    (HERE / "RESULTS.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
