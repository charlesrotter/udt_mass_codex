#!/usr/bin/env python3
"""Fail-closed package verification for G136."""

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
    production_stdout = run("derive_constitution.py")
    independent_stdout = run("verify_constitution_independent.py")
    production = json.loads(production_stdout)
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    require(production == saved, "saved derivation output differs from executable result")
    require(production["checks_passed"] == production["checks_total"] == 20, "production count")
    require("PASS 30/30" in independent_stdout, "independent replay count")
    require(
        (HERE / "INDEPENDENT_VERIFICATION.txt").read_text(encoding="utf-8").strip()
        == independent_stdout.strip(),
        "saved independent output differs",
    )

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS.md").read_text(encoding="utf-8")
    for token in (
        "F(phi)=tanh(k phi)",
        "F'(0)=1",
        "constitutive clarification",
        "390123/25975936",
        "XMAX_VALUE_PROPER_LENGTH_PAIR_REALIZATION_AND_HISTORY_OPEN",
    ):
        require(token in report, f"report token absent: {token}")
    require("The proof begins with the requirement" in exact, "circularity boundary absent")
    require("FRESH_ADVERSARIAL_FOLLOWUP_PASS" in status, "fresh-review follow-up state absent")
    require("neither `c_E` nor the existing `phi` convention removes it" in report,
            "normalization ownership repair absent")
    require("does not name `tanh`" in report, "minimal noncircular premise repair absent")
    require((HERE / "FOLLOWUP_REVIEW.md").is_file(), "follow-up review record absent")
    require("No canonization follows" in (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8"),
            "canon boundary absent")
    print("PASS 14/14: G136 executable outputs, classifications, ownership boundary, and caveats")


if __name__ == "__main__":
    main()
