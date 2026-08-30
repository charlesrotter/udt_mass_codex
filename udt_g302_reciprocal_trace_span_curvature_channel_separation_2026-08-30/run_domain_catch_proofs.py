#!/usr/bin/env python3
"""Hostile checks for the G302 exhaustive domain-census repair."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def validate(data):
    assert data["status"] == "PASS"
    assert data["imports_production_code"] is False
    assert data["physical_threshold"] == "b=-4/(3*sqrt(R0))"
    assert data["positive_repeated_root"] == "x=1,beta=-2/3"
    assert data["repeated_factorization"] == "-(x-1)^2*(x+2)"
    assert data["root_at_zero_boundary"] == "beta=0"
    assert data["rows_verified_field_by_field"] == 8
    assert data["all_fields_match"] is True
    assert data["cell_positive_root_counts"]["R0_positive_at_negative_threshold"] == 1
    assert data["cell_positive_root_counts"]["R0_positive_between_threshold_and_zero"] == 2
    assert data["cell_positive_root_counts"]["R0_positive_below_negative_threshold"] == 0
    assert data["interval_orientation"]["R0>0,b=-threshold"] == "nonpositive_with_one_double_zero"
    assert data["interval_orientation"]["R0>0,-threshold<b<0"] == "negative_positive_negative_across_two_roots"


def main():
    source = json.loads((ROOT / "DOMAIN_CENSUS_VERIFICATION.json").read_text(encoding="utf-8"))
    validate(source)
    mutations = {
        "wrong_threshold": lambda d: d.__setitem__("physical_threshold", "b=-2/(3*sqrt(R0))"),
        "wrong_double_root": lambda d: d.__setitem__("repeated_factorization", "-(x-1)*(x+2)"),
        "false_positive_repeated_interval": lambda d: d["interval_orientation"].__setitem__("R0>0,b=-threshold", "positive_near_root"),
        "reversed_two_root_interval": lambda d: d["interval_orientation"].__setitem__("R0>0,-threshold<b<0", "positive_outside_roots"),
        "missing_row": lambda d: d.__setitem__("rows_verified_field_by_field", 7),
        "wrong_open_cell_count": lambda d: d["cell_positive_root_counts"].__setitem__("R0_positive_between_threshold_and_zero", 1),
    }
    caught = {}
    for name, mutate in mutations.items():
        trial = deepcopy(source)
        mutate(trial)
        try:
            validate(trial)
        except AssertionError:
            caught[name] = True
        else:
            caught[name] = False
    assert all(caught.values())
    output = {"status": "PASS", "count": len(caught), "caught": caught}
    (ROOT / "DOMAIN_CATCH_PROOF_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"G302 domain catch proofs PASS ({len(caught)}/{len(caught)})")


if __name__ == "__main__":
    main()

