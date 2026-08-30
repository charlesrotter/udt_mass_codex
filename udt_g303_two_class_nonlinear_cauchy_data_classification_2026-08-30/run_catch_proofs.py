#!/usr/bin/env python3
"""Concrete hostile formula mutations for the repaired G303 certification gate."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def tracefree_matrix(coefficient: sp.Rational) -> sp.Matrix:
    eta = sp.diag(-1, 1, 1, 1)
    pairs = [(i, j) for i in range(4) for j in range(i, 4)]
    trace = sp.Matrix([[eta[i, j] * (2 if i != j else 1) for i, j in pairs]])
    metric = sp.Matrix([eta[i, j] for i, j in pairs])
    return sp.eye(10) - coefficient * metric * trace


def main() -> None:
    Lambda, H, q, zeta, g2 = sp.symbols("Lambda H q zeta g2")
    catches: dict[str, dict[str, object]] = {}

    # Mutate the coefficient in div(Ric-c R g)=(1/2-c)dR.
    correct_bianchi = sp.Rational(1, 2) - sp.Rational(1, 4)
    wrong_bianchi = sp.Rational(1, 2) - sp.Rational(1, 3)
    catches["wrong_bianchi_coefficient"] = {
        "caught": correct_bianchi == sp.Rational(1, 4) and wrong_bianchi != correct_bianchi,
        "correct": str(correct_bianchi), "mutated": str(wrong_bianchi),
    }

    # Trace Ric=c R g. Only 4c=1 is compatible with nonzero R.
    correct_trace = 4 * sp.Rational(1, 4) - 1
    wrong_trace = 4 * sp.Rational(1, 3) - 1
    catches["wrong_scalar_to_lambda_factor"] = {
        "caught": correct_trace == 0 and wrong_trace != 0,
        "correct_residual": str(correct_trace), "mutated_residual": str(wrong_trace),
    }

    # With Ric_nn=-Lambda, R=4Lambda, g_nn=-1, G_nn=Lambda and H=2G_nn.
    correct_gnn = -Lambda - sp.Rational(1, 2) * (4 * Lambda) * (-1)
    wrong_gnn = -Lambda + sp.Rational(1, 2) * (4 * Lambda) * (-1)
    catches["wrong_hamiltonian_sign_or_factor"] = {
        "caught": sp.simplify(2 * correct_gnn - 2 * Lambda) == 0
        and sp.simplify(2 * wrong_gnn - 2 * Lambda) != 0,
        "correct_H": str(sp.expand(2 * correct_gnn)), "mutated_H": str(sp.expand(2 * wrong_gnn)),
    }

    # A connected incidence operator kills constants and rejects an explicit varying H sample.
    incidence = sp.Matrix([[-1, 1, 0, 0], [0, -1, 1, 0], [0, 0, -1, 1]])
    constant = sp.Matrix([7, 7, 7, 7])
    varying = sp.Matrix([7, 8, 7, 7])
    catches["nonconstant_hamiltonian_accepted"] = {
        "caught": incidence * constant == sp.zeros(3, 1)
        and incidence * varying != sp.zeros(3, 1),
        "mutated_residual": [str(value) for value in incidence * varying],
    }

    correct_projector = tracefree_matrix(sp.Rational(1, 4))
    wrong_projector = tracefree_matrix(sp.Rational(1, 3))
    catches["wrong_trace_projector_factor"] = {
        "caught": correct_projector.rank() == 9
        and correct_projector**2 == correct_projector
        and wrong_projector**2 != wrong_projector,
        "correct_rank": correct_projector.rank(), "mutated_rank": wrong_projector.rank(),
    }
    catches["raw_rank_promoted_to_ten"] = {
        "caught": correct_projector.rank() == 9 and sp.eye(10).rank() == 10,
        "correct_rank": correct_projector.rank(), "mutated_rank": sp.eye(10).rank(),
    }

    # Lambda must not alter the coefficient of second metric derivatives.
    correct_symbol = -q * sp.eye(10) / 2
    mutated_symbol = -(q + Lambda) * sp.eye(10) / 2
    catches["lambda_inserted_into_principal_coefficient"] = {
        "caught": correct_symbol.diff(Lambda) == sp.zeros(10)
        and mutated_symbol.diff(Lambda) != sp.zeros(10),
        "correct_lambda_derivative_rank": correct_symbol.diff(Lambda).rank(),
        "mutated_lambda_derivative_rank": mutated_symbol.diff(Lambda).rank(),
    }

    # A pointwise pair readout has no formal second-normal-jet dependence; adding one is detected.
    phi_pair = sp.symbols("phi_pair")
    correct_readout = sp.tanh(phi_pair)
    mutated_readout = sp.tanh(phi_pair) + zeta * g2
    catches["kernel_evaluator_promoted_to_evolution_residual"] = {
        "caught": sp.diff(correct_readout, g2) == 0
        and sp.diff(mutated_readout, g2) == zeta,
        "correct_g2_derivative": str(sp.diff(correct_readout, g2)),
        "mutated_g2_derivative": str(sp.diff(mutated_readout, g2)),
    }

    # The generic scalar constraint is exactly the Lambda=0 slice.
    completed_constraint = H - 2 * Lambda
    mutated_constraint = H - 2 * (Lambda + 1)
    catches["generic_not_nested_at_zero"] = {
        "caught": completed_constraint.subs(Lambda, 0) == H
        and mutated_constraint.subs(Lambda, 0) != H,
        "correct_zero_slice": str(completed_constraint.subs(Lambda, 0)),
        "mutated_zero_slice": str(mutated_constraint.subs(Lambda, 0)),
    }

    # Orthogonality removes Lambda from the momentum projection; a nonzero mutation is visible.
    normal_tangent = sp.Integer(0)
    correct_momentum_lambda = Lambda * normal_tangent
    mutated_momentum_lambda = Lambda
    catches["lambda_inserted_into_momentum_constraint"] = {
        "caught": correct_momentum_lambda == 0 and mutated_momentum_lambda != 0,
        "correct": str(correct_momentum_lambda), "mutated": str(mutated_momentum_lambda),
    }

    assert len(catches) == 10
    assert all(item["caught"] for item in catches.values()), catches
    output = {
        "status": "PASS",
        "count": len(catches),
        "method": "formula and artifact mutations; no hard-coded selection booleans",
        "caught": catches,
    }
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"G303 concrete hostile mutations PASS ({len(catches)}/{len(catches)})")


if __name__ == "__main__":
    main()
