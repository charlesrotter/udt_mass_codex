#!/usr/bin/env python3
"""Rerunnable G117 package verifier."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "a7890d9f"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_sources() -> tuple[bool, list[dict]]:
    records = []
    all_ok = True
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        path = Path(row["path"])
        if path.is_absolute():
            actual = digest(path) if path.is_file() else "MISSING"
        else:
            proc = subprocess.run(["git", "show", f"{PREREG_COMMIT}:{row['path']}"], cwd=ROOT, capture_output=True, check=False)
            actual = hashlib.sha256(proc.stdout).hexdigest() if proc.returncode == 0 else "MISSING"
        ok = actual == row["sha256"]
        all_ok &= ok
        records.append({"path": row["path"], "actual": actual, "ok": ok})
    return len(rows) == 18 and all_ok, records


def run_script(script: str, output: str) -> dict[str, bool]:
    target = HERE / output
    before = target.read_bytes()
    proc = subprocess.run([sys.executable, str(HERE / script)], cwd=ROOT, capture_output=True, check=False)
    after = target.read_bytes()
    return {
        "returncode_zero": proc.returncode == 0,
        "output_exactly_reproduced": before == after,
        "reported_pass": json.loads(after).get("all_checks_pass", json.loads(after).get("status") == "PASS") is True,
    }


def main() -> None:
    required = [
        "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md",
        "LAY_REPORT.md", "TYPE_AND_PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md", "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv", "STATUS.md", "NEXT_GATE.md", "REVIEW_REQUEST.md", "COMMANDS.md",
        "PRODUCTION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "run_operational_sne_regrade.py", "verify_operational_sne_independent.py", "run_catch_proofs.py",
        "BLIND_REVIEW_ADJUDICATION.md", "CORRECTION_RECORD.md", "REPOSITORY_GATES.json",
    ]
    manifest_ok, manifest_records = verify_sources()
    scripts = {
        "production": run_script("run_operational_sne_regrade.py", "PRODUCTION_RESULT.json"),
        "independent": run_script("verify_operational_sne_independent.py", "INDEPENDENT_VERIFICATION.json"),
        "catch_proofs": run_script("run_catch_proofs.py", "CATCH_PROOF_RESULT.json"),
    }
    checks = {
        "required_files": all((HERE / name).is_file() for name in required),
        "preregistered_commit_is_ancestor": subprocess.run(["git", "merge-base", "--is-ancestor", PREREG_COMMIT, "HEAD"], cwd=ROOT, check=False).returncode == 0,
        "source_manifest_at_preregistration": manifest_ok,
        "all_scripts_return_zero": all(value["returncode_zero"] for value in scripts.values()),
        "all_outputs_exactly_reproduced": all(value["output_exactly_reproduced"] for value in scripts.values()),
        "all_scripts_report_pass": all(value["reported_pass"] for value in scripts.values()),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "script_checks": scripts,
        "manifest_checks": manifest_records,
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
