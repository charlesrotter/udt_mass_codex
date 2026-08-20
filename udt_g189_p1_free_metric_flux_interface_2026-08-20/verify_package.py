#!/usr/bin/env python3
"""Verify the complete G189 package and live replays."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REQUIRED = (
    "PREREGISTRATION.md",
    "SCOPE_CORRECTION_PREREGISTRATION.md",
    "EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md",
    "TRANSMISSION_RECORD.md",
    "EXTERNAL_REVIEW_RAW.md",
    "EXTERNAL_REVIEW_TRANSCRIPT.txt.gz",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
    "EXTERNAL_REVIEW_FOLLOWUP_REQUEST.md",
    "EXTERNAL_REVIEW_FOLLOWUP_RAW.md",
    "EXTERNAL_REVIEW_FOLLOWUP_TRANSCRIPT.txt.gz",
    "EXTERNAL_REVIEW_FOLLOWUP_TRANSMISSION_RECORD.md",
    "SOURCE_MANIFEST.tsv",
    "derive_p1_free_flux_interface.py",
    "verify_p1_free_flux_independent.py",
    "run_catch_proofs.py",
    "build_review_intake.py",
    "PRODUCTION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv",
)


def replay(script: str) -> tuple[int, dict[str, object], str]:
    env = os.environ.copy()
    env.pop("UDT_WRITE_G189_RESULT", None)
    env.pop("UDT_WRITE_G189_INDEPENDENT", None)
    env.pop("UDT_WRITE_G189_CATCHES", None)
    completed = subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=HERE.parent,
        env=env,
        check=False,
        text=True,
        capture_output=True,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        payload = {}
    return completed.returncode, payload, completed.stderr


def main() -> None:
    missing = [name for name in REQUIRED if not (HERE / name).is_file()]
    stored_production = json.loads((HERE / "PRODUCTION_RESULT.json").read_text())
    stored_independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    stored_catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())

    prod_rc, live_production, prod_err = replay("derive_p1_free_flux_interface.py")
    ind_rc, live_independent, ind_err = replay("verify_p1_free_flux_independent.py")
    catch_rc, live_catches, catch_err = replay("run_catch_proofs.py")

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    external_review = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    followup_review = (HERE / "EXTERNAL_REVIEW_FOLLOWUP_RAW.md").read_text(encoding="utf-8")
    independent_source = (HERE / "verify_p1_free_flux_independent.py").read_text(
        encoding="utf-8"
    )
    production_source = (HERE / "derive_p1_free_flux_interface.py").read_text(
        encoding="utf-8"
    )
    builder_source = (HERE / "build_review_intake.py").read_text(encoding="utf-8")
    source_manifest = (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8")
    cross_residuals = {
        "pantheon_chi2": abs(
            float(live_independent["pantheon"]["chi2"])
            - float(stored_production["pantheon"]["chi2"])
        ),
        "pantheon_offset": abs(
            float(live_independent["pantheon"]["offset"])
            - float(stored_production["pantheon"]["offset"])
        ),
        "des_chi2": abs(
            float(live_independent["des"]["chi2"])
            - float(stored_production["des"]["chi2"])
        ),
        "des_offset": abs(
            float(live_independent["des"]["offset"])
            - float(stored_production["des"]["offset"])
        ),
    }
    checks = {
        "all_required_files": not missing,
        "production_pass": stored_production.get("status") == "PASS",
        "independent_pass": stored_independent.get("status") == "PASS",
        "catch_proofs_pass": stored_catches.get("status") == "PASS",
        "production_live_replay": prod_rc == 0 and live_production == stored_production,
        "independent_live_replay": ind_rc == 0 and live_independent == stored_independent,
        "catch_live_replay": catch_rc == 0 and live_catches == stored_catches,
        "scientific_landing_retained": stored_production.get("scientific_landing")
        == (
            "STATIC_CHI_SCREEN_JOIN_TYPE_FAILS_REGULAR_CENTER_AND_IS_DATA_REJECTED_AS_FORMAL_ANNULAR_CONTROL__"
            "METRIC_TO_FLUX_FACTORIZATION_CLOSES_CONDITIONALLY__"
            "P1_ROLE_LOCALIZED_TO_UNOWNED_PHI_OF_R_OR_TIMELIVE_FREQUENCY_HISTORY"
        ),
        "pantheon_score_retained": abs(
            float(stored_production["pantheon"]["chi2"]) - 3204.9509632650042
        ) <= 1e-9,
        "des_score_retained": abs(
            float(stored_production["des"]["chi2"]) - 2685.9110340934367
        ) <= 1e-9,
        "zero_shape_parameters": stored_production["candidate"]["shape_parameters"] == 0,
        "transfer_stays_imported": "IMPORTED_CONDITIONAL" in report,
        "join_stays_provisional": "CHOSE_PROVISIONAL_CONTROL" in report,
        "timelive_stays_open": "time-live" in exact,
        "kernel_negative_forbidden": "does not reject completed-pair" in report,
        "source_hashes_pass": all(stored_production["source_hashes"].values()),
        "source_hash_keys_host_independent": all(
            not Path(key).is_absolute() for key in stored_production["source_hashes"]
        ),
        "DES_root_has_no_host_default": all(
            "/media/" not in source
            and 'os.environ["G189_DES_ROOT"]' in source
            for source in (production_source, independent_source, builder_source)
        ),
        "DES_manifest_paths_are_logical": (
            "external_data/DES-Dovekie_HD.csv" in source_manifest
            and "external_data/STAT+SYS.npz" in source_manifest
            and "/media/" not in source_manifest
        ),
        "independent_replay_reads_no_production_artifact": (
            "PRODUCTION_RESULT.json" not in independent_source
            and live_independent.get("production_artifact_read") is False
        ),
        "implementation_distinct_cross_replay": (
            cross_residuals["pantheon_chi2"] <= 3e-6
            and cross_residuals["pantheon_offset"] <= 3e-9
            and cross_residuals["des_chi2"] <= 3e-6
            and cross_residuals["des_offset"] <= 3e-9
        ),
        "external_grade_retained": "G189_ACCEPTED_WITH_REPAIRS" in external_review,
        "all_four_scientific_claims_survive_review": all(
            phrase in external_review
            for phrase in (
                "Metric-to-flux factorization survives conditionally",
                "Regular-center type failure survives",
                "Numerical negative survives",
                "Localization of P1 to profile/frequency history survives",
            )
        ),
        "repair_followup_accepted": (
            "G189_REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED" in followup_review
            and "EXTERNALLY_ACCEPTED_WITH_REPAIRS_CLOSED" in adjudication
        ),
    }
    result = {
        "audit": "G189_PACKAGE",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "missing": missing,
        "replay_stderr": {
            "production": prod_err,
            "independent": ind_err,
            "catches": catch_err,
        },
        "cross_replay_residuals": cross_residuals,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
