#!/usr/bin/env python3
"""Build a sealed G292 repair-only follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
ORIGINAL = Path("/tmp/udt_g292_review_2j8fc8rg")

CORRECTED_FILES = (
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "CATCH_PROOF_RESULT.json",
    "COMPLETENESS_MAP.md",
    "DERIVATION_RESULT.json",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "EXTERNAL_REVIEW_GPT54.md",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
    "INDEPENDENT_VERIFICATION.json",
    "LAY_REPORT.md",
    "MAP.md",
    "PACKAGE_VERIFICATION_RESULT.json",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "REPAIR_FOLLOWUP_REQUEST.md",
    "REPAIR_PREREGISTRATION.md",
    "REPAIR_REPORT.md",
    "REPAIR_VERIFICATION_RESULT.json",
    "RUN_RECORD.md",
    "STATUS_LEDGER.tsv",
    "derive_orientable_screen_flux.py",
    "run_orientable_screen_flux_catches.py",
    "verify_orientable_screen_flux_independent.py",
    "verify_package.py",
    "verify_repairs.py",
)

ORIGINAL_FILES = (
    "REVIEW_SCOPE.json",
    "REVIEW_MANIFEST.tsv",
    "REVIEW_MANIFEST.sha256",
    f"{PACKAGE.name}/EVIDENCE_GATES.md",
    f"{PACKAGE.name}/EXACT_DERIVATION.md",
    f"{PACKAGE.name}/RUN_RECORD.md",
    f"{PACKAGE.name}/verify_package.py",
)

PROTECTED_FRAGMENTS = (
    "8_25",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
    "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
    "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_path(source: Path, target: Path) -> None:
    relative = target.as_posix()
    if any(fragment in relative for fragment in PROTECTED_FRAGMENTS):
        raise AssertionError(f"protected path rejected: {relative}")
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    if sha256(ORIGINAL / "REVIEW_SCOPE.json") != "42a5b2303b1a2356afd338847b5ed1a3622ce7223cc25e2f0a01ae2198a019a5":
        raise AssertionError("original review scope seal changed")
    if sha256(ORIGINAL / "REVIEW_MANIFEST.tsv") != "5f91630d9b34dcd15cd675e419ff20197982e8f8826edcec790311d8ca196d3b":
        raise AssertionError("original review manifest seal changed")

    destination = Path(tempfile.mkdtemp(prefix="udt_g292_repair_followup_", dir="/tmp"))
    for filename in CORRECTED_FILES:
        copy_path(PACKAGE / filename, destination / PACKAGE.name / filename)
    for relative in ORIGINAL_FILES:
        copy_path(ORIGINAL / relative, destination / "ORIGINAL_SEALED_G292" / relative)

    scope = {
        "audit": "G292_REPAIRS_R1_R4_ONLY",
        "mode": "read-only repair-only follow-up review",
        "allowed": (
            "inspect only the sealed intake; compare corrected files to ORIGINAL_SEALED_G292; "
            "run verify_repairs.py or bounded repair checks only in a writable ephemeral copy"
        ),
        "forbidden": (
            "edit evidence files, continue or change the scientific question, access repository "
            "files outside the intake or protected packages, use the internet, or inspect "
            "observational outcomes"
        ),
        "scientific_landing_must_remain_unchanged": True,
        "registered_repairs": ["R1", "R2", "R3", "R4"],
        "original_scope_sha256": "42a5b2303b1a2356afd338847b5ed1a3622ce7223cc25e2f0a01ae2198a019a5",
        "original_manifest_sha256": "5f91630d9b34dcd15cd675e419ff20197982e8f8826edcec790311d8ca196d3b",
    }
    (destination / "REVIEW_SCOPE.json").write_text(
        json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    manifest_rows = []
    for path in sorted(item for item in destination.rglob("*") if item.is_file()):
        relative = path.relative_to(destination).as_posix()
        if any(fragment in relative for fragment in PROTECTED_FRAGMENTS):
            raise AssertionError(f"protected path entered intake: {relative}")
        manifest_rows.append((relative, path.stat().st_size, sha256(path)))
    manifest = destination / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "bytes", "sha256"))
        writer.writerows(manifest_rows)
    seal = destination / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{sha256(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

    print(json.dumps({
        "path": str(destination),
        "payloads": len(manifest_rows),
        "total_files": len(manifest_rows) + 2,
        "scope_sha256": sha256(destination / "REVIEW_SCOPE.json"),
        "manifest_sha256": sha256(manifest),
        "seal_sha256": sha256(seal),
        "corrected_files": len(CORRECTED_FILES),
        "original_control_files": len(ORIGINAL_FILES),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
