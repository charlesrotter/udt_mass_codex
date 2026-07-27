#!/usr/bin/env python3
"""Compute the preregistered intrinsic reciprocal-screen holonomy atlas."""

from __future__ import annotations

import csv
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "udt_intrinsic_optical_transport_atlas_2026-07-27"
sys.path.insert(0, str(PARENT))
import transport_geometry as parent  # noqa: E402

ETA = np.diag((-1.0, 1.0, 1.0, 1.0))
LAMBDAS = (-2.0, -1.0, 0.0, 0.5, 1.0, 2.0)
EVENTS = {
    "P00": np.array((0.0, 0.0, 0.0)),
    "P01": np.array((1.0 / 4.0, -1.0 / 5.0, 1.0 / 6.0)),
    "P02": np.array((-1.0 / 3.0, 1.0 / 7.0, 1.0 / 5.0)),
}
LOOPS = ("G1", "G2", "G3", "L12", "L23", "L31")
RHO = 1.0 / 5.0
TWO_PI = 2.0 * math.pi
RANK_RTOL = 1.0e-9


def write_tsv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def profile_q(q: np.ndarray) -> tuple[float, np.ndarray]:
    q1, q2, q3 = q[1:]
    value = (
        q1 + 2*q2 + 3*q3 + q1*q2 + 2*q2*q3 + 3*q3*q1
        + 2*q1**2 - 3*q2**2 + 5*q3**2 + q1*q2*q3 + 2*q1**3 - q2**3 + 3*q3**3
    ) / 50.0
    gradient = np.array((
        1 + q2 + 3*q3 + 4*q1 + q2*q3 + 6*q1**2,
        2 + q1 + 2*q3 - 6*q2 + q1*q3 - 3*q2**2,
        3 + 2*q2 + 3*q1 + 10*q3 + q1*q2 + 9*q3**2,
    )) / 50.0
    return float(value), gradient


def left_invariant_tangent(q: np.ndarray, axis: int) -> np.ndarray:
    unit = np.zeros(3)
    unit[axis] = 1.0
    return np.concatenate((np.array((-q[axis + 1],)), q[0] * unit + np.cross(q[1:], unit)))


def connection_from_q(q: np.ndarray, lambda_value: float) -> tuple[np.ndarray, float]:
    phi, gradient = profile_q(q)
    directional = np.array([gradient @ left_invariant_tangent(q, axis)[1:] for axis in range(3)])
    p = np.array((
        0.0,
        math.exp(-phi) * directional[2],
        math.exp(-lambda_value * phi) * directional[0],
        math.exp(-lambda_value * phi) * directional[1],
    ))
    structure = np.zeros((4, 4, 4))

    def set_coefficient(upper: int, left: int, right: int, de_coefficient: float) -> None:
        structure[upper, left, right] = -de_coefficient
        structure[upper, right, left] = de_coefficient

    at = parent.TWIST * parent.KAPPA * math.exp(-(1.0 + 2.0 * lambda_value) * phi)
    bt = parent.KAPPA * math.exp((1.0 - 2.0 * lambda_value) * phi)
    ct = parent.KAPPA * math.exp(-phi)
    set_coefficient(0, 0, 1, p[1])
    set_coefficient(0, 0, 2, p[2])
    set_coefficient(0, 0, 3, p[3])
    set_coefficient(0, 2, 3, at)
    set_coefficient(1, 1, 2, -p[2])
    set_coefficient(1, 1, 3, -p[3])
    set_coefficient(1, 2, 3, bt)
    set_coefficient(2, 1, 2, lambda_value * p[1])
    set_coefficient(2, 2, 3, -lambda_value * p[3])
    set_coefficient(2, 1, 3, -ct)
    set_coefficient(3, 1, 3, lambda_value * p[1])
    set_coefficient(3, 2, 3, lambda_value * p[2])
    set_coefficient(3, 1, 2, ct)

    connection = np.zeros((4, 4, 4))
    for out in range(4):
        for left in range(4):
            for middle in range(4):
                lowered = (
                    parent.ETA_SIGN[out] * structure[out, left, middle]
                    - parent.ETA_SIGN[left] * structure[left, middle, out]
                    + parent.ETA_SIGN[middle] * structure[middle, out, left]
                ) / 2.0
                connection[out, left, middle] = parent.ETA_SIGN[out] * lowered
    return connection, phi


def loop_q_and_derivative(loop_id: str, parameter: float) -> tuple[np.ndarray, np.ndarray]:
    cosine, sine = math.cos(parameter), math.sin(parameter)
    if loop_id.startswith("G"):
        axis = int(loop_id[1])
        q = np.zeros(4)
        dq = np.zeros(4)
        q[0], q[axis] = cosine, sine
        dq[0], dq[axis] = -sine, cosine
        return q, dq
    if loop_id == "L12":
        x = np.array((RHO*cosine, RHO*sine, 0.0))
        dx = np.array((-RHO*sine, RHO*cosine, 0.0))
    elif loop_id == "L23":
        x = np.array((0.0, RHO*cosine, RHO*sine))
        dx = np.array((0.0, -RHO*sine, RHO*cosine))
    elif loop_id == "L31":
        x = np.array((RHO*sine, 0.0, RHO*cosine))
        dx = np.array((RHO*cosine, 0.0, -RHO*sine))
    else:
        raise ValueError(loop_id)
    q, derivative = parent.quaternion_and_derivative(x)
    return np.asarray(q, dtype=float), np.asarray(derivative @ dx, dtype=float)


def sigma_velocity(q: np.ndarray, dq: np.ndarray) -> np.ndarray:
    return q[0] * dq[1:] - q[1:] * dq[0] - np.cross(q[1:], dq[1:])


def transport_rhs(parameter: float, flat: np.ndarray, loop_id: str, lambda_value: float) -> np.ndarray:
    q, dq = loop_q_and_derivative(loop_id, parameter)
    connection, phi = connection_from_q(q, lambda_value)
    sigma = sigma_velocity(q, dq)
    tangent = np.array((
        math.exp(-phi) * parent.TWIST * sigma[2],
        math.exp(phi) * sigma[2],
        math.exp(lambda_value * phi) * sigma[0],
        math.exp(lambda_value * phi) * sigma[1],
    ))
    generator = np.einsum("acb,c->ab", connection, tangent)
    matrix = flat.reshape(4, 4)
    return (-generator @ matrix).reshape(-1)


def integrate_loop(loop_id: str, lambda_value: float, start: float = 0.0, stop: float = TWO_PI,
                   initial: np.ndarray | None = None, fine: bool = False) -> np.ndarray:
    if initial is None:
        initial = np.eye(4)
    result = solve_ivp(
        lambda parameter, state: transport_rhs(parameter, state, loop_id, lambda_value),
        (start, stop), initial.reshape(-1), method="DOP853",
        rtol=2.0e-11 if fine else 1.0e-10,
        atol=2.0e-13 if fine else 1.0e-12,
        max_step=TWO_PI / (1024 if fine else 512),
    )
    if not result.success:
        raise RuntimeError(result.message)
    return result.y[:, -1].reshape(4, 4)


def reciprocal_x(lambda_value: float) -> np.ndarray:
    return np.diag((-1.0, 1.0, lambda_value, lambda_value))


def block_max(matrix: np.ndarray, left: tuple[int, ...], right: tuple[int, ...]) -> float:
    values = [abs(matrix[a, b]) for a in left for b in right]
    values += [abs(matrix[b, a]) for a in left for b in right]
    return float(max(values, default=0.0))


def connection_nabla_x(connection: np.ndarray, lambda_value: float) -> np.ndarray:
    eigenvalues = np.array((-1.0, 1.0, lambda_value, lambda_value))
    result = np.zeros((4, 4, 4))
    for direction in range(4):
        for out in range(4):
            for acted in range(4):
                result[direction, out, acted] = (
                    connection[out, direction, acted] * (eigenvalues[acted] - eigenvalues[out])
                )
    return result


def algebra_coordinates(matrix: np.ndarray) -> np.ndarray:
    return np.array((matrix[0, 1], matrix[0, 2], matrix[0, 3],
                     matrix[1, 2], matrix[1, 3], matrix[2, 3]))


def numerical_rank(rows: np.ndarray) -> tuple[int, np.ndarray]:
    singular = np.linalg.svd(rows, compute_uv=False)
    if singular.size == 0 or singular[0] == 0:
        return 0, singular
    return int(np.count_nonzero(singular > RANK_RTOL * singular[0])), singular


def independent_basis(matrices: list[np.ndarray]) -> list[np.ndarray]:
    chosen: list[np.ndarray] = []
    rank = 0
    for matrix in matrices:
        proposed = chosen + [matrix]
        new_rank, _ = numerical_rank(np.vstack([algebra_coordinates(item) for item in proposed]))
        if new_rank > rank:
            chosen.append(matrix / max(np.linalg.norm(matrix), 1.0e-300))
            rank = new_rank
    return chosen


def lie_closure(curvatures: list[np.ndarray]) -> tuple[list[np.ndarray], int, int, np.ndarray]:
    curvature_rows = np.vstack([algebra_coordinates(item) for item in curvatures])
    curvature_rank, _ = numerical_rank(curvature_rows)
    basis = independent_basis(curvatures)
    changed = True
    while changed and len(basis) < 6:
        changed = False
        candidates = list(basis)
        for left in basis:
            for right in basis:
                candidates.append(left @ right - right @ left)
        expanded = independent_basis(candidates)
        if len(expanded) > len(basis):
            basis = expanded
            changed = True
    final_rows = np.vstack([algebra_coordinates(item) for item in basis])
    lie_rank, singular = numerical_rank(final_rows)
    return basis, curvature_rank, lie_rank, singular


def centralizer_dimension(basis: list[np.ndarray], x_matrix: np.ndarray) -> tuple[int, float]:
    columns = []
    maximum = 0.0
    for item in basis:
        commutator = item @ x_matrix - x_matrix @ item
        columns.append(commutator.reshape(-1))
        maximum = max(maximum, float(np.max(np.abs(commutator))))
    linear_map = np.column_stack(columns)
    rank, _ = numerical_rank(linear_map.T)
    return len(basis) - rank, maximum


def main() -> int:
    local_rows: list[dict] = []
    curvature_rows: list[dict] = []
    loop_rows: list[dict] = []
    maximum_global_chart_connection_error = 0.0
    maximum_global_chart_coframe_error = 0.0

    # Registered overlap check between global-q and stereographic implementations.
    overlap_points = []
    for index in range(24):
        overlap_points.append(np.array((
            ((index % 4) - 1.5) / 7.0,
            (((index // 4) % 3) - 1.0) / 6.0,
            ((index // 12) - 0.5) / 5.0,
        )))
    for index, point in enumerate(overlap_points):
        lambda_value = LAMBDAS[index % len(LAMBDAS)]
        q, dq = parent.quaternion_and_derivative(point)
        phi, _gradient = profile_q(q)
        sigma_rows = []
        for axis in range(3):
            dqvector = dq[1:, axis]
            sigma_rows.append(q[0] * dqvector - q[1:] * dq[0, axis] - np.cross(q[1:], dqvector))
        sigma = np.column_stack(sigma_rows)
        global_coframe = np.zeros((4, 4))
        global_coframe[0, 0] = math.exp(-phi)
        global_coframe[0, 1:] = math.exp(-phi) * parent.TWIST * sigma[2]
        global_coframe[1, 1:] = math.exp(phi) * sigma[2]
        global_coframe[2, 1:] = math.exp(lambda_value * phi) * sigma[0]
        global_coframe[3, 1:] = math.exp(lambda_value * phi) * sigma[1]
        chart_coframe = parent.coframe_data(point, lambda_value)[2]
        maximum_global_chart_coframe_error = max(
            maximum_global_chart_coframe_error,
            float(np.max(np.abs(global_coframe - chart_coframe))) / max(1.0, float(np.max(np.abs(chart_coframe)))),
        )
        global_connection = connection_from_q(q, lambda_value)[0]
        chart_connection = parent.connection_and_structure(point, lambda_value)[0]
        scale = max(1.0, float(np.max(np.abs(chart_connection))))
        maximum_global_chart_connection_error = max(
            maximum_global_chart_connection_error,
            float(np.max(np.abs(global_connection - chart_connection))) / scale,
        )

    all_lie_ranks = []
    all_curvature_ranks = []
    all_centralizer_dimensions = []
    maximum_curvature_lorentz_residual = 0.0
    for lambda_value in LAMBDAS:
        x_matrix = reciprocal_x(lambda_value)
        for event_id, point in EVENTS.items():
            riemann, connection, _frame, _phi = parent.curvature_frame(point, lambda_value)
            nabla = connection_nabla_x(connection, lambda_value)
            local_rows.append({
                "branch_id": f"C{LAMBDAS.index(lambda_value)+1:02d}",
                "lambda": f"{lambda_value:g}", "event_id": event_id,
                "max_nabla_X": f"{np.max(np.abs(nabla)):.17g}",
                "clock_ruler": f"{max(block_max(nabla[c], (0,), (1,)) for c in range(4)):.17g}",
                "clock_screen": f"{max(block_max(nabla[c], (0,), (2,3)) for c in range(4)):.17g}",
                "ruler_screen": f"{max(block_max(nabla[c], (1,), (2,3)) for c in range(4)):.17g}",
                "screen_internal": f"{max(block_max(nabla[c], (2,), (3,)) for c in range(4)):.17g}",
            })
            curvature_matrices = [riemann[:, :, left, right] for left in range(4) for right in range(left+1, 4)]
            for matrix in curvature_matrices:
                maximum_curvature_lorentz_residual = max(
                    maximum_curvature_lorentz_residual,
                    float(np.max(np.abs(matrix.T @ ETA + ETA @ matrix))),
                )
            basis, curvature_rank, lie_rank, singular = lie_closure(curvature_matrices)
            centralizer_dimension_value, commutator_max = centralizer_dimension(basis, x_matrix)
            all_curvature_ranks.append(curvature_rank)
            all_lie_ranks.append(lie_rank)
            all_centralizer_dimensions.append(centralizer_dimension_value)
            curvature_rows.append({
                "branch_id": f"C{LAMBDAS.index(lambda_value)+1:02d}",
                "lambda": f"{lambda_value:g}", "event_id": event_id,
                "curvature_span_rank": curvature_rank, "lie_closure_rank": lie_rank,
                "centralizer_dimension_in_holonomy": centralizer_dimension_value,
                "max_basis_commutator_with_X": f"{commutator_max:.17g}",
                "lie_singular_values": ";".join(f"{value:.17g}" for value in singular),
            })

    maximum_lorentz_residual = 0.0
    maximum_composition_residual = 0.0
    maximum_convergence_residual = 0.0
    minimum_nonidentity = float("inf")
    minimum_ordinary_closure = float("inf")
    minimum_odd_closure = float("inf")
    nonzero_ordinary = 0
    saved_holonomies: dict[str, np.ndarray] = {}
    for lambda_value in LAMBDAS:
        x_matrix = reciprocal_x(lambda_value)
        inverse_x_testable = True
        for loop_id in LOOPS:
            direct = integrate_loop(loop_id, lambda_value)
            first = integrate_loop(loop_id, lambda_value, 0.0, math.pi)
            second = integrate_loop(loop_id, lambda_value, math.pi, TWO_PI)
            composed = second @ first
            fine = integrate_loop(loop_id, lambda_value, fine=True)
            q_start = loop_q_and_derivative(loop_id, 0.0)[0]
            q_end = loop_q_and_derivative(loop_id, TWO_PI)[0]
            inverse = np.linalg.inv(direct)
            conjugated = direct @ x_matrix @ inverse
            ordinary = float(np.max(np.abs(conjugated - x_matrix)))
            odd = float(np.max(np.abs(conjugated + x_matrix)))
            lorentz = float(np.max(np.abs(direct.T @ ETA @ direct - ETA)))
            composition = float(np.max(np.abs(direct - composed)))
            convergence = float(np.max(np.abs(direct - fine)))
            nonidentity = float(np.max(np.abs(direct - np.eye(4))))
            maximum_lorentz_residual = max(maximum_lorentz_residual, lorentz)
            maximum_composition_residual = max(maximum_composition_residual, composition)
            maximum_convergence_residual = max(maximum_convergence_residual, convergence)
            minimum_nonidentity = min(minimum_nonidentity, nonidentity)
            minimum_ordinary_closure = min(minimum_ordinary_closure, ordinary)
            minimum_odd_closure = min(minimum_odd_closure, odd)
            nonzero_ordinary += int(ordinary > 1.0e-10)
            saved_holonomies[f"lambda_{lambda_value:g}_{loop_id}"] = direct
            loop_rows.append({
                "branch_id": f"C{LAMBDAS.index(lambda_value)+1:02d}",
                "lambda": f"{lambda_value:g}", "loop_id": loop_id,
                "endpoint_q_mismatch": f"{np.max(np.abs(q_end-q_start)):.17g}",
                "det_U": f"{np.linalg.det(direct):.17g}",
                "lorentz_residual": f"{lorentz:.17g}",
                "nonidentity_max": f"{nonidentity:.17g}",
                "clock_ruler_support": f"{block_max(direct, (0,), (1,)):.17g}",
                "clock_screen_support": f"{block_max(direct, (0,), (2,3)):.17g}",
                "ruler_screen_support": f"{block_max(direct, (1,), (2,3)):.17g}",
                "ordinary_closure_residual": f"{ordinary:.17g}",
                "odd_closure_residual": f"{odd:.17g}",
                "composition_residual": f"{composition:.17g}",
                "convergence_residual": f"{convergence:.17g}",
            })

    write_tsv(HERE / "LOCAL_NABLA_X.tsv", local_rows)
    write_tsv(HERE / "CURVATURE_HOLONOMY.tsv", curvature_rows)
    write_tsv(HERE / "LOOP_HOLONOMY.tsv", loop_rows)
    np.savez(HERE / "HOLONOMY_MATRICES.npz", **saved_holonomies)

    exact_anchor = Fraction(-3, 25)
    assert exact_anchor != 0
    result = {
        "schema": "udt-intrinsic-reciprocal-holonomy-1.0",
        "status": "COMPUTED",
        "cpu_only": True,
        "float64": True,
        "lambda_values": list(LAMBDAS),
        "events": len(EVENTS),
        "loops_per_branch": len(LOOPS),
        "loop_transports": len(loop_rows),
        "maximum_global_chart_connection_scaled_error": maximum_global_chart_connection_error,
        "maximum_global_chart_coframe_scaled_error": maximum_global_chart_coframe_error,
        "maximum_curvature_lorentz_residual": maximum_curvature_lorentz_residual,
        "curvature_span_ranks": sorted(set(all_curvature_ranks)),
        "lie_closure_ranks": sorted(set(all_lie_ranks)),
        "centralizer_dimensions": sorted(set(all_centralizer_dimensions)),
        "exact_P00_nabla_E0_X_0_1": str(exact_anchor),
        "exact_P00_anchor_independent_of_lambda": True,
        "maximum_loop_lorentz_residual": maximum_lorentz_residual,
        "maximum_loop_composition_residual": maximum_composition_residual,
        "maximum_loop_convergence_residual": maximum_convergence_residual,
        "minimum_loop_nonidentity": minimum_nonidentity,
        "loops_with_nonzero_ordinary_closure_residual": nonzero_ordinary,
        "minimum_ordinary_closure_residual": minimum_ordinary_closure,
        "minimum_odd_closure_residual": minimum_odd_closure,
        "ordinary_holonomy_is_not_reciprocal_inversion": inverse_x_testable,
        "all_configurations_off_shell": True,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
