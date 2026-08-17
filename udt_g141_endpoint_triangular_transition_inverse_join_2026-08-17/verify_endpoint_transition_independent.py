#!/usr/bin/env python3
"""Independent numeric/stdlib replay for G141."""

from __future__ import annotations

import hashlib
import math
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def tr(a):
    return [list(row) for row in zip(*a)]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def inv2(a):
    d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def block(rows):
    return [[F(x) for x in row] for row in rows]


def close(a, b, tol=2e-11):
    return abs(float(a) - float(b)) <= tol * max(1.0, abs(float(a)), abs(float(b)))


def rank(a):
    work = [row[:] for row in a]
    rows, cols = len(work), len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if work[r][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for r in range(rows):
            if r != pivot_row and work[r][col] != 0:
                factor = work[r][col]
                work[r] = [work[r][c] - factor * work[pivot_row][c] for c in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def complete_metric(B, Q, S):
    QS = mm(Q, S)
    E = [B[0] + [F(0), F(0)], B[1] + [F(0), F(0)], QS[0] + Q[0], QS[1] + Q[1]]
    eta4 = block([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    return E, mm(mm(tr(E), eta4), E)


def main() -> None:
    tests = []
    B = block([[2, F(1, 5)], [0, F(3, 2)]])
    Q = block([[F(4, 3), F(1, 7)], [0, F(5, 4)]])
    S = block([[F(1, 10), -F(1, 12)], [F(1, 15), F(1, 9)]])
    E, g = complete_metric(B, Q, S)
    B_no_shift = [row[:] for row in B]
    B_no_shift[0][1] = F(0)
    Q_no_shear = [row[:] for row in Q]
    Q_no_shear[0][1] = F(0)
    _, g_no_base_shift = complete_metric(B_no_shift, Q, S)
    _, g_no_screen_shear = complete_metric(B, Q_no_shear, S)
    _, g_no_mixing = complete_metric(B, Q, block([[0, 0], [0, 0]]))
    raw = {
        "A": (block([[1, 0], [0, 1]]), block([[F(1, 20), -F(1, 25)], [F(1, 30), F(1, 18)]])),
        "B": (block([[1, F(1, 20)], [-F(1, 30), 1]]), block([[-F(1, 24), F(1, 28)], [F(1, 32), -F(1, 21)]])),
        "C": (block([[1, -F(1, 25)], [F(1, 40), 1]]), block([[F(1, 27), F(1, 31)], [-F(1, 29), F(1, 26)]])),
    }
    states = {}
    endpoint_J = {}
    channel_sensitivity = {key: False for key in (
        "base_shift", "screen_shear", "mixing", "angular_embedding",
    )}
    for name, (Y, Z) in raw.items():
        J = Y + Z
        h = mm(mm(tr(J), g), J)
        J_no_angular = Y + block([[0, 0], [0, 0]])
        channel_sensitivity["base_shift"] |= mm(mm(tr(J), g_no_base_shift), J) != h
        channel_sensitivity["screen_shear"] |= mm(mm(tr(J), g_no_screen_shear), J) != h
        channel_sensitivity["mixing"] |= mm(mm(tr(J), g_no_mixing), J) != h
        channel_sensitivity["angular_embedding"] |= mm(mm(tr(J_no_angular), g), J_no_angular) != h
        h00, h01, h11 = map(float, (h[0][0], h[0][1], h[1][1]))
        det = h00 * h11 - h01 * h01
        tests.extend((h00 < 0, det < 0))
        T = math.sqrt(-h00)
        L = math.sqrt(-det) / T
        beta = h01 / h00
        R = [[T, T * beta], [0.0, L]]
        eta2 = [[-1.0, 0.0], [0.0, 1.0]]
        rebuilt = mm(mm(tr(R), eta2), R)
        tests.append(max(abs(rebuilt[i][j] - float(h[i][j])) for i in range(2) for j in range(2)) < 2e-11)
        states[name] = {"R": R, "q": T / L, "phi": 0.5 * math.log(L / T)}
        endpoint_J[name] = J

    for target, source in (("B", "A"), ("C", "B"), ("C", "A")):
        joined = [endpoint_J[source][i] + endpoint_J[target][i] for i in range(4)]
        tests.append(rank(joined) == 4)
    tests.extend(channel_sensitivity.values())
    gauge_R = block([[2, F(1, 3)], [0, 3]])
    gauge_P = block([[F(5, 2), F(1, 7)], [0, F(7, 3)]])
    gauge_RP = mm(gauge_R, gauge_P)
    tests.append((gauge_RP[1][1] / gauge_RP[0][0]) / (gauge_R[1][1] / gauge_R[0][0])
                 == gauge_P[1][1] / gauge_P[0][0])
    eta2_exact = block([[-1, 0], [0, 1]])
    boost = block([[F(5, 4), F(3, 4)], [F(3, 4), F(5, 4)]])
    tests.append(mm(mm(tr(boost), eta2_exact), boost) == eta2_exact)
    tests.append(boost != block([[1, 0], [0, 1]]))

    # Carrier-matching map on the explicitly shared two-dimensional pair-coordinate carrier.
    # This is not identified with a full four-dimensional observer-chart differential.
    def D(target, source):
        return mm(inv2(states[target]["R"]), states[source]["R"])

    DBA, DCB, DCA, DAB = D("B", "A"), D("C", "B"), D("C", "A"), D("A", "B")
    tests.append(max(abs(mm(DCB, DBA)[i][j] - DCA[i][j]) for i in range(2) for j in range(2)) < 2e-11)
    tests.append(max(abs(mm(DAB, DBA)[i][j] - (1.0 if i == j else 0.0)) for i in range(2) for j in range(2)) < 2e-11)
    tests.append(any(abs(d[0][1]) > 1e-12 for d in (DBA, DCB, DCA)))
    for target, source, d in (("B", "A", DBA), ("C", "B", DCB), ("C", "A", DCA)):
        delta = -0.5 * math.log(d[1][1] / d[0][0])
        tests.append(close(delta, states[target]["phi"] - states[source]["phi"]))
        inverse_d = D(source, target)
        hrel = mm(mm(tr(inverse_d), [[-1.0, 0.0], [0.0, 1.0]]), inverse_d)
        det = hrel[0][0] * hrel[1][1] - hrel[0][1] ** 2
        phi_rel = 0.25 * math.log((-det) / hrel[0][0] ** 2)
        tests.append(close(phi_rel, delta))
    delta_ba = -0.5 * math.log(DBA[1][1] / DBA[0][0])
    delta_cb = -0.5 * math.log(DCB[1][1] / DCB[0][0])
    delta_ca = -0.5 * math.log(DCA[1][1] / DCA[0][0])
    tests.append(close(delta_ba + delta_cb, delta_ca))
    tests.append(close(-0.5 * math.log(DAB[1][1] / DAB[0][0]), -delta_ba))
    qba = states["B"]["q"] / states["A"]["q"]
    qcb = states["C"]["q"] / states["B"]["q"]
    qca = states["C"]["q"] / states["A"]["q"]
    tests.append(close(qba * qcb, qca))
    xba, xcb, xca = ((1 - q) / (1 + q) for q in (qba, qcb, qca))
    tests.append(close((xba + xcb) / (1 + xba * xcb), xca))

    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, rel, _role = line.split("\t")
        tests.append(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == expected)

    passed = sum(bool(x) for x in tests)
    if passed != len(tests):
        raise SystemExit(f"FAIL {passed}/{len(tests)}")
    print(f"PASS {passed}/{len(tests)}: independent calibration/carrier maps, grading, and source replay")


if __name__ == "__main__":
    main()
