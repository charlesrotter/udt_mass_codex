#!/usr/bin/env python3
"""Exact G106 sky/depth projection algebra; no observational outcomes."""

from __future__ import annotations

import json
import os
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
LANDING = (
    "COMPLETE_SKY_DEPTH_REFERENCE_PROJECTOR_DERIVED_CONDITIONALLY"
    "__PURE_RADIAL_MODULATION_REMOVED"
    "__DEPTH_DEPENDENT_ANGULAR_RESPONSE_SURVIVES"
    "__ONE_HISTORY_CROSS_WINDOW_TEST_DEFINED"
    "__PHYSICAL_HISTORY_AND_OUTCOMES_OPEN"
)


def matrix_as_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.factor(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def projector_witness() -> dict:
    s = [sp.Rational(1, 10), sp.Rational(2, 10), sp.Rational(3, 10), sp.Rational(4, 10)]
    pz = [sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)]
    u = [-2, -1, 0, 1]
    amp = [sp.Rational(1, 10), 0, sp.Rational(1, 5)]
    p = sp.Matrix(
        [[pz[i] * s[j] * (1 + amp[i] * u[j]) for j in range(4)] for i in range(3)]
    )

    def reference(density: sp.Matrix) -> sp.Matrix:
        row_mass = [sum(density[i, j] for j in range(density.cols)) for i in range(density.rows)]
        return sp.Matrix([[row_mass[i] * s[j] for j in range(4)] for i in range(density.rows)])

    q = reference(p)
    residual = sp.simplify(p - q)
    q_twice = reference(q)
    radial = sp.Matrix([[pz[i] * s[j] for j in range(4)] for i in range(3)])
    radial_residual = sp.simplify(radial - reference(radial))
    row_residuals = [sp.factor(sum(residual[i, j] for j in range(4))) for i in range(3)]
    checks = {
        "selection_normalized": sp.factor(sum(s)) == 1,
        "angular_mode_zero_selection_mean": sp.factor(sum(s[j] * u[j] for j in range(4))) == 0,
        "density_normalized": sp.factor(sum(p)) == 1,
        "density_positive": all(value > 0 for value in p),
        "reference_idempotent": q_twice == q,
        "residual_in_kernel": row_residuals == [0, 0, 0],
        "pure_radial_removed": radial_residual == sp.zeros(3, 4),
        "angular_depth_residual_nonzero": residual != sp.zeros(3, 4),
    }
    checks = {name: bool(value) for name, value in checks.items()}
    return {
        "selection": [str(value) for value in s],
        "depth_marginal": [str(value) for value in pz],
        "angular_mode": [str(value) for value in u],
        "depth_amplitude": [str(value) for value in amp],
        "density": matrix_as_strings(p),
        "reference": matrix_as_strings(q),
        "residual": matrix_as_strings(residual),
        "residual_row_masses": [str(value) for value in row_residuals],
        "checks": checks,
    }


def coordinate_invariance_witness() -> dict:
    m = sp.Matrix(
        [
            [2, sp.Rational(1, 3), sp.Rational(1, 5)],
            [sp.Rational(1, 3), 3, sp.Rational(1, 7)],
            [sp.Rational(1, 5), sp.Rational(1, 7), 5],
        ]
    )
    gamma = sp.Matrix(
        [
            [3, sp.Rational(1, 4), 0],
            [sp.Rational(1, 4), 2, sp.Rational(1, 6)],
            [0, sp.Rational(1, 6), 4],
        ]
    )
    c = sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    ratio = sp.factor(m.det() / gamma.det())
    transformed = sp.factor((c.T * m * c).det() / (c.T * gamma * c).det())
    return {
        "det_C": str(c.det()),
        "ratio": str(ratio),
        "transformed_ratio": str(transformed),
        "invariant": bool(sp.simplify(ratio - transformed) == 0),
        "positive": bool(ratio > 0),
    }


def global_full_sky_witness() -> dict:
    t, mu = sp.symbols("t mu", real=True)
    amplitude = (2 * t - 1) ** 2 / 4
    p2 = (3 * mu**2 - 1) / 2
    source_mu = mu + amplitude * (mu**3 - mu) / 2
    density_ratio = sp.factor(sp.diff(source_mu, mu))
    expected = sp.factor(1 + amplitude * p2)
    intervals = [
        (sp.Rational(0), sp.Rational(1, 3)),
        (sp.Rational(1, 3), sp.Rational(2, 3)),
        (sp.Rational(2, 3), sp.Rational(1)),
    ]
    averages = [sp.factor(sp.integrate(amplitude, (t, lo, hi)) / (hi - lo)) for lo, hi in intervals]
    c = sp.symbols("c", real=True)
    fourth_moment = (1 + 2 * c**2) / 15
    fixed_separation_average = sp.factor((9 * fourth_moment - 1) / 4)
    expected_correlation = sp.factor((3 * c**2 - 1) / 10)
    pair_coefficients = [sp.factor(value**2 / 5) for value in averages]
    checks = {
        "jacobian_identity": sp.simplify(density_ratio - expected) == 0,
        "north_pole_fixed": sp.simplify(source_mu.subs(mu, 1) - 1) == 0,
        "south_pole_fixed": sp.simplify(source_mu.subs(mu, -1) + 1) == 0,
        "full_sky_normalization": sp.integrate(expected, (mu, -1, 1)) == 2,
        "density_lower_bound": sp.factor(expected.subs({t: sp.Rational(0), mu: 0})) == sp.Rational(7, 8),
        "density_upper_bound": sp.factor(expected.subs({t: sp.Rational(0), mu: 1})) == sp.Rational(5, 4),
        "fixed_separation_identity": sp.simplify(fixed_separation_average - expected_correlation) == 0,
        "loud_quiet_loud": averages[0] == averages[2] and averages[0] == 13 * averages[1],
        "pair_ratio_169": sp.factor(pair_coefficients[0] / pair_coefficients[1]) == 169,
    }
    checks = {name: bool(value) for name, value in checks.items()}
    return {
        "amplitude": str(sp.factor(amplitude)),
        "P2": str(p2),
        "source_mu_of_observer_mu": str(sp.factor(source_mu)),
        "density_ratio": str(density_ratio),
        "window_averages": [str(value) for value in averages],
        "pair_coefficients": [str(value) for value in pair_coefficients],
        "fixed_separation_correlation": str(expected_correlation),
        "checks": checks,
    }


def main() -> None:
    coordinate = coordinate_invariance_witness()
    projector = projector_witness()
    full_sky = global_full_sky_witness()
    checks = {
        "coordinate_invariance": all([coordinate["invariant"], coordinate["positive"]]),
        "reference_projection": all(projector["checks"].values()),
        "full_sky_witness": all(full_sky["checks"].values()),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "landing": LANDING,
        "checks": checks,
        "coordinate_invariance_witness": coordinate,
        "reference_projector_witness": projector,
        "full_sky_witness": full_sky,
        "outcome_paths_read": [],
    }
    if result["status"] != "PASS":
        raise AssertionError(result)
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
