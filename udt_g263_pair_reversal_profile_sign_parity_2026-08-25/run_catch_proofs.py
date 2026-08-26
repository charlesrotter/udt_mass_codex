#!/usr/bin/env python3
"""Applied artifact-mutation catches for G263."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


LANDING = (
    "PAIR_ARROW_REVERSAL_IS_EXACT_RECIPROCAL_INVOLUTION"
    "__WHOLE_PROFILE_SIGN_CONJUGATION_IS_A_DISTINCT_METRIC_INVOLUTION"
    "__SCALAR_DEPTH_INVERSION_SHARED_BUT_COMPLETE_CHANNEL_PARITIES_MIXED"
)

EXPECTED_CHECKS = (
    "pair_reversal_inverse",
    "pair_D_even",
    "pair_D_odd",
    "pair_D_reconstruction",
    "pair_clock_even",
    "pair_clock_odd",
    "pair_chi_odd",
    "pair_contrast_even",
    "profile_f_inverse",
    "profile_lapse_inverse",
    "profile_lapse_even",
    "profile_lapse_odd",
    "profile_f_even",
    "profile_f_odd",
    "mass_aspect_even",
    "mass_aspect_odd",
    "mass_aspect_reconstruction",
    "acceleration_even",
    "acceleration_odd",
    "E0_even",
    "E0_odd",
    "E1_even",
    "E1_odd",
    "Aparallel_even",
    "Aparallel_odd",
    "Aperp_even",
    "Aperp_odd",
    "angular_residual_join",
    "conjugate_angular_residual_join",
    "zero_tide_conjugate_Aparallel",
    "zero_tide_conjugate_Aperp",
)

EXPECTED_OPERATIONS = {
    "R_pair": "endpoint swap at fixed ambient metric; delta->-delta",
    "C_phi": "whole profile and jets conjugated; (phi,p,z)->(-phi,-p,-z), f->1/f",
}

EXPECTED_SEPARATION = {
    "distinct": "R_pair fixes g; C_phi changes g_phi to g_minus_phi and generally changes every hierarchy channel",
    "shared": "both can invert endpoint scalar depth when C_phi acts on both endpoint values",
    "sphere_guard": "areal r^2 dOmega^2 is unchanged under C_phi, so clock/radial coefficient exchange is not a full coframe swap",
}

EXPECTED_ENDS = {
    "phi_to_negative_infinity": "N->infinity; mu/r->-infinity; Aparallel->0; Aperp->-infinity",
    "phi_to_positive_infinity": "N->0; mu/r->1/2; Aparallel->0; Aperp->1",
}


def validate(data: dict[str, object]) -> None:
    if data["status"] != "PASS" or data["landing"] != LANDING:
        raise AssertionError("landing")
    if data["classification"] != "SCALAR_EQUIVALENCE_ONLY":
        raise AssertionError("classification")
    if data["symbolic_check_count"] != len(EXPECTED_CHECKS):
        raise AssertionError("symbolic count")
    if data["symbolic_checks"] != list(EXPECTED_CHECKS):
        raise AssertionError("complete symbolic check set")
    if data["operations"] != EXPECTED_OPERATIONS:
        raise AssertionError("R_pair type")
    if data["separation"] != EXPECTED_SEPARATION:
        raise AssertionError("operation separation and shared scalar")
    ownership = data["ownership"]
    if ownership["profile_conjugation"] != "MATHEMATICAL_DIAGNOSTIC_NOT_PHYSICAL_SYMMETRY":
        raise AssertionError("profile ownership")
    if ownership["history_selection"] != "NOT_DERIVED":
        raise AssertionError("history promotion")
    if ownership["physical_mass_or_source"] != "NOT_DERIVED":
        raise AssertionError("mass promotion")
    if ownership["universal_angular_loudness"] != "NOT_DERIVED_G201_ZERO_TIDE_COUNTERFAMILY_RETAINED":
        raise AssertionError("lockstep promotion")
    if data["asymptotic_constant_jet"] != EXPECTED_ENDS:
        raise AssertionError("scoped constant-jet asymptotics")


def run() -> dict[str, object]:
    source = Path(__file__).with_name("DERIVATION_RESULT.json")
    baseline = json.loads(source.read_text(encoding="utf-8"))
    validate(baseline)
    mutations = {
        "full_equivalence_promoted": lambda d: d.update(classification="FULL_EQUIVALENCE"),
        "pair_metric_not_fixed": lambda d: d["separation"].update(distinct="both change g"),
        "profile_called_physical_symmetry": lambda d: d["ownership"].update(profile_conjugation="DERIVED_PHYSICAL_SYMMETRY"),
        "history_selected": lambda d: d["ownership"].update(history_selection="DERIVED"),
        "mass_promoted": lambda d: d["ownership"].update(physical_mass_or_source="DERIVED"),
        "lockstep_loudness_promoted": lambda d: d["ownership"].update(universal_angular_loudness="DERIVED"),
        "sphere_deleted": lambda d: d["separation"].update(sphere_guard="sphere omitted"),
        "negative_asymptotic_mirrored": lambda d: d["asymptotic_constant_jet"].update(phi_to_negative_infinity="mu/r->-1/2"),
        "positive_asymptotic_corrupted": lambda d: d["asymptotic_constant_jet"].update(phi_to_positive_infinity="mu/r->infinity"),
        "symbolic_count_reduced": lambda d: d.update(symbolic_check_count=30),
        "angular_join_removed": lambda d: d["symbolic_checks"].remove("angular_residual_join"),
        "zero_tide_conjugate_claimed_quiet": lambda d: d["symbolic_checks"].remove("zero_tide_conjugate_Aperp"),
        "shared_scalar_story_corrupted": lambda d: d["separation"].update(shared="shared scalar inversion never happens"),
        "pair_contrast_replaced_with_padding": lambda d: (
            d["symbolic_checks"].remove("pair_contrast_even"),
            d["symbolic_checks"].append("bogus_placeholder_check"),
        ),
        "positive_end_angular_corrupted": lambda d: d["asymptotic_constant_jet"].update(
            phi_to_positive_infinity="N->0; mu/r->1/2; Aparallel->999; Aperp->999"
        ),
        "negative_end_angular_corrupted": lambda d: d["asymptotic_constant_jet"].update(
            phi_to_negative_infinity="N->infinity; mu/r->-infinity; Aparallel->999; Aperp->999"
        ),
        "pair_delta_reversal_weakened": lambda d: d["operations"].update(
            R_pair="endpoint swap at fixed ambient metric; delta stays the same except in examples"
        ),
    }
    caught: dict[str, bool] = {}
    for name, mutate in mutations.items():
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        try:
            validate(candidate)
        except AssertionError:
            caught[name] = True
        else:
            caught[name] = False
    if not all(caught.values()):
        raise AssertionError(f"uncaught mutations: {[k for k, v in caught.items() if not v]}")
    return {
        "status": "PASS",
        "mutation_count": len(caught),
        "caught_count": sum(caught.values()),
        "mutations": caught,
        "qualification": "artifact_regression_only_not_scientific_proof",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
