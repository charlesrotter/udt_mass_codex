#!/usr/bin/env python3
"""Build and replay a sealed G243 fresh-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
EXTERNAL_ROOT = Path(os.environ["G243_DES_ROOT"]).resolve()
EXCLUDED = {"EXTERNAL_REVIEW.md", "EXTERNAL_REVIEW_RAW.md", "TRANSMISSION_RECORD.md"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preregistration_registry_digest(path: Path) -> str:
    """Retain preregistration lineage after the append-only G243 bank."""
    lines = path.read_bytes().splitlines(keepends=True)
    g243_rows = [line for line in lines if line.startswith(b"G243\t")]
    if not g243_rows:
        return digest(path)
    assert len(g243_rows) == 1, "registry may contain at most one G243 row"
    historical = b"".join(line for line in lines if not line.startswith(b"G243\t"))
    return hashlib.sha256(historical).hexdigest()


def resolve_source(path: str) -> Path:
    if path == "external_data/DES-Dovekie_HD.csv":
        return EXTERNAL_ROOT / "DES-Dovekie_HD.csv"
    if path == "external_data/STAT+SYS.npz":
        return EXTERNAL_ROOT / "STAT+SYS.npz"
    return REPO / path


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g243_review_", dir="/tmp"))
    package_destination = destination / PACKAGE.name
    package_destination.mkdir()
    copied: list[Path] = []

    for source in sorted(PACKAGE.iterdir()):
        if not source.is_file() or source.name in EXCLUDED or source.suffix == ".pyc":
            continue
        target = package_destination / source.name
        shutil.copy2(source, target)
        copied.append(target)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(source_rows) == 8
    for row in source_rows:
        source = resolve_source(row["path"])
        actual = (
            preregistration_registry_digest(source)
            if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv"
            else digest(source)
        )
        assert actual == row["sha256"], row["path"]
        target = destination / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    replay_environment = dict(os.environ)
    replay_environment["G243_DES_ROOT"] = str(destination / "external_data")
    commands = [
        [sys.executable, "-B", str(package_destination / "derive_radial_spline_representation.py"), "--no-write"],
        [sys.executable, "-B", str(package_destination / "verify_radial_spline_independent.py"), "--no-write"],
        [sys.executable, "-B", str(package_destination / "verify_package.py"), "--no-write"],
        [sys.executable, "-B", str(package_destination / "run_catch_proofs.py"), "--no-write"],
    ]
    replay_rows = []
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=destination,
            env=replay_environment,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr
        replay_rows.append(
            {
                "command": command,
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
        )
    replay = destination / "SEALED_REPLAY_RESULT.json"
    replay.write_text(
        json.dumps(
            {
                "status": "PASS",
                "direct_repository_relative_layout": True,
                "commands": replay_rows,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    copied.append(replay)

    scope = {
        "package": "G243",
        "purpose": "fresh_read_only_adversarial_review",
        "allowed": [
            "inspect_only_this_intake",
            "run_registered_no_write_replays",
            "run_bounded_read_only_checks_in_ephemeral_copy",
        ],
        "forbidden": [
            "edit_evidence_files",
            "continue_research",
            "access_repository_outside_intake",
        ],
        "required_verdict": [
            "G243_NO_FREEZE_ACCEPTED__LOCAL_TURNING_CANDIDATE_RETAINED",
            "G243_REPAIR_REQUIRED__SCIENTIFIC_LANDING_RETAINED",
            "G243_SCIENTIFIC_LANDING_REJECTED",
        ],
        "landing_ceiling": (
            "direct_reciprocal_SNe_redshift_plus_uncertified_local_radial_candidate_only__"
            "no_angular_BAO_CMB_Xmax_or_physical_history_claim"
        ),
        "payload_file_count_excluding_scope_and_manifest": len(copied),
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    manifest_path = destination / "REVIEW_MANIFEST.tsv"
    payload = sorted(copied + [scope_path], key=lambda path: str(path.relative_to(destination)))
    with manifest_path.open("w", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["sha256", "bytes", "path"])
        for path in payload:
            writer.writerow([digest(path), path.stat().st_size, path.relative_to(destination)])

    print(f"intake={destination}")
    print(f"files_including_scope_and_manifest={len(payload) + 1}")
    print(f"scope_sha256={digest(scope_path)}")
    print(f"manifest_sha256={digest(manifest_path)}")


if __name__ == "__main__":
    main()
