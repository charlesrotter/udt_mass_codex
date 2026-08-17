#!/usr/bin/env python3
"""Independent exact-Fraction replay for G142."""

from __future__ import annotations

import hashlib
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def upper(a, u, d):
    return [[F(a), F(u)], [F(0), F(d)]]


def ratio(a):
    return a[1][1] / a[0][0]


def total(rt, m, rs):
    return mm(mm(rt, m), inv2(rs))


def main() -> None:
    tests = []
    triples = [
        (upper(2, F(1, 3), 3), upper(F(5, 4), F(-2, 7), F(7, 5)), upper(4, F(3, 8), 5),
         upper(F(3, 2), F(1, 9), F(4, 3)), upper(F(5, 3), F(-1, 6), F(7, 4))),
        (upper(F(7, 3), -1, F(9, 5)), upper(3, F(2, 5), 2), upper(F(11, 4), F(-3, 10), F(13, 6)),
         upper(F(4, 5), F(5, 7), F(6, 5)), upper(F(9, 7), F(-2, 3), F(8, 9))),
        (upper(5, F(7, 11), 4), upper(F(8, 3), F(-5, 12), F(7, 2)), upper(F(9, 2), F(1, 13), F(10, 3)),
         upper(F(11, 8), F(3, 14), F(13, 9)), upper(F(15, 11), F(-4, 15), F(14, 13))),
    ]
    gauges = [
        (upper(F(5, 2), F(1, 5), F(7, 3)), upper(F(4, 3), F(-2, 9), F(9, 4))),
        (upper(F(6, 5), F(-3, 8), F(8, 5)), upper(F(7, 4), F(5, 12), F(10, 7))),
        (upper(F(9, 7), F(2, 11), F(11, 8)), upper(F(12, 5), F(-1, 10), F(13, 6))),
    ]
    for (ra, rb, rc, mba, mcb), (pa, pb) in zip(triples, gauges):
        mca_composed = mm(mcb, mba)
        mca_independent = upper(F(17, 13), F(5, 19), F(19, 17))
        cba, ccb = total(rb, mba, ra), total(rc, mcb, rb)
        cca_composed = total(rc, mca_composed, ra)
        cca_independent = total(rc, mca_independent, ra)
        tests.append(mm(ccb, cba) == cca_composed)
        total_obstruction = [
            [mm(ccb, cba)[i][j] - cca_independent[i][j] for j in range(2)] for i in range(2)
        ]
        carry_obstruction = [
            [mca_composed[i][j] - mca_independent[i][j] for j in range(2)] for i in range(2)
        ]
        transported_obstruction = mm(mm(inv2(rc), total_obstruction), ra)
        tests.append(transported_obstruction == carry_obstruction)
        tests.append(total_obstruction != [[F(0), F(0)], [F(0), F(0)]])
        tests.append(mm(total(ra, inv2(mba), rb), cba) == upper(1, 0, 1))
        rap, rbp = mm(ra, pa), mm(rb, pb)
        mbap = mm(mm(inv2(pb), mba), pa)
        tests.append(total(rbp, mbap, rap) == cba)
        tests.append(ratio(mbap) == ratio(mba) * ratio(pa) / ratio(pb))
        tests.append(ratio(cba) == (ratio(rb) / ratio(ra)) * ratio(mba))
        tests.append(ratio(mm(ccb, cba)) == ratio(ccb) * ratio(cba))
        tests.append((cba[0][0] * cba[1][1])
                     == (rb[0][0] * rb[1][1]) / (ra[0][0] * ra[1][1])
                     * (mba[0][0] * mba[1][1]))

    neutral = upper(F(5, 3), F(4, 7), F(5, 3))
    tests.append(ratio(neutral) == 1)
    tests.append(neutral != upper(1, 0, 1))
    tests.append(neutral[0][1] != 0)
    tests.append(neutral[0][0] * neutral[1][1] != 1)
    identity = upper(1, 0, 1)
    depth = upper(F(1, 2), 0, 2)
    tests.append(ratio(total(identity, identity, identity)) == 1)
    tests.append(ratio(total(identity, depth, identity)) == 4)

    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative, _role = line.split("\t")
        tests.append(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected)

    passed = sum(bool(test) for test in tests)
    if passed != len(tests):
        raise SystemExit(f"FAIL {passed}/{len(tests)}")
    print(f"PASS {passed}/{len(tests)}: independent carrier/carry composition, gauge, grading, and ownership countermodel")


if __name__ == "__main__":
    main()
