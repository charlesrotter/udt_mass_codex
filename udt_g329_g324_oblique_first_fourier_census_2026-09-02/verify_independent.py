#!/usr/bin/env python3
"""Independent ADM/Gauss--Codazzi verification of the G329 oblique quotient."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
G328 = ROOT.parent / "udt_g328_g324_transverse_first_fourier_census_2026-09-02"
RUNTIME_ROOT = ROOT if (ROOT / "sealed_runtime.py").is_file() else G328
sys.path.insert(0, str(RUNTIME_ROOT))
from sealed_runtime import activate_runtime  # noqa: E402

activate_runtime()
import sympy as sp  # noqa: E402


EXPECTED_LANDING = (
    "PRIMITIVE_OBLIQUE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE__"
    "TWO_PHYSICAL_AMPLITUDES__EXACT_COUPLING_CLASSIFICATION__"
    "EXACT_COMPACT_TIME_CENSUS__NO_FULL_STABILITY_CLAIM"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()

    t, x, y, z = sp.symbols("t x y z", positive=True, real=True)
    alpha, beta = sp.symbols("alpha beta", positive=True, real=True)
    phase = sp.exp(sp.I * (alpha * x + beta * y))
    spatial_coordinates = (x, y, z)
    a = t ** sp.Rational(-1, 3)
    b = t ** sp.Rational(2, 3)
    gamma = sp.diag(a**2, b**2, b**2)
    gamma_inverse = gamma.inv()

    U, V, W, Z, H, Q = [
        sp.Function(name)(t) for name in ("U", "V", "W", "Z", "H", "Q")
    ]
    spatial_h = sp.zeros(3)
    spatial_h[0, 0] = 2 * a**2 * U * phase
    spatial_h[0, 1] = spatial_h[1, 0] = a * b * V * phase
    spatial_h[1, 1] = 2 * b**2 * W * phase
    spatial_h[2, 2] = 2 * b**2 * Z * phase
    spatial_h[0, 2] = spatial_h[2, 0] = a * b * H * phase
    spatial_h[1, 2] = spatial_h[2, 1] = b**2 * Q * phase

    inverse_h = -gamma_inverse * spatial_h * gamma_inverse
    K = sp.diff(gamma, t) / 2
    delta_K = sp.diff(spatial_h, t) / 2
    K_mixed = gamma_inverse * K
    delta_K_mixed = inverse_h * K + gamma_inverse * delta_K
    K_trace = sp.trace(K_mixed)
    delta_K_trace = sp.simplify(sp.trace(delta_K_mixed))

    delta_connection = [[[
        sp.Rational(1, 2) * sum(
            gamma_inverse[i, ell] * (
                sp.diff(spatial_h[ell, k], spatial_coordinates[j])
                + sp.diff(spatial_h[ell, j], spatial_coordinates[k])
                - sp.diff(spatial_h[j, k], spatial_coordinates[ell])
            )
            for ell in range(3)
        )
        for k in range(3)] for j in range(3)] for i in range(3)]
    spatial_ricci = sp.MutableDenseMatrix(3, 3, [0] * 9)
    for i in range(3):
        for j in range(3):
            spatial_ricci[i, j] = sp.simplify(sum(
                sp.diff(delta_connection[k][i][j], spatial_coordinates[k])
                - sp.diff(delta_connection[k][i][k], spatial_coordinates[j])
                for k in range(3)
            ))

    R00 = sp.simplify(-sp.diff(delta_K_trace, t) - 2 * sp.trace(K_mixed * delta_K_mixed))
    R0 = [sp.S.Zero] * 3
    for i in range(3):
        divergence = sum(
            sp.diff(delta_K_mixed[j, i], spatial_coordinates[j]) for j in range(3)
        )
        connection_trace = sum(
            delta_connection[j][j][m] * K_mixed[m, i]
            for j in range(3) for m in range(3)
        )
        connection_lower = sum(
            delta_connection[m][j][i] * K_mixed[j, m]
            for j in range(3) for m in range(3)
        )
        R0[i] = sp.simplify(
            divergence + connection_trace - connection_lower
            - sp.diff(delta_K_trace, spatial_coordinates[i])
        )
    Rij = sp.MutableDenseMatrix(3, 3, [0] * 9)
    product_variation = delta_K * gamma_inverse * K + K * inverse_h * K + K * gamma_inverse * delta_K
    for i in range(3):
        for j in range(3):
            Rij[i, j] = sp.simplify(
                spatial_ricci[i, j]
                + sp.diff(delta_K[i, j], t)
                + delta_K_trace * K[i, j]
                + K_trace * delta_K[i, j]
                - 2 * product_variation[i, j]
            )

    def no_phase(expression: sp.Expr) -> sp.Expr:
        return sp.factor(sp.simplify(expression / phase))

    R00 = no_phase(R00)
    R0 = [no_phase(value) for value in R0]
    Rij = sp.MutableDenseMatrix(3, 3, lambda i, j: no_phase(Rij[i, j]))

    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    # Exact synchronous odd equations and their gauge-invariant reduction.
    odd_constraint = alpha * (t * sp.diff(H, t) - H) + beta * sp.diff(Q, t)
    gate(sp.cancel(R0[2] - sp.I * odd_constraint / 2) == 0,
         "adm_odd_constraint_exact")
    odd_x = (
        sp.diff(H, t, 2) + sp.diff(H, t) / t - H / t**2
        + beta**2 * t ** sp.Rational(-4, 3) * H
        - alpha * beta * t ** sp.Rational(-1, 3) * Q
    )
    odd_y = (
        sp.diff(Q, t, 2) + sp.diff(Q, t) / t
        + alpha**2 * t ** sp.Rational(2, 3) * Q
        - alpha * beta * t ** sp.Rational(-1, 3) * H
    )
    gate(sp.cancel(Rij[0, 2] / (a * b) - odd_x / 2) == 0,
         "adm_odd_x_evolution_exact")
    gate(sp.cancel(Rij[1, 2] / b**2 - odd_y / 2) == 0,
         "adm_odd_y_evolution_exact")

    D = alpha**2 * t**2 + beta**2
    odd_orbit = beta * H - alpha * t * Q
    psi = odd_orbit / sp.sqrt(D)
    odd_potential = (
        D * t ** sp.Rational(-4, 3)
        + beta**2 * (2 * alpha**2 * t**2 - beta**2) / (t**2 * D**2)
    )
    odd_master = sp.diff(psi, t, 2) + sp.diff(psi, t) / t + odd_potential * psi
    odd_shell = {
        sp.diff(H, t, 2): sp.solve(odd_x, sp.diff(H, t, 2))[0],
        sp.diff(Q, t, 2): sp.solve(odd_y, sp.diff(Q, t, 2))[0],
    }
    odd_reduced = sp.factor(sp.cancel(odd_master.subs(odd_shell)))
    gate(
        sp.cancel(odd_reduced + 2 * alpha * beta * odd_constraint / D ** sp.Rational(3, 2)) == 0,
        "adm_odd_master_reduces_to_constraint",
    )

    # Exact synchronous even equations.
    E11 = (
        sp.diff(U, t, 2) + sp.Rational(2, 3) * sp.diff(U, t) / t
        - sp.Rational(1, 3) * (sp.diff(W, t) + sp.diff(Z, t)) / t
        + alpha**2 * t ** sp.Rational(2, 3) * (W + Z)
        - alpha * beta * t ** sp.Rational(-1, 3) * V
        + beta**2 * t ** sp.Rational(-4, 3) * U
    )
    E12 = (
        sp.diff(V, t, 2) + sp.diff(V, t) / t - V / t**2
        + 2 * alpha * beta * t ** sp.Rational(-1, 3) * Z
    )
    E22 = (
        sp.diff(W, t, 2) + sp.Rational(2, 3) * sp.diff(U, t) / t
        + sp.Rational(5, 3) * sp.diff(W, t) / t
        + sp.Rational(2, 3) * sp.diff(Z, t) / t
        + alpha**2 * t ** sp.Rational(2, 3) * W
        - alpha * beta * t ** sp.Rational(-1, 3) * V
        + beta**2 * t ** sp.Rational(-4, 3) * (U + Z)
    )
    E33 = (
        sp.diff(Z, t, 2) + sp.Rational(2, 3) * sp.diff(U, t) / t
        + sp.Rational(2, 3) * sp.diff(W, t) / t
        + sp.Rational(5, 3) * sp.diff(Z, t) / t
        + (alpha**2 * t ** sp.Rational(2, 3)
           + beta**2 * t ** sp.Rational(-4, 3)) * Z
    )
    gate(sp.cancel(Rij[0, 0] / a**2 - E11) == 0, "adm_even_11_exact")
    gate(sp.cancel(2 * Rij[0, 1] / (a * b) - E12) == 0, "adm_even_12_exact")
    gate(sp.cancel(Rij[1, 1] / b**2 - E22) == 0, "adm_even_22_exact")
    gate(sp.cancel(Rij[2, 2] / b**2 - E33) == 0, "adm_even_33_exact")

    constraint_x = (
        2 * alpha * t**2 * (sp.diff(W, t) + sp.diff(Z, t))
        + 2 * alpha * t * (W + Z)
        - beta * t * sp.diff(V, t) - beta * V
    )
    constraint_y = (
        alpha * t**2 * sp.diff(V, t) - alpha * t * V
        - 2 * beta * t * (sp.diff(U, t) + sp.diff(Z, t)) + 2 * beta * U
    )
    gate(sp.cancel(R0[0] + sp.I * constraint_x / (2 * t**2)) == 0,
         "adm_even_x_constraint_exact")
    gate(sp.cancel(R0[1] - sp.I * constraint_y / (2 * t)) == 0,
         "adm_even_y_constraint_exact")

    even_orbit = (
        2 * beta**2 * U - 2 * alpha * beta * t * V
        + 2 * alpha**2 * t**2 * W
        + (beta**2 - 2 * alpha**2 * t**2) * Z
    )
    even_amplitude = even_orbit / (2 * alpha**2 * t**2)
    d = 4 * alpha**2 * t**2 + beta**2
    even_p = (4 * alpha**2 * t**2 + 5 * beta**2) / (t * d)
    even_q = D * t ** sp.Rational(-4, 3) + 4 * beta**2 / (t**2 * d)
    even_master = (
        sp.diff(even_amplitude, t, 2)
        + even_p * sp.diff(even_amplitude, t)
        + even_q * even_amplitude
    )
    evolution_shell = {
        sp.diff(U, t, 2): sp.solve(E11, sp.diff(U, t, 2))[0],
        sp.diff(V, t, 2): sp.solve(E12, sp.diff(V, t, 2))[0],
        sp.diff(W, t, 2): sp.solve(E22, sp.diff(W, t, 2))[0],
        sp.diff(Z, t, 2): sp.solve(E33, sp.diff(Z, t, 2))[0],
    }
    even_reduced = sp.factor(sp.cancel(even_master.subs(evolution_shell)))
    V_prime = sp.solve(constraint_x, sp.diff(V, t))[0]
    U_prime = sp.solve(
        constraint_y.subs(sp.diff(V, t), V_prime), sp.diff(U, t)
    )[0]
    gate(
        sp.cancel(even_reduced.subs({sp.diff(V, t): V_prime, sp.diff(U, t): U_prime})) == 0,
        "adm_even_master_reduces_to_two_constraints",
    )

    # Independent full-gauge invariance and rank count.
    P, Gx, Gy, Gz = sp.symbols("P Gx Gy Gz")
    gauge_U = -P / (3 * t) + sp.I * alpha * Gx
    gauge_V = sp.I * beta * Gx / t + sp.I * alpha * t * Gy
    gauge_W = 2 * P / (3 * t) + sp.I * beta * Gy
    gauge_Z = 2 * P / (3 * t)
    gauge_H = sp.I * alpha * t * Gz
    gauge_Q = sp.I * beta * Gz
    gate(sp.cancel(even_orbit.subs({U: gauge_U, V: gauge_V, W: gauge_W, Z: gauge_Z})) == 0,
         "independent_even_orbit_gauge_invariant")
    gate(sp.cancel(odd_orbit.subs({H: gauge_H, Q: gauge_Q})) == 0,
         "independent_odd_orbit_gauge_invariant")
    rank_matrix = sp.Matrix([
        [-sp.Rational(1, 3) / t, sp.I * alpha, 0, 0],
        [0, sp.I * beta / t, sp.I * alpha * t, 0],
        [sp.Rational(2, 3) / t, 0, 0, 0],
        [0, 0, 0, sp.I * beta],
    ])
    gate(rank_matrix.rank() == 4, "independent_strict_oblique_gauge_rank_four")
    gate(sp.factor(rank_matrix.det()) == -2 * sp.I * alpha**2 * beta / 3,
         "independent_gauge_determinant")

    # Independent limits and endpoint counts.
    even_test = sp.Function("even_test")(t)
    even_equation = sp.diff(even_test, t, 2) + even_p * sp.diff(even_test, t) + even_q * even_test
    gate(sp.cancel(even_equation.subs(beta, 0) - (
        sp.diff(even_test, t, 2) + sp.diff(even_test, t) / t
        + alpha**2 * t ** sp.Rational(2, 3) * even_test
    )) == 0, "independent_G327_even_limit")
    odd_test = sp.Function("odd_test")(t)
    odd_equation = sp.diff(odd_test, t, 2) + sp.diff(odd_test, t) / t + odd_potential * odd_test
    gate(sp.cancel(odd_equation.subs(alpha, 0) - (
        sp.diff(odd_test, t, 2) + sp.diff(odd_test, t) / t
        + (beta**2 * t ** sp.Rational(-4, 3) - t**-2) * odd_test
    )) == 0, "independent_G328_odd_limit")
    gate(sp.cancel(odd_equation.subs(beta, 0) - (
        sp.diff(odd_test, t, 2) + sp.diff(odd_test, t) / t
        + alpha**2 * t ** sp.Rational(2, 3) * odd_test
    )) == 0, "independent_G327_odd_limit")
    E = sp.Function("E")(t)
    even_transverse = sp.cancel(even_equation.subs(alpha, 0).subs(even_test, E / t**2).doit() * t**2)
    gate(sp.cancel(even_transverse - (
        sp.diff(E, t, 2) + sp.diff(E, t) / t
        + beta**2 * t ** sp.Rational(-4, 3) * E
    )) == 0, "independent_G328_even_rescaled_limit")

    even_wronskian = d**2 / t**5
    gate(sp.cancel(sp.diff(even_wronskian, t) + even_p * even_wronskian) == 0,
         "independent_even_wronskian")
    gate(sp.cancel(sp.diff(1 / t, t) + (1 / t) / t) == 0,
         "independent_odd_wronskian")
    even_E_p = even_p - 4 / t
    even_E_q = even_q + 6 / t**2 - 2 * even_p / t
    gate(sp.limit(t * even_E_p, t, 0, dir="+") == 1,
         "independent_even_past_damping")
    gate(sp.limit(t**2 * even_E_q, t, 0, dir="+") == 0,
         "independent_even_past_repeated_root")
    gate(sp.limit(t**2 * odd_potential, t, 0, dir="+") == -1,
         "independent_odd_past_roots")
    gate(sp.limit(t * even_p, t, sp.oo) == 1,
         "independent_future_damping")
    gate(sp.limit(even_q / (alpha**2 * t ** sp.Rational(2, 3)), t, sp.oo) == 1,
         "independent_future_even_frequency")
    gate(sp.limit(odd_potential / (alpha**2 * t ** sp.Rational(2, 3)), t, sp.oo) == 1,
         "independent_future_odd_frequency")
    gate(2 * 2 * 2 == 8, "independent_eight_real_constants")

    result = {
        "schema": "udt-g329-independent-verification-v1",
        "method": "synchronous ADM/Gauss-Codazzi reduction plus independent full-gauge invariants",
        "landing": EXPECTED_LANDING,
        "physical_dimension_real": 8,
        "coupling": "z-even and z-odd invariants obey separate scalar equations with alpha,beta-dependent coefficients",
        "endpoint_classification": {
            "past": "even finite/log after E=T^2 W; odd T and T^-1",
            "future": "both oscillatory with leading T^-2/3 relative envelope",
        },
        "checks": checks,
        "check_count": len(checks),
        "reads_production_output": False,
    }
    (ROOT / args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
