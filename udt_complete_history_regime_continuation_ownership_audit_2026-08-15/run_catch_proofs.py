#!/usr/bin/env python3
"""Hostile in-memory mutations for the G98 ownership boundary."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def valid(rows: list[dict[str, str]], result: dict[str, object]) -> bool:
    by_id = {row["candidate_id"]: row for row in rows}
    required = {f"O{i:02d}" for i in range(1, 16)}
    return all(
        (
            set(by_id) == required,
            all(row["active_native_nonidentity_history_rule"] == "no" for row in rows),
            by_id["O04"]["mathematical_type"] == "integrability identity",
            by_id["O11"]["current_status"] == "CONDITIONAL_NOT_SELECTED",
            by_id["O12"]["current_status"] == "CONDITIONAL_INACTIVE",
            by_id["O14"]["mathematical_type"] == "after-the-fact observational test",
            result.get("landing") == "PERMITTED_NOT_OWNED",
            result.get("all_checks_pass") is True,
            len(result.get("families", [])) == 3,
            all(item.get("all_checks_pass") is True for item in result.get("families", [])),
        )
    )


def main() -> None:
    with (HERE / "CANDIDATE_OWNER_ATLAS.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    checks = {"baseline": valid(rows, result)}

    mutations = []
    r = copy.deepcopy(rows)
    next(row for row in r if row["candidate_id"] == "O04")["active_native_nonidentity_history_rule"] = "yes"
    mutations.append(("maurer_cartan_promoted_to_dynamics", r, result))
    r = copy.deepcopy(rows)
    next(row for row in r if row["candidate_id"] == "O11")["active_native_nonidentity_history_rule"] = "yes"
    mutations.append(("conditional_EH_promoted_to_native", r, result))
    r = copy.deepcopy(rows)
    next(row for row in r if row["candidate_id"] == "O14")["active_native_nonidentity_history_rule"] = "yes"
    mutations.append(("SNe_mismatch_promoted_to_native_owner", r, result))
    mutations.append(("candidate_omitted", copy.deepcopy(rows[:-1]), result))
    d = copy.deepcopy(result)
    d["landing"] = "SELECTED_CONTINUATION"
    mutations.append(("nonselection_promoted_to_unique_selection", rows, d))
    d = copy.deepcopy(result)
    d["families"][0]["all_checks_pass"] = False
    mutations.append(("flat_separating_witness_silently_dropped", rows, d))

    for name, mutated_rows, mutated_result in mutations:
        checks[f"catch:{name}"] = not valid(mutated_rows, mutated_result)

    payload = {
        "schema": "udt.complete_history_regime_continuation_catches.v1",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "all_checks_pass": all(checks.values()),
        "role": "semantic and package-scope guards; not independent mathematical evidence",
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if not payload["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
