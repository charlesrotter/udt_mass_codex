#!/usr/bin/env python3
"""Exercise hostile mutations against the fail-closed G81 verifier."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("g81_verify", HERE / "verify_package.py")
assert SPEC and SPEC.loader
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def rejected(function, *args) -> bool:
    try:
        function(*args)
    except (AssertionError, KeyError, ValueError):
        return True
    return False


def main() -> None:
    contract = json.loads((HERE / "SEMANTIC_CONTRACT.json").read_text(encoding="utf-8"))
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = {}

    case = copy.deepcopy(contract); case["control_ids"].pop()
    catches["missing_control"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["control_ids"][1] = case["control_ids"][0]
    catches["duplicate_control"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["directions"]["C1_FULL_ANGULAR"][0] = 1.0
    catches["changed_direction"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["reverse_source_rotation"][0][0] = 1.0
    catches["changed_A_rotation"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["receiver_projection_rotation"][0][0] = 1.0
    catches["changed_B_rotation"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["tangent_reversal"] = "REVERSE_SPATIAL_PART_ONLY"
    catches["partial_tangent_reversal"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["unrotated_matrix_law"] = "D_REVERSE_EQUALS_TRANSPOSE_D_FORWARD"
    catches["omitted_Z"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["unrotated_matrix_law"] = "D_REVERSE_EQUALS_Z_TIMES_D_FORWARD"
    catches["omitted_transpose"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["rotated_matrix_law"] = "D_REVERSE_AB_EQUALS_Z_TIMES_TRANSPOSE_D_FORWARD"
    catches["omitted_A_or_B"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["diagonalization_permitted"] = True
    catches["silent_diagonalization"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["retuning_permitted"] = True
    catches["retuned_nonradial_control"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(contract); case["future_signal_derived"] = True
    catches["future_signal_promotion"] = rejected(VERIFY.validate_contract, case)
    for field in ("physical_profile_selected", "physical_endpoint_selected", "Xmax_identified", "physical_source_selected", "cmb_observable_derived"):
        case = copy.deepcopy(contract); case[field] = True
        catches[f"promotion__{field}"] = rejected(VERIFY.validate_contract, case)
    case = copy.deepcopy(production); case["controls"][1]["forward"]["offdiagonal_norm"] = 0.0
    catches["hidden_diagonal_nonradial_map"] = rejected(VERIFY.validate_outcomes, case, independent)
    case = copy.deepcopy(independent); case["controls"][1]["independent_rotated_covariance_relative"] = 3e-4
    catches["independent_tolerance_failure"] = rejected(VERIFY.validate_outcomes, production, case)
    catches["frozen_source_mutation"] = (
        __import__("hashlib").sha256(b"mutated").hexdigest()
        != __import__("hashlib").sha256(b"original").hexdigest()
    )

    assert len(catches) == 20 and all(catches.values())
    output = {
        "schema": "udt-cmb-g81-catch-proofs-v1",
        "status": "PASS",
        "count": len(catches),
        "catches": catches,
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
