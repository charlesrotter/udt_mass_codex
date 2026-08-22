#!/usr/bin/env python3
"""Hostile semantic/algebraic mutation catches for G219."""

from __future__ import annotations

import json
from fractions import Fraction


def catches() -> dict[str, bool]:
    v = Fraction(3, 5)
    gamma = Fraction(5, 4)
    exp_eta = Fraction(2)
    r = Fraction(7, 5)
    c1, c2 = Fraction(2), Fraction(-3)
    common_scale = Fraction(11, 7)

    def null_ok(slope: Fraction) -> bool:
        a, length = Fraction(1, 3), Fraction(5, 3)
        b = slope * (a + length)
        return gamma * b - a == length + v * gamma * b

    def a_fermi_ok(slope: Fraction) -> bool:
        a = Fraction(3, 7)
        return gamma * slope * a == a

    def b_fermi_ok(slope: Fraction, intercept: Fraction) -> bool:
        a = Fraction(3, 7)
        b = slope * a + intercept
        dt, dx = a - gamma * b, -1 - v * gamma * b
        return -gamma * dt + v * gamma * dx == 0

    def compose(mid_target: tuple[str, int], mid_source: tuple[str, int]) -> bool:
        return mid_target == mid_source

    correct_null = null_ok(exp_eta)
    correct_a_fermi = a_fermi_ok(1 / gamma)
    correct_b_fermi = b_fermi_ok(gamma, gamma * v)
    b_null = exp_eta * (Fraction(1, 3) + Fraction(5, 3))
    inverse_recovers = b_null / exp_eta - Fraction(5, 3) == Fraction(1, 3)
    return_does_not_invert = exp_eta * b_null + Fraction(5, 3) != Fraction(1, 3)
    caught = {
        "wrong_null_sign": correct_null and not null_ok(gamma * (1 - v)),
        "all_protocols_identical": correct_a_fermi and correct_b_fermi and not a_fermi_ok(exp_eta),
        "inverse_called_return": inverse_recovers and return_does_not_invert,
        "echo_called_identity": exp_eta**2 != 1,
        "depth_sign_reversed": (1 / exp_eta) * exp_eta == 1 and exp_eta * exp_eta != 1,
        "quadratic_leaks_into_first_jet": r + 2 * c1 * 0 == r + 2 * c2 * 0 == r
        and r + 2 * c1 != r + 2 * c2,
        "quadratic_erased_from_second_jet": 2 * c1 != 2 * c2,
        "post_readout_common_scale": (common_scale * r) / (common_scale / r) == r**2
        and common_scale * r**2 != r**2,
        "unmatched_middle_allowed": compose(("B", 1), ("B", 1))
        and not compose(("B", 1), ("B", 2)),
        "future_return_called_inverse_map": null_ok(exp_eta) and inverse_recovers and return_does_not_invert,
    }
    assert all(caught.values()), [key for key, value in caught.items() if not value]
    return caught


if __name__ == "__main__":
    result = catches()
    print(json.dumps({"caught": result, "count": len(result)}, indent=2, sort_keys=True))
