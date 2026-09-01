#!/usr/bin/env python3
"""Registered G312 semantic mutation catches; regression evidence only."""

from __future__ import annotations

import json


def classify(state):
    if state["shape_equals_constitution"]:
        raise AssertionError("G311 response shape promoted into constitution")
    if state["g301_owned"]:
        raise AssertionError("G301 class assumptions promoted")
    if state["quadratic_has_gr_principal"]:
        raise AssertionError("solution overlap conflated with principal overlap")
    if state["mixed_has_no_length"]:
        raise AssertionError("hidden length coefficient erased")
    if state["ratio_quiet_regular"]:
        raise AssertionError("quiet singularity erased")
    if state["nonlocal_has_no_carry"]:
        raise AssertionError("nonlocal Green/boundary carry erased")
    return "TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED"


def main():
    baseline = {
        "shape_equals_constitution": False,
        "g301_owned": False,
        "quadratic_has_gr_principal": False,
        "mixed_has_no_length": False,
        "ratio_quiet_regular": False,
        "nonlocal_has_no_carry": False,
    }
    assert classify(baseline) == "TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED"
    caught = {}
    for key in baseline:
        mutated = dict(baseline)
        mutated[key] = True
        try:
            classify(mutated)
        except AssertionError as error:
            caught[key] = str(error)
        else:
            raise AssertionError(f"mutation escaped: {key}")
    result = {
        "status": "PASS",
        "grade": "SEMANTIC_REGRESSION_CATCHES_NOT_INDEPENDENT_CONFIRMATION",
        "caught": caught,
        "catch_count": len(caught),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
