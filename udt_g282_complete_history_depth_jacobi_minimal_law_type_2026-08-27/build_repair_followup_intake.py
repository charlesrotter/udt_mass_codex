#!/usr/bin/env python3
"""Build a sealed G282 R1 repair-only external follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent

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


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g282_repair_followup_", dir="/tmp"))
    package_destination = destination / PACKAGE.name
    package_destination.mkdir()

    excluded_generated = {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256", "REVIEW_SCOPE.json"}
    for source in sorted(PACKAGE.iterdir()):
        if source.is_file() and source.name not in excluded_generated:
            shutil.copy2(source, package_destination / source.name)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(source_rows) != 18:
        raise AssertionError(f"expected 18 immutable sources, found {len(source_rows)}")
    for row in source_rows:
        relative = row["path"]
        if any(fragment in relative for fragment in PROTECTED_FRAGMENTS):
            raise AssertionError(f"protected path rejected: {relative}")
        source = ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(source)
        if sha256(source) != row["sha256"] or str(source.stat().st_size) != row["bytes"]:
            raise AssertionError(f"source provenance changed: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    scope = {
        "audit": "G282_R1_CLAIM_SCHEMA_CERTIFICATION_REPAIR_FOLLOWUP",
        "mode": "read-only repair-only follow-up review",
        "allowed": (
            "inspect only the sealed intake; verify only preregistered repair R1, the five "
            "registered no-write replays, and the unchanged bounded scientific landing; run "
            "bounded checks only in a writable ephemeral copy"
        ),
        "forbidden": (
            "edit evidence files, continue the research, access the repository or any path outside "
            "the sealed intake, inspect protected packages or unsealed outcomes, reopen the "
            "scientific question, or import or adopt a field equation, history, profile, fit, "
            "scale, X_max, source, action, or matter model"
        ),
        "repair_ceiling": (
            "accept or reject only the R1 retyping of the schematic claim-schema guard while "
            "checking that the accepted G282 mathematical and scientific landing is unchanged"
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
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
