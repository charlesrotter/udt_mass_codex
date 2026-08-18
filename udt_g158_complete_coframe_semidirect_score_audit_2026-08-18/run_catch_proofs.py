#!/usr/bin/env python3
"""Mutation catches for G158 composition order, coupling, and ownership guards."""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def block(b, q, s):
    qs = mm(q, s)
    return [
        [b[0][0], b[0][1], F(0), F(0)],
        [b[1][0], b[1][1], F(0), F(0)],
        [qs[0][0], qs[0][1], q[0][0], q[0][1]],
        [qs[1][0], qs[1][1], q[1][0], q[1][1]],
    ]


B1 = [[F(2), F(1)], [F(0), F(3)]]
B2 = [[F(5), F(-2)], [F(0), F(7)]]
Q1 = [[F(3), F(2)], [F(0), F(4)]]
Q2 = [[F(2), F(-1)], [F(0), F(5)]]
S1 = [[F(1), F(2)], [F(3), F(4)]]
S2 = [[F(-2), F(1)], [F(5), F(-3)]]
DIRECT = mm(block(B2, Q2, S2), block(B1, Q1, S1))


def candidate(b, q, s):
    return block(b, q, s)


def caught_formula(name, proposed):
    return {"name": name, "caught": proposed != DIRECT}


def validate_metadata(result):
    assert result["coordinate_count"] == 10
    assert result["query_blocks_are_group_coordinates"] is False
    assert result["fixed_ratios_derived"] is False
    assert result["physical_score_derived"] is False
    assert result["physical_cross_query_carry_derived"] is False


def caught_metadata(name, key, value):
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    result[key] = value
    try:
        validate_metadata(result)
    except AssertionError:
        return {"name": name, "caught": True}
    return {"name": name, "caught": False}


def main():
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    validate_metadata(result)
    correct_b = mm(B2, B1)
    correct_q = mm(Q2, Q1)
    correct_s = add(S1, mm(mm(inv2(Q1), S2), B1))

    catches = [
        caught_formula("reverse_base_order", candidate(mm(B1, B2), correct_q, correct_s)),
        caught_formula("reverse_screen_order", candidate(correct_b, mm(Q1, Q2), correct_s)),
        caught_formula("omit_Q1_inverse_from_mixing", candidate(correct_b, correct_q, add(S1, mm(S2, B1)))),
        caught_formula("omit_B1_from_mixing", candidate(correct_b, correct_q, add(S1, mm(inv2(Q1), S2)))),
        caught_formula("make_mixing_direct_additive", candidate(correct_b, correct_q, add(S1, S2))),
        caught_metadata("promote_YZ_to_group_coordinates", "query_blocks_are_group_coordinates", True),
        caught_metadata("derive_fixed_ratios", "fixed_ratios_derived", True),
        caught_metadata("promote_score_to_physical", "physical_score_derived", True),
        caught_metadata("promote_cross_query_carry", "physical_cross_query_carry_derived", True),
        caught_metadata("inflate_coordinate_count_with_query_blocks", "coordinate_count", 18),
    ]
    assert all(item["caught"] for item in catches)
    output = {
        "status": "PASS",
        "catch_count": len(catches),
        "algebra_mutation_count": 5,
        "metadata_guard_mutation_count": 5,
        "metadata_guards_are_independent_semantic_proofs": False,
        "caught": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
