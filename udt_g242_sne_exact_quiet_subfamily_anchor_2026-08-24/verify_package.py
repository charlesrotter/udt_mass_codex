#!/usr/bin/env python3
"""Package-level replay and cross-route verification for G242."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
PRODUCTION_PATH = PACKAGE / "DERIVATION_RESULT.json"
INDEPENDENT_PATH = PACKAGE / "INDEPENDENT_VERIFICATION.json"
CATCH_PATH = PACKAGE / "CATCH_PROOF_RESULT.json"
OUTPUT_PATH = PACKAGE / "VERIFICATION_RESULT.json"
EXPECTED = "EXACT_QUIET_SUBFAMILY_INCOMPATIBLE__SMALL_NONZERO_RESPONSE_REMAINS_OPEN"


def replay(script: str) -> dict[str, object]:
    process = subprocess.run(
        [sys.executable, str(PACKAGE / script), "--no-write"],
        cwd=PACKAGE.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(process.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    saved_production = json.loads(PRODUCTION_PATH.read_text(encoding="utf-8"))
    saved_independent = json.loads(INDEPENDENT_PATH.read_text(encoding="utf-8"))
    saved_catches = json.loads(CATCH_PATH.read_text(encoding="utf-8"))
    replay_production = replay("derive_exact_quiet_anchor.py")
    replay_independent = replay("verify_exact_quiet_anchor_independent.py")
    replay_catches = replay("run_catch_proofs.py")

    checks = {
        "saved_classification": saved_production["classification"] == EXPECTED,
        "independent_classification": saved_independent["classification"] == EXPECTED,
        "production_replay_exact": replay_production == saved_production,
        "independent_replay_exact": replay_independent == saved_independent,
        "catch_replay_exact": replay_catches == saved_catches,
        "cross_route_chi2": abs(float(saved_production["chi2"]) - float(saved_independent["chi2"])) < 1.0e-10,
        "cross_route_ceiling": abs(
            float(saved_production["chi2_ceiling_0p999"]) - float(saved_independent["chi2_ceiling_0p999"])
        ) < 1.0e-12,
        "cross_route_prediction": max(
            abs(float(left) - float(right))
            for left, right in zip(saved_production["predicted_theta"], saved_independent["predicted_theta"])
        ) < 1.0e-12,
        "zero_tide_production": float(saved_production["maximum_abs_J"]) <= 1.0e-10,
        "zero_tide_independent": float(saved_independent["maximum_abs_J"]) <= 1.0e-60,
        "boss_closed": (
            saved_production["boss_outcomes"] == "CLOSED_AND_UNREAD"
            and saved_independent["boss_outcomes"] == "CLOSED_AND_UNREAD"
        ),
        "hostile_catches": saved_catches["status"] == "PASS" and all(saved_catches["checks"].values()),
    }
    if not all(checks.values()):
        raise RuntimeError(f"package verification failure: {checks}")
    result = {
        "status": "PASS",
        "classification": EXPECTED,
        "checks": checks,
        "production_chi2": saved_production["chi2"],
        "independent_chi2": saved_independent["chi2"],
        "ceiling": saved_production["chi2_ceiling_0p999"],
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT_PATH.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
