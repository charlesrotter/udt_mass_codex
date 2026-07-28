#!/usr/bin/env python3
"""Build the fixed-base general-screen dependency regrade.

This script reads scientific sources only from the preregistered Git tree.  It does not
read their working-tree counterparts and it never edits a historical package.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from collections import Counter
from pathlib import Path


BASE = "e098338b2a24cc85796ea8ab651378925b825dfb"
ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent


SOURCE_SPECS = {
    "udt_complete_screen_response_branch_atlas_2026-07-28/STATUS_LEDGER.tsv": ("claim_id", "claim", "status"),
    "udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv": ("claim_id", "claim", "status"),
    "udt_metric_natural_joint_selector_nogo_2026-07-28/STATUS_LEDGER.tsv": ("object", "object", "status"),
    "udt_joint_selector_provenance_audit_2026-07-28/STATUS_LEDGER.tsv": ("object", "object", "status"),
    "udt_native_global_coframe_definition_audit_2026-07-28/STATUS_LEDGER.tsv": ("status_id", "object", "status"),
    "udt_global_functional_dof_constraint_rank_audit_2026-07-26/STATUS_LEDGER.tsv": ("id", "object", "status"),
    "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/STATUS_LEDGER.tsv": ("object", "object", "status"),
    "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/STATUS_LEDGER.tsv": ("claim", "claim", "status"),
    "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/STATUS_LEDGER.tsv": ("status_id", "object", "status"),
    "udt_bootstrap_clock_angular_closure_audit_2026-07-24/STATUS_LEDGER.tsv": ("id", "object", "status"),
    "udt_intrinsic_clock_transverse_solder_audit_2026-07-24/STATUS_LEDGER.tsv": ("claim", "claim", "status"),
    "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv": ("claim_id", "object", "status"),
    "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv": ("claim_id", "object", "status"),
    "matter_bootstrap_dimensional_inventory_2026-07-20/STATUS_LEDGER.tsv": ("id", "question", "status"),
    "scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv": ("id", "claim", "status"),
    "udt_observer_pair_clock_operator_audit_2026-07-24/STATUS_LEDGER.tsv": ("claim", "claim", "status"),
    "udt_common_scale_neutrality_provenance_audit_2026-07-24/STATUS_LEDGER.tsv": ("id", "object", "current_audit_status"),
    "udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv": ("id", "object", "status"),
    "udt_xmax_observer_separation_audit_2026-07-24/STATUS_LEDGER.tsv": ("claim_id", "claim", "status"),
    "udt_historical_angular_method_salvage_audit_2026-07-28/STATUS_LEDGER.tsv": ("item", "item", "status"),
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": ("id", "object", "status"),
    "CURRENT_SCIENTIFIC_PREMISES.tsv": ("premise_id", "term", "current_status"),
}

TOP_CURRENT_SOURCE_PATHS = {
    "LIVE.md",
    "HANDOFF.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_general_screen_complete_cell_atlas_2026-07-28/AUDIT_REPORT.md",
    "udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv",
    "udt_complete_screen_response_branch_atlas_2026-07-28/AUDIT_REPORT.md",
    "udt_complete_screen_response_branch_atlas_2026-07-28/STATUS_LEDGER.tsv",
}

# These are explicit later-owner routes for high-risk historical lineages. They are not content
# rewrites: the historical package retains its scope, while current effective status is read from
# the named later owner.
NAMED_LATER_OWNER_ROUTES = {
    "udt_post_july_offshell_response_availability_audit_2026-07-25": "udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv:S13-S14",
    "udt_bootstrap_to_local_response_map_audit_2026-07-25": "udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv:S12-S15",
    "udt_complete_relational_configuration_variation_domain_audit_2026-07-26": "udt_global_functional_dof_constraint_rank_audit_2026-07-26/STATUS_LEDGER.tsv:S09-S15",
    "udt_finite_cell_reciprocal_quotient_reduction_audit_2026-07-27": "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/STATUS_LEDGER.tsv:S11-S13",
    "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27": "udt_native_global_coframe_definition_audit_2026-07-28/STATUS_LEDGER.tsv:S04-S12",
    "udt_complete_physical_comparison_map_audit_2026-07-27": "udt_joint_selector_provenance_audit_2026-07-28/STATUS_LEDGER.tsv:stationary_hybrid_comparison-overall",
    "udt_native_reciprocal_comparison_bundle_audit_2026-07-27": "udt_metric_natural_joint_selector_nogo_2026-07-28/STATUS_LEDGER.tsv:reducible_comparison_groupoid-overall",
    "udt_intrinsic_pair_lambda_component_atlas_2026-07-27": "udt_native_global_coframe_definition_audit_2026-07-28/STATUS_LEDGER.tsv:S03-S08",
    "udt_reduced_holonomy_condition_audit_2026-07-27": "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/STATUS_LEDGER.tsv",
    "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27": "udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv:S07-S09",
    "udt_twisted_s3_killing_algebra_audit_2026-07-27": "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/STATUS_LEDGER.tsv",
    "udt_nonlinear_cartan_bianchi_ensemble_atlas_2026-07-26": "udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv:S06-S08",
    "udt_metric_natural_complete_extension_selector_audit_2026-07-27": "udt_metric_natural_joint_selector_nogo_2026-07-28/STATUS_LEDGER.tsv",
    "udt_metric_native_selector_rank_closure_audit_2026-07-27": "udt_global_functional_dof_constraint_rank_audit_2026-07-26/STATUS_LEDGER.tsv",
    "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27": "udt_joint_selector_provenance_audit_2026-07-28/STATUS_LEDGER.tsv",
    "udt_finite_reciprocal_quotient_lift_audit_2026-07-27": "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/STATUS_LEDGER.tsv",
    "udt_founded_pair_first_jet_one_form_atlas_2026-07-26": "udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv:S06",
    "udt_founded_pair_global_alignment_audit_2026-07-26": "udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv:S07-S08",
    "metric_cartan_holonomy_audit_2026-07-19": "udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv:S06-S08",
    "projective_transport_section_selector_2026-07-19": "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv:T02-T18",
    "transverse_reciprocal_realization_selector_2026-07-19": "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv:N02-N22",
    "reciprocal_metric_null_line_selector_2026-07-19": "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv:N03-N06",
    "udt_reciprocal_plane_projector_audit_2026-07-21": "udt_metric_natural_joint_selector_nogo_2026-07-28/STATUS_LEDGER.tsv",
    "udt_coframe_hopf_bridge_audit_2026-07-23": "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv:N17-N22",
    "udt_hopf_realization_deformation_audit_2026-07-23": "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv:T06-T18",
    "udt_hopf_transport_bootstrap_dependency_audit_2026-07-23": "udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv:S06-S14",
    "udt_bootstrap_substrate_micro_closure_audit_2026-07-23": "udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv:S10-S19",
    "udt_pre_density_substrate_response_atlas_2026-07-24": "udt_bootstrap_clock_angular_closure_audit_2026-07-24/STATUS_LEDGER.tsv:S16-S25",
    "xmax_accelerating_finite_cell_cartan_2026-07-19": "udt_xmax_observer_separation_audit_2026-07-24/STATUS_LEDGER.tsv",
    "xmax_full_frame_realization_2026-07-19": "udt_xmax_observer_separation_audit_2026-07-24/STATUS_LEDGER.tsv",
}

C2_PREFIXES = (
    "c2_", "angular_derivative_weight_selector_", "bootstrap_csn_phi_angular_selector_",
    "finite_cell_seal_boundary_phase_join_", "complete_coframe_seal_involution_",
)

EXPLICIT_HISTORICAL_ROUTES: dict[str, str] = {}


def route_many(names: str, owner: str) -> None:
    for name in names.split():
        if name in EXPLICIT_HISTORICAL_ROUTES or name in NAMED_LATER_OWNER_ROUTES:
            raise RuntimeError(f"duplicate family route {name}")
        EXPLICIT_HISTORICAL_ROUTES[name] = owner


route_many("""
grok rescued_workspaces verifier_evidence_2026-07-14 w_alg_verifier_scripts
""", "LIVE.md;CURRENT_SCIENTIFIC_PREMISES.tsv")

route_many("""
copresence_causal_accessibility_selector_2026-07-19 copresence_gr_constraint_regrade_2026-07-19
infinite_c_reciprocity_adjudication_2026-07-18 invariant_reciprocal_causal_flow_2026-07-18
reciprocal_line_realization_selector_2026-07-18 udt_foundational_semantic_regression_correction_2026-07-26
udt_founding_observer_comparison_semantics_audit_2026-07-27 udt_founding_reciprocity_object_audit_2026-07-27
udt_frame_bivector_equivariance_audit_2026-07-23 udt_metric_pure_frame_rederivation_2026-07-23
udt_observer_depth_angle_transition_audit_2026-07-24 udt_observer_longitudinal_transverse_cocycle_audit_2026-07-24
udt_phi_metric_ontology_audit_2026-07-22 udt_premise_reset_audit_2026-07-19
udt_reciprocal_c_metric_meaning_audit_2026-07-22 udt_reciprocal_pair_global_module_audit_2026-07-24
udt_reciprocal_subbundle_ownership_audit_2026-07-22 udt_reciprocity_regime_angular_center_audit_2026-07-22
udt_three_reciprocity_delta_k_audit_2026-07-23 udt_two_frame_regime_metric_limit_audit_2026-07-22
""", "CURRENT_SCIENTIFIC_PREMISES.tsv:G01-G08;udt_native_global_coframe_definition_audit_2026-07-28/STATUS_LEDGER.tsv;udt_metric_natural_joint_selector_nogo_2026-07-28/STATUS_LEDGER.tsv")

route_many("""
udt_calibrated_reciprocal_readout_descent_audit_2026-07-26 udt_cleanroom_metric_reduction_readiness_audit_2026-07-27
udt_clock_ruler_soldering_selector_audit_2026-07-20 udt_complete_branch_founded_pair_pullback_audit_2026-07-26
udt_complete_coframe_metric_telescope_p01_2026-07-27 udt_complete_coframe_native_selector_audit_2026-07-26
udt_complete_connector_assembly_audit_2026-07-22 udt_complete_lift_mu_closure_audit_2026-07-20
udt_covariant_reciprocal_coframe_lift_atlas_2026-07-26 udt_csn_dphi_transport_selector_audit_2026-07-23
udt_global_reciprocal_closure_audit_2026-07-20 udt_global_reciprocal_persistence_selector_audit_2026-07-23
udt_local_selector_holonomy_closure_2026-07-22 udt_metric_native_signed_depth_availability_audit_2026-07-26
udt_metric_native_two_pair_selector_audit_2026-07-21 udt_native_coframe_composition_law_audit_2026-07-23
udt_observer_pair_path_groupoid_assembly_audit_2026-07-26 udt_observer_pair_triangle_consistency_audit_2026-07-26
udt_reciprocal_seam_descent_audit_2026-07-23 udt_reciprocal_transport_holonomy_atlas_2026-07-26
udt_reciprocal_transport_naturality_selector_audit_2026-07-23
""", "udt_joint_selector_provenance_audit_2026-07-28/STATUS_LEDGER.tsv;udt_metric_natural_joint_selector_nogo_2026-07-28/STATUS_LEDGER.tsv;udt_global_reciprocal_bundle_assembly_audit_2026-07-26/STATUS_LEDGER.tsv")

route_many("""
udt_amplitude_volume_metric_atlas_2026-07-21 udt_angular_generator_branch_census_2026-07-23
udt_canonical_geometry_evaluator_p01_2026-07-21 udt_chart_coframe_invariance_atlas_2026-07-21
udt_complete_metric_intrinsic_object_audit_2026-07-23 udt_complete_metric_realization_zoomout_2026-07-23
udt_complete_metric_solution_space_map_2026-07-21 udt_completion_scoped_realized_observable_map_2026-07-26
udt_configuration_space_adjacency_atlas_2026-07-22 udt_constructive_metric_family_atlas_2026-07-21
udt_finite_cell_cartan_transport_atlas_2026-07-23 udt_finite_cell_completion_atlas_2026-07-21
udt_finite_cell_transnormal_asymptote_branch_audit_2026-07-24 udt_founded_constraint_atlas_p03_2026-07-21
udt_full_local_jet_strata_p02_2026-07-27 udt_global_metric_assembly_atlas_2026-07-22
udt_independent_amplitude_metric_atlas_2026-07-21 udt_instrument_motif_atlas_2026-07-21
udt_intrinsic_optical_transport_atlas_2026-07-27 udt_intrinsic_pair_deformation_neighborhood_audit_2026-07-27
udt_joint_invariant_subspace_atlas_2026-07-21 udt_local_jet_atlas_p02_2026-07-21
udt_metric_to_frontier_reference_2026-07-22 udt_relative_angular_area_shape_selector_audit_2026-07-23
udt_structural_ensemble_metric_atlas_2026-07-21
""", "udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv;udt_global_functional_dof_constraint_rank_audit_2026-07-26/STATUS_LEDGER.tsv")

route_many("""
udt_angular_bulk_jacobi_selector_audit_2026-07-23 udt_dual_systole_global_transport_audit_2026-07-24
udt_dual_systole_wall_crossing_selector_audit_2026-07-24 udt_motif_hopf_correspondence_audit_2026-07-22
udt_reciprocal_angular_intertwiner_audit_2026-07-23
""", "CURRENT_SCIENTIFIC_PREMISES.tsv:G09-G13-G15;null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv;angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv")

route_many("""
bootstrap_variation_selector_2026-07-18 boundary_bootstrap_representative_selector_audit_2026-07-19
udt_finite_cell_reciprocal_survival_density_audit_2026-07-23 udt_metric_native_nontriviality_connector_audit_2026-07-25
udt_metric_orchestra_rehearsal_2026-07-25 udt_native_global_observable_closure_census_2026-07-26
udt_relational_metric_fixed_point_typing_audit_2026-07-26 udt_scientific_consolidation_checkpoint_2026-07-23
""", "CURRENT_SCIENTIFIC_PREMISES.tsv:G12-G16;udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv;udt_bootstrap_clock_angular_closure_audit_2026-07-24/STATUS_LEDGER.tsv")

route_many("""
asymptotic_boundary_lineage_audit_2026-07-19 gr_constraint_paired_trial_2026-07-18
native_action_sync_audit_2026-07-17 native_boundary_generator_scale_audit_2026-07-19
reciprocity_offshell_constraint_selector_2026-07-18 rung2_weld_postjuly_regrade_2026-07-19
udt_complete_seal_fixed_set_selector_audit_2026-07-21 udt_free_global_seal_transversality_audit_2026-07-21
udt_full_equation_variation_p05_2026-07-21 udt_gr_subtraction_reciprocal_connection_audit_2026-07-21
udt_pre_p06_boundary_selector_audit_2026-07-21 udt_time_live_characteristic_flux_audit_2026-07-21
udt_timelive_spherical_areal_polarization_audit_2026-07-22
""", "CURRENT_SCIENTIFIC_PREMISES.tsv:G10-G11-G16;native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv")

route_many("""
udt_center_free_observer_optical_correspondence_audit_2026-07-24 udt_clock_anchor_scale_threading_audit_2026-07-22
udt_cmb_polarization_observable_typing_audit_2026-07-27 udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23
udt_metric_native_observer_separation_asymptote_audit_2026-07-24 udt_observer_centered_xmax_frame_correction_2026-07-23
udt_observer_pair_xmax_bridge_audit_2026-07-27 udt_two_observer_separation_selector_audit_2026-07-24
udt_wrl_xmax_lightcone_frame_audit_2026-07-23 udt_xmax_dilation_asymptote_correction_2026-07-23
""", "CURRENT_SCIENTIFIC_PREMISES.tsv:G06-G14;udt_xmax_observer_separation_audit_2026-07-24/STATUS_LEDGER.tsv;udt_common_scale_neutrality_provenance_audit_2026-07-24/STATUS_LEDGER.tsv:S22")

route_many("""
udt_historical_phi_equation_salvage_audit_2026-07-24
""", "CURRENT_SCIENTIFIC_PREMISES.tsv:G01-G03;udt_founded_phi_complete_coframe_extension_audit_2026-07-25/AUDIT_REPORT.md")


# key -> dependency, ruling, optional effective status, explanation, rerun priority
OVERRIDES = {}


def add(path: str, ids: str | list[str], dep: str, ruling: str, explanation: str,
        priority: str = "NONE", effective: str = "") -> None:
    items = ids if isinstance(ids, list) else ids.split()
    for item in items:
        key = (path, item)
        if key in OVERRIDES:
            raise RuntimeError(f"duplicate decision {key}")
        OVERRIDES[key] = (dep, ruling, effective, explanation, priority)


def unchanged(path: str, ids: str | list[str], explanation: str) -> None:
    add(path, ids, "D0_NONE", "UNAFFECTED_LOGICALLY_INDEPENDENT", explanation)


P = "udt_complete_screen_response_branch_atlas_2026-07-28/STATUS_LEDGER.tsv"
add(P, "S03 S04 S05", "D1_EQUAL_WEIGHT_OR_LAMBDA_ONLY", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "Exact only in the registered homogeneous or equal-screen response family; it is not the full GL2 screen response.")
add(P, "S06", "D4_PARALLEL_PAIR_SCREEN", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER",
    "The old twisted-contact S3 mixing theorem survives and is strengthened by the all-invertible-P block-family Cartan/Frobenius obstruction.")
add(P, "S08", "D3_SHEAR_ZERO_PROMOTION", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The 30 zero-shear rows remain exact observations in the frozen branch census and cannot be extrapolated beyond it.")
add(P, "S09", "D1_EQUAL_WEIGHT_OR_LAMBDA_ONLY", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The general-screen result independently confirms this was an ansatz freeze, not a metric no-go.")
add(P, "S10", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SUPERSEDED_BY_GENERAL_SCREEN_RESULT",
    "A smooth general screen on the chosen S3 control exposes both regular shear tangents, not only one counterfactual axis.",
    effective="DERIVED_TWO_SHEAR_TANGENTS_IN_GENERAL_SCREEN_CONFIGURATION_FAMILY")
add(P, "S11", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SUPERSEDED_BY_GENERAL_SCREEN_RESULT",
    "The general GL2 screen is now constructed on the chosen stationary complete S3 control; other completions, selection, off-blocks and time dependence remain open.",
    effective="DERIVED_ON_CHOSEN_STATIONARY_S3__GENERAL_METRIC_AND_PHYSICAL_SELECTION_OPEN")

P = "udt_metric_natural_joint_selector_nogo_2026-07-28/STATUS_LEDGER.tsv"
add(P, "observer_line_extension ruler_line_extension ordered_pair_extension", "D1_EQUAL_WEIGHT_OR_LAMBDA_ONLY",
    "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The lambda lift is exact in the stated reduced SO2/self-adjoint isotropic-screen class; it is not the complete transverse metric response.")
add(P, "comparison_versus_realization_ownership overall", "D6_MULTIPLE", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER",
    "The full screen adds independent shear data, so the failure to select one complete realization is stronger while the bounded Lorentz no-go remains unchanged.")
add(P, "full_holonomy_endpoint_lift", "D1_EQUAL_WEIGHT_OR_LAMBDA_ONLY",
    "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The obstruction is exact for the registered tested lambda strata and is not a full-GL2 endpoint-holonomy classification.")

P = "udt_joint_selector_provenance_audit_2026-07-28/STATUS_LEDGER.tsv"
add(P, "affine_complete_response", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The seven-parameter triangular tangent family remains exact; the new finite general-screen configuration realizes part of its angular sector.")
add(P, "diagonal_full_frame_extension complete_nonultrastatic_RxS3", "D1_EQUAL_WEIGHT_OR_LAMBDA_ONLY",
    "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The real-lambda complete family survives as an isotropic-screen subfamily, not as the complete GL2 screen family.")
add(P, "joint_operation overall", "D6_MULTIPLE", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER",
    "Zero registered candidates still pass the frozen obligations; newly exposed screen freedom supplies configurations, not a selector or joint operation.")

P = "udt_native_global_coframe_definition_audit_2026-07-28/STATUS_LEDGER.tsv"
add(P, "S03 S04", "D1_EQUAL_WEIGHT_OR_LAMBDA_ONLY", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The lambda and complete RxS3 constructions remain exact isotropic-screen subfamilies.")
add(P, "S08", "D6_MULTIPLE", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "General transverse screen configurations and their stationary first jet are now mapped on one S3 control; physical selection, direct pair-screen mixing and time dependence remain open.",
    effective="GENERAL_SCREEN_CONFIGURATION_MAPPED__SELECTOR_OFFBLOCKS_AND_TIME_DEPENDENCE_OPEN")
add(P, "S15", "D6_MULTIPLE", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "One availability gap has narrowed, but the physical comparison, selected finite lift, descent, global completion and realized equations remain open.")

P = "udt_global_functional_dof_constraint_rank_audit_2026-07-26/STATUS_LEDGER.tsv"
add(P, "S04 S07", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "A three-mode screen metric configuration is now explicit on one S3 branch; unique physical extension and projector ownership remain open.")
add(P, "S09", "D6_MULTIPLE", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "Distinguish availability from selection: the general screen has three metric modes, but founded phi alone selects none of them.",
    effective="ZERO_SELECTED_NATIVE_SCREEN_RESPONSE_RANK__THREE_AVAILABLE_SCREEN_METRIC_MODES")
add(P, "S13 S15", "D6_MULTIPLE", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The smallest missing object is now a selected complete extension/variation law, not bare existence of screen response modes.")

P = "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/STATUS_LEDGER.tsv"
add(P, "local_screen_area_response raw_local_screen_area_as_WRL_optical_area lambda_minus_two_SNe_relation",
    "D1_EQUAL_WEIGHT_OR_LAMBDA_ONLY", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "These are exact trace/equal-screen statements only; the physical SNe readout itself is unchanged.")
add(P, "intrinsic_ruler_null_congruence clock_angular_connection_mixing", "D4_PARALLEL_PAIR_SCREEN",
    "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER",
    "The general-screen Cartan and Frobenius calculation extends the twisted-S3 nonparallel obstruction to every invertible P in that block family.")

P = "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/STATUS_LEDGER.tsv"
add(P, "stationary_scalar_clock_join exact_local_nonparallel_anchor sampled_curvature_holonomy_algebra ordinary_endpoint_X_closure Lorentz_holonomy_as_reciprocal_inversion physical_lambda_profile_topology",
    "D1_EQUAL_WEIGHT_OR_LAMBDA_ONLY", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The exact or sampled result remains evidence for the registered lambda subfamily; it is not a full-GL2 holonomy classification.")
add(P, "ordinary_vs_twisted_vs_groupoid_selection", "D6_MULTIPLE", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER",
    "Additional screen freedom does not supply the missing selection law.")

P = "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/STATUS_LEDGER.tsv"
add(P, "S01 S02 S03 S04 S05 S07 S09 S10", "D1_EQUAL_WEIGHT_OR_LAMBDA_ONLY",
    "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The X_lambda bundle algebra remains exact as the isotropic-screen comparison subbundle; it is not the full metric screen response.")
add(P, "S13", "D4_PARALLEL_PAIR_SCREEN", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER",
    "The prior refusal to impose parallelism is reinforced by the twisted-S3 all-P obstruction.")

P = "udt_bootstrap_clock_angular_closure_audit_2026-07-24/STATUS_LEDGER.tsv"
add(P, "S04", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER",
    "Volume sees only trace and therefore cannot distinguish either newly explicit trace-free shear mode.")
add(P, "S12 S13", "D4_PARALLEL_PAIR_SCREEN", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The local criterion remains exact, but an all-direction parallel pair/screen split is impossible on the registered twisted S3 block family.")
add(P, "S18 S19", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The negative remains exact only in its stated round/local control and is not a full-screen theorem.")
add(P, "S20 S21 S22 S24", "D6_MULTIPLE", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The frozen censuses still have zero complete witnesses; the new screen family was not in those freezes and supplies no bootstrap or solder selector.")

P = "udt_intrinsic_clock_transverse_solder_audit_2026-07-24/STATUS_LEDGER.tsv"
add(P, ["screen-gauge-equivariant linear clock-to-phase map"], "D2_FIXED_DIAGONAL_ROUND_SCREEN",
    "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER",
    "A larger screen configuration space does not create a gauge-equivariant selected phase vector.")
add(P, ["parallel tidal-invariant screen line criterion"], "D4_PARALLEL_PAIR_SCREEN",
    "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The iff algebra survives locally; its all-direction realization fails on the twisted S3 general-screen block family.")
add(P, ["WRL pointwise natural-frame clock-transverse generator solder"], "D2_FIXED_DIAGONAL_ROUND_SCREEN",
    "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The no-similarity result is retained only for the exact local radial control.")
add(P, ["dphi 3plus3 clock-to-Jacobi solder", "prior matched reciprocal-angular intertwiner",
        "intrinsic irreducible clock-transverse solder", "complete nontrivial all-observer realization"],
    "D6_MULTIPLE", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The general screen supplies response modes and a connection, but not a selected irreducible solder, physical section or all-observer realization.")

P = "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv"
add(P, "N02", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "A general positive block-screen configuration now exists on one complete S3 control; physical slot selection, off-blocks, boundary and dynamics remain open.",
    effective="GENERAL_BLOCK_SCREEN_CONFIGURATION_EXISTS__PHYSICAL_TRANSVERSE_SELECTION_OPEN")
add(P, "N07 N08 N09 N10 N11 N12 N13 N14 N15 N16", "D2_FIXED_DIAGONAL_ROUND_SCREEN",
    "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The reciprocal/Hopf statements remain exact or conditional inside their diagonal toric/round witnesses and are not unique over a general GL2 screen.")
add(P, "N17", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SUPERSEDED_BY_GENERAL_SCREEN_RESULT",
    "Both screen shear tangents and their anisotropic rotation/shear mixing are now explicit on the chosen S3 control; physical angular slots and selection remain open.",
    priority="HIGH", effective="GENERAL_SCREEN_TWO_SHEAR_CONFIGURATION_DERIVED__HOPF_SELECTION_OPEN")
add(P, "N18", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The angle-dependent coupling remains exact in the supplied diagonal reciprocal radial witness and is not a generic full-screen result.")
add(P, "N22", "D6_MULTIPLE", "REQUIRES_FULL_SCREEN_REDERIVATION",
    "The conditional bridge remains promising but any claim that diagonal reciprocal anisotropy is privileged must be rerun across the full screen family.",
    priority="HIGH")

P = "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv"
add(P, "T02", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "A complete S3 block-screen configuration exists, but physical transverse ownership and toric periodicity/action remain unselected.",
    effective="CONFIGURATION_EXISTENCE_PARTLY_CLOSED__PHYSICAL_TORIC_SLOT_SELECTION_OPEN")
add(P, "T03 T06 T07 T08 T09 T10 T11 T12 T13 T14", "D2_FIXED_DIAGONAL_ROUND_SCREEN",
    "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "Each statement remains exact in its supplied diagonal/toric/cap class; the general screen prevents promotion to a generic uniqueness claim.")
add(P, "T18", "D6_MULTIPLE", "REQUIRES_FULL_SCREEN_REDERIVATION",
    "The first gate is no longer bare screen existence; it is selection of a toric reduction/periodicity and compatible global completion inside the larger screen family.",
    priority="HIGH")

P = "udt_observer_pair_clock_operator_audit_2026-07-24/STATUS_LEDGER.tsv"
add(P, "complete_angular_shift_transport", "D6_MULTIPLE", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "A complete stationary general-screen connection now exists on one chosen S3 branch, but physical endpoint frames, path semantics, off-blocks and general holonomy remain open.")

P = "udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv"
add(P, "S04", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER",
    "The independent screen-gauge obstruction survives the larger response vocabulary.")
add(P, "S06 S07 S08", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The conditional Hopf-coordinate and toric-cap statements remain witness-scoped, not generic screen selection.")
add(P, "S09 S10 S13 S14", "D6_MULTIPLE", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The global lift/response closure is still absent; the new general screen supplies configurations but no off-shell response law or selector.")

P = "udt_xmax_observer_separation_audit_2026-07-24/STATUS_LEDGER.tsv"
add(P, "S21", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER",
    "The need for the full angular global metric is strengthened by the two newly explicit shear directions.")

P = "udt_historical_angular_method_salvage_audit_2026-07-28/STATUS_LEDGER.tsv"
add(P, "current_positive_screen_decomposition current_traceless_screen_closure lambda_as_complete_screen_response complete_screen_operator_method",
    "D0_NONE", "UNAFFECTED_LOGICALLY_INDEPENDENT",
    "The general-screen construction is the preregistered realization of this salvaged complete-operator method; historical particle/QCD claims remain quarantined.")

P = "CURRENT_SCIENTIFIC_PREMISES.tsv"
add(P, "G08", "D6_MULTIPLE", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The effective open gate is selected complete extension plus direct off-block/time/global continuation; general screen availability on one stationary S3 control is now derived.",
    effective="OPEN_SELECTION_WITH_GENERAL_SCREEN_CONFIGURATION_CLASS")
add(P, "G13", "D2_FIXED_DIAGONAL_ROUND_SCREEN", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION",
    "The conditional toric geometry is witness-scoped; a general screen does not select U1, action, source, current or charge.")


# Every remaining current-owner row is enumerated explicitly. There is no automatic D0 fallback.
unchanged("udt_complete_screen_response_branch_atlas_2026-07-28/STATUS_LEDGER.tsv",
          "S01 S02 S07 S12 S13 S14",
          "Ambient screen algebra, fixed mixing certificate, open physics, and bounded verification grade do not rely on a promoted zero-shear or complete-lambda premise.")
unchanged("udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv",
          "S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14",
          "This is the correction-source ledger itself; every row already carries stationary, block-screen, off-shell, and unselected scope.")
unchanged("udt_metric_natural_joint_selector_nogo_2026-07-28/STATUS_LEDGER.tsv",
          "full_Lorentz_real_character noncollinear_angular_component pointwise_metric_only_reciprocal_generator observer_query_law stationary_Killing_depth reducible_comparison_groupoid universal_whole_solution_selector_no_go founded_phi action_source_carrier_boundary_density_Xmax_mass_dynamics",
          "The Lorentz/cocycle/founded-depth theorem or retained open boundary is algebraically independent of the transverse screen parameter count.")
unchanged("udt_joint_selector_provenance_audit_2026-07-28/STATUS_LEDGER.tsv",
          "source_discovery founded_reciprocal_pair stationary_Killing_norm_depth Levi_Civita_coframe_transport stationary_hybrid_comparison global_completion bootstrap co_presence strong_local_CSN c_E_and_G_obs action_source_carrier_boundary_density_Xmax_mass_dynamics",
          "The provenance, founded pair, stationary depth, typed transport, global multiplicity, anchors, and retained open/working stamps do not use equal screen weights as a complete response.")
unchanged("udt_native_global_coframe_definition_audit_2026-07-28/STATUS_LEDGER.tsv",
          "S01 S02 S05 S06 S07 S09 S10 S11 S12 S13 S14 S16",
          "These rows concern the founded generator, frame obstruction, conditional stationary lines, physical semantics, global interfaces, anchors, equations, frozen P03 scope, or verification grade rather than full-screen completeness.")
unchanged("udt_global_functional_dof_constraint_rank_audit_2026-07-26/STATUS_LEDGER.tsv",
          "S01 S02 S03 S05 S06 S08 S10 S11 S12 S14",
          "Generic quotient rank, inactive CSN arithmetic, untyped extra fields, boundary rank, completion taxonomy, conditional Maxwell identity, and propagating-mode openness are independent of the old equal-screen ansatz.")
unchanged("udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/STATUS_LEDGER.tsv",
          "intrinsic_clock_line_C01_to_C06 intrinsic_ruler_line_C01_to_C06 intrinsic_rank_two_screen_C01_to_C06 founding_depth_equals_log_Q same_metric_clock_plus_Jacobi_cocycle SNe_result copresence metric_causal_structure instantaneous_operational_access complete_whole_solution_law path_event_endpoint_semantics lambda_profile_twist_topology action_source_carrier_boundary_density_bootstrap_mass_Xmax_dynamics",
          "The intrinsic lines/screen, branch depth, typed cocycle, preserved SNe evidence, interpretive stamps, chosen topology/profile, and open physics do not assert that lambda exhausts the screen.")
unchanged("udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/STATUS_LEDGER.tsv",
          "path_groupoid_reciprocal_lift action_source_carrier_boundary_density_bootstrap_mass_Xmax_dynamics copresence",
          "Typed path assembly and retained authority boundaries are independent of how many screen metric modes are available.")
unchanged("udt_global_reciprocal_bundle_assembly_audit_2026-07-26/STATUS_LEDGER.tsv",
          "S06 S08 S11 S12 S14",
          "Homogeneous-control spatial holonomy and the open endpoint, completion, signed-depth, and downstream-physics gates do not require a complete-lambda assumption.")
unchanged("udt_bootstrap_clock_angular_closure_audit_2026-07-24/STATUS_LEDGER.tsv",
          "S01 S02 S03 S05 S06 S07 S08 S09 S10 S11 S14 S15 S16 S17 S23 S25 S26",
          "Bootstrap semantics, exact density variation, absent mass functional, generic two-screen spectral algebra, conditional matched projector, connection openness, and retained physics boundaries remain independent or explicitly conditional.")
unchanged("udt_intrinsic_clock_transverse_solder_audit_2026-07-24/STATUS_LEDGER.tsv",
          ["oriented normal-screen area Hodge duality", "Hodge area duality is clock-Jacobi solder",
           "scalar Jacobi-reciprocal generator criterion", "WRL clock-transverse scalar profile relation",
           "direct-sum common-path cocycle", "action source carrier density bootstrap physical Xmax"],
          "Typed Hodge/Jacobi algebra, the exact scalar criterion, local WRL identity, reducible path cocycle, and retained physics boundary do not rely on screen completeness.")
unchanged("null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv",
          "N01 N03 N04 N05 N06 N19 N20 N21",
          "Founded pair, celestial-fiber typing, frame-covariance obstructions, scoped wall probe, co-presence compatibility, and open action remain independent of the diagonal screen being exhaustive.")
unchanged("angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
          "T01 T04 T05 T15 T16 T17",
          "Founded reciprocity, supplied-toric lattice topology, finite-cell canon insufficiency, bootstrap absence, and open dynamics retain their exact premise scopes.")
unchanged("matter_bootstrap_dimensional_inventory_2026-07-20/STATUS_LEDGER.tsv",
          "S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16",
          "Every row is a dimensional, coefficient, topology, numerical-control, or carrier/action scope theorem independent of the transverse screen parameterization.")
unchanged("scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv",
          "S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16",
          "Every row concerns dimensional homogeneity, scale closure, boundary normalization, bootstrap absence, or retained open physics rather than screen-response completeness.")
unchanged("udt_observer_pair_clock_operator_audit_2026-07-24/STATUS_LEDGER.tsv",
          ["abstract_ordered_reciprocal_pair_operator", "operator_determinant_composition_inverse",
           "balanced_basis_O11_boost", "K_as_physical_observer_interval",
           "named_temporal_channel_exp_minus_rho", "reversal_even_half_trace_cosh",
           "sech_as_mutual_observer_slow_factor", "endpoint_local_phi_factorization",
           "static_metric_coordinate_covector_transport", "static_metric_orthonormal_spatial_transport",
           "stationary_lapse_ratio", "global_metric_pair_depth_realization", "path_family_at_cut_locus",
           "physical_global_mutual_clock_law", "physical_Xmax_mass_density_CMB", "overall"],
          "The two-channel reciprocal operator and its still-open global physical readout are upstream of transverse-screen completion.")
unchanged("udt_common_scale_neutrality_provenance_audit_2026-07-24/STATUS_LEDGER.tsv",
          "S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23 S24",
          "The CSN provenance, calibration, action-class, conformal, macro, particle, and complete-physics statuses are controlled by scale/variation premises, not the stationary screen ansatz.")
unchanged("udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv",
          "S01 S02 S03 S05 S11 S12 S15 S16 S17 S18 S19 S20 S21",
          "Typed cocycles, topology insufficiency, on-shell bootstrap semantics, conditional action ordering, integrability gates, complete-action openness, grade, and next-task history do not assume lambda is the full screen.")
unchanged("udt_xmax_observer_separation_audit_2026-07-24/STATUS_LEDGER.tsv",
          "S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S22 S23 S24",
          "The observer-separation schema, one-dimensional controls, WRL/SNe retention, scale theorem, mass/bootstrap openness, local frame reciprocity, particle independence, and complete-physics boundary are not altered by the general screen.")
unchanged("udt_historical_angular_method_salvage_audit_2026-07-28/STATUS_LEDGER.tsv",
          "historical_mass_ratio_arithmetic historical_lepton_quark_qcd_claims old_3_plus_5_dimension_count old_3_plus_5_as_unique_QCD_structure compact_su3_interpretation screen_response_coefficients global_screen_bundle_and_transport action_source_carrier_matter_map",
          "Historical arithmetic remains quarantined; generic algebra and open downstream questions are not affirmative physics and are not altered by realizing the method.")
unchanged("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
          "S01 S02 S03 S04 S05 S06 S07 S08 S09 S10 S11 S12 S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23 S24 S25 S26 S27 S28 S29 S30 S31 S32 S33",
          "The frozen action adjudication rows are controlled by their founding, variation-domain, carrier, boundary, mass, and provenance-firewall premises; S08 already says the reciprocal block is not the full metric, so the general screen does not correct these rows.")
unchanged("CURRENT_SCIENTIFIC_PREMISES.tsv",
          "G01 G02 G03 G04 G05 G06 G07 G09 G10 G11 G12 G14 G15 G16",
          "The current premise remains independently controlled by its cited owner; no general-screen availability is promoted into foundation, carrier, action, bootstrap, Xmax, stability, or complete physics.")


FAMILY_SUMMARY = [
    ("founded_phi_and_observer_pair", "UNAFFECTED_LOGICALLY_INDEPENDENT", "Founded reciprocal depth and the two-channel operator do not depend on the transverse screen.", "NONE"),
    ("historical_complete_screen_method", "UNAFFECTED_LOGICALLY_INDEPENDENT", "The salvaged method is confirmed; its historical particle and QCD claims remain quarantined.", "NONE"),
    ("registered_screen_response_parent", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION", "Zero shear remains exact only in the frozen equal-weight rows; general-screen existence supersedes the old open existence row.", "NONE"),
    ("native_complete_coframe_and_joint_selector", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER", "Lambda is an isotropic trace modulus, not the full screen; no selector is gained.", "HIGH_IF_SELECTION_IS_RESUMED"),
    ("metric_natural_Lorentz_no_go", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION", "Character, commutant and bracket proofs are independent; reduced lambda lifts are explicitly subfamily results.", "NONE"),
    ("functional_DOF_rank", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION", "Three screen metric modes are available but zero are selected by founded phi alone.", "NONE"),
    ("twisted_S3_Cartan_cocycle_holonomy", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER", "Equal-screen exact results survive and the all-P block-screen nonparallel obstruction is stronger.", "MEDIUM_IF_FULL_HOLONOMY_IS_NEEDED"),
    ("bootstrap_clock_angular_solder", "SURVIVES_WITH_EXPLICIT_SCOPE_CORRECTION", "Volume is blind to both shears; local projector algebra survives; no bootstrap selection appears.", "MEDIUM_IF_BOOTSTRAP_SELECTOR_IS_RESUMED"),
    ("conditional_Hopf_toric_bridge", "REQUIRES_FULL_SCREEN_REDERIVATION", "Conditional witnesses survive, but diagonal/round structures cannot be privileged without testing the full screen family.", "HIGH"),
    ("static_Hopfion_stability", "UNAFFECTED_LOGICALLY_INDEPENDENT", "The finite-box carrier-conditional stability result uses its stated carrier/operator, not the metric screen-selection claim.", "NONE"),
    ("matter_and_scale_dimensional_theorems", "UNAFFECTED_LOGICALLY_INDEPENDENT", "The dimensional-rank and coefficient-ruler conclusions do not depend on equal screen weights.", "NONE"),
    ("Xmax_observer_separation", "SURVIVES_AND_NONUNIQUENESS_IS_STRONGER", "Its demand for the full angular global metric is reinforced; no value or pairing functional is selected.", "NONE"),
    ("WRL_SNe_macro_readout", "UNAFFECTED_LOGICALLY_INDEPENDENT", "The observed conditional fit is unchanged; only the optional lambda-minus-two interpretation remains trace-subfamily scoped.", "NONE"),
    ("C2_Bach_EH_and_complete_action", "UNAFFECTED_LOGICALLY_INDEPENDENT", "Those statuses are controlled by variation-domain and CSN/minimality premises, not this stationary screen parameterization.", "NONE"),
    ("complete_action_source_boundary_mass", "UNAFFECTED_LOGICALLY_INDEPENDENT", "All remain open; the screen atlas supplies no action, source, charge or mass law.", "NONE"),
]


RERUNS = [
    ("R01", "HIGH", "conditional_Hopf_toric_bridge", "Re-express the toric/Hopf compatibility and selector gates over the full positive GL2 screen, retaining both shears, frame rotation, cap data and off-block exclusions.", "Only if the Hopf/toric selection route is resumed; no claim that a carrier emerges."),
    ("R02", "HIGH", "native_complete_coframe_and_joint_selector", "Retest candidate physical selectors on the general screen rather than X_lambda alone, while preserving the Lorentz no-go and founded pair.", "Only if a selector derivation is authorized; no parameter choice in this audit."),
    ("R03", "MEDIUM", "bootstrap_clock_angular_solder", "Carry any future typed bootstrap response across trace plus both shears and test the twisted-S3 nonparallel obstruction.", "Only after a native off-shell response map exists; density scanning is not authorized."),
    ("R04", "MEDIUM", "twisted_S3_Cartan_cocycle_holonomy", "Map E0(P) or broader holonomy only under a separate preregistration; retain the present stationary all-P theorem.", "No evolution equation, ODE/PDE or time-live solve follows automatically."),
    ("R05", "LOW", "WRL_SNe_macro_readout", "Revisit only the proposed lambda-minus-two angular identification if it is reused; do not rerun or demote the registered SNe fit merely because the screen enlarged.", "Macro evidence stays unchanged."),
]


def git_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def git_blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True).strip()


def read_tsv_at_base(path: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(git_bytes(path).decode("utf-8")), delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def family_route(family: str, family_owner_paths: dict[str, list[str]],
                 registry_owner_paths: dict[str, list[str]]) -> tuple[str, str, str]:
    if family == "CONTROL_ROOT":
        return ("MIXED_CONTROL_AUTHORITY", "LIVE.md;CURRENT_SCIENTIFIC_PREMISES.tsv",
                "Top LIVE state and the effective premise registry control; other root matches are forensic support only.")
    if family in family_owner_paths:
        return ("CURRENT_COMPARISON_FAMILY_EXPLICIT_ROW_REVIEW", ";".join(family_owner_paths[family]),
                "Every row of the named status ledger has an explicit dependency decision in this audit.")
    if family in registry_owner_paths:
        return ("CURRENT_PREMISE_CONTROLLER", ";".join(registry_owner_paths[family]),
                "The effective current claim is explicitly represented in CURRENT_SCIENTIFIC_PREMISES.tsv and its controlling source is hash-frozen here.")
    if family in NAMED_LATER_OWNER_ROUTES:
        return ("HISTORICAL_FAMILY_WITH_NAMED_LATER_OWNER", NAMED_LATER_OWNER_ROUTES[family],
                "Preserve the historical package; use the named later owner for current effective status and screen-scope regrade.")
    if family.startswith(C2_PREFIXES):
        return ("HISTORICAL_C2_OR_BOUNDARY_LINEAGE_WITH_NAMED_CURRENT_OWNER",
                "CURRENT_SCIENTIFIC_PREMISES.tsv:G10-G11-G16;native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv:S11-S25",
                "Historical angular/coframe/boundary calculations retain their scope; current C2/Bach/EH/action authority is the named adjudication chain.")
    if family in EXPLICIT_HISTORICAL_ROUTES:
        return ("HISTORICAL_SCOPED_FAMILY_WITH_EXPLICIT_CURRENT_AUTHORITY_ROUTE",
                EXPLICIT_HISTORICAL_ROUTES[family],
                "The historical package retains its exact scope; the named current owner controls any effective reuse under the general-screen correction.")
    raise RuntimeError(f"family lacks explicit authority route: {family}")


def main() -> None:
    claims = []
    manifest = []
    source_ids = set()
    used_overrides = set()
    for path, (id_col, claim_col, status_col) in SOURCE_SPECS.items():
        raw = git_bytes(path)
        rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8")), delimiter="\t"))
        blob = git_blob(path)
        sha = hashlib.sha256(raw).hexdigest()
        manifest.append({"path": path, "source_role": "ROW_ADJUDICATED_LEDGER", "git_blob": blob,
                         "sha256": sha, "bytes": len(raw), "claim_rows": len(rows)})
        for row in rows:
            identity = row[id_col]
            key = (path, identity)
            if key in source_ids:
                raise RuntimeError(f"duplicate source identity {key}")
            source_ids.add(key)
            decision = OVERRIDES.get(key)
            if decision is None:
                raise RuntimeError(f"missing explicit row decision {key}")
            used_overrides.add(key)
            dep, ruling, effective, explanation, priority = decision
            claims.append({
                "source_path": path,
                "source_blob": blob,
                "claim_identity": identity,
                "claim": row[claim_col],
                "original_status": row[status_col],
                "dependency_class": dep,
                "regrade_class": ruling,
                "effective_status": effective or row[status_col],
                "correction_or_reason": explanation,
                "rerun_priority": priority,
            })
    missing = sorted(set(OVERRIDES) - used_overrides)
    if missing:
        raise RuntimeError(f"override keys missing from sources: {missing}")

    premise_rows = read_tsv_at_base("CURRENT_SCIENTIFIC_PREMISES.tsv")
    controller_paths = {row["controlling_source"] for row in premise_rows}
    supplemental_paths = sorted((TOP_CURRENT_SOURCE_PATHS | controller_paths) - set(SOURCE_SPECS))
    for path in supplemental_paths:
        raw = git_bytes(path)
        role = "CURRENT_PREMISE_CONTROLLER_SOURCE" if path in controller_paths else "TOP_CURRENT_AUTHORITY_SOURCE"
        manifest.append({"path": path, "source_role": role, "git_blob": git_blob(path),
                         "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "claim_rows": 0})
    manifest.sort(key=lambda row: row["path"])

    write_tsv(OUT / "LOAD_BEARING_SOURCE_MANIFEST.tsv",
              ["path", "source_role", "git_blob", "sha256", "bytes", "claim_rows"], manifest)
    write_tsv(OUT / "CURRENT_LOAD_BEARING_CLAIM_REGRADING.tsv",
              ["source_path", "source_blob", "claim_identity", "claim", "original_status",
               "dependency_class", "regrade_class", "effective_status", "correction_or_reason",
               "rerun_priority"], claims)

    discovered = list(csv.DictReader((OUT / "DISCOVERED_SOURCE_CENSUS.tsv").open(encoding="utf-8"), delimiter="\t"))
    exact_paths = set(SOURCE_SPECS)
    family_owner_paths: dict[str, list[str]] = {}
    for path in exact_paths:
        if "/" in path:
            family_owner_paths.setdefault(path.split("/", 1)[0], []).append(path)
    for paths in family_owner_paths.values():
        paths.sort()
    registry_owner_paths: dict[str, list[str]] = {}
    for path in controller_paths:
        if "/" in path:
            registry_owner_paths.setdefault(path.split("/", 1)[0], []).append(path)
    for paths in registry_owner_paths.values():
        paths.sort()
    source_dispositions = []
    for row in discovered:
        route, owner, basis = family_route(row["family"], family_owner_paths, registry_owner_paths)
        if row["path"] in exact_paths:
            disposition = "CURRENT_EXACT_ROW_ADJUDICATED"
        elif row["path"] in controller_paths:
            disposition = "CURRENT_PREMISE_CONTROLLER_HASH_FROZEN"
        elif row["role"] == "PRIMARY_CLAIM_SOURCE":
            disposition = route
        else:
            disposition = "FORENSIC_SUPPORTING_SOURCE_NOT_CLAIM_OWNER"
        source_dispositions.append({**row, "audit_disposition": disposition,
                                    "effective_owner": owner, "routing_basis": basis})
    write_tsv(OUT / "DISCOVERED_SOURCE_DISPOSITION.tsv",
              list(discovered[0]) + ["audit_disposition", "effective_owner", "routing_basis"], source_dispositions)

    primary_fields = ["path", "family", "git_blob", "sha256", "dependency_hits", "audit_disposition",
                      "effective_owner", "routing_basis"]
    primary_routes = [
        {field: row[field] for field in primary_fields}
        for row in source_dispositions if row["role"] == "PRIMARY_CLAIM_SOURCE"
    ]
    write_tsv(OUT / "PRIMARY_CLAIM_AUTHORITY_ROUTING.tsv",
              primary_fields, primary_routes)

    family_rows = list(csv.DictReader((OUT / "DISCOVERED_FAMILY_CENSUS.tsv").open(encoding="utf-8"), delimiter="\t"))
    family_dispositions = []
    for row in family_rows:
        family = row["family"]
        disposition, owner, basis = family_route(family, family_owner_paths, registry_owner_paths)
        family_dispositions.append({**row, "adjudication_status": disposition,
                                    "effective_owner": owner, "routing_basis": basis})
    write_tsv(OUT / "DISCOVERED_FAMILY_DISPOSITION.tsv",
              list(family_rows[0]) + ["effective_owner", "routing_basis"], family_dispositions)
    write_tsv(OUT / "FAMILY_AUTHORITY_ROUTING.tsv",
              ["family", "all_matching_sources", "primary_claim_sources", "adjudication_status",
               "effective_owner", "routing_basis"], family_dispositions)

    summary_rows = [{"family": a, "ruling": b, "reason": c, "redo_priority": d}
                    for a, b, c, d in FAMILY_SUMMARY]
    write_tsv(OUT / "FAMILY_IMPACT_SUMMARY.tsv", ["family", "ruling", "reason", "redo_priority"], summary_rows)
    rerun_rows = [{"rank": a, "priority": b, "family": c, "bounded_task": d, "authority_boundary": e}
                  for a, b, c, d, e in RERUNS]
    write_tsv(OUT / "RERUN_PRIORITY.tsv", ["rank", "priority", "family", "bounded_task", "authority_boundary"], rerun_rows)

    dep_counts = Counter(row["dependency_class"] for row in claims)
    ruling_counts = Counter(row["regrade_class"] for row in claims)
    result = {
        "schema": "udt-general-screen-dependency-regrade-1.0",
        "base": BASE,
        "status": "PASS",
        "sources": len(manifest),
        "claim_rows": len(claims),
        "explicit_decision_rows": len(used_overrides),
        "dependency_counts": dict(sorted(dep_counts.items())),
        "regrade_counts": dict(sorted(ruling_counts.items())),
        "discovered_sources_dispositioned": len(source_dispositions),
        "discovered_families_dispositioned": len(family_dispositions),
        "primary_claim_sources_routed": len(primary_routes),
        "family_summary_rows": len(summary_rows),
        "rerun_rows": len(rerun_rows),
    }
    (OUT / "BUILD_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
