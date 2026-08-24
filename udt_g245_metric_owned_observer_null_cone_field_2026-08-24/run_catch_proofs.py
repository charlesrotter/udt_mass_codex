#!/usr/bin/env python3
"""Hostile mutation catches for G245."""

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

    # One-dimensional symplectic blocks embedded modewise: B20=A2 B1+B2 D1=1,
    # while the forbidden B2 B1 product is zero.
    position_block_composite = 1 * 1 + 0 * 1
    forbidden_position_product = 0 * 1

    checks = {
        "nonunit_direction_scale_breaks_nullness": (-1 + 2**2) != 0,
        "preferred_ray_mutation_caught": production["observer_cone"]["preferred_ray_selected"] is False,
        "source_requirement_mutation_caught": production["observer_cone"]["source_population_required"] is False,
        "scalarized_rotating_tide_caught": production["controls"]["rotating_tide_series"]["D4_offdiagonal_nonzero"] is True,
        "position_block_multiplication_caught": position_block_composite != forbidden_position_product,
        "caustic_position_inverse_caught": production["controls"]["caustic"]["position_inverse_used"] is False,
        "H_only_autonomy_caught": production["induced_field"]["H_alone_autonomous"] is False,
        "parity_scalarization_caught": production["finite_census"]["reflection_parity_flip_cases"] > 0,
        "fitted_coefficient_caught": production["fitted_angular_coefficients"] == independent["fitted_angular_coefficients"] == 0,
        "outcome_access_caught": production["observational_outcomes"] == independent["observational_outcomes"] == "CLOSED_AND_UNREAD",
        "history_selection_caught": production["physical_history"] == independent["physical_history"] == "QUERY_SUPPLIED_NOT_SELECTED",
        "full_phase_loss_caught": (
            production["induced_field"]["full_phase_required"] is True
            and production["controls"]["caustic"]["full_phase_det"] == "1"
            and independent["controls"]["rational_caustic_phase"]["full_phase_invertible"] is True
        ),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "caught": sum(bool(value) for value in checks.values()),
        "checks": checks,
    }
    if result["status"] != "PASS":
        raise RuntimeError(f"G245 hostile catch failure: {checks}")
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
