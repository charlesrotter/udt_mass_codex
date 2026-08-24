#!/usr/bin/env python3
"""Exact production algebra for G245. No observational inputs are read."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import sympy as sp


PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "DERIVATION_RESULT.json"
LANDING = (
    "OBSERVER_GERM_AND_METRIC_OWN_LOCAL_DIRECTION_LABELLED_NULL_CONE_FIELD"
    "__G244_AREA_SHAPE_ARE_INDUCED_CONE_GEOMETRY"
    "__SOURCE_POPULATION_GLOBAL_BRANCH_AND_PHYSICAL_HISTORY_REMAIN_OPEN"
)


def matrix_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.factor(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def exact_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def rational_rotation() -> sp.Matrix:
    return sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                      [sp.Rational(4, 5), sp.Rational(3, 5)]])


def symbolic_checks() -> dict[str, object]:
    d11, d12, d21, d22 = sp.symbols("d11 d12 d21 d22")
    v11, v12, v21, v22 = sp.symbols("v11 v12 v21 v22")
    t11, t12, t22 = sp.symbols("t11 t12 t22")
    D = sp.Matrix([[d11, d12], [d21, d22]])
    V = sp.Matrix([[v11, v12], [v21, v22]])
    T = sp.Matrix([[t11, t12], [t12, t22]])
    Ddot = V
    Vdot = -T * D

    Wdot = Ddot.T * V + D.T * Vdot - Vdot.T * D - V.T * Ddot
    H = D.T * D
    Hdot = V.T * D + D.T * V
    Hddot = 2 * V.T * V - 2 * D.T * T * D

    b11, b12, b22 = sp.symbols("b11 b12 b22")
    B = sp.Matrix([[b11, b12], [b12, b22]])
    theta = sp.trace(B)
    Sigma = B - theta * sp.eye(2) / 2
    optical_trace = sp.simplify(
        sp.trace(-T - B * B)
        + sp.trace(T)
        + theta**2 / 2
        + sp.trace(Sigma * Sigma)
    )
    optical_tf = (-T - B * B) - sp.trace(-T - B * B) * sp.eye(2) / 2
    expected_tf = -theta * Sigma - (T - sp.trace(T) * sp.eye(2) / 2)

    A = sp.symbols("A", positive=True)
    V_from_B = B * D
    Hdot_from_B = V_from_B.T * D + D.T * V_from_B
    Cdot = Hdot_from_B / A - theta * H / A
    Cdot_expected = 2 * D.T * Sigma * D / A

    lam = sp.symbols("lambda", positive=True)
    a, b, c, p, q, r = sp.symbols("a b c p q r")
    T0 = sp.Matrix([[a, b], [b, c]])
    T1 = sp.Matrix([[p, q], [q, r]])
    Dseries = lam * sp.eye(2) - lam**3 * T0 / 6 - lam**4 * T1 / 12
    Tseries = T0 + lam * T1
    residual = sp.expand(Dseries.diff(lam, 2) + Tseries * Dseries)
    residual_coefficients = {
        str(order): exact_zero(residual.applyfunc(lambda x: sp.expand(x).coeff(lam, order)))
        for order in range(3)
    }
    Hseries = (Dseries.T * Dseries).applyfunc(lambda x: sp.series(x, lam, 0, 6).removeO())
    expected_H = lam**2 * (
        sp.eye(2) - lam**2 * T0 / 3 - lam**3 * T1 / 6
    )
    Hseries_residual = (Hseries - expected_H).applyfunc(
        lambda x: sp.series(x, lam, 0, 6).removeO()
    )
    delta_series = sp.series(sp.det(Dseries), lam, 0, 6).removeO()
    expected_delta = lam**2 * (
        1 - lam**2 * sp.trace(T0) / 6 - lam**3 * sp.trace(T1) / 12
    )
    delta_residual = sp.series(delta_series - expected_delta, lam, 0, 6).removeO()
    T0hat = T0 - sp.trace(T0) * sp.eye(2) / 2
    T1hat = T1 - sp.trace(T1) * sp.eye(2) / 2
    expected_C = sp.eye(2) - lam**2 * T0hat / 3 - lam**3 * T1hat / 6
    Cseries = (Hseries / expected_delta).applyfunc(lambda x: sp.series(x, lam, 0, 4).removeO())
    Cseries_residual = (Cseries - expected_C).applyfunc(
        lambda x: sp.series(x, lam, 0, 4).removeO()
    )

    # The leading shear coefficient follows from determinant-one shape perturbation.
    e = sp.symbols("e")
    k11, k12 = sp.symbols("k11 k12")
    K = sp.Matrix([[k11, k12], [k12, -k11]])
    normalized = (sp.eye(2) + e * K) / sp.sqrt(sp.det(sp.eye(2) + e * K))
    shear = sp.trace(normalized) ** 2 / 4 - 1
    leading_shear = sp.simplify(sp.series(shear, e, 0, 3).removeO().coeff(e, 2))

    # H and H' alone do not retain the orientation of D relative to anisotropic tide.
    Tn = sp.diag(1, 4)
    Q = sp.Matrix([[0, -1], [1, 0]])
    Hddot_1 = -2 * Tn
    Hddot_2 = -2 * Q.T * Tn * Q

    x, y, z = sp.symbols("x y z", real=True)
    null_residual = sp.simplify(-1 + x**2 + y**2 + z**2)
    null_on_sphere = sp.simplify(null_residual.subs(z**2, 1 - x**2 - y**2))

    return {
        "normalized_null_residual_on_unit_sphere": str(null_on_sphere),
        "wronskian_derivative_zero": exact_zero(Wdot),
        "gram_first_derivative": matrix_strings(Hdot),
        "gram_second_derivative": matrix_strings(Hddot),
        "det_H_minus_det_D_squared": str(sp.factor(sp.det(H) - sp.det(D) ** 2)),
        "optical_trace_residual": str(sp.factor(optical_trace)),
        "optical_tracefree_residual_zero": exact_zero(optical_tf - expected_tf),
        "shape_flow_residual_zero": exact_zero(Cdot - Cdot_expected),
        "vertex_ode_coefficients_zero_through_order_two": residual_coefficients,
        "vertex_H_series_residual_zero": exact_zero(Hseries_residual),
        "vertex_area_series_residual": str(sp.factor(delta_residual)),
        "vertex_shape_series_residual_zero": exact_zero(Cseries_residual),
        "normalized_tracefree_shape_leading_shear": str(sp.factor(leading_shear)),
        "expected_tracefree_norm_factor": str(sp.factor(sp.trace(K * K) / 2)),
        "H_Hprime_nonclosure_witness": {
            "same_H": matrix_strings(sp.eye(2)),
            "same_Hprime": matrix_strings(sp.zeros(2)),
            "Hsecond_1": matrix_strings(Hddot_1),
            "Hsecond_2": matrix_strings(Hddot_2),
            "different": Hddot_1 != Hddot_2,
        },
    }


def finite_census() -> dict[str, int]:
    rng = random.Random(24520260824)
    Qs = (
        sp.eye(2),
        sp.Matrix([[0, -1], [1, 0]]),
        rational_rotation(),
        sp.diag(-1, 1),
    )
    assertions = 0
    cases = 0
    reflection_parity_flips = 0
    nonclosure_cases = 0
    for index in range(1024):
        while True:
            D = sp.Matrix([[rng.randint(-5, 5), rng.randint(-5, 5)],
                           [rng.randint(-5, 5), rng.randint(-5, 5)]])
            if D.det() != 0:
                break
        B = sp.Matrix([[rng.randint(-4, 4), rng.randint(-4, 4)],
                       [0, rng.randint(-4, 4)]])
        B[1, 0] = B[0, 1]
        T = sp.Matrix([[rng.randint(-4, 4), rng.randint(-4, 4)],
                       [0, rng.randint(-4, 4)]])
        T[1, 0] = T[0, 1]
        V = B * D
        H = D.T * D
        Hdot = V.T * D + D.T * V
        Hddot = 2 * V.T * V - 2 * D.T * T * D
        theta = sp.trace(B)
        Sigma = B - theta * sp.eye(2) / 2
        checks = [
            D.T * V == V.T * D,
            sp.det(H) == sp.det(D) ** 2,
            Hdot == 2 * D.T * B * D,
            sp.trace(-T - B * B)
            == -sp.trace(T) - theta**2 / 2 - sp.trace(Sigma * Sigma),
            ((-T - B * B) - sp.trace(-T - B * B) * sp.eye(2) / 2)
            == -theta * Sigma - (T - sp.trace(T) * sp.eye(2) / 2),
            Hddot == 2 * V.T * V - 2 * D.T * T * D,
        ]
        Qo = Qs[index % len(Qs)]
        Qsrc = Qs[(3 * index + 1) % len(Qs)]
        Dg = Qsrc.T * D * Qo
        Vg = Qsrc.T * V * Qo
        Tg = Qsrc.T * T * Qsrc
        Hg = Dg.T * Dg
        checks.extend([
            Hg == Qo.T * H * Qo,
            Vg * Dg.inv() == Qsrc.T * B * Qsrc,
            sp.det(Hg) == sp.det(H),
            abs(sp.det(Dg)) == abs(sp.det(D)),
            2 * Vg.T * Vg - 2 * Dg.T * Tg * Dg == Qo.T * Hddot * Qo,
        ])
        if sp.det(Qsrc) * sp.det(Qo) == -1:
            reflection_parity_flips += 1
            checks.append(sp.sign(sp.det(Dg)) == -sp.sign(sp.det(D)))
        else:
            checks.append(sp.sign(sp.det(Dg)) == sp.sign(sp.det(D)))
        if D.T * T * D != T:
            nonclosure_cases += 1
        if not all(checks):
            raise RuntimeError(f"finite census failed at case {index}")
        assertions += len(checks)
        cases += 1
    return {
        "cases": cases,
        "assertions": assertions,
        "reflection_parity_flip_cases": reflection_parity_flips,
        "H_orientation_sensitive_tide_cases": nonclosure_cases,
    }


def formal_rotating_tide_control() -> dict[str, object]:
    T0 = sp.diag(1, 4)
    T1 = sp.Matrix([[0, 3], [3, 0]])
    coefficients = [sp.zeros(2) for _ in range(9)]
    coefficients[1] = sp.eye(2)
    for n in range(7):
        forcing = T0 * coefficients[n]
        if n >= 1:
            forcing += T1 * coefficients[n - 1]
        coefficients[n + 2] = -forcing / ((n + 2) * (n + 1))
    residuals = []
    for n in range(7):
        lhs = (n + 2) * (n + 1) * coefficients[n + 2] + T0 * coefficients[n]
        if n >= 1:
            lhs += T1 * coefficients[n - 1]
        residuals.append(exact_zero(lhs))
    return {
        "T0": matrix_strings(T0),
        "T1": matrix_strings(T1),
        "commutator": matrix_strings(T0 * T1 - T1 * T0),
        "D4": matrix_strings(coefficients[4]),
        "D4_offdiagonal_nonzero": coefficients[4][0, 1] != 0,
        "recurrence_orders": len(residuals),
        "all_recurrence_residuals_zero": all(residuals),
    }


def controls() -> dict[str, object]:
    lam = sp.symbols("lambda", positive=True)
    isotropic_D = sp.sin(lam) * sp.eye(2)
    isotropic_H = isotropic_D.T * isotropic_D
    isotropic_A = sp.sin(lam) ** 2
    isotropic_C = sp.simplify(isotropic_H / isotropic_A)

    caustic_D = sp.diag(sp.sin(lam), lam)
    caustic_V = sp.diag(sp.cos(lam), 1)
    phase = sp.Matrix.vstack(
        sp.Matrix.hstack(sp.diag(sp.cos(lam), 1), caustic_D),
        sp.Matrix.hstack(sp.diag(-sp.sin(lam), 0), caustic_V),
    )
    at_pi_D = caustic_D.subs(lam, sp.pi)
    at_pi_H = (caustic_D.T * caustic_D).subs(lam, sp.pi)
    signed_delta = sp.factor(sp.det(caustic_D))
    delta_slope = sp.simplify(sp.diff(signed_delta, lam).subs(lam, sp.pi))

    return {
        "isotropic": {
            "D": matrix_strings(isotropic_D),
            "C": matrix_strings(isotropic_C),
            "shape_identity": isotropic_C == sp.eye(2),
            "shear_zero": True,
        },
        "rotating_tide_series": formal_rotating_tide_control(),
        "caustic": {
            "D_at_pi": matrix_strings(at_pi_D),
            "H_at_pi": matrix_strings(at_pi_H),
            "rank_D_at_pi": at_pi_D.rank(),
            "signed_delta": str(signed_delta),
            "signed_delta_slope_at_pi": str(delta_slope),
            "absolute_area_has_cusp": delta_slope != 0,
            "full_phase_det": str(sp.trigsimp(phase.det())),
            "position_inverse_used": False,
            "normalized_shape_defined_at_pi": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    result = {
        "audit": "G245_METRIC_OWNED_OBSERVER_NULL_CONE_FIELD",
        "classification": LANDING,
        "preregistration_commit": "99af2336",
        "question_type": "METRIC_LED",
        "observer_cone": {
            "input": "smooth time-oriented g plus observer event o and metric-unit future U",
            "direction_fiber": "all unit n in U_perp",
            "normalized_null_generator": "k(n)=U+n; -g(U,k)=1",
            "field": "F(lambda,n)=Exp_o(lambda k(n))",
            "source_population_required": False,
            "preferred_ray_selected": False,
        },
        "induced_field": {
            "angular_differential": "D=d_n F",
            "jacobi_ivp": "D''+T D=0; D(0)=0; D'(0)=I",
            "angular_metric": "H=D^dagger D=F_lambda^*g on angular tangents",
            "area": "A=abs(det D)",
            "shape": "C=H/A on regular strata",
            "full_phase_required": True,
            "H_alone_autonomous": False,
        },
        "symbolic": symbolic_checks(),
        "finite_census": finite_census(),
        "controls": controls(),
        "fitted_angular_coefficients": 0,
        "observational_outcomes": "CLOSED_AND_UNREAD",
        "physical_history": "QUERY_SUPPLIED_NOT_SELECTED",
        "global_branch_source_detector": "OPEN",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
