"""Regression-lock the bounded current startup route and premise verifier."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import verify_current_scientific_premises as premise_guard


REPO = Path(__file__).resolve().parents[1]
CURRENT_TARGETS = (
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
)


def _startup_copy(tmp_path: Path) -> Path:
    for relative in premise_guard.CURRENT_ORIENTATION_CONTROLS:
        source = REPO / relative
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    for relative in CURRENT_TARGETS:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if relative == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            shutil.copy2(REPO / relative, destination)
        else:
            destination.touch()

    archive = tmp_path / "archive" / "startup_surface_2026-08-14"
    archive.mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        REPO / "archive/startup_surface_2026-08-14/SHA256_MANIFEST.tsv",
        archive / "SHA256_MANIFEST.tsv",
    )
    for name in premise_guard.ARCHIVED_STARTUP_SNAPSHOTS:
        shutil.copy2(REPO / "archive/startup_surface_2026-08-14" / name, archive / name)
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
    assert "PASS: 77-row premise registry" in result.stdout


def test_current_startup_surface_passes_in_isolation(tmp_path: Path) -> None:
    premise_guard.validate_startup_surface(_startup_copy(tmp_path))


def test_catch_duplicate_live_marker(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    live = root / "LIVE.md"
    live.write_text(live.read_text(encoding="utf-8") + "\n<!-- STARTUP_CURRENT_BEGIN -->\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="current-block begin marker count"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_r3_outcome_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "LIVE.md", "R3_OUTCOME_REPORT.md", "REMOVED_R3_OUTCOME.md")
    with pytest.raises(SystemExit, match="marked current block lacks"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_r4_outcome_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "LIVE.md", "R4_OUTCOME_REPORT.md", "REMOVED_R4_OUTCOME.md")
    with pytest.raises(SystemExit, match="marked current block lacks"):
        premise_guard.validate_startup_surface(root)


def test_catch_missing_r5_outcome_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(root / "LIVE.md", "R5_OUTCOME_REPORT.md", "REMOVED_R5_OUTCOME.md")
    with pytest.raises(SystemExit, match="marked current block lacks"):
        premise_guard.validate_startup_surface(root)


def test_catch_stale_active_arc(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    path = root / "INDEX.md"
    path.write_text(path.read_text(encoding="utf-8") + "\nACTIVE ARC = CMB PEAK OPTIMIZATION\n", encoding="utf-8")
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


def test_catch_missing_current_parent_route(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    _replace(
        root / "INDEX.md",
        "udt_pair_terminal_reachability_atlas_2026-08-12/",
        "REMOVED_REACHABILITY/",
    )
    with pytest.raises(SystemExit, match="current route lacks"):
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


def test_catch_missing_current_evidence_target(tmp_path: Path) -> None:
    root = _startup_copy(tmp_path)
    (root / "udt_pair_chord_network_descent_audit_2026-08-12/AUDIT_REPORT.md").unlink()
    with pytest.raises(SystemExit, match="current startup target missing"):
        premise_guard.validate_startup_surface(root)


def test_active_orientation_surface_stays_bounded() -> None:
    limits = {
        "AGENTS.md": 220,
        "LIVE.md": 170,
        "HANDOFF.md": 130,
        "INDEX.md": 100,
        "MEMORY.md": 80,
        "CURRENT_RESEARCH_PROGRAM.md": 170,
        "CURRENT_SCIENTIFIC_PREMISES.md": 150,
        "README.md": 100,
        "research/README.md": 80,
        "research/_registry/README.md": 80,
        "INFLIGHT_STATE.md": 40,
    }
    for relative, maximum in limits.items():
        count = len((REPO / relative).read_text(encoding="utf-8").splitlines())
        assert count <= maximum, f"{relative} regrew to {count} lines (limit {maximum})"


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
    for relative in premise_guard.CURRENT_ORIENTATION_CONTROLS:
        text = (REPO / relative).read_text(encoding="utf-8").lower()
        for token in premise_guard.STALE_STARTUP_TOKENS:
            assert token.lower() not in text, f"{token!r} revived in {relative}"
