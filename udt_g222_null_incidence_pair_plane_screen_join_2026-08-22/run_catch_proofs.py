#!/usr/bin/env python3
"""Payload-contract mutation guard for the bounded G222 landing."""

from __future__ import annotations

import copy
import json


if not __debug__:
    raise RuntimeError("G222 evidence requires Python assertions; optimized mode is forbidden")


def canonical() -> dict[str, object]:
    return {
        "area_definition": "-g(J,K)",
        "area_conserved": True,
        "pair_determinant": "-a^2",
        "completed_density": "a",
        "boundary_ratio": "W_A/W_B",
        "target_depth": "-log(r_AB)",
        "screen_map": "X-g(X,J)/g(K,J)*K",
        "screen_isometry": True,
        "screen_representative_independent": True,
        "null_shift_independent": True,
        "global_coordinate_requires_closedness": True,
        "zero_area_rejected": True,
        "clock_turn_not_pair_degeneracy": True,
        "screen_caustic_separate": True,
        "null_query_typed": True,
        "Jacobi_not_scalarized": True,
        "full_pair_plane_constructed_conditionally": True,
        "physical_history_selected": False,
    }


def valid(payload: dict[str, object]) -> bool:
    return bool(
        payload.get("area_definition") == "-g(J,K)"
        and payload.get("area_conserved") is True
        and payload.get("pair_determinant") == "-a^2"
        and payload.get("completed_density") == "a"
        and payload.get("boundary_ratio") == "W_A/W_B"
        and payload.get("target_depth") == "-log(r_AB)"
        and payload.get("screen_map") == "X-g(X,J)/g(K,J)*K"
        and payload.get("screen_isometry") is True
        and payload.get("screen_representative_independent") is True
        and payload.get("null_shift_independent") is True
        and payload.get("global_coordinate_requires_closedness") is True
        and payload.get("zero_area_rejected") is True
        and payload.get("clock_turn_not_pair_degeneracy") is True
        and payload.get("screen_caustic_separate") is True
        and payload.get("null_query_typed") is True
        and payload.get("Jacobi_not_scalarized") is True
        and payload.get("full_pair_plane_constructed_conditionally") is True
        and payload.get("physical_history_selected") is False
    )


def catches() -> dict[str, object]:
    base = canonical()
    if not valid(base):
        raise RuntimeError("canonical G222 payload rejected")
    mutations = {
        "reverse_area_sign": ("area_definition", "g(J,K)"),
        "drop_area_conservation": ("area_conserved", False),
        "wrong_pair_determinant": ("pair_determinant", "-T^2*a^2"),
        "use_clock_as_ruler_density": ("completed_density", "T"),
        "invert_boundary_ratio": ("boundary_ratio", "W_B/W_A"),
        "reverse_target_depth": ("target_depth", "log(r_AB)"),
        "wrong_screen_projection_sign": ("screen_map", "X+g(X,J)/g(K,J)*K"),
        "drop_screen_isometry": ("screen_isometry", False),
        "choose_screen_representative": ("screen_representative_independent", False),
        "make_null_shift_physical": ("null_shift_independent", False),
        "assert_global_ruler_coordinate": ("global_coordinate_requires_closedness", False),
        "allow_zero_area_rank_two": ("zero_area_rejected", False),
        "call_clock_turn_pair_degeneracy": ("clock_turn_not_pair_degeneracy", False),
        "call_screen_caustic_pair_degeneracy": ("screen_caustic_separate", False),
        "promote_null_to_universal_protocol": ("null_query_typed", False),
        "collapse_Jacobi_to_clock_scalar": ("Jacobi_not_scalarized", False),
        "withdraw_conditional_pair_plane": ("full_pair_plane_constructed_conditionally", False),
        "select_physical_history": ("physical_history_selected", True),
    }
    caught: dict[str, bool] = {}
    for name, (field, value) in mutations.items():
        mutant = copy.deepcopy(base)
        mutant[field] = value
        caught[name] = not valid(mutant)
    if not all(caught.values()):
        raise RuntimeError({name: value for name, value in caught.items() if not value})
    return {
        "canonical_pass": True,
        "payload_contract_mutations": len(caught),
        "all_contract_mutants_rejected": True,
        "catches": caught,
    }


if __name__ == "__main__":
    print(json.dumps(catches(), indent=2, sort_keys=True))
