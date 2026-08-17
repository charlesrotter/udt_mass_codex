#!/usr/bin/env python3
"""Fail-closed verifier for G143."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHECKS: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)
    CHECKS.append(message)


def run(name: str) -> str:
    result = subprocess.run(
        [sys.executable, str(HERE / name)], cwd=HERE.parent, text=True,
        capture_output=True, check=False,
    )
    require(result.returncode == 0, result.stdout + result.stderr)
    return result.stdout.strip()


def main() -> None:
    production = json.loads(run("derive_single_pair_domain_carry.py"))
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = run("verify_domain_carry_independent.py")
    require(production == saved, "saved production result differs")
    require(production["checks_passed"] == production["checks_total"], "production count mismatch")
    require(independent == (HERE / "INDEPENDENT_VERIFICATION.txt").read_text(encoding="utf-8").strip(),
            "saved independent output differs")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ownership = (HERE / "OWNERSHIP_ADJUDICATION.tsv").read_text(encoding="utf-8")
    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS.md").read_text(encoding="utf-8")
    require("M_{BA}^{(y)}=I" in exact, "same-chart identity absent")
    require("M_{BA}^{(z)}=J_BJ_A^{-1}" in exact, "chart carry absent")
    require("C_{BA}^{(z)}" in exact and "C_{BA}^{(y)}" in exact,
            "total invariance derivation absent")
    require("same_query_carry_nonidentity_after_smooth_reparameterization" in production["checks"],
            "smooth nonidentity witness absent")
    require("smooth_strip_chart_regular_on_unit_strip" in production["checks"],
            "smooth chart regularity absent")
    require("OPEN" in ownership and "cross_query_carry" in ownership,
            "cross-query ownership boundary absent")
    require("not a universal path-independent" in report,
            "coordinate-free carry ceiling absent")
    require("Verdict: `PASS`" in review and "24/24" in review and "28/28" in review,
            "fresh adversarial pass absent")
    require("VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS" in status,
            "final bounded grade absent")
    allowed_controls = {9, 10, 13}
    require(not any(byte < 32 and byte not in allowed_controls
                    for path in HERE.iterdir() if path.is_file() for byte in path.read_bytes()),
            "unexpected control byte")
    print(f"PASS {len(CHECKS)}/{len(CHECKS)}: G143 same-query carry, covariance, and ownership guards")


if __name__ == "__main__":
    main()
