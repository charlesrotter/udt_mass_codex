#!/usr/bin/env python3
"""Applied artifact-mutation catches for the bounded G264 landing."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


LANDING = (
    "NEGATIVE_PHI_SIGN_ALONE_DOES_NOT_SELECT"
    "__FINITE_ARBITRARILY_DEEP_SMOOTH_ASYMPTOTICALLY_FLAT_SLICE_COMPLETE_COUNTERFAMILY_EXISTS"
    "__UNBOUNDED_NEGATIVE_ENDS_HAVE_AN_ALPHA_TWO_CURVATURE_ACCELERATION_AND_SLICE_COMPLETENESS_THRESHOLD"
    "__THE_ALPHA_TWO_CRITICAL_REPRESENTATIVE_IS_THE_G201_ZERO_TIDE_FAMILY"
)

EXPECTED_CHECKS = (
    "metric_determinant_f_independent",
    "scalar_curvature_direct",
    "einstein_radial_channel",
    "einstein_angular_channel",
    "scalar_from_channel_trace",
    "kretschmann_direct",
    "bump_first_derivative",
    "bump_second_derivative",
    "bump_scalar_curvature",
    "bump_kretschmann",
    "bump_center_f",
    "bump_center_first_derivative",
    "bump_center_scalar",
    "bump_center_kretschmann",
    "bump_asymptotic_f",
    "bump_asymptotic_scalar",
    "bump_asymptotic_kretschmann",
    "bump_center_phi_coefficient",
    "bump_maximum_value",
    "power_scalar_leading",
    "power_kretschmann_leading",
    "power_acceleration_leading",
    "critical_scalar_constant",
    "critical_kretschmann_constant",
    "critical_Aparallel_zero",
    "critical_Aperp_zero",
    "critical_acceleration_limit",
)


def validate(data: dict[str, object]) -> None:
    if data["status"] != "PASS" or data["landing"] != LANDING:
        raise AssertionError("landing")
    if data["classification"] != "SIGN_ONLY_NONSELECTION_WITH_GROWTH_THRESHOLDS":
        raise AssertionError("classification")
    if data["symbolic_check_count"] != len(EXPECTED_CHECKS):
        raise AssertionError("symbolic count")
    if data["symbolic_checks"] != list(EXPECTED_CHECKS):
        raise AssertionError("complete check set")
    if data["invariants"] != {
        "determinant": "-c_E^2 r^4 sin(theta)^2 independent of f",
        "scalar_curvature": "-f_second-4 f_first/r-2(f-1)/r^2",
        "kretschmann": "f_second^2+4(f_first/r)^2+4((f-1)/r^2)^2",
    }:
        raise AssertionError("invariant formulas")
    bump = data["negative_bump"]
    if bump["ownership"] != "counterfamily_not_selected_physical_history":
        raise AssertionError("counterfamily promotion")
    required_bump = {
        "phi<0 for every finite r>0",
        "smooth areal center",
        "asymptotically flat",
        "bounded scalar and Kretschmann curvature for each finite epsilon and length",
        "complete static spatial slice",
        "arbitrarily negative finite minimum as epsilon increases",
    }
    if set(bump["properties"]) != required_bump:
        raise AssertionError("counterfamily completeness")
    power = data["power_end"]
    if "logarithmically infinite" not in power["alpha_equal_2"]:
        raise AssertionError("alpha-two radial threshold")
    if "R,K and normalized acceleration diverge" not in power["alpha_greater_than_2"]:
        raise AssertionError("supercritical threshold")
    if power["spatial_volume"] != "infinite for alpha<=6 and finite for alpha>6":
        raise AssertionError("volume threshold")
    critical = data["alpha_two_critical"]
    if critical["family"] != "f=1+C(r/L)^2 with C>0":
        raise AssertionError("critical family")
    if critical["G201_angular_channels"] != "Aparallel=Aperp=0 exactly":
        raise AssertionError("G201 intersection")
    if critical["ownership"] != "derived_conditional_intersection_not_physical_selection":
        raise AssertionError("critical selection promotion")
    ownership = data["ownership"]
    if ownership["sign_only_selection"] != "NOT_DERIVED_COUNTERFAMILY":
        raise AssertionError("sign-only selection")
    if ownership["spatial_completeness"] != "CONDITIONAL_GEOMETRIC_CLASSIFIER":
        raise AssertionError("completeness promotion")
    if ownership["physical_mass_or_energy_positivity"] != "NOT_USED_NOT_DERIVED":
        raise AssertionError("mass import")
    if ownership["history_source_dynamics_xmax"] != "OPEN":
        raise AssertionError("open physics promotion")


def run() -> dict[str, object]:
    baseline = json.loads(Path(__file__).with_name("DERIVATION_RESULT.json").read_text())
    validate(baseline)
    mutations = {
        "sign_only_selection_promoted": lambda d: d.update(classification="NEGATIVE_SIGN_SELECTS"),
        "finite_negative_called_singular": lambda d: d["negative_bump"]["properties"].remove(
            "bounded scalar and Kretschmann curvature for each finite epsilon and length"
        ),
        "counterfamily_promoted_to_history": lambda d: d["negative_bump"].update(
            ownership="selected_physical_history"
        ),
        "counterfamily_deleted": lambda d: d["negative_bump"]["properties"].clear(),
        "completeness_promoted": lambda d: d["ownership"].update(spatial_completeness="FOUNDED_LAW"),
        "mass_positivity_imported": lambda d: d["ownership"].update(
            physical_mass_or_energy_positivity="DERIVED"
        ),
        "alpha_threshold_shifted": lambda d: d["power_end"].update(
            alpha_equal_2="radial slice length finite; all invariants diverge"
        ),
        "supercritical_divergence_deleted": lambda d: d["power_end"].update(
            alpha_greater_than_2="all channels finite"
        ),
        "volume_threshold_corrupted": lambda d: d["power_end"].update(
            spatial_volume="finite for alpha>2"
        ),
        "critical_family_corrupted": lambda d: d["alpha_two_critical"].update(
            family="f=1+C(r/L)^3"
        ),
        "G201_intersection_deleted": lambda d: d["alpha_two_critical"].update(
            G201_angular_channels="unknown"
        ),
        "G201_intersection_promoted": lambda d: d["alpha_two_critical"].update(
            ownership="selected_physical_history"
        ),
        "history_promoted": lambda d: d["ownership"].update(history_source_dynamics_xmax="DERIVED"),
        "determinant_corrupted": lambda d: d["invariants"].update(determinant="depends on f"),
        "scalar_corrupted": lambda d: d["invariants"].update(scalar_curvature="-f_second"),
        "kretschmann_corrupted": lambda d: d["invariants"].update(kretschmann="f_second^2"),
        "symbolic_count_reduced": lambda d: d.update(symbolic_check_count=26),
        "critical_check_deleted": lambda d: d["symbolic_checks"].remove("critical_Aperp_zero"),
    }
    caught: dict[str, bool] = {}
    for name, mutation in mutations.items():
        candidate = copy.deepcopy(baseline)
        mutation(candidate)
        try:
            validate(candidate)
        except AssertionError:
            caught[name] = True
        else:
            caught[name] = False
    if not all(caught.values()):
        raise AssertionError(f"uncaught mutations: {[name for name, value in caught.items() if not value]}")
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
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
