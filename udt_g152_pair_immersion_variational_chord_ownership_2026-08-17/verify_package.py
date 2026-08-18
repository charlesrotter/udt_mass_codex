#!/usr/bin/env python3
"""Package verifier for G152."""

from __future__ import annotations

import hashlib
import json
import py_compile
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    checks: dict[str, bool] = {}

    def add(name: str, value: object) -> None:
        checks[name] = bool(value)

    required = [
        "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv",
        "derive_variational_ownership.py", "verify_variational_ownership_independent.py",
        "DERIVATION_RESULT.json", "INDEPENDENT_RESULT.json", "EXACT_DERIVATION.md",
        "EVIDENCE_GATES.md", "LAY_REPORT.md", "OUTCOME_PREMISE_LEDGER.tsv",
    ]
    review_files = ["FRESH_ADVERSARIAL_REVIEW.md", "AUDIT_REPORT.md"]
    repair_files = ["REVIEW_REPAIR.md", "FRESH_ADVERSARIAL_FOLLOWUP.md"]
    for name in required:
        add(f"file_{name}", (HERE / name).is_file())
    review_present = [name for name in review_files if (HERE / name).is_file()]
    repair_present = [name for name in repair_files if (HERE / name).is_file()]
    add("review_bundle_all_or_none", len(review_present) in (0, len(review_files)))
    add("repair_bundle_all_or_none", len(repair_present) in (0, len(repair_files)))

    for name in ("derive_variational_ownership.py", "verify_variational_ownership_independent.py"):
        py_compile.compile(str(HERE / name), doraise=True)
        add(f"compile_{name}", True)

    runs = {}
    for key, name in (
        ("production", "derive_variational_ownership.py"),
        ("independent", "verify_variational_ownership_independent.py"),
    ):
        run = subprocess.run(
            [sys.executable, str(HERE / name)], cwd=ROOT, capture_output=True, text=True,
        )
        runs[key] = run
        add(f"{key}_rerun", run.returncode == 0)

    prod = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    ind = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    add("production_status", prod["status"] == "PASS")
    add("independent_status", ind["status"] == "PASS")
    for name, value in prod["gates"].items():
        add(f"production_{name}", value is True)
    for name, value in ind["gates"].items():
        add(f"independent_{name}", value is True)

    lines = (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()
    add("manifest_header", lines[0] == "path\tsha256\trole")
    for row in lines[1:]:
        path, expected, _role = row.split("\t")
        add(
            f"source_hash_{path}",
            hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected,
        )

    shown = subprocess.run(
        ["git", "show", "--quiet", "--format=%H", "09a45aa3"],
        cwd=ROOT, capture_output=True, text=True,
    )
    add("frozen_preregistration_commit", shown.returncode == 0)

    if review_present:
        add(
            "fresh_review_pass",
            (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text().lstrip().startswith("# PASS"),
        )
    if repair_present:
        add(
            "fresh_review_followup_pass",
            "FOLLOWUP_PASS" in (HERE / "FRESH_ADVERSARIAL_FOLLOWUP.md").read_text(),
        )

    result = {
        "schema": "udt.g152.package_verification.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "checks": checks,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
