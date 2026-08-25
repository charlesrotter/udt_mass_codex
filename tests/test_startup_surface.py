"""Regression-lock the bounded current startup route and premise verifier."""

from __future__ import annotations

import shutil
import subprocess
import sys
import re
from pathlib import Path

import pytest

import verify_current_scientific_premises as premise_guard


REPO = Path(__file__).resolve().parents[1]
CURRENT_TARGETS = (
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_observed_angular_pattern_raw_restart_2026-08-12/R2_OUTCOME_REPORT.md",
    "udt_observed_angular_pattern_raw_restart_2026-08-12/R3_OUTCOME_REPORT.md",
    "udt_observed_angular_pattern_raw_restart_2026-08-12/R3_VERIFICATION_RESULT.json",
    "udt_observed_angular_pattern_raw_restart_2026-08-12/R4_OUTCOME_REPORT.md",
    "udt_observed_angular_pattern_raw_restart_2026-08-12/R4_VERIFICATION_RESULT.json",
    "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_OUTCOME_REPORT.md",
    "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_VERIFICATION_RESULT.json",
    "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_EXTERNAL_FOLLOWUP_REVIEW.md",
    "udt_observed_angular_pattern_raw_restart_2026-08-12/R5_FINAL_EVIDENCE_MANIFEST.tsv",
    "udt_boss_primary_method_crosswalk_2026-08-13/AUDIT_REPORT.md",
    "udt_pair_first_relational_plane_reconstruction_2026-08-12/AUDIT_REPORT.md",
    "udt_pair_terminal_reachability_atlas_2026-08-12/AUDIT_REPORT.md",
    "udt_pair_chord_network_descent_audit_2026-08-12/AUDIT_REPORT.md",
    "udt_uncompressed_pair_kernel_reconstruction_2026-08-14/AUDIT_REPORT.md",
    "udt_g116_calibrated_frequency_terminal_pair_junction_2026-08-16/AUDIT_REPORT.md",
    "udt_g119_finite_radius_timelive_spherical_screen_theorem_2026-08-16/AUDIT_REPORT.md",
    "udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20/AUDIT_REPORT.md",
    "udt_g129_copresent_relational_network_faithfulness_2026-08-16/AUDIT_REPORT.md",
    "udt_g130_copresence_rank_complete_network_ownership_2026-08-16/AUDIT_REPORT.md",
    "udt_g131_all_plane_terminal_reciprocal_scalar_faithfulness_2026-08-16/AUDIT_REPORT.md",
    "udt_g132_common_scale_owner_and_anchor_audit_2026-08-16/AUDIT_REPORT.md",
    "udt_g133_fixed_K_two_density_overlap_descent_2026-08-16/AUDIT_REPORT.md",
    "udt_g134_full_metric_area_history_reframe_audit_2026-08-17/AUDIT_REPORT.md",
    "udt_g135_projective_pair_separation_constitution_audit_2026-08-17/AUDIT_REPORT.md",
    "udt_g136_copresent_projective_distance_constitution_2026-08-17/AUDIT_REPORT.md",
    "udt_g137_copresent_relational_position_join_2026-08-17/AUDIT_REPORT.md",
    "udt_g138_copresent_relational_position_network_descent_2026-08-17/AUDIT_REPORT.md",
    "udt_g139_endpoint_position_transport_join_2026-08-17/AUDIT_REPORT.md",
    "udt_g141_endpoint_triangular_transition_inverse_join_2026-08-17/AUDIT_REPORT.md",
    "udt_g142_abstract_carrier_physical_carry_join_2026-08-17/AUDIT_REPORT.md",
    "udt_g143_single_pair_domain_carry_ownership_2026-08-17/AUDIT_REPORT.md",
    "udt_g144_cross_query_overlap_carry_descent_2026-08-17/AUDIT_REPORT.md",
    "udt_g145_copresent_relation_history_descent_equivalence_2026-08-17/AUDIT_REPORT.md",
    "udt_g146_multidirectional_relational_position_composition_2026-08-17/AUDIT_REPORT.md",
    "udt_g147_pair_directional_metric_screen_solder_2026-08-17/AUDIT_REPORT.md",
    "udt_g148_relation_first_pair_first_jet_decomposition_2026-08-17/AUDIT_REPORT.md",
    "udt_g149_genuine_spacetime_pair_first_jet_join_2026-08-17/AUDIT_REPORT.md",
    "udt_g150_first_order_pair_chord_freedom_ceiling_2026-08-17/AUDIT_REPORT.md",
    "udt_g151_pair_chord_generalized_deviation_join_2026-08-17/AUDIT_REPORT.md",
    "udt_g152_pair_immersion_variational_chord_ownership_2026-08-17/AUDIT_REPORT.md",
    "udt_g153_relational_position_ruler_differential_join_2026-08-17/AUDIT_REPORT.md",
    "udt_g154_shared_xmax_asymptotic_response_classification_2026-08-18/AUDIT_REPORT.md",
    "udt_g155_scale_sector_closure_whiteboard_2026-08-18/AUDIT_REPORT.md",
    "udt_g156_three_observer_scale_carry_audit_2026-08-18/AUDIT_REPORT.md",
    "udt_g157_regime_dependent_channel_balance_regrading_2026-08-18/AUDIT_REPORT.md",
    "udt_g158_complete_coframe_semidirect_score_audit_2026-08-18/AUDIT_REPORT.md",
    "udt_g159_complete_score_terminal_descent_2026-08-18/AUDIT_REPORT.md",
    "udt_g160_three_observer_timelive_first_jet_carry_2026-08-18/AUDIT_REPORT.md",
    "udt_g161_pair_carry_lorentz_quotient_screen_resolution_2026-08-18/AUDIT_REPORT.md",
    "udt_g162_lambda_dependence_frontier_census_2026-08-18/AUDIT_REPORT.md",
    "udt_g163_xmax_dependency_reversal_audit_2026-08-18/AUDIT_REPORT.md",
    "udt_g172_primary_metric_smooth_pair_family_integrability_2026-08-19/AUDIT_REPORT.md",
    "udt_g173_primary_metric_turning_chart_calibration_atlas_2026-08-19/AUDIT_REPORT.md",
    "udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/AUDIT_REPORT.md",
    "udt_g200_primary_metric_bidirectional_nonradial_null_2026-08-21/AUDIT_REPORT.md",
    "udt_g201_primary_metric_phi_jet_regime_amplitude_2026-08-21/AUDIT_REPORT.md",
    "udt_g202_quiet_overlap_profile_anchor_classification_2026-08-21/AUDIT_REPORT.md",
    "udt_g203_quiet_overlap_parameter_ownership_classification_2026-08-21/AUDIT_REPORT.md",
    "udt_g204_primary_metric_global_regularity_asymptotic_profile_2026-08-21/AUDIT_REPORT.md",
    "udt_g207_g205_tracefree_screen_timelive_robustness_2026-08-21/AUDIT_REPORT.md",
    "udt_g208_g205_radial_screen_mixing_robustness_2026-08-21/AUDIT_REPORT.md",
    "udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/AUDIT_REPORT.md",
    "udt_g241_sne_anchored_native_tidal_bridge_2026-08-23/AUDIT_REPORT.md",
    "udt_g242_sne_exact_quiet_subfamily_anchor_2026-08-24/AUDIT_REPORT.md",
    "udt_g257_gr_quiet_limit_embedding_audit_2026-08-25/AUDIT_REPORT.md",
)


def _startup_copy(tmp_path: Path) -> Path:
    for relative in premise_guard.STARTUP_SURFACE_CONTROLS:
        source = REPO / relative
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    for relative in premise_guard.MAPPED_SKILL_FILES:
        source = REPO / relative
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    for relative in premise_guard.FIXED_ROOT_PROVENANCE_PATHS:
        source = REPO / relative
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    solver_map = Path("archive/SOLVER_COMPLETENESS_MAP.md")
    solver_map_destination = tmp_path / solver_map
    solver_map_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO / solver_map, solver_map_destination)

    for relative in CURRENT_TARGETS:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if relative == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            shutil.copy2(REPO / relative, destination)
        else:
            destination.touch()

    relocation = Path("research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    relocation_destination = tmp_path / relocation
    relocation_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO / relocation, relocation_destination)

    archive = tmp_path / "archive" / "startup_surface_2026-08-14"
    archive.mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        REPO / "archive/startup_surface_2026-08-14/SHA256_MANIFEST.tsv",
        archive / "SHA256_MANIFEST.tsv",
    )
    for name in premise_guard.ARCHIVED_STARTUP_SNAPSHOTS:
        shutil.copy2(REPO / "archive/startup_surface_2026-08-14" / name, archive / name)

    pre_zoomout = tmp_path / "archive" / "startup_surface_2026-08-17_pre_zoomout"
    pre_zoomout.mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        REPO / "archive/startup_surface_2026-08-17_pre_zoomout/SHA256_MANIFEST.tsv",
        pre_zoomout / "SHA256_MANIFEST.tsv",
    )
    for name in premise_guard.PRE_ZOOMOUT_STARTUP_SNAPSHOTS:
        shutil.copy2(REPO / "archive/startup_surface_2026-08-17_pre_zoomout" / name, pre_zoomout / name)
    return tmp_path


def _replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"catch-proof fixture token absent: {old}"
    path.write_text(text.replace(old, new), encoding="utf-8")


def test_full_foundational_premise_verifier_is_in_pytest() -> None:
    result = subprocess.run(
        [sys.executable, str(REPO / "verify_current_scientific_premises.py")],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    registry_rows = len((REPO / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_text(encoding="utf-8").splitlines()) - 1
    assert f"PASS: {registry_rows}-row premise registry" in result.stdout


def test_catch_scaffolded_kernel_regression_gate_removal(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "AGENTS.md", "Primary-kernel regression gate", "REMOVED_KERNEL_GATE")
    with pytest.raises(SystemExit, match="AGENTS guard absent"):
        premise_guard.validate_startup_surface(root)


def test_current_startup_surface_passes_in_isolation(tmp_path: Path) -> None:
    premise_guard.validate_startup_surface(_startup_copy(tmp_path))


def test_catch_duplicate_live_marker(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    live = root / "LIVE.md"
    live.write_text(live.read_text(encoding="utf-8") + "\n<!-- STARTUP_CURRENT_BEGIN -->\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="current-block begin marker count"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_observational_package_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_observed_angular_pattern_raw_restart_2026-08-12",
        "REMOVED_OBSERVATIONAL_PACKAGE",
    )
    with pytest.raises(SystemExit, match="marked current block lacks"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_raw_archive_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/",
        "REMOVED_RAW_ARCHIVE/",
    )
    with pytest.raises(SystemExit, match="marked current block lacks"):
        premise_guard.validate_startup_surface(root)


@pytest.mark.parametrize("token", ("G166--G258", "G197", "G215", "G216", "G217", "G218", "G219", "G220", "G221", "G222", "G223", "G224", "G225", "G226", "G227", "G228", "G229", "G230", "G231", "G232", "G233", "G234", "G235", "G236", "G237", "G238", "G239", "G240", "G241", "G242", "G243", "G244", "G245", "G246", "G247", "G248", "G249", "G250", "G251", "G252", "G253", "G254", "G255", "G256", "G257", "G258", "G190--G198"))
def test_catch_missing_current_dependency_spine(tmp_path: Path, token: str) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "LIVE.md", token, "REMOVED_CURRENT_SPINE")
    with pytest.raises(SystemExit, match="marked current block lacks"):
        premise_guard.validate_startup_surface(root)


def test_catch_stale_active_arc(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    path = root / "INDEX.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nACTIVE ARC = CMB PEAK OPTIMIZATION\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="stale startup token"):
        premise_guard.validate_startup_surface(root)


def test_catch_stale_readme_frontier(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    path = root / "README.md"
    path.write_text(
        path.read_text(encoding="utf-8")
        + "\nThe current spine culminates in the G129--G133 reconstruction/ownership chain.\n",
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="stale startup token"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_protected_pair_response(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/",
        "REMOVED_PAIR_RESPONSE/",
    )
    with pytest.raises(SystemExit, match="protected local path"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_handoff_protected_path(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "HANDOFF.md",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/",
        "REMOVED_G88/",
    )
    with pytest.raises(SystemExit, match="HANDOFF lacks protected local path"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_current_parent_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "INDEX.md",
        "udt_pair_terminal_reachability_atlas_2026-08-12/",
        "REMOVED_REACHABILITY/",
    )
    with pytest.raises(SystemExit, match="current route lacks"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_g203_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "INDEX.md",
        "udt_g203_quiet_overlap_parameter_ownership_classification_2026-08-21/",
        "REMOVED_G203/",
    )
    with pytest.raises(SystemExit, match="current route lacks"):
        premise_guard.validate_startup_surface(root)


def test_catch_historical_root_guard_removal(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    path = root / "UDT_ELEGANT_FRAME.md"
    _replace(
        path,
        "HISTORICAL WORKING FRAME — NOT CURRENT BINDING STATUS",
        "UNBANNERED WORKING FRAME",
    )
    with pytest.raises(SystemExit, match="historical root guard missing"):
        premise_guard.validate_startup_surface(root)


def test_catch_scaffold_quarantine_route_removal(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "INDEX.md",
        "archive/scaffolded_kernel_controls_2026-08-19/README.md",
        "REMOVED_SCAFFOLD_QUARANTINE",
    )
    with pytest.raises(SystemExit, match="current route lacks"):
        premise_guard.validate_startup_surface(root)


def test_catch_obsolete_completeness_target(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    path = root / ".claude/skills/completeness-map/SKILL.md"
    _replace(
        path,
        "`archive/SOLVER_COMPLETENESS_MAP.md` and subsumed",
        "use root `SOLVER_COMPLETENESS_MAP.md`",
    )
    with pytest.raises(SystemExit, match="completeness skill"):
        premise_guard.validate_startup_surface(root)


def test_catch_obsolete_solver_first_target(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    path = root / ".claude/skills/solver-first/SKILL.md"
    _replace(path, "`archive/SOLVER_COMPLETENESS_MAP.md`", "`SOLVER_COMPLETENESS_MAP.md`")
    with pytest.raises(SystemExit, match="solver-first skill"):
        premise_guard.validate_startup_surface(root)


def test_catch_chosen_family_mislabeled_current(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "INDEX.md", "Chosen-family evaluators/controls:", "Current longitudinal result:")
    with pytest.raises(SystemExit, match="INDEX chosen-family/scaffold quarantine"):
        premise_guard.validate_startup_surface(root)


def test_catch_fixed_root_quarantine_removal(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "README.md", "codex_rehearsal_final.md", "REMOVED_REHEARSAL_FINAL.md")
    with pytest.raises(SystemExit, match="current route lacks|README lacks fixed-root quarantine"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_complete_startup_order(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "INDEX.md", "`CLAUDE.md`", "`REMOVED_CHARTER.md`")
    with pytest.raises(SystemExit, match="current route lacks CLAUDE.md"):
        premise_guard.validate_startup_surface(root)


def test_catch_abbreviated_readme_startup_order(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "README.md", "CLAUDE.md", "REMOVED_CHARTER.md")
    with pytest.raises(SystemExit, match="current route lacks CLAUDE.md"):
        premise_guard.validate_startup_surface(root)


def test_catch_weakened_mandatory_claude_sections(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "README.md", "DRIVER TRIGGERS", "TASK_TRIGGERED_ONLY")
    with pytest.raises(SystemExit, match="current route lacks DRIVER TRIGGERS"):
        premise_guard.validate_startup_surface(root)


def test_catch_reordered_startup_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "README.md",
        "1. `LIVE.md` — only its `STARTUP_CURRENT` block;\n2. `HANDOFF.md` — only its matching current block;",
        "2. `HANDOFF.md` — only its matching current block;\n1. `LIVE.md` — only its `STARTUP_CURRENT` block;",
    )
    with pytest.raises(SystemExit, match="startup order broken"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_driver_skill_mapping(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "CLAUDE.md",
        "mnemonic trigger labels, not filesystem paths",
        "unspecified trigger references",
    )
    with pytest.raises(SystemExit, match="current route lacks mnemonic trigger labels"):
        premise_guard.validate_startup_surface(root)


def test_catch_swapped_driver_skill_mapping(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    claude = root / "CLAUDE.md"
    text = claude.read_text(encoding="utf-8")
    no_shortcuts = ".claude/skills/no-shortcuts/SKILL.md"
    solver_first = ".claude/skills/solver-first/SKILL.md"
    assert no_shortcuts in text and solver_first in text
    text = text.replace(no_shortcuts, "MAPPING_SWAP_PLACEHOLDER", 1)
    text = text.replace(solver_first, no_shortcuts, 1)
    text = text.replace("MAPPING_SWAP_PLACEHOLDER", solver_first, 1)
    claude.write_text(text, encoding="utf-8")
    with pytest.raises(SystemExit, match="CLAUDE skill mapping missing or changed"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_mapped_skill_file(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    (root / ".claude/skills/no-shortcuts/SKILL.md").unlink()
    with pytest.raises(SystemExit, match="mapped CLAUDE skill missing"):
        premise_guard.validate_startup_surface(root)


def test_catch_hard_coded_readme_frontier(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    readme = root / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8")
        + "\nCurrent: `udt_g153_relational_position_ruler_differential_join_2026-08-17/`.\n",
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="README hard-codes a moving G-frontier package"):
        premise_guard.validate_startup_surface(root)


def test_catch_bare_hard_coded_readme_frontier(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    readme = root / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\nCurrent: udt_g154.\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="README hard-codes a moving G-frontier package"):
        premise_guard.validate_startup_surface(root)


def test_catch_ambiguous_research_index_wording(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "research/README.md",
        "Use root `INDEX.md` for the compact current-frontier path list. The relocation ledger is not a",
        "Use root `INDEX.md` for the compact current-frontier path list. It is not a",
    )
    with pytest.raises(SystemExit, match="ambiguously says INDEX.md"):
        premise_guard.validate_startup_surface(root)


def test_catch_relocation_row_count_mutation(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    ledger = root / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv"
    lines = ledger.read_text(encoding="utf-8").splitlines()
    ledger.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="relocation ledger must have 1,114 data rows plus header"):
        premise_guard.validate_startup_surface(root)


def test_catch_relocation_header_mutation(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    ledger = root / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv"
    lines = ledger.read_text(encoding="utf-8").splitlines()
    lines[0] = "mutated_header"
    ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="relocation ledger header changed"):
        premise_guard.validate_startup_surface(root)


def test_catch_relocation_blank_row_substitution(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    ledger = root / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv"
    lines = ledger.read_text(encoding="utf-8").splitlines()
    lines[1] = ""
    ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="1,114 parsed data rows"):
        premise_guard.validate_startup_surface(root)


def test_catch_claude_handoff_order_omission(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "CLAUDE.md", "Follow it with `HANDOFF.md`,", "Continue directly to")
    with pytest.raises(SystemExit, match="startup order broken at `HANDOFF.md`"):
        premise_guard.validate_startup_surface(root)


def test_catch_readme_late_premise_verifier(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace(
        ", then `python3 verify_current_scientific_premises.py` — bounded\n   premise orientation plus full-registry consistency;",
        " — bounded premise orientation;",
    )
    text += "\nAfter all startup steps run `python3 verify_current_scientific_premises.py`.\n"
    readme.write_text(text, encoding="utf-8")
    with pytest.raises(SystemExit, match="startup order broken"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_premise_registry_pointer(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "README.md", "CURRENT_SCIENTIFIC_PREMISES.tsv", "REMOVED_PREMISE_REGISTRY.tsv")
    with pytest.raises(SystemExit, match="control lacks premise registry"):
        premise_guard.validate_startup_surface(root)


def test_catch_reactivated_inflight_state(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "INFLIGHT_STATE.md", "retired compatibility pointer", "active status ledger")
    with pytest.raises(SystemExit, match="current route lacks"):
        premise_guard.validate_startup_surface(root)


def test_catch_archive_snapshot_mutation(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    path = root / "archive/startup_surface_2026-08-14/LIVE_before_cleanup.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nmutation\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="startup archive hash mismatch"):
        premise_guard.validate_startup_surface(root)


def test_catch_pre_zoomout_archive_snapshot_mutation(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    path = root / "archive/startup_surface_2026-08-17_pre_zoomout/LIVE.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nmutation\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="pre-zoomout archive hash mismatch"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_current_evidence_target(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    (root / "udt_pair_chord_network_descent_audit_2026-08-12/AUDIT_REPORT.md").unlink()
    with pytest.raises(SystemExit, match="current startup target missing"):
        premise_guard.validate_startup_surface(root)


def test_active_orientation_surface_stays_readably_bounded() -> None:
    limits = {
        "AGENTS.md": (220, 1800),
        "LIVE.md": (135, 900),
        "HANDOFF.md": (100, 600),
        "INDEX.md": (110, 550),
        "MEMORY.md": (70, 450),
        "CURRENT_RESEARCH_PROGRAM.md": (155, 1100),
        "CURRENT_SCIENTIFIC_PREMISES.md": (135, 1250),
        "README.md": (100, 400),
        "research/README.md": (80, 300),
        "research/_registry/README.md": (80, 280),
        "INFLIGHT_STATE.md": (40, 150),
    }
    for relative, (maximum_lines, maximum_words) in limits.items():
        text = (REPO / relative).read_text(encoding="utf-8")
        lines = text.splitlines()
        words = text.split()
        assert len(lines) <= maximum_lines, (
            f"{relative} regrew to {len(lines)} lines (limit {maximum_lines})"
        )
        assert len(words) <= maximum_words, (
            f"{relative} regrew to {len(words)} words (limit {maximum_words})"
        )
        longest = max((len(line) for line in lines), default=0)
        assert longest <= 220, f"{relative} contains a {longest}-character compressed line"


def test_startup_keeps_dependency_spine_not_execution_chronology() -> None:
    for relative in (
        "LIVE.md",
        "HANDOFF.md",
        "CURRENT_RESEARCH_PROGRAM.md",
        "CURRENT_SCIENTIFIC_PREMISES.md",
        "INDEX.md",
        "MEMORY.md",
    ):
        text = (REPO / relative).read_text(encoding="utf-8")
        mentions = re.findall(r"\bG(?:9\d|1\d\d)\b", text)
        assert len(mentions) <= 24, (
            f"{relative} regrew an execution chronology with {len(mentions)} G-result mentions"
        )


def test_startup_does_not_promote_full_evidence_or_relocation_dump() -> None:
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    index = (REPO / "INDEX.md").read_text(encoding="utf-8")
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    registry = (REPO / "research/_registry/README.md").read_text(encoding="utf-8")
    assert "Stop the startup read here" in agents
    assert "does not make full scripts" in agents
    assert "without dumping its wide rows into model context" in agents
    assert "not a startup read or a current-frontier index" in agents
    assert "not a startup read" in registry
    assert "not a current-frontier index" in registry
    assert "After orientation" in index
    assert "verify_current_scientific_premises.py" in index
    assert "after orientation" in readme
    assert "verify_current_scientific_premises.py" in readme


def test_retired_route_words_absent_from_active_orientation() -> None:
    for relative in premise_guard.STARTUP_SURFACE_CONTROLS:
        text = (REPO / relative).read_text(encoding="utf-8").lower()
        for token in premise_guard.STALE_STARTUP_TOKENS:
            assert token.lower() not in text, f"{token!r} revived in {relative}"
