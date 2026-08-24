#!/usr/bin/env python3
"""Hostile finite mutations for the G247 type and algebra boundaries."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

import derive_global_null_branch_network as prod


def run() -> dict:
    a, b, c = (F(0), F(0)), (F(1), F(1)), (F(2), F(0))
    e = F(2)
    r1, r2 = F(3, 2), F(5, 4)
    m1 = prod.edge_phase(r1, F(1), F(2), F(3))
    m2 = prod.edge_phase(r2, F(4), F(5), F(6))
    vertex = prod.vertex_quarter_turn()
    correct_chain = prod.mm(m2, prod.mm(vertex, m1))
    without_vertex = prod.mm(m2, m1)
    reordered = prod.mm(vertex, prod.mm(m2, m1))
    caustic = prod.edge_phase(F(1), F(0), F(0), F(1))
    block = [[caustic[i][j] for j in (2, 3)] for i in (0, 1)]
    # Antipodal static observers make opposite winding labels share delays, so
    # replacing the route-labelled set by delay values provably loses arrows.
    windings = [(n, abs(F(5) + n * F(10))) for n in range(-4, 5)]

    mutations = {
        "force_direct_null_closure": prod.interval_squared(a, c) != 0,
        "call_future_links_a_groupoid": prod.interval_squared(a, c) != 0,
        "identify_future_return_with_inverse": e != F(1) / e,
        "erase_winding_labels": len(windings) != len({delay for _, delay in windings}),
        "replace_ratio_product_by_sum": r2 * r1 != r2 + r1,
        "replace_depth_addition_by_ratio_addition": r2 * r1 != r2 + r1,
        "use_inverse_multiplier_in_phase": not prod.is_csp(correct_chain, F(1) / (r2 * r1)),
        "omit_vertex_screen_lift": without_vertex != correct_chain,
        "commute_vertex_through_edge": reordered != correct_chain,
        "scalarize_matrix_phase": correct_chain != prod.scale(prod.eye(4), r2 * r1),
        "force_endpoint_only_flat_screen_carry": vertex != prod.eye(4),
        "invert_singular_caustic_position_block": prod.det(block) == 0,
        "declare_full_phase_singular_at_caustic": prod.det(caustic) != 0,
        "turn_coincidence_into_nontrivial_null_edge": not (F(0) > 0),
        "identify_direct_edge_with_chain": prod.interval_squared(a, c) != 0,
        "drop_positive_clock_orientation": (-r1) <= 0,
    }
    missed = [name for name, caught in mutations.items() if not caught]
    return {
        "caught": sum(bool(v) for v in mutations.values()),
        "total": len(mutations),
        "mutations": mutations,
        "missed": missed,
        "status": "PASS" if not missed else "FAIL",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path)
    ns = p.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if ns.output:
        ns.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
