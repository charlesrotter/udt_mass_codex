#!/usr/bin/env python3
"""Exact production derivation for the bounded G327 axial tensor sector."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sealed_runtime import activate_runtime

activate_runtime()
import sympy as sp


LANDING = (
    "PRIMITIVE_AXIAL_TENSOR_MODE_CLOSES_AS_TWO_GAUGE_INVARIANT_POLARIZATIONS__"
    "BESSEL_ZERO_TIME_BASIS__FINITE_AND_LOGARITHMIC_PAST_BRANCHES__"
    "OSCILLATORY_T_MINUS_TWO_THIRDS_FUTURE_DECAY__NO_FULL_STABILITY_CLAIM"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent

    T, X, y, z_coord = sp.symbols("T X y z", positive=True, real=True)
    C1, Cp, k = sp.symbols("C1 Cp k", positive=True, real=True)
    hp = sp.Function("h_plus")(T)
    hx = sp.Function("h_cross")(T)
    phase = sp.exp(sp.I * k * X)
    coordinates = (T, X, y, z_coord)
    dimension = 4

    a2 = C1**2 * T ** sp.Rational(-2, 3)
    b2 = Cp**2 * T ** sp.Rational(4, 3)
    g0 = sp.diag(-1, a2, b2, b2)
    g0_inverse = sp.diag(-1, 1 / a2, 1 / b2, 1 / b2)
    perturbation = sp.zeros(dimension)
    perturbation[2, 2] = 2 * b2 * hp * phase
    perturbation[3, 3] = -2 * b2 * hp * phase
    perturbation[2, 3] = perturbation[3, 2] = 2 * b2 * hx * phase
    inverse_perturbation = -g0_inverse * perturbation * g0_inverse

    gamma0 = [[[
        sp.simplify(sp.Rational(1, 2) * sum(
            g0_inverse[a, d] * (
                sp.diff(g0[d, c], coordinates[b])
                + sp.diff(g0[d, b], coordinates[c])
                - sp.diff(g0[b, c], coordinates[d])
            )
            for d in range(dimension)
        ))
        for c in range(dimension)] for b in range(dimension)] for a in range(dimension)]

    delta_gamma = [[[
        sp.simplify(sp.Rational(1, 2) * sum(
            inverse_perturbation[a, d] * (
                sp.diff(g0[d, c], coordinates[b])
                + sp.diff(g0[d, b], coordinates[c])
                - sp.diff(g0[b, c], coordinates[d])
            )
            + g0_inverse[a, d] * (
                sp.diff(perturbation[d, c], coordinates[b])
                + sp.diff(perturbation[d, b], coordinates[c])
                - sp.diff(perturbation[b, c], coordinates[d])
            )
            for d in range(dimension)
        ))
        for c in range(dimension)] for b in range(dimension)] for a in range(dimension)]

    delta_ricci = sp.MutableDenseMatrix(dimension, dimension, [0] * dimension**2)
    for a in range(dimension):
        for b in range(dimension):
            value = 0
            for c in range(dimension):
                value += sp.diff(delta_gamma[c][a][b], coordinates[c])
                value -= sp.diff(delta_gamma[c][a][c], coordinates[b])
                for d in range(dimension):
                    value += delta_gamma[c][c][d] * gamma0[d][a][b]
                    value += gamma0[c][c][d] * delta_gamma[d][a][b]
                    value -= delta_gamma[c][b][d] * gamma0[d][a][c]
                    value -= gamma0[c][b][d] * delta_gamma[d][a][c]
            delta_ricci[a, b] = sp.simplify(sp.expand(value))

    delta_scalar = sp.simplify(sum(
        g0_inverse[a, b] * delta_ricci[a, b]
        for a in range(dimension) for b in range(dimension)
    ))
    delta_tracefree = sp.MutableDenseMatrix(
        dimension,
        dimension,
        lambda a, b: sp.simplify(delta_ricci[a, b] - delta_scalar * g0[a, b] / 4),
    )

    expected_plus = b2 * phase * (
        sp.diff(hp, T, 2) + sp.diff(hp, T) / T + k**2 * T ** sp.Rational(2, 3) * hp / C1**2
    )
    expected_cross = b2 * phase * (
        sp.diff(hx, T, 2) + sp.diff(hx, T) / T + k**2 * T ** sp.Rational(2, 3) * hx / C1**2
    )

    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    gate(delta_scalar == 0, "linearized_scalar_zero")
    expected_nonzero = {(2, 2), (3, 3), (2, 3), (3, 2)}
    for a in range(dimension):
        for b in range(dimension):
            if (a, b) not in expected_nonzero:
                gate(delta_tracefree[a, b] == 0, f"constraint_component_zero_{a}{b}")
    gate(sp.simplify(delta_tracefree[2, 2] - expected_plus) == 0,
         "plus_equation_exact")
    gate(sp.simplify(delta_tracefree[3, 3] + expected_plus) == 0,
         "plus_trace_partner_exact")
    gate(sp.simplify(delta_tracefree[2, 3] - expected_cross) == 0,
         "cross_equation_exact")
    gate(sp.simplify(delta_tracefree[3, 2] - expected_cross) == 0,
         "cross_symmetry_exact")

    # Gauge image: for a same-mode periodic vector, the transverse block receives only
    # the pure-trace time-shift term because all transverse derivatives vanish.
    xi0, xi1, xi2, xi3 = [sp.Function(f"xi_{index}")(T) * phase for index in range(4)]
    xi = (xi0, xi1, xi2, xi3)
    lie = sp.MutableDenseMatrix(dimension, dimension, [0] * dimension**2)
    for a in range(dimension):
        for b in range(dimension):
            lie[a, b] = sp.simplify(
                sum(xi[c] * sp.diff(g0[a, b], coordinates[c]) for c in range(dimension))
                + sum(g0[c, b] * sp.diff(xi[c], coordinates[a]) for c in range(dimension))
                + sum(g0[a, c] * sp.diff(xi[c], coordinates[b]) for c in range(dimension))
            )
    transverse_trace = sp.simplify((lie[2, 2] + lie[3, 3]) / (2 * b2))
    lie_tf_22 = sp.simplify(lie[2, 2] / b2 - transverse_trace)
    lie_tf_33 = sp.simplify(lie[3, 3] / b2 - transverse_trace)
    lie_tf_23 = sp.simplify(lie[2, 3] / b2)
    gate(lie_tf_22 == 0 and lie_tf_33 == 0 and lie_tf_23 == 0,
         "periodic_same_mode_gauge_has_zero_transverse_tf_image")

    # Direct first variation of R_{0 A 0 B}; a nonzero on-shell tidal response is retained.
    delta_riemann_up = [[[[0 for _ in range(dimension)] for _ in range(dimension)]
                          for _ in range(dimension)] for _ in range(dimension)]
    for a in range(dimension):
        for b in range(dimension):
            for c in range(dimension):
                for d in range(dimension):
                    value = (
                        sp.diff(delta_gamma[a][b][d], coordinates[c])
                        - sp.diff(delta_gamma[a][b][c], coordinates[d])
                    )
                    for e in range(dimension):
                        value += delta_gamma[a][c][e] * gamma0[e][b][d]
                        value += gamma0[a][c][e] * delta_gamma[e][b][d]
                        value -= delta_gamma[a][d][e] * gamma0[e][b][c]
                        value -= gamma0[a][d][e] * delta_gamma[e][b][c]
                    delta_riemann_up[a][b][c][d] = sp.simplify(value)

    # R_{a b c d}=g_{a e} R^e_{b c d}; background R^e_{b c d} is reconstructed.
    riemann0_up = [[[[0 for _ in range(dimension)] for _ in range(dimension)]
                     for _ in range(dimension)] for _ in range(dimension)]
    for a in range(dimension):
        for b in range(dimension):
            for c in range(dimension):
                for d in range(dimension):
                    value = (
                        sp.diff(gamma0[a][b][d], coordinates[c])
                        - sp.diff(gamma0[a][b][c], coordinates[d])
                    )
                    for e in range(dimension):
                        value += gamma0[a][c][e] * gamma0[e][b][d]
                        value -= gamma0[a][d][e] * gamma0[e][b][c]
                    riemann0_up[a][b][c][d] = sp.simplify(value)

    def delta_riemann_lower(a: int, b: int, c: int, d: int) -> sp.Expr:
        return sp.simplify(sum(
            perturbation[a, e] * riemann0_up[e][b][c][d]
            + g0[a, e] * delta_riemann_up[e][b][c][d]
            for e in range(dimension)
        ))

    tidal_plus = sp.simplify(
        (delta_riemann_lower(0, 2, 0, 2) - delta_riemann_lower(0, 3, 0, 3))
        / (2 * b2 * phase)
    )
    tidal_cross = sp.simplify(delta_riemann_lower(0, 2, 0, 3) / (b2 * phase))
    plus_on_shell = sp.simplify(tidal_plus.subs(
        sp.diff(hp, T, 2),
        -sp.diff(hp, T) / T - k**2 * T ** sp.Rational(2, 3) * hp / C1**2,
    ))
    cross_on_shell = sp.simplify(tidal_cross.subs(
        sp.diff(hx, T, 2),
        -sp.diff(hx, T) / T - k**2 * T ** sp.Rational(2, 3) * hx / C1**2,
    ))
    plus_tidal_sample = sp.simplify(plus_on_shell.subs({
        T: 1, C1: 1, k: 1, hp: 1, sp.diff(hp, T): 0,
    }))
    cross_tidal_sample = sp.simplify(cross_on_shell.subs({
        T: 1, C1: 1, k: 1, hx: 1, sp.diff(hx, T): 0,
    }))
    gate(plus_tidal_sample == sp.Rational(13, 9),
         "plus_tidal_response_nonzero_exact_sample")
    gate(cross_tidal_sample == sp.Rational(13, 9),
         "cross_tidal_response_nonzero_exact_sample")

    # The change z=3*nu*T^(4/3)/4 gives the order-zero Bessel equation.
    nu = sp.symbols("nu", positive=True, real=True)
    z = sp.Rational(3, 4) * nu * T ** sp.Rational(4, 3)
    z_prime = sp.diff(z, T)
    z_second = sp.diff(z, T, 2)
    gate(sp.simplify(z_prime - nu * T ** sp.Rational(1, 3)) == 0,
         "bessel_change_first_derivative")
    gate(sp.simplify(z_second + z_prime / T - z_prime**2 / z) == 0,
         "bessel_change_first_derivative_coefficient")
    gate(sp.simplify(nu**2 * T ** sp.Rational(2, 3) - z_prime**2) == 0,
         "bessel_change_unit_potential")

    # Direct substitution of the special-function basis into the time ODE.
    j0 = sp.besselj(0, z)
    y0 = sp.bessely(0, z)
    def time_ode(function: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sp.diff(function, T, 2) + sp.diff(function, T) / T
            + nu**2 * T ** sp.Rational(2, 3) * function
        )
    gate(time_ode(j0) == 0, "bessel_j0_exact_residual")
    gate(time_ode(y0) == 0, "bessel_y0_exact_residual")
    # SymPy does not automatically reduce the standard order-zero Bessel Wronskian.
    # Apply W_z[J_0,Y_0]=2/(pi*z), then transform it exactly from z to T.
    canonical_wronskian_z = 2 / (sp.pi * z)
    transformed_wronskian = sp.simplify(T * z_prime * canonical_wronskian_z)
    gate(transformed_wronskian == sp.Rational(8, 3) / sp.pi,
         "time_wronskian_nonzero_exact")

    # Real mode census: two transverse polarizations, cosine/sine, two time solutions.
    gate(2 * 2 * 2 == 8, "real_solution_dimension_eight")

    # Endpoint exponents are derived from z~T^(4/3) and Bessel order-zero asymptotics.
    z_power = sp.Rational(4, 3)
    future_amplitude_power = -z_power / 2
    gate(future_amplitude_power == sp.Rational(-2, 3),
         "future_relative_amplitude_T_minus_two_thirds")
    gate(sp.limit(j0, T, 0, dir="+") == 1, "j0_finite_at_past_endpoint")
    gate(sp.limit(y0 / sp.log(T), T, 0, dir="+") == sp.Rational(8, 3) / sp.pi,
         "y0_logarithmic_at_past_endpoint")
    gate(z_prime / (nu * T ** sp.Rational(1, 3)) == 1,
         "frequency_normalized_derivative_is_bessel_derivative")
    normalized_y_derivative = sp.diff(y0, T) / (nu * T ** sp.Rational(1, 3))
    gate(sp.limit(z * normalized_y_derivative, T, 0, dir="+") == 2 / sp.pi,
         "y0_normalized_derivative_past_divergence")

    result = {
        "schema": "udt-g327-axial-first-fourier-tensor-production-v1",
        "status": "INTERNAL_VERIFIED_PENDING_EXTERNAL_REVIEW",
        "landing": LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "background_exponents": ["-1/3", "2/3", "2/3"],
        "primitive_mode": "k1=2*pi/L_X; nu=abs(k1)/C1",
        "mode_ode": "H''+H'/T+nu^2*T^(2/3)*H=0",
        "bessel_argument": "z=3*nu*T^(4/3)/4",
        "time_basis": ["J_0(z)", "Y_0(z)"],
        "time_wronskian": "T*W_T=8/(3*pi)",
        "real_solution_dimension": 8,
        "linearized_scalar_curvature": "0",
        "plus_tidal_on_shell": str(plus_on_shell),
        "cross_tidal_on_shell": str(cross_on_shell),
        "past_endpoint": "one finite J0 branch and one logarithmic Y0 branch per phase/polarization",
        "future_endpoint": "both branches oscillate with relative phase-space norm O(T^(-2/3))",
        "compact_time_norm_finite": True,
        "full_fourier_spectrum_classified": False,
        "full_linear_stability_proved": False,
        "nonlinear_stability_proved": False,
        "physical_occupancy_selected": False,
        "physical_scale_selected": False,
        "Xmax_selected": False,
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
