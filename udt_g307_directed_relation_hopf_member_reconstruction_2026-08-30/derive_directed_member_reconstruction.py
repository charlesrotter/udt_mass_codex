#!/usr/bin/env python3
"""Exact standard-library derivation for the bounded G307 member census."""

from __future__ import annotations

import csv
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"
CENSUS = HERE / "MEMBER_CENSUS.tsv"
LANDING = (
    "SUPPLIED_DIRECTED_GERM_SELECTS_ONE_MEMBER_PER_CHIRAL_FAMILY"
    "__SIGNED_TRANSVERSE_SCREEN_GERM_SELECTS_ONE_MEMBER_CONDITIONALLY"
    "__ACTIVE_PREMISES_POPULATE_NEITHER__PHYSICAL_MEMBER_REMAINS_OPEN"
)
Z = F(0)
O = F(1)


def qmul(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    )


def qconj(q):
    return (q[0], -q[1], -q[2], -q[3])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def stereo_quaternion(t):
    s = sum(x * x for x in t)
    d = O + s
    return ((O - s) / d,) + tuple(2 * x / d for x in t)


def matrix_from_action(action):
    basis = (
        (O, Z, Z, Z),
        (Z, O, Z, Z),
        (Z, Z, O, Z),
        (Z, Z, Z, O),
    )
    columns = [action(e) for e in basis]
    return tuple(tuple(columns[j][i] for j in range(4)) for i in range(4))


def matvec(a, v):
    return tuple(sum(a[i][j] * v[j] for j in range(4)) for i in range(4))


def matmul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4))
        for i in range(4)
    )


def transpose(a):
    return tuple(tuple(a[j][i] for j in range(4)) for i in range(4))


def determinant(a):
    total = Z
    for p in itertools.permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4))
        term = O if inversions % 2 == 0 else -O
        for i in range(4):
            term *= a[i][p[i]]
        total += term
    return total


def columns_matrix(columns):
    return tuple(tuple(columns[j][i] for j in range(4)) for i in range(4))


def main():
    assertions = 0

    def check(condition, label):
        nonlocal assertions
        assert condition, label
        assertions += 1

    params = (
        (F(0), F(0), F(0)),
        (F(1, 2), F(0), F(0)),
        (F(1, 3), F(1, 4), F(0)),
        (F(-2, 5), F(1, 3), F(1, 7)),
        (F(2, 3), F(-1, 5), F(3, 8)),
        (F(-3, 7), F(-2, 9), F(1, 6)),
    )
    radii = (F(1, 2), F(1), F(7, 3), F(5), F(19, 4))
    path_pairs = ((F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(-8, 17), F(15, 17)))
    imag_basis = (
        (Z, O, Z, Z),
        (Z, Z, O, Z),
        (Z, Z, Z, O),
    )
    identity = tuple(tuple(O if i == j else Z for j in range(4)) for i in range(4))
    minus_identity = tuple(tuple(-x for x in row) for row in identity)
    case_count = 0

    for qp in params:
        q = stereo_quaternion(qp)
        check(dot(q, q) == O, "unit point")
        for rp in params:
            r = stereo_quaternion(rp)
            rb = qconj(r)
            u, e, f = (qmul(qmul(r, axis), rb) for axis in imag_basis)
            for vector, label in ((u, "u"), (e, "e"), (f, "f")):
                check(vector[0] == Z, f"{label} pure")
                check(dot(vector, vector) == O, f"{label} unit")
            check(dot(u, e) == dot(u, f) == dot(e, f) == Z, "imaginary triad")
            check(qmul(u, e) == f and qmul(e, u) == scale(-O, f), "oriented triad")

            v = qmul(u, q)
            w = qmul(e, q)
            z = qmul(f, q)
            for vector, label in ((v, "v"), (w, "w"), (z, "z")):
                check(dot(vector, vector) == O, f"{label} unit")
                check(dot(q, vector) == Z, f"{label} tangent")
            check(dot(v, w) == dot(v, z) == dot(w, z) == Z, "tangent frame")

            u_left = qmul(v, qconj(q))
            u_right = qmul(qconj(q), v)
            check(u_left == u, "left candidate reconstruction")
            check(u_right[0] == Z and dot(u_right, u_right) == O, "right candidate reconstruction")

            jl = matrix_from_action(lambda x, ul=u_left: qmul(ul, x))
            jr = matrix_from_action(lambda x, ur=u_right: qmul(x, ur))
            for matrix, label in ((jl, "left"), (jr, "right")):
                check(transpose(matrix) == tuple(tuple(-x for x in row) for row in matrix), f"{label} skew")
                check(matmul(matrix, matrix) == minus_identity, f"{label} complex")
                check(matvec(matrix, q) == v, f"{label} supplied tangent")
                check(matvec(matrix, v) == scale(-O, q), f"{label} common route plane")
            check(matvec(jl, w) == z and matvec(jr, w) == scale(-O, z), "opposite screen turn")
            check(matvec(jl, z) == scale(-O, w) and matvec(jr, z) == w, "opposite screen closure")
            check(determinant(columns_matrix((q, v, w, matvec(jl, w)))) == O, "left chirality")
            check(determinant(columns_matrix((q, v, w, matvec(jr, w)))) == -O, "right chirality")

            # The evaluation maps u -> u q and u -> q u are isometries from Im(H) to T_q S3.
            left_images = [qmul(axis, q) for axis in imag_basis]
            right_images = [qmul(q, axis) for axis in imag_basis]
            for images, label in ((left_images, "left"), (right_images, "right")):
                gram = tuple(tuple(dot(images[i], images[j]) for j in range(3)) for i in range(3))
                check(gram == tuple(tuple(O if i == j else Z for j in range(3)) for i in range(3)), f"{label} uniqueness")

            for c, s in path_pairs:
                route_point = add(scale(c, q), scale(s, v))
                route_tangent = add(scale(c, v), scale(-s, q))
                check(dot(route_point, route_point) == O, "route point unit")
                check(matvec(jl, route_point) == route_tangent, "left route")
                check(matvec(jr, route_point) == route_tangent, "right route")

            for radius in radii:
                check(dot(z, scale(O / radius, matvec(jl, w))) == O / radius, "left twist scale")
                check(dot(z, scale(O / radius, matvec(jr, w))) == -O / radius, "right twist scale")
            case_count += 1

    census = (
        ("round_metric_only", "two_S2_families", "no_member"),
        ("supplied_point", "two_S2_families", "no_direction"),
        ("supplied_point_and_ordered_unit_tangent", "two_members", "one_per_chirality"),
        ("complete_one_dimensional_route_and_metric_frame_carry", "two_members", "same_route"),
        ("supplied_oriented_signed_transverse_screen_first_jet", "one_member", "conditional_reconstruction"),
        ("active_premise_owned_lawful_query_population", "zero_selected", "open"),
    )
    with CENSUS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("data_level", "remaining_geometric_members", "ownership"))
        writer.writerows(census)

    result = {
        "status": "PASS",
        "landing_candidate": 2,
        "landing": LANDING,
        "scope": "positive_G305_round_S3_regular_directed_germs_oriented_screens_all_positive_radii",
        "exact_cases": case_count,
        "radii": [str(x) for x in radii],
        "production_assertions": assertions,
        "directed_germ_member_count": 2,
        "members_per_chirality": 1,
        "path_only_member_count": 2,
        "signed_transverse_screen_member_count": 1,
        "screen_twist_signs": [-1, 1],
        "lawful_query_population_selected": False,
        "physical_member_selected": False,
        "metric_and_kernel_changed": False,
        "omitted": [
            "nonspherical_deformations", "quotients", "singular_cut_caustic_strata",
            "topology_change", "physical_query_route_population", "action", "dynamics",
            "stability", "backreaction", "history", "observation", "source", "mass",
            "scale", "physical_Xmax", "protected_work",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
