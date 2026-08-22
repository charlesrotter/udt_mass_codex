#!/usr/bin/env python3
"""Final byte-stable package verification for G211 after external review."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "PACKAGE_VERIFICATION_RESULT.json"


def run_json(script: str) -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["UDT_NO_WRITE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(PACKAGE / script)],
        cwd=PACKAGE,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def compact(name: str) -> str:
    return " ".join((PACKAGE / name).read_text(encoding="utf-8").split())


def main() -> None:
    core = run_json("verify_core_package.py")
    assert core["status"] == "PASS"
    assert core["production_assertions"] == 29
    assert core["independent_cases"] == 10_000
    assert core["independent_assertions"] == 280_003
    assert core["radial_precision_digits"] == 120
    assert core["radial_profiles"] == 4
    assert core["mutation_catches"] == 31
    assert core["provenance_manifest_rows"] == 8
    assert core["no_write_replay"] is True
    assert core["external_review"] == "PENDING_SEPARATE_GATE"

    review = (PACKAGE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    assert review.startswith("**Primary Grade**\n\n`VERIFIED_WITH_CAVEATS`")
    assert "No refuting defect was found" in review
    assert "all 34 registered payload hashes matched" in review
    assert "None required for the sealed claim set" in review
    assert "exactly two-dimensional" in review

    transmission = compact("TRANSMISSION_RECORD.md")
    for token in (
        "553151874b32f4411ac184eae7d3c8d035b8230e9b87f5d46e3c94c0aea7dbc5",
        "1c74daf06c0be362726ff4154abbe42a73dcf12e3b9fc77f6ed43d4162731c26",
        "Payload hashes: 34/34 passed",
        "VERIFIED_WITH_CAVEATS",
        "Required repairs: none",
    ):
        assert token in transmission

    gates = compact("EVIDENCE_GATES.md")
    assert "Fresh external review — PASS WITH CAVEATS" in gates
    assert "EXTERNALLY_VERIFIED_WITH_CAVEATS__NO_REPAIRS_REQUIRED" in gates
    report = compact("AUDIT_REPORT.md")
    assert "NO_PHYSICAL_SCALAR_HISTORY_OR_XMAX_SELECTION" in report
    assert "all 34 payload hashes" in report

    result = {
        "status": "PASS",
        "core_no_write_replay": True,
        "production_assertions": core["production_assertions"],
        "independent_cases": core["independent_cases"],
        "independent_assertions": core["independent_assertions"],
        "radial_precision_digits": core["radial_precision_digits"],
        "radial_profiles": core["radial_profiles"],
        "mutation_catches": core["mutation_catches"],
        "provenance_manifest_rows": core["provenance_manifest_rows"],
        "external_review": "VERIFIED_WITH_CAVEATS",
        "required_repairs": 0,
        "scientific_landing_changed": False,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
