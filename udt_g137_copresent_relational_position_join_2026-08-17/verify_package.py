#!/usr/bin/env python3
"""Fail-closed verifier for G137."""

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
    produced = json.loads(run("derive_position_join.py"))
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = run("verify_position_join_independent.py").strip()
    require(produced == saved, "saved production result differs from executable output")
    require(produced["checks_passed"] == produced["checks_total"] == 21, "production count")
    require("PASS 37/37" in independent, "independent replay count")
    require(
        independent == (HERE / "INDEPENDENT_VERIFICATION.txt").read_text(encoding="utf-8").strip(),
        "saved independent output differs",
    )
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS.md").read_text(encoding="utf-8")
    require("CHOSE / WORKING_FOUNDATIONAL_CLARIFICATION" in report, "adoption stamp absent")
    require("Nonnegative separation cannot compose by itself" in report, "orientation boundary absent")
    require("same unsigned inputs" in exact, "unsigned-composition no-go absent")
    require("## What remains open" in report and "proper length" in report, "proper-length boundary absent")
    require("CANON.md` canonization" in prereg, "canon boundary absent")
    require("FRESH_ADVERSARIAL_PASS" in status, "review pass state absent")
    require((HERE / "FRESH_ADVERSARIAL_REVIEW.md").is_file(), "fresh review record absent")
    print("PASS 13/13: G137 executable outputs, typing, ownership boundaries, and review pass")


if __name__ == "__main__":
    main()
