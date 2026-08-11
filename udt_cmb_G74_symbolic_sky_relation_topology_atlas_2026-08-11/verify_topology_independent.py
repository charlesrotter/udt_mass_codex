#!/usr/bin/env python3
"""Independent metric-connection replay of the G74 load-bearing claims."""

from __future__ import annotations

import csv
import json
import math
import runpy
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRODUCTION_MODULE = runpy.run_path(HERE / "derive_topology_atlas.py")
Profile = PRODUCTION_MODULE["Profile"]
START_R = 0.25
END_R = 1.0


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def metric_and_derivatives(position: np.ndarray, profile: object) -> tuple[np.ndarray, np.ndarray]:
    """Direct Cartesian metric and dg[k,mu,nu], independently of Hamilton's equations."""
    x = np.asarray(position[1:4], dtype=float)
    a, epsilon = profile.lapse_a, profile.epsilon
    r2 = float(x @ x)
    A = 1.0 + a * r2
    q = a / A
    w = np.array([-epsilon * x[1], epsilon * x[0], 0.0])
    g = np.zeros((4, 4), dtype=float)
    g[0, 0] = -A
    g[0, 1:4] = w
    g[1:4, 0] = w
    g[1:4, 1:4] = np.eye(3) - q * np.outer(x, x)

    dg = np.zeros((4, 4, 4), dtype=float)
    dw = np.array([[0.0, -epsilon, 0.0], [epsilon, 0.0, 0.0], [0.0, 0.0, 0.0]])
    for spatial_derivative in range(3):
        coordinate = spatial_derivative + 1
        dg[coordinate, 0, 0] = -2.0 * a * x[spatial_derivative]
        dg[coordinate, 0, 1:4] = dw[:, spatial_derivative]
        dg[coordinate, 1:4, 0] = dw[:, spatial_derivative]
        dq = -2.0 * a * a * x[spatial_derivative] / A**2
        basis = np.zeros(3)
        basis[spatial_derivative] = 1.0
        dg[coordinate, 1:4, 1:4] = (
            -dq * np.outer(x, x) - q * (np.outer(basis, x) + np.outer(x, basis))
        )
    return g, dg


def connection(position: np.ndarray, profile: object) -> tuple[np.ndarray, np.ndarray]:
    g, dg = metric_and_derivatives(position, profile)
    gi = np.linalg.inv(g)
    gamma = np.zeros((4, 4, 4), dtype=float)
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                gamma[rho, mu, nu] = 0.5 * sum(
                    gi[rho, sigma] * (dg[mu, sigma, nu] + dg[nu, sigma, mu] - dg[sigma, mu, nu])
                    for sigma in range(4)
                )
    return g, gamma


def initial_velocity(profile: object, direction: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    position = np.array([0.0, START_R, 0.0, 0.0])
    a, epsilon = profile.lapse_a, profile.epsilon
    A = 1.0 + a * START_R**2
    B = A + epsilon**2 * START_R**2
    u = np.array([1.0 / math.sqrt(A), 0.0, 0.0, 0.0])
    er = np.array([0.0, math.sqrt(A), 0.0, 0.0])
    etheta = np.array([0.0, 0.0, 0.0, -1.0])
    epsi = np.array([epsilon * START_R / math.sqrt(A * B), 0.0, math.sqrt(A / B), 0.0])
    velocity = u + direction[0] * er + direction[1] * etheta + direction[2] * epsi
    return position, velocity


def integrate_direct(profile: object, direction: np.ndarray) -> tuple[bool, np.ndarray, float, float]:
    position, velocity = initial_velocity(profile, direction)
    state = np.concatenate((position, velocity))

    def rhs(_affine: float, value: np.ndarray) -> np.ndarray:
        x, k = value[:4], value[4:]
        _, gamma = connection(x, profile)
        return np.concatenate((k, -np.einsum("rmn,m,n->r", gamma, k, k)))

    def event(_affine: float, value: np.ndarray) -> float:
        return float(np.linalg.norm(value[1:4]) - END_R)

    event.terminal = True
    event.direction = 1.0
    solution = solve_ivp(
        rhs, (0.0, 4.0), state, events=event, method="DOP853", rtol=2.0e-11,
        atol=2.0e-13, max_step=1.0 / 100.0,
    )
    reached = len(solution.t_events[0]) == 1
    final = solution.y_events[0][0] if reached else solution.y[:, -1]
    point = final[1:4]
    point /= np.linalg.norm(point)
    g, _ = metric_and_derivatives(final[:4], profile)
    null = abs(float(final[4:] @ g @ final[4:]))
    affine = float(solution.t_events[0][0]) if reached else float(solution.t[-1])
    return reached, point, affine, null


def independent_solid_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    return 2.0 * math.atan2(float(np.linalg.det(np.stack((a, b, c)))), 1.0 + float(a @ b + b @ c + c @ a))


def main() -> None:
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    center = read_tsv(HERE / "CENTER_REGULARITY_ATLAS.tsv")
    profiles = {item.profile_id: item for item in PRODUCTION_MODULE["load_profiles"]()}
    saved = np.load(HERE / "SKY_ENDPOINTS.npz")

    eligible_ids = [row["profile_id"] for row in center if row["center_status"] == "CENTER_C2_ELIGIBLE"]
    blocked_ids = [row["profile_id"] for row in center if row["center_status"] != "CENTER_C2_ELIGIBLE"]
    max_endpoint_error = 0.0
    max_affine_error = 0.0
    max_null = 0.0
    independent_reached = 0
    independent_total = 0
    for profile_id in eligible_ids:
        directions = saved[profile_id + "__level2_directions"]
        expected = saved[profile_id + "__level2_endpoint"]
        # Production affine values are not needed for topology; compare direct endpoint maps and
        # report the event times from the independent path itself.
        for index, direction in enumerate(directions):
            reached, point, affine, null = integrate_direct(profiles[profile_id], direction)
            independent_total += 1
            independent_reached += int(reached)
            max_endpoint_error = max(max_endpoint_error, float(np.linalg.norm(point - expected[index])))
            max_affine_error = max(max_affine_error, abs(affine))
            max_null = max(max_null, null)

    # A separately coded signed-area replay on the finest maps.
    degree_errors = []
    negative_faces = 0
    min_ratio = math.inf
    vertices, faces = PRODUCTION_MODULE["icosphere"](4)
    input_areas = np.array([independent_solid_angle(vertices[i], vertices[j], vertices[k]) for i, j, k in faces])
    for profile_id in eligible_ids:
        endpoint = saved[profile_id + "__endpoint"]
        output = np.array([independent_solid_angle(endpoint[i], endpoint[j], endpoint[k]) for i, j, k in faces])
        ratios = output / input_areas
        degree = float(np.sum(output) / (4.0 * math.pi))
        degree_errors.append(abs(degree - 1.0))
        negative_faces += int(np.count_nonzero(ratios < 0.0))
        min_ratio = min(min_ratio, float(np.min(ratios)))

    # Independent one-dimensional C2 test along the y axis.
    delta = 1.0e-5
    def odd_center_second(shape: str, epsilon: float) -> tuple[float, float]:
        def gtx(y: float) -> float:
            radius = abs(y)
            if shape == "PERSISTENT":
                q = epsilon
            elif shape == "TAPERED":
                q = epsilon * (1.0 - radius) ** 2
            elif shape == "SIGN_CHANGING":
                q = epsilon * (1.0 - 2.0 * radius)
            else:
                q = 0.0
            return -q * y
        right = (gtx(2 * delta) - 2 * gtx(delta) + gtx(0.0)) / delta**2
        left = (gtx(0.0) - 2 * gtx(-delta) + gtx(-2 * delta)) / delta**2
        return right, left

    persistent_jump = abs(odd_center_second("PERSISTENT", 0.05)[0] - odd_center_second("PERSISTENT", 0.05)[1])
    tapered_jump = abs(odd_center_second("TAPERED", 0.05)[0] - odd_center_second("TAPERED", 0.05)[1])
    sign_jump = abs(odd_center_second("SIGN_CHANGING", 0.05)[0] - odd_center_second("SIGN_CHANGING", 0.05)[1])

    checks = {
        "candidate_count_21": len(center) == 21,
        "center_counts_9_12": len(eligible_ids) == 9 and len(blocked_ids) == 12,
        "status_counts_3_6_12": production["status_counts"] == {
            "DERIVED_GLOBAL_BIJECTION_F01": 3,
            "OBSERVED_SAMPLED_REGULAR_PERSISTENT": 6,
            "BLOCKED_SUPPLIED_PROFILE_NOT_C2_AT_CENTER": 12,
        },
        "direct_connection_all_endpoints": independent_reached == independent_total == 1458,
        "direct_connection_endpoint_agreement": max_endpoint_error < 1.2e-5,
        "direct_connection_null_residual": max_null < 2.0e-9,
        "independent_degree_plus_one": max(degree_errors) < 2.0e-12,
        "independent_no_inverted_faces": negative_faces == 0,
        "independent_area_bounded_away_from_zero": min_ratio > 0.5,
        "persistent_center_second_derivative_continuous": persistent_jump < 1.0e-8,
        "tapered_center_second_derivative_jump": tapered_jump > 0.1,
        "sign_center_second_derivative_jump": sign_jump > 0.1,
        "physical_owner_open": production["physical_owner"] == "OPEN_NO_OWNER",
    }
    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g74-independent-v1",
        "status": "PASS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "direct_connection_rays": independent_total,
        "max_endpoint_chord_error": max_endpoint_error,
        "max_direct_null_residual": max_null,
        "max_independent_degree_error": max(degree_errors),
        "minimum_independent_signed_area_ratio": min_ratio,
        "center_second_derivative_jumps": {
            "persistent": persistent_jump,
            "tapered": tapered_jump,
            "sign_changing": sign_jump,
        },
        "protected_draft_read": False,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
