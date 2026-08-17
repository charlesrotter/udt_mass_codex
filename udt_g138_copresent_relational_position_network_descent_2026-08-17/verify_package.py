#!/usr/bin/env python3
"""Fail-closed verifier for G138."""

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
    return result.stdout


def main() -> None:
    produced = json.loads(run("derive_network_descent.py"))
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = run("verify_network_descent_independent.py").strip()
    require(produced == saved, "saved production result differs from executable output")
    require(produced["checks_passed"] == produced["checks_total"] == 22, "production count")
    require("PASS 3159/3159" in independent, "independent replay count")
    require(
        independent == (HERE / "INDEPENDENT_VERIFICATION.txt").read_text(encoding="utf-8").strip(),
        "saved independent output differs",
    )
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "OUTCOME_PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    status = (HERE / "STATUS.md").read_text(encoding="utf-8")
    require("arbitrary reference depth" in report, "full gauge-torsor scope absent")
    require("select no coordinate root" in report, "coordinate-root boundary absent")
    require("do not prohibit a physical graph" in report, "physical-center overclaim guard absent")
    require("not automatically a physical failure" in report, "holonomy fork absent")
    require("does not select edge values" in exact, "network-value boundary absent")
    require("X_max\tNOT_SELECTED_BY_NETWORK_DESCENT" in ledger, "Xmax boundary absent")
    require("full_metric_network\tOPEN" in ledger, "full-metric boundary absent")
    require((HERE / "PREREGISTRATION_EXECUTION_NOTE.md").is_file(), "numerical correction note absent")
    require("FRESH_ADVERSARIAL_FOLLOWUP_PASS" in status, "review follow-up state absent")
    require((HERE / "FOLLOWUP_REVIEW.md").is_file(), "follow-up review record absent")
    print("PASS 16/16: G138 outputs, descent theorem, repaired torsor, holonomy, and review pass")


if __name__ == "__main__":
    main()
