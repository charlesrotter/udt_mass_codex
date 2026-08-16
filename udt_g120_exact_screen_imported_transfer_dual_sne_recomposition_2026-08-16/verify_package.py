#!/usr/bin/env python3
"""Rerunnable G120 package verifier."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "8f9e9b53"


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            result.update(chunk)
    return result.hexdigest()


def main() -> None:
    required = [
        "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "CORRECTION_RECORD.md",
        "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "PREMISE_LEDGER.tsv", "LAY_REPORT.md",
        "EVIDENCE_GATES.md", "STATUS.md", "NEXT_GATE.md", "PRODUCTION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json", "run_exact_screen_sne_recomposition.py",
        "verify_exact_screen_sne_independent.py", "BLIND_REVIEW_RAW.md",
        "BLIND_REVIEW_ADJUDICATION.md", "REPOSITORY_GATES.json",
    ]
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    source_hashes = {}
    for row in sources:
        path = Path(row["path"])
        if not path.is_absolute():
            path = ROOT / path
        source_hashes[row["path"]] = path.is_file() and digest(path) == row["sha256"]
    production_expected = (HERE / "PRODUCTION_RESULT.json").read_bytes()
    independent_expected = (HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()
    with tempfile.TemporaryDirectory(prefix=".g120_verify_", dir=ROOT) as temp_name:
        temp = Path(temp_name)
        for name in (
            "SOURCE_MANIFEST.tsv", "run_exact_screen_sne_recomposition.py",
            "verify_exact_screen_sne_independent.py", "PRODUCTION_RESULT.json",
            "INDEPENDENT_VERIFICATION.json",
        ):
            shutil.copy2(HERE / name, temp / name)
        production_process = subprocess.run(
            [sys.executable, str(temp / "run_exact_screen_sne_recomposition.py")],
            cwd=ROOT, capture_output=True, check=False,
        )
        production_zero = production_process.returncode == 0
        production_exact = (
            production_process.stdout == production_expected
            and (temp / "PRODUCTION_RESULT.json").read_bytes() == production_expected
        )
        independent_process = subprocess.run(
            [sys.executable, str(temp / "verify_exact_screen_sne_independent.py")],
            cwd=ROOT, capture_output=True, check=False,
        )
        independent_zero = independent_process.returncode == 0
        independent_exact = (
            independent_process.stdout == independent_expected
            and (temp / "INDEPENDENT_VERIFICATION.json").read_bytes() == independent_expected
        )
    production = json.loads((HERE / "PRODUCTION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    with (HERE / "PREMISE_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        premises = list(csv.DictReader(handle, delimiter="\t"))
    checks = {
        "required_files": all((HERE / name).is_file() for name in required),
        "all_15_source_hashes": len(sources) == 15 and all(source_hashes.values()),
        "preregistration_is_ancestor": subprocess.run(
            ["git", "merge-base", "--is-ancestor", PREREG_COMMIT, "HEAD"],
            cwd=ROOT, check=False,
        ).returncode == 0,
        "production_returns_zero": production_zero,
        "production_exact_replay": production_exact,
        "production_reports_pass": production.get("all_checks_pass") is True,
        "independent_returns_zero": independent_zero,
        "independent_exact_replay": independent_exact,
        "independent_reports_pass": independent.get("all_checks_pass") is True,
        "fifteen_premise_rows": len(premises) == 15,
        "transfer_is_imported": any(
            row["object"] == "transfer_product" and row["status"] == "IMPORTED_CONDITIONAL"
            for row in premises
        ),
        "complete_history_open": any(
            row["object"] == "complete_metric_history" and row["status"] == "OPEN"
            for row in premises
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
