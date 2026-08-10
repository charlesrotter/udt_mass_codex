#!/usr/bin/env python3
"""Exercise fail-closed semantic catches for the bounded R17 result."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent


def valid(result: dict) -> bool:
    return all(
        [
            result["scope"] == "R17/W01 C01-C06 regular global off-shell configurations",
            not result["zero_lift_is_a_depth_realization"],
            result["metric_vertical_factor_unique_modulo_screen_rotation"],
            not result["raw_arrow_uniqueness"],
            result["complete_coframe_realization_gate_used"],
            result["complete_coframe_realization_status"] == "CONDITIONAL_BRANCH_CONFIGURATION_INPUT",
            not result["founding_pair_alone_fixes_screen"],
            not result["lambda_selected_across_family"],
            not result["full_semidirect_assembly_selected"],
            not result["physical_path_or_isometric_factor_selected"],
            not result["intrinsic_endpoint_reset_selected"],
            not result["pair_surface_selected"],
            not result["universal_mixed_ceff_selected"],
            result["downstream_physics_derived"] == [],
            result["primary_landing"].startswith("COMPLETE_COFRAME_CONDITIONAL_"),
        ]
    )


def main() -> None:
    baseline = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    if not valid(baseline):
        raise AssertionError("baseline semantic result is invalid")

    mutations = [
        ("C01", "call identity a nonzero-depth lift", "zero_lift_is_a_depth_realization", True),
        ("C02", "claim raw-arrow uniqueness", "raw_arrow_uniqueness", True),
        ("C03", "drop complete-coframe realization gate", "complete_coframe_realization_gate_used", False),
        ("C04", "claim founding pair fixes screen", "founding_pair_alone_fixes_screen", True),
        ("C05", "select lambda across C01-C06", "lambda_selected_across_family", True),
        ("C06", "promote full semidirect assembly", "full_semidirect_assembly_selected", True),
        ("C07", "select physical path or isometry", "physical_path_or_isometric_factor_selected", True),
        ("C08", "set endpoint reset to identity", "intrinsic_endpoint_reset_selected", True),
        ("C09", "promote linear lift to pair surface", "pair_surface_selected", True),
        ("C10", "promote mixed c_eff universally", "universal_mixed_ceff_selected", True),
    ]
    rows: list[dict[str, str]] = []
    for catch_id, description, field, bad_value in mutations:
        mutant = deepcopy(baseline)
        mutant[field] = bad_value
        rejected = not valid(mutant)
        rows.append(
            {
                "catch_id": catch_id,
                "mutation": description,
                "expected": "REJECT",
                "observed": "REJECT" if rejected else "ACCEPT",
            }
        )

    scope_mutant = deepcopy(baseline)
    scope_mutant["scope"] = "all Lorentzian metrics"
    rows.append(
        {
            "catch_id": "C11",
            "mutation": "generalize beyond R17 C01-C06",
            "expected": "REJECT",
            "observed": "REJECT" if not valid(scope_mutant) else "ACCEPT",
        }
    )
    physics_mutant = deepcopy(baseline)
    physics_mutant["downstream_physics_derived"] = ["action"]
    rows.append(
        {
            "catch_id": "C12",
            "mutation": "infer downstream action",
            "expected": "REJECT",
            "observed": "REJECT" if not valid(physics_mutant) else "ACCEPT",
        }
    )
    conditional_mutant = deepcopy(baseline)
    conditional_mutant["complete_coframe_realization_status"] = "DERIVED_UNCONDITIONAL"
    rows.append(
        {
            "catch_id": "C13",
            "mutation": "erase complete-coframe conditionality",
            "expected": "REJECT",
            "observed": "REJECT" if not valid(conditional_mutant) else "ACCEPT",
        }
    )

    if any(row["observed"] != "REJECT" for row in rows):
        raise AssertionError("one or more semantic mutations escaped")
    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"catch proofs: {len(rows)}/{len(rows)}")


if __name__ == "__main__":
    main()
