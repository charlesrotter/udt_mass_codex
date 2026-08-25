#!/usr/bin/env python3
"""Hostile mutation catches for G261."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    result = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    classes = {row["item"]: row["classification"] for row in result["ownership"]}
    catches = {
        "promote_naturality_to_generated_operator": classes["diffeomorphism_naturality_of_future_law"]
        == "SUPPORTED_ACCEPTANCE_REQUIREMENT",
        "promote_metric_only_state": classes["metric_only_gravitational_state"]
        == "NOT_DERIVED_FROM_W4",
        "promote_rank_two_equation": classes["symmetric_rank_two_equation"]
        == "NOT_DERIVED_FROM_W4",
        "promote_locality": classes["pointwise_locality"] == "NOT_DERIVED_FROM_W4",
        "promote_second_order": classes["at_most_second_metric_order"] == "NOT_DERIVED_FROM_W4",
        "promote_divergence_freedom": classes["identity_divergence_freedom"]
        == "NOT_DERIVED_FROM_W4",
        "promote_nonidentity_law": classes["nonidentity_parent_residual"] == "NOT_DERIVED_FROM_W4",
        "claim_primary_metric_changed": result["metric_effect"]["primary_metric_form"] == "UNCHANGED",
        "promote_pair_c_eff_to_local_cone": "ONE_UNIVERSALLY_COUPLED_LOCAL_GEOMETRY"
        == result["metric_effect"]["physical_interpretation"],
        "promote_candidate_W5_to_adopted": "NOT_ADOPTED" in result["G259_specific_candidate_not_adopted"],
    }
    output = {
        "status": "PASS" if all(catches.values()) else "FAIL",
        "caught_count": sum(catches.values()),
        "caught": catches,
    }
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    if output["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
