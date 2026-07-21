#!/usr/bin/env python3
"""Independent Torch verification of transverse background, Bach, gauge, and mixed blocks."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import sympy as sp
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


def metric_point(coords, epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature,
                 backreaction=True, angular_derivatives=True):
    r, theta = coords
    y = polynomial(r, ycoeff)
    area = polynomial(r, acoeff)
    shear = polynomial(r, scoeff)
    u = polynomial(r, ucoeff)
    # The registered variation-domain witness is a constant angular-leg rescaling.  An r-dependent
    # test mode adds derivative-of-variation terms to the pointwise density derivative and is not
    # the comparison encoded by the exact product projection.
    mode = torch.ones_like(r)
    b = area * torch.exp(shear + area_amp * mode + shear_amp * mode)
    c = area * torch.exp(-shear + area_amp * mode - shear_amp * mode)
    factor = angular_factor(theta, curvature, angular_derivatives)
    zero = r * 0
    back = (epsilon * u * c * factor) ** 2 if backreaction else zero
    return torch.stack((
        torch.stack((-y, zero, zero, zero)),
        torch.stack((zero, 1 / y, zero, zero)),
        torch.stack((zero, zero, b**2 + back, epsilon * u * c**2 * factor**2)),
        torch.stack((zero, zero, epsilon * u * c**2 * factor**2, c**2 * factor**2)),
    ))


def slot(index):
    if index == R_INDEX:
        return 0
    if index == THETA_INDEX:
        return 1
    return None


def connection_point(coords, epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature,
                     backreaction=True, angular_derivatives=True):
    args = (epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature, backreaction, angular_derivatives)
    g = metric_point(coords, *args)
    dg = jacfwd(metric_point, argnums=0)(coords, *args)
    inverse = torch.linalg.inv(g)
    zero = coords[0] * 0

    def partial(a, b, coordinate):
        selected = slot(coordinate)
        return dg[a, b, selected] if selected is not None else zero

    return torch.stack([torch.stack([torch.stack([
        sum(inverse[a, e] * (partial(e, c, b) + partial(e, b, c) - partial(b, c, e)) for e in range(DIM)) / 2
        for c in range(DIM)]) for b in range(DIM)]) for a in range(DIM)])


def curvature_point(coords, epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature,
                    backreaction=True, angular_derivatives=True):
    args = (epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature, backreaction, angular_derivatives)
    g = metric_point(coords, *args)
    inverse = torch.linalg.inv(g)
    gamma = connection_point(coords, *args)
    dgamma = jacfwd(connection_point, argnums=0)(coords, *args)
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
    return g, inverse, gamma, ricci, weyl


def density_point(coords, epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature,
                  backreaction=True, angular_derivatives=True):
    g, inverse, _, _, weyl = curvature_point(
        coords, epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature,
        backreaction, angular_derivatives,
    )
    cup = torch.einsum("ae,bf,cg,dh,efgh->abcd", inverse, inverse, inverse, inverse, weyl)
    return torch.sqrt(torch.abs(torch.linalg.det(g))) * torch.einsum("abcd,abcd->", weyl, cup)


def weyl_point(coords, epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature):
    return curvature_point(coords, epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature)[4]


def divergence_point(coords, epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature):
    args = (epsilon, area_amp, shear_amp, ycoeff, acoeff, scoeff, ucoeff, curvature)
    _, inverse, gamma, _, weyl = curvature_point(coords, *args)
    dweyl = jacfwd(weyl_point, argnums=0)(coords, *args)
    zero = coords[0] * 0

    def partial_weyl(a, c, b, d, coordinate):
        selected = slot(coordinate)
        return dweyl[a, c, b, d, selected] if selected is not None else zero

    return torch.stack([torch.stack([torch.stack([
        sum(inverse[d, e] * (
            partial_weyl(a, c, b, d, e)
            - sum(gamma[q, e, a] * weyl[q, c, b, d] + gamma[q, e, c] * weyl[a, q, b, d]
                  + gamma[q, e, b] * weyl[a, c, q, d] + gamma[q, e, d] * weyl[a, c, b, q]
                  for q in range(DIM))
        ) for d in range(DIM) for e in range(DIM))
        for b in range(DIM)]) for c in range(DIM)]) for a in range(DIM)])


def bach_point(coords, ycoeff, curvature):
    zero = torch.tensor([0.0])
    one = torch.tensor([1.0])
    args = (torch.tensor(0.0), torch.tensor(0.0), torch.tensor(0.0), ycoeff, one, zero, zero, curvature)
    _, inverse, gamma, ricci, weyl = curvature_point(coords, *args)
    divergence = divergence_point(coords, *args)
    ddivergence = jacfwd(divergence_point, argnums=0)(coords, *args)
    ricci_up = torch.einsum("ac,bd,cd->ab", inverse, inverse, ricci)
    zero_scalar = coords[0] * 0

    def partial_divergence(a, c, b, coordinate):
        selected = slot(coordinate)
        return ddivergence[a, c, b, selected] if selected is not None else zero_scalar

    return torch.stack([torch.stack([
        sum(inverse[c, f] * (
            partial_divergence(a, c, b, f)
            - sum(gamma[q, f, a] * divergence[q, c, b] + gamma[q, f, c] * divergence[a, q, b]
                  + gamma[q, f, b] * divergence[a, c, q] for q in range(DIM))
        ) for c in range(DIM) for f in range(DIM))
        + sum(ricci_up[c, d] * weyl[a, c, b, d] / 2 for c in range(DIM) for d in range(DIM))
        for b in range(DIM)]) for a in range(DIM)])


def symbolic_expected(text, raw_r, raw_theta, curvature):
    rs, ts = sp.symbols("r theta", real=True)
    yf, bf, cf, ff = [sp.Function(name) for name in ("y", "b", "c", "F")]
    expression = sp.sympify(text, locals={"r": rs, "theta": ts, "K": sp.Symbol("K"), "y": yf, "b": bf, "c": cf, "F": ff})
    yexpr = 2 + rs / 3 + rs**2 / 5 - rs**3 / 7
    aexpr = 1 + rs / 5 + rs**2 / 10
    sexpr = rs / 7 - rs**2 / 11
    bexpr, cexpr = aexpr * sp.exp(sexpr), aexpr * sp.exp(-sexpr)
    fexpr = {1: sp.sin(ts), 0: sp.Integer(1), -1: sp.cosh(ts)}[curvature]
    substitutions = {sp.Symbol("K"): curvature}
    for function, profile in ((yf, yexpr), (bf, bexpr), (cf, cexpr)):
        substitutions[function(rs)] = profile
        for order in range(1, 3):
            substitutions[sp.diff(function(rs), rs, order)] = sp.diff(profile, rs, order)
    substitutions[ff(ts)] = fexpr
    substitutions[sp.diff(ff(ts), ts)] = sp.diff(fexpr, ts)
    value = expression.subs(substitutions).subs({rs: sp.Rational(str(raw_r)), ts: sp.Rational(str(raw_theta))})
    return float(sp.N(value, 17))


def relative_error(a, b):
    scale = max(1e-10, abs(a), abs(b))
    return abs(a - b) / scale


def main():
    background = json.loads((HERE / "BACKGROUND_CLOSURE.json").read_text(encoding="utf-8"))
    ycoeff = torch.tensor([2, 1/3, 1/5, -1/7])
    acoeff = torch.tensor([1, 1/5, 1/10])
    scoeff = torch.tensor([0, 1/7, -1/11])
    ucoeff = torch.tensor([0, 2/5, -1/4, 1/6])
    zero_u = torch.tensor([0.0])
    records = []
    for curvature, raw_theta in ((1, 0.7), (0, 0.4), (-1, 0.6)):
        for raw_r in (-1/3, 1/5):
            coords = torch.tensor([raw_r, raw_theta])
            direct = float(density_point(coords, torch.tensor(0.0), torch.tensor(0.0), torch.tensor(0.0),
                                         ycoeff, acoeff, scoeff, zero_u, curvature))
            expected = symbolic_expected(background["action_density"], raw_r, raw_theta, curvature)
            records.append({"K": curvature, "r": raw_r, "theta": raw_theta, "direct": direct,
                            "formula": expected, "scaled_error": relative_error(direct, expected)})

    product_one = torch.tensor([1.0])
    product_zero = torch.tensor([0.0])
    coords = torch.tensor([0.2, 0.7])
    einstein_y = torch.tensor([2.0, 0.0, -1.0])
    conformal_y = torch.tensor([2.0, 0.0, 1.0])
    einstein_bach = bach_point(coords, einstein_y, 1)
    conformal_bach = bach_point(coords, conformal_y, 1)

    def shear_derivative(profile):
        return jacfwd(lambda shear_amp: density_point(
            coords, torch.tensor(0.0), torch.tensor(0.0), shear_amp, profile,
            product_one, product_zero, product_zero, 1,
        ))(torch.tensor(0.0))

    einstein_shear = float(shear_derivative(einstein_y))
    conformal_shear = float(shear_derivative(conformal_y))
    einstein_expected = float(-32 * math.sin(0.7) / 3)

    mixed_records = []
    for curvature, raw_theta in ((1, 0.7), (0, 0.4), (-1, 0.6)):
        for raw_r in (-1/3, 1/5):
            point = torch.tensor([raw_r, raw_theta])
            def parameter_density(parameters):
                return density_point(point, parameters[0], parameters[1], parameters[2],
                                     ycoeff, acoeff, scoeff, ucoeff, curvature)
            hessian = jacfwd(jacfwd(parameter_density))(torch.zeros(3))
            mixed_records.append({"K": curvature, "r": raw_r, "theta": raw_theta,
                                  "twist_area": float(hessian[0, 1]), "twist_shear": float(hessian[0, 2]),
                                  "pure_twist": float(hessian[0, 0])})

    constant_differences = []
    for curvature, raw_theta in ((1, 0.7), (0, 0.4), (-1, 0.6)):
        point = torch.tensor([0.2, raw_theta])
        center = density_point(point, torch.tensor(0.0), torch.tensor(0.0), torch.tensor(0.0),
                               ycoeff, acoeff, scoeff, torch.tensor([2/7]), curvature)
        shifted = density_point(point, torch.tensor(0.2), torch.tensor(0.0), torch.tensor(0.0),
                                ycoeff, acoeff, scoeff, torch.tensor([2/7]), curvature)
        constant_differences.append(float(torch.abs(shifted - center)))

    max_background = max(row["scaled_error"] for row in records)
    max_bach = max(float(torch.max(torch.abs(einstein_bach))), float(torch.max(torch.abs(conformal_bach))))
    max_mixed = max(max(abs(row["twist_area"]), abs(row["twist_shear"])) for row in mixed_records)
    min_pure = min(abs(row["pure_twist"]) for row in mixed_records)
    max_constant = max(constant_differences)
    checks = {
        "background_density_matches": max_background <= 1e-8,
        "einstein_and_conformal_products_bach_zero": max_bach <= 1e-9,
        "einstein_restricted_shear_matches": relative_error(einstein_shear, einstein_expected) <= 1e-8,
        "conformal_restricted_shear_zero": abs(conformal_shear) <= 1e-9,
        "twist_even_sector_mixed_blocks_zero": max_mixed <= 1e-9,
        "pure_twist_control_nonzero": min_pure > 1e-6,
        "constant_connection_zero_mode": max_constant <= 1e-9,
    }
    if not all(checks.values()):
        raise AssertionError({"checks": checks, "max_background": max_background, "max_bach": max_bach,
                              "einstein_shear": einstein_shear, "einstein_expected": einstein_expected,
                              "conformal_shear": conformal_shear, "max_mixed": max_mixed,
                              "min_pure": min_pure, "max_constant": max_constant})

    with (HERE / "BACKGROUND_VERIFICATION_POINTS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    with (HERE / "MIXED_BLOCK_POINTS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(mixed_records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(mixed_records)
    result = {
        "schema": "udt-c2-transverse-coframe-independent-verification-1.0",
        "result": "PASS", "checks": checks,
        "counts": {"background_records": len(records), "mixed_block_records": len(mixed_records), "bach_components": 32},
        "maxima": {"background_scaled_error": max_background, "bach_zero_absolute": max_bach,
                   "mixed_block_absolute": max_mixed, "constant_connection_absolute": max_constant},
        "controls": {"einstein_restricted_shear": einstein_shear, "einstein_expected": einstein_expected,
                     "conformal_restricted_shear": conformal_shear, "minimum_pure_twist_magnitude": min_pure},
        "compute": {"method": "independent Torch two-coordinate forward-AD metric, Bach, action, and parameter Hessian", "dtype": "float64", "cpu_only": True},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", **result["counts"], **result["maxima"], **result["controls"]}, sort_keys=True))


if __name__ == "__main__":
    main()
