#!/usr/bin/env python3
"""Exact founded-phi complete-coframe extension classification."""

from __future__ import annotations

import json
import sympy as sp


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    phi, phi1, phi2 = sp.symbols("phi phi1 phi2", real=True)
    c = sp.symbols("c", positive=True)
    a, b, d = sp.symbols("a b d", real=True)
    s11, s12, s21, s22 = sp.symbols("s11 s12 s21 s22", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    H = sp.diag(-1, 1)
    K = sp.Matrix([[a, b], [0, d]])
    C = sp.Matrix([[s11, s12], [s21, s22]])
    X = H.row_join(sp.zeros(2)).col_join(C.row_join(K))
    checks: dict[str, str] = {}

    # General generator count after the full founded base generator is fixed.
    extension_parameters = (a, b, d, s11, s12, s21, s22)
    tangents = [X.diff(parameter) for parameter in extension_parameters]
    tangent_matrix = sp.Matrix.hstack(*(value.reshape(16, 1) for value in tangents))
    check("seven_extension_parameters", len(extension_parameters) == 7, checks)
    check("seven_extension_tangent_rank", tangent_matrix.rank() == 7, checks)
    check("founded_base_generator_fixed", X[:2, :2] == H, checks)
    check("upper_block_zero", X[:2, 2:] == sp.zeros(2), checks)

    # Determinant character and determinant-one subfamily.
    check("full_generator_trace_is_angular_trace", sp.trace(X) == a + d, checks)
    determinant_character = sp.exp(phi * sp.trace(X))
    check(
        "determinant_character",
        sp.simplify(determinant_character - sp.exp(phi * (a + d))) == 0,
        checks,
    )
    determinant_one_basis = [
        X.subs({a: 1, d: -1, b: 0, s11: 0, s12: 0, s21: 0, s22: 0}),
        X.diff(b),
        X.diff(s11),
        X.diff(s12),
        X.diff(s21),
        X.diff(s22),
    ]
    extension_only_det_one = [
        value - H.row_join(sp.zeros(2)).col_join(sp.zeros(2, 4))
        if index == 0 else value
        for index, value in enumerate(determinant_one_basis)
    ]
    check(
        "six_det_one_extension_directions",
        sp.Matrix.hstack(
            *(value.reshape(16, 1) for value in extension_only_det_one)
        ).rank()
        == 6,
        checks,
    )

    # Angular metric invariance in the triangular section.
    angular_metric_tangent = sp.simplify(K.T + K)
    check(
        "angular_metric_tangent",
        angular_metric_tangent == sp.Matrix([[2 * a, b], [b, 2 * d]]),
        checks,
    )
    angular_solution = sp.solve(
        list(angular_metric_tangent), (a, b, d), dict=True
    )
    check(
        "triangular_angular_invariance_forces_zero_generator",
        angular_solution == [{a: 0, b: 0, d: 0}],
        checks,
    )

    # Metric mixing appears at first order exactly through C.
    metric_tangent = sp.simplify(X.T * eta + eta * X)
    check("base_angular_metric_tangent_is_C_transpose", metric_tangent[:2, 2:] == C.T, checks)
    check("angular_base_metric_tangent_is_C", metric_tangent[2:, :2] == C, checks)
    mixing_solution = sp.solve(list(C), (s11, s12, s21, s22), dict=True)
    check(
        "no_metric_mixing_forces_zero_shift_generator",
        mixing_solution == [{s11: 0, s12: 0, s21: 0, s22: 0}],
        checks,
    )

    # Exact spectator extension and physical metric readout.
    spectator = sp.diag(sp.exp(-phi), sp.exp(phi), 1, 1)
    spectator1 = spectator.subs(phi, phi1)
    spectator2 = spectator.subs(phi, phi2)
    check(
        "spectator_composition",
        zero(spectator2 * spectator1 - spectator.subs(phi, phi1 + phi2)),
        checks,
    )
    check("spectator_reversal", zero(spectator.subs(phi, -phi) * spectator - sp.eye(4)), checks)
    check("spectator_determinant_one", sp.simplify(spectator.det()) == 1, checks)
    calibrated = sp.diag(c, 1, 1, 1) * spectator
    spectator_metric = sp.simplify(calibrated.T * eta * calibrated)
    check(
        "spectator_metric_readout",
        spectator_metric
        == sp.diag(-c**2 * sp.exp(-2 * phi), sp.exp(2 * phi), 1, 1),
        checks,
    )

    # Nontrivial determinant-one angular counterfamily.
    k = sp.symbols("k", real=True)
    angular = sp.diag(
        sp.exp(-phi), sp.exp(phi), sp.exp(-k * phi), sp.exp(k * phi)
    )
    check("angular_counterfamily_projects_founded_pair", angular[:2, :2] == spectator[:2, :2], checks)
    check("angular_counterfamily_determinant_one", sp.simplify(angular.det()) == 1, checks)
    check(
        "angular_counterfamily_composition",
        zero(
            angular.subs(phi, phi2) * angular.subs(phi, phi1)
            - angular.subs(phi, phi1 + phi2)
        ),
        checks,
    )
    angular_metric = sp.simplify(angular.T * eta * angular)
    check(
        "angular_counterfamily_changes_transverse_metric",
        angular_metric[2:, 2:]
        == sp.diag(sp.exp(-2 * k * phi), sp.exp(2 * k * phi)),
        checks,
    )
    check(
        "angular_counterfamily_nontrivial_for_k_nonzero",
        angular_metric[2:, 2:].subs({k: 1, phi: 1}) != sp.eye(2),
        checks,
    )

    # Exact determinant-one shift counterfamily from a lower-block generator.
    shift_strength = sp.symbols("shift_strength", real=True)
    shift = sp.eye(4)
    shift[0, 0] = sp.exp(-phi)
    shift[1, 1] = sp.exp(phi)
    shift[2, 0] = shift_strength * (1 - sp.exp(-phi))
    check("shift_counterfamily_projects_founded_pair", shift[:2, :2] == spectator[:2, :2], checks)
    check("shift_counterfamily_determinant_one", sp.simplify(shift.det()) == 1, checks)
    check(
        "shift_counterfamily_composition",
        zero(
            shift.subs(phi, phi2) * shift.subs(phi, phi1)
            - shift.subs(phi, phi1 + phi2)
        ),
        checks,
    )
    shift_metric = sp.simplify(shift.T * eta * shift)
    check(
        "shift_counterfamily_has_metric_cross_term",
        sp.simplify(
            shift_metric[0, 2]
            - shift_strength * (1 - sp.exp(-phi))
        )
        == 0,
        checks,
    )
    check(
        "shift_counterfamily_nontrivial",
        shift_metric.subs({shift_strength: 1, phi: 1})
        != spectator_metric.subs({c: 1, phi: 1}),
        checks,
    )

    # The direct sum is unique only after both extra spectator premises.
    check(
        "spectator_unique_given_transverse_invariance_and_no_mixing",
        angular_solution == [{a: 0, b: 0, d: 0}]
        and mixing_solution == [{s11: 0, s12: 0, s21: 0, s22: 0}],
        checks,
    )

    if len(checks) != 27:
        raise AssertionError(f"unexpected check count {len(checks)}")

    result = {
        "schema": "udt-founded-phi-complete-coframe-extension-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "complete_triangular_metric_modes": 10,
            "fixed_founded_base_generator_modes": 3,
            "free_extension_generator_parameters": 7,
            "determinant_one_extension_parameters": 6,
            "spectator_extension_parameters": 0,
        },
        "rulings": {
            "founded_phi_role": "ADDITIVE_PARAMETER_OF_FIXED_RECIPROCAL_BASE_SUBGROUP",
            "extension_existence": "DERIVED_EXACT_DIRECT_SUM_WITNESS",
            "unrestricted_uniqueness": "REFUTED_BY_ANGULAR_AND_SHIFT_COUNTERFAMILIES",
            "spectator_uniqueness": "UNIQUE_ONLY_GIVEN_TRANSVERSE_METRIC_INVARIANCE_AND_NO_BASE_ANGULAR_MIXING_IN_SUPPLIED_TRIANGULAR_SECTION",
            "physical_selection": "OPEN_NOT_SELECTED_BY_FOUNDED_TWO_CHANNEL_POSTULATES",
            "scope": "POINTWISE_CONTINUOUS_ONE_PARAMETER_EXTENSIONS_IN_REGISTERED_TRIANGULAR_COFRAME_CHART",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
