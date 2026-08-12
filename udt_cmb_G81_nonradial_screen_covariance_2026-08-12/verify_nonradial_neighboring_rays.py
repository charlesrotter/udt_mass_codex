#!/usr/bin/env python3
"""Independent Christoffel/neighboring-ray replay of the two G81 controls."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
DELTAS = (1.0e-4, 5.0e-5)  # NUMERIC: independently registered before this run.
A_ROT = np.array([[3.0 / 5.0, -4.0 / 5.0], [4.0 / 5.0, 3.0 / 5.0]])
B_ROT = np.array([[5.0 / 13.0, -12.0 / 13.0], [12.0 / 13.0, 5.0 / 13.0]])
CONTROLS = (
    ("C0_RADIAL_ROTATED", (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
    (
        "C1_FULL_ANGULAR",
        (12.0 / 13.0, 3.0 / 13.0, 4.0 / 13.0),
        (0.0, 4.0 / 5.0, -3.0 / 5.0),
        (-5.0 / 13.0, 36.0 / 65.0, 48.0 / 65.0),
    ),
)


def fields(x: float) -> tuple[float, float, float, float]:
    return 1.0 - x * x / 4.0, -x / 2.0, x**6 / 20.0, 3.0 * x**5 / 10.0


def metric_and_first(position: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    _, x, theta, _ = position
    A, Ax, h, hx = fields(float(x))
    sn, cs = math.sin(float(theta)), math.cos(float(theta))
    g = np.zeros((4, 4), dtype=np.float64)
    g[0, 0], g[1, 1], g[2, 2], g[3, 3] = -A, 1.0 / A, x * x, x * x * sn * sn
    g[0, 3] = g[3, 0] = h * sn * sn
    dg = np.zeros((4, 4, 4), dtype=np.float64)
    dg[1, 0, 0] = -Ax
    dg[1, 1, 1] = -Ax / (A * A)
    dg[1, 2, 2] = 2.0 * x
    dg[1, 3, 3] = 2.0 * x * sn * sn
    dg[1, 0, 3] = dg[1, 3, 0] = hx * sn * sn
    dg[2, 3, 3] = 2.0 * x * x * sn * cs
    dg[2, 0, 3] = dg[2, 3, 0] = 2.0 * h * sn * cs
    return g, dg


def connection(position: np.ndarray) -> np.ndarray:
    g, dg = metric_and_first(position)
    gi = np.linalg.inv(g)
    Gamma = np.zeros((4, 4, 4), dtype=np.float64)
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                for lam in range(4):
                    Gamma[rho, mu, nu] += 0.5 * gi[rho, lam] * (
                        dg[mu, lam, nu] + dg[nu, lam, mu] - dg[lam, mu, nu]
                    )
    return Gamma


def observer(position: np.ndarray) -> np.ndarray:
    A = fields(float(position[1]))[0]
    return np.array([1.0 / math.sqrt(A), 0.0, 0.0, 0.0])


def frequency(position: np.ndarray, tangent: np.ndarray) -> float:
    g, _ = metric_and_first(position)
    return -float(observer(position) @ g @ tangent)


def receiver_frame() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    p = np.array([0.0, 0.25, math.pi / 2.0, 0.0])
    A, _, h, _ = fields(0.25)
    block = A * 0.25**2 + h * h
    triad = np.stack((
        np.array([0.0, math.sqrt(A), 0.0, 0.0]),
        np.array([0.0, 0.0, 4.0, 0.0]),
        np.array([h / (math.sqrt(A) * math.sqrt(block)), 0.0, 0.0, math.sqrt(A) / math.sqrt(block)]),
    ))
    return p, observer(p), triad


def integrate(
    position: np.ndarray,
    tangent: np.ndarray,
    screen: np.ndarray | None,
    *,
    target_x: float | None = None,
    direction: float = 0.0,
    affine_end: float | None = None,
) -> object:
    state0 = np.concatenate((position, tangent)) if screen is None else np.concatenate((position, tangent, screen.ravel()))

    def rhs(_affine: float, state: np.ndarray) -> np.ndarray:
        p, k = state[:4], state[4:8]
        Gamma = connection(p)
        dk = -np.einsum("rmn,m,n->r", Gamma, k, k)
        if screen is None:
            return np.concatenate((k, dk))
        E = state[8:16].reshape(2, 4)
        dE = -np.einsum("rmn,m,an->ar", Gamma, k, E)
        return np.concatenate((k, dk, dE.ravel()))

    events = None
    if target_x is not None:
        def event(_affine: float, state: np.ndarray) -> float:
            return float(state[1] - target_x)
        event.terminal = True
        event.direction = direction
        events = event
    return solve_ivp(
        rhs,
        (0.0, 10.0 if affine_end is None else affine_end),
        state0,
        events=events,
        dense_output=True,
        method="DOP853",
        rtol=2.0e-12,
        atol=2.0e-14,
        max_step=1.0 / 800.0,
    )


def endpoint(solution: object, event: bool) -> tuple[float, np.ndarray]:
    affine = float(solution.t_events[0][0]) if event else float(solution.t[-1])
    return affine, np.asarray(solution.sol(affine), dtype=np.float64)


def neighboring_map(
    position: np.ndarray,
    time_axis: np.ndarray,
    direction_axis: np.ndarray,
    initial_screen: np.ndarray,
    affine: float,
    projection_screen: np.ndarray,
    endpoint_metric: np.ndarray,
    time_sign: float,
    direction_sign: float,
) -> tuple[dict[float, np.ndarray], float]:
    maps: dict[float, np.ndarray] = {}
    max_null = 0.0
    for delta in DELTAS:
        D = np.zeros((2, 2))
        for column in range(2):
            plus_k = time_sign * time_axis + direction_sign * direction_axis * math.cos(delta) + initial_screen[column] * math.sin(delta)
            minus_k = time_sign * time_axis + direction_sign * direction_axis * math.cos(delta) - initial_screen[column] * math.sin(delta)
            plus = integrate(position, plus_k, None, affine_end=affine)
            minus = integrate(position, minus_k, None, affine_end=affine)
            assert plus.success and minus.success
            deviation = (plus.y[:4, -1] - minus.y[:4, -1]) / (2.0 * delta)
            D[:, column] = projection_screen @ endpoint_metric @ deviation
            for solution in (plus, minus):
                p, k = solution.y[:4, -1], solution.y[4:8, -1]
                g, _ = metric_and_first(p)
                max_null = max(max_null, abs(float(k @ g @ k)))
        maps[delta] = D
    return maps, max_null


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def run_control(control: tuple, production: dict) -> dict:
    control_id, direction, screen1, screen2 = control
    p_r, u_r, triad = receiver_frame()
    n_r = np.asarray(direction) @ triad
    E_r = np.stack((np.asarray(screen1) @ triad, np.asarray(screen2) @ triad))
    forward = integrate(p_r, u_r + n_r, E_r, target_x=1.0, direction=1.0)
    assert forward.success and len(forward.t_events[0]) == 1
    forward_affine, forward_state = endpoint(forward, True)
    p_s, k_s = forward_state[:4], forward_state[4:8]
    E_s = forward_state[8:16].reshape(2, 4)
    Z = frequency(p_s, k_s)
    u_s = observer(p_s)
    n_s = k_s / Z - u_s
    reverse = integrate(p_s, -k_s / Z, E_s, target_x=0.25, direction=-1.0)
    reverse_rot = integrate(p_s, -k_s / Z, A_ROT @ E_s, target_x=0.25, direction=-1.0)
    assert reverse.success and reverse_rot.success
    assert len(reverse.t_events[0]) == len(reverse_rot.t_events[0]) == 1
    reverse_affine, reverse_state = endpoint(reverse, True)
    _, reverse_rot_state = endpoint(reverse_rot, True)
    p_back, k_back = reverse_state[:4], reverse_state[4:8]
    E_back = reverse_state[8:16].reshape(2, 4)
    g_s, _ = metric_and_first(p_s)
    g_back, _ = metric_and_first(p_back)

    forward_maps, null_forward = neighboring_map(p_r, u_r, n_r, E_r, forward_affine, E_s, g_s, 1.0, 1.0)
    reverse_maps, null_reverse = neighboring_map(p_s, u_s, n_s, E_s, reverse_affine, E_back, g_back, -1.0, -1.0)
    rotated_maps, null_rotated = neighboring_map(
        p_s, u_s, n_s, A_ROT @ E_s, reverse_affine, B_ROT @ E_r, g_back, -1.0, -1.0
    )
    forward_coarse, forward_fine = (forward_maps[value] for value in DELTAS)
    reverse_coarse, reverse_fine = (reverse_maps[value] for value in DELTAS)
    rotated_coarse, rotated_fine = (rotated_maps[value] for value in DELTAS)
    D_forward_production = np.asarray(production["forward"]["D"])
    D_reverse_production = np.asarray(production["reverse_unrotated"]["D"])
    D_rotated_production = np.asarray(production["reverse_rotated"]["D"])
    inverse_Z = abs(frequency(p_back, k_back)) / abs(frequency(p_s, -k_s / Z))
    result = {
        "control_id": control_id,
        "Z": Z,
        "inverse_Z": inverse_Z,
        "frequency_product_error": abs(Z * inverse_Z - 1.0),
        "endpoint_return_max_absolute": float(np.max(np.abs(p_back - p_r))),
        "rotated_endpoint_return_max_absolute": float(np.max(np.abs(reverse_rot_state[:4] - p_r))),
        "forward_coarse_fine_relative": relative(forward_coarse, forward_fine),
        "reverse_coarse_fine_relative": relative(reverse_coarse, reverse_fine),
        "rotated_coarse_fine_relative": relative(rotated_coarse, rotated_fine),
        "forward_fine_D": forward_fine.tolist(),
        "reverse_fine_D": reverse_fine.tolist(),
        "rotated_fine_D": rotated_fine.tolist(),
        "forward_production_relative": relative(forward_fine, D_forward_production),
        "reverse_production_relative": relative(reverse_fine, D_reverse_production),
        "rotated_production_relative": relative(rotated_fine, D_rotated_production),
        "independent_unrotated_reciprocity_relative": relative(reverse_fine, Z * forward_fine.T),
        "independent_rotated_covariance_relative": relative(rotated_fine, Z * B_ROT @ forward_fine.T @ A_ROT.T),
        "independent_area_ratio_minus_Z": abs(
            math.sqrt(abs(float(np.linalg.det(reverse_fine))))
            / math.sqrt(abs(float(np.linalg.det(forward_fine)))) - Z
        ),
        "max_endpoint_null_absolute": max(null_forward, null_reverse, null_rotated),
    }
    gates = {
        "frequency": result["frequency_product_error"] < 1.0e-10,
        "endpoint": max(result["endpoint_return_max_absolute"], result["rotated_endpoint_return_max_absolute"]) < 1.0e-8,
        "production_maps": max(
            result["forward_production_relative"], result["reverse_production_relative"], result["rotated_production_relative"]
        ) < 2.0e-4,
        "unrotated_reciprocity": result["independent_unrotated_reciprocity_relative"] < 2.0e-4,
        "rotated_covariance": result["independent_rotated_covariance_relative"] < 2.0e-4,
        "area": result["independent_area_ratio_minus_Z"] < 2.0e-4,
        "null": result["max_endpoint_null_absolute"] < 1.0e-9,
    }
    result["gates"] = gates
    result["status"] = "PASS" if all(gates.values()) else "FAIL"
    return result


def main() -> None:
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert [row["control_id"] for row in production["controls"]] == [row[0] for row in CONTROLS]
    results = [run_control(control, prod) for control, prod in zip(CONTROLS, production["controls"], strict=True)]
    output = {
        "schema": "udt-cmb-g81-independent-neighboring-ray-v1",
        "method": "locally rebuilt full Christoffels plus centered neighboring rays; no production Riemann or Jacobi equation",
        "status": "PASS" if all(row["status"] == "PASS" for row in results) else "FAIL",
        "deltas": list(DELTAS),
        "controls": results,
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(rendered, encoding="utf-8")
    (HERE / "INDEPENDENT_TRANSCRIPT.txt").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if output["status"] != "PASS":
        raise SystemExit("independent G81 gate failed")


if __name__ == "__main__":
    main()
