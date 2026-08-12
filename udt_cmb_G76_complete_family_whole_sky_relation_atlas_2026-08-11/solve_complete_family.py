#!/usr/bin/env python3
"""Map the complete frozen G75 whole-sky endpoint relation family."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import time
from collections import Counter
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.spatial import ConvexHull


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROFILE_PATH = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv"
SHAPE_PATH = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/SHAPE_ATLAS.tsv"
G74_ENDPOINTS = ROOT / "udt_cmb_G74_symbolic_sky_relation_topology_atlas_2026-08-11/SKY_ENDPOINTS.npz"
START_R = 0.25  # PINNED_BY_HISTORICAL_CONTROL: exact G74 observer query.
END_R = 1.0  # PINNED_BY_HISTORICAL_CONTROL: comparison sphere, not last scattering or X_max.
AFFINE_CAP = 4.0  # CHOSE_NUMERIC: bounded path integration, not physics.
LEVELS = (2, 3, 4)  # CHOSE_NUMERIC: mesh convergence controls.
FINE_STEPS = 1024  # CHOSE_NUMERIC: preregistered RK4 resolution.
COARSE_STEPS = 512  # CHOSE_NUMERIC: preregistered time refinement.
TIME_TOL = 5.0e-5  # CHOSE_NUMERIC: preregistered certification threshold.
DEGREE_TOL = 5.0e-4  # CHOSE_NUMERIC: preregistered certification threshold.
H_TOL = 1.0e-6  # CHOSE_NUMERIC: preregistered backward-error threshold.
G74_TOL = 5.0e-6  # CHOSE_NUMERIC: preregistered regression threshold.
REFLECTION_TOL = 2.0e-5  # CHOSE_NUMERIC: preregistered reflection threshold.
NEAR_THRESHOLDS = (1.0e-2, 1.0e-3, 1.0e-4)  # CHOSE_NUMERIC: diagnostics, never filters.


@dataclass(frozen=True)
class Profile:
    profile_id: str
    lapse_a: float
    shape_id: str
    amplitude: float
    q_coeffs: tuple[float, float, float]
    behavior_class: str
    stratum_code: str

    def q(self, s: np.ndarray | float) -> np.ndarray | float:
        return self.q_coeffs[0] + self.q_coeffs[1] * s + self.q_coeffs[2] * s * s

    def qs(self, s: np.ndarray | float) -> np.ndarray | float:
        return self.q_coeffs[1] + 2.0 * self.q_coeffs[2] * s


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def number(text: str) -> float:
    return float(Fraction(text))


def verify_sources() -> int:
    rows = table(HERE / "SOURCE_MANIFEST.tsv")
    for row in rows:
        target = ROOT / row["path"]
        assert target.is_file() and digest(target) == row["sha256"], row["path"]
    return len(rows)


def load_profiles() -> list[Profile]:
    shapes = {row["shape_id"]: row for row in table(SHAPE_PATH)}
    profiles: list[Profile] = []
    for row in table(PROFILE_PATH):
        if row["shape_id"] == "ZERO":
            coeffs = (0.0, 0.0, 0.0)
            behavior, stratum = "ZERO_MIXING_CONTROL", "ZERO"
        else:
            shape = shapes[row["shape_id"]]
            amplitude = number(row["amplitude"])
            coeffs = tuple(amplitude * number(shape[f"normalized_c{i}"]) for i in range(3))
            behavior, stratum = shape["behavior_class"], shape["stratum_code"]
        profiles.append(
            Profile(
                row["profile_id"], number(row["lapse_a"]), row["shape_id"],
                number(row["amplitude"]), coeffs, behavior, stratum,
            )
        )
    assert len(profiles) == len({item.profile_id for item in profiles}) == 591
    assert len({item.shape_id for item in profiles if item.shape_id != "ZERO"}) == 49
    return profiles


def initial_icosahedron() -> tuple[np.ndarray, np.ndarray]:
    golden = (1.0 + math.sqrt(5.0)) / 2.0
    vertices = []
    for a, b in ((-1.0, golden), (1.0, golden), (-1.0, -golden), (1.0, -golden)):
        vertices.extend(((0.0, a, b), (a, b, 0.0), (b, 0.0, a)))
    vertices = np.asarray(vertices, dtype=float)
    vertices /= np.linalg.norm(vertices, axis=1)[:, None]
    faces = orient_faces(vertices, np.asarray(ConvexHull(vertices).simplices, dtype=np.int64))
    return vertices, faces


def orient_faces(vertices: np.ndarray, faces: np.ndarray) -> np.ndarray:
    output = faces.copy()
    for index, (i, j, k) in enumerate(output):
        normal = np.cross(vertices[j] - vertices[i], vertices[k] - vertices[i])
        if float(np.dot(normal, vertices[i] + vertices[j] + vertices[k])) < 0.0:
            output[index, 1], output[index, 2] = output[index, 2], output[index, 1]
    return output


def icosphere(level: int) -> tuple[np.ndarray, np.ndarray]:
    vertices, faces = initial_icosahedron()
    for _ in range(level):
        values = vertices.tolist()
        edge_midpoint: dict[tuple[int, int], int] = {}

        def midpoint(i: int, j: int) -> int:
            key = (min(i, j), max(i, j))
            if key not in edge_midpoint:
                point = vertices[i] + vertices[j]
                point /= np.linalg.norm(point)
                edge_midpoint[key] = len(values)
                values.append(point.tolist())
            return edge_midpoint[key]

        new_faces = []
        for i, j, k in faces:
            ij, jk, ki = midpoint(int(i), int(j)), midpoint(int(j), int(k)), midpoint(int(k), int(i))
            new_faces.extend(((i, ij, ki), (j, jk, ij), (k, ki, jk), (ij, jk, ki)))
        vertices = np.asarray(values, dtype=float)
        faces = orient_faces(vertices, np.asarray(new_faces, dtype=np.int64))
    assert len(vertices) == 10 * 4**level + 2 and len(faces) == 20 * 4**level
    return vertices, faces


def initial_state(profile: Profile, directions: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    count = len(directions)
    position = np.zeros((count, 3), dtype=float)
    position[:, 0] = START_R
    s0 = START_R**2
    q0 = float(profile.q(s0))
    A = 1.0 + profile.lapse_a * s0
    B = A + q0**2 * s0
    u_t = 1.0 / math.sqrt(A)
    epsi_t = q0 * START_R / math.sqrt(A * B)
    epsi_y = math.sqrt(A / B)
    k_t = u_t + directions[:, 2] * epsi_t
    velocity = np.empty((count, 3), dtype=float)
    velocity[:, 0] = directions[:, 0] * math.sqrt(A)
    velocity[:, 1] = directions[:, 2] * epsi_y
    velocity[:, 2] = -directions[:, 1]
    w = np.zeros_like(position)
    w[:, 1] = q0 * START_R
    spatial_metric_v = velocity.copy()
    spatial_metric_v[:, 0] /= A
    p_t = -A * k_t + np.einsum("ij,ij->i", w, velocity)
    momentum = w * k_t[:, None] + spatial_metric_v
    coordinates = np.column_stack((np.zeros(count), position))
    return np.column_stack((coordinates, momentum)), p_t


def hamiltonian_rhs(state: np.ndarray, p_t: np.ndarray, profile: Profile) -> np.ndarray:
    X, p = state[:, 1:4], state[:, 4:7]
    s = np.einsum("ij,ij->i", X, X)
    rho2 = X[:, 0] ** 2 + X[:, 1] ** 2
    q, qs = np.asarray(profile.q(s)), np.asarray(profile.qs(s))
    A = 1.0 + profile.lapse_a * s
    B = A + q**2 * rho2
    w = np.column_stack((-q * X[:, 1], q * X[:, 0], np.zeros(len(X))))
    Lz = X[:, 0] * p[:, 1] - X[:, 1] * p[:, 0]
    E = p_t - q * Lz
    radial = np.einsum("ij,ij->i", X, p)
    dq = 2.0 * qs[:, None] * X
    dL = np.column_stack((p[:, 1], -p[:, 0], np.zeros(len(X))))
    dB = (
        2.0 * profile.lapse_a * X
        + (2.0 * q * rho2)[:, None] * dq
        + (2.0 * q**2)[:, None] * np.column_stack((X[:, 0], X[:, 1], np.zeros(len(X))))
    )
    dt = -E / B
    dX = p + profile.lapse_a * radial[:, None] * X + (E / B)[:, None] * w
    dp = (
        -profile.lapse_a * radial[:, None] * p
        - (E / B)[:, None] * (Lz[:, None] * dq + q[:, None] * dL)
        - (0.5 * E**2 / B**2)[:, None] * dB
    )
    return np.column_stack((dt, dX, dp))


def hamiltonian_value(state: np.ndarray, p_t: np.ndarray, profile: Profile) -> np.ndarray:
    X, p = state[:, 1:4], state[:, 4:7]
    s = np.einsum("ij,ij->i", X, X)
    rho2 = X[:, 0] ** 2 + X[:, 1] ** 2
    q = np.asarray(profile.q(s))
    B = 1.0 + profile.lapse_a * s + q**2 * rho2
    Lz = X[:, 0] * p[:, 1] - X[:, 1] * p[:, 0]
    radial = np.einsum("ij,ij->i", X, p)
    return 0.5 * (
        np.einsum("ij,ij->i", p, p)
        + profile.lapse_a * radial**2
        - (p_t - q * Lz) ** 2 / B
    )


def rk4_step(state: np.ndarray, p_t: np.ndarray, profile: Profile, step: float) -> np.ndarray:
    k1 = hamiltonian_rhs(state, p_t, profile)
    k2 = hamiltonian_rhs(state + 0.5 * step * k1, p_t, profile)
    k3 = hamiltonian_rhs(state + 0.5 * step * k2, p_t, profile)
    k4 = hamiltonian_rhs(state + step * k3, p_t, profile)
    return state + (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate_sky(profile: Profile, directions: np.ndarray, steps: int) -> dict[str, np.ndarray | float | int]:
    state, p_t = initial_state(profile, directions)
    initial_h = hamiltonian_value(state, p_t, profile)
    active = np.ones(len(state), dtype=bool)
    crossed = np.zeros(len(state), dtype=bool)
    nonfinite_count = 0
    endpoint = np.full((len(state), 3), np.nan)
    endpoint_t = np.full(len(state), np.nan)
    endpoint_affine = np.full(len(state), np.nan)
    turns = np.zeros(len(state), dtype=np.int32)
    first_rhs = hamiltonian_rhs(state, p_t, profile)
    previous_dr = np.einsum("ij,ij->i", state[:, 1:4], first_rhs[:, 1:4]) / START_R
    step = AFFINE_CAP / steps
    max_h = float(np.max(np.abs(initial_h)))

    for step_index in range(steps):
        if not np.any(active):
            break
        index = np.flatnonzero(active)
        old = state[index]
        new = rk4_step(old, p_t[index], profile, step)
        old_r = np.linalg.norm(old[:, 1:4], axis=1)
        new_r = np.linalg.norm(new[:, 1:4], axis=1)
        dr = (new_r - old_r) / step
        prior = previous_dr[index]
        changed = (np.abs(prior) > 1.0e-9) & (np.abs(dr) > 1.0e-9) & (prior * dr < 0.0)
        turns[index[changed]] += 1
        previous_dr[index] = dr
        hit = (old_r < END_R) & (new_r >= END_R)
        if np.any(hit):
            old_hit, new_hit = old[hit], new[hit]
            lo, hi = old_r[hit], new_r[hit]
            weight = np.clip((END_R - lo) / np.maximum(hi - lo, 1.0e-15), 0.0, 1.0)
            interpolated = old_hit + weight[:, None] * (new_hit - old_hit)
            hit_index = index[hit]
            vectors = interpolated[:, 1:4]
            vectors /= np.linalg.norm(vectors, axis=1)[:, None]
            endpoint[hit_index] = vectors
            endpoint_t[hit_index] = interpolated[:, 0]
            endpoint_affine[hit_index] = (step_index + weight) * step
            crossed[hit_index] = True
            active[hit_index] = False
        state[index] = new
        finite = np.all(np.isfinite(new), axis=1)
        if np.any(finite):
            max_h = max(max_h, float(np.max(np.abs(hamiltonian_value(new[finite], p_t[index][finite], profile)))))
        if np.any(~finite):
            failed = index[~finite]
            active[failed] = False
            nonfinite_count += len(failed)
    return {
        "endpoint": endpoint,
        "endpoint_t": endpoint_t,
        "endpoint_affine": endpoint_affine,
        "crossed": crossed,
        "turns": turns,
        "active_remaining": int(np.count_nonzero(active)),
        "nonfinite_count": nonfinite_count,
        "max_abs_hamiltonian": max_h,
        "initial_max_abs_hamiltonian": float(np.max(np.abs(initial_h))),
    }


def solid_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    numerator = np.einsum("ij,ij->i", a, np.cross(b, c))
    denominator = 1.0 + np.einsum("ij,ij->i", a, b) + np.einsum("ij,ij->i", b, c) + np.einsum("ij,ij->i", c, a)
    return 2.0 * np.arctan2(numerator, denominator)


def tangent_basis(center: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    reference = np.zeros_like(center)
    reference[:, 2] = 1.0
    polar = np.abs(center[:, 2]) > 0.85
    reference[polar] = np.array([0.0, 1.0, 0.0])
    e1 = np.cross(reference, center)
    e1 /= np.linalg.norm(e1, axis=1)[:, None]
    e2 = np.cross(center, e1)
    return e1, e2


def log_coordinates(points: np.ndarray, center: np.ndarray, e1: np.ndarray, e2: np.ndarray) -> np.ndarray:
    dot = np.clip(np.einsum("fi,fji->fj", center, points), -1.0, 1.0)
    angle = np.arccos(dot)
    tangent = points - dot[:, :, None] * center[:, None, :]
    sine = np.sin(angle)
    factor = np.ones_like(angle)
    mask = np.abs(sine) > 1.0e-14
    factor[mask] = angle[mask] / sine[mask]
    tangent *= factor[:, :, None]
    return np.stack((np.einsum("fji,fi->fj", tangent, e1), np.einsum("fji,fi->fj", tangent, e2)), axis=2)


def face_singular_values(vertices: np.ndarray, faces: np.ndarray, endpoint: np.ndarray, valid_faces: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    count = len(faces)
    smax = np.full(count, np.nan)
    smin = np.full(count, np.nan)
    determinant = np.full(count, np.nan)
    selected = np.flatnonzero(valid_faces)
    if not len(selected):
        return smax, smin, determinant
    tri_in = vertices[faces[selected]]
    tri_out = endpoint[faces[selected]]
    center_in = np.sum(tri_in, axis=1)
    center_out = np.sum(tri_out, axis=1)
    norm_in = np.linalg.norm(center_in, axis=1)
    norm_out = np.linalg.norm(center_out, axis=1)
    usable = (norm_in > 1.0e-12) & (norm_out > 1.0e-12)
    if not np.any(usable):
        return smax, smin, determinant
    kept = selected[usable]
    tri_in, tri_out = tri_in[usable], tri_out[usable]
    center_in = center_in[usable] / norm_in[usable, None]
    center_out = center_out[usable] / norm_out[usable, None]
    ein1, ein2 = tangent_basis(center_in)
    eout1, eout2 = tangent_basis(center_out)
    cin = log_coordinates(tri_in, center_in, ein1, ein2)
    cout = log_coordinates(tri_out, center_out, eout1, eout2)
    xin = np.stack((cin[:, 1] - cin[:, 0], cin[:, 2] - cin[:, 0]), axis=2)
    xout = np.stack((cout[:, 1] - cout[:, 0], cout[:, 2] - cout[:, 0]), axis=2)
    det_in = np.linalg.det(xin)
    nonsingular = np.abs(det_in) > 1.0e-14
    if not np.any(nonsingular):
        return smax, smin, determinant
    kept = kept[nonsingular]
    maps = xout[nonsingular] @ np.linalg.inv(xin[nonsingular])
    values = np.linalg.svd(maps, compute_uv=False)
    smax[kept], smin[kept], determinant[kept] = values[:, 0], values[:, 1], np.linalg.det(maps)
    return smax, smin, determinant


def mesh_diagnostics(vertices: np.ndarray, faces: np.ndarray, result: dict) -> dict[str, float | int | str]:
    crossed = np.asarray(result["crossed"])
    endpoint = np.asarray(result["endpoint"])
    valid_faces = np.all(crossed[faces], axis=1)
    input_area = solid_angle(vertices[faces[:, 0]], vertices[faces[:, 1]], vertices[faces[:, 2]])
    output_area = np.full(len(faces), np.nan)
    selected_faces = faces[valid_faces]
    output_area[valid_faces] = solid_angle(endpoint[selected_faces[:, 0]], endpoint[selected_faces[:, 1]], endpoint[selected_faces[:, 2]])
    ratios = output_area[valid_faces] / input_area[valid_faces]
    smax, smin, det_map = face_singular_values(vertices, faces, endpoint, valid_faces)
    finite_sv = np.isfinite(smax) & np.isfinite(smin)
    shear = np.full(len(faces), np.nan)
    shear[finite_sv] = smax[finite_sv] / np.maximum(smin[finite_sv], 1.0e-300)
    return {
        "vertices": len(vertices),
        "faces": len(faces),
        "crossed_vertices": int(np.count_nonzero(crossed)),
        "missing_vertices": int(np.count_nonzero(~crossed)),
        "active_remaining": int(result["active_remaining"]),
        "nonfinite_count": int(result["nonfinite_count"]),
        "directions_with_turns": int(np.count_nonzero(np.asarray(result["turns"]) > 0)),
        "maximum_turn_count": int(np.max(result["turns"])),
        "valid_faces": int(np.count_nonzero(valid_faces)),
        "degree_signed_area_estimate": float(np.nansum(output_area) / (4.0 * math.pi)),
        "min_signed_area_ratio": float(np.min(ratios)) if len(ratios) else math.nan,
        "max_signed_area_ratio": float(np.max(ratios)) if len(ratios) else math.nan,
        "negative_faces": int(np.count_nonzero(ratios < 0.0)),
        "near_area_1e2": int(np.count_nonzero(np.abs(ratios) < NEAR_THRESHOLDS[0])),
        "near_area_1e3": int(np.count_nonzero(np.abs(ratios) < NEAR_THRESHOLDS[1])),
        "near_area_1e4": int(np.count_nonzero(np.abs(ratios) < NEAR_THRESHOLDS[2])),
        "face_maps_resolved": int(np.count_nonzero(finite_sv)),
        "min_face_smin": float(np.nanmin(smin)) if np.any(finite_sv) else math.nan,
        "max_face_smax": float(np.nanmax(smax)) if np.any(finite_sv) else math.nan,
        "median_face_shear_ratio": float(np.nanmedian(shear)) if np.any(finite_sv) else math.nan,
        "p95_face_shear_ratio": float(np.nanquantile(shear, 0.95)) if np.any(finite_sv) else math.nan,
        "max_face_shear_ratio": float(np.nanmax(shear)) if np.any(finite_sv) else math.nan,
        "negative_intrinsic_face_maps": int(np.count_nonzero(det_map[finite_sv] < 0.0)),
        "max_abs_hamiltonian": float(result["max_abs_hamiltonian"]),
        "initial_max_abs_hamiltonian": float(result["initial_max_abs_hamiltonian"]),
    }


def endpoint_chord(left: np.ndarray, right: np.ndarray, left_mask: np.ndarray, right_mask: np.ndarray) -> tuple[float, int]:
    mismatch = int(np.count_nonzero(left_mask != right_mask))
    common = left_mask & right_mask
    error = float(np.max(np.linalg.norm(left[common] - right[common], axis=1))) if np.any(common) else math.inf
    return error, mismatch


def reflection_audit(profile: Profile, directions: np.ndarray, positive: dict) -> tuple[float, int]:
    reflected_directions = directions.copy()
    reflected_directions[:, 2] *= -1.0
    negative = integrate_sky(replace(profile, q_coeffs=tuple(-value for value in profile.q_coeffs)), reflected_directions, FINE_STEPS)
    reflected_endpoint = np.asarray(positive["endpoint"]).copy()
    reflected_endpoint[:, 1] *= -1.0
    return endpoint_chord(reflected_endpoint, np.asarray(negative["endpoint"]), np.asarray(positive["crossed"]), np.asarray(negative["crossed"]))


def old_profile_name(profile: Profile) -> str | None:
    lapse = {-0.25: "AM", 0.0: "A0", 0.25: "AP"}.get(profile.lapse_a)
    if lapse is None:
        return None
    if profile.shape_id == "ZERO":
        return f"G68_F01_{lapse}"
    if profile.shape_id == "S21" and profile.amplitude in {0.05, 0.2}:
        strength = "P05" if profile.amplitude == 0.05 else "P20"
        return f"G68_F02_{lapse}_{strength}"
    return None


def classify(summary: dict) -> str:
    resolved = (
        summary["time_refinement_endpoint_max_chord"] <= TIME_TOL
        and summary["time_refinement_mask_mismatch"] == 0
        and summary["mesh_degree_drift_level3_to4"] <= DEGREE_TOL
        and summary["max_abs_hamiltonian"] <= H_TOL
        and summary["reflection_mask_mismatch"] == 0
        and summary["reflection_max_chord"] <= REFLECTION_TOL
    )
    if not resolved:
        return "NUMERICALLY_UNRESOLVED"
    if summary["finest_missing_vertices"] or summary["finest_nonfinite_count"]:
        return "SAMPLED_MISSING_OR_MULTIBRANCH_CANDIDATE"
    if summary["finest_negative_faces"] or summary["finest_negative_intrinsic_face_maps"]:
        return "SAMPLED_ORIENTATION_REVERSING_OR_FOLD_CANDIDATE"
    return "SAMPLED_COMPLETE_ORIENTATION_PRESERVING"


def write_tsv(path: Path, rows: list[dict]) -> None:
    assert rows
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def checkpoint_path(profile: Profile) -> Path:
    return HERE / "_checkpoints" / f"{profile.profile_id}.npz"


def save_checkpoint(profile: Profile, summary: dict, trials: list[dict], fine: dict) -> None:
    path = checkpoint_path(profile)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        summary=np.asarray(json.dumps(summary, sort_keys=True)),
        trials=np.asarray(json.dumps(trials, sort_keys=True)),
        endpoint=fine["endpoint"], endpoint_t=fine["endpoint_t"],
        endpoint_affine=fine["endpoint_affine"], crossed=fine["crossed"], turns=fine["turns"],
    )


def load_checkpoint(profile: Profile) -> tuple[dict, list[dict], dict] | None:
    path = checkpoint_path(profile)
    if not path.is_file():
        return None
    data = np.load(path, allow_pickle=False)
    summary = json.loads(str(data["summary"]))
    trials = json.loads(str(data["trials"]))
    fine = {name: data[name] for name in ("endpoint", "endpoint_t", "endpoint_affine", "crossed", "turns")}
    return summary, trials, fine


def compute_profile(profile: Profile, mesh: dict[int, tuple[np.ndarray, np.ndarray]], old: np.lib.npyio.NpzFile) -> tuple[dict, list[dict], dict]:
    trials_raw: dict[tuple[int, int], tuple[dict, dict]] = {}
    trial_rows = []
    for level in LEVELS:
        vertices, faces = mesh[level]
        steps_set = (COARSE_STEPS, FINE_STEPS) if level == 4 else (FINE_STEPS,)
        for steps in steps_set:
            result = integrate_sky(profile, vertices, steps)
            diagnostics = mesh_diagnostics(vertices, faces, result)
            diagnostics.update({"profile_id": profile.profile_id, "level": level, "steps": steps})
            trials_raw[(level, steps)] = (result, diagnostics)
            trial_rows.append(diagnostics)

    fine, fine_diag = trials_raw[(4, FINE_STEPS)]
    coarse, _ = trials_raw[(4, COARSE_STEPS)]
    time_error, time_mask = endpoint_chord(
        np.asarray(fine["endpoint"]), np.asarray(coarse["endpoint"]),
        np.asarray(fine["crossed"]), np.asarray(coarse["crossed"]),
    )
    degree_drift = abs(fine_diag["degree_signed_area_estimate"] - trials_raw[(3, FINE_STEPS)][1]["degree_signed_area_estimate"])
    if profile.shape_id == "ZERO":
        reflection_error, reflection_mask = 0.0, 0
    else:
        reflection_error, reflection_mask = reflection_audit(profile, mesh[3][0], trials_raw[(3, FINE_STEPS)][0])
    old_name = old_profile_name(profile)
    if old_name is None:
        old_error, old_mask = math.nan, -1
    else:
        old_endpoint = old[old_name + "__endpoint"]
        old_mask_array = np.all(np.isfinite(old_endpoint), axis=1)
        old_error, old_mask = endpoint_chord(np.asarray(fine["endpoint"]), old_endpoint, np.asarray(fine["crossed"]), old_mask_array)

    summary = {
        "profile_id": profile.profile_id,
        "shape_id": profile.shape_id,
        "behavior_class": profile.behavior_class,
        "stratum_code": profile.stratum_code,
        "lapse_a": profile.lapse_a,
        "amplitude": profile.amplitude,
        "q_c0": profile.q_coeffs[0], "q_c1": profile.q_coeffs[1], "q_c2": profile.q_coeffs[2],
        "finest_crossed_vertices": fine_diag["crossed_vertices"],
        "finest_missing_vertices": fine_diag["missing_vertices"],
        "finest_nonfinite_count": fine_diag["nonfinite_count"],
        "finest_directions_with_turns": fine_diag["directions_with_turns"],
        "finest_maximum_turn_count": fine_diag["maximum_turn_count"],
        "finest_degree_estimate": fine_diag["degree_signed_area_estimate"],
        "finest_min_signed_area_ratio": fine_diag["min_signed_area_ratio"],
        "finest_max_signed_area_ratio": fine_diag["max_signed_area_ratio"],
        "finest_negative_faces": fine_diag["negative_faces"],
        "finest_near_area_1e2": fine_diag["near_area_1e2"],
        "finest_near_area_1e3": fine_diag["near_area_1e3"],
        "finest_near_area_1e4": fine_diag["near_area_1e4"],
        "finest_min_face_smin": fine_diag["min_face_smin"],
        "finest_max_face_smax": fine_diag["max_face_smax"],
        "finest_median_face_shear_ratio": fine_diag["median_face_shear_ratio"],
        "finest_p95_face_shear_ratio": fine_diag["p95_face_shear_ratio"],
        "finest_max_face_shear_ratio": fine_diag["max_face_shear_ratio"],
        "finest_negative_intrinsic_face_maps": fine_diag["negative_intrinsic_face_maps"],
        "time_refinement_endpoint_max_chord": time_error,
        "time_refinement_mask_mismatch": time_mask,
        "mesh_degree_drift_level3_to4": degree_drift,
        "max_abs_hamiltonian": max(row["max_abs_hamiltonian"] for row in trial_rows),
        "reflection_max_chord": reflection_error,
        "reflection_mask_mismatch": reflection_mask,
        "G74_regression_profile": old_name or "-",
        "G74_regression_max_chord": old_error,
        "G74_regression_mask_mismatch": old_mask,
        "physical_status": "CHOSE_CONTROL_NOT_SELECTED",
    }
    summary["sample_class"] = classify(summary)
    return summary, trial_rows, fine


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Operational smoke limit; never a scientific census.")
    parser.add_argument("--force", action="store_true", help="Recompute even when a checkpoint exists.")
    args = parser.parse_args()
    assert (HERE / "EQUATION_VERIFICATION.json").is_file(), "run derive_equations.py first"
    equation = json.loads((HERE / "EQUATION_VERIFICATION.json").read_text(encoding="utf-8"))
    assert equation["status"] == "PASS" and equation["passed"] == equation["total"] == 6
    source_rows = verify_sources()
    profiles = load_profiles()
    selected = profiles if args.limit is None else profiles[: args.limit]
    mesh = {level: icosphere(level) for level in LEVELS}
    old = np.load(G74_ENDPOINTS)
    started = time.time()
    summaries, all_trials, endpoints = [], [], {}
    for index, profile in enumerate(selected, 1):
        cached = None if args.force else load_checkpoint(profile)
        if cached is None:
            summary, trials, fine = compute_profile(profile, mesh, old)
            save_checkpoint(profile, summary, trials, fine)
        else:
            summary, trials, fine = cached
        summaries.append(summary)
        all_trials.extend(trials)
        endpoints[profile.profile_id + "__endpoint"] = fine["endpoint"]
        endpoints[profile.profile_id + "__endpoint_t"] = fine["endpoint_t"]
        endpoints[profile.profile_id + "__endpoint_affine"] = fine["endpoint_affine"]
        endpoints[profile.profile_id + "__crossed"] = fine["crossed"]
        endpoints[profile.profile_id + "__turns"] = fine["turns"]
        print(f"{index}/{len(selected)} {profile.profile_id} {summary['sample_class']}", flush=True)

    if args.limit is not None:
        print(json.dumps({"status": "SMOKE_COMPLETE", "profiles": len(selected)}, sort_keys=True))
        return

    endpoints["level4_directions"] = mesh[4][0]
    endpoints["level4_faces"] = mesh[4][1]
    write_tsv(HERE / "WHOLE_SKY_RELATION_ATLAS.tsv", summaries)
    write_tsv(HERE / "MESH_CONVERGENCE_ATLAS.tsv", all_trials)
    np.savez_compressed(HERE / "SKY_ENDPOINTS.npz", **endpoints)
    counts = Counter(row["sample_class"] for row in summaries)
    old_rows = [row for row in summaries if row["G74_regression_profile"] != "-"]
    result = {
        "schema": "udt-cmb-g76-complete-family-whole-sky-v1",
        "status": "PASS",
        "source_manifest_rows": source_rows,
        "profile_count": len(summaries),
        "shape_count": len({row["shape_id"] for row in summaries if row["shape_id"] != "ZERO"}),
        "mesh_trial_rows": len(all_trials),
        "sample_class_counts": dict(sorted(counts.items())),
        "maximum_time_refinement_chord": max(row["time_refinement_endpoint_max_chord"] for row in summaries),
        "maximum_mesh_degree_drift": max(row["mesh_degree_drift_level3_to4"] for row in summaries),
        "maximum_hamiltonian_backward_error": max(row["max_abs_hamiltonian"] for row in summaries),
        "maximum_reflection_chord": max(row["reflection_max_chord"] for row in summaries),
        "maximum_G74_regression_chord": max(row["G74_regression_max_chord"] for row in old_rows),
        "G74_regression_rows": len(old_rows),
        "physical_owner": "OPEN_NO_OWNER",
        "scale_status": "R_POSITIVE_SYMBOLIC_NOT_SELECTED",
        "screen_transport_status": "OPEN_NOT_COMPUTED_BY_ENDPOINT_TANGENT_MAP",
        "runtime_seconds": time.time() - started,
        "protected_draft_read": False,
    }
    assert result["profile_count"] == 591 and result["shape_count"] == 49 and result["mesh_trial_rows"] == 2364
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
