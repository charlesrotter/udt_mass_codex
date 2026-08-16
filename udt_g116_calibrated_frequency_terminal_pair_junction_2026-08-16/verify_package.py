#!/usr/bin/env python3
"""Rerunnable G116 package verifier."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "4497ace9"


def run_script(name: str, output: str) -> dict:
    path = HERE / output
    before = path.read_bytes()
    proc = subprocess.run(
        [sys.executable, str(HERE / name)], cwd=ROOT, text=True, capture_output=True, check=False
    )
    after = path.read_bytes()
    return {
        "returncode_zero": proc.returncode == 0,
        "output_exactly_reproduced": before == after,
        "reported_pass": json.loads(after)["status"] == "PASS",
    }


def verify_sources() -> tuple[bool, list[dict]]:
    rows = []
    all_ok = True
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            proc = subprocess.run(
                ["git", "show", f"{PREREG_COMMIT}:{row['path']}"],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )
            actual = hashlib.sha256(proc.stdout).hexdigest() if proc.returncode == 0 else "MISSING"
            ok = actual == row["sha256"]
            all_ok &= ok
            rows.append({"path": row["path"], "actual": actual, "ok": ok})
    return all_ok, rows


def main() -> None:
    required = [
        "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "AUDIT_REPORT.md", "EXACT_DERIVATION.md",
        "LAY_REPORT.md", "TYPE_AND_PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md", "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv", "STATUS.md", "NEXT_GATE.md", "COMMANDS.md", "REVIEW_REQUEST.md",
        "BLIND_REVIEW_ADJUDICATION.md", "CORRECTION_RECORD.md", "REPOSITORY_GATES.json",
        "derive_calibrated_junction.py", "verify_calibrated_junction_independent.py",
        "run_catch_proofs.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION_RESULT.json",
        "CATCH_PROOF_RESULT.json",
    ]
    manifest_ok, manifest_rows = verify_sources()
    scripts = {
        "production": run_script("derive_calibrated_junction.py", "DERIVATION_RESULT.json"),
        "independent": run_script(
            "verify_calibrated_junction_independent.py", "INDEPENDENT_VERIFICATION_RESULT.json"
        ),
        "catch_proofs": run_script("run_catch_proofs.py", "CATCH_PROOF_RESULT.json"),
    }
    checks = {
        "required_files": all((HERE / name).is_file() for name in required),
        "preregistered_commit_is_ancestor": subprocess.run(
            ["git", "merge-base", "--is-ancestor", PREREG_COMMIT, "HEAD"], cwd=ROOT, check=False
        ).returncode == 0,
        "source_manifest_at_prereg_commit": manifest_ok,
        "all_scripts_return_zero": all(x["returncode_zero"] for x in scripts.values()),
        "all_outputs_exactly_reproduced": all(x["output_exactly_reproduced"] for x in scripts.values()),
        "all_scripts_report_pass": all(x["reported_pass"] for x in scripts.values()),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "script_checks": scripts,
        "manifest_checks": manifest_rows,
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
