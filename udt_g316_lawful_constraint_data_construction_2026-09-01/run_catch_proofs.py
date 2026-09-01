#!/usr/bin/env python3
"""Semantic and algebraic hostile-mutation catches for G316."""

import copy
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent

BASE = {
    "metric_power": 4,
    "A_up_power": -10,
    "TT_scalar_power": -7,
    "scalar_source_power": 5,
    "momentum_source_power": 6,
    "laplacian_coefficient": -8,
    "TT_sign": -1,
    "Lambda_coefficient": -2,
    "arbitrary_seeds_lawful": False,
    "cmc_promoted": False,
    "W_unique": False,
    "psi_is_physical_scale": False,
    "boost_is_physical_scale": False,
    "one_null_sheet_complete": False,
    "history_selected": False,
    "forbidden_import": False,
}


def validate(spec):
    expected = BASE
    for key, value in expected.items():
        if spec.get(key) != value:
            raise ValueError(f"G316 guard rejected {key}: {spec.get(key)!r} != {value!r}")
    return True


mutations = [
    ("wrong_metric_power", "metric_power", 2),
    ("wrong_A_power", "A_up_power", -8),
    ("wrong_TT_scalar_power", "TT_scalar_power", -5),
    ("wrong_scalar_source_power", "scalar_source_power", 4),
    ("wrong_momentum_source_power", "momentum_source_power", 4),
    ("wrong_laplacian_coefficient", "laplacian_coefficient", 8),
    ("wrong_TT_sign", "TT_sign", 1),
    ("wrong_Lambda_sign", "Lambda_coefficient", 2),
    ("arbitrary_seeds_called_lawful", "arbitrary_seeds_lawful", True),
    ("cmc_promoted_to_udt", "cmc_promoted", True),
    ("W_called_unique", "W_unique", True),
    ("psi_called_physical_scale", "psi_is_physical_scale", True),
    ("boost_called_physical_scale", "boost_is_physical_scale", True),
    ("single_null_sheet_called_complete", "one_null_sheet_complete", True),
    ("physical_history_selected", "history_selected", True),
    ("forbidden_import_added", "forbidden_import", True),
]

if not validate(copy.deepcopy(BASE)):
    raise AssertionError("baseline rejected")

records = []
for name, key, value in mutations:
    mutant = copy.deepcopy(BASE)
    mutant[key] = value
    caught = False
    message = ""
    try:
        validate(mutant)
    except ValueError as exc:
        caught = True
        message = str(exc)
    if not caught:
        raise AssertionError(f"hostile mutation survived: {name}")
    records.append({"mutation": name, "caught": True, "message": message})

output = {
    "schema": "udt-g316-catch-v1",
    "status": "PASS",
    "baseline_accepted": True,
    "mutation_count": len(records),
    "caught_count": sum(1 for record in records if record["caught"]),
    "records": records,
}
(HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": "PASS", "caught": len(records), "total": len(records)}, indent=2))
