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

    latest = "udt_r17_stationary_connection_sublocus_ownership_audit_2026-08-10/AUDIT_REPORT.md"
    for control in LATEST_ROUTE_CONTROLS:
        require(latest in controls[control], f"latest complete-branch route absent: {control}")

    for control in ("README.md", "research/README.md", "MEMORY.md"):
        text = controls[control]
        require("RA2-PARTIAL-WEAK" in text, f"current route loses RA2 grade: {control}")
        require("BANKED + TABLED" in text, f"current route loses BAO status: {control}")

    memory_top = " ".join(controls["MEMORY.md"].split("## Historical memory archive", 1)[0].split())
    require("2026-08-10" in memory_top, "MEMORY top pointer is not August 10 current")
    require("CMB PEAK OPTIMIZATION" in memory_top, "MEMORY top pointer is stale")
    require("RA2-PARTIAL-WEAK" in memory_top, "MEMORY top pointer loses RA2 grade")

    for relative in (
        "CURRENT_SCIENTIFIC_PREMISES.md",
        "CURRENT_SCIENTIFIC_PREMISES.tsv",
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
    require(len(rows) == 50, "premise registry must contain exactly 50 rows")
    by_id = {row["premise_id"]: row for row in rows}
    require(len(by_id) == 50, "duplicate premise id")
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
    print("PASS: 50 premise guards, stationary R17 flat/descent/holonomy subloci classified with no manifest-backed selector, complete metric-projected R17 normal connection and path functor with physical path and arrow open, conditional metric-owned R17 pair-leaf normal connection and representative-free holonomy, conditional R17 global pair foliation and same-leaf scalar depth, complete-coframe-conditional R17 vertical reciprocal metric class, branch-conditional non-isometric magnitude ownership, reciprocal scalar/calibration bitorsor descent, carried/intrinsic alignment bitorsor, branch-transition ownership correction, complete-branch relation-family classification, three-observer overlap carry, founding pair-relation ownership, calibrated pair-map ownership, terminal reciprocal-c_E pair-metric readout, calibration-state solder, reciprocal-flag ownership, N03 profile-role map, N02 radial admissibility, N01 coupling and complete-angular family routing, marked-block atlas guards, relational-depth/orchestra and conceptual-type corrections, current startup controls, 754 historical candidate dispositions, corrected DOF semantics")


if __name__ == "__main__":
    main()
