#!/usr/bin/env python3
"""Exact mutation catches and semantic guards for G160."""

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


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def pull(h, dh, m, dm):
    hbar = mm(mm(tr(m), h), m)
    dhbar = add(add(mm(mm(tr(dm), h), m), mm(mm(tr(m), dh), m)), mm(mm(tr(m), h), dm))
    return hbar, dhbar


def kappa_rate(h, dh):
    det = h[0][0] * h[1][1] - h[0][1] ** 2
    ddet = dh[0][0] * h[1][1] + h[0][0] * dh[1][1] - 2 * h[0][1] * dh[0][1]
    return ddet / (4 * det)


def metadata_catch(name, key, wrong):
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    expected = {
        "intrinsic_connection_split_gauge_independent": False,
        "physical_carry_derived": False,
        "physical_history_derived": False,
        "physical_lambda_owned": False,
    }
    result[key] = wrong
    return {"name": name, "caught": result[key] != expected[key]}


def main():
    h = [[F(-4), F(1)], [F(1), F(2)]]
    dh = [[F(1), F(2)], [F(2), F(3)]]
    m = [[F(2), F(1)], [F(1), F(1)]]
    dm = [[F(1), F(-1)], [F(2), F(1)]]
    hbar, dhbar = pull(h, dh, m, dm)
    _, frozen = pull(h, dh, m, [[F(0), F(0)], [F(0), F(0)]])
    omit_left = add(mm(mm(tr(m), dh), m), mm(mm(tr(m), h), dm))

    mba = [[F(1), F(1)], [F(0), F(1)]]
    mcb = [[F(2), F(0)], [F(1), F(1)]]
    dmba = [[F(0), F(1)], [F(0), F(0)]]
    dmcb = [[F(1), F(0)], [F(0), F(-1)]]
    mca = mm(mcb, mba)
    dmca = add(mm(dmcb, mba), mm(mcb, dmba))
    kba, kcb, kca = mm(dmba, inv2(mba)), mm(dmcb, inv2(mcb)), mm(dmca, inv2(mca))
    correct_rate = add(kcb, mm(mm(mcb, kba), inv2(mcb)))
    wrong_rate = add(kba, mm(mm(mba, kcb), inv2(mba)))

    pa, dpa = [[F(2), F(0)], [F(0), F(1)]], [[F(1), F(0)], [F(0), F(0)]]
    expected_h, expected_dh = pull(hbar, dhbar, pa, dpa)
    _, frozen_source_gauge = pull(hbar, dhbar, pa, [[F(0), F(0)], [F(0), F(0)]])

    base_k, carried_k = kappa_rate(h, dh), kappa_rate(hbar, dhbar)
    k = mm(dm, inv2(m))

    mlower = [[F(1), F(0)], [F(1, 2), F(1)]]
    z = [[F(0), F(0)], [F(0), F(0)]]
    hf, hs = [[F(-1), F(0)], [F(0), F(1)]], [[F(-4), F(0)], [F(0), F(1)]]
    hfb, _ = pull(hf, z, mlower, z)
    hsb, _ = pull(hs, z, mlower, z)
    clock_ratio_f = (-hfb[0][0]) / (-hf[0][0])
    clock_ratio_s = (-hsb[0][0]) / (-hs[0][0])

    shear = [[F(0), F(1)], [F(0), F(0)]]

    eta = [[F(-1), F(0)], [F(0), F(1)]]
    identity = [[F(1), F(0)], [F(0), F(1)]]
    lorentz = [[F(5, 3), F(4, 3)], [F(4, 3), F(5, 3)]]
    boost_rate = [[F(0), F(1)], [F(1), F(0)]]
    sign_reversal = [[F(-1), F(0)], [F(0), F(-1)]]

    ra, dra = [[F(1), F(0)], [F(0), F(1)]], [[F(1), F(0)], [F(0), F(-1)]]
    rb, drb = [[F(2), F(0)], [F(0), F(1)]], [[F(0), F(0)], [F(0), F(0)]]
    c = mm(mm(rb, m), inv2(ra))
    dc = add(add(mm(mm(drb, m), inv2(ra)), mm(mm(rb, dm), inv2(ra))),
             scale(F(-1), mm(mm(mm(mm(rb, m), inv2(ra)), dra), inv2(ra))))
    gamma = mm(dc, inv2(c))
    omega_b, omega_a = mm(drb, inv2(rb)), mm(dra, inv2(ra))
    omit_source_score = add(omega_b, mm(mm(rb, k), inv2(rb)))

    catches = [
        {"name": "freeze_live_carry_rate", "caught": frozen != dhbar},
        {"name": "omit_left_connection_term", "caught": omit_left != dhbar},
        {"name": "reverse_noncommuting_carry_order", "caught": mm(mba, mcb) != mca},
        {"name": "reverse_right_rate_composition_order", "caught": wrong_rate != correct_rate and correct_rate == kca},
        {"name": "freeze_live_source_endpoint_gauge", "caught": frozen_source_gauge != expected_dh},
        {"name": "drop_half_trace_common_scale_rate", "caught": carried_k - base_k == (k[0][0] + k[1][1]) / 2
         and carried_k - base_k != k[0][0] + k[1][1]},
        {"name": "promote_general_gl2_phi_shift_to_carry_only_character", "caught": clock_ratio_f != clock_ratio_s},
        {"name": "scalar_rate_closure_promoted_to_matrix_rate_closure",
         "caught": shear[0][0] + shear[1][1] == 0 and shear[1][1] - shear[0][0] == 0
         and shear != [[F(0), F(0)], [F(0), F(0)]]},
        {"name": "omit_source_endpoint_score_from_total_rate", "caught": omit_source_score != gamma},
        {"name": "promote_equal_pair_first_jets_to_finite_and_rate_carry_closure",
         "caught": lorentz != identity and mm(mm(tr(lorentz), eta), lorentz) == eta
         and boost_rate != z and add(mm(tr(boost_rate), eta), mm(eta, boost_rate)) == z},
        {"name": "promote_positive_bplus2_from_sufficient_to_necessary",
         "caught": sign_reversal[0][0] < 0 and sign_reversal[1][1] < 0
         and mm(mm(tr(sign_reversal), hf), sign_reversal) == hf},
        metadata_catch("promote_connection_split_to_gauge_independent",
                       "intrinsic_connection_split_gauge_independent", True),
        metadata_catch("promote_supplied_carry_to_physical", "physical_carry_derived", True),
        metadata_catch("promote_history_to_derived", "physical_history_derived", True),
        metadata_catch("promote_lambda_to_physical", "physical_lambda_owned", True),
    ]
    assert all(item["caught"] for item in catches)
    result = {
        "status": "PASS",
        "catch_count": len(catches),
        "algebra_mutation_count": 11,
        "metadata_guard_mutation_count": 4,
        "metadata_guards_are_independent_semantic_proofs": False,
        "caught": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
