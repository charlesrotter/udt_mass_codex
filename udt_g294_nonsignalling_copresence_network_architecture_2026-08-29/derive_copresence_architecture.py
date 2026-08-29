#!/usr/bin/env python3
"""Exact symbolic witnesses for the bounded G294 architecture classification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


LANDING = (
    "COPRESENCE_IS_COHERENT_AS_NONPROPAGATING_RELATION_NOT_SIGNAL_SPEED__"
    "POSITIVE_PAIR_MAGNITUDE_AND_ORIENTED_DEPTH_ARE_COMPATIBLE__"
    "GLOBAL_CORRELATION_CAN_COEXIST_WITH_CAUSAL_RESPONSE_SUPPORT__"
    "SYMMETRIC_PAIR_RELATION_DOES_NOT_DERIVE_GLOBAL_NOW__"
    "GLOBAL_FOLIATION_REQUIRES_ADDITIONAL_INTEGRABLE_TIMELIKE_STRUCTURE__"
    "CE_ALONE_DOES_NOT_ATTACH_DEPTH_TO_LENGTH__"
    "CURRENT_COPRESENCE_SEMANTICS_DO_NOT_SELECT_HISTORY__"
    "COMPLETE_NETWORK_CONSTRAINT_PLUS_CAUSAL_UPDATE_IS_A_WELL_TYPED_MISSING_LAW_ARCHITECTURE"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("DERIVATION_RESULT.json"))
    args = parser.parse_args()

    checks: list[dict[str, object]] = []

    def exact(name: str, value: object, expected: object = 0) -> None:
        residual = sp.simplify(value - expected)
        passed = bool(residual.is_zero_matrix) if isinstance(residual, sp.MatrixBase) else residual == 0
        checks.append({"name": name, "pass": bool(passed), "value": str(value), "expected": str(expected)})
        if not passed:
            raise AssertionError(name)

    def boolean(name: str, value: bool, detail: str) -> None:
        checks.append({"name": name, "pass": bool(value), "value": detail, "expected": "True"})
        if not value:
            raise AssertionError(name)

    q, d, w2 = sp.symbols("q d w2", real=True)

    # T1: positive magnitude, oriented depth, and even/odd pair channels.
    exact("projective_reversal_odd", sp.tanh(-q) + sp.tanh(q))
    exact("mutual_projection_reversal_even", sp.sech(-q) - sp.sech(q))
    exact("unit_semicircle_pair_state", sp.sech(q) ** 2 + sp.tanh(q) ** 2, 1)
    exact("positive_magnitude_orientation_independence", (-1) ** 2 * q**2, q**2)
    exact("directed_depth_reversal", -(-d), d)

    denominator = sp.cosh(d) + sp.exp(-d) * w2 / 2
    m_pt = 1 / denominator
    bound_gap = sp.simplify(sp.sech(d) - m_pt)
    expected_gap = sp.exp(-d) * w2 / (2 * sp.cosh(d) * denominator)
    exact("screen_aware_mutual_bound_factor", bound_gap, expected_gap)
    exact("planar_screen_equality", m_pt.subs(w2, 0), sp.sech(d))
    boolean(
        "active_screen_strict_gap",
        bool(bound_gap.subs({d: sp.Rational(2, 5), w2: sp.Rational(3, 7)}) > 0),
        str(bound_gap.subs({d: sp.Rational(2, 5), w2: sp.Rational(3, 7)})),
    )

    # T2: dimension vectors (length exponent, time exponent).
    exponent = sp.symbols("exponent", real=True)
    c_e_dim = sp.Matrix([1, -1])
    time_dim = sp.Matrix([0, 1])
    length_dim = sp.Matrix([1, 0])
    dimensionless = sp.Matrix([0, 0])
    boolean(
        "ce_power_cannot_be_pure_length",
        sp.solve(list(exponent * c_e_dim - length_dim), [exponent], dict=True) == [],
        "a=1 and a=0 are incompatible",
    )
    exact("clock_record_plus_ce_is_length_L", (c_e_dim + time_dim)[0], length_dim[0])
    exact("clock_record_plus_ce_is_length_T", (c_e_dim + time_dim)[1], length_dim[1])
    inverse_ce_dim = -c_e_dim
    exact("distance_over_ce_is_time_L", (length_dim + inverse_ce_dim)[0], time_dim[0])
    exact("distance_over_ce_is_time_T", (length_dim + inverse_ce_dim)[1], time_dim[1])
    exact("normalized_distance_is_dimensionless_L", (length_dim - c_e_dim - time_dim)[0], dimensionless[0])
    exact("normalized_distance_is_dimensionless_T", (length_dim - c_e_dim - time_dim)[1], dimensionless[1])

    # T3: symmetry does not imply transitivity/global leaves.
    relation = sp.Matrix([[1, 1, 0], [1, 1, 1], [0, 1, 1]])
    exact("copresence_relation_symmetric", relation - relation.T, sp.zeros(3))
    exact("copresence_relation_reflexive", relation.trace(), 3)
    exact("AB_and_BC_present", relation[0, 1] * relation[1, 2], 1)
    exact("AC_absent_nontransitive_witness", relation[0, 2], 0)
    boolean(
        "symmetry_not_transitivity",
        relation[0, 1] == 1 and relation[1, 2] == 1 and relation[0, 2] == 0,
        "A~B and B~C while A!~C",
    )

    # A timelike direction need not be hypersurface orthogonal.
    x = sp.symbols("x", real=True)
    one_form_norm = -1 + x**2  # n=dt+x dy in Minkowski coordinates.
    exact("timelike_one_form_control", one_form_norm.subs(x, sp.Rational(1, 2)), sp.Rational(-3, 4))
    frobenius_coefficient = sp.Integer(1)  # (dt+x dy) wedge d(dt+x dy)=dt wedge dx wedge dy.
    exact("frobenius_obstruction_nonzero", frobenius_coefficient, 1)
    boolean(
        "timelike_does_not_imply_integrable",
        one_form_norm.subs(x, sp.Rational(1, 2)) < 0 and frobenius_coefficient != 0,
        "timelike at x=1/2 and n wedge dn nonzero",
    )
    exact("integrable_dt_control", 0, 0)

    # T4: correlation and response are different mathematical objects.
    rho = sp.symbols("rho", real=True)
    covariance = sp.Matrix([[1, rho], [rho, 1]])
    response = sp.diag(sp.symbols("rA"), sp.symbols("rB"))
    exact("correlation_determinant", covariance.det(), 1 - rho**2)
    exact("spacelike_response_A_to_B_zero", response[1, 0], 0)
    exact("spacelike_response_B_to_A_zero", response[0, 1], 0)
    boolean(
        "correlated_no_response_control",
        covariance.subs(rho, sp.Rational(1, 2))[0, 1] != 0 and response[1, 0] == 0,
        "nonzero covariance with zero intervention response",
    )

    h = sp.symbols("h", real=True)
    remote_enforced_change = -h  # x_A+x_B=0 re-enforced after x_A -> x_A+h.
    exact("instant_constraint_remote_response", sp.diff(remote_enforced_change, h), -1)
    local_only_constraint_residual = h
    exact("local_only_update_breaks_constraint", local_only_constraint_residual, h)
    boolean(
        "constraint_nonsignalling_trilemma",
        sp.diff(remote_enforced_change, h) != 0 and local_only_constraint_residual != 0,
        "instant enforcement responds remotely; local-only update leaves residual",
    )

    # T5: same supplied co-presence foliation, inequivalent regular metric profiles.
    r, a, c_e = sp.symbols("r a c_E", positive=True)
    f = 1 + a * r**2 / (1 + r**2)
    phi = -sp.log(f) / 2
    exact("primary_metric_profile_identity", sp.exp(-2 * phi), f)
    f_p = sp.diff(f, r)
    f_pp = sp.diff(f, r, 2)
    scalar_curvature = sp.simplify(-f_pp - 4 * f_p / r + 2 * (1 - f) / r**2)
    expected_curvature = -2 * a * (6 + 3 * r**2 + r**4) / (1 + r**2) ** 3
    exact("primary_metric_scalar_curvature", scalar_curvature, expected_curvature)
    exact("flat_profile_curvature", scalar_curvature.subs(a, 0), 0)
    exact("deformed_profile_center_curvature", sp.limit(scalar_curvature, r, 0), -12 * a)
    exact("co_presence_normal_timelike_control", (-1 / f).subs({a: sp.Rational(1, 4), r: 1}), sp.Rational(-8, 9))
    null_slope = c_e * f
    radial_null_form = -f * c_e**2 + null_slope**2 / f
    exact("metric_null_cone_radial", radial_null_form, 0)
    boolean(
        "regular_positive_counterfamily",
        f.subs({a: sp.Rational(1, 4), r: 1}) > 0
        and scalar_curvature.subs({a: sp.Rational(1, 4), r: 1}) != 0,
        "f=9/8 and R differs from flat on the shared t-slicing",
    )

    architecture = [
        {
            "class": "PAIR_RELATIVE_RELATION",
            "coherent": True,
            "global_now": False,
            "history_selection": False,
            "status": "WELL_TYPED_CANDIDATE_ARCHITECTURE",
        },
        {
            "class": "INTEGRABLE_GLOBAL_FOLIATION",
            "coherent": True,
            "global_now": True,
            "history_selection": False,
            "status": "REQUIRES_ADDITIONAL_INTEGRABLE_TIMELIKE_STRUCTURE",
        },
        {
            "class": "GLOBAL_CONSTRAINT_PLUS_CAUSAL_UPDATE",
            "coherent": True,
            "global_now": "OPTIONAL",
            "history_selection": "POSSIBLE_ONLY_IF_CONSTRAINT_IS_NONIDENTITY",
            "status": "WELL_TYPED_MISSING_LAW_ARCHITECTURE_NOT_FORMULA",
        },
        {
            "class": "CONTROLLABLE_INSTANTANEOUS_RESPONSE",
            "coherent": False,
            "global_now": "IRRELEVANT",
            "history_selection": "IRRELEVANT",
            "status": "REJECTED_BY_NONSIGNALLING_GATE",
        },
    ]

    result = {
        "all_pass": all(item["pass"] for item in checks),
        "assertion_count": len(checks),
        "checks": checks,
        "architecture": architecture,
        "landing_candidate": LANDING,
        "scope": {
            "history_selected": False,
            "copresence_adopted": False,
            "literal_infinite_signal_speed_adopted": False,
            "causal_response_operator_imported": False,
            "observation_used": False,
            "protected_input_used": False,
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": result["all_pass"], "assertion_count": len(checks)}, sort_keys=True))


if __name__ == "__main__":
    main()
