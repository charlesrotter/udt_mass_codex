#!/usr/bin/env python3
"""Numeric tensor engine for the preregistered conditional stationary C2 tile.

All physics content is the metric written in ``metric_from_coefficients``.  The rest is a generic
coordinate-tensor and spectral/Galerkin implementation (category-A numerical method).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import torch


DTYPE = torch.float64  # NUMERICAL_CONTROL: backward-error requirement.
ETA_INDEX = 1  # DERIVED: coordinate order is (tau, eta, xi1, xi2).
DIMENSION = 4  # PINNED_BY_THEORY: declared four-dimensional conditional action class.


@dataclass(frozen=True)
class SpectralLayout:
    sector: str
    order: int
    n_degrees: tuple[int, ...]
    h_degrees: tuple[int, ...]
    s_degrees: tuple[int, ...]
    w_degrees: tuple[int, ...]

    @property
    def size(self) -> int:
        return sum(map(len, (self.n_degrees, self.h_degrees, self.s_degrees, self.w_degrees)))

    @property
    def slices(self) -> dict[str, slice]:
        lengths = [len(self.n_degrees), len(self.h_degrees), len(self.s_degrees), len(self.w_degrees)]
        starts = np.cumsum([0, *lengths])
        return {name: slice(int(starts[i]), int(starts[i + 1])) for i, name in enumerate("nhsw")}


def make_layout(sector: str, order: int) -> SpectralLayout:
    if order < 2:
        raise ValueError("order must be at least two")
    all_degrees = tuple(range(order + 1))
    if sector == "GENERAL":
        return SpectralLayout(sector, order, tuple(range(1, order + 1)), all_degrees,
                              all_degrees, tuple(range(1, order + 1)))
    even = tuple(k for k in all_degrees if k % 2 == 0)
    even_nonconstant = tuple(k for k in even if k)
    if sector == "SEAL_EVEN":
        return SpectralLayout(sector, order, even_nonconstant, even, even, even_nonconstant)
    if sector == "SEAL_ODD_W":
        odd = tuple(k for k in all_degrees if k % 2 == 1)
        return SpectralLayout(sector, order, even_nonconstant, even, even, odd)
    raise ValueError(f"unknown sector {sector}")


def chebyshev_table(x: torch.Tensor, order: int) -> list[torch.Tensor]:
    table = [torch.ones_like(x)]
    if order == 0:
        return table
    table.append(x)
    for _ in range(2, order + 1):
        table.append(2 * x * table[-1] - table[-2])
    return table


def chebyshev_zero(order: int) -> list[float]:
    values = [1.0]
    if order == 0:
        return values
    values.append(0.0)
    for _ in range(2, order + 1):
        values.append(-values[-2])
    return values


def series(coefficients: torch.Tensor, degrees: Iterable[int], table: list[torch.Tensor],
           subtract_midpoint: bool = False) -> torch.Tensor:
    degrees = tuple(degrees)
    if not degrees:
        return torch.zeros_like(table[0])
    mid = chebyshev_zero(len(table) - 1)
    terms = [table[k] - mid[k] if subtract_midpoint else table[k] for k in degrees]
    return sum(coefficients[i] * terms[i] for i in range(len(terms)))


def fields_from_coefficients(eta: torch.Tensor, coefficients: torch.Tensor,
                             layout: SpectralLayout) -> tuple[torch.Tensor, ...]:
    x = torch.cos(2 * eta)
    table = chebyshev_table(x, layout.order)
    sl = layout.slices
    # Coordinate gauges: n(eta=pi/4)=0 and W(eta=pi/4)=0.
    n = series(coefficients[sl["n"]], layout.n_degrees, table, subtract_midpoint=True)
    h = series(coefficients[sl["h"]], layout.h_degrees, table)
    squash = series(coefficients[sl["s"]], layout.s_degrees, table)
    shift = series(coefficients[sl["w"]], layout.w_degrees, table, subtract_midpoint=True)
    lapse = torch.exp(n)
    radial = torch.exp((1 - x * x) * h)  # DERIVED: H=1 at both registered primitive caps.
    fiber = torch.exp(squash)
    return lapse, radial, fiber, shift


def metric_from_coefficients(eta: torch.Tensor, coefficients: torch.Tensor,
                             layout: SpectralLayout) -> tuple[torch.Tensor, tuple[torch.Tensor, ...]]:
    lapse, radial, fiber, shift = fields_from_coefficients(eta, coefficients, layout)
    c2 = torch.cos(eta) ** 2
    s2 = torch.sin(eta) ** 2
    q = torch.sin(eta) * torch.cos(eta)
    count = eta.numel()
    g = torch.zeros((count, DIMENSION, DIMENSION), dtype=eta.dtype, device=eta.device)
    g[:, 0, 0] = -lapse * lapse + fiber * fiber * shift * shift
    g[:, 1, 1] = radial * radial
    g[:, 0, 2] = g[:, 2, 0] = fiber * fiber * shift * c2
    g[:, 0, 3] = g[:, 3, 0] = fiber * fiber * shift * s2
    g[:, 2, 2] = q * q + fiber * fiber * c2 * c2
    g[:, 2, 3] = g[:, 3, 2] = -q * q + fiber * fiber * c2 * s2
    g[:, 3, 3] = q * q + fiber * fiber * s2 * s2
    return g, (lapse, radial, fiber, shift)


def eta_derivatives(g: torch.Tensor, eta: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    first = torch.zeros_like(g)
    second = torch.zeros_like(g)
    for a in range(DIMENSION):
        for b in range(DIMENSION):
            d1 = torch.autograd.grad(g[:, a, b].sum(), eta, create_graph=True, retain_graph=True)[0]
            d2 = torch.autograd.grad(d1.sum(), eta, create_graph=True, retain_graph=True)[0]
            first[:, a, b] = d1
            second[:, a, b] = d2
    return first, second


def curvature_from_metric(g: torch.Tensor, dg: torch.Tensor, ddg: torch.Tensor) -> dict[str, torch.Tensor]:
    batch = g.shape[0]
    inverse = torch.linalg.inv(g)
    dinverse = -torch.einsum("...ab,...bc,...cd->...ad", inverse, dg, inverse)
    gamma = torch.zeros((batch, DIMENSION, DIMENSION, DIMENSION), dtype=g.dtype, device=g.device)
    dgamma = torch.zeros_like(gamma)
    for a in range(DIMENSION):
        for b in range(DIMENSION):
            for c in range(DIMENSION):
                base = torch.zeros((batch, DIMENSION), dtype=g.dtype, device=g.device)
                varied = torch.zeros_like(base)
                for e in range(DIMENSION):
                    base[:, e] = ((dg[:, e, c] if b == ETA_INDEX else 0)
                                  + (dg[:, e, b] if c == ETA_INDEX else 0)
                                  - (dg[:, b, c] if e == ETA_INDEX else 0))
                    varied[:, e] = ((ddg[:, e, c] if b == ETA_INDEX else 0)
                                    + (ddg[:, e, b] if c == ETA_INDEX else 0)
                                    - (ddg[:, b, c] if e == ETA_INDEX else 0))
                gamma[:, a, b, c] = torch.einsum("...e,...e->...", inverse[:, a, :], base) / 2
                dgamma[:, a, b, c] = (torch.einsum("...e,...e->...", dinverse[:, a, :], base)
                                             + torch.einsum("...e,...e->...", inverse[:, a, :], varied)) / 2
    rup = torch.zeros((batch, DIMENSION, DIMENSION, DIMENSION, DIMENSION), dtype=g.dtype, device=g.device)
    for a in range(DIMENSION):
        for b in range(DIMENSION):
            for c in range(DIMENSION):
                for d in range(DIMENSION):
                    value = (dgamma[:, a, b, d] if c == ETA_INDEX else 0) - (
                        dgamma[:, a, b, c] if d == ETA_INDEX else 0)
                    for e in range(DIMENSION):
                        value = value + gamma[:, a, e, c] * gamma[:, e, b, d]
                        value = value - gamma[:, a, e, d] * gamma[:, e, b, c]
                    rup[:, a, b, c, d] = value
    ricci = torch.zeros((batch, DIMENSION, DIMENSION), dtype=g.dtype, device=g.device)
    for b in range(DIMENSION):
        for d in range(DIMENSION):
            ricci[:, b, d] = sum(rup[:, a, b, a, d] for a in range(DIMENSION))
    scalar = torch.einsum("...ab,...ab->...", inverse, ricci)
    rlow = torch.einsum("...ae,...ebcd->...abcd", g, rup)
    weyl = torch.zeros_like(rlow)
    for a in range(DIMENSION):
        for b in range(DIMENSION):
            for c in range(DIMENSION):
                for d in range(DIMENSION):
                    trace = (g[:, a, c] * ricci[:, b, d] - g[:, a, d] * ricci[:, b, c]
                             - g[:, b, c] * ricci[:, a, d] + g[:, b, d] * ricci[:, a, c]) / 2
                    wedge = scalar * (g[:, a, c] * g[:, b, d] - g[:, a, d] * g[:, b, c]) / 6
                    weyl[:, a, b, c, d] = rlow[:, a, b, c, d] - trace + wedge
    weyl_squared = torch.einsum("...abcd,...ae,...bf,...cg,...dh,...efgh->...",
                                weyl, inverse, inverse, inverse, inverse, weyl)
    determinant = torch.linalg.det(g)
    return {"inverse": inverse, "gamma": gamma, "riemann_up": rup, "ricci": ricci,
            "scalar": scalar, "weyl": weyl, "weyl_squared": weyl_squared,
            "determinant": determinant}


def quadrature(nodes: int) -> tuple[torch.Tensor, torch.Tensor]:
    roots, weights = np.polynomial.legendre.leggauss(nodes)
    eta = torch.tensor((roots + 1) * np.pi / 4, dtype=DTYPE, requires_grad=True)
    weight = torch.tensor(weights * np.pi / 4, dtype=DTYPE)
    return eta, weight


def reduced_action(coefficients: torch.Tensor, layout: SpectralLayout, nodes: int = 48,
                   return_details: bool = False):
    eta, weights = quadrature(nodes)
    g, fields = metric_from_coefficients(eta, coefficients, layout)
    dg, ddg = eta_derivatives(g, eta)
    curvature = curvature_from_metric(g, dg, ddg)
    volume = torch.sqrt(-curvature["determinant"])
    density = volume * curvature["weyl_squared"]
    action = torch.dot(weights, density)
    if return_details:
        return action, {"eta": eta, "weights": weights, "g": g, "dg": dg, "ddg": ddg,
                        "fields": fields, "volume": volume, "density": density, **curvature}
    return action


def stationarity(coefficients: torch.Tensor, layout: SpectralLayout, nodes: int = 48,
                 create_graph: bool = False) -> torch.Tensor:
    action = reduced_action(coefficients, layout, nodes)
    return torch.autograd.grad(action, coefficients, create_graph=create_graph)[0]
