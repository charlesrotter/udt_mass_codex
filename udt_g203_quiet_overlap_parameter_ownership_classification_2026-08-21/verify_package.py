#!/usr/bin/env python3
"""No-write package replay for G203."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_json(script: str) -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["UDT_NO_WRITE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(PACKAGE / script)],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    source_checks = 0
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["path"]
            assert path.is_file(), row["path"]
            assert sha256(path) == row["sha256"], row["path"]
            source_checks += 1

    result_paths = (
        PACKAGE / "PRODUCTION_RESULT.json",
        PACKAGE / "INDEPENDENT_VERIFICATION.json",
        PACKAGE / "CATCH_PROOF_RESULT.json",
    )
    before = {path.name: sha256(path) for path in result_paths}
    production = run_json("derive_parameter_ownership.py")
    independent = run_json("verify_parameter_ownership_independent.py")
    catches = run_json("run_catch_proofs.py")
    after = {path.name: sha256(path) for path in result_paths}
    assert before == after

    assert production == json.loads(result_paths[0].read_text())
    assert independent == json.loads(result_paths[1].read_text())
    assert catches == json.loads(result_paths[2].read_text())
    assert production["all_pass"] and production["assertions"] == 70
    assert independent["all_pass"] and independent["cases"] == 20000
    assert independent["distinct_cases"] == 20000
    assert independent["assertions"] == 280011
    assert independent["production_imported"] is False
    assert independent["production_artifact_read"] is False
    assert catches["all_pass"] and catches["caught"] == 10

    report = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    prereg = (PACKAGE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for token in (
        "INVARIANT_AFTER_AREAL_AND_DEPTH_CALIBRATION",
        "FOUNDING_DOES_NOT_SELECT_ORDER_LOCATION_OR_STEEPNESS",
        "OBSERVATIONS_MAY_CALIBRATE_A_DECLARED_FAMILY",
    ):
        assert token in report and token in exact
    assert "Maximum conclusion" in prereg
    assert "not a proposed physical profile" in (PACKAGE / "MAP.md").read_text(encoding="utf-8")
    assert "does not select the physical profile" in report

    result = {
        "all_pass": True,
        "source_hashes": source_checks,
        "production_assertions": production["assertions"],
        "independent_assertions": independent["assertions"],
        "independent_cases": independent["cases"],
        "distinct_cases": independent["distinct_cases"],
        "mutation_catches": catches["caught"],
        "no_write_replay": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
