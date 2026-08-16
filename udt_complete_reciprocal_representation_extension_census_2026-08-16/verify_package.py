#!/usr/bin/env python3
"""Verify source hashes and exact executable ownership for the census package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def run_json(script: str):
    completed = subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main():
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    source_checks = []
    for row in rows:
        source = ROOT / row["path"]
        source_checks.append(source.is_file() and digest(source) == row["sha256"])

    production = run_json("derive_representation_census.py")
    independent = run_json("verify_representation_census_independent.py")
    saved_production = json.loads((HERE / "CENSUS_RESULT.json").read_text())
    saved_independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())

    required = [
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "REPRESENTATION_CLASS_ATLAS.tsv",
        "ACTIVE_PASSIVE_ATLAS.tsv",
        "FALSIFICATION_CONTRACT.tsv",
        "COMPLETENESS_MAP.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_FOLLOWUP_REVIEW_RAW.md",
    ]
    result = {
        "source_count": len(rows),
        "all_source_hashes_match": all(source_checks),
        "production_replay_matches_saved": production == saved_production,
        "independent_replay_matches_saved": independent == saved_independent,
        "independent_checks_pass": independent["all_checks_pass"],
        "required_files_present": all((HERE / name).is_file() for name in required),
    }
    result["all_checks_pass"] = all(result.values())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
