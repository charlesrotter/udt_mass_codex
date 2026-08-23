#!/usr/bin/env python3
"""Verify registered G233 evidence and optionally run no-write replays."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_json(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def validate_exact(data):
    require(data["all_checks_pass"] is True, "production aggregate failed")
    require(all(data["checks"].values()), "production registered check failed")
    require(
        data["metric_jet_nonzero_counts"] == {str(k): (0 if k < 5 else 2) for k in range(6)},
        "metric jet collision changed",
    )
    require(data["next_difference_b1_minus_b0"] == "240/r0**5", "symbolic separator changed")
    require(
        data["radial_values_orders_0_to_3"]
        == ["0", "12/r0**3", "24*(2*c - 1)/r0**4", "12*(20*b - 24*c + 1)/r0**5"],
        "radial scalar contractions changed",
    )
    expected = {
        "0": "12/r0**3",
        "1": "48/r0**4",
        "2": "240/r0**5",
        "3": "1440/r0**6",
        "4": "10080/r0**7",
        "5": "80640/r0**8",
        "6": "725760/r0**9",
    }
    for order, coefficient in expected.items():
        item = data["arbitrary_order_checks"][order]
        require(item["pass"] is True, f"arbitrary order {order} failed")
        require(item["coefficient"] == coefficient, f"arbitrary order {order} coefficient changed")
        require(item["expected"] == coefficient, f"arbitrary order {order} expected changed")
    require(data["g204"]["state"] == ["x", "amplitude", "scale", "n"], "G204 state changed")


def validate_independent(data):
    require(data["all_checks_pass"] is True, "independent aggregate failed")
    require(all(data["checks"].values()), "independent registered check failed")
    require(data["next_difference"] == "560/81", "independent separator changed")
    require(data["expected_difference"] == "560/81", "independent expectation changed")
    require(data["radial_values_first"][:3] == data["radial_values_second"][:3], "shared state changed")
    require(data["radial_values_first"][3] != data["radial_values_second"][3], "next state no longer differs")


def validate_initial_failure(data):
    require(data["all_checks_pass"] is False, "initial failure was erased")
    require(data["checks"]["radial_unit_field_geodesic"] is False, "initial failed guard changed")
    require(data["checks"]["nabla3_difference_matches_exact_coefficient"] is True, "load-bearing initial pass changed")


def verify_sources():
    lines = (ROOT / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    require(lines[0] == "sha256\tpath\trole", "source manifest header changed")
    count = 0
    for line in lines[1:]:
        expected, relative, _ = line.split("\t")
        payload = (REPO / relative).read_bytes()
        require(hashlib.sha256(payload).hexdigest() == expected, f"source hash changed: {relative}")
        count += 1
    require(count == 8, "source manifest count changed")


def replay(script_name):
    completed = subprocess.run(
        [sys.executable, str(ROOT / script_name), "--no-write"],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    require(completed.stderr == "", f"unexpected stderr from {script_name}")
    return json.loads(completed.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "package_verification.json")
    args = parser.parse_args()

    exact = load_json("exact_results.json")
    independent = load_json("independent_results.json")
    initial = load_json("INITIAL_INDEPENDENT_FAILURE.json")
    validate_exact(exact)
    validate_independent(independent)
    validate_initial_failure(initial)
    verify_sources()

    replay_checks = {}
    if args.replay:
        production_replay = replay("derive_primary_profile_cartan_closure.py")
        independent_replay = replay("verify_independent_series.py")
        validate_exact(production_replay)
        validate_independent(independent_replay)
        replay_checks = {
            "production_no_write_replay_matches": production_replay == exact,
            "independent_no_write_replay_matches": independent_replay == independent,
        }
        require(all(replay_checks.values()), "registered no-write replay changed")

    checks = {
        "production_evidence_valid": True,
        "independent_evidence_valid": True,
        "initial_failure_preserved": True,
        "source_hashes_valid": True,
        **replay_checks,
    }
    result = {"all_pass": all(checks.values()), "checks": checks}
    if not args.no_write:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
