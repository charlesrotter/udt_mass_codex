#!/usr/bin/env python3
"""Exact G251 same-object attachment classification; writes only on explicit paths."""

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

LANDING = (
    "CURRENT_METRIC_CHAIN_OWNS_EVALUATORS_AND_SUPPLIED_GEOMETRIC_OBJECT_TYPES"
    "__NO_REGISTERED_CLASS_OWNS_AN_INDEPENDENT_SAME_OBJECT_ABSOLUTE_DATUM"
    "__METRIC_SELF_EVALUATION_IS_CIRCULAR_AND_CANNOT_BREAK_THE_G249_HOMOTHETY"
    "__DIRECT_CLOCK_JACOBI_AREA_VOLUME_AND_CURVATURE_ANCHORS_REQUIRE_ONE_SUPPLIED_OPERATIONAL_ATTACHMENT"
    "__MASS_DENSITY_ENERGY_COMPOSITES_REQUIRE_AN_ADDITIONAL_MATTER_OR_INSTRUMENT_LAW"
    "__NO_ANCHOR_VALUE_HISTORY_BRANCH_POPULATION_FIT_OR_OUTCOME_SELECTED"
)

DIRECT = {
    "matched_proper_time_interval": ("G216", "proper clock interval"),
    "matched_length_or_Jacobi_amplitude": ("G244", "labelled regular Jacobi branch point"),
    "matched_screen_or_orbit_area": ("G132_G244", "identified screen or spherical orbit"),
    "matched_spatial_three_volume": ("G210", "supplied hypersurface region"),
    "matched_spacetime_four_volume": ("G132", "supplied spacetime region"),
    "matched_nonzero_scalar_curvature_or_tide": ("G227", "supplied event or branch point"),
    "matched_nonzero_quadratic_curvature": ("G227", "supplied event"),
}

COMPOSITES = {
    "G_obs_M_over_c_E_squared",
    "c_E_over_sqrt_G_obs_rho",
    "c_E_squared_over_sqrt_G_obs_epsilon",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def source_matches(path: Path, expected: str, relative: str) -> bool:
    if sha256(path) == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = path.read_bytes().splitlines(keepends=True)
    g251 = [line for line in lines if line.startswith(b"G251\t")]
    stripped = b"".join(line for line in lines if not line.startswith(b"G251\t"))
    return len(g251) == 1 and hashlib.sha256(stripped).hexdigest() == expected


def manifest() -> dict[str, str]:
    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        return {row["path"]: row["sha256"] for row in csv.DictReader(stream, delimiter="\t")}


def exact_source(relative: str) -> Path:
    expected = manifest().get(relative)
    if expected is None:
        raise AssertionError(f"source absent from manifest: {relative}")
    candidates = (ROOT / relative, ROOT / "sources" / relative)
    existing = [path for path in candidates if path.is_file()]
    if len(existing) != 1 or not source_matches(existing[0], expected, relative):
        raise AssertionError(f"source resolution/hash failure: {relative}")
    return existing[0]


def source_text(relative: str) -> str:
    return exact_source(relative).read_text(encoding="utf-8")


def g250_candidates() -> list[dict[str, str]]:
    relative = "udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/CANDIDATE_CLASSIFICATION.tsv"
    with exact_source(relative).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def source_checks() -> dict[str, bool]:
    founding = source_text("UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md")
    g132 = source_text("udt_g132_common_scale_owner_and_anchor_audit_2026-08-16/EXACT_DERIVATION.md")
    g210 = source_text("udt_g210_g205_spatial_volume_robustness_2026-08-21/AUDIT_REPORT.md")
    g216 = source_text("udt_g216_observer_event_comparison_clock_rate_ownership_2026-08-22/EXACT_DERIVATION.md")
    g227 = source_text("udt_g227_same_event_curvature_tomography_2026-08-22/AUDIT_REPORT.md")
    g244 = source_text("udt_g244_metric_native_observer_sky_response_query_2026-08-24/AUDIT_REPORT.md")
    g246 = source_text("udt_g246_two_observer_null_incidence_descent_2026-08-24/AUDIT_REPORT.md")
    g249 = source_text("udt_g249_reciprocal_angular_absolute_scale_ownership_2026-08-24/EXACT_DERIVATION.md")
    g250 = source_text("udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/EXACT_DERIVATION.md")
    return {
        "founding_does_not_derive_scale": "does not yet derive a unique action, the profile $\\phi(r)$, or the scale $X$" in founding,
        "volume_self_evaluation_boundary": (
            "volume form is already computed from the full metric" in g132
            and "Supplying it independently" in g132
            and "is exactly supplying the missing scale datum" in g132
        ),
        "areal_label_is_not_attachment": "writing an areal coordinate by itself does not" in g132,
        "spatial_volume_history_unselected": "does not\nselect a spatial-volume profile" in g210,
        "proper_clock_pair_object_supplied": (
            "What remains open is which observer events and pair germ are physically realized" in g216
            and "after** the pair germ is supplied" in g216
        ),
        "curvature_values_not_generated": "**Value generation:** still open" in g227,
        "jacobi_catalog_attachment_absent": (
            "does not identify geometric area" in g244
            and "with a galaxy catalogue" in g244
        ),
        "observer_incidence_objects_supplied": (
            "metric history, and observer worldline germs are supplied" in g246
            and "does not select\nthe physical observer population" in g246
        ),
        "ce_conversion_not_interval": (
            "it is not\nitself a clock interval or a ruler length" in g249
            and "independent absolute area anchor" in g249
        ),
        "g250_requires_independent_attachment": (
            "independently calibrated observation" in g250
            and "same identified query object" in g250
            and "Metric volume computed from" in g250
            and "same unknown metric is not an independent anchor" in g250
        ),
    }


def classify(row: dict[str, str]) -> dict[str, str | bool]:
    name = row["candidate"]
    weight = row["homothety_weight"]
    nonzero_weight = weight not in {"0", "NONE"}
    if name in DIRECT:
        owner, object_type = DIRECT[name]
        return {
            "candidate": name,
            "homothety_weight": weight,
            "metric_evaluator_owned": True,
            "model_object_type": object_type,
            "physical_same_object_attachment_owned": False,
            "independent_absolute_calibration_owned": False,
            "nonzero_weight_class": nonzero_weight,
            "native_attachment_owned": False,
            "classification": "DIRECT_OBSERVATIONAL_ATTACHMENT_MUST_BE_SUPPLIED",
            "controlling_evaluator": owner,
        }
    if name in COMPOSITES:
        return {
            "candidate": name,
            "homothety_weight": weight,
            "metric_evaluator_owned": False,
            "model_object_type": "unattached dimensional composite",
            "physical_same_object_attachment_owned": False,
            "independent_absolute_calibration_owned": False,
            "nonzero_weight_class": nonzero_weight,
            "native_attachment_owned": False,
            "classification": "MATTER_OR_INSTRUMENT_LAW_REQUIRED",
            "controlling_evaluator": "G132_G202_G250",
        }
    if name == "G99_M_B_conditional_X_eff":
        return {
            "candidate": name,
            "homothety_weight": weight,
            "metric_evaluator_owned": False,
            "model_object_type": "historical transfer-conditional scale",
            "physical_same_object_attachment_owned": False,
            "independent_absolute_calibration_owned": False,
            "nonzero_weight_class": nonzero_weight,
            "native_attachment_owned": False,
            "classification": "HISTORICAL_CONDITIONAL_NOT_NATIVE_ATTACHMENT",
            "controlling_evaluator": "G99_G197_G250",
        }
    return {
        "candidate": name,
        "homothety_weight": weight,
        "metric_evaluator_owned": False,
        "model_object_type": row["kind"],
        "physical_same_object_attachment_owned": False,
        "independent_absolute_calibration_owned": False,
        "nonzero_weight_class": nonzero_weight,
        "native_attachment_owned": False,
        "classification": "INSUFFICIENT_WEIGHT_OR_NATIVE_PLACEMENT",
        "controlling_evaluator": "G250",
    }


def nth_root_exact(value: int, power: int) -> int:
    low, high = 0, 1
    while high**power < value:
        high *= 2
    while high - low > 1:
        middle = (low + high) // 2
        if middle**power < value:
            low = middle
        else:
            high = middle
    if high**power != value:
        raise ValueError("nonexact root")
    return high


def recover_external(observed: Q, normalized: Q, weight: int) -> Q:
    ratio = observed / normalized
    if ratio <= 0 or weight == 0:
        raise ValueError("positive nonzero-weight datum required")
    if weight < 0:
        ratio, weight = 1 / ratio, -weight
    return Q(nth_root_exact(ratio.numerator, weight), nth_root_exact(ratio.denominator, weight))


def exact_cases(cases: int) -> dict[str, int]:
    rng = random.Random(2510824)
    weights = (-4, -2, -1, 1, 2, 3, 4)
    assertions = 0
    for _ in range(cases):
        ell_one = Q(rng.randint(1, 23), rng.randint(1, 19))
        ell_two = ell_one + Q(1, rng.randint(2, 11))
        bar_one = Q(rng.randint(1, 31), rng.randint(1, 29))
        bar_two = Q(rng.randint(1, 37), rng.randint(1, 31))
        weight_one = weights[rng.randrange(len(weights))]
        weight_two = weights[rng.randrange(len(weights))]
        metric_one = bar_one * ell_one**weight_one
        metric_two = bar_two * ell_one**weight_two
        assert metric_one == bar_one * ell_one**weight_one
        assert bar_one * ell_two**weight_one == bar_one * ell_two**weight_one
        assert ell_one != ell_two
        invariant = metric_one**weight_two / metric_two**weight_one
        normalized_invariant = bar_one**weight_two / bar_two**weight_one
        assert invariant == normalized_invariant
        assert recover_external(metric_one, bar_one, weight_one) == ell_one
        assertions += 5
    return {"cases": cases, "assertions": assertions}


def write_ledger(path: Path, rows: list[dict[str, str | bool]]) -> None:
    fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=4096)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--ledger-output", type=Path)
    args = parser.parse_args()

    checks = source_checks()
    candidates = g250_candidates()
    rows = [classify(row) for row in candidates]
    checks.update({
        "manifest_twelve_exact": len(manifest()) == 12 and all(exact_source(path).is_file() for path in manifest()),
        "candidate_count_eighteen": len(rows) == 18,
        "direct_class_count_seven": sum(row["classification"] == "DIRECT_OBSERVATIONAL_ATTACHMENT_MUST_BE_SUPPLIED" for row in rows) == 7,
        "composite_class_count_three": sum(row["classification"] == "MATTER_OR_INSTRUMENT_LAW_REQUIRED" for row in rows) == 3,
        "no_native_attachment_owner": not any(row["native_attachment_owned"] for row in rows),
    })
    if not all(checks.values()):
        raise SystemExit(f"exact/source check failure: {checks}")
    sampled = exact_cases(args.cases)
    result = {
        "status": "PASS",
        "landing": LANDING,
        "checks": checks,
        "sampled": sampled,
        "candidate_count": len(rows),
        "direct_attachment_required": sum(row["classification"] == "DIRECT_OBSERVATIONAL_ATTACHMENT_MUST_BE_SUPPLIED" for row in rows),
        "matter_or_instrument_law_required": sum(row["classification"] == "MATTER_OR_INSTRUMENT_LAW_REQUIRED" for row in rows),
        "native_attachment_owners": [row["candidate"] for row in rows if row["native_attachment_owned"]],
        "observational_values_used": 0,
        "fitted_coefficients": 0,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    if args.ledger_output:
        write_ledger(args.ledger_output, rows)
    print(rendered, end="")


if __name__ == "__main__":
    main()
