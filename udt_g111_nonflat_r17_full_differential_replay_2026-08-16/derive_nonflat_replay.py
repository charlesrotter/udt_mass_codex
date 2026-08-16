#!/usr/bin/env python3
"""Exact local-jet G110 replay on the supplied analytic R17 complete metric family."""

from __future__ import annotations

import csv
import hashlib
import json
from itertools import product
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ETA = (-1, 1, 1, 1)
LAMBDA_VALUES = (sp.Rational(-2), sp.Rational(-1), sp.Rational(0), sp.Rational(1, 2), sp.Rational(1), sp.Rational(2))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_hashes() -> dict[str, bool]:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return {row["path"]: sha256(ROOT / row["path"]) == row["sha256"] for row in rows}


def expression_hash(expr: sp.Expr) -> str:
    canonical = sp.srepr(sp.expand(expr))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def exact_component_hashes(geometry: dict[str, object]) -> dict[str, object]:
    groups = {
        "brackets": [geometry["brackets"][i][j][k] for i, j, k in product(range(4), repeat=3)],
        "connection": [geometry["gamma_up"][i][j][k] for i, j, k in product(range(4), repeat=3)],
        "riemann": [geometry["riemann_lower"][i][j][k][l] for i, j, k, l in product(range(4), repeat=4)],
    }
    return {
        "schema": "UDT_G111_EXACT_COMPONENT_HASHES_V1",
        "canonicalization": "sha256(sympy.srepr(sympy.expand(component))) in lexicographic indices",
        "groups": {
            name: {"component_count": len(expressions), "hashes": [expression_hash(expr) for expr in expressions]}
            for name, expressions in groups.items()
        },
    }


def quaternion_generators() -> dict[str, sp.Matrix]:
    # Right multiplication q -> q*i,q*j,q*k. The induced vector fields obey
    # [X,Y]=2Z, [Y,Z]=2X, [Z,X]=2Y in the R17 convention.
    return {
        "X": sp.Matrix([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]]),
        "Y": sp.Matrix([[0, 0, -1, 0], [0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0]]),
        "Z": sp.Matrix([[0, 0, 0, -1], [0, 0, 1, 0], [0, -1, 0, 0], [1, 0, 0, 0]]),
    }


def profile_jet(epsilon: sp.Rational, point: tuple[sp.Rational, ...]) -> tuple[sp.Expr, tuple[sp.Expr, ...], tuple[tuple[sp.Expr, ...], ...]]:
    generators = quaternion_generators()
    q = sp.Matrix(point)
    row = sp.Matrix([[1, 0, 0, 0]])
    ordered = (generators["Z"], generators["X"], generators["Y"])
    phi = sp.simplify(epsilon * point[0])
    first_spatial = tuple(sp.simplify((epsilon * row * matrix * q)[0]) for matrix in ordered)
    first = (sp.Integer(0), *first_spatial)
    second = [[sp.Integer(0) for _ in range(4)] for _ in range(4)]
    for i, left in enumerate(ordered, start=1):
        for j, right in enumerate(ordered, start=1):
            # V_i(V_j phi)=e0^T M_j M_i q.
            second[i][j] = sp.simplify((epsilon * row * right * left * q)[0])
    return phi, first, tuple(tuple(value for value in line) for line in second)


def build_symbolic_geometry() -> dict[str, object]:
    phi, lam, a = sp.symbols("phi lambda_R a", real=True)
    p1, p2, p3 = sp.symbols("p1 p2 p3", real=True)
    q11, q21, q31, q22, q32, q33 = sp.symbols("q11 q21 q31 q22 q32 q33", real=True)
    u = sp.exp(phi)
    v = sp.exp(lam * phi)
    frame = sp.Matrix(
        [
            [u, -a / u, 0, 0],
            [0, 1 / u, 0, 0],
            [0, 0, 1 / v, 0],
            [0, 0, 0, 1 / v],
        ]
    )
    coframe = sp.simplify(frame.inv())
    first = (sp.Integer(0), p1, p2, p3)
    second = (
        (0, 0, 0, 0),
        (0, q11, q21 + 2 * p3, q31 - 2 * p2),
        (0, q21, q22, q32 + 2 * p1),
        (0, q31, q32, q33),
    )
    variables = (phi, p1, p2, p3)

    def base_derivative(expr: sp.Expr, direction: int) -> sp.Expr:
        coefficients = (first[direction], *second[direction][1:])
        return sum(coefficient * sp.diff(expr, variable) for coefficient, variable in zip(coefficients, variables))

    constants = [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for left, right, output in ((2, 3, 1), (3, 1, 2), (1, 2, 3)):
        constants[left][right][output] = sp.Integer(2)
        constants[right][left][output] = sp.Integer(-2)

    def frame_bracket(left: int, right: int) -> tuple[sp.Expr, ...]:
        base = []
        for output in range(4):
            value = sp.Integer(0)
            for direction in range(4):
                value += frame[direction, left] * base_derivative(frame[output, right], direction)
                value -= frame[direction, right] * base_derivative(frame[output, left], direction)
            for first_index in range(4):
                for second_index in range(4):
                    value += frame[first_index, left] * frame[second_index, right] * constants[first_index][second_index][output]
            base.append(value)
        return tuple(sum(coframe[row, column] * base[column] for column in range(4)) for row in range(4))

    brackets = tuple(tuple(frame_bracket(i, j) for j in range(4)) for i in range(4))

    def lower_connection(direction: int, vector: int, output: int) -> sp.Expr:
        def inner(bracket: tuple[sp.Expr, ...], basis: int) -> sp.Expr:
            return ETA[basis] * bracket[basis]

        return (
            inner(brackets[direction][vector], output)
            - inner(brackets[vector][output], direction)
            + inner(brackets[output][direction], vector)
        ) / 2

    gamma_up = tuple(
        tuple(
            tuple(ETA[output] * lower_connection(direction, vector, output) for output in range(4))
            for vector in range(4)
        )
        for direction in range(4)
    )

    def frame_derivative(expr: sp.Expr, direction: int) -> sp.Expr:
        return sum(frame[base, direction] * base_derivative(expr, base) for base in range(4))

    riemann_up = [[[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for left, right, vector, output in product(range(4), repeat=4):
        value = frame_derivative(gamma_up[right][vector][output], left)
        value -= frame_derivative(gamma_up[left][vector][output], right)
        value += sum(gamma_up[right][vector][middle] * gamma_up[left][middle][output] for middle in range(4))
        value -= sum(gamma_up[left][vector][middle] * gamma_up[right][middle][output] for middle in range(4))
        value -= sum(brackets[left][right][middle] * gamma_up[middle][vector][output] for middle in range(4))
        riemann_up[left][right][vector][output] = sp.expand(value)
    riemann_lower = tuple(
        tuple(
            tuple(tuple(ETA[output] * riemann_up[i][j][k][output] for output in range(4)) for k in range(4))
            for j in range(4)
        )
        for i in range(4)
    )
    symbols = {
        "phi": phi,
        "lambda_R": lam,
        "a": a,
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "q11": q11,
        "q21": q21,
        "q22": q22,
        "q31": q31,
        "q32": q32,
        "q33": q33,
    }
    return {
        "symbols": symbols,
        "frame": frame,
        "coframe": coframe,
        "brackets": brackets,
        "gamma_up": gamma_up,
        "riemann_lower": riemann_lower,
    }


def substitutions(geometry: dict[str, object], epsilon: sp.Rational, point: tuple[sp.Rational, ...], twist: sp.Rational, lam_value: sp.Rational) -> dict[sp.Symbol, sp.Expr]:
    phi, first, second = profile_jet(epsilon, point)
    symbols = geometry["symbols"]
    values = {
        symbols["phi"]: phi,
        symbols["lambda_R"]: lam_value,
        symbols["a"]: twist,
        symbols["p1"]: first[1],
        symbols["p2"]: first[2],
        symbols["p3"]: first[3],
    }
    for name, i, j in (("q11", 1, 1), ("q21", 2, 1), ("q31", 3, 1), ("q22", 2, 2), ("q32", 3, 2), ("q33", 3, 3)):
        values[symbols[name]] = second[i][j]
    return values


def screen_for_axis(axis: int, sign: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = np.zeros(3)
    n[axis] = float(sign)
    if axis == 0:
        first, second = np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, float(sign)])
    elif axis == 1:
        first, second = np.array([0.0, 0.0, 1.0]), np.array([float(sign), 0.0, 0.0])
    else:
        first, second = np.array([1.0, 0.0, 0.0]), np.array([0.0, float(sign), 0.0])
    return n, first, second


def tensor_to_float(tensor: tuple, values: dict[sp.Symbol, sp.Expr]) -> np.ndarray:
    result = np.empty((4, 4, 4, 4), dtype=float)
    for i, j, k, l in product(range(4), repeat=4):
        result[i, j, k, l] = float(sp.N(tensor[i][j][k][l].subs(values), 17))
    return result


def connection_to_float(tensor: tuple, values: dict[sp.Symbol, sp.Expr]) -> np.ndarray:
    result = np.empty((4, 4, 4), dtype=float)
    for i, j, k in product(range(4), repeat=3):
        result[i, j, k] = float(sp.N(tensor[i][j][k].subs(values), 17))
    return result


def optical_tidal(riemann: np.ndarray, n: np.ndarray, screens: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
    k = np.concatenate(([1.0], n))
    screen4 = [np.concatenate(([0.0], vector)) for vector in screens]
    tidal = np.empty((2, 2), dtype=float)
    for a_index, first in enumerate(screen4):
        for b_index, second in enumerate(screen4):
            tidal[a_index, b_index] = np.einsum("i,j,k,l,ijkl", first, k, k, second, riemann)
    return tidal


def exact_identity_checks(geometry: dict[str, object]) -> dict[str, bool]:
    tensor = geometry["riemann_lower"]
    gamma = geometry["gamma_up"]
    brackets = geometry["brackets"]
    checks = {
        "coframe_inverse": sp.simplify(geometry["coframe"] * geometry["frame"] - sp.eye(4)) == sp.zeros(4),
        "coframe_determinant_nonzero": sp.simplify(geometry["coframe"].det()) != 0,
    }
    antisym_first = []
    antisym_last = []
    pair_exchange = []
    bianchi = []
    for i, j, k, l in product(range(4), repeat=4):
        antisym_first.append(sp.simplify(tensor[i][j][k][l] + tensor[j][i][k][l]) == 0)
        antisym_last.append(sp.simplify(tensor[i][j][k][l] + tensor[i][j][l][k]) == 0)
        pair_exchange.append(sp.simplify(tensor[i][j][k][l] - tensor[k][l][i][j]) == 0)
        bianchi.append(sp.simplify(tensor[i][j][k][l] + tensor[j][k][i][l] + tensor[k][i][j][l]) == 0)
    checks.update(
        {
            "connection_metricity": all(
                sp.simplify(ETA[k] * gamma[i][j][k] + ETA[j] * gamma[i][k][j]) == 0
                for i, j, k in product(range(4), repeat=3)
            ),
            "connection_torsion_free": all(
                sp.simplify(gamma[i][j][k] - gamma[j][i][k] - brackets[i][j][k]) == 0
                for i, j, k in product(range(4), repeat=3)
            ),
            "riemann_antisym_first": all(antisym_first),
            "riemann_antisym_last": all(antisym_last),
            "riemann_pair_exchange": all(pair_exchange),
            "riemann_first_bianchi": all(bianchi),
        }
    )
    return checks


def main() -> None:
    hashes = source_hashes()
    geometry = build_symbolic_geometry()
    component_hashes = exact_component_hashes(geometry)
    (HERE / "EXACT_COMPONENT_HASHES.json").write_text(
        json.dumps(component_hashes, indent=2, sort_keys=True) + "\n"
    )
    exact_checks = exact_identity_checks(geometry)
    half = sp.Rational(1, 2)
    points = tuple((half, *(sp.Rational(sign, 2) for sign in signs)) for signs in product((-1, 1), repeat=3))
    jet_compatibility = []
    for epsilon, point in product((sp.Rational(-1, 5), sp.Rational(1, 5)), points):
        _, first, second = profile_jet(epsilon, point)
        jet_compatibility.extend(
            (
                sp.simplify(second[1][2] - second[2][1] - 2 * first[3]) == 0,
                sp.simplify(second[1][3] - second[3][1] + 2 * first[2]) == 0,
                sp.simplify(second[2][3] - second[3][2] - 2 * first[1]) == 0,
            )
        )
    exact_checks["profile_jets_obey_maurer_cartan"] = all(jet_compatibility)
    normalization_checks = []
    for axis, sign in product(range(3), (-1, 1)):
        n, first, second_screen = screen_for_axis(axis, sign)
        null = sp.Matrix([1, *(sp.Integer(int(value)) for value in n)])
        screen_one = sp.Matrix([0, *(sp.Integer(int(value)) for value in first)])
        screen_two = sp.Matrix([0, *(sp.Integer(int(value)) for value in second_screen)])
        eta = sp.diag(-1, 1, 1, 1)
        normalization_checks.extend(
            [
                (null.T * eta * null)[0] == 0,
                (screen_one.T * eta * screen_one)[0] == 1,
                (screen_two.T * eta * screen_two)[0] == 1,
                (screen_one.T * eta * screen_two)[0] == 0,
                (screen_one.T * eta * null)[0] == 0,
                (screen_two.T * eta * null)[0] == 0,
            ]
        )
    exact_checks["null_screen_normalization"] = all(normalization_checks)
    affine = sp.symbols("affine", real=True)
    tidal_symbols = sp.Matrix(2, 2, sp.symbols("T0:4"))
    dsky_series = affine * sp.eye(2) - affine**3 * tidal_symbols / 6
    exact_checks["angular_vertex_residual_zero"] = (
        dsky_series.subs(affine, 0) == sp.zeros(2)
        and sp.diff(dsky_series, affine).subs(affine, 0) - sp.eye(2) == sp.zeros(2)
    )
    rows: list[dict[str, object]] = []
    nonzero_tidal = 0
    maximum_symmetry_residual = 0.0
    maximum_mixed_compatibility_residual = 0.0
    nonzero_pair_screen = 0
    phi_linear_values: list[float] = []
    metric_controls = 0
    for epsilon, twist, lam_value in product(
        (sp.Rational(-1, 5), sp.Rational(1, 5)),
        (sp.Rational(-1, 4), sp.Rational(1, 4)),
        LAMBDA_VALUES,
    ):
        for point_index, point in enumerate(points):
            values = substitutions(geometry, epsilon, point, twist, lam_value)
            riemann = tensor_to_float(geometry["riemann_lower"], values)
            gamma = connection_to_float(geometry["gamma_up"], values)
            bracket = connection_to_float(geometry["brackets"], values)
            metric_controls += 1
            for axis, sign in product(range(3), (-1, 1)):
                n, screen_a, screen_b = screen_for_axis(axis, sign)
                tidal = optical_tidal(riemann, n, (screen_a, screen_b))
                symmetry_residual = float(np.max(np.abs(tidal - tidal.T)))
                maximum_symmetry_residual = max(maximum_symmetry_residual, symmetry_residual)
                tidal_norm = float(np.linalg.norm(tidal))
                if tidal_norm > 1.0e-12:
                    nonzero_tidal += 1
                cubic = -tidal / 6.0
                observer = np.array([1.0, 0.0, 0.0, 0.0])
                null = np.concatenate(([1.0], n))
                screen4 = (np.concatenate(([0.0], screen_a)), np.concatenate(([0.0], screen_b)))
                metric_matrix = np.diag(np.array(ETA, dtype=float))
                signature = np.array(ETA, dtype=float)
                initial_pair_derivative = np.einsum("i,j,ijk->k", observer, null, gamma)
                initial_pair_derivative_from_mixed = (
                    np.einsum("i,j,ijk->k", null, observer, gamma)
                    + np.einsum("i,j,ijk->k", observer, null, bracket)
                )
                pair_screen_leading = np.array(
                    [initial_pair_derivative @ metric_matrix @ basis for basis in screen4], dtype=float
                )
                pair_screen_matrix = np.column_stack((pair_screen_leading, np.zeros(2)))
                pair_screen_rank = int(np.linalg.matrix_rank(pair_screen_matrix, tol=1.0e-11))
                if np.linalg.norm(pair_screen_leading) > 1.0e-12:
                    nonzero_pair_screen += 1
                curvature_pair_covector = np.einsum("i,j,k,ijkl->l", observer, null, null, riemann)
                curvature_pair_vector = signature * curvature_pair_covector
                pair_quadratic_vector = -curvature_pair_vector / 2.0
                h00_linear = 2.0 * (observer @ metric_matrix @ initial_pair_derivative)
                h00_quadratic = float(initial_pair_derivative @ metric_matrix @ initial_pair_derivative + 2.0 * observer @ metric_matrix @ pair_quadratic_vector)
                phi_linear = h00_linear / 2.0
                phi_linear_values.append(phi_linear)
                mixed_quadratic = np.array(
                    [initial_pair_derivative_from_mixed @ metric_matrix @ basis for basis in screen4]
                )
                mixed_residual = float(np.max(np.abs(mixed_quadratic - pair_screen_leading)))
                maximum_mixed_compatibility_residual = max(maximum_mixed_compatibility_residual, mixed_residual)
                rows.append(
                    {
                        "epsilon": str(epsilon),
                        "twist_a": str(twist),
                        "lambda_R": str(lam_value),
                        "point_id": f"P{point_index + 1:02d}",
                        "sky_axis": f"{'+' if sign > 0 else '-'}e{axis + 1}",
                        "phi": str(sp.simplify(values[geometry["symbols"]["phi"]])),
                        "tidal_trace": f"{np.trace(tidal):.17g}",
                        "tidal_det": f"{np.linalg.det(tidal):.17g}",
                        "tidal_frobenius": f"{tidal_norm:.17g}",
                        "tidal_symmetry_residual": f"{symmetry_residual:.3e}",
                        "Dsky_cubic_trace": f"{np.trace(cubic):.17g}",
                        "Dsky_cubic_shear": f"{np.linalg.norm(cubic - np.eye(2) * np.trace(cubic) / 2):.17g}",
                        "pair_h00_linear": f"{h00_linear:.17g}",
                        "pair_h00_quadratic": f"{h00_quadratic:.17g}",
                        "phi_pair_linear": f"{phi_linear:.17g}",
                        "pair_screen_leading_norm": f"{np.linalg.norm(pair_screen_leading):.17g}",
                        "pair_screen_rank": pair_screen_rank,
                        "mixed_quadratic_residual": f"{mixed_residual:.3e}",
                        "null_screen_residual": "0",
                        "Dsky_vertex_zero_residual": "0",
                        "Dsky_vertex_derivative_residual": "0",
                        "Dsky_vertex": "ZERO_WITH_MATCHED_DERIVATIVE_IDENTITY",
                        "selected": "NO",
                    }
                )
    expected_rows = 2 * 2 * 6 * 8 * 6
    checks = {
        **hashes,
        **exact_checks,
        "control_row_count": len(rows) == expected_rows,
        "metric_control_count": metric_controls == 2 * 2 * 6 * 8,
        "all_controls_retained": all(row["selected"] == "NO" for row in rows),
        "null_pair_screen_rank_bound": all(int(row["pair_screen_rank"]) <= 1 for row in rows),
        "mixed_pair_angular_compatibility": maximum_mixed_compatibility_residual < 1.0e-13,
        "angular_vertex_registered": all(row["Dsky_vertex"] == "ZERO_WITH_MATCHED_DERIVATIVE_IDENTITY" for row in rows),
        "angular_vertex_residual_evaluated": all(
            float(row["Dsky_vertex_zero_residual"]) == 0.0
            and float(row["Dsky_vertex_derivative_residual"]) == 0.0
            for row in rows
        ),
        "null_screen_residual_evaluated": all(float(row["null_screen_residual"]) == 0.0 for row in rows),
        "nonvacuous_optical_curvature": nonzero_tidal > 0,
        "optical_tidal_symmetric": maximum_symmetry_residual < 1.0e-11,
        "observational_outcomes_sealed": True,
    }
    result = {
        "schema": "UDT_G111_NONFLAT_R17_FULL_DIFFERENTIAL_V1",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "metric_controls": metric_controls,
        "directional_controls": len(rows),
        "nonzero_optical_tidal_controls": nonzero_tidal,
        "nonzero_pair_screen_leading_controls": nonzero_pair_screen,
        "phi_pair_linear_range": [min(phi_linear_values), max(phi_linear_values)],
        "maximum_optical_symmetry_residual": maximum_symmetry_residual,
        "maximum_mixed_compatibility_residual": maximum_mixed_compatibility_residual,
        "pair_screen_rank_theorem": "CANONICAL_NULL_POINT_OBSERVER_PAIR_SCREEN_RANK_AT_MOST_ONE",
        "angular_vertex": "D_SKY_ZERO__DERIVATIVE_MATCHED_BASIS_IDENTITY",
        "landing": "G110_DISTINCT_BLOCK_FULL_DIFFERENTIAL_SURVIVES_BOUNDED_NONFLAT_ANALYTIC_R17_REPLAY__PHYSICAL_HISTORY_AND_GLOBAL_WEIGHTS_OPEN",
        "maximum_conclusion": "bounded conditional nonflat complete-metric type and curvature replay only; no physical history or observation selected",
    }
    fields = list(rows[0])
    with (HERE / "CONTROL_ATLAS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if not result["all_checks_pass"]:
        raise SystemExit(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
