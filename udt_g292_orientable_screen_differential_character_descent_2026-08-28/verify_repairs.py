#!/usr/bin/env python3
"""Bounded verifier for the four preregistered G292 external-review repairs."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "REPAIR_VERIFICATION_RESULT.json"
LANDING = (
    "ORIENTABLE_SCREEN_EULER_FLUX_DESCENDS_EXACTLY"
    "__G225_SKY_AND_G290_PAIR_CONNECTIONS_REQUIRE_SUPPLIED_IDENTIFICATION"
    "__GLOBAL_SAME_PAIR_BLOCK_SAME_EULER_CLASS_DIFFERENT_LOCAL_FLUX_METRIC_FAMILY"
    "__NO_CONTINUOUS_FLUX_PROPAGATION_OR_HISTORY_SELECTION"
)


def require_token(filename: str, token: str) -> None:
    text = (HERE / filename).read_text(encoding="utf-8")
    if token not in text:
        raise AssertionError(f"{filename} lacks required repair token: {token}")


def main() -> None:
    no_sympy = subprocess.run(
        [sys.executable, "-S", str(HERE / "verify_package.py")],
        cwd=HERE,
        capture_output=True,
        text=True,
        check=False,
    )
    combined = no_sympy.stdout + no_sympy.stderr
    if no_sympy.returncode == 0 or "sympy is required" not in combined:
        raise AssertionError("R1 fail-closed no-sympy catch failed")

    require_token("RUN_RECORD.md", "PYTHONPYCACHEPREFIX")
    require_token("RUN_RECORD.md", "writable ephemeral")
    require_token("EXACT_DERIVATION.md", "abstract smooth orientable")
    require_token("EXACT_DERIVATION.md", "does not prove that every such")
    require_token("EXTERNAL_REVIEW_GPT54.md", "ACCEPT_WITH_REPAIRS")
    require_token("EVIDENCE_GATES.md", "PASS_ACCEPT_G292_REPAIRS")
    require_token("EXTERNAL_REPAIR_FOLLOWUP_GPT54.md", "ACCEPT_G292_REPAIRS")
    require_token("EXACT_DERIVATION.md", LANDING)

    package = json.loads((HERE / "PACKAGE_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    if package["status"] != "PASS" or package["landing"] != LANDING:
        raise AssertionError("repaired aggregate landing regressed")
    if not package["sympy_production_replayed"]:
        raise AssertionError("symbolic production did not replay")
    if not package["registered_repairs_applied"]:
        raise AssertionError("aggregate does not record applied repairs")
    if package["repair_followup"] != "PASS_ACCEPT_G292_REPAIRS":
        raise AssertionError("repair-only external follow-up is not closed")

    result = {
        "status": "PASS",
        "repairs_verified": ["R1", "R2", "R3", "R4"],
        "scientific_landing_unchanged": True,
        "landing": LANDING,
        "no_sympy_aggregate_returncode": no_sympy.returncode,
        "no_sympy_fail_closed": True,
        "symbolic_production_replayed": True,
        "fresh_external_verdict": "ACCEPT_WITH_REPAIRS",
        "repair_only_followup": "PASS_ACCEPT_G292_REPAIRS",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
