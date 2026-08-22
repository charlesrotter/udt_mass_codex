#!/usr/bin/env python3
"""Byte-stable no-write core package replay for G207."""

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
        run_json("derive_tracefree_screen_robustness.py"),
        run_json("verify_tracefree_screen_independent.py"),
        run_json("run_boundary_diagnostics.py"),
        run_json("run_catch_proofs.py"),
    )
    after = {path.name: sha256(path) for path in result_paths}
    assert before == after

    saved = tuple(json.loads(path.read_text(encoding="utf-8")) for path in result_paths)
    assert replay == saved[:4]
    production, independent, diagnostics, catches, provenance = saved
    assert production["all_pass"] and production["assertions"] == 36
    assert "global_hyperbolicity_for_every_smooth_declared_S" in production["analytic_theorems_recorded_not_mechanized"]
    assert "null_completeness_for_every_smooth_static_declared_S" in production["analytic_theorems_recorded_not_mechanized"]
    assert "global_hyperbolicity_for_every_smooth_declared_S" not in production["mechanized_scope"]
    assert independent["all_pass"] and independent["cases"] == 10_000
    assert independent["distinct_cases"] == 10_000 and independent["assertions"] == 110_009
    assert independent["production_imported"] is False and independent["production_artifact_read"] is False
    assert independent["changed_clock_cases"] == 10_000
    assert independent["changed_pair_area_cases"] == 10_000
    assert independent["changed_beta_cases"] == 10_000
    assert diagnostics["all_pass"] and diagnostics["precision_digits"] == 100
    assert catches["all_pass"] and catches["caught"] == 24
    assert provenance["all_pass"] and provenance["checked_in_live_repository_context"] == 7
    assert provenance["package_replay_dependency"] is False

    report = " ".join((PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    exact = " ".join((PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8").split())
    for token in (
        "TRACEFREE_SCREEN_SHEAR_PRESERVES_AMBIENT_VOLUME_SIGNATURE_RADIAL_CAUSAL_BOUND_AND_G205_GLOBAL_HYPERBOLICITY",
        "UNRESTRICTED_SMOOTH_TIME_LIVE_SHEAR_CAN_AFFINELY_COMPRESS_A_G205_CIRCULAR_NULL_ORBIT_TO_FINITE_LENGTH",
        "COMPLETED_PAIR_KERNEL_HEARS_SHEAR_EXACTLY_WHEN_THE_SUPPLIED_CLOCK_GERM_HAS_SCREEN_CONTENT",
        "NO_PHYSICAL_S_HISTORY_OR_XMAX_SELECTION",
    ):
        assert token in report and token in exact
    for guard in (
        "not a selected UDT history",
        "does not classify timelike/spacelike completeness",
        "does not use observations or `X_max`",
    ):
        assert guard in report or guard in " ".join((PACKAGE / "LAY_REPORT.md").read_text(encoding="utf-8").split())
    evidence = " ".join((PACKAGE / "EVIDENCE_GATES.md").read_text(encoding="utf-8").split())
    assert "f7f9d92d" in evidence and "Fresh adversarial review:** `VERIFIED_WITH_CAVEATS`" in evidence
    external = " ".join((PACKAGE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8").split())
    assert "`VERIFIED_WITH_CAVEATS`" in external
    assert "Mathematical errors found: none within the sealed intake" in external
    assert "No repair changes the science" in external
    transmission = " ".join((PACKAGE / "TRANSMISSION_RECORD.md").read_text(encoding="utf-8").split())
    assert "c116af7a562eccdc372b4d78955b813be964f8fcb121abcbe76e324581db29c4" in transmission
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
