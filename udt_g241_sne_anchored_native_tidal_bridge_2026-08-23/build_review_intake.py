#!/usr/bin/env python3
"""Build a sealed G241 review intake without observational outcome files."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
EXCLUDED_NAMES = {
    "EXTERNAL_REVIEW.md",
    "EXTERNAL_REVIEW_RAW.md",
    "REVIEW_REQUEST.md",
    "TRANSMISSION_RECORD.md",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g241_review_", dir="/tmp"))
    package_destination = destination / PACKAGE.name
    package_destination.mkdir()
    copied = []

    for source in sorted(PACKAGE.iterdir()):
        if not source.is_file() or source.name in EXCLUDED_NAMES or source.name.endswith(".pyc"):
            continue
        target = package_destination / source.name
        shutil.copy2(source, target)
        copied.append(target)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in source_rows:
        source = REPO / row["path"]
        assert digest(source) == row["sha256"]
        target = destination / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    expected_state = destination / "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23" / "FROZEN_PRIMARY_K12_STATE.json"
    assert expected_state.is_file()
    assert not (destination / "sources").exists()

    replay_commands = [
        [sys.executable, "-B", str(package_destination / "derive_sne_tidal_bridge.py"), "--no-write"],
        [sys.executable, "-B", str(package_destination / "verify_sne_tidal_bridge_independent.py"), "--no-write"],
        [sys.executable, "-B", str(package_destination / "verify_package.py"), "--no-write"],
        [sys.executable, "-B", str(package_destination / "run_catch_proofs.py"), "--no-write"],
    ]
    replay_rows = []
    for command in replay_commands:
        completed = subprocess.run(command, cwd=destination, check=False, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stdout + completed.stderr
        replay_rows.append(
            {
                "command": command,
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
        )
    replay_result = destination / "SEALED_REPLAY_RESULT.json"
    replay_result.write_text(
        json.dumps(
            {
                "status": "PASS",
                "direct_repository_relative_layout": True,
                "duplicate_sources_tree_absent": True,
                "commands": replay_rows,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    copied.append(replay_result)

    scope = {
        "package": "G241",
        "purpose": "read_only_repair_only_followup_review",
        "allowed": [
            "inspect_only_this_intake",
            "run_bounded_checks_in_ephemeral_copy",
            "verify_only_preregistered_R4",
            "verify_unchanged_bounded_scientific_landing",
        ],
        "forbidden": [
            "edit_evidence_files",
            "continue_research",
            "inspect_BOSS_outcomes",
            "access_repository_outside_intake",
            "access_protected_packages",
        ],
        "repair": "R4_sealed_replay_layout_and_command_scope_only",
        "required_verdict": [
            "G241_BOUNDED_NEGATIVE_ACCEPTED__RADIAL_TO_TIDAL_IDENTITY_RETAINED",
            "G241_REPAIR_REQUIRED__SCIENTIFIC_LANDING_RETAINED",
            "G241_SCIENTIFIC_LANDING_REJECTED",
        ],
        "landing_ceiling": "bounded_2_to_4_coefficient_negative_plus_conditional_radial_to_tidal_identity_only",
        "payload_file_count_excluding_scope_and_manifest": len(copied),
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    manifest_path = destination / "REVIEW_MANIFEST.tsv"
    all_payload = sorted(copied + [scope_path], key=lambda path: str(path.relative_to(destination)))
    with manifest_path.open("w", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["sha256", "bytes", "path"])
        for path in all_payload:
            writer.writerow([digest(path), path.stat().st_size, path.relative_to(destination)])

    print(f"intake={destination}")
    print(f"files_including_scope_and_manifest={len(all_payload) + 1}")
    print(f"scope_sha256={digest(scope_path)}")
    print(f"manifest_sha256={digest(manifest_path)}")


if __name__ == "__main__":
    main()
