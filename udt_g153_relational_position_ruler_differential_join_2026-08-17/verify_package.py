#!/usr/bin/env python3
"""Package verifier for G153."""

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
        "PREREGISTRATION.md", "PREREGISTRATION_EXECUTION_NOTE.md", "SOURCE_MANIFEST.tsv", "derive_differential_join.py",
        "verify_differential_join_independent.py", "DERIVATION_RESULT.json",
        "INDEPENDENT_RESULT.json", "EXACT_DERIVATION.md", "EVIDENCE_GATES.md",
        "LAY_REPORT.md", "OUTCOME_PREMISE_LEDGER.tsv",
    ]
    review_files = ["FRESH_ADVERSARIAL_REVIEW.md", "AUDIT_REPORT.md"]
    repair_files = ["REVIEW_REPAIR.md", "FRESH_ADVERSARIAL_FOLLOWUP.md"]
    for name in required:
        add(f"file_{name}", (HERE / name).is_file())
    review_present = [name for name in review_files if (HERE / name).is_file()]
    repair_present = [name for name in repair_files if (HERE / name).is_file()]
    add("review_bundle_all_or_none", len(review_present) in (0, len(review_files)))
    add("repair_bundle_all_or_none", len(repair_present) in (0, len(repair_files)))

    for name in ("derive_differential_join.py", "verify_differential_join_independent.py"):
        py_compile.compile(str(HERE / name), doraise=True)
        add(f"compile_{name}", True)
        run = subprocess.run([sys.executable, str(HERE / name)], cwd=ROOT, capture_output=True, text=True)
        add(f"rerun_{name}", run.returncode == 0)

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
        add(f"source_hash_{path}", hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected)

    prereg = subprocess.run(
        ["git", "show", "--name-only", "--format=", "18060cba"], cwd=ROOT,
        capture_output=True, text=True,
    )
    frozen_names = {line for line in prereg.stdout.splitlines() if line}
    expected_names = {
        str(HERE.relative_to(ROOT) / "PREREGISTRATION.md"),
        str(HERE.relative_to(ROOT) / "SOURCE_MANIFEST.tsv"),
    }
    add("preregistration_commit_exact_files", prereg.returncode == 0 and frozen_names == expected_names)

    if review_present:
        review_text = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text()
        initial_pass = review_text.lstrip().startswith("# PASS")
        repaired_review = "REPAIR_REQUIRED" in review_text and len(repair_present) == len(repair_files)
        add("fresh_review_verdict_recorded", initial_pass or repaired_review)
    if repair_present:
        add("fresh_followup_pass", "FOLLOWUP_PASS" in (HERE / "FRESH_ADVERSARIAL_FOLLOWUP.md").read_text())

    result = {
        "schema": "udt.g153.package_verification.v1",
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
