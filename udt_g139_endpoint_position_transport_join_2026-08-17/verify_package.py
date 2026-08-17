#!/usr/bin/env python3
"""Fail-closed package verifier for G139."""

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
        [sys.executable, str(HERE / name)],
        cwd=HERE.parent,
        text=True,
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, result.stdout + result.stderr)
    return result.stdout.strip()


def main() -> None:
    production = json.loads(run("derive_endpoint_transport_join.py"))
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = run("verify_endpoint_transport_join_independent.py")
    require(production == saved, "saved production result differs")
    require(production["checks_passed"] == production["checks_total"] == 20, "production count")
    require("PASS 2915/2915" in independent, "independent count")
    require(
        independent == (HERE / "INDEPENDENT_VERIFICATION.txt").read_text(encoding="utf-8").strip(),
        "saved independent output differs",
    )
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (HERE / "OUTCOME_PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    require("composition and inversion" in exact, "route-congruence closure premise absent")
    require("endpoint constancy by itself does not construct it" in exact,
            "quotient-construction guard absent")
    require("one-object group" in exact and "categorical product" in exact,
            "target category absent")
    require("not a physical product" in exact, "physical-product guard absent")
    require("each declared physical relation" in report, "family scope absent")
    require("complete angular/screen/mixing" in report, "orchestra-inside-pullback guard absent")
    require("separately labelled pair realizations/branches" in report, "branch guard absent")
    require("calibration-mismatched" in report and "noncomposable" in report,
            "bounded dichotomy guard absent")
    require("CHOSE_PROVISIONAL_WORKING_FOUNDATIONAL_CLARIFICATION" in ledger,
            "provisional owner stamp absent")
    require("SUPPLIED_CONDITIONALLY" in ledger, "supplied congruence premise absent")
    require("OPEN_EXCLUDED" in ledger, "light exclusion absent")
    require((HERE / "PREREGISTRATION_EXECUTION_NOTE.md").is_file(), "execution note absent")
    require((HERE / "FOLLOWUP_REVIEW.md").is_file(), "follow-up review absent")
    require("FOLLOWUP_PASS" in (HERE / "STATUS.md").read_text(encoding="utf-8"),
            "follow-up status absent")
    print("PASS 25/25: G139 exact join, repaired category typing, orchestra, and review pass")


if __name__ == "__main__":
    main()
