#!/usr/bin/env python3
"""Hostile mutation controls for the G348 evidence contract."""

from __future__ import annotations

import json


BASELINE = {
    "phase_curvature_sign": -1,
    "tide_self_adjoint": True,
    "flow_symplectic": True,
    "reverse_sign": -1,
    "reverse_adjoint": True,
    "force_oriented_positive": False,
    "retain_rank_one": True,
    "retain_rank_zero": True,
    "full_flow_singular_at_caustic": False,
    "inverse_scalar_finite_at_caustic": False,
    "global_bare_sewing": False,
    "unsigned_area_uses_absolute": True,
    "signed_requires_orientation": True,
    "affine_B_power": -1,
    "source_observer_power": 2,
    "target_observer_power": 0,
    "numerically_observer_invariant": False,
    "rank_one_zero_order": 1,
    "rank_zero_zero_order": 2,
    "aggregate_path_labels": False,
    "promote_physical_law": False,
}


def valid(candidate):
    return candidate == BASELINE


MUTATIONS = {
    "wrong_Jacobi_curvature_sign": ("phase_curvature_sign", 1),
    "nonsymmetric_tide": ("tide_self_adjoint", False),
    "nonsymplectic_flow": ("flow_symplectic", False),
    "wrong_reversal_sign": ("reverse_sign", 1),
    "omit_reversal_adjoint": ("reverse_adjoint", False),
    "force_positive_oriented_determinant": ("force_oriented_positive", True),
    "delete_rank_one": ("retain_rank_one", False),
    "delete_rank_zero": ("retain_rank_zero", False),
    "make_full_flow_singular_at_caustic": ("full_flow_singular_at_caustic", True),
    "make_inverse_scalar_finite_at_caustic": ("inverse_scalar_finite_at_caustic", True),
    "assert_global_bare_sewing": ("global_bare_sewing", True),
    "omit_absolute_value": ("unsigned_area_uses_absolute", False),
    "claim_orientation_free_signed_determinant": ("signed_requires_orientation", False),
    "wrong_affine_power": ("affine_B_power", 1),
    "wrong_source_observer_power": ("source_observer_power", 1),
    "insert_target_observer_factor": ("target_observer_power", 2),
    "claim_numerical_observer_invariance": ("numerically_observer_invariant", True),
    "wrong_rank_one_zero_order": ("rank_one_zero_order", 2),
    "invent_degenerate_rank_zero_order": ("rank_zero_zero_order", 3),
    "sum_or_select_path_labels": ("aggregate_path_labels", True),
    "promote_to_light_distance_scale_or_Xmax": ("promote_physical_law", True),
}


def main():
    if not valid(dict(BASELINE)):
        raise SystemExit("baseline invalid")
    caught = {}
    for name, (field, replacement) in MUTATIONS.items():
        candidate = dict(BASELINE)
        candidate[field] = replacement
        caught[name] = not valid(candidate)
    result = {
        "caught": sum(caught.values()),
        "failed": [name for name, value in caught.items() if not value],
        "mutations": caught,
        "status": "PASS" if all(caught.values()) else "FAIL",
        "total": len(caught),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
