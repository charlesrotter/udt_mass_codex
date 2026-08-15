#!/usr/bin/env python3
"""Build a sealed manifest-limited intake for fresh external review."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_native_current_review_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()
    package_files = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_CENSUS.tsv",
        "CANDIDATE_OWNER_ATLAS.tsv",
        "EXACT_DERIVATION.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "STATUS_LEDGER.tsv",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "derive_native_current_energy.py",
        "verify_native_current_energy_independent.py",
        "verify_package.py",
        "SOURCE_MANIFEST.tsv",
        "REVIEW_DISPATCH.md",
    ]
    copied = []
    for name in package_files:
        source = PACKAGE / name
        target = package_target / name
        shutil.copy2(source, target)
        copied.append(target)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    for row in sources:
        source = ROOT / row["path"]
        if sha256(source) != row["sha256"]:
            raise SystemExit(f"source hash drift: {row['path']}")
        target = intake / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    scope = {
        "purpose": "fresh read-only adversarial review of native radiative current and energy ownership",
        "file_count_including_scope": len(copied) + 1,
        "files": [
            {"path": str(path.relative_to(intake)), "sha256": sha256(path)}
            for path in sorted(copied)
        ],
        "forbidden": [
            "repository outside intake",
            "protected curvature atlas",
            "stopped native-on-shell draft",
            "internet",
            "file edits",
            "continuation of research",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake),
        "file_count": scope["file_count_including_scope"],
        "review_scope_sha256": sha256(scope_path),
    }, indent=2))


if __name__ == "__main__":
    main()

