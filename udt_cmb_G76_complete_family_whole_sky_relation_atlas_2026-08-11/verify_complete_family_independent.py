#!/usr/bin/env python3
"""Independent G76 replay using the metric geodesic equation, not production H."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROFILE_PATH = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv"
SHAPE_PATH = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/SHAPE_ATLAS.tsv"
ATLAS_PATH = HERE / "WHOLE_SKY_RELATION_ATLAS.tsv"
ENDPOINT_PATH = HERE / "SKY_ENDPOINTS.npz"
START_R = 0.25
END_R = 1.0
AFFINE_CAP = 4.0
STEPS = 2048
REPLAY_TOL = 1.0e-5
REGISTERED_UNRESOLVED_REPLAY_TOL = 5.0e-5
NULL_TOL = 2.0e-7


@dataclass(frozen=True)
class Profile:
    profile_id: str
    lapse_a: float
    coefficients: tuple[float, float, float]
    stratum: str

    def q(self, s: np.ndarray) -> np.ndarray:
        c0, c1, c2 = self.coefficients
        return c0 + c1 * s + c2 * s * s

    def qs(self, s: np.ndarray) -> np.ndarray:
        _, c1, c2 = self.coefficients
        return c1 + 2.0 * c2 * s


PANEL = (
    "G75_AM_S13_E05",   # C0_E0_O0_T0; negative lapse, low amplitude
    "G75_AP_S09_E100",  # C0_E0_O1_T0; positive lapse, high amplitude
    "G75_AM_S16_E100",  # C0_E1_O0_T0; negative lapse, high amplitude
    "G75_AP_S12_E05",   # C0_E2_O0_T0; positive lapse, low amplitude
    "G75_AP_S04_E05",   # C1_E0_O0_T0; positive lapse, low amplitude
    "G75_AM_S02_E100",  # C1_E0_O1_T0; negative lapse, high amplitude
    "G75_AP_S03_E100",  # C1_E1_O0_T0; positive lapse, high amplitude; unresolved control
    "G75_AM_S01_E05",   # C2_E0_O0_T0; negative lapse, low amplitude
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def rational(text: str) -> float:
    return float(Fraction(text))


def load_profiles() -> dict[str, Profile]:
    shapes = {row["shape_id"]: row for row in read_tsv(SHAPE_PATH)}
    output: dict[str, Profile] = {}
    for row in read_tsv(PROFILE_PATH):
        if row["shape_id"] == "ZERO":
            coefficients = (0.0, 0.0, 0.0)
            stratum = "ZERO"
        else:
            shape = shapes[row["shape_id"]]
            amplitude = rational(row["amplitude"])
            coefficients = tuple(amplitude * rational(shape[f"normalized_c{i}"]) for i in range(3))
            stratum = shape["stratum_code"]
        output[row["profile_id"]] = Profile(
            row["profile_id"], rational(row["lapse_a"]), coefficients, stratum
        )
    return output


def metric_and_derivative(profile: Profile, position: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return g[m,n] and partial[k,m,n]; k=0 is the stationary t derivative."""
    count = len(position)
    s = np.einsum("ni,ni->n", position, position)
    a = profile.lapse_a
    A = 1.0 + a * s
    q = profile.q(s)
    qs = profile.qs(s)
    X, Y = position[:, 0], position[:, 1]
    radial_rotation = np.column_stack((-Y, X, np.zeros(count)))
    w = q[:, None] * radial_rotation

    g = np.zeros((count, 4, 4), dtype=float)
    g[:, 0, 0] = -A
    g[:, 0, 1:4] = w
    g[:, 1:4, 0] = w
    eye3 = np.eye(3)[None, :, :]
    outer = np.einsum("ni,nj->nij", position, position)
    g[:, 1:4, 1:4] = eye3 - (a / A)[:, None, None] * outer

    partial = np.zeros((count, 4, 4, 4), dtype=float)
    # Spatial derivative coordinate k+1.
    rotation_derivative = np.array(
        [[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 0.0]], dtype=float
    )  # rows k=(X,Y,Z), columns vector component i
    for k in range(3):
        pg = partial[:, k + 1]
        pg[:, 0, 0] = -2.0 * a * position[:, k]
        dw = (
            (2.0 * qs * position[:, k])[:, None] * radial_rotation
            + q[:, None] * rotation_derivative[k][None, :]
        )
        pg[:, 0, 1:4] = dw
        pg[:, 1:4, 0] = dw
        unit = np.zeros(3)
        unit[k] = 1.0
        product_derivative = (
            np.einsum("i,nj->nij", unit, position)
            + np.einsum("ni,j->nij", position, unit)
        )
        pg[:, 1:4, 1:4] = (
            -(a / A)[:, None, None] * product_derivative
            + (2.0 * a * a * position[:, k] / (A * A))[:, None, None] * outer
        )
    return g, partial


def christoffel_rhs(profile: Profile, state: np.ndarray) -> np.ndarray:
    coordinates = state[:, :4]
    tangent = state[:, 4:8]
    g, partial = metric_and_derivative(profile, coordinates[:, 1:4])
    inverse = np.linalg.inv(g)
    # Gamma^m_ab = 1/2 g^mn (d_a g_nb + d_b g_na - d_n g_ab).
    gamma = 0.5 * np.einsum(
        "nmk,nabk->nmab",
        inverse,
        partial + np.swapaxes(partial, 1, 2) - np.transpose(partial, (0, 2, 3, 1)),
        optimize=True,
    )
    acceleration = -np.einsum("nmab,na,nb->nm", gamma, tangent, tangent, optimize=True)
    return np.column_stack((tangent, acceleration))


def initial_state(profile: Profile, directions: np.ndarray) -> np.ndarray:
    count = len(directions)
    position = np.zeros((count, 3), dtype=float)
    position[:, 0] = START_R
    s0 = START_R**2
    q0 = float(profile.q(np.array([s0]))[0])
    A = 1.0 + profile.lapse_a * s0
    B = A + q0 * q0 * s0
    tangent = np.empty((count, 4), dtype=float)
    tangent[:, 0] = 1.0 / math.sqrt(A) + directions[:, 2] * q0 * START_R / math.sqrt(A * B)
    tangent[:, 1] = directions[:, 0] * math.sqrt(A)
    tangent[:, 2] = directions[:, 2] * math.sqrt(A / B)
    tangent[:, 3] = -directions[:, 1]
    coordinates = np.column_stack((np.zeros(count), position))
    return np.column_stack((coordinates, tangent))


def rk4(profile: Profile, state: np.ndarray, step: float) -> np.ndarray:
    k1 = christoffel_rhs(profile, state)
    k2 = christoffel_rhs(profile, state + 0.5 * step * k1)
    k3 = christoffel_rhs(profile, state + 0.5 * step * k2)
    k4 = christoffel_rhs(profile, state + step * k3)
    return state + step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0


def null_error(profile: Profile, state: np.ndarray) -> float:
    g, _ = metric_and_derivative(profile, state[:, 1:4])
    tangent = state[:, 4:8]
    value = np.einsum("na,nab,nb->n", tangent, g, tangent)
    return float(np.max(np.abs(value)))


def integrate(profile: Profile, directions: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    state = initial_state(profile, directions)
    active = np.ones(len(state), dtype=bool)
    crossed = np.zeros(len(state), dtype=bool)
    endpoint = np.full((len(state), 3), np.nan)
    step = AFFINE_CAP / STEPS
    maximum_null = null_error(profile, state)
    for _ in range(STEPS):
        if not np.any(active):
            break
        index = np.flatnonzero(active)
        old = state[index]
        new = rk4(profile, old, step)
        old_r = np.linalg.norm(old[:, 1:4], axis=1)
        new_r = np.linalg.norm(new[:, 1:4], axis=1)
        hit = (old_r < END_R) & (new_r >= END_R)
        if np.any(hit):
            lo, hi = old_r[hit], new_r[hit]
            weight = np.clip((END_R - lo) / np.maximum(hi - lo, 1.0e-15), 0.0, 1.0)
            point = old[hit] + weight[:, None] * (new[hit] - old[hit])
            vector = point[:, 1:4]
            vector /= np.linalg.norm(vector, axis=1)[:, None]
            hit_index = index[hit]
            endpoint[hit_index] = vector
            crossed[hit_index] = True
            active[hit_index] = False
        state[index] = new
        if np.all(np.isfinite(new)):
            maximum_null = max(maximum_null, null_error(profile, new))
    return endpoint, crossed, maximum_null


def main() -> None:
    profiles = load_profiles()
    production_rows = {row["profile_id"]: row for row in read_tsv(ATLAS_PATH)}
    production = np.load(ENDPOINT_PATH, allow_pickle=False)
    directions = production["level4_directions"]
    # A deterministic 162-ray subset spans the stored complete sphere without sharing solver code.
    indices = np.linspace(0, len(directions) - 1, 162, dtype=int)
    selected_directions = directions[indices]
    panel_rows = []
    for profile_id in PANEL:
        profile = profiles[profile_id]
        endpoint, crossed, maximum_null = integrate(profile, selected_directions)
        reference = production[profile_id + "__endpoint"][indices]
        reference_crossed = production[profile_id + "__crossed"][indices]
        mismatch = int(np.count_nonzero(crossed != reference_crossed))
        common = crossed & reference_crossed
        chord = float(np.max(np.linalg.norm(endpoint[common] - reference[common], axis=1)))
        production_class = production_rows[profile_id]["sample_class"]
        if production_class == "NUMERICALLY_UNRESOLVED":
            verified = mismatch == 0 and chord <= REGISTERED_UNRESOLVED_REPLAY_TOL and maximum_null <= NULL_TOL
            row_status = "REPRODUCES_PRODUCTION_UNRESOLVED" if verified else "FAIL"
        else:
            verified = mismatch == 0 and chord <= REPLAY_TOL and maximum_null <= NULL_TOL
            row_status = "PASS" if verified else "FAIL"
        panel_rows.append(
            {
                "profile_id": profile_id,
                "stratum": profile.stratum,
                "lapse_a": profile.lapse_a,
                "amplitude": production_rows[profile_id]["amplitude"],
                "production_class": production_class,
                "ray_count": len(indices),
                "crossing_mask_mismatch": mismatch,
                "maximum_endpoint_chord": chord,
                "maximum_null_backward_error": maximum_null,
                "status": row_status,
            }
        )
        print(profile_id, panel_rows[-1]["status"], f"chord={chord:.3e}", f"null={maximum_null:.3e}")

    strata = {row["stratum"] for row in panel_rows}
    expected_strata = {profiles[row].stratum for row in PANEL}
    lapse_values = {float(row["lapse_a"]) for row in panel_rows}
    amplitude_values = {float(row["amplitude"]) for row in panel_rows}
    checks = {
        "all_panel_rows_verified": all(row["status"] != "FAIL" for row in panel_rows),
        "all_eight_strata_present": len(strata) == len(expected_strata) == 8,
        "both_lapse_extremes_present": lapse_values == {-0.25, 0.25},
        "both_amplitude_extremes_present": 0.05 in amplitude_values and 1.0 in amplitude_values,
        "unresolved_production_control_replayed": production_rows["G75_AP_S03_E100"]["sample_class"] == "NUMERICALLY_UNRESOLVED",
    }
    result = {
        "schema": "udt-cmb-g76-independent-christoffel-replay-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "method": "direct_metric_christoffel_geodesic_rk4",
        "production_rhs_imported": False,
        "steps": STEPS,
        "ray_count_per_profile": len(indices),
        "panel_count": len(panel_rows),
        "checks": checks,
        "maximum_endpoint_chord": max(row["maximum_endpoint_chord"] for row in panel_rows),
        "maximum_null_backward_error": max(row["maximum_null_backward_error"] for row in panel_rows),
        "panel": panel_rows,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
