#!/usr/bin/env python3
"""Package replay and cross-route checks for G246."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "VERIFICATION_RESULT.json"
EXPECTED = (
    "METRIC_AND_TWO_OBSERVER_GERMS_OWN_LOCAL_REGULAR_NULL_INCIDENCE_BRANCHES"
    "__EACH_BRANCH_OWNS_G222_COMPLETED_PAIR_RIBBON"
    "__MATHEMATICAL_REVERSAL_DIFFERS_FROM_PHYSICAL_FUTURE_RETURN"
    "__GLOBAL_BRANCH_SELECTION_AND_PHYSICAL_HISTORY_REMAIN_OPEN"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def replay(script: str) -> dict[str, object]:
    process = subprocess.run(
        [sys.executable, str(PACKAGE / script), "--no-write"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(process.stdout)


def verify_sources() -> int:
    lines = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    if lines[0] != "sha256\tpath\trole":
        raise RuntimeError("invalid source manifest header")
    checked = 0
    for line in lines[1:]:
        expected, relative, _role = line.split("\t")
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"source hash mismatch: {relative}")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    source_count = verify_sources()
    saved_production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    saved_independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    saved_catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    replay_production = replay("derive_two_observer_null_incidence.py")
    replay_independent = replay("verify_two_observer_null_incidence_independent.py")
    replay_catches = replay("run_catch_proofs.py")
    checks = {
        "source_manifest": source_count == 8,
        "production_classification": saved_production["classification"] == EXPECTED,
        "independent_classification": saved_independent["classification"] == EXPECTED,
        "production_replay_exact": replay_production == saved_production,
        "independent_replay_exact": replay_independent == saved_independent,
        "catch_replay_exact": replay_catches == saved_catches,
        "cross_route_local_incidence": (
            saved_production["local_theorem"]["cone_worldline_transverse"] is True
            and saved_independent["local_incidence"]["cone_worldline_transverse"] is True
            and saved_production["local_theorem"]["separate_null_sheet_required"] is False
            and saved_independent["local_incidence"]["separate_null_sheet_required"] is False
        ),
        "cross_route_pair_ribbon": (
            saved_production["pair_ribbon"]["determinant"]
            == saved_independent["pair_ribbon"]["determinant"]
            == "-a^2"
        ),
        "cross_route_reversal_return": (
            saved_production["reversal"]["generic_inverse_equals_return"] is False
            and saved_independent["reversal"]["physical_return_generically_distinct"] is True
        ),
        "cone_cone_not_transverse": (
            saved_production["cone_cone_intersection"]["direct_null_pair_transverse"] is False
            and saved_independent["cone_cone_direct_transverse"] is False
        ),
        "multiple_branch_no_selection": (
            saved_production["cylinder_multiple_branch_control"]["branch_count_in_registered_window"] > 1
            and saved_independent["cylinder_control"]["branch_count"] > 1
            and saved_production["cylinder_multiple_branch_control"]["preferred_branch_selected"] is False
            and saved_independent["cylinder_control"]["preferred_branch_selected"] is False
        ),
        "no_fit_or_outcome": (
            saved_production["fitted_coefficients"] == saved_independent["fitted_coefficients"] == 0
            and saved_production["observational_outcomes"]
            == saved_independent["observational_outcomes"]
            == "CLOSED_AND_UNREAD"
        ),
        "history_and_query_not_selected": (
            saved_production["physical_history"]
            == saved_independent["physical_history"]
            == "QUERY_SUPPLIED_NOT_SELECTED"
            and saved_production["universal_query_type_selected"] is False
            and saved_independent["universal_query_type_selected"] is False
        ),
        "hostile_catches": saved_catches["status"] == "PASS" and all(saved_catches["checks"].values()),
    }
    if not all(checks.values()):
        raise RuntimeError(f"G246 package failure: {checks}")
    result = {
        "status": "PASS",
        "classification": EXPECTED,
        "source_count": source_count,
        "checks": checks,
        "production_cases": saved_production["finite_census"]["cases"],
        "production_assertions": saved_production["finite_census"]["assertions"],
        "independent_cases": saved_independent["finite_census"]["cases"],
        "independent_assertions": saved_independent["finite_census"]["assertions"],
        "hostile_catches": saved_catches["caught"],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
