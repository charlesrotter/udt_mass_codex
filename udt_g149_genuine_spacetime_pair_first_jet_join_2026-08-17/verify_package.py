#!/usr/bin/env python3
"""Self-contained package verifier for G149."""

from __future__ import annotations

import hashlib
import json
import py_compile
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def check(name, condition, checks):
    checks[name] = bool(condition)


def main():
    checks = {}
    required = [
        "PREREGISTRATION.md",
        "WITNESS_REGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "derive_genuine_spacetime_first_jet.py",
        "verify_genuine_spacetime_first_jet_independent.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_RESULT.json",
        "EXACT_DERIVATION.md",
        "EVIDENCE_GATES.md",
        "LAY_REPORT.md",
        "OUTCOME_PREMISE_LEDGER.tsv",
        "FRESH_ADVERSARIAL_REVIEW.md",
        "REVIEW_REPAIR.md",
        "FRESH_ADVERSARIAL_FOLLOWUP.md",
        "AUDIT_REPORT.md",
    ]
    for name in required:
        check(f"file_{name}", (HERE / name).is_file(), checks)

    for script in ["derive_genuine_spacetime_first_jet.py", "verify_genuine_spacetime_first_jet_independent.py"]:
        py_compile.compile(str(HERE / script), doraise=True)
        check(f"compile_{script}", True, checks)

    prod_run = subprocess.run(
        [sys.executable, str(HERE / "derive_genuine_spacetime_first_jet.py")],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    ind_run = subprocess.run(
        [sys.executable, str(HERE / "verify_genuine_spacetime_first_jet_independent.py")],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    check("production_rerun", prod_run.returncode == 0, checks)
    check("independent_rerun", ind_run.returncode == 0, checks)

    prod = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    ind = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    check("production_status", prod.get("status") == "PASS", checks)
    check("independent_status", ind.get("status") == "PASS", checks)
    for name, value in prod["exact_gates"].items():
        check(f"production_gate_{name}", value is True, checks)
    for name, value in ind["gates"].items():
        check(f"independent_gate_{name}", value is True, checks)
    check("independent_identity_tolerance", ind["identity_residual_max_abs"] < 1e-12, checks)
    check("independent_agreement_tolerance", max(ind["production_comparison_abs"].values()) < 1e-12, checks)

    lines = (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()
    check("manifest_header", lines[0] == "path\tsha256\trole", checks)
    for row in lines[1:]:
        path, expected, role = row.split("\t")
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        check(f"source_hash_{path}", actual == expected, checks)

    prereg_commit = subprocess.run(
        ["git", "show", "--quiet", "--format=%H", "1a30aa0d"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    check("prereg_commit_exists", prereg_commit.returncode == 0, checks)

    result = {
        "schema": "udt.g149.package_verification.v1",
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
