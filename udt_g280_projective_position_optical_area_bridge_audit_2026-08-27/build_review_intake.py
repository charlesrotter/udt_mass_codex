#!/usr/bin/env python3
"""Build a sealed, source-bounded G280 external-review intake."""

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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repair-followup", action="store_true")
    args = parser.parse_args()
    prefix = "udt_g280_repair_followup_" if args.repair_followup else "udt_g280_review_"
    destination = Path(tempfile.mkdtemp(prefix=prefix, dir="/tmp"))
    package_destination = destination / PACKAGE.name
    package_destination.mkdir()

    for source in sorted(PACKAGE.iterdir()):
        if source.is_file() and source.name not in {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}:
            shutil.copy2(source, package_destination / source.name)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        source = ROOT / row["path"]
        target = destination / "sources" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    if args.repair_followup:
        scope = {
            "audit": "G280_PROJECTIVE_POSITION_OPTICAL_AREA_BRIDGE_REPAIR_FOLLOWUP",
            "mode": "read-only repair-only follow-up review",
            "allowed": (
                "verify only preregistered repairs R1-R3, unchanged bounded scientific landing, "
                "and registered checks in a writable ephemeral copy"
            ),
            "forbidden": (
                "edit evidence, continue research, alter the scientific question, inspect "
                "repository/protected packages, or use observational outcomes"
            ),
        }
    else:
        scope = {
            "audit": "G280_PROJECTIVE_POSITION_OPTICAL_AREA_BRIDGE",
            "mode": "fresh read-only adversarial review",
            "allowed": "inspect sealed intake and run bounded checks in a writable ephemeral copy",
            "forbidden": (
                "edit evidence, continue research, inspect repository/protected packages, or import "
                "observational outcomes, a history law, fitted curve, field equation, X_max, source, or matter model"
            ),
        }
    (destination / "REVIEW_SCOPE.json").write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    manifest_rows = []
    for path in sorted(item for item in destination.rglob("*") if item.is_file()):
        relative = path.relative_to(destination).as_posix()
        manifest_rows.append((relative, path.stat().st_size, sha256(path)))
    manifest = destination / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
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
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
