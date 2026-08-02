#!/usr/bin/env python3
"""Independent high-precision reconstruction; does not import production code."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import mpmath as mp
import sympy as sp


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "udt_intrinsic_general_screen_neighborhood_audit_2026-08-02"
POINT_SPECS = {
    "p1": ((1, 5), (1, 7), (1, 11)),
    "p2": ((1, 3), (-1, 5), (1, 7)),
}
FULL_IDS = ("C04", "C08", "C09", "C10", "C16", "C17")


def read_tsv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def omega_numeric(candidate, x, y, z):
    rho2 = x*x + y*y + z*z
    denominator = 1 + rho2
    q0, q1, q2, q3 = (
        (1-rho2)/denominator,
        2*x/denominator,
        2*y/denominator,
        2*z/denominator,
    )
    primary_u = 3 + q0*q0 + 2*q1*q1 + 4*q2*q2 + 8*q3*q3
    u = primary_u if candidate["u_profile"] == "U" else mp.mpf(4)
    v0 = q0*q0 + 3*q1*q1 + 7*q2*q2 + 9*q3*q3
    r0 = 2*q0*q0 + 5*q1*q1 + 11*q2*q2 + 13*q3*q3
    b0 = q0*q1 + 2*q0*q2 + 3*q0*q3 + 5*q1*q2 + 7*q1*q3 + 11*q2*q3
    v = {
        "ONE": mp.mpf(1), "TWO": mp.mpf(2), "U": u,
        "V_EPS": 1 + v0/10, "ZERO": mp.mpf(0),
    }[candidate["V_profile"]]
    r = {"ONE": mp.mpf(1), "R_EPS": 1 + r0/10}[candidate["r_profile"]]
    b = {"ZERO": mp.mpf(0), "B_EPS": b0/10}[candidate["b_profile"]]
    area = u**int(candidate["lambda"])*v

    f12 = q0*q1*q1 + 3*q0*q2*q2 + 2*q1*q2*q3
    f13 = q0*q0*q1 + 3*q0*q2*q3 - 2*q1*q2*q2
    f23 = 3*q0*q0*q2 - q0*q1*q3 + 2*q1*q1*q2
    root_area, root_u = mp.sqrt(area), mp.sqrt(u)
    nraw = (
        f12/area,
        -(b*f13-r*f23)/(root_area*root_u),
        -f13/(root_area*r*root_u),
    )
    nlength = mp.sqrt(sum(value*value for value in nraw))
    n = tuple(value/nlength for value in nraw)

    d2 = denominator*denominator
    sigma1 = (
        2*(x*x-y*y-z*z+1)/d2,
        4*(x*y+z)/d2,
        4*(x*z-y)/d2,
    )
    sigma2 = (
        4*(x*y-z)/d2,
        -2*(x*x-y*y+z*z-1)/d2,
        4*(x+y*z)/d2,
    )
    theta2 = tuple(root_area*(r*sigma1[i]+b*sigma2[i]) for i in range(3))
    theta3 = tuple(root_area*sigma2[i]/r for i in range(3))
    q_t = 2*int(candidate["a"])/(root_u*area)
    return tuple(q_t*(n[2]*theta2[i]-n[1]*theta3[i])/2 for i in range(3))


def curvature_numeric(candidate, point):
    x, y, z = point
    d_x_omega_y = mp.diff(lambda xx: omega_numeric(candidate, xx, y, z)[1], x)
    d_y_omega_x = mp.diff(lambda yy: omega_numeric(candidate, x, yy, z)[0], y)
    d_x_omega_z = mp.diff(lambda xx: omega_numeric(candidate, xx, y, z)[2], x)
    d_z_omega_x = mp.diff(lambda zz: omega_numeric(candidate, x, y, zz)[0], z)
    d_y_omega_z = mp.diff(lambda yy: omega_numeric(candidate, x, yy, z)[2], y)
    d_z_omega_y = mp.diff(lambda zz: omega_numeric(candidate, x, y, zz)[1], z)
    return (
        d_x_omega_y-d_y_omega_x,
        d_x_omega_z-d_z_omega_x,
        d_y_omega_z-d_z_omega_y,
    )


def exact_to_mp(text):
    return mp.mpf(str(sp.N(sp.sympify(text), 90)))


def close(left, right):
    scale = max(mp.mpf(1), abs(left), abs(right))
    return abs(left-right) <= mp.mpf("1e-60")*scale


def main():
    mp.mp.dps = 90
    points = {
        point_id: tuple(mp.mpf(numerator)/denominator for numerator, denominator in spec)
        for point_id, spec in POINT_SPECS.items()
    }
    candidates = {row["candidate_id"]: row for row in read_tsv(PARENT / "CANDIDATE_UNIVERSE.tsv")}
    recorded = {(row["candidate_id"], row["point_id"]): row for row in read_tsv(HERE / "CONNECTION_POINTS.tsv")}
    assert len(recorded) == 12

    comparisons = 0
    nonzero = 0
    signatures = {point_id: [] for point_id in points}
    recomputed = {}
    for candidate_id in FULL_IDS:
        for point_id, point in points.items():
            omega = omega_numeric(candidates[candidate_id], *point)
            curvature = curvature_numeric(candidates[candidate_id], point)
            row = recorded[(candidate_id, point_id)]
            recorded_omega = tuple(exact_to_mp(item) for item in row["omega_xyz"].split(";"))
            recorded_curvature = tuple(exact_to_mp(item) for item in row["Omega_xy_xz_yz"].split(";"))
            assert all(close(a, b) for a, b in zip(omega, recorded_omega))
            assert all(close(a, b) for a, b in zip(curvature, recorded_curvature))
            assert any(abs(value) > mp.mpf("1e-70") for value in curvature)
            comparisons += 6
            nonzero += 1
            recomputed[(candidate_id, point_id)] = (omega, curvature)
            if candidate_id in ("C04", "C08", "C09", "C10"):
                signatures[point_id].append(tuple(mp.nstr(value, 70) for value in curvature))

    for point_id in points:
        assert len(set(signatures[point_id])) == 4
        for target, factor in (("C16", 4), ("C17", 5)):
            for field_index in (0, 1):
                base = recomputed[("C08", point_id)][field_index]
                test = recomputed[(target, point_id)][field_index]
                assert all(close(value, factor*reference) for value, reference in zip(test, base))

    # Separately reconstructed exact local topology algebra.
    a, b, c, d = sp.symbols("a b c d", real=True)
    matrices = (
        sp.Matrix([[a*a, 3*a*d], [-a*d, 3*a*a]]),
        sp.Matrix([[b*b, 2*b*d], [-b*d, 2*b*b]]),
        sp.Matrix([[3*c*c, 2*c*d], [3*c*d, -2*c*c]]),
    )
    assert [sp.factor(matrix.det()) for matrix in matrices] == [
        3*a*a*(a*a+d*d), 2*b*b*(b*b+d*d), -6*c*c*(c*c+d*d),
    ]
    px, py, pz = sp.symbols("px py pz")
    assert sp.solve([py*pz, px*pz, px*py], [px, py, pz], dict=True) == [
        {px: 0, py: 0}, {px: 0, pz: 0}, {py: 0, pz: 0},
    ]

    result = {
        "schema": "udt-defect-transport-independent-1.0",
        "status": "PASS_INDEPENDENT_HIGH_PRECISION",
        "method": "separate_mpmath_90_digit_differentiation_plus_exact_local_algebra",
        "production_module_imported": False,
        "point_components_compared": comparisons,
        "nonzero_curvature_points": nonzero,
        "registered_screen_lambda_curvature_coordinate_triples_distinct_at_p1_p2": True,
        "twist_scaling_reproduced": {"C16_over_C08": 4, "C17_over_C08": 5},
        "edge_determinants_reproduced": True,
        "pole_six_axis_zero_set_reproduced": True,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
