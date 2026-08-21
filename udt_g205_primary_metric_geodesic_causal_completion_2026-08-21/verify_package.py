#!/usr/bin/env python3
"""Byte-stable no-write package replay for G205."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "PACKAGE_VERIFICATION_RESULT.json"


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
        cwd=PACKAGE,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    provenance_rows = 0
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            assert len(row["sha256"]) == 64
            int(row["sha256"], 16)
            assert row["path"] and not Path(row["path"]).is_absolute()
            provenance_rows += 1
    assert provenance_rows == 7

    result_paths = (
        PACKAGE / "PRODUCTION_RESULT.json",
        PACKAGE / "INDEPENDENT_VERIFICATION.json",
        PACKAGE / "BOUNDARY_DIAGNOSTICS.json",
        PACKAGE / "CATCH_PROOF_RESULT.json",
        PACKAGE / "SOURCE_PROVENANCE_VERIFICATION.json",
    )
    before = {path.name: sha256(path) for path in result_paths}
    production = run_json("derive_geodesic_completion.py")
    independent = run_json("verify_geodesic_completion_independent.py")
    diagnostics = run_json("run_boundary_diagnostics.py")
    catches = run_json("run_catch_proofs.py")
    after = {path.name: sha256(path) for path in result_paths}
    assert before == after

    observed = [json.loads(path.read_text(encoding="utf-8")) for path in result_paths]
    assert production == observed[0]
    assert independent == observed[1]
    assert diagnostics == observed[2]
    assert catches == observed[3]
    provenance = observed[4]
    assert production["all_pass"] and production["assertions"] == 112
    assert set(production["geodesic_types"]) == {"timelike", "null", "spacelike"}
    assert "global_hyperbolicity" in production["analytic_theorems_recorded_not_mechanized"]
    assert production["finite_radius_killing_horizon"] is False
    assert independent["all_pass"] and independent["cases"] == 10000
    assert independent["distinct_cases"] == 10000
    assert independent["assertions"] == 150000
    assert independent["method"] == "independent_exact_rational_algebraic_core_only"
    assert diagnostics["all_pass"] and diagnostics["precision_digits"] == 80
    assert catches["all_pass"] and catches["caught"] == 17
    assert provenance["all_pass"] and provenance["checked_in_live_repository_context"] == 7
    assert provenance["package_replay_dependency"] is False

    report = " ".join((PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    exact = " ".join((PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    followup = " ".join((PACKAGE / "EXTERNAL_REPAIR_FOLLOWUP.md").read_text(encoding="utf-8").split())
    assert "REPAIRS_VERIFIED__LANDING_RETAINED" in report and "REPAIRS_VERIFIED__LANDING_RETAINED" in followup
    for token in (
        "FULL_GEODESIC_COMPLETENESS_AND_GLOBAL_HYPERBOLICITY_SURVIVE_ALL_REGISTERED_PARAMETERS",
        "NULL_TRAPPING_HAS_SUBCRITICAL_CRITICAL_AND_SUPERCRITICAL_STRATA",
        "NO_PARAMETER_XMAX_OR_PHYSICAL_HISTORY_SELECTION",
    ):
        assert token in report and token in exact
    for guard in (
        "not standard asymptotic flatness",
        "not identified with `X_max`",
        "not a newly adopted postulate",
        "does not select",
    ):
        assert guard in exact or guard in report

    result = {
        "all_pass": True,
        "provenance_manifest_rows": provenance_rows,
        "live_source_hash_check": "SEPARATE_REPOSITORY_CONTEXT_GATE",
        "production_assertions": production["assertions"],
        "independent_assertions": independent["assertions"],
        "independent_cases": independent["cases"],
        "distinct_cases": independent["distinct_cases"],
        "diagnostic_precision_digits": diagnostics["precision_digits"],
        "mutation_catches": catches["caught"],
        "live_source_hashes_recorded": provenance["checked_in_live_repository_context"],
        "no_write_replay": True,
        "initial_adversarial_review": "REPAIR_REQUIRED_WITH_LANDING_RETAINED",
        "repair_only_followup": "REPAIRS_VERIFIED__LANDING_RETAINED",
        "registered_repairs": "VERIFIED",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
