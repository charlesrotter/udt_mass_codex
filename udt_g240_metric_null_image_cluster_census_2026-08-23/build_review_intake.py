#!/usr/bin/env python3
"""Build a sealed G240 review intake without observational outcomes."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_no_write(intake_root: Path) -> subprocess.CompletedProcess[str]:
    package = intake_root / PACKAGE.name
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(package / "verify_package.py"), "--no-write"],
        cwd=package,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g240_review_"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()

    package_files = sorted(
        path for path in PACKAGE.iterdir()
        if path.is_file() and path.name not in {"REVIEW_MANIFEST.tsv"}
    )
    for source in package_files:
        shutil.copy2(source, package_target / source.name)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in source_rows:
        source = REPO / row["path"]
        target = intake / "sources" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    manifest_rows = []
    for path in sorted(p for p in intake.rglob("*") if p.is_file()):
        relative = path.relative_to(intake).as_posix()
        manifest_rows.append((relative, digest(path)))

    manifest = intake / "REVIEW_MANIFEST.tsv"
    manifest.write_text(
        "path\tsha256\n" + "".join(f"{path}\t{sha}\n" for path, sha in manifest_rows),
        encoding="utf-8",
    )
    scope = {
        "audit": "G240_METRIC_NULL_IMAGE_CLUSTER_CENSUS",
        "review_mode": "READ_ONLY_REPAIR_ONLY_FOLLOWUP",
        "payload_files": len(manifest_rows),
        "manifest_sha256": digest(manifest),
        "internet": False,
        "observational_outcomes": False,
        "protected_packages": False,
        "reviewer_may_edit": False,
        "reviewer_may_continue_research": False,
        "sealed_no_write_replay": "REQUIRED",
        "repair_scope": "R1_SEALED_SOURCE_LAYOUT_ONLY__SCIENTIFIC_LANDING_FROZEN",
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    positive = replay_no_write(intake)
    if positive.returncode != 0:
        raise AssertionError(
            "sealed no-write replay failed as delivered:\n"
            + positive.stdout
            + positive.stderr
        )
    positive_result = json.loads(positive.stdout)
    if positive_result.get("source_layout") != "SEALED_SOURCES_ROOT":
        raise AssertionError("sealed replay did not use the sealed sources root")

    with tempfile.TemporaryDirectory(prefix="udt_g240_missing_sources_") as negative_name:
        negative_root = Path(negative_name)
        shutil.copytree(package_target, negative_root / PACKAGE.name)
        shutil.copy2(scope_path, negative_root / scope_path.name)
        negative = replay_no_write(negative_root)
        if negative.returncode == 0:
            raise AssertionError("sealed replay accepted an intake without its sources root")
        if "sealed source root missing: sources" not in negative.stderr:
            raise AssertionError("sealed missing-sources replay failed for an unexpected reason")

    print(
        json.dumps(
            {
                "intake": str(intake),
                "scope": scope,
                "sealed_no_write_replay": "PASS",
                "missing_sources_negative_gate": "PASS",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
