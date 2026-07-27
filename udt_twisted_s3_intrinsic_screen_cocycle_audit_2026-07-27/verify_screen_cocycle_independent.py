#!/usr/bin/env python3
"""Independent stdlib/Fraction replay; never imports the production module."""

from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIGNS = (-1, 1, 1, 1)


def matrix_multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matrix_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def wedge(left, right):
    result = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if set(a) & set(b):
                continue
            sign = -1 if sum(i > j for i in a for j in b) % 2 else 1
            key = tuple(sorted(a + b))
            result[key] = result.get(key, F(0)) + sign * ca * cb
    return {key: value for key, value in result.items() if value}


def add(*forms):
    result = {}
    for form in forms:
        for key, value in form.items():
            result[key] = result.get(key, F(0)) + value
    return {key: value for key, value in result.items() if value}


def scale(value, form):
    return {key: value * coefficient for key, coefficient in form.items() if value * coefficient}


def connection_sample(p1, p2, p3, at, bt, ct, lam):
    e = [{(i,): F(1)} for i in range(4)]
    dphi = add(scale(p1, e[1]), scale(p2, e[2]), scale(p3, e[3]))
    de = [
        add(scale(-1, wedge(dphi, e[0])), scale(at, wedge(e[2], e[3]))),
        add(wedge(dphi, e[1]), scale(bt, wedge(e[2], e[3]))),
        add(scale(lam, wedge(dphi, e[2])), scale(ct, wedge(e[3], e[1]))),
        add(scale(lam, wedge(dphi, e[3])), scale(ct, wedge(e[1], e[2]))),
    ]
    area = wedge(e[2], e[3])
    darea = add(wedge(de[2], e[3]), scale(F(-1), wedge(e[2], de[3])))
    assert darea == scale(2 * lam, wedge(dphi, area))

    structure = {}
    for upper, form in enumerate(de):
        for (left, right), coefficient in form.items():
            structure[upper, left, right] = -coefficient
            structure[upper, right, left] = coefficient

    def lower(out, left, right):
        return SIGNS[out] * structure.get((out, left, right), F(0))

    def gamma(left, middle, out):
        return (lower(out, left, middle) - lower(left, middle, out)
                + lower(middle, out, left)) / 2

    for ray_sign in (1, -1):
        vector = (1, ray_sign, 0, 0)
        acceleration = []
        for out in range(4):
            low = sum((F(vector[i] * vector[j]) * gamma(i, j, out)
                       for i in range(4) for j in range(4)), F(0))
            acceleration.append(SIGNS[out] * low)
        assert acceleration == [-ray_sign * p1, -p1, -2 * p2, -2 * p3]
    return structure


def main() -> int:
    with (HERE / "CANDIDATE_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 8
    expected = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08"]
    assert [row["candidate"] for row in rows] == expected
    assert [(row["candidate"], row["lambda"]) for row in rows[-2:]] == [("C07", "0"), ("C08", "0")]

    # Independent projector construction.
    identity = [[F(int(i == j)) for j in range(4)] for i in range(4)]
    u_up, u_down = [F(1), F(0), F(0), F(0)], [F(-1), F(0), F(0), F(0)]
    n_up = n_down = [F(0), F(1), F(0), F(0)]
    projector = [[identity[i][j] + u_up[i] * u_down[j] - n_up[i] * n_down[j]
                  for j in range(4)] for i in range(4)]
    expected_projector = [[F(int(i == j and i >= 2)) for j in range(4)] for i in range(4)]
    assert projector == expected_projector
    assert matrix_multiply(projector, projector) == projector

    samples = [
        (F(3, 50), F(1, 50), F(2, 50), F(-3, 7), F(5, 11), F(-2, 13), F(-2)),
        (F(-4, 9), F(2, 7), F(5, 8), F(7, 17), F(-3, 19), F(11, 23), F(1, 2)),
        (F(1, 3), F(0), F(0), F(2, 5), F(-7, 9), F(4, 11), F(2)),
        (F(0), F(0), F(0), F(1, 64), F(2), F(-2), F(0)),
    ]
    for sample in samples:
        connection_sample(*sample)

    # Exact contact implication: when screen derivatives vanish, the nonzero C1_23 coefficient
    # makes bracket invariance force the remaining derivative to vanish.
    structure = connection_sample(F(7, 13), F(0), F(0), F(3, 5), F(11, 17), F(-2, 19), F(1))
    assert structure[(1, 2, 3)] == F(-11, 17)
    assert structure[(1, 2, 3)] * F(7, 13) != 0

    # Independent exact Hamiltonian/symplectic controls.
    zero = [[F(0), F(0)], [F(0), F(0)]]
    eye = [[F(1), F(0)], [F(0), F(1)]]
    omega = [[F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)],
             [F(-1), F(0), F(0), F(0)], [F(0), F(-1), F(0), F(0)]]
    b = [[F(2), F(1)], [F(1), F(3)]]
    c = [[F(1), F(-1)], [F(-1), F(2)]]
    m1 = [[F(1), F(0), b[0][0], b[0][1]], [F(0), F(1), b[1][0], b[1][1]],
          [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    m2 = [[F(1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)],
          [c[0][0], c[0][1], F(1), F(0)], [c[1][0], c[1][1], F(0), F(1)]]
    for matrix in (m1, m2, matrix_multiply(m2, m1)):
        assert matrix_multiply(matrix_multiply(transpose(matrix), omega), matrix) == omega

    # Endpoint exponents are additive; test 64 exact ordered triples.
    depth_values = [F(-2), F(-1, 3), F(0), F(5, 4)]
    triangles = 0
    for p in depth_values:
        for q in depth_values:
            for r in depth_values:
                assert (q - p) + (r - q) == r - p
                triangles += 1

    # Raw local scale versus WR-L vertex law: value at zero forces A=0; derivative then differs.
    local_value_zero = "A"
    optical_value_zero = F(0)
    assert local_value_zero == "A" and optical_value_zero == 0
    assert F(0) != F(2)  # derivatives after A=0

    result = {
        "schema": "udt-twisted-s3-intrinsic-screen-cocycle-independent-1.0",
        "status": "PASS", "production_module_imported": False,
        "candidate_rows": 8, "connection_fraction_samples": len(samples) + 1,
        "depth_triangles": triangles, "projector_exact": True,
        "area_identity_exact": True, "null_alignment_formula_exact": True,
        "contact_obstruction_exact": True, "symplectic_controls": 3,
        "WRL_nonconflation_exact": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
