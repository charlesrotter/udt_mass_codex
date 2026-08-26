#!/usr/bin/env python3
"""Run G272 formula mutations and typed scope-regression catches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"
MUTATIONS = (
    "drop_screen_term",
    "flip_screen_sign",
    "wrong_reverse_screen",
    "force_signed_eta",
    "claim_chi_complete",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    caught: dict[str, list[str]] = {}
    for mutation in MUTATIONS:
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "derive_complete_relation_rapidity.py"),
                "--mutation",
                mutation,
            ],
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
        "screen_state_retained": "complete nonradial metric relation" in derivation,
        "planar_only_qualified": "exact one-dimensional relation-space profile" in derivation,
        "distance_attachment_conditional": "CONDITIONAL_DISTANCE_ATTACHMENT" in derivation,
        "local_velocity_not_promoted": "not automatically a local signal velocity" in derivation,
        "ce_scale_limit_stated": "does not alone attach the missing length" in derivation,
        "history_xmax_open": "complete history; and `X_max` realization" in derivation,
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
