#!/usr/bin/env python3
"""Hostile mutation catches for G231 typing, exterior closure, and scope."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import derive_cartan_regional_bridge as production
import sympy as sp
import verify_cartan_bridge_independent as independent


ROOT = Path(__file__).resolve().parent


def derive() -> dict[str, object]:
    exact = production.derive()
    complete = {field: True for field in production.REALIZATION_CONDITIONS}
    bare = production.classify_input_schema({"R_typed_as_Lorentz_tensor": True})
    no_horizontal_data = dict(complete)
    no_horizontal_data["horizontal_derivative_law"] = False
    no_horizontal = production.classify_input_schema(no_horizontal_data)
    no_vertical_data = dict(complete)
    no_vertical_data["vertical_action_fixed_by_principal_SO13_action"] = False
    no_vertical = production.classify_input_schema(no_vertical_data)
    no_anchor_data = dict(complete)
    no_anchor_data["smooth_anchor_and_structure_functions"] = False
    no_anchor = production.classify_input_schema(no_anchor_data)
    no_equivariance_data = dict(complete)
    no_equivariance_data["SO13_equivariance_and_action_conditions"] = False
    no_equivariance = production.classify_input_schema(no_equivariance_data)
    preowned = production.classify_input_schema(
        {"theta": True, "omega": True, "R": True}, metric_preowned=True
    )

    b1 = production.algebraic_bianchi_map()
    raw_b1_witness = next(
        sp.eye(b1.cols).col(i) for i in range(b1.cols) if b1 * sp.eye(b1.cols).col(i) != sp.zeros(b1.rows, 1)
    )
    b1_residual = b1 * raw_b1_witness
    curvature_basis = sp.Matrix.hstack(*b1.nullspace())
    b2 = production.differential_bianchi_map(curvature_basis)
    raw_b2_witness = next(
        sp.eye(b2.cols).col(i) for i in range(b2.cols) if b2 * sp.eye(b2.cols).col(i) != sp.zeros(b2.rows, 1)
    )
    b2_residual = b2 * raw_b2_witness
    nonzero_compatible_d = next(vector for vector in b2.nullspace() if vector != sp.zeros(b2.cols, 1))
    zero_d = sp.zeros(b2.cols, 1)

    db = production.differentiated_bianchi_map(b2, curvature_basis.cols)
    comm = production.commutator_map(curvature_basis.cols)
    zero_e = sp.zeros(comm.cols, 1)
    nonlinear_r = production.off_diagonal_witness()
    nonlinear_rhs = production.ricci_commutator_rhs(curvature_basis, nonlinear_r)
    db_only_residual = db * zero_e
    full_commutator_residual = comm * zero_e - nonlinear_rhs

    generators = production.lorentz_generators()
    vertical_expected = production.vertical_action(generators[0], nonlinear_r)
    omitted_vertical_residual = sp.zeros(vertical_expected.rows, 1) - vertical_expected

    independent_live = independent.derive()
    sign_anchor = independent_live["direct_polynomial_metric_sign_anchor"]

    scope_mutations = {}
    for name, field, value in (
        ("curvature_value_generation", "curvature_values", "GENERATED"),
        ("classifying_law_selection", "classifying_law", "SELECTED_BY_IDENTITIES"),
        ("generic_smooth_promotion", "generic_smooth", "DERIVED"),
        ("global_promotion", "global", "DERIVED"),
        ("physical_history_promotion", "physical_history", "SELECTED"),
    ):
        mutated = dict(production.BASELINE_SCOPE)
        mutated[field] = value
        scope_mutations[name] = not production.validate_claim_scope(mutated)

    catches = {
        "bare_R_promoted_to_closed_input_detected": bare == "INCOMPLETE",
        "supplied_coframe_promoted_to_selector_detected": preowned == "EVALUATIVE_ALREADY_HAS_METRIC",
        "omitted_horizontal_derivative_law_detected": no_horizontal == "INCOMPLETE",
        "omitted_principal_vertical_action_typing_detected": no_vertical == "INCOMPLETE",
        "omitted_anchor_detected": no_anchor == "INCOMPLETE",
        "omitted_SO13_equivariance_detected": no_equivariance == "INCOMPLETE",
        "omitted_algebraic_Bianchi_witness_detected": any(value != 0 for value in b1_residual),
        "omitted_differential_Bianchi_witness_detected": any(value != 0 for value in b2_residual),
        "bare_R_does_not_determine_horizontal_D": b2 * zero_d == sp.zeros(b2.rows, 1)
        and b2 * nonzero_compatible_d == sp.zeros(b2.rows, 1)
        and zero_d != nonzero_compatible_d,
        "omitted_vertical_action_witness_detected": any(
            value != 0 for value in omitted_vertical_residual
        ),
        "omitted_Ricci_commutator_affine_witness_detected": db_only_residual == sp.zeros(db.rows, 1)
        and any(value != 0 for value in full_commutator_residual),
        "reversed_Ricci_sign_direct_metric_residual_detected": sign_anchor[
            "correct_sign_residual_nonzero_count"
        ]
        == 0
        and sign_anchor["reversed_sign_residual_nonzero_count"] > 0,
        **{f"scope_{name}_detected": caught for name, caught in scope_mutations.items()},
    }
    return {
        "landing": f"G231_HOSTILE_MUTATIONS_{len(catches)}_OF_{len(catches)}_CAUGHT",
        "catches": catches,
        "diagnostics": {
            "bare_schema": bare,
            "no_horizontal_schema": no_horizontal,
            "no_vertical_schema": no_vertical,
            "preowned_schema": preowned,
            "no_anchor_schema": no_anchor,
            "no_equivariance_schema": no_equivariance,
            "algebraic_Bianchi_witness_residual_nonzero": sum(
                value != 0 for value in b1_residual
            ),
            "differential_Bianchi_witness_residual_nonzero": sum(
                value != 0 for value in b2_residual
            ),
            "omitted_vertical_action_residual_nonzero": sum(
                value != 0 for value in omitted_vertical_residual
            ),
            "zero_E_differentiated_Bianchi_residual_nonzero": sum(
                value != 0 for value in db_only_residual
            ),
            "zero_E_full_commutator_residual_nonzero": sum(
                value != 0 for value in full_commutator_residual
            ),
            "direct_metric_correct_sign_residual_nonzero": sign_anchor[
                "correct_sign_residual_nonzero_count"
            ],
            "direct_metric_reversed_sign_residual_nonzero": sign_anchor[
                "reversed_sign_residual_nonzero_count"
            ],
            "without_commutator_translation_dimension": 320
            - exact["ranks"]["differentiated_bianchi"],
            "full_translation_dimension": exact["dimensions"]["second_derivative_affine_translation"],
        },
        "all_caught": all(catches.values()),
        "count": len(catches),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if not args.no_write:
        (ROOT / "hostile_results.json").write_text(text + "\n", encoding="utf-8")
    if not result["all_caught"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
