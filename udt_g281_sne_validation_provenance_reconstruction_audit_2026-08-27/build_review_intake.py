#!/usr/bin/env python3
"""Build a sealed, source-bounded G281 external-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent

REPLAY_DEPENDENCIES = (
    "verify_luminosity_distance_n2.py",
    "udt_xmax_scale_observational_M3_runs_2026-08-07/sne_results.json",
    "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/PRODUCTION_RESULT.json",
    "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/JOINT_STATE_RESULT.json",
    "udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/DERIVATION_RESULT.json",
    "udt_g279_native_kernel_observational_interface_provenance_audit_2026-08-27/DERIVATION_RESULT.json",
    "udt_g280_projective_position_optical_area_bridge_audit_2026-08-27/DERIVATION_RESULT.json",
)

PROTECTED_FRAGMENTS = (
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


def copy_relative(relative: str, destination: Path) -> None:
    if any(fragment in relative for fragment in PROTECTED_FRAGMENTS):
        raise AssertionError(f"protected path rejected: {relative}")
    source = ROOT / relative
    if not source.is_file():
        raise FileNotFoundError(source)
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g281_review_", dir="/tmp"))
    package_destination = destination / PACKAGE.name
    package_destination.mkdir()

    excluded_generated = {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256", "REVIEW_SCOPE.json"}
    for source in sorted(PACKAGE.iterdir()):
        if source.is_file() and source.name not in excluded_generated:
            shutil.copy2(source, package_destination / source.name)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(source_rows) != 32:
        raise AssertionError(f"expected 32 immutable sources, found {len(source_rows)}")
    for row in source_rows:
        relative = row["path"]
        source = ROOT / relative
        if sha256(source) != row["sha256"]:
            raise AssertionError(f"source hash changed: {relative}")
        copy_relative(relative, destination)

    for relative in REPLAY_DEPENDENCIES:
        copy_relative(relative, destination)

    scope = {
        "audit": "G281_SNE_VALIDATION_PROVENANCE_RECONSTRUCTION",
        "mode": "fresh read-only adversarial review",
        "allowed": (
            "inspect only the sealed intake; challenge the 24-tile chronology, six prediction "
            "gates, layer classifications, stale-claim dispositions, and bounded landing; run "
            "registered G281 checks only in a writable ephemeral copy"
        ),
        "forbidden": (
            "edit evidence files, continue the research, access the repository or any path outside "
            "the sealed intake, inspect protected packages, or import an unsealed observational "
            "outcome, profile, history, transfer law, field equation, fit, scale, X_max, source, "
            "action, or matter model"
        ),
        "scientific_ceiling": (
            "source-bounded epistemic regrade only; no new metric, kernel, SNe prediction, history, "
            "scale, transfer law, X_max, or canonization"
        ),
    }
    (destination / "REVIEW_SCOPE.json").write_text(
        json.dumps(scope, indent=2, sort_keys=True) + "\n"
    )

    manifest_rows = []
    for path in sorted(item for item in destination.rglob("*") if item.is_file()):
        relative = path.relative_to(destination).as_posix()
        if any(fragment in relative for fragment in PROTECTED_FRAGMENTS):
            raise AssertionError(f"protected path entered intake: {relative}")
        manifest_rows.append((relative, path.stat().st_size, sha256(path)))
    manifest = destination / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "bytes", "sha256"))
        writer.writerows(manifest_rows)
    seal = destination / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{sha256(manifest)}  REVIEW_MANIFEST.tsv\n")

    print(
        json.dumps(
            {
                "path": str(destination),
                "payloads": len(manifest_rows),
                "total_files": len(manifest_rows) + 2,
                "scope_sha256": sha256(destination / "REVIEW_SCOPE.json"),
                "manifest_sha256": sha256(manifest),
                "seal_sha256": sha256(seal),
                "immutable_sources": len(source_rows),
                "replay_dependencies": len(REPLAY_DEPENDENCIES),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
