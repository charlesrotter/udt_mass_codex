#!/usr/bin/env python3
"""Fail-closed regression catches for the preregistered SNe replay policy."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from replay_m3_unchanged import compare


HERE = Path(__file__).resolve().parent

EXPECTED = {
    "catalog": "Data/Pantheon+SH0ES.dat",
    "covariance": "Data/Pantheon+SH0ES_STAT+SYS.cov",
    "z_cut": 0.023,
    "profiles": ["P1", "P2", "P3"],
    "anchor_M_B": -19.253,
    "anchor_error": 0.027,
    "extra_native_parameters": 0,
    "external_probe_data": [],
    "P1_role": "OBSERVER_PAIR_SNE_ONLY",
    "c_eff_role": "CONDITIONAL_PAIR_CONE_NOT_SIGNAL_SPEED",
    "angular_mixing": "LIVE_UPSTREAM_NOT_ZEROED",
    "native_correction_owner": "NONE",
    "formula_change_from_retyping": False,
}


def validate(state: dict[str, object]) -> None:
    if state != EXPECTED:
        changed = sorted(key for key in EXPECTED if state.get(key) != EXPECTED[key])
        raise AssertionError(f"policy mutation rejected: {changed}")


def run() -> dict[str, object]:
    mutations = {
        "changed_catalog": ("catalog", "Data/other.dat"),
        "changed_covariance": ("covariance", "Data/diagonal_only.cov"),
        "changed_cut": ("z_cut", 0.01),
        "changed_menu": ("profiles", ["P1", "P2", "P3", "P4"]),
        "changed_anchor": ("anchor_M_B", -19.30),
        "changed_anchor_error": ("anchor_error", 0.0),
        "extra_shape_coefficient": ("extra_native_parameters", 1),
        "CMB_data_import": ("external_probe_data", ["CMB"]),
        "BAO_data_import": ("external_probe_data", ["BAO"]),
        "P1_centered_lapse_promotion": ("P1_role", "CENTERED_COMPLETE_LAPSE"),
        "c_eff_signal_promotion": ("c_eff_role", "MATERIAL_SIGNAL_SPEED"),
        "orchestra_zeroing": ("angular_mixing", "ZERO"),
        "unowned_correction": ("native_correction_owner", "ASSUMED"),
        "semantic_formula_retune": ("formula_change_from_retyping", True),
    }
    catches: dict[str, str] = {}
    validate(copy.deepcopy(EXPECTED))
    for name, (key, value) in mutations.items():
        changed = copy.deepcopy(EXPECTED)
        changed[key] = value
        try:
            validate(changed)
        except AssertionError:
            catches[name] = "PASS_REJECTED"
        else:
            raise AssertionError(f"catch failed: {name}")

    type_catches: dict[str, str] = {}
    for name, replay_value in {
        "stringified_float_leaf": "1.25",
        "boolean_in_float_leaf": True,
    }.items():
        try:
            compare(1.25, replay_value, name)
        except AssertionError:
            type_catches[name] = "PASS_REJECTED"
        else:
            raise AssertionError(f"type catch failed: {name}")

    count, difference = compare(1.0, 1, "integer_numeric_float_leaf")
    if count != 1 or difference != 0.0:
        raise AssertionError("numeric integer representation control failed")
    type_catches["integer_numeric_float_leaf"] = "PASS_ACCEPTED"

    result = {
        "schema": "udt-sne-native-query-catches-1.0",
        "status": "PASS",
        "catch_count": len(catches),
        "catches": catches,
        "type_catch_count": len(type_catches),
        "type_catches": type_catches,
        "note": "Regression guards only; not an independent semantic derivation.",
    }
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS catches={len(catches)}")
    return result


if __name__ == "__main__":
    run()
