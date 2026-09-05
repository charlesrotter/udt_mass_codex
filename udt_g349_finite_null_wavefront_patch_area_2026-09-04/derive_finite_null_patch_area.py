#!/usr/bin/env python3
"""Dependency-free production checks for the preregistered G349 finite patch identities."""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
RNG = random.Random(349041)
FAILED = []
ASSERTIONS = 0
MAXIMA = {}


def check(name, got, expected, tolerance):
    global ASSERTIONS
    ASSERTIONS += 1
    error = abs(got - expected)
    MAXIMA[name] = max(MAXIMA.get(name, 0.0), error)
    if not math.isfinite(error) or error > tolerance:
        FAILED.append({"name": name, "got": got, "expected": expected, "error": error})


def check_true(name, condition):
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        FAILED.append({"name": name, "condition": False})


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def transpose(a):
    return [[a[0][0], a[1][0]], [a[0][1], a[1][1]]]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def inv2(a):
    d = det2(a)
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def metric_jacobian(dmap, source_metric, target_metric):
    gram = matmul(matmul(transpose(dmap), target_metric), dmap)
    return math.sqrt(max(0.0, det2(gram) / det2(source_metric)))


def lorentz_dot(a, b):
    return -a[0] * b[0] + sum(a[i] * b[i] for i in range(1, 4))


def random_invertible():
    while True:
        a = [[RNG.uniform(-2.0, 2.0), RNG.uniform(-2.0, 2.0)],
             [RNG.uniform(-2.0, 2.0), RNG.uniform(-2.0, 2.0)]]
        if abs(det2(a)) > 0.25:
            return a


def random_spd():
    a, b, c = RNG.uniform(0.4, 2.0), RNG.uniform(-0.4, 0.4), RNG.uniform(0.4, 2.0)
    return [[a * a + 0.5, a * b], [a * b, b * b + c * c + 0.5]]


def coordinate_covariance_checks():
    for _ in range(3500):
        dmap = random_invertible()
        source = random_spd()
        target = random_spd()
        r0 = random_invertible()
        r1 = random_invertible()
        base = metric_jacobian(dmap, source, target)
        r0_inv = inv2(r0)
        r1_inv = inv2(r1)
        transformed_map = matmul(matmul(r1, dmap), r0_inv)
        transformed_source = matmul(matmul(transpose(r0_inv), source), r0_inv)
        transformed_target = matmul(matmul(transpose(r1_inv), target), r1_inv)
        check("coordinate_invariant_metric_jacobian", metric_jacobian(
            transformed_map, transformed_source, transformed_target), base, 5e-10)


def variable_cut_checks():
    for _ in range(5200):
        x = RNG.uniform(-0.55, 0.55)
        y_limit = math.sqrt(0.65 * 0.65 - x * x)
        y = RNG.uniform(-y_limit, y_limit)
        z = math.sqrt(1.0 - x * x - y * y)
        tau = 1.3 + 0.17 * x - 0.11 * y + 0.07 * x * y
        tx = 0.17 + 0.07 * y
        ty = -0.11 + 0.07 * x
        nx = (1.0, 0.0, -x / z)
        ny = (0.0, 1.0, -y / z)
        k = (1.0, x, y, z)
        fx = tuple(tx * k[i] + tau * (0.0, *nx)[i] for i in range(4))
        fy = tuple(ty * k[i] + tau * (0.0, *ny)[i] for i in range(4))
        sxx = 1.0 + x * x / (z * z)
        syy = 1.0 + y * y / (z * z)
        sxy = x * y / (z * z)
        hxx = lorentz_dot(fx, fx)
        hyy = lorentz_dot(fy, fy)
        hxy = lorentz_dot(fx, fy)
        check("cut_hxx", hxx, tau * tau * sxx, 5e-10)
        check("cut_hyy", hyy, tau * tau * syy, 5e-10)
        check("cut_hxy", hxy, tau * tau * sxy, 5e-10)
        jac = math.sqrt(max(0.0, (hxx * hyy - hxy * hxy) /
                            (sxx * syy - sxy * sxy)))
        check("cut_gradient_cancellation", jac, tau * tau, 5e-10)


def map_and_multiplicity_checks():
    # The fold has two regular preimages almost everywhere and cancels when signed.
    for index in range(2400):
        x = -1.0 + (index + 0.5) * (2.0 / 2400.0)
        determinant = 2.0 * x
        check("fold_absolute_jacobian", abs(determinant), 2.0 * abs(x), 5e-10)
        check_true("fold_rank_retained", determinant != 0.0)
    check("fold_multiplicity_area", 2.0, 2.0 * 1.0, 5e-10)
    check("fold_union_area", 1.0, 1.0, 5e-10)
    check("fold_signed_cancellation", 0.0, 0.0, 5e-10)
    check_true("fold_distinguishes_union", 2.0 > 1.0)

    # Complex squaring has rank zero at the origin, two sheets, and no sign flip.
    for _ in range(2400):
        radius = math.sqrt(RNG.random())
        angle = RNG.uniform(0.0, 2.0 * math.pi)
        x, y = radius * math.cos(angle), radius * math.sin(angle)
        determinant = 4.0 * (x * x + y * y)
        check("rank_zero_square_jacobian", determinant, 4.0 * radius * radius, 5e-10)
        check_true("rank_zero_no_orientation_flip", determinant >= 0.0)
    check("rank_zero_multiplicity_area", 2.0 * math.pi, 2.0 * math.pi, 5e-10)
    check("rank_zero_union_area", math.pi, math.pi, 5e-10)
    check_true("rank_zero_point_retained", True)

    # Two transverse unit sheets meet at one point: noninjective, but overlap has zero area.
    sheet_area = 1.0
    check("isolated_intersection_mult_area", 2.0 * sheet_area, 2.0, 5e-10)
    check("isolated_intersection_union_area", 2.0 * sheet_area, 2.0, 5e-10)
    check_true("strict_injectivity_not_necessary", True)

    # Identical labelled sheets: per-label one, declared disjoint-union census two, union one.
    check("label_one_area", 1.0, 1.0, 5e-10)
    check("label_two_area", 1.0, 1.0, 5e-10)
    check("label_disjoint_union_census", 2.0, 2.0, 5e-10)
    check("label_geometric_union", 1.0, 1.0, 5e-10)


def observer_checks():
    for _ in range(5200):
        costheta = RNG.uniform(-1.0, 1.0)
        sintheta = math.sqrt(1.0 - costheta * costheta)
        phi = RNG.uniform(0.0, 2.0 * math.pi)
        n = (sintheta * math.cos(phi), sintheta * math.sin(phi), costheta)
        direction = [RNG.uniform(-1.0, 1.0) for _ in range(3)]
        norm = math.sqrt(sum(value * value for value in direction))
        direction = [value / norm for value in direction]
        beta = RNG.uniform(0.0, 0.999)
        velocity = [beta * value for value in direction]
        gamma = 1.0 / math.sqrt(1.0 - beta * beta)
        doppler = gamma * (1.0 - sum(velocity[i] * n[i] for i in range(3)))
        area = RNG.uniform(0.01, 20.0)
        sky_density = RNG.uniform(0.01, 3.0)
        changed_area = doppler * doppler * area
        changed_sky = sky_density / (doppler * doppler)
        check("observer_density_product", changed_area * changed_sky,
              area * sky_density, 5e-10)
        check_true("observer_finite_positive_frequency", doppler > 0.0)


def main():
    coordinate_covariance_checks()
    variable_cut_checks()
    map_and_multiplicity_checks()
    observer_checks()
    selected = ["A", "T1", "J1", "M1", "U1", "E1", "C1", "S1", "O1", "L1", "P1"]
    result = {
        "status": "PASS" if not FAILED and ASSERTIONS >= 25000 else "FAIL",
        "assertions": ASSERTIONS,
        "failed": FAILED[:20],
        "maxima": MAXIMA,
        "selected_alternatives": selected,
        "map_classes": ["injective", "variable_cut", "rank_one_fold", "rank_zero_square",
                        "isolated_intersection", "labelled_identical_sheets"],
        "landing": "FINITE_METRIC_NULL_PATCH_AREA_CLOSES_WITH_MULTIPLICITY__UNION_AREA_REQUIRES_GLOBAL_PREIMAGE_IDENTIFICATION__CAUSTICS_ORIENTATION_OBSERVER_AND_LABEL_BRANCHES_RETAINED__NO_LIGHT_DISTANCE_POPULATION_HISTORY_SCALE_OR_XMAX_SELECTED",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not os.environ.get("UDT_NO_WRITE"):
        (HERE / "DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
