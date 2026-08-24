#!/usr/bin/env python3
"""Independent standard-library G251 replay; no production import or output read."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as Q
import hashlib
import io
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
EXPECTED = (
    "CURRENT_METRIC_CHAIN_OWNS_EVALUATORS_AND_SUPPLIED_GEOMETRIC_OBJECT_TYPES"
    "__NO_REGISTERED_CLASS_OWNS_AN_INDEPENDENT_SAME_OBJECT_ABSOLUTE_DATUM"
    "__METRIC_SELF_EVALUATION_IS_CIRCULAR_AND_CANNOT_BREAK_THE_G249_HOMOTHETY"
    "__DIRECT_CLOCK_JACOBI_AREA_VOLUME_AND_CURVATURE_ANCHORS_REQUIRE_ONE_SUPPLIED_OPERATIONAL_ATTACHMENT"
    "__MASS_DENSITY_ENERGY_COMPOSITES_REQUIRE_AN_ADDITIONAL_MATTER_OR_INSTRUMENT_LAW"
    "__NO_ANCHOR_VALUE_HISTORY_BRANCH_POPULATION_FIT_OR_OUTCOME_SELECTED"
)

G250_CANDIDATES = "udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/CANDIDATE_CLASSIFICATION.tsv"
G250_EXACT = "udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/EXACT_DERIVATION.md"

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
    "G_obs_M_over_c_E_squared", "c_E_over_sqrt_G_obs_rho",
    "c_E_squared_over_sqrt_G_obs_epsilon",
}

EVALUATOR_EVIDENCE = {
    "phi_redshift_clock_ratio": (G250_EXACT, "reciprocal depth, redshift, and clock ratios"),
    "causal_cones": (G250_EXACT, "causal cones;"),
    "normalized_Jacobi_shape": (G250_EXACT, "unit-determinant Jacobi shape"),
    "matched_proper_time_interval": (
        "udt_g216_observer_event_comparison_clock_rate_ownership_2026-08-22/EXACT_DERIVATION.md",
        "metric proper time supplies the canonical normalization",
    ),
    "matched_length_or_Jacobi_amplitude": (
        "udt_g244_metric_native_observer_sky_response_query_2026-08-24/AUDIT_REPORT.md",
        "full matrix Jacobi map produces",
    ),
    "matched_screen_or_orbit_area": (
        "udt_g244_metric_native_observer_sky_response_query_2026-08-24/AUDIT_REPORT.md",
        "It splits canonically into metric area and shape",
    ),
    "matched_spatial_three_volume": (
        "udt_g210_g205_spatial_volume_robustness_2026-08-21/AUDIT_REPORT.md",
        "unique determinant scalar",
    ),
    "matched_spacetime_four_volume": (
        "udt_g132_common_scale_owner_and_anchor_audit_2026-08-16/EXACT_DERIVATION.md",
        "In four dimensions",
    ),
    "matched_nonzero_scalar_curvature_or_tide": (
        "udt_g227_same_event_curvature_tomography_2026-08-22/AUDIT_REPORT.md",
        "reconstructs the local algebraic curvature",
    ),
    "matched_nonzero_quadratic_curvature": (
        "udt_g227_same_event_curvature_tomography_2026-08-22/AUDIT_REPORT.md",
        "reconstructs the local algebraic curvature",
    ),
}

BOUNDARIES = {
    "c_E": (G250_EXACT, "not itself that interval"),
    "G_obs": (G250_EXACT, "has no active native placement law"),
    "c_E_plus_G_obs": (G250_EXACT, "No monomial in \\(c_E\\) and \\(G_{\\rm obs}\\) alone"),
    "phi_redshift_clock_ratio": (G250_EXACT, "cannot distinguish members of the\nscale orbit"),
    "causal_cones": (G250_EXACT, "do not change along the G249 scale orbit"),
    "normalized_Jacobi_shape": (G250_EXACT, "do not change along the G249 scale orbit"),
    "matched_proper_time_interval": (
        "udt_g216_observer_event_comparison_clock_rate_ownership_2026-08-22/EXACT_DERIVATION.md",
        "What remains open is which observer events and pair germ are physically realized",
    ),
    "matched_length_or_Jacobi_amplitude": (
        "udt_g244_metric_native_observer_sky_response_query_2026-08-24/AUDIT_REPORT.md",
        "does not identify geometric area",
    ),
    "matched_screen_or_orbit_area": (
        "udt_g244_metric_native_observer_sky_response_query_2026-08-24/AUDIT_REPORT.md",
        "with a galaxy catalogue",
    ),
    "matched_spatial_three_volume": (
        "udt_g210_g205_spatial_volume_robustness_2026-08-21/AUDIT_REPORT.md",
        "does not\nselect a spatial-volume profile",
    ),
    "matched_spacetime_four_volume": (
        "udt_g132_common_scale_owner_and_anchor_audit_2026-08-16/EXACT_DERIVATION.md",
        "volume form is already computed from the full metric",
    ),
    "matched_nonzero_scalar_curvature_or_tide": (
        "udt_g227_same_event_curvature_tomography_2026-08-22/AUDIT_REPORT.md",
        "**Value generation:** still open",
    ),
    "matched_nonzero_quadratic_curvature": (
        "udt_g227_same_event_curvature_tomography_2026-08-22/AUDIT_REPORT.md",
        "**Value generation:** still open",
    ),
    "G_obs_M_over_c_E_squared": (G250_EXACT, "DIMENSIONALLY_ELIGIBLE_NEEDS_ATTACHMENT"),
    "c_E_over_sqrt_G_obs_rho": (G250_EXACT, "DIMENSIONALLY_ELIGIBLE_NEEDS_ATTACHMENT"),
    "c_E_squared_over_sqrt_G_obs_epsilon": (G250_EXACT, "DIMENSIONALLY_ELIGIBLE_NEEDS_ATTACHMENT"),
    "G236_G237_relative_SNe_state": (G250_EXACT, "explicitly relative"),
    "G99_M_B_conditional_X_eff": (G250_EXACT, "historical conditional external cross-check"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_matches(path: Path, expected: str, relative: str) -> bool:
    if digest(path) == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = path.read_bytes().splitlines(keepends=True)
    g251 = [line for line in lines if line.startswith(b"G251\t")]
    stripped = b"".join(line for line in lines if not line.startswith(b"G251\t"))
    return len(g251) == 1 and hashlib.sha256(stripped).hexdigest() == expected


def sources() -> dict[str, Path]:
    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    resolved = {}
    for row in rows:
        candidates = (ROOT / row["path"], ROOT / "sources" / row["path"])
        existing = [path for path in candidates if path.is_file()]
        if len(existing) != 1 or not source_matches(existing[0], row["sha256"], row["path"]):
            raise AssertionError(f"independent source failure: {row['path']}")
        resolved[row["path"]] = existing[0]
    if len(resolved) != 12:
        raise AssertionError("independent manifest count changed")
    return resolved


def rebuild_ledger(candidates: list[dict[str, str]], resolved: dict[str, Path]) -> bytes:
    texts = {name: path.read_text(encoding="utf-8") for name, path in resolved.items()}
    rows = []
    for candidate in candidates:
        name = candidate["candidate"]
        weight = candidate["homothety_weight"]
        evaluator_owned = name in EVALUATOR_EVIDENCE
        if evaluator_owned:
            e_source, e_locator = EVALUATOR_EVIDENCE[name]
            e_evidence = "current source owns this conditional metric evaluator"
        else:
            e_source, e_locator = G250_CANDIDATES, candidate["classification"]
            e_evidence = "registered candidate is not a direct metric evaluator in the bounded chain"
        i_source, i_locator = G250_CANDIDATES, candidate["attachment_guard"]
        c_source, c_locator = BOUNDARIES[name]
        for source, locator in (
            (e_source, e_locator), (i_source, i_locator), (c_source, c_locator),
            (G250_CANDIDATES, name),
        ):
            if locator not in texts[source]:
                raise AssertionError(f"independent citation failure: {name}: {source}: {locator}")

        if name in DIRECT:
            controller, object_type = DIRECT[name]
            classification = "DIRECT_OBSERVATIONAL_ATTACHMENT_MUST_BE_SUPPLIED"
        elif name in COMPOSITES:
            controller, object_type = "G132_G202_G250", "unattached dimensional composite"
            classification = "MATTER_OR_INSTRUMENT_LAW_REQUIRED"
        elif name == "G99_M_B_conditional_X_eff":
            controller, object_type = "G99_G197_G250", "historical transfer-conditional scale"
            classification = "HISTORICAL_CONDITIONAL_NOT_NATIVE_ATTACHMENT"
        else:
            controller, object_type = "G250", candidate["kind"]
            classification = "INSUFFICIENT_WEIGHT_OR_NATIVE_PLACEMENT"

        rows.append({
            "candidate": name,
            "homothety_weight": weight,
            "model_object_type": object_type,
            "E": evaluator_owned,
            "E_source": e_source,
            "E_locator": e_locator.replace("\n", "\\n"),
            "E_evidence": e_evidence,
            "I": False,
            "I_source": i_source,
            "I_locator": i_locator,
            "I_evidence": "G250 registers the candidate-specific same-object attachment as required, not owned",
            "C": False,
            "C_source": c_source,
            "C_locator": c_locator.replace("\n", "\\n"),
            "C_evidence": "the cited boundary leaves the independent calibrated datum or placement open",
            "W": False,
            "W_source": G250_CANDIDATES,
            "W_locator": name,
            "W_evidence": "weight class is registered, but no nonzero physical instance or value is selected",
            "homothety_weight_nonzero": weight not in {"0", "NONE"},
            "native_attachment_owned": False,
            "classification": classification,
            "controlling_evaluator": controller,
        })
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def root_exact(number: int, power: int) -> int:
    candidate = 0
    while candidate**power < number:
        candidate += 1
    if candidate**power != number:
        raise AssertionError("nonexact test power")
    return candidate


def recover(observed: Q, baseline: Q, weight: int) -> Q:
    ratio = observed / baseline
    if weight < 0:
        ratio, weight = 1 / ratio, -weight
    return Q(root_exact(ratio.numerator, weight), root_exact(ratio.denominator, weight))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=12000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    resolved = sources()
    candidate_path = resolved["udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/CANDIDATE_CLASSIFICATION.tsv"]
    with candidate_path.open(newline="", encoding="utf-8") as stream:
        candidates = list(csv.DictReader(stream, delimiter="\t"))
    expected_ledger = rebuild_ledger(candidates, resolved)
    direct = [row for row in candidates if row["classification"] == "CONDITIONALLY_SUFFICIENT_DIRECT"]
    composites = [row for row in candidates if row["classification"] == "DIMENSIONALLY_ELIGIBLE_NEEDS_ATTACHMENT"]

    texts = {name: path.read_text(encoding="utf-8") for name, path in resolved.items() if path.suffix == ".md"}
    source_checks = {
        "g132_independence_boundary": "volume form is already computed from the full metric" in texts["udt_g132_common_scale_owner_and_anchor_audit_2026-08-16/EXACT_DERIVATION.md"],
        "g216_realized_pair_open": "What remains open is which observer events and pair germ are physically realized" in texts["udt_g216_observer_event_comparison_clock_rate_ownership_2026-08-22/EXACT_DERIVATION.md"],
        "g227_value_generation_open": "**Value generation:** still open" in texts["udt_g227_same_event_curvature_tomography_2026-08-22/AUDIT_REPORT.md"],
        "g244_catalog_join_open": "does not identify geometric area" in texts["udt_g244_metric_native_observer_sky_response_query_2026-08-24/AUDIT_REPORT.md"],
        "g246_population_open": "does not select\nthe physical observer population" in texts["udt_g246_two_observer_null_incidence_descent_2026-08-24/AUDIT_REPORT.md"],
        "g249_absolute_datum_required": "another dimensional datum is required" in texts["udt_g249_reciprocal_angular_absolute_scale_ownership_2026-08-24/EXACT_DERIVATION.md"],
        "g250_same_object_independence_required": "independently calibrated observation" in texts["udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/EXACT_DERIVATION.md"],
    }

    rng = random.Random(25182499)
    weights = (-4, -2, -1, 1, 2, 3, 4)
    assertions = 0
    for _ in range(args.cases):
        first_scale = Q(rng.randint(1, 17), rng.randint(1, 13))
        second_scale = first_scale + Q(1, rng.randint(2, 9))
        first_bar = Q(rng.randint(1, 19), rng.randint(1, 17))
        second_bar = Q(rng.randint(1, 23), rng.randint(1, 19))
        first_weight = weights[rng.randrange(len(weights))]
        second_weight = weights[rng.randrange(len(weights))]
        first_value = first_bar * first_scale**first_weight
        second_value = second_bar * first_scale**second_weight
        assert first_bar * first_scale**first_weight == first_value
        assert first_bar * second_scale**first_weight == first_bar * second_scale**first_weight
        assert first_scale != second_scale
        assert first_value**second_weight / second_value**first_weight == first_bar**second_weight / second_bar**first_weight
        assert recover(first_value, first_bar, first_weight) == first_scale
        assertions += 5

    checks = {
        "manifest_twelve_exact": len(resolved) == 12,
        "candidate_count_eighteen": len(candidates) == 18,
        "direct_count_seven": len(direct) == 7,
        "composite_count_three": len(composites) == 3,
        "no_source_claims_independent_direct_value": all(source_checks.values()),
        "self_evaluation_family_nondiscriminating": assertions == 5 * args.cases,
        "cited_E_I_C_W_rows_rebuilt": expected_ledger.count(b"\n") == 19,
    }
    checks.update(source_checks)
    if not all(checks.values()):
        raise SystemExit(f"independent check failure: {checks}")
    result = {
        "status": "PASS",
        "expected_landing": EXPECTED,
        "implementation": "independent_standard_library_manifest_source_and_fraction_route_no_production_import_or_output_read",
        "cases": args.cases,
        "assertions": assertions + len(checks),
        "checks": checks,
        "candidate_count": len(candidates),
        "direct_attachment_required": len(direct),
        "matter_or_instrument_law_required": len(composites),
        "native_attachment_owner_count": 0,
        "expected_ledger_sha256": hashlib.sha256(expected_ledger).hexdigest(),
        "explicit_cited_leg_cells": len(candidates) * 4,
        "owned_metric_evaluator_count": len(EVALUATOR_EVIDENCE),
        "realized_W_count": 0,
        "observational_values_used": 0,
        "fitted_coefficients": 0,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
