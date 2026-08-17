#!/usr/bin/env python3
"""Isolated package and source replay for G131."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    required = (
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS.md",
        "REVIEW_REQUEST.md",
        "FRESH_ADVERSARIAL_REVIEW.md",
        "FOLLOWUP_REVIEW.md",
        "derive_terminal_scalar_kernel.py",
        "verify_terminal_scalar_kernel_independent.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "KERNEL_CLASSIFICATION.tsv",
    )
    checks = {f"present::{name}": (HERE / name).is_file() for name in required}

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_count_six"] = len(sources) == 6 and len({row["path"] for row in sources}) == 6
    for row in sources:
        source = ROOT / row["path"]
        checks[f"source::{row['path']}"] = source.is_file() and digest(source) == row["sha256"]

    generated = (
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "KERNEL_CLASSIFICATION.tsv",
    )
    saved = {name: (HERE / name).read_bytes() for name in generated}
    with tempfile.TemporaryDirectory(prefix="g131_verify_") as temp_name:
        temp_root = Path(temp_name)
        temp_package = temp_root / HERE.name
        shutil.copytree(HERE, temp_package, ignore=shutil.ignore_patterns("__pycache__"))
        for row in sources:
            destination = temp_root / row["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / row["path"], destination)
        production = subprocess.run(
            [sys.executable, str(temp_package / "derive_terminal_scalar_kernel.py")],
            cwd=temp_package, text=True, capture_output=True, check=False,
        )
        independent = subprocess.run(
            [sys.executable, str(temp_package / "verify_terminal_scalar_kernel_independent.py")],
            cwd=temp_package, text=True, capture_output=True, check=False,
        )
        checks["fresh_production_exit"] = production.returncode == 0
        checks["fresh_independent_exit"] = independent.returncode == 0
        for name in generated:
            checks[f"fresh::{name}"] = (temp_package / name).read_bytes() == saved[name]

    production_result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent_result = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    expected = "ALL_PLANE_TERMINAL_SCALAR_CONFORMAL_FAITHFUL_ONLY__COMMON_SCALE_OPEN"
    checks["production_18_of_18"] = (
        production_result.get("production_check_count") == 18
        and all(production_result.get("checks", {}).values())
    )
    checks["independent_8_of_8"] = (
        independent_result.get("independent_check_count") == 8
        and all(independent_result.get("checks", {}).values())
    )
    checks["landings_agree"] = production_result.get("landing") == independent_result.get("landing")
    checks["expected_landing"] = production_result.get("landing") == expected
    checks["production_pass"] = production_result.get("status") == "PASS"
    checks["independent_pass"] = independent_result.get("status") == "PASS"
    if (HERE / "FRESH_ADVERSARIAL_REVIEW.md").is_file():
        review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text()
        checks["adversarial_verdict"] = "PASS" in review
    if (HERE / "FOLLOWUP_REVIEW.md").is_file():
        followup = (HERE / "FOLLOWUP_REVIEW.md").read_text()
        checks["followup_pass"] = "FOLLOWUP_PASS" in followup

    status = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "status": status,
        "verification_kind": "source_manifest_plus_fresh_isolated_symbolic_and_fraction_replay",
        "source_count": len(sources),
        "checks": checks,
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
