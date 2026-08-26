#!/usr/bin/env python3
"""Run G271 production mutations and typed conclusion catches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"
MUTATIONS = (
    "flip_connection_sign",
    "drop_lapse_factor",
    "flip_screen_orientation",
    "omit_frequency",
    "force_w_zero",
    "wrong_depth_sign",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    caught: dict[str, list[str]] = {}
    for mutation in MUTATIONS:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "derive_first_jet_interlock.py"), "--mutation", mutation],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        payload = json.loads(completed.stdout)
        assert payload["status"] == "MUTATION_CAUGHT", mutation
        assert payload["failed_checks"], mutation
        caught[mutation] = payload["failed_checks"]

    preregistration = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")
    typed_catches = {
        "finite_path_blocked": "No finite-path uniqueness may be inferred" in preregistration,
        "history_blocked": "select `phi(r)`" in preregistration,
        "distance_blocked": "derive distance or" in preregistration,
        "xmax_blocked": "`X_max`" in preregistration,
        "observations_blocked": "fit observations" in preregistration,
        "population_blocked": "populate observers or branches" in preregistration,
    }
    assert all(typed_catches.values()), typed_catches

    result = {
        "status": "PASS",
        "implementation_mutations": caught,
        "implementation_mutations_caught": len(caught),
        "typed_conclusion_catches": typed_catches,
        "typed_conclusion_catches_passed": sum(typed_catches.values()),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
