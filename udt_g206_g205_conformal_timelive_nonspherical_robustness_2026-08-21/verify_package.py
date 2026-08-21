#!/usr/bin/env python3
"""Byte-stable no-write package replay for G206."""

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
    rows = 0
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            assert len(row["sha256"]) == 64
            int(row["sha256"], 16)
            assert row["path"] and not Path(row["path"]).is_absolute()
            rows += 1
    assert rows == 7

    result_paths = (
        PACKAGE / "PRODUCTION_RESULT.json",
        PACKAGE / "INDEPENDENT_VERIFICATION.json",
        PACKAGE / "BOUNDARY_DIAGNOSTICS.json",
        PACKAGE / "CATCH_PROOF_RESULT.json",
        PACKAGE / "SOURCE_PROVENANCE_VERIFICATION.json",
    )
    before = {path.name: sha256(path) for path in result_paths}
    replay = (
        run_json("derive_conformal_robustness.py"),
        run_json("verify_conformal_robustness_independent.py"),
        run_json("run_boundary_diagnostics.py"),
        run_json("run_catch_proofs.py"),
    )
    after = {path.name: sha256(path) for path in result_paths}
    assert before == after

    saved = tuple(json.loads(path.read_text(encoding="utf-8")) for path in result_paths)
    assert replay == saved[:4]
    production, independent, diagnostics, catches, provenance = saved
    assert production["all_pass"] and production["assertions"] == 27
    assert "global_hyperbolicity_conformal_transfer" in production["analytic_theorems_recorded_not_mechanized"]
    assert "all_null_geodesic_integral_iff_criterion" in production["analytic_theorems_recorded_not_mechanized"]
    assert independent["all_pass"] and independent["cases"] == 10000
    assert independent["distinct_cases"] == 10000 and independent["assertions"] == 160006
    assert independent["production_imported"] is False and independent["production_artifact_read"] is False
    assert "direct_radial_coordinate_geodesic" in independent["method"]
    assert diagnostics["all_pass"] and diagnostics["precision_digits"] == 160
    assert "cancellation" in diagnostics["repair_note"]
    assert catches["all_pass"] and catches["caught"] == 19
    assert provenance["all_pass"] and provenance["checked_in_live_repository_context"] == 7
    assert provenance["package_replay_dependency"] is False

    report = " ".join((PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    exact = " ".join((PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    for token in (
        "CONFORMAL_COMMON_SCALE_PRESERVES_G205_CAUSAL_ORDER_AND_GLOBAL_HYPERBOLICITY",
        "NULL_COMPLETENESS_IFF_THE_CONFORMAL_AFFINE_WEIGHT_DIVERGES",
        "COMPLETED_PAIR_PHI_SHIFTS_BY_MINUS_OMEGA_PULLBACK",
        "NO_PHYSICAL_OMEGA_HISTORY_OR_XMAX_SELECTION",
    ):
        assert token in report and token in exact
    for guard in (
        "not a selected UDT history",
        "does not classify timelike or spacelike completeness",
        "does not yet say which time-live",
    ):
        assert guard in report or guard in " ".join((PACKAGE / "LAY_REPORT.md").read_text(encoding="utf-8").split())
    external = " ".join((PACKAGE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8").split())
    assert "VERIFIED_WITH_CAVEATS" in external
    assert "Mathematical errors found:" in external and "none in the bounded landing" in external
    assert "does not alter the witnesses, formulas, completeness classes, or scientific landing" in external
    transmission = " ".join((PACKAGE / "TRANSMISSION_RECORD.md").read_text(encoding="utf-8").split())
    assert "ba82383240b505a46c9ca4d46eeef55e841861d69be76bbd405cd62a1693a590" in transmission
    assert "VERIFIED_WITH_CAVEATS" in transmission and "Process exit: zero" in transmission

    result = {
        "all_pass": True,
        "provenance_manifest_rows": rows,
        "live_source_hash_check": "SEPARATE_REPOSITORY_CONTEXT_GATE",
        "production_assertions": production["assertions"],
        "independent_assertions": independent["assertions"],
        "independent_cases": independent["cases"],
        "distinct_cases": independent["distinct_cases"],
        "diagnostic_precision_digits": diagnostics["precision_digits"],
        "mutation_catches": catches["caught"],
        "live_source_hashes_recorded": provenance["checked_in_live_repository_context"],
        "no_write_replay": True,
        "external_adversarial_review": "VERIFIED_WITH_CAVEATS",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
