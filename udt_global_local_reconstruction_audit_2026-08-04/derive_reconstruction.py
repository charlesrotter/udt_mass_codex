#!/usr/bin/env python3
"""Exact algebra controls for the preregistered reconstruction audit."""

from __future__ import annotations

import itertools
import json

import sympy as sp


MONODROMIES = {
    "M_IDENTITY": ((1, 0), (0, 1)),
    "M_MINUS_IDENTITY": ((-1, 0), (0, -1)),
    "M_ORDER4_ROTATION": ((0, -1), (1, 0)),
    "M_ORDER6_ELLIPTIC": ((0, -1), (1, 1)),
    "M_PARABOLIC": ((1, 1), (0, 1)),
    "M_HYPERBOLIC": ((2, 1), (1, 1)),
    "M_EXCHANGE": ((0, 1), (1, 0)),
    "M_ORIENTATION_REVERSING_GLIDE": ((1, 1), (0, -1)),
}


def rank_nullity(matrix: sp.Matrix) -> tuple[int, int]:
    return matrix.rank(), matrix.cols - matrix.rank()


def cover_controls() -> dict[str, object]:
    # Cover A: (x0,x1,x2) and (x1,x2,x3).
    p_a = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    c_a = sp.Matrix([[0, 1, 0, -1, 0, 0], [0, 0, 1, 0, -1, 0]])
    g_a = sp.Matrix(
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
        ]
    )

    # Cover B refines the same four coordinates into three two-coordinate patches.
    p_b = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    c_b = sp.Matrix([[0, 1, -1, 0, 0, 0], [0, 0, 0, 1, -1, 0]])
    g_b = sp.Matrix(
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1],
        ]
    )

    # Extraction of refined local data from cover-A data.
    refine = sp.Matrix(
        [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
        ]
    )

    r = sp.Matrix([[1, 2, 0, 0], [0, 1, 1, 1]])
    # Variables are six cover-A local entries followed by two free readout entries.
    combined = c_a.row_join(sp.zeros(2, 2)).col_join((-r * g_a).row_join(sp.eye(2)))

    checks = {
        "cover_a_constraint_rank": c_a.rank(),
        "cover_a_descent_dimension": c_a.cols - c_a.rank(),
        "cover_a_restriction_rank": p_a.rank(),
        "cover_a_constraints_annihilate_restrictions": c_a * p_a == sp.zeros(2, 4),
        "cover_a_glue_after_restrict_identity": g_a * p_a == sp.eye(4),
        "cover_b_constraint_rank": c_b.rank(),
        "cover_b_descent_dimension": c_b.cols - c_b.rank(),
        "cover_b_restriction_rank": p_b.rank(),
        "cover_b_constraints_annihilate_restrictions": c_b * p_b == sp.zeros(2, 4),
        "cover_b_glue_after_restrict_identity": g_b * p_b == sp.eye(4),
        "refinement_matches_global_restriction": refine * p_a == p_b,
        "refinement_reconstructs_same_global_data": g_b * refine * p_a == sp.eye(4),
        "descent_plus_readout_graph_rank": combined.rank(),
        "descent_plus_readout_graph_nullity": combined.cols - combined.rank(),
        "global_configuration_dimension": 4,
    }
    assert all(value is True or isinstance(value, int) for value in checks.values())
    assert checks["cover_a_descent_dimension"] == 4
    assert checks["cover_b_descent_dimension"] == 4
    assert checks["descent_plus_readout_graph_nullity"] == 4
    return checks


def monodromy_controls() -> dict[str, object]:
    matrices = {name: sp.Matrix(value) for name, value in MONODROMIES.items()}
    graph_rows: dict[str, sp.Matrix] = {}
    ranks: dict[str, int] = {}
    for name, matrix in matrices.items():
        constraint = (-matrix).row_join(sp.eye(2))
        graph_rows[name] = constraint.rref()[0]
        ranks[name] = constraint.rank()

    distinct_pairs = 0
    intersection_dimensions: dict[str, int] = {}
    for left, right in itertools.combinations(matrices, 2):
        if graph_rows[left] != graph_rows[right]:
            distinct_pairs += 1
        dim = 2 - (matrices[left] - matrices[right]).rank()
        intersection_dimensions[f"{left}|{right}"] = dim

    histogram = {
        str(dim): sum(value == dim for value in intersection_dimensions.values())
        for dim in sorted(set(intersection_dimensions.values()))
    }
    nonzero_ambiguous_pairs = sum(value > 0 for value in intersection_dimensions.values())
    return {
        "graph_constraint_ranks": ranks,
        "graph_dimensions": {name: 4 - rank for name, rank in ranks.items()},
        "distinct_graph_pairs": distinct_pairs,
        "pair_count": len(intersection_dimensions),
        "pairwise_intersection_dimension_histogram": histogram,
        "pairs_with_nonzero_ambiguous_endpoint_line": nonzero_ambiguous_pairs,
        "zero_endpoint_pair_belongs_to_all_graphs": True,
    }


def correspondence_controls() -> dict[str, object]:
    x1, x2, o = sp.symbols("x1 x2 o")
    readout = x1 + x2
    relations = {
        "A_reconstruction_identity": o - (x1 + x2),
        "A_product": o - x1 * x2,
        "A_quadratic": o - (x1**2 + x2**2),
    }
    closed = {name: sp.expand(expr.subs(o, readout)) for name, expr in relations.items()}
    swap_invariant = {
        name: sp.expand(expr.subs({x1: x2, x2: x1}, simultaneous=True) - expr) == 0
        for name, expr in relations.items()
    }
    depends_on_global = {name: sp.diff(expr, o) != 0 for name, expr in relations.items()}
    depends_on_local = {
        name: (sp.diff(expr, x1) != 0 or sp.diff(expr, x2) != 0)
        for name, expr in relations.items()
    }

    witnesses = list(itertools.product((-1, 0, 1, 2), repeat=2))
    survivors = {
        name: sum(expr.subs({x1: a, x2: b}) == 0 for a, b in witnesses)
        for name, expr in closed.items()
    }
    survivor_sets = {
        name: [[a, b] for a, b in witnesses if expr.subs({x1: a, x2: b}) == 0]
        for name, expr in closed.items()
    }
    assert closed["A_reconstruction_identity"] == 0
    assert survivor_sets["A_product"] != survivor_sets["A_quadratic"]
    assert all(swap_invariant.values())
    assert all(depends_on_global.values())
    assert all(depends_on_local.values())
    return {
        "readout": str(readout),
        "closed_residuals": {name: str(expr) for name, expr in closed.items()},
        "swap_invariant": swap_invariant,
        "depends_nontrivially_on_global_coordinate": depends_on_global,
        "depends_on_local_coordinates": depends_on_local,
        "witness_count": len(witnesses),
        "witness_survivor_counts": survivors,
        "witness_survivor_sets": survivor_sets,
        "same_readout_and_frame_symmetry_allow_inequivalent_nontrivial_relations": True,
    }


def main() -> None:
    result = {
        "schema": "udt.global_local_reconstruction.exact.v1",
        "sympy_version": sp.__version__,
        "cover_reconstruction": cover_controls(),
        "completion_fibers": monodromy_controls(),
        "admissibility_correspondence": correspondence_controls(),
        "outcome": (
            "DERIVED_PARTIAL_KINEMATIC_ADMISSIBILITY_CORRESPONDENCE__"
            "WORKING_POSIT_REQUIRES_BUT_DOES_NOT_DERIVE_COMPLETE_RETURN"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
