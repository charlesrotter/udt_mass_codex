#!/usr/bin/env python3
"""Exact G158 complete-coframe semidirect composition derivation."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "f26c7ace"
LANDING = (
    "GAUGE_FIXED_COMPLETE_COFRAME_SEMIDIRECT_SCORE_DERIVED__"
    "TEN_CHANNEL_REGULAR_GROUP_CLOSES__BASE_AND_SCREEN_BPLUS2_CHANNELS_"
    "ACT_ON_FOUR_MIXING_COMPONENTS__Y_Z_ARE_QUERY_REPRESENTATION_DATA_"
    "NOT_GROUP_COORDINATES__CHANGING_BALANCE_ALLOWED__PHYSICAL_CARRY_"
    "HISTORY_SCORE_AND_GLOBAL_COMPLETION_OPEN"
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest() -> int:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 10
    assert [row["source_id"] for row in rows] == [f"S{i:02d}" for i in range(1, 11)]
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"]), row["source_id"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["source_id"]
    return len(rows)


def upper(a, u, d):
    return sp.Matrix([[a, u], [0, d]])


def full_e(b, q, s):
    return b.row_join(sp.zeros(2)).col_join((q * s).row_join(q))


def split_e(e):
    b = e[:2, :2]
    q = e[2:, 2:]
    s = sp.simplify(q.inv() * e[2:, :2])
    return b, q, s


def group_product(g2, g1):
    b2, q2, s2 = g2
    b1, q1, s1 = g1
    return (
        sp.simplify(b2 * b1),
        sp.simplify(q2 * q1),
        sp.simplify(s1 + q1.inv() * s2 * b1),
    )


def group_inverse(g):
    b, q, s = g
    return sp.simplify(b.inv()), sp.simplify(q.inv()), sp.simplify(-q * s * b.inv())


def exact_checks() -> dict[str, object]:
    checks: list[str] = []

    b00, b01, b11 = sp.symbols("b00 b01 b11", positive=True)
    q00, q01, q11 = sp.symbols("q00 q01 q11", positive=True)
    s00, s01, s10, s11 = sp.symbols("s00 s01 s10 s11", real=True)
    b = upper(b00, b01, b11)
    q = upper(q00, q01, q11)
    s = sp.Matrix([[s00, s01], [s10, s11]])
    e = full_e(b, q, s)

    rb, rq, rs = split_e(e)
    assert rb == b and rq == q and sp.simplify(rs - s) == sp.zeros(2)
    checks.append("unique_complete_coframe_factorization")

    # Ten structured coframe entries versus ten gauge-fixed coordinates.
    variables = (b00, b01, b11, q00, q01, q11, s00, s01, s10, s11)
    entries = sp.Matrix(
        [e[0, 0], e[0, 1], e[1, 1], e[2, 2], e[2, 3], e[3, 3],
         e[2, 0], e[2, 1], e[3, 0], e[3, 1]]
    )
    jac_det = sp.factor(entries.jacobian(variables).det())
    assert sp.simplify(jac_det - (q00 * q11) ** 2) == 0
    checks.append("ten_coordinate_jacobian_full_rank")

    def generic_tuple(prefix):
        a0, a1 = sp.symbols(f"{prefix}b0 {prefix}b1", positive=True)
        au = sp.symbols(f"{prefix}bu", real=True)
        c0, c1 = sp.symbols(f"{prefix}q0 {prefix}q1", positive=True)
        cu = sp.symbols(f"{prefix}qu", real=True)
        x = sp.symbols(f"{prefix}s0:4", real=True)
        return upper(a0, au, a1), upper(c0, cu, c1), sp.Matrix(2, 2, x)

    g1 = generic_tuple("a")
    g2 = generic_tuple("b")
    product = group_product(g2, g1)
    assert sp.simplify(full_e(*g2) * full_e(*g1) - full_e(*product)) == sp.zeros(4)
    checks.append("exact_complete_coframe_closure_and_composition")

    identity = (sp.eye(2), sp.eye(2), sp.zeros(2))
    assert sp.simplify(full_e(*group_product(g1, identity)) - full_e(*g1)) == sp.zeros(4)
    assert sp.simplify(full_e(*group_product(identity, g1)) - full_e(*g1)) == sp.zeros(4)
    inverse = group_inverse(g1)
    assert sp.simplify(full_e(*inverse) * full_e(*g1) - sp.eye(4)) == sp.zeros(4)
    assert sp.simplify(full_e(*g1) * full_e(*inverse) - sp.eye(4)) == sp.zeros(4)
    checks.append("identity_and_exact_inverse")

    # Closure plus unique factorization inherits associativity from ordinary matrices.
    g3 = generic_tuple("c")
    assert sp.simplify(
        (full_e(*g3) * full_e(*g2)) * full_e(*g1)
        - full_e(*g3) * (full_e(*g2) * full_e(*g1))
    ) == sp.zeros(4)
    checks.append("associativity_inherited_from_matrix_group")

    h = sp.diag(b, q)
    n = full_e(sp.eye(2), sp.eye(2), s)
    conjugated = sp.simplify(h * n * h.inv())
    expected_conjugated = full_e(sp.eye(2), sp.eye(2), sp.simplify(q * s * b.inv()))
    assert sp.simplify(conjugated - expected_conjugated) == sp.zeros(4)
    assert sp.simplify(
        full_e(sp.eye(2), sp.eye(2), s)
        * full_e(sp.eye(2), sp.eye(2), sp.eye(2))
        - full_e(sp.eye(2), sp.eye(2), s + sp.eye(2))
    ) == sp.zeros(4)
    checks.append("base_screen_conjugation_and_additive_mixing_normal_subgroup")

    det_e = sp.factor(e.det())
    assert sp.simplify(det_e - b.det() * q.det()) == 0
    for value in (s00, s01, s10, s11):
        assert sp.diff(det_e, value) == 0
    checks.append("base_and_screen_determinant_characters_miss_mixing")

    # Query data are acted on as a rank-two representation; they are not group coordinates.
    y = sp.Matrix(2, 2, sp.symbols("y0:4", real=True))
    z = sp.Matrix(2, 2, sp.symbols("z0:4", real=True))
    j = y.col_join(z)
    direct = sp.simplify(full_e(*g2) * (full_e(*g1) * j))
    joined = sp.simplify(full_e(*product) * j)
    assert sp.simplify(direct - joined) == sp.zeros(4, 2)
    y1 = sp.simplify(g1[0] * y)
    z1 = sp.simplify(g1[1] * (g1[2] * y + z))
    assert sp.simplify(full_e(*g1) * j - y1.col_join(z1)) == sp.zeros(4, 2)

    a = sp.Matrix(2, 2, sp.symbols("r0:4", real=True))
    eta = sp.diag(-1, 1, 1, 1)
    metric = sp.simplify(j.T * e.T * eta * e * j)
    reparameterized = sp.simplify((j * a).T * e.T * eta * e * (j * a))
    assert sp.simplify(reparameterized - a.T * metric * a) == sp.zeros(2)
    checks.append("query_representation_action_and_pair_domain_covariance")

    # Exact right/left logarithmic derivatives: the native time-live score.
    db = sp.Matrix(2, 2, sp.symbols("db0:4", real=True))
    dq = sp.Matrix(2, 2, sp.symbols("dq0:4", real=True))
    ds = sp.Matrix(2, 2, sp.symbols("ds0:4", real=True))
    de = db.row_join(sp.zeros(2)).col_join((dq * s + q * ds).row_join(dq))
    right = sp.simplify(de * e.inv())
    right_expected = (db * b.inv()).row_join(sp.zeros(2)).col_join(
        (q * ds * b.inv()).row_join(dq * q.inv())
    )
    assert sp.simplify(right - right_expected) == sp.zeros(4)
    left = sp.simplify(e.inv() * de)
    left_mix = sp.simplify(ds + q.inv() * dq * s - s * b.inv() * db)
    left_expected = (b.inv() * db).row_join(sp.zeros(2)).col_join(
        left_mix.row_join(q.inv() * dq)
    )
    assert sp.simplify(left - left_expected) == sp.zeros(4)
    checks.append("exact_right_and_left_logarithmic_score")

    dj = sp.Matrix(4, 2, sp.symbols("dj0:8", real=True))
    v = sp.simplify(e * j)
    dv = sp.simplify(de * j + e * dj)
    assert sp.simplify(dv - (right * v + e * dj)) == sp.zeros(4, 2)
    dh = sp.simplify(dv.T * eta * v + v.T * eta * dv)
    assert dh == dh.T
    checks.append("pair_score_splits_metric_generator_and_query_motion")

    # Smooth changing-balance endpoint frames telescope, without forming one scalar subgroup.
    def frame(t):
        bt = sp.Matrix([[1 + t, t**2], [0, 1 + t**2]])
        qt = sp.Matrix([[1 + t**2, t], [0, 1 + 2 * t]])
        st = sp.Matrix([[t, t**2], [t**3, -t]])
        return full_e(bt, qt, st)

    e0, e1, e2 = frame(sp.Integer(0)), frame(sp.Integer(1)), frame(sp.Integer(2))
    c10 = sp.simplify(e1 * e0.inv())
    c21 = sp.simplify(e2 * e1.inv())
    c20 = sp.simplify(e2 * e0.inv())
    assert sp.simplify(c21 * c10 - c20) == sp.zeros(4)
    assert e2 != e1 * e1
    tt = sp.symbols("tt", real=True)
    et = frame(tt)
    omega_t = sp.simplify(et.diff(tt) * et.inv())
    omega_bb_0 = sp.simplify(omega_t[:2, :2].subs(tt, 0))
    omega_bb_1 = sp.simplify(omega_t[:2, :2].subs(tt, 1))
    assert omega_bb_0 == sp.Matrix([[1, 0], [0, 0]])
    assert omega_bb_1 == sp.Matrix([[sp.Rational(1, 2), sp.Rational(3, 4)], [0, 1]])
    # The two scores cannot differ by a scalar reparameterization factor.
    assert omega_bb_0[1, 1] == 0 and omega_bb_1[1, 1] != 0
    checks.append("changing_full_score_endpoint_family_telescopes")

    # Fixed-generator control: X=[[A,0],[M,C]], with diagonal A,C for a closed exact formula.
    t, u = sp.symbols("t u", real=True)
    aa = (sp.Rational(1, 3), sp.Rational(-2, 5))
    cc = (sp.Rational(-1, 4), sp.Rational(3, 7))
    mm = sp.Matrix([[sp.Rational(2, 3), sp.Rational(-3, 5)],
                    [sp.Rational(5, 7), sp.Rational(7, 11)]])

    def fixed_generator_tuple(x):
        bx = sp.diag(*[sp.exp(value * x) for value in aa])
        qx = sp.diag(*[sp.exp(value * x) for value in cc])
        sx = sp.Matrix(2, 2, lambda i, j: sp.simplify(
            mm[i, j] * (sp.exp((aa[j] - cc[i]) * x) - 1) / (aa[j] - cc[i])
        ))
        return bx, qx, sx

    gt, gu, gtu = fixed_generator_tuple(t), fixed_generator_tuple(u), fixed_generator_tuple(t + u)
    assert sp.simplify(full_e(*group_product(gt, gu)) - full_e(*gtu)) == sp.zeros(4)
    fixed_right_mix = sp.simplify(
        gt[1] * gt[2].diff(t) * gt[0].inv()
    )
    assert sp.simplify(fixed_right_mix - mm) == sp.zeros(2)
    checks.append("fixed_generator_full_score_is_extra_one_parameter_restriction")

    assert len(checks) == 12
    return {
        "exact_checks": len(checks),
        "exact_check_names": checks,
        "ten_coordinate_jacobian_determinant": str(jac_det),
        "composition_law": {
            "B21": "B2*B1",
            "Q21": "Q2*Q1",
            "S21": "S1+Q1^-1*S2*B1",
        },
        "inverse_law": {
            "B_inv": "B^-1",
            "Q_inv": "Q^-1",
            "S_inv": "-Q*S*B^-1",
        },
        "right_score": {
            "base": "dB*B^-1",
            "screen": "dQ*Q^-1",
            "mixing": "Q*dS*B^-1",
        },
        "pair_score": "dV=Omega_R*V+E*dJ",
        "coordinate_count": 10,
        "base_channel_count": 3,
        "screen_channel_count": 3,
        "mixing_channel_count": 4,
        "query_blocks_are_group_coordinates": False,
        "changing_score_witness_noncollinear": True,
        "changing_score_base_blocks": {
            "lambda_0": "[[1,0],[0,0]]",
            "lambda_1": "[[1/2,3/4],[0,1]]",
        },
        "fixed_ratios_derived": False,
        "physical_score_derived": False,
        "physical_cross_query_carry_derived": False,
    }


def main() -> None:
    source_count = verify_manifest()
    result = {
        "status": "PASS",
        "registered_outcome_class": "COMPLETE_COFRAME_SEMIDIRECT_SCORE_DERIVED",
        "landing": LANDING,
        "source_count": source_count,
        **exact_checks(),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
