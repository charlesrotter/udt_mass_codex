#!/usr/bin/env python3
"""Build a self-contained sealed G255 adversarial-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g255_review_", dir="/tmp"))
    package_target = intake / PKG.name

    package_files = sorted(
        path for path in PKG.iterdir() if path.is_file() and path.name != "REVIEW_MANIFEST.tsv"
    )
    for source in package_files:
        copy_file(source, package_target / source.name)

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    for row in sources:
        source = ROOT / row["path"]
        if sha(source) != row["sha256"]:
            raise RuntimeError(f"source hash changed: {row['path']}")
        copy_file(source, intake / row["path"])

    commands = "\n".join(
        [
            f"python3 {PKG.name}/verify_package.py --no-write",
            f"python3 {PKG.name}/verify_independent.py --no-write",
        ]
    ) + "\n"
    (intake / "REGISTERED_COMMANDS.txt").write_text(commands, encoding="utf-8")

    scope = {
        "audit": "G255 G165-G254 lost-closure recovery",
        "package": PKG.name,
        "slot_count": 90,
        "scientific_source_count": 321,
        "allowed": [
            "read sealed intake",
            "run registered no-write checks",
            "run bounded read-only checks",
            "use writable ephemeral copy only if runtime requires it",
        ],
        "forbidden": [
            "edit evidence files",
            "continue research",
            "inspect repository outside intake",
            "inspect protected packages",
            "inspect observational outcomes not present in intake",
        ],
        "requested_grades": [
            "G255_ACCEPTED_WITH_CAVEATS",
            "G255_SCOPE_RECONCILIATION_REQUIRES_REPAIR",
            "G255_MISSED_CLOSURE_CANDIDATE",
            "G255_REJECTED",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["path", "sha256", "bytes"])
        for path in payloads:
            writer.writerow([path.relative_to(intake).as_posix(), sha(path), path.stat().st_size])

    # Seal files and directories after construction.
    for path in intake.rglob("*"):
        if path.is_file():
            os.chmod(path, 0o444)
    for path in sorted((p for p in intake.rglob("*") if p.is_dir()), reverse=True):
        os.chmod(path, 0o555)
    os.chmod(intake, 0o555)

    print(json.dumps({
        "intake": str(intake),
        "payload_count": len(payloads),
        "review_manifest_sha256": sha(manifest_path),
        "review_scope_sha256": sha(scope_path),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
