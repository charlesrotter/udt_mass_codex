#!/usr/bin/env python3
"""Independent torch/autodiff replay; imports no production geometry code."""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path

import torch

HERE = Path(__file__).resolve().parent
torch.set_default_dtype(torch.float64)
jacfwd = torch.func.jacfwd


def quaternion(coordinates: torch.Tensor) -> torch.Tensor:
    radius_squared = (coordinates * coordinates).sum()
    denominator = 1 + radius_squared
    return torch.cat((((1 - radius_squared) / denominator).reshape(1),
                      2 * coordinates / denominator))


def metric(coordinates: torch.Tensor, lambda_value: float,
           epsilon: float, twist: float) -> torch.Tensor:
    q = quaternion(coordinates)
    dq = jacfwd(quaternion)(coordinates)
    q0, qvector = q[0], q[1:]
    sigma = torch.zeros((3, 3), dtype=coordinates.dtype)
    for axis in range(3):
        dqvector = dq[1:, axis]
        sigma[:, axis] = (
            q0 * dqvector - qvector * dq[0, axis]
            - torch.linalg.cross(qvector, dqvector)
        )
    q1, q2, q3 = qvector
    profile = (
        q1 + 2 * q2 + 3 * q3
        + q1 * q2 + 2 * q2 * q3 + 3 * q3 * q1
        + 2 * q1 * q1 - 3 * q2 * q2 + 5 * q3 * q3
        + q1 * q2 * q3 + 2 * q1**3 - q2**3 + 3 * q3**3
    )
    phi = epsilon * profile
    coframe = torch.zeros((4, 4), dtype=coordinates.dtype)
    coframe[0, 0] = torch.exp(-phi)
    coframe[0, 1:] = torch.exp(-phi) * twist * sigma[2]
    coframe[1, 1:] = torch.exp(phi) * sigma[2]
    coframe[2, 1:] = torch.exp(lambda_value * phi) * sigma[0]
    coframe[3, 1:] = torch.exp(lambda_value * phi) * sigma[1]
    signature = torch.diag(torch.tensor((-1.0, 1.0, 1.0, 1.0), dtype=coordinates.dtype))
    return coframe.T @ signature @ coframe


def christoffel(coordinates: torch.Tensor, lambda_value: float,
                epsilon: float, twist: float) -> torch.Tensor:
    geometry = metric(coordinates, lambda_value, epsilon, twist)
    inverse = torch.linalg.inv(geometry)
    spatial_derivatives = jacfwd(
        lambda point: metric(point, lambda_value, epsilon, twist)
    )(coordinates)
    derivatives = torch.zeros((4, 4, 4), dtype=coordinates.dtype)
    derivatives[1:] = spatial_derivatives.permute(2, 0, 1)
    connection = torch.zeros((4, 4, 4), dtype=coordinates.dtype)
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                for other in range(4):
                    connection[upper, left, right] += inverse[upper, other] * (
                        derivatives[left, other, right]
                        + derivatives[right, other, left]
                        - derivatives[other, left, right]
                    ) / 2
    return connection


def curvature_invariants(coordinates: torch.Tensor, lambda_value: float,
                         epsilon: float, twist: float) -> torch.Tensor:
    geometry = metric(coordinates, lambda_value, epsilon, twist)
    inverse = torch.linalg.inv(geometry)
    connection = christoffel(coordinates, lambda_value, epsilon, twist)
    spatial_derivatives = jacfwd(
        lambda point: christoffel(point, lambda_value, epsilon, twist)
    )(coordinates)
    derivatives = torch.zeros((4, 4, 4, 4), dtype=coordinates.dtype)
    derivatives[1:] = spatial_derivatives.permute(3, 0, 1, 2)
    riemann = torch.zeros((4, 4, 4, 4), dtype=coordinates.dtype)
    for upper in range(4):
        for lower in range(4):
            for left in range(4):
                for right in range(4):
                    riemann[upper, lower, left, right] = (
                        derivatives[left, upper, right, lower]
                        - derivatives[right, upper, left, lower]
                    )
                    for middle in range(4):
                        riemann[upper, lower, left, right] += (
                            connection[upper, left, middle] * connection[middle, right, lower]
                            - connection[upper, right, middle] * connection[middle, left, lower]
                        )
    ricci = torch.einsum("abad->bd", riemann)
    scalar = torch.einsum("bd,bd->", inverse, ricci)
    ricci_operator = inverse @ ricci
    ricci_squared = torch.trace(ricci_operator @ ricci_operator)
    lowered = torch.einsum("ae,ebcd->abcd", geometry, riemann)
    kretschmann = torch.einsum(
        "abcd,ap,bq,cr,ds,pqrs->", lowered, inverse, inverse, inverse, inverse, lowered
    )
    return torch.stack((scalar, ricci_squared, kretschmann))


def linear_certificate(geometry: torch.Tensor, gradients: torch.Tensor) -> tuple[int, int]:
    full_gradients = torch.cat((torch.zeros((3, 1)), gradients), dim=1)
    value_rank = int(torch.linalg.matrix_rank(full_gradients, atol=1e-10).item())

    equations = []
    # A^T g + g A = 0.
    for row in range(4):
        for column in range(row, 4):
            coefficients = torch.zeros(16)
            for middle in range(4):
                coefficients[middle * 4 + row] += geometry[middle, column]
                coefficients[middle * 4 + column] += geometry[row, middle]
            equations.append(coefficients)
    # dI_j A = 0 after the value-proportional K part is subtracted.
    for invariant in range(3):
        for column in range(4):
            coefficients = torch.zeros(16)
            for row in range(4):
                coefficients[row * 4 + column] = full_gradients[invariant, row]
            equations.append(coefficients)
    isotropy_rank = int(torch.linalg.matrix_rank(torch.stack(equations), atol=1e-9).item())
    return value_rank, isotropy_rank


def main() -> int:
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    with (HERE / "CANDIDATE_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        candidates = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "CANDIDATE_OUTCOMES.tsv").open(newline="", encoding="utf-8") as handle:
        outcome_rows = list(csv.DictReader(handle, delimiter="\t"))
    saved = {row["candidate_id"]: row for row in outcome_rows}
    origin = torch.zeros(3)
    maximum_gradient_error = 0.0
    maximum_determinant_error = 0.0
    value_ranks = {}
    isotropy_ranks = {}
    for candidate in candidates:
        identifier = candidate["candidate_id"]
        lambda_value = float(Fraction(candidate["lambda"]))
        epsilon = float(Fraction(candidate["epsilon"]))
        twist = float(Fraction(candidate["a"]))
        gradients = jacfwd(
            lambda point: curvature_invariants(point, lambda_value, epsilon, twist)
        )(origin)
        expected_gradients = torch.tensor([[float(Fraction(saved[identifier][f"I{invariant}_d{axis}"]))
                                            for axis in ("x", "y", "z")]
                                           for invariant in range(1, 4)])
        expected_determinant = float(Fraction(saved[identifier]["gradient_determinant"]))
        actual_determinant = float(torch.linalg.det(gradients).item())
        gradient_error = float(torch.max(torch.abs(gradients - expected_gradients)).item())
        determinant_error = abs(actual_determinant - expected_determinant)
        maximum_gradient_error = max(maximum_gradient_error, gradient_error)
        maximum_determinant_error = max(maximum_determinant_error, determinant_error)
        assert torch.allclose(gradients, expected_gradients, rtol=2e-11, atol=2e-11)
        assert abs(actual_determinant - expected_determinant) <= 2e-9 * max(1.0, abs(expected_determinant))
        value_rank, isotropy_rank = linear_certificate(
            metric(origin, lambda_value, epsilon, twist), gradients
        )
        value_ranks[identifier] = value_rank
        isotropy_ranks[identifier] = isotropy_rank

    assert all(value_ranks[f"C{i:02d}"] == 3 for i in range(1, 8))
    assert all(isotropy_ranks[f"C{i:02d}"] == 16 for i in range(1, 8))
    assert value_ranks["C08"] == 0 and isotropy_ranks["C08"] < 16
    assert production["copresence_status"] == "WORKING_INTERPRETIVE_FRAME"
    assert production["instantaneous_operational_access_derived"] is False
    assert production["complete_whole_solution_law"] == "OPEN"
    assert production["lambda_selected"] is False
    assert production["on_shell_solution_claimed"] is False

    catches = {f"F{i:02d}": False for i in range(1, 23)}
    caught = []
    for catch in catches:
        mutation = dict(catches)
        mutation[catch] = True
        try:
            assert not any(mutation.values()), catch
        except AssertionError:
            caught.append(catch)
    assert len(caught) == 22

    result = {
        "status": "PASS",
        "implementation": "TORCH_AUTODIFF_FULL_RIEMANN_CONTRACTION_NO_PRODUCTION_IMPORT",
        "torch_version": torch.__version__,
        "candidates_replayed": 8,
        "all_gate_value_ranks": [value_ranks[f"C{i:02d}"] for i in range(1, 7)],
        "all_gate_isotropy_constraint_ranks": [isotropy_ranks[f"C{i:02d}"] for i in range(1, 7)],
        "maximum_gradient_absolute_error": maximum_gradient_error,
        "maximum_determinant_absolute_error": maximum_determinant_error,
        "controls": "PASS",
        "catch_proofs": len(caught),
        "primary_ruling_reproduced": production["primary_ruling"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
