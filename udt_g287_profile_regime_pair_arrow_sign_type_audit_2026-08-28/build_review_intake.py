#!/usr/bin/env python3
"""Build a sealed, source-bounded G287 external-review intake."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent

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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repair-followup", action="store_true")
    args = parser.parse_args()
    prefix = "udt_g287_repair_followup_" if args.repair_followup else "udt_g287_review_"
    destination = Path(tempfile.mkdtemp(prefix=prefix, dir="/tmp"))
    package_destination = destination / PACKAGE.name
    package_destination.mkdir()

    excluded_generated = {
        "REVIEW_MANIFEST.tsv",
        "REVIEW_MANIFEST.sha256",
        "REVIEW_SCOPE.json",
    }
    for source in sorted(PACKAGE.iterdir()):
        if source.is_file() and source.name not in excluded_generated:
            shutil.copy2(source, package_destination / source.name)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(source_rows) != 23:
        raise AssertionError(f"expected 23 immutable sources, found {len(source_rows)}")
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

    if args.repair_followup:
        scope = {
            "audit": "G287_PROFILE_REGIME_PAIR_ARROW_SIGN_TYPE_AUDIT_REPAIR_FOLLOWUP",
            "mode": "read-only repair-only follow-up review",
            "allowed": (
                "inspect only the sealed intake; verify only preregistered repairs R1 through R3, "
                "the registered replays, and the unchanged bounded scientific landing; run checks "
                "only in a writable ephemeral copy"
            ),
            "forbidden": (
                "edit evidence files, continue the research, change the scientific question, access "
                "repository files outside the intake or protected packages, or promote profile/history, "
                "micro/macro, mass, scale, X_max, observation, or canon claims"
            ),
            "scientific_ceiling": "repair-only certification with no scientific-landing change",
        }
    else:
        scope = {
            "audit": "G287_PROFILE_REGIME_PAIR_ARROW_SIGN_TYPE_AUDIT",
            "mode": "fresh read-only adversarial review",
            "allowed": (
                "inspect only the sealed intake; rederive the pair-reversal versus profile-conjugation "
                "distinction; audit the complete 22-row dependency census; challenge the G267 and G272 "
                "interpretive guards; run registered checks only in a writable ephemeral copy"
            ),
            "forbidden": (
                "edit evidence files, continue the research, access repository files outside the sealed "
                "intake, inspect protected packages, or promote sign typing into a profile/history law, "
                "micro/macro assignment, mass mechanism, scale, X_max, or canon"
            ),
            "scientific_ceiling": (
                "bounded adjudication of whether current UDT mathematics distinguishes ambient profile "
                "sign from reversal-odd ordered pair depth without a native-kernel regression"
            ),
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
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
