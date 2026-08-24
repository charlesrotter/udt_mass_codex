#!/usr/bin/env python3
"""Independent high-precision replay of the G241 carrier census."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import mpmath as mp


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
STATE_PATH = REPO / "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23" / "FROZEN_PRIMARY_K12_STATE.json"
STATE_SHA256 = "88d3006a646f2be105a3fb15f2c4c694732b884da97f8fdeefc39323e6bbc8cf"
CANDIDATE_DEGREES = (2, 3, 4)
SLOPE_TOLERANCE = mp.mpf("1e-10")
DENSE_GRID_SIZE = 2001
mp.mp.dps = 80


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_state():
    assert sha256(STATE_PATH) == STATE_SHA256
    payload = json.loads(STATE_PATH.read_text(), parse_float=mp.mpf)
    state = payload["state"]
    knots = [mp.mpf(value) for value in state["knots"]]
    theta = mp.matrix([mp.mpf(value) for value in state["theta"]])
    covariance = mp.matrix([[mp.mpf(value) for value in row] for row in state["theta_covariance"]])
    return knots, theta, covariance


def poly_add(left, right):
    out = [mp.mpf("0")] * max(len(left), len(right))
    for index, value in enumerate(left):
        out[index] += value
    for index, value in enumerate(right):
        out[index] += value
    return out


def poly_scale(poly, scale):
    return [scale * value for value in poly]


def poly_mul_t(poly):
    return [mp.mpf("0")] + list(poly)


def poly_derivative(poly):
    if len(poly) <= 1:
        return [mp.mpf("0")]
    return [mp.mpf(index) * poly[index] for index in range(1, len(poly))]


def poly_eval(poly, value):
    total = mp.mpf("0")
    for coefficient in reversed(poly):
        total = total * value + coefficient
    return total


def chebyshev_polynomials(max_degree):
    polys = [[mp.mpf("1")], [mp.mpf("0"), mp.mpf("1")]]
    for _ in range(2, max_degree + 1):
        polys.append(poly_add(poly_scale(poly_mul_t(polys[-1]), 2), poly_scale(polys[-2], -1)))
    return polys[: max_degree + 1]


def chi2_ceiling(dof):
    shape = mp.mpf(dof) / 2
    target = mp.mpf("0.999")
    low = mp.mpf("0")
    high = mp.mpf(max(20, 10 * dof))
    cdf = lambda value: mp.gammainc(shape, 0, value / 2) / mp.gamma(shape)
    while cdf(high) < target:
        high *= 2
    for _ in range(300):
        mid = (low + high) / 2
        if cdf(mid) < target:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def stationary_points(second_poly):
    coefficients = list(second_poly)
    while len(coefficients) > 1 and abs(coefficients[-1]) < mp.mpf("1e-60"):
        coefficients.pop()
    points = [mp.mpf("-1"), mp.mpf("1")]
    degree = len(coefficients) - 1
    roots = []
    if degree == 1:
        roots = [-coefficients[0] / coefficients[1]]
    elif degree == 2:
        a, b, c = coefficients[2], coefficients[1], coefficients[0]
        discriminant = b * b - 4 * a * c
        if discriminant >= 0:
            root = mp.sqrt(discriminant)
            roots = [(-b - root) / (2 * a), (-b + root) / (2 * a)]
    for root in roots:
        if -1 <= root <= 1:
            points.append(root)
    return sorted(set(points))


def fit_candidate(degree, knots, theta, covariance):
    phi_lo, phi_hi = knots[0], knots[-1]
    scale_t = 2 / (phi_hi - phi_lo)
    cheb_polys = chebyshev_polynomials(degree)
    rows = []
    for phi in knots[1:]:
        t = scale_t * (phi - phi_lo) - 1
        rows.append([poly_eval(cheb_polys[k], t) - ((-1) ** k) for k in range(1, degree + 1)])
    basis = mp.matrix(rows)
    covariance_inverse = covariance**-1
    precision_basis = covariance_inverse * basis
    precision_theta = covariance_inverse * theta
    normal = basis.T * precision_basis
    coefficients = mp.lu_solve(normal, basis.T * precision_theta)
    residual = theta - basis * coefficients
    chi2 = (residual.T * mp.lu_solve(covariance, residual))[0]
    dof = len(theta) - degree
    ceiling = chi2_ceiling(dof)

    theta_poly = [mp.mpf("0")]
    for k in range(1, degree + 1):
        anchored = list(cheb_polys[k])
        anchored[0] -= (-1) ** k
        theta_poly = poly_add(theta_poly, poly_scale(anchored, coefficients[k - 1]))
    log_factor = mp.log(10) / 5
    s_poly = poly_scale(theta_poly, log_factor)
    s_t_poly = poly_derivative(s_poly)
    s_tt_poly = poly_derivative(s_t_poly)
    points = stationary_points(s_tt_poly)
    slopes = [poly_eval(s_t_poly, point) * scale_t for point in points]
    slope_min = min(slopes)
    slope_t = points[slopes.index(slope_min)]
    slope_phi = phi_lo + (slope_t + 1) / scale_t

    finite = True
    tidal_min = mp.inf
    tidal_max = -mp.inf
    scale_residual = mp.mpf("0")
    knot_rows = []
    for grid_index in range(DENSE_GRID_SIZE):
        phi = phi_lo + (phi_hi - phi_lo) * grid_index / (DENSE_GRID_SIZE - 1)
        t = scale_t * (phi - phi_lo) - 1
        s = poly_eval(s_poly, t)
        s_prime = poly_eval(s_t_poly, t) * scale_t
        s_second = poly_eval(s_tt_poly, t) * scale_t**2
        p = 1 / s_prime
        q = -(s_second + s_prime**2) / s_prime**3
        decay = mp.exp(-2 * phi)
        tidal = decay * (2 * p**2 - q + 2 * p) - (1 - decay)
        finite = finite and all(mp.isfinite(value) for value in (s, s_prime, s_second, p, q, tidal))
        tidal_min = min(tidal_min, tidal)
        tidal_max = max(tidal_max, tidal)
        for radial_scale in (mp.mpf("0.125"), mp.mpf("1"), mp.mpf("8")):
            radius = radial_scale * mp.exp(s)
            radius_prime = radius * s_prime
            radius_second = radius * (s_second + s_prime**2)
            phi_prime = 1 / radius_prime
            phi_second = -radius_second / radius_prime**3
            xi = decay * (2 * phi_prime**2 - phi_second + 2 * phi_prime / radius) - (1 - decay) / radius**2
            scale_residual = max(scale_residual, abs(radius**2 * xi - tidal))
    for phi in knots:
        t = scale_t * (phi - phi_lo) - 1
        s = poly_eval(s_poly, t)
        s_prime = poly_eval(s_t_poly, t) * scale_t
        s_second = poly_eval(s_tt_poly, t) * scale_t**2
        p = 1 / s_prime
        q = -(s_second + s_prime**2) / s_prime**3
        decay = mp.exp(-2 * phi)
        tidal = decay * (2 * p**2 - q + 2 * p) - (1 - decay)
        knot_rows.append([s, s_prime, s_second, p, q, tidal])
    adequate = chi2 <= ceiling
    monotone = slope_min > SLOPE_TOLERANCE
    passed = bool(adequate and monotone and finite)
    return {
        "degree": degree,
        "coefficients_theta_units": [float(value) for value in coefficients],
        "chi2": float(chi2),
        "dof": dof,
        "chi2_ceiling": float(ceiling),
        "adequate": bool(adequate),
        "minimum_s_prime": float(slope_min),
        "minimum_s_prime_phi": float(slope_phi),
        "monotone_invertible": bool(monotone),
        "finite_dense_grid": bool(finite),
        "scale_invariance_max_abs_residual": float(scale_residual),
        "passed": passed,
        "knot_s": [float(row[0]) for row in knot_rows],
        "knot_s_prime": [float(row[1]) for row in knot_rows],
        "knot_s_second": [float(row[2]) for row in knot_rows],
        "knot_p": [float(row[3]) for row in knot_rows],
        "knot_q": [float(row[4]) for row in knot_rows],
        "knot_tidal_J": [float(row[5]) for row in knot_rows],
        "dense_tidal_J_min": float(tidal_min),
        "dense_tidal_J_max": float(tidal_max),
    }


def derive():
    knots, theta, covariance = load_state()
    candidates = [fit_candidate(degree, knots, theta, covariance) for degree in CANDIDATE_DEGREES]
    selected = next((candidate for candidate in candidates if candidate["passed"]), None)
    landing = (
        "NO_REGISTERED_SMOOTH_ANCHOR_ADEQUATE__STOP_BEFORE_BOSS"
        if selected is None
        else f"D{selected['degree']}_SNE_ANCHOR_ADEQUATE__NATIVE_TIDAL_BRIDGE_FROZEN"
    )
    return {
        "package": "G241",
        "implementation": "independent_mpmath_direct_polynomial",
        "landing": landing,
        "selected_degree": None if selected is None else selected["degree"],
        "candidates": candidates,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert rendered == (PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text()
    else:
        (PACKAGE / "INDEPENDENT_VERIFICATION.json").write_text(rendered)
    print(result["landing"])


if __name__ == "__main__":
    main()
