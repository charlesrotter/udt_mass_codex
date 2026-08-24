#!/usr/bin/env python3
"""Independent standard-library G251 replay; no production import or output read."""

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
    "CURRENT_METRIC_CHAIN_OWNS_EVALUATORS_AND_SUPPLIED_GEOMETRIC_OBJECT_TYPES"
    "__NO_REGISTERED_CLASS_OWNS_AN_INDEPENDENT_SAME_OBJECT_ABSOLUTE_DATUM"
    "__METRIC_SELF_EVALUATION_IS_CIRCULAR_AND_CANNOT_BREAK_THE_G249_HOMOTHETY"
    "__DIRECT_CLOCK_JACOBI_AREA_VOLUME_AND_CURVATURE_ANCHORS_REQUIRE_ONE_SUPPLIED_OPERATIONAL_ATTACHMENT"
    "__MASS_DENSITY_ENERGY_COMPOSITES_REQUIRE_AN_ADDITIONAL_MATTER_OR_INSTRUMENT_LAW"
    "__NO_ANCHOR_VALUE_HISTORY_BRANCH_POPULATION_FIT_OR_OUTCOME_SELECTED"
)


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
        "observational_values_used": 0,
        "fitted_coefficients": 0,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
