#!/usr/bin/env python3
"""Build a sealed G239 review intake without BOSS outcomes or protected work."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g239_review_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()

    package_files = sorted(
        path for path in PACKAGE.iterdir()
        if path.is_file() and path.name not in {"build_review_intake.py"}
    )
    # Include the builder itself as evidence of the sealed scope.
    package_files.append(PACKAGE / "build_review_intake.py")
    manifest_rows = list(csv.DictReader((PACKAGE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    source_files = [REPO / row["path"] for row in manifest_rows]

    copied: list[Path] = []
    for source in package_files + source_files:
        relative = source.relative_to(REPO)
        target = intake / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    hashes = []
    for path in sorted(copied):
        hashes.append({
            "path": str(path.relative_to(intake)),
            "sha256": digest(path),
            "bytes": path.stat().st_size,
        })
    scope = {
        "audit": "G239_FRESH_EXTERNAL_REVIEW",
        "permissions": "read-only evidence review; ephemeral-copy checks allowed; no research continuation",
        "boss_outcomes": "excluded",
        "protected_packages": "excluded",
        "repository_outside_intake": "excluded",
        "file_count_excluding_scope": len(hashes),
        "files": hashes,
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
    os.chmod(scope_path, 0o444)
    for path in copied:
        os.chmod(path, 0o444)
    for directory, _, _ in os.walk(intake):
        os.chmod(directory, 0o555)
    print(json.dumps({
        "intake": str(intake),
        "scope_sha256": digest(scope_path),
        "file_count_including_scope": len(hashes) + 1,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

