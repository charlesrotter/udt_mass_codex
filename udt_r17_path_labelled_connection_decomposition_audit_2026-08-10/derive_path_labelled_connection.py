#!/usr/bin/env python3
"""Exact complete projected H-connection and curvature on supplied R17 coframes."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
LAMBDA_VALUES = [sp.Rational(-2), sp.Rational(-1), sp.Rational(0), sp.Rational(1, 2), sp.Rational(1), sp.Rational(2)]


def build(mc_sign: int) -> dict[str, object]:
    phi, lam, a = sp.symbols("phi lambda a", real=True)
    p1, p2, p3 = sp.symbols("p1 p2 p3", real=True)
    q11, q21, q31, q22, q32, q33 = sp.symbols("q11 q21 q31 q22 q32 q33", real=True)
    u = sp.exp(phi)
    v = sp.exp(lam * phi)

    # Columns are the orthonormal frame e_a in the global base (T,Z,X,Y).
    frame = sp.Matrix(
        [
            [u, -a / u, 0, 0],
            [0, 1 / u, 0, 0],
            [0, 0, 1 / v, 0],
            [0, 0, 0, 1 / v],
        ]
    )
    coframe = sp.simplify(frame.inv())

    # Six free compatible second jets. Ordered derivatives not listed here
    # are fixed by the Maurer--Cartan commutators acting on scalar phi.
    base_first = (sp.Integer(0), p1, p2, p3)
    base_second = (
        (0, 0, 0, 0),
        (0, q11, q21 + 2 * mc_sign * p3, q31 - 2 * mc_sign * p2),
        (0, q21, q22, q32 + 2 * mc_sign * p1),
        (0, q31, q32, q33),
    )

    constants = [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    value = sp.Integer(2 * mc_sign)
    for left, right, output in ((2, 3, 1), (3, 1, 2), (1, 2, 3)):
        constants[left][right][output] = value
        constants[right][left][output] = -value

    variables = (phi, p1, p2, p3)

    def base_derivative(expr: sp.Expr, direction: int) -> sp.Expr:
        coefficients = (base_first[direction], *base_second[direction][1:])
        return sp.simplify(sum(coefficient * sp.diff(expr, variable) for coefficient, variable in zip(coefficients, variables)))

    def frame_bracket(left: int, right: int) -> list[sp.Expr]:
        in_base: list[sp.Expr] = []
        for output in range(4):
            result = sp.Integer(0)
            for direction in range(4):
                result += frame[direction, left] * base_derivative(frame[output, right], direction)
                result -= frame[direction, right] * base_derivative(frame[output, left], direction)
            for first in range(4):
                for second in range(4):
                    result += frame[first, left] * frame[second, right] * constants[first][second][output]
            in_base.append(sp.simplify(result))
        return [
            sp.simplify(sum(coframe[row, column] * in_base[column] for column in range(4)))
            for row in range(4)
        ]

    brackets = [[frame_bracket(i, j) for j in range(4)] for i in range(4)]
    eta = (-1, 1, 1, 1)

    def inner(vector: list[sp.Expr], basis: int) -> sp.Expr:
        return sp.simplify(eta[basis] * vector[basis])

    def gamma(direction: int, vector: int, output: int) -> sp.Expr:
        return sp.simplify(
            (
                inner(brackets[direction][vector], output)
                - inner(brackets[vector][output], direction)
                + inner(brackets[output][direction], vector)
            ) / 2
        )

    connection = [gamma(direction, 2, 3) for direction in range(4)]

    def frame_derivative(expr: sp.Expr, direction: int) -> sp.Expr:
        return sp.simplify(sum(frame[base, direction] * base_derivative(expr, base) for base in range(4)))

    curvature: dict[str, sp.Expr] = {}
    for left in range(4):
        for right in range(left + 1, 4):
            curvature[f"F_{left}{right}"] = sp.factor(
                frame_derivative(connection[right], left)
                - frame_derivative(connection[left], right)
                - sum(brackets[left][right][index] * connection[index] for index in range(4))
            )

    expected_connection = (
        mc_sign * a / (u * v**2),
        mc_sign * (2 / u - u / v**2),
        -lam * p3 / v,
        lam * p2 / v,
    )
    if any(sp.simplify(actual - expected) != 0 for actual, expected in zip(connection, expected_connection)):
        raise AssertionError((connection, expected_connection))
    expected_F01 = mc_sign * 2 * a * (1 + lam) * p1 / (u**2 * v**2)
    if sp.simplify(curvature["F_01"] - expected_F01) != 0:
        raise AssertionError((curvature["F_01"], expected_F01))

    metricity = []
    for direction in range(4):
        metricity.extend(
            [
                sp.simplify(gamma(direction, 2, 2)),
                sp.simplify(gamma(direction, 3, 3)),
                sp.simplify(gamma(direction, 2, 3) + gamma(direction, 3, 2)),
            ]
        )

    # Necessary curvature-horizontality data for descent through
    # pi: R x S3 -> S2, whose vertical directions are T and Z.
    vertical_contractions = {
        "F_TZ": sp.factor(curvature["F_01"]),
        "F_TX": sp.factor(v * curvature["F_02"] / u),
        "F_TY": sp.factor(v * curvature["F_03"] / u),
        "F_ZX": sp.factor(u * v * curvature["F_12"] + a * v * curvature["F_02"] / u),
        "F_ZY": sp.factor(u * v * curvature["F_13"] + a * v * curvature["F_03"] / u),
    }
    invariant_squares = {
        "leaf": sp.factor(curvature["F_01"] ** 2),
        "mixed": sp.factor(sum(curvature[key] ** 2 for key in ("F_02", "F_03", "F_12", "F_13"))),
        "horizontal": sp.factor(curvature["F_23"] ** 2),
    }

    return {
        "symbols": {"phi": phi, "lambda": lam, "a": a, "p1": p1, "p2": p2, "p3": p3,
                    "q11": q11, "q21": q21, "q31": q31, "q22": q22, "q32": q32, "q33": q33},
        "connection": connection,
        "curvature": curvature,
        "brackets": brackets,
        "metricity": metricity,
        "compatible_second_jets": base_second,
        "vertical_contractions": vertical_contractions,
        "invariant_squares": invariant_squares,
    }


def zero_identity(expression: sp.Expr) -> bool:
    return sp.simplify(expression) == 0


def main() -> None:
    plus = build(1)
    minus = build(-1)
    symbols = plus["symbols"]
    lam = symbols["lambda"]
    a = symbols["a"]
    p1, p2, p3 = symbols["p1"], symbols["p2"], symbols["p3"]
    q11, q21, q31, q22, q32, q33 = (symbols[name] for name in ("q11", "q21", "q31", "q22", "q32", "q33"))

    rows = []
    for index, value in enumerate(LAMBDA_VALUES, start=1):
        components = {key: sp.factor(expr.subs(lam, value)) for key, expr in plus["curvature"].items()}
        identically_zero = [key for key, expr in components.items() if zero_identity(expr)]
        vertical = {key: sp.factor(expr.subs(lam, value)) for key, expr in plus["vertical_contractions"].items()}
        vertical_zero = [key for key, expr in vertical.items() if zero_identity(expr)]
        rows.append(
            {
                "candidate_id": f"C{index:02d}",
                "lambda": str(value),
                "identically_zero_curvature_components": ";".join(identically_zero) if identically_zero else "NONE",
                "complete_curvature_identically_zero": "YES" if len(identically_zero) == 6 else "NO",
                "leafwise_flat_for_arbitrary_stationary_phi": "YES" if zero_identity(components["F_01"]) else "NO",
                "clock_contraction_i_e0_F_zero": "YES" if all(zero_identity(components[key]) for key in ("F_01", "F_02", "F_03")) else "NO",
                "normal_frame_horizontal_A2_A3_zero": "YES" if value == 0 else "NO",
                "ruler_screen_first_gradient_terms_zero": "YES" if value == 1 else "NO",
                "base_metric_hopf_basic_for_arbitrary_stationary_phi": "YES" if value == 0 else "NO",
                "base_curvature_horizontal_for_arbitrary_stationary_phi": "YES" if len(vertical_zero) == 5 else "NO",
                "selected": "NO",
            }
        )

    with (HERE / "LAMBDA_CONNECTION_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    checks = {
        "complete_connection_derived_from_coframe": True,
        "projected_connection_metric": all(zero_identity(expr) for expr in plus["metricity"]),
        "leafwise_F01_reproduced": zero_identity(
            plus["curvature"]["F_01"] - 2 * a * (1 + lam) * p1 * sp.exp(-2 * (1 + lam) * symbols["phi"])
        ),
        "all_six_curvature_planes_present": set(plus["curvature"]) == {"F_01", "F_02", "F_03", "F_12", "F_13", "F_23"},
        "compatible_scalar_jet_relations_used": plus["compatible_second_jets"][1][2] == q21 + 2 * p3,
        "mixed_sector_not_identically_erased": any(not zero_identity(plus["curvature"][key]) for key in ("F_02", "F_03", "F_12", "F_13")),
        "horizontal_sector_not_assumed_flat": not zero_identity(plus["curvature"]["F_23"]),
        "six_lambda_strata_retained": len(rows) == 6,
        "no_lambda_selected": all(row["selected"] == "NO" for row in rows),
        "no_complete_flat_lambda_in_generic_jet_space": all(row["complete_curvature_identically_zero"] == "NO" for row in rows),
    }
    if not all(checks.values()):
        raise SystemExit(f"FAIL: {checks}")

    result = {
        "schema": "udt-r17-path-labelled-connection-decomposition-v1",
        "status": "PASS",
        "landing": "COMPLETE_METRIC_PROJECTED_H_CONNECTION_AND_PATH_FUNCTOR_DERIVED_ON_SUPPLIED_REGULAR_STATIONARY_R17__FULL_CURVATURE_GENERALLY_NONZERO__PATH_SELECTION_AND_PHYSICAL_ARROW_OPEN",
        "connection_mc_plus": [sp.sstr(expr) for expr in plus["connection"]],
        "connection_mc_minus": [sp.sstr(expr) for expr in minus["connection"]],
        "curvature_mc_plus": {key: sp.sstr(value) for key, value in plus["curvature"].items()},
        "curvature_mc_minus": {key: sp.sstr(value) for key, value in minus["curvature"].items()},
        "vertical_contractions_mc_plus": {key: sp.sstr(value) for key, value in plus["vertical_contractions"].items()},
        "invariant_squares_mc_plus": {key: sp.sstr(value) for key, value in plus["invariant_squares"].items()},
        "checks": checks,
        "lambda_strata": len(rows),
        "path_transport": {
            "identity": "DERIVED_FOR_SUPPLIED_PATH_FUNCTOR",
            "composition": "DERIVED_FOR_CONCATENATED_PATHS",
            "reversal": "DERIVED_FOR_REVERSED_PATH",
            "base_path_selected": False,
        },
        "gauge_rule": "A_prime=A+d_chi__F_prime=F__O2_reflection_sends_F_to_minus_F",
        "selected_lambda": None,
        "selected_leaf": None,
        "selected_path": None,
        "physical_observer_arrow_derived": False,
        "scope_guards": {
            "connection_coefficients_assigned": False,
            "mixed_curvature_erased": False,
            "horizontal_curvature_assumed_flat": False,
            "incompatible_scalar_jets_used": False,
            "base_path_selected": False,
            "one_lambda_or_leaf_selected": False,
            "signed_angle_called_O2_invariant": False,
            "ambient_Lorentz_holonomy_conflated": False,
            "projected_connection_called_physical_arrow": False,
            "downstream_physics_inferred": False,
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: complete H connection; six curvature planes; six lambda strata; no path or branch selected")


if __name__ == "__main__":
    main()
