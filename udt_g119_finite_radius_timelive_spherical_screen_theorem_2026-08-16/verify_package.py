#!/usr/bin/env python3
"""Rerunnable G119 package verifier."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "bb1be0f9"


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            result.update(chunk)
    return result.hexdigest()


def replay(script: str, saved: str) -> tuple[bool, bool]:
    process = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT, capture_output=True, check=False
    )
    return process.returncode == 0, process.stdout == (HERE / saved).read_bytes()


def main() -> None:
    required = [
        "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md",
        "THEOREM_STRATA.tsv", "PREMISE_LEDGER.tsv", "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json", "LAY_REPORT.md", "EVIDENCE_GATES.md",
        "REVIEW_REQUEST.md", "derive_spherical_screen.py", "verify_spherical_screen_independent.py",
        "build_review_intake.py", "EXTERNAL_REVIEW_RAW.md", "EXTERNAL_REVIEW_ADJUDICATION.md",
        "CORRECTION_RECORD.md", "verify_offdiagonal_orbit_witness.py",
        "OFFDIAGONAL_VERIFICATION.json", "REPOSITORY_GATES.json", "STATUS.md",
    ]
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    source_hashes = {
        row["path"]: digest(ROOT / row["path"]) == row["sha256"] for row in sources
    }
    production_zero, production_exact = replay("derive_spherical_screen.py", "DERIVATION_RESULT.json")
    independent_zero, independent_exact = replay(
        "verify_spherical_screen_independent.py", "INDEPENDENT_VERIFICATION.json"
    )
    offdiagonal_zero, offdiagonal_exact = replay(
        "verify_offdiagonal_orbit_witness.py", "OFFDIAGONAL_VERIFICATION.json"
    )
    strata = list(csv.DictReader((HERE / "THEOREM_STRATA.tsv").open(encoding="utf-8"), delimiter="\t"))
    premises = list(csv.DictReader((HERE / "PREMISE_LEDGER.tsv").open(encoding="utf-8"), delimiter="\t"))
    checks = {
        "required_files": all((HERE / name).is_file() for name in required),
        "ten_source_hashes": len(sources) == 10 and all(source_hashes.values()),
        "preregistration_is_ancestor": subprocess.run(
            ["git", "merge-base", "--is-ancestor", PREREG_COMMIT, "HEAD"], cwd=ROOT, check=False
        ).returncode == 0,
        "production_returns_zero": production_zero,
        "production_exact_replay": production_exact,
        "independent_returns_zero": independent_zero,
        "independent_exact_replay": independent_exact,
        "offdiagonal_returns_zero": offdiagonal_zero,
        "offdiagonal_exact_replay": offdiagonal_exact,
        "six_strata": len(strata) == 6,
        "thirteen_premise_rows": len(premises) == 13,
        "transfer_retained_open": any(
            row["object"] == "transfer_T" and row["status"] == "OPEN" for row in premises
        ),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "source_hashes": source_hashes,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
