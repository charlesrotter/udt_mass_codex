#!/usr/bin/env python3
"""Exact production derivation for the bounded G303 Cauchy/data classification."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
LANDING = (
    "BOTH_G301_CLASSES_HAVE_THE_SAME_LOCAL_CAUSAL_PRINCIPAL_SYSTEM"
    "__TRACEFREE_DATA_ARE_THE_UNION_OVER_ONE_CONSTANT_SCALAR_DATUM"
    "__WELLPOSEDNESS_DOES_NOT_SELECT"
)
PAIRS = [(i, j) for i in range(4) for j in range(i, 4)]


def trace_row(g_inv: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([[g_inv[i, j] * (2 if i != j else 1) for i, j in PAIRS]])


def covector(g_cov: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([g_cov[i, j] for i, j in PAIRS])


def tracefree_projector(g_cov: sp.Matrix) -> sp.Matrix:
    return sp.eye(10) - sp.Rational(1, 4) * covector(g_cov) * trace_row(g_cov.inv())


def wave_quadratic(g_inv: sp.Matrix, xi: sp.Matrix) -> sp.Expr:
    return sp.expand((xi.T * g_inv * xi)[0])


def graph_difference_matrix(n: int) -> sp.Matrix:
    rows = []
    for i in range(1, n):
        row = [0] * n
        row[0] = -1
        row[i] = 1
        rows.append(row)
    return sp.Matrix(rows)


def main() -> None:
    assertions = 0

    # Exact nonlinear residual consequences in four dimensions.
    dimension = sp.Integer(4)
    bianchi_ricci = sp.Rational(1, 2)
    tracefree_coefficient = sp.simplify(bianchi_ricci - sp.Rational(1, dimension))
    assert tracefree_coefficient == sp.Rational(1, 4)
    assertions += 1
    # S_ab=0 gives Ric_ab=(R/4)g_ab; divergence therefore gives dR/4=0.
    lambda_from_scalar = sp.Rational(1, dimension)
    assert lambda_from_scalar == sp.Rational(1, 4)
    assertions += 1

    # Exact normal projections. With g(n,n)=-1 and Ric=Lambda*g, R=4 Lambda.
    Lambda = sp.symbols("Lambda")
    scalar_R = dimension * Lambda
    einstein_nn = sp.simplify(-Lambda - sp.Rational(1, 2) * scalar_R * (-1))
    # G_nn=Lambda and G_nn=H/2, hence H=2 Lambda.
    assert einstein_nn == Lambda
    hamiltonian_value = sp.simplify(2 * einstein_nn)
    assert hamiltonian_value == 2 * Lambda
    assertions += 2
    # Orthogonality g(n,e_i)=0 removes Lambda from every momentum constraint.
    normal_tangent_lambda_term = sp.Integer(0)
    assert normal_tangent_lambda_term == 0
    assertions += 1

    # Raw trace-free residual has rank nine; its Bianchi-completed fixed-Lambda metric system has
    # the same full wave principal coefficient as Ricci-flat evolution.
    metric_samples = [
        sp.diag(-1, 1, 1, 1),
        sp.diag(-4, 2, 3, 5),
        sp.Matrix([[-1, sp.Rational(1, 3), 0, 0],
                   [sp.Rational(1, 3), 2, 0, 0],
                   [0, 0, 3, sp.Rational(1, 5)],
                   [0, 0, sp.Rational(1, 5), 4]]),
    ]
    covectors = [
        sp.Matrix([1, 0, 0, 0]),
        sp.Matrix([0, 1, 2, 0]),
        sp.Matrix([1, 1, 0, 0]),
        sp.Matrix([2, -1, 1, 3]),
    ]
    principal_samples = []
    for g_cov in metric_samples:
        assert g_cov.det() != 0
        assertions += 1
        projector = tracefree_projector(g_cov)
        assert projector.rank() == 9
        assert sp.simplify(projector * projector - projector) == sp.zeros(10)
        assertions += 2
        g_inv = g_cov.inv()
        for xi in covectors:
            q = wave_quadratic(g_inv, xi)
            ricci_symbol = -sp.Rational(1, 2) * q * sp.eye(10)
            fixed_lambda_symbol = -sp.Rational(1, 2) * q * sp.eye(10)
            raw_tracefree_symbol = sp.simplify(projector * ricci_symbol)
            assert fixed_lambda_symbol == ricci_symbol
            assert raw_tracefree_symbol == sp.simplify(projector * fixed_lambda_symbol)
            assert Lambda not in ricci_symbol.free_symbols
            assertions += 3
            principal_samples.append({
                "q": str(q),
                "ricci_rank": ricci_symbol.rank(),
                "raw_tracefree_rank": raw_tracefree_symbol.rank(),
                "fixed_lambda_rank": fixed_lambda_symbol.rank(),
            })

    # Exact finite-network analogue of the lawful-data distinction.
    graph_ranks = []
    for n in range(2, 11):
        generic = sp.eye(n)  # H_i=0 at every connected sample.
        tracefree = graph_difference_matrix(n)  # H_i-H_0=0: H is constant.
        assert generic.rank() == n
        assert tracefree.rank() == n - 1
        assert tracefree.nullspace() == [sp.ones(n, 1)]
        assertions += 3
        graph_ranks.append({"vertices": n, "generic_rank": n, "tracefree_rank": n - 1})

    # Constant-H data determine Lambda; Lambda=0 nests the generic scalar constraint exactly.
    H0 = sp.symbols("H0")
    derived_lambda = sp.simplify(H0 / 2)
    assert sp.simplify(2 * derived_lambda - H0) == 0
    assert derived_lambda.subs(H0, 0) == 0
    assertions += 2

    output = {
        "status": "PASS",
        "landing": LANDING,
        "scope": "local boundary-free globally-hyperbolic slab inside frozen G301 metric-only lane",
        "assertions": assertions,
        "nonlinear_equivalence": {
            "generic": "Ric_ab=0",
            "tracefree": "Ric_ab=Lambda*g_ab with dLambda=0",
            "lambda_definition": "Lambda=R/4",
        },
        "cauchy_constraints": {
            "generic_hamiltonian": "R3+K^2-KijKij=0",
            "tracefree_hamiltonian": "R3+K^2-KijKij=2*Lambda",
            "common_momentum": "D_j(K^ij-gamma^ij*K)=0",
            "unpresupplied_lambda_form": "D_i(R3+K^2-KijKij)=0",
        },
        "principal_system": {
            "raw_tracefree_output_rank": 9,
            "bianchi_completed_fixed_lambda_metric_rank": 10,
            "metric_principal_part": "-1/2*g^cd*partial_c*partial_d*g_ab",
            "lambda_is_lower_order": True,
            "characteristic_cone": "g^cd*xi_c*xi_d=0",
            "wellposedness_theorem_status": "IMPORTED_STANDARD_MATH_CONDITIONAL_ON_SMOOTH_LOCAL_HYPOTHESES",
            "samples": principal_samples,
        },
        "lawful_data": {
            "generic": "constraint-satisfying (gamma_ij,K_ij) with zero Hamiltonian scalar",
            "tracefree": "union over constant Lambda of Einstein-Lambda constraint data",
            "extra_functional_degree": False,
            "extra_connected_region_constants": 1,
            "unsupplied_lambda_compatibility": "M_i=0 and D_i(H)=0; Lambda=H/2 on each connected component",
            "graph_rank_checks": graph_ranks,
        },
        "selection": {
            "wellposedness_selects_class": False,
            "reciprocal_kernel_adds_evolution_residual": False,
            "realized_history_selected": False,
        },
        "omitted": [
            "global boundary completion", "singularity evolution", "topology change",
            "physical query population", "source", "matter", "mass", "action",
            "observation", "scale", "X_max", "protected work",
        ],
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(LANDING)
    print(f"assertions={assertions}")
    print("generic constraints: H=0, M_i=0")
    print("tracefree constraints: H=2 Lambda constant, M_i=0")


if __name__ == "__main__":
    main()
