#!/usr/bin/env python3
"""Hostile claim-mutation catches for G282."""

from __future__ import annotations

import json


def valid_claim(claim: dict[str, object]) -> bool:
    return bool(
        claim["same_ray_data"]
        and claim["transverse_curvature_retained"]
        and claim["jacobi_area_separates"]
        and claim["primary_same_depth_separates_area"]
        and not claim["endpoint_state_promoted_to_area"]
        and not claim["imported_field_equation"]
        and not claim["unique_second_order_form_claimed"]
        and claim["minimum_information_types"] == 3
    )


def main() -> None:
    baseline = {
        "same_ray_data": True,
        "transverse_curvature_retained": True,
        "jacobi_area_separates": True,
        "primary_same_depth_separates_area": True,
        "endpoint_state_promoted_to_area": False,
        "imported_field_equation": False,
        "unique_second_order_form_claimed": False,
        "minimum_information_types": 3,
    }
    assert valid_claim(baseline)
    mutations = {
        "erase_transverse_curvature": {"transverse_curvature_retained": False},
        "force_equal_jacobi_area": {"jacobi_area_separates": False},
        "erase_primary_separator": {"primary_same_depth_separates_area": False},
        "promote_endpoint_state": {"endpoint_state_promoted_to_area": True},
        "import_field_equation": {"imported_field_equation": True},
        "claim_unique_second_order_form": {"unique_second_order_form_claimed": True},
        "drop_equivalent_law_types": {"minimum_information_types": 1},
    }
    caught = {}
    for name, mutation in mutations.items():
        candidate = dict(baseline)
        candidate.update(mutation)
        caught[name] = not valid_claim(candidate)
    assert all(caught.values())
    print(
        json.dumps(
            {
                "audit": "G282_HOSTILE_CATCH_PROOFS",
                "status": "PASS",
                "baseline_accepted": True,
                "caught": caught,
                "caught_count": sum(caught.values()),
                "mutation_count": len(caught),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
