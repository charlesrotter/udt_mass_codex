#!/usr/bin/env python3
"""Build a sealed, self-contained, read-only-review intake for G271."""

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
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g271_review_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    shutil.copytree(PACKAGE, package_target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    for row in sources:
        source = REPO / row["path"]
        assert source.is_file(), row["path"]
        assert digest(source) == row["sha256"], row["path"]
        target = intake / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() != (PACKAGE / "PREREGISTRATION.md").resolve():
            shutil.copy2(source, target)

    scope = {
        "title": "G271 primary-metric null-screen first-jet interlock fresh review",
        "mode": "READ_ONLY_ADVERSARIAL_REVIEW",
        "scientific_scope": (
            "Verify only the bounded arbitrary-profile primary-static first-jet theorem, exact "
            "screen evaluator, radial/quiet controls, evidence, and premise grades."
        ),
        "prohibited": [
            "edit evidence files",
            "continue the research",
            "access the repository outside this intake",
            "access protected packages",
            "inspect observational outcomes",
            "select a history population distance or X_max",
            "import a field equation source action matter model fit or transfer law",
        ],
        "registered_replay": (
            "python3 udt_g271_primary_metric_null_screen_first_jet_interlock_2026-08-26/"
            "verify_package.py --no-write"
        ),
        "package_grade": "INTERNALLY_VERIFIED_LEAD__EXTERNAL_REVIEW_OPEN",
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    with manifest_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        for path in payloads:
            writer.writerow((path.relative_to(intake), digest(path), path.stat().st_size))

    actual_files = sorted(path for path in intake.rglob("*") if path.is_file())
    result = {
        "intake": str(intake),
        "file_count_including_manifest": len(actual_files),
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest_path),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
