#!/usr/bin/env python3
"""Hostile semantic/evidence mutations for the bounded G307 result."""

from __future__ import annotations

import copy
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "DERIVATION_RESULT.json"
OUT = HERE / "CATCH_PROOF_RESULT.json"


def qmul(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    )


def qconj(q):
    return (q[0], -q[1], -q[2], -q[3])


def scale(c, vector):
    return tuple(c * value for value in vector)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def stereo(values):
    squared = sum(value * value for value in values)
    denominator = F(1) + squared
    return ((F(1) - squared) / denominator,) + tuple(
        2 * value / denominator for value in values
    )


def direct_mathematical_mutations():
    """Exercise corruptions of the theorem itself on one exact noncommuting witness."""
    q = stereo((F(1, 2), F(1, 3), F(1, 5)))
    q_bar = qconj(q)
    one, zero = F(1), F(0)
    u = (zero, one, zero, zero)
    e = (zero, zero, one, zero)
    f = (zero, zero, zero, one)
    v = qmul(u, q)
    w = qmul(e, q)
    z = qmul(f, q)
    u_left = qmul(v, q_bar)
    u_right = qmul(q_bar, v)
    assert u_left == u
    assert qmul(u_left, q) == v
    assert qmul(q, u_right) == v
    left_screen = qmul(u_left, w)
    right_screen = qmul(w, u_right)
    assert left_screen == z
    assert right_screen == scale(-one, z)

    records = []

    def caught(name, condition, expected):
        assert condition, name
        records.append({"case": name, "caught": True, "expected": expected})

    wrong_left = qmul(q_bar, v)
    caught("wrong_left_quaternion_order", qmul(wrong_left, q) != v, "left_reconstruction")

    wrong_right = qmul(v, q_bar)
    caught("wrong_right_quaternion_order", qmul(q, wrong_right) != v, "right_reconstruction")

    correct_route_closure = qmul(u_left, v)
    caught(
        "broken_route_plane_sign",
        correct_route_closure == scale(-one, q) and correct_route_closure != q,
        "route_complex_structure",
    )

    mutated_same_screen_turn = left_screen
    caught(
        "same_instead_of_opposite_screen_turn",
        mutated_same_screen_turn != right_screen,
        "opposite_transverse_turn",
    )

    radius = F(7, 3)
    correct_twist = dot(z, scale(one / radius, left_screen))
    mutated_twist = dot(z, left_screen)
    caught(
        "omitted_inverse_radius_factor",
        correct_twist == one / radius and mutated_twist != correct_twist,
        "radius_scaling",
    )

    alternative_tangent = qmul(e, q)
    caught(
        "point_only_false_uniqueness",
        alternative_tangent != v and dot(alternative_tangent, q) == zero,
        "point_does_not_supply_direction",
    )

    caught(
        "route_only_false_chirality_selection",
        qmul(u_left, q) == qmul(q, u_right)
        and qmul(u_left, v) == qmul(v, u_right)
        and left_screen != right_screen,
        "route_nonselection",
    )

    original_sign = dot(z, left_screen)
    reversed_sign = dot(scale(-one, z), left_screen)
    caught(
        "orientation_reversal_without_sign_reversal",
        original_sign == one and reversed_sign == -one,
        "orientation_relative_twist",
    )
    return records


def failure(value):
    if value["metric_and_kernel_changed"]:
        return "kernel_change"
    if value["directed_germ_member_count"] != 2:
        return "directed_count"
    if value["members_per_chirality"] != 1:
        return "per_chirality_uniqueness"
    if value["path_only_member_count"] != 2:
        return "path_nonselection"
    if value["signed_transverse_screen_member_count"] != 1:
        return "signed_screen_uniqueness"
    if value["screen_twist_signs"] != [-1, 1]:
        return "opposite_twist"
    if value["lawful_query_population_selected"]:
        return "query_population_promotion"
    if value["physical_member_selected"]:
        return "physical_member_promotion"
    required = {"mass", "scale", "physical_Xmax", "protected_work", "nonspherical_deformations"}
    if not required.issubset(value["omitted"]):
        return "scope_export"
    if value["production_assertions"] <= 0:
        return "vacuous_production"
    return None


def main():
    base = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert failure(base) is None
    mutations = (
        ("metric_only_selects_member", "physical_member_selected", True, "physical_member_promotion"),
        ("directed_germ_one_member", "directed_germ_member_count", 1, "directed_count"),
        ("chirality_not_unique", "members_per_chirality", 2, "per_chirality_uniqueness"),
        ("path_selects_chirality", "path_only_member_count", 1, "path_nonselection"),
        ("screen_leaves_two", "signed_transverse_screen_member_count", 2, "signed_screen_uniqueness"),
        ("same_twist_sign", "screen_twist_signs", [1, 1], "opposite_twist"),
        ("control_fiber_called_population", "lawful_query_population_selected", True, "query_population_promotion"),
        ("kernel_modified", "metric_and_kernel_changed", True, "kernel_change"),
        ("empty_assertions", "production_assertions", 0, "vacuous_production"),
    )
    semantic_records = []
    for name, key, replacement, expected in mutations:
        trial = copy.deepcopy(base)
        trial[key] = replacement
        actual = failure(trial)
        assert actual == expected, (name, actual, expected)
        semantic_records.append({"case": name, "caught": True, "expected": expected})

    for omitted in ("mass", "scale", "physical_Xmax", "protected_work", "nonspherical_deformations"):
        trial = copy.deepcopy(base)
        trial["omitted"].remove(omitted)
        actual = failure(trial)
        assert actual == "scope_export", (omitted, actual)
        semantic_records.append({"case": f"promote_{omitted}", "caught": True, "expected": "scope_export"})

    mathematical_records = direct_mathematical_mutations()
    records = mathematical_records + semantic_records

    result = {
        "status": "PASS",
        "baseline_valid": True,
        "hostile_cases": len(records),
        "direct_mathematical_mutations": len(mathematical_records),
        "semantic_result_mutations": len(semantic_records),
        "records": records,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
