#!/usr/bin/env python3
"""Build a sealed read-only intake for the constant representation census."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_representation_census_review_"))
    package_target = intake / HERE.name
    package_target.mkdir()
    excluded = {
        "build_review_intake.py",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "REVIEW_DISPATCH.md",
    }
    for source in sorted(HERE.iterdir()):
        if source.is_file() and source.name not in excluded:
            shutil.copy2(source, package_target / source.name)

    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        source = ROOT / row["path"]
        target = intake / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    scope = {
        "status": "SEALED_READ_ONLY_INTAKE",
        "package": HERE.name,
        "restrictions": [
            "inspect only this intake",
            "do not edit files",
            "do not continue the research",
            "no internet",
            "no repository access",
            "no protected-package access",
            "no BOSS or CMB outcome access",
        ],
        "payloads": [
            {
                "path": str(path.relative_to(intake)),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
            for path in payloads
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "intake": str(intake),
                "payload_count_including_scope": len(payloads) + 1,
                "scope_sha256": digest(scope_path),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

