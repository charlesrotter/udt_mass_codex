#!/usr/bin/env python3
"""Altered-copy catches for the G264 metric-first evidence repair."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


ORDERED_CONSTRUCTION = (
    "g_first = rank3()",
    "g_second = rank4()",
    "inverse_first = rank3()",
    "gamma = rank3()",
    "gamma_first = rank4()",
    "riemann_up = rank4()",
    "ricci = matrix()",
    "scalar = sum(",
    "einstein_cov = matrix()",
    "riemann_down = rank4()",
    "kretschmann = sum(",
    "return scalar, kretschmann, radial_mixed, angular_mixed",
)


def validate(metric_source: str, consistency_source: str, result: dict[str, object]) -> None:
    positions = [metric_source.find(token) for token in ORDERED_CONSTRUCTION]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        raise AssertionError("metric-first construction removed or reordered")
    for forbidden in (
        "import sympy",
        "from sympy",
        "import derive_selectivity",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
    ):
        if forbidden in metric_source:
            raise AssertionError("forbidden dependency")
    if "case_count = 250" not in metric_source:
        raise AssertionError("metric-first case coverage")
    if metric_source.count("exact(") < 5:
        raise AssertionError("metric-first comparisons removed")
    if result["status"] != "PASS" or result["case_count"] != 250:
        raise AssertionError("metric-first result coverage")
    if result["assertion_count"] != 1000:
        raise AssertionError("metric-first result assertions")
    if result["implementation"] != (
        "standard_library_fraction_metric_first_no_sympy_no_production_import_no_result_read"
    ):
        raise AssertionError("metric-first provenance")
    if "consistency_replay_not_metric_first_derivation" not in consistency_source:
        raise AssertionError("consistency role promoted")


def run() -> dict[str, object]:
    package = Path(__file__).resolve().parent
    metric_source = (package / "verify_metric_first.py").read_text()
    consistency_source = (package / "verify_independent.py").read_text()
    result = json.loads((package / "METRIC_FIRST_VERIFICATION.json").read_text())
    validate(metric_source, consistency_source, result)

    mutations = {
        "production_import_inserted": lambda m, c, r: ("import derive_selectivity\n" + m, c, r),
        "sympy_import_inserted": lambda m, c, r: ("import sympy\n" + m, c, r),
        "saved_result_read_inserted": lambda m, c, r: (m + "\n# DERIVATION_RESULT.json\n", c, r),
        "riemann_construction_removed": lambda m, c, r: (m.replace("riemann_up = rank4()", "riemann_up = []"), c, r),
        "scalar_construction_removed": lambda m, c, r: (m.replace("scalar = sum(", "scalar_target = sum("), c, r),
        "kretschmann_construction_removed": lambda m, c, r: (m.replace("kretschmann = sum(", "k_target = sum("), c, r),
        "coverage_reduced": lambda m, c, r: (m.replace("case_count = 250", "case_count = 2"), c, r),
        "result_count_reduced": lambda m, c, r: (m, c, {**r, "assertion_count": 8}),
        "provenance_corrupted": lambda m, c, r: (m, c, {**r, "implementation": "imports production"}),
        "consistency_repromoted": lambda m, c, r: (
            m,
            c.replace("consistency_replay_not_metric_first_derivation", "independent_metric_first_derivation"),
            r,
        ),
    }
    caught: dict[str, bool] = {}
    for name, mutation in mutations.items():
        candidate_metric, candidate_consistency, candidate_result = mutation(
            metric_source, consistency_source, copy.deepcopy(result)
        )
        try:
            validate(candidate_metric, candidate_consistency, candidate_result)
        except AssertionError:
            caught[name] = True
        else:
            caught[name] = False
    if not all(caught.values()):
        raise AssertionError(f"uncaught repair mutations: {[k for k, v in caught.items() if not v]}")
    return {
        "status": "PASS",
        "mutation_count": len(caught),
        "caught_count": sum(caught.values()),
        "mutations": caught,
        "qualification": "altered_copy_repair_regression_not_scientific_proof",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
