#!/usr/bin/env python3
"""Mutation catches for G159 terminal first-jet descent and ownership guards."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[c * value for value in row] for row in a]


ETA = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)],
       [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]


def pair_metric(v):
    return mm(mm(transpose(v), ETA), v)


def pair_first_jet(v, p):
    return add(mm(mm(transpose(p), ETA), v), mm(mm(transpose(v), ETA), p))


def rates(h, dh):
    det = h[0][0] * h[1][1] - h[0][1] ** 2
    det_dot = dh[0][0] * h[1][1] + h[0][0] * dh[1][1] - 2 * h[0][1] * dh[0][1]
    kd = det_dot / (4 * det)
    pd = kd - dh[0][0] / (2 * h[0][0])
    bd = (dh[0][1] * h[0][0] - h[0][1] * dh[0][0]) / h[0][0] ** 2
    return kd, pd, bd


def metadata_catch(name, key, wrong_value):
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    result[key] = wrong_value
    expected = {
        "query_motion_frozen": False,
        "h_and_doth_lorentz_coframe_gauge_invariant": True,
        "terminal_coefficients_arbitrary_gl2_invariant": False,
        "physical_history_derived": False,
        "physical_lambda_owned": False,
        "calibration_carry_derived": False,
    }
    return {"name": name, "caught": result[key] != expected[key]}


def main():
    h = [[F(-2), F(1)], [F(1), F(3)]]
    dh = [[F(3), F(-1)], [F(-1), F(4)]]
    kd, pd, bd = rates(h, dh)
    det = h[0][0] * h[1][1] - h[0][1] ** 2
    det_dot = dh[0][0] * h[1][1] + h[0][0] * dh[1][1] - 2 * h[0][1] * dh[0][1]

    # Query-motion witness and a live Lorentz-gauge witness.
    vq = [[F(1), F(0)], [F(0), F(1)], [F(0), F(0)], [F(0), F(0)]]
    pq = [[F(0), F(1)], [F(0), F(1)], [F(0), F(0)], [F(0), F(0)]]
    query_rates = rates(pair_metric(vq), pair_first_jet(vq, pq))
    frozen_query_rates = rates(pair_metric(vq), pair_first_jet(vq, [[F(0), F(0)] for _ in range(4)]))

    lam = [[F(5, 3), F(4, 3), F(0), F(0)], [F(4, 3), F(5, 3), F(0), F(0)],
           [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    gen = [[F(0), F(2), F(0), F(0)], [F(2), F(0), F(0), F(0)],
           [F(0), F(0), F(0), F(-1)], [F(0), F(0), F(1), F(0)]]
    dlam = mm(gen, lam)
    vp = mm(lam, vq)
    correct_pp = add(mm(dlam, vq), mm(lam, pq))
    wrong_pp = mm(lam, pq)

    # Direct central derivative of Lambda(t)V(t), using exact quadratic paths.
    # Lambda(t)=(I+t*gen)Lambda and V(t)=V+tP, so the symmetric quotient
    # at +/-1 keeps exactly dLambda*V+Lambda*P.
    identity4 = [[F(int(i == j)) for j in range(4)] for i in range(4)]
    lam_plus = mm(add(identity4, gen), lam)
    lam_minus = mm(add(identity4, scale(F(-1), gen)), lam)
    v_plus = add(vq, pq)
    v_minus = add(vq, scale(F(-1), pq))
    direct_pp = scale(F(1, 2), add(mm(lam_plus, v_plus), scale(F(-1), mm(lam_minus, v_minus))))
    assert direct_pp == correct_pp

    catches = [
        {"name": "double_kappa_determinant_rate", "caught": det_dot / (2 * det) != kd},
        {"name": "omit_clock_norm_from_phi_rate", "caught": kd != pd},
        {"name": "omit_beta_quotient_rule", "caught": dh[0][1] / h[0][0] != bd},
        {"name": "freeze_query_motion", "caught": frozen_query_rates != query_rates},
        {"name": "omit_live_lorentz_inhomogeneous_term",
         "caught": wrong_pp != direct_pp},
        {"name": "call_log_ceff_rate_minus_phi", "caught": -pd != -2 * pd},
        metadata_catch("promote_terminal_coefficients_to_gl2_invariants",
                       "terminal_coefficients_arbitrary_gl2_invariant", True),
        metadata_catch("promote_history_to_derived", "physical_history_derived", True),
        metadata_catch("promote_lambda_to_owned", "physical_lambda_owned", True),
        metadata_catch("promote_calibration_carry_to_derived", "calibration_carry_derived", True),
    ]
    assert all(item["caught"] for item in catches)
    output = {
        "status": "PASS",
        "catch_count": len(catches),
        "algebra_mutation_count": 6,
        "metadata_guard_mutation_count": 4,
        "metadata_guards_are_independent_semantic_proofs": False,
        "live_lorentz_catch_targets_dotV_score_law_not_terminal_doth": True,
        "caught": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
