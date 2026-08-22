#!/usr/bin/env python3
"""Final byte-stable package verification for G209 after external review."""

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
    assert core["production_assertions"] == 21
    assert core["independent_cases"] == 10_000
    assert core["independent_assertions"] == 100_001
    assert core["diagnostic_precision_digits"] == 120
    assert core["mutation_catches"] == 25
    assert core["provenance_manifest_rows"] == 8
    assert core["no_write_replay"] is True
    assert core["external_review"] == "PENDING_SEPARATE_GATE"

    first = (PACKAGE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    followup = (PACKAGE / "EXTERNAL_REPAIR_FOLLOWUP_RAW.md").read_text(encoding="utf-8")
    assert first.startswith("VERIFIED_WITH_CAVEATS")
    assert "All `33/33` scoped payload hashes matched" in first
    assert "I do not see a counterexample within the declared G205 scope" in first
    assert followup.startswith("G209_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED")
    assert "all `37/37` listed payload hashes matched" in followup
    assert "exited `0`" in followup

    transmission = compact("TRANSMISSION_RECORD.md")
    for token in (
        "2699a11aa5368ae0f36df2ab1936db819181a627bf093c3ea27776a9138123d5",
        "797462ac0b853c2e8e94f0b478ca7497df21c4217ea97b636ab0860eaf089566",
        "731ac771b193cdcf074fa04d4d9418eda45d76b31037b60797b7914d796454c3",
        "cf362fab780df23542f327bffda7c0f1edfce18a0de4167d2691d3eea2e23765",
        "G209_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED",
    ):
        assert token in transmission

    gates = compact("EVIDENCE_GATES.md")
    assert "Repair-only follow-up — PASS" in gates
    assert "EXTERNALLY_VERIFIED_WITH_CAVEATS__REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED" in gates
    report = compact("AUDIT_REPORT.md")
    assert "NO_PHYSICAL_SHIFT_HISTORY_OR_XMAX_SELECTION" in report
    assert "all 37 scoped payload hashes" in report

    result = {
        "status": "PASS",
        "core_no_write_replay": True,
        "production_assertions": core["production_assertions"],
        "independent_cases": core["independent_cases"],
        "independent_assertions": core["independent_assertions"],
        "diagnostic_precision_digits": core["diagnostic_precision_digits"],
        "mutation_catches": core["mutation_catches"],
        "provenance_manifest_rows": core["provenance_manifest_rows"],
        "first_external_review": "VERIFIED_WITH_CAVEATS",
        "repair_followup": "G209_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED",
        "scientific_landing_changed": False,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
