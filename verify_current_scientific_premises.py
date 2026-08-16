#!/usr/bin/env python3
"""Fail closed on current foundational premise and startup-precedence regressions."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent

PREMISE_REGISTRY_CONTROLS = (
    "AGENTS.md",
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "MEMORY.md",
    "README.md",
    "research/README.md",
    "research/_registry/README.md",
    "CURRENT_RESEARCH_PROGRAM.md",
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "INFLIGHT_STATE.md",
)

CURRENT_ORIENTATION_CONTROLS = (
    "AGENTS.md",
    "LIVE.md",
    "HANDOFF.md",
    "INDEX.md",
    "MEMORY.md",
    "README.md",
    "research/README.md",
    "research/_registry/README.md",
    "CURRENT_RESEARCH_PROGRAM.md",
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "INFLIGHT_STATE.md",
)

STALE_STARTUP_TOKENS = (
    "CMB PEAK OPTIMIZATION",
    "ACTIVE ARC =",
    "G86 remains the latest",
    "fresh restart pending",
    "x_max O1 pending",
    "global cell assembly lane is active",
    "udt-r3-covariance-patchlists-20260813.service",
    "Complete R3 -> assemble -> independently verify",
    "194 component cells -> assembly -> independent verification -> outcome inspection",
)

ARCHIVED_STARTUP_SNAPSHOTS = {
    "AGENTS_before_cleanup.md": ("4c4acf412daeb2761a19a3877ac1e589c69572d9c65c8a6fc5756789f7945bb3", 347),
    "LIVE_before_cleanup.md": ("4edd35923db884a14ca8d1995119184044abbc9d3897229d1a2fee5dab63928a", 1314),
    "HANDOFF_before_cleanup.md": ("2f307c1a4c8972a9b8e6aa9cb66a8f30b33a0d2d9427621f66dbb05e8738b56f", 839),
    "INDEX_before_cleanup.md": ("abb7bb9a9bf46478ca21a5fa8ff51f594ee0a370e081aaae0c6fb580b9b2f386", 527),
    "MEMORY_before_cleanup.md": ("fc9aef1bcd82e25f3e0f09bd7aed16fd2def3d85c0f8823c7439bce865b50f71", 471),
    "CURRENT_RESEARCH_PROGRAM_before_cleanup.md": ("714a6d3fde1709289863f19cd3e134cc968a3f6972df8671d111eee5d4e7b3e8", 759),
    "CURRENT_SCIENTIFIC_PREMISES_before_cleanup.md": ("e4e936e4408ced06ce2633462c0b9aaf3491e0a2ce56a2e5b484f53fe68dfcdb", 917),
    "README_before_cleanup.md": ("d25c29b891a702345c06bc9767ccb38cdb345c0dc53cef106768f3dc2baf8ea9", 452),
    "research_README_before_cleanup.md": ("a66a5653ead353b6c124ae2fa451ff61aef22080519a8ad05e64e4ad742ddfe8", 308),
    "research_registry_README_before_cleanup.md": ("74ca21670526a7b6a1731b514b35be32ec0d93a415627c4140f0337f7db16224", 232),
    "INFLIGHT_STATE_before_cleanup.md": ("0ab4394549b72f17a4fbdee75425d1da91a75d8d5cb13da5bb8051e7a748704f", 278),
    "verify_current_scientific_premises_before_cleanup.py": ("f2abb9928bab03960fdfe7bb1283419abd3c04d63eab301eaa7326f10adb236c", 1411),
    "test_startup_surface_before_cleanup.py": ("4e293c1d2204d2ec4d4c1b71f9f3dec62a43ce75ca32e899b15dcb195c0aee76", 420),
}


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
    """Fail closed on current routing while preserving, not rereading, historical detail."""
    controls: dict[str, str] = {}
    for relative in CURRENT_ORIENTATION_CONTROLS:
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
        for token in (
            "udt_observed_angular_pattern_raw_restart_2026-08-12",
            "R3_OUTCOME_REPORT.md",
            "R3_VERIFICATION_RESULT.json",
            "R4_OUTCOME_REPORT.md",
            "R4_VERIFICATION_RESULT.json",
            "R5_OUTCOME_REPORT.md",
            "R5_VERIFICATION_RESULT.json",
            "R5_EXTERNAL_FOLLOWUP_REVIEW.md",
            "R5_FINAL_EVIDENCE_MANIFEST.tsv",
            "/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/",
            "194",
            "independent verification",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "archive/startup_surface_2026-08-14",
        ):
            require(token in block, f"marked current block lacks {token}: {name}")
        require("R2" in block and "VERIFIED-WITH-CAVEATS" in block, f"R2 grade absent: {name}")
        require(
            "OBSERVED_VERIFIED_WITH_CAVEATS__COVARIANCE_RESOLUTION_OR_RANK_LIMITED" in block,
            f"R3 completed grade absent: {name}",
        )
        require(
            "OBSERVED_VERIFIED_WITH_CAVEATS__BROAD_SHAPE_PERSISTENCE_WITHOUT_FEATURE_SELECTION__FULL_COVARIANCE_METRIC_GRID_DEPENDENT" in block,
            f"R4 completed grade absent: {name}",
        )
        require(
            "OBSERVED_VERIFIED_WITH_CAVEATS__ONE_DOMINANT_SHARED_DIRECTION__ADDITIONAL_SUBSPACE_ALIGNMENT_CONTROL_DEPENDENT__COVARIANCE_RANGE_PARTLY_UNRESOLVED" in block,
            f"R5 completed grade absent: {name}",
        )
        require(
            "no preferred" in block.lower(),
            f"R3 no-preferred-selection guard absent: {name}",
        )
        require("G96" in block, f"G96 category boundary absent: {name}")
        require("G97" in block, f"G97 SNe control result absent: {name}")
        require("G98" in block, f"G98 continuation ownership result absent: {name}")
        require("G99" in block, f"G99 calibration result absent: {name}")
        require("G101" in block, f"G101 grok2 integration result absent: {name}")
        require("G102" in block, f"G102 two-source evaluator absent: {name}")
        require("G103" in block, f"G103 restriction result absent: {name}")
        require("G104" in block, f"G104 kaleidoscope result absent: {name}")
        require("G105" in block, f"G105 Jacobian artifact result absent: {name}")
        require("G106" in block, f"G106 sky-depth projector result absent: {name}")
        require("G107" in block, f"G107 representation census absent: {name}")
        require("G108" in block, f"G108 screen propagation result absent: {name}")
        require("G109" in block, f"G109 same-query depth join absent: {name}")
        require("G110" in block, f"G110 full-differential type correction absent: {name}")
        require(
            "udt_complete_reciprocal_representation_extension_census_2026-08-16/" in block
            or "constant reciprocal-extension census" in block.lower(),
            f"G107 package route absent: {name}",
        )
        require(
            "udt_complete_screen_jacobi_riccati_propagation_atlas_2026-08-16/" in block
            or "propagated screen" in block.lower(),
            f"G108 package route absent: {name}",
        )
        require(
            "udt_same_query_terminal_depth_screen_propagation_join_2026-08-16/" in block,
            f"G109 package route absent: {name}",
        )
        require(
            "udt_observer_exponential_full_differential_type_audit_2026-08-16/" in block,
            f"G110 package route absent: {name}",
        )
        require(
            "udt_orchestra_score_whiteboard_2026-08-15/" in block
            or "whiteboard" in block.lower(),
            f"orchestra-score next-gate route absent: {name}",
        )

    for token in (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/",
    ):
        require(token in live, f"LIVE lacks protected local path: {token}")
    require("udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/" in controls["AGENTS.md"],
            "AGENTS lacks protected curvature-atlas guard")

    required_routes = {
        "AGENTS.md": (
            "Stop the startup read here",
            "does not make full scripts",
            "without dumping its wide rows into model context",
            "not a startup read or a current-frontier index",
        ),
        "INDEX.md": (
            "udt_observed_angular_pattern_raw_restart_2026-08-12/",
            "R5_OUTCOME_REPORT.md",
            "R5_EXTERNAL_FOLLOWUP_REVIEW.md",
            "R5_FINAL_EVIDENCE_MANIFEST.tsv",
            "udt_pair_first_relational_plane_reconstruction_2026-08-12/",
            "udt_pair_terminal_reachability_atlas_2026-08-12/",
            "udt_pair_chord_network_descent_audit_2026-08-12/",
            "udt_null_carrier_measure_ownership_audit_2026-08-15/",
            "udt_bao_G106_complete_sky_depth_reference_projection_2026-08-15/",
            "udt_orchestra_score_whiteboard_2026-08-15/",
            "udt_complete_reciprocal_representation_extension_census_2026-08-16/",
            "udt_same_query_terminal_depth_screen_propagation_join_2026-08-16/",
            "udt_observer_exponential_full_differential_type_audit_2026-08-16/",
            "After orientation",
            "verify_current_scientific_premises.py",
        ),
        "MEMORY.md": (
            "OBSERVED_VERIFIED_WITH_CAVEATS__COVARIANCE_RESOLUTION_OR_RANK_LIMITED",
            "R5 data-only common-subspace assembly",
            "/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/",
            "After orientation",
        ),
        "CURRENT_RESEARCH_PROGRAM.md": (
            "COVARIANCE_RESOLUTION_OR_RANK_LIMITED",
            "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/",
            "udt_pair_first_relational_plane_reconstruction_2026-08-12/",
            "udt_pair_terminal_reachability_atlas_2026-08-12/",
            "udt_pair_chord_network_descent_audit_2026-08-12/",
            "G106",
            "G107",
            "G108",
            "G109",
            "G110",
            "dV=E(dJ+E^-1dE J)",
        ),
        "CURRENT_SCIENTIFIC_PREMISES.md": (
            "WORKING_FOUNDATIONAL_FRAME",
            "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "G107",
            "G108",
            "G109",
            "G110",
        ),
        "README.md": (
            "LIVE.md",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "verify_current_scientific_premises.py",
            "after orientation",
            "AGENTS.md",
        ),
        "research/README.md": (
            "CURRENT_ARTIFACT_PATHS.tsv",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "After orientation",
            "verify_current_scientific_premises.py",
            "not a startup read",
        ),
        "research/_registry/README.md": (
            "CURRENT_ARTIFACT_PATHS.tsv",
            "CURRENT_SCIENTIFIC_PREMISES.tsv",
            "not a startup read",
            "not a current-frontier index",
        ),
        "INFLIGHT_STATE.md": (
            "retired compatibility pointer",
            "INFLIGHT_STATE_before_cleanup.md",
            "After orientation",
            "verify_current_scientific_premises.py",
        ),
    }
    for control, tokens in required_routes.items():
        for token in tokens:
            require(token in controls[control], f"current route lacks {token}: {control}")

    for control in CURRENT_ORIENTATION_CONTROLS:
        lowered = controls[control].lower()
        for token in STALE_STARTUP_TOKENS:
            require(token.lower() not in lowered, f"stale startup token {token}: {control}")

    for relative in (
        "CURRENT_SCIENTIFIC_PREMISES.tsv",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R2_OUTCOME_REPORT.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R3_PREREGISTRATION.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R3_OUTCOME_REPORT.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R3_VERIFICATION_RESULT.json",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R3_FINAL_STATUS.json",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R4_PREREGISTRATION.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R4_OUTCOME_REPORT.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R4_VERIFICATION_RESULT.json",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R4_FINAL_STATUS.json",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_PREREGISTRATION.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_OUTCOME_REPORT.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_VERIFICATION_RESULT.json",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_EXTERNAL_FOLLOWUP_REVIEW.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_FINAL_STATUS.json",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_FINAL_EVIDENCE_MANIFEST.tsv",
        "udt_observed_angular_pattern_raw_restart_2026-08-12/STATUS_LEDGER.tsv",
        "udt_boss_primary_method_crosswalk_2026-08-13/AUDIT_REPORT.md",
        "udt_pair_first_relational_plane_reconstruction_2026-08-12/AUDIT_REPORT.md",
        "udt_pair_terminal_reachability_atlas_2026-08-12/AUDIT_REPORT.md",
        "udt_pair_chord_network_descent_audit_2026-08-12/AUDIT_REPORT.md",
        "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/AUDIT_REPORT.md",
        "udt_august6_mu_complete_kernel_crosswalk_2026-08-15/AUDIT_REPORT.md",
        "udt_reciprocal_kernel_release_candidate_interface_audit_2026-08-15/AUDIT_REPORT.md",
        "udt_reciprocal_kernel_release_candidate_interface_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_native_flux_luminosity_law_ownership_audit_2026-08-15/AUDIT_REPORT.md",
        "udt_native_flux_luminosity_law_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_native_radiative_current_energy_owner_audit_2026-08-15/AUDIT_REPORT.md",
        "udt_native_radiative_current_energy_owner_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_null_carrier_measure_ownership_audit_2026-08-15/AUDIT_REPORT.md",
        "udt_null_carrier_measure_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_reciprocal_kernel_release_candidate_interface_audit_2026-08-15/SNE_EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_complete_history_regime_continuation_ownership_audit_2026-08-15/AUDIT_REPORT.md",
        "udt_observed_middle_regime_pair_calibration_2026-08-15/AUDIT_REPORT.md",
        "udt_grok2_parallel_branch_integration_audit_2026-08-15/AUDIT_REPORT.md",
        "udt_bao_G102_complete_two_source_observable_map_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_bao_G103_source_independent_restriction_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_bao_G104_kaleidoscope_forward_operator_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_bao_G105_complete_orchestra_two_route_lift_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_bao_G106_complete_sky_depth_reference_projection_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_complete_reciprocal_representation_extension_census_2026-08-16/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_complete_screen_jacobi_riccati_propagation_atlas_2026-08-16/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_same_query_terminal_depth_screen_propagation_join_2026-08-16/EXTERNAL_REVIEW_ADJUDICATION.md",
        "udt_observer_exponential_full_differential_type_audit_2026-08-16/AUDIT_REPORT.md",
    ):
        require((root / relative).is_file(), f"current startup target missing: {relative}")

    archive = root / "archive" / "startup_surface_2026-08-14"
    require((archive / "SHA256_MANIFEST.tsv").is_file(), "startup archive manifest missing")
    for name, (expected_hash, expected_lines) in ARCHIVED_STARTUP_SNAPSHOTS.items():
        path = archive / name
        require(path.is_file(), f"startup archive snapshot missing: {name}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected_hash, f"startup archive hash mismatch: {name}")
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        require(line_count == expected_lines, f"startup archive line-count mismatch: {name}")


def main() -> None:
    rows = read_tsv(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    require(len(rows) == 97, "premise registry must contain exactly 97 rows")
    by_id = {row["premise_id"]: row for row in rows}
    require(len(by_id) == 97, "duplicate premise id")
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
        == "EXTERNALLY_VERIFIED_BOUNDED_FAMILY__49_EXACT_PRIMITIVE_QUADRATIC_SHAPES__591_CENTER_C_INFINITY_LORENTZ_REGULAR_CONTROLS__ZERO_ROW_MISMATCHES__LOCAL_EVIDENCE_CAVEATS_CLOSED",
        "G75 center-regular family status regressed or promoted",
    )
    require(by_id["G75"]["epistemic_label"] == "MIXED", "G75 family label changed")
    require("all smooth center-regular axial profiles" in by_id["G75"]["open_scope"], "G75 bounded family promoted to full smooth space")
    require("original local replay called a fresh or fully independent reconstruction" in by_id["G75"]["forbidden_regression"], "G75 independence guard absent")
    require("original local catch layer called catch-complete" in by_id["G75"]["forbidden_regression"], "G75 catch-completeness guard absent")
    require("G74 blocked rows called repaired" in by_id["G75"]["forbidden_regression"], "G75 no-repair guard absent")
    require(
        by_id["G75"]["controlling_source"]
        == "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G75 family source changed",
    )
    require("G75_EXTERNALLY_VERIFIES_THE_BOUNDED_CENTER_REGULAR_PROFILE_FAMILY_MAP" in by_id["G75"]["precedence_rule"], "G75 family refinement absent")
    require(
        by_id["G76"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__587_SAMPLED_COMPLETE_ORIENTATION_PRESERVING__4_HISTORICAL_NUMERICALLY_UNRESOLVED_UNDER_FROZEN_G76_GATE",
        "G76 historical whole-sky status rewritten",
    )
    require(by_id["G76"]["epistemic_label"] == "OBSERVED", "G76 historical label changed")
    require("four G76 rows silently promoted" in by_id["G76"]["forbidden_regression"], "G76 immutable-history guard absent")
    require(
        by_id["G76"]["controlling_source"]
        == "udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G76 historical source changed",
    )
    require(
        by_id["G77"]["current_status"]
        == "VERIFIED_FULL_FAMILY_DIRECT_REPLAY__590_STRONG__1_REGISTERED__0_UNRESOLVED__FOUR_G76_EXCEPTIONS_RESOLVED_IN_G77",
        "G77 direct-replay status regressed or promoted",
    )
    require(by_id["G77"]["epistemic_label"] == "OBSERVED", "G77 direct-replay label changed")
    require("continuum injectivity" in by_id["G77"]["open_scope"], "G77 finite-mesh scope promoted")
    require("G77 used to rewrite G76 history" in by_id["G77"]["forbidden_regression"], "G77/G76 history guard absent")
    require(
        by_id["G77"]["controlling_source"]
        == "udt_cmb_G77_full_family_direct_christoffel_replay_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G77 direct-replay source changed",
    )
    require("G77_STRENGTHENS_G76" in by_id["G77"]["precedence_rule"], "G77 refinement absent")
    require(
        by_id["G78"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__NO_PHYSICAL_PROFILE_ENDPOINT_SCALE_OR_SOURCE_OWNER_IN_EXACT_20_SOURCE_G78_UNIVERSE",
        "G78 bounded owner-join status regressed or promoted",
    )
    require(by_id["G78"]["epistemic_label"] == "MIXED", "G78 owner-join label changed")
    require("exhaustive current repository" in by_id["G78"]["open_scope"], "G78 source scope promoted")
    require("internal route-status regression check" in by_id["G78"]["forbidden_regression"], "G78 semantic independence caveat absent")
    require("dimensionless R factorization called CSN" in by_id["G78"]["forbidden_regression"], "G78 scale guard absent")
    require(
        by_id["G78"]["controlling_source"]
        == "udt_cmb_G78_profile_endpoint_source_owner_join_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G78 owner-join source changed",
    )
    require("G78_REFINES_G77" in by_id["G78"]["precedence_rule"], "G78 refinement absent")
    require(
        by_id["G79"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__BOUNDED_SAME_GEOMETRY_REDSHIFT_AND_ANGULAR_DISTANCE_QUERY",
        "G79 bounded dimensional-query status regressed or promoted",
    )
    require(by_id["G79"]["epistemic_label"] == "MIXED", "G79 dimensional-query label changed")
    require("physical profile and scale R" in by_id["G79"]["open_scope"], "G79 physical-owner scope promoted")
    require("cmb_temp or CMB spectrum" in by_id["G79"]["open_scope"], "G79 thermal deferral absent")
    require("control profile called physical" in by_id["G79"]["forbidden_regression"], "G79 control-profile guard absent")
    require("neighboring-ray route called fully end-to-end independent" in by_id["G79"]["forbidden_regression"], "G79 independence caveat absent")
    require(
        by_id["G79"]["controlling_source"]
        == "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G79 dimensional-query source changed",
    )
    require("G79_COMPLETES_G78" in by_id["G79"]["precedence_rule"], "G79 refinement absent")
    require(
        by_id["G80"]["current_status"] == "VERIFIED_AS_BOUNDED_GEOMETRIC_RECIPROCITY",
        "G80 bounded reciprocity status regressed or promoted",
    )
    require(by_id["G80"]["epistemic_label"] == "MIXED", "G80 reciprocity label changed")
    require("nonradial and general endpoint-screen branches" in by_id["G80"]["open_scope"], "G80 screen scope promoted")
    require("generic Jacobi theorem called a UDT-specific selector" in by_id["G80"]["forbidden_regression"], "G80 genericity guard absent")
    require("past-directed reversal called a future signal" in by_id["G80"]["forbidden_regression"], "G80 signal guard absent")
    require("bare transpose identity applied across arbitrary screen gauges" in by_id["G80"]["forbidden_regression"], "G80 screen-gauge guard absent")
    require(
        by_id["G80"]["controlling_source"]
        == "udt_cmb_G80_reverse_pair_reciprocity_2026-08-11/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G80 reciprocity source changed",
    )
    require("G80_COMPLETES_G79" in by_id["G80"]["precedence_rule"], "G80 refinement absent")
    require(
        by_id["G81"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS",
        "G81 bounded covariance status regressed or promoted",
    )
    require(by_id["G81"]["epistemic_label"] == "MIXED", "G81 covariance label changed")
    require("METHOD_CAVEAT_CLOSED_BY_G82" in by_id["G81"]["active_use"], "G81 method closure absent")
    require("integrator families" in by_id["G81"]["open_scope"], "G81 method scope promoted")
    require("two fixed controls called a generic UDT selector" in by_id["G81"]["forbidden_regression"], "G81 bounded-scope guard absent")
    require("bounded neighboring-ray independence called absolute" in by_id["G81"]["forbidden_regression"], "G81 independence guard absent")
    require("reviewer said to have reopened nine source bytes" in by_id["G81"]["forbidden_regression"], "G81 source-review boundary absent")
    require(
        by_id["G81"]["controlling_source"]
        == "udt_cmb_G81_nonradial_screen_covariance_2026-08-12/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G81 covariance source changed",
    )
    require("G81_COMPLETES_G80" in by_id["G81"]["precedence_rule"], "G81 refinement absent")
    require(
        by_id["G82"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY",
        "G82 bounded method-support status regressed or promoted",
    )
    require(by_id["G82"]["epistemic_label"] == "OBSERVED", "G82 support label changed")
    require("absolute method independence" in by_id["G82"]["open_scope"], "G82 method scope promoted")
    require("original 15 catches called exhaustive" in by_id["G82"]["forbidden_regression"], "G82 catch caveat absent")
    require("literal packaged CLI rerun" in by_id["G82"]["forbidden_regression"], "G82 rerun caveat absent")
    require(
        by_id["G82"]["controlling_source"]
        == "udt_cmb_G82_fixed_c1_radau_replay_2026-08-12/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G82 support source changed",
    )
    require("G82_CLOSES_ONLY_G81S_REGISTERED" in by_id["G82"]["precedence_rule"], "G82 refinement absent")
    require(
        by_id["G87"]["current_status"]
        == "ACCEPT__VERIFIED_WITH_CAVEATS__EXACT_ENDPOINT_TRANSITIONS_AND_PSD_PARTIAL_ORDER_SEPARATED__PHYSICAL_GLOBAL_FAMILY_OPEN",
        "G87 chord-network status regressed or promoted",
    )
    require(by_id["G87"]["epistemic_label"] == "MIXED", "G87 chord-network label changed")
    require("physical common calibrated global state family" in by_id["G87"]["open_scope"], "G87 global-family owner promoted")
    require("PSD reachability called Reciprocity" in by_id["G87"]["forbidden_regression"], "G87 order/Reciprocity guard absent")
    require("independent derivation of the coframe transition" in by_id["G87"]["forbidden_regression"], "G87 replay-independence caveat absent")
    require(
        by_id["G87"]["controlling_source"]
        == "udt_pair_chord_network_descent_audit_2026-08-12/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G87 chord-network source changed",
    )
    require("G87_CLOSES_THE_ZERO_ORDER_CHORD_COMPOSITION_QUESTION" in by_id["G87"]["precedence_rule"], "G87 refinement absent")
    require(
        by_id["G89"]["current_status"]
        == "EXTERNALLY_VERIFIED_WITH_CAVEATS__FULL_B_Q_S_Y_Z_PULLBACK_AND_FIRST_VARIATION__TERMINAL_PHI_PAIR_AND_CEFF_OVER_CE_DERIVED__NO_UNIQUE_SCALAR_MU_OWNED__PHYSICAL_PAIR_AND_HISTORY_OPEN",
        "G89 uncompressed evaluator status regressed or promoted",
    )
    require(by_id["G89"]["epistemic_label"] == "MIXED", "G89 evaluator label changed")
    require("physical pair realization and live history" in by_id["G89"]["open_scope"], "G89 pair/history promoted")
    require("overlapping-pair compatibility law" in by_id["G89"]["open_scope"], "G89 compatibility-law gate absent")
    require("modern four-component S identified with July mu_old" in by_id["G89"]["forbidden_regression"], "G89 mu type guard absent")
    require("fixed-P convexity called a derived quiet-middle regime" in by_id["G89"]["forbidden_regression"], "G89 fixed-P promotion guard absent")
    require("external review described as canonization" in by_id["G89"]["forbidden_regression"], "G89 external-review scope guard absent")
    require(
        by_id["G89"]["controlling_source"]
        == "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G89 evaluator source changed",
    )
    require("G89_FRESH_SEALED_REVIEW_REPRODUCED_THE_COMPLETE_SUPPLIED_PAIR_EVALUATOR" in by_id["G89"]["precedence_rule"], "G89 review refinement absent")
    require(
        by_id["G90"]["current_status"]
        == "INTERNALLY_VERIFIED_WITH_CAVEATS__NONIDENTITY_SIMULTANEOUS_OVERLAP_COMPATIBILITY__ALL_INSTRUMENTS_ACTIVITY_ALONE_DOES_NOT_SELECT_RESPONSE_SHAPE__LOUD_QUIET_LOUD_SURVIVES_DECLARED_ALL_ACTIVE_CLASS",
        "G90 overlap/loud-quiet status regressed or promoted",
    )
    require(by_id["G90"]["epistemic_label"] == "MIXED", "G90 overlap label changed")
    require("fresh semantic review" in by_id["G90"]["open_scope"], "G90 semantic review falsely closed")
    require("physical pair family and metric/query history owner" in by_id["G90"]["open_scope"], "G90 physical history promoted")
    require("original explicit lifts called fully live" in by_id["G90"]["forbidden_regression"], "G90 activity correction guard absent")
    require("flat or monotone C2 lifts omitted" in by_id["G90"]["forbidden_regression"], "G90 C2 counterfamily guard absent")
    require("quiet-middle survivor called universal physical law" in by_id["G90"]["forbidden_regression"], "G90 selection guard absent")
    require(
        by_id["G90"]["controlling_source"]
        == "udt_overlapping_pair_live_compatibility_audit_2026-08-14/AUDIT_REPORT.md",
        "G90 overlap source changed",
    )
    require("G90_CORRECTS_THE_EXPLICIT_LIFT_ALL_ACTIVE_CATEGORY_ERROR" in by_id["G90"]["precedence_rule"], "G90 correction refinement absent")
    require(
        by_id["G91"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ONE_SCREEN_COMPARISON_ARROW_MU_LOCK_IS_GENERIC_SPECTRAL_RECIPROCAL_LOCK_DEFECT_FOR_s_NE_r__EXACT_GAUGE_CARVEOUT_ON_PART_OF_s_EQ_r__COUPLING_INERT_FOR_PHI_PROFILE_SELECTION__COMPLETE_KERNEL_CROSSWALK_OPEN",
        "G91 scoped mu_lock result regressed or promoted",
    )
    require(by_id["G91"]["epistemic_label"] == "MIXED", "G91 mu_lock label changed")
    require("type-correct map into complete B Q S Y Z pair evaluator" in by_id["G91"]["open_scope"], "G91 complete-kernel crosswalk falsely closed")
    require("mu_lock collapsed into July mu_old" in by_id["G91"]["forbidden_regression"], "G91 mu type guard absent")
    require("s equals r gauge carve-out omitted" in by_id["G91"]["forbidden_regression"], "G91 gauge carve-out guard absent")
    require("physical depth cocycle" in by_id["G91"]["forbidden_regression"], "G91 physical-depth promotion guard absent")
    require(
        by_id["G91"]["controlling_source"]
        == "udt_mixing_channel_lane_2026-08-06/BLIND_VERIFICATION_FINAL.md",
        "G91 mu_lock source changed",
    )
    require("G91_RECOVERS_THE_DISTINCT_AUGUST6_SCOPED_RECIPROCAL_LOCK_DEFECT" in by_id["G91"]["precedence_rule"], "G91 recovery precedence absent")
    require(
        by_id["G92"]["current_status"]
        == "INTERNALLY_VERIFIED_WITH_CAVEATS__RESTRICTED_MU_LOCK_IS_SIGNED_COMPONENT_OF_SUPPLIED_ENDPOINT_TRANSITION__NO_UNIQUE_FULL_2X2_SCALAR_EXTENSION__NOT_UNIVERSALLY_RECOVERABLE_FROM_TERMINAL_PAIR_METRIC__FRESH_SEMANTIC_REVIEW_OPEN",
        "G92 mu crosswalk status regressed or promoted",
    )
    require(by_id["G92"]["epistemic_label"] == "MIXED", "G92 crosswalk label changed")
    require("fresh semantic adversary" in by_id["G92"]["open_scope"], "G92 fresh review falsely closed")
    require("physical endpoint carry" in by_id["G92"]["open_scope"], "G92 endpoint carry promoted")
    require("restricted component promoted to universal scalar" in by_id["G92"]["forbidden_regression"], "G92 scalar-promotion guard absent")
    require("terminal h or phi_pair identified with full-arrow strain" in by_id["G92"]["forbidden_regression"], "G92 channel-type guard absent")
    require("S/Z pullback fiber ignored" in by_id["G92"]["forbidden_regression"], "G92 pullback-fiber guard absent")
    require("s equals r gauge carve-out omitted" in by_id["G92"]["forbidden_regression"], "G92 old gauge carve-out guard absent")
    require(
        by_id["G92"]["controlling_source"]
        == "udt_august6_mu_complete_kernel_crosswalk_2026-08-15/AUDIT_REPORT.md",
        "G92 crosswalk source changed",
    )
    require("G92_DERIVES_THE_RESTRICTED_ENDPOINT_TRANSITION_COMPONENT_BRIDGE" in by_id["G92"]["precedence_rule"], "G92 crosswalk precedence absent")
    require(
        by_id["G93"]["current_status"]
        == "EXTERNALLY_VERIFIED_WITH_CAVEATS__G87_G89_G90_G92_KERNEL_INTERFACES_COHERENT__AMBIENT_AND_TERMINAL_TRANSITIONS_COMPOSE_SEPARATELY__ALL_FIVE_CHANNELS_PRECEDE_READOUT__NO_FIT_GEOMETRY_REPLAY_JUSTIFIED__PHYSICAL_HISTORY_AND_FLUX_OPEN",
        "G93 release-candidate status regressed or promoted",
    )
    require(by_id["G93"]["epistemic_label"] == "MIXED", "G93 release-candidate label changed")
    require("witness-independent state ensemble" in by_id["G93"]["open_scope"], "G93 shared-witness caveat silently closed")
    require("semantic mutations beyond status guards" in by_id["G93"]["open_scope"], "G93 catch-proof caveat silently closed")
    require("physical complete history and pair family" in by_id["G93"]["open_scope"], "G93 physical history promoted")
    require("native flux source and luminosity law" in by_id["G93"]["open_scope"], "G93 flux owner promoted")
    require("ambient and terminal arrows identified" in by_id["G93"]["forbidden_regression"], "G93 arrow-type guard absent")
    require("mu_lock appended after phi_pair" in by_id["G93"]["forbidden_regression"], "G93 mu double-count guard absent")
    require("frozen P1 retype called rebuilt-kernel replay" in by_id["G93"]["forbidden_regression"], "G93 replay-identity guard absent")
    require("geometry readiness called full SNe validation" in by_id["G93"]["forbidden_regression"], "G93 validation-promotion guard absent")
    require(
        by_id["G93"]["controlling_source"]
        == "udt_reciprocal_kernel_release_candidate_interface_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G93 release-candidate source changed",
    )
    require("G93_FRESH_SEALED_REVIEW_REPRODUCES_THE_JOINED_KERNEL" in by_id["G93"]["precedence_rule"], "G93 external-review precedence absent")
    require(
        by_id["G94"]["current_status"]
        == "EXTERNALLY_VERIFIED_WITH_CAVEATS__Z3_GEOMETRIC_CLOCK_FACTOR_DERIVED_ON_REGULAR_SUPPLIED_QUERY__TRANSFER_PRODUCT_ETA_EPSILON_OPEN__HISTORICAL_Z2_LAW_COMPATIBLE_CONDITIONAL",
        "G94 flux ownership status regressed or promoted",
    )
    require(by_id["G94"]["epistemic_label"] == "MIXED", "G94 flux label changed")
    require("physical radiative carrier current and conserved measure" in by_id["G94"]["open_scope"], "G94 current ownership promoted")
    require("energy-frequency law" in by_id["G94"]["open_scope"], "G94 energy ownership promoted")
    require("caustics multiple images" in by_id["G94"]["open_scope"], "G94 singular/global scope promoted")
    require("clock or frequency ratio identified with energy ratio" in by_id["G94"]["forbidden_regression"], "G94 clock-energy type guard absent")
    require("eta set to one" in by_id["G94"]["forbidden_regression"], "G94 survival guard absent")
    require("historical dL equals Z2 dA called unconditional" in by_id["G94"]["forbidden_regression"], "G94 luminosity-law guard absent")
    require(
        by_id["G94"]["controlling_source"]
        == "udt_native_flux_luminosity_law_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G94 flux source changed",
    )
    require("G94_FRESH_SEALED_REVIEW_RECONSTRUCTS_WRONSKIAN" in by_id["G94"]["precedence_rule"], "G94 external-review precedence absent")
    require(
        by_id["G95"]["current_status"]
        == "EXTERNALLY_VERIFIED_WITH_CAVEATS__GEOMETRIC_RESPONSE_AND_PHASESPACE_TRANSPORT_ONLY__PHYSICAL_TRANSFER_OPEN__EPSILON_ONE_OVER_Z_ONLY_AFTER_ONE_CARRIER_COVECTOR_IDENTIFICATION",
        "G95 current-energy status regressed or promoted",
    )
    require(by_id["G95"]["epistemic_label"] == "MIXED", "G95 current-energy label changed")
    require("physical radiative carrier and populated conserved measure" in by_id["G95"]["open_scope"], "G95 physical carrier promoted")
    require("energy-covector identification" in by_id["G95"]["open_scope"], "G95 energy premise promoted")
    require("Maxwell-shaped response called physical Maxwell theory or cargo" in by_id["G95"]["forbidden_regression"], "G95 response-cargo guard absent")
    require("Liouville volume called a populated conserved distribution" in by_id["G95"]["forbidden_regression"], "G95 population guard absent")
    require("package consistency verifier called independent derivation" in by_id["G95"]["forbidden_regression"], "G95 evidence-scope repair absent")
    require(
        by_id["G95"]["controlling_source"]
        == "udt_native_radiative_current_energy_owner_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G95 current-energy source changed",
    )
    require("G95_FRESH_SEALED_REVIEW_RECONSTRUCTS_RESPONSE_COUNTEREXAMPLE" in by_id["G95"]["precedence_rule"], "G95 external-review precedence absent")
    require(
        by_id["G96"]["current_status"]
        == "EXTERNALLY_REVIEWED_WITH_CAVEATS__LABEL_CURRENT_VALID_BUT_TAUTOLOGICAL__NO_NEW_OWNERSHIP_BEYOND_QUERY_TYPING__PHYSICAL_ETA_OPEN",
        "G96 label-current status regressed or promoted",
    )
    require(by_id["G96"]["epistemic_label"] == "MIXED", "G96 label-current label changed")
    require("physical radiative carrier identification" in by_id["G96"]["open_scope"], "G96 carrier identification promoted")
    require("physical zero side flux" in by_id["G96"]["open_scope"], "G96 physical side-flux premise promoted")
    require("query label closure called new metric dynamics" in by_id["G96"]["forbidden_regression"], "G96 tautology guard absent")
    require("eta_label equals one substituted for physical eta equals one" in by_id["G96"]["forbidden_regression"], "G96 eta type guard absent")
    require("det D called the full spacetime current" in by_id["G96"]["forbidden_regression"], "G96 Jacobian type guard absent")
    require(
        by_id["G96"]["controlling_source"]
        == "udt_null_carrier_measure_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G96 label-current source changed",
    )
    require("G96_FRESH_SEALED_REVIEW_CONFIRMS_THE_LABEL_PUSHFORWARD_ALGEBRA" in by_id["G96"]["precedence_rule"], "G96 external-review precedence absent")
    require(
        by_id["G97"]["current_status"]
        == "VERIFIED_WITH_CAVEATS__ONE_PRESELECTED_G79_CONTROL_STRONGLY_INCOMPATIBLE_WITH_REGISTERED_SNE_MEAN_RELATION__END_TO_END_CONDITIONAL_INTERFACE_OPERATIONAL__NO_HISTORY_OR_NATIVE_TRANSFER",
        "G97 scoped SNe control result regressed or promoted",
    )
    require(by_id["G97"]["epistemic_label"] == "MIXED", "G97 SNe label changed")
    require("all other complete geometries directions skies histories and branches" in by_id["G97"]["open_scope"], "G97 one-control scope promoted")
    require("native radiative carrier transfer luminosity and source law" in by_id["G97"]["open_scope"], "G97 provisional transfer promoted")
    require("one control negative called rejection of reciprocal kernel or UDT" in by_id["G97"]["forbidden_regression"], "G97 kernel/theory rejection guard absent")
    require("one equatorial curve called all-sky isotropy" in by_id["G97"]["forbidden_regression"], "G97 all-sky guard absent")
    require("another geometry fitted or tuned to repair the mismatch" in by_id["G97"]["forbidden_regression"], "G97 mismatch-tuning guard absent")
    require("scope guards called independent numerical evidence" in by_id["G97"]["forbidden_regression"], "G97 evidence-scope guard absent")
    require(
        by_id["G97"]["controlling_source"]
        == "udt_reciprocal_kernel_release_candidate_interface_audit_2026-08-15/SNE_EXTERNAL_REVIEW_ADJUDICATION.md",
        "G97 SNe source changed",
    )
    require("G97_FRESH_SEALED_REVIEW_REBUILDS_THE_FULL_CURVE_AND_RAW_LIKELIHOOD" in by_id["G97"]["precedence_rule"], "G97 external-review precedence absent")
    require(
        by_id["G98"]["current_status"]
        == "INTERNALLY_VERIFIED_WITH_CAVEATS__PERMITTED_NOT_OWNED__EXACT_FLAT_MONOTONE_AND_LOUD_QUIET_LOUD_CONTRIBUTION_LIVE_HISTORIES_SURVIVE__NO_ACTIVE_NATIVE_SELECTOR_IN_FROZEN_SOURCE_UNIVERSE",
        "G98 continuation-owner status regressed or promoted",
    )
    require(by_id["G98"]["epistemic_label"] == "MIXED", "G98 continuation label changed")
    require("fresh external semantic review" in by_id["G98"]["open_scope"], "G98 review scope silently closed")
    require("physical metric history and query family" in by_id["G98"]["open_scope"], "G98 physical owner promoted")
    require("permitted loud quiet loud family called selected UDT history" in by_id["G98"]["forbidden_regression"], "G98 survivor-selection guard absent")
    require("kinematic identity called dynamics" in by_id["G98"]["forbidden_regression"], "G98 identity/dynamics guard absent")
    require("one SNe mismatch called native history equation" in by_id["G98"]["forbidden_regression"], "G98 observation-owner guard absent")
    require("source-bounded result called generic no-go" in by_id["G98"]["forbidden_regression"], "G98 scope guard absent")
    require(
        by_id["G98"]["controlling_source"]
        == "udt_complete_history_regime_continuation_ownership_audit_2026-08-15/AUDIT_REPORT.md",
        "G98 source changed",
    )
    require("G98_CONSTRUCTIVELY_PROVES_THAT_CURRENT_COMPLETE_EQUATIONS_PERMIT" in by_id["G98"]["precedence_rule"], "G98 precedence absent")
    require(
        by_id["G99"]["current_status"]
        == "INTERNALLY_VERIFIED_WITH_CAVEATS__OBSERVED_CONDITIONAL_TERMINAL_CALIBRATION_FROZEN__NO_OPTIMIZER_OR_HOLDOUT_READ__COMPLETE_HISTORY_TRANSFER_AND_JOINT_UNCERTAINTY_OPEN",
        "G99 calibration status regressed or promoted",
    )
    require(by_id["G99"]["epistemic_label"] == "MIXED", "G99 calibration label changed")
    require("full joint n X_eff covariance" in by_id["G99"]["open_scope"], "G99 joint covariance promoted")
    require("complete B Q S Y Z history" in by_id["G99"]["open_scope"], "G99 history promoted")
    require("P1 called metric-derived or a complete history" in by_id["G99"]["forbidden_regression"], "G99 history guard absent")
    require("BAO CMB or endpoint used to retune" in by_id["G99"]["forbidden_regression"], "G99 holdout guard absent")
    require("SNe domain called Xmax" in by_id["G99"]["forbidden_regression"], "G99 Xmax guard absent")
    require(
        by_id["G99"]["controlling_source"]
        == "udt_observed_middle_regime_pair_calibration_2026-08-15/AUDIT_REPORT.md",
        "G99 source changed",
    )
    require("G99_FREEZES_THE_ALREADY_VERIFIED_P1_CENTRAL_LUMINOSITY_RELATION" in by_id["G99"]["precedence_rule"], "G99 precedence absent")
    require(
        by_id["G101"]["current_status"]
        == "INTERNALLY_VERIFIED_WITH_CAVEATS__PARTIAL_CONCEPTUAL_INTEGRATION_ONLY__OBSERVER_CENTERED_TWO_SOURCE_BAO_QUERY_CLARIFIED__MEGAMASER_LOCAL_SLOPE_SOURCE_LEAD__NO_BRANCH_MERGE_OR_XMAX_PROMOTION",
        "G101 integration status regressed or promoted",
    )
    require(by_id["G101"]["epistemic_label"] == "MIXED", "G101 integration label changed")
    require("raw megamaser table and uncertainty replay" in by_id["G101"]["open_scope"], "G101 raw maser replay promoted")
    require("profile selection" in by_id["G101"]["open_scope"], "G101 profile selection promoted")
    require("tanh profile called derived" in by_id["G101"]["forbidden_regression"], "G101 tanh guard absent")
    require("c over H0 or nearby maser slope identified with Xmax" in by_id["G101"]["forbidden_regression"], "G101 Xmax guard absent")
    require("single Earth-source arrow called a two-point angular statistic" in by_id["G101"]["forbidden_regression"], "G101 query-type guard absent")
    require(
        by_id["G101"]["controlling_source"]
        == "udt_grok2_parallel_branch_integration_audit_2026-08-15/AUDIT_REPORT.md",
        "G101 source changed",
    )
    require("G101_RETAINS_ONLY_THE_CORRECTED_OBSERVER_CENTERED_TWO_SOURCE_QUERY" in by_id["G101"]["precedence_rule"], "G101 precedence absent")
    require(
        by_id["G102"]["current_status"]
        == "EXTERNALLY_VERIFIED_WITH_CAVEATS__COMPLETE_TWO_SOURCE_OBSERVABLE_EVALUATOR_DERIVED__DIRECTION_IDENTIFICATION_QUERY_OWNED__ENDPOINT_DEPTH_CARRY_CONDITIONAL__PHYSICAL_HISTORY_AND_SOURCE_PAIR_MEASURE_OPEN",
        "G102 evaluator status regressed or promoted",
    )
    require(by_id["G102"]["epistemic_label"] == "MIXED", "G102 evaluator label changed")
    require("source one and two point measures" in by_id["G102"]["open_scope"], "G102 source measure promoted")
    require("physical complete history" in by_id["G102"]["open_scope"], "G102 history promoted")
    require("conditional evaluator called BAO prediction" in by_id["G102"]["forbidden_regression"], "G102 prediction guard absent")
    require("observer-local h reused as accumulated redshift" in by_id["G102"]["forbidden_regression"], "G102 endpoint guard absent")
    require("image/support qualification dropped" in by_id["G102"]["forbidden_regression"], "G102 support guard absent")
    require(
        by_id["G102"]["controlling_source"]
        == "udt_bao_G102_complete_two_source_observable_map_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G102 source changed",
    )
    require("G102_FRESH_SEALED_REVIEW_REPLAYS_THE_EXACT_TWO_SOURCE_JOIN" in by_id["G102"]["precedence_rule"], "G102 precedence absent")
    require(
        by_id["G103"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__LOCAL_REGULAR_ZERO_AND_FIRST_JET_OBSERVABLE_SURJECTION_DERIVED"
        ),
        "G103 restriction status regressed or promoted",
    )
    require(by_id["G103"]["epistemic_label"] == "MIXED", "G103 restriction label changed")
    require("global singular critical" in by_id["G103"]["open_scope"], "G103 global caveat promoted")
    require("bootstrap or joint source-history" in by_id["G103"]["open_scope"], "G103 bootstrap caveat promoted")
    require("source-bounded local result called a generic no-go" in by_id["G103"]["forbidden_regression"], "G103 no-go guard absent")
    require(
        by_id["G103"]["controlling_source"]
        == "udt_bao_G103_source_independent_restriction_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G103 source changed",
    )
    require("G103_FRESH_SEALED_REVIEW_REPRODUCES_LOCAL_ZERO_AND_FIRST_JET_SURJECTION" in by_id["G103"]["precedence_rule"], "G103 precedence absent")
    require(
        by_id["G104"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__FACTORIZED_REGULAR_KALEIDOSCOPE_NULL_DERIVED"
        ),
        "G104 kaleidoscope status regressed or promoted",
    )
    require(by_id["G104"]["epistemic_label"] == "MIXED", "G104 kaleidoscope label changed")
    require("physical nonzero one-point modulation m" in by_id["G104"]["open_scope"], "G104 modulation promoted")
    require("nonfactorizing positive connected operator H" in by_id["G104"]["open_scope"], "G104 connected operator promoted")
    require("dormant coefficients activated before a basis exists" in by_id["G104"]["forbidden_regression"], "G104 coefficient guard absent")
    require("null source posit called metric-derived" in by_id["G104"]["forbidden_regression"], "G104 source-posit guard absent")
    require(
        by_id["G104"]["controlling_source"]
        == "udt_bao_G104_kaleidoscope_forward_operator_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G104 source changed",
    )
    require("G104_FRESH_SEALED_REVIEW_REPRODUCES_THE_FACTORIZED_NULL" in by_id["G104"]["precedence_rule"], "G104 precedence absent")
    require(
        by_id["G105"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__COMPLETE_ORCHESTRA_ONE_POINT_OBSERVER_ARTIFACT_CHANNEL_DERIVED_CONDITIONALLY"
        ),
        "G105 Jacobian artifact status regressed or promoted",
    )
    require(by_id["G105"]["epistemic_label"] == "MIXED", "G105 Jacobian artifact label changed")
    require("physical complete history and relation family" in by_id["G105"]["open_scope"], "G105 history promoted")
    require("actual survey-random projection" in by_id["G105"]["open_scope"], "G105 reference projection promoted")
    require("global nonfactorizing H" in by_id["G105"]["open_scope"], "G105 H promoted")
    require("conditional existence witness called a physical BAO prediction" in by_id["G105"]["forbidden_regression"], "G105 prediction guard absent")
    require("coefficients activated before a selected basis" in by_id["G105"]["forbidden_regression"], "G105 coefficient guard absent")
    require(
        by_id["G105"]["controlling_source"]
        == "udt_bao_G105_complete_orchestra_two_route_lift_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G105 source changed",
    )
    require("G105_FRESH_SEALED_REVIEW_REPRODUCES_THE_FACTORIZED_NULL" in by_id["G105"]["precedence_rule"], "G105 precedence absent")
    require(
        by_id["G106"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__COMPLETE_SKY_DEPTH_REFERENCE_PROJECTOR_DERIVED_CONDITIONALLY"
        ),
        "G106 sky-depth projector status regressed or promoted",
    )
    require(by_id["G106"]["epistemic_label"] == "MIXED", "G106 projector label changed")
    require("physical complete history and common all-sector realization" in by_id["G106"]["open_scope"], "G106 history promoted")
    require("exact finite random catalog weight and stratum projection" in by_id["G106"]["open_scope"], "G106 finite reference promoted")
    require("angular mode basis and coefficients" in by_id["G106"]["open_scope"], "G106 coefficients promoted")
    require("pure radial abundance called an observable angular pattern" in by_id["G106"]["forbidden_regression"], "G106 radial-null guard absent")
    require("constructive P2 witness called a physical history or BAO prediction" in by_id["G106"]["forbidden_regression"], "G106 witness guard absent")
    require("independent per-window retuning" in by_id["G106"]["forbidden_regression"], "G106 one-history guard absent")
    require("ideal reference operator called the exact finite survey pipeline" in by_id["G106"]["forbidden_regression"], "G106 finite-pipeline guard absent")
    require(
        by_id["G106"]["controlling_source"]
        == "udt_bao_G106_complete_sky_depth_reference_projection_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G106 source changed",
    )
    require("G106_FRESH_SEALED_REVIEW_REPLAYS_ALL_FOUR_EXECUTABLES" in by_id["G106"]["precedence_rule"], "G106 precedence absent")
    require(
        by_id["G107"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__CONSTANT_ZERO_ORDER_O2_SO2_EXTENSION_CENSUS_COMPLETE"
        ),
        "G107 representation census status regressed or promoted",
    )
    require(by_id["G107"]["epistemic_label"] == "MIXED", "G107 census label changed")
    require("physical active action and E/J carry" in by_id["G107"]["open_scope"], "G107 active carry promoted")
    require("field-dependent or query-reduced generators" in by_id["G107"]["open_scope"], "G107 field-dependent scope silently closed")
    require("coefficients" in by_id["G107"]["open_scope"], "G107 coefficient scope promoted")
    require("constant bounded census called the complete orchestra score" in by_id["G107"]["forbidden_regression"], "G107 score-promotion guard absent")
    require("screen dilation a fitted or promoted as physical" in by_id["G107"]["forbidden_regression"], "G107 dilation-promotion guard absent")
    require("complete determinant pairing or exchange silently promoted" in by_id["G107"]["forbidden_regression"], "G107 complete-gate guard absent")
    require(
        by_id["G107"]["controlling_source"]
        == "udt_complete_reciprocal_representation_extension_census_2026-08-16/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G107 source changed",
    )
    require("G107_FRESH_SEALED_REVIEW_AND_CORRECTED_FOLLOWUP_VERIFY" in by_id["G107"]["precedence_rule"], "G107 precedence absent")
    require(
        by_id["G108"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__CONDITIONAL_SCREEN_DILATION_RATE_DERIVED"
        ),
        "G108 screen propagation status regressed or promoted",
    )
    require(by_id["G108"]["epistemic_label"] == "MIXED", "G108 label changed")
    require("delta(lambda) ownership" in by_id["G108"]["open_scope"], "G108 depth map promoted")
    require("initial screen and branch" in by_id["G108"]["open_scope"], "G108 initial data promoted")
    require("universal identification" in by_id["G108"]["open_scope"], "G108 query tie promoted")
    require("automatically called the physical Jacobi map" in by_id["G108"]["forbidden_regression"], "G108 type-tie guard absent")
    require("universal distance-only law" in by_id["G108"]["forbidden_regression"], "G108 distance-law guard absent")
    require("G68 affine rates called dimensionless G107 coefficients" in by_id["G108"]["forbidden_regression"], "G108 unit guard absent")
    require("while shear survives" in by_id["G108"]["forbidden_regression"], "G108 full-family guard absent")
    require(
        by_id["G108"]["controlling_source"]
        == "udt_complete_screen_jacobi_riccati_propagation_atlas_2026-08-16/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G108 source changed",
    )
    require("G108_FRESH_SEALED_REVIEW_AND_CORRECTED_FOLLOWUP_VERIFY" in by_id["G108"]["precedence_rule"], "G108 precedence absent")
    require(
        by_id["G109"]["current_status"].startswith(
            "EXTERNALLY_VERIFIED_WITH_CAVEATS__CONDITIONAL_SAME_QUERY_DEPTH_JOIN_DERIVED"
        ),
        "G109 same-query depth status regressed or promoted",
    )
    require(by_id["G109"]["epistemic_label"] == "MIXED", "G109 label changed")
    require("physical complete metric history and observer query" in by_id["G109"]["open_scope"], "G109 history/query promoted")
    require("branch and initial screen" in by_id["G109"]["open_scope"], "G109 branch/initial data promoted")
    require("global endpoint descent" in by_id["G109"]["open_scope"], "G109 global descent promoted")
    require("conditional same-query endpoint depth called a universal spacetime scalar" in by_id["G109"]["forbidden_regression"], "G109 universal-scalar guard absent")
    require("matched middle calibration omitted" in by_id["G109"]["forbidden_regression"], "G109 middle-reset guard absent")
    require("through dot(phi_pair)=0" in by_id["G109"]["forbidden_regression"], "G109 turning-point guard absent")
    require("through det(W)=0" in by_id["G109"]["forbidden_regression"], "G109 caustic guard absent")
    require(
        by_id["G109"]["controlling_source"]
        == "udt_same_query_terminal_depth_screen_propagation_join_2026-08-16/EXTERNAL_REVIEW_ADJUDICATION.md",
        "G109 source changed",
    )
    require("G109_TWO_SEALED_REVIEWS_VERIFY" in by_id["G109"]["precedence_rule"], "G109 precedence absent")
    require(
        by_id["G110"]["current_status"].startswith(
            "BLIND_VERIFIED_WITH_CAVEATS__OBSERVER_EXPONENTIAL_FULL_DIFFERENTIAL_RECONSTRUCTION_DERIVED_CONDITIONALLY"
        ),
        "G110 full-differential status regressed or promoted",
    )
    require(by_id["G110"]["epistemic_label"] == "MIXED", "G110 label changed")
    require(
        "POINT_OBSERVER_FULL_DIFFERENTIAL" in by_id["G110"]["active_use"],
        "G110 active use changed",
    )
    for token in (
        "physical complete metric history",
        "time-dependent celestial trivialization",
        "global endpoint preimage",
        "actual complete UDT mixed-block replay",
    ):
        require(token in by_id["G110"]["open_scope"], f"G110 open scope promoted: {token}")
    for token in (
        "equal 2x2 size called intrinsic equality",
        "rank-two Jacobi map",
        "universal sky propagation coordinate",
        "basis-free identity",
        "G93 terminal or G108 Jacobi algebra discarded",
    ):
        require(token in by_id["G110"]["forbidden_regression"], f"G110 guard absent: {token}")
    require(
        by_id["G110"]["controlling_source"]
        == "udt_observer_exponential_full_differential_type_audit_2026-08-16/AUDIT_REPORT.md",
        "G110 source changed",
    )
    require(
        "G110_REFINES_G93_G98_G103_G107_G108_G109" in by_id["G110"]["precedence_rule"],
        "G110 precedence absent",
    )

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
        "complete observer/event/path-to-depth assignment",
        "Angular, screen, and mixing data",
        "observed clock/ruler calibration scale",
        "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED",
        "WORKING_FOUNDATIONAL_FRAME",
        "preferred center",
        "S^2` carrier is a `POSIT",
        "EH metric-only action is `CONDITIONAL",
        "Bootstrap/stable-matter is a working hypothesis",
    ]:
        require(token in agents, f"AGENTS guard absent: {token}")

    xmax_controls = (
        "AGENTS.md",
        "LIVE.md",
        "HANDOFF.md",
        "INDEX.md",
        "MEMORY.md",
        "CURRENT_RESEARCH_PROGRAM.md",
        "CURRENT_SCIENTIFIC_PREMISES.md",
    )
    xmax_source = "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md"
    for control in xmax_controls:
        text = (ROOT / control).read_text(encoding="utf-8")
        require("X_max" in text, f"control lacks Xmax guard: {control}")
        require("asymptot" in text.lower(), f"control lacks Xmax limiting meaning: {control}")
    require("udt_xmax_asymptotic_limit_frame_correction_2026-08-05/" in
            (ROOT / "INDEX.md").read_text(encoding="utf-8"),
            "INDEX lacks controlling Xmax correction route")
    require((ROOT / xmax_source).is_file(), "controlling Xmax correction source missing")

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
    print(
        "PASS: G110-extended premise guards; PASS: 97-row premise "
        "registry, current bounded startup route, archive integrity, "
        "relational-depth/orchestra guards, X_max semantics, 754 historical dispositions, "
        "and corrected DOF semantics"
    )


if __name__ == "__main__":
    main()
