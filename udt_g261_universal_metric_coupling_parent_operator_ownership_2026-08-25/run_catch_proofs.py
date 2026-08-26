#!/usr/bin/env python3
"""Apply and reject preregistered G261 artifact mutations."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent

EXPECTED = {
    "one_universal_physical_metric": "DERIVED_FROM_W4",
    "levi_civita_local_inertial_freefall_evaluator": (
        "DERIVED_FROM_W4_PLUS_EXISTING_METRIC_GEOMETRY"
    ),
    "diffeomorphism_naturality_of_future_law": "SUPPORTED_ACCEPTANCE_REQUIREMENT",
    "metric_only_gravitational_state": "NOT_DERIVED_FROM_W4",
    "symmetric_rank_two_equation": "NOT_DERIVED_FROM_W4",
    "pointwise_locality": "NOT_DERIVED_FROM_W4",
    "at_most_second_metric_order": "NOT_DERIVED_FROM_W4",
    "identity_divergence_freedom": "NOT_DERIVED_FROM_W4",
    "nonidentity_parent_residual": "NOT_DERIVED_FROM_W4",
    "source_history_values": "NOT_DERIVED_FROM_W4",
}


def validate(result: dict[str, object]) -> list[str]:
    errors: list[str] = []
    classes = {row["item"]: row["classification"] for row in result["ownership"]}
    if classes != EXPECTED:
        errors.append("ownership_classification")
    if result["metric_effect"]["primary_metric_form"] != "UNCHANGED":
        errors.append("primary_metric_form")
    if result["metric_effect"]["physical_interpretation"] != "ONE_UNIVERSALLY_COUPLED_LOCAL_GEOMETRY":
        errors.append("local_geometry")
    if not result["G259_specific_candidate_not_adopted"].startswith("NOT_ADOPTED__"):
        errors.append("candidate_adoption")
    if result["W4_status"] != "WORKING_POSIT_NOT_CANON":
        errors.append("W4_status")
    if result["remaining_premise_scope"] != "BROAD_FAMILY_NOT_UNIQUE_SPECIFIC_MECHANISM":
        errors.append("premise_scope")
    return errors


def main() -> None:
    result = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert not validate(result), validate(result)

    def set_class(item: str, value: str):
        def mutate(candidate: dict[str, object]) -> None:
            for row in candidate["ownership"]:
                if row["item"] == item:
                    row["classification"] = value
                    return
            raise AssertionError(item)
        return mutate

    mutations = {
        "promote_naturality_to_generated_operator": set_class(
            "diffeomorphism_naturality_of_future_law", "DERIVED_FROM_W4"
        ),
        "promote_metric_only_state": set_class("metric_only_gravitational_state", "DERIVED_FROM_W4"),
        "promote_rank_two_equation": set_class("symmetric_rank_two_equation", "DERIVED_FROM_W4"),
        "promote_locality": set_class("pointwise_locality", "DERIVED_FROM_W4"),
        "promote_second_order": set_class("at_most_second_metric_order", "DERIVED_FROM_W4"),
        "promote_divergence_freedom": set_class("identity_divergence_freedom", "DERIVED_FROM_W4"),
        "promote_nonidentity_law": set_class("nonidentity_parent_residual", "DERIVED_FROM_W4"),
        "claim_primary_metric_changed": lambda candidate: candidate["metric_effect"].__setitem__(
            "primary_metric_form", "CHANGED"
        ),
        "promote_pair_c_eff_to_local_cone": lambda candidate: candidate["metric_effect"].__setitem__(
            "physical_interpretation", "SECOND_LOCAL_SIGNAL_CONE"
        ),
        "promote_candidate_W5_to_adopted": lambda candidate: candidate.__setitem__(
            "G259_specific_candidate_not_adopted", "ADOPTED"
        ),
    }
    rejected = {}
    rejection_reasons = {}
    for name, mutate in mutations.items():
        candidate = deepcopy(result)
        mutate(candidate)
        errors = validate(candidate)
        rejected[name] = bool(errors)
        rejection_reasons[name] = errors
    output = {
        "status": "PASS" if all(rejected.values()) else "FAIL",
        "baseline_valid": True,
        "mutation_count": len(mutations),
        "rejected_mutation_count": sum(rejected.values()),
        "rejected": rejected,
        "rejection_reasons": rejection_reasons,
        "evidence_scope": "ARTIFACT_GUARD_REGRESSION_NOT_SCIENTIFIC_PROOF",
    }
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
