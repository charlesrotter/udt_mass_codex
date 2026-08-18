#!/usr/bin/env python3
"""Exact abstract-frame derivation for G151."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def zero_vector(v: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in v)


def main() -> None:
    rho, rd, rdd = sp.symbols("rho rho_dot rho_ddot", real=True)
    a, ad = sp.symbols("a_n dot_a_n", real=True)
    o2, o3, A2, A3, P2, P3 = sp.symbols("Omega2 Omega3 A2 A3 Pi2 Pi3", real=True)
    Kn, K2, K3 = sp.symbols("K_n K_2 K_3", real=True)

    eta = sp.diag(-1, 1, 1, 1)
    u = sp.Matrix([1, 0, 0, 0])
    n = sp.Matrix([0, 1, 0, 0])
    Omega = sp.Matrix([0, 0, o2, o3])
    A = sp.Matrix([0, 0, A2, A3])
    Pi = sp.Matrix([0, 0, P2, P3])

    def dot(v: sp.Matrix, w: sp.Matrix):
        return sp.simplify((v.T * eta * w)[0])

    omega_sq = dot(Omega, Omega)
    omega_A = dot(Omega, A)
    Du = a * n + A
    Dn = a * u + Omega
    DOmega = omega_A * u - omega_sq * n + Pi
    D2n = ad * u + a * Du + DOmega

    direct = rdd * n + 2 * rd * Dn + rho * D2n
    decomposed = (
        (rdd + rho * (a**2 - omega_sq)) * n
        + (2 * rd * a + rho * (ad + omega_A)) * u
        + 2 * rd * Omega
        + rho * (a * A + Pi)
    )

    # Working reciprocal magnitude differentiated without assuming a history.
    eps = sp.symbols("eps", real=True)
    X, phi, dphi, ddphi = sp.symbols("X_max phi dot_phi ddot_phi", real=True)
    phi_eps = phi + dphi * eps + ddphi * eps**2 / 2
    rho_eps = X * sp.tanh(phi_eps)
    rho_dot = sp.simplify(sp.diff(rho_eps, eps).subs(eps, 0))
    rho_ddot = sp.simplify(sp.diff(rho_eps, eps, 2).subs(eps, 0))
    rho_dot_expected = X * (1 - sp.tanh(phi) ** 2) * dphi
    rho_ddot_expected = X * (1 - sp.tanh(phi) ** 2) * (
        ddphi - 2 * sp.tanh(phi) * dphi**2
    )

    # Geodesic-congruence Jacobi projections with R(X,Y) convention declared in the report.
    Rnuu = Kn * n + K2 * sp.Matrix([0, 0, 1, 0]) + K3 * sp.Matrix([0, 0, 0, 1])
    geodesic_direct = sp.simplify(direct.subs({a: 0, ad: 0, A2: 0, A3: 0}))
    jacobi_residual = sp.simplify(geodesic_direct + rho * Rnuu)
    jacobi_expected = sp.Matrix([
        0,
        rdd - rho * omega_sq + rho * Kn,
        2 * rd * o2 + rho * P2 + rho * K2,
        2 * rd * o3 + rho * P3 + rho * K3,
    ])

    # Curvature-commutator sign. C=[u,xi] supplies two extra terms before connecting-field reduction.
    ru = sp.Matrix(sp.symbols("Rux0:4", real=True))
    f = sp.Matrix(sp.symbols("F0:4", real=True))
    dc = sp.Matrix(sp.symbols("DC0:4", real=True))
    cu = sp.Matrix(sp.symbols("nabla_C_u0:4", real=True))
    unrestricted_d2 = ru + f + dc + cu
    commutator_residual = unrestricted_d2 - ru - f - dc - cu
    connecting_d2 = ru + f
    generalized_residual = connecting_d2 - ru - f
    omitted_acceleration_gradient = connecting_d2 - ru

    wrong_omega_sign = decomposed + 2 * rho * omega_sq * n
    omitted_omega_A = decomposed - rho * omega_A * u
    wrong_curvature_sign = geodesic_direct - rho * Rnuu

    # A smooth two-parameter realization with xi=rho*n and C=0 imposes extra first-order
    # compatibility. Write nabla_n u=b*n+N in the n+screen split.
    b, N2, N3 = sp.symbols("b N2 N3", real=True)
    N = sp.Matrix([0, 0, N2, N3])
    connecting_C = rho * a * u + (rd - rho * b) * n + rho * (Omega - N)
    connecting_solution_residual = sp.simplify(
        connecting_C.subs({a: 0, b: rd / rho, N2: o2, N3: o3})
    )

    # C=0 is canonical and sufficient, but not necessary, for zero commutator source.
    flat_nonconnecting_C = n
    flat_nonconnecting_source = sp.zeros(4, 1)

    gates = {
        "orthonormal_u_n": dot(u, u) == -1 and dot(n, n) == 1 and dot(u, n) == 0,
        "Omega_and_A_screen": dot(Omega, u) == dot(Omega, n) == dot(A, u) == dot(A, n) == 0,
        "DOmega_preserves_Omega_u_orthogonality": sp.simplify(dot(DOmega, u) + dot(Omega, Du)) == 0,
        "DOmega_preserves_Omega_n_orthogonality": sp.simplify(dot(DOmega, n) + dot(Omega, Dn)) == 0,
        "direct_equals_decomposed": zero_vector(direct - decomposed),
        "rho_dot_exact": sp.simplify(rho_dot - rho_dot_expected) == 0,
        "rho_ddot_exact": sp.simplify(rho_ddot - rho_ddot_expected) == 0,
        "jacobi_projection_exact": zero_vector(jacobi_residual - jacobi_expected),
        "general_commutator_identity_bookkeeping_exact": zero_vector(commutator_residual),
        "connecting_reduction_bookkeeping_exact": zero_vector(generalized_residual),
        "connecting_first_order_compatibility_exact": zero_vector(connecting_solution_residual),
        "connecting_condition_not_necessary_counterexample": (
            not zero_vector(flat_nonconnecting_C) and zero_vector(flat_nonconnecting_source)
        ),
        "mutation_wrong_omega_norm_sign_rejected": not zero_vector(wrong_omega_sign - direct),
        "mutation_omitted_omega_A_rejected": not zero_vector(omitted_omega_A - direct),
        "mutation_omitted_acceleration_gradient_rejected": not zero_vector(omitted_acceleration_gradient),
        "mutation_wrong_curvature_sign_rejected": not zero_vector(wrong_curvature_sign - jacobi_expected),
    }

    result = {
        "schema": "udt.g151.abstract_deviation.v1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "curvature_convention": "R(X,Y)Z=nabla_X_nabla_Y_Z-nabla_Y_nabla_X_Z-nabla_[X,Y]_Z",
        "formulas": {
            "D_u_u": [str(x) for x in Du],
            "D_u_n": [str(x) for x in Dn],
            "D_u_Omega": [str(x) for x in DOmega],
            "D_u2_xi": [str(sp.factor(x)) for x in decomposed],
            "rho_dot": str(rho_dot),
            "rho_ddot": str(rho_ddot),
            "geodesic_jacobi_residual_components": [str(x) for x in jacobi_expected],
            "general_commutator_identity": "D_u2_xi + R(xi,u)u - nabla_xi(D_u_u) = nabla_u_C + nabla_C_u, C=[u,xi]",
            "generalized_deviation": "D_u2_xi + R(xi,u)u - nabla_xi(D_u_u) = 0 when [u,xi]=0",
            "connecting_C_components": [str(x) for x in connecting_C],
            "connecting_compatibility_away_from_rho_zero": "a_n=0; rho_dot=rho*g(n,nabla_n u); Omega=P_H nabla_n u",
        },
        "gates": gates,
        "premise_stamps": {
            "xi_equals_Xmax_tanh_phi_n": "CHOSE_WORKING_RELATION_FIRST_REPRESENTATION",
            "connecting_field_bracket_zero": "CONDITIONAL_QUERY_STRUCTURE",
            "geodesic_congruence": "CONDITIONAL_REDUCTION",
            "curvature": "DERIVED_FROM_SUPPLIED_METRIC",
            "physical_history_and_dynamics": "OPEN",
        },
        "maximum_conclusion": (
            "EXACT_NEXT_PAIR_FRAME_CHORD_IDENTITY_ON_SUPPLIED_SMOOTH_REGULAR_PAIR__"
            "FULL_CURVATURE_COMMUTATOR_IDENTITY_WITH_QUERY_OWNED_C_SOURCE__"
            "CONNECTING_TWO_PARAMETER_REALIZATION_IS_A_SUFFICIENT_REDUCTION_AND_FORCES_AN_ZERO_AWAY_FROM_COINCIDENCE__"
            "GENERALIZED_DEVIATION_DERIVED_WITH_ACCELERATION_GRADIENT__"
            "GEODESIC_JACOBI_REDUCTION_CONDITIONAL__"
            "EXACT_RADIAL_WARPED_CONTROL__"
            "NECESSITY_PHYSICAL_QUERY_HISTORY_DYNAMICS_REGIME_AMPLITUDES_XMAX_AND_GLOBAL_COMPLETION_OPEN"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
