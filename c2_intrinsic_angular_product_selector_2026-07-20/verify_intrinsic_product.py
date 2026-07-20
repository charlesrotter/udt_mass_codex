#!/usr/bin/env python3
"""Independent Torch two-coordinate Bach and finite-epsilon action-density verification."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import torch
from torch.func import jacfwd

HERE = Path(__file__).resolve().parent
DTYPE = torch.float64
DIM = 4
R_INDEX = 1
THETA_INDEX = 2
torch.set_default_dtype(DTYPE)
torch.set_num_threads(1)


def polynomial(r, coefficients):
    return sum(coefficients[index] * r**index for index in range(coefficients.numel()))


def angular_factor(theta, curvature, angular_derivatives=True):
    if curvature == 1:
        value = torch.sin(theta)
    elif curvature == 0:
        value = torch.ones_like(theta)
    elif curvature == -1:
        value = torch.cosh(theta)
    else:
        raise ValueError(curvature)
    return value if angular_derivatives else value.detach() + theta * 0


def metric_point(coords, epsilon, ycoeff, ucoeff, curvature, backreaction=True, angular_derivatives=True):
    r, theta = coords
    y = polynomial(r, ycoeff)
    u = polynomial(r, ucoeff)
    factor = angular_factor(theta, curvature, angular_derivatives)
    zero = r * 0
    return torch.stack((
        torch.stack((-y, zero, zero, zero)),
        torch.stack((zero, 1 / y, zero, zero)),
        torch.stack((zero, zero, 1 + (epsilon * u * factor) ** 2 if backreaction else 1 + zero, epsilon * u * factor**2)),
        torch.stack((zero, zero, epsilon * u * factor**2, factor**2)),
    ))


def slot(index):
    if index == R_INDEX:
        return 0
    if index == THETA_INDEX:
        return 1
    return None


def connection_point(coords, epsilon, ycoeff, ucoeff, curvature, backreaction=True, angular_derivatives=True):
    g = metric_point(coords, epsilon, ycoeff, ucoeff, curvature, backreaction, angular_derivatives)
    dg = jacfwd(metric_point, argnums=0)(coords, epsilon, ycoeff, ucoeff, curvature, backreaction, angular_derivatives)
    inverse = torch.linalg.inv(g)
    zero = coords[0] * 0

    def partial(a, b, coordinate):
        selected = slot(coordinate)
        return dg[a, b, selected] if selected is not None else zero

    return torch.stack([torch.stack([torch.stack([
        sum(inverse[a, e] * (partial(e, c, b) + partial(e, b, c) - partial(b, c, e)) for e in range(DIM)) / 2
        for c in range(DIM)]) for b in range(DIM)]) for a in range(DIM)])


def curvature_point(coords, epsilon, ycoeff, ucoeff, curvature, backreaction=True, angular_derivatives=True):
    g = metric_point(coords, epsilon, ycoeff, ucoeff, curvature, backreaction, angular_derivatives)
    inverse = torch.linalg.inv(g)
    gamma = connection_point(coords, epsilon, ycoeff, ucoeff, curvature, backreaction, angular_derivatives)
    dgamma = jacfwd(connection_point, argnums=0)(coords, epsilon, ycoeff, ucoeff, curvature, backreaction, angular_derivatives)
    zero = coords[0] * 0

    def partial_gamma(a, b, c, coordinate):
        selected = slot(coordinate)
        return dgamma[a, b, c, selected] if selected is not None else zero

    rup = torch.stack([torch.stack([torch.stack([torch.stack([
        partial_gamma(a, b, d, c) - partial_gamma(a, b, c, d)
        + sum(gamma[a, e, c] * gamma[e, b, d] - gamma[a, e, d] * gamma[e, b, c] for e in range(DIM))
        for d in range(DIM)]) for c in range(DIM)]) for b in range(DIM)]) for a in range(DIM)])
    ricci = torch.stack([torch.stack([sum(rup[a, b, a, d] for a in range(DIM)) for d in range(DIM)]) for b in range(DIM)])
    scalar = torch.einsum("ab,ab->", inverse, ricci)
    rlow = torch.einsum("ae,ebcd->abcd", g, rup)
    weyl = torch.stack([torch.stack([torch.stack([torch.stack([
        rlow[a, b, c, d]
        - (g[a, c] * ricci[b, d] - g[a, d] * ricci[b, c] - g[b, c] * ricci[a, d] + g[b, d] * ricci[a, c]) / 2
        + scalar * (g[a, c] * g[b, d] - g[a, d] * g[b, c]) / 6
        for d in range(DIM)]) for c in range(DIM)]) for b in range(DIM)]) for a in range(DIM)])
    return g, inverse, gamma, ricci, scalar, weyl


def density_point(coords, epsilon, ycoeff, ucoeff, curvature, backreaction=True, angular_derivatives=True):
    metric, inverse, _, _, _, weyl = curvature_point(coords, epsilon, ycoeff, ucoeff, curvature, backreaction, angular_derivatives)
    cup = torch.einsum("ae,bf,cg,dh,efgh->abcd", inverse, inverse, inverse, inverse, weyl)
    c2 = torch.einsum("abcd,abcd->", weyl, cup)
    return torch.sqrt(torch.abs(torch.linalg.det(metric))) * c2


def weyl_point(coords, epsilon, ycoeff, ucoeff, curvature):
    return curvature_point(coords, epsilon, ycoeff, ucoeff, curvature)[5]


def divergence_point(coords, epsilon, ycoeff, ucoeff, curvature):
    _, inverse, gamma, _, _, weyl = curvature_point(coords, epsilon, ycoeff, ucoeff, curvature)
    dweyl = jacfwd(weyl_point, argnums=0)(coords, epsilon, ycoeff, ucoeff, curvature)
    zero = coords[0] * 0

    def partial_weyl(a, c, b, d, coordinate):
        selected = slot(coordinate)
        return dweyl[a, c, b, d, selected] if selected is not None else zero

    return torch.stack([torch.stack([torch.stack([
        sum(inverse[d, e] * (
            partial_weyl(a, c, b, d, e)
            - sum(gamma[q, e, a] * weyl[q, c, b, d]
                  + gamma[q, e, c] * weyl[a, q, b, d]
                  + gamma[q, e, b] * weyl[a, c, q, d]
                  + gamma[q, e, d] * weyl[a, c, b, q] for q in range(DIM))
        ) for d in range(DIM) for e in range(DIM))
        for b in range(DIM)]) for c in range(DIM)]) for a in range(DIM)])


def bach_point(coords, epsilon, ycoeff, ucoeff, curvature):
    _, inverse, gamma, ricci, _, weyl = curvature_point(coords, epsilon, ycoeff, ucoeff, curvature)
    divergence = divergence_point(coords, epsilon, ycoeff, ucoeff, curvature)
    ddivergence = jacfwd(divergence_point, argnums=0)(coords, epsilon, ycoeff, ucoeff, curvature)
    ricci_up = torch.einsum("ac,bd,cd->ab", inverse, inverse, ricci)
    zero = coords[0] * 0

    def partial_divergence(a, c, b, coordinate):
        selected = slot(coordinate)
        return ddivergence[a, c, b, selected] if selected is not None else zero

    return torch.stack([torch.stack([
        sum(inverse[c, f] * (
            partial_divergence(a, c, b, f)
            - sum(gamma[q, f, a] * divergence[q, c, b]
                  + gamma[q, f, c] * divergence[a, q, b]
                  + gamma[q, f, b] * divergence[a, c, q] for q in range(DIM))
        ) for c in range(DIM) for f in range(DIM))
        + sum(ricci_up[c, d] * weyl[a, c, b, d] / 2 for c in range(DIM) for d in range(DIM))
        for b in range(DIM)]) for a in range(DIM)])


def derivative(function, value, order):
    result = function
    for _ in range(order):
        result = jacfwd(result)
    return result(value)


def expected_bach(r, theta, ycoeff, curvature):
    yfun = lambda x: polynomial(x, ycoeff)
    y0, y1, y2, y3, y4 = [derivative(yfun, r, order) for order in range(5)]
    factor = angular_factor(theta, curvature)
    zero = r * 0
    base = -4 * curvature**2 - 2 * y1 * y3 + y2**2
    b00 = -(base - 4 * y0 * y4) * y0 / 24
    b11 = base / (24 * y0)
    b22 = -(base - 2 * y0 * y4) / 24
    return torch.stack((
        torch.stack((b00, zero, zero, zero)),
        torch.stack((zero, b11, zero, zero)),
        torch.stack((zero, zero, b22, zero)),
        torch.stack((zero, zero, zero, b22 * factor**2)),
    ))


def expected_twist(r, theta, ycoeff, ucoeff, curvature):
    yfun = lambda x: polynomial(x, ycoeff)
    ufun = lambda x: polynomial(x, ucoeff)
    y0, y2 = derivative(yfun, r, 0), derivative(yfun, r, 2)
    u1, u2 = derivative(ufun, r, 1), derivative(ufun, r, 2)
    factor = angular_factor(theta, curvature)
    fprime = derivative(lambda x: angular_factor(x, curvature), theta, 1)
    return factor * y0 * (4 * curvature * factor**2 * u1**2 + 3 * factor**2 * y0 * u2**2 - 2 * factor**2 * y2 * u1**2 + 27 * fprime**2 * u1**2) / 3


def relative_error(a, b):
    scale = torch.maximum(torch.tensor(1e-10), torch.maximum(torch.abs(a), torch.abs(b)))
    return float(torch.abs(a - b) / scale)


def even_quadratic(function, step=2e-3):
    def estimate(size):
        positive = function(torch.tensor(size))
        negative = function(torch.tensor(-size))
        center = function(torch.tensor(0.0))
        return (positive + negative - 2 * center) / (2 * size * size)
    coarse = estimate(step)
    fine = estimate(step / 2)
    return (4 * fine - coarse) / 3


PROFILES = [
    ("P1", [2, 1/3, 1/5, -1/7], [-1/3, 1/5]),
    ("P2", [3, -1/4, 2/7, 0, 1/13], [-2/5, 3/5]),
    ("P3", [2], [-1/2, 1/4]),
]
ANGULAR = [(1, 0.7), (0, 0.4), (-1, 0.6)]
U1 = [0, 2/5, -1/4, 1/6, 1/9]
U0 = [2/7]


def main():
    zero_u = torch.tensor([0.0])
    bach_records = []
    for profile, raw_y, points in PROFILES:
        ycoeff = torch.tensor(raw_y)
        for curvature, raw_theta in ANGULAR:
            for raw_r in points:
                coords = torch.tensor([raw_r, raw_theta])
                observed = bach_point(coords, torch.tensor(0.0), ycoeff, zero_u, curvature)
                expected = expected_bach(coords[0], coords[1], ycoeff, curvature)
                for a in range(DIM):
                    for b in range(DIM):
                        bach_records.append({
                            "profile": profile, "K": curvature, "r": raw_r, "theta": raw_theta,
                            "component": f"B_{a}{b}", "direct": float(observed[a, b]),
                            "formula": float(expected[a, b]),
                            "absolute_error": float(torch.abs(observed[a, b] - expected[a, b])),
                            "scaled_error": relative_error(observed[a, b], expected[a, b]),
                        })

    twist_records = []
    for profile, raw_y, points in PROFILES[:2]:
        ycoeff = torch.tensor(raw_y)
        for curvature, raw_theta in ANGULAR:
            for raw_r in points:
                for twist_name, raw_u in (("U1", U1), ("U0", U0)):
                    ucoeff = torch.tensor(raw_u)
                    coords = torch.tensor([raw_r, raw_theta])
                    direct = even_quadratic(lambda eps: density_point(coords, eps, ycoeff, ucoeff, curvature))
                    expected = expected_twist(coords[0], coords[1], ycoeff, ucoeff, curvature)
                    if twist_name == "U0":
                        center = density_point(coords, torch.tensor(0.0), ycoeff, ucoeff, curvature)
                        positive = density_point(coords, torch.tensor(0.2), ycoeff, ucoeff, curvature)
                        negative = density_point(coords, torch.tensor(-0.2), ycoeff, ucoeff, curvature)
                        invariance = float(torch.maximum(torch.abs(positive - center), torch.abs(negative - center)))
                    else:
                        invariance = None
                    twist_records.append({
                        "profile": profile, "twist": twist_name, "K": curvature, "r": raw_r, "theta": raw_theta,
                        "direct_quadratic": float(direct), "formula_quadratic": float(expected),
                        "absolute_error": float(torch.abs(direct - expected)),
                        "scaled_error": relative_error(direct, expected),
                        "constant_finite_amplitude_invariance": invariance,
                    })

    bach_nonzero = [row for row in bach_records if abs(row["formula"]) > 1e-10]
    bach_zero = [row for row in bach_records if abs(row["formula"]) <= 1e-10]
    twist_nonconstant = [row for row in twist_records if row["twist"] == "U1"]
    twist_constant = [row for row in twist_records if row["twist"] == "U0"]
    max_bach_relative = max(row["scaled_error"] for row in bach_nonzero)
    max_bach_zero = max(row["absolute_error"] for row in bach_zero)
    max_twist_relative = max(row["scaled_error"] for row in twist_nonconstant)
    max_constant_coefficient_noise = max(abs(row["direct_quadratic"]) for row in twist_constant)
    max_constant = max(row["constant_finite_amplitude_invariance"] for row in twist_constant)

    mutation_coords = torch.tensor([0.2, 0.7])
    mutation_y = torch.tensor(PROFILES[0][1])
    mutation_u = torch.tensor(U1)
    correct = density_point(mutation_coords, torch.tensor(2e-3), mutation_y, mutation_u, 1)
    missing_angular = density_point(mutation_coords, torch.tensor(2e-3), mutation_y, mutation_u, 1, True, False)
    missing_backreaction = density_point(mutation_coords, torch.tensor(2e-3), mutation_y, mutation_u, 1, False, True)
    angular_difference = float(torch.abs(correct - missing_angular))
    backreaction_difference = float(torch.abs(correct - missing_backreaction))

    checks = {
        "all_registered_bach_records": len(bach_records) == 18 * 16,
        "all_registered_twist_records": len(twist_records) == 24,
        "bach_nonzero_match": max_bach_relative <= 1e-8,
        "bach_zero_match": max_bach_zero <= 1e-9,
        "twist_nonconstant_match": max_twist_relative <= 1e-8,
        "constant_twist_zero": max_constant <= 1e-9,
        "omitted_angular_derivatives_caught": angular_difference > 1e-6,
        "missing_backreaction_caught": backreaction_difference > 1e-8,
    }
    if not all(checks.values()):
        raise AssertionError({"checks": checks, "max_bach_relative": max_bach_relative,
                              "max_bach_zero": max_bach_zero, "max_twist_relative": max_twist_relative,
                              "max_constant": max_constant, "max_constant_coefficient_noise": max_constant_coefficient_noise,
                              "angular_difference": angular_difference,
                              "backreaction_difference": backreaction_difference})

    with (HERE / "BACH_VERIFICATION_POINTS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(bach_records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(bach_records)
    with (HERE / "TWIST_VERIFICATION_POINTS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(twist_records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(twist_records)
    result = {
        "schema": "udt-c2-intrinsic-angular-product-independent-verification-1.0",
        "result": "PASS", "checks": checks,
        "counts": {"bach_records": len(bach_records), "twist_records": len(twist_records)},
        "maxima": {"bach_nonzero_scaled_error": max_bach_relative, "bach_zero_absolute_error": max_bach_zero,
                   "twist_nonconstant_scaled_error": max_twist_relative,
                   "constant_twist_finite_amplitude_absolute": max_constant,
                   "constant_twist_second_difference_noise": max_constant_coefficient_noise,
                   "omitted_angular_derivative_difference": angular_difference,
                   "missing_backreaction_difference": backreaction_difference},
        "compute": {"method": "independent Torch two-coordinate forward-AD tensor, Bach, and sqrt(-g) C2 construction",
                    "dtype": "float64", "cpu_only": True},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", **result["counts"], **result["maxima"]}, sort_keys=True))


if __name__ == "__main__":
    main()
