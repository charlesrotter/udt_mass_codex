#!/usr/bin/env python3
"""Direct-Christoffel neighboring-ray replay of G80 forward/reverse reciprocity."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
DELTAS = (1.0e-4, 5.0e-5)


def radial_fields(x: float) -> tuple[float, float, float, float]:
    return 1.0 - x * x / 4.0, -x / 2.0, x**6 / 20.0, 3.0 * x**5 / 10.0


def metric_and_first(position: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    _, x, theta, _ = position
    A, Ax, h, hx = radial_fields(float(x))
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


def stationary_observer(position: np.ndarray) -> np.ndarray:
    A = radial_fields(float(position[1]))[0]
    return np.array([1.0 / math.sqrt(A), 0.0, 0.0, 0.0])


def receiver_frame() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    p = np.array([0.0, 0.25, math.pi / 2.0, 0.0])
    A, _, h, _ = radial_fields(0.25)
    block = A * 0.25**2 + h * h
    u = stationary_observer(p)
    radial = np.array([0.0, math.sqrt(A), 0.0, 0.0])
    e0 = np.array([0.0, 0.0, 4.0, 0.0])
    e1 = np.array([h / (math.sqrt(A) * math.sqrt(block)), 0.0, 0.0, math.sqrt(A) / math.sqrt(block)])
    return p, u, radial, e0, e1


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
        max_step=1.0 / 400.0,
    )


def frequency(position: np.ndarray, tangent: np.ndarray) -> float:
    g, _ = metric_and_first(position)
    return -float(stationary_observer(position) @ g @ tangent)


def endpoint(solution: object, event: bool) -> tuple[float, np.ndarray]:
    affine = float(solution.t_events[0][0]) if event else float(solution.t[-1])
    return affine, np.asarray(solution.sol(affine), dtype=np.float64)


def neighboring_map(
    position: np.ndarray,
    time_axis: np.ndarray,
    direction_axis: np.ndarray,
    screen_initial: np.ndarray,
    affine: float,
    endpoint_screen: np.ndarray,
    endpoint_metric: np.ndarray,
    time_sign: float,
    direction_sign: float,
) -> tuple[dict[float, np.ndarray], float]:
    maps: dict[float, np.ndarray] = {}
    max_null = 0.0
    for delta in DELTAS:
        D = np.zeros((2, 2))
        for column in range(2):
            plus_k = time_sign * time_axis + direction_sign * direction_axis * math.cos(delta) + screen_initial[column] * math.sin(delta)
            minus_k = time_sign * time_axis + direction_sign * direction_axis * math.cos(delta) - screen_initial[column] * math.sin(delta)
            plus = integrate(position, plus_k, None, affine_end=affine)
            minus = integrate(position, minus_k, None, affine_end=affine)
            assert plus.success and minus.success
            p_plus = plus.y[:4, -1]
            p_minus = minus.y[:4, -1]
            deviation = (p_plus - p_minus) / (2.0 * delta)
            D[:, column] = endpoint_screen @ endpoint_metric @ deviation
            for solution in (plus, minus):
                p, k = solution.y[:4, -1], solution.y[4:8, -1]
                g, _ = metric_and_first(p)
                max_null = max(max_null, abs(float(k @ g @ k)))
        maps[delta] = D
    return maps, max_null


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def main() -> None:
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    D_forward_production = np.asarray(production["forward"]["D"], dtype=np.float64)
    D_reverse_production = np.asarray(production["reverse"]["D"], dtype=np.float64)
    p_r, u_r, radial_r, e0_r, e1_r = receiver_frame()
    E_r = np.stack((e0_r, e1_r))
    forward = integrate(p_r, u_r + radial_r, E_r, target_x=1.0, direction=1.0)
    assert forward.success and len(forward.t_events[0]) == 1
    forward_affine, forward_state = endpoint(forward, True)
    p_s, k_s = forward_state[:4], forward_state[4:8]
    E_s = forward_state[8:16].reshape(2, 4)
    Z = frequency(p_s, k_s)
    u_s = stationary_observer(p_s)
    outward_s = k_s / Z - u_s
    k_reverse = -k_s / Z
    reverse = integrate(p_s, k_reverse, E_s, target_x=0.25, direction=-1.0)
    assert reverse.success and len(reverse.t_events[0]) == 1
    reverse_affine, reverse_state = endpoint(reverse, True)
    p_back, k_back = reverse_state[:4], reverse_state[4:8]
    E_back = reverse_state[8:16].reshape(2, 4)
    g_s, _ = metric_and_first(p_s)
    g_r, _ = metric_and_first(p_back)

    forward_maps, forward_null = neighboring_map(
        p_r, u_r, radial_r, E_r, forward_affine, E_s, g_s, 1.0, 1.0
    )
    reverse_maps, reverse_null = neighboring_map(
        p_s, u_s, outward_s, E_s, reverse_affine, E_back, g_r, -1.0, -1.0
    )
    forward_coarse, forward_fine = (forward_maps[value] for value in DELTAS)
    reverse_coarse, reverse_fine = (reverse_maps[value] for value in DELTAS)
    inverse_Z = abs(frequency(p_back, k_back)) / abs(frequency(p_s, k_reverse))
    output = {
        "schema": "udt-cmb-g80-independent-neighboring-ray-v1",
        "status": "PASS",
        "method": "direct Christoffel central rays plus finite-difference neighboring rays in both orientations; no production Riemann or Jacobi equation",
        "Z": Z,
        "inverse_Z": inverse_Z,
        "frequency_product_error": abs(Z * inverse_Z - 1.0),
        "forward_affine": forward_affine,
        "reverse_affine": reverse_affine,
        "endpoint_return_max_absolute": float(np.max(np.abs(p_back - p_r))),
        "screen_return_relative": relative(E_back, E_r),
        "forward_coarse_fine_relative": relative(forward_coarse, forward_fine),
        "reverse_coarse_fine_relative": relative(reverse_coarse, reverse_fine),
        "forward_fine_D": forward_fine.tolist(),
        "reverse_fine_D": reverse_fine.tolist(),
        "forward_production_relative": relative(forward_fine, D_forward_production),
        "reverse_production_relative": relative(reverse_fine, D_reverse_production),
        "independent_reciprocity_relative": relative(reverse_fine, Z * forward_fine.T),
        "independent_area_ratio_minus_Z": abs(
            math.sqrt(abs(float(np.linalg.det(reverse_fine))))
            / math.sqrt(abs(float(np.linalg.det(forward_fine)))) - Z
        ),
        "max_endpoint_null_absolute": max(forward_null, reverse_null),
    }
    assert output["frequency_product_error"] < 1.0e-10
    assert output["endpoint_return_max_absolute"] < 1.0e-8
    assert output["screen_return_relative"] < 1.0e-8
    assert output["forward_production_relative"] < 2.0e-4
    assert output["reverse_production_relative"] < 2.0e-4
    assert output["independent_reciprocity_relative"] < 2.0e-4
    assert output["independent_area_ratio_minus_Z"] < 2.0e-4
    assert output["max_endpoint_null_absolute"] < 1.0e-9
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
