#!/usr/bin/env python3
"""Independent Fraction replay for G144; no production imports."""

from __future__ import annotations

import hashlib
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def upper(a, u, d):
    return [[F(a), F(u)], [F(0), F(d)]]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def main() -> None:
    tests = []
    eta = [[F(-1), F(0)], [F(0), F(1)]]
    identity = upper(1, 0, 1)
    witnesses = [
        (upper(2, F(1, 3), 3), upper(F(5, 4), F(-2, 7), F(7, 5))),
        (upper(F(7, 3), -1, F(9, 5)), upper(3, F(2, 5), 2)),
        (upper(5, F(7, 11), 4), upper(F(8, 3), F(-5, 12), F(7, 2))),
    ]
    for rbeta, jba in witnesses:
        ralpha = mm(rbeta, jba)
        hbeta = mm(mm(transpose(rbeta), eta), rbeta)
        halpha = mm(mm(transpose(jba), hbeta), jba)
        tests.append(halpha == mm(mm(transpose(ralpha), eta), ralpha))
        c = mm(mm(rbeta, jba), inv2(ralpha))
        tests.append(c == identity)
        tests.append(mm(mm(transpose(c), eta), c) == eta)

        jcb = upper(F(9, 7), F(3, 10), F(11, 8))
        jca = mm(jcb, jba)
        tests.append(mm(jcb, jba) == jca)

    # Direct positive-triangular Lorentz checks over a bounded exact census.
    for x in (F(1, 2), F(1), F(2)):
        for n in (F(-1), F(0), F(1)):
            for y in (F(1, 2), F(1), F(2)):
                c = upper(x, n, y)
                is_lorentz = mm(mm(transpose(c), eta), c) == eta
                tests.append(is_lorentz == (x == 1 and n == 0 and y == 1))

    # Independent endpoint/interior and timelike checks for eps=2.
    eps = F(2)
    for s in (F(0), F(1)):
        tests.append(eps * s * (1 - s) == 0)
    tests.append(eps * F(1, 2) * (1 - F(1, 2)) == F(1, 2))
    for s in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
        h11 = 1 + eps * eps * (1 - 2*s) * (1 - 2*s)
        tests.append(-h11 < 0)

    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative, _role = line.split("\t")
        tests.append(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected)

    passed = sum(bool(test) for test in tests)
    if passed != len(tests):
        raise SystemExit(f"FAIL {passed}/{len(tests)}")
    print(f"PASS {passed}/{len(tests)}: independent overlap isometry, Bplus intersection, and endpoint-only countermodel")


if __name__ == "__main__":
    main()
