#!/usr/bin/env python3
"""Build a sealed, source-bounded G289 external-review intake."""

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
PACKAGE_BANK_COMMIT = "0e0caa204dab09f6e9379605b89c60644d03ba47"

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


def git_blob(relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{PACKAGE_BANK_COMMIT}:{relative}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g289_review_", dir="/tmp"))
    package_destination = destination / PACKAGE.name
    package_destination.mkdir()

    excluded_generated = {
        "REVIEW_MANIFEST.tsv",
        "REVIEW_MANIFEST.sha256",
        "REVIEW_SCOPE.json",
    }
    for source in sorted(PACKAGE.iterdir()):
        if source.is_file() and source.name not in excluded_generated:
            if source.name != "build_review_intake.py":
                committed = git_blob(f"{PACKAGE.name}/{source.name}")
                if committed != source.read_bytes():
                    raise AssertionError(f"G289 package changed after banking: {source.name}")
            shutil.copy2(source, package_destination / source.name)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(source_rows) != 13:
        raise AssertionError(f"expected 13 immutable sources, found {len(source_rows)}")
    for row in source_rows:
        relative = row["source"]
        if any(fragment in relative for fragment in PROTECTED_FRAGMENTS):
            raise AssertionError(f"protected path rejected: {relative}")
        payload = git_blob(relative)
        if hashlib.sha256(payload).hexdigest() != row["sha256"]:
            raise AssertionError(f"banked source provenance changed: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)

    scope = {
        "audit": "G289_NATIVE_KERNEL_HOPFION_COMPATIBILITY_HISTORY_CONSTRAINT",
        "mode": "fresh read-only adversarial review",
        "allowed": (
            "inspect only the sealed intake; independently rebuild the local null embedding, exact "
            "boost and large-frame-gauge witnesses, and conformal-history counterfamily from the "
            "frozen G289 metric and sources; run registered replays or bounded checks only in a "
            "writable ephemeral copy"
        ),
        "forbidden": (
            "edit evidence files, continue the research, access repository files outside the intake "
            "or protected packages, inspect G290 or later work, trust an older audit as proof, use the "
            "internet, or import an action, source, matter model, mass, observation, scale, Planck "
            "cutoff, history, X_max, fixed carrier, boundary, or canonization"
        ),
        "scientific_ceiling": (
            "bounded adjudication of G289 local null embedding, frame-gauge descent, conditional "
            "Hopfion compatibility, and texture-existence history nonselection"
        ),
        "frozen_source_commit": PACKAGE_BANK_COMMIT,
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
        "immutable_sources": len(source_rows),
        "frozen_source_commit": PACKAGE_BANK_COMMIT,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
