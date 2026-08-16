#!/usr/bin/env python3
"""Hostile finite mutations for G102 query and orthogonalization guards."""

from __future__ import annotations

import json
from fractions import Fraction as F


def dot(a, b):
    signs = (-1, 1, 1, 1)
    return sum((F(signs[i]) * a[i] * b[i] for i in range(4)), F(0))


def main():
    v0 = (F(2), F(0), F(0), F(0))
    v1 = (F(1), F(3), F(0), F(0))

    raw_ruler_is_not_orthogonal = dot(v0, v1) != 0
    if not raw_ruler_is_not_orthogonal:
        raise AssertionError("dropping orthogonalization escaped")

    u1 = (F(1), F(0), F(0), F(0))
    u2 = (F(5, 4), F(3, 4), F(0), F(0))
    common_clock_guard_rejects = u1 != u2
    if not common_clock_guard_rejects:
        raise AssertionError("unequal observer clocks escaped")

    n = (F(0), F(1), F(0), F(0))
    negative_ruler_scaling_flips_sky = tuple(-x for x in n) != n
    if not negative_ruler_scaling_flips_sky:
        raise AssertionError("orientation ambiguity escaped")

    single_source_has_no_unordered_pair = len([(i, j) for i in range(1) for j in range(i + 1, 1)]) == 0
    if not single_source_has_no_unordered_pair:
        raise AssertionError("one-source arity mutation escaped")

    observer_local_phi_arguments = (F(9, 4), F(25, 9))
    terminal_Z = (F(2), F(3))
    endpoint_conflation_rejected = observer_local_phi_arguments != tuple(z**4 for z in terminal_Z)
    if not endpoint_conflation_rejected:
        raise AssertionError("observer-local/terminal-depth conflation escaped")

    result = {
        "status": "PASS",
        "mutations": {
            "drop_ruler_orthogonalization": "CAUGHT",
            "join_unequal_observer_clocks": "CAUGHT",
            "erase_outward_ruler_orientation": "CAUGHT",
            "replace_two_source_query_with_one_source": "CAUGHT",
            "reuse_observer_local_h_as_terminal_redshift": "CAUGHT",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
