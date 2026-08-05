#!/usr/bin/env python3
"""Exact primary controls for the complete-coframe extension/solvability audit."""

from __future__ import annotations

import ast
import argparse
import csv
import json
from pathlib import Path

import sympy as sp


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
MONODROMY = ROOT / "udt_completion_parameterized_local_fiber_audit_2026-08-01" / "MONODROMY_LOCAL_FIBERS.tsv"
OUT = PKG / "RESULT.json"


def flat_extension(h: sp.Matrix, sigma: sp.Matrix) -> list[sp.Expr]:
    return [h[0, 0], h[0, 1], h[1, 1], *list(sigma)]


def transform_extension(
    h: sp.Matrix, sigma: sp.Matrix, p: sp.Matrix, q: sp.Matrix
) -> tuple[sp.Matrix, sp.Matrix]:
    return q.inv().T * h * q.inv(), q * sigma * p.inv()


def extension_descent_control() -> dict:
    p01 = sp.Matrix([[1, 1], [0, 1]])
    p12 = sp.Matrix([[1, 0], [1, 1]])
    q01 = sp.Matrix([[2, 1], [1, 1]])
    q12 = sp.Matrix([[1, 1], [0, 1]])
    p02 = p12 * p01
    q02 = q12 * q01

    h00, h01, h11 = sp.symbols("h00 h01 h11")
    s00, s01, s10, s11 = sp.symbols("s00 s01 s10 s11")
    variables = [h00, h01, h11, s00, s01, s10, s11]
    h0 = sp.Matrix([[h00, h01], [h01, h11]])
    sigma0 = sp.Matrix([[s00, s01], [s10, s11]])

    h1, sigma1 = transform_extension(h0, sigma0, p01, q01)
    h2_direct, sigma2_direct = transform_extension(h0, sigma0, p02, q02)
    h2_via1, sigma2_via1 = transform_extension(h1, sigma1, p12, q12)

    cocycle_h = sp.simplify(h2_direct - h2_via1) == sp.zeros(2)
    cocycle_sigma = sp.simplify(sigma2_direct - sigma2_via1) == sp.zeros(2)

    local_vector = sp.Matrix(
        flat_extension(h0, sigma0)
        + flat_extension(h1, sigma1)
        + flat_extension(h2_direct, sigma2_direct)
    )
    descent_map = local_vector.jacobian(variables)

    h_example = sp.Matrix([[2, sp.Rational(1, 2)], [sp.Rational(1, 2), 3]])
    sigma_example = sp.Matrix([[1, 2], [-1, 3]])
    positive_checks = []
    for p, q in [(sp.eye(2), sp.eye(2)), (p01, q01), (p02, q02)]:
        h_chart, _ = transform_extension(h_example, sigma_example, p, q)
        positive_checks.append(bool(h_chart[0, 0] > 0 and h_chart.det() > 0))

    return {
        "chart_count": 3,
        "seed_extension_dimension": 7,
        "local_component_count": 21,
        "descent_map_rank": int(descent_map.rank()),
        "surviving_extension_dimension": int(descent_map.rank()),
        "cocycle_h_exact": cocycle_h,
        "cocycle_sigma_exact": cocycle_sigma,
        "positive_metric_preserved_all_charts": all(positive_checks),
        "selection_rank_from_descent": 0,
    }


def gamma_key(a: int, b: int, c: int) -> tuple[tuple[int, int, int] | None, int]:
    """Return the antisymmetric first-pair connection key and its sign."""
    if a == b:
        return None, 0
    if a < b:
        return (a, b, c), 1
    return (b, a, c), -1


def cartan_reconstruction_control() -> dict:
    unknowns = [(a, b, c) for a in range(4) for b in range(a + 1, 4) for c in range(4)]
    index = {key: i for i, key in enumerate(unknowns)}
    signature = [-1, 1, 1, 1]
    rows: list[list[int]] = []

    # T^a_bc=0 is linear in the metric-compatible connection Gamma_ab_c=-Gamma_ba_c.
    # Overall sign conventions for C^a_bc change only the right-hand side, not this map.
    for a in range(4):
        for b in range(4):
            for c in range(b + 1, 4):
                row = [0] * len(unknowns)
                for q, r, coefficient in [(c, b, 1), (b, c, -1)]:
                    key, antisymmetry_sign = gamma_key(a, q, r)
                    if key is not None:
                        row[index[key]] += signature[a] * coefficient * antisymmetry_sign
                rows.append(row)

    matrix = sp.Matrix(rows)
    rank = int(matrix.rank())
    return {
        "dimension": 4,
        "connection_unknowns": len(unknowns),
        "torsion_equations": len(rows),
        "coefficient_rank": rank,
        "coefficient_nullity": len(unknowns) - rank,
        "arbitrary_anholonomy_rhs_solvable": rank == len(rows) == len(unknowns),
        "coframe_constraints_from_reconstruction": 0 if rank == len(rows) else len(rows) - rank,
    }


def coordinate_integrability_control() -> dict:
    # Start from theta=(dx,dy), then apply the position-dependent orthogonal frame rotation R(x).
    # R preserves the metric, while d(R theta)=dR wedge theta is generally nonzero.
    x = sp.symbols("x", real=True)
    rotation = sp.Matrix([[sp.cos(x), sp.sin(x)], [-sp.sin(x), sp.cos(x)]])
    metric_preserved = sp.simplify(rotation.T * rotation - sp.eye(2)) == sp.zeros(2)
    # Coefficients of dx wedge dy in d(theta'_1), d(theta'_2).
    exterior_coefficients = [sp.diff(rotation[0, 1], x), sp.diff(rotation[1, 1], x)]
    at_zero = [sp.simplify(value.subs(x, 0)) for value in exterior_coefficients]
    return {
        "metric_preserved_exact": metric_preserved,
        "input_coordinate_coframe_closed": True,
        "rotated_exterior_coefficients_at_x0": [int(value) for value in at_zero],
        "rotated_coframe_not_closed": any(value != 0 for value in at_zero),
        "coordinate_integrability_is_frame_gauge_invariant": False,
    }


def monodromy_control() -> dict:
    rows = []
    with MONODROMY.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            matrix = sp.Matrix(ast.literal_eval(row["matrix"]))
            graph_matrix = sp.Matrix.hstack(-matrix, sp.eye(2))
            fixed_rank = int((matrix - sp.eye(2)).rank())
            fixed_dimension = 2 - fixed_rank
            expected = int(row["conditional_fixed_parallel_dimension"])
            rows.append(
                {
                    "monodromy_id": row["monodromy_id"],
                    "endpoint_graph_rank": int(graph_matrix.rank()),
                    "endpoint_graph_dimension": 4 - int(graph_matrix.rank()),
                    "fixed_parallel_rank": fixed_rank,
                    "fixed_parallel_dimension": fixed_dimension,
                    "matches_frozen_conditional_dimension": fixed_dimension == expected,
                }
            )
    histogram: dict[str, int] = {}
    for row in rows:
        key = str(row["fixed_parallel_dimension"])
        histogram[key] = histogram.get(key, 0) + 1
    return {
        "matrix_count": len(rows),
        "all_endpoint_graphs_dimension_two": all(r["endpoint_graph_dimension"] == 2 for r in rows),
        "all_frozen_fixed_dimensions_match": all(r["matches_frozen_conditional_dimension"] for r in rows),
        "fixed_parallel_dimension_histogram": histogram,
        "rows": rows,
    }


def operation_control() -> dict:
    rows = [
        ("E01", "KINEMATIC_DESCENT_NONSELECTION", False, False, False, False),
        ("E02", "DERIVED_EXISTENCE_NONSELECTION", False, False, False, False),
        ("E03", "CONDITIONAL_STRONG_WITNESS_NOT_REQUIRED", True, False, True, False),
        ("E04", "CONDITIONAL_EXTRA_INTEGRABILITY_NOT_FRAME_NATURAL", True, False, True, False),
        ("E05", "DERIVED_RECONSTRUCTION_NONSELECTION", False, False, False, False),
        ("E06", "DERIVED_IDENTITY_NONSELECTION", False, False, False, False),
        ("E07", "CONDITIONAL_PARALLELISM_SELECTOR", True, False, True, False),
        ("E08", "CIRCULAR_PARENT_LAW_REQUIRED", True, True, False, False),
        ("E09", "CIRCULAR_PARENT_BULK_AND_BOUNDARY_REQUIRED", True, True, False, False),
        ("E10", "OPEN_OUTSIDE_FIXED_RANK_TILE", None, False, False, False),
    ]
    records = []
    for operation_id, status, nonidentity, parent_law, extra_premise, native_pass in rows:
        records.append(
            {
                "operation_id": operation_id,
                "status": status,
                "nonidentity_if_imposed": nonidentity,
                "requires_parent_law": parent_law,
                "requires_extra_premise": extra_premise,
                "native_complete_return_pass": native_pass,
            }
        )
    return {
        "operation_count": len(records),
        "native_complete_return_passes": sum(r["native_complete_return_pass"] for r in records),
        "circular_parent_law_operations": sum(r["requires_parent_law"] for r in records),
        "conditional_extra_premise_operations": sum(r["requires_extra_premise"] for r in records),
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true", help="replay to stdout without changing RESULT.json")
    args = parser.parse_args()
    result = {
        "schema": "udt.complete_coframe_extension_solvability.result.v1",
        "sympy_version": sp.__version__,
        "outcome": (
            "DERIVED_EXTENSION_EXISTENCE_AND_CARTAN_RECONSTRUCTION_ARE_NONSELECTING__"
            "CONDITIONAL_HOLONOMY_OBSTRUCTIONS_REQUIRE_EXTRA_PARALLELISM__"
            "NATIVE_INTERIOR_RETURN_REMAINS_OPEN"
        ),
        "extension_descent": extension_descent_control(),
        "cartan_reconstruction": cartan_reconstruction_control(),
        "coordinate_integrability": coordinate_integrability_control(),
        "monodromy": monodromy_control(),
        "operations": operation_control(),
    }
    if not args.no_write:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
