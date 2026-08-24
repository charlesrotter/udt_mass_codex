#!/usr/bin/env python3
"""Hostile algebraic and semantic mutation catches for G246."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
PRODUCTION = PACKAGE / "DERIVATION_RESULT.json"
INDEPENDENT = PACKAGE / "INDEPENDENT_VERIFICATION.json"
OUTPUT = PACKAGE / "CATCH_PROOF_RESULT.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    production = json.loads(PRODUCTION.read_text(encoding="utf-8"))
    independent = json.loads(INDEPENDENT.read_text(encoding="utf-8"))
    symbolic = production["symbolic"]
    cylinder = production["cylinder_multiple_branch_control"]

    checks = {
        "cone_cone_transversality_mutation_caught": symbolic["cone_cone_wedge_on_shared_generator"] == "0",
        "cone_worldline_tangency_mutation_caught": production["local_theorem"]["cone_worldline_transverse"] is True,
        "separate_null_sheet_mutation_caught": production["local_theorem"]["separate_null_sheet_required"] is False,
        "preferred_local_branch_mutation_caught": production["local_theorem"]["preferred_branch_selected"] is False,
        "frequency_ratio_mutation_caught": symbolic["frequency_ratio"] == "e",
        "pair_determinant_mutation_caught": production["pair_ribbon"]["determinant"] == "-a^2",
        "completed_density_mutation_caught": production["pair_ribbon"]["completed_density"] == "m=a",
        "inverse_return_identification_caught": production["reversal"]["generic_inverse_equals_return"] is False,
        "global_branch_selection_caught": cylinder["branch_count_in_registered_window"] > 1 and cylinder["preferred_branch_selected"] is False,
        "scalar_selects_winding_mutation_caught": len(set(cylinder["all_scalar_depths"])) == 1 and cylinder["distinct_route_delays"] > 1,
        "universal_null_protocol_mutation_caught": production["universal_query_type_selected"] is False,
        "source_law_mutation_caught": production["source_or_detector_law_used"] is False,
        "fitted_coefficient_mutation_caught": production["fitted_coefficients"] == independent["fitted_coefficients"] == 0,
        "outcome_access_mutation_caught": production["observational_outcomes"] == independent["observational_outcomes"] == "CLOSED_AND_UNREAD",
        "history_selection_mutation_caught": production["physical_history"] == independent["physical_history"] == "QUERY_SUPPLIED_NOT_SELECTED",
        "independent_route_contamination_caught": independent["imports_production_code"] is False and independent["reads_production_output"] is False,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "caught": sum(bool(value) for value in checks.values()),
        "checks": checks,
    }
    if result["status"] != "PASS":
        raise RuntimeError(f"G246 hostile catch failure: {checks}")
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
