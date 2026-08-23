#!/usr/bin/env python3
"""Build a sealed G237 intake with exact source and raw replay inputs."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DES_ROOT = Path(os.environ["G237_DES_ROOT"]).resolve()
HISTORICAL_PREMISE_COMMIT = "650170087c661f246d301c3dba2f266e4a8695b7"

PACKAGE_FILES = [
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "AUDIT_REPORT.md",
    "CATCH_PROOF_RESULT.json",
    "CHRONOLOGY_BUNDLE_VERIFICATION.json",
    "CHRONOLOGY_OBJECT_BUNDLE.json",
    "CHRONOLOGY_PROOF.json",
    "COMMANDS.md",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "EXTERNAL_REVIEW.md",
    "FROZEN_PRIMARY_K12_STATE.json",
    "INDEPENDENT_RAW_GLS.json",
    "JOINT_STATE.tsv",
    "JOINT_STATE_RESULT.json",
    "LAY_REPORT.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "REPAIR_CERTIFICATION.json",
    "REPAIR_FOLLOWUP_REQUEST.md",
    "REPAIR_PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "STATUS_LEDGER.tsv",
    "VERIFICATION_RESULT.json",
    "build_chronology_proof.py",
    "build_review_intake.py",
    "derive_joint_state.py",
    "run_catch_proofs.py",
    "verify_joint_state_from_raw.py",
    "verify_chronology_bundle.py",
    "verify_package.py",
    "verify_repair.py",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def resolve_underlying(logical: str) -> Path:
    external = {
        "external_data/README.md": DES_ROOT / "README.md",
        "external_data/DES-Dovekie_HD.csv": DES_ROOT / "DES-Dovekie_HD.csv",
        "external_data/STAT+SYS.npz": DES_ROOT / "STAT+SYS.npz",
    }
    return external.get(logical, ROOT / logical)


def copy_file(source: Path, target: Path, copied: set[Path]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    copied.add(target)


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g237_review_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()
    copied: set[Path] = set()

    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        copy_file(source, package_target / name, copied)

    # G237's immediate frozen G236 sources.
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        g237_rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in g237_rows:
        source = ROOT / row["path"]
        if not source.is_file() or digest(source) != row["sha256"]:
            raise RuntimeError(f"G237 source mismatch: {row['path']}")
        copy_file(source, intake / row["path"], copied)

    # Exact raw/source spine needed by the independent replay.
    g236_manifest = ROOT / "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/SOURCE_MANIFEST.tsv"
    with g236_manifest.open(newline="") as stream:
        g236_rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in g236_rows:
        logical = row["path"]
        target = intake / logical
        if logical == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            data = subprocess.check_output(
                ["git", "show", f"{HISTORICAL_PREMISE_COMMIT}:{logical}"], cwd=ROOT
            )
            if hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise RuntimeError("historical premise hash mismatch")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            copied.add(target)
            continue
        source = resolve_underlying(logical)
        if not source.is_file() or digest(source) != row["sha256"]:
            raise RuntimeError(f"G236 underlying source mismatch: {logical}")
        copy_file(source, target, copied)

    entries = [
        {"path": str(path.relative_to(intake)), "sha256": digest(path)}
        for path in sorted(copied)
    ]
    tree_material = "".join(
        f"{entry['sha256']}  {entry['path']}\n" for entry in entries
    ).encode()
    scope = {
        "task": "repair-only read-only follow-up review of G237 R1-R4",
        "instructions": str(Path(PACKAGE.name) / "REPAIR_FOLLOWUP_REQUEST.md"),
        "replay_environment": {"G237_DES_ROOT": str(intake / "external_data")},
        "restrictions": [
            "inspect only this sealed intake",
            "run bounded read-only checks or registered replays in an ephemeral copy",
            "do not edit evidence files",
            "do not continue the research",
            "do not inspect BAO or CMB outcomes outside the intake",
            "verify only preregistered repairs R1-R4 and the unchanged scientific landing",
        ],
        "payload_file_count": len(entries),
        "tree_digest_sha256": hashlib.sha256(tree_material).hexdigest(),
        "files": entries,
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake),
        "payload_file_count": len(entries),
        "total_file_count_including_scope": len(entries) + 1,
        "tree_digest_sha256": scope["tree_digest_sha256"],
        "review_scope_sha256": digest(scope_path),
    }, indent=2))


if __name__ == "__main__":
    main()
