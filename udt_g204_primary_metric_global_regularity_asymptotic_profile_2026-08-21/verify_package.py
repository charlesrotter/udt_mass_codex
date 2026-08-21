#!/usr/bin/env python3
"""Byte-stable no-write package replay for G204."""

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
        PACKAGE / "BOUNDARY_DIAGNOSTICS.json",
        PACKAGE / "CATCH_PROOF_RESULT.json",
    )
    before = {path.name: sha256(path) for path in result_paths}
    production = run_json("derive_global_regularity.py")
    independent = run_json("verify_global_regularity_independent.py")
    diagnostics = run_json("run_boundary_diagnostics.py")
    catches = run_json("run_catch_proofs.py")
    after = {path.name: sha256(path) for path in result_paths}
    assert before == after

    observed = [json.loads(path.read_text(encoding="utf-8")) for path in result_paths]
    assert production == observed[0]
    assert independent == observed[1]
    assert diagnostics == observed[2]
    assert catches == observed[3]
    assert production["all_pass"] and production["assertions"] == 113
    assert independent["all_pass"] and independent["cases"] == 10000
    assert independent["distinct_cases"] == 10000
    assert independent["assertions"] == 160010
    assert diagnostics["all_pass"] and diagnostics["precision_digits"] == 80
    assert catches["all_pass"] and catches["caught"] == 13

    report = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    correction = (PACKAGE / "CORRECTION_PREREGISTRATION.md").read_text(encoding="utf-8")
    for token in (
        "SMOOTH_CENTER_EXCLUDES_MONOTONE_TWO_SIDED_LOG_EXTENSION",
        "EVEN_AREAL_INNER_TROUGH_AND_OUTER_RECIPROCAL_ASYMPTOTE_FAMILY_SURVIVES",
        "GLOBAL_REGULARITY_DOES_NOT_SELECT_N_R0_OR_A",
    ):
        assert token in report and token in exact
    assert "CENTER_CURVATURE_BOUNDED_BUT_NOT_SMOOTH" in correction
    assert "not standard asymptotic flatness" in exact
    assert "does not select" in " ".join(report.lower().split())

    result = {
        "all_pass": True,
        "source_hashes": source_checks,
        "production_assertions": production["assertions"],
        "independent_assertions": independent["assertions"],
        "independent_cases": independent["cases"],
        "distinct_cases": independent["distinct_cases"],
        "diagnostic_precision_digits": diagnostics["precision_digits"],
        "mutation_catches": catches["caught"],
        "no_write_replay": True,
        "repair_preregistered": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
