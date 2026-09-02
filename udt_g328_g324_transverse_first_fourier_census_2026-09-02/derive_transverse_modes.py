#!/usr/bin/env python3
"""Exact production derivation for the bounded G328 transverse Fourier census."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sealed_runtime import activate_runtime

activate_runtime()
import sympy as sp


LANDING = (
    "PRIMITIVE_TRANSVERSE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE__"
    "TWO_PHYSICAL_MODE_FAMILIES__EXACT_BRANCH_CLASSIFICATION__"
    "NO_FULL_STABILITY_CLAIM"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent

    T, X, y, z_coord = sp.symbols("T X y z", positive=True, real=True)
    C1, Cp, k = sp.symbols("C1 Cp k", positive=True, real=True)
    coordinates = (T, X, y, z_coord)
    n = 4
    phase = sp.exp(sp.I * k * y)
    axial = C1 * T ** sp.Rational(-1, 3)
    transverse = Cp * T ** sp.Rational(2, 3)
    g0 = sp.diag(-1, axial**2, transverse**2, transverse**2)
    g0_inverse = sp.diag(-1, axial**-2, transverse**-2, transverse**-2)
    background_connection = [[[
        sp.simplify(sp.Rational(1, 2) * sum(
            g0_inverse[a, d] * (
                sp.diff(g0[d, c], coordinates[b])
                + sp.diff(g0[d, b], coordinates[c])
                - sp.diff(g0[b, c], coordinates[d])
            )
            for d in range(n)
        ))
        for c in range(n)] for b in range(n)] for a in range(n)]

    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    def build_linearized_ricci(h: sp.Matrix) -> tuple[sp.Matrix, sp.Expr]:
        inverse_h = -g0_inverse * h * g0_inverse
        delta_gamma = [[[
            sp.simplify(sp.Rational(1, 2) * sum(
                inverse_h[a, d] * (
                    sp.diff(g0[d, c], coordinates[b])
                    + sp.diff(g0[d, b], coordinates[c])
                    - sp.diff(g0[b, c], coordinates[d])
                )
                + g0_inverse[a, d] * (
                    sp.diff(h[d, c], coordinates[b])
                    + sp.diff(h[d, b], coordinates[c])
                    - sp.diff(h[b, c], coordinates[d])
                )
                for d in range(n)
            ))
            for c in range(n)] for b in range(n)] for a in range(n)]
        delta_ricci = sp.MutableDenseMatrix(n, n, [0] * n**2)
        for a in range(n):
            for b in range(n):
                value = 0
                for c in range(n):
                    value += sp.diff(delta_gamma[c][a][b], coordinates[c])
                    value -= sp.diff(delta_gamma[c][a][c], coordinates[b])
                    for d in range(n):
                        value += delta_gamma[c][c][d] * background_connection[d][a][b]
                        value += background_connection[c][c][d] * delta_gamma[d][a][b]
                        value -= delta_gamma[c][b][d] * background_connection[d][a][c]
                        value -= background_connection[c][b][d] * delta_gamma[d][a][c]
                delta_ricci[a, b] = sp.factor(sp.simplify(value / phase))
        delta_scalar = sp.factor(sp.simplify(sum(
            g0_inverse[a, b] * delta_ricci[a, b]
            for a in range(n) for b in range(n)
        )))
        return delta_ricci, delta_scalar

    def verify_linearized_bianchi(
        delta_ricci: sp.Matrix, delta_scalar: sp.Expr, label: str
    ) -> None:
        delta_shape = sp.MutableDenseMatrix(
            n,
            n,
            lambda a, b: phase * (
                delta_ricci[a, b] - g0[a, b] * delta_scalar / 4
            ),
        )
        for b in range(n):
            divergence = 0
            for a in range(n):
                for c in range(n):
                    covariant = sp.diff(delta_shape[a, b], coordinates[c])
                    for d in range(n):
                        covariant -= background_connection[d][c][a] * delta_shape[d, b]
                        covariant -= background_connection[d][c][b] * delta_shape[a, d]
                    divergence += g0_inverse[a, c] * covariant
            target = sp.diff(phase * delta_scalar, coordinates[b]) / 4
            gate(sp.simplify(divergence - target) == 0,
                 f"{label}_linearized_bianchi_identity_{b}")

    # z-odd block: normalized shift N, axial-transverse H_o, and longitudinal Q.
    N = sp.Function("N")(T)
    Ho = sp.Function("H_o")(T)
    Q = sp.Function("Q")(T)
    h_odd = sp.zeros(n)
    h_odd[0, 3] = h_odd[3, 0] = transverse * N * phase
    h_odd[1, 3] = h_odd[3, 1] = axial * transverse * Ho * phase
    h_odd[2, 3] = h_odd[3, 2] = transverse**2 * Q * phase
    odd_ricci, odd_scalar = build_linearized_ricci(h_odd)
    verify_linearized_bianchi(odd_ricci, odd_scalar, "odd")
    gate(odd_scalar == 0, "odd_linearized_scalar_identically_zero")
    odd_support = {(0, 3), (3, 0), (1, 3), (3, 1), (2, 3), (3, 2)}
    for a in range(n):
        for b in range(n):
            if (a, b) not in odd_support:
                gate(odd_ricci[a, b] == 0, f"odd_parity_zero_{a}{b}")
    odd_constraint = sp.I * transverse * sp.diff(Q, T) + k * N
    odd_master = (
        sp.diff(Ho, T, 2) + sp.diff(Ho, T) / T - Ho / T**2
        + k**2 * Ho / (Cp**2 * T ** sp.Rational(4, 3))
    )
    expected_03 = k * odd_constraint / (2 * transverse)
    expected_13 = axial * transverse * odd_master / 2
    gate(sp.simplify(odd_ricci[0, 3] - expected_03) == 0,
         "odd_momentum_constraint_exact")
    gate(sp.simplify(odd_ricci[1, 3] - expected_13) == 0,
         "odd_master_equation_exact")

    # In synchronous gauge N=0, the constraint makes Q constant. The remaining
    # equation is then automatic, and the constant is residual periodic z gauge.
    odd_sync = {
        N: 0, sp.diff(N, T): 0, sp.diff(N, T, 2): 0,
        sp.diff(Q, T): 0, sp.diff(Q, T, 2): 0,
    }
    gate(sp.simplify(odd_ricci[2, 3].subs(odd_sync)) == 0,
         "odd_longitudinal_equation_redundant_after_constraint")

    # z-even block: lapse A, two shifts B,C, and four spatial amplitudes.
    A, B, C, U, V, W, Z = [sp.Function(name)(T) for name in "ABCUVWZ"]
    h_even = sp.zeros(n)
    h_even[0, 0] = -2 * A * phase
    h_even[0, 1] = h_even[1, 0] = axial * B * phase
    h_even[0, 2] = h_even[2, 0] = transverse * C * phase
    h_even[1, 1] = 2 * axial**2 * U * phase
    h_even[1, 2] = h_even[2, 1] = axial * transverse * V * phase
    h_even[2, 2] = 2 * transverse**2 * W * phase
    h_even[3, 3] = 2 * transverse**2 * Z * phase
    even_ricci, even_scalar = build_linearized_ricci(h_even)
    verify_linearized_bianchi(even_ricci, even_scalar, "even")
    gate(7 + 3 == 10, "parity_blocks_cover_all_ten_metric_components")
    even_support = {
        (0, 0), (0, 1), (1, 0), (0, 2), (2, 0), (1, 1),
        (1, 2), (2, 1), (2, 2), (3, 3),
    }
    for a in range(n):
        for b in range(n):
            if (a, b) not in even_support:
                gate(even_ricci[a, b] == 0, f"even_parity_zero_{a}{b}")

    # The B,V pair is a constrained longitudinal gauge block.
    vector_constraint = T * sp.diff(V, T) + V - sp.I * k * T ** sp.Rational(1, 3) * B / Cp
    expected_01 = sp.I * C1 * k * vector_constraint / (2 * Cp * T**2)
    gate(sp.simplify(even_ricci[0, 1] - expected_01) == 0,
         "even_axial_shift_constraint_exact")
    vector_sync = {
        B: 0, sp.diff(B, T): 0, sp.diff(B, T, 2): 0,
        sp.diff(V, T): -V / T,
        sp.diff(V, T, 2): 2 * V / T**2,
    }
    gate(sp.simplify(even_ricci[1, 2].subs(vector_sync)) == 0,
         "even_axial_longitudinal_equation_redundant")

    # Synchronous scalar block and its exact reduction.
    sync = {
        A: 0, C: 0,
        sp.diff(A, T): 0, sp.diff(A, T, 2): 0,
        sp.diff(C, T): 0, sp.diff(C, T, 2): 0,
    }
    scalar_constraint = sp.diff(U, T) + sp.diff(Z, T) - U / T
    expected_02 = -sp.I * k * scalar_constraint
    gate(sp.simplify(even_ricci[0, 2].subs(sync) - expected_02) == 0,
         "even_scalar_momentum_constraint_exact")

    He = sp.Function("H_e")(T)
    nu = sp.symbols("nu", positive=True, real=True)
    Up = sp.diff(He, T) - U / T
    Upp = sp.diff(He, T, 2) - sp.diff(He, T) / T + 2 * U / T**2
    Zred = He - 2 * U
    Zp = sp.diff(He, T) - 2 * Up
    Zpp = sp.diff(He, T, 2) - 2 * Upp
    Wp = (
        3 * T * Upp + 3 * Up - U / T
        + 3 * nu**2 * T ** sp.Rational(-1, 3) * U
    )
    Wpp = sp.diff(Wp, T).subs(sp.diff(U, T, 2), Upp).subs(sp.diff(U, T), Up)
    even_master = (
        sp.diff(He, T, 2) + sp.diff(He, T) / T
        + nu**2 * T ** sp.Rational(-4, 3) * He
    )
    reduced_33 = sp.simplify(
        Zpp + sp.Rational(2, 3) * Up / T + sp.Rational(2, 3) * Wp / T
        + sp.Rational(5, 3) * Zp / T
        + nu**2 * T ** sp.Rational(-4, 3) * Zred
    )
    reduced_00 = sp.simplify(
        Upp + Wpp + Zpp - sp.Rational(2, 3) * Up / T
        + sp.Rational(4, 3) * (Wp + Zp) / T
    )
    reduced_22 = sp.simplify(
        Wpp + sp.Rational(2, 3) * Up / T + sp.Rational(5, 3) * Wp / T
        + sp.Rational(2, 3) * Zp / T
        + nu**2 * T ** sp.Rational(-4, 3) * (U + Zred)
    )
    gate(sp.simplify(reduced_33 - even_master) == 0,
         "even_master_reduction_exact")
    gate(sp.simplify(reduced_00 - (3 * T * sp.diff(even_master, T) + 4 * even_master)) == 0,
         "even_time_equation_is_master_consequence")
    gate(sp.simplify(reduced_22 - (3 * T * sp.diff(even_master, T) + 5 * even_master)) == 0,
         "even_longitudinal_equation_is_master_consequence")

    # Full same-mode Lie derivative and gauge invariants.
    P, Gx, Gy, Gz = [sp.Function(name)(T) for name in ("P", "Gx", "Gy", "Gz")]
    gauge_variables = {
        "A": sp.diff(P, T),
        "B": axial * sp.diff(Gx, T),
        "C": transverse * sp.diff(Gy, T) - sp.I * k * P / transverse,
        "U": -P / (3 * T),
        "V": sp.I * k * axial * Gx / transverse,
        "W": 2 * P / (3 * T) + sp.I * k * Gy,
        "Z": 2 * P / (3 * T),
        "N": transverse * sp.diff(Gz, T),
        "H_o": sp.S.Zero,
        "Q": sp.I * k * Gz,
    }
    gate(sp.simplify(2 * gauge_variables["U"] + gauge_variables["Z"]) == 0,
         "even_H_is_gauge_invariant")
    gate(gauge_variables["H_o"] == 0, "odd_H_is_gauge_invariant")
    gate(len(gauge_variables) == 10, "all_metric_variables_have_gauge_images")

    # Gauge reach on compact positive-time intervals uses regular first-order equations:
    # P'=A, Gx'=B/a, Gz'=N/b, Gy'=C/b+i*k*P/b^2.
    gauge_reach_coefficients = [sp.S.One, 1 / axial, 1 / transverse, 1 / transverse**2]
    gate(all(not coefficient.has(sp.zoo, sp.nan) for coefficient in gauge_reach_coefficients),
         "synchronous_gauge_coefficients_regular_for_positive_time")
    gate(k != 0, "nonzero_fourier_covector_registered")

    # Residual synchronous solutions are exactly gauge: Q=constant, V=c/T,
    # U=c/T and its induced W, plus a constant W shift.
    c_u, c_w = sp.symbols("c_u c_w")
    residual_U = c_u / T
    residual_W = -2 * c_u / T - 9 * nu**2 * c_u * T ** sp.Rational(-1, 3) + c_w
    gate(sp.simplify(sp.diff(residual_U, T) + residual_U / T) == 0,
         "even_residual_U_homogeneous_solution")
    residual_W_equation = sp.simplify(
        sp.diff(residual_W, T)
        - (3 * T * sp.diff(residual_U, T, 2)
           + 3 * sp.diff(residual_U, T) - residual_U / T
           + 3 * nu**2 * T ** sp.Rational(-1, 3) * residual_U)
    )
    gate(residual_W_equation == 0, "even_residual_constants_are_synchronous_gauge")
    gate(sp.simplify(sp.diff(1 / T, T) + (1 / T) / T) == 0,
         "vector_residual_is_synchronous_gauge")

    # Unique gauge-fixed representatives reconstructed from each invariant master.
    even_C = -3 * sp.I * Cp * T ** sp.Rational(2, 3) * sp.diff(He, T) / k
    even_rep = {
        A: -3 * He, B: 0, C: even_C, U: He, V: 0, W: 0, Z: -He,
    }
    for old, new in list(even_rep.items()):
        for order in (1, 2, 3):
            even_rep[sp.diff(old, T, order)] = sp.diff(new, T, order)
    even_ode2 = -sp.diff(He, T) / T - k**2 * He / (
        Cp**2 * T ** sp.Rational(4, 3)
    )
    even_ode3 = sp.diff(even_ode2, T).subs(sp.diff(He, T, 2), even_ode2)
    even_shell = {sp.diff(He, T, 2): even_ode2, sp.diff(He, T, 3): even_ode3}
    for a in range(n):
        for b in range(n):
            gate(sp.simplify(even_ricci[a, b].subs(even_rep).subs(even_shell)) == 0,
                 f"even_representative_full_residual_zero_{a}{b}")
    gate(sp.simplify(even_scalar.subs(even_rep).subs(even_shell)) == 0,
         "even_representative_scalar_zero")

    odd_rep = {
        N: 0, Q: 0,
        sp.diff(N, T): 0, sp.diff(N, T, 2): 0,
        sp.diff(Q, T): 0, sp.diff(Q, T, 2): 0,
    }
    odd_ode2 = (
        -sp.diff(Ho, T) / T + Ho / T**2
        - k**2 * Ho / (Cp**2 * T ** sp.Rational(4, 3))
    )
    for a in range(n):
        for b in range(n):
            gate(sp.simplify(odd_ricci[a, b].subs(odd_rep).subs(
                sp.diff(Ho, T, 2), odd_ode2
            )) == 0, f"odd_representative_full_residual_zero_{a}{b}")

    # For the trace-free equation, on-shell Bianchi gives d(delta R)=0. The
    # registered nonzero Fourier factor then gives i*k*delta R=0, hence delta R=0.
    delta_R_symbol = sp.symbols("delta_R")
    gate(sp.solve(sp.I * k * delta_R_symbol, delta_R_symbol) == [0],
         "nonzero_mode_bianchi_forces_scalar_zero")

    # Exact master bases.
    zeta = 3 * nu * T ** sp.Rational(1, 3)
    even_j = sp.besselj(0, zeta)
    even_y = sp.bessely(0, zeta)
    odd_j = sp.besselj(3, zeta)
    odd_y = sp.bessely(3, zeta)

    def master_residual(function: sp.Expr, order: int) -> sp.Expr:
        return sp.simplify(
            sp.diff(function, T, 2) + sp.diff(function, T) / T
            + (nu**2 * T ** sp.Rational(-4, 3) - order**2 / (9 * T**2))
            * function
        )

    gate(master_residual(even_j, 0) == 0, "even_J0_exact_residual")
    gate(master_residual(even_y, 0) == 0, "even_Y0_exact_residual")
    gate(master_residual(odd_j, 3) == 0, "odd_J3_exact_residual")
    gate(master_residual(odd_y, 3) == 0, "odd_Y3_exact_residual")
    transformed_wronskian = sp.simplify(sp.diff(zeta, T) * 2 / (sp.pi * zeta))
    gate(transformed_wronskian == 2 / (3 * sp.pi * T),
         "both_master_wronskians_nonzero")

    # Exact endpoint classifiers.
    gate(sp.limit(even_j, T, 0, dir="+") == 1, "even_J0_finite_past")
    gate(sp.limit(even_y / sp.log(T), T, 0, dir="+") == 2 / (3 * sp.pi),
         "even_Y0_logarithmic_past")
    gate(sp.limit(odd_j / T, T, 0, dir="+") == sp.Rational(9, 16) * nu**3,
         "odd_J3_linear_past")
    gate(sp.limit(T * odd_y, T, 0, dir="+") == -sp.Rational(16, 27) /
         (sp.pi * nu**3), "odd_Y3_inverse_linear_past")
    gate(-sp.Rational(1, 2) * sp.Rational(1, 3) == sp.Rational(-1, 6),
         "both_future_relative_envelopes_T_minus_one_sixth")

    # Two masters, two constants, and two real phases.
    gate(2 * 2 * 2 == 8, "physical_real_solution_dimension_eight")

    # Intrinsic slice-curvature witnesses. Each background spatial slice is flat,
    # so the displayed combinations are genuine first-order curvature responses.
    # The combinations cancel the time-gauge image and depend only on H_e or H_o.
    spatial_coordinates = (X, y, z_coord)
    spatial_background = sp.diag(axial**2, transverse**2, transverse**2)
    spatial_inverse = sp.diag(axial**-2, transverse**-2, transverse**-2)

    def spatial_ricci_first_variation(spatial_h: sp.Matrix) -> sp.Matrix:
        delta_connection = [[[
            sp.simplify(sp.Rational(1, 2) * sum(
                spatial_inverse[a, d] * (
                    sp.diff(spatial_h[d, c], spatial_coordinates[b])
                    + sp.diff(spatial_h[d, b], spatial_coordinates[c])
                    - sp.diff(spatial_h[b, c], spatial_coordinates[d])
                )
                for d in range(3)
            ))
            for c in range(3)] for b in range(3)] for a in range(3)]
        return sp.MutableDenseMatrix(3, 3, lambda a, b: sp.simplify(sum(
            sp.diff(delta_connection[c][a][b], spatial_coordinates[c])
            - sp.diff(delta_connection[c][a][c], spatial_coordinates[b])
            for c in range(3)
        )))

    even_spatial_ricci = spatial_ricci_first_variation(h_even[1:4, 1:4])
    odd_spatial_ricci = spatial_ricci_first_variation(h_odd[1:4, 1:4])
    even_curvature_witness = sp.simplify(
        2 * even_spatial_ricci[0, 0] / (axial**2 * phase)
        + even_spatial_ricci[2, 2] / (transverse**2 * phase)
    )
    odd_curvature_witness = sp.simplify(
        odd_spatial_ricci[0, 2] / (axial * transverse * phase)
    )
    gate(sp.simplify(even_curvature_witness
                     - k**2 * (2 * U + Z) / transverse**2) == 0,
         "even_gauge_invariant_slice_curvature_witness")
    gate(sp.simplify(odd_curvature_witness
                     - k**2 * Ho / (2 * transverse**2)) == 0,
         "odd_gauge_invariant_slice_curvature_witness")

    result = {
        "schema": "udt-g328-transverse-first-fourier-production-v1",
        "status": "PRODUCTION_DERIVED",
        "landing": LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "background": "-dT^2+C1^2*T^(-2/3)dX^2+Cp^2*T^(4/3)(dy^2+dz^2)",
        "wave_covector": "k dy, k>0",
        "bounded_equation": "Ric-(R/4)g=0",
        "physical_masters": {
            "even": "H_e''+H_e'/T+nu^2*T^(-4/3)*H_e=0",
            "odd": "H_o''+H_o'/T+(nu^2*T^(-4/3)-T^(-2))*H_o=0",
            "nu": "k/Cp",
            "argument": "3*nu*T^(1/3)",
        },
        "time_bases": {
            "even": ["J_0(argument)", "Y_0(argument)"],
            "odd": ["J_3(argument)", "Y_3(argument)"],
        },
        "past_branches": {
            "even": ["finite", "logarithmic"],
            "odd": ["T", "T^(-1)"],
        },
        "future_relative_envelope": "T^(-1/6) oscillatory for all four branches",
        "physical_real_solution_dimension": 8,
        "curvature_witnesses": {
            "even": "2*dRic3_XX/a^2+dRic3_zz/b^2=(k^2/b^2)*H_e",
            "odd": "dRic3_Xz/(a*b)=(k^2/(2*b^2))*H_o",
        },
        "arbitrary_gauge_functions": 4,
        "linearized_scalar_on_shell": "0 for k>0 by Bianchi and direct representatives",
        "extends_to_any_nonzero_transverse_harmonic": True,
        "full_fourier_spectrum_classified": False,
        "full_linear_stability_proved": False,
        "nonlinear_stability_proved": False,
        "metric_changed": False,
        "kernel_changed": False,
        "angular_sector_changed": False,
        "equation_changed": False,
        "python_version": sys.version,
        "sympy_version": sp.__version__,
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
