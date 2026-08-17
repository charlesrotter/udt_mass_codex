#!/usr/bin/env python3
"""Isolated replay and integrity checks for the G132 package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(script: str, output: Path) -> str:
    proc = subprocess.run(
        [sys.executable, str(PKG / script), "--output", str(output)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def main() -> None:
    checks: dict[str, bool] = {}

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks["manifest_has_ten_exact_sources"] = len(rows) == 10
    checks["manifest_sources_exist"] = all((ROOT / row["path"]).is_file() for row in rows)
    checks["manifest_hashes_match"] = all(sha256(ROOT / row["path"]) == row["sha256"] for row in rows)
    checks["protected_paths_absent_from_manifest"] = all(
        "udt_native_onshell_timelive_reset_owner_audit" not in row["path"]
        and "udt_pair_regime_flow_reciprocal_orchestra_amplification" not in row["path"]
        and "udt_sne_xmax_G88_am_radial_compatibility_atlas" not in row["path"]
        and "curvature_holonomy_atlas" not in row["path"]
        for row in rows
    )

    required = [
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "EXACT_DERIVATION.md",
        "CANDIDATE_CLASSIFICATION.tsv",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS.md",
        "FRESH_ADVERSARIAL_REVIEW.md",
        "REPAIR_RECORD.md",
        "FOLLOWUP_REVIEW.md",
        "derive_common_scale_owner.py",
        "verify_common_scale_owner_independent.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
    ]
    checks["required_package_files_present"] = all((PKG / name).is_file() for name in required)

    with tempfile.TemporaryDirectory(prefix="g132_verify_") as tmp:
        tmpdir = Path(tmp)
        production_out = tmpdir / "DERIVATION_RESULT.json"
        independent_out = tmpdir / "INDEPENDENT_VERIFICATION.json"
        production_stdout = run("derive_common_scale_owner.py", production_out)
        independent_stdout = run("verify_common_scale_owner_independent.py", independent_out)
        checks["isolated_production_reports_pass"] = production_stdout.startswith("PASS: 22/22")
        checks["isolated_independent_reports_pass"] = independent_stdout.startswith("PASS: 18/18")
        checks["isolated_production_byte_identical"] = production_out.read_bytes() == (PKG / "DERIVATION_RESULT.json").read_bytes()
        checks["isolated_independent_byte_identical"] = independent_out.read_bytes() == (PKG / "INDEPENDENT_VERIFICATION.json").read_bytes()

    production = json.loads((PKG / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((PKG / "INDEPENDENT_VERIFICATION.json").read_text())
    checks["production_json_pass"] = production.get("status") == "PASS" and production.get("passed") == 22
    checks["independent_json_pass"] = independent.get("status") == "PASS" and independent.get("passed") == 18
    checks["landing_keeps_general_history_open"] = "GENERAL_HISTORY_AND_VALUE_LAW_OPEN" in production.get("landing", "")

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "passed": sum(checks.values()),
        "total": len(checks),
        "checks": checks,
    }
    (PKG / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {result['passed']}/{result['total']} G132 package checks" if result["status"] == "PASS" else json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
