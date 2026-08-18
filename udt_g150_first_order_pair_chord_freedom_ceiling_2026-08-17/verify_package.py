#!/usr/bin/env python3
"""Package verifier for G150."""

from __future__ import annotations

import hashlib
import json
import py_compile
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    checks = {}

    def add(name, value):
        checks[name] = bool(value)

    required = [
        "PREREGISTRATION.md", "WITNESS_REGISTRATION.md", "SOURCE_MANIFEST.tsv",
        "derive_first_order_freedom_ceiling.py", "verify_first_order_freedom_independent.py",
        "DERIVATION_RESULT.json", "INDEPENDENT_RESULT.json", "EXACT_DERIVATION.md",
        "EVIDENCE_GATES.md", "LAY_REPORT.md", "OUTCOME_PREMISE_LEDGER.tsv",
        "FRESH_ADVERSARIAL_REVIEW.md", "REVIEW_REPAIR.md",
        "FRESH_ADVERSARIAL_FOLLOWUP.md", "AUDIT_REPORT.md",
    ]
    for name in required:
        add(f"file_{name}", (HERE / name).is_file())
    for name in ("derive_first_order_freedom_ceiling.py", "verify_first_order_freedom_independent.py"):
        py_compile.compile(str(HERE / name), doraise=True)
        add(f"compile_{name}", True)

    prod_run = subprocess.run([sys.executable, str(HERE / "derive_first_order_freedom_ceiling.py")], cwd=ROOT, capture_output=True, text=True)
    ind_run = subprocess.run([sys.executable, str(HERE / "verify_first_order_freedom_independent.py")], cwd=ROOT, capture_output=True, text=True)
    add("production_rerun", prod_run.returncode == 0)
    add("independent_rerun", ind_run.returncode == 0)
    prod = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    ind = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    add("production_status", prod["status"] == "PASS")
    add("independent_status", ind["status"] == "PASS")
    for name, value in prod["gates"].items():
        add(f"production_{name}", value is True)
    for name, value in ind["gates"].items():
        add(f"independent_{name}", value is True)
    add("independent_error", max(row["max_abs_error"] for row in ind["cases"]) < 1e-12)

    lines = (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()
    add("manifest_header", lines[0] == "path\tsha256\trole")
    for row in lines[1:]:
        path, expected, role = row.split("\t")
        add(f"source_hash_{path}", hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected)
    prereg = subprocess.run(["git", "show", "--quiet", "--format=%H", "24968eb7"], cwd=ROOT, capture_output=True, text=True)
    add("prereg_commit_exists", prereg.returncode == 0)

    result = {
        "schema": "udt.g150.package_verification.v1",
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
