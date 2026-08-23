#!/usr/bin/env python3
"""In-memory catch proofs for the G233 evidence verifier."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from verify_package import validate_exact, validate_independent, validate_initial_failure


ROOT = Path(__file__).resolve().parent


def caught(validator, payload):
    try:
        validator(payload)
    except AssertionError:
        return True
    return False


def main():
    exact = json.loads((ROOT / "exact_results.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "independent_results.json").read_text(encoding="utf-8"))
    initial = json.loads((ROOT / "INITIAL_INDEPENDENT_FAILURE.json").read_text(encoding="utf-8"))

    mutations = []

    item = copy.deepcopy(exact)
    item["next_difference_b1_minus_b0"] = "0"
    mutations.append(("erase_symbolic_separator", caught(validate_exact, item)))

    item = copy.deepcopy(exact)
    item["metric_jet_nonzero_counts"]["4"] = 1
    mutations.append(("break_shared_metric_four_jet", caught(validate_exact, item)))

    item = copy.deepcopy(exact)
    item["arbitrary_order_checks"]["6"]["coefficient"] = "0"
    mutations.append(("break_arbitrary_order_coefficient", caught(validate_exact, item)))

    item = copy.deepcopy(exact)
    item["g204"]["state"] = ["x"]
    mutations.append(("collapse_G204_state", caught(validate_exact, item)))

    item = copy.deepcopy(independent)
    item["next_difference"] = "0"
    mutations.append(("erase_independent_separator", caught(validate_independent, item)))

    item = copy.deepcopy(independent)
    item["radial_values_second"][:3] = ["1", "2", "3"]
    mutations.append(("break_independent_shared_state", caught(validate_independent, item)))

    item = copy.deepcopy(initial)
    item["all_checks_pass"] = True
    mutations.append(("erase_initial_failure", caught(validate_initial_failure, item)))

    result = {
        "all_caught": all(flag for _, flag in mutations),
        "count": len(mutations),
        "mutations": {name: flag for name, flag in mutations},
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_caught"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
