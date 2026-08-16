#!/usr/bin/env python3
"""Verify the bounded G113 package without writing artifacts."""

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PREREG_COMMIT = "6c16eb3c"


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def frozen_payload(path: str) -> bytes:
    if path in {"CURRENT_SCIENTIFIC_PREMISES.md", "CURRENT_RESEARCH_PROGRAM.md"}:
        return subprocess.check_output(
            ["git", "show", f"{PREREG_COMMIT}:{path}"], cwd=ROOT
        )
    return (ROOT / path).read_bytes()


def run_json(script: str) -> dict:
    output = subprocess.check_output(
        [sys.executable, str(PACKAGE / script)], cwd=ROOT, text=True
    )
    return json.loads(output)


def main() -> None:
    required = {
        "PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "WHITEBOARD_RECORD.md",
        "LAY_REPORT.md",
        "NEXT_GATE.md",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
        "STATUS.md",
        "CORRECTION_RECORD.md",
        "BLIND_REVIEW_ADJUDICATION.md",
        "STATIC_SPHERICAL_VERIFICATION_RESULT.json",
        "INDEPENDENT_VERIFICATION_RESULT.json",
        "verify_static_spherical_chord.py",
        "verify_static_spherical_independent.py",
    }
    missing = sorted(name for name in required if not (PACKAGE / name).is_file())

    manifest_checks = []
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            actual = sha256(frozen_payload(row["path"]))
            manifest_checks.append(actual == row["sha256"])

    symbolic = run_json("verify_static_spherical_chord.py")
    independent = run_json("verify_static_spherical_independent.py")
    saved_symbolic = json.loads(
        (PACKAGE / "STATIC_SPHERICAL_VERIFICATION_RESULT.json").read_text()
    )
    saved_independent = json.loads(
        (PACKAGE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text()
    )

    report = (PACKAGE / "AUDIT_REPORT.md").read_text()
    guards = {
        "no_missing_files": not missing,
        "all_source_hashes": all(manifest_checks) and len(manifest_checks) == 17,
        "symbolic_pass": symbolic["status"] == "PASS",
        "independent_pass": independent["status"] == "PASS",
        "saved_symbolic_exact": symbolic == saved_symbolic,
        "saved_independent_exact": independent == saved_independent,
        "history_open": "PHYSICAL_HISTORY" in report,
        "static_scope_explicit": "static, central, spherical" in report,
        "p1_center_scope_explicit": "P1_STATIC_PROFILE_INVERSION_FAILS_SMOOTH_CENTER" in report,
        "next_gate_explicit": "COMMON_SOURCE_MULTI_OBSERVER_QUERY_IS_NEXT_GATE" in report,
    }
    result = {
        "status": "PASS" if all(guards.values()) else "FAIL",
        "guards": guards,
        "manifest_rows": len(manifest_checks),
        "missing": missing,
        "preregistration_commit": PREREG_COMMIT,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
