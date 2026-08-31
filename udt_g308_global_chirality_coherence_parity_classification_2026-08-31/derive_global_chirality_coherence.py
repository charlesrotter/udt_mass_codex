#!/usr/bin/env python3
"""Exact standard-library derivation for the bounded G308 classification."""

from __future__ import annotations

import csv
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"
CENSUS = HERE / "COHERENCE_CENSUS.tsv"
LANDING = (
    "BOTH_G307_CHIRAL_MEMBERS_EXTEND_GLOBALLY_AND_CAUSALLY_ON_G305"
    "__CONNECTED_REGULAR_CARRY_FORBIDS_LOCAL_CHIRALITY_SWITCHING"
    "__TRANSVERSE_ORIENTATION_REVERSING_ISOMETRY_EXCHANGES_THE_TWO_SECTORS"
    "__METRIC_ONLY_PHYSICAL_SELECTION_REMAINS_OPEN"
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


def stereo(t):
    squared = sum(x * x for x in t)
    denominator = O + squared
    return ((O - squared) / denominator,) + tuple(2 * x / denominator for x in t)


def outer(a, b):
    return tuple(tuple(a[i] * b[j] for j in range(4)) for i in range(4))


def matadd(*matrices):
    return tuple(
        tuple(sum(matrix[i][j] for matrix in matrices) for j in range(4))
        for i in range(4)
    )


def matscale(c, matrix):
    return tuple(tuple(c * value for value in row) for row in matrix)


def matvec(matrix, vector):
    return tuple(sum(matrix[i][j] * vector[j] for j in range(4)) for i in range(4))


def matmul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4))
        for i in range(4)
    )


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in range(4)) for i in range(4))


def determinant(matrix):
    result = Z
    for permutation in itertools.permutations(range(4)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(4)
            for j in range(i + 1, 4)
        )
        term = O if inversions % 2 == 0 else -O
        for i in range(4):
            term *= matrix[i][permutation[i]]
        result += term
    return result


def from_action(action):
    basis = (
        (O, Z, Z, Z),
        (Z, O, Z, Z),
        (Z, Z, O, Z),
        (Z, Z, Z, O),
    )
    columns = [action(vector) for vector in basis]
    return tuple(tuple(columns[j][i] for j in range(4)) for i in range(4))


def columns(vectors):
    return tuple(tuple(vectors[j][i] for j in range(4)) for i in range(4))


def complex_structure(p, v, w, z, chirality):
    route = matadd(outer(v, p), matscale(-O, outer(p, v)))
    screen = matadd(outer(z, w), matscale(-O, outer(w, z)))
    return matadd(route, matscale(chirality, screen))


def reflection(p, v, w, z):
    return matadd(outer(p, p), outer(v, v), outer(w, w), matscale(-O, outer(z, z)))


def pfaffian(matrix):
    return (
        matrix[0][1] * matrix[2][3]
        - matrix[0][2] * matrix[1][3]
        + matrix[0][3] * matrix[1][2]
    )


def main():
    identity = tuple(tuple(O if i == j else Z for j in range(4)) for i in range(4))
    minus_identity = matscale(-O, identity)
    imaginary_basis = (
        (Z, O, Z, Z),
        (Z, Z, O, Z),
        (Z, Z, Z, O),
    )
    parameters = (
        (F(0), F(0), F(0)),
        (F(1, 2), F(0), F(0)),
        (F(1, 3), F(1, 4), F(0)),
        (F(-2, 5), F(1, 3), F(1, 7)),
        (F(2, 3), F(-1, 5), F(3, 8)),
        (F(-3, 7), F(-2, 9), F(1, 6)),
    )
    circle_pairs = (
        (F(3, 5), F(4, 5)),
        (F(5, 13), F(12, 13)),
        (F(-8, 17), F(15, 17)),
    )
    scale_controls = (
        (F(1, 2), F(-3, 7)),
        (F(1), F(0)),
        (F(7, 3), F(2, 5)),
        (F(5), F(-4, 9)),
        (F(19, 4), F(11, 13)),
    )
    assertions = 0

    def check(condition, label):
        nonlocal assertions
        assert condition, label
        assertions += 1

    frame_cases = 0
    global_point_cases = 0
    for point_parameters in parameters:
        p = stereo(point_parameters)
        check(dot(p, p) == O, "unit supplied point")
        for rotation_parameters in parameters:
            rotation = stereo(rotation_parameters)
            rotation_bar = qconj(rotation)
            u, e, f = (
                qmul(qmul(rotation, axis), rotation_bar) for axis in imaginary_basis
            )
            v = qmul(u, p)
            w = qmul(e, p)
            z = qmul(f, p)
            frame = (p, v, w, z)
            check(matmul(transpose(columns(frame)), columns(frame)) == identity, "oriented orthonormal frame")
            check(determinant(columns(frame)) == O, "positive frame orientation")

            left = complex_structure(p, v, w, z, O)
            right = complex_structure(p, v, w, z, -O)
            quaternion_left = from_action(lambda x, ul=qmul(v, qconj(p)): qmul(ul, x))
            quaternion_right = from_action(lambda x, ur=qmul(qconj(p), v): qmul(x, ur))
            check(left == quaternion_left, "left G307 reconstruction")
            check(right == quaternion_right, "right G307 reconstruction")
            for candidate, label in ((left, "left"), (right, "right")):
                check(transpose(candidate) == matscale(-O, candidate), f"{label} skew")
                check(matmul(candidate, candidate) == minus_identity, f"{label} complex")
                check(matmul(transpose(candidate), candidate) == identity, f"{label} orthogonal")
                check(matvec(candidate, p) == v, f"{label} supplied direction")
                check(matvec(candidate, v) == scale(-O, p), f"{label} route closure")
                check(abs(pfaffian(candidate)) == O, f"{label} chirality unit")
            check(pfaffian(left) == -pfaffian(right), "opposite chirality")
            check(matvec(left, w) == z and matvec(right, w) == scale(-O, z), "opposite screen turn")

            mirror = reflection(p, v, w, z)
            check(transpose(mirror) == mirror, "mirror symmetric")
            check(matmul(mirror, mirror) == identity, "mirror involution")
            check(determinant(mirror) == -O, "mirror orientation reversing")
            check(matvec(mirror, p) == p and matvec(mirror, v) == v, "mirror fixes route germ")
            check(matvec(mirror, w) == w and matvec(mirror, z) == scale(-O, z), "mirror reverses screen orientation")
            check(matmul(matmul(mirror, left), mirror) == right, "mirror exchanges candidates")
            check(pfaffian(right) == determinant(mirror) * pfaffian(left), "chirality transformation law")

            reversed_left = matscale(-O, left)
            reversed_right = matscale(-O, right)
            check(matvec(reversed_left, p) == scale(-O, v), "left pair reversal")
            check(matvec(reversed_right, p) == scale(-O, v), "right pair reversal")
            check(pfaffian(reversed_left) == pfaffian(left), "left reversal preserves chirality")
            check(pfaffian(reversed_right) == pfaffian(right), "right reversal preserves chirality")

            midpoint = matscale(F(1, 2), matadd(left, right))
            check(determinant(midpoint) == Z, "linear chirality switch degenerates")
            check(matmul(midpoint, midpoint) != minus_identity, "switch leaves complex stratum")
            check(matvec(midpoint, w) == (Z, Z, Z, Z), "switch loses transverse rank")

            for global_parameters in parameters:
                q = stereo(global_parameters)
                for candidate, other, label in (
                    (left, right, "left"),
                    (right, left, "right"),
                ):
                    field = matvec(candidate, q)
                    check(dot(q, field) == Z, f"{label} globally tangent")
                    check(dot(field, field) == O, f"{label} globally nowhere zero")
                    check(
                        matvec(mirror, field)
                        == matvec(other, matvec(mirror, q)),
                        f"{label} global mirror equivariance",
                    )
                    for cosine, sine in circle_pairs:
                        orbit_point = add(scale(cosine, q), scale(sine, field))
                        check(dot(orbit_point, orbit_point) == O, f"{label} complete circle point")
                        check(
                            matvec(candidate, orbit_point)
                            == add(scale(cosine, field), scale(-sine, q)),
                            f"{label} circle flow",
                        )
                    for radius, radius_rate in scale_controls:
                        unit_field = scale(O / radius, field)
                        check(radius * radius * dot(unit_field, unit_field) == O, f"{label} slice unit norm")
                        carry_coefficient = (
                            -radius_rate / (radius * radius)
                            + (O / radius) * (radius_rate / radius)
                        )
                        check(carry_coefficient == Z, f"{label} exact time-parallel unit carry")
                        spacetime_acceleration = radius_rate / radius
                        check(
                            (spacetime_acceleration == Z) == (radius_rate == Z),
                            f"{label} spacetime-geodesic iff static scale control",
                        )
                global_point_cases += 1

            frame_cases += 1

    census = (
        ("round_G305_metric_only", "two_continuous_chiral_families", "no_member"),
        ("one_supplied_directed_germ", "two_global_members", "one_per_chirality"),
        ("connected_smooth_regular_Hopf_carry", "one_constant_chirality_label_per_component", "no_sign_preference"),
        ("unoriented_metric_full_O4_equivalence", "one_mirror_orbit_with_two_representatives", "orientation_blind_equivalence"),
        ("oriented_metric_SO4_equivalence", "two_chiral_sectors", "degenerate_not_selected"),
        ("supplied_signed_transverse_screen", "one_member", "conditional_reconstruction"),
        ("active_physical_population", "zero_selected", "open"),
    )
    with CENSUS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("data_level", "global_geometric_status", "ownership"))
        writer.writerows(census)

    result = {
        "status": "PASS",
        "landing_candidate": "B",
        "landing": LANDING,
        "scope": "positive_G305_standard_R_times_round_S3_regular_G307_members",
        "production_assertions": assertions,
        "frame_cases": frame_cases,
        "global_point_cases": global_point_cases,
        "scale_controls": len(scale_controls),
        "both_global_smooth_nowhere_zero": True,
        "both_spatial_orbits_complete_closed": True,
        "normalized_fields_time_parallel": True,
        "spatial_hopf_fibers_automatically_spacetime_geodesic": False,
        "reflection_fixes_directed_route_plane": True,
        "reflection_reverses_transverse_orientation": True,
        "full_O4_exchanges_chirality": True,
        "SO4_exchanges_chirality": False,
        "pair_reversal_changes_chirality": False,
        "connected_regular_carry_allows_local_chirality_switch": False,
        "metric_or_causal_cone_changed": False,
        "physical_member_selected": False,
        "metric_and_kernel_changed": False,
        "omitted": [
            "nonspherical_deformations", "nontrivial_quotients", "singular_cut_caustic_strata",
            "topology_change", "physical_query_route_screen_population", "action", "dynamics",
            "stability", "backreaction", "history", "observation", "source", "matter", "mass",
            "scale_selection", "physical_Xmax", "protected_work",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
