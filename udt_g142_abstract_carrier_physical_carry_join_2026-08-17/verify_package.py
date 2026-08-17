#!/usr/bin/env python3
"""Fail-closed package verifier for G142."""

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
    production = json.loads(run("derive_carrier_carry_join.py"))
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = run("verify_carrier_carry_independent.py")
    require(production == saved, "saved production result differs")
    require(production["checks_passed"] == production["checks_total"] == 28,
            "production count")
    require("PASS 41/41" in independent, "independent count")
    require(independent == (HERE / "INDEPENDENT_VERIFICATION.txt").read_text(encoding="utf-8").strip(),
            "saved independent output differs")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    ownership = (HERE / "OWNERSHIP_ADJUDICATION.tsv").read_text(encoding="utf-8")
    followup = (HERE / "FOLLOWUP_REVIEW.md").read_text(encoding="utf-8")
    status = (HERE / "STATUS.md").read_text(encoding="utf-8")
    words = " ".join((exact + "\n" + report + "\n" + lay).split())
    require("C_{BA}=R_BM_{BA}R_A^{-1}" in exact, "total transition absent")
    require("M_{BA}'=P_B^{-1}M_{BA}P_A" in exact and "C_{BA}'" in exact,
            "endpoint gauge law absent")
    require("\\chi(C_{BA})" in exact and "\\Phi_B-\\Phi_A+\\chi(M_{BA})" in exact,
            "grading decomposition absent")
    require("G141" in exact and "fixed matched" in words,
            "G141 reduction absent")
    require("identity carry alone recovers its full transition" in production["landing"]["G141_reduction"],
            "G141 full-transition boundary absent")
    require("composition_obstruction_exactly_carry_obstruction" in production["checks"],
            "composition iff guard absent")
    require("total_transition_endpoint_gauge_invariant" in production["checks"],
            "gauge invariant production guard absent")
    require("carry_grading_gauge_shift_exact" in production["checks"],
            "carry-grading gauge-shift guard absent")
    require("off_closure_red_case_has_nonzero_matched_obstructions" in production["checks"],
            "non-tautological off-closure guard absent")
    require("copresence_and_endpoint_metrics_do_not_select_carry" in production["checks"],
            "nonselection countermodel absent")
    require("FOUNDING_SUPPLIED_CHOSEN_TYPE" in ownership and "SUPPLIED_CONDITIONAL" in ownership,
            "ownership type separation absent")
    require("K" in ownership and "POSIT" in ownership and "c_E" in ownership,
            "founding premise stamps absent")
    require("does not make all such relations identical" in exact,
            "query-relative ceiling absent")
    require("does not derive a unique physical query" in exact,
            "physical ownership ceiling absent")
    require("COPRESENCE_ALONE_DOES_NOT_SELECT" in report,
            "copresence no-selection landing absent")
    require("FOLLOWUP_PASS" in followup and "28/28" in followup and "41/41" in followup,
            "fresh repair-only follow-up absent")
    require("VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS" in status,
            "final bounded grade absent")
    allowed_controls = {9, 10, 13}
    require(not any(byte < 32 and byte not in allowed_controls
                    for path in HERE.iterdir() if path.is_file() for byte in path.read_bytes()),
            "unexpected control byte in package")
    print(f"PASS {len(CHECKS)}/{len(CHECKS)}: G142 carrier/carry algebra, gauge, ownership, and evidence guards")


if __name__ == "__main__":
    main()
