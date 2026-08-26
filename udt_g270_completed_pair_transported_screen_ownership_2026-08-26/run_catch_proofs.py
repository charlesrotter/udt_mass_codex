#!/usr/bin/env python3
"""G270 production-implementation mutations and typed-ledger consistency catches."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"
PRODUCTION = ROOT / "derive_screen_ownership.py"


BASE_LEDGER = {
    "full_realization_evaluates_w": True,
    "w_channel": "endpoint_clock_transport_projection",
    "w_is_jacobi": False,
    "query_supplied": True,
    "history_selected": False,
}


def run_production(*extra: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(PRODUCTION), "--no-write", *extra],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def validate_ledger(candidate: dict[str, object]) -> list[str]:
    failures: list[str] = []
    if candidate["full_realization_evaluates_w"] is not True:
        failures.append("realization_evaluation")
    if candidate["w_channel"] != "endpoint_clock_transport_projection":
        failures.append("transported_mismatch_type")
    if candidate["w_is_jacobi"] is not False:
        failures.append("no_jacobi_conflation")
    if candidate["query_supplied"] is not True:
        failures.append("query_status")
    if candidate["history_selected"] is not False:
        failures.append("no_history_promotion")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    baseline = run_production()
    implementation_mutations = {
        "omit_tilt_from_gamma": "target_clock_unit",
        "flip_longitudinal_offset": "target_clock_unit",
        "drop_null_normalization": "target_null_clock_normalization",
        "inject_tilt_into_pullback": "intrinsic_pullback",
        "wrong_completion_density": "completed_metric",
        "reverse_frequency_ratio": "target_frequency",
        "zero_screen_projection": "screen_projection_norm",
        "drop_inverse_readout": "mutual_inverse_gamma",
    }
    implementation_results: dict[str, dict[str, object]] = {}
    for name, target in implementation_mutations.items():
        replay = run_production("--mutation", name)
        failures = replay["failed_checks"]
        implementation_results[name] = {
            "caught": replay["status"] == "MUTATION_CAUGHT",
            "targeted_caught": target in failures,
            "targeted_failure": target,
            "failures": failures,
            "production_implementation_exercised": True,
        }

    ledger_mutations = {
        "deny_realization_evaluation": (
            "full_realization_evaluates_w", False, "realization_evaluation"
        ),
        "rename_w_as_jacobi_area": (
            "w_channel", "jacobi_area", "transported_mismatch_type"
        ),
        "conflate_w_with_jacobi": ("w_is_jacobi", True, "no_jacobi_conflation"),
        "delete_query_supply": ("query_supplied", False, "query_status"),
        "promote_history": ("history_selected", True, "no_history_promotion"),
    }
    baseline_ledger = validate_ledger(BASE_LEDGER)
    ledger_results: dict[str, dict[str, object]] = {}
    for name, (key, value, target) in ledger_mutations.items():
        candidate = copy.deepcopy(BASE_LEDGER)
        candidate[key] = value
        failures = validate_ledger(candidate)
        ledger_results[name] = {
            "caught": bool(failures),
            "targeted_caught": target in failures,
            "targeted_failure": target,
            "failures": failures,
        }

    implementation_missed = [
        name for name, item in implementation_results.items() if not item["targeted_caught"]
    ]
    ledger_missed = [
        name for name, item in ledger_results.items() if not item["targeted_caught"]
    ]
    result = {
        "status": "PASS" if baseline["status"] == "PASS"
        and not baseline_ledger and not implementation_missed and not ledger_missed else "FAIL",
        "production_baseline": {
            "status": baseline["status"],
            "exact_checks": baseline["exact_checks"],
            "landing": baseline["landing"],
        },
        "baseline_ledger_failures": baseline_ledger,
        "implementation_mutations": implementation_results,
        "implementation_catches": sum(
            bool(item["targeted_caught"]) for item in implementation_results.values()
        ),
        "implementation_missed": implementation_missed,
        "ledger_mutations": ledger_results,
        "ledger_catches": sum(bool(item["targeted_caught"]) for item in ledger_results.values()),
        "ledger_missed": ledger_missed,
        "production_implementation_exercised": True,
        "ledger_validator_exercised": True,
    }
    assert result["status"] == "PASS", result
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
