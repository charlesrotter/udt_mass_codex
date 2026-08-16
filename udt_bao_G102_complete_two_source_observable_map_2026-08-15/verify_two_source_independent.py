#!/usr/bin/env python3
"""Independent Fraction-only replay of G102 load-bearing finite claims."""

from __future__ import annotations

import json
from fractions import Fraction as F


ETA = (F(-1), F(1), F(1), F(1))


def dot(a, b):
    return sum((ETA[i] * a[i] * b[i] for i in range(4)), F(0))


def scale(a, x):
    return tuple(x * value for value in a)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def pair(v0, v1, known_T, known_L):
    h00 = dot(v0, v0)
    h01 = dot(v0, v1)
    h11 = dot(v1, v1)
    ruler = add(v1, scale(v0, -h01 / h00))
    u = scale(v0, F(1, known_T))
    n = scale(ruler, F(1, known_L))
    det_h = h00 * h11 - h01 * h01
    assert dot(u, u) == -1
    assert dot(u, n) == 0
    assert dot(n, n) == 1
    return {"u": u, "n": n, "phi_argument": (-det_h) / (h00 * h00)}


def bin_id(cosine):
    if cosine > F(1, 2):
        return 0
    if cosine > F(-1, 2):
        return 1
    return 2


def enumerate_auto(points, weights):
    out = [F(0), F(0), F(0)]
    pairs = [(i, j) for i in range(len(points)) for j in range(len(points)) if i < j]
    for i, j in pairs:
        c = sum((points[i][k] * points[j][k] for k in range(2)), F(0))
        out[bin_id(c)] += weights[i] * weights[j]
    return out


def enumerate_cross(a_points, a_weights, b_points, b_weights):
    out = [F(0), F(0), F(0)]
    for i, p in enumerate(a_points):
        for j, q in enumerate(b_points):
            c = sum((p[k] * q[k] for k in range(2)), F(0))
            out[bin_id(c)] += a_weights[i] * b_weights[j]
    return out


def main():
    p1 = pair((F(2), F(0), F(0), F(0)), (F(1), F(3), F(0), F(0)), 2, 3)
    p2 = pair((F(3), F(0), F(0), F(0)), (F(-1), F(3), F(4), F(0)), 3, 5)
    assert p1["u"] == p2["u"]
    assert dot(p1["n"], p2["n"]) == F(3, 5)
    # The observer-local pair metrics are not reused as accumulated redshifts.
    local_phi_arguments = [p1["phi_argument"], p2["phi_argument"]]
    terminal_Z = [2, 3]
    assert local_phi_arguments == [F(9, 4), F(25, 9)]
    assert terminal_Z == [2, 3]

    data = [(F(1), F(0)), (F(3, 5), F(4, 5)), (F(0), F(1)), (F(-1), F(0))]
    dw = [F(1), F(2), F(3), F(4)]
    randoms = [(F(1), F(0)), (F(0), F(-1)), (F(-3, 5), F(4, 5)), (F(-1), F(0)), (F(0), F(1))]
    rw = [F(1)] * 5
    DD = enumerate_auto(data, dw)
    DR = enumerate_cross(data, dw, randoms, rw)
    RR = enumerate_auto(randoms, rw)
    DD_total = F(35)
    DR_total = F(50)
    RR_total = F(10)
    ls = [
        ((DD[i] / DD_total) - 2 * (DR[i] / DR_total) + (RR[i] / RR_total))
        / (RR[i] / RR_total)
        for i in range(3)
    ]

    expected = {
        "DD": [F(8), F(15), F(12)],
        "DR": [F(19), F(18), F(13)],
        "RR": [F(2), F(4), F(4)],
        "LS": [F(-58, 35), F(19, 70), F(39, 70)],
    }
    assert DD == expected["DD"]
    assert DR == expected["DR"]
    assert RR == expected["RR"]
    assert ls == expected["LS"]

    result = {
        "status": "PASS",
        "implementation": "stdlib Fraction only; no sympy or production import",
        "common_observer": True,
        "cos_theta": str(F(3, 5)),
        "observer_local_phi_arguments_not_used_as_redshift": [str(x) for x in local_phi_arguments],
        "terminal_Z_separately_typed": terminal_Z,
        "DD": [str(x) for x in DD],
        "DR": [str(x) for x in DR],
        "RR": [str(x) for x in RR],
        "landy_szalay": [str(x) for x in ls],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
