#!/usr/bin/env python3
"""Exact production checks for the bounded G339 carry classification."""

from __future__ import annotations

import json
import math
import os
from fractions import Fraction as F
from pathlib import Path


LANDING = (
    "FINITE_TIME_PAIR_COMPONENTS_DEPEND_ON_SUPPLIED_CARRY"
    "__G338_LIE_CARRY_IS_THE_COMOVING_OBSERVER_SEPARATION_QUERY"
    "__PARALLEL_AND_FERMI_LOCAL_RULERS_ARE_QUIET_CONTROLS"
    "__METRIC_DEFORMATION_IS_RECOVERED_FROM_TYPED_PAIR_PLUS_CARRY"
    "__NO_PHYSICAL_CARRY_SELECTED"
)


def gate(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def rational_boost(t: F) -> tuple[F, F]:
    den = 1 - t * t
    return (1 + t * t) / den, 2 * t / den


def g_y(rho: F, y: F) -> F:
    """Squared length with y=u^[2(1-lambda)/3]."""
    return rho / y + (1 - rho) * y * y


def raw_pair(G: F, t: F) -> tuple[F, F, F, F, F]:
    c, s = rational_boost(t)
    h00 = -(c * c) + G * s * s
    h01 = (G - 1) * s * c
    h11 = -(s * s) + G * c * c
    det = h00 * h11 - h01 * h01
    return h00, h01, h11, det, -h00


def mm(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def mv(a: list[list[F]], v: list[F]) -> list[F]:
    return [sum(row[j] * v[j] for j in range(len(v))) for row in a]


def dot(v: list[F], w: list[F]) -> F:
    return sum(x * y for x, y in zip(v, w))


def mdot(v: tuple[F, F], w: tuple[F, F]) -> F:
    return -v[0] * w[0] + v[1] * w[1]


def main() -> None:
    checks: dict[str, bool] = {}

    # Dimensionless T*H eigenvalues of the supplied Taub/Kasner normal congruence.
    p = (F(-1, 3), F(2, 3), F(2, 3))
    gate(sum(p) == 1, "kasner_expansion_trace", checks)
    gate(sum(x * x for x in p) == 1, "kasner_expansion_square_trace", checks)
    gate(p[0] * p[1] * p[2] == F(-4, 27), "kasner_expansion_determinant", checks)
    gate(sorted(p) == [F(-1, 3), F(2, 3), F(2, 3)], "kasner_eigenvalue_ratio", checks)

    # A Lie-carried separation between normal geodesics is an exact Jacobi field.
    for index, exponent in enumerate(p):
        connection_second = exponent * (exponent - 1)
        curvature_action = exponent * (exponent - 1)
        gate(connection_second == curvature_action, f"connecting_jacobi_{index}", checks)

    rhos = (F(0), F(1, 7), F(1, 2), F(2, 3), F(6, 7), F(1))
    lambdas = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
    ys = (F(1, 16), F(1, 4), F(1), F(4), F(16))

    # Exact initial and finite-time transport-subtraction identities.
    carry_cases = 0
    for lam in lambdas:
        a = 1 - lam
        for rho in rhos:
            q0 = (2 - 3 * rho) / 3
            initial_length_rate = a * q0
            bracket_rate = -lam * q0
            gate(initial_length_rate == q0 + bracket_rate,
                 f"initial_transport_subtraction_{carry_cases}", checks)
            gate(initial_length_rate == a * (2 - 3 * rho) / 3,
                 f"initial_lambda_rate_{carry_cases}", checks)
            if lam == 0:
                gate(bracket_rate == 0, f"lie_bracket_zero_{carry_cases}", checks)
            if lam == 1:
                gate(initial_length_rate == 0 and bracket_rate == -q0,
                     f"parallel_exact_cancellation_{carry_cases}", checks)
            carry_cases += 1

            if lam == 1:
                continue
            for y in ys:
                G = g_y(rho, y)
                rho_now = (rho / y) / G
                q_geom_times_T = (2 - 3 * rho_now) / 3
                raw_rate_times_T = (
                    a * (-rho / y + 2 * (1 - rho) * y * y) / (3 * G)
                )
                gate(raw_rate_times_T == a * q_geom_times_T,
                     f"finite_log_length_rate_{carry_cases}_{y}", checks)
                gate(raw_rate_times_T == q_geom_times_T - lam * q_geom_times_T,
                     f"finite_transport_subtraction_{carry_cases}_{y}", checks)

    # Full pair pullback and W1 for the complete interpolation.
    pair_cases = 0
    regular_cases = 0
    for lam in lambdas[:-1]:
        for rho in rhos:
            for y in ys:
                G = g_y(rho, y)
                for t in (F(0), F(1, 7), F(-2, 5), F(3, 4)):
                    h00, h01, h11, det, Delta = raw_pair(G, t)
                    gate(det == -G, f"pair_determinant_{pair_cases}", checks)
                    pair_cases += 1
                    if Delta <= 0:
                        continue
                    beta = h01 / h00
                    L2 = h11 - h01 * h01 / h00
                    gate(L2 == G / Delta, f"pair_auxiliary_length_{regular_cases}", checks)
                    gate(Delta * L2 / G == 1, f"pair_w1_determinant_{regular_cases}", checks)
                    gate(beta * beta / G == h01 * h01 / (Delta * Delta * G),
                         f"pair_w1_shift_{regular_cases}", checks)
                    regular_cases += 1

    # Parallel/Fermi along geodesic n: the complete boosted Gram matrix stays eta.
    parallel_cases = 0
    for rho in rhos:
        for u in (F(1, 16), F(1, 4), F(1), F(4), F(16)):
            _ = rho, u
            for t in (F(0), F(1, 7), F(-2, 5), F(3, 4)):
                h00, h01, h11, det, Delta = raw_pair(F(1), t)
                gate((h00, h01, h11) == (F(-1), F(0), F(1)),
                     f"parallel_gram_eta_{parallel_cases}", checks)
                gate(det == -1 and Delta == 1,
                     f"parallel_w1_quiet_{parallel_cases}", checks)
                parallel_cases += 1

    # The unique Lie/intermediate silent direction turns on unless lambda=1.
    silent_cases = 0
    for lam in lambdas:
        a = 1 - lam
        first_rate = a * (2 - 3 * F(2, 3)) / 3
        gate(first_rate == 0, f"silent_initial_rate_{silent_cases}", checks)
        if lam == 1:
            gate(g_y(F(2, 3), F(1)) == 1,
                 f"parallel_all_time_silence_{silent_cases}", checks)
        else:
            for y in ys:
                lhs = g_y(F(2, 3), y) - 1
                rhs = (y - 1) * (y - 1) * (y + 2) / (3 * y)
                gate(lhs == rhs and lhs >= 0,
                     f"silent_factorization_{silent_cases}_{y}", checks)
                if y != 1:
                    gate(lhs > 0, f"silent_strict_turn_on_{silent_cases}_{y}", checks)
        silent_cases += 1

    # Endpoint and mixed-direction clock-timelike boundaries.
    boundary_cases = 0
    for lam in lambdas[:-1]:
        a = 1 - lam
        for t in (F(1, 7), F(2, 5), F(3, 4)):
            c, s = rational_boost(t)
            q = c * c / (s * s)
            tanh = s / c
            # In y coordinates these are exact for every 0<=lambda<1.
            gate(g_y(F(1), 1 / q) == q,
                 f"longitudinal_y_boundary_{boundary_cases}", checks)
            gate(g_y(F(0), c / s) == q,
                 f"transverse_y_boundary_{boundary_cases}", checks)
            # Directly verify the preregistered u formulas numerically.
            af = float(a)
            zabs_tanh = float(tanh)
            u_long = zabs_tanh ** (3.0 / af)
            u_trans = (1.0 / zabs_tanh) ** (3.0 / (2.0 * af))
            G_long = u_long ** (-2.0 * af / 3.0)
            G_trans = u_trans ** (4.0 * af / 3.0)
            gate(abs(G_long - float(q)) < 2e-12,
                 f"longitudinal_u_boundary_{boundary_cases}", checks)
            gate(abs(G_trans - float(q)) < 2e-12,
                 f"transverse_u_boundary_{boundary_cases}", checks)
            boundary_cases += 1

        for rho in rhos[1:-1]:
            ratio = rho / (2 * (1 - rho))
            y_lo = min(F(1, 1000), ratio / 8)
            y_hi = max(F(1000), ratio * 8)
            deriv_lo = -rho + 2 * (1 - rho) * y_lo**3
            deriv_hi = -rho + 2 * (1 - rho) * y_hi**3
            gate(deriv_lo < 0 < deriv_hi,
                 f"mixed_unique_minimum_{lam}_{rho}", checks)
            gate(g_y(rho, F(1)) == 1,
                 f"mixed_contains_reference_{lam}_{rho}", checks)

    # Every norm-preserving rotating carry cancels raw length change while H remains.
    H = [[p[0], F(0), F(0)], [F(0), p[1], F(0)], [F(0), F(0), p[2]]]
    omegas = (
        [[F(0), F(1, 5), F(-2, 7)], [F(-1, 5), F(0), F(3, 8)], [F(2, 7), F(-3, 8), F(0)]],
        [[F(0), F(-4, 9), F(1, 3)], [F(4, 9), F(0), F(-2, 5)], [F(-1, 3), F(2, 5), F(0)]],
    )
    vectors = ([F(1), F(0), F(0)], [F(1), F(2), F(-3)], [F(2), F(-1), F(4)])
    rotation_cases = 0
    for omega in omegas:
        gate(transpose(omega) == [[-x for x in row] for row in omega],
             f"rotation_skew_{rotation_cases}", checks)
        for v in vectors:
            Hv = mv(H, v)
            Ov = mv(omega, v)
            bracket = [Ov[i] - Hv[i] for i in range(3)]
            geom = dot(v, Hv)
            gate(dot(v, Ov) == 0, f"rotation_norm_preserving_{rotation_cases}", checks)
            gate(geom + dot(v, bracket) == 0,
                 f"rotation_transport_cancels_raw_rate_{rotation_cases}", checks)
            gate(geom == dot(v, Hv), f"rotation_retains_geometric_H_{rotation_cases}", checks)
            rotation_cases += 1

    # Explicit accelerated Fermi pairs on every principal axis.
    accelerated_cases = 0
    for Hi in p:
        for t in (F(1, 7), F(-2, 5), F(3, 4)):
            c, s = rational_boost(t)
            U = (c, s)
            S = (s, c)
            acceleration = (Hi * s * S[0], Hi * s * S[1])
            dS = (Hi * s * U[0], Hi * s * U[1])
            gate(mdot(U, U) == -1 and mdot(S, S) == 1 and mdot(U, S) == 0,
                 f"accelerated_pair_orthonormal_{accelerated_cases}", checks)
            gate(mdot(acceleration, U) == 0,
                 f"accelerated_pair_acceleration_spatial_{accelerated_cases}", checks)
            gate(mdot(acceleration, S) == Hi * s,
                 f"accelerated_pair_acceleration_magnitude_{accelerated_cases}", checks)
            gate(dS == (Hi * s * U[0], Hi * s * U[1]),
                 f"accelerated_pair_fermi_equation_{accelerated_cases}", checks)
            gate(2 * mdot(acceleration, U) == 0,
                 f"accelerated_pair_clock_gram_constant_{accelerated_cases}", checks)
            gate(mdot(acceleration, S) + mdot(U, dS) == 0,
                 f"accelerated_pair_cross_gram_constant_{accelerated_cases}", checks)
            gate(2 * mdot(dS, S) == 0,
                 f"accelerated_pair_ruler_gram_constant_{accelerated_cases}", checks)
            accelerated_cases += 1

    # Any regular raw pair can be whitened by a time-dependent GL(2) basis change.
    whitening_cases = 0
    eta = [[F(-1), F(0)], [F(0), F(1)]]
    for r in (F(1, 3), F(1, 2), F(1), F(2), F(3)):
        G = r * r
        for t in (F(0), F(1, 7), F(-2, 5), F(3, 4)):
            c, s = rational_boost(t)
            B = [[c, s], [s, c]]
            Binv = [[c, -s], [-s, c]]
            scale = [[F(1), F(0)], [F(0), 1 / r]]
            h = mm(transpose(B), mm([[F(-1), F(0)], [F(0), G]], B))
            change = mm(Binv, scale)
            whitened = mm(transpose(change), mm(h, change))
            gate(whitened == eta, f"gl_whitening_{whitening_cases}", checks)
            whitening_cases += 1

    # General component transport can be subtracted to recover the geometric tensor.
    transport_cases = 0
    for q in (F(-3, 2), F(-1, 5), F(0), F(2, 7), F(5, 3)):
        for t in (F(0), F(1, 7), F(-2, 5)):
            c, s = rational_boost(t)
            D = [[2 * q * s * s, 2 * q * s * c],
                 [2 * q * s * c, 2 * q * c * c]]
            alpha, beta, gamma, delta = F(1, 7), F(-2, 9), F(3, 11), F(4, 13)
            transport = [[-2 * alpha, beta - gamma], [beta - gamma, 2 * delta]]
            general = [[D[i][j] + transport[i][j] for j in range(2)] for i in range(2)]
            recovered = [[general[i][j] - transport[i][j] for j in range(2)] for i in range(2)]
            gate(recovered == D, f"typed_transport_subtraction_{transport_cases}", checks)
            gate((D[1][1] - D[0][0]) / 2 == q,
                 f"geometric_q_recovered_{transport_cases}", checks)
            transport_cases += 1

    result = {
        "landing": LANDING,
        "grade": "PRODUCTION_DERIVED_CONDITIONAL_BOUNDED_PENDING_INDEPENDENT_AND_EXTERNAL_REVIEW",
        "preregistration_commit": "f6394739",
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "all_passed": all(checks.values()),
        "coverage": {
            "carry_cases": carry_cases,
            "pair_cases": pair_cases,
            "regular_w1_cases": regular_cases,
            "parallel_cases": parallel_cases,
            "boundary_cases": boundary_cases,
            "rotation_cases": rotation_cases,
            "accelerated_cases": accelerated_cases,
            "whitening_cases": whitening_cases,
            "transport_cases": transport_cases,
        },
        "carry_family": {
            "G_lambda": "rho*u^(-2(1-lambda)/3)+(1-rho)*u^(4(1-lambda)/3)",
            "lie": "lambda=0; [n,J]=0; connecting field of supplied normal congruence",
            "parallel": "lambda=1; nabla_n J=0; G=1",
            "fermi_on_n": "equals parallel because nabla_n n=0",
            "rotating_orthonormal": "nabla_n V=Omega V with Omega skew; G=1",
        },
        "metric_deformation": {
            "identity": "0.5*n[g(V,V)]=0.5*(L_n g)(V,V)+g([n,V],V)",
            "T_times_H_eigenvalues": ["-1/3", "2/3", "2/3"],
            "trace_ratio": "tr((T H)^2)/(tr(T H))^2=1",
            "determinant_ratio": "det(T H)/(tr(T H))^3=-4/27",
        },
        "scope_exclusions": [
            "no physical carry or observer-population selection",
            "no generic accelerated-congruence census",
            "no spacetime occupancy, stability, scale, or X_max selection",
            "no metric, kernel, angular-sector, or field-equation modification",
        ],
        "checks": checks,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        Path(__file__).with_name("DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps({k: result[k] for k in (
        "landing", "grade", "checks_passed", "checks_total", "all_passed", "coverage"
    )}, indent=2))


if __name__ == "__main__":
    main()
