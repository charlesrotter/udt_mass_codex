#!/usr/bin/env python3
"""Fail-closed verifier for G140."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def run(name: str) -> str:
    result = subprocess.run(
        [sys.executable, str(HERE / name)], cwd=HERE.parent, text=True,
        capture_output=True, check=False,
    )
    require(result.returncode == 0, result.stdout + result.stderr)
    return result.stdout.strip()


def main() -> None:
    production = json.loads(run("derive_atlas_congruence.py"))
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = run("verify_atlas_congruence_independent.py")
    require(production == saved, "saved production result differs")
    require(production["checks_passed"] == production["checks_total"] == 43, "production count")
    require("PASS 15/15" in independent, "independent count")
    require(independent == (HERE / "INDEPENDENT_VERIFICATION.txt").read_text(encoding="utf-8").strip(),
            "saved independent output differs")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (HERE / "OUTCOME_PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    note = (HERE / "TYPE_PRECISION_NOTE.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS.md").read_text(encoding="utf-8")
    followup = (HERE / "FOLLOWUP_REVIEW.md").read_text(encoding="utf-8")
    report_words = " ".join(report.split())
    exact_words = " ".join(exact.split())
    note_words = " ".join(note.split())
    require("pooled rank-ten design" in report_words and "log(2)/4" in report,
            "load-bearing result absent")
    require("same constant metric coefficient matrix" in report, "same-history control absent")
    require("not an equation on `g` alone" in report, "metric-only ceiling absent")
    require("do not pre-supply" in report, "congruence noncircularity guard absent")
    require("affine parameter reversal alone" in report, "inverse-query guard absent")
    require("same middle observer worldline" in report and "piecewise route is composable" in report,
            "middle-observer composition witness absent")
    require("not a fully realized physical observer-network counterexample" in report_words,
            "physical-counterexample overclaim guard absent")
    require("later native observer-relation construction" in exact_words,
            "future derivation boundary absent")
    require("SUPPLIED_G137_G138_LIFT" in ledger, "inverse status absent")
    require("does **not** mean" in note and "assume the tested property" in note,
            "matched-calibration type guard absent")
    require("ell_0" in note and "tau_0=ell_0/c_E" in note and
            "does not supply an absolute physical length" in note_words,
            "explicit dimensional calibration guard absent")
    require("unoriented terminal scalar" in note and "antisymmetric" in note,
            "terminal/orientation type separation absent")
    require(production["nonclosing"]["inverse_sign_assignments_tested"] == 8 and
            production["nonclosing"]["closing_sign_assignments"] == 0,
            "inverse sign exhaustion absent")
    require("not a G129 pointwise rank-ten atlas for an arbitrary metric" in exact_words,
            "pooled-versus-pointwise rank guard absent")
    require("does not construct the still-open physical inverse/query owner" in note_words,
            "physical inverse ownership ceiling absent")
    require("VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS" in status,
            "final grade absent")
    require("Landing: `PASS`" in followup and "zero closing lifts" in followup,
            "repair-only follow-up evidence absent")
    print("PASS 21/21: G140 exact controls, independent replay, and repaired type guards")


if __name__ == "__main__":
    main()
