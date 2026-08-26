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


def validate(data: dict[str, object]) -> None:
    if data["status"] != "PASS" or data["landing"] != LANDING:
        raise AssertionError("landing")
    if data["classification"] != "SCALAR_EQUIVALENCE_ONLY":
        raise AssertionError("classification")
    if data["symbolic_check_count"] != 31:
        raise AssertionError("symbolic count")
    checks = data["symbolic_checks"]
    for required in (
        "pair_reversal_inverse",
        "angular_residual_join",
        "conjugate_angular_residual_join",
        "zero_tide_conjugate_Aparallel",
        "zero_tide_conjugate_Aperp",
    ):
        if required not in checks:
            raise AssertionError(required)
    if not data["operations"]["R_pair"].startswith("endpoint swap at fixed ambient metric"):
        raise AssertionError("R_pair type")
    if "whole profile and jets conjugated" not in data["operations"]["C_phi"]:
        raise AssertionError("C_phi type")
    if not data["separation"]["distinct"].startswith("R_pair fixes g"):
        raise AssertionError("operation separation")
    if "areal r^2 dOmega^2 is unchanged" not in data["separation"]["sphere_guard"]:
        raise AssertionError("sphere guard")
    ownership = data["ownership"]
    if ownership["profile_conjugation"] != "MATHEMATICAL_DIAGNOSTIC_NOT_PHYSICAL_SYMMETRY":
        raise AssertionError("profile ownership")
    if ownership["history_selection"] != "NOT_DERIVED":
        raise AssertionError("history promotion")
    if ownership["physical_mass_or_source"] != "NOT_DERIVED":
        raise AssertionError("mass promotion")
    if ownership["universal_angular_loudness"] != "NOT_DERIVED_G201_ZERO_TIDE_COUNTERFAMILY_RETAINED":
        raise AssertionError("lockstep promotion")
    if "mu/r->1/2" not in data["asymptotic_constant_jet"]["phi_to_positive_infinity"]:
        raise AssertionError("positive asymptotic")
    if "mu/r->-infinity" not in data["asymptotic_constant_jet"]["phi_to_negative_infinity"]:
        raise AssertionError("negative asymptotic")


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
