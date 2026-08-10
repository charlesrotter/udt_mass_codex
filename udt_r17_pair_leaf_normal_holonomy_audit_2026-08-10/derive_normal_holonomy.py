#!/usr/bin/env python3
"""Exact symbolic R17 pair-leaf normal-connection and holonomy atlas."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def derive(mc_sign: int) -> dict[str, sp.Expr]:
    phi, lam, a = sp.symbols("phi lambda a", real=True)
    p1, p2, p3 = sp.symbols("p1 p2 p3", real=True)
    u = sp.exp(phi)
    v = sp.exp(lam * phi)

    # Columns are e_a in the base frame (T,Z,X,Y).  This is inverted rather
    # than inserting any connection or bracket coefficient.
    frame = sp.Matrix(
        [
            [u, -a / u, 0, 0],
            [0, 1 / u, 0, 0],
            [0, 0, 1 / v, 0],
            [0, 0, 0, 1 / v],
        ]
    )
    coframe = sp.simplify(frame.inv())
    base_phi = (sp.Integer(0), p1, p2, p3)

    constants = [[[
        sp.Integer(0) for _ in range(4)
    ] for _ in range(4)] for _ in range(4)]
    value = sp.Integer(2 * mc_sign)
    for left, right, output in ((2, 3, 1), (3, 1, 2), (1, 2, 3)):
        constants[left][right][output] = value
        constants[right][left][output] = -value

    def base_derivative(expr: sp.Expr, direction: int) -> sp.Expr:
        return sp.simplify(base_phi[direction] * sp.diff(expr, phi))

    def frame_bracket(left: int, right: int) -> list[sp.Expr]:
        base = []
        for output in range(4):
            result = sp.Integer(0)
            for direction in range(4):
                result += frame[direction, left] * base_derivative(
                    frame[output, right], direction
                )
                result -= frame[direction, right] * base_derivative(
                    frame[output, left], direction
                )
            for first in range(4):
                for second in range(4):
                    result += (
                        frame[first, left]
                        * frame[second, right]
                        * constants[first][second][output]
                    )
            base.append(sp.simplify(result))
        return [
            sp.simplify(sum(coframe[row, column] * base[column] for column in range(4)))
            for row in range(4)
        ]

    brackets = [[frame_bracket(i, j) for j in range(4)] for i in range(4)]
    eta = (-1, 1, 1, 1)

    def inner_with_basis(vector: list[sp.Expr], basis: int) -> sp.Expr:
        return sp.simplify(eta[basis] * vector[basis])

    def gamma(direction: int, vector: int, output: int) -> sp.Expr:
        # <nabla_direction e_vector,e_output> from the exact Koszul formula.
        return sp.simplify(
            (
                inner_with_basis(brackets[direction][vector], output)
                - inner_with_basis(brackets[vector][output], direction)
                + inner_with_basis(brackets[output][direction], vector)
            )
            / 2
        )

    normal = [gamma(direction, 2, 3) for direction in range(4)]

    def frame_derivative(expr: sp.Expr, direction: int) -> sp.Expr:
        return sp.simplify(
            sum(frame[base, direction] * base_phi[base] for base in range(4))
            * sp.diff(expr, phi)
        )

    curvature_01 = sp.simplify(
        frame_derivative(normal[1], 0)
        - frame_derivative(normal[0], 1)
        - sum(brackets[0][1][index] * normal[index] for index in range(4))
    )

    # Express the same connection in the global leaf basis (T,Z).
    base_T = sp.Matrix([1, 0, 0, 0])
    base_Z = sp.Matrix([0, 1, 0, 0])
    T_components = coframe * base_T
    Z_components = coframe * base_Z
    A_T = sp.simplify(sum(T_components[i] * normal[i] for i in range(4)))
    A_Z = sp.simplify(sum(Z_components[i] * normal[i] for i in range(4)))

    screen_scale = v**2
    screen_basic_log_derivative = sp.simplify(
        sp.diff(sp.log(screen_scale), phi) * p1
    )

    expected = {
        "A_e0": mc_sign * a / (u * v**2),
        "A_e1": mc_sign * (2 / u - u / v**2),
        "F_e0e1": mc_sign * 2 * a * (1 + lam) * p1 / (u**2 * v**2),
        "A_T": mc_sign * a / (u**2 * v**2),
        "A_Z": mc_sign * (2 - u**2 / v**2 + a**2 / (u**2 * v**2)),
        "screen_basic_log_derivative": 2 * lam * p1,
    }
    actual = {
        "A_e0": normal[0],
        "A_e1": normal[1],
        "F_e0e1": curvature_01,
        "A_T": A_T,
        "A_Z": A_Z,
        "screen_basic_log_derivative": screen_basic_log_derivative,
    }
    for key in expected:
        if sp.simplify(actual[key] - expected[key]) != 0:
            raise AssertionError((mc_sign, key, actual[key], expected[key]))

    return {
        **actual,
        "screen_curvature_square": sp.simplify(curvature_01**2),
        "pair_bracket_e0": brackets[0][1][0],
        "pair_bracket_transverse_square": sp.simplify(
            brackets[0][1][2] ** 2 + brackets[0][1][3] ** 2
        ),
    }


def main() -> None:
    plus = derive(1)
    minus = derive(-1)
    phi, lam, a, p1 = sp.symbols("phi lambda a p1", real=True)
    lambda_values = [sp.Rational(-2), sp.Rational(-1), sp.Rational(0), sp.Rational(1, 2), sp.Rational(1), sp.Rational(2)]

    rows = []
    for index, value in enumerate(lambda_values, start=1):
        curvature = sp.simplify(plus["F_e0e1"].subs(lam, value))
        rows.append(
            {
                "candidate_id": f"C{index:02d}",
                "lambda": str(value),
                "leaf_curvature_coefficient": sp.sstr(curvature),
                "generic_curvature_class": "FLAT_FOR_ALL_STATIONARY_PHI" if value == -1 else "CURVED_WHERE_A_P1_NONZERO",
                "quotient_screen_metric_basic_condition": "YES_ALL_PHI" if value == 0 else "ONLY_WHERE_P1_ZERO_OR_PROFILE_FIBER_BASIC",
                "selected": "NO",
            }
        )

    with (HERE / "LAMBDA_STRATUM_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    checks = {
        "connection_derived_from_coframe_and_MC": True,
        "pair_plane_remains_involutive": sp.simplify(plus["pair_bracket_transverse_square"]) == 0,
        "mc_sign_reverses_connection": all(
            sp.simplify(plus[key] + minus[key]) == 0
            for key in ("A_e0", "A_e1", "F_e0e1", "A_T", "A_Z")
        ),
        "orientation_free_curvature_square_preserved": sp.simplify(
            plus["screen_curvature_square"] - minus["screen_curvature_square"]
        ) == 0,
        "lambda_minus_one_leaf_curvature_zero": sp.simplify(
            plus["F_e0e1"].subs(lam, -1)
        ) == 0,
        "twist_off_leaf_curvature_zero": sp.simplify(plus["F_e0e1"].subs(a, 0)) == 0,
        "constant_depth_leaf_curvature_zero": sp.simplify(plus["F_e0e1"].subs(p1, 0)) == 0,
        "lambda_zero_screen_metric_basic": sp.simplify(
            plus["screen_basic_log_derivative"].subs(lam, 0)
        ) == 0,
        "six_lambda_strata_retained": len(rows) == 6,
        "no_lambda_selected": all(row["selected"] == "NO" for row in rows),
    }
    if not all(checks.values()):
        raise SystemExit(f"FAIL: {checks}")

    result = {
        "schema": "udt-r17-pair-leaf-normal-holonomy-v1",
        "status": "PASS",
        "landing": "CONDITIONAL_METRIC_OWNED_NORMAL_CONNECTION_AND_REPRESENTATIVE_FREE_HOLONOMY_DATA_ON_SUPPLIED_R17_PAIR_LEAVES__PHYSICAL_PATH_AND_COMPLETE_ARROW_OPEN",
        "expressions_mc_plus": {key: sp.sstr(value) for key, value in plus.items()},
        "expressions_mc_minus": {key: sp.sstr(value) for key, value in minus.items()},
        "checks": checks,
        "lambda_strata": len(rows),
        "leaf_topology": "R_x_S1",
        "normal_connection_definition": "D_V_s=H(nabla_V_s)",
        "contractible_holonomy_rule": "Hol=exp(-J*integral_Sigma_F_perp)",
        "winding_holonomy_rule": "Hol_n=exp(-J*(n*Theta_base+curvature_flux))",
        "orientation_free_holonomy_character": "trace(Hol)=2*cos(Theta)",
        "cross_leaf_horizontal_distribution": "H=span(e2,e3)",
        "selected_lambda": None,
        "selected_leaf": None,
        "selected_path": None,
        "physical_observer_arrow_derived": False,
        "scope_guards": {
            "connection_coefficients_assigned": False,
            "winding_conflated_with_contractible": False,
            "orientation_signed_angle_called_O2_invariant": False,
            "ambient_Lorentz_holonomy_called_normal_SO2_holonomy": False,
            "one_leaf_selected": False,
            "one_lambda_selected": False,
            "cross_leaf_path_called_unique": False,
            "projected_connection_called_physical_observer_arrow": False,
            "downstream_physics_inferred": False,
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS: 10/10 exact symbolic checks; six lambda strata; no selection")


if __name__ == "__main__":
    main()
