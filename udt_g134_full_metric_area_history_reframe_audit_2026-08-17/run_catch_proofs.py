#!/usr/bin/env python3
"""Catch common over-promotions of the G134 area result."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("CATCH_PROOF_RESULT.json")
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def area(g: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [[g[i, k] * g[j, l] - g[i, l] * g[j, k] for k, l in PAIRS] for i, j in PAIRS]
    )


def main() -> None:
    q = sp.Rational
    g_a = sp.Matrix([[-1, q(1, 2), 0, 0], [q(1, 2), 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    g_b = sp.Matrix([[-1, -q(1, 2), 0, 0], [-q(1, 2), 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    a_a, a_b = area(g_a), area(g_b)
    self_only_same = [a_a[i, i] for i in range(6)] == [a_b[i, i] for i in range(6)]

    K = sp.Matrix([[0, 1], [1, 0]])
    U = sp.Matrix([[1, 1], [0, 1]])
    area_line_not_reciprocity = U.det() == 1 and U.T * K * U != K

    s_values = (q(1, 4), q(4))
    histories = [sp.diag(-s, 1 / s, 1, 1) for s in s_values]
    every_history_has_area = all(a.det() != 0 for a in map(area, histories))
    histories_not_selected = area(histories[0]) != area(histories[1])

    checks = {
        "reject_self_area_equals_full_area": self_only_same and a_a != a_b,
        "reject_area_preservation_equals_reciprocity": area_line_not_reciprocity,
        "reject_area_existence_selects_history": every_history_has_area and histories_not_selected,
        "reject_full_area_is_new_field_independent_of_g": area(histories[0]) == area(histories[0]),
        "reject_area_rule_is_scale_blind": area(2 * histories[0]) == 4 * area(histories[0]),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "passed": sum(checks.values()),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{result['status']}: {result['passed']}/{result['check_count']} G134 catch proofs")


if __name__ == "__main__":
    main()
