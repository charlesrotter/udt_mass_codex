#!/usr/bin/env python3
"""Hostile semantic mutations for the load-bearing G238 package validator."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import verify_package


PACKAGE = Path(__file__).resolve().parent


def must_fail(name, state, result, ledger, sources_valid) -> dict[str, object]:
    try:
        verify_package.validate_payload(state, result, ledger, sources_valid)
    except (AssertionError, KeyError, TypeError):
        return {"mutation": name, "caught": True}
    return {"mutation": name, "caught": False}


def main() -> None:
    state, result, ledger, sources_valid = verify_package.load_actual()
    cases = []

    mutant = copy.deepcopy(state)
    mutant["resolution"] = 13
    cases.append(must_fail("resolution", mutant, result, ledger, sources_valid))

    mutant = copy.deepcopy(state)
    mutant["state"]["interpolation"] = "outcome_fitted"
    cases.append(must_fail("interpolation_insertion", mutant, result, ledger, sources_valid))

    mutant = copy.deepcopy(result)
    mutant["boss_outcomes_opened"] = True
    cases.append(must_fail("outcome_opening", state, mutant, ledger, sources_valid))

    mutant = copy.deepcopy(result)
    mutant["profile_or_feature_fit_performed"] = True
    cases.append(must_fail("feature_fit", state, mutant, ledger, sources_valid))

    mutant = copy.deepcopy(result)
    mutant["counterfamily"]["q_prime"]["numerator"] = 0
    cases.append(must_fail("counterfamily_derivative", state, mutant, ledger, sources_valid))

    mutant = copy.deepcopy(ledger)
    next(row for row in mutant if row["stage"] == "Q02")["status"] = "DERIVED"
    cases.append(must_fail("interpolation_ownership_promotion", state, result, mutant, sources_valid))

    mutant = copy.deepcopy(ledger)
    next(row for row in mutant if row["stage"] == "Q10")["status"] = "DERIVED"
    cases.append(must_fail("source_measure_promotion", state, result, mutant, sources_valid))

    cases.append(must_fail("source_hash_failure", state, result, ledger, False))

    if not all(case["caught"] for case in cases):
        raise SystemExit("one or more hostile mutations escaped")
    output = {"audit": "G238_CATCH_PROOFS", "status": "PASS", "cases": cases}
    (PACKAGE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
