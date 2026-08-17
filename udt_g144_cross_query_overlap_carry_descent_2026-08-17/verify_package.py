#!/usr/bin/env python3
"""Fail-closed verifier for G144."""

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
    production = json.loads(run("derive_cross_query_overlap.py"))
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = run("verify_cross_query_overlap_independent.py")
    require(production == saved, "saved production result differs")
    require(production["checks_passed"] == production["checks_total"], "production count mismatch")
    require(independent == (HERE / "INDEPENDENT_VERIFICATION.txt").read_text(encoding="utf-8").strip(),
            "saved independent output differs")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ownership = (HERE / "OWNERSHIP_ADJUDICATION.tsv").read_text(encoding="utf-8")
    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS.md").read_text(encoding="utf-8")
    require("F_\\beta\\circ\\psi_{\\beta\\alpha}=F_\\alpha" in exact,
            "overlap criterion absent")
    require("O(1,1)\\cap B^+(2)=\\{I\\}" in exact, "Bplus Lorentz intersection absent")
    require("image_intersection_only_on_boundaries_in_strip_coordinate" in production["checks"],
            "endpoint-only countermodel absent")
    require("overlap_total_is_Lorentz_isometric" in production["checks"],
            "overlap isometry check absent")
    require("endpoint_incidence" in ownership and "INSUFFICIENT_COUNTERMODEL" in ownership,
            "endpoint-incidence ownership guard absent")
    require("does not select pair sheets" in report, "physical-selection ceiling absent")
    require("Verdict: `PASS`" in review and "22/22" in review and "53/53" in review,
            "fresh adversarial pass absent")
    require("VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS" in status,
            "final bounded grade absent")
    allowed_controls = {9, 10, 13}
    require(not any(byte < 32 and byte not in allowed_controls
                    for path in HERE.iterdir() if path.is_file() for byte in path.read_bytes()),
            "unexpected control byte")
    print(f"PASS {len(CHECKS)}/{len(CHECKS)}: G144 overlap descent, isometry, and endpoint countermodel guards")


if __name__ == "__main__":
    main()
