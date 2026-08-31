#!/usr/bin/env python3
"""Hostile semantic/evidence mutations for the bounded G307 result."""

from __future__ import annotations

import copy
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "DERIVATION_RESULT.json"
OUT = HERE / "CATCH_PROOF_RESULT.json"


def failure(value):
    if value["metric_and_kernel_changed"]:
        return "kernel_change"
    if value["directed_germ_member_count"] != 2:
        return "directed_count"
    if value["members_per_chirality"] != 1:
        return "per_chirality_uniqueness"
    if value["path_only_member_count"] != 2:
        return "path_nonselection"
    if value["signed_transverse_screen_member_count"] != 1:
        return "signed_screen_uniqueness"
    if value["screen_twist_signs"] != [-1, 1]:
        return "opposite_twist"
    if value["lawful_query_population_selected"]:
        return "query_population_promotion"
    if value["physical_member_selected"]:
        return "physical_member_promotion"
    required = {"mass", "scale", "physical_Xmax", "protected_work", "nonspherical_deformations"}
    if not required.issubset(value["omitted"]):
        return "scope_export"
    if value["production_assertions"] <= 0:
        return "vacuous_production"
    return None


def main():
    base = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert failure(base) is None
    mutations = (
        ("metric_only_selects_member", "physical_member_selected", True, "physical_member_promotion"),
        ("directed_germ_one_member", "directed_germ_member_count", 1, "directed_count"),
        ("chirality_not_unique", "members_per_chirality", 2, "per_chirality_uniqueness"),
        ("path_selects_chirality", "path_only_member_count", 1, "path_nonselection"),
        ("screen_leaves_two", "signed_transverse_screen_member_count", 2, "signed_screen_uniqueness"),
        ("same_twist_sign", "screen_twist_signs", [1, 1], "opposite_twist"),
        ("control_fiber_called_population", "lawful_query_population_selected", True, "query_population_promotion"),
        ("kernel_modified", "metric_and_kernel_changed", True, "kernel_change"),
        ("empty_assertions", "production_assertions", 0, "vacuous_production"),
    )
    records = []
    for name, key, replacement, expected in mutations:
        trial = copy.deepcopy(base)
        trial[key] = replacement
        actual = failure(trial)
        assert actual == expected, (name, actual, expected)
        records.append({"case": name, "caught": True, "expected": expected})

    for omitted in ("mass", "scale", "physical_Xmax", "protected_work", "nonspherical_deformations"):
        trial = copy.deepcopy(base)
        trial["omitted"].remove(omitted)
        actual = failure(trial)
        assert actual == "scope_export", (omitted, actual)
        records.append({"case": f"promote_{omitted}", "caught": True, "expected": "scope_export"})

    result = {
        "status": "PASS",
        "baseline_valid": True,
        "hostile_cases": len(records),
        "direct_mutations": len(records),
        "records": records,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
