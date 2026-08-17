#!/usr/bin/env python3
"""Exact symbolic and rational finite-graph derivation for G138."""

from __future__ import annotations

import json
from collections import deque

import sympy as sp


def mobius(x: sp.Expr, y: sp.Expr) -> sp.Expr:
    return sp.simplify((x + y) / (1 + x * y))


def exp_simplify(expr: sp.Expr) -> sp.Expr:
    return sp.simplify(expr.rewrite(sp.exp))


def tree_path(tree: dict[int, list[int]], start: int, end: int) -> list[int]:
    queue = deque([start])
    parent = {start: None}
    while queue:
        node = queue.popleft()
        if node == end:
            break
        for nxt in tree[node]:
            if nxt not in parent:
                parent[nxt] = node
                queue.append(nxt)
    if end not in parent:
        raise AssertionError("tree path absent")
    result = []
    node = end
    while node is not None:
        result.append(node)
        node = parent[node]
    return list(reversed(result))


def path_sum(path: list[int], depth: dict[tuple[int, int], sp.Rational]) -> sp.Rational:
    return sp.simplify(sum((depth[(a, b)] for a, b in zip(path, path[1:])), sp.Rational(0)))


def main() -> None:
    checks = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    X, scale = sp.symbols("X_max scale", real=True, positive=True)
    a, b, c, ref1, ref2 = sp.symbols("a b c ref1 ref2", real=True)
    pab, pbc, pac, pca = b - a, c - b, c - a, a - c
    xab, xbc, xac, xca = map(sp.tanh, (pab, pbc, pac, pca))

    check("triangle_additive", sp.simplify(pab + pbc - pac) == 0)
    check("triangle_cycle", sp.simplify(pab + pbc + pca) == 0)
    check("q_cycle_product", sp.simplify(sp.exp(-2 * pab) * sp.exp(-2 * pbc) * sp.exp(-2 * pca)) == 1)
    check("mobius_pair_composition", exp_simplify(mobius(xab, xbc) - xac) == 0)
    check("mobius_cycle_zero", exp_simplify(mobius(mobius(xab, xbc), xca)) == 0)

    uA, uB, uC = sp.tanh(a), sp.tanh(b), sp.tanh(c)
    pair_from_root = (uB - uA) / (1 - uA * uB)
    check("pair_from_root_chart", exp_simplify(pair_from_root - xab) == 0)
    uA_from_B = (uA - uB) / (1 - uA * uB)
    uC_from_B = (uC - uB) / (1 - uC * uB)
    pair_in_B_chart = (uC_from_B - uA_from_B) / (1 - uA_from_B * uC_from_B)
    check("root_change_formula", exp_simplify(uA_from_B - sp.tanh(a - b)) == 0)
    check("pair_invariant_under_root_change", exp_simplify(pair_in_B_chart - sp.tanh(c - a)) == 0)
    check("root_is_zero", sp.simplify((uB - uB) / (1 - uB**2)) == 0)
    uA_ref1 = sp.tanh(a - ref1)
    reference_shift = sp.tanh(ref1 - ref2)
    uA_ref2_from_action = mobius(reference_shift, uA_ref1)
    check("arbitrary_reference_gauge_action", exp_simplify(uA_ref2_from_action - sp.tanh(a - ref2)) == 0)

    dim_pair = X * pair_from_root
    scaled_pair = scale * X * pair_from_root
    check("common_Xmax_dimensional_join", exp_simplify(dim_pair - X * xab) == 0)
    check("Xmax_rescaling_leaves_normalized_pair", sp.simplify(scaled_pair / (scale * X) - dim_pair / X) == 0)

    potentials = [
        sp.Rational(2, 3),
        sp.Rational(-1, 5),
        sp.Rational(4, 7),
        sp.Rational(9, 11),
        sp.Rational(-5, 13),
    ]
    tree_edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
    chords = [(0, 2), (2, 4), (0, 4)]
    edges = tree_edges + chords
    depth: dict[tuple[int, int], sp.Rational] = {}
    for i, j in edges:
        value = sp.simplify(potentials[j] - potentials[i])
        depth[(i, j)] = value
        depth[(j, i)] = -value

    tree = {i: [] for i in range(len(potentials))}
    for i, j in tree_edges:
        tree[i].append(j)
        tree[j].append(i)

    reconstructed = [path_sum(tree_path(tree, 0, i), depth) for i in range(len(potentials))]
    expected = [sp.simplify(value - potentials[0]) for value in potentials]
    check("tree_reconstruction", reconstructed == expected)
    check("potential_gauge_offset", all(sp.simplify(reconstructed[i] - reconstructed[j] - (potentials[i] - potentials[j])) == 0 for i in range(5) for j in range(5)))

    residuals = []
    for i, j in chords:
        residuals.append(sp.simplify(depth[(i, j)] + path_sum(tree_path(tree, j, i), depth)))
    check("all_fundamental_cycles_close", residuals == [0, 0, 0])
    check("direct_equals_tree_path", all(sp.simplify(depth[(i, j)] - path_sum(tree_path(tree, i, j), depth)) == 0 for i, j in chords))

    incidence = sp.zeros(len(potentials), len(edges))
    for col, (i, j) in enumerate(edges):
        incidence[i, col] = -1
        incidence[j, col] = 1
    check("incidence_rank_n_minus_one", incidence.rank() == len(potentials) - 1)
    cycle_rank = len(edges) - incidence.rank()
    check("cycle_rank_m_minus_n_plus_one", cycle_rank == len(edges) - len(potentials) + 1 == 3)

    corrupt = dict(depth)
    corrupt[(0, 2)] += sp.Rational(1, 11)
    corrupt[(2, 0)] = -corrupt[(0, 2)]
    holonomy = sp.simplify(corrupt[(0, 2)] + path_sum(tree_path(tree, 2, 0), corrupt))
    check("nonzero_holonomy_detected", holonomy == sp.Rational(1, 11))
    check("nonzero_holonomy_blocks_endpoint_potential", corrupt[(0, 2)] != reconstructed[2] - reconstructed[0])
    alternate_path = sp.simplify(corrupt[(0, 2)] + corrupt[(2, 1)])
    check("distinct_path_values_differ_by_holonomy", sp.simplify(alternate_path - corrupt[(0, 1)]) == holonomy)
    check("bounded_holonomy_nonzero", sp.tanh(holonomy) != 0)

    result = {
        "classification": (
            "ENDPOINT_DESCENT_IFF_ALL_MATCHED_CYCLE_RESIDUALS_VANISH__"
            "ALL_REFERENCE_DEPTH_GAUGES_FORM_A_MOBIUS_TORSOR__"
            "OBSERVER_ROOTED_CHARTS_ARE_MOBIUS_RELATED_WITH_NO_COORDINATE_ROOT_SELECTED__"
            "NONZERO_CYCLE_RESIDUAL_IS_PATH_HOLONOMY_ONLY_WHEN_DISTINCT_ROUTES_REMAIN_DISTINCT_ARROWS__"
            "CURRENT_FOUNDATIONS_DO_NOT_SELECT_BETWEEN_THESE_GLOBAL_RELATION_TYPES__"
            "XMAX_VALUE_PAIR_REALIZATION_HISTORY_AND_GLOBAL_COMPLETION_OPEN"
        ),
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "finite_graph": {
            "vertices": len(potentials),
            "edges": len(edges),
            "cycle_rank": cycle_rank,
            "fundamental_residuals": [str(value) for value in residuals],
            "corrupt_cycle_holonomy": str(holonomy),
        },
        "exact": {
            "pair_chart": "xi_AB=(u_B-u_A)/(1-u_A*u_B)",
            "root_change": "u_A^(R)=(u_A^(O)-u_R^(O))/(1-u_A^(O)*u_R^(O))",
            "cycle_tests": "sum(phi)=0 iff product(q)=1 iff MobiusSum(xi)=0",
        },
        "open": [
            "physical identification of direct and composite branches",
            "network values pair realizations and complete history",
            "X_max numerical value and dimensional owner",
            "singular null and global completion",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
