#!/usr/bin/env python3
"""Exact symbolic classification for G152."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    T, L, X = sp.symbols("T L X_max", positive=True)
    beta = sp.symbols("beta", real=True)
    f, ft, Tt, Ts, bt = sp.symbols("f partial_tau_f partial_tau_T partial_sigma_T partial_tau_beta", real=True)

    rho = sp.simplify(X * (L - T) / (L + T))
    phi = sp.log(L / T) / 2

    # Components in the orthonormal (u,n) pair plane.
    J1_un = sp.Matrix([beta * T, L])
    r_un = sp.Matrix([0, L])
    xi_un = sp.Matrix([0, rho])

    branches = {}
    branch_gates = []
    for eps in (1, -1):
        T_branch = sp.simplify(L * (X - eps * L) / (X + eps * L))
        X_candidate = sp.simplify(eps * L * (L + T) / (L - T))
        rho_on_T = sp.simplify(rho.subs(T, T_branch))
        rho_on_X = sp.simplify(rho.subs(X, X_candidate))
        coordinate_match = sp.simplify(
            xi_un.subs({T: T_branch, beta: 0}) - eps * J1_un.subs({T: T_branch, beta: 0})
        )
        branch = {
            "epsilon": eps,
            "T_for_oriented_match": str(T_branch),
            "X_candidate": str(X_candidate),
            "rho_after_T_substitution": str(rho_on_T),
            "rho_after_X_substitution": str(rho_on_X),
            "domain": "T>0,L>0,X>0 requires 0<L<X and epsilon*(L-T)>0",
        }
        branches[str(eps)] = branch
        branch_gates.extend([
            sp.simplify(rho_on_T - eps * L) == 0,
            sp.simplify(rho_on_X - eps * L) == 0,
            all(sp.simplify(q) == 0 for q in coordinate_match),
        ])

    # Direct coordinate bracket. J0,J1 commute; u=J0/T and xi=f(J1-beta J0).
    C0 = sp.simplify(
        -(ft * beta + f * bt) / T
        - f * beta * Tt / T**2
        + f * Ts / T**2
    )
    C1 = sp.simplify(ft / T)
    C_coordinate = sp.Matrix([C0, C1])
    C_un = sp.Matrix([
        sp.simplify(T * (C0 + beta * C1)),
        sp.simplify(L * C1),
    ])
    u_f = sp.simplify(ft / T)
    kappa = sp.simplify(Ts / T - (bt * T + beta * Tt) / T)
    C_expected = sp.Matrix([sp.simplify(f * kappa), sp.simplify(L * u_f)])

    # Counterexamples frozen algebraically.
    regular_nonequality = {
        "T": sp.Rational(1), "L": sp.Rational(3, 2), "X": sp.Rational(4), "beta": sp.Rational(1, 5)
    }
    rho_nonequality = sp.simplify(rho.subs({T: regular_nonequality["T"], L: regular_nonequality["L"], X: regular_nonequality["X"]}))

    s = sp.symbols("sigma", real=True)
    Ls = 1 + s / 10
    Ts_fun = sp.simplify(Ls * (2 - Ls) / (2 + Ls))
    kappa_equal_not_carried = sp.simplify((sp.diff(Ts_fun, s) / Ts_fun).subs(s, 0))

    rho_connecting_not_equal = sp.simplify(rho.subs({T: 1, L: 2, X: 3}))
    f_connecting_not_equal = sp.simplify(rho_connecting_not_equal / 2)

    gates = {
        "terminal_tanh_identity": sp.simplify(
            rho - X * (sp.exp(2 * phi) - 1) / (sp.exp(2 * phi) + 1)
        ) == 0,
        "J1_decomposition": all(sp.simplify(q) == 0 for q in J1_un - (sp.Matrix([beta * T, 0]) + r_un)),
        "both_orientation_branches_exact": all(branch_gates),
        "coordinate_bracket_matches_invariant_split": all(sp.simplify(q) == 0 for q in C_un - C_expected),
        "carried_oriented_ruler_requires_kappa_zero": sp.simplify(C_expected[0].subs({f: 1, ft: 0}) - kappa) == 0,
        "coordinate_subcase_beta_zero_requires_Tsigma_zero": sp.simplify(kappa.subs({beta: 0, bt: 0}) - Ts / T) == 0,
        "counterexample_regular_non_equality": (
            rho_nonequality != regular_nonequality["L"]
            and rho_nonequality != -regular_nonequality["L"]
        ),
        "counterexample_equality_without_carry": kappa_equal_not_carried == -sp.Rational(1, 30),
        "counterexample_connecting_without_equality": (
            rho_connecting_not_equal == 1 and f_connecting_not_equal == sp.Rational(1, 2)
        ),
    }
    gates = {name: bool(value) for name, value in gates.items()}

    result = {
        "schema": "udt.g152.variational_ownership.v1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "formulas": {
            "phi_pair": str(phi),
            "rho": str(rho),
            "J1_in_u_n": [str(q) for q in J1_un],
            "r_in_u_n": [str(q) for q in r_un],
            "xi_in_u_n": [str(q) for q in xi_un],
            "C_coordinate": [str(q) for q in C_coordinate],
            "C_u_n": [str(q) for q in C_un],
            "C_invariant": [str(q) for q in C_expected],
            "kappa": str(kappa),
            "branches": branches,
        },
        "counterexamples": {
            "regular_non_equality": {
                "T": "1", "L": "3/2", "X": "4", "beta": "1/5", "rho": str(rho_nonequality)
            },
            "equality_without_carry": {
                "X": "2", "L_sigma": str(Ls), "T_sigma": str(Ts_fun),
                "rho_equals_L": True, "kappa_at_zero": str(kappa_equal_not_carried),
            },
            "connecting_without_equality": {
                "T": "1", "L": "2", "X": "3", "rho": str(rho_connecting_not_equal),
                "rho_over_L": str(f_connecting_not_equal), "kappa": "0",
            },
        },
        "gates": gates,
        "premise_stamps": {
            "pair_immersion": "SUPPLIED",
            "T_L_beta_and_variations": "DERIVED_FROM_SUPPLIED_PAIR_METRIC",
            "xi": "CHOSE_WORKING_RELATION_FIRST_REPRESENTATION",
            "epsilon": "CHOSE_ORIENTATION_LABEL",
            "identification_and_connecting_carry": "CONDITIONAL_NOT_AUTOMATIC",
            "Xmax_value_and_physical_history": "OPEN",
        },
        "maximum_conclusion": (
            "PAIR_IMMERSION_OWNS_COORDINATE_AND_ORTHOGONAL_VARIATIONS_BUT_NOT_THEIR_IDENTIFICATION_WITH_WORKING_XI__"
            "EXACT_MAGNITUDE_SHIFT_LAPSE_AND_COMMUTATOR_CONDITIONS_CLASSIFIED__"
            "UNIVERSAL_XMAX_WOULD_REQUIRE_CANDIDATE_CONSTANCY_ACROSS_THE_SUPPLIED_FAMILY__"
            "PHYSICAL_IDENTIFICATION_QUERY_HISTORY_DYNAMICS_XMAX_VALUE_AND_COMPLETION_OPEN"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
