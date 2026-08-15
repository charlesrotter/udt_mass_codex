#!/usr/bin/env python3
"""Independent stdlib Fraction/Numpy replay; imports no production functions."""

from __future__ import annotations

from fractions import Fraction as F
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_VERIFICATION.json"


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def diag(values):
    n = len(values)
    return [[F(values[i]) if i == j else F(0) for j in range(n)] for i in range(n)]


def stack(top, bottom):
    return [row[:] for row in top] + [row[:] for row in bottom]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv2(a):
    d = det2(a)
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def determinant(a):
    m = [row[:] for row in a]
    n = len(m)
    out = F(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if m[r][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            out *= -1
        p = m[col][col]
        out *= p
        for j in range(col, n):
            m[col][j] /= p
        for r in range(col + 1, n):
            c = m[r][col]
            for j in range(col, n):
                m[r][j] -= c * m[col][j]
    return out


def rank(a):
    m = [row[:] for row in a]
    rows, cols = len(m), len(m[0])
    r = 0
    for col in range(cols):
        pivot = next((i for i in range(r, rows) if m[i][col]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        p = m[r][col]
        m[r] = [x / p for x in m[r]]
        for i in range(rows):
            if i != r:
                c = m[i][col]
                m[i] = [m[i][j] - c * m[r][j] for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def gram(v, eta):
    return mul(mul(transpose(v), eta), v)


def terminal_phi(h):
    return 0.25 * math.log(float(-det2(h) / (h[0][0] ** 2)))


def live_flat(t):
    b = diag([F(1, 1) / t, t])
    db = diag([-F(1, 1) / (t * t), 1])
    s = scale(F(1, 2), b)
    ds = scale(F(1, 2), db)
    v = stack(b, s)
    dv = stack(db, ds)
    eta4 = diag([-1, 1, 1, 1])
    h = gram(v, eta4)
    dh = add(mul(mul(transpose(dv), eta4), v), mul(mul(transpose(v), eta4), dv))
    return b, s, v, dv, h, dh


def main():
    eta4 = diag([-1, 1, 1, 1])

    # Independent O1 live overlap at t=3/2.
    t = F(3, 2)
    _, _, v, dv, h, dh = live_flat(t)
    r = mat([[1, t], [0, 1]])
    dr = mat([[0, 1], [0, 0]])
    v_a = mul(v, r)
    dv_a = add(mul(dv, r), mul(v, dr))
    h_a_direct = gram(v_a, eta4)
    dh_a_direct = add(mul(mul(transpose(dv_a), eta4), v_a), mul(mul(transpose(v_a), eta4), dv_a))
    h_a_overlap = mul(mul(transpose(r), h), r)
    dh_a_overlap = add(add(mul(mul(transpose(r), dh), r), mul(mul(transpose(dr), h), r)), mul(mul(transpose(r), h), dr))

    # O2 shared clock witness.
    j1 = [[F(1), F(0)], [F(0), F(1)], [F(0), F(0)], [F(0), F(0)]]
    j2 = [[F(1), F(0)], [F(0), F(2)], [F(0), F(1)], [F(0), F(0)]]
    h1 = gram(j1, eta4)
    h2 = gram(j2, eta4)

    # O3 middle reset.
    b_in = mat([[2, 1], [0, 3]])
    b_out = mat([[1, F(1, 2)], [0, 4]])
    r_ab = mat([[F(3, 2), F(1, 3)], [0, F(5, 4)]])
    r_bc = mat([[F(4, 3), -F(2, 5)], [0, F(6, 5)]])
    middle = mul(b_out, inv2(b_in))
    with_reset = mul(mul(r_bc, middle), r_ab)
    without_reset = mul(r_bc, r_ab)

    # Joint Gram rank/determinant/inertia.
    mathcal_j = [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 0, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
    ]
    mathcal_j = mat(mathcal_j)
    k = gram(mathcal_j, eta4)
    evals = np.linalg.eigvalsh(np.array([[float(x) for x in row] for row in k]))
    inertia = {
        "negative": int(np.sum(evals < -1e-12)),
        "positive": int(np.sum(evals > 1e-12)),
        "zero": int(np.sum(np.abs(evals) <= 1e-12)),
    }

    # Fully lifted response families at exact rational t samples.
    samples = [F(1, 4), F(1, 2), F(1), F(3, 2)]
    flat_trace = []
    flat_modulation = []
    monotone_trace = []
    monotone_modulation = []
    quiet_trace = []
    quiet_modulation = []
    for u in samples:
        b = diag([1 / u, u])
        binv = inv2(b)

        s_flat = scale(F(1, 2), b)
        p_flat = mul(transpose(s_flat), s_flat)
        pi_flat = mul(mul(transpose(binv), p_flat), binv)
        h_flat = add(mul(mul(transpose(b), diag([-1, 1])), b), p_flat)
        flat_trace.append(float(pi_flat[0][0] + pi_flat[1][1]))
        flat_modulation.append(terminal_phi(h_flat) - math.log(float(u)))

        scalar = (1 + 2 * u) / (4 * (1 + u))
        s_mono = scale(scalar, b)
        p_mono = mul(transpose(s_mono), s_mono)
        pi_mono = mul(mul(transpose(binv), p_mono), binv)
        h_mono = add(mul(mul(transpose(b), diag([-1, 1])), b), p_mono)
        monotone_trace.append(float(pi_mono[0][0] + pi_mono[1][1]))
        monotone_modulation.append(terminal_phi(h_mono) - math.log(float(u)))

        q_quiet = diag([u, 1 / u])
        s_quiet = diag([1 / (2 * u), u / 2])
        qs = mul(q_quiet, s_quiet)
        p_quiet = mul(transpose(qs), qs)
        pi_quiet = mul(mul(transpose(binv), p_quiet), binv)
        h_quiet = add(mul(mul(transpose(b), diag([-1, 1])), b), p_quiet)
        quiet_trace.append(float(pi_quiet[0][0] + pi_quiet[1][1]))
        quiet_modulation.append(terminal_phi(h_quiet) - math.log(float(u)))

    checks = {
        "O1_nonidentity_overlap_h": h_a_direct == h_a_overlap,
        "O1_nonidentity_overlap_dh": dh_a_direct == dh_a_overlap,
        "O1_nonidentity_overlap_V": v_a == mul(v, r),
        "O2_shared_h00": h1[0][0] == h2[0][0] == -1,
        "O2_different_phi": abs(terminal_phi(h1) - terminal_phi(h2)) > 0.1,
        "O2_regular": h1[0][0] < 0 and det2(h1) < 0 and h2[0][0] < 0 and det2(h2) < 0,
        "O3_reset_nonidentity": middle != diag([1, 1]),
        "O3_reset_changes_composite": with_reset != without_reset,
        "joint_Gram_rank_four": rank(k) == 4,
        "joint_Gram_det_zero": determinant(k) == 0,
        "joint_Gram_inertia": inertia == {"negative": 1, "positive": 3, "zero": 1},
        "flat_trace_constant": max(flat_trace) - min(flat_trace) < 1e-14,
        "flat_modulation_constant": max(flat_modulation) - min(flat_modulation) < 1e-14,
        "monotone_trace_strict": all(a < b for a, b in zip(monotone_trace, monotone_trace[1:])),
        "monotone_modulation_strict": all(a < b for a, b in zip(monotone_modulation, monotone_modulation[1:])),
        "quiet_trace_middle_lower": quiet_trace[2] < quiet_trace[1] and quiet_trace[2] < quiet_trace[3],
        "quiet_modulation_middle_lower_than_sampled_ends": quiet_modulation[2] < quiet_modulation[0] and quiet_modulation[2] < quiet_modulation[3],
    }
    passed = all(checks.values())
    result = {
        "schema": "udt.overlapping_pair_live_compatibility.independent.v1",
        "method": "standalone stdlib Fraction matrices plus Numpy inertia; no production imports",
        "checks": checks,
        "passed": passed,
        "O1_t": str(t),
        "joint_Gram": {"rank": rank(k), "determinant": str(determinant(k)), "inertia": inertia},
        "samples_t": [str(x) for x in samples],
        "flat_trace": flat_trace,
        "flat_modulation": flat_modulation,
        "monotone_trace": monotone_trace,
        "monotone_modulation": monotone_modulation,
        "quiet_trace": quiet_trace,
        "quiet_modulation": quiet_modulation,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
