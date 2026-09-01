#!/usr/bin/env python3
"""Hostile semantic and formula mutations for the G315 bounded landing."""

import copy
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


BASE = {
    "hamiltonian_lambda_coefficient": 2,
    "evolution_lambda_coefficient": -1,
    "momentum_constraint_present": True,
    "phase_space_functions": 4,
    "configuration_modes": 2,
    "lapse_shift_class": "GAUGE",
    "all_seed_data_lawful": False,
    "same_null_lambda_coefficient": 0,
    "mixed_null_lambda_coefficient": -1,
    "intersecting_null_sheets_required_for_complete_local_characteristic_claim": True,
    "propagation_scope": "LOCAL_CONDITIONAL",
    "pair_adds_evolution_residual": False,
    "unique_history_selected": False,
    "Lambda_selected_or_calibrated": False,
    "physical_Xmax_selected": False,
    "metric_or_kernel_changed": False,
    "action_source_matter_observation_imported": False,
    "protected_work_used": False,
}


def validate(record):
    errors = []
    expected = BASE
    for key, value in expected.items():
        if record.get(key) != value:
            errors.append(f"{key}: expected {value!r}, got {record.get(key)!r}")
    if record.get("phase_space_functions") != 2 * record.get("configuration_modes", -999):
        errors.append("phase/configuration data type mismatch")
    return errors


MUTATIONS = [
    ("wrong_hamiltonian_Lambda_sign", "hamiltonian_lambda_coefficient", -2),
    ("wrong_evolution_Lambda_sign", "evolution_lambda_coefficient", 1),
    ("erase_momentum_constraint", "momentum_constraint_present", False),
    ("four_configuration_modes", "configuration_modes", 4),
    ("lapse_shift_called_physical", "lapse_shift_class", "PHYSICAL_SELECTED"),
    ("all_seed_data_called_lawful", "all_seed_data_lawful", True),
    ("Lambda_inserted_in_same_null_focusing", "same_null_lambda_coefficient", 1),
    ("mixed_null_Lambda_erased", "mixed_null_lambda_coefficient", 0),
    ("single_null_sheet_called_complete", "intersecting_null_sheets_required_for_complete_local_characteristic_claim", False),
    ("local_called_global_complete", "propagation_scope", "GLOBAL_COMPLETE"),
    ("pair_called_evolution_equation", "pair_adds_evolution_residual", True),
    ("unique_history_promoted", "unique_history_selected", True),
    ("Lambda_called_calibrated", "Lambda_selected_or_calibrated", True),
    ("Xmax_promoted", "physical_Xmax_selected", True),
    ("kernel_change_claimed", "metric_or_kernel_changed", True),
    ("physics_import_smuggled", "action_source_matter_observation_imported", True),
    ("protected_work_smuggled", "protected_work_used", True),
]


def main():
    if validate(BASE):
        raise AssertionError("baseline rejected")
    records = []
    caught = 0
    for name, field, value in MUTATIONS:
        trial = copy.deepcopy(BASE)
        trial[field] = value
        errors = validate(trial)
        is_caught = bool(errors)
        caught += int(is_caught)
        records.append({"mutation": name, "field": field, "caught": is_caught, "errors": errors})
    if caught != len(MUTATIONS):
        raise AssertionError(f"caught {caught}/{len(MUTATIONS)}")
    result = {
        "baseline_passes": True,
        "hostile_mutations": len(MUTATIONS),
        "caught": caught,
        "all_caught": True,
        "records": records,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"G315 hostile checks PASS: {caught}/{len(MUTATIONS)} caught")


if __name__ == "__main__":
    main()
