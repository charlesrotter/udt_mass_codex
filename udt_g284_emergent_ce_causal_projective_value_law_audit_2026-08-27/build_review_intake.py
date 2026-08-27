#!/usr/bin/env python3
"""Build a sealed, source-bounded G284 external-review intake."""

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
    destination = Path(tempfile.mkdtemp(prefix="udt_g284_review_", dir="/tmp"))
    package_destination = destination / PACKAGE.name
    package_destination.mkdir()

    excluded_generated = {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256", "REVIEW_SCOPE.json"}
    for source in sorted(PACKAGE.iterdir()):
        if source.is_file() and source.name not in excluded_generated:
            shutil.copy2(source, package_destination / source.name)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(source_rows) != 15:
        raise AssertionError(f"expected 15 immutable sources, found {len(source_rows)}")
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
        "audit": "G284_EMERGENT_CE_CAUSAL_PROJECTIVE_VALUE_LAW_DISCRIMINATOR",
        "mode": "fresh read-only adversarial review",
        "allowed": (
            "inspect only the sealed intake; challenge the exact causal/projective reconstruction, "
            "arbitrary-T nonselection witness, scale boundary, and bounded landing; run registered "
            "no-write replays or bounded checks only in a writable ephemeral copy"
        ),
        "forbidden": (
            "edit evidence files, continue the research, access the repository or any path outside "
            "the sealed intake, inspect protected packages or unsealed observational outcomes, or "
            "import or adopt a field equation, history, operational distance, absolute scale, "
            "X_max, source, action, matter model, fit, transfer law, or canonization"
        ),
        "scientific_ceiling": (
            "source-bounded classification of whether emergent c_E, local causal structure, W5 "
            "projective state, and path-labelled network carry select the G283 tidal-history values; "
            "no replacement law or physical-history selection"
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
