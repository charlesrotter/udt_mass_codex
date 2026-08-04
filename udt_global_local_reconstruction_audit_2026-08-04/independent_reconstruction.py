#!/usr/bin/env python3
"""Independent Fraction/integer reconstruction; imports no production module or SymPy."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


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


def rank(rows: list[list[int | Fraction]]) -> int:
    work = [[Fraction(value) for value in row] for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for col in range(len(work[0])):
        pivot = next((r for r in range(pivot_row, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            factor = work[row][col]
            if factor:
                work[row] = [a - factor * b for a, b in zip(work[row], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def cover_checks() -> dict[str, object]:
    p_a = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    c_a = [[0, 1, 0, -1, 0, 0], [0, 0, 1, 0, -1, 0]]
    g_a = [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]]
    p_b = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    c_b = [[0, 1, -1, 0, 0, 0], [0, 0, 0, 1, -1, 0]]
    g_b = [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1]]
    refine = [[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]]
    zero_2x4 = [[0] * 4 for _ in range(2)]
    eye4 = [[int(i == j) for j in range(4)] for i in range(4)]
    r = [[1, 2, 0, 0], [0, 1, 1, 1]]
    rg = matmul(r, g_a)
    combined = [c_a[i] + [0, 0] for i in range(2)] + [
        [-value for value in rg[i]] + [int(i == j) for j in range(2)] for i in range(2)
    ]
    return {
        "cover_a_constraint_rank": rank(c_a),
        "cover_a_descent_dimension": 6 - rank(c_a),
        "cover_a_restriction_rank": rank(p_a),
        "cover_a_constraints_annihilate_restrictions": matmul(c_a, p_a) == zero_2x4,
        "cover_a_glue_after_restrict_identity": matmul(g_a, p_a) == eye4,
        "cover_b_constraint_rank": rank(c_b),
        "cover_b_descent_dimension": 6 - rank(c_b),
        "cover_b_restriction_rank": rank(p_b),
        "cover_b_constraints_annihilate_restrictions": matmul(c_b, p_b) == zero_2x4,
        "cover_b_glue_after_restrict_identity": matmul(g_b, p_b) == eye4,
        "refinement_matches_global_restriction": matmul(refine, p_a) == p_b,
        "refinement_reconstructs_same_global_data": matmul(g_b, matmul(refine, p_a)) == eye4,
        "descent_plus_readout_graph_rank": rank(combined),
        "descent_plus_readout_graph_nullity": 8 - rank(combined),
        "global_configuration_dimension": 4,
    }


def determinant(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def monodromy_checks() -> dict[str, object]:
    graph_ranks = {}
    graph_rows = {}
    for name, matrix in MONODROMIES.items():
        rows = [[-matrix[i][j] for j in range(2)] + [int(i == j) for j in range(2)] for i in range(2)]
        graph_ranks[name] = rank(rows)
        graph_rows[name] = rows
    distinct = 0
    dims = []
    for left, right in itertools.combinations(MONODROMIES, 2):
        # Graphs of maps are equal iff the maps are equal.
        distinct += MONODROMIES[left] != MONODROMIES[right]
        difference = [
            [MONODROMIES[left][i][j] - MONODROMIES[right][i][j] for j in range(2)]
            for i in range(2)
        ]
        dims.append(2 - rank(difference))
    histogram = {str(dim): dims.count(dim) for dim in sorted(set(dims))}
    return {
        "graph_constraint_ranks": graph_ranks,
        "graph_dimensions": {name: 4 - value for name, value in graph_ranks.items()},
        "distinct_graph_pairs": distinct,
        "pair_count": len(dims),
        "pairwise_intersection_dimension_histogram": histogram,
        "pairs_with_nonzero_ambiguous_endpoint_line": sum(dim > 0 for dim in dims),
        "zero_endpoint_pair_belongs_to_all_graphs": True,
        "all_matrices_are_GL2Z": all(abs(determinant(matrix)) == 1 for matrix in MONODROMIES.values()),
    }


def correspondence_checks() -> dict[str, object]:
    witnesses = list(itertools.product((-1, 0, 1, 2), repeat=2))
    closed = {
        "A_reconstruction_identity": lambda a, b: 0,
        "A_product": lambda a, b: a + b - a * b,
        "A_quadratic": lambda a, b: a + b - a * a - b * b,
    }
    sets = {name: [[a, b] for a, b in witnesses if fn(a, b) == 0] for name, fn in closed.items()}
    return {
        "witness_count": len(witnesses),
        "witness_survivor_counts": {name: len(value) for name, value in sets.items()},
        "witness_survivor_sets": sets,
        "all_three_are_swap_invariant": all(fn(a, b) == fn(b, a) for fn in closed.values() for a, b in witnesses),
        "same_readout_and_frame_symmetry_allow_inequivalent_nontrivial_relations": sets["A_product"] != sets["A_quadratic"],
    }


def main() -> None:
    checks = {
        "schema": "udt.global_local_reconstruction.independent.v1",
        "cover_reconstruction": cover_checks(),
        "completion_fibers": monodromy_checks(),
        "admissibility_correspondence": correspondence_checks(),
    }
    print(json.dumps(checks, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
