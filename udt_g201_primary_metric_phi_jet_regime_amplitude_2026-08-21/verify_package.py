#!/usr/bin/env python3
"""No-write package replay for G201."""

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

    production = run_json("derive_phi_jet_regime_amplitude.py")
    independent = run_json("verify_phi_jet_amplitude_independent.py")
    catches = run_json("run_catch_proofs.py")
    assert production == json.loads((PACKAGE / "PRODUCTION_RESULT.json").read_text())
    assert independent == json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    assert catches == json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["all_pass"] and production["assertions"] == 20
    assert independent["all_pass"] and independent["cases"] == 10000
    assert independent["assertions"] == 23606
    assert independent["cancellation_cases"] == 1000
    assert independent["family_signs_seen"] == [-1, 1]
    assert independent["production_imports"] is False
    assert independent["production_artifacts_read"] is False
    assert catches["all_pass"] and catches["caught"] == catches["total"] == 9

    report = (PACKAGE / "AUDIT_REPORT.md").read_text()
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text()
    prereg = (PACKAGE / "PREREGISTRATION.md").read_text()
    for token in (
        "TWO_SIDED_RECIPROCAL_MAGNITUDE",
        "ANGULAR_VOLUME_IS_PHI_JET_DEPENDENT",
        "NO_LOCKSTEP_LOUDNESS_FORCED",
    ):
        assert token in report and token in exact
    assert "PREREGISTERED_BEFORE_CONFIRMATORY_IMPLEMENTATION" in prereg
    assert "does not choose among them" in exact
    assert "does not select which allowed profile" in report

    print(json.dumps({
        "all_pass": True,
        "source_hashes": source_checks,
        "production_assertions": production["assertions"],
        "independent_assertions": independent["assertions"],
        "independent_cases": independent["cases"],
        "cancellation_cases": independent["cancellation_cases"],
        "family_controls": independent["family_controls_requested"],
        "mutation_catches": catches["caught"],
        "no_write_replay": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
