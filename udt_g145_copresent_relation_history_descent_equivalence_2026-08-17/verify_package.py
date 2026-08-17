#!/usr/bin/env python3
"""Fail-closed package verifier for G145 before and after fresh review."""

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


def run(name: str) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(HERE / name), "--no-write"], cwd=HERE.parent,
        text=True, capture_output=True, check=False,
    )
    require(result.returncode == 0, result.stdout + result.stderr)
    return json.loads(result.stdout)


def main() -> None:
    # Load immutable saved evidence first. Child recomputations run in no-write mode so comparison
    # cannot be made vacuous by refreshing the artifacts before they are read.
    saved_production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    saved_independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    production = run("derive_relation_history_equivalence.py")
    independent = run("verify_relation_history_independent.py")
    require(production == saved_production, "saved production result differs")
    require(independent == saved_independent, "saved independent result differs")
    require(production["checks_passed"] == 43 == production["checks_total"], "production count mismatch")
    require(independent["checks_passed"] == 23 == independent["checks_total"], "independent count mismatch")
    require(
        independent["curvature_method"] == "direct_fraction_christoffel_ricci_contraction",
        "independent curvature reconstruction absent",
    )
    require(independent["independently_live_complete_coframe_fields"] == 9,
            "independent nine-field liveness absent")
    require(production["six_plane_rank"] == 10, "rank-ten reconstruction absent")
    require(
        production["landing_candidate"] == "RELATION_NETWORK_EQUIVALENT_TO_HISTORY__VALUES_OPEN",
        "preregistered landing changed",
    )
    require(
        production["marked_curvatures"] == {"Phi_minus": "-4*a**2", "Phi_plus": "-4*a**2 + 4*b"},
        "marked curvature witnesses changed",
    )
    for label in (
        "endpoint_depth_triangle_closure",
        "signed_position_mobius_composition",
        "cech_pullback_metric_descent",
        "four_dimensional_base_chart_metric_descent",
        "dt_covector_strictly_timelike_for_positive_cE",
        "base_common_scale_live",
        "base_shift_live",
        "mixing_mu4_live",
        "cE_and_G_cannot_form_length_without_additional_dimensionful_datum",
    ):
        require(label in production["checks"], f"production guard absent: {label}")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    status = (HERE / "STATUS.md").read_text(encoding="utf-8")
    require("coherent rank-complete valued relation atlas" in exact, "descent theorem absent")
    require("query atlas" in exact and "not a derivation" in exact, "query ownership ceiling absent")
    require("Pair sheets alone do not form a four-dimensional" in exact, "base/pair overlap type guard absent")
    require(production["active_complete_coframe_fields"] == 9, "complete-coframe liveness count absent")
    require("every complete-coframe sector active" in exact, "active-orchestra robustness absent")
    require("Values open" in report or "values" in report, "value nonselection absent")
    require("FREE_AND_EXPLORED" in ledger and "CHOSE_PROVISIONAL" in ledger, "premise tags absent")

    review_path = HERE / "FRESH_ADVERSARIAL_REVIEW.md"
    if review_path.exists():
        review = review_path.read_text(encoding="utf-8")
        require("Verdict: `PASS`" in review, "fresh adversarial pass absent")
        require("VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS" in status, "final grade absent")
    else:
        require("PREREGISTERED__NOT_RUN" in status, "pre-review status changed prematurely")

    allowed_controls = {9, 10, 13}
    require(
        not any(
            byte < 32 and byte not in allowed_controls
            for path in HERE.iterdir() if path.is_file() for byte in path.read_bytes()
        ),
        "unexpected control byte",
    )
    print(f"PASS {len(CHECKS)}/{len(CHECKS)}: G145 relation/history coherence package guards")


if __name__ == "__main__":
    main()
