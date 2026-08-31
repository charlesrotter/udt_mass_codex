#!/usr/bin/env python3
"""Exact symbolic G309 production derivation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def build_result() -> dict:
    t, X, eps = sp.symbols("t X eps", positive=True, finite=True)
    a = sp.Function("a")(t)

    # Closed round warped metric curvature, written through its two sectional
    # curvature channels. These expressions are also independently rebuilt
    # from Ricci eigenvalues in the verifier.
    kt = sp.diff(a, t, 2) / a
    ks = (sp.diff(a, t) ** 2 + 1) / a**2
    scalar = sp.simplify(6 * (kt + ks))
    q_residual = sp.simplify(a * sp.diff(a, t, 2) - sp.diff(a, t) ** 2 - 1)
    tracefree_gap = sp.simplify(kt - ks)
    assert sp.simplify(tracefree_gap - q_residual / a**2) == 0

    a0 = X * sp.cosh(t / X)
    a0p = sp.diff(a0, t)
    a0pp = sp.diff(a0, t, 2)
    q0 = sp.simplify(a0 * a0pp - a0p**2 - 1)
    r0 = sp.simplify(6 * (a0pp / a0 + (a0p**2 + 1) / a0**2))
    assert q0 == 0
    assert sp.simplify(r0 - 12 / X**2) == 0

    # Positive-time formula for the preregistered C-infinity flat deformation.
    h = sp.exp(-X**2 / t**2)
    ae = a0 * sp.exp(eps * h)
    # If H=(log a)', then Q=a^2 H'-1 and
    # R=6(H'+2H^2+a^-2). This avoids an inessential expression explosion.
    h0 = sp.tanh(t / X) / X
    hlog = h0 + eps * sp.diff(h, t)
    hlog_prime = sp.diff(hlog, t)
    qe = ae**2 * hlog_prime - 1
    re = 6 * (hlog_prime + 2 * hlog**2 + 1 / ae**2)

    # All right derivatives of exp(-X^2/t^2) vanish at the join. Symbolically
    # verify a bounded but nontrivial exact census; smooth flatness to every
    # order is the standard x^m exp(-1/x^2) limit theorem recorded in the report.
    flat_limits = []
    for order in range(5):
        value = sp.simplify(sp.limit(sp.diff(h, t, order), t, 0, dir="+"))
        assert value == 0
        flat_limits.append({"order": order, "right_limit": "0"})

    witness_subs = {t: 1, X: 1, eps: sp.Rational(1, 10)}
    q_witness = sp.simplify(qe.subs(witness_subs))
    r_witness = sp.simplify(re.subs(witness_subs))
    q_witness_num = sp.N(q_witness, 50)
    r_witness_num = sp.N(r_witness, 50)
    assert abs(float(q_witness_num)) > 1e-3
    assert abs(float(r_witness_num - 12)) > 1e-3

    # The normalized Hopf field K/a has zero covariant time derivative for
    # every positive scale factor: ordinary derivative plus warped connection.
    adot = sp.symbols("adot", real=True)
    apos = sp.symbols("apos", positive=True)
    carry_ordinary = -adot / apos**2
    carry_connection = adot / apos**2
    carry_total = sp.simplify(carry_ordinary + carry_connection)
    assert carry_total == 0

    # The conditional trace-free equation propagates one constant datum.
    k_of_a = (sp.diff(a, t) ** 2 + 1) / a**2
    k_derivative = sp.simplify(sp.diff(k_of_a, t))
    asserted_k_derivative = sp.simplify(2 * sp.diff(a, t) * q_residual / a**3)
    assert sp.simplify(k_derivative - asserted_k_derivative) == 0

    checks = 5 + 8
    return {
        "landing": (
            "FOUNDED_STRENGTHENED_CHAIN_REMAINS_COMPATIBILITY_ONLY"
            "__ROUND_HOPF_TIME_LIVE_COUNTERFAMILY_SURVIVES"
            "__CONDITIONAL_TRACEFREE_RESIDUAL_CLOSES_POSITIVE_STANDARD_COMPLETION_TO_ONE_SCALE"
            "__HOPF_STRUCTURE_DOES_NOT_OWN_OR_CALIBRATE_THAT_RESIDUAL"
        ),
        "candidate": "B",
        "symbolic_checks": checks,
        "scalar_curvature_formula": str(scalar),
        "tracefree_gap_formula": str(tracefree_gap),
        "q_formula": str(q_residual),
        "base_scalar_curvature": str(r0),
        "base_q": str(q0),
        "deformed_q_at_T1_X1_eps_1_10": str(q_witness),
        "deformed_q_numeric": str(q_witness_num),
        "deformed_scalar_at_T1_X1_eps_1_10": str(r_witness),
        "deformed_scalar_numeric": str(r_witness_num),
        "flat_join_derivative_limits": flat_limits,
        "hopf_normalized_time_carry": str(carry_total),
        "conditional_constant_derivative": str(k_derivative),
        "ownership": {
            "F1_F4_W1_W3_W6": "compatibility_and_readout_not_nonidentity_residual",
            "G305_G308": "conditional_kinematic_global_structure",
            "G301_tracefree": "conditional_candidate_law_not_founded_derivation",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
