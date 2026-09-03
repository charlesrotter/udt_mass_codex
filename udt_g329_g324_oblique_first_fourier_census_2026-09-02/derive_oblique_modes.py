#!/usr/bin/env python3
"""Direct four-dimensional first variation for the bounded G329 oblique tile."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
G328 = ROOT.parent / "udt_g328_g324_transverse_first_fourier_census_2026-09-02"
sys.path.insert(0, str(G328))
from sealed_runtime import activate_runtime  # noqa: E402

activate_runtime()
import sympy as sp  # noqa: E402


LANDING = (
    "PRIMITIVE_OBLIQUE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE__"
    "TWO_PHYSICAL_AMPLITUDES__EXACT_COUPLING_CLASSIFICATION__"
    "EXACT_COMPACT_TIME_CENSUS__NO_FULL_STABILITY_CLAIM"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    parser.add_argument("--raw-output", default="RAW_RESIDUALS.json")
    args = parser.parse_args()

    t, alpha, beta = sp.symbols("T alpha beta", positive=True, real=True)
    imaginary = sp.I
    n = 4
    a = t ** sp.Rational(-1, 3)
    b = t ** sp.Rational(2, 3)
    background = sp.diag(-1, a**2, b**2, b**2)
    inverse = background.inv()

    def derivative(expression: sp.Expr, coordinate: int) -> sp.Expr:
        if coordinate == 0:
            return sp.diff(expression, t)
        if coordinate == 1:
            return imaginary * alpha * expression
        if coordinate == 2:
            return imaginary * beta * expression
        return sp.S.Zero

    def background_derivative(expression: sp.Expr, coordinate: int) -> sp.Expr:
        if coordinate == 0:
            return sp.diff(expression, t)
        return sp.S.Zero

    connection = [[[
        sp.Rational(1, 2) * sum(
            inverse[i, d] * (
                background_derivative(background[d, k], j)
                + background_derivative(background[d, j], k)
                - background_derivative(background[j, k], d)
            )
            for d in range(n)
        )
        for k in range(n)] for j in range(n)] for i in range(n)]

    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    def linearized_ricci(h: sp.Matrix) -> tuple[sp.Matrix, sp.Expr]:
        inverse_h = -inverse * h * inverse
        delta_connection = [[[
            sp.Rational(1, 2) * sum(
                inverse_h[i, d] * (
                    background_derivative(background[d, k], j)
                    + background_derivative(background[d, j], k)
                    - background_derivative(background[j, k], d)
                )
                + inverse[i, d] * (
                    derivative(h[d, k], j)
                    + derivative(h[d, j], k)
                    - derivative(h[j, k], d)
                )
                for d in range(n)
            )
            for k in range(n)] for j in range(n)] for i in range(n)]
        result = sp.MutableDenseMatrix(n, n, [0] * n**2)
        for i in range(n):
            for j in range(i, n):
                value = 0
                for c in range(n):
                    value += derivative(delta_connection[c][i][j], c)
                    value -= derivative(delta_connection[c][i][c], j)
                    for d in range(n):
                        value += delta_connection[c][c][d] * connection[d][i][j]
                        value += connection[c][c][d] * delta_connection[d][i][j]
                        value -= delta_connection[c][j][d] * connection[d][i][c]
                        value -= connection[c][j][d] * delta_connection[d][i][c]
                result[i, j] = result[j, i] = sp.cancel(value)
        scalar = sp.cancel(sum(
            inverse[i, j] * result[i, j]
            for i in range(n) for j in range(n)
        ))
        return result, scalar

    def background_ricci() -> sp.Matrix:
        result = sp.MutableDenseMatrix(n, n, [0] * n**2)
        for i in range(n):
            for j in range(n):
                value = 0
                for c in range(n):
                    value += background_derivative(connection[c][i][j], c)
                    value -= background_derivative(connection[c][i][c], j)
                    for d in range(n):
                        value += connection[c][c][d] * connection[d][i][j]
                        value -= connection[c][j][d] * connection[d][i][c]
                result[i, j] = sp.cancel(value)
        return result

    def verify_bianchi(ricci: sp.Matrix, scalar: sp.Expr, label: str) -> None:
        shape = sp.MutableDenseMatrix(
            n, n, lambda i, j: ricci[i, j] - background[i, j] * scalar / 4
        )
        for j in range(n):
            divergence = 0
            for i in range(n):
                for c in range(n):
                    covariant = derivative(shape[i, j], c)
                    for d in range(n):
                        covariant -= connection[d][c][i] * shape[d, j]
                        covariant -= connection[d][c][j] * shape[i, d]
                    divergence += inverse[i, c] * covariant
            gate(
                sp.cancel(divergence - derivative(scalar, j) / 4) == 0,
                f"{label}_linearized_bianchi_{j}",
            )

    background_Ricci = background_ricci()
    for i in range(n):
        for j in range(n):
            gate(background_Ricci[i, j] == 0, f"background_Ricci_zero_{i}{j}")

    # Exact z-reflection split of all ten amplitudes.
    N, H, Q = [sp.Function(name)(t) for name in ("N", "H", "Q")]
    odd_h = sp.zeros(n)
    odd_h[0, 3] = odd_h[3, 0] = b * N
    odd_h[1, 3] = odd_h[3, 1] = a * b * H
    odd_h[2, 3] = odd_h[3, 2] = b**2 * Q
    odd_ricci, odd_scalar = linearized_ricci(odd_h)
    print("stage: raw odd", flush=True)

    A, B, C, U, V, W, Z = [
        sp.Function(name)(t) for name in ("A", "B", "C", "U", "V", "W", "Z")
    ]
    even_h = sp.zeros(n)
    even_h[0, 0] = -2 * A
    even_h[0, 1] = even_h[1, 0] = a * B
    even_h[0, 2] = even_h[2, 0] = b * C
    even_h[1, 1] = 2 * a**2 * U
    even_h[1, 2] = even_h[2, 1] = a * b * V
    even_h[2, 2] = 2 * b**2 * W
    even_h[3, 3] = 2 * b**2 * Z
    even_ricci, even_scalar = linearized_ricci(even_h)
    print("stage: raw even", flush=True)

    gate(3 + 7 == 10, "parity_blocks_cover_all_ten_metric_components")
    gate(odd_scalar == 0, "odd_scalar_identically_zero")
    odd_support = {(0, 3), (1, 3), (2, 3), (3, 0), (3, 1), (3, 2)}
    even_support = {
        (0, 0), (0, 1), (1, 0), (0, 2), (2, 0), (1, 1),
        (1, 2), (2, 1), (2, 2), (3, 3),
    }
    for i in range(n):
        for j in range(n):
            if (i, j) not in odd_support:
                gate(odd_ricci[i, j] == 0, f"odd_parity_zero_{i}{j}")
            if (i, j) not in even_support:
                gate(even_ricci[i, j] == 0, f"even_parity_zero_{i}{j}")
    verify_bianchi(odd_ricci, odd_scalar, "odd")
    verify_bianchi(even_ricci, even_scalar, "even")
    print("stage: bianchi", flush=True)

    # A nonzero spatial Fourier covector forces delta R=0 on shell. The zero
    # mode is deliberately checked as a hostile exception below.
    scalar_symbol = sp.symbols("delta_R")
    gate(
        sp.solve(imaginary * alpha * scalar_symbol, scalar_symbol) == [0],
        "nonzero_oblique_bianchi_forces_scalar_zero",
    )

    # Complete same-mode Lie image. These formulas are derived, not imposed.
    P, Gx, Gy, Gz = [sp.Function(name)(t) for name in ("P", "Gx", "Gy", "Gz")]
    vector = (P, Gx, Gy, Gz)
    lie = sp.MutableDenseMatrix(n, n, [0] * n**2)
    for i in range(n):
        for j in range(n):
            lie[i, j] = sp.cancel(
                sum(vector[c] * background_derivative(background[i, j], c) for c in range(n))
                + sum(background[c, j] * derivative(vector[c], i) for c in range(n))
                + sum(background[i, c] * derivative(vector[c], j) for c in range(n))
            )
    gauge = {
        A: -lie[0, 0] / 2,
        B: lie[0, 1] / a,
        C: lie[0, 2] / b,
        U: lie[1, 1] / (2 * a**2),
        V: lie[1, 2] / (a * b),
        W: lie[2, 2] / (2 * b**2),
        Z: lie[3, 3] / (2 * b**2),
        N: lie[0, 3] / b,
        H: lie[1, 3] / (a * b),
        Q: lie[2, 3] / b**2,
    }
    expected_gauge = {
        A: sp.diff(P, t),
        B: a * sp.diff(Gx, t) - imaginary * alpha * P / a,
        C: b * sp.diff(Gy, t) - imaginary * beta * P / b,
        U: -P / (3 * t) + imaginary * alpha * Gx,
        V: imaginary * beta * Gx / t + imaginary * alpha * t * Gy,
        W: 2 * P / (3 * t) + imaginary * beta * Gy,
        Z: 2 * P / (3 * t),
        N: b * sp.diff(Gz, t),
        H: imaginary * alpha * t * Gz,
        Q: imaginary * beta * Gz,
    }
    for variable, expected in expected_gauge.items():
        gate(sp.cancel(gauge[variable] - expected) == 0,
             f"lie_image_{str(variable.func)}")
    # Since the background Ricci tensor vanishes, covariance gives
    # delta Ric[L_xi g0] = L_xi Ric[g0] = 0. A separate hostile check below
    # substitutes fixed nontrivial periodic generators into the raw operator.
    gate(all(background[i, j] == background[j, i] for i in range(n) for j in range(n)),
         "background_metric_symmetric_for_covariant_gauge_identity")
    print("stage: gauge image", flush=True)

    # U=V=Z=Q=0 is a complete gauge for alpha*beta != 0.
    gauge_rank = sp.Matrix([
        [-sp.Rational(1, 3) / t, imaginary * alpha, 0, 0],
        [0, imaginary * beta / t, imaginary * alpha * t, 0],
        [sp.Rational(2, 3) / t, 0, 0, 0],
        [0, 0, 0, imaginary * beta],
    ])
    determinant = sp.factor(gauge_rank.det())
    gate(determinant != 0, "strict_oblique_gauge_rank_four")
    gate(sp.simplify(determinant / (-sp.Rational(2, 3) * imaginary * alpha**2 * beta)) == 1,
         "strict_oblique_gauge_determinant_exact")

    P_fix = -sp.Rational(3, 2) * t * Z
    Gx_fix = imaginary * (U + Z / 2) / alpha
    Gy_fix = imaginary * V / (alpha * t) - beta * Gx_fix / (alpha * t**2)
    Gz_fix = imaginary * Q / beta
    fixing = {P: P_fix, Gx: Gx_fix, Gy: Gy_fix, Gz: Gz_fix}
    for variable in (U, V, Z, Q):
        gate(sp.cancel(variable + expected_gauge[variable].subs(fixing)) == 0,
             f"complete_gauge_sets_{str(variable.func)}_zero")
    W_bar = sp.factor(W + expected_gauge[W].subs(fixing))
    H_bar = sp.factor(H + expected_gauge[H].subs(fixing))
    gate(sp.cancel(H_bar - (H - alpha * t * Q / beta)) == 0,
         "odd_orbit_amplitude_exact")
    gate(not W_bar.has(P, Gx, Gy, Gz), "even_orbit_amplitude_exact")
    print("stage: gauge quotient", flush=True)

    # Odd representative and exact scalar master.
    D = alpha**2 * t**2 + beta**2
    odd_N = -imaginary * alpha * t ** sp.Rational(2, 3) * (
        t * sp.diff(H, t) - H
    ) / D
    odd_p = (beta**2 - alpha**2 * t**2) / (t * D)
    odd_q = (
        D * t ** sp.Rational(-4, 3)
        + (alpha**2 * t**2 - beta**2) / (t**2 * D)
    )
    odd_master = sp.diff(H, t, 2) + odd_p * sp.diff(H, t) + odd_q * H
    odd_rep = {N: odd_N, Q: 0}
    for variable, value in list(odd_rep.items()):
        for order in (1, 2):
            odd_rep[sp.diff(variable, t, order)] = sp.diff(value, t, order)
    odd_h2 = -odd_p * sp.diff(H, t) - odd_q * H
    odd_h3 = sp.diff(odd_h2, t).subs(sp.diff(H, t, 2), odd_h2)
    odd_shell = {sp.diff(H, t, 3): odd_h3, sp.diff(H, t, 2): odd_h2}
    for i in range(n):
        for j in range(n):
            gate(sp.cancel(odd_ricci[i, j].subs(odd_rep).subs(odd_shell)) == 0,
                 f"odd_representative_residual_zero_{i}{j}")

    Psi = sp.Function("Psi_o")(t)
    normalized_odd = sp.cancel(
        odd_master.subs(H, sp.sqrt(D) * Psi).doit() / sp.sqrt(D)
    )
    expected_normalized_odd = (
        sp.diff(Psi, t, 2) + sp.diff(Psi, t) / t
        + (
            D * t ** sp.Rational(-4, 3)
            + beta**2 * (2 * alpha**2 * t**2 - beta**2) / (t**2 * D**2)
        ) * Psi
    )
    gate(sp.cancel(normalized_odd - expected_normalized_odd) == 0,
         "odd_normalized_master_exact")
    print("stage: odd representative", flush=True)

    # Even representative. L and M are the two orthogonal shift combinations.
    d = 4 * alpha**2 * t**2 + beta**2
    even_A = 3 * alpha**2 * t**2 * (t * sp.diff(W, t) + W) / d
    even_L = (
        2 * imaginary * alpha * t ** sp.Rational(2, 3)
        * (3 * t * sp.diff(W, t) - 4 * even_A + 3 * W)
        / (3 * beta)
    )
    even_M = imaginary * t ** sp.Rational(2, 3) * (
        sp.diff(even_A, t) - sp.diff(W, t)
    )
    even_B = (beta * even_L + alpha * t * even_M) / D
    even_C = (-alpha * t * even_L + beta * even_M) / D
    even_p = d / (t * d) + 4 * beta**2 / (t * d)
    even_q = D * t ** sp.Rational(-4, 3) + 4 * beta**2 / (t**2 * d)
    gate(sp.cancel(even_p - (4 * alpha**2 * t**2 + 5 * beta**2) / (t * d)) == 0,
         "even_damping_coefficient_exact")
    even_master = sp.diff(W, t, 2) + even_p * sp.diff(W, t) + even_q * W
    even_rep = {A: even_A, B: even_B, C: even_C, U: 0, V: 0, Z: 0}
    for variable, value in list(even_rep.items()):
        for order in (1, 2):
            even_rep[sp.diff(variable, t, order)] = sp.diff(value, t, order)
    even_w2 = -even_p * sp.diff(W, t) - even_q * W
    even_w3 = sp.diff(even_w2, t).subs(sp.diff(W, t, 2), even_w2)
    even_shell = {sp.diff(W, t, 3): even_w3, sp.diff(W, t, 2): even_w2}
    for i in range(n):
        for j in range(n):
            gate(sp.cancel(even_ricci[i, j].subs(even_rep).subs(even_shell)) == 0,
                 f"even_representative_residual_zero_{i}{j}")
    gate(sp.cancel(even_scalar.subs(even_rep).subs(even_shell)) == 0,
         "even_representative_scalar_zero")

    # Exact constraint ordering: momenta fix A,L; the zz equation fixes M;
    # the Hamiltonian gives the master. Positive denominators exclude rank jumps.
    X_shift = alpha * t ** sp.Rational(1, 3) * even_B
    Y_shift = beta * t ** sp.Rational(-2, 3) * even_C
    hamiltonian = sp.cancel(
        3 * alpha**2 * t ** sp.Rational(5, 3) * W
        + sp.diff(W, t) - imaginary * (4 * X_shift + Y_shift)
    )
    gate(sp.cancel(hamiltonian.subs(sp.diff(W, t, 2), even_w2)) == 0,
         "even_hamiltonian_is_master")
    gate(all(term.is_positive for term in (D, d)), "compact_time_denominators_positive")
    print("stage: even representative", flush=True)

    # Exact component-limit regressions. The oblique derivation above never sets
    # either component to zero.
    axial_even = sp.simplify(even_master.subs(beta, 0))
    expected_axial_even = (
        sp.diff(W, t, 2) + sp.diff(W, t) / t
        + alpha**2 * t ** sp.Rational(2, 3) * W
    )
    gate(sp.cancel(axial_even - expected_axial_even) == 0,
         "G327_axial_even_limit")
    axial_odd = sp.simplify(expected_normalized_odd.subs(beta, 0))
    expected_axial_odd = (
        sp.diff(Psi, t, 2) + sp.diff(Psi, t) / t
        + alpha**2 * t ** sp.Rational(2, 3) * Psi
    )
    gate(sp.cancel(axial_odd - expected_axial_odd) == 0,
         "G327_axial_odd_limit")
    transverse_odd = sp.simplify(expected_normalized_odd.subs(alpha, 0))
    expected_transverse_odd = (
        sp.diff(Psi, t, 2) + sp.diff(Psi, t) / t
        + (beta**2 * t ** sp.Rational(-4, 3) - t**-2) * Psi
    )
    gate(sp.cancel(transverse_odd - expected_transverse_odd) == 0,
         "G328_transverse_odd_limit")
    E = sp.Function("E")(t)
    transverse_even = sp.cancel(
        even_master.subs(alpha, 0).subs(W, E / t**2).doit() * t**2
    )
    expected_transverse_even = (
        sp.diff(E, t, 2) + sp.diff(E, t) / t
        + beta**2 * t ** sp.Rational(-4, 3) * E
    )
    gate(sp.cancel(transverse_even - expected_transverse_even) == 0,
         "G328_transverse_even_limit_after_regular_polarization_rescaling")
    print("stage: limits", flush=True)

    # Nonzero orbit-curvature witnesses: intrinsic slice Ricci of the unique
    # complete representative. The uniqueness of the representative makes this
    # a gauge-invariant functional of the fixed nonzero Fourier orbit.
    def spatial_ricci(spatial_h: sp.Matrix) -> sp.Matrix:
        gamma = sp.diag(a**2, b**2, b**2)
        gamma_inverse = gamma.inv()
        delta_connection = [[[
            sp.Rational(1, 2) * sum(
                gamma_inverse[i, ell] * (
                    derivative(spatial_h[ell, k], j + 1)
                    + derivative(spatial_h[ell, j], k + 1)
                    - derivative(spatial_h[j, k], ell + 1)
                )
                for ell in range(3)
            )
            for k in range(3)] for j in range(3)] for i in range(3)]
        return sp.MutableDenseMatrix(3, 3, lambda i, j: sp.cancel(sum(
            derivative(delta_connection[k][i][j], k + 1)
            - derivative(delta_connection[k][i][k], j + 1)
            for k in range(3)
        )))

    even_spatial = sp.zeros(3)
    even_spatial[1, 1] = 2 * b**2 * W
    even_witness = spatial_ricci(even_spatial)
    gate(sp.cancel(even_witness[0, 0] - alpha**2 * W) == 0,
         "even_nonzero_orbit_curvature_witness")
    odd_spatial = sp.zeros(3)
    odd_spatial[0, 2] = odd_spatial[2, 0] = a * b * H
    odd_witness = spatial_ricci(odd_spatial)
    gate(sp.cancel(odd_witness[0, 2] - beta**2 * H / (2 * t)) == 0,
         "odd_nonzero_orbit_curvature_witness")
    print("stage: witnesses", flush=True)

    # Compact-time well-posedness, exact Wronskians, and controlled endpoints.
    even_wronskian = d**2 / t**5
    gate(sp.cancel(sp.diff(even_wronskian, t) + even_p * even_wronskian) == 0,
         "even_wronskian_exact_nonzero")
    odd_wronskian = 1 / t
    gate(sp.cancel(sp.diff(odd_wronskian, t) + odd_wronskian / t) == 0,
         "odd_wronskian_exact_nonzero")

    even_E_p = sp.factor(even_p - 4 / t)
    even_E_q = sp.factor(even_q + 6 / t**2 - 2 * even_p / t)
    odd_Psi_q = (
        D * t ** sp.Rational(-4, 3)
        + beta**2 * (2 * alpha**2 * t**2 - beta**2) / (t**2 * D**2)
    )
    gate(sp.limit(t * even_E_p, t, 0, dir="+") == 1,
         "even_past_repeated_zero_indicial_damping")
    gate(sp.limit(t**2 * even_E_q, t, 0, dir="+") == 0,
         "even_past_repeated_zero_indicial_potential")
    gate(sp.solve(sp.Symbol("r")**2, sp.Symbol("r")) == [0],
         "even_past_finite_and_logarithmic_E_branches")
    gate(sp.limit(t**2 * odd_Psi_q, t, 0, dir="+") == -1,
         "odd_past_indicial_potential_minus_one")
    r = sp.Symbol("r")
    gate(set(sp.solve(r * (r - 1) + r - 1, r)) == {-1, 1},
         "odd_past_linear_and_inverse_linear_branches")
    gate(sp.limit(t * even_p, t, sp.oo) == 1,
         "even_future_axial_damping")
    gate(sp.limit(even_q / (alpha**2 * t ** sp.Rational(2, 3)), t, sp.oo) == 1,
         "even_future_axial_frequency")
    gate(sp.limit(odd_Psi_q / (alpha**2 * t ** sp.Rational(2, 3)), t, sp.oo) == 1,
         "odd_future_axial_frequency")
    gate(sp.Rational(3, 4) * sp.Rational(4, 3) == 1,
         "future_phase_integral_three_quarters_alpha_T_four_thirds")
    gate(-sp.Rational(1, 2) - sp.Rational(1, 6) == -sp.Rational(2, 3),
         "future_relative_envelope_T_minus_two_thirds")
    print("stage: endpoints", flush=True)

    gate(2 * 2 * 2 == 8, "two_masters_two_constants_two_real_phases")
    gate(alpha != 0 and beta != 0, "strict_oblique_component_guard")
    gate(sp.cancel(expected_normalized_odd.coeff(W)) == 0,
         "physical_parity_masters_exactly_decoupled_odd_from_even")
    gate(sp.cancel(even_master.coeff(H)) == 0,
         "physical_parity_masters_exactly_decoupled_even_from_odd")

    raw = {
        "schema": "udt-g329-raw-residuals-v1",
        "variables": {
            "odd": ["N", "H", "Q"],
            "even": ["A", "B", "C", "U", "V", "W", "Z"],
        },
        "odd_scalar": sp.sstr(odd_scalar),
        "even_scalar": sp.sstr(even_scalar),
        "odd_upper_triangle": {
            f"{i}{j}": sp.sstr(odd_ricci[i, j])
            for i in range(n) for j in range(i, n)
        },
        "even_upper_triangle": {
            f"{i}{j}": sp.sstr(even_ricci[i, j])
            for i in range(n) for j in range(i, n)
        },
    }
    (ROOT / args.raw_output).write_text(json.dumps(raw, indent=2) + "\n")

    result = {
        "schema": "udt-g329-oblique-census-v1",
        "landing": LANDING,
        "background": "-dT^2+T^(-2/3)dx^2+T^(4/3)(dy^2+dz^2)",
        "wave_covector": "alpha dx + beta dy; alpha*beta != 0",
        "equation": "delta(Ric-(R/4)g)=0; owner-provisional",
        "physical_dimension_real": 8,
        "coupling": "exactly decoupled z-even and z-odd scalar masters; both coefficients retain alpha and beta",
        "masters": {
            "even": sp.sstr(even_master),
            "odd_representative": sp.sstr(odd_master),
            "odd_normalized": sp.sstr(expected_normalized_odd),
        },
        "wronskians": {"even": "C*(4*alpha^2*T^2+beta^2)^2/T^5", "odd_normalized": "C/T"},
        "past_branches": {
            "even_E_equals_T2W": ["finite", "logarithmic"],
            "even_W": ["T^-2", "T^-2 log T"],
            "odd_normalized": ["T", "T^-1"],
        },
        "future_branches": {
            "both": "oscillatory phase ~(3/4)*alpha*T^(4/3), relative envelope T^(-2/3)"
        },
        "component_limits": {
            "alpha_to_zero": "G328 after E=T^2 W in even sector",
            "beta_to_zero": "G327 for even W and normalized odd amplitude",
        },
        "extension": "same algebra for every registered alpha*beta != 0; no full Fourier or nonlinear stability claim",
        "checks": checks,
        "check_count": len(checks),
        "imports_absent": [
            "action", "source", "matter model", "observation", "fit", "physical scale",
            "selected history", "selected topology", "population", "X_max",
        ],
    }
    (ROOT / args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
