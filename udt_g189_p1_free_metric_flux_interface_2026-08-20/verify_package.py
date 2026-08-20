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
    "SOURCE_MANIFEST.tsv",
    "derive_p1_free_flux_interface.py",
    "verify_p1_free_flux_independent.py",
    "run_catch_proofs.py",
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
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
