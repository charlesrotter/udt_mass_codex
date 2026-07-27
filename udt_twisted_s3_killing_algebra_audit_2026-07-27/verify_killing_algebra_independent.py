#!/usr/bin/env python3
"""Independent full-expression automatic-differentiation check of the exact jet result.

This implementation does not import the primary derivation.  It constructs the exact
unit-quaternion chart metric with sqrt and exp retained, differentiates the full metric
by CPU automatic differentiation, and compares the curvature-invariant gradient matrix
with the exact rational primary artifact.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import torch
from torch.func import jacrev


ROOT = Path(__file__).resolve().parent
torch.set_default_dtype(torch.float64)


def metric(coordinates: torch.Tensor) -> torch.Tensor:
    _, x, y, z = coordinates.unbind()
    w = torch.sqrt(1 - x * x - y * y - z * z)
    dw = torch.stack((-x / w, -y / w, -z / w))
    zero = torch.zeros_like(x)
    one = torch.ones_like(x)
    dx = torch.stack((one, zero, zero))
    dy = torch.stack((zero, one, zero))
    dz = torch.stack((zero, zero, one))

    sigma1 = w * dx - x * dw - y * dz + z * dy
    sigma2 = w * dy - y * dw - z * dx + x * dz
    sigma3 = w * dz - z * dw - x * dy + y * dx

    phi = (
        x
        + 2 * y
        + 3 * z
        + 4 * x * y
        + 5 * y * z
        + 6 * z * x
        + 7 * x * x
        + 11 * y * y
        + 13 * z * z
        + 17 * x * y * z
        + 19 * x * x * x
        + 23 * y * y * y
        + 29 * z * z * z
    ) / 400

    a = torch.as_tensor(0.1)
    lam = torch.as_tensor(2.0 / 3.0)
    em2 = torch.exp(-2 * phi)
    ep2 = torch.exp(2 * phi)
    e2l = torch.exp(2 * lam * phi)

    g = torch.zeros((4, 4), dtype=coordinates.dtype)
    g[0, 0] = -em2
    g[0, 1:] = -a * em2 * sigma3
    g[1:, 0] = g[0, 1:]
    spatial = (
        (ep2 - a * a * em2) * torch.outer(sigma3, sigma3)
        + e2l * (torch.outer(sigma1, sigma1) + torch.outer(sigma2, sigma2))
    )
    g[1:, 1:] = spatial
    return g


def christoffel(coordinates: torch.Tensor) -> torch.Tensor:
    g = metric(coordinates)
    g_inv = torch.linalg.inv(g)
    dg = jacrev(metric)(coordinates)  # dg[a,b,c] = partial_c g[a,b]
    gamma = torch.zeros((4, 4, 4), dtype=coordinates.dtype)
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                gamma[rho, mu, nu] = 0.5 * sum(
                    g_inv[rho, sig]
                    * (dg[sig, nu, mu] + dg[sig, mu, nu] - dg[mu, nu, sig])
                    for sig in range(4)
                )
    return gamma


def invariant_vector(coordinates: torch.Tensor) -> torch.Tensor:
    g = metric(coordinates)
    g_inv = torch.linalg.inv(g)
    gamma = christoffel(coordinates)
    dgamma = jacrev(christoffel)(coordinates)
    riemann = torch.zeros((4, 4, 4, 4), dtype=coordinates.dtype)
    for rho in range(4):
        for sig in range(4):
            for mu in range(4):
                for nu in range(4):
                    value = dgamma[rho, nu, sig, mu] - dgamma[rho, mu, sig, nu]
                    value = value + sum(
                        gamma[rho, mu, eta] * gamma[eta, nu, sig]
                        - gamma[rho, nu, eta] * gamma[eta, mu, sig]
                        for eta in range(4)
                    )
                    riemann[rho, sig, mu, nu] = value
    ricci = torch.zeros((4, 4), dtype=coordinates.dtype)
    for sig in range(4):
        for nu in range(4):
            ricci[sig, nu] = sum(riemann[rho, sig, rho, nu] for rho in range(4))
    mixed = g_inv @ ricci
    return torch.stack((torch.trace(mixed), torch.trace(mixed @ mixed), torch.trace(mixed @ mixed @ mixed)))


def main() -> None:
    primary = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    exact = torch.tensor(
        [[float(Fraction(value)) for value in row] for row in primary["invariant_gradient_matrix"]]
    )
    point = torch.zeros(4, requires_grad=True)
    values = invariant_vector(point)
    gradients = jacrev(invariant_vector)(point)[:, 1:]
    determinant = torch.linalg.det(gradients)
    max_absolute_error = torch.max(torch.abs(gradients - exact)).item()
    max_relative_error = torch.max(torch.abs((gradients - exact) / exact)).item()
    exact_det = float(Fraction(primary["invariant_gradient_determinant"]))
    determinant_relative_error = abs(determinant.item() - exact_det) / abs(exact_det)

    result = {
        "schema": "udt.twisted_s3_killing_algebra.independent.v1",
        "method": "full_sqrt_exp_metric_cpu_torch_nested_automatic_differentiation",
        "torch_version": torch.__version__,
        "device": "cpu",
        "dtype": "float64",
        "invariants_at_origin": values.detach().tolist(),
        "invariant_gradient_matrix": gradients.detach().tolist(),
        "invariant_gradient_determinant": determinant.item(),
        "primary_exact_determinant_float": exact_det,
        "max_gradient_absolute_error": max_absolute_error,
        "max_gradient_relative_error": max_relative_error,
        "determinant_relative_error": determinant_relative_error,
        "rank_three": int(torch.linalg.matrix_rank(gradients).item()) == 3,
        "agreement_pass": max_relative_error < 1e-10 and determinant_relative_error < 1e-10,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (ROOT / "INDEPENDENT_RESULT.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    assert result["rank_three"]
    assert result["agreement_pass"]


if __name__ == "__main__":
    main()
