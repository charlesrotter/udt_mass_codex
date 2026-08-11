#!/usr/bin/env python3
"""Fail closed on current foundational premise and startup-precedence regressions."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent

PREMISE_REGISTRY_CONTROLS = (
    "AGENTS.md",
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "research/README.md",
    "research/_registry/README.md",
    "MEMORY.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
)

PROTECTED_ATLAS_CONTROLS = (
    "AGENTS.md",
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "MEMORY.md",
)

CURRENT_ROUTE_CONTROLS = (
    "AGENTS.md",
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "README.md",
    "research/README.md",
    "MEMORY.md",
    "CURRENT_RESEARCH_PROGRAM.md",
    "INFLIGHT_STATE.md",
)

LATEST_ROUTE_CONTROLS = (
    "LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "research/README.md",
    "research/_registry/README.md", "MEMORY.md", "CURRENT_RESEARCH_PROGRAM.md",
    "CURRENT_SCIENTIFIC_PREMISES.md", "INFLIGHT_STATE.md",
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def marked_current_block(path: Path) -> str:
    """Return the bounded startup block; fail closed on missing or duplicate markers."""
    text = path.read_text(encoding="utf-8")
    begin = "<!-- STARTUP_CURRENT_BEGIN -->"
    end = "<!-- STARTUP_CURRENT_END -->"
    require(text.count(begin) == 1, f"current-block begin marker count: {path.name}")
    require(text.count(end) == 1, f"current-block end marker count: {path.name}")
    start = text.index(begin) + len(begin)
    stop = text.index(end, start)
    return text[start:stop]


def validate_startup_surface(root: Path) -> None:
    """Validate current routing separately from the historical bodies of startup files."""
    controls: dict[str, str] = {}
    for relative in set(
        PREMISE_REGISTRY_CONTROLS + PROTECTED_ATLAS_CONTROLS + CURRENT_ROUTE_CONTROLS
        + LATEST_ROUTE_CONTROLS
    ):
        path = root / relative
        require(path.is_file(), f"missing startup control: {relative}")
        controls[relative] = path.read_text(encoding="utf-8")

    for control in PREMISE_REGISTRY_CONTROLS:
        require(
            "CURRENT_SCIENTIFIC_PREMISES.tsv" in controls[control],
            f"control lacks premise registry: {control}",
        )

    live = marked_current_block(root / "LIVE.md")
    handoff = marked_current_block(root / "HANDOFF.md")
    for name, block in (("LIVE.md", live), ("HANDOFF.md", handoff)):
        flat_block = " ".join(block.split())
        require(
            "CURRENT_SCIENTIFIC_PREMISES.tsv" in block,
            f"marked current block lacks premise registry: {name}",
        )
        for token in (
            "CMB PEAK OPTIMIZATION",
            "udt_cmb_complete_observation_query_map_2026-08-11/AUDIT_REPORT.md",
            "udt_solved_geometry_relation_family_survivor_atlas_2026-08-11/AUDIT_REPORT.md",
            "udt_complete_observer_network_assembly_from_scratch_2026-08-11/AUDIT_REPORT.md",
            "udt_native_history_restriction_from_scratch_2026-08-10/AUDIT_REPORT.md",
            "udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_pair_instrument_mixing_solution_space_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_copresent_causal_pair_functor_selector_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_complete_coframe_calibration_transport_from_scratch_2026-08-10/AUDIT_REPORT.md",
            "udt_multiregime_pair_relation_admissibility_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_ordered_observer_query_projection_ownership_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_multichannel_observer_relation_assembly_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_stationary_local_one_form_selection_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_depth_holonomy_joint_invariant_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_stationary_connection_sublocus_ownership_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_magnitude_to_grading_selection_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_nonisometric_calibration_magnitude_owner_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_reciprocal_scalar_calibration_bitorsor_descent_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_carried_intrinsic_middle_morphism_ownership_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/AUDIT_REPORT.md",
            "udt_three_observer_overlap_calibration_carry_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_calibrated_pair_map_owner_atlas_2026-08-09/AUDIT_REPORT.md",
            "udt_reciprocal_calibration_state_solder_audit_2026-08-09/AUDIT_REPORT.md",
            "udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/AUDIT_REPORT.md",
            "udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/AUDIT_REPORT.md",
            "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/AUDIT_REPORT.md",
            "udt_cmb_complete_angular_family_atlas_map_2026-08-09/AUDIT_REPORT.md",
            "udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/AUDIT_REPORT.md",
            "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/AUDIT_REPORT.md",
            "udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md",
            "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md",
            "udt_freedata_inventory_MAP_2026-08-09.md",
            "RA2-PARTIAL-WEAK",
            "BANKED + TABLED",
            "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md",
            "positional-dilation asymptote",
        ):
            require(token in flat_block, f"marked current block lacks {token}: {name}")
        lowered = block.lower()
        require("o1 pending" not in lowered, f"stale x_max O1 route in marked current block: {name}")
        require(
            "global cell assembly lane is active" not in lowered,
            f"stale Global Cell Assembly route in marked current block: {name}",
        )
        if "Global Cell Assembly" in block:
            require("ARCHIVED-LEGACY" in block, f"Global Cell Assembly not archive-stamped: {name}")
        require(
            "OPEN-COMPATIBILITY-WINDOW` is WITHDRAWN" in flat_block,
            f"corrected FD1 withdrawal absent: {name}",
        )

    protected_atlas = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
    for name, block in (("LIVE.md", live), ("HANDOFF.md", handoff)):
        for token in (protected_atlas, "83 protected untracked", "explicit later dispatch"):
            require(token in block, f"marked current block lacks protected-atlas guard {token}: {name}")

    for control in PROTECTED_ATLAS_CONTROLS:
        text = controls[control]
        for token in (protected_atlas, "83 protected untracked", "explicit later dispatch"):
            require(token in text, f"control lacks protected-atlas guard {token}: {control}")

    for control in CURRENT_ROUTE_CONTROLS:
        text = " ".join(controls[control].replace("\n> ", "\n").split())
        for token in (
            "CMB PEAK OPTIMIZATION",
            "udt_complete_observer_network_assembly_from_scratch_2026-08-11/AUDIT_REPORT.md",
            "udt_native_history_restriction_from_scratch_2026-08-10/AUDIT_REPORT.md",
            "udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_pair_instrument_mixing_solution_space_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_copresent_causal_pair_functor_selector_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_complete_coframe_calibration_transport_from_scratch_2026-08-10/AUDIT_REPORT.md",
            "udt_multiregime_pair_relation_admissibility_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_ordered_observer_query_projection_ownership_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_multichannel_observer_relation_assembly_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_depth_holonomy_joint_invariant_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_stationary_connection_sublocus_ownership_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_nonisometric_calibration_magnitude_owner_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_reciprocal_scalar_calibration_bitorsor_descent_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_carried_intrinsic_middle_morphism_ownership_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/AUDIT_REPORT.md",
            "udt_three_observer_overlap_calibration_carry_audit_2026-08-10/AUDIT_REPORT.md",
            "udt_calibrated_pair_map_owner_atlas_2026-08-09/AUDIT_REPORT.md",
            "udt_reciprocal_calibration_state_solder_audit_2026-08-09/AUDIT_REPORT.md",
            "udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/AUDIT_REPORT.md",
            "udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/AUDIT_REPORT.md",
            "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/AUDIT_REPORT.md",
            "udt_cmb_complete_angular_family_atlas_map_2026-08-09/AUDIT_REPORT.md",
            "udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/AUDIT_REPORT.md",
            "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/AUDIT_REPORT.md",
            "udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md",
            "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md",
            "udt_freedata_inventory_MAP_2026-08-09.md",
        ):
            require(token in text, f"current route lacks {token}: {control}")

    latest = "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/AUDIT_REPORT.md"
    for control in LATEST_ROUTE_CONTROLS:
        require(latest in controls[control], f"latest complete-branch route absent: {control}")

    for control in ("README.md", "research/README.md", "MEMORY.md"):
        text = controls[control]
        require("RA2-PARTIAL-WEAK" in text, f"current route loses RA2 grade: {control}")
        require("BANKED + TABLED" in text, f"current route loses BAO status: {control}")

    memory_top = " ".join(controls["MEMORY.md"].split("## Historical memory archive", 1)[0].split())
    require("2026-08-11" in memory_top, "MEMORY top pointer is not August 11 current")
    require("CMB PEAK OPTIMIZATION" in memory_top, "MEMORY top pointer is stale")
    require("RA2-PARTIAL-WEAK" in memory_top, "MEMORY top pointer loses RA2 grade")

    for relative in (
        "CURRENT_SCIENTIFIC_PREMISES.md",
        "CURRENT_SCIENTIFIC_PREMISES.tsv",
        "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/AUDIT_REPORT.md",
        "udt_cmb_complete_observation_query_map_2026-08-11/AUDIT_REPORT.md",
        "udt_cmb_complete_observation_query_map_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_solved_geometry_relation_family_survivor_atlas_2026-08-11/AUDIT_REPORT.md",
        "udt_solved_geometry_relation_family_survivor_atlas_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_complete_observer_network_assembly_from_scratch_2026-08-11/AUDIT_REPORT.md",
        "udt_native_history_restriction_from_scratch_2026-08-10/AUDIT_REPORT.md",
        "udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_pair_instrument_mixing_solution_space_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_copresent_causal_pair_functor_selector_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_complete_coframe_calibration_transport_from_scratch_2026-08-10/AUDIT_REPORT.md",
        "udt_multiregime_pair_relation_admissibility_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_ordered_observer_query_projection_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_multichannel_observer_relation_assembly_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_r17_stationary_local_one_form_selection_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_r17_depth_holonomy_joint_invariant_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_r17_stationary_connection_sublocus_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_r17_magnitude_to_grading_selection_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_nonisometric_calibration_magnitude_owner_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_reciprocal_scalar_calibration_bitorsor_descent_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_carried_intrinsic_middle_morphism_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_global_relation_family_branch_classification_2026-08-10/AUDIT_REPORT.md",
        "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/AUDIT_REPORT.md",
        "udt_three_observer_overlap_calibration_carry_audit_2026-08-10/AUDIT_REPORT.md",
        "udt_calibrated_pair_map_owner_atlas_2026-08-09/AUDIT_REPORT.md",
        "udt_reciprocal_calibration_state_solder_audit_2026-08-09/AUDIT_REPORT.md",
        "udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/AUDIT_REPORT.md",
        "udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/AUDIT_REPORT.md",
        "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/AUDIT_REPORT.md",
        "udt_cmb_complete_angular_family_atlas_map_2026-08-09/AUDIT_REPORT.md",
        "udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/AUDIT_REPORT.md",
        "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/AUDIT_REPORT.md",
        "udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md",
        "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md",
        "udt_freedata_inventory_MAP_2026-08-09.md",
        "udt_roadA_mode_quantization_MAP_2026-08-08.md",
        "udt_roadA_RA1_muon_modes_2026-08-08/DERIVATION_NOTES.md",
        "udt_roadA_RA2_projection_2026-08-08/DERIVATION_NOTES.md",
        "udt_complete_pair_phi_orchestra_audit_2026-08-05/AUDIT_REPORT.md",
    ):
        require((root / relative).is_file(), f"current startup target missing: {relative}")


def main() -> None:
    rows = read_tsv(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    require(len(rows) == 68, "premise registry must contain exactly 68 rows")
    by_id = {row["premise_id"]: row for row in rows}
    require(len(by_id) == 68, "duplicate premise id")
    require(
        by_id["G01"]["current_status"] == "DERIVED_RECIPROCAL_CHARACTER_ON_SUPPLIED_ORDERED_DEPTH",
        "founded relational character",
    )
    require(
        by_id["G02"]["current_status"]
        == "DERIVED_DELTA_MAPS_TO_DIAG_EXP_MINUS_DELTA_EXP_PLUS_DELTA",
        "founded relational character action",
    )
    require("physical complete-pair cocycle selection" in by_id["G02"]["open_scope"], "complete-pair target absent")
    require("general observer/event/path-to-depth law" in by_id["G01"]["open_scope"], "depth law promoted")
    require("universal pointwise physical scalar" in by_id["G01"]["forbidden_regression"], "pointwise owner guard absent")
    require(by_id["G03"]["active_use"] == "COMPARISON_ONLY_NOT_NATIVE", "independent phi promoted")
    require(by_id["G04"]["current_status"] == "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED", "strong local CSN status")
    require(by_id["G04"]["active_use"] == "INACTIVE_UNLESS_CHARLES_EXPLICITLY_REAUTHORIZES", "strong local CSN activated")
    require(by_id["G05"]["active_use"] == "ALGEBRA_ONLY", "common cancellation promoted")
    require(by_id["G06"]["active_use"] == "ACTIVE_CALIBRATION", "c/G anchors dropped")
    require(by_id["G07"]["active_use"] == "GENERIC_ARENA_BASELINE_ONLY", "generic metric count promoted")
    require(by_id["G08"]["epistemic_label"] == "OPEN", "4D extension promoted")
    require(by_id["G09"]["epistemic_label"] == "POSIT", "carrier promoted")
    require(by_id["G10"]["active_use"] == "INACTIVE_WITHOUT_STRONG_CSN_PREMISE", "C2/Bach promoted")
    require(by_id["G11"]["active_use"] == "NOT_SELECTED", "EH promoted")
    require(
        by_id["G12"]["current_status"]
        == "WORKING_MUTUAL_ADMISSIBILITY_POSIT__PARTIAL_KINEMATIC_JOIN_DERIVED__SMOOTH_EXTENSION_CARTAN_NONSELECTION__FULL_FIRST_AND_SECOND_JET_CURVATURE_ATLASES_DERIVED__CONDITIONAL_LOCAL_SAME_SOLUTION_PHI_CURVATURE_COMPATIBILITY__GLOBAL_FACTORIZATION_GROUPOID_AND_OVERLAP_NONSELECTION_DERIVED__FOUNDING_RELATIONAL_CHARACTER_ON_SUPPLIED_DEPTH_DERIVED__POINTWISE_PHI_PRESENTATION_POTENTIAL_ON_SUPPLIED_FACTORIZATION__CONDITIONAL_STATIONARY_KILLING_DEPTH__COMPLETE_PAIR_ORCHESTRA_MODULATION_AND_GROUPOID_COCYCLE_HOME_DERIVED__PHYSICAL_COMPLETE_PAIR_COCYCLE_AND_COMPLETE_RETURN_OPEN",
        "bootstrap status regressed or promoted",
    )
    require(by_id["G12"]["active_use"] == "FALSIFIABLE_RELATIONAL_ARCHITECTURE_ONLY", "bootstrap use changed")
    require("complete-arrow strain or spectral magnitude promoted" in by_id["G12"]["forbidden_regression"], "orchestra promotion guard absent")
    require(by_id["G13"]["active_use"] == "TORIC_GEOMETRY_ONLY", "Maxwell promoted")
    require(
        by_id["G14"]["current_status"] == "WORKING_FOUNDATIONAL_POSITIONAL_DILATION_ASYMPTOTE",
        "Xmax limiting role reopened or promoted",
    )
    require(
        by_id["G14"]["active_use"] == "OWNER_RATIFIED_LIMIT_FRAME_AND_REQUIRED_DEPTH_LAW_GATE",
        "Xmax workflow gate mistyped",
    )
    require("numerical value" in by_id["G14"]["open_scope"], "numerical Xmax promoted")
    require("all-frame theorem" in by_id["G14"]["open_scope"], "Xmax frame theorem promoted")
    require("material wall" in by_id["G14"]["forbidden_regression"], "Xmax wall guard absent")
    require(by_id["G15"]["active_use"] == "STATIC_FINITE_BOX_AND_CARRIER_CONDITIONAL", "Hopfion promoted")
    require(by_id["G16"]["current_status"] == "OPEN", "complete physics promoted")
    require(
        by_id["G17"]["current_status"] == "KEPT_MULTIPLY_ANCHORED_SPLIT_FROM_MIRROR_CLAUSE",
        "finite-cell split reading changed",
    )
    require(by_id["G17"]["active_use"] == "ACTIVE_FOUNDATION_SPLIT_READING", "finite-cell split inactive")
    require(
        by_id["G18"]["current_status"] == "OWNER_RATIFIED_PROPOSAL_NOT_DERIVED_SPLIT_RULED_2026-07-30",
        "mirror closure promoted or dropped",
    )
    require(
        by_id["G18"]["active_use"] == "WORKING_PREMISE_ONLY_STAMPS_TRAVEL_VIA_CONSUMER_LEDGER",
        "mirror closure use changed",
    )
    require(by_id["G19"]["active_use"] == "CONFIGURATION_ARENA_ONLY", "coframe promoted")
    require(by_id["G20"]["active_use"] == "NO_UNIVERSAL_VARIATION_DOMAIN_SELECTED", "variation owner promoted")
    require("query varied as field" in by_id["G20"]["forbidden_regression"], "query variation guard absent")
    require(by_id["G21"]["current_status"] == "OPEN_RESPONSE_OR_CURRENT_ROLE_NOT_SUBSTANCE", "source mistyped")
    require(by_id["G22"]["active_use"] == "NO_UNCONDITIONAL_MASS_CLAIM", "mass promoted")
    require(by_id["G23"]["active_use"] == "SEMANTIC_FRAME_ONLY", "copresence promoted")
    require("instantaneous access" in by_id["G23"]["forbidden_regression"], "copresence signal guard absent")
    require(by_id["G24"]["active_use"] == "GEOMETRIC_REACHABILITY_ONLY", "causal access promoted")
    require(by_id["G25"]["active_use"] == "TYPE_GUARD_ONLY", "boundary type guard promoted")
    require("Xmax" in by_id["G25"]["forbidden_regression"], "Xmax/boundary guard absent")
    require(by_id["G26"]["active_use"] == "NO_CARRIER_EMERGENCE_CLAIM", "angular carrier promoted")
    require(by_id["G27"]["active_use"] == "NO_ORDER_SELECTED", "action/closure order selected")
    require(
        by_id["G28"]["current_status"]
        == "DERIVED_COMPLETE_ARROW_MODULATION_AND_GROUPOID_COCYCLE_HOME__UNIQUE_PHYSICAL_COCYCLE_OPEN",
        "complete-pair orchestra status regressed or promoted",
    )
    require(by_id["G28"]["epistemic_label"] == "DERIVED", "complete-pair orchestra label changed")
    require(by_id["G28"]["active_use"] == "ACTIVE_RELATIONAL_STRUCTURE", "complete-pair orchestra use changed")
    require("metric-natural physical cocycle selection" in by_id["G28"]["open_scope"], "physical cocycle open scope absent")
    require("angular sector held external" in by_id["G28"]["forbidden_regression"], "prior counterexample narrowing guard absent")
    require("stationary screen-modulated family promoted" in by_id["G28"]["forbidden_regression"], "stationary premise guard absent")
    require(
        by_id["G28"]["controlling_source"]
        == "udt_complete_pair_phi_orchestra_audit_2026-08-05/AUDIT_REPORT.md",
        "complete-pair orchestra source changed",
    )
    require(
        by_id["G29"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__THREE_INTERLEAVED_ANGULAR_LADDERS__OLD_SAME_INDEX_MULTIPLET_WINDOW_WITHDRAWN",
        "corrected FD1 status regressed or promoted",
    )
    require(by_id["G29"]["epistemic_label"] == "OBSERVED", "corrected FD1 label changed")
    require(
        by_id["G29"]["active_use"] == "CORRECTED_SCALAR_SLICE_BACKGROUND_GEOMETRY_ONLY",
        "corrected FD1 use promoted",
    )
    require("mode-family ownership" in by_id["G29"]["open_scope"], "FD1 mode-family gate absent")
    require(
        "old FD1 open compatibility window revived" in by_id["G29"]["forbidden_regression"],
        "old FD1 window revival guard absent",
    )
    require(
        "best standalone ladder postselected" in by_id["G29"]["forbidden_regression"],
        "FD1 postselection guard absent",
    )
    require(
        by_id["G29"]["controlling_source"]
        == "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md",
        "corrected FD1 source changed",
    )
    require(
        by_id["G30"]["current_status"]
        == "DERIVED_CONDITIONAL_U1_MODE_DECOMPOSITION__FD1_ROOTS_DO_NOT_LIFT__PHYSICAL_COMPLETE_LIFT_AND_POPULATION_PROJECTION_OPEN",
        "complete-angular ownership status regressed or promoted",
    )
    require(by_id["G30"]["epistemic_label"] == "MIXED", "complete-angular ownership label changed")
    require(by_id["G30"]["active_use"] == "FULL_ANGULAR_REGRESSION_GATE_ONLY", "complete-angular ownership use promoted")
    require("physical complete angular screen" in by_id["G30"]["open_scope"], "complete-angular lift promoted")
    require("equatorial roots relabeled full-angular" in by_id["G30"]["forbidden_regression"], "full-angular relabel guard absent")
    require("symmetry projector promoted to population law" in by_id["G30"]["forbidden_regression"], "population projection guard absent")
    require(
        by_id["G30"]["controlling_source"]
        == "udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md",
        "complete-angular ownership source changed",
    )
    require(
        by_id["G31"]["current_status"]
        == "VERIFIED_DESIGN_MAP__GENERAL_STATIONARY_SCREEN_OPERATOR_DERIVED__PHYSICAL_SCREEN_AND_SOLVES_OPEN",
        "complete-angular family-map status regressed or promoted",
    )
    require(by_id["G31"]["epistemic_label"] == "MIXED", "complete-angular family-map label changed")
    require(by_id["G31"]["active_use"] == "ARCHITECTURE_AND_REGRESSION_GATE_ONLY", "family map promoted")
    require("physical complete angular screen" in by_id["G31"]["open_scope"], "physical screen promoted")
    require("axial shortcut applied" in by_id["G31"]["forbidden_regression"], "general-shift guard absent")
    require("C1 promoted to native screen" in by_id["G31"]["forbidden_regression"], "C1 promotion guard absent")
    require("FD2 called authorized" in by_id["G31"]["forbidden_regression"], "FD2 authorization guard absent")
    require(
        by_id["G31"]["controlling_source"]
        == "udt_cmb_complete_angular_family_atlas_map_2026-08-09/AUDIT_REPORT.md",
        "complete-angular family-map source changed",
    )
    require(
        by_id["G32"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__CONDITIONAL_C1_FIXED_ABS_M_PARITY_MATRIX_ARCHITECTURE__NO_EIGENSOLVE",
        "N01 coupling status regressed or promoted",
    )
    require(by_id["G32"]["epistemic_label"] == "MIXED", "N01 coupling label changed")
    require(
        by_id["G32"]["active_use"] == "BOUNDED_COUPLING_ARCHITECTURE_AND_REGRESSION_CONTROL_ONLY",
        "N01 coupling use promoted",
    )
    require("physical B(r)" in by_id["G32"]["open_scope"], "N01 physical profile promoted")
    require("negative m discarded" in by_id["G32"]["forbidden_regression"], "N01 sign guard absent")
    require("scalar Box_g promoted" in by_id["G32"]["forbidden_regression"], "N01 probe guard absent")
    require("FD2" in by_id["G32"]["forbidden_regression"], "N01 FD2 guard absent")
    require(
        by_id["G32"]["controlling_source"]
        == "udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/AUDIT_REPORT.md",
        "N01 coupling source changed",
    )
    require(
        by_id["G33"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__NO_BANKED_P1_REGULAR_COMPLETE_C1_C2_CENTER_TO_WALL_ANCHOR__NO_EIGENSOLVE",
        "N02 admissibility status regressed or promoted",
    )
    require(by_id["G33"]["epistemic_label"] == "MIXED", "N02 admissibility label changed")
    require(
        by_id["G33"]["active_use"] == "RADIAL_ADMISSIBILITY_AND_REGRESSION_GATE_ONLY",
        "N02 admissibility use promoted",
    )
    require("regular complete profile" in by_id["G33"]["open_scope"], "N02 regular profile promoted")
    require("P1 relational or SNe role called invalid" in by_id["G33"]["forbidden_regression"], "N02 P1 role guard absent")
    require("D or N called physically selected" in by_id["G33"]["forbidden_regression"], "N02 boundary guard absent")
    require("N02 eigensolve" in by_id["G33"]["forbidden_regression"], "N02 execution guard absent")
    require(
        by_id["G33"]["controlling_source"]
        == "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/AUDIT_REPORT.md",
        "N02 admissibility source changed",
    )
    require(
        by_id["G34"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__NO_MAPPED_ROLE_CORRECT_COMPLETE_GLOBAL_PROFILE__REGULAR_C1_LOCAL_JETS_NONEMPTY__PHYSICAL_GROUPOID_COCYCLE_OPEN",
        "N03 profile-role status regressed or promoted",
    )
    require(by_id["G34"]["epistemic_label"] == "MIXED", "N03 profile-role label changed")
    require(
        by_id["G34"]["active_use"] == "PROFILE_ROLE_CENTER_REGULARITY_AND_REGRESSION_GATE_ONLY",
        "N03 profile-role use promoted",
    )
    require("metric-natural physical groupoid cocycle" in by_id["G34"]["open_scope"], "N03 cocycle selected")
    require("P1 observer-pair or SNe role called invalid" in by_id["G34"]["forbidden_regression"], "N03 P1 role guard absent")
    require("k0 called selected invariant" in by_id["G34"]["forbidden_regression"], "N03 k0 guard absent")
    require("transport or connection called derived" in by_id["G34"]["forbidden_regression"], "N03 transport guard absent")
    require("Xmax called a wall" in by_id["G34"]["forbidden_regression"], "N03 Xmax guard absent")
    require(
        by_id["G34"]["controlling_source"]
        == "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/AUDIT_REPORT.md",
        "N03 profile-role source changed",
    )
    require(
        by_id["G35"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ABSTRACT_RECIPROCAL_CALIBRATION_SEED_DERIVED__RECIPROCAL_ROOT_CONDITIONAL_UNIQUE_UNIVERSAL_ORDER_ZERO_READOUT__PHYSICAL_FLAG_ARROW_CALIBRATION_OPEN",
        "reciprocal-flag ownership status regressed or promoted",
    )
    require(by_id["G35"]["epistemic_label"] == "MIXED", "reciprocal-flag label changed")
    require(
        by_id["G35"]["active_use"] == "FOUNDATION_OWNERSHIP_AND_REGRESSION_GATE_ONLY",
        "reciprocal-flag result promoted",
    )
    require("pair-relative physical flag" in by_id["G35"]["open_scope"], "physical flag selected")
    require("physical comparison or calibration morphism" in by_id["G35"]["open_scope"], "physical arrow selected")
    require("timelike-strain eigenvalue called a general cocycle" in by_id["G35"]["forbidden_regression"], "strain cocycle guard absent")
    require("K called a causal Lorentz exchange" in by_id["G35"]["forbidden_regression"], "K type guard absent")
    require("arbitrary higher-jet nonmetric connection selected" in by_id["G35"]["forbidden_regression"], "connection-selection guard absent")
    require(
        by_id["G35"]["controlling_source"]
        == "udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/AUDIT_REPORT.md",
        "reciprocal-flag ownership source changed",
    )
    require(
        by_id["G36"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ABSTRACT_CALIBRATION_LINE_DERIVED__PAIR_FLAG_CONDITIONAL_REGULAR_QUERY__NO_NONZERO_ORDER_ZERO_OR_FIRST_METRIC_JET_NATURAL_SOLDER__STATIONARY_KILLING_SOLDER_CONDITIONAL__GENERAL_BILOCAL_GLOBAL_FUNCTOR_OPEN",
        "calibration-state solder status regressed or promoted",
    )
    require(by_id["G36"]["epistemic_label"] == "MIXED", "calibration-state solder label changed")
    require(
        by_id["G36"]["active_use"] == "LOCAL_SOLDER_NOGO_AND_GLOBAL_OWNER_ROUTING_GATE_ONLY",
        "calibration-state solder result promoted",
    )
    require("complete-branch calibration owner" in by_id["G36"]["open_scope"], "global owner selected")
    require("physical c_eff trivialization" in by_id["G36"]["open_scope"], "physical c_eff join selected")
    require("coordinate identity called physical" in by_id["G36"]["forbidden_regression"], "coordinate identity guard absent")
    require("stationary Killing ratio called universal" in by_id["G36"]["forbidden_regression"], "Killing branch promoted")
    require("scoped local no-go generalized to all geometry" in by_id["G36"]["forbidden_regression"], "no-go scope guard absent")
    require(
        by_id["G36"]["controlling_source"]
        == "udt_reciprocal_calibration_state_solder_audit_2026-08-09/AUDIT_REPORT.md",
        "calibration-state solder source changed",
    )
    require(
        by_id["G37"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__PAIR_METRIC_DECOMPOSITION_DERIVED_ON_SUPPLIED_REGULAR_A_CALIBRATED_PAIR_METRIC__PHI_UNIQUE_RECIPROCAL_LOG_IMBALANCE_WITHIN_FIXED_CALIBRATION__PHYSICAL_PAIR_MAP_CEFF_AND_CALIBRATION_OWNER_OPEN",
        "terminal pair-metric readout status regressed or promoted",
    )
    require(by_id["G37"]["epistemic_label"] == "MIXED", "terminal pair readout label changed")
    require(
        by_id["G37"]["active_use"] == "ACTIVE_TERMINAL_READOUT_AND_PAIR_MAP_ROUTING_GATE_ONLY",
        "terminal pair readout use promoted",
    )
    require("physical calibrated pair surface" in by_id["G37"]["open_scope"], "pair surface selected")
    require("physical calibration-state owner" in by_id["G37"]["open_scope"], "calibration owner selected")
    require("signed cocycle-type composition" in by_id["G37"]["open_scope"], "signed composition selected")
    require("universal mixed-geometry c_eff" in by_id["G37"]["open_scope"], "physical c_eff promoted")
    require("pair metric claimed derived from complete metric alone" in by_id["G37"]["forbidden_regression"], "pair-map type guard absent")
    require("calibration state called eliminated" in by_id["G37"]["forbidden_regression"], "calibration-state guard absent")
    require("signed cocycle requirement withdrawn" in by_id["G37"]["forbidden_regression"], "signed-cocycle guard absent")
    require(
        by_id["G37"]["controlling_source"]
        == "udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/AUDIT_REPORT.md",
        "terminal pair-metric readout source changed",
    )
    require(
        by_id["G38"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__LOCAL_ORTHOGONAL_EXPONENTIAL_TUBE_DERIVED_FROM_METRIC_AND_FULL_DECLARED_QUERY__NO_UNIQUE_UNIVERSAL_PAIR_MAP_FROM_BARE_ENDPOINTS__PHYSICAL_CALIBRATED_PAIR_RELATION_FUNCTOR_OPEN",
        "pair-map owner atlas status changed",
    )
    require(by_id["G38"]["epistemic_label"] == "MIXED", "pair-map atlas label changed")
    require(
        by_id["G38"]["active_use"]
        == "ACTIVE_PAIR_MAP_OWNERSHIP_AND_NEXT_FUNCTOR_ROUTING_GATE_ONLY",
        "pair-map atlas use changed",
    )
    require("event pairing" in by_id["G38"]["open_scope"], "event pairing selected")
    require("middle calibration-state update" in by_id["G38"]["open_scope"], "middle update selected")
    require("branch-labelled global relation" in by_id["G38"]["open_scope"], "global branch selected")
    require("local exponential tube called universally selected" in by_id["G38"]["forbidden_regression"], "local-to-global guard absent")
    require("Killing norm called terminal pair depth without TL=1" in by_id["G38"]["forbidden_regression"], "stationary join guard absent")
    require("reciprocal reset called common-scale gauge" in by_id["G38"]["forbidden_regression"], "reset guard absent")
    require(
        by_id["G38"]["controlling_source"]
        == "udt_calibrated_pair_map_owner_atlas_2026-08-09/AUDIT_REPORT.md",
        "pair-map owner atlas source changed",
    )
    require(
        by_id["G39"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__FOUNDED_ORDERED_DEPTH_CHARACTER_DERIVED__COMPLETE_CALIBRATED_QUERY_CONDITIONAL_LOCAL_ENRICHMENT__CE_CALIBRATION_NOT_RELATION_SELECTOR__ASSOCIATIVE_MIDDLE_CARRY_OPEN",
        "founding pair-relation ownership status changed",
    )
    require(by_id["G39"]["epistemic_label"] == "MIXED", "pair-relation ownership label changed")
    require(
        by_id["G39"]["active_use"]
        == "ACTIVE_QUERY_OWNERSHIP_AND_THREE_OBSERVER_OVERLAP_ROUTING_GATE_ONLY",
        "pair-relation ownership use changed",
    )
    require("associative calibration carry" in by_id["G39"]["open_scope"], "middle carry promoted")
    require("triple-overlap and loop obstruction" in by_id["G39"]["open_scope"], "overlap gate absent")
    require("ordering called a unique physical arrow" in by_id["G39"]["forbidden_regression"], "ordered-pair guard absent")
    require("c_E called a simultaneity path or branch selector" in by_id["G39"]["forbidden_regression"], "c_E selector guard absent")
    require("Reciprocity called an existence or uniqueness theorem" in by_id["G39"]["forbidden_regression"], "Reciprocity selector guard absent")
    require(
        by_id["G39"]["controlling_source"]
        == "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/AUDIT_REPORT.md",
        "pair-relation ownership source changed",
    )
    require(
        by_id["G40"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__CARRY_ASSOCIATIVITY_DERIVED_ON_MATCHED_ENRICHED_OBJECTS__DIRECT_EQUALS_COMPOSITE_IS_CECH_DESCENT_OR_PATH_INDEPENDENCE__TRIANGLE_LOOP_OBSTRUCTION_TYPED__PHYSICAL_GLOBAL_RELATION_FAMILY_AND_SCALAR_REDUCTION_OPEN",
        "three-observer overlap status regressed or promoted",
    )
    require(by_id["G40"]["epistemic_label"] == "MIXED", "three-observer overlap label changed")
    require(
        by_id["G40"]["active_use"]
        == "ACTIVE_OVERLAP_TYPE_AND_GLOBAL_RELATION_FAMILY_ROUTING_GATE_ONLY",
        "three-observer overlap use promoted",
    )
    require("global relation-family type" in by_id["G40"]["open_scope"], "global family selected")
    require("reciprocal scalar reduction" in by_id["G40"]["open_scope"], "scalar reduction selected")
    require("associativity conflated with path independence" in by_id["G40"]["forbidden_regression"], "associativity type guard absent")
    require("M_B set to identity" in by_id["G40"]["forbidden_regression"], "middle-transition guard absent")
    require("atlas called fully independently re-derived" in by_id["G40"]["forbidden_regression"], "independent-scope guard absent")
    require(
        by_id["G40"]["controlling_source"]
        == "udt_three_observer_overlap_calibration_carry_audit_2026-08-10/AUDIT_REPORT.md",
        "three-observer overlap source changed",
    )
    require("G40_OPERATIONALLY_REFINES_G39" in by_id["G40"]["precedence_rule"], "G39 refinement absent")
    require(
        by_id["G41"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__24_IDENTITIES_57_ALIASES__PATH_HOLONOMY_ENDPOINT_CLOCK_AND_STRATIFIED_SET_VALUED_GEOMETRIC_FAMILIES_SURVIVE__PHYSICAL_NONISOMETRIC_PAIR_FUNCTOR_AND_SCALAR_REDUCTION_OPEN",
        "global relation-family branch status regressed or promoted",
    )
    require(by_id["G41"]["epistemic_label"] == "MIXED", "global family classification label changed")
    require(
        by_id["G41"]["active_use"]
        == "ACTIVE_COMPLETE_BRANCH_FAMILY_CLASSIFICATION_AND_ROUTING_GATE_ONLY",
        "global family classification use promoted",
    )
    require("branch-derived non-isometric calibration transition" in by_id["G41"]["open_scope"], "non-isometric transition selected")
    require("mixed scalar reciprocal character" in by_id["G41"]["open_scope"], "mixed scalar selected")
    require("geometric Levi-Civita path groupoid called physical depth" in by_id["G41"]["forbidden_regression"], "path/depth guard absent")
    require("W02 clock coboundary called complete pair without TL=1" in by_id["G41"]["forbidden_regression"], "clock-only scope guard absent")
    require("toric projector set called calibrated pair arrow" in by_id["G41"]["forbidden_regression"], "toric type guard absent")
    require(
        by_id["G41"]["controlling_source"]
        == "udt_global_relation_family_branch_classification_2026-08-10/AUDIT_REPORT.md",
        "global family classification source changed",
    )
    require("G41_REFINES_G40_GLOBAL_FAMILY_TYPE" in by_id["G41"]["precedence_rule"], "G40 refinement absent")
    require(
        by_id["G42"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__R17_SEMIDIRECT_FORMULA_EXACT_ON_MATCHED_PATH_CARRIED_STATES__CONDITIONAL_ASSEMBLY_NOT_BRANCH_OWNED__ZERO_BRANCH_OWNED_COMPLETE_TRANSITIONS",
        "branch-transition ownership correction regressed or promoted",
    )
    require(by_id["G42"]["epistemic_label"] == "MIXED", "branch-transition label changed")
    require(
        by_id["G42"]["active_use"]
        == "ACTIVE_BRANCH_TRANSITION_OWNERSHIP_CORRECTION_AND_NEXT_MIDDLE_MORPHISM_GATE_ONLY",
        "branch-transition use promoted",
    )
    require("carried-to-rebuilt middle morphism M_B" in by_id["G42"]["open_scope"], "M_B selected")
    require("pair-surface integrability" in by_id["G42"]["open_scope"], "pair surface selected")
    require("R17 semidirect assembly called branch-owned" in by_id["G42"]["forbidden_regression"], "R17 ownership guard absent")
    require("M_B set to identity" in by_id["G42"]["forbidden_regression"], "G42 middle-transition guard absent")
    require("terminal carried-flag equality called universal mixed-geometry c_eff" in by_id["G42"]["forbidden_regression"], "G42 c_eff guard absent")
    require(
        by_id["G42"]["controlling_source"]
        == "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/AUDIT_REPORT.md",
        "branch-transition source changed",
    )
    require("G42_REFINES_G41_TRANSITION_OWNERSHIP" in by_id["G42"]["precedence_rule"], "G41 transition refinement absent")
    require(
        by_id["G43"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__REGULAR_C01_C06_PROJECTOR_ALIGNMENTS_FORM_PATH_LABELLED_SO2_BITORSORS__BALANCED_REPRESENTATIVE_FREE_COMPOSITION_EXACT__NO_SCREEN_PHASE_SELECTED__CALIBRATION_AND_SCALAR_DESCENT_OPEN",
        "middle-morphism ownership status regressed or promoted",
    )
    require(by_id["G43"]["epistemic_label"] == "MIXED", "middle-morphism label changed")
    require(
        by_id["G43"]["active_use"]
        == "ACTIVE_PROJECTOR_ALIGNMENT_GAUGE_GROUPOID_AND_NEXT_SCALAR_CALIBRATION_DESCENT_GATE_ONLY",
        "middle-morphism use promoted",
    )
    require("calibration-density descent" in by_id["G43"]["open_scope"], "calibration descent selected")
    require("terminal reciprocal scalar descent" in by_id["G43"]["open_scope"], "scalar descent selected")
    require("double-coset shadow called a group" in by_id["G43"]["forbidden_regression"], "double-coset guard absent")
    require("path labels or holonomy erased" in by_id["G43"]["forbidden_regression"], "path-label guard absent")
    require("projector alignment called calibration-density alignment" in by_id["G43"]["forbidden_regression"], "calibration-promotion guard absent")
    require(
        by_id["G43"]["controlling_source"]
        == "udt_carried_intrinsic_middle_morphism_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "middle-morphism controlling source changed",
    )
    require("G43_REFINES_G42_MIDDLE_MORPHISM" in by_id["G43"]["precedence_rule"], "G42 middle-morphism refinement absent")
    require(
        by_id["G44"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__SUPPLIED_RECIPROCAL_READOUTS_DESCEND_THROUGH_REGULAR_C01_C06_SO2_ALIGNMENT_BITORSORS__BALANCED_DENSITY_TELESCOPING_EXACT__ISOMETRIC_ALIGNMENT_GENERATES_ZERO_CALIBRATION__PHYSICAL_NONISOMETRIC_MAGNITUDE_OWNER_OPEN",
        "reciprocal scalar descent status regressed or promoted",
    )
    require(by_id["G44"]["epistemic_label"] == "MIXED", "reciprocal scalar descent label changed")
    require(
        by_id["G44"]["active_use"]
        == "ACTIVE_SCALAR_DESCENT_CORRECTION_AND_NEXT_NONISOMETRIC_CALIBRATION_OWNER_GATE_ONLY",
        "reciprocal scalar descent use promoted",
    )
    require("physical non-isometric calibration magnitude and its owner" in by_id["G44"]["open_scope"], "calibration owner selected")
    require("selection of delta_RF or R17 as the physical law" in by_id["G44"]["open_scope"], "conditional readout selected")
    require("terminal determinant formula used without normalized source calibration" in by_id["G44"]["forbidden_regression"], "source-normalization guard absent")
    require("isometric alignment called a nonzero magnitude generator" in by_id["G44"]["forbidden_regression"], "zero-generation guard absent")
    require("path labels or holonomy erased" in by_id["G44"]["forbidden_regression"], "G44 path-label guard absent")
    require(
        by_id["G44"]["controlling_source"]
        == "udt_reciprocal_scalar_calibration_bitorsor_descent_audit_2026-08-10/AUDIT_REPORT.md",
        "reciprocal scalar descent source changed",
    )
    require("G44_REFINES_G43_BY_DERIVING_SCREEN_GAUGE_DESCENT" in by_id["G44"]["precedence_rule"], "G43 scalar-descent refinement absent")
    require(
        by_id["G45"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__R17_R18_OWN_BRANCH_CONDITIONAL_ENDPOINT_CLOCK_MAGNITUDES__ZERO_COMPLETE_PHYSICAL_MAGNITUDE_OWNERS__R17_RECIPROCAL_LIFT_SELECTION_AND_R18_RULER_COMPLETION_OPEN",
        "magnitude-owner status regressed or promoted",
    )
    require(by_id["G45"]["epistemic_label"] == "MIXED", "magnitude-owner label changed")
    require(
        by_id["G45"]["active_use"]
        == "ACTIVE_BRANCH_CONDITIONAL_MAGNITUDE_OWNER_CORRECTION_AND_NEXT_R17_MAGNITUDE_TO_GRADING_SELECTION_GATE_ONLY",
        "magnitude-owner use promoted",
    )
    require("R17 selection of the non-isometric reciprocal lift" in by_id["G45"]["open_scope"], "R17 lift selected")
    require("R18 intrinsic ruler scale" in by_id["G45"]["open_scope"], "R18 ruler completion selected")
    require("native dynamical or bootstrap calibration return" in by_id["G45"]["open_scope"], "bootstrap return invented")
    require("R17 delta_K ownership confused with semidirect assembly ownership" in by_id["G45"]["forbidden_regression"], "R17 type guard absent")
    require("R18 clock magnitude called a complete reciprocal law" in by_id["G45"]["forbidden_regression"], "R18 completion guard absent")
    require("bounded 24x5 negative generalized to all metrics" in by_id["G45"]["forbidden_regression"], "bounded-scope guard absent")
    require(
        by_id["G45"]["controlling_source"]
        == "udt_nonisometric_calibration_magnitude_owner_audit_2026-08-10/AUDIT_REPORT.md",
        "magnitude-owner source changed",
    )
    require("G45_REFINES_G44_BY_LOCATING_TWO_BRANCH_CONDITIONAL_CLOCK_MAGNITUDES" in by_id["G45"]["precedence_rule"], "G44 magnitude-owner refinement absent")
    require(
        by_id["G46"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__FOUNDED_NONZERO_DEPTH_FIXES_CLOCK_RULER_WEIGHTS__SUPPLIED_COMPLETE_C01_C06_COFRAME_FIXES_VERTICAL_RECIPROCAL_METRIC_CLASS_MOD_SO2__FULL_PHYSICAL_ARROW_OPEN",
        "R17 magnitude-to-grading result regressed or promoted",
    )
    require(by_id["G46"]["epistemic_label"] == "MIXED", "R17 selector label changed")
    require(
        by_id["G46"]["active_use"]
        == "ACTIVE_COMPLETE_COFRAME_CONDITIONAL_VERTICAL_METRIC_CLASS_AND_NEXT_R17_INTEGRABILITY_PAIR_SURFACE_GATE_ONLY",
        "R17 selector use promoted",
    )
    require("metric-owned R17 integrability or relation-family condition" in by_id["G46"]["open_scope"], "R17 integrability invented")
    require("physical pair-surface family" in by_id["G46"]["open_scope"], "R17 pair surface selected")
    require("R17 branch and lambda selection" in by_id["G46"]["open_scope"], "R17 branch or lambda selected")
    require("pair-only Reciprocity said to fix the screen" in by_id["G46"]["forbidden_regression"], "pair-only screen guard absent")
    require("vertical metric factor called the complete physical arrow" in by_id["G46"]["forbidden_regression"], "vertical/full-arrow type guard absent")
    require("G42 demotion reversed" in by_id["G46"]["forbidden_regression"], "G42 precedence guard absent")
    require(
        by_id["G46"]["controlling_source"]
        == "udt_r17_magnitude_to_grading_selection_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 selector source changed",
    )
    require("G46_REFINES_G45_BY_FIXING_THE_COMPLETE_COFRAME_CONDITIONAL_VERTICAL_METRIC_CLASS_MOD_SO2" in by_id["G46"]["precedence_rule"], "G45 R17 selector refinement absent")
    require(
        by_id["G47"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__GLOBAL_R_X_S1_INTRINSIC_PAIR_FOLIATION_ON_SUPPLIED_C01_C06__LEAF_METRIC_DET_MINUS1_AND_TERMINAL_PHI__4D_SCREEN_NONINTEGRABLE_NORMAL_BUNDLE__FULL_NORMAL_CARRY_AND_PHYSICAL_ARROW_OPEN",
        "R17 pair-foliation status regressed or promoted",
    )
    require(by_id["G47"]["epistemic_label"] == "MIXED", "R17 pair-foliation label changed")
    require(
        by_id["G47"]["active_use"]
        == "ACTIVE_R17_PAIR_SURFACE_CLOSURE_AND_NEXT_NORMAL_BUNDLE_HOLONOMY_GATE_ONLY",
        "R17 pair-foliation use promoted",
    )
    require("cross-leaf common pair surface" in by_id["G47"]["open_scope"], "cross-leaf surface selected")
    require("normal-bundle connection carry and holonomy" in by_id["G47"]["open_scope"], "normal carry promoted")
    require("four-dimensional normal bundle called a literal contact structure" in by_id["G47"]["forbidden_regression"], "4D contact type guard absent")
    require("endpoint scalar called a common cross-leaf pair surface" in by_id["G47"]["forbidden_regression"], "same-leaf depth promotion guard absent")
    require(
        by_id["G47"]["controlling_source"]
        == "udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 pair-foliation source changed",
    )
    require("G47_REFINES_G46_BY_CLOSING_THE_SUPPLIED_R17_PAIR_FOLIATION_AND_LEAF_DEPTH" in by_id["G47"]["precedence_rule"], "G46 pair-foliation refinement absent")
    require(
        by_id["G48"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__METRIC_PROJECTED_NORMAL_CONNECTION_AND_LEAF_CURVATURE_DERIVED_ON_SUPPLIED_C01_C06__LAMBDA_MINUS_ONE_FLAT_AND_LAMBDA_ZERO_HOPF_BASIC_ROLES_DISTINCT__PHYSICAL_PATH_AND_COMPLETE_ARROW_OPEN",
        "R17 normal-holonomy status regressed or promoted",
    )
    require(by_id["G48"]["epistemic_label"] == "MIXED", "R17 normal-holonomy label changed")
    require(
        by_id["G48"]["active_use"]
        == "ACTIVE_R17_NORMAL_HOLONOMY_CLASSIFICATION_AND_NEXT_GLOBAL_CONNECTION_DECOMPOSITION_GATE_ONLY",
        "R17 normal-holonomy use promoted",
    )
    require("physical cross-leaf base path" in by_id["G48"]["open_scope"], "cross-leaf path selected")
    require("vertical horizontal and mixed curvature decomposition" in by_id["G48"]["open_scope"], "global connection decomposition invented")
    require("lambda minus one flatness called branch selection" in by_id["G48"]["forbidden_regression"], "flat-branch selection guard absent")
    require("lambda zero Hopf-basicness called branch selection" in by_id["G48"]["forbidden_regression"], "Hopf-basic branch-selection guard absent")
    require("wound holonomy erased because curvature is zero" in by_id["G48"]["forbidden_regression"], "winding holonomy guard absent")
    require("horizontal lift said to select a base path" in by_id["G48"]["forbidden_regression"], "horizontal-lift ownership guard absent")
    require(
        by_id["G48"]["controlling_source"]
        == "udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 normal-holonomy source changed",
    )
    require("G48_REFINES_G47_BY_DERIVING_THE_SUPPLIED_R17_PAIR_LEAF_NORMAL_CONNECTION_AND_HOLONOMY_CLASSIFICATION" in by_id["G48"]["precedence_rule"], "G47 normal-holonomy refinement absent")
    require(
        by_id["G49"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__COMPLETE_METRIC_PROJECTED_H_CONNECTION_AND_PATH_FUNCTOR_ON_SUPPLIED_REGULAR_STATIONARY_R17__FULL_CURVATURE_GENERALLY_NONZERO__PATH_SELECTION_AND_PHYSICAL_ARROW_OPEN",
        "R17 complete path-connection status regressed or promoted",
    )
    require(by_id["G49"]["epistemic_label"] == "MIXED", "R17 complete path-connection label changed")
    require(
        by_id["G49"]["active_use"]
        == "ACTIVE_R17_COMPLETE_PATH_CONNECTION_CLASSIFICATION_AND_NEXT_SUBLOCUS_OWNERSHIP_GATE_ONLY",
        "R17 complete path-connection use promoted",
    )
    require("flat base-basic or reduced-holonomy compatible stationary jet subloci" in by_id["G49"]["open_scope"], "R17 sublocus classification invented")
    require("physical path and non-isometric observer arrow" in by_id["G49"]["open_scope"], "physical observer arrow promoted")
    require("lambda minus one called completely flat" in by_id["G49"]["forbidden_regression"], "complete-flatness guard absent")
    require("lambda zero called a descended base connection" in by_id["G49"]["forbidden_regression"], "base-descent guard absent")
    require("isometric normal carry called physical non-isometric observer arrow" in by_id["G49"]["forbidden_regression"], "isometric/non-isometric guard absent")
    require(
        by_id["G49"]["controlling_source"]
        == "udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 complete path-connection source changed",
    )
    require("G49_REFINES_G48_BY_DERIVING_THE_COMPLETE_PROJECTED_NORMAL_CONNECTION_ALL_SIX_CURVATURE_PLANES_AND_SUPPLIED_PATH_FUNCTOR" in by_id["G49"]["precedence_rule"], "G48 complete path-connection refinement absent")
    require(
        by_id["G50"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__GLOBAL_CURVATURE_HORIZONTALITY_IFF_CONSTANT_PHI__FLAT_AND_ABSTRACT_DESCENT_LOCI_EXPLICIT__NO_REGULAR_CANONICAL_HOPF_TANGENT_DESCENT__COMPLETE_HOLONOMY_TRIVIAL_OR_SO2__MANIFEST_BACKED_R17_SOURCES_SELECT_NONE",
        "R17 stationary sublocus status regressed or promoted",
    )
    require(by_id["G50"]["epistemic_label"] == "MIXED", "R17 stationary sublocus label changed")
    require(
        by_id["G50"]["active_use"]
        == "ACTIVE_STATIONARY_SUBLOCUS_CLASSIFICATION_AND_NEXT_GENERIC_JOINT_INVARIANT_GATE_ONLY",
        "R17 stationary sublocus use promoted",
    )
    require("generic full-SO2 joint invariant" in by_id["G50"]["open_scope"], "generic joint invariant selected")
    require("repo-wide independent selector exhaustion" in by_id["G50"]["open_scope"], "ownership scope widened")
    require("flat or integer-descent locus called physically selected" in by_id["G50"]["forbidden_regression"], "special-locus selection guard absent")
    require("supporting local census called independently reviewed authority" in by_id["G50"]["forbidden_regression"], "external-review fence guard absent")
    require("full SO2 carry erased" in by_id["G50"]["forbidden_regression"], "generic holonomy guard absent")
    require(
        by_id["G50"]["controlling_source"]
        == "udt_r17_stationary_connection_sublocus_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 stationary sublocus source changed",
    )
    require("G50_REFINES_G49_BY_CLASSIFYING_ALL_STATIONARY_SPECIAL_SUBLOCI" in by_id["G50"]["precedence_rule"], "G49 stationary sublocus refinement absent")
    require(
        by_id["G51"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ENDPOINT_DEPTH_AND_NORMAL_ISOMETRY_FORM_EXACT_PRODUCT_GROUPOID__COMPLETE_COFRAME_FIXES_SCREEN_CO2_WEIGHTS_BY_VARIANCE__UNIQUE_NORMALIZED_CONTINUOUS_REAL_ORDER_ZERO_CHARACTER_IS_DELTA_K__LOOP_AND_RELATIVE_PATH_HOLONOMY_SURVIVE__PHYSICAL_PATH_ARROW_AND_STATIONARY_HIGHER_JET_SELECTION_OPEN",
        "R17 depth/holonomy joint status regressed or promoted",
    )
    require(by_id["G51"]["epistemic_label"] == "MIXED", "R17 joint-invariant label changed")
    require(
        by_id["G51"]["active_use"]
        == "ACTIVE_R17_JOINT_KINEMATIC_CLASSIFICATION_AND_NEXT_NATIVE_ONE_FORM_SELECTION_GATE_ONLY",
        "R17 joint-invariant use promoted",
    )
    require("stationary R17-owned endpoint-frame-invariant non-exact scalar one-form" in by_id["G51"]["open_scope"], "stationary higher-jet owner promoted")
    require("physical path or query" in by_id["G51"]["open_scope"], "physical path selected")
    require("global normal carry called one fixed SO2 matrix group" in by_id["G51"]["forbidden_regression"], "global groupoid type guard absent")
    require("general rectangle control called an R17 solution witness" in by_id["G51"]["forbidden_regression"], "higher-jet scope guard absent")
    require("screen CO2 representation called the physical observer arrow" in by_id["G51"]["forbidden_regression"], "screen/full-arrow guard absent")
    require(
        by_id["G51"]["controlling_source"]
        == "udt_r17_depth_holonomy_joint_invariant_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 joint-invariant source changed",
    )
    require("G51_REFINES_G50_BY_DERIVING_THE_TYPED_DEPTH_NORMAL_ISOMETRY_PRODUCT_GROUPOID" in by_id["G51"]["precedence_rule"], "G50 joint-invariant refinement absent")
    require(
        by_id["G52"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__CANONICAL_LOCAL_FORMS_BEYOND_dphi_AND_GENERIC_FIRST_JET_FULL_COTANGENT_DERIVED__CONSTRUCTIVE_NONUNIQUENESS_ONLY__NONCLOSED_PAIR_LEAF_AND_EXACT_PAIR_PURE_FAMILIES_SURVIVE__NO_DISTINGUISHED_ADDITIONAL_RECIPROCAL_TRANSGRESSION_SELECTED",
        "R17 stationary local one-form status regressed or promoted",
    )
    require(by_id["G52"]["epistemic_label"] == "MIXED", "R17 one-form label changed")
    require(
        by_id["G52"]["active_use"]
        == "ACTIVE_STATIONARY_R17_LOCAL_ONE_FORM_NONSELECTION_AND_NEXT_FOUNDING_QUERY_MEASUREMENT_SELECTOR_GATE_ONLY",
        "R17 one-form use promoted",
    )
    require("explicit physical query or measurement selection rule" in by_id["G52"]["open_scope"], "query selector invented")
    require("exhaustive higher-jet classification" in by_id["G52"]["open_scope"], "constructive scope widened")
    require("constructive families called an exhaustive finite-jet classification" in by_id["G52"]["forbidden_regression"], "constructive scope guard absent")
    require("metric-owned form called selected physical transgression" in by_id["G52"]["forbidden_regression"], "ownership/selection guard absent")
    require("line-integral composition or path independence called a coefficient selector" in by_id["G52"]["forbidden_regression"], "composition selection guard absent")
    require(
        by_id["G52"]["controlling_source"]
        == "udt_r17_stationary_local_one_form_selection_audit_2026-08-10/AUDIT_REPORT.md",
        "R17 stationary local one-form source changed",
    )
    require("G52_REFINES_G51_BY_DERIVING_MULTIPLE_STATIONARY_R17_LOCAL_FORMS" in by_id["G52"]["precedence_rule"], "G51 local one-form refinement absent")
    require(
        by_id["G53"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__REGULAR_CALIBRATED_PAIR_METRIC_HAS_UNIQUE_KAPPA_PHI_BETA_STATE_COORDINATES__MATCHED_DELTA_KAPPA_AND_DELTA_PHI_ADD__ANGULAR_U_PATH_CHANNEL_DISTINCT__CONDITIONAL_MINIMAL_BANKED_ASSEMBLY__PHYSICAL_QUERY_PROJECTION_PATH_REGIME_AND_CONDUCTOR_OPEN",
        "multi-channel assembly status regressed or promoted",
    )
    require(by_id["G53"]["epistemic_label"] == "MIXED", "multi-channel assembly label changed")
    require(
        by_id["G53"]["active_use"]
        == "ACTIVE_CONDITIONAL_MULTICHANNEL_ASSEMBLY_AND_NEXT_ORDERED_QUERY_PROJECTION_OWNERSHIP_GATE_ONLY",
        "multi-channel assembly use promoted",
    )
    require("physical ordered-query projection or measurement rule" in by_id["G53"]["open_scope"], "query projection owner invented")
    require("physical pair map and path" in by_id["G53"]["open_scope"], "physical pair map/path promoted")
    require("physical regime map" in by_id["G53"]["open_scope"], "physical regime map invented")
    require("on-shell or global bootstrap conductor" in by_id["G53"]["open_scope"], "conductor invented")
    require("conditional state assembly called a selected physical observer arrow" in by_id["G53"]["forbidden_regression"], "conditional/physical-arrow guard absent")
    require("kappa deleted by strong CSN or calibration cancellation" in by_id["G53"]["forbidden_regression"], "common-scale retention guard absent")
    require("beta called a standalone additive character" in by_id["G53"]["forbidden_regression"], "shift state/arrow guard absent")
    require("U_gamma scalarized or path labels erased" in by_id["G53"]["forbidden_regression"], "angular path guard absent")
    require("bounded minimality widened to full metric reconstruction" in by_id["G53"]["forbidden_regression"], "minimality scope guard absent")
    require(
        by_id["G53"]["controlling_source"]
        == "udt_multichannel_observer_relation_assembly_audit_2026-08-10/AUDIT_REPORT.md",
        "multi-channel assembly source changed",
    )
    require("G53_REFINES_G52_BY_REPLACING_THE_ONE_SCALAR_SEARCH_WITH_A_BOUNDED_TYPED_MULTICHANNEL_ASSEMBLY" in by_id["G53"]["precedence_rule"], "G52 multi-channel refinement absent")
    require(
        by_id["G54"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__AFTER_COMPLETE_CALIBRATED_QUERY_SUPPLIES_REGULAR_PAIR_RELATION_REALIZED_FOUNDING_RECIPROCAL_PROJECTION_IS_UNIQUELY_DELTA_PHI_WITHIN_CONTINUOUS_MATCHED_TWO_DENSITY_CHARACTERS__BROADER_MEASUREMENTS_AND_PAIR_OWNER_OPEN",
        "ordered-query projection status regressed or promoted",
    )
    require(by_id["G54"]["epistemic_label"] == "MIXED", "ordered-query projection label changed")
    require(
        by_id["G54"]["active_use"]
        == "ACTIVE_CONDITIONAL_RECIPROCAL_PROJECTION_AND_NEXT_PAIR_RELATION_OR_MEASUREMENT_OWNER_GATE_ONLY",
        "ordered-query projection use promoted",
    )
    require("calibrated physical observer-query and pair-relation selector" in by_id["G54"]["open_scope"], "pair-relation owner invented")
    require("physical path" in by_id["G54"]["open_scope"], "physical path promoted")
    require("bare observer endpoints said to select Delta_phi" in by_id["G54"]["forbidden_regression"], "bare-endpoint selection guard absent")
    require("uniqueness widened beyond continuous two-density characters" in by_id["G54"]["forbidden_regression"], "conditional uniqueness scope guard absent")
    require("endpoint coboundaries called impossible" in by_id["G54"]["forbidden_regression"], "coboundary survival guard absent")
    require("kappa deleted" in by_id["G54"]["forbidden_regression"], "common-scale retention guard absent")
    require("phi orchestra reduced to pure block" in by_id["G54"]["forbidden_regression"], "phi-orchestra upstream guard absent")
    require(
        by_id["G54"]["controlling_source"]
        == "udt_ordered_observer_query_projection_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "ordered-query projection source changed",
    )
    require("G54_REFINES_G53_BY_SELECTING_DELTA_PHI_ONLY_AS_THE_CONDITIONAL_REALIZATION_OF_THE_FOUNDED_RECIPROCAL_PROJECTION" in by_id["G54"]["precedence_rule"], "G53 ordered-query projection refinement absent")
    require(
        by_id["G55"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__24_BY_6_BRANCH_MEASUREMENT_ATLAS__11_MATHEMATICAL_APPARATUS_PATTERNS__FIVE_RESTRICTED_GLOBAL_RELATION_TYPES__R17_ONLY_FULL_PANEL_CONDITIONAL__ZERO_PHYSICAL_PAIR_ARROW_SELECTOR_OR_REGIME_OWNERS",
        "multi-regime admissibility status regressed or promoted",
    )
    require(by_id["G55"]["epistemic_label"] == "MIXED", "multi-regime admissibility label changed")
    require(
        by_id["G55"]["active_use"]
        == "ACTIVE_BRANCH_DEPENDENT_APPARATUS_AVAILABILITY_MAP_AND_NEXT_ON_SHELL_GLOBAL_DESCENT_BOOTSTRAP_OR_PREMISE_DECISION_GATE_ONLY",
        "multi-regime admissibility use promoted",
    )
    require("time-live or on-shell realized branch/query selection" in by_id["G55"]["open_scope"], "on-shell owner invented")
    require("global descent selecting pair surfaces or middle resets" in by_id["G55"]["open_scope"], "global descent invented")
    require("bootstrap closure correlating background completion with local admissibility" in by_id["G55"]["open_scope"], "bootstrap closure invented")
    require("R04 aggregate said to inherit one member's instrument panel" in by_id["G55"]["forbidden_regression"], "R04 aggregate guard absent")
    require("mathematical apparatus patterns called physical micro ordinary or cosmological regimes" in by_id["G55"]["forbidden_regression"], "physical regime guard absent")
    require("pinned static-corpus workflow exhaustion called a theorem about all static geometry" in by_id["G55"]["forbidden_regression"], "static no-go scope guard absent")
    require(
        by_id["G55"]["controlling_source"]
        == "udt_multiregime_pair_relation_admissibility_audit_2026-08-10/AUDIT_REPORT.md",
        "multi-regime admissibility source changed",
    )
    require("G55_REFINES_G54_BY_MAPPING_THE_COMPLETE_PINNED_24_BRANCH_CORPUS" in by_id["G55"]["precedence_rule"], "G54 multi-regime refinement absent")
    require(
        by_id["G56"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__24_BY_10_GLOBAL_DESCENT_ATLAS__R17_GLOBAL_PAIR_FOLIATION_PATH_FUNCTOR_AND_SO2_ALIGNMENT_BITORSOR_OWNED__R18_CLOCK_ONLY_ENDPOINT_DESCENT_OWNED__CALIBRATION_RESET_PAIR_QUERY_AND_COMPLETE_SELECTOR_OPEN",
        "global descent status regressed or promoted",
    )
    require(by_id["G56"]["epistemic_label"] == "MIXED", "global descent label changed")
    require(
        by_id["G56"]["active_use"]
        == "ACTIVE_BOUNDED_GLOBAL_DESCENT_OWNERSHIP_MAP_AND_NEXT_NATIVE_ON_SHELL_OR_TIME_LIVE_EQUATION_OWNERSHIP_GATE_ONLY",
        "global descent use promoted",
    )
    require("R17 calibration-bearing representative and scalar reset" in by_id["G56"]["open_scope"], "R17 calibration reset invented")
    require("physical pair leaf path winding and query selector" in by_id["G56"]["open_scope"], "physical pair query invented")
    require("native on-shell or time-live equation" in by_id["G56"]["open_scope"], "native evolution equation invented")
    require("SO2 alignment bitorsor called one selected calibration representative" in by_id["G56"]["forbidden_regression"], "bitorsor/representative guard absent")
    require("R18 clock-only chain silently spliced into R17" in by_id["G56"]["forbidden_regression"], "R17/R18 splice guard absent")
    require("no complete selector in pinned corpus called a universal no-go" in by_id["G56"]["forbidden_regression"], "bounded no-go guard absent")
    require(
        by_id["G56"]["controlling_source"]
        == "udt_global_descent_pair_surface_reset_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "global descent source changed",
    )
    require("G56_REFINES_G55_BY_CONSOLIDATING_GLOBAL_PAIR_SURFACE_PATH_CARRY_ALIGNMENT_AND_CLOCK_ONLY_DESCENT" in by_id["G56"]["precedence_rule"], "G55 global descent refinement absent")
    require(
        by_id["G57"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__LOCAL_LINEAR_POSITIVE_LINE_TRANSPORTS_AFFINE__CANONICAL_METRIC_AND_COMPLETE_COFRAME_TRANSPORTS_ISOMETRIC_ZERO__SUPPLIED_REGULAR_CALIBRATED_PAIR_FAMILY_INDUCES_EXACT_FULL_COFRAME_dPHI_PAIR_WITH_TIME_AND_MIXING__PHYSICAL_FAMILY_TRANSITION_AND_GLOBAL_OWNER_OPEN",
        "complete-coframe calibration transport status regressed or promoted",
    )
    require(by_id["G57"]["epistemic_label"] == "MIXED", "calibration transport label changed")
    require(
        by_id["G57"]["active_use"]
        == "ACTIVE_CONDITIONAL_PAIR_FAMILY_TRANSPORT_RESULT_AND_NEXT_ON_SHELL_GLOBAL_FAMILY_OWNER_GATE_ONLY",
        "calibration transport use promoted",
    )
    require("physical calibrated observer-pair family or query selector" in by_id["G57"]["open_scope"], "physical pair-family owner invented")
    require("lawful transitions among independently rebuilt families" in by_id["G57"]["open_scope"], "pair-family transitions promoted")
    require("null rank-changing cut-locus and nonlocal strata" in by_id["G57"]["open_scope"], "degenerate/global scope erased")
    require("supplied calibrated pair family called metric-selected" in by_id["G57"]["forbidden_regression"], "conditional family guard absent")
    require("algebraically live time dependence called an on-shell time-live solution" in by_id["G57"]["forbidden_regression"], "time-live ownership guard absent")
    require("catch-proof harness called independent derivation" in by_id["G57"]["forbidden_regression"], "independence guard absent")
    require("an extra scalar reset equation invented after a common family is supplied" in by_id["G57"]["forbidden_regression"], "scalar-reset reduction guard absent")
    require(
        by_id["G57"]["controlling_source"]
        == "udt_complete_coframe_calibration_transport_from_scratch_2026-08-10/AUDIT_REPORT.md",
        "calibration transport source changed",
    )
    require("G57_REFINES_G56_BY_DERIVING_THE_FULL_DECLARED_LOCAL_TRANSPORT_CLASS" in by_id["G57"]["precedence_rule"], "G56 calibration transport refinement absent")
    require(
        by_id["G58"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__SUPPLIED_PAIR_CONE_EXACTLY_JOINS_BETA_PHI_PAIR_AND_CONDITIONAL_CEFF__LOCAL_BIDIRECTIONAL_CAUSAL_ISOMORPHISMS_RETAIN_INFINITE_TRANSITION_CALIBRATION_FREEDOM__NO_AMBIENT_PHYSICAL_FAMILY_MULTIPLICITY_OR_SELECTOR_THEOREM",
        "co-present causal pair gate regressed or promoted",
    )
    require(by_id["G58"]["epistemic_label"] == "MIXED", "causal pair gate label changed")
    require(
        by_id["G58"]["active_use"]
        == "ACTIVE_SCOPED_PAIR_CONE_CAUSAL_JOIN_AND_NEXT_AMBIENT_PHYSICAL_PAIR_SELECTOR_GATE_ONLY",
        "causal pair gate use promoted",
    )
    require("metric/query construction of ambiently distinct pair immersions" in by_id["G58"]["open_scope"], "ambient pair construction silently closed")
    require("global causal order reflection and faithfulness" in by_id["G58"]["open_scope"], "global causal scope erased")
    require("local transition or profile freedom called physically distinct ambient pair families" in by_id["G58"]["forbidden_regression"], "physical-family overclaim guard absent")
    require("one-way causal maps included in the bidirectional classification" in by_id["G58"]["forbidden_regression"], "causal-class scope guard absent")
    require("sampled smoke test called theorem-strength independent proof" in by_id["G58"]["forbidden_regression"], "verification-grade guard absent")
    require(
        by_id["G58"]["controlling_source"]
        == "udt_copresent_causal_pair_functor_selector_audit_2026-08-10/AUDIT_REPORT.md",
        "causal pair source changed",
    )
    require("G58_REFINES_G57_BY_DERIVING_THE_EXACT_COMPLETE_PAIR_CONE_PHI_CEFF_JOIN" in by_id["G58"]["precedence_rule"], "G57 causal pair refinement absent")
    require(
        by_id["G59"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__CONDITIONAL_SPLIT_RELATIVE_MATRIX_ORCHESTRA_H_EQUALS_HR_PLUS_HA__GENERIC_CONTINUOUS_ORBIT_AND_SIGNED_AREA_LOCKS_DERIVED__ANGULAR_MODULATES_KAPPA_PHI_PAIR_BETA__POSITIVE_WEIGHTS_AND_PHYSICAL_REGIME_CURVE_OPEN",
        "pair-instrument mixing atlas status regressed or promoted",
    )
    require(by_id["G59"]["epistemic_label"] == "MIXED", "pair-instrument atlas label changed")
    require(
        by_id["G59"]["active_use"]
        == "ACTIVE_CONDITIONAL_POINTWISE_ORCHESTRA_ATLAS_AND_NEXT_OWNED_BRANCH_CURVE_GATE_ONLY",
        "pair-instrument atlas use promoted",
    )
    require("universal ownership of reciprocal/angular split" in by_id["G59"]["open_scope"], "split ownership silently closed")
    require("actual time-live or scale-live curve s to (H_R,H_A)" in by_id["G59"]["open_scope"], "physical curve silently closed")
    require("positive measurement weights" in by_id["G59"]["open_scope"], "positive weights invented")
    require("signed R A M called positive probabilities or importance weights" in by_id["G59"]["forbidden_regression"], "signed-channel guard absent")
    require("off-shell algebra called time-live evolution" in by_id["G59"]["forbidden_regression"], "time-live ownership guard absent")
    require("catch harness called independent proof" in by_id["G59"]["forbidden_regression"], "independence-scope guard absent")
    require(
        by_id["G59"]["controlling_source"]
        == "udt_pair_instrument_mixing_solution_space_audit_2026-08-10/AUDIT_REPORT.md",
        "pair-instrument atlas source changed",
    )
    require("G59_REFINES_G58_BY_DERIVING_THE_COMPLETE_SPLIT_RELATIVE_MATRIX_AND_SIGNED_AREA_ORCHESTRA_ATLAS" in by_id["G59"]["precedence_rule"], "G58 pair-instrument refinement absent")
    require(
        by_id["G60"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__FULL_REGULAR_PAIR_ADAPTED_COFRAME_MOVIES_OBEY_EXACT_BASE_ANGULAR_MIXING_COMPATIBILITY__ARBITRARY_TIME_ONLY_FREQUENCIES_SURVIVE__NO_NATIVE_EVOLUTION_CHARACTERISTIC_OR_REGIME_SELECTED",
        "time-live orchestra status regressed or promoted",
    )
    require(by_id["G60"]["epistemic_label"] == "MIXED", "time-live orchestra label changed")
    require(
        by_id["G60"]["active_use"]
        == "ACTIVE_LOCAL_TIMELIVE_KINEMATIC_PARENT_AND_NEXT_OWNED_HISTORY_RESTRICTION_GATE_ONLY",
        "time-live orchestra use promoted",
    )
    require("an owned principal differential relation or equivalent global-completion rule" in by_id["G60"]["open_scope"], "history-selection owner silently closed")
    require("characteristics dispersion frequencies and regime map" in by_id["G60"]["open_scope"], "time-live physical outputs silently selected")
    require("bootstrap tuning only after a history restriction is owned" in by_id["G60"]["open_scope"], "bootstrap sequencing guard absent")
    require("Maurer-Cartan compatibility called an equation of motion" in by_id["G60"]["forbidden_regression"], "identity-versus-EOM guard absent")
    require("the metric null cone called a field characteristic without a principal operator" in by_id["G60"]["forbidden_regression"], "cone-versus-characteristic guard absent")
    require("local nonselection widened to a theorem that no native or global law exists" in by_id["G60"]["forbidden_regression"], "bounded nonselection guard absent")
    require(
        by_id["G60"]["controlling_source"]
        == "udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/AUDIT_REPORT.md",
        "time-live orchestra source changed",
    )
    require("G60_REFINES_G59_BY_TURNING_ON_ALL_DECLARED_TIME_AND_SPACE_CHANNELS" in by_id["G60"]["precedence_rule"], "G59 time-live refinement absent")
    require(
        by_id["G61"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__COMPLETE_REGULAR_CHART_LOCALLY_FINITE_JET_OPEN_ON_DECLARED_POSITIVE_SCREEN_TIME_ORIENTED_COMPONENT__NO_OWNED_NONIDENTITY_HISTORY_RESTRICTION_FOUND_IN_TEN_FROZEN_SOURCES",
        "native history restriction status regressed or promoted",
    )
    require(by_id["G61"]["epistemic_label"] == "MIXED", "native history restriction label changed")
    require(
        by_id["G61"]["active_use"]
        == "ACTIVE_CHART_AND_SOURCE_BOUNDED_HISTORY_NONSELECTION_AND_NEXT_GLOBAL_SELECTOR_TYPE_GATE_ONLY",
        "native history restriction use promoted",
    )
    require("other chart components and split-changing null rank-changing cut-locus strata" in by_id["G61"]["open_scope"], "other chart/strata silently closed")
    require("global causal faithfulness chronology hyperbolicity completeness and descent" in by_id["G61"]["open_scope"], "global gates silently closed")
    require("preservation of a boundary germ called preservation of global causality or completion" in by_id["G61"]["forbidden_regression"], "boundary/global guard absent")
    require("the type signature R(j^k g;G_global)=0 called a formula or derived law" in by_id["G61"]["forbidden_regression"], "selector type guard absent")
    require(
        by_id["G61"]["controlling_source"]
        == "udt_native_history_restriction_from_scratch_2026-08-10/AUDIT_REPORT.md",
        "native history restriction source changed",
    )
    require("G61_REFINES_G60_BY_PROVING_FINITE_JET_OPENNESS" in by_id["G61"]["precedence_rule"], "G60 history restriction refinement absent")
    require(
        by_id["G62"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__FINITE_REGULAR_OBSERVER_NETWORK_HAS_EXACT_ENDPOINT_ATLAS_AND_PATH_LABELLED_ASSEMBLY_IDENTITIES__ROUTE_DEPENDENCE_ALLOWED__UNIVERSAL_FLAT_DESCENT_UNOWNED",
        "observer-network assembly status regressed or promoted",
    )
    require(by_id["G62"]["epistemic_label"] == "MIXED", "observer-network label changed")
    require(
        by_id["G62"]["active_use"]
        == "ACTIVE_NETWORK_ASSEMBLY_AND_PHYSICAL_RELATION_FAMILY_ROUTE_POLICY_OWNERSHIP_GATE_ONLY",
        "observer-network use promoted",
    )
    require("physical calibrated observer pair query relation family" in by_id["G62"]["open_scope"], "physical relation-family owner silently closed")
    require("endpoint descended path labelled or path quotient policy branch by branch" in by_id["G62"]["open_scope"], "route policy silently selected")
    require("K4 d2 or abelian Bianchi bookkeeping called new physics or a history law" in by_id["G62"]["forbidden_regression"], "four-face novelty guard absent")
    require("continuum curvature inferred without a chosen smooth local connection" in by_id["G62"]["forbidden_regression"], "continuum-flatness hypothesis guard absent")
    require("route policy used before relation family ownership" in by_id["G62"]["forbidden_regression"], "relation-family ordering guard absent")
    require(
        by_id["G62"]["controlling_source"]
        == "udt_complete_observer_network_assembly_from_scratch_2026-08-11/AUDIT_REPORT.md",
        "observer-network source changed",
    )
    require("G62_REFINES_G61_AND_G40_BY_ASSEMBLING_THE_FINITE_REGULAR_NETWORK" in by_id["G62"]["precedence_rule"], "G62 assembly refinement absent")
    require(
        by_id["G63"]["current_status"]
        == "VERIFIED_WITH_CORRECTIONS__BOUNDED_14_WITNESS_SOLVED_ATLAS_RETAINS_ENDPOINT_DEPTH_CAUSAL_PROPAGATORS_FULL_COFRAME_HOLONOMY_AND_R17_NORMAL_HOLONOMY__MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES__NO_PHYSICAL_SELECTOR_DYNAMICS_OR_STABILITY",
        "solved-geometry survivor status regressed or promoted",
    )
    require(by_id["G63"]["epistemic_label"] == "OBSERVED", "solved-geometry label changed")
    require(
        by_id["G63"]["active_use"]
        == "ACTIVE_BOUNDED_SOLVED_GEOMETRY_AND_NEXT_COUPLED_CHANNEL_RELATION_GATE_ONLY",
        "solved-geometry use promoted",
    )
    require("metric-native relation or independence among endpoint depth causal propagator full-coframe holonomy and normal holonomy" in by_id["G63"]["open_scope"], "coupled-channel relation silently closed")
    require("native on-shell equation and time-live global completion" in by_id["G63"]["open_scope"], "on-shell/global completion silently closed")
    require("bounded persistence called physical or dynamical stability" in by_id["G63"]["forbidden_regression"], "stability overclaim guard absent")
    require("endpoint scalar and path holonomy forced to compete" in by_id["G63"]["forbidden_regression"], "typed coexistence guard absent")
    require("arbitrary wider scan launched before channel invariants and independence contract" in by_id["G63"]["forbidden_regression"], "next-step ordering guard absent")
    require(
        by_id["G63"]["controlling_source"]
        == "udt_solved_geometry_relation_family_survivor_atlas_2026-08-11/AUDIT_REPORT.md",
        "solved-geometry source changed",
    )
    require("G63_REFINES_G62_G47_G49_G51_G60_BY_SOLVING_THE_EXACT_BOUNDED_WITNESS_ATLAS" in by_id["G63"]["precedence_rule"], "G63 solved-atlas refinement absent")
    require(
        by_id["G64"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__QUERY_CLASS_DEPENDENT_CHANNEL_ARCHITECTURE__COMMON_QUERY_CHANNELS_COMPATIBILITY_LINKED_WITH_RETAINED_EXTRINSIC_DATA__PHYSICAL_QUERY_BRANCH_AND_DYNAMICS_OPEN",
        "common-query architecture status regressed or promoted",
    )
    require(by_id["G64"]["epistemic_label"] == "MIXED", "common-query label changed")
    require("universal preferred path search resumed" in by_id["G64"]["forbidden_regression"], "preferred-path guard absent")
    require("unresolved Q2 Codazzi certification" in by_id["G64"]["open_scope"], "Codazzi caveat silently closed")
    require(
        by_id["G64"]["controlling_source"]
        == "udt_common_query_pair_immersion_reconstruction_2026-08-11/AUDIT_REPORT.md",
        "common-query source changed",
    )
    require("G64_REFINES_G63_BY_PLACING_COEXISTING_ENDPOINT_EXTRINSIC_JACOBI_AND_TRANSPORT_CHANNELS" in by_id["G64"]["precedence_rule"], "G64 query refinement absent")
    require(
        by_id["G65"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ALL_18_FROZEN_M3_SNE_FITS_AND_443_LEAVES_BIT_IDENTICAL__NATIVE_OBSERVER_QUERY_RETYPING_ALGEBRAICALLY_IDENTICAL__NO_OWNED_COMPLETE_SNE_QUERY_CORRECTION",
        "native-query SNe status regressed or promoted",
    )
    require(by_id["G65"]["epistemic_label"] == "MIXED", "native-query SNe label changed")
    require("physical complete SNe query and pair immersion" in by_id["G65"]["open_scope"], "complete SNe query silently owned")
    require("P1 promoted to centered CMB lapse" in by_id["G65"]["forbidden_regression"], "P1 role guard absent")
    require("conditional pair c_eff called material signal speed" in by_id["G65"]["forbidden_regression"], "conditional c_eff guard absent")
    require(
        by_id["G65"]["controlling_source"]
        == "udt_sne_native_observer_query_replay_2026-08-11/AUDIT_REPORT.md",
        "native-query SNe source changed",
    )
    require("G65_REFINES_G64_AND_THE_FROZEN_M3_SNE_UNIVERSE" in by_id["G65"]["precedence_rule"], "G65 SNe refinement absent")
    require(
        by_id["G66"]["current_status"]
        == "VERIFIED_AFTER_SPECIFIED_CORRECTIONS__16_SOURCE_F00_F17_QUERY_ARCHITECTURE_MAPPED__NO_COMPLETE_PHYSICAL_CMB_REALIZATION_OWNED__F00_COMPATIBILITY_ONLY",
        "complete CMB query-map status regressed or promoted",
    )
    require(by_id["G66"]["epistemic_label"] == "MIXED", "complete CMB query-map label changed")
    require("physical CMB observer-sky query and pair immersion" in by_id["G66"]["open_scope"], "physical CMB query silently owned")
    require("local artifact checker called independent semantic derivation" in by_id["G66"]["forbidden_regression"], "artifact/semantic evidence guard absent")
    require("eigenvalues called nonzero power" in by_id["G66"]["forbidden_regression"], "spectrum/power type guard absent")
    require("pair c_eff called local signal speed" in by_id["G66"]["forbidden_regression"], "pair/local speed guard absent")
    require(
        by_id["G66"]["controlling_source"]
        == "udt_cmb_complete_observation_query_map_2026-08-11/AUDIT_REPORT.md",
        "complete CMB query-map source changed",
    )
    require("G66_REFINES_G65_G64_AND_THE_F00_F17_CMB_FAMILY_UNIVERSE" in by_id["G66"]["precedence_rule"], "G66 CMB refinement absent")
    require(
        by_id["G74"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__EXACT_21_PROFILE_WHOLE_SKY_CONTROL_CENSUS__3_F01_GLOBAL_DIFFEO__6_PERSISTENT_SAMPLED_REGULAR_ONLY__12_CENTER_C2_BLOCKED_NO_REPAIR",
        "G74 topology status regressed or promoted",
    )
    require(by_id["G74"]["epistemic_label"] == "MIXED", "G74 topology label changed")
    require("globally center-regular complete-metric profile family" in by_id["G74"]["open_scope"], "G74 center-regular profile silently owned")
    require("sampled regularity promoted to global theorem" in by_id["G74"]["forbidden_regression"], "G74 sampled/global guard absent")
    require("direct Christoffel replay called clean-room independent" in by_id["G74"]["forbidden_regression"], "G74 independence caveat absent")
    require(
        by_id["G74"]["controlling_source"]
        == "udt_cmb_G74_symbolic_sky_relation_topology_atlas_2026-08-11/AUDIT_REPORT.md",
        "G74 topology source changed",
    )
    require("G74_COMPLETES_G73_SYMBOLIC_SKY_TOPOLOGY_GATE" in by_id["G74"]["precedence_rule"], "G74 topology refinement absent")
    require(
        by_id["G75"]["current_status"]
        == "INTERNALLY_REPLAYED_BOUNDED_LEAD__49_EXACT_PRIMITIVE_QUADRATIC_SHAPES__591_CENTER_C_INFINITY_LORENTZ_REGULAR_CONTROLS__MULTIPLE_SHAPE_STRATA__FRESH_EXTERNAL_REVIEW_OPEN",
        "G75 center-regular family status regressed or promoted",
    )
    require(by_id["G75"]["epistemic_label"] == "MIXED", "G75 family label changed")
    require("fresh blind external review" in by_id["G75"]["open_scope"], "G75 external-review gate silently closed")
    require("all smooth center-regular axial profiles" in by_id["G75"]["open_scope"], "G75 bounded family promoted to full smooth space")
    require("same-context exact replay called fresh independent review" in by_id["G75"]["forbidden_regression"], "G75 independence guard absent")
    require("G74 blocked rows called repaired" in by_id["G75"]["forbidden_regression"], "G75 no-repair guard absent")
    require(
        by_id["G75"]["controlling_source"]
        == "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/AUDIT_REPORT.md",
        "G75 family source changed",
    )
    require("G75_COMPLETES_THE_BOUNDED_CENTER_REGULAR_PROFILE_FAMILY_MAP" in by_id["G75"]["precedence_rule"], "G75 family refinement absent")

    guard_rows = read_tsv(
        ROOT / "udt_foundational_semantic_regression_correction_2026-07-26/SEMANTIC_GUARD_UNIVERSE.tsv"
    )
    require(len(guard_rows) == 16, "guard universe must contain exactly 16 rows")
    guard_sources = {row["guard_id"]: row["controlling_source"] for row in guard_rows}
    for guard, source in guard_sources.items():
        if guard in {"G01", "G02", "G12", "G14"}:
            expected = {
                "G01": "udt_founding_phi_ownership_morphism_audit_2026-08-05/AUDIT_REPORT.md",
                "G02": "udt_founding_phi_ownership_morphism_audit_2026-08-05/EXACT_DERIVATION.md",
                "G12": "udt_complete_pair_phi_orchestra_audit_2026-08-05/AUDIT_REPORT.md",
                "G14": "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md",
            }[guard]
            require(
                by_id[guard]["controlling_source"] == expected,
                f"relational correction source priority changed: {guard}",
            )
        else:
            require(by_id[guard]["controlling_source"] == source, f"source priority changed: {guard}")

    expected_sources = {row["controlling_source"] for row in rows}
    for source in expected_sources:
        require((ROOT / source).is_file(), f"missing controlling source: {source}")

    validate_startup_surface(ROOT)

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for token in [
        "on **supplied ordered depth**",
        "presentation potential",
        "universal physical scalar",
        "complete-arrow strain",
        "groupoid 1-cocycle",
        "CHOSE_COMPARISON_CONFIGURATION",
        "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED",
        "generic configuration-arena count",
        "WORKING_FOUNDATIONAL_FRAME",
        "positional-dilation asymptote",
        "finite-cell seal",
    ]:
        require(token in agents, f"AGENTS guard absent: {token}")

    xmax_controls = [
        "LIVE.md",
        "HANDOFF.md",
        "INDEX.md",
        "README.md",
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
        "research/README.md",
    ]
    xmax_source = "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md"
    for control in xmax_controls:
        text = (ROOT / control).read_text(encoding="utf-8")
        require(xmax_source in text, f"control lacks Xmax correction: {control}")
        require("positional-dilation asymptote" in text, f"control lacks Xmax limiting meaning: {control}")

    adjudication = read_tsv(
        ROOT / "udt_foundational_semantic_regression_correction_2026-07-26/ACTIVE_SEMANTIC_ADJUDICATION.tsv"
    )
    require(len(adjudication) == 754, "semantic candidate adjudication must contain 754 rows")
    require(len({row["candidate_id"] for row in adjudication}) == 754, "duplicate semantic candidate id")
    require(len({row["path"] for row in adjudication}) == 754, "duplicate semantic candidate path")
    require(all(row["controlling_disposition"] for row in adjudication), "unadjudicated semantic candidate")

    dof = ROOT / "udt_global_functional_dof_constraint_rank_audit_2026-07-26"
    status = {row["id"]: row for row in read_tsv(dof / "STATUS_LEDGER.tsv")}
    presentation = {row["id"]: row for row in read_tsv(dof / "LOCAL_PRESENTATION_RANK.tsv")}
    require(status["S03"]["status"] == "CHOSE_COMPARISON_F4_7_TOTAL", "DOF independent phi still native")
    require(status["S04"]["status"] == "DERIVED_FOUNDED_PHI_ADDS_ZERO__COMPLETE_EXTENSION_OPEN", "DOF founded phi still conditional")
    require(presentation["P04"]["status"] == "CHOSE_COMPARISON_CONFIGURATION", "DOF comparison branch promotion")
    require(presentation["P05"]["status"] == "DERIVED_FOUNDED_SUBGROUP__FULL_EXTENSION_OPEN", "DOF founded branch regression")
    print("PASS: 68 premise guards, G75 bounded 49-shape and 591-profile center-regular Lorentz-control family internally replayed while fresh adversarial review and physical selection remain open; G74 exact frozen 21-profile whole-sky control census with 3 F01 global diffeomorphisms, 6 persistent sampled-regular controls, 12 unrepaired center-C2 blocks, and physical CMB profile/source/scale still open; bounded 16-source F00-F17 complete CMB query architecture with no owned physical realization and F00 compatibility only, exact frozen M3 SNe replay with algebraically identical native pair-depth retyping and no owned complete-query correction, conditional common-query channel architecture with physical query and Q2 Codazzi certification open, bounded solved-geometry endpoint/propagator/full-holonomy/normal-holonomy coexistence with no physical selector or stability promotion, exact finite observer-network assembly in endpoint-atlas and path-labelled homes with route dependence allowed and physical relation-family/route-policy ownership open, declared regular complete chart finite-jet open with no owned nonidentity history restriction in ten frozen sources and global selector ownership still open, exact complete time-live compatibility orchestra with arbitrary time-only frequencies and native history selection still open, conditional complete split-relative matrix orchestra with generic orbit and signed area locks while positive weights and physical branch curve remain open, exact supplied-pair cone/phi/conditional-c-eff join with scoped local causal transition/calibration nonselection and ambient physical-family selector open, conditional full-coframe dphi_pair descent on a supplied coherent calibrated pair family with physical family/transition owner open, corrected global descent atlas with R17 foliation/path/alignment ownership and R18 clock-only descent while complete selector remains open, corrected 24-by-6 multi-regime mathematical apparatus atlas with no physical regime owner, conditional founded reciprocal projection uniquely Delta_phi within continuous matched two-density characters with pair-relation and broader measurement owner open, conditional multi-channel pair-state and angular-transport assembly, stationary R17 canonical local forms and constructive nonuniqueness, depth/normal-holonomy product groupoid, flat/descent/holonomy subloci, complete metric-projected path functor, pair-leaf normal holonomy, global pair foliation, complete-coframe vertical reciprocal metric class, branch-conditional non-isometric magnitude ownership, reciprocal calibration bitorsor descent, carried/intrinsic alignment, branch-transition ownership, complete-branch relation families, three-observer overlap carry, founding pair-relation ownership, calibrated pair-map ownership, terminal reciprocal-c_E readout, calibration-state solder, reciprocal-flag ownership, N03 profile-role map, N02 radial admissibility, N01 coupling and complete-angular routing, marked-block atlas guards, relational-depth/orchestra and conceptual-type corrections, current startup controls, 754 historical candidate dispositions, corrected DOF semantics")


if __name__ == "__main__":
    main()
