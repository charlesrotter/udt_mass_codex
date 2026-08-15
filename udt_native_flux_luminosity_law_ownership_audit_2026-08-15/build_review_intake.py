#!/usr/bin/env python3
"""Build a sealed read-only review intake from the declared source manifest."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_flux_law_review_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    shutil.copytree(
        PACKAGE,
        package_target,
        ignore=shutil.ignore_patterns("__pycache__", "EXTERNAL_ADVERSARIAL_REVIEW.md"),
    )

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    for row in sources:
        source = REPO / row["path"]
        if digest(source) != row["sha256"]:
            raise SystemExit(f"source hash drift: {row['path']}")
        target = intake / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    files = sorted(path for path in intake.rglob("*") if path.is_file())
    scope = {
        "purpose": "fresh read-only adversarial review of native flux/luminosity ownership",
        "package": PACKAGE.name,
        "restrictions": [
            "read only",
            "no repository access outside intake",
            "no edits",
            "no continuation of research",
            "no internet",
        ],
        "files": [
            {
                "path": str(path.relative_to(intake)),
                "sha256": digest(path),
                "bytes": path.stat().st_size,
            }
            for path in files
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")
    print(f"intake={intake}")
    print(f"payload_files={len(files)}")
    print(f"scope_sha256={digest(scope_path)}")


if __name__ == "__main__":
    main()
