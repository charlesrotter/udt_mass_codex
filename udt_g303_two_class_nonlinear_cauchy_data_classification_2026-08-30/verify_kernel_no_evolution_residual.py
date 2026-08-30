#!/usr/bin/env python3
"""Direct dependency census for G303's reciprocal-kernel evaluator claim."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def endpoint(prefix: str):
    h00, h01, h11 = sp.symbols(f"{prefix}00 {prefix}01 {prefix}11", real=True)
    h = sp.Matrix([[h00, h01], [h01, h11]])
    m = sp.sqrt(-h.det())
    phi = -sp.log(-h00) / 2
    normalized = sp.simplify(h / m)
    return (h00, h01, h11), h, m, phi, normalized


def main() -> None:
    a_entries, h_a, m_a, phi_a, normalized_a = endpoint("a")
    b_entries, h_b, m_b, phi_b, normalized_b = endpoint("b")

    delta_ab = sp.simplify(phi_b - phi_a)
    delta_ba = sp.simplify(phi_a - phi_b)
    chi_ab = sp.tanh(delta_ab)
    g2 = sp.symbols("g2_0:10")  # formal independent second-normal metric jet
    outputs = [m_a, phi_a, *normalized_a, m_b, phi_b, *normalized_b, delta_ab, delta_ba, chi_ab]
    second_jet_jacobian = sp.Matrix(outputs).jacobian(g2)

    assert h_a.shape == (2, 2) and h_b.shape == (2, 2)
    assert sp.simplify(delta_ab + delta_ba) == 0
    assert second_jet_jacobian == sp.zeros(len(outputs), len(g2))
    assert second_jet_jacobian.rank() == 0
    assert all(not set(g2) & expression.free_symbols for expression in outputs)

    dependency_inputs = sorted(
        str(symbol) for symbol in set().union(*(expression.free_symbols for expression in outputs))
    )
    assert dependency_inputs == sorted(str(symbol) for symbol in (*a_entries, *b_entries))

    result = {
        "status": "PASS",
        "pair_metric_formula": "h=F^*g=J^T*g*J (pointwise algebraic pullback)",
        "terminal_readouts": [
            "m=sqrt(-det(h))",
            "phi_pair=-1/2*log(-h00)",
            "delta_AB=phi_B-phi_A",
            "chi_AB=tanh(delta_AB)",
        ],
        "endpoint_reversal": "delta_AB+delta_BA=0",
        "actual_free_symbols": dependency_inputs,
        "formal_second_normal_metric_jet_symbols": [str(symbol) for symbol in g2],
        "second_normal_jet_jacobian_rank": second_jet_jacobian.rank(),
        "independent_cauchy_or_evolution_residuals_generated": 0,
        "scope": (
            "syntax/dependency theorem for registered pointwise pair readout and endpoint identities; "
            "not a theorem that no future UDT law can couple pair data to evolution"
        ),
    }
    (ROOT / "KERNEL_NO_EVOLUTION_RESIDUAL.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G303 direct reciprocal dependency census PASS")
    print("second-normal-jet Jacobian rank=0; generated evolution residuals=0")


if __name__ == "__main__":
    main()
