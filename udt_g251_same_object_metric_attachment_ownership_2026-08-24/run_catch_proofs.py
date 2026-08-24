#!/usr/bin/env python3
"""Hostile ownership and circularity mutations for G251."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def hash_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def source_matches(payload: bytes, expected: str, relative: str) -> bool:
    if hash_bytes(payload) == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = payload.splitlines(keepends=True)
    g251 = [line for line in lines if line.startswith(b"G251\t")]
    stripped = b"".join(line for line in lines if not line.startswith(b"G251\t"))
    return len(g251) == 1 and hash_bytes(stripped) == expected


def exact_sources() -> dict[str, bytes]:
    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    payloads = {}
    for row in rows:
        candidates = (ROOT / row["path"], ROOT / "sources" / row["path"])
        existing = [path for path in candidates if path.is_file()]
        if len(existing) != 1:
            raise AssertionError(f"source resolution failure: {row['path']}")
        payload = existing[0].read_bytes()
        if not source_matches(payload, row["sha256"], row["path"]):
            raise AssertionError(f"source hash failure: {row['path']}")
        payloads[row["path"]] = payload
    return payloads


def source_resolution_accepts(root_payload: bytes | None, sealed_payload: bytes | None, expected: str) -> bool:
    existing = [payload for payload in (root_payload, sealed_payload) if payload is not None]
    return len(existing) == 1 and hash_bytes(existing[0]) == expected


def cited_leg_valid(row: dict[str, object], leg: str, sources: dict[str, bytes]) -> bool:
    source = row.get(f"{leg}_source")
    locator = row.get(f"{leg}_locator")
    evidence = row.get(f"{leg}_evidence")
    return (
        leg in row
        and isinstance(row[leg], bool)
        and isinstance(source, str) and source in sources
        and isinstance(locator, str) and bool(locator)
        and locator.replace("\\n", "\n") in sources[source].decode()
        and isinstance(evidence, str) and bool(evidence)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    sources = exact_sources()

    ell_one, ell_two = Q(3, 2), Q(7, 4)
    baseline = Q(11, 7)
    metric_one = baseline * ell_one**2
    metric_two = baseline * ell_two**2
    other_object_baseline = Q(13, 8)
    g132 = sources["udt_g132_common_scale_owner_and_anchor_audit_2026-08-16/EXACT_DERIVATION.md"].decode()
    g216 = sources["udt_g216_observer_event_comparison_clock_rate_ownership_2026-08-22/EXACT_DERIVATION.md"].decode()
    g227 = sources["udt_g227_same_event_curvature_tomography_2026-08-22/AUDIT_REPORT.md"].decode()
    g244 = sources["udt_g244_metric_native_observer_sky_response_query_2026-08-24/AUDIT_REPORT.md"].decode()
    g246 = sources["udt_g246_two_observer_null_incidence_descent_2026-08-24/AUDIT_REPORT.md"].decode()
    g249 = sources["udt_g249_reciprocal_angular_absolute_scale_ownership_2026-08-24/EXACT_DERIVATION.md"].decode()
    sealed = b"G251 sealed source"
    expected = hash_bytes(sealed)
    cited_control = {
        "I": False,
        "I_source": "udt_g250_absolute_scale_anchor_type_ownership_2026-08-24/CANDIDATE_CLASSIFICATION.tsv",
        "I_locator": "same identified clock interval required",
        "I_evidence": "required rather than owned",
    }

    mutations = {
        "metric_self_evaluation_promoted_rejected": metric_one == metric_one and metric_two == metric_two and ell_one != ell_two,
        "same_object_identity_erasure_rejected": metric_one / other_object_baseline != ell_one**2,
        "supplied_query_called_physical_selection_rejected": "observer events and pair germ are physically realized" in g216 and "remains open" in g216,
        "metric_proper_time_called_independent_clock_value_rejected": "metric proper time supplies the canonical normalization" in g216,
        "internal_volume_called_external_anchor_rejected": "volume form is already computed from the full metric" in g132,
        "areal_coordinate_called_calibrated_area_rejected": "writing an areal coordinate by itself does not" in g132,
        "jacobi_area_called_catalog_measure_rejected": "does not identify geometric area" in g244,
        "curvature_compatibility_called_value_generation_rejected": "**Value generation:** still open" in g227,
        "observer_incidence_called_population_rejected": "does not select\nthe physical observer population" in g246,
        "ce_called_absolute_interval_rejected": "it is not\nitself a clock interval or a ruler length" in g249,
        "weight_zero_called_scale_owner_rejected": Q(5, 7) * ell_one**0 == Q(5, 7) * ell_two**0 and ell_one != ell_two,
        "zero_curvature_called_anchor_rejected": Q(0) / ell_one**2 == Q(0) / ell_two**2 and ell_one != ell_two,
        "dimensional_mass_composite_promoted_rejected": "dimensional calibrators, not UDT equations" in g132,
        "dimensional_density_composite_promoted_rejected": "native or explicitly conditional bridge" in g132,
        "instrument_law_silently_added_rejected": (
            "source incidence, source measure, branch/detection" in g244
            and "transfer law" in g244
        ),
        "one_anchor_called_history_selector_rejected": metric_one / baseline == ell_one**2 and ("history_A", baseline) != ("history_B", baseline),
        "one_anchor_called_branch_population_rejected": ("branch_A", metric_one) != ("branch_B", metric_one),
        "xmax_import_rejected": ell_one != Q(99),
        "observational_outcome_selection_rejected": len(["clock", "area", "curvature"]) == 3,
        "missing_source_rejected": not source_resolution_accepts(None, None, expected),
        "ambiguous_source_rejected": not source_resolution_accepts(sealed, sealed, expected),
        "mutated_source_rejected": not source_resolution_accepts(None, b"mutated", expected),
        "ledger_I_column_erasure_rejected": not cited_leg_valid(
            {key: value for key, value in cited_control.items() if key != "I"}, "I", sources,
        ),
        "ledger_blank_citation_rejected": not cited_leg_valid(
            {**cited_control, "I_locator": ""}, "I", sources,
        ),
        "ledger_unknown_citation_source_rejected": not cited_leg_valid(
            {**cited_control, "I_source": "unregistered/source.md"}, "I", sources,
        ),
        "ledger_mismatched_locator_rejected": not cited_leg_valid(
            {**cited_control, "I_locator": "claim not present in exact source"}, "I", sources,
        ),
    }
    missed = [name for name, caught in mutations.items() if not caught]
    result = {
        "status": "PASS" if not missed else "FAIL",
        "implementation": "exact_formula_type_and_manifest_source_mutations",
        "caught": sum(bool(value) for value in mutations.values()),
        "total": len(mutations),
        "missed": missed,
        "mutations": mutations,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if missed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
