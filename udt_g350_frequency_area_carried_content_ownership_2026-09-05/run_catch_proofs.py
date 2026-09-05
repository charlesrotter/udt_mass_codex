#!/usr/bin/env python3
"""Hostile claim mutations for the preregistered G350 ownership boundary."""

import copy
import json
import os
from pathlib import Path


BASELINE = {
    "primary": "NONUNIQUE_CHARACTER_FAMILY",
    "unique": False,
    "identity_retained": True,
    "p_status": "FREE",
    "q_status": "FREE",
    "conservation_status": "NEW_PREMISE_NOT_ADOPTED",
    "frequency_weight_status": "OPEN_CARRIED_TYPE",
    "source_generated": False,
    "zero_preserved": True,
    "reversal": True,
    "sewing": True,
    "transfer_form": "MULTIPLICATIVE_CHARACTER",
    "observer_covariance": True,
    "observer_invariant": False,
    "two_ratio_class_exhaustive": False,
    "endpoint_coboundaries_retained": True,
    "finite_nonzero_all_caustics": False,
    "caustics_retained": True,
    "physical_label_sum": False,
    "photon_or_energy_import": False,
    "brightness_flux_luminosity_probability": False,
    "observational_distance": False,
    "matter_or_mass": False,
    "scale_or_xmax": False,
    "canon": False,
}


def valid(record):
    return record == BASELINE


def main():
    mutations = [
        ("assert_unique", "unique", True),
        ("delete_identity", "identity_retained", False),
        ("fix_p", "p_status", "FIXED_ONE"),
        ("fix_q", "q_status", "FIXED_MINUS_ONE"),
        ("derive_conservation", "conservation_status", "DERIVED_FROM_AREA"),
        ("fix_frequency_weight", "frequency_weight_status", "FIXED_ONE"),
        ("create_source", "source_generated", True),
        ("break_zero", "zero_preserved", False),
        ("omit_reversal", "reversal", False),
        ("break_sewing", "sewing", False),
        ("additive_transfer", "transfer_form", "ADDITIVE"),
        ("drop_observer_covariance", "observer_covariance", False),
        ("claim_observer_invariance", "observer_invariant", True),
        ("claim_exhaustive", "two_ratio_class_exhaustive", True),
        ("remove_coboundaries", "endpoint_coboundaries_retained", False),
        ("finite_inverse_area_at_caustic", "finite_nonzero_all_caustics", True),
        ("delete_caustics", "caustics_retained", False),
        ("sum_labels_physically", "physical_label_sum", True),
        ("import_photon_energy", "photon_or_energy_import", True),
        ("promote_brightness", "brightness_flux_luminosity_probability", True),
        ("promote_distance", "observational_distance", True),
        ("promote_matter", "matter_or_mass", True),
        ("select_scale_xmax", "scale_or_xmax", True),
        ("promote_canon", "canon", True),
        ("wrong_primary", "primary", "ONE_UNIQUE_TRANSFER"),
    ]
    caught = []
    for name, key, value in mutations:
        candidate = copy.deepcopy(BASELINE)
        candidate[key] = value
        if valid(candidate):
            raise AssertionError(f"hostile mutation escaped: {name}")
        caught.append(name)

    if not valid(copy.deepcopy(BASELINE)):
        raise AssertionError("baseline rejected")

    result = {
        "all_passed": True,
        "mutations_caught": len(caught),
        "mutations_total": len(mutations),
        "caught": caught,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") == "1":
        print(rendered, end="")
    else:
        Path("CATCH_PROOF_RESULT.json").write_text(rendered, encoding="utf-8")
        print(rendered, end="")


if __name__ == "__main__":
    main()
