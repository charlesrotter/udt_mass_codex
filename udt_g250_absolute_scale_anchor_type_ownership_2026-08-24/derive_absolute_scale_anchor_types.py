#!/usr/bin/env python3
"""Exact G250 anchor-type classification; writes only with explicit output paths."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as Q
import json
from math import isqrt
from pathlib import Path
import random

import sympy as sp


LANDING = (
    "ONE_MATCHED_NONZERO_HOMOTHETY_WEIGHT_ANCHOR_CONDITIONALLY_FIXES_THE_SINGLE_G249_SCALE"
    "__ADDITIONAL_INDEPENDENT_ANCHORS_TEST_THE_SUPPLIED_DIMENSIONLESS_HISTORY_RATHER_THAN_ADD_SCALE_PARAMETERS"
    "__CE_GOBS_RECIPROCAL_REDSHIFT_AND_RELATIVE_SNE_STATE_DO_NOT_FIX_ABSOLUTE_SCALE"
    "__MASS_DENSITY_ENERGY_COMPOSITES_ARE_DIMENSIONAL_CANDIDATES_ONLY_UNTIL_A_METRIC_ATTACHMENT_LAW_IS_SUPPLIED"
    "__G99_XEFF_REMAINS_HISTORICAL_TRANSFER_CONDITIONAL_NOT_NATIVE_G249_INPUT"
    "__NO_ANCHOR_VALUE_HISTORY_PROFILE_OR_OUTCOME_SELECTED"
)


# Dimension vectors use the order (L, M, T).
DIMENSIONS = {
    "c_E": (Q(1), Q(0), Q(-1)),
    "G_obs": (Q(3), Q(-1), Q(-2)),
    "M": (Q(0), Q(1), Q(0)),
    "rho": (Q(-3), Q(1), Q(0)),
    "epsilon": (Q(-1), Q(1), Q(-2)),
}
TARGET_LENGTH = (Q(1), Q(0), Q(0))


CANDIDATES = [
    ("c_E", "conversion", "NONE", "OBSERVED", "INSUFFICIENT_CONVERSION_ONLY", "not an interval"),
    ("G_obs", "constant", "NONE", "OBSERVED", "INSUFFICIENT_NO_NATIVE_PLACEMENT", "mass dimension remains"),
    ("c_E_plus_G_obs", "constant_pair", "NONE", "OBSERVED", "INSUFFICIENT_NO_LENGTH_MONOMIAL", "exact dimensional no-solution"),
    ("phi_redshift_clock_ratio", "dimensionless", "0", "DERIVED_CONDITIONAL", "INSUFFICIENT_WEIGHT_ZERO", "preserved by homothety"),
    ("causal_cones", "dimensionless_structure", "0", "DERIVED_GEOMETRIC", "INSUFFICIENT_WEIGHT_ZERO", "preserved by positive homothety"),
    ("normalized_Jacobi_shape", "dimensionless_shape", "0", "DERIVED_CONDITIONAL_G244_G249", "INSUFFICIENT_WEIGHT_ZERO", "unit determinant shape"),
    ("matched_proper_time_interval", "direct_metric", "1", "CONDITIONAL_ANCHOR_CLASS", "CONDITIONALLY_SUFFICIENT_DIRECT", "same identified clock interval required"),
    ("matched_length_or_Jacobi_amplitude", "direct_metric", "1", "CONDITIONAL_ANCHOR_CLASS", "CONDITIONALLY_SUFFICIENT_DIRECT", "same branch point and normalization required"),
    ("matched_screen_or_orbit_area", "direct_metric", "2", "CONDITIONAL_ANCHOR_CLASS", "CONDITIONALLY_SUFFICIENT_DIRECT", "same screen or orbit required"),
    ("matched_spatial_three_volume", "direct_metric", "3", "CONDITIONAL_ANCHOR_CLASS", "CONDITIONALLY_SUFFICIENT_DIRECT", "same region and hypersurface required"),
    ("matched_spacetime_four_volume", "direct_metric", "4", "CONDITIONAL_ANCHOR_CLASS", "CONDITIONALLY_SUFFICIENT_DIRECT", "same spacetime region required"),
    ("matched_nonzero_scalar_curvature_or_tide", "direct_metric_invariant", "-2", "CONDITIONAL_ANCHOR_CLASS", "CONDITIONALLY_SUFFICIENT_DIRECT", "same event or branch and nonzero invariant required"),
    ("matched_nonzero_quadratic_curvature", "direct_metric_invariant", "-4", "CONDITIONAL_ANCHOR_CLASS", "CONDITIONALLY_SUFFICIENT_DIRECT", "same event and nonzero invariant required"),
    ("G_obs_M_over_c_E_squared", "dimensional_composite", "1", "OBSERVED_CANDIDATE_G132_G202", "DIMENSIONALLY_ELIGIBLE_NEEDS_ATTACHMENT", "coefficient and metric placement unowned"),
    ("c_E_over_sqrt_G_obs_rho", "dimensional_composite", "1", "OBSERVED_CANDIDATE_G132_G202", "DIMENSIONALLY_ELIGIBLE_NEEDS_ATTACHMENT", "density identity coefficient and placement unowned"),
    ("c_E_squared_over_sqrt_G_obs_epsilon", "dimensional_composite", "1", "OBSERVED_CANDIDATE_G132", "DIMENSIONALLY_ELIGIBLE_NEEDS_ATTACHMENT", "energy-density identity coefficient and placement unowned"),
    ("G236_G237_relative_SNe_state", "observed_relative_state", "0", "OBSERVED_PROCESSED_CONDITIONAL", "INSUFFICIENT_ABSOLUTE_ZERO_POINT_REMOVED", "release offsets remove absolute normalization"),
    ("G99_M_B_conditional_X_eff", "historical_absolute_scale", "1", "OBSERVED_CONDITIONAL_HISTORICAL", "CONDITIONAL_EXTERNAL_CROSSCHECK_NOT_NATIVE_INPUT", "depends on P1 external M_B and imported transfer"),
]


def solve_dimensions(names: tuple[str, ...]):
    matrix = sp.Matrix([[sp.Rational(value.numerator, value.denominator) for value in DIMENSIONS[name]] for name in names]).T
    target = sp.Matrix(TARGET_LENGTH)
    symbols = sp.symbols(f"a0:{len(names)}")
    solution = sp.linsolve((matrix, target), symbols)
    if solution is sp.EmptySet or solution == sp.EmptySet:
        return None
    tuples = list(solution)
    if len(tuples) != 1 or any(item.free_symbols for item in tuples[0]):
        return "NONUNIQUE"
    return tuple(Q(int(item.p), int(item.q)) for item in tuples[0])


def integer_nth_root_exact(value: int, n: int) -> int:
    if value < 0 or n <= 0:
        raise ValueError("positive root required")
    if value in (0, 1):
        return value
    low, high = 0, 1
    while high**n < value:
        high *= 2
    while high - low > 1:
        middle = (low + high) // 2
        if middle**n < value:
            low = middle
        else:
            high = middle
    if high**n != value:
        raise ValueError("not an exact integer power")
    return high


def rational_nth_root_exact(value: Q, n: int) -> Q:
    return Q(integer_nth_root_exact(value.numerator, n), integer_nth_root_exact(value.denominator, n))


def recover_scale(q_observed: Q, q_bar: Q, weight: int) -> Q:
    if weight == 0 or q_bar == 0:
        raise ValueError("weight and normalized value must be nonzero")
    ratio = q_observed / q_bar
    if ratio <= 0:
        raise ValueError("positive homothety ratio required")
    if weight < 0:
        ratio = 1 / ratio
        weight = -weight
    return rational_nth_root_exact(ratio, weight)


def exact_checks() -> dict[str, bool]:
    ell, q1, q2 = sp.symbols("ell q1 q2", positive=True)
    w1, w2 = sp.symbols("w1 w2", integer=True, nonzero=True)
    two_anchor = sp.simplify(((ell**w1 * q1) / q1) ** w2 - ((ell**w2 * q2) / q2) ** w1)
    return {
        "ce_gobs_no_length_solution": solve_dimensions(("c_E", "G_obs")) is None,
        "ce_gobs_mass_unique": solve_dimensions(("c_E", "G_obs", "M")) == (Q(-2), Q(1), Q(1)),
        "ce_gobs_density_unique": solve_dimensions(("c_E", "G_obs", "rho")) == (Q(1), Q(-1, 2), Q(-1, 2)),
        "ce_gobs_energy_density_unique": solve_dimensions(("c_E", "G_obs", "epsilon")) == (Q(2), Q(-1, 2), Q(-1, 2)),
        "two_anchor_consistency_identity": two_anchor == 0,
        "relative_sne_is_registered_zero_point_free": next(row for row in CANDIDATES if row[0] == "G236_G237_relative_SNe_state")[4] == "INSUFFICIENT_ABSOLUTE_ZERO_POINT_REMOVED",
        "g99_is_not_native_input": next(row for row in CANDIDATES if row[0] == "G99_M_B_conditional_X_eff")[4] == "CONDITIONAL_EXTERNAL_CROSSCHECK_NOT_NATIVE_INPUT",
    }


def run_weight_cases(cases: int) -> dict[str, int]:
    rng = random.Random(2500824)
    assertions = 0
    second_anchor_checks = 0
    negative_weight_checks = 0
    weights = (-4, -2, -1, 1, 2, 3, 4)
    for _ in range(cases):
        ell = Q(rng.randint(1, 19), rng.randint(1, 17))
        q1 = Q(rng.randint(1, 29), rng.randint(1, 23))
        q2 = Q(rng.randint(1, 31), rng.randint(1, 27))
        w1 = weights[rng.randrange(len(weights))]
        w2 = weights[rng.randrange(len(weights))]
        observed1 = q1 * ell**w1
        observed2 = q2 * ell**w2
        assert recover_scale(observed1, q1, w1) == ell
        assertions += 1
        ratio1 = observed1 / q1
        ratio2 = observed2 / q2
        assert ratio1**w2 == ratio2**w1
        assertions += 1
        second_anchor_checks += 1
        if w1 < 0:
            negative_weight_checks += 1
    return {
        "cases": cases,
        "assertions": assertions,
        "second_anchor_checks": second_anchor_checks,
        "negative_weight_checks": negative_weight_checks,
    }


def write_tsv(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("candidate", "kind", "homothety_weight", "premise_status", "classification", "attachment_guard"))
        writer.writerows(CANDIDATES)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=4096)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--classification-output", type=Path)
    args = parser.parse_args()

    checks = exact_checks()
    if not all(checks.values()):
        raise SystemExit(f"exact check failure: {checks}")
    sampled = run_weight_cases(args.cases)
    direct = [row[0] for row in CANDIDATES if row[4] == "CONDITIONALLY_SUFFICIENT_DIRECT"]
    insufficient = [row[0] for row in CANDIDATES if row[4].startswith("INSUFFICIENT")]
    bridge = [row[0] for row in CANDIDATES if row[4] == "DIMENSIONALLY_ELIGIBLE_NEEDS_ATTACHMENT"]
    result = {
        "status": "PASS",
        "landing": LANDING,
        "exact_checks": checks,
        "sampled": sampled,
        "candidate_count": len(CANDIDATES),
        "direct_conditional_calibrators": direct,
        "dimensionally_eligible_needing_attachment": bridge,
        "insufficient_without_new_data_or_bridge": insufficient,
        "g99_grade": "CONDITIONAL_EXTERNAL_CROSSCHECK_NOT_NATIVE_INPUT",
        "g236_g237_grade": "INSUFFICIENT_ABSOLUTE_ZERO_POINT_REMOVED",
        "observational_values_used": 0,
        "fitted_coefficients": 0,
        "outcome_status": "OUTCOME_INDEPENDENT_DRIVER_NOT_STRICTLY_BLINDED_PER_EXECUTION_NOTE",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    if args.classification_output:
        write_tsv(args.classification_output)
    print(rendered, end="")


if __name__ == "__main__":
    main()
