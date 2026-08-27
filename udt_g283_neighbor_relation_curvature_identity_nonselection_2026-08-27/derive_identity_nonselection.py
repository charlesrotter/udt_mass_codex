#!/usr/bin/env python3
"""Exact symbolic G283 arbitrary-optical-tide construction."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


PACKAGE = Path(__file__).resolve().parent


def main() -> None:
    u, v, x, y = sp.symbols("u v x y", real=True)
    coords = (u, v, x, y)
    a = sp.Function("a")(u)
    b = sp.Function("b")(u)
    c = sp.Function("c")(u)
    tidal = sp.Matrix([[a, b], [b, c]])
    transverse = sp.Matrix([x, y])
    H = -sp.expand((transverse.T * tidal * transverse)[0])
    metric = sp.Matrix(
        [
            [H, -1, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    inverse = sp.simplify(metric.inv())

    gamma = [[[
        sp.simplify(
            sp.Rational(1, 2)
            * sum(
                inverse[rho, delta]
                * (
                    sp.diff(metric[delta, nu], coords[mu])
                    + sp.diff(metric[delta, mu], coords[nu])
                    - sp.diff(metric[mu, nu], coords[delta])
                )
                for delta in range(4)
            )
        )
        for nu in range(4)] for mu in range(4)] for rho in range(4)]

    riemann_up = [[[[] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for rho in range(4):
        for sigma in range(4):
            for mu in range(4):
                for nu in range(4):
                    riemann_up[rho][sigma][mu].append(
                        sp.simplify(
                            sp.diff(gamma[rho][nu][sigma], coords[mu])
                            - sp.diff(gamma[rho][mu][sigma], coords[nu])
                            + sum(
                                gamma[rho][mu][lam] * gamma[lam][nu][sigma]
                                - gamma[rho][nu][lam] * gamma[lam][mu][sigma]
                                for lam in range(4)
                            )
                        )
                    )

    def rlow(alpha: int, beta: int, mu: int, nu: int) -> sp.Expr:
        return sp.simplify(
            sum(metric[alpha, rho] * riemann_up[rho][beta][mu][nu] for rho in range(4))
        )

    center = {x: 0, y: 0}
    flat_center = sp.Matrix(
        [[0, -1, 0, 0], [-1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    )
    first_jets = [
        sp.simplify(sp.diff(metric[i, j], coordinate).subs(center))
        for coordinate in coords
        for i in range(4)
        for j in range(4)
    ]
    center_gamma = [
        sp.simplify(gamma[rho][mu][nu].subs(center))
        for rho in range(4)
        for mu in range(4)
        for nu in range(4)
    ]
    curvature_screen = sp.Matrix(
        [
            [sp.simplify(rlow(0, 2, 0, 2).subs(center)), sp.simplify(rlow(0, 2, 0, 3).subs(center))],
            [sp.simplify(rlow(0, 3, 0, 2).subs(center)), sp.simplify(rlow(0, 3, 0, 3).subs(center))],
        ]
    )

    # Abstract central curvature and its u derivative. These arrays test all algebraic and
    # differential Bianchi slots without specializing the three free functions.
    A, B, C, Ap, Bp, Cp = sp.symbols("A B C Ap Bp Cp")
    T0 = sp.Matrix([[A, B], [B, C]])
    T1 = sp.Matrix([[Ap, Bp], [Bp, Cp]])
    R = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    dR = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4, 4)
    for i_screen, i in enumerate((2, 3)):
        for j_screen, j in enumerate((2, 3)):
            value = T0[i_screen, j_screen]
            derivative = T1[i_screen, j_screen]
            for p, q, sign1 in ((0, i, 1), (i, 0, -1)):
                for r, s, sign2 in ((0, j, 1), (j, 0, -1)):
                    R[p, q, r, s] = sign1 * sign2 * value
                    dR[0, p, q, r, s] = sign1 * sign2 * derivative

    riemann_pair_symmetry = all(
        sp.simplify(R[i, j, k, l] - R[k, l, i, j]) == 0
        for i in range(4)
        for j in range(4)
        for k in range(4)
        for l in range(4)
    )
    algebraic_bianchi = all(
        sp.simplify(R[a0, b0, c0, d0] + R[a0, c0, d0, b0] + R[a0, d0, b0, c0]) == 0
        for a0 in range(4)
        for b0 in range(4)
        for c0 in range(4)
        for d0 in range(4)
    )
    differential_bianchi = all(
        sp.simplify(
            dR[e0, a0, b0, c0, d0]
            + dR[c0, a0, b0, d0, e0]
            + dR[d0, a0, b0, e0, c0]
        )
        == 0
        for e0 in range(4)
        for a0 in range(4)
        for b0 in range(4)
        for c0 in range(4)
        for d0 in range(4)
    )

    t11, t12, t22 = sp.symbols("t11 t12 t22", real=True)
    T = sp.Matrix([[t11, t12], [t12, t22]])
    zero = sp.zeros(2)
    eye = sp.eye(2)
    generator = zero.row_join(eye).col_join((-T).row_join(zero))
    symplectic_form = zero.row_join(eye).col_join((-eye).row_join(zero))
    hamiltonian_residual = sp.simplify(generator.T * symplectic_form + symplectic_form * generator)

    r = sp.symbols("r", positive=True)
    N = sp.Function("N")(r)
    mu = sp.simplify(r * (1 - N**2) / 2)
    e0 = sp.simplify(-2 * sp.diff(mu, r))
    e1 = sp.simplify(-r * sp.diff(mu, r, 2))
    primary_free_symbols = {
        str(N),
        str(sp.diff(N, r)),
        str(sp.diff(N, r, 2)),
        str(sp.diff(N, r, 3)),
    }

    checks = {
        "metric_inverse_exact": sp.simplify(metric * inverse - sp.eye(4)) == sp.zeros(4),
        "central_metric_independent_of_T": sp.simplify(metric.subs(center) - flat_center) == sp.zeros(4),
        "central_first_metric_jet_independent_of_T": all(value == 0 for value in first_jets),
        "central_connection_independent_of_T": all(value == 0 for value in center_gamma),
        "transverse_curvature_equals_arbitrary_T": sp.simplify(curvature_screen - tidal) == sp.zeros(2),
        "connection_transverse_derivative_carries_T": all(
            sp.simplify(sp.diff(gamma[i][0][0], coordinate).subs(center) - tidal[i - 2, j]) == 0
            for i in (2, 3)
            for j, coordinate in enumerate((x, y))
        ),
        "riemann_pair_symmetry_generic": riemann_pair_symmetry,
        "algebraic_Bianchi_generic": algebraic_bianchi,
        "differential_Bianchi_allows_arbitrary_Tprime": differential_bianchi,
        "Jacobi_generator_Hamiltonian_for_arbitrary_symmetric_T": hamiltonian_residual == sp.zeros(4),
        "tracefree_family_retains_two_free_functions": sp.simplify(sp.trace(tidal.subs(c, -a))) == 0 and b != 0,
        "primary_hierarchy_retains_arbitrary_N_jets": all(
            any(symbol in str(expression) for symbol in primary_free_symbols)
            for expression in (mu, e0, e1)
        ),
    }
    if not all(checks.values()):
        raise AssertionError({name: value for name, value in checks.items() if not value})

    result = {
        "audit": "G283_NEIGHBOR_RELATION_CURVATURE_IDENTITY_NONSELECTION",
        "status": "PASS",
        "landing": "ARBITRARY_SMOOTH_TIDAL_HISTORY_SURVIVES_OWNED_IDENTITIES__VALUE_LAW_STILL_MISSING",
        "checks": checks,
        "arbitrary_functions_retained": ["T_xx(u)", "T_xy(u)", "T_yy(u)"],
        "tracefree_control_functions_retained": ["T_plus(u)", "T_cross(u)"],
        "central_data_fixed_through_metric_jet_order": 1,
        "curvature_enters_at_metric_jet_order": 2,
        "identity_layers_selecting_values": 0,
        "field_equations_adopted": 0,
        "observational_outcomes_used": 0,
        "fitted_coefficients": 0,
        "Xmax_used": False,
        "metric_two_jet_home": "T_ij(u)=R_uiuj on central ray",
        "connection_home": "T_ij(u)=partial_j Gamma^i_uu on central ray",
        "network_home": "D''+T(u)D=0 with symplectic interval transfer",
        "primary_control": {
            "mu": str(mu),
            "E0": str(e0),
            "E1": str(e1),
        },
    }
    (PACKAGE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
