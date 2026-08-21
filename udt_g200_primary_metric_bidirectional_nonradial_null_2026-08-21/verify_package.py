#!/usr/bin/env python3
"""No-write package replay for G200."""

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

    production = run_json("derive_primary_bidirectional_nonradial_null.py")
    independent = run_json("verify_primary_bidirectional_nonradial_independent.py")
    catches = run_json("run_catch_proofs.py")
    assert production == json.loads((PACKAGE / "PRODUCTION_RESULT.json").read_text())
    assert independent == json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    assert catches == json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["all_pass"] and production["assertions"] == 64
    assert independent["all_pass"] and independent["cases"] == 2000
    assert independent["assertions"] == 38160
    assert independent["nonzero_gradient_cases"] == 2000
    assert independent["production_imports"] is False
    assert independent["production_artifacts_read"] is False
    assert catches["all_pass"] and catches["caught"] == catches["total"] == 9

    report = (PACKAGE / "AUDIT_REPORT.md").read_text()
    prereg = (PACKAGE / "PREREGISTRATION.md").read_text()
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text()
    required = [
        "ONE_PRIMARY_NONRADIAL_LAW",
        "FINITE_DIRECTIONAL_DIFFERENCE_IS_RADIAL_REGIME_SAMPLING",
    ]
    assert all(token in report and token in exact for token in required)
    assert "PREREGISTERED_BEFORE_CONFIRMATORY_IMPLEMENTATION" in prereg
    assert "same two diagonal" in report
    assert "does not select" in exact
    assert "does not derive that full magnitude profile" in report

    print(json.dumps({
        "all_pass": True,
        "source_hashes": source_checks,
        "production_assertions": production["assertions"],
        "independent_assertions": independent["assertions"],
        "independent_cases": independent["cases"],
        "independent_nonzero_gradient_cases": independent["nonzero_gradient_cases"],
        "flat_controls": independent["flat_controls"],
        "mutation_catches": catches["caught"],
        "no_write_replay": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
