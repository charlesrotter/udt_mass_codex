#!/usr/bin/env python3
"""Fail-closed semantic and mutation verification."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(gate: list[dict[str, str]], hierarchy: list[dict[str, str]], result: dict[str, object]) -> None:
    assert [row["candidate_id"] for row in gate] == [f"G{i:02d}" for i in range(1, 13)]
    assert len(hierarchy) == 6
    by_id = {row["candidate_id"]: row for row in gate}
    assert by_id["G07"]["ruling"] == "NATURAL_PARAMETRIC_LOCAL_JOIN_FIBER_SCHEMA"
    assert by_id["G07"]["same_configuration_reidentification"] == "SCHEMA_ONLY_NO_COMPLETE_METRIC_WITNESS"
    assert by_id["G08"]["ruling"] == "NATURAL_PARTIAL_CAP_JET_FIBER_CONDITIONAL_FAMILY"
    assert "CONDITIONAL" in by_id["G08"]["registered_datum"]
    assert by_id["G09"]["ruling"] == "NATURAL_PARAMETRIC_JET_MATCHING_SCHEMA_PHYSICAL_SEAM_OPEN"
    assert by_id["G09"]["same_configuration_reidentification"] == "SCHEMA_IF_FULL_TRANSITION_SUPPLIED"
    assert by_id["G01"]["ruling"] == "FORWARD_LOCAL_READOUT_NOT_RETURN"
    assert by_id["G02"]["premise_firewall"] == "FAIL_IF_LEVEL_ADOPTED"
    assert by_id["G04"]["premise_firewall"] == "FAIL_IF_PROMOTED"
    assert by_id["G05"]["ruling"] == "CONDITIONAL_TRANSPORT_FIBER_NOT_CONFIGURATION_ADMISSIBILITY"
    assert by_id["G12"]["ruling"] == "NO_CURRENT_SELECTOR_OR_BOOTSTRAP_RETURN"
    assert hierarchy[-1]["status"] == "OPEN" and hierarchy[-1]["selection"] == "OPEN"
    assert result["status"] == "PASS"
    assert result["curvature_native_return_routes"] == 0
    assert result["physical_completion_selectors"] == 0
    assert result["parametric_fiber_schema_routes"] == ["G07", "G09"]
    assert result["conditional_completed_family_fiber_route"] == "G08"
    assert result["outcome"] == "COMPLETION_DATA_SUPPLY_PARAMETRIC_LOCAL_FIBER_SCHEMAS_AND_ONE_CONDITIONAL_CAP_REALIZATION__CURVATURE_RETURN_AND_PHYSICAL_SELECTION_OPEN"


def main() -> int:
    gate, hierarchy = rows("GLOBAL_DATA_FIBER_GATE_MATRIX.tsv"), rows("FIBER_OWNERSHIP_LEDGER.tsv")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    validate(gate, hierarchy, result)
    mutations = []
    for index in range(12):
        changed = deepcopy(gate); changed[index]["candidate_id"] = "G99"; mutations.append((changed, deepcopy(hierarchy), deepcopy(result)))
    for candidate, field, value in (("G07", "ruling", "REALIZED_COMPLETE_FAMILY"), ("G07", "same_configuration_reidentification", "YES_COMPLETE"), ("G08", "registered_datum", "DERIVED_NATIVE"), ("G09", "ruling", "PHYSICAL_SEAM_SELECTED"), ("G01", "ruling", "CURVATURE_RETURN"), ("G02", "premise_firewall", "PASS"), ("G04", "premise_firewall", "PASS"), ("G05", "ruling", "CONFIGURATION_ADMISSIBILITY"), ("G12", "ruling", "SELECTOR_DERIVED")):
        changed = deepcopy(gate); next(row for row in changed if row["candidate_id"] == candidate)[field] = value; mutations.append((changed, deepcopy(hierarchy), deepcopy(result)))
    for field, value in (("curvature_native_return_routes", 1), ("physical_completion_selectors", 1), ("conditional_completed_family_fiber_route", "G07"), ("outcome", "BOOTSTRAP_DERIVED")):
        changed = deepcopy(result); changed[field] = value; mutations.append((deepcopy(gate), deepcopy(hierarchy), changed))
    changed_hierarchy = deepcopy(hierarchy); changed_hierarchy[-1]["status"] = "DERIVED"; mutations.append((deepcopy(gate), changed_hierarchy, deepcopy(result)))
    catches = 0
    for args in mutations:
        try:
            validate(*args)
        except AssertionError:
            catches += 1
    assert catches == len(mutations) == 26
    output = {"schema": "udt.completion_parameterized_local_fiber.verification.v1", "status": "PASS", "candidate_rows": len(gate), "mutation_catches": catches, "parametric_schema_routes": 2, "conditional_realized_routes": 1, "curvature_native_return_routes": 0, "physical_selectors": 0}
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
