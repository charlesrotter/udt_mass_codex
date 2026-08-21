#!/usr/bin/env python3
"""No-write package replay for G202."""

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


def run_json(script: str):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
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

    production = run_json("derive_quiet_overlap_profile.py")
    independent = run_json("verify_quiet_overlap_independent.py")
    catches = run_json("run_catch_proofs.py")
    assert production == json.loads((PACKAGE / "PRODUCTION_RESULT.json").read_text())
    assert independent == json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    assert catches == json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["all_pass"] and production["assertions"] == 32
    assert independent["all_pass"] and independent["cases"] == 20000
    assert independent["anchor_controls"] == 1000
    assert independent["assertions"] == 170003
    assert independent["production_imports"] is False
    assert independent["production_artifacts_read"] is False
    assert catches["all_pass"] and catches["caught"] == catches["total"] == 9

    report = (PACKAGE / "AUDIT_REPORT.md").read_text()
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text()
    prereg = (PACKAGE / "PREREGISTRATION.md").read_text()
    for token in (
        "QUIET_OVERLAP_FORCES_SECOND_ORDER_FLATNESS",
        "TWO_SIDED_GROWTH_HAS_INFINITE_NATIVE_PROFILES",
        "ANCHORS_CALIBRATE_BUT_DO_NOT_DERIVE_HISTORY",
    ):
        assert token in report and token in exact
    assert "PREREGISTERED_BEFORE_CONFIRMATORY_IMPLEMENTATION" in prereg
    assert "not a selected UDT history" in exact
    assert "does not select the physical profile" in report

    print(json.dumps({
        "all_pass": True,
        "source_hashes": source_checks,
        "production_assertions": production["assertions"],
        "independent_assertions": independent["assertions"],
        "independent_cases": independent["cases"],
        "anchor_controls": independent["anchor_controls"],
        "mutation_catches": catches["caught"],
        "no_write_replay": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
