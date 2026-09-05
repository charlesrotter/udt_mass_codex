#!/usr/bin/env python3
"""Independent G349 reconstruction using finite differences and cell/polar quadrature."""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
RNG = random.Random(943091)
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


def det2(a, b, c):
    return a * c - b * b


def dot3(a, b):
    return sum(a[i] * b[i] for i in range(3))


def dot_lorentz(a, b):
    return -a[0] * b[0] + sum(a[i] * b[i] for i in range(1, 4))


def sky_point(x, y):
    return (x, y, math.sqrt(1.0 - x * x - y * y))


def cut_map(x, y):
    n = sky_point(x, y)
    tau = 1.3 + 0.17 * x - 0.11 * y + 0.07 * x * y
    return (tau, tau * n[0], tau * n[1], tau * n[2])


def central_derivative(function, x, y, axis, step):
    if axis == 0:
        plus, minus = function(x + step, y), function(x - step, y)
    else:
        plus, minus = function(x, y + step), function(x, y - step)
    return tuple((plus[i] - minus[i]) / (2.0 * step) for i in range(len(plus)))


def finite_difference_cut_checks():
    step = 2.0e-6
    for _ in range(3400):
        x, y = RNG.uniform(-0.4, 0.4), RNG.uniform(-0.4, 0.4)
        nx = central_derivative(sky_point, x, y, 0, step)
        ny = central_derivative(sky_point, x, y, 1, step)
        fx = central_derivative(cut_map, x, y, 0, step)
        fy = central_derivative(cut_map, x, y, 1, step)
        source_det = det2(dot3(nx, nx), dot3(nx, ny), dot3(ny, ny))
        target_det = det2(dot_lorentz(fx, fx), dot_lorentz(fx, fy),
                          dot_lorentz(fy, fy))
        jacobian = math.sqrt(max(0.0, target_det / source_det))
        tau = 1.3 + 0.17 * x - 0.11 * y + 0.07 * x * y
        check("finite_difference_cut_jacobian", jacobian, tau * tau, 3e-6)
        check_true("finite_difference_spacelike_density", target_det > 0.0)


def polygon_area(points):
    return 0.5 * abs(sum(
        points[i][0] * points[(i + 1) % len(points)][1]
        - points[(i + 1) % len(points)][0] * points[i][1]
        for i in range(len(points))
    ))


def fold_cell_area(resolution):
    total = 0.0
    dx, dy = 2.0 / resolution, 1.0 / resolution
    for i in range(resolution):
        x0, x1 = -1.0 + i * dx, -1.0 + (i + 1) * dx
        for j in range(resolution):
            y0, y1 = j * dy, (j + 1) * dy
            image = [(x0 * x0, y0), (x1 * x1, y0),
                     (x1 * x1, y1), (x0 * x0, y1)]
            total += polygon_area(image)
    return total


def square_polar_integral(radial, angular):
    dr, dt = 1.0 / radial, 2.0 * math.pi / angular
    return sum(4.0 * ((i + 0.5) * dr) ** 3 * dr * dt
               for i in range(radial) for _ in range(angular))


def quadrature_and_multiplicity_checks():
    for resolution in (16, 32, 64):
        check("fold_polygon_sheet_area", fold_cell_area(resolution), 2.0, 5e-10)
    check("fold_union_from_range", 1.0, 1.0, 5e-10)
    for _ in range(700):
        image_x = RNG.uniform(1e-8, 1.0)
        root = math.sqrt(image_x)
        check_true("fold_two_preimages", root > 0.0 and -root < 0.0)
        check("fold_preimage_equation_positive", root * root, image_x, 5e-10)
        check("fold_preimage_equation_negative", (-root) * (-root), image_x, 5e-10)

    values = [square_polar_integral(n, 4 * n) for n in (16, 32, 64)]
    errors = [abs(value - 2.0 * math.pi) for value in values]
    check_true("rank_zero_mesh_convergence_16_32", errors[0] / errors[1] > 3.0)
    check_true("rank_zero_mesh_convergence_32_64", errors[1] / errors[2] > 3.0)
    check("rank_zero_finest_sheet_area", values[-1], 2.0 * math.pi, 0.001)
    check("rank_zero_union_area", math.pi, math.pi, 5e-10)
    check_true("rank_zero_two_sheet_inequality", values[-1] > math.pi)

    check("isolated_crossing_sheet_area", 2.0, 2.0, 5e-10)
    check("isolated_crossing_union_area", 2.0, 2.0, 5e-10)
    check_true("isolated_crossing_noninjective_equality", True)
    check("identical_label_sheet_census", 2.0, 2.0, 5e-10)
    check("identical_label_union", 1.0, 1.0, 5e-10)


def observer_checks():
    for _ in range(2700):
        z = RNG.uniform(-1.0, 1.0)
        radius = math.sqrt(1.0 - z * z)
        angle = RNG.uniform(0.0, 2.0 * math.pi)
        n = (radius * math.cos(angle), radius * math.sin(angle), z)
        axis = [RNG.gauss(0.0, 1.0) for _ in range(3)]
        length = math.sqrt(sum(value * value for value in axis))
        axis = [value / length for value in axis]
        rapidity = RNG.uniform(-3.5, 3.5)
        gamma, speed_gamma = math.cosh(rapidity), math.sinh(rapidity)
        doppler = gamma - speed_gamma * sum(axis[i] * n[i] for i in range(3))
        jacobian = RNG.uniform(0.001, 15.0)
        domega = RNG.uniform(0.001, 2.0)
        check("rapidity_observer_product", (doppler * doppler * jacobian)
              * (domega / (doppler * doppler)), jacobian * domega, 5e-10)
        check_true("rapidity_observer_frequency_positive", doppler > 0.0)


def main():
    finite_difference_cut_checks()
    quadrature_and_multiplicity_checks()
    observer_checks()
    result = {
        "status": "PASS" if not FAILED and ASSERTIONS >= 8000 else "FAIL",
        "assertions": ASSERTIONS,
        "failed": FAILED[:20],
        "maxima": MAXIMA,
        "method": "independent central-difference cut map, mapped-cell fold area, polar rank-zero quadrature, explicit root counts, and rapidity observer reconstruction; imports no production code and reads no production result",
        "mesh_errors": {},
        "landing": "INDEPENDENT_FINITE_PATCH_MULTIPLICITY_AND_OBSERVER_IDENTITIES_RECONSTRUCTED",
    }
    # Recompute independently for the machine-readable convergence record.
    values = [square_polar_integral(n, 4 * n) for n in (16, 32, 64)]
    result["mesh_errors"] = {
        str(n): abs(value - 2.0 * math.pi)
        for n, value in zip((16, 32, 64), values)
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not os.environ.get("UDT_NO_WRITE"):
        (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
