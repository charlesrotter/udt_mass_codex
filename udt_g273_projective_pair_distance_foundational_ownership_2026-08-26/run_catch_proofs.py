#!/usr/bin/env python3
"""Mutation and typed-scope catches for G273."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"
MUTATIONS = (
    "drop_screen",
    "wrong_projective_sign",
    "claim_bounded_unique",
    "radial_only_complete",
    "wrong_reversal_screen",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    caught: dict[str, list[str]] = {}
    for mutation in MUTATIONS:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "derive_projective_distance_ownership.py"), "--mutation", mutation],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr
        payload = json.loads(completed.stdout)
        assert payload["status"] == "MUTATION_CAUGHT", payload
        assert payload["failed_checks"], payload
        caught[mutation] = payload["failed_checks"]

    derivation = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    typed_catches = {
        "strict_entailment_rejected": "STRICT_FOUNDING_ENTAILMENT is not proved" in derivation,
        "projective_uniqueness_scoped": "linear-fractional projective class" in derivation,
        "screen_state_retained": "complete open-ball vector" in derivation,
        "attachment_not_derived": "WORKING_FOUNDATIONAL_CLARIFICATION" in derivation,
        "scale_open": "dimensionful scale `X` remains open" in derivation,
        "history_xmax_open": "history, branch population, and `X_max` remain open" in derivation,
    }
    assert all(typed_catches.values()), typed_catches

    result = {
        "status": "PASS",
        "implementation_mutations": caught,
        "implementation_mutations_caught": len(caught),
        "typed_scope_catches": typed_catches,
        "typed_scope_catches_passed": sum(typed_catches.values()),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
