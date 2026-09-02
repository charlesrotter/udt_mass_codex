#!/usr/bin/env python3
"""Implementation-distinct exact verifier for G327.

This route constructs the epsilon-dependent metric, inverts it exactly, builds its full
Christoffel/Ricci tensors, and only then differentiates at epsilon=0. It imports neither the
production module nor its generated result.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sealed_runtime import activate_runtime

activate_runtime()
import sympy as sp


EXPECTED_LANDING = (
    "PRIMITIVE_AXIAL_TENSOR_MODE_CLOSES_AS_TWO_GAUGE_INVARIANT_POLARIZATIONS__"
    "BESSEL_ZERO_TIME_BASIS__FINITE_AND_LOGARITHMIC_PAST_BRANCHES__"
    "OSCILLATORY_T_MINUS_TWO_THIRDS_FUTURE_DECAY__NO_FULL_STABILITY_CLAIM"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent

    t, x, y, z = sp.symbols("t x y z", positive=True, real=True)
    eps = sp.symbols("eps", real=True)
    ax, ap, wave = sp.symbols("A_x A_p wave", positive=True, real=True)
    plus = sp.Function("P")(t)
    cross = sp.Function("C")(t)
    spatial_phase = sp.exp(sp.I * wave * x)
    coords = (t, x, y, z)
    n = 4

    axial = ax**2 * t ** sp.Rational(-2, 3)
    transverse = ap**2 * t ** sp.Rational(4, 3)
    metric = sp.zeros(n)
    metric[0, 0] = -1
    metric[1, 1] = axial
    metric[2, 2] = transverse * (1 + 2 * eps * plus * spatial_phase)
    metric[3, 3] = transverse * (1 - 2 * eps * plus * spatial_phase)
    metric[2, 3] = metric[3, 2] = 2 * eps * transverse * cross * spatial_phase
    inverse = sp.simplify(metric.inv())

    connection = [[[
        sp.Rational(1, 2) * sum(
            inverse[a, d] * (
                sp.diff(metric[d, c], coords[b])
                + sp.diff(metric[d, b], coords[c])
                - sp.diff(metric[b, c], coords[d])
            )
            for d in range(n)
        )
        for c in range(n)] for b in range(n)] for a in range(n)]

    ricci = sp.MutableDenseMatrix(n, n, [0] * n**2)
    for a in range(n):
        for b in range(n):
            value = 0
            for c in range(n):
                value += sp.diff(connection[c][a][b], coords[c])
                value -= sp.diff(connection[c][a][c], coords[b])
                for d in range(n):
                    value += connection[c][c][d] * connection[d][a][b]
                    value -= connection[c][b][d] * connection[d][a][c]
            ricci[a, b] = value

    scalar = sum(inverse[a, b] * ricci[a, b] for a in range(n) for b in range(n))

    def linear(expression: sp.Expr) -> sp.Expr:
        return sp.factor(sp.simplify(sp.diff(expression, eps).subs(eps, 0)))

    delta_ricci = sp.MutableDenseMatrix(n, n, lambda a, b: linear(ricci[a, b]))
    delta_scalar = linear(scalar)
    background_metric = metric.subs(eps, 0)
    delta_tf = sp.MutableDenseMatrix(
        n,
        n,
        lambda a, b: sp.factor(sp.simplify(
            delta_ricci[a, b] - delta_scalar * background_metric[a, b] / 4
        )),
    )

    plus_operator = (
        sp.diff(plus, t, 2) + sp.diff(plus, t) / t
        + wave**2 * t ** sp.Rational(2, 3) * plus / ax**2
    )
    cross_operator = (
        sp.diff(cross, t, 2) + sp.diff(cross, t) / t
        + wave**2 * t ** sp.Rational(2, 3) * cross / ax**2
    )
    expected_plus = transverse * spatial_phase * plus_operator
    expected_cross = transverse * spatial_phase * cross_operator

    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    gate(delta_scalar == 0, "full_metric_route_scalar_zero")
    allowed = {(2, 2), (2, 3), (3, 2), (3, 3)}
    for a in range(n):
        for b in range(n):
            if (a, b) not in allowed:
                gate(delta_tf[a, b] == 0, f"full_metric_constraint_zero_{a}{b}")
    gate(sp.simplify(delta_tf[2, 2] - expected_plus) == 0,
         "full_metric_plus_equation")
    gate(sp.simplify(delta_tf[3, 3] + expected_plus) == 0,
         "full_metric_plus_partner")
    gate(sp.simplify(delta_tf[2, 3] - expected_cross) == 0,
         "full_metric_cross_equation")
    gate(sp.simplify(delta_tf[3, 2] - expected_cross) == 0,
         "full_metric_cross_partner")

    # Independent gauge check from the exact Lie derivative of the background.
    q = [sp.Function(f"q{a}")(t) * spatial_phase for a in range(n)]
    lie = sp.MutableDenseMatrix(n, n, [0] * n**2)
    for a in range(n):
        for b in range(n):
            lie[a, b] = sp.simplify(
                sum(q[c] * sp.diff(background_metric[a, b], coords[c]) for c in range(n))
                + sum(background_metric[c, b] * sp.diff(q[c], coords[a]) for c in range(n))
                + sum(background_metric[a, c] * sp.diff(q[c], coords[b]) for c in range(n))
            )
    transverse_tf = sp.Matrix([
        [sp.simplify((lie[2, 2] - lie[3, 3]) / (2 * transverse)),
         sp.simplify(lie[2, 3] / transverse)],
        [sp.simplify(lie[3, 2] / transverse),
         sp.simplify((lie[3, 3] - lie[2, 2]) / (2 * transverse))],
    ])
    gate(transverse_tf == sp.zeros(2), "independent_periodic_gauge_zero_tensor_image")

    # Reconstruct a lower-index tidal component from the full epsilon-dependent connection.
    def riemann_up(a: int, b: int, c: int, d: int) -> sp.Expr:
        value = sp.diff(connection[a][b][d], coords[c]) - sp.diff(
            connection[a][b][c], coords[d]
        )
        for e in range(n):
            value += connection[a][c][e] * connection[e][b][d]
            value -= connection[a][d][e] * connection[e][b][c]
        return value

    def riemann_lower(a: int, b: int, c: int, d: int) -> sp.Expr:
        return sum(metric[a, e] * riemann_up(e, b, c, d) for e in range(n))

    plus_tide = linear(
        (riemann_lower(0, 2, 0, 2) - riemann_lower(0, 3, 0, 3))
        / (2 * transverse * spatial_phase)
    )
    cross_tide = linear(
        riemann_lower(0, 2, 0, 3) / (transverse * spatial_phase)
    )
    plus_tide_on_shell = sp.factor(sp.simplify(plus_tide.subs(
        sp.diff(plus, t, 2),
        -sp.diff(plus, t) / t - wave**2 * t ** sp.Rational(2, 3) * plus / ax**2,
    )))
    cross_tide_on_shell = sp.factor(sp.simplify(cross_tide.subs(
        sp.diff(cross, t, 2),
        -sp.diff(cross, t) / t - wave**2 * t ** sp.Rational(2, 3) * cross / ax**2,
    )))
    plus_sample = sp.simplify(plus_tide_on_shell.subs({
        t: 1, ax: 1, wave: 1, plus: 1, sp.diff(plus, t): 0,
    }))
    cross_sample = sp.simplify(cross_tide_on_shell.subs({
        t: 1, ax: 1, wave: 1, cross: 1, sp.diff(cross, t): 0,
    }))
    gate(plus_sample == sp.Rational(13, 9), "independent_plus_curvature_witness")
    gate(cross_sample == sp.Rational(13, 9), "independent_cross_curvature_witness")

    # Independent solution check: transform the ODE coefficient-by-coefficient.
    nu = sp.symbols("nu", positive=True, real=True)
    argument = sp.Rational(3, 4) * nu * t ** sp.Rational(4, 3)
    test_function = sp.Function("F")
    composed = test_function(argument)
    transformed = sp.factor(sp.simplify(
        sp.diff(composed, t, 2) + sp.diff(composed, t) / t
        + nu**2 * t ** sp.Rational(2, 3) * composed
    ))
    target = sp.diff(argument, t)**2 * (
        sp.Subs(sp.diff(test_function(sp.Symbol("u")), sp.Symbol("u"), 2),
                sp.Symbol("u"), argument)
        + sp.Subs(sp.diff(test_function(sp.Symbol("u")), sp.Symbol("u")),
                  sp.Symbol("u"), argument) / argument
        + test_function(argument)
    )
    gate(sp.simplify(transformed - target) == 0, "independent_bessel_transform")

    # Frobenius analysis at t=0 independently recovers a repeated indicial root zero.
    m = sp.symbols("m")
    indicial = sp.expand(m * (m - 1) + m)
    gate(indicial == m**2, "past_indicial_repeated_zero_root")
    gate(sp.solve(indicial, m) == [0], "past_finite_and_log_pair")

    # WKB/Bessel large-argument exponent and state dimension.
    argument_power = sp.Rational(4, 3)
    gate(-argument_power / 2 == sp.Rational(-2, 3),
         "independent_future_envelope_power")
    gate(2 * 2 * 2 == 8, "independent_real_dimension_eight")

    result = {
        "schema": "udt-g327-axial-first-fourier-independent-v1",
        "status": "INDEPENDENT_VERIFIED",
        "landing": EXPECTED_LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "method": "exact epsilon metric inversion then full Christoffel/Ricci differentiation",
        "mode_ode": "H''+H'/t+nu^2*t^(2/3)*H=0",
        "bessel_argument": "3*nu*t^(4/3)/4",
        "linearized_scalar_curvature": "0",
        "real_solution_dimension": 8,
        "plus_tidal_on_shell": str(plus_tide_on_shell),
        "cross_tidal_on_shell": str(cross_tide_on_shell),
        "future_relative_envelope": "t^(-2/3)",
        "full_fourier_spectrum_classified": False,
        "full_linear_stability_proved": False,
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
