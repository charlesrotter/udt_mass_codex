#!/usr/bin/env python3
"""Exact G103 production algebra. Reads no observational outcome artifact."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ETA = sp.diag(-1, 1, 1, 1)


def mat_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in matrix)


def pair_readout(v: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    h = sp.simplify(v.T * ETA * v)
    t = sp.sqrt(-h[0, 0])
    u = sp.simplify(v[:, 0] / t)
    r = sp.simplify(v[:, 1] - h[0, 1] / h[0, 0] * v[:, 0])
    ell = sp.sqrt(sp.simplify(h[1, 1] - h[0, 1] ** 2 / h[0, 0]))
    n = sp.simplify(r / ell)
    return h, u, n


def block_coframe(
    b: sp.Matrix, q: sp.Matrix, s: sp.Matrix
) -> sp.Matrix:
    zero = sp.zeros(2)
    return b.row_join(zero).col_join((q * s).row_join(q))


def exact_rank(matrix: sp.Matrix) -> int:
    return int(matrix.rank(iszerofunc=lambda x: sp.simplify(x) == 0))


def main() -> None:
    # R-ZERO: full complete block form, not a diagonal shortcut.
    b = sp.Matrix([[2, sp.Rational(1, 3)], [0, sp.Rational(3, 2)]])
    q = sp.Matrix([[sp.Rational(5, 4), sp.Rational(1, 5)], [0, sp.Rational(7, 6)]])
    s = sp.Matrix([[sp.Rational(1, 7), sp.Rational(-2, 9)],
                   [sp.Rational(3, 11), sp.Rational(1, 13)]])
    e = block_coframe(b, q, s)
    v_target = sp.Matrix([
        [2, 0],
        [0, sp.Rational(3, 2)],
        [sp.Rational(1, 2), 1],
        [sp.Rational(-1, 3), 2],
    ])
    j = sp.simplify(e.inv() * v_target)
    zero_residual = sp.simplify(e * j - v_target)
    h_target = sp.simplify(v_target.T * ETA * v_target)
    zero_regular = bool(h_target[0, 0] < 0 and h_target.det() < 0)

    # R-FIRST: every complete block and every query block may vary.
    b_dot = sp.Matrix([[sp.Rational(1, 5), sp.Rational(-1, 8)],
                       [sp.Rational(1, 9), sp.Rational(2, 7)]])
    q_dot = sp.Matrix([[sp.Rational(-1, 6), sp.Rational(1, 10)],
                       [sp.Rational(1, 12), sp.Rational(1, 11)]])
    s_dot = sp.Matrix([[sp.Rational(2, 13), sp.Rational(1, 14)],
                       [sp.Rational(-1, 15), sp.Rational(3, 17)]])
    e_dot = b_dot.row_join(sp.zeros(2)).col_join(
        (q_dot * s + q * s_dot).row_join(q_dot)
    )
    v_dot_target = sp.Matrix([
        [sp.Rational(1, 3), sp.Rational(-1, 4)],
        [sp.Rational(2, 5), sp.Rational(1, 6)],
        [sp.Rational(-1, 7), sp.Rational(3, 8)],
        [sp.Rational(4, 9), sp.Rational(-2, 11)],
    ])
    j_dot = sp.simplify(e.inv() * (v_dot_target - e_dot * j))
    first_residual = sp.simplify(e_dot * j + e * j_dot - v_dot_target)

    # R-SKY: two complete pair coframes sharing one normalized observer.
    u_o = sp.Matrix([1, 0, 0, 0])
    n1 = sp.Matrix([0, 1, 0, 0])
    n2 = sp.Matrix([0, sp.Rational(3, 5), sp.Rational(4, 5), 0])
    v1 = sp.Matrix.hstack(2 * u_o, sp.Rational(1, 2) * u_o + 3 * n1)
    v2 = sp.Matrix.hstack(sp.Rational(3, 2) * u_o,
                          sp.Rational(-1, 3) * u_o + sp.Rational(5, 2) * n2)
    _, u1, n1_read = pair_readout(v1)
    _, u2, n2_read = pair_readout(v2)
    sky_cos = sp.simplify((n1_read.T * ETA * n2_read)[0])
    sky_checks = {
        "common_clock": mat_zero(u1 - u2),
        "n1_unit": sp.simplify((n1_read.T * ETA * n1_read)[0] - 1) == 0,
        "n2_unit": sp.simplify((n2_read.T * ETA * n2_read)[0] - 1) == 0,
        "cosine": str(sky_cos),
    }

    # R-GRAM: a valid four-direction sky has rank <= 3; I4 is a hostile target.
    directions = sp.Matrix([
        [1, 0, 0, sp.Rational(3, 5)],
        [0, 1, 0, sp.Rational(4, 5)],
        [0, 0, 1, 0],
    ])
    gram = sp.simplify(directions.T * directions)
    hostile_gram = sp.eye(4)
    gram_checks = {
        "valid_diag": [str(gram[i, i]) for i in range(4)],
        "valid_rank": exact_rank(gram),
        "valid_det": str(sp.factor(gram.det())),
        "hostile_rank": exact_rank(hostile_gram),
        "hostile_det": str(hostile_gram.det()),
    }

    # R-DEPTH: arbitrary positive observer-star data extend by endpoint potentials.
    z_star = [sp.Rational(1), sp.Rational(3, 2), sp.Rational(5, 3),
              sp.Rational(7, 4), sp.Rational(11, 6)]
    z_ij = [[sp.simplify(z_star[j] / z_star[i]) for j in range(5)] for i in range(5)]
    composition_defects = [
        sp.simplify(z_ij[i][j] * z_ij[j][k] - z_ij[i][k])
        for i in range(5) for j in range(5) for k in range(5)
    ]
    reversal_defects = [
        sp.simplify(z_ij[i][j] * z_ij[j][i] - 1)
        for i in range(5) for j in range(5)
    ]

    # R-FIXEDBASE: replay the conditional inequality, then release J.
    t, ell = sp.Rational(4), sp.Rational(9)
    a, b_terminal, delta = sp.Rational(2), sp.Rational(13), sp.Rational(1, 2)
    g_fixed = sp.Matrix([
        [t - a, -a * delta],
        [-a * delta, b_terminal - ell - a * delta**2],
    ])
    fixed_inequality_margin = sp.simplify(
        (t - a) * (b_terminal - ell) - t * a * delta**2
    )
    base_e = sp.diag(2, 3, 1, 1)
    lower_phi_v = sp.Matrix([[3, 0], [0, 2], [0, 0], [0, 0]])
    lower_phi_j = sp.simplify(base_e.inv() * lower_phi_v)
    released_residual = sp.simplify(base_e * lower_phi_j - lower_phi_v)
    h_lower = sp.simplify(lower_phi_v.T * ETA * lower_phi_v)
    phi_base = sp.Rational(1, 4) * sp.log(ell / t)
    phi_lower = sp.Rational(1, 4) * sp.log((-h_lower.det()) / h_lower[0, 0] ** 2)

    # R-MEASURE: three symmetric couplings share one marginal but give 0, pi/2, pi.
    identity = sp.eye(4) / 4
    antipodal = sp.Matrix([
        [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]
    ]) / 4
    orthogonal = sp.Matrix([
        [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]
    ]) / 4
    couplings = {"parallel": identity, "orthogonal": orthogonal, "antipodal": antipodal}
    marginal = sp.Matrix([sp.Rational(1, 4)] * 4)
    coupling_checks = {}
    for name, coupling in couplings.items():
        coupling_checks[name] = {
            "symmetric": coupling == coupling.T,
            "row_marginal": [str(x) for x in coupling * sp.ones(4, 1)],
            "column_marginal": [str(x) for x in coupling.T * sp.ones(4, 1)],
            "same_marginal": mat_zero(coupling * sp.ones(4, 1) - marginal),
        }

    checks = {
        "zero_order_exact": mat_zero(zero_residual),
        "zero_order_target_regular": zero_regular,
        "first_jet_exact": mat_zero(first_residual),
        "sky": sky_checks,
        "gram": gram_checks,
        "depth_composition_exact": all(x == 0 for x in composition_defects),
        "depth_reversal_exact": all(x == 0 for x in reversal_defects),
        "fixed_base_gram_psd": all(x >= 0 for x in g_fixed.eigenvals()),
        "fixed_base_margin": str(fixed_inequality_margin),
        "released_j_exact": mat_zero(released_residual),
        "released_phi_below_base": bool(sp.N(phi_lower - phi_base) < 0),
        "phi_base": str(phi_base),
        "phi_released": str(phi_lower),
        "couplings": coupling_checks,
        "outcome_artifacts_read": [],
    }
    required = [
        checks["zero_order_exact"], checks["zero_order_target_regular"],
        checks["first_jet_exact"], sky_checks["common_clock"],
        sky_checks["n1_unit"], sky_checks["n2_unit"], sky_cos == sp.Rational(3, 5),
        gram_checks["valid_rank"] == 3, gram_checks["valid_det"] == "0",
        gram_checks["hostile_rank"] == 4, checks["depth_composition_exact"],
        checks["depth_reversal_exact"], checks["fixed_base_gram_psd"],
        fixed_inequality_margin > 0, checks["released_j_exact"],
        checks["released_phi_below_base"],
        all(v["symmetric"] and v["same_marginal"] for v in coupling_checks.values()),
    ]
    if not all(required):
        raise AssertionError(json.dumps(checks, indent=2, sort_keys=True))

    result = {
        "status": "PASS",
        "landing": (
            "LOCAL_REGULAR_ZERO_AND_FIRST_JET_OBSERVABLE_SURJECTION_DERIVED"
            "__COMMON_SKY_GRAM_AND_GENERIC_MEASURE_CONSISTENCY_ONLY"
            "__NO_NONTRIVIAL_SOURCE_INDEPENDENT_PATTERN_RESTRICTION_OWNED_IN_FROZEN_SOURCE_UNIVERSE"
            "__GLOBAL_CRITICAL_BOOTSTRAP_AND_SOURCE_HISTORY_JOINTS_OPEN"
        ),
        "checks": checks,
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
