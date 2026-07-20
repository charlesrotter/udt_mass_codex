#!/usr/bin/env python3
"""Independent Torch coordinate-tensor and direct Bach verification."""
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
RADIAL = 1
torch.set_default_dtype(DTYPE)
torch.set_num_threads(1)


def polynomial(r, coefficients):
    return sum(coefficients[index] * r**index for index in range(coefficients.numel()))


def metric_point(r, epsilon, pcoeff, ucoeff, lorentz=True, backreaction=True):
    p = polynomial(r, pcoeff)
    u = polynomial(r, ucoeff)
    zero = r * 0
    sign = -1.0 if lorentz else 1.0
    return torch.stack((
        torch.stack((sign * torch.exp(-2 * p), zero, zero, zero)),
        torch.stack((zero, torch.exp(2 * p), zero, zero)),
        torch.stack((zero, zero, 1 + (epsilon * u)**2 if backreaction else 1 + zero, epsilon * u)),
        torch.stack((zero, zero, epsilon * u, 1 + zero)),
    ))


def connection_point(r, epsilon, pcoeff, ucoeff, lorentz=True, backreaction=True):
    g = metric_point(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    dg = jacfwd(metric_point, argnums=0)(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    inverse = torch.linalg.inv(g)
    zero = r * 0
    return torch.stack([torch.stack([torch.stack([
        sum(inverse[a, e] * (
            (dg[e, c] if b == RADIAL else zero)
            + (dg[e, b] if c == RADIAL else zero)
            - (dg[b, c] if e == RADIAL else zero)
        ) for e in range(DIM)) / 2
        for c in range(DIM)]) for b in range(DIM)]) for a in range(DIM)])


def curvature_point(r, epsilon, pcoeff, ucoeff, lorentz=True, backreaction=True):
    g = metric_point(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    inverse = torch.linalg.inv(g)
    gamma = connection_point(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    dgamma = jacfwd(connection_point, argnums=0)(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    zero = r * 0
    rup = torch.stack([torch.stack([torch.stack([torch.stack([
        (dgamma[a, b, d] if c == RADIAL else zero)
        - (dgamma[a, b, c] if d == RADIAL else zero)
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


def density_point(r, epsilon, pcoeff, ucoeff, lorentz=True, backreaction=True):
    g, inverse, _, _, _, weyl = curvature_point(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    cup = torch.einsum("ae,bf,cg,dh,efgh->abcd", inverse, inverse, inverse, inverse, weyl)
    return torch.sqrt(torch.abs(torch.linalg.det(g))) * torch.einsum("abcd,abcd->", weyl, cup)


def weyl_point(r, epsilon, pcoeff, ucoeff, lorentz=True, backreaction=True):
    return curvature_point(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)[5]


def divergence_point(r, epsilon, pcoeff, ucoeff, lorentz=True, backreaction=True):
    _, inverse, gamma, _, _, weyl = curvature_point(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    dweyl = jacfwd(weyl_point, argnums=0)(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    zero = r * 0
    return torch.stack([torch.stack([torch.stack([
        sum(inverse[d, e] * (
            (dweyl[a, c, b, d] if e == RADIAL else zero)
            - sum(gamma[q, e, a] * weyl[q, c, b, d]
                  + gamma[q, e, c] * weyl[a, q, b, d]
                  + gamma[q, e, b] * weyl[a, c, q, d]
                  + gamma[q, e, d] * weyl[a, c, b, q] for q in range(DIM))
        ) for d in range(DIM) for e in range(DIM))
        for b in range(DIM)]) for c in range(DIM)]) for a in range(DIM)])


def bach_point(r, epsilon, pcoeff, ucoeff, lorentz=True, backreaction=True):
    _, inverse, gamma, ricci, _, weyl = curvature_point(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    divergence = divergence_point(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    ddivergence = jacfwd(divergence_point, argnums=0)(r, epsilon, pcoeff, ucoeff, lorentz, backreaction)
    ricci_up = torch.einsum("ac,bd,cd->ab", inverse, inverse, ricci)
    zero = r * 0
    return torch.stack([torch.stack([
        sum(inverse[c, f] * (
            (ddivergence[a, c, b] if f == RADIAL else zero)
            - sum(gamma[q, f, a] * divergence[q, c, b]
                  + gamma[q, f, c] * divergence[a, q, b]
                  + gamma[q, f, b] * divergence[a, c, q] for q in range(DIM))
        ) for c in range(DIM) for f in range(DIM))
        + sum(ricci_up[c, d] * weyl[a, c, b, d] / 2 for c in range(DIM) for d in range(DIM))
        for b in range(DIM)]) for a in range(DIM)])


def bach_raised_point(r, epsilon, pcoeff, ucoeff):
    g = metric_point(r, epsilon, pcoeff, ucoeff)
    inverse = torch.linalg.inv(g)
    bach = bach_point(r, epsilon, pcoeff, ucoeff)
    return torch.einsum("ac,bd,cd->ab", inverse, inverse, bach)


def derivative(function, r, order):
    result = function
    for _ in range(order):
        result = jacfwd(result)
    return result(r)


def formula_values(r, pcoeff, ucoeff):
    pfun = lambda x: polynomial(x, pcoeff)
    ufun = lambda x: polynomial(x, ucoeff)
    p0, p1, p2, p3 = [derivative(pfun, r, order) for order in range(4)]
    u1, u2, u3, u4 = [derivative(ufun, r, order) for order in range(1, 5)]
    quadratic = torch.exp(-4 * p0) * (3 * u2**2 + (4 * p2 - 8 * p1**2) * u1**2) / 3
    jacobi = 2 * torch.exp(-4 * p0) * (
        -32 * p1**3 * u1 + 56 * p1**2 * u2 + 32 * p1 * p2 * u1
        - 24 * p1 * u3 - 16 * p2 * u2 - 4 * p3 * u1 + 3 * u4
    ) / 3
    return quadratic, jacobi


def relative_error(a, b):
    return float(torch.abs(a - b) / torch.maximum(torch.tensor(1e-10), torch.maximum(torch.abs(a), torch.abs(b))))


def even_quadratic_coefficient(function, step=2e-3):
    def estimate(size):
        positive = function(torch.tensor(size))
        negative = function(torch.tensor(-size))
        center = function(torch.tensor(0.0))
        return (positive + negative - 2 * center) / (2 * size * size)
    coarse = estimate(step)
    fine = estimate(step / 2)
    return (4 * fine - coarse) / 3


def odd_linear_coefficient(function, step=2e-3):
    def estimate(size):
        return (function(torch.tensor(size)) - function(torch.tensor(-size))) / (2 * size)
    coarse = estimate(step)
    fine = estimate(step / 2)
    return (4 * fine - coarse) / 3


PROFILES = [
    ("A", [0, 1/3, 1/5, -1/7], [0, 2/5, -1/4, 1/6, 1/9], [-1/3, 1/5, 2/3]),
    ("B", [0, -1/4, 2/7, 0, 1/13], [1/7, 1/2, 0, -1/5, 0, 1/11], [-2/5, 1/7, 3/5]),
    ("FLAT", [1/6], [0, 0, 1/3, 0, 1/8], [-1/2, 1/4]),
    ("CONSTANT_U", [0, 1/3, 1/5], [2/7], [-1/3, 1/3]),
]


def main():
    records = []
    epsilon0 = torch.tensor(0.0)
    for name, pc, uc, points in PROFILES:
        pcoeff = torch.tensor(pc)
        ucoeff = torch.tensor(uc)
        for raw_point in points:
            r = torch.tensor(raw_point)
            direct_quadratic = even_quadratic_coefficient(lambda eps: density_point(r, eps, pcoeff, ucoeff))
            expected_quadratic, expected_jacobi = formula_values(r, pcoeff, ucoeff)
            linear_bach = odd_linear_coefficient(lambda eps: bach_raised_point(r, eps, pcoeff, ucoeff)[2, 3])
            background_bach_xx = bach_raised_point(r, epsilon0, pcoeff, ucoeff)[2, 2]
            local_u = polynomial(r, ucoeff)
            # Full metric-path projection: g_xy=epsilon*u and g_xx=1+epsilon^2*u^2.
            # The background Euler term is required off shell and enforces the constant-shear zero mode.
            projected_bach = linear_bach + local_u * background_bach_xx
            missing_backreaction = even_quadratic_coefficient(lambda eps: density_point(r, eps, pcoeff, ucoeff, True, False))
            euclidean = even_quadratic_coefficient(lambda eps: density_point(r, eps, pcoeff, ucoeff, False, True))
            records.append({
                "profile": name, "r": raw_point,
                "direct_quadratic": float(direct_quadratic), "formula_quadratic": float(expected_quadratic),
                "quadratic_relative_error": relative_error(direct_quadratic, expected_quadratic),
                "formula_jacobi": float(expected_jacobi), "linear_raised_bach_xy": float(linear_bach),
                "background_raised_bach_xx": float(background_bach_xx),
                "metric_path_projected_bach": float(projected_bach),
                "jacobi_to_bach_ratio": float(expected_jacobi / projected_bach) if abs(float(projected_bach)) > 1e-11 else None,
                "missing_backreaction_quadratic": float(missing_backreaction),
                "missing_backreaction_difference": float(torch.abs(missing_backreaction - expected_quadratic)),
                "euclidean_quadratic": float(euclidean),
                "euclidean_difference": float(torch.abs(euclidean - expected_quadratic)),
            })
    nonconstant = [record for record in records if record["profile"] != "CONSTANT_U"]
    constant = [record for record in records if record["profile"] == "CONSTANT_U"]
    ratios = [record["jacobi_to_bach_ratio"] for record in nonconstant if record["jacobi_to_bach_ratio"] is not None]
    ratio_reference = ratios[0]
    ratio_spread = max(abs(value - ratio_reference) for value in ratios)
    quadratic_error = max(record["quadratic_relative_error"] for record in nonconstant)
    constant_max = max(max(abs(record["direct_quadratic"]), abs(record["formula_jacobi"]), abs(record["metric_path_projected_bach"])) for record in constant)
    missing_difference = max(record["missing_backreaction_difference"] for record in nonconstant)
    euclidean_difference = max(record["euclidean_difference"] for record in nonconstant)
    checks = {
        "all_registered_points": len(records) == 10,
        "direct_density_matches": quadratic_error <= 1e-8,
        "bach_normalization_constant": ratio_spread <= 1e-7 * max(1.0, abs(ratio_reference)),
        "constant_twist_zero": constant_max <= 1e-9,
        "missing_backreaction_caught": missing_difference > 1e-6,
        "euclidean_signature_classified": math.isfinite(euclidean_difference),
    }
    if not all(checks.values()):
        raise AssertionError({"checks": checks, "quadratic_error": quadratic_error, "ratio_reference": ratio_reference, "ratio_spread": ratio_spread, "constant_max": constant_max, "missing_difference": missing_difference, "euclidean_difference": euclidean_difference})
    fields = list(records[0])
    with (HERE / "VERIFICATION_POINTS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    result = {
        "schema": "udt-c2-reciprocal-transverse-twist-verification-1.0",
        "result": "PASS", "checks": checks, "points": len(records),
        "maxima": {"quadratic_relative_error": quadratic_error, "bach_ratio_reference": ratio_reference, "bach_ratio_spread": ratio_spread, "constant_twist_absolute": constant_max, "missing_backreaction_difference": missing_difference, "euclidean_signature_difference": euclidean_difference},
        "interpretation": {"direct_bach_relation": "action_jacobi equals the recorded constant multiple of direct linearized covariant Bach_xy at every nonzero witness", "euclidean_mutation": "DIFFERS" if euclidean_difference > 1e-6 else "QUADRATIC_TWIST_DENSITY_SIGNATURE_INDEPENDENT_IN_THIS_STATIC_TILE"},
        "compute": {"method": "independent Torch forward-AD coordinate tensor and direct Weyl divergence", "dtype": "float64", "cpu_only": True},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"result": "PASS", "points": len(records), **result["maxima"], "euclidean": result["interpretation"]["euclidean_mutation"]}, sort_keys=True))


if __name__ == "__main__":
    main()
