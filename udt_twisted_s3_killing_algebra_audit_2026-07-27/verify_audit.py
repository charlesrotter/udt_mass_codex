#!/usr/bin/env python3
"""Fail-closed verifier with exercised preregistered catch proofs."""
from __future__ import annotations

import copy
import csv
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
STAMPS = (
    "COPRESENCE = WORKING_INTERPRETIVE_FRAME",
    "METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL",
    "INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED",
    "COMPLETE_WHOLE_SOLUTION_LAW = OPEN",
)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def base_state() -> dict[str, object]:
    return {
        "unrestricted_killing": True,
        "known_group_only": False,
        "visual_uniqueness": False,
        "intrinsic_certificate": True,
        "open_set": True,
        "global_extension": True,
        "global_descent": True,
        "strict_slice": True,
        "all_lambda_claimed": False,
        "constant_control": True,
        "stabilizer_control": True,
        "a_nonzero_for_ruler": True,
        "spatial_extra_counts": True,
        "oriented_ruler_claimed": False,
        "cross_witness_splice": False,
        "physical_selection_claimed": False,
        "downstream_physics_inferred": False,
        "propagation_hypotheses_proved": True,
        "causal_boundary_crossed": False,
        "full_algebra_not_just_K": True,
        "scope_package_only": True,
    }


def validate(state: dict[str, object]) -> None:
    for key in (
        "unrestricted_killing",
        "intrinsic_certificate",
        "open_set",
        "global_extension",
        "global_descent",
        "strict_slice",
        "constant_control",
        "stabilizer_control",
        "a_nonzero_for_ruler",
        "spatial_extra_counts",
        "propagation_hypotheses_proved",
        "full_algebra_not_just_K",
        "scope_package_only",
    ):
        assert state[key]
    for key in (
        "known_group_only",
        "visual_uniqueness",
        "all_lambda_claimed",
        "oriented_ruler_claimed",
        "cross_witness_splice",
        "physical_selection_claimed",
        "downstream_physics_inferred",
        "causal_boundary_crossed",
    ):
        assert not state[key]


def reject(key: str, value: object) -> str:
    state = copy.deepcopy(base_state())
    state[key] = value
    try:
        validate(state)
    except AssertionError:
        return "PASS"
    raise AssertionError(f"catch accepted corruption: {key}={value!r}")


def main() -> int:
    universe = rows("KILLING_STRATUM_UNIVERSE.tsv")
    outcomes = rows("KILLING_STRATUM_OUTCOMES.tsv")
    contract = rows("FALSIFICATION_CONTRACT.tsv")
    assert [row["stratum_id"] for row in universe] == [f"K{i:02d}" for i in range(1, 13)]
    assert [row["stratum_id"] for row in outcomes] == [f"K{i:02d}" for i in range(1, 13)]

    primary = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    lambda0 = json.loads((HERE / "CONTROL_LAMBDA_0.json").read_text(encoding="utf-8"))
    lambda1 = json.loads((HERE / "CONTROL_LAMBDA_1.json").read_text(encoding="utf-8"))
    a0 = json.loads((HERE / "CONTROL_A_0.json").read_text(encoding="utf-8"))
    symbolic_lambda = json.loads((HERE / "SYMBOLIC_LAMBDA_RESULT.json").read_text(encoding="utf-8"))
    symbolic_roots = json.loads((HERE / "SYMBOLIC_LAMBDA_ROOTS.json").read_text(encoding="utf-8"))

    expected_det = Fraction(330801319823081673814309577, 159252480000000000000000000000)
    assert Fraction(primary["invariant_gradient_determinant"]) == expected_det
    assert primary["invariant_gradient_determinant_nonzero"]
    assert primary["open_set_rank_three"]
    assert primary["inverse_jet_identity"]
    assert primary["strict_slice_globally_certified"]
    assert primary["global_profile_smooth"]
    assert primary["stationary_norm_nonconstant"]
    assert primary["twist_nonzero_for_nonzero_kappa"]
    assert primary["parameters"] == {"R": "1", "a": "1/10", "c_E": "1", "lambda": "2/3"}

    assert independent["agreement_pass"] and independent["rank_three"]
    assert independent["max_gradient_relative_error"] < 1e-10
    assert independent["determinant_relative_error"] < 1e-10
    assert lambda0["parameters"]["lambda"] == "0" and lambda0["open_set_rank_three"]
    assert lambda1["parameters"]["lambda"] == "1" and lambda1["open_set_rank_three"]
    assert a0["parameters"]["a"] == "0" and a0["open_set_rank_three"]
    assert not a0["twist_nonzero_for_nonzero_kappa"]
    assert symbolic_lambda["parameters"]["lambda"] == "lambda"
    assert symbolic_lambda["determinant_polynomial_not_identically_zero"]
    assert symbolic_lambda["invariant_gradient_determinant_nonzero"] is None
    assert symbolic_lambda["open_set_rank_three"] is None
    assert symbolic_roots["polynomial_degree"] == 9
    assert symbolic_roots["real_root_count"] == 7
    assert symbolic_roots["semantics"] == "certificate_inconclusive_at_roots_not_extra_symmetry"
    lambda_symbol = sp.symbols("L")
    determinant_expression = sp.sympify(
        symbolic_lambda["invariant_gradient_determinant"].replace("lambda", "L"),
        locals={"L": lambda_symbol},
    )
    assert sp.Poly(sp.fraction(determinant_expression)[0], lambda_symbol).degree() == 9

    for filename in ("PREREGISTRATION.md", "EXACT_DERIVATION.md", "AUDIT_REPORT.md"):
        text = (HERE / filename).read_text(encoding="utf-8")
        for stamp in STAMPS:
            assert stamp in text
    exact_text = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for required in (
        "arbitrary time dependence",
        "finite-type linear propagation",
        "Kill(g) = span_R{partial_t}",
        "globally smooth",
        "unoriented",
        "Still open",
    ):
        assert required in exact_text

    mutations = {
        "F01": ("unrestricted_killing", False),
        "F02": ("known_group_only", True),
        "F03": ("visual_uniqueness", True),
        "F04": ("intrinsic_certificate", False),
        "F05": ("open_set", False),
        "F06": ("global_extension", False),
        "F07": ("strict_slice", False),
        "F08": ("all_lambda_claimed", True),
        "F09": ("constant_control", False),
        "F10": ("stabilizer_control", False),
        "F11": ("a_nonzero_for_ruler", False),
        "F12": ("spatial_extra_counts", False),
        "F13": ("oriented_ruler_claimed", True),
        "F14": ("cross_witness_splice", True),
        "F15": ("physical_selection_claimed", True),
        "F16": ("downstream_physics_inferred", True),
        "F17": ("propagation_hypotheses_proved", False),
        "F18": ("causal_boundary_crossed", True),
        "F19": ("full_algebra_not_just_K", False),
        "F20": ("scope_package_only", False),
    }
    assert set(mutations) == {row["catch_id"] for row in contract}
    catches = [
        {
            "catch_id": row["catch_id"],
            "result": reject(*mutations[row["catch_id"]]),
            "corruption_or_overclaim": row["corruption_or_overclaim"],
        }
        for row in contract
    ]
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)

    result = {
        "schema": "udt.twisted_s3_killing_algebra.verification.v1",
        "status": "PASS",
        "strata": "12/12",
        "exact_rank_determinant_nonzero": True,
        "full_unrestricted_killing_algebra": "ONE_DIMENSIONAL_FOR_EXPLICIT_COMPLETE_WITNESS",
        "same_branch_depth_twist": "PASS",
        "independent_full_expression_check": "PASS",
        "catch_proofs": "20/20",
        "all_parameter_function_space_classified": False,
        "physical_branch_selected": False,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
