#!/usr/bin/env python3
"""Semantic mutation checks for the bounded G352 landing contract."""

import copy
import json
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "CATCH_PROOF_RESULT.json"


def validate(record):
    return all(
        [
            record["premise_status"] == "OWNER_ADOPTED_PROVISIONAL_PREMISE",
            record["realization_status"] == "CHOSE_BOUNDED_MATHEMATICAL_REALIZATION",
            record["clock_rate_p"] == 1,
            record["regular_density_q"] == -1,
            record["phase_normalization_cancels"],
            record["continuous_phase_intensity"],
            not record["literal_discrete_instantaneous_rate_claimed"],
            record["product_measure_nonnegative"],
            record["phase_label_factorization_explicit"],
            not record["phase_label_factorization_derived_from_g351"],
            not record["preferred_observer"],
            not record["universal_p_selected"],
            not record["zero_source_creates_content"],
            not record["finite_density_at_every_caustic"],
            not record["image_union_replaces_label_measure"],
            not record["cross_label_physics_selected"],
            not record["light_or_energy_selected"],
            not record["detector_or_distance_selected"],
            not record["history_scale_xmax_matter_canon_selected"],
        ]
    )


def main():
    baseline = {
        "premise_status": "OWNER_ADOPTED_PROVISIONAL_PREMISE",
        "realization_status": "CHOSE_BOUNDED_MATHEMATICAL_REALIZATION",
        "clock_rate_p": 1,
        "regular_density_q": -1,
        "phase_normalization_cancels": True,
        "continuous_phase_intensity": True,
        "literal_discrete_instantaneous_rate_claimed": False,
        "product_measure_nonnegative": True,
        "phase_label_factorization_explicit": True,
        "phase_label_factorization_derived_from_g351": False,
        "preferred_observer": False,
        "universal_p_selected": False,
        "zero_source_creates_content": False,
        "finite_density_at_every_caustic": False,
        "image_union_replaces_label_measure": False,
        "cross_label_physics_selected": False,
        "light_or_energy_selected": False,
        "detector_or_distance_selected": False,
        "history_scale_xmax_matter_canon_selected": False,
    }
    if not validate(baseline):
        raise AssertionError("baseline contract rejected")

    mutations = [
        ("wrong_p", "clock_rate_p", 0),
        ("wrong_q", "regular_density_q", 0),
        ("phase_scale_leak", "phase_normalization_cancels", False),
        ("atomic_count_called_smooth", "literal_discrete_instantaneous_rate_claimed", True),
        ("signed_product_measure", "product_measure_nonnegative", False),
        ("hidden_phase_label_factorization", "phase_label_factorization_explicit", False),
        ("factorization_called_g351_derived", "phase_label_factorization_derived_from_g351", True),
        ("realization_called_derived", "realization_status", "DERIVED"),
        ("preferred_observer", "preferred_observer", True),
        ("universal_p", "universal_p_selected", True),
        ("source_creation", "zero_source_creates_content", True),
        ("finite_caustic_density", "finite_density_at_every_caustic", True),
        ("image_union_substitution", "image_union_replaces_label_measure", True),
        ("cross_label_promotion", "cross_label_physics_selected", True),
        ("premise_called_derived", "premise_status", "DERIVED"),
        ("light_energy_import", "light_or_energy_selected", True),
        ("detector_distance_import", "detector_or_distance_selected", True),
        ("history_scale_import", "history_scale_xmax_matter_canon_selected", True),
    ]

    caught = []
    for name, key, value in mutations:
        trial = copy.deepcopy(baseline)
        trial[key] = value
        if validate(trial):
            raise AssertionError(f"mutation escaped: {name}")
        caught.append(name)

    result = {
        "baseline_passed": True,
        "mutations_caught": len(caught),
        "mutations_total": len(mutations),
        "caught": caught,
        "status": "PASS",
        "semantic_regression_only": True,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
