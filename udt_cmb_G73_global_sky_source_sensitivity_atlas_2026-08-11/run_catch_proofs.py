#!/usr/bin/env python3
"""Exercise semantic catches for the G73 source-sensitivity classification."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "REGULAR_SKY_RESPONSE_SOURCE_INVERTIBLE__"
    "ROBUST_KALEIDOSCOPE_REQUIRES_GLOBAL_BRANCHING_SINGULARITY_OR_SOURCE_RESTRICTION"
)


def valid(payload: dict) -> bool:
    status = payload.get("status", {})
    return (
        payload.get("landing") == LANDING
        and payload.get("g68_control", {}).get("rows") == 21
        and payload.get("g68_control", {}).get("max_singular_value_ratio", 0.0) < 1.01
        and status.get("regular_single_branch_source_recovery") == "DERIVED_EXACT"
        and status.get("strong_shear_directional_alignment") == "DERIVED_ASYMPTOTIC_CONDITIONAL"
        and status.get("rank_loss_or_fold_kaleidoscope") == "POTENTIAL_MECHANISM_OPEN_NO_BRANCH_OWNER"
        and status.get("multibranch_observable_combination") == "OPEN_NO_OWNER"
        and status.get("g68_kaleidoscope_strength") == "OBSERVED_WEAK_ON_BOUNDED_TILE"
        and status.get("physical_cmb_source_and_observable") == "OPEN_NO_OWNER"
    )


def main() -> None:
    base = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert valid(base)
    changes = {
        "regular_source_erased": ("status", "regular_single_branch_source_recovery", "SOURCE_ERASED"),
        "strong_shear_promoted_to_owned": ("status", "strong_shear_directional_alignment", "OWNED_PHYSICAL"),
        "fold_promoted_to_derived": ("status", "rank_loss_or_fold_kaleidoscope", "DERIVED_CMB_KALEIDOSCOPE"),
        "branch_sum_invented": ("status", "multibranch_observable_combination", "DERIVED_SUM"),
        "g68_called_strong": ("status", "g68_kaleidoscope_strength", "OBSERVED_STRONG"),
        "physical_cmb_promoted": ("status", "physical_cmb_source_and_observable", "DERIVED"),
        "wrong_landing": ("landing", "", "CMB_KALEIDOSCOPE_DERIVED"),
        "missing_g68_row": ("g68_control", "rows", 20),
        "false_g68_ratio": ("g68_control", "max_singular_value_ratio", 4.0),
    }
    caught = {}
    for name, (outer, inner, value) in changes.items():
        candidate = deepcopy(base)
        if inner:
            candidate[outer][inner] = value
        else:
            candidate[outer] = value
        caught[name] = not valid(candidate)
    assert all(caught.values()), [name for name, value in caught.items() if not value]
    payload = {
        "schema": "udt-cmb-g73-catches-v1",
        "caught": caught,
        "passed": sum(caught.values()),
        "total": len(caught),
    }
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
