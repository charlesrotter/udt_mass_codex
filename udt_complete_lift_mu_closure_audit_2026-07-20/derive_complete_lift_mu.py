#!/usr/bin/env python3
"""Exact algebra for the UDT complete-lift/global-cocycle mu audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(name: str, condition, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def require_zero(name: str, expression, checks: dict[str, str]) -> None:
    value = sp.simplify(expression)
    if isinstance(value, sp.MatrixBase):
        good = value == sp.zeros(*value.shape)
    else:
        good = value == 0
    require(name, good, checks)


def block_diagonal(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    output = sp.zeros(left.rows + right.rows)
    output[: left.rows, : left.cols] = left
    output[left.rows :, left.cols :] = right
    return output


def full_metric(base: sp.Matrix, cross: sp.Matrix, angular: sp.Matrix) -> sp.Matrix:
    return base.row_join(cross).col_join(cross.T.row_join(angular))


def pair_invariant(metric: sp.Matrix, generator: sp.Matrix) -> sp.Expr:
    return sp.factor(sp.trace(metric.inv() * generator.T * metric * generator))


def main() -> None:
    checks: dict[str, str] = {}
    k, u, v = sp.symbols("k u v", real=True)
    b, c, a = sp.symbols("b c a", real=True, nonzero=True)
    theta, psi = sp.symbols("theta psi", real=True)
    q11, q12, q22 = sp.symbols("q11 q12 q22", real=True)

    H = sp.Matrix([[1, -k], [-k, 1]])
    L2 = sp.diag(-1, 1)
    F1 = sp.Matrix([[0, 1], [1, 0]])
    L4 = sp.diag(-1, 1, 0, 0)
    Q_general = sp.Matrix([[q11, q12], [q12, q22]])

    lifts = {
        "PLUS_IDENTITY": {
            "A": sp.eye(2),
            "C": sp.Matrix([[u, v], [u, v]]),
            "Q": Q_general,
            "cross_dimension": 2,
            "angular_metric_dimension": 3,
            "orientation": -1,
            "fixed": 3,
            "antifixed": 1,
        },
        "MINUS_IDENTITY": {
            "A": -sp.eye(2),
            "C": sp.Matrix([[u, v], [-u, -v]]),
            "Q": Q_general,
            "cross_dimension": 2,
            "angular_metric_dimension": 3,
            "orientation": -1,
            "fixed": 1,
            "antifixed": 3,
        },
        "AXIS_REFLECTION": {
            "A": sp.diag(1, -1),
            "C": sp.Matrix([[u, v], [u, -v]]),
            "Q": sp.diag(q11, q22),
            "cross_dimension": 2,
            "angular_metric_dimension": 2,
            "orientation": 1,
            "fixed": 2,
            "antifixed": 2,
        },
        "HOPF_EXCHANGE_LOCAL": {
            "A": F1,
            "C": sp.Matrix([[u, v], [v, u]]),
            "Q": sp.Matrix([[q11, q12], [q12, q11]]),
            "cross_dimension": 2,
            "angular_metric_dimension": 2,
            "orientation": 1,
            "fixed": 2,
            "antifixed": 2,
        },
    }

    lift_results: dict[str, dict[str, object]] = {}
    witness_results: dict[str, dict[str, object]] = {}
    epsilon = sp.Rational(1, 10)
    expected_witnesses = {
        "PLUS_IDENTITY": {
            2: (sp.Rational(-78, 25), sp.Rational(-251, 78)),
            3: (sp.Rational(-204, 25), sp.Rational(-251, 102)),
        },
        "MINUS_IDENTITY": {
            2: (sp.Rational(-74, 25), sp.Rational(-247, 74)),
            3: (sp.Rational(-198, 25), sp.Rational(-248, 99)),
        },
        "AXIS_REFLECTION": {
            2: (sp.Rational(-7599, 2500), sp.Rational(-8300, 2533)),
            3: (sp.Rational(-20099, 2500), sp.Rational(-49900, 20099)),
        },
        "HOPF_EXCHANGE_LOCAL": {
            2: (sp.Rational(-78, 25), sp.Rational(-251, 78)),
            3: (sp.Rational(-204, 25), sp.Rational(-251, 102)),
        },
    }

    for name, data in lifts.items():
        angular = data["A"]
        cross = data["C"]
        angular_metric = data["Q"]
        require_zero(f"{name}_angular_involution", angular**2 - sp.eye(2), checks)
        require_zero(
            f"{name}_complete_cross_parity",
            F1.T * cross * angular - cross,
            checks,
        )
        require_zero(
            f"{name}_angular_metric_isometry",
            angular.T * angular_metric * angular - angular_metric,
            checks,
        )
        seal = block_diagonal(F1, angular)
        metric = full_metric(H, cross, angular_metric)
        require_zero(f"{name}_complete_seal_involution", seal**2 - sp.eye(4), checks)
        require_zero(f"{name}_complete_metric_isometry", seal.T * metric * seal - metric, checks)
        require_zero(f"{name}_complete_generator_inversion", seal * L4 * seal + L4, checks)
        require(f"{name}_orientation", seal.det() == data["orientation"], checks)
        require(
            f"{name}_fixed_dimension",
            len((seal - sp.eye(4)).nullspace()) == data["fixed"],
            checks,
        )
        require(
            f"{name}_antifixed_dimension",
            len((seal + sp.eye(4)).nullspace()) == data["antifixed"],
            checks,
        )

        # Witnesses use the same positive angular metric I2 and the same
        # nonzero u=v=1/10 pattern within each lift.
        witness_metric_template = metric.subs({q11: 1, q12: 0, q22: 1})
        invariant_template = pair_invariant(witness_metric_template, L4)
        witness_ids = []
        for kval in (2, 3):
            substitutions = {k: kval, u: epsilon, v: epsilon}
            witness = witness_metric_template.subs(substitutions)
            determinant = sp.factor(witness.det())
            invariant = sp.factor(invariant_template.subs(substitutions))
            expected_det, expected_invariant = expected_witnesses[name][kval]
            label = f"{name}_MU{kval**2}"
            require_zero(f"{label}_determinant", determinant - expected_det, checks)
            require_zero(f"{label}_full_pair_invariant", invariant - expected_invariant, checks)
            require(f"{label}_nonzero_cross", witness[:2, 2:] != sp.zeros(2), checks)
            schur = sp.simplify(
                sp.eye(2)
                - cross.subs({u: epsilon, v: epsilon}).T
                * H.subs(k, kval).inv()
                * cross.subs({u: epsilon, v: epsilon})
            )
            require(
                f"{label}_positive_transverse_Schur",
                schur[0, 0] > 0 and schur.det() > 0,
                checks,
            )
            witness_results[label] = {
                "lift": name,
                "mu": kval**2,
                "determinant": str(expected_det),
                "full_pair_invariant": str(expected_invariant),
                "cross_u": "1/10",
                "cross_v": "1/10",
                "signature": "(-,+,+,+)",
                "orientation": int(data["orientation"]),
                "fixed_antifixed": f"{data['fixed']}/{data['antifixed']}",
            }
            witness_ids.append(label)
        require(
            f"{name}_mu_witnesses_inequivalent",
            witness_results[witness_ids[0]]["full_pair_invariant"]
            != witness_results[witness_ids[1]]["full_pair_invariant"],
            checks,
        )
        lift_results[name] = {
            "cross_dimension": data["cross_dimension"],
            "angular_metric_dimension": data["angular_metric_dimension"],
            "orientation": int(data["orientation"]),
            "fixed_antifixed": f"{data['fixed']}/{data['antifixed']}",
            "mu_values_surviving": [4, 9],
            "status": "CONDITIONAL_LIFT_FAMILY_LEAVES_MU_OPEN",
        }

    require(
        "both_orientation_classes_retain_mu4_and_mu9",
        {
            (row["orientation"], row["mu"])
            for row in witness_results.values()
        }
        == {(-1, 4), (-1, 9), (1, 4), (1, 9)},
        checks,
    )

    # Reciprocal transition group and closed-loop parity.
    def F(value):
        return sp.Matrix([[0, value], [1 / value, 0]])

    def G(value):
        return sp.diag(value, 1 / value)

    require_zero("reciprocal_F_involution", F(b) ** 2 - sp.eye(2), checks)
    require_zero("reciprocal_even_product", F(b) * F(c) - G(b / c), checks)
    require_zero("reciprocal_valid_triple_cocycle", F(b) * F(c) * G(c / b) - sp.eye(2), checks)
    require(
        "reciprocal_three_inversions_not_identity",
        F(b) * F(c) * F(a) != sp.eye(2),
        checks,
    )
    require_zero("reciprocal_conjugation", G(a) * F(b) * G(1 / a) - F(a**2 * b), checks)

    # Every normalized base seal is the same standard reflection, independent
    # of k. The k-dependent modulus remains in the normalized reciprocal generator.
    alpha = sp.symbols("alpha", positive=True)
    kval = sp.symbols("kval", real=True, positive=True)
    Hk = sp.Matrix([[alpha, -kval * alpha], [-kval * alpha, alpha]])
    vp = sp.Matrix([1, 1])
    vm = sp.Matrix([-1, 1])
    nt = sp.sqrt(2 * alpha * (kval - 1))
    nr = sp.sqrt(2 * alpha * (kval + 1))
    S0 = sp.Matrix.hstack(vp / nt, vm / nr)
    normalized_seal = sp.simplify(S0.inv() * F1 * S0)
    normalized_generator = sp.simplify(S0.inv() * L2 * S0)
    require_zero("normalized_seal_mu_blind", normalized_seal - sp.diag(1, -1), checks)
    require(
        "normalized_seal_same_for_mu4_mu9",
        normalized_seal.subs(kval, 2) == normalized_seal.subs(kval, 3),
        checks,
    )
    require(
        "normalized_generator_retains_mu",
        normalized_generator.subs(kval, 2) != normalized_generator.subs(kval, 3),
        checks,
    )

    # Axis-reflection corners. Their group words depend on relative axes and
    # declared order, not on the metric modulus.
    def rotation(angle):
        return sp.Matrix(
            [[sp.cos(angle), -sp.sin(angle)], [sp.sin(angle), sp.cos(angle)]]
        )

    def angular_axis(angle):
        return sp.simplify(
            rotation(angle) * sp.diag(1, -1) * rotation(angle).T
        )

    A_theta = angular_axis(theta)
    A_psi = angular_axis(psi)
    angular_corner = sp.simplify(A_theta * A_psi)
    require_zero(
        "angular_corner_trace",
        sp.trace(angular_corner) - 2 * sp.cos(2 * (theta - psi)),
        checks,
    )
    require_zero(
        "same_axis_angular_corner_identity",
        angular_corner.subs(psi, theta) - sp.eye(2),
        checks,
    )
    require_zero(
        "perpendicular_axis_reflections_commute",
        (A_theta * A_psi - A_psi * A_theta).subs(psi, theta + sp.pi / 2),
        checks,
    )
    require(
        "generic_axis_reflections_do_not_commute",
        (A_theta * A_psi - A_psi * A_theta).subs({theta: 0, psi: sp.pi / 4})
        != sp.zeros(2),
        checks,
    )
    require_zero(
        "quarter_turn_corner_order_four",
        (A_theta * A_psi).subs({theta: 0, psi: sp.pi / 4}) ** 4 - sp.eye(2),
        checks,
    )
    require_zero(
        "corner_word_has_zero_mu_derivative",
        angular_corner.diff(k),
        checks,
    )

    # Mirror-compatible primitive cap determinants are multiple and contain no mu.
    cap_pairs = {
        "P0": ((1, 1), (1, 1), 0),
        "P1": ((1, 0), (0, 1), 1),
        "P3": ((2, 1), (1, 2), 3),
        "P5": ((3, 2), (2, 3), 5),
    }
    for label, (left, right, expected) in cap_pairs.items():
        determinant = abs(left[0] * right[1] - left[1] * right[0])
        require(f"{label}_cap_determinant", determinant == expected, checks)
    require(
        "cap_classes_remain_multiple",
        {entry[2] for entry in cap_pairs.values()} == {0, 1, 3, 5},
        checks,
    )

    outcomes = [
        "ORIENTATION_CLASS_LEAVES_MU_OPEN",
        "CORNER_COCYCLE_IS_MU_BLIND",
        "ALL_REGISTERED_ALGEBRAIC_LIFTS_LEAVE_MU_OPEN",
        "NONZERO_CROSS_BLOCKS_LEAVE_MU_OPEN_IN_EVERY_LIFT",
        "NORMALIZED_SEAL_TRANSITIONS_ARE_MU_BLIND",
        "CONDITIONAL_HOPF_LIFT_HAS_NO_CURRENT_MU_EQUATION",
        "METRIC_DEPENDENT_GLOBAL_CLOSURE_EQUATION_ABSENT",
        "GLOBAL_COMPLETION_REMAINS_OPEN",
    ]
    result = {
        "schema": "udt-complete-lift-mu-closure-derivation-1.0",
        "maximum_conclusion": "UDT_COMPLETE_LIFT_AND_GLOBAL_MU_CLOSURE_STATUS_CHARACTERIZED",
        "outcomes": outcomes,
        "lift_results": lift_results,
        "witnesses": witness_results,
        "transition_result": {
            "reciprocal_group": "Z2_GRADED_EVEN_REVERSAL_PARITY",
            "normalized_seal": "diag(+1,-1) independent of mu",
            "normalized_generator": "retains mu through sqrt((k-1)/(k+1))",
            "corner_words": "depend on transition ratios, angular axes, and declared order; no mu variable occurs",
        },
        "orientation_result": {
            "orientation_reversing_lifts": ["PLUS_IDENTITY", "MINUS_IDENTITY"],
            "orientation_preserving_lifts": ["AXIS_REFLECTION", "HOPF_EXCHANGE_LOCAL"],
            "both_classes_mu_values": [4, 9],
            "status": "ORIENTATION_CLASS_LEAVES_MU_OPEN",
        },
        "global_authority": {
            "cover": "OPEN",
            "overlap_incidence": "OPEN",
            "corner_order_and_angles": "OPEN",
            "caps_periods_lattice_topology": "OPEN_OR_CONDITIONAL",
            "normal_time_on_executable_lift": "OPEN",
            "metric_dependent_equation_for_pair_invariant": "ABSENT_FROM_CURRENT_LEDGER",
            "bootstrap_role": "ON_SHELL_ADMISSIBILITY_NO_CURRENT_MU_EQUATION",
        },
        "check_count": len(checks),
        "checks": checks,
        "exclusions": [
            "topology, cap, period, or corner choice",
            "action, field equation, or boundary functional",
            "physical representative, scale, or Xmax",
            "carrier, source, mass, and matter",
            "GPU work and canonization",
        ],
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
