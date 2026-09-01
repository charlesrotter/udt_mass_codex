#!/usr/bin/env python3
"""Hostile semantic mutation harness for the preregistered G314 claims."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
LANDING = (
    "GLOBAL_ADMISSIBILITY_AND_ACTUALIZATION_ARE_DISTINCT_MISSING_TYPES"
    "__CURRENT_STRUCTURE_SUPPLIES_NEITHER"
)


def defects(claims: dict[str, object]) -> list[str]:
    found: list[str] = []
    false_guards = (
        "reconstruction_is_selection",
        "nonidentity_implies_unique",
        "admissibility_equals_actualization",
        "maximal_symmetry_owned",
        "weyl_flatness_owned",
        "topology_owned",
        "scale_owned",
        "berger_is_complete_history",
        "witnesses_exhaust_full_solution_space",
        "global_selector_changes_local_response",
        "observation_is_native_selector",
        "xmax_is_selector_input",
        "fixed_point_syntax_is_sufficient",
        "current_owns_nonidentity_admissibility",
        "current_owns_actualization",
    )
    for guard in false_guards:
        if claims.get(guard) is not False:
            found.append(guard)
    if claims.get("landing") != LANDING:
        found.append("landing_changed")
    if claims.get("scope") != "REGISTERED_TYPES_AND_WITNESSES_ONLY":
        found.append("scope_promoted")
    return sorted(found)


def main() -> None:
    baseline = {
        "landing": LANDING,
        "scope": "REGISTERED_TYPES_AND_WITNESSES_ONLY",
        "reconstruction_is_selection": False,
        "nonidentity_implies_unique": False,
        "admissibility_equals_actualization": False,
        "maximal_symmetry_owned": False,
        "weyl_flatness_owned": False,
        "topology_owned": False,
        "scale_owned": False,
        "berger_is_complete_history": False,
        "witnesses_exhaust_full_solution_space": False,
        "global_selector_changes_local_response": False,
        "observation_is_native_selector": False,
        "xmax_is_selector_input": False,
        "fixed_point_syntax_is_sufficient": False,
        "current_owns_nonidentity_admissibility": False,
        "current_owns_actualization": False,
    }
    if defects(baseline):
        raise AssertionError(f"baseline defects: {defects(baseline)}")
    mutations = [(key, True) for key in baseline if isinstance(baseline[key], bool)]
    mutations.extend((
        ("landing", "ONE_OWNED_PREDICATE_SELECTS_A_UNIQUE_HISTORY_CLASS"),
        ("scope", "ALL_CONCEIVABLE_GLOBAL_MATHEMATICS"),
    ))
    rows = []
    for key, value in mutations:
        mutated = deepcopy(baseline)
        mutated[key] = value
        observed = defects(mutated)
        caught = key in observed or (key == "landing" and "landing_changed" in observed) or (
            key == "scope" and "scope_promoted" in observed
        )
        rows.append({"mutation": key, "caught": caught, "observed_defects": observed})
        if not caught:
            raise AssertionError(f"mutation escaped: {key}")
    result = {
        "status": "PASS",
        "baseline_clean": True,
        "mutations_registered": len(rows),
        "mutations_caught": sum(int(row["caught"]) for row in rows),
        "rows": rows,
    }
    (PACKAGE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
