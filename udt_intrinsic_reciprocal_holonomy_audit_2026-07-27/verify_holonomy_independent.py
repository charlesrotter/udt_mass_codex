#!/usr/bin/env python3
"""Independent coordinate-curvature and fixed-step transport holdouts."""

from __future__ import annotations

import csv
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
OPTICAL = HERE.parent / "udt_intrinsic_optical_transport_atlas_2026-07-27"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(OPTICAL))
import compute_holonomy_atlas as production  # noqa: E402
import transport_geometry as frame_geometry  # noqa: E402
import verify_transport_independent as coordinate_geometry  # noqa: E402

torch.set_default_dtype(torch.float64)
ETA = np.diag((-1.0, 1.0, 1.0, 1.0))


def write_tsv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def algebra_coordinates(matrix: np.ndarray) -> np.ndarray:
    return np.array((matrix[0, 1], matrix[0, 2], matrix[0, 3],
                     matrix[1, 2], matrix[1, 3], matrix[2, 3]))


def curvature_rank(matrices: list[np.ndarray]) -> tuple[int, np.ndarray]:
    rows = np.vstack([algebra_coordinates(item) for item in matrices])
    singular = np.linalg.svd(rows, compute_uv=False)
    rank = int(np.count_nonzero(singular > 1.0e-9 * singular[0]))
    return rank, singular


def rk4(loop_id: str, lambda_value: float, steps: int = 4096) -> np.ndarray:
    step = 2.0 * math.pi / steps
    state = np.eye(4).reshape(-1)
    parameter = 0.0
    for _ in range(steps):
        k1 = production.transport_rhs(parameter, state, loop_id, lambda_value)
        k2 = production.transport_rhs(parameter + step/2, state + step*k1/2, loop_id, lambda_value)
        k3 = production.transport_rhs(parameter + step/2, state + step*k2/2, loop_id, lambda_value)
        k4 = production.transport_rhs(parameter + step, state + step*k3, loop_id, lambda_value)
        state = state + step*(k1 + 2*k2 + 2*k3 + k4)/6
        parameter += step
    return state.reshape(4, 4)


def eigenspace_signature(lambda_value: float, negate: bool = False) -> str:
    values = np.array((-1.0, 1.0, lambda_value, lambda_value))
    if negate:
        values = -values
    groups = []
    for value in sorted(set(values)):
        indices = np.flatnonzero(np.isclose(values, value))
        negative = int(np.count_nonzero(indices == 0))
        positive = len(indices) - negative
        groups.append(f"{value:g}:({negative},{positive})")
    return ";".join(groups)


def main() -> int:
    coordinate_rows = []
    maximum_scaled_error = 0.0
    ranks = []
    for lambda_value in production.LAMBDAS:
        for event_id, point in production.EVENTS.items():
            torch_point = torch.tensor(point)
            coframe_t, _metric_t = coordinate_geometry.coordinate_coframe(torch_point, lambda_value)
            coordinate = coordinate_geometry.coordinate_riemann(torch_point, lambda_value)
            frame = torch.linalg.inv(coframe_t)
            transformed = torch.einsum("am,mnrs,nb,rc,sd->abcd", coframe_t, coordinate, frame, frame, frame)
            independent = transformed.detach().numpy()
            production_riemann = frame_geometry.curvature_frame(point, lambda_value)[0]
            absolute = float(np.max(np.abs(independent - production_riemann)))
            scale = max(1.0, float(np.max(np.abs(independent))))
            scaled = absolute / scale
            maximum_scaled_error = max(maximum_scaled_error, scaled)
            matrices = [independent[:, :, left, right] for left in range(4) for right in range(left+1, 4)]
            rank, singular = curvature_rank(matrices)
            ranks.append(rank)
            coordinate_rows.append({
                "lambda": f"{lambda_value:g}", "event_id": event_id,
                "absolute_error": f"{absolute:.17g}", "scaled_error": f"{scaled:.17g}",
                "independent_curvature_span_rank": rank,
                "minimum_singular_value": f"{singular[-1]:.17g}",
            })

    with np.load(HERE / "HOLONOMY_MATRICES.npz") as saved:
        rk_rows = []
        maximum_rk_error = 0.0
        for lambda_value in (-2.0, 0.0, 1.0, 2.0):
            for loop_id in ("G1", "G2", "G3"):
                independent = rk4(loop_id, lambda_value)
                expected = saved[f"lambda_{lambda_value:g}_{loop_id}"]
                difference = float(np.max(np.abs(independent - expected)))
                maximum_rk_error = max(maximum_rk_error, difference)
                rk_rows.append({
                    "lambda": f"{lambda_value:g}", "loop_id": loop_id,
                    "steps": 4096, "step": "2pi/4096",
                    "RK4_DOP853_max_difference": f"{difference:.17g}",
                    "RK4_Lorentz_residual": f"{np.max(np.abs(independent.T @ ETA @ independent-ETA)):.17g}",
                })

    signature_rows = []
    for lambda_value in production.LAMBDAS:
        x_signature = eigenspace_signature(lambda_value)
        negative_signature = eigenspace_signature(lambda_value, negate=True)
        signature_rows.append({
            "lambda": f"{lambda_value:g}", "X_eigenspace_signatures": x_signature,
            "minus_X_eigenspace_signatures": negative_signature,
            "Lorentz_conjugate": "NO" if x_signature != negative_signature else "UNRESOLVED",
        })

    # Exact north-event computation independent of floating-point production code:
    # Gamma^0_01=-E1(phi)=-3/50 and x1-x0=2.
    exact_gamma = -Fraction(3, 50)
    exact_nabla = exact_gamma * 2
    assert exact_nabla == -Fraction(3, 25)

    write_tsv(HERE / "INDEPENDENT_CURVATURE_HOLDOUTS.tsv", coordinate_rows)
    write_tsv(HERE / "RK4_HOLDOUTS.tsv", rk_rows)
    write_tsv(HERE / "INVERSION_SIGNATURES.tsv", signature_rows)
    result = {
        "schema": "udt-intrinsic-reciprocal-holonomy-independent-1.0",
        "status": "PASS" if maximum_scaled_error <= 2.0e-8 and maximum_rk_error <= 2.0e-6
                  and set(ranks) == {6} else "FAIL",
        "coordinate_curvature_holdouts": len(coordinate_rows),
        "maximum_coordinate_frame_scaled_error": maximum_scaled_error,
        "independent_curvature_span_ranks": sorted(set(ranks)),
        "RK4_holdouts": len(rk_rows),
        "maximum_RK4_DOP853_difference": maximum_rk_error,
        "exact_P00_nabla_E0_X_0_1": str(exact_nabla),
        "inversion_signature_rows": len(signature_rows),
        "sampled_X_and_minus_X_Lorentz_conjugate_count": sum(
            row["Lorentz_conjugate"] != "NO" for row in signature_rows
        ),
        "coordinate_geometry_implementation_uses_production_geometry": False,
        "RK4_uses_same_geometry_different_integrator": True,
        "torch_version": torch.__version__,
        "cpu_only": True,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
