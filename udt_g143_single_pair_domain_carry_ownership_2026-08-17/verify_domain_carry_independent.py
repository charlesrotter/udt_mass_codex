#!/usr/bin/env python3
"""Independent Fraction replay for G143; no SymPy or production imports."""

from __future__ import annotations

import hashlib
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def upper(a, u, d):
    return [[F(a), F(u)], [F(0), F(d)]]


def total(rt, m, rs):
    return mm(mm(rt, m), inv2(rs))


def ratio(a):
    return a[1][1] / a[0][0]


def main() -> None:
    tests = []
    identity = upper(1, 0, 1)
    witnesses = [
        (upper(2, F(1, 3), 3), upper(5, F(-2, 7), 7), upper(4, F(2, 9), 6),
         upper(1, 0, 1), upper(2, 0, 1), upper(3, F(1, 4), 2)),
        (upper(F(7, 3), -1, F(9, 5)), upper(3, F(2, 5), 2), upper(F(11, 4), F(-3, 10), F(13, 6)),
         upper(F(5, 4), F(1, 8), F(6, 5)), upper(F(7, 3), F(-2, 9), F(8, 7)), upper(F(9, 5), F(3, 11), F(10, 9))),
        (upper(5, F(7, 11), 4), upper(F(8, 3), F(-5, 12), F(7, 2)), upper(F(9, 2), F(1, 13), F(10, 3)),
         upper(F(4, 3), F(-1, 6), F(5, 4)), upper(F(6, 5), F(2, 7), F(7, 6)), upper(F(8, 7), F(-3, 10), F(9, 8))),
    ]
    for ra, rb, rc, ja, jb, jc in witnesses:
        c_y = total(rb, identity, ra)
        rap, rbp, rcp = mm(ra, inv2(ja)), mm(rb, inv2(jb)), mm(rc, inv2(jc))
        mba, mcb, mca = mm(jb, inv2(ja)), mm(jc, inv2(jb)), mm(jc, inv2(ja))
        c_z = total(rbp, mba, rap)
        tests.append(c_y == c_z)
        tests.append(mm(mcb, mba) == mca)
        tests.append(mm(total(rcp, mcb, rbp), c_z) == total(rcp, mca, rap))
        tests.append(ratio(mba) == ratio(jb) / ratio(ja))
        tests.append(ratio(c_z) == ratio(c_y))
        tests.append(ratio(rbp) / ratio(rap) * ratio(mba) == ratio(c_y))

    # Independently evaluate z0=(1+s)t, z1=s at (0,0) and (0,1).
    ja_strip, jb_strip = upper(1, 0, 1), upper(2, 0, 1)
    m_strip = mm(jb_strip, inv2(ja_strip))
    tests.append(m_strip == upper(2, 0, 1))
    tests.append(m_strip != identity)
    tests.append(ratio(m_strip) == F(1, 2))
    tests.append(total(mm(witnesses[0][1], inv2(jb_strip)), m_strip,
                       mm(witnesses[0][0], inv2(ja_strip)))
                 == total(witnesses[0][1], identity, witnesses[0][0]))

    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative, _role = line.split("\t")
        tests.append(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected)

    passed = sum(bool(test) for test in tests)
    if passed != len(tests):
        raise SystemExit(f"FAIL {passed}/{len(tests)}")
    print(f"PASS {passed}/{len(tests)}: independent same-query domain carry and reparameterization replay")


if __name__ == "__main__":
    main()
