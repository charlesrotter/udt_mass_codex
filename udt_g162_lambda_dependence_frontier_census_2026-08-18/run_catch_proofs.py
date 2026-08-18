#!/usr/bin/env python3
"""Algebra mutations and semantic guards for G162."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def tr(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det],
            [-a[1][0] / det, a[0][0] / det]]


def root(t, ell, beta):
    return [[t, t * beta], [F(0), ell]]


def boost(z):
    den = 1 - z * z
    return [[(1 + z * z) / den, 2 * z / den],
            [2 * z / den, (1 + z * z) / den]]


def metadata_catch(name, key, wrong):
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    expected = {
        "scalar_kernel_lambda_invariant": True,
        "canonical_endpoint_section_is_physical_overlap_or_path": False,
        "joined_C_Gamma_lambda_sensitive": True,
        "all_active_objects_lambda_invariant": False,
        "normal_jacobi_extrinsic_channels_reduced_to_tangent_lambda": False,
        "rapidity_selection_remains_scalar_kernel_gate": False,
        "physical_history_derived": False,
        "physical_query_path_carry_derived": False,
    }
    result[key] = wrong
    return {"name": name, "caught": result[key] != expected[key]}


def main():
    eta = [[F(-1), F(0)], [F(0), F(1)]]
    ra = root(F(2), F(3), F(1, 2))
    rb = root(F(5), F(7), F(-1, 3))
    lam = boost(F(1, 3))
    ha = mm(mm(tr(ra), eta), ra)
    hb = mm(mm(tr(rb), eta), rb)
    correct = mm(mm(inv2(rb), lam), ra)
    wrong_order = mm(mm(lam, inv2(rb)), ra)
    joined = mm(mm(rb, correct), inv2(ra))
    witness = boost(F(2, 5))
    flat_mcal = [[F(1), F(0)], [F(0), F(1)]]

    catches = [
        {"name": "move_Lambda_outside_endpoint_factorization",
         "caught": mm(mm(tr(correct), hb), correct) == ha
         and mm(mm(tr(wrong_order), hb), wrong_order) != ha},
        {"name": "erase_joined_route_transition",
         "caught": joined == lam and joined != [[F(1), F(0)], [F(0), F(1)]]},
        {"name": "promote_endpoint_rebuild_to_actual_flat_overlap",
         "caught": mm(mm(tr(witness), eta), witness) == eta and witness != flat_mcal},
        {"name": "claim_Lambda_changes_determinant_character",
         "caught": (lam[0][0] * lam[1][1] - lam[0][1] * lam[1][0]) == 1},
        metadata_catch("claim_scalar_kernel_retains_Lambda",
                       "scalar_kernel_lambda_invariant", False),
        metadata_catch("promote_calibration_section_to_physical_path",
                       "canonical_endpoint_section_is_physical_overlap_or_path", True),
        metadata_catch("erase_C_and_Gamma_route_channel",
                       "joined_C_Gamma_lambda_sensitive", False),
        metadata_catch("claim_every_active_object_is_Lambda_invariant",
                       "all_active_objects_lambda_invariant", True),
        metadata_catch("collapse_normal_Jacobi_extrinsic_channels_into_Lambda",
                       "normal_jacobi_extrinsic_channels_reduced_to_tangent_lambda", True),
        metadata_catch("retain_rapidity_selector_as_scalar_kernel_gate",
                       "rapidity_selection_remains_scalar_kernel_gate", True),
        metadata_catch("promote_census_to_history_law",
                       "physical_history_derived", True),
        metadata_catch("promote_census_to_query_path_carry_law",
                       "physical_query_path_carry_derived", True),
    ]
    assert all(item["caught"] for item in catches)
    result = {
        "status": "PASS",
        "catch_count": len(catches),
        "algebra_mutation_count": 4,
        "metadata_guard_mutation_count": 8,
        "metadata_guards_are_independent_semantic_proofs": False,
        "caught": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
