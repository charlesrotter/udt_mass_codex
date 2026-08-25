#!/usr/bin/env python3
"""Build a sealed self-contained G256 adversarial-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g256_r2_followup_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    package_files = sorted(path for path in PACKAGE.iterdir() if path.is_file())
    for source in package_files:
        copy_file(source, package_target / source.name)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    for row in sources:
        source = ROOT / row["path"]
        if sha256(source) != row["sha256"]:
            raise RuntimeError(f"source hash changed: {row['path']}")
        copy_file(source, intake / row["path"])

    commands = "\n".join([
        f"python3 {PACKAGE.name}/verify_package.py --no-write",
        f"python3 {PACKAGE.name}/verify_independent.py",
        f"python3 {PACKAGE.name}/run_catch_proofs.py",
    ]) + "\n"
    (intake / "REGISTERED_COMMANDS.txt").write_text(commands, encoding="utf-8")

    scope = {
        "audit": "G256 R2 dependency-free sealed-replay repair follow-up",
        "package": PACKAGE.name,
        "scientific_source_count": len(sources),
        "allowed": [
            "read sealed intake",
            "run registered no-write checks",
            "run bounded checks in a writable ephemeral copy",
        ],
        "forbidden": [
            "edit evidence files",
            "continue research",
            "access repository outside intake",
            "access protected packages",
            "inspect observational outcomes not present in intake",
        ],
        "requested_grades": [
            "G256_R2_SELF_CONTAINED_REPLAY_ACCEPTED__SCIENTIFIC_LANDING_RETAINED",
            "G256_R2_REPAIR_INCOMPLETE",
        ],
        "followup_limit": (
            "verify only R2 dependency-free replay certification and the unchanged bounded "
            "scientific landing"
        ),
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["path", "sha256", "bytes"])
        for path in payloads:
            writer.writerow([path.relative_to(intake).as_posix(), sha256(path), path.stat().st_size])

    for path in intake.rglob("*"):
        if path.is_file():
            os.chmod(path, 0o444)
    for path in sorted((item for item in intake.rglob("*") if item.is_dir()), reverse=True):
        os.chmod(path, 0o555)
    os.chmod(intake, 0o555)

    print(json.dumps({
        "intake": str(intake),
        "payload_count": len(payloads),
        "review_manifest_sha256": sha256(manifest_path),
        "review_scope_sha256": sha256(scope_path),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
