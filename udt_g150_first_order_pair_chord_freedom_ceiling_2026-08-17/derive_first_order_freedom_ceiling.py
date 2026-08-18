#!/usr/bin/env python3
"""Exact symbolic G150 first-order pair-chord freedom theorem."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def inner(g, x, y):
    return sp.simplify((x.T * g * y)[0])


def vec_zero(x):
    return all(sp.simplify(v) == 0 for v in x)


def main():
    T, L = sp.symbols("T L", positive=True, finite=True)
    A0, A1, A2, A3 = sp.symbols("A0 A1 A2 A3", real=True)
    B0, B1, B2, B3 = sp.symbols("B0 B1 B2 B3", real=True)
    p, a, w2, w3 = sp.symbols("p a w2 w3", real=True)
    tau, sigma = sp.symbols("tau sigma", real=True)
    C0, C1, C2, C3 = sp.symbols("C0 C1 C2 C3", real=True)
    g = sp.diag(-1, 1, 1, 1)
    e0, e1, e2, e3 = [sp.eye(4)[:, i] for i in range(4)]
    J0, J1 = T * e0, L * e1
    A = sp.Matrix([A0, A1, A2, A3])
    B = sp.Matrix([B0, B1, B2, B3])
    C = sp.Matrix([C0, C1, C2, C3])
    Fmap = T * tau * e0 + L * sigma * e1 + A * tau**2 / 2 + B * tau * sigma + C * sigma**2 / 2
    zero = {tau: 0, sigma: 0}
    explicit_jets = {
        "J0": sp.simplify(Fmap.diff(tau).subs(zero) - J0),
        "J1": sp.simplify(Fmap.diff(sigma).subs(zero) - J1),
        "A": sp.simplify(Fmap.diff(tau, 2).subs(zero) - A),
        "B": sp.simplify(Fmap.diff(tau, sigma).subs(zero) - B),
    }
    J = J0.row_join(J1)
    Jtau = A.row_join(B)
    h = sp.simplify(J.T * g * J)
    htau = sp.simplify(Jtau.T * g * J + J.T * g * Jtau)

    Tpair = sp.sqrt(-h[0, 0])
    Ttau = sp.simplify(-htau[0, 0] / (2 * Tpair))
    beta = sp.simplify(h[0, 1] / h[0, 0])
    betatau = sp.simplify(
        (htau[0, 1] * h[0, 0] - h[0, 1] * htau[0, 0]) / h[0, 0] ** 2
    )
    r = sp.simplify(J1 - beta * J0)
    rtau = sp.simplify(B - betatau * J0 - beta * A)
    Lpair = sp.sqrt(inner(g, r, r))
    L2tau = sp.simplify(2 * inner(g, rtau, r))
    Ltau = sp.simplify(L2tau / (2 * Lpair))
    u = sp.simplify(J0 / Tpair)
    n = sp.simplify(r / Lpair)
    utau = sp.simplify(A / Tpair - J0 * Ttau / Tpair**2)
    ntau = sp.simplify(rtau / Lpair - r * Ltau / Lpair**2)
    nabla_u_u = sp.simplify(utau / Tpair)
    nabla_u_n = sp.simplify(ntau / Tpair)
    an = sp.simplify(inner(g, nabla_u_u, n))
    Omega = sp.simplify(
        nabla_u_n + inner(g, nabla_u_n, u) * u - inner(g, nabla_u_n, n) * n
    )
    phitau = sp.simplify(
        sp.trace(h.inv() * htau) / 4 - htau[0, 0] / (2 * h[0, 0])
    )
    dotphi = sp.simplify(phitau / Tpair)

    proposed = {
        "dotphi": -A0 / (2 * T**2) + B1 / (2 * T * L),
        "a_n": A1 / T**2,
        "Omega": sp.Matrix([0, 0, B2 / (T * L), B3 / (T * L)]),
    }
    outputs = sp.Matrix([dotphi, an, Omega[2], Omega[3]])
    variables = sp.Matrix([A0, A1, B1, B2, B3])
    jac = outputs.jacobian(variables)
    minor = sp.simplify(jac[:, [1, 2, 3, 4]].det())

    right_inverse = {
        A0: 0,
        A1: a * T**2,
        A2: 0,
        A3: 0,
        B0: 0,
        B1: 2 * p * T * L,
        B2: w2 * T * L,
        B3: w3 * T * L,
    }
    target = sp.Matrix([p, a, w2, w3])
    recovered = sp.simplify(outputs.subs(right_inverse))
    mutation_unnormalized = sp.Matrix([phitau, an, Omega[2], Omega[3]]).subs(right_inverse)
    mutation_missing_screen = sp.Matrix([dotphi, an, 0, 0]).subs(right_inverse)

    gates = {
        "regular_h": sp.simplify(h - sp.diag(-T**2, L**2)) == sp.zeros(2),
        "orthonormal_u_n": all(
            sp.simplify(x) == 0
            for x in (inner(g, u, u) + 1, inner(g, n, n) - 1, inner(g, u, n))
        ),
        "dotphi_formula": sp.simplify(dotphi - proposed["dotphi"]) == 0,
        "a_n_formula": sp.simplify(an - proposed["a_n"]) == 0,
        "Omega_formula": vec_zero(Omega - proposed["Omega"]),
        "Omega_screen": all(sp.simplify(x) == 0 for x in (inner(g, Omega, u), inner(g, Omega, n))),
        "rank_four_minor_nonzero": sp.simplify(minor) != 0,
        "right_inverse_exact": vec_zero(recovered - target),
        "explicit_quadratic_immersion_realizes_jets": all(vec_zero(x) for x in explicit_jets.values()),
        "mutation_unnormalized_clock_rejected": not vec_zero(mutation_unnormalized - target),
        "mutation_missing_screen_rejected": not vec_zero(mutation_missing_screen - target),
        "counterexample_dotphi_equals_an": sp.simplify(recovered[0] - recovered[1]) != 0,
    }
    result = {
        "schema": "udt.g150.symbolic.v1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "scope": "unrestricted smooth regular local pair first jets at arbitrary positive T,L",
        "derived": {
            "h": [[str(h[i, j]) for j in range(2)] for i in range(2)],
            "phi_pair": "log(L/T)/2",
            "dotphi": str(dotphi),
            "a_n": str(an),
            "Omega": [str(x) for x in Omega],
            "output_jacobian": [[str(jac[i, j]) for j in range(5)] for i in range(4)],
            "rank_four_minor_columns_A1_B1_B2_B3": str(minor),
            "right_inverse_recovered": [str(x) for x in recovered],
        },
        "gates": gates,
        "premise_stamps": {
            "flat_metric": "CHOSE_MATHEMATICAL_COUNTERFAMILY",
            "pair_jets": "FREE_AND_EXPLORED",
            "kinematic_ceiling": "DERIVED_IN_STATED_UNRESTRICTED_LOCAL_CLASS",
            "physical_query_restrictions": "OPEN",
            "next_pair_frame_jet_and_metric_curvature": "OPEN",
            "dynamics_and_global_completion": "OPEN",
        },
        "maximum_conclusion": (
            "UNIVERSAL_ALGEBRAIC_FIRST_ORDER_PAIR_CHORD_SELECTOR_ABSENT_IN_UNRESTRICTED_SMOOTH_REGULAR_METRIC_QUERY_KINEMATICS__"
            "DOTPHI_AN_AND_TWO_OMEGA_COMPONENTS_CONSTRUCTIVELY_INDEPENDENT_AT_ANY_FINITE_PAIR_DEPTH__"
            "NO_ADDITIONAL_UNIVERSAL_ALGEBRAIC_RELATION_AMONG_THESE_FOUR_OUTPUTS__"
            "PHYSICAL_QUERY_RESTRICTIONS_NEXT_PAIR_FRAME_JET_METRIC_CURVATURE_GLOBAL_COMPLETION_DYNAMICS_AND_REGIME_LAW_OPEN"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
