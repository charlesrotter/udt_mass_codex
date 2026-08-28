#!/usr/bin/env python3
"""Build a sealed, source-bounded G290 external-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
EVIDENCE_COMMIT = "48b3af81"

SOURCE_PATHS = (
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_g225_shared_event_normal_screen_carry_2026-08-22/AUDIT_REPORT.md",
    "udt_g226_null_chain_conformal_symplectic_assembly_2026-08-22/AUDIT_REPORT.md",
    "udt_g274_projective_pair_position_network_descent_2026-08-26/AUDIT_REPORT.md",
    "udt_g289_native_kernel_hopfion_compatibility_history_constraint_audit_2026-08-28/AUDIT_REPORT.md",
    "udt_g289_native_kernel_hopfion_compatibility_history_constraint_audit_2026-08-28/EXACT_DERIVATION.md",
    "udt_g289_native_kernel_hopfion_compatibility_history_constraint_audit_2026-08-28/EXTERNAL_REVIEW_GPT54.md",
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


def git_blob(commit: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def evidence_package_paths() -> list[str]:
    completed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", EVIDENCE_COMMIT, PACKAGE.name],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return [line for line in completed.stdout.splitlines() if line]


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g290_review_", dir="/tmp"))

    package_paths = evidence_package_paths()
    if len(package_paths) != 22:
        raise AssertionError(f"expected 22 banked G290 evidence files, found {len(package_paths)}")
    for relative in package_paths:
        if any(fragment in relative for fragment in PROTECTED_FRAGMENTS):
            raise AssertionError(f"protected path rejected: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git_blob(EVIDENCE_COMMIT, relative))

    request_relative = f"{PACKAGE.name}/ADVERSARIAL_REVIEW_REQUEST.md"
    request_bytes = git_blob("HEAD", request_relative)
    if request_bytes != (PACKAGE / "ADVERSARIAL_REVIEW_REQUEST.md").read_bytes():
        raise AssertionError("review request changed after packaging commit")
    request_target = destination / request_relative
    request_target.write_bytes(request_bytes)

    source_rows = []
    for relative in SOURCE_PATHS:
        if any(fragment in relative for fragment in PROTECTED_FRAGMENTS):
            raise AssertionError(f"protected source rejected: {relative}")
        payload = git_blob(EVIDENCE_COMMIT, relative)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        source_rows.append((relative, len(payload), hashlib.sha256(payload).hexdigest()))

    source_manifest = destination / "SOURCE_MANIFEST.tsv"
    with source_manifest.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("source", "bytes", "sha256"))
        writer.writerows(source_rows)

    scope = {
        "audit": "G290_COMPLETE_PAIR_SCREEN_HOLONOMY_AND_TIMELIVE_TRANSGRESSION",
        "mode": "fresh read-only adversarial review",
        "allowed": (
            "inspect only the sealed intake; independently recompute the projected screen connection, "
            "SO2 and O2 descent, conformal-twin separator, phase alias controls, and time-live "
            "transgression; run registered replays or bounded checks only in a writable ephemeral copy"
        ),
        "forbidden": (
            "edit evidence files, continue the research, access repository files outside the intake "
            "or protected packages, use the internet, inspect observational outcomes, or import an "
            "action, source, field equation, matter model, mass, scale, Planck cutoff, physical "
            "history, loop population, boundary, X_max, fixed round carrier, or canonization"
        ),
        "scientific_ceiling": (
            "bounded conditional complete-pair projected-screen connection and holonomy descent, "
            "registered flat/nonflat conformal-history discrimination, time-live curvature-flux "
            "transgression, and explicit nonselection"
        ),
        "evidence_commit": EVIDENCE_COMMIT,
        "immutable_sources": len(SOURCE_PATHS),
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
        "immutable_sources": len(SOURCE_PATHS),
        "evidence_commit": EVIDENCE_COMMIT,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
