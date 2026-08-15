#!/usr/bin/env python3
"""Hostile mutations for overlap typing and uncompressed loud/quiet families."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "CATCH_PROOF_RESULT.json"


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def tr(a):
    return [list(row) for row in zip(*a)]


def diag(values):
    return [[F(values[i]) if i == j else F(0) for j in range(len(values))] for i in range(len(values))]


def inv2(a):
    d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def determinant(a):
    m = [row[:] for row in a]
    out = F(1)
    for c in range(len(m)):
        p = next((r for r in range(c, len(m)) if m[r][c]), None)
        if p is None:
            return F(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            out *= -1
        pivot = m[c][c]
        out *= pivot
        for j in range(c, len(m)):
            m[c][j] /= pivot
        for r in range(c + 1, len(m)):
            q = m[r][c]
            for j in range(c, len(m)):
                m[r][j] -= q * m[c][j]
    return out


def main():
    # C1: omitted dot-R term must be visible.
    h = [[F(-3, 4), 0], [0, F(5, 4)]]
    dh = [[F(2, 3), F(1, 5)], [F(1, 5), F(7, 6)]]
    r = [[1, F(3, 2)], [0, 1]]
    dr = [[0, 1], [0, 0]]
    full = add(add(mul(mul(tr(r), dh), r), mul(mul(tr(dr), h), r)), mul(mul(tr(r), h), dr))
    omitted = mul(mul(tr(r), dh), r)

    # C2: identity middle reset fails for unequal states.
    b_in = [[F(2), F(1)], [0, F(3)]]
    b_out = [[F(1), F(1, 2)], [0, F(4)]]
    middle = mul(b_out, inv2(b_in))

    # C3: frozen/omitted S changes the flat live family.
    t = F(3, 2)
    b = diag([1 / t, t])
    s = [[x / 2 for x in row] for row in b]
    p = mul(tr(s), s)
    p_frozen_out = [[F(0), F(0)], [F(0), F(0)]]

    # C4: a declared Gram family must actually have a lift; wrong S is caught.
    declared_p = diag([F(1, 4), F(1, 4)])
    wrong_s = diag([F(1, 3), F(1, 2)])
    reconstructed_wrong = mul(tr(wrong_s), wrong_s)

    # C5: an inconsistent five-channel target has rank five and cannot be a 4D Gram matrix.
    inconsistent_k = diag([-1, 1, 1, 1, 1])

    # C6: shared clock does not imply shared complete pair metric.
    h1 = diag([-1, 1])
    h2 = diag([-1, 5])

    caught = {
        "omit_dot_R": full != omitted,
        "identity_middle_reset": middle != diag([1, 1]),
        "freeze_or_omit_S": p != p_frozen_out,
        "Gram_family_without_correct_lift": declared_p != reconstructed_wrong,
        "ignore_4D_joint_Gram_rank": determinant(inconsistent_k) != 0,
        "shared_clock_promoted_to_shared_pair": h1[0][0] == h2[0][0] and h1 != h2,
    }
    result = {
        "schema": "udt.overlapping_pair_live_compatibility.catch.v1",
        "caught": caught,
        "passed": all(caught.values()),
        "residuals": {
            "omit_dot_R": [[str(x) for x in row] for row in sub(full, omitted)],
            "middle_reset": [[str(x) for x in row] for row in middle],
            "S_Gram": [[str(x) for x in row] for row in p],
            "wrong_lift_Gram": [[str(x) for x in row] for row in reconstructed_wrong],
            "inconsistent_Gram_determinant": str(determinant(inconsistent_k)),
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
