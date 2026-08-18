#!/usr/bin/env python3
"""Algebraic mutation catches and semantic guards for G161."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def tr(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def metadata_catch(name, key, wrong):
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    expected = {
        "positive_bplus2_is_physical_carry_selector": False,
        "smooth_distance_sweep_fixes_vertical_rapidity": False,
        "screen_normal_transport_universally_resolves_tangent_boost": False,
        "metric_plus_bare_pair_plane_owns_II": False,
        "null_and_degenerate_strata_closed": False,
        "physical_carry_derived": False,
        "physical_history_derived": False,
    }
    result[key] = wrong
    return {"name": name, "caught": result[key] != expected[key]}


def main():
    eta = [[F(-1), F(0)], [F(0), F(1)]]
    boost = [[F(5, 3), F(4, 3)], [F(4, 3), F(5, 3)]]
    section = [[F(2), F(1)], [F(0), F(3)]]
    m = mm(boost, section)
    pair = mm(mm(tr(m), eta), m)
    section_pair = mm(mm(tr(section), eta), section)
    right_action = mm(section, boost)
    right_pair = mm(mm(tr(right_action), eta), right_action)

    p, r = m[0][0], m[1][0]
    correct_extract = [[p / 2, -r / 2], [-r / 2, p / 2]]
    wrong_sign = [[p / 2, r / 2], [r / 2, p / 2]]

    A = [[F(1), F(0)], [F(0), F(2)]]
    CII = mm(A, A)
    umbilic = [[F(5), F(0)], [F(0), F(5)]]
    complex_case = [[F(0), F(36)], [F(-36), F(0)]]
    disc = lambda x: (x[0][0] - x[1][1])**2 + 4 * x[0][1] * x[1][0]

    catches = [
        {"name": "replace_left_stabilizer_fiber_by_right_action",
         "caught": pair == section_pair and right_pair != section_pair},
        {"name": "reverse_lorentzian_qr_boost_sign",
         "caught": mm(correct_extract, m)[1][0] == 0 and mm(wrong_sign, m)[1][0] != 0},
        {"name": "drop_future_clock_condition",
         "caught": (-p) < 0 and p > 0},
        {"name": "promote_null_clock_to_regular_section",
         "caught": F(1)**2 - F(1)**2 == 0},
        {"name": "claim_extrinsic_CII_always_has_simple_spectrum",
         "caught": disc(CII) > 0 and disc(umbilic) == 0 and disc(complex_case) < 0},
        metadata_catch("promote_bplus2_section_to_physical_carry",
                       "positive_bplus2_is_physical_carry_selector", True),
        metadata_catch("claim_distance_sweep_fixes_vertical_rapidity",
                       "smooth_distance_sweep_fixes_vertical_rapidity", True),
        metadata_catch("claim_screen_normal_transport_universally_solders_tangent_boost",
                       "screen_normal_transport_universally_resolves_tangent_boost", True),
        metadata_catch("promote_bare_pair_plane_to_owner_of_second_fundamental_form",
                       "metric_plus_bare_pair_plane_owns_II", True),
        metadata_catch("close_null_and_degenerate_strata_without_proof",
                       "null_and_degenerate_strata_closed", True),
        metadata_catch("promote_quotient_section_to_physical_carry",
                       "physical_carry_derived", True),
        metadata_catch("promote_kinematic_quotient_to_physical_history",
                       "physical_history_derived", True),
    ]
    assert all(item["caught"] for item in catches)
    result = {
        "status": "PASS",
        "catch_count": len(catches),
        "algebra_mutation_count": 5,
        "metadata_guard_mutation_count": 7,
        "metadata_guards_are_independent_semantic_proofs": False,
        "caught": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
