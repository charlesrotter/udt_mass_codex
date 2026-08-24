#!/usr/bin/env python3
"""Package replay and cross-route checks for G245."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
EXPECTED = (
    "OBSERVER_GERM_AND_METRIC_OWN_LOCAL_DIRECTION_LABELLED_NULL_CONE_FIELD"
    "__G244_AREA_SHAPE_ARE_INDUCED_CONE_GEOMETRY"
    "__SOURCE_POPULATION_GLOBAL_BRANCH_AND_PHYSICAL_HISTORY_REMAIN_OPEN"
)
OUTPUT = PACKAGE / "VERIFICATION_RESULT.json"


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
        actual = sha256(ROOT / relative)
        if actual != expected:
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
    replay_production = replay("derive_metric_owned_null_cone.py")
    replay_independent = replay("verify_metric_owned_null_cone_independent.py")
    replay_catches = replay("run_catch_proofs.py")

    checks = {
        "source_manifest": source_count == 5,
        "production_classification": saved_production["classification"] == EXPECTED,
        "independent_classification": saved_independent["classification"] == EXPECTED,
        "production_replay_exact": replay_production == saved_production,
        "independent_replay_exact": replay_independent == saved_independent,
        "catch_replay_exact": replay_catches == saved_catches,
        "cross_route_rotating_D4": (
            saved_production["controls"]["rotating_tide_series"]["D4"]
            == saved_independent["controls"]["rotating_tide_series"]["D4"]
            == [["0", "-1/4"], ["-1/4", "0"]]
        ),
        "cross_route_nonclosure": (
            saved_production["symbolic"]["H_Hprime_nonclosure_witness"]["different"] is True
            and saved_independent["controls"]["H_Hprime_nonclosure"]["different"] is True
        ),
        "no_fit": (
            saved_production["fitted_angular_coefficients"]
            == saved_independent["fitted_angular_coefficients"]
            == 0
        ),
        "outcomes_closed": (
            saved_production["observational_outcomes"]
            == saved_independent["observational_outcomes"]
            == "CLOSED_AND_UNREAD"
        ),
        "history_not_selected": (
            saved_production["physical_history"]
            == saved_independent["physical_history"]
            == "QUERY_SUPPLIED_NOT_SELECTED"
        ),
        "no_preferred_ray_or_source": (
            saved_production["observer_cone"]["preferred_ray_selected"] is False
            and saved_production["observer_cone"]["source_population_required"] is False
        ),
        "caustic_phase_retained": (
            saved_production["controls"]["caustic"]["rank_D_at_pi"] == 1
            and saved_production["controls"]["caustic"]["full_phase_det"] == "1"
            and saved_independent["controls"]["rational_caustic_phase"]["full_phase_invertible"] is True
        ),
        "hostile_catches": saved_catches["status"] == "PASS" and all(saved_catches["checks"].values()),
    }
    if not all(checks.values()):
        raise RuntimeError(f"G245 package failure: {checks}")
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
