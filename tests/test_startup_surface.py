"""Regression-lock the bounded current startup route and foundational premise verifier."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import verify_current_scientific_premises as premise_guard


REPO = Path(__file__).resolve().parents[1]
TARGETS = (
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_ordered_observer_query_projection_ownership_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_multichannel_observer_relation_assembly_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_r17_stationary_local_one_form_selection_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_r17_depth_holonomy_joint_invariant_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_r17_stationary_connection_sublocus_ownership_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_nonisometric_calibration_magnitude_owner_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_reciprocal_scalar_calibration_bitorsor_descent_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_carried_intrinsic_middle_morphism_ownership_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_global_relation_family_branch_classification_2026-08-10/AUDIT_REPORT.md",
    "udt_three_observer_overlap_calibration_carry_audit_2026-08-10/AUDIT_REPORT.md",
    "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/AUDIT_REPORT.md",
    "udt_reciprocal_calibration_state_solder_audit_2026-08-09/AUDIT_REPORT.md",
    "udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/AUDIT_REPORT.md",
    "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/AUDIT_REPORT.md",
    "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/AUDIT_REPORT.md",
    "udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md",
    "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md",
    "udt_freedata_inventory_MAP_2026-08-09.md",
    "udt_roadA_mode_quantization_MAP_2026-08-08.md",
    "udt_roadA_RA1_muon_modes_2026-08-08/DERIVATION_NOTES.md",
    "udt_roadA_RA2_projection_2026-08-08/DERIVATION_NOTES.md",
    "udt_complete_pair_phi_orchestra_audit_2026-08-05/AUDIT_REPORT.md",
)


def _startup_copy(tmp_path: Path) -> Path:
    controls = set(
        premise_guard.PREMISE_REGISTRY_CONTROLS
        + premise_guard.PROTECTED_ATLAS_CONTROLS
        + premise_guard.CURRENT_ROUTE_CONTROLS
        + premise_guard.LATEST_ROUTE_CONTROLS
    )
    for relative in controls:
        source = REPO / relative
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    for relative in TARGETS:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            destination.touch()
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
    assert "PASS: 54 premise guards" in result.stdout


def test_catch_missing_current_ordered_query_projection_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_ordered_observer_query_projection_ownership_audit_2026-08-10/AUDIT_REPORT.md",
        "ORDERED_QUERY_PROJECTION_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="ordered_observer_query_projection_ownership|latest complete-branch route"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_current_multichannel_assembly_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_multichannel_observer_relation_assembly_audit_2026-08-10/AUDIT_REPORT.md",
        "MULTICHANNEL_ASSEMBLY_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="multichannel_observer_relation_assembly|latest complete-branch route"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_current_stationary_one_form_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_r17_stationary_local_one_form_selection_audit_2026-08-10/AUDIT_REPORT.md",
        "R17_STATIONARY_ONE_FORM_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="stationary_local_one_form_selection|latest complete-branch route"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_current_path_connection_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/AUDIT_REPORT.md",
        "R17_PATH_CONNECTION_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="path_labelled_connection_decomposition|latest complete-branch route"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_current_joint_invariant_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_r17_depth_holonomy_joint_invariant_audit_2026-08-10/AUDIT_REPORT.md",
        "R17_JOINT_INVARIANT_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="depth_holonomy_joint_invariant|latest complete-branch route"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_current_magnitude_owner_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_nonisometric_calibration_magnitude_owner_audit_2026-08-10/AUDIT_REPORT.md",
        "MAGNITUDE_OWNER_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="nonisometric_calibration_magnitude_owner|latest complete-branch route"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_live_premise_pointer(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "LIVE.md", "CURRENT_SCIENTIFIC_PREMISES.tsv", "PREMISE_REGISTRY_REMOVED.tsv")
    with pytest.raises(SystemExit, match="premise registry"):
        premise_guard.validate_startup_surface(root)


@pytest.mark.parametrize("control", ("LIVE.md", "HANDOFF.md"))
def test_catch_missing_current_atlas_authorization(tmp_path: Path, control: str) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / control, "explicit later dispatch", "unspecified future dispatch")
    with pytest.raises(SystemExit, match="protected-atlas guard"):
        premise_guard.validate_startup_surface(root)


def test_catch_stale_xmax_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "LIVE.md", "CMB PEAK OPTIMIZATION", "x_max O1 pending")
    with pytest.raises(SystemExit, match="marked current block"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_xmax_semantic_guard(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md",
        "XMAX_CONTROLLING_SOURCE_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="marked current block"):
        premise_guard.validate_startup_surface(root)


def test_catch_lost_ra2_or_bao_status(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "README.md", "RA2-PARTIAL-WEAK", "RA2")
    _replace(root / "README.md", "BANKED + TABLED", "complete")
    with pytest.raises(SystemExit, match="RA2 grade|BAO status"):
        premise_guard.validate_startup_surface(root)


def test_catch_stale_memory_top(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "MEMORY.md", "2026-08-10", "2026-08-05")
    _replace(root / "MEMORY.md", "CMB PEAK OPTIMIZATION", "complete-pair cocycle home")
    with pytest.raises(SystemExit, match="MEMORY top pointer|current route lacks CMB PEAK OPTIMIZATION"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_founding_pair_relation_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/AUDIT_REPORT.md",
        "FOUNDING_PAIR_RELATION_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="founding_pair_relation_functor_ownership|current startup target"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_three_observer_overlap_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_three_observer_overlap_calibration_carry_audit_2026-08-10/AUDIT_REPORT.md",
        "THREE_OBSERVER_OVERLAP_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="three_observer_overlap_calibration_carry|current startup target"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_corrected_fd1_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md",
        "CORRECTED_FD1_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="corrected_full_spectral_atlas|current startup target"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_n02_radial_admissibility_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/AUDIT_REPORT.md",
        "N02_ADMISSIBILITY_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="N02_radial_anchor_admissibility|current startup target"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_n03_profile_role_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_cmb_N03_profile_role_regular_center_map_2026-08-09/AUDIT_REPORT.md",
        "N03_PROFILE_ROLE_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="N03_profile_role_regular_center_map|current startup target"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_reciprocal_flag_ownership_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/AUDIT_REPORT.md",
        "RECIPROCAL_FLAG_OWNERSHIP_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="reciprocal_flag_foundation_ownership|current startup target"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_calibration_state_solder_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_reciprocal_calibration_state_solder_audit_2026-08-09/AUDIT_REPORT.md",
        "CALIBRATION_STATE_SOLDER_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="reciprocal_calibration_state_solder|current startup target"):
        premise_guard.validate_startup_surface(root)


def test_catch_revived_old_fd1_window(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "HANDOFF.md",
        "OPEN-COMPATIBILITY-WINDOW` is WITHDRAWN",
        "OPEN-COMPATIBILITY-WINDOW` is ACTIVE",
    )
    with pytest.raises(SystemExit, match="corrected FD1 withdrawal"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_complete_angular_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "LIVE.md",
        "udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md",
        "COMPLETE_ANGULAR_REPORT_REMOVED.md",
    )
    with pytest.raises(SystemExit, match="complete_angular_mode_ownership|current startup target"):
        premise_guard.validate_startup_surface(root)
