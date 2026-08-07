#!/usr/bin/env python3
"""Derive the observer-pair X_max correction overlay.

This script is deliberately finite and deterministic.  It classifies the
preregistered base-commit census, evaluates elementary metric countermodels,
and emits only dependency/status records.  It does not modify source records.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
BASE = "696cf401c441fdd3aefea6f3de188e6425ae5636"


HISTORICAL_PREFIXES = (
    "archive/",
    "legacy/",
    "rescued_workspaces/",
    "reorganization_r",
)
FROZEN_PREFIXES = (
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_final_adjudication_2026-07-18/",
)
RELATIONAL_FAMILIES = {
    "udt_observer_centered_xmax_frame_correction_2026-07-23",
    "udt_metric_pure_frame_rederivation_2026-07-23",
    "udt_two_frame_regime_metric_limit_audit_2026-07-22",
    "udt_reciprocity_regime_angular_center_audit_2026-07-22",
}
LOCAL_FAMILIES = {
    "asymptotic_boundary_lineage_audit_2026-07-19",
    "clock_curvature_selector_audit_2026-07-19",
    "native_boundary_generator_scale_audit_2026-07-19",
    "udt_wrl_xmax_lightcone_frame_audit_2026-07-23",
    "udt_xmax_dilation_asymptote_correction_2026-07-23",
}
EDGE_FAMILIES = {
    "udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23",
}
BOUNDARY_FAMILIES = {
    "boundary_bootstrap_representative_selector_audit_2026-07-19",
    "c2_finite_cell_boundary_variation_2026-07-20",
    "complete_coframe_seal_involution_2026-07-20",
    "finite_cell_seal_boundary_phase_join_2026-07-20",
    "udt_complete_seal_fixed_set_selector_audit_2026-07-21",
    "udt_free_global_seal_transversality_audit_2026-07-21",
    "udt_global_reciprocal_closure_audit_2026-07-20",
    "udt_pre_p06_boundary_selector_audit_2026-07-21",
    "udt_time_extendability_constraint_audit_2026-07-20",
    "udt_time_live_characteristic_flux_audit_2026-07-21",
}
SCALE_FAMILIES = {
    "angular_derivative_weight_selector_2026-07-20",
    "matter_bootstrap_dimensional_inventory_2026-07-20",
    "scale_breaking_closure_census_2026-07-20",
}
ASYMPTOTIC_FAMILIES = {
    "projective_position_direction_magnitude_correction_2026-07-19",
    "projective_position_join_audit_2026-07-19",
    "reciprocal_c_clock_channel_correction_2026-07-19",
    "udt_three_reciprocity_delta_k_audit_2026-07-23",
    "xmax_accelerating_finite_cell_cartan_2026-07-19",
    "xmax_dynamic_observer_frame_2026-07-19",
    "xmax_full_frame_realization_2026-07-19",
    "xmax_reciprocity_audit_2026-07-19",
}
ROOT_CONTROL = {
    "HANDOFF.md",
    "INDEX.md",
    "LIVE.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md",
}
ROOT_FROZEN = {
    "CANON.md",
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md",
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md",
    "UDT_NATIVE_ACTION_WORKSTATION_SYNC_AUDIT_2026-07-17.md",
    "UDT_NATIVE_ACTION_WORKSTATION_SYNC_DISPATCH.md",
    "UDT_WORKSTATION_TRANSFER_MANIFEST_2026-07-17.md",
}
ROOT_HISTORICAL = {
    "HANDOFF_ARCHIVE.md",
    "MEMORY.md",
    "codex_rehearsal_transcript.txt",
    "external.md",
    "grok",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def family(path: str) -> str:
    return path.split("/", 1)[0]


def is_generated(path: str) -> bool:
    name = Path(path).name
    generated_names = {
        "CANDIDATE_UNIVERSE.tsv",
        "SOURCE_CENSUS.tsv",
        "SOURCE_ADJUDICATION.tsv",
        "SOURCE_MANIFEST.tsv",
        "MANIFEST.sha256",
        "SHA256SUMS.txt",
        "REPOSITORY_GATES.json",
        "VERIFICATION_RESULT.json",
        "RESULTS.json",
        "DERIVATION_RESULT.json",
        "CATCH_PROOFS.tsv",
        "CATCH_PROOF_RESULTS.tsv",
    }
    return (
        name in generated_names
        or name.endswith("_out.json")
        or "transcript" in name.lower()
        or "rerun" in name.lower()
    )


def classify(path: str) -> tuple[str, str, str, str]:
    """Return classification, effect, evidence basis, load-bearing flag."""
    top = family(path)
    if path in ROOT_FROZEN or path.startswith(FROZEN_PREFIXES):
        return (
            "FROZEN_EVIDENCE",
            "PRESERVE_WITH_OVERLAY",
            "manifest_or_controller_immutability",
            "NO",
        )
    if path in ROOT_HISTORICAL or path.startswith(HISTORICAL_PREFIXES):
        return (
            "HISTORICAL_SNAPSHOT",
            "PRESERVE_WITH_OVERLAY",
            "historical_or_reorganization_provenance",
            "NO",
        )
    if is_generated(path):
        return (
            "GENERATED_AUDIT_RECORD",
            "FAMILY_ADJUDICATION_ALLOWED",
            "mechanical_or_replay_record",
            "NO",
        )
    if path in ROOT_CONTROL:
        return (
            "RELATIONAL_COMPATIBLE",
            "RETAIN_WITH_PREMISE_STAMP",
            "current_control_requires_correction_overlay",
            "YES",
        )
    if path == "NEGATIVES_REGISTRY.md":
        return (
            "RELATIONAL_COMPATIBLE",
            "RETAIN_WITH_PREMISE_STAMP",
            "frame_level_centered_bearing_already_retracted",
            "YES",
        )
    if path == "UDT_ELEGANT_FRAME.md":
        return (
            "ASYMPTOTIC_LIMIT_COMPATIBLE",
            "RETAIN_CONDITIONAL",
            "projective_1D_law_requires_scope_regrade",
            "YES",
        )
    if top in RELATIONAL_FAMILIES:
        return (
            "RELATIONAL_COMPATIBLE",
            "RETAIN_WITH_PREMISE_STAMP",
            "observer_pair_or_no_preferred_frame_scope",
            "YES" if Path(path).name in {"AUDIT_REPORT.md", "STATUS_LEDGER.tsv"} else "NO",
        )
    if top in LOCAL_FAMILIES:
        return (
            "LOCAL_X_DISTINCT",
            "RETAIN_LOCAL_RESULT_SEPARATE_GLOBAL_ID_OPEN",
            "WRL_or_local_boundary_scale",
            "YES" if Path(path).name in {"AUDIT_REPORT.md", "STATUS_LEDGER.tsv"} else "NO",
        )
    if top in EDGE_FAMILIES:
        return (
            "EDGE_CONFLATION",
            "CORRECT_OR_REGRADE",
            "one_radial_boundary_inferred_from_Xmax_working_frame",
            "YES" if Path(path).name in {"AUDIT_REPORT.md", "STATUS_LEDGER.tsv"} else "NO",
        )
    if top in BOUNDARY_FAMILIES:
        return (
            "BOUNDARY_DEPENDENT",
            "CONDITIONS_CHANGED_IF_XMAX_WAS_SOLE_BOUNDARY_SOURCE",
            "requires_surface_seal_or_variation_data",
            "YES" if Path(path).name in {"AUDIT_REPORT.md", "STATUS_LEDGER.tsv"} else "NO",
        )
    if top in SCALE_FAMILIES:
        return (
            "SCALE_ONLY_UNAFFECTED",
            "RETAIN_UNCHANGED",
            "dimensional_or_common_homothety_use",
            "YES" if Path(path).name in {"AUDIT_REPORT.md", "STATUS_LEDGER.tsv"} else "NO",
        )
    if top in ASYMPTOTIC_FAMILIES:
        return (
            "ASYMPTOTIC_LIMIT_COMPATIBLE",
            "RETAIN_CONDITIONAL",
            "exact_1D_or_projective_mathematics_not_general_pair_metric",
            "YES" if Path(path).name in {"AUDIT_REPORT.md", "STATUS_LEDGER.tsv"} else "NO",
        )
    if path.startswith("macro_") or path.startswith("simple_metric_") or path in {
        "derive_xmax_boost.py",
        "luminosity_distance_n2_optics_results.md",
        "verify_xmax_mass_optics.py",
    }:
        return (
            "LOCAL_X_DISTINCT",
            "RETAIN_LOCAL_RESULT_SEPARATE_GLOBAL_ID_OPEN",
            "root_macro_WRL_or_SNe_artifact",
            "NO",
        )
    return (
        "GENERATED_AUDIT_RECORD",
        "FAMILY_ADJUDICATION_ALLOWED",
        "non_load_bearing_context_or_inherited_open_status",
        "NO",
    )


def relational_rows() -> list[dict[str, str]]:
    return [
        {
            "object_id": "R01",
            "object": "admissible_observer_set_O",
            "definition_or_requirement": "domain of observer histories or observational frames",
            "status": "OPEN",
            "why": "complete metric has not selected an observer class",
        },
        {
            "object_id": "R02",
            "object": "comparison_relation_Cg",
            "definition_or_requirement": "which event on observer A is compared with which event on observer B",
            "status": "OPEN",
            "why": "no native simultaneity co-presence radar or quotient rule is derived",
        },
        {
            "object_id": "R03",
            "object": "pair_separation_Dg",
            "definition_or_requirement": "Dg(A,B)>=0 on admissibly paired observer events",
            "status": "OPEN",
            "why": "Lorentzian metric alone does not supply a unique nonnegative worldline distance",
        },
        {
            "object_id": "R04",
            "object": "pair_exchange",
            "definition_or_requirement": "Dg(A,B)=Dg(B,A)",
            "status": "WORKING_REQUIRED_SYMMETRY",
            "why": "distance meaning and no preferred member of a pair",
        },
        {
            "object_id": "R05",
            "object": "coincidence",
            "definition_or_requirement": "Dg(A,A)=0",
            "status": "WORKING_REQUIRED_DISTANCE_AXIOM",
            "why": "observer separation rather than signed displacement",
        },
        {
            "object_id": "R06",
            "object": "global_pair_diameter",
            "definition_or_requirement": "Xmax=sup{Dg(A,B):A,B in O and Cg(A,B)}",
            "status": "WORKING_OWNER_MEANING",
            "why": "correct relational type; functional and domain remain open",
        },
        {
            "object_id": "R07",
            "object": "attained_maximum",
            "definition_or_requirement": "there exist A,B with Dg(A,B)=Xmax",
            "status": "OPEN",
            "why": "requires compactness/completeness or a separate existence theorem",
        },
        {
            "object_id": "R08",
            "object": "per_observer_reach",
            "definition_or_requirement": "sup_B Dg(A,B)=Xmax for every A",
            "status": "OPEN_STRONGER_THAN_GLOBAL_DIAMETER",
            "why": "requires transitivity/homogeneity or equivalent global structure",
        },
        {
            "object_id": "R09",
            "object": "edge_or_boundary",
            "definition_or_requirement": "a codimension-one terminal surface at Xmax",
            "status": "NOT_IMPLIED",
            "why": "finite-diameter boundaryless countermodels exist",
        },
        {
            "object_id": "R10",
            "object": "local_WRL_join",
            "definition_or_requirement": "recorded static radial X equals global observer-pair Xmax",
            "status": "OPEN",
            "why": "radius-to-diameter coefficient and complete angular/global completion absent",
        },
        {
            "object_id": "R11",
            "object": "three_observer_composition",
            "definition_or_requirement": "Dg(A,C) determined only from Dg(A,B),Dg(B,C)",
            "status": "REFUTED_IN_GENERAL",
            "why": "angle/holonomy/curvature data are load-bearing",
        },
        {
            "object_id": "R12",
            "object": "smallest_missing_selector",
            "definition_or_requirement": "native complete-metric two-point observer separation functional including event pairing and angular/global completion",
            "status": "OPEN",
            "why": "needed before Xmax becomes metric-derived",
        },
    ]


def countermodel_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "C01",
            "space": "closed_interval_[0,X]",
            "diameter": "X",
            "boundary": "YES",
            "attained": "YES",
            "observer_transitive": "NO",
            "lesson": "finite_diameter_can_have_boundary_and_preferred_end_roles",
        },
        {
            "model_id": "C02",
            "space": "open_interval_(0,X)",
            "diameter": "supremum_X",
            "boundary": "NO_INTRINSIC_INCLUDED_BOUNDARY",
            "attained": "NO",
            "observer_transitive": "NO",
            "lesson": "finite_supremum_need_not_be_attained",
        },
        {
            "model_id": "C03",
            "space": "circle_circumference_2X",
            "diameter": "X",
            "boundary": "NO",
            "attained": "YES",
            "observer_transitive": "YES",
            "lesson": "finite_diameter_and_full_point_equivalence_do_not_imply_edge",
        },
        {
            "model_id": "C04",
            "space": "round_sphere_radius_X/pi",
            "diameter": "X",
            "boundary": "NO",
            "attained": "YES",
            "observer_transitive": "YES",
            "lesson": "diameter_to_local_radius_coefficient_depends_on_completion",
        },
        {
            "model_id": "C05",
            "space": "Euclidean_ball_radius_X/2",
            "diameter": "X",
            "boundary": "YES",
            "attained": "YES",
            "observer_transitive": "NO",
            "lesson": "diameter_is_twice_radial_scale_in_this_completion",
        },
        {
            "model_id": "C06",
            "space": "flat_torus_scaled_to_diameter_X",
            "diameter": "X",
            "boundary": "NO",
            "attained": "YES",
            "observer_transitive": "YES",
            "lesson": "quotient_completion_also_realizes_invariant_finite_diameter",
        },
        {
            "model_id": "C07",
            "space": "Euclidean_three_observer_triangle",
            "diameter": "not_fixed_by_two_adjacent_lengths",
            "boundary": "IRRELEVANT",
            "attained": "YES",
            "observer_transitive": "YES",
            "lesson": "pairwise_scalar_composition_requires_angle_data",
        },
        {
            "model_id": "C08",
            "space": "Lorentzian_worldline_pair",
            "diameter": "undefined_without_event_pairing_and_distance_choice",
            "boundary": "UNDETERMINED",
            "attained": "UNDETERMINED",
            "observer_transitive": "UNDETERMINED",
            "lesson": "metric_signature_alone_does_not_define_nonnegative observer distance",
        },
    ]


def claim_rows() -> list[dict[str, str]]:
    return [
        {"claim_id": "Q01", "claim": "Xmax_is_maximum_possible_observer_pair_separation", "prior_status": "owner_working_limit", "corrected_status": "WORKING_OWNER_MEANING", "scope": "Xmax_is_a_global_supremum_until_attainment_is_derived"},
        {"claim_id": "Q02", "claim": "Xmax_is_edge_of_universe", "prior_status": "sometimes_assumed_in_historical_language", "corrected_status": "NOT_DERIVED", "scope": "finite_diameter_does_not_select_boundary_or_topology"},
        {"claim_id": "Q03", "claim": "Xmax_selects_preferred_center", "prior_status": "historical_centered_reading", "corrected_status": "REFUTED_AS_LOGICAL_INFERENCE", "scope": "pair_diameter_is_center_free"},
        {"claim_id": "Q04", "claim": "Xmax_is_attained_by_some_observer_pair", "prior_status": "maximum_wording", "corrected_status": "OPEN", "scope": "use_supremum_without compactness theorem"},
        {"claim_id": "Q05", "claim": "every_observer_has_partner_at_Xmax", "prior_status": "frame_shared_limit_language", "corrected_status": "OPEN_STRONG_FORM", "scope": "requires_transitive_global_completion"},
        {"claim_id": "Q06", "claim": "global_Xmax_is_same_scalar_for_all_frames", "prior_status": "owner_locked conditional consistency", "corrected_status": "WORKING_OWNER_MEANING", "scope": "diameter_is_global; this does_not imply an edge distance"},
        {"claim_id": "Q07", "claim": "observer_pair_exchange_symmetry", "prior_status": "ordinary frame reciprocity", "corrected_status": "WORKING_REQUIRED_SYMMETRY", "scope": "does_not_select a composition law"},
        {"claim_id": "Q08", "claim": "metric_defines_Dg_on_observer_pairs", "prior_status": "implicitly missing", "corrected_status": "OPEN_SELECTOR", "scope": "observer domain event pairing and nonnegative functional absent"},
        {"claim_id": "Q09", "claim": "fixed_WRL_X_equals_global_Xmax", "prior_status": "open strongest candidate", "corrected_status": "OPEN_JOIN_DIAMETER_VS_RADIUS", "scope": "complete geometry must derive coefficient and identification"},
        {"claim_id": "Q10", "claim": "WRL_A_equals_1_minus_r_over_X", "prior_status": "derived conditional WRL", "corrected_status": "RETAINED_DERIVED_CONDITIONAL_WRL", "scope": "local centered profile only"},
        {"claim_id": "Q11", "claim": "WRL_clock_factor_tends_zero_as_r_tends_X", "prior_status": "derived conditional WRL", "corrected_status": "RETAINED_DERIVED_CONDITIONAL_WRL", "scope": "local static centered chart"},
        {"claim_id": "Q12", "claim": "WRL_optical_reach_is_infinite_and_wall_is_regular_null_surface", "prior_status": "derived conditional WRL", "corrected_status": "RETAINED_DERIVED_CONDITIONAL_WRL", "scope": "does_not prove global pair-diameter boundary"},
        {"claim_id": "Q13", "claim": "native_mass_diverges_at_global_Xmax", "prior_status": "working open", "corrected_status": "OPEN", "scope": "native matter mass functional absent"},
        {"claim_id": "Q14", "claim": "SNe_profile_score", "prior_status": "observed", "corrected_status": "RETAINED_OBSERVED", "scope": "calibrates supplied local WRL profile shape; not global diameter join"},
        {"claim_id": "Q15", "claim": "SNe_derives_global_Xmax_definition", "prior_status": "not claimed", "corrected_status": "NOT_DERIVED", "scope": "observation does not supply observer-pair functional or topology"},
        {"claim_id": "Q16", "claim": "fractional_Xmax_composition_is_general_observer_distance_law", "prior_status": "chose conditional signed interval", "corrected_status": "REFUTED_IN_GENERAL", "scope": "exact only in supplied collinear oriented projective class"},
        {"claim_id": "Q17", "claim": "tanh_position_law", "prior_status": "derived conditional projective", "corrected_status": "RETAINED_UNIQUE_CONDITIONAL", "scope": "anchored first-degree projective readout; not derived global distance"},
        {"claim_id": "Q18", "claim": "three_observer_distance_composition_is_scalar", "prior_status": "not explicitly separated", "corrected_status": "REFUTED_IN_GENERAL", "scope": "angular relation is load-bearing"},
        {"claim_id": "Q19", "claim": "one_asymptotic_radial_boundary_follows_from_Xmax", "prior_status": "adopted in invariant-Xmax audit", "corrected_status": "WITHDRAWN_INTERPRETATION", "scope": "retain exact 1D action classification as conditional coordinate mathematics"},
        {"claim_id": "Q20", "claim": "finite_cell_seal_is_Xmax_edge", "prior_status": "open or silent join", "corrected_status": "NOT_DERIVED", "scope": "seal type and global completion remain open"},
        {"claim_id": "Q21", "claim": "boundary_functional_or_charge_follows_from_Xmax", "prior_status": "open", "corrected_status": "OPEN", "scope": "pair diameter is not a variational boundary datum"},
        {"claim_id": "Q22", "claim": "scale_theorem_compactness_GM_over_c2Xmax", "prior_status": "derived dimensional theorem", "corrected_status": "RETAINED_DERIVED_SCOPED", "scope": "uses Xmax only as a length"},
        {"claim_id": "Q23", "claim": "c_and_G_fix_absolute_Xmax", "prior_status": "refuted by dimension and rank", "corrected_status": "RETAINED_NOT_DERIVED", "scope": "observer-pair reinterpretation does_not add a scale equation"},
        {"claim_id": "Q24", "claim": "density_or_mass_bootstrap_selects_Xmax", "prior_status": "open", "corrected_status": "OPEN", "scope": "native mass volume response and complete global solution absent"},
        {"claim_id": "Q25", "claim": "constant_CSN_homothety_preserves_D_over_Xmax", "prior_status": "scale-neutral", "corrected_status": "RETAINED_DERIVED_SCOPED", "scope": "provided D and Xmax derive from same selected representative"},
        {"claim_id": "Q26", "claim": "local_CSN_or_representative_is_fixed_by_Xmax", "prior_status": "refuted in bounded orbit", "corrected_status": "RETAINED_NOT_DERIVED", "scope": "diameter does_not remove endpoint-flat representative freedom"},
        {"claim_id": "Q27", "claim": "local_Lorentz_frame_reciprocity", "prior_status": "derived local calibrated", "corrected_status": "RETAINED_DERIVED_LOCAL", "scope": "distinct from global observer separation"},
        {"claim_id": "Q28", "claim": "local_frame_reciprocity_derives_global_Dg", "prior_status": "false excluded", "corrected_status": "RETAINED_FALSE_EXCLUDED", "scope": "needs global isometry or pair metric"},
        {"claim_id": "Q29", "claim": "global_topology_boundary_quotient_or_seam", "prior_status": "open", "corrected_status": "OPEN", "scope": "countermodels show Xmax alone cannot choose"},
        {"claim_id": "Q30", "claim": "angular_sector_is_load_bearing_for_global_pair_geometry", "prior_status": "bounded obstruction", "corrected_status": "STRENGTHENED_LOGICAL_REQUIREMENT", "scope": "three-observer composition and radius-to-diameter join require full angular/global data"},
        {"claim_id": "Q31", "claim": "complete_action_source_carrier_mass", "prior_status": "open", "corrected_status": "OPEN_UNCHANGED", "scope": "not addressed"},
        {"claim_id": "Q32", "claim": "dual_systole_and_Hopf_metric_results", "prior_status": "verified with caveats and conditional", "corrected_status": "UNCHANGED", "scope": "their local/global toric premises do_not use Xmax as an edge"},
        {"claim_id": "Q33", "claim": "CANON_WRL_xmax_wall_language", "prior_status": "canon local causal horizon", "corrected_status": "PRESERVED_CANON_LOCAL_SYMBOL", "scope": "no global observer-pair equality is inferred; Charles alone canonizes"},
        {"claim_id": "Q34", "claim": "historical_Xmax_packages", "prior_status": "conditional mathematics or withdrawn interpretation", "corrected_status": "PRESERVED_WITH_OVERLAY", "scope": "bytes and provenance unchanged"},
    ]


def dependency_rows() -> list[dict[str, str]]:
    return [
        {"dependency_id": "D01", "family": "founding_reciprocal_c", "dependency_on_Xmax": "none", "effect": "UNCHANGED", "reason": "clock_ruler anchor uses c_E not global spatial diameter"},
        {"dependency_id": "D02", "family": "local_Lorentz_3plus3_frame_geometry", "dependency_on_Xmax": "none_or_contextual", "effect": "UNCHANGED", "reason": "pointwise metric frame structure"},
        {"dependency_id": "D03", "family": "WRL_static_profile", "dependency_on_Xmax": "local_X_only", "effect": "RETAIN_LOCAL_X_DISTINCT", "reason": "exact local algebra survives"},
        {"dependency_id": "D04", "family": "SNe_WRL_score", "dependency_on_Xmax": "fitted_local_profile_scale", "effect": "RETAIN_OBSERVED_RELABELED", "reason": "does_not define global diameter"},
        {"dependency_id": "D05", "family": "projective_fractional_frame_math", "dependency_on_Xmax": "1D_oriented_bound", "effect": "RETAIN_UNIQUE_CONDITIONAL", "reason": "not a general distance composition law"},
        {"dependency_id": "D06", "family": "accelerating_Cartan_frame_math", "dependency_on_Xmax": "supplied_projective_profile", "effect": "RETAIN_CONDITIONAL_MATH", "reason": "physical frame interpretation remains withdrawn"},
        {"dependency_id": "D07", "family": "invariant_Xmax_1D_action_classification", "dependency_on_Xmax": "interval_endpoint", "effect": "EXACT_MATH_RETAINED_INTERPRETATION_WITHDRAWN", "reason": "pair diameter does_not imply one radial boundary"},
        {"dependency_id": "D08", "family": "finite_cell_boundary_and_seal", "dependency_on_Xmax": "possible_boundary_identification", "effect": "OPEN_JOIN", "reason": "diameter is not a surface or seal"},
        {"dependency_id": "D09", "family": "boundary_action_charge_flux", "dependency_on_Xmax": "local_surface_scale", "effect": "OPEN_UNCHANGED", "reason": "requires selected surface action and normalization"},
        {"dependency_id": "D10", "family": "scale_breaking_dimensional_theorem", "dependency_on_Xmax": "length_dimension_only", "effect": "UNCHANGED", "reason": "compactness rank theorem is type-stable"},
        {"dependency_id": "D11", "family": "matter_coefficient_scale", "dependency_on_Xmax": "hypothetical_ratio", "effect": "UNCHANGED_CONDITIONAL", "reason": "future kappa_over_xi relation remains unproved"},
        {"dependency_id": "D12", "family": "bootstrap_density_mass", "dependency_on_Xmax": "global_complete_solution", "effect": "OPEN_UNCHANGED", "reason": "native density-to-geometry and mass laws absent"},
        {"dependency_id": "D13", "family": "Hopf_carrier_and_dual_systole", "dependency_on_Xmax": "none_load_bearing", "effect": "UNCHANGED", "reason": "topology and toric transport results retain own premises"},
        {"dependency_id": "D14", "family": "complete_metric_solution_space", "dependency_on_Xmax": "future_global_pair_functional", "effect": "NEW_EXPLICIT_GATE", "reason": "must derive observer domain comparison and angular/global distance"},
        {"dependency_id": "D15", "family": "native_action_source_mass", "dependency_on_Xmax": "not_closed", "effect": "OPEN_UNCHANGED", "reason": "audit supplies no dynamics"},
    ]


def negative_rows() -> list[dict[str, str]]:
    return [
        {
            "negative_id": "N01",
            "source": "NEGATIVES_REGISTRY.md:22-47",
            "negative": "no_static_homogeneous_redshifting_field_in_declared_branch",
            "prior_frame_bearing": "centered_universe_reading_retracted_in_same_entry",
            "audit_ruling": "STANDING_ONLY_IN_RECORDED_STATIC_FIELD_SCOPE",
            "blocking_effect": "NONE_ON_RELATIONAL_XMAX",
            "reason": "field homogeneity no-go does not define observer-pair distance or preferred frame",
        },
        {
            "negative_id": "N02",
            "source": "udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23",
            "negative": "finite_invariant_bound_does_not_uniquely_select_tanh",
            "prior_frame_bearing": "one_radial_asymptotic_boundary",
            "audit_ruling": "RETAIN_NEGATIVE_REGRADE_DOMAIN",
            "blocking_effect": "BLOCKS_UNIQUE_LAW_FROM_DIAMETER_ALONE",
            "reason": "counterfamily remains valid and becomes stronger once general angular pair geometry is admitted",
        },
        {
            "negative_id": "N03",
            "source": "udt_observer_centered_xmax_frame_correction_2026-07-23",
            "negative": "fixed_WRL_tensor_cannot_be_recentered_as_one_geometry",
            "prior_frame_bearing": "fixed_static_tensor",
            "audit_ruling": "RETAINED",
            "blocking_effect": "BLOCKS_FIXED_WRL_AS_COMPLETE_PAIR_GEOMETRY",
            "reason": "curvature scalars still distinguish its radial center",
        },
        {
            "negative_id": "N04",
            "source": "scale_breaking_closure_census_2026-07-20",
            "negative": "c_E_and_G_obs_do_not_select_absolute_scale",
            "prior_frame_bearing": "Xmax_as_length",
            "audit_ruling": "RETAINED",
            "blocking_effect": "BLOCKS_SCALE_PROMOTION",
            "reason": "relational reinterpretation supplies no new dimensional equation",
        },
    ]


def main() -> None:
    candidates = read_tsv(HERE / "CANDIDATE_UNIVERSE.tsv")
    if len(candidates) != 907 or len({row["path"] for row in candidates}) != 907:
        raise AssertionError("candidate universe is not the corrected 907-path set")

    path_rows = []
    family_counts: dict[tuple[str, str], int] = defaultdict(int)
    for row in candidates:
        classification, effect, basis, load = classify(row["path"])
        top = family(row["path"])
        family_counts[(top, classification)] += 1
        path_rows.append(
            {
                "candidate_id": row["candidate_id"],
                "path": row["path"],
                "family": top,
                "classification": classification,
                "current_authority_effect": effect,
                "evidence_basis": basis,
                "load_bearing": load,
                "base_git_blob": row["git_blob"],
                "base_sha256": row["sha256"],
            }
        )
    write_tsv(
        "PATH_DISPOSITION.tsv",
        [
            "candidate_id", "path", "family", "classification",
            "current_authority_effect", "evidence_basis", "load_bearing",
            "base_git_blob", "base_sha256",
        ],
        path_rows,
    )
    write_tsv(
        "LOAD_BEARING_SOURCE_REGISTRY.tsv",
        [
            "candidate_id", "path", "classification",
            "current_authority_effect", "evidence_basis",
            "base_git_blob", "base_sha256",
        ],
        [
            {
                key: row[key]
                for key in [
                    "candidate_id", "path", "classification",
                    "current_authority_effect", "evidence_basis",
                    "base_git_blob", "base_sha256",
                ]
            }
            for row in path_rows
            if row["load_bearing"] == "YES"
        ],
    )

    family_rows = []
    for (top, classification), count in sorted(family_counts.items()):
        family_rows.append(
            {
                "family": top,
                "classification": classification,
                "path_count": count,
                "ruling_basis": next(
                    row["evidence_basis"]
                    for row in path_rows
                    if row["family"] == top and row["classification"] == classification
                ),
                "family_review": "EXPLICIT_RULE" if classification != "GENERATED_AUDIT_RECORD" else "CONTEXTUAL_NO_PROMOTION",
            }
        )
    write_tsv(
        "FAMILY_RULINGS.tsv",
        ["family", "classification", "path_count", "ruling_basis", "family_review"],
        family_rows,
    )
    write_tsv(
        "RELATIONAL_DEFINITION_LEDGER.tsv",
        ["object_id", "object", "definition_or_requirement", "status", "why"],
        relational_rows(),
    )
    write_tsv(
        "COUNTERMODEL_ATLAS.tsv",
        ["model_id", "space", "diameter", "boundary", "attained", "observer_transitive", "lesson"],
        countermodel_rows(),
    )
    write_tsv(
        "CLAIM_REGRADE.tsv",
        ["claim_id", "claim", "prior_status", "corrected_status", "scope"],
        claim_rows(),
    )
    write_tsv(
        "DEPENDENCY_IMPACT.tsv",
        ["dependency_id", "family", "dependency_on_Xmax", "effect", "reason"],
        dependency_rows(),
    )
    write_tsv(
        "NEGATIVE_REGRADE.tsv",
        ["negative_id", "source", "negative", "prior_frame_bearing", "audit_ruling", "blocking_effect", "reason"],
        negative_rows(),
    )

    X, a, b, theta, x, y = sp.symbols(
        "X a b theta x y", positive=True, finite=True
    )
    triangle_sq = sp.trigsimp(
        sp.expand((a + b * sp.cos(theta)) ** 2 + (b * sp.sin(theta)) ** 2)
    )
    projective = (x + y) / (1 + x * y / X**2)
    rapidity_addition_formula = X * (
        (x / X + y / X) / (1 + (x / X) * (y / X))
    )
    rapidity_identity = sp.factor(rapidity_addition_formula - projective)
    csn_ratio = sp.simplify((sp.Symbol("Omega", positive=True) * a) / (sp.Symbol("Omega", positive=True) * X))
    classification_counts = Counter(row["classification"] for row in path_rows)
    path_identity = hashlib.sha256(
        "\n".join(sorted(row["path"] for row in path_rows)).encode()
    ).hexdigest()
    results = {
        "schema": "udt-xmax-observer-separation-audit-v1",
        "base": BASE,
        "candidate_paths": len(path_rows),
        "candidate_path_identity_sha256": path_identity,
        "classification_counts": dict(sorted(classification_counts.items())),
        "load_bearing_sources": sum(
            row["load_bearing"] == "YES" for row in path_rows
        ),
        "family_ruling_rows": len(family_rows),
        "relational_objects": len(relational_rows()),
        "countermodels": len(countermodel_rows()),
        "claim_regrades": len(claim_rows()),
        "dependency_families": len(dependency_rows()),
        "negative_regrades": len(negative_rows()),
        "exact_controls": {
            "triangle_distance_squared": str(triangle_sq),
            "triangle_angle_dependence_derivative": str(sp.diff(triangle_sq, theta)),
            "projective_addition_formula_residual": str(rapidity_identity),
            "constant_CSN_ratio": str(csn_ratio),
            "interval_diameter_over_radius_control": "2",
            "sphere_diameter_over_radius_control": "pi",
        },
        "rulings": {
            "owner_meaning": "WORKING_OWNER_MEANING",
            "metric_derived_pair_separation": "OPEN_SELECTOR",
            "maximum_attainment": "OPEN_USE_SUPREMUM",
            "edge_from_Xmax": "NOT_DERIVED",
            "preferred_center_from_Xmax": "REFUTED_AS_LOGICAL_INFERENCE",
            "local_WRL_X_equals_global_Xmax": "OPEN_DIAMETER_RADIUS_JOIN",
            "general_fractional_pair_distance_composition": "REFUTED_IN_GENERAL",
            "projective_1D_math": "RETAINED_UNIQUE_CONDITIONAL",
            "WRL_local_math_and_SNe_score": "RETAINED_SCOPED",
            "scale_dimensional_theorem": "RETAINED_SCOPED",
            "complete_action_source_boundary_mass": "OPEN_UNCHANGED",
        },
        "smallest_missing_object": (
            "native complete-metric two-point observer separation functional "
            "including observer domain, event pairing, and angular/global completion"
        ),
        "gpu_used": False,
        "matter_or_time_live_solve": False,
        "canon_changed": False,
        "historical_or_frozen_source_changed": False,
    }
    (HERE / "RESULTS.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
