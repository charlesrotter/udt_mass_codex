#!/usr/bin/env python3
"""Fail-closed verifier for G141."""

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
    production = json.loads(run("derive_endpoint_transition.py"))
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = run("verify_endpoint_transition_independent.py")
    require(production == saved, "saved production result differs")
    require(production["checks_passed"] == production["checks_total"] == 65, "production count")
    require("PASS 40/40" in independent, "independent count")
    require(independent == (HERE / "INDEPENDENT_VERIFICATION.txt").read_text(encoding="utf-8").strip(),
            "saved independent output differs")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (HERE / "OUTCOME_PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    execution = (HERE / "PREREGISTRATION_EXECUTION_NOTE.md").read_text(encoding="utf-8")
    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    repair = (HERE / "REPAIR_ADJUDICATION.md").read_text(encoding="utf-8")
    followup = (HERE / "FOLLOWUP_REVIEW.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    words = " ".join((exact + "\n" + report).split())
    require("C_{BA}=R_BR_A^{-1}" in exact, "calibration transition absent")
    require("delta_{AB}" in exact and "Phi_B-\\Phi_A" in exact, "endpoint difference absent")
    require("C_{CB}C_{BA}=C_{CA}" in exact, "composition absent")
    require("C_{AB}=C_{BA}^{-1}" in exact, "reversal absent")
    require("phi_{\\rm pair}(h_{B|A}^{\\rm rel})" in exact, "relative terminal identity absent")
    require("q_{AB}=e^{-2\\delta_{AB}}=\\frac{q_B}{q_A}" in exact, "reciprocal ratio absent")
    require("full `GL(4)`" in exact and "positive upper-triangular" in words,
            "full-GL no-go boundary absent")
    require("Neither two-dimensional map is identified" in words, "full-chart type guard absent")
    require("within a supplied compatible regular calibrated endpoint family" in words,
            "conditional-family ceiling absent")
    require("G141 does not overturn that result" in exact, "G140 preservation absent")
    require("OPEN_SUPPLIED" in ledger and "arbitrary strip terminal scalar called ordered depth" in ledger,
            "premise ledger family/sign guard absent")
    require("produced no outcome before being stopped" in execution,
            "execution refactor disclosure absent")
    require(production["metric"]["det_E"] == "5" and production["metric"]["det_g"] == "-25",
            "all-instruments metric witness absent")
    require("pair_carrier_matching_map_composes" in production["checks"] and
            "relative_terminal_readout_is_grading_squared" in production["checks"],
            "load-bearing production checks absent")
    require("REPAIR_REQUIRED__ALGEBRAIC_LANDING_SURVIVES" in review,
            "fresh adversarial verdict absent")
    require("All nine fresh-review requirements were accepted" in repair,
            "repair adjudication absent")
    require(all(f"ambient_pair_planes_distinct_{pair}" in production["checks"]
                for pair in ("BA", "CB", "CA")), "distinct-plane guards absent")
    require(all(f"witness_sensitive_to_{channel}" in production["checks"] for channel in
                ("base_shift", "screen_shear", "mixing", "angular_embedding")),
            "channel-sensitivity guards absent")
    require("matched endpoint carry" in words and "arbitrary `GL(2)`" in exact,
            "endpoint-gauge guard absent")
    require("endpoint_phi_changes_under_independent_triangular_gauge" in production["checks"] and
            "nontrivial_transition_not_recovered_from_equal_metrics" in production["checks"],
            "gauge/counterexample algebra guards absent")
    require("Physical inverse/query ownership remains `OPEN`" in words and
            "PHYSICAL_INVERSE_QUERY_IDENTIFICATION_OPEN" in report and
            "does **not** yet prove" in lay, "physical-inverse ownership guard absent")
    allowed_controls = {9, 10, 13}
    package_files = [path for path in HERE.iterdir() if path.is_file()]
    require(not any(byte < 32 and byte not in allowed_controls
                    for path in package_files for byte in path.read_bytes()),
            "unexpected control byte in package")
    require("FOLLOWUP_PASS" in followup and
            "VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_FOLLOWUP_PASS" in report,
            "repair-only follow-up pass absent")
    print("PASS 29/29: G141 calibration transition, grading, type, gauge, and evidence guards")


if __name__ == "__main__":
    main()
