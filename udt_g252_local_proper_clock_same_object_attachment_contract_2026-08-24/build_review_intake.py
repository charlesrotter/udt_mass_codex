#!/usr/bin/env python3
"""Build a sealed local G252 review intake from the exact source manifest."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import stat
import tempfile


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
FORBIDDEN_FRAGMENTS = (
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
    "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
    "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g252_review_", dir="/tmp"))
    payloads: list[str] = []

    for source in sorted(PKG.iterdir()):
        if source.is_file() and source.name != "__pycache__":
            relative = Path(PKG.name) / source.name
            destination = intake / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            payloads.append(relative.as_posix())

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        relative = Path(row["path"])
        if any(fragment in relative.as_posix() for fragment in FORBIDDEN_FRAGMENTS):
            raise SystemExit(f"forbidden source in manifest: {relative}")
        source = ROOT / relative
        if not source.is_file() or sha256(source) != row["sha256"]:
            raise SystemExit(f"source hash mismatch: {relative}")
        destination = intake / "sources" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        payloads.append((Path("sources") / relative).as_posix())

    payloads = sorted(set(payloads))
    scope = {
        "package": PKG.name,
        "purpose": "fresh_read_only_adversarial_review",
        "payload_count_excluding_scope": len(payloads),
        "payloads": [
            {"path": relative, "sha256": sha256(intake / relative)}
            for relative in payloads
        ],
        "restrictions": [
            "inspect_only_this_intake",
            "read_only_evidence",
            "registered_replays_or_bounded_read_only_checks",
            "no_evidence_edits",
            "no_research_continuation",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for path in sorted(intake.rglob("*"), reverse=True):
        if path.is_file():
            path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        elif path.is_dir():
            path.chmod(
                stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
            )
    intake.chmod(
        stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    )

    print(json.dumps({
        "intake": str(intake),
        "scope_sha256": sha256(scope_path),
        "file_count_including_scope": len(payloads) + 1,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
