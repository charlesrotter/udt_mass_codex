#!/usr/bin/env python3
"""Independent SciPy/finite-difference Christoffel panel for G77."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G75 = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11"
G76 = ROOT / "udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11"
START_R = 0.25
END_R = 1.0
AFFINE_CAP = 4.0
FD_STEP = 2.0e-6  # CHOSE_NUMERIC: finite-difference method control.
CHORD_TOL = 5.0e-5  # CHOSE_NUMERIC: preregistered registered-agreement tier.
NULL_TOL = 2.0e-7
PANEL = (
    "G75_AM_S13_E05", "G75_AP_S09_E100", "G75_AM_S16_E100", "G75_AP_S12_E05",
    "G75_AP_S04_E05", "G75_AM_S02_E100", "G75_AP_S03_E100", "G75_AM_S01_E05",
    "G75_A0_S03_E100", "G75_AM_S03_E100", "G75_AM_S24_E100",
)
RAY_INDICES = (0, 641, 1281, 1921, 2561)


@dataclass(frozen=True)
class Profile:
    profile_id: str
    lapse_a: float
    coefficients: tuple[float, float, float]
    stratum: str

    def q(self, s: float) -> float:
        c0, c1, c2 = self.coefficients
        return c0 + c1 * s + c2 * s * s


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def number(text: str) -> float:
    return float(Fraction(text))


def profiles() -> dict[str, Profile]:
    shapes = {row["shape_id"]: row for row in read_tsv(G75 / "SHAPE_ATLAS.tsv")}
    output = {}
    for row in read_tsv(G75 / "PROFILE_ATLAS.tsv"):
        if row["shape_id"] == "ZERO":
            coefficients, stratum = (0.0, 0.0, 0.0), "ZERO"
        else:
            shape = shapes[row["shape_id"]]
            amplitude = number(row["amplitude"])
            coefficients = tuple(amplitude * number(shape[f"normalized_c{i}"]) for i in range(3))
            stratum = shape["stratum_code"]
        output[row["profile_id"]] = Profile(row["profile_id"], number(row["lapse_a"]), coefficients, stratum)
    return output


def metric(profile: Profile, coordinate: np.ndarray) -> np.ndarray:
    X = coordinate[1:4]
    s = float(X @ X)
    A = 1.0 + profile.lapse_a * s
    q = profile.q(s)
    rotation = np.array([-X[1], X[0], 0.0])
    value = np.zeros((4, 4))
    value[0, 0] = -A
    value[0, 1:4] = value[1:4, 0] = q * rotation
    value[1:4, 1:4] = np.eye(3) - (profile.lapse_a / A) * np.outer(X, X)
    return value


def finite_difference_partial(profile: Profile, coordinate: np.ndarray) -> np.ndarray:
    partial = np.zeros((4, 4, 4))
    for axis in range(1, 4):
        plus, minus = coordinate.copy(), coordinate.copy()
        plus[axis] += FD_STEP
        minus[axis] -= FD_STEP
        partial[axis] = (metric(profile, plus) - metric(profile, minus)) / (2.0 * FD_STEP)
    return partial


def rhs(profile: Profile, _lambda: float, state: np.ndarray) -> np.ndarray:
    coordinate, tangent = state[:4], state[4:]
    g = metric(profile, coordinate)
    partial = finite_difference_partial(profile, coordinate)
    inverse = np.linalg.inv(g)
    gamma = np.zeros((4, 4, 4))
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                gamma[upper, left, right] = 0.5 * sum(
                    inverse[upper, lower]
                    * (partial[left, lower, right] + partial[right, lower, left] - partial[lower, left, right])
                    for lower in range(4)
                )
    acceleration = -np.einsum("mab,a,b->m", gamma, tangent, tangent)
    return np.concatenate((tangent, acceleration))


def initial(profile: Profile, direction: np.ndarray) -> np.ndarray:
    s0 = START_R * START_R
    q0 = profile.q(s0)
    A = 1.0 + profile.lapse_a * s0
    B = A + q0 * q0 * s0
    coordinate = np.array([0.0, START_R, 0.0, 0.0])
    tangent = np.array([
        1.0 / math.sqrt(A) + direction[2] * q0 * START_R / math.sqrt(A * B),
        direction[0] * math.sqrt(A),
        direction[2] * math.sqrt(A / B),
        -direction[1],
    ])
    return np.concatenate((coordinate, tangent))


def endpoint(profile: Profile, direction: np.ndarray) -> tuple[np.ndarray, float]:
    def event(_lambda, state):
        return np.linalg.norm(state[1:4]) - END_R
    event.direction = 1.0
    event.terminal = True
    result = solve_ivp(
        lambda parameter, state: rhs(profile, parameter, state),
        (0.0, AFFINE_CAP),
        initial(profile, direction),
        method="DOP853",
        rtol=2.0e-10,
        atol=2.0e-12,
        events=event,
        max_step=0.04,
    )
    assert result.success and len(result.y_events[0]) == 1
    state = result.y_events[0][0]
    vector = state[1:4] / np.linalg.norm(state[1:4])
    tangent = state[4:]
    null = abs(float(tangent @ metric(profile, state[:4]) @ tangent))
    return vector, null


def main() -> None:
    profile_map = profiles()
    reference = np.load(G76 / "SKY_ENDPOINTS.npz", allow_pickle=False)
    directions = reference["level4_directions"]
    direct = np.load(HERE / "DIRECT_ENDPOINTS.npy", mmap_mode="r")
    profile_ids = [row["profile_id"] for row in read_tsv(G75 / "PROFILE_ATLAS.tsv")]
    indices = {value: index for index, value in enumerate(profile_ids)}
    rows = []
    for profile_id in PANEL:
        profile = profile_map[profile_id]
        chords, nulls = [], []
        for ray_index in RAY_INDICES:
            value, null = endpoint(profile, directions[ray_index])
            chords.append(float(np.linalg.norm(value - direct[indices[profile_id], ray_index])))
            nulls.append(null)
        row = {
            "profile_id": profile_id,
            "stratum": profile.stratum,
            "ray_count": len(RAY_INDICES),
            "maximum_endpoint_chord": max(chords),
            "maximum_null_backward_error": max(nulls),
            "status": "PASS" if max(chords) <= CHORD_TOL and max(nulls) <= NULL_TOL else "FAIL",
        }
        rows.append(row)
        print(profile_id, row["status"], f"chord={max(chords):.3e}", f"null={max(nulls):.3e}")
    unresolved = {"G75_A0_S03_E100", "G75_AM_S03_E100", "G75_AM_S24_E100", "G75_AP_S03_E100"}
    checks = {
        "all_panel_rows_pass": all(row["status"] == "PASS" for row in rows),
        "all_eight_strata_present": len({row["stratum"] for row in rows[:8]}) == 8,
        "all_four_G76_unresolved_present": unresolved <= {row["profile_id"] for row in rows},
        "finite_difference_metric_derivative": True,
        "scipy_DOP853_not_RK4": True,
    }
    result = {
        "schema": "udt-cmb-g77-independent-scipy-fd-panel-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "method": "SciPy_DOP853_full_Christoffel_central_finite_difference_metric",
        "finite_difference_step": FD_STEP,
        "panel_count": len(rows),
        "rays_per_profile": len(RAY_INDICES),
        "maximum_endpoint_chord": max(row["maximum_endpoint_chord"] for row in rows),
        "maximum_null_backward_error": max(row["maximum_null_backward_error"] for row in rows),
        "panel": rows,
    }
    (HERE / "INDEPENDENT_PANEL_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
