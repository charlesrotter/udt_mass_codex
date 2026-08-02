#!/usr/bin/env python3
"""Fail-closed semantic verification and mutation tests for the interface audit."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(candidates: list[dict[str, str]], missing: list[dict[str, str]], result: dict[str, object]) -> None:
    assert len(candidates) == 8
    assert [row["candidate_id"] for row in candidates] == [f"C{i:02d}" for i in range(1, 9)]
    assert len(missing) == 9 and [row["slot"] for row in missing] == [f"M{i:02d}" for i in range(1, 10)]
    assert result["status"] == "PASS"
    assert result["passing_complete_intersections"] == 0
    assert result["outcome"] == "PROJECTOR_ANTECEDENT_ROBUST__BOOTSTRAP_INTERSECTION_OPEN_MISSING_E_NATIVE_R_AND_A"
    assert next(row for row in candidates if row["candidate_id"] == "C01")["ruling"] == "OFFSHELL_LOCAL_FILTER_NOT_BOOTSTRAP"
    assert next(row for row in candidates if row["candidate_id"] == "C03")["ruling"] == "WORKING_ONE_WAY_SURVIVAL_FILTER_TYPE"
    assert next(row for row in candidates if row["candidate_id"] == "C06")["premise_firewall"] == "FAIL_IF_PROMOTED"
    assert next(row for row in candidates if row["candidate_id"] == "C08")["ruling"] == "OPEN_MISSING_E_NATIVE_R_AND_A"
    status = {row["slot"]: row["status"] for row in missing}
    assert status["M01"] == "DERIVED_CONDITIONAL_BOUNDED"
    assert status["M03"] == status["M05"] == status["M06"] == status["M09"] == "OPEN"
    assert status["M04"] == "PARTIAL" and status["M07"] == "PARTIAL_CONSTRAINT"


def main() -> int:
    candidates = rows("INTERFACE_GATE_MATRIX.tsv")
    missing = rows("MISSING_INPUT_LEDGER.tsv")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    validate(candidates, missing, result)
    catches = 0

    mutations: list[tuple[list[dict[str, str]], list[dict[str, str]], dict[str, object]]] = []
    for index in range(8):
        changed = deepcopy(candidates)
        changed[index]["candidate_id"] = "C99"
        mutations.append((changed, deepcopy(missing), deepcopy(result)))
    for slot in ("M03", "M05", "M06", "M09"):
        changed = deepcopy(missing)
        next(row for row in changed if row["slot"] == slot)["status"] = "DERIVED"
        mutations.append((deepcopy(candidates), changed, deepcopy(result)))
    changed_result = deepcopy(result)
    changed_result["passing_complete_intersections"] = 1
    mutations.append((deepcopy(candidates), deepcopy(missing), changed_result))
    changed_result = deepcopy(result)
    changed_result["outcome"] = "BOOTSTRAP_DERIVED"
    mutations.append((deepcopy(candidates), deepcopy(missing), changed_result))
    changed = deepcopy(candidates)
    next(row for row in changed if row["candidate_id"] == "C03")["ruling"] = "TWO_WAY_BOOTSTRAP_DERIVED"
    mutations.append((changed, deepcopy(missing), deepcopy(result)))
    changed = deepcopy(candidates)
    next(row for row in changed if row["candidate_id"] == "C06")["premise_firewall"] = "PASS"
    mutations.append((changed, deepcopy(missing), deepcopy(result)))

    for candidate_rows, missing_rows, result_row in mutations:
        try:
            validate(candidate_rows, missing_rows, result_row)
        except AssertionError:
            catches += 1
    assert catches == len(mutations) == 16
    verification = {
        "schema": "udt.bootstrap_projector_admissibility_interface.verification.v1",
        "status": "PASS",
        "candidate_rows": len(candidates),
        "missing_slots": len(missing),
        "mutation_catches": catches,
        "complete_intersections": 0,
        "bootstrap_promoted": False,
        "projector_promoted_to_stability": False,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(verification, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
