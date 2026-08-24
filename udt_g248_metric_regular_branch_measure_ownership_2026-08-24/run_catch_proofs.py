#!/usr/bin/env python3
"""Hostile finite mutations for the G248 measure-type and ownership boundaries."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def run() -> dict:
    r = F(9, 4)
    area = F(25, 7)
    dtau_a = F(11, 5)
    dtau_b = r * dtau_a
    coarea = r / area
    inverse_area = area / (r * r)
    inverse_coefficient = (F(1) / r) / inverse_area
    phase_pullback = r * r
    counting = F(1)
    half_character = F(3, 2)

    good_scope = {
        "regular_area_positive": True,
        "source_population_derived": False,
        "detection_probability_derived": False,
        "observational_outcomes": "CLOSED_AND_UNREAD",
    }

    def scope_valid(value: dict) -> bool:
        return (
            value.get("regular_area_positive") is True
            and value.get("source_population_derived") is False
            and value.get("detection_probability_derived") is False
            and value.get("observational_outcomes") == "CLOSED_AND_UNREAD"
        )

    try:
        _ = F(1) / F(0)
        caustic_inverse_failed = False
    except ZeroDivisionError:
        caustic_inverse_failed = True

    mutations = {
        "drop_clock_ratio_from_coarea": coarea != F(1) / area,
        "multiply_instead_of_divide_by_area": coarea != r * area,
        "use_inverse_clock_ratio": coarea != F(1) / (r * area),
        "erase_absolute_area_orientation": abs(F(-25, 7)) != F(-25, 7),
        "identify_counting_with_coarea": counting != coarea,
        "identify_phase_volume_with_coarea": phase_pullback != coarea,
        "identify_half_character_with_counting": half_character != counting,
        "claim_composition_selects_alpha": r ** F(1) != r ** F(2),
        "wrong_phase_determinant_weight": phase_pullback != r,
        "wrong_phase_pushforward_weight": F(1) / phase_pullback != phase_pullback,
        "wrong_inverse_position_area": inverse_area != area / r,
        "wrong_inverse_coarea_coefficient": inverse_coefficient != F(1) / coarea,
        "claim_full_ordered_density_reversal_invariant": coarea * dtau_a != inverse_coefficient * dtau_b,
        "identify_matched_chain_with_direct_edge": (F(2, 3) * F(5, 7)) != F(13, 17),
        "extend_regular_formula_through_caustic": caustic_inverse_failed,
        "derive_source_population_from_geometry": not scope_valid(
            {**good_scope, "source_population_derived": True}
        ),
        "derive_detection_probability_from_coarea": not scope_valid(
            {**good_scope, "detection_probability_derived": True}
        ),
        "open_observational_outcomes": not scope_valid(
            {**good_scope, "observational_outcomes": "OPENED"}
        ),
    }
    caught = {name: bool(value) for name, value in mutations.items()}
    missed = [name for name, value in caught.items() if not value]
    return {
        "caught": sum(caught.values()),
        "total": len(caught),
        "mutations": caught,
        "missed": missed,
        "status": "PASS" if not missed else "FAIL",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
