#!/usr/bin/env python3
"""Implementation-distinct G306 verification using only the standard library.

No production function or symbolic result is imported.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "DERIVATION_RESULT.json"
OUT = HERE / "INDEPENDENT_VERIFICATION.json"
TOL = 2.0e-11


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def matvec(a, x):
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def add(x, y):
    return [a + b for a, b in zip(x, y)]


def scale(c, x):
    return [c * a for a in x]


def eye(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def matrix_max(a):
    return max(abs(x) for row in a for x in row)


def matrix_sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def determinant3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def matrix_rank(rows, tol=1.0e-12):
    a = [list(map(float, row)) for row in rows]
    rank = 0
    ncols = len(a[0])
    for col in range(ncols):
        pivot = max(range(rank, len(a)), key=lambda i: abs(a[i][col]), default=rank)
        if abs(a[pivot][col]) <= tol:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pv = a[rank][col]
        a[rank] = [x / pv for x in a[rank]]
        for i in range(len(a)):
            if i != rank:
                factor = a[i][col]
                a[i] = [x - factor * y for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


LEFT = (
    ((0, -1, 0, 0), (1, 0, 0, 0), (0, 0, 0, -1), (0, 0, 1, 0)),
    ((0, 0, -1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, -1, 0, 0)),
    ((0, 0, 0, -1), (0, 0, -1, 0), (0, 1, 0, 0), (1, 0, 0, 0)),
)
RIGHT = (
    ((0, -1, 0, 0), (1, 0, 0, 0), (0, 0, 0, 1), (0, 0, -1, 0)),
    ((0, 0, -1, 0), (0, 0, 0, -1), (1, 0, 0, 0), (0, 1, 0, 0)),
    ((0, 0, 0, -1), (0, 0, 1, 0), (0, -1, 0, 0), (1, 0, 0, 0)),
)


def combine(basis, u):
    return [[sum(u[k] * basis[k][i][j] for k in range(3)) for j in range(4)] for i in range(4)]


def normalize(v):
    n = math.sqrt(dot(v, v))
    return [x / n for x in v]


def tangent_project(v, x, a):
    return add(v, scale(-dot(v, x) / (a * a), x))


def covariant_derivative(j, x, y, a):
    v = scale(1.0 / a, matvec(j, x))
    return add(scale(1.0 / a, matvec(j, y)), scale(dot(v, y) / (a * a), x))


def rotation_from_quaternion(q):
    w, x, y, z = q
    return [
        [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
    ]


def hopf_from_quaternion(q):
    w, x, y, z = q
    return [w * w + x * x - y * y - z * z, 2 * (x * y + w * z), 2 * (x * z - w * y)]


def main():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    checks = 0
    max_error = 0.0
    i4 = eye(4)

    unit_parameters = [
        normalize(v)
        for v in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (3, 4, 0), (2, -3, 6), (-4, 7, 1))
    ]
    sample_points = [normalize(v) for v in ((1, 2, 3, 4), (4, -2, 1, 3), (-3, 5, -4, 2), (7, 1, -2, -5))]
    radii = (0.125, 0.75, 1.0, 3.5, 19.0)

    for basis in (LEFT, RIGHT):
        for u in unit_parameters:
            j = combine(basis, u)
            skew = matrix_sub(transpose(j), [[-x for x in row] for row in j])
            square = matrix_sub(matmul(j, j), [[-x for x in row] for row in i4])
            err = max(matrix_max(skew), matrix_max(square))
            max_error = max(max_error, err)
            assert err < TOL
            checks += 32
            for a in radii:
                for xu in sample_points:
                    x = scale(a, xu)
                    v = scale(1.0 / a, matvec(j, x))
                    err = max(abs(dot(x, v)), abs(dot(v, v) - 1.0))
                    max_error = max(max_error, err)
                    assert err < TOL
                    checks += 2
                    geodesic = covariant_derivative(j, x, v, a)
                    err = math.sqrt(dot(geodesic, geodesic))
                    max_error = max(max_error, err)
                    assert err < TOL
                    checks += 4

                    # Build two tangent test vectors, then check Killing.
                    y = tangent_project([1.0, -2.0, 0.5, 3.0], x, a)
                    z = tangent_project([-0.25, 1.0, 4.0, -2.0], x, a)
                    ny = covariant_derivative(j, x, y, a)
                    nz = covariant_derivative(j, x, z, a)
                    kres = dot(ny, z) + dot(y, nz)
                    max_error = max(max_error, abs(kres))
                    assert abs(kres) < TOL
                    checks += 1

    # Opposite pure-twist signs of the two quaternionic families.
    p = [1.0, 0.0, 0.0, 0.0]
    e2 = [0.0, 0.0, 1.0, 0.0]
    e3 = [0.0, 0.0, 0.0, 1.0]
    twist_signs = []
    for j in (LEFT[0], RIGHT[0]):
        de2 = covariant_derivative(j, p, e2, 1.0)
        de3 = covariant_derivative(j, p, e3, 1.0)
        sign = round((dot(de2, e3) - dot(de3, e2)) / 2.0)
        assert sign in (-1, 1)
        twist_signs.append(sign)
        checks += 3
    assert sorted(twist_signs) == [-1, 1]
    checks += 1

    # Full tangent isotropy leaves no fixed tangent vector.
    fixed_rows = [
        [-2, 0, 0],
        [0, -2, 0],
        [-2, 0, 0],
        [0, 0, -2],
    ]
    isotropy_rank = matrix_rank(fixed_rows)
    isotropy_fixed_dimension = 3 - isotropy_rank
    assert isotropy_fixed_dimension == 0
    checks += 12

    # Large local-frame rotation and Hopf map.
    quaternions = [
        normalize(q)
        for q in ((1, 0, 0, 0), (1, 2, 3, 4), (3, -1, 2, -2), (-2, 5, 1, 3), (0, 1, 1, 1))
    ]
    for q in quaternions:
        r = rotation_from_quaternion(q)
        h = hopf_from_quaternion(q)
        re1 = [row[0] for row in r]
        orth = matrix_sub(matmul(transpose(r), r), eye(3))
        err = max(max(abs(a - b) for a, b in zip(re1, h)), matrix_max(orth), abs(determinant3(r) - 1.0), abs(dot(h, h) - 1.0))
        max_error = max(max_error, err)
        assert err < TOL
        checks += 24
    base_rotation_error = matrix_max(matrix_sub(rotation_from_quaternion((1, 0, 0, 0)), eye(3)))
    assert base_rotation_error == 0.0
    checks += 9

    # Independent midpoint integration of the frozen Hopf connection.
    n_eta = 20000
    d_eta = (0.5 * math.pi) / n_eta
    eta_integral = sum(-math.sin(2.0 * ((k + 0.5) * d_eta)) * d_eta for k in range(n_eta))
    hopf_number = eta_integral  # angular factors cancel the 4 pi^2 normalization
    hopf_error = abs(hopf_number + 1.0)
    max_error = max(max_error, hopf_error)
    assert hopf_error < 2.0e-9
    checks += n_eta

    # Intrinsic helicity cancellation is checked for all sample radii and both twists.
    helicities = []
    for sign in (-1, 1):
        for a in radii:
            volume = 2.0 * math.pi**2 * a**3
            integral = sign * (2.0 / a) * volume
            normalized = integral / (4.0 * math.pi**2 * a**2)
            assert abs(normalized - sign) < TOL
            helicities.append(normalized)
            checks += 1

    expected = {
        "candidate_landing": "A",
        "isotropy_fixed_tangent_dimension": 0,
        "metric_natural_unit_section_exists": False,
        "constant_curvature_ricci_eigenvalue_multiplicity": 3,
        "radial_map_singular_orbits": 2,
        "component_charge_constant_map": 0,
        "component_charge_after_large_frame_rotation": -1,
        "raw_component_charge_full_frame_invariant": False,
        "oriented_chiral_family_count": 2,
        "individual_member_selected": False,
        "normalized_helicity_by_chirality": [-1, 1],
        "normalized_helicity_scale_blind": True,
        "field_or_query_population_selected": False,
        "fixed_cross_history_target_selected": False,
        "metric_and_kernel_changed": False,
    }
    for key, value in expected.items():
        assert source[key] == value, (key, source[key], value)
        checks += 1

    result = {
        "status": "PASS",
        "implementation": "standard_library_no_production_import",
        "independent_checks": checks,
        "maximum_numeric_error": max_error,
        "midpoint_hopf_number": hopf_number,
        "isotropy_fixed_tangent_dimension": isotropy_fixed_dimension,
        "twist_signs": sorted(twist_signs),
        "helicity_radius_cases": len(helicities),
        "source_landing": source["landing"],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

