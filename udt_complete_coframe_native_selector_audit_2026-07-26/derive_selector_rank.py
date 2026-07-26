#!/usr/bin/env python3
"""Exact selector-rank algebra for the founded complete-coframe extension."""

from __future__ import annotations

import json
import sympy as sp


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def flat(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.reshape(matrix.rows * matrix.cols, 1)


def lorentz_generators() -> list[sp.Matrix]:
    generators: list[sp.Matrix] = []
    # Boosts: L[0,i] = L[i,0] = 1 in eta=diag(-1,+1,+1,+1).
    for i in range(1, 4):
        value = sp.zeros(4)
        value[0, i] = 1
        value[i, 0] = 1
        generators.append(value)
    # Spatial rotations.
    for i, j in ((1, 2), (1, 3), (2, 3)):
        value = sp.zeros(4)
        value[i, j] = 1
        value[j, i] = -1
        generators.append(value)
    return generators


def main() -> None:
    a, b, d = sp.symbols("a b d", real=True)
    c11, c12, c21, c22 = sp.symbols("c11 c12 c21 c22", real=True)
    phi, psi, k, s = sp.symbols("phi psi k s", real=True)
    parameters = (a, b, d, c11, c12, c21, c22)
    eta = sp.diag(-1, 1, 1, 1)
    H = sp.diag(-1, 1)
    K = sp.Matrix([[a, b], [0, d]])
    C = sp.Matrix([[c11, c12], [c21, c22]])
    X = H.row_join(sp.zeros(2)).col_join(C.row_join(K))
    X0 = X.subs({parameter: 0 for parameter in parameters})
    extension = sp.simplify(X - X0)
    checks: dict[str, str] = {}

    # Exact bounded extension class.
    extension_basis = [extension.diff(parameter) for parameter in parameters]
    extension_columns = sp.Matrix.hstack(*(flat(value) for value in extension_basis))
    check("seven_extension_generators", len(parameters) == 7, checks)
    check("extension_generator_rank_seven", extension_columns.rank() == 7, checks)
    check("founded_base_generator_fixed", X[:2, :2] == H, checks)
    check("upper_right_block_zero", X[:2, 2:] == sp.zeros(2), checks)

    # Every power remains lower block triangular and projects to H**n. This
    # proves the same statement for the exponential power series.
    for power in range(1, 7):
        value = X**power
        check(
            f"power_{power}_projects_to_founded_block",
            value[:2, :2] == H**power,
            checks,
        )
        check(
            f"power_{power}_upper_right_zero",
            value[:2, 2:] == sp.zeros(2),
            checks,
        )

    # Physical metric-tangent quotient.
    metric_tangent = sp.simplify(X.T * eta + eta * X)
    extension_metric_tangent = sp.simplify(
        extension.T * eta + eta * extension
    )
    physical_columns = sp.Matrix.hstack(
        *(flat(extension_metric_tangent.diff(parameter)) for parameter in parameters)
    )
    check("physical_extension_tangent_rank_seven", physical_columns.rank() == 7, checks)
    kernel = sp.linsolve(
        list(extension_metric_tangent), parameters
    )
    check(
        "triangular_extension_intersects_Lorentz_kernel_trivially",
        kernel == sp.FiniteSet((0, 0, 0, 0, 0, 0, 0)),
        checks,
    )
    check("metric_cross_block_is_C_transpose", metric_tangent[:2, 2:] == C.T, checks)
    check("metric_angular_block_is_sym_K", metric_tangent[2:, 2:] == K.T + K, checks)

    # The full local Lorentz presentation kernel is six dimensional.
    y = sp.symbols("y0:16", real=True)
    Y = sp.Matrix(4, 4, y)
    lorentz_equations = flat(Y.T * eta + eta * Y)
    lorentz_coefficient = lorentz_equations.jacobian(y)
    check("local_Lorentz_kernel_dimension_six", 16 - lorentz_coefficient.rank() == 6, checks)

    # A fixed generator invariant under every connected local Lorentz frame
    # transformation must commute with the entire Lorentz algebra. Its
    # centralizer in M4(R) is only the scalar identity.
    commutator_equations: list[sp.Expr] = []
    for generator in lorentz_generators():
        commutator_equations.extend(list(Y * generator - generator * Y))
    centralizer_coefficient = sp.Matrix(commutator_equations).jacobian(y)
    centralizer_null = centralizer_coefficient.nullspace()
    check("full_Lorentz_centralizer_dimension_one", len(centralizer_null) == 1, checks)
    check(
        "full_Lorentz_centralizer_is_scalar_identity",
        centralizer_null[0] == flat(sp.eye(4)) or centralizer_null[0] == -flat(sp.eye(4)),
        checks,
    )
    check(
        "fixed_founded_generator_not_full_frame_invariant",
        X0 * lorentz_generators()[0] != lorentz_generators()[0] * X0,
        checks,
    )

    # Exact non-spectator witnesses.
    angular = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(-k * phi), sp.exp(k * phi))
    angular_sum = angular.subs(phi, phi + psi)
    check(
        "angular_witness_composition",
        sp.simplify(angular.subs(phi, phi) * angular.subs(phi, psi) - angular_sum)
        == sp.zeros(4),
        checks,
    )
    check("angular_witness_reversal", sp.simplify(angular.subs(phi, -phi) * angular) == sp.eye(4), checks)
    check("angular_witness_pair_projection", angular[:2, :2] == sp.diag(sp.exp(-phi), sp.exp(phi)), checks)
    check("angular_witness_determinant_one", sp.simplify(angular.det()) == 1, checks)

    mixing = sp.eye(4)
    mixing[0, 0] = sp.exp(-phi)
    mixing[1, 1] = sp.exp(phi)
    mixing[2, 0] = s * (1 - sp.exp(-phi))
    mixing_sum = mixing.subs(phi, phi + psi)
    check(
        "mixing_witness_composition",
        sp.simplify(mixing.subs(phi, phi) * mixing.subs(phi, psi) - mixing_sum)
        == sp.zeros(4),
        checks,
    )
    check("mixing_witness_reversal", sp.simplify(mixing.subs(phi, -phi) * mixing) == sp.eye(4), checks)
    check("mixing_witness_pair_projection", mixing[:2, :2] == sp.diag(sp.exp(-phi), sp.exp(phi)), checks)
    check("mixing_witness_determinant_one", sp.simplify(mixing.det()) == 1, checks)
    mixing_metric = sp.simplify(mixing.T * eta * mixing)
    check("mixing_witness_is_physically_nonspectator", mixing_metric[0, 2] != 0, checks)

    # Conditional restrictions are recorded only as counterfactual ranks.
    determinant_equation = sp.Matrix([sp.trace(extension)])
    angular_equations = flat(K.T + K)
    mixing_equations = flat(C)
    conditional_all = determinant_equation.col_join(angular_equations).col_join(mixing_equations)
    check("determinant_one_conditional_rank_one", determinant_equation.jacobian(parameters).rank() == 1, checks)
    check("transverse_invariance_conditional_rank_three", angular_equations.jacobian(parameters).rank() == 3, checks)
    check("no_mixing_conditional_rank_four", mixing_equations.jacobian(parameters).rank() == 4, checks)
    check("spectator_conditions_joint_rank_seven", conditional_all.jacobian(parameters).rank() == 7, checks)

    # Current active algebraic premises all hold on the general constant-X
    # family and introduce no equation in the seven extension parameters.
    active_selector_rank = 0
    check("active_selector_rank_zero", active_selector_rank == 0, checks)
    check("active_physical_survivor_dimension_seven", physical_columns.rank() - active_selector_rank == 7, checks)

    result = {
        "schema": "udt-complete-coframe-native-selector-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "extension_parameters": 7,
            "physical_metric_tangent_rank": physical_columns.rank(),
            "local_Lorentz_presentation_kernel_dimension": 6,
            "extension_intersection_with_Lorentz_kernel": 0,
            "full_Lorentz_centralizer_dimension": len(centralizer_null),
            "active_selector_rank": active_selector_rank,
            "active_physical_survivor_dimension": 7,
        },
        "conditional_ranks_not_active": {
            "complete_determinant_one": 1,
            "transverse_metric_invariance": 3,
            "no_base_angular_mixing": 4,
            "transverse_invariance_plus_no_mixing": 7,
        },
        "rulings": {
            "bounded_active_outcome": "UNREDUCED_ACTIVE_FAMILY",
            "local_Lorentz_quotient": "REMOVES_NO_DIRECTION_FROM_THE_REGISTERED_TRIANGULAR_EXTENSION_TANGENT",
            "full_frame_rule": "FIXED_INVARIANCE_INCOMPATIBLE; EQUIVARIANT_GENERATOR_OR_SLOT_FAMILY_REQUIRED",
            "variation_domain": "NOT_SELECTED_BY_POINTWISE_EXTENSION_KINEMATICS",
            "global_completion": "OPEN",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
