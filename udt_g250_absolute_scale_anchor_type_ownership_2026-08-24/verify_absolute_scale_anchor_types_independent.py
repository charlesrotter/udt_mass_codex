#!/usr/bin/env python3
"""Independent standard-library exact replay for G250.

Imports neither production code nor production output.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


EXPECTED = (
    "ONE_MATCHED_NONZERO_HOMOTHETY_WEIGHT_ANCHOR_CONDITIONALLY_FIXES_THE_SINGLE_G249_SCALE"
    "__ADDITIONAL_INDEPENDENT_ANCHORS_TEST_THE_SUPPLIED_DIMENSIONLESS_HISTORY_RATHER_THAN_ADD_SCALE_PARAMETERS"
    "__CE_GOBS_RECIPROCAL_REDSHIFT_AND_RELATIVE_SNE_STATE_DO_NOT_FIX_ABSOLUTE_SCALE"
    "__MASS_DENSITY_ENERGY_COMPOSITES_ARE_DIMENSIONAL_CANDIDATES_ONLY_UNTIL_A_METRIC_ATTACHMENT_LAW_IS_SUPPLIED"
    "__G99_XEFF_REMAINS_HISTORICAL_TRANSFER_CONDITIONAL_NOT_NATIVE_G249_INPUT"
    "__NO_ANCHOR_VALUE_HISTORY_PROFILE_OR_OUTCOME_SELECTED"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def independent_exact_source(relative: str) -> Path:
    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        manifest = {row["path"]: row["sha256"] for row in csv.DictReader(stream, delimiter="\t")}
    if relative not in manifest:
        raise AssertionError(f"missing independent manifest source: {relative}")
    candidates = (ROOT / relative, ROOT / "sources" / relative)
    existing = [path for path in candidates if path.is_file()]
    if len(existing) != 1 or sha256(existing[0]) != manifest[relative]:
        raise AssertionError(f"independent exact-source failure: {relative}")
    return existing[0]


def independent_tsv(relative: str, key: str) -> dict[str, dict[str, str]]:
    with independent_exact_source(relative).open(newline="", encoding="utf-8") as stream:
        return {row[key]: row for row in csv.DictReader(stream, delimiter="\t")}


def independent_provenance_checks() -> dict[str, bool]:
    g236 = independent_tsv(
        "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/PREMISE_LEDGER.tsv",
        "object",
    )["one additive offset per catalog"]
    g237 = independent_tsv(
        "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/PREMISE_LEDGER.tsv",
        "object",
    )["release_offsets"]
    g99 = independent_tsv(
        "udt_observed_middle_regime_pair_calibration_2026-08-15/PREMISE_LEDGER.tsv",
        "item",
    )
    g132 = independent_exact_source(
        "udt_g132_common_scale_owner_and_anchor_audit_2026-08-16/EXACT_DERIVATION.md"
    ).read_text(encoding="utf-8")
    g202 = independent_exact_source(
        "udt_g202_quiet_overlap_profile_anchor_classification_2026-08-21/EXACT_DERIVATION.md"
    ).read_text(encoding="utf-8")
    return {
        "relative_state_cannot_supply_deleted_zero_point": (
            g236["status"] == "DECLARED_NUISANCE_CALIBRATION"
            and "distance-scale zero point" in g236["role"]
            and g237["status"] == "FREE_AND_PROFILED"
            and g237["open_scope"] == "absolute R normalization"
        ),
        "dimensional_composite_requires_attachment": (
            "These are dimensional calibrators, not UDT equations." in g132
            and "A native or explicitly conditional bridge" in g132
            and "These are dimensional candidates only." in g202
            and "Neither the proportionality, the relevant mass/density" in g202
        ),
        "historical_transfer_condition_is_not_native_metric_ownership": (
            g99["profile_family"]["value_or_rule"] == "P1 only"
            and "external M_B anchor" in g99["absolute_scale"]["status"]
            and "X_eff" in g99["absolute_scale"]["value_or_rule"]
            and g99["luminosity_readout"]["role"] == "effective observational transfer"
        ),
    }


def solve_square(matrix, target):
    size = len(matrix)
    augmented = [[Q(matrix[row][column]) for column in range(size)] + [Q(target[row])] for row in range(size)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if augmented[row][column] != 0), None)
        if pivot is None:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        factor = augmented[column][column]
        augmented[column] = [value / factor for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [augmented[row][j] - factor * augmented[column][j] for j in range(size + 1)]
    return tuple(augmented[row][-1] for row in range(size))


def dimensions_solution(columns):
    matrix = [[column[row] for column in columns] for row in range(3)]
    return solve_square(matrix, (1, 0, 0))


def nth_root(value, power):
    def root_int(number):
        low, high = 0, 1
        while high**power < number:
            high *= 2
        while high - low > 1:
            middle = (low + high) // 2
            if middle**power < number:
                low = middle
            else:
                high = middle
        if high**power != number:
            raise AssertionError("nonexact test root")
        return high
    return Q(root_int(value.numerator), root_int(value.denominator))


def recover(observed, normalized, weight):
    if weight == 0 or normalized == 0:
        raise ValueError("nonzero weight and normalized value required")
    ratio = observed / normalized
    if weight < 0:
        ratio = 1 / ratio
        weight = -weight
    return nth_root(ratio, weight)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=12000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    c_e = (Q(1), Q(0), Q(-1))
    g_obs = (Q(3), Q(-1), Q(-2))
    mass = (Q(0), Q(1), Q(0))
    density = (Q(-3), Q(1), Q(0))
    energy = (Q(-1), Q(1), Q(-2))

    # Two columns cannot span a three-row target here: exhaustive bounded proof
    # is supplemented by the exact mass equation forcing the G exponent to zero.
    ce_g_candidates = []
    for a_num in range(-24, 25):
        for b_num in range(-24, 25):
            a, b = Q(a_num, 4), Q(b_num, 4)
            exponents = tuple(a * c_e[i] + b * g_obs[i] for i in range(3))
            if exponents == (Q(1), Q(0), Q(0)):
                ce_g_candidates.append((a, b))
    assert ce_g_candidates == []
    forced_b = Q(0)  # -b=0 from the mass row.
    forced_a = -2 * forced_b  # -a-2b=0 from the time row.
    assert forced_a * c_e[0] + forced_b * g_obs[0] == 0  # not target length exponent one.

    solutions = {
        "mass": dimensions_solution((c_e, g_obs, mass)),
        "density": dimensions_solution((c_e, g_obs, density)),
        "energy_density": dimensions_solution((c_e, g_obs, energy)),
    }
    expected_solutions = {
        "mass": (Q(-2), Q(1), Q(1)),
        "density": (Q(1), Q(-1, 2), Q(-1, 2)),
        "energy_density": (Q(2), Q(-1, 2), Q(-1, 2)),
    }
    assert solutions == expected_solutions

    rng = random.Random(25082451)
    weights = (-4, -3, -2, -1, 1, 2, 3, 4)
    assertions = 0
    zero_weight_rejections = 0
    zero_value_rejections = 0
    nonpositive_ratio_rejections = 0
    inconsistent_second_anchor_rejections = 0
    for _ in range(args.cases):
        ell = Q(rng.randint(1, 31), rng.randint(1, 29))
        bar_one = Q(rng.randint(1, 37), rng.randint(1, 31))
        bar_two = Q(rng.randint(1, 41), rng.randint(1, 37))
        weight_one = weights[rng.randrange(len(weights))]
        weight_two = weights[rng.randrange(len(weights))]
        obs_one = bar_one * ell**weight_one
        obs_two = bar_two * ell**weight_two
        assert recover(obs_one, bar_one, weight_one) == ell
        assertions += 1
        assert (obs_one / bar_one) ** weight_two == (obs_two / bar_two) ** weight_one
        assertions += 1
        mutant = obs_two * Q(3, 2)
        if (obs_one / bar_one) ** weight_two != (mutant / bar_two) ** weight_one:
            inconsistent_second_anchor_rejections += 1
        try:
            recover(bar_one, bar_one, 0)
        except ValueError:
            zero_weight_rejections += 1
        try:
            recover(obs_one, Q(0), weight_one)
        except ValueError:
            zero_value_rejections += 1
        try:
            recover(-obs_one, bar_one, weight_one)
        except (ValueError, AssertionError):
            nonpositive_ratio_rejections += 1

    checks = {
        "ce_gobs_no_length": not ce_g_candidates,
        "mass_density_energy_exponents": solutions == expected_solutions,
        "all_nonzero_weight_recoveries": assertions == 2 * args.cases,
        "zero_weight_rejected": zero_weight_rejections == args.cases,
        "zero_normalized_value_rejected": zero_value_rejections == args.cases,
        "nonpositive_ratio_rejected": nonpositive_ratio_rejections == args.cases,
        "inconsistent_second_anchor_rejected": inconsistent_second_anchor_rejections == args.cases,
    }
    checks.update(independent_provenance_checks())
    assert all(checks.values())
    result = {
        "status": "PASS",
        "expected_landing": EXPECTED,
        "implementation": "standard_library_fraction_and_exact_source_manifest_no_production_import_or_output_read",
        "provenance_sources_verified": 5,
        "cases": args.cases,
        "assertions": assertions + sum(checks.values()),
        "checks": checks,
        "dimension_solutions": {name: [str(value) for value in values] for name, values in solutions.items()},
        "zero_weight_rejections": zero_weight_rejections,
        "zero_value_rejections": zero_value_rejections,
        "nonpositive_ratio_rejections": nonpositive_ratio_rejections,
        "inconsistent_second_anchor_rejections": inconsistent_second_anchor_rejections,
        "observational_values_used": 0,
        "fitted_coefficients": 0,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
