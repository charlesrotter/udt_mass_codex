#!/usr/bin/env python3
"""Hostile payload mutations for the G224 contract verifier."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from verify_package import contained_source_path, validate_payloads


ROOT = Path(__file__).resolve().parent


def main() -> None:
    d0 = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    i0 = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    f0 = json.loads((ROOT / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    mutations = [
        ("derivation_status", "d", "status", "FAIL"),
        ("outcome", "d", "preregistered_outcome", "A"),
        ("symbolic_count", "d", "symbolic_checks", 23),
        ("metric_pairing", "d", "metric_clock_pairing_nondegenerate", False),
        ("unique_switch", "d", "shared_event_vertical_switch_unique", False),
        ("affine_invariance", "d", "independent_affine_rescaling_invariant", False),
        ("clock_invariance", "d", "common_clock_recalibration_invariant", False),
        ("vertex_cocycle", "d", "vertex_identity_inverse_cocycle", False),
        ("inverse_representation", "d", "vertical_carry_inverse_clock_representation", False),
        ("direct_promotion", "d", "independent_direct_relation_constrained", True),
        ("direction_promotion", "d", "ambient_null_directions_identified", True),
        ("screen_promotion", "d", "screen_map_derived", True),
        ("distinct_normalization", "d", "distinct_event_abstract_line_normalization_possible", False),
        ("distinct_composition", "d", "distinct_event_physical_composition_derived", True),
        ("landing", "d", "landing", "PROMOTED"),
        ("independent_cases", "i", "cases", 19999),
        ("independent_assertions", "i", "exact_rational_assertions", 220002),
        ("direct_counterexample", "i", "independent_direct_edge_counterexample", False),
        ("direction_control", "i", "different_null_direction_control", False),
        ("preregistration_commit", "f", "preregistration_commit", "UNFROZEN"),
        ("final_grade", "f", "grade", "PENDING"),
        ("observation_repair", "f", "distinct_event_observation_repaired", False),
        ("review_grade", "f", "fresh_external_review", "ACCEPT_BOUNDED_LANDING"),
        ("scientific_grade", "f", "external_scientific_grade", "A+"),
        ("followup_regression", "f", "repair_followup_review", "PENDING"),
    ]
    rejected: list[str] = []
    for name, target, field, value in mutations:
        d, i, f = copy.deepcopy(d0), copy.deepcopy(i0), copy.deepcopy(f0)
        {"d": d, "i": i, "f": f}[target][field] = value
        try:
            validate_payloads(d, i, f)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(f"mutation survived: {name}")

    path_mutations = ("/tmp/outside_intake", "../outside_intake")
    path_rejected: list[str] = []
    for raw in path_mutations:
        try:
            contained_source_path(raw)
        except AssertionError:
            path_rejected.append(raw)
        else:
            raise AssertionError(f"manifest path mutation survived: {raw}")

    result = {
        "status": "PASS",
        "mutations_attempted": len(mutations),
        "mutations_rejected": len(rejected),
        "rejected": rejected,
        "manifest_path_mutations_attempted": len(path_mutations),
        "manifest_path_mutations_rejected": len(path_rejected),
    }
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(f"PASS: G224 catch proofs; {len(rejected)}/{len(mutations)} mutations rejected")


if __name__ == "__main__":
    main()
