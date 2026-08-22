#!/usr/bin/env python3
"""Final byte-stable package verification for G210 after external review."""

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
    assert core["production_assertions"] == 24
    assert core["independent_cases"] == 10_000
    assert core["independent_assertions"] == 250_001
    assert core["diagnostic_precision_digits"] == 120
    assert core["mutation_catches"] == 25
    assert core["provenance_manifest_rows"] == 9
    assert core["no_write_replay"] is True
    assert core["external_review"] == "PENDING_SEPARATE_GATE"

    review = (PACKAGE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    assert review.startswith("Primary grade: `VERIFIED_WITH_CAVEATS`.")
    assert "No refuting error emerged inside the sealed intake" in review
    assert "all 35 scoped file hashes matched" in review
    assert "Required repairs: none." in review
    assert "finite-dimensional local core is independently verified" in review

    transmission = compact("TRANSMISSION_RECORD.md")
    for token in (
        "a24c576e2deddfa0531bbb8645f92d2e31c002799b9a31616e69e22119c463a0",
        "316bc5cb513911595a9b8903d3d48af0ac40c962183019dc22669776ec44f16e",
        "Payload hashes: 35/35 passed",
        "VERIFIED_WITH_CAVEATS",
        "Required repairs: none",
    ):
        assert token in transmission

    gates = compact("EVIDENCE_GATES.md")
    assert "Fresh external review — PASS WITH CAVEATS" in gates
    assert "EXTERNALLY_VERIFIED_WITH_CAVEATS__NO_REPAIRS_REQUIRED" in gates
    report = compact("AUDIT_REPORT.md")
    assert "NO_PHYSICAL_SIGMA_HISTORY_OR_XMAX_SELECTION" in report
    assert "all 35 scoped payload hashes" in report

    result = {
        "status": "PASS",
        "core_no_write_replay": True,
        "production_assertions": core["production_assertions"],
        "independent_cases": core["independent_cases"],
        "independent_assertions": core["independent_assertions"],
        "diagnostic_precision_digits": core["diagnostic_precision_digits"],
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
