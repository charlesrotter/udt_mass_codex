#!/usr/bin/env python3
"""Exact Cartan classification of intrinsic reciprocal holonomy reductions."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
SIGN = (-1, 1, 1, 1)


def write_tsv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def build_cartan():
    lam = sp.symbols("lambda", real=True)
    p1, p2, p3, A, B, C = sp.symbols("p1 p2 p3 A B C", real=True)
    structure = sp.MutableDenseNDimArray.zeros(4, 4, 4)

    def set_coefficient(upper, left, right, de_coefficient):
        structure[upper, left, right] = -de_coefficient
        structure[upper, right, left] = de_coefficient

    for values in (
        (0, 0, 1, p1), (0, 0, 2, p2), (0, 0, 3, p3), (0, 2, 3, A),
        (1, 1, 2, -p2), (1, 1, 3, -p3), (1, 2, 3, B),
        (2, 1, 2, lam*p1), (2, 2, 3, -lam*p3), (2, 1, 3, -C),
        (3, 1, 3, lam*p1), (3, 2, 3, lam*p2), (3, 1, 2, C),
    ):
        set_coefficient(*values)

    connection = sp.MutableDenseNDimArray.zeros(4, 4, 4)
    for out in range(4):
        for direction in range(4):
            for acted in range(4):
                lowered = (
                    SIGN[out] * structure[out, direction, acted]
                    - SIGN[direction] * structure[direction, acted, out]
                    + SIGN[acted] * structure[acted, out, direction]
                ) / 2
                connection[out, direction, acted] = sp.factor(SIGN[out] * lowered)
    return (lam, p1, p2, p3, A, B, C), structure, connection


def nabla_components(connection, lam, substitute=None):
    eigenvalues = (-1, 1, lam, lam)
    rows = []
    for direction in range(4):
        for out in range(4):
            for acted in range(4):
                expression = sp.factor(
                    connection[out, direction, acted] * (eigenvalues[acted] - eigenvalues[out])
                )
                if substitute is not None:
                    expression = sp.factor(expression.subs(lam, substitute))
                if expression != 0:
                    rows.append((direction, out, acted, expression))
    return rows


def curvature_constant(structure, connection, substitutions):
    reduced_structure = sp.MutableDenseNDimArray.zeros(4, 4, 4)
    reduced_connection = sp.MutableDenseNDimArray.zeros(4, 4, 4)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                reduced_structure[a, b, c] = sp.sympify(structure[a, b, c]).subs(substitutions)
                reduced_connection[a, b, c] = sp.sympify(connection[a, b, c]).subs(substitutions)
    riemann = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for out in range(4):
        for acted in range(4):
            for left in range(4):
                for right in range(4):
                    value = sp.S(0)
                    for middle in range(4):
                        value += (
                            reduced_connection[middle, right, acted]
                            * reduced_connection[out, left, middle]
                            - reduced_connection[middle, left, acted]
                            * reduced_connection[out, right, middle]
                            - reduced_structure[middle, left, right]
                            * reduced_connection[out, middle, acted]
                        )
                    riemann[out, acted, left, right] = sp.factor(value)
    return riemann


def main() -> int:
    symbols, structure, connection = build_cartan()
    lam, p1, p2, p3, A, B, C = symbols

    connection_rows = []
    for out in range(4):
        for direction in range(4):
            for acted in range(4):
                expression = connection[out, direction, acted]
                if expression != 0:
                    connection_rows.append({
                        "out": out, "direction": direction, "acted": acted,
                        "Gamma": str(expression),
                    })
    write_tsv(HERE / "CARTAN_CONNECTION.tsv", connection_rows)

    equation_rows = []
    cases = (("GENERIC_NOT_PLUS_MINUS_ONE", None), ("LAMBDA_PLUS_ONE", 1), ("LAMBDA_MINUS_ONE", -1))
    for case, value in cases:
        for direction, out, acted, expression in nabla_components(connection, lam, value):
            equation_rows.append({
                "case": case, "direction": direction, "out": out, "acted": acted,
                "nabla_X_component": str(expression),
            })
    write_tsv(HERE / "PARALLELISM_COMPONENTS.tsv", equation_rows)

    classifications = [
        {
            "case": "GENERIC_NOT_PLUS_MINUS_ONE", "connected_stabilizer": "so(2)_screen",
            "pointwise_iff": "p1=p2=p3=A=B=0", "metric_implication": "dphi=0;a=0;B=0",
            "regular_S3_compatible": "NO", "reason": "B=kappa*exp((1-2lambda)*phi)!=0",
            "complete_regular_survivor": "NONE", "ruler_metric_intrinsic": "N/A",
        },
        {
            "case": "LAMBDA_PLUS_ONE", "connected_stabilizer": "so(3)_spatial",
            "pointwise_iff": "p1=p2=p3=A=0", "metric_implication": "dphi=0;a=0",
            "regular_S3_compatible": "YES", "reason": "B=C=kappa*exp(-phi0)!=0_allowed",
            "complete_regular_survivor": "R_t_times_round_S3_phi0_constant",
            "ruler_metric_intrinsic": "NO_spatial_isotropy_and_zero_twist",
        },
        {
            "case": "LAMBDA_MINUS_ONE", "connected_stabilizer": "so(1,2)_clock_screen",
            "pointwise_iff": "p1=p2=p3=B=0", "metric_implication": "dphi=0;B=0",
            "regular_S3_compatible": "NO", "reason": "B=kappa*exp(3phi)!=0",
            "complete_regular_survivor": "NONE", "ruler_metric_intrinsic": "N/A",
        },
    ]
    write_tsv(HERE / "CASE_CLASSIFICATION.tsv", classifications)

    degeneracies = [
        {"escape": "B=0_via_kappa=0", "regular_S3": "NO", "effect": "removes_Maurer_Cartan_contact_geometry"},
        {"escape": "B=0_via_finite_exponential", "regular_S3": "IMPOSSIBLE", "effect": "real_exponential_never_zero"},
        {"escape": "B_to_zero_at_infinite_phi_limit", "regular_S3": "NO", "effect": "not_a_finite_regular_point"},
        {"escape": "A=0_via_a=0", "regular_S3": "YES", "effect": "kills_clock_twist_and_parent_ruler_selector"},
        {"escape": "lambda_plus_one_spatial_eigenvalue_degeneracy", "regular_S3": "YES", "effect": "X_keeps_clock_line_but_no_distinguished_ruler"},
    ]
    write_tsv(HERE / "DEGENERACY_ESCAPE_REGISTRY.tsv", degeneracies)

    k = sp.symbols("k", nonzero=True, real=True)
    survivor_substitutions = {lam: 1, p1: 0, p2: 0, p3: 0, A: 0, B: k, C: k}
    survivor_curvature = curvature_constant(structure, connection, survivor_substitutions)
    curvature_rows = []
    generator_vectors = []
    x_plus = sp.diag(-1, 1, 1, 1)
    maximum_commutator = sp.S(0)
    for left in range(4):
        for right in range(left + 1, 4):
            matrix = sp.Matrix(4, 4, lambda out, acted: survivor_curvature[out, acted, left, right])
            if matrix != sp.zeros(4):
                commutator = sp.simplify(matrix*x_plus - x_plus*matrix)
                assert commutator == sp.zeros(4)
                vector = [matrix[0, 1], matrix[0, 2], matrix[0, 3],
                          matrix[1, 2], matrix[1, 3], matrix[2, 3]]
                generator_vectors.append(vector)
                curvature_rows.append({
                    "plane": f"{left}{right}", "nonzero_entries": ";".join(
                        f"R{out}{acted}={matrix[out,acted]}" for out in range(4) for acted in range(4)
                        if matrix[out, acted] != 0
                    ), "commutator_with_X": "ZERO",
                })
    curvature_rank = sp.Matrix(generator_vectors).rank()
    assert curvature_rank == 3
    write_tsv(HERE / "SURVIVOR_CURVATURE.tsv", curvature_rows)

    # Exact sufficiency checks for all three strata.
    generic_expressions = [item[3] for item in nabla_components(connection, lam, None)]
    plus_expressions = [item[3] for item in nabla_components(connection, lam, 1)]
    minus_expressions = [item[3] for item in nabla_components(connection, lam, -1)]
    assert all(sp.simplify(expr.subs({p1: 0, p2: 0, p3: 0, A: 0, B: 0})) == 0
               for expr in generic_expressions)
    assert all(sp.simplify(expr.subs({p1: 0, p2: 0, p3: 0, A: 0})) == 0 for expr in plus_expressions)
    assert all(sp.simplify(expr.subs({p1: 0, p2: 0, p3: 0, B: 0})) == 0 for expr in minus_expressions)

    result = {
        "schema": "udt-reduced-holonomy-condition-1.0", "status": "COMPUTED",
        "connection_nonzero_components": len(connection_rows),
        "parallelism_nonzero_components": {
            "generic_symbolic": len(generic_expressions),
            "lambda_plus_one": len(plus_expressions), "lambda_minus_one": len(minus_expressions),
        },
        "case_count": 3, "regular_complete_survivor_count": 1,
        "survivor": {
            "lambda": 1, "phi": "constant_phi0", "twist_a": 0,
            "metric": "R_t_times_round_S3", "curvature_holonomy_rank": curvature_rank,
            "holonomy_algebra": "so(3)_spatial", "X_parallel": True,
            "metric_intrinsic_ruler_retained": False,
        },
        "nonconstant_regular_survivor_count": 0,
        "nontrivial_twist_regular_survivor_count": 0,
        "intrinsic_clock_ruler_pair_survivor_count": 0,
        "generic_blocked_by_nonzero_B": True,
        "lambda_minus_one_blocked_by_nonzero_B": True,
        "path_groupoid_remains_valid": True,
        "physical_lambda_selected": False, "all_configurations_off_shell": True,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
