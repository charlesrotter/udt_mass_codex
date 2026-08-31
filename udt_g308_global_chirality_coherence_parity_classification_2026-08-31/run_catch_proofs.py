#!/usr/bin/env python3
"""Hostile mathematical and ownership controls for G308."""

from __future__ import annotations

import copy
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "DERIVATION_RESULT.json"
OUT = HERE / "CATCH_PROOF_RESULT.json"
Z = F(0)
O = F(1)


def diagonal(values):
    return tuple(
        tuple(values[i] if i == j else Z for j in range(4))
        for i in range(4)
    )


def matmul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4))
        for i in range(4)
    )


def matvec(a, v):
    return tuple(sum(a[i][j] * v[j] for j in range(4)) for i in range(4))


def transpose(a):
    return tuple(tuple(a[j][i] for j in range(4)) for i in range(4))


def matscale(c, a):
    return tuple(tuple(c * value for value in row) for row in a)


def matadd(a, b):
    return tuple(tuple(a[i][j] + b[i][j] for j in range(4)) for i in range(4))


def determinant(a):
    # Sufficient exact elimination for the fixed witnesses below.
    work = [list(row) for row in a]
    result = O
    for column in range(4):
        pivot = next((row for row in range(column, 4) if work[row][column] != Z), None)
        if pivot is None:
            return Z
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result *= pivot_value
        for j in range(column, 4):
            work[column][j] /= pivot_value
        for row in range(column + 1, 4):
            factor = work[row][column]
            for j in range(column, 4):
                work[row][j] -= factor * work[column][j]
    return result


def pfaffian(a):
    return a[0][1] * a[2][3] - a[0][2] * a[1][3] + a[0][3] * a[1][2]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def direct_mathematical_mutations():
    left = (
        (Z, -O, Z, Z),
        (O, Z, Z, Z),
        (Z, Z, Z, -O),
        (Z, Z, O, Z),
    )
    right = (
        (Z, -O, Z, Z),
        (O, Z, Z, Z),
        (Z, Z, Z, O),
        (Z, Z, -O, Z),
    )
    mirror = diagonal((O, O, O, -O))
    identity = diagonal((O, O, O, O))
    p = (O, Z, Z, Z)
    v = (Z, O, Z, Z)
    w = (Z, Z, O, Z)
    z = (Z, Z, Z, O)
    q = (F(1, 2), F(1, 2), F(1, 2), F(1, 2))
    records = []

    def caught(name, condition, expected):
        assert condition, name
        records.append({"case": name, "caught": True, "expected": expected})

    caught(
        "false_one_sided_global_failure",
        dot(matvec(left, q), matvec(left, q)) == O
        and dot(matvec(right, q), matvec(right, q)) == O,
        "both_global_fields",
    )
    caught(
        "orientation_preserving_chirality_exchange",
        pfaffian(left) == pfaffian(matmul(matmul(identity, left), transpose(identity)))
        and pfaffian(left) != pfaffian(right),
        "SO4_chirality_preservation",
    )
    midpoint = matscale(F(1, 2), matadd(left, right))
    caught(
        "smooth_local_chirality_switch",
        determinant(midpoint) == Z,
        "switch_leaves_regular_complex_stratum",
    )
    caught(
        "pair_reversal_changes_chirality",
        pfaffian(matscale(-O, left)) == pfaffian(left)
        and pfaffian(matscale(-O, right)) == pfaffian(right),
        "reversal_preserves_chirality",
    )
    caught(
        "screen_preserving_parity_exchange",
        matmul(matmul(mirror, left), mirror) == right
        and matvec(mirror, p) == p
        and matvec(mirror, v) == v
        and matvec(mirror, w) == w
        and matvec(mirror, z) == (Z, Z, Z, -O),
        "exchange_reverses_transverse_orientation",
    )
    radius = F(7, 3)
    spatial = (Z, Z, F(3, 5), F(4, 5))
    reflected_spatial = matvec(mirror, spatial)
    dt = F(5, 7)
    before = -dt * dt + radius * radius * dot(spatial, spatial)
    after = -dt * dt + radius * radius * dot(reflected_spatial, reflected_spatial)
    caught(
        "causal_cone_difference",
        before == after,
        "metric_and_causal_form_preserved",
    )
    expanding_radius = F(2)
    expanding_radius_rate = F(1)
    spacetime_time_acceleration = expanding_radius_rate / expanding_radius
    caught(
        "spatial_Hopf_fiber_called_spacetime_geodesic",
        spacetime_time_acceleration == F(1, 2) and spacetime_time_acceleration != Z,
        "nonzero_expanding_warp_time_acceleration",
    )
    caught(
        "full_O4_fails_to_exchange",
        determinant(mirror) == -O and matmul(matmul(mirror, left), mirror) == right,
        "orientation_reversing_exchange",
    )
    return records


def failure(result):
    if result["metric_and_kernel_changed"]:
        return "kernel_change"
    if result["metric_or_causal_cone_changed"]:
        return "causal_change"
    if not result["both_global_smooth_nowhere_zero"]:
        return "global_field_failure"
    if result["SO4_exchanges_chirality"]:
        return "SO4_false_exchange"
    if not result["full_O4_exchanges_chirality"]:
        return "O4_exchange_missing"
    if result["pair_reversal_changes_chirality"]:
        return "reversal_mistyped"
    if result["connected_regular_carry_allows_local_chirality_switch"]:
        return "switch_mistyped"
    if result["spatial_hopf_fibers_automatically_spacetime_geodesic"]:
        return "spacetime_geodesic_overclaim"
    if result["physical_member_selected"]:
        return "population_promotion"
    required = {"action", "dynamics", "mass", "scale_selection", "physical_Xmax", "protected_work"}
    if not required.issubset(result["omitted"]):
        return "scope_export"
    return None


def main():
    baseline = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert failure(baseline) is None
    semantic_mutations = (
        ("kernel_modified", "metric_and_kernel_changed", True, "kernel_change"),
        ("causal_cone_changed", "metric_or_causal_cone_changed", True, "causal_change"),
        ("one_global_field_fails", "both_global_smooth_nowhere_zero", False, "global_field_failure"),
        ("SO4_selects_exchange", "SO4_exchanges_chirality", True, "SO4_false_exchange"),
        ("pair_reversal_switches_sector", "pair_reversal_changes_chirality", True, "reversal_mistyped"),
        ("local_chirality_switch_allowed", "connected_regular_carry_allows_local_chirality_switch", True, "switch_mistyped"),
        ("spatial_fibers_called_spacetime_geodesics", "spatial_hopf_fibers_automatically_spacetime_geodesic", True, "spacetime_geodesic_overclaim"),
        ("coherence_called_physical_population", "physical_member_selected", True, "population_promotion"),
    )
    semantic_records = []
    for name, key, replacement, expected in semantic_mutations:
        trial = copy.deepcopy(baseline)
        trial[key] = replacement
        actual = failure(trial)
        assert actual == expected, (name, actual, expected)
        semantic_records.append({"case": name, "caught": True, "expected": expected})

    for omitted in ("action", "dynamics", "mass", "scale_selection", "physical_Xmax", "protected_work"):
        trial = copy.deepcopy(baseline)
        trial["omitted"].remove(omitted)
        assert failure(trial) == "scope_export"
        semantic_records.append({
            "case": f"promote_{omitted}",
            "caught": True,
            "expected": "scope_export",
        })

    mathematical_records = direct_mathematical_mutations()
    records = mathematical_records + semantic_records
    result = {
        "status": "PASS",
        "baseline_valid": True,
        "direct_mathematical_mutations": len(mathematical_records),
        "semantic_result_mutations": len(semantic_records),
        "hostile_cases": len(records),
        "records": records,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
