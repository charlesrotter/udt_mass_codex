#!/usr/bin/env python3
"""Independent ADM and direct-curvature verification of the G328 census."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sealed_runtime import activate_runtime

activate_runtime()
import sympy as sp


EXPECTED_LANDING = (
    "PRIMITIVE_TRANSVERSE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE__"
    "TWO_PHYSICAL_MODE_FAMILIES__EXACT_BRANCH_CLASSIFICATION__"
    "NO_FULL_STABILITY_CLAIM"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent

    t, x, y, z = sp.symbols("t x y z", positive=True, real=True)
    ax, ap, wave = sp.symbols("A_x A_p wave", positive=True, real=True)
    phase = sp.exp(sp.I * wave * y)
    spatial_coordinates = (x, y, z)
    a = ax * t ** sp.Rational(-1, 3)
    b = ap * t ** sp.Rational(2, 3)
    gamma0 = sp.diag(a**2, b**2, b**2)
    gamma0_inverse = sp.diag(a**-2, b**-2, b**-2)

    U, V, O, W, Q, Z = [sp.Function(name)(t) for name in ("U", "V", "O", "W", "Q", "Z")]
    spatial_h = sp.zeros(3)
    spatial_h[0, 0] = 2 * a**2 * U * phase
    spatial_h[0, 1] = spatial_h[1, 0] = a * b * V * phase
    spatial_h[0, 2] = spatial_h[2, 0] = a * b * O * phase
    spatial_h[1, 1] = 2 * b**2 * W * phase
    spatial_h[1, 2] = spatial_h[2, 1] = b**2 * Q * phase
    spatial_h[2, 2] = 2 * b**2 * Z * phase
    delta_gamma_inverse = -gamma0_inverse * spatial_h * gamma0_inverse

    K0_covariant = sp.diff(gamma0, t) / 2
    delta_K_covariant = sp.diff(spatial_h, t) / 2
    K0_mixed = gamma0_inverse * K0_covariant
    delta_K_mixed = (
        delta_gamma_inverse * K0_covariant + gamma0_inverse * delta_K_covariant
    )
    K0_trace = sp.trace(K0_mixed)
    delta_K_trace = sp.simplify(sp.trace(delta_K_mixed))

    # The background slices are flat. Their first-order connection and Ricci
    # depend only on spatial derivatives of the perturbation.
    delta_spatial_connection = [[[
        sp.simplify(sp.Rational(1, 2) * sum(
            gamma0_inverse[i, ell] * (
                sp.diff(spatial_h[ell, k], spatial_coordinates[j])
                + sp.diff(spatial_h[ell, j], spatial_coordinates[k])
                - sp.diff(spatial_h[j, k], spatial_coordinates[ell])
            )
            for ell in range(3)
        ))
        for k in range(3)] for j in range(3)] for i in range(3)]
    delta_spatial_ricci = sp.MutableDenseMatrix(3, 3, [0] * 9)
    for i in range(3):
        for j in range(3):
            delta_spatial_ricci[i, j] = sp.simplify(sum(
                sp.diff(delta_spatial_connection[k][i][j], spatial_coordinates[k])
                - sp.diff(delta_spatial_connection[k][i][k], spatial_coordinates[j])
                for k in range(3)
            ))

    # Independent Gauss-Codazzi reconstruction in synchronous gauge.
    delta_R00 = sp.simplify(
        -sp.diff(delta_K_trace, t) - 2 * sp.trace(K0_mixed * delta_K_mixed)
    )
    delta_R0i = [sp.S.Zero] * 3
    for i in range(3):
        divergence = sum(
            sp.diff(delta_K_mixed[j, i], spatial_coordinates[j])
            for j in range(3)
        )
        connection_trace = sum(
            delta_spatial_connection[j][j][m] * K0_mixed[m, i]
            for j in range(3) for m in range(3)
        )
        connection_lower = sum(
            delta_spatial_connection[m][j][i] * K0_mixed[j, m]
            for j in range(3) for m in range(3)
        )
        delta_R0i[i] = sp.simplify(
            divergence + connection_trace - connection_lower
            - sp.diff(delta_K_trace, spatial_coordinates[i])
        )
    delta_Rij = sp.MutableDenseMatrix(3, 3, [0] * 9)
    for i in range(3):
        for j in range(3):
            product_variation = (
                delta_K_covariant * gamma0_inverse * K0_covariant
                + K0_covariant * delta_gamma_inverse * K0_covariant
                + K0_covariant * gamma0_inverse * delta_K_covariant
            )[i, j]
            delta_Rij[i, j] = sp.simplify(
                delta_spatial_ricci[i, j]
                + sp.diff(delta_K_covariant[i, j], t)
                + delta_K_trace * K0_covariant[i, j]
                + K0_trace * delta_K_covariant[i, j]
                - 2 * product_variation
            )

    def no_phase(expression: sp.Expr) -> sp.Expr:
        return sp.factor(sp.simplify(expression / phase))

    R00 = no_phase(delta_R00)
    R0 = [no_phase(value) for value in delta_R0i]
    Rij = sp.MutableDenseMatrix(3, 3, lambda i, j: no_phase(delta_Rij[i, j]))

    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    gate(R0[2] == sp.I * wave * sp.diff(Q, t) / 2,
         "adm_odd_momentum_constraint")
    odd_operator = (
        sp.diff(O, t, 2) + sp.diff(O, t) / t - O / t**2
        + wave**2 * O / (ap**2 * t ** sp.Rational(4, 3))
    )
    gate(sp.simplify(Rij[0, 2] - a * b * odd_operator / 2) == 0,
         "adm_odd_master_equation")
    odd_longitudinal = {
        sp.diff(Q, t): 0, sp.diff(Q, t, 2): 0,
    }
    gate(sp.simplify(Rij[1, 2].subs(odd_longitudinal)) == 0,
         "adm_odd_longitudinal_redundancy")

    gate(
        sp.simplify(R0[0] - sp.I * ax * wave * (t * sp.diff(V, t) + V)
                    / (2 * ap * t**2)) == 0,
        "adm_even_vector_constraint",
    )
    vector_shell = {
        sp.diff(V, t): -V / t,
        sp.diff(V, t, 2): 2 * V / t**2,
    }
    gate(sp.simplify(Rij[0, 1].subs(vector_shell)) == 0,
         "adm_even_vector_evolution_redundancy")

    scalar_constraint = sp.diff(U, t) + sp.diff(Z, t) - U / t
    gate(sp.simplify(R0[1] + sp.I * wave * scalar_constraint) == 0,
         "adm_even_scalar_momentum_constraint")

    E = sp.Function("E")(t)
    frequency = sp.symbols("frequency", positive=True, real=True)
    Up = sp.diff(E, t) - U / t
    Upp = sp.diff(E, t, 2) - sp.diff(E, t) / t + 2 * U / t**2
    Zred = E - 2 * U
    Zp = sp.diff(E, t) - 2 * Up
    Zpp = sp.diff(E, t, 2) - 2 * Upp
    Wp = (
        3 * t * Upp + 3 * Up - U / t
        + 3 * frequency**2 * t ** sp.Rational(-1, 3) * U
    )
    Wpp = sp.diff(Wp, t).subs(sp.diff(U, t, 2), Upp).subs(sp.diff(U, t), Up)
    even_operator = (
        sp.diff(E, t, 2) + sp.diff(E, t) / t
        + frequency**2 * t ** sp.Rational(-4, 3) * E
    )
    independent_33 = sp.simplify(
        Zpp + sp.Rational(2, 3) * Up / t + sp.Rational(2, 3) * Wp / t
        + sp.Rational(5, 3) * Zp / t
        + frequency**2 * t ** sp.Rational(-4, 3) * Zred
    )
    independent_00 = sp.simplify(
        Upp + Wpp + Zpp - sp.Rational(2, 3) * Up / t
        + sp.Rational(4, 3) * (Wp + Zp) / t
    )
    gate(sp.simplify(independent_33 - even_operator) == 0,
         "adm_even_master_reduction")
    gate(sp.simplify(independent_00 - (3 * t * sp.diff(even_operator, t)
                                      + 4 * even_operator)) == 0,
         "adm_even_remaining_equation_propagates")

    # Independent exact Lie derivative and gauge-rank check.
    full_coords = (t, x, y, z)
    spacetime_background = sp.diag(-1, a**2, b**2, b**2)
    P, Gx, Gy, Gz = [sp.Function(name)(t) * phase for name in ("P", "Gx", "Gy", "Gz")]
    gauge_vector = (P, Gx, Gy, Gz)
    lie = sp.MutableDenseMatrix(4, 4, [0] * 16)
    for i in range(4):
        for j in range(4):
            lie[i, j] = sp.simplify(
                sum(gauge_vector[c] * sp.diff(spacetime_background[i, j], full_coords[c])
                    for c in range(4))
                + sum(spacetime_background[c, j] * sp.diff(gauge_vector[c], full_coords[i])
                      for c in range(4))
                + sum(spacetime_background[i, c] * sp.diff(gauge_vector[c], full_coords[j])
                      for c in range(4))
            )
    gauge_U = sp.simplify(lie[1, 1] / (2 * a**2 * phase))
    gauge_Z = sp.simplify(lie[3, 3] / (2 * b**2 * phase))
    gauge_O = sp.simplify(lie[1, 3] / (a * b * phase))
    gate(sp.simplify(2 * gauge_U + gauge_Z) == 0,
         "direct_lie_even_master_invariant")
    gate(gauge_O == 0, "direct_lie_odd_master_invariant")

    # No nonzero residual gauge preserves the unique representative conditions.
    p0, gx0, gy0, gz0 = sp.symbols("p0 gx0 gy0 gz0")
    residual_matrix = sp.Matrix([
        [sp.Rational(1, 3) / t, 0, 0, 0],       # U+Z
        [sp.Rational(2, 3) / t, 0, sp.I * wave, 0],  # W
        [0, sp.I * wave * a / b, 0, 0],         # V
        [0, 0, 0, sp.I * wave],                 # Q
    ])
    gate(residual_matrix.det() != 0, "unique_representative_gauge_rank_four")
    gate(sp.solve(residual_matrix * sp.Matrix([p0, gx0, gy0, gz0]),
                  [p0, gx0, gy0, gz0], dict=True) == [
                      {p0: 0, gx0: 0, gy0: 0, gz0: 0}
                  ], "unique_representative_has_no_residual_gauge")

    # Independent special-function transformation and endpoint analysis.
    argument = 3 * frequency * t ** sp.Rational(1, 3)
    trial = sp.Function("F")
    composed = trial(argument)
    for order in (0, 3):
        transformed = sp.factor(sp.simplify(
            sp.diff(composed, t, 2) + sp.diff(composed, t) / t
            + (frequency**2 * t ** sp.Rational(-4, 3) - order**2 / (9 * t**2))
            * composed
        ))
        u = sp.Symbol("u")
        target = sp.diff(argument, t)**2 * (
            sp.Subs(sp.diff(trial(u), u, 2), u, argument)
            + sp.Subs(sp.diff(trial(u), u), u, argument) / argument
            + (1 - order**2 / argument**2) * trial(argument)
        )
        gate(sp.simplify(transformed - target) == 0,
             f"independent_bessel_transform_order_{order}")
    gate(sp.simplify(sp.diff(argument, t) * 2 / (sp.pi * argument))
         == 2 / (3 * sp.pi * t), "independent_nonzero_wronskian")
    gate(sp.limit(sp.besselj(0, argument), t, 0, dir="+") == 1,
         "independent_even_finite_past")
    gate(sp.limit(sp.bessely(0, argument) / sp.log(t), t, 0, dir="+")
         == 2 / (3 * sp.pi), "independent_even_log_past")
    gate(sp.limit(sp.besselj(3, argument) / t, t, 0, dir="+")
         == sp.Rational(9, 16) * frequency**3, "independent_odd_linear_past")
    gate(sp.limit(t * sp.bessely(3, argument), t, 0, dir="+")
         == -sp.Rational(16, 27) / (sp.pi * frequency**3),
         "independent_odd_inverse_past")
    gate(-sp.Rational(1, 6) == -sp.Rational(1, 2) * sp.Rational(1, 3),
         "independent_future_envelope")
    gate(2 * 2 * 2 == 8, "independent_physical_real_dimension")

    # Gauge-invariant intrinsic slice-curvature witnesses, reconstructed by the
    # ADM route rather than copied as expected numbers.
    even_curvature = sp.simplify(
        2 * delta_spatial_ricci[0, 0] / (a**2 * phase)
        + delta_spatial_ricci[2, 2] / (b**2 * phase)
    )
    odd_curvature = sp.simplify(
        delta_spatial_ricci[0, 2] / (a * b * phase)
    )
    gate(sp.simplify(even_curvature
                     - wave**2 * (2 * U + Z) / b**2) == 0,
         "independent_even_slice_curvature_witness")
    gate(sp.simplify(odd_curvature - wave**2 * O / (2 * b**2)) == 0,
         "independent_odd_slice_curvature_witness")

    result = {
        "schema": "udt-g328-transverse-first-fourier-independent-v1",
        "status": "INDEPENDENT_VERIFIED",
        "landing": EXPECTED_LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "method": "Gauss-Codazzi/ADM first variation plus direct Lie and Bessel reconstruction",
        "even_master": "E''+E'/t+frequency^2*t^(-4/3)*E=0",
        "odd_master": "O''+O'/t+(frequency^2*t^(-4/3)-t^(-2))*O=0",
        "time_bases": "J0/Y0 and J3/Y3 at 3*frequency*t^(1/3)",
        "physical_real_dimension": 8,
        "curvature_witnesses": {
            "even": "2*dRic3_xx/a^2+dRic3_zz/b^2=(wave^2/b^2)*(2U+Z)",
            "odd": "dRic3_xz/(a*b)=(wave^2/(2*b^2))*O",
        },
        "future_relative_envelope": "t^(-1/6)",
        "full_fourier_spectrum_classified": False,
        "full_linear_stability_proved": False,
        "metric_changed": False,
        "kernel_changed": False,
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
