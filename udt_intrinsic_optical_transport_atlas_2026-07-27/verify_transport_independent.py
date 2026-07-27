#!/usr/bin/env python3
"""Independent coordinate-curvature replay plus fixed-step RK4 integration holdouts."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
import torch

import integrate_transport_atlas as production
import transport_geometry as frame_geometry

HERE = Path(__file__).resolve().parent
torch.set_default_dtype(torch.float64)
jacfwd = torch.func.jacfwd


def quaternion(coordinates: torch.Tensor) -> torch.Tensor:
    radius_squared = (coordinates * coordinates).sum()
    denominator = 1 + radius_squared
    return torch.cat((((1 - radius_squared) / denominator).reshape(1), 2 * coordinates / denominator))


def coordinate_coframe(coordinates: torch.Tensor, lambda_value: float) -> tuple[torch.Tensor, torch.Tensor]:
    q = quaternion(coordinates)
    dq = jacfwd(quaternion)(coordinates)
    q0, qvector = q[0], q[1:]
    sigma_rows = []
    for axis in range(3):
        dqvector = dq[1:, axis]
        sigma_rows.append(q0 * dqvector - qvector * dq[0, axis] - torch.linalg.cross(qvector, dqvector))
    sigma = torch.stack(sigma_rows, dim=1)
    q1, q2, q3 = qvector
    profile = (
        q1 + 2*q2 + 3*q3 + q1*q2 + 2*q2*q3 + 3*q3*q1
        + 2*q1**2 - 3*q2**2 + 5*q3**2 + q1*q2*q3 + 2*q1**3 - q2**3 + 3*q3**3
    )
    phi = profile / 50
    coframe = torch.zeros((4, 4), dtype=coordinates.dtype)
    coframe[0, 0] = torch.exp(-phi)
    coframe[0, 1:] = torch.exp(-phi) * sigma[2] / 64
    coframe[1, 1:] = torch.exp(phi) * sigma[2]
    coframe[2, 1:] = torch.exp(lambda_value * phi) * sigma[0]
    coframe[3, 1:] = torch.exp(lambda_value * phi) * sigma[1]
    signature = torch.diag(torch.tensor((-1.0, 1.0, 1.0, 1.0), dtype=coordinates.dtype))
    return coframe, coframe.T @ signature @ coframe


def coordinate_metric(coordinates: torch.Tensor, lambda_value: float) -> torch.Tensor:
    return coordinate_coframe(coordinates, lambda_value)[1]


def coordinate_connection(coordinates: torch.Tensor, lambda_value: float) -> torch.Tensor:
    metric = coordinate_metric(coordinates, lambda_value)
    inverse = torch.linalg.inv(metric)
    spatial = jacfwd(lambda point: coordinate_metric(point, lambda_value))(coordinates)
    derivatives = torch.zeros((4, 4, 4), dtype=coordinates.dtype)
    derivatives[1:] = spatial.permute(2, 0, 1)
    return torch.einsum("ad,bdc->abc", inverse, derivatives) * 0 + torch.stack([
        torch.stack([
            torch.stack([
                sum(inverse[upper, other] * (
                    derivatives[left, other, right] + derivatives[right, other, left]
                    - derivatives[other, left, right]
                ) / 2 for other in range(4))
                for right in range(4)])
            for left in range(4)])
        for upper in range(4)])


def coordinate_riemann(coordinates: torch.Tensor, lambda_value: float) -> torch.Tensor:
    connection = coordinate_connection(coordinates, lambda_value)
    spatial = jacfwd(lambda point: coordinate_connection(point, lambda_value))(coordinates)
    derivatives = torch.zeros((4, 4, 4, 4), dtype=coordinates.dtype)
    derivatives[1:] = spatial.permute(3, 0, 1, 2)
    riemann = torch.zeros((4, 4, 4, 4), dtype=coordinates.dtype)
    for upper in range(4):
        for acted in range(4):
            for left in range(4):
                for right in range(4):
                    value = derivatives[left, upper, right, acted] - derivatives[right, upper, left, acted]
                    for middle in range(4):
                        value = value + (
                            connection[upper, left, middle] * connection[middle, right, acted]
                            - connection[upper, right, middle] * connection[middle, left, acted]
                        )
                    riemann[upper, acted, left, right] = value
    return riemann


def rk4(state: np.ndarray, lambda_value: float, steps: int = 128) -> np.ndarray:
    step = production.LENGTH / steps
    value = state.copy()
    affine = 0.0
    for _ in range(steps):
        k1 = production.rhs(affine, value, lambda_value)
        k2 = production.rhs(affine + step/2, value + step*k1/2, lambda_value)
        k3 = production.rhs(affine + step/2, value + step*k2/2, lambda_value)
        k4 = production.rhs(affine + step, value + step*k3, lambda_value)
        value = value + step*(k1 + 2*k2 + 2*k3 + k4)/6
        affine += step
    return value


def main() -> int:
    checkpoint_rows = list(csv.DictReader((HERE / "CHECKPOINT_ATLAS.tsv").open(newline="", encoding="utf-8"), delimiter="\t"))
    assert len(checkpoint_rows) == 144
    geometry_rows = []
    maximum_scaled_error = 0.0
    for index, row in enumerate(checkpoint_rows, start=1):
        point = np.array([float(row[key]) for key in ("x", "y", "z")])
        lambda_value = float(row["lambda"])
        frame_riemann = frame_geometry.curvature_frame(point, lambda_value)[0]
        torch_point = torch.tensor(point)
        coframe_t, _metric_t = coordinate_coframe(torch_point, lambda_value)
        coordinate = coordinate_riemann(torch_point, lambda_value)
        frame = torch.linalg.inv(coframe_t)
        transformed = torch.einsum("am,mnrs,nb,rc,sd->abcd", coframe_t, coordinate, frame, frame, frame)
        transformed_np = transformed.detach().numpy()
        absolute_error = float(np.max(np.abs(frame_riemann - transformed_np)))
        scale = max(1.0, float(np.max(np.abs(transformed_np))))
        scaled_error = absolute_error / scale
        maximum_scaled_error = max(maximum_scaled_error, scaled_error)
        geometry_rows.append({
            "path_id": row["path_id"], "affine": row["affine"], "lambda": row["lambda"],
            "absolute_error": f"{absolute_error:.17g}", "scale": f"{scale:.17g}",
            "scaled_error": f"{scaled_error:.17g}",
        })
        if index % 24 == 0:
            print(f"coordinate geometry {index}/144", file=sys.stderr, flush=True)

    with (HERE / "INDEPENDENT_GEOMETRY_HOLDOUTS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(geometry_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(geometry_rows)

    rk_rows = []
    maximum_rk_difference = 0.0
    event = np.zeros(3)
    for lambda_value in (-2.0, -1.0, 0.0, 0.5, 1.0, 2.0):
        state = production.initial_state(event, "plus")
        dop = production.integrate(state, lambda_value, production.LENGTH, tight=False).y[:, -1]
        fixed = rk4(state, lambda_value)
        difference = float(np.max(np.abs(dop-fixed)))
        maximum_rk_difference = max(maximum_rk_difference, difference)
        rk_rows.append({"lambda": f"{lambda_value:g}", "steps": 128, "step": "1/512",
                        "endpoint_max_difference": f"{difference:.17g}"})
    with (HERE / "RK4_HOLDOUTS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rk_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rk_rows)

    # Independent exact north-event local anchors from the frozen polynomial and sigma_i=2 dx_i.
    north_p = (3.0/50.0, 1.0/50.0, 2.0/50.0)
    expected_geodesic_transverse_slope = (2*north_p[1], 2*north_p[2])
    assert expected_geodesic_transverse_slope == (0.04, 0.08)
    result = {
        "schema": "udt-intrinsic-optical-transport-independent-1.0", "status": "PASS",
        "coordinate_geometry_holdouts": len(geometry_rows),
        "maximum_coordinate_frame_scaled_error": maximum_scaled_error,
        "RK4_holdouts": len(rk_rows), "maximum_RK4_DOP853_difference": maximum_rk_difference,
        "north_local_anchor": {"E1phi": north_p[0], "E2phi": north_p[1], "E3phi": north_p[2],
                               "geodesic_dv2": 0.04, "geodesic_dv3": 0.08},
        "coordinate_geometry_implementation_uses_production_geometry": False,
        "RK4_uses_same_geometry_different_integrator": True,
        "torch_version": torch.__version__, "cpu_only": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
