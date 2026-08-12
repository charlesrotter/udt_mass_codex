#!/usr/bin/env python3
"""Full G77 direct-Christoffel replay of the frozen G76 whole-sky atlas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
import scipy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G75 = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11"
G76 = ROOT / "udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11"
PROFILE_PATH = G75 / "PROFILE_ATLAS.tsv"
SHAPE_PATH = G75 / "SHAPE_ATLAS.tsv"
REFERENCE_ATLAS_PATH = G76 / "WHOLE_SKY_RELATION_ATLAS.tsv"
REFERENCE_ENDPOINT_PATH = G76 / "SKY_ENDPOINTS.npz"
START_R = 0.25  # PINNED_BY_HISTORICAL_CONTROL: frozen G74/G76 query.
END_R = 1.0  # PINNED_BY_HISTORICAL_CONTROL: not last scattering or X_max.
AFFINE_CAP = 4.0  # CHOSE_NUMERIC: frozen integration cap.
STEPS = 2048  # CHOSE_NUMERIC: preregistered full-family direct replay.
REFINEMENT_STEPS = (1024, 2048, 4096)  # CHOSE_NUMERIC.
STRONG_TOL = 2.0e-5  # CHOSE_NUMERIC: preregistered agreement class.
REGISTERED_TOL = 5.0e-5  # CHOSE_NUMERIC: preregistered agreement class.
NULL_TOL = 2.0e-7  # CHOSE_NUMERIC: preregistered backward-error gate.
DEGREE_TOL = 5.0e-4  # CHOSE_NUMERIC: inherited G76 convergence scale.
GAMMA_TOL = 2.0e-12  # CHOSE_NUMERIC: contracted/full Christoffel agreement.
NEAR_THRESHOLDS = (1.0e-2, 1.0e-3, 1.0e-4)  # diagnostics, never filters.
EXPECTED_UNRESOLVED = {
    "G75_A0_S03_E100",
    "G75_AM_S03_E100",
    "G75_AM_S24_E100",
    "G75_AP_S03_E100",
}


@dataclass(frozen=True)
class Profile:
    profile_id: str
    lapse_a: float
    shape_id: str
    amplitude: float
    coefficients: tuple[float, float, float]
    behavior_class: str
    stratum: str

    def q(self, s: np.ndarray) -> np.ndarray:
        c0, c1, c2 = self.coefficients
        return c0 + c1 * s + c2 * s * s

    def qs(self, s: np.ndarray) -> np.ndarray:
        _, c1, c2 = self.coefficients
        return c1 + 2.0 * c2 * s


def digest(path: Path) -> str:
    block = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            block.update(chunk)
    return block.hexdigest()


def array_digest(value: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(value)
    return hashlib.sha256(contiguous.view(np.uint8)).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict]) -> None:
    assert rows
    fields = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rational(text: str) -> float:
    return float(Fraction(text))


def verify_sources() -> dict[str, str]:
    output = {}
    for row in read_tsv(HERE / "SOURCE_MANIFEST.tsv"):
        target = ROOT / row["path"]
        actual = digest(target)
        assert actual == row["sha256"], row["path"]
        output[row["path"]] = actual
    return output


def load_profiles() -> list[Profile]:
    shapes = {row["shape_id"]: row for row in read_tsv(SHAPE_PATH)}
    profiles = []
    for row in read_tsv(PROFILE_PATH):
        if row["shape_id"] == "ZERO":
            coefficients = (0.0, 0.0, 0.0)
            behavior, stratum = "ZERO_MIXING_CONTROL", "ZERO"
        else:
            shape = shapes[row["shape_id"]]
            amplitude = rational(row["amplitude"])
            coefficients = tuple(amplitude * rational(shape[f"normalized_c{i}"]) for i in range(3))
            behavior, stratum = shape["behavior_class"], shape["stratum_code"]
        profiles.append(
            Profile(
                profile_id=row["profile_id"],
                lapse_a=rational(row["lapse_a"]),
                shape_id=row["shape_id"],
                amplitude=rational(row["amplitude"]),
                coefficients=coefficients,
                behavior_class=behavior,
                stratum=stratum,
            )
        )
    assert len(profiles) == len({item.profile_id for item in profiles}) == 591
    return profiles


def metric_only(profile: Profile, position: np.ndarray) -> np.ndarray:
    count = len(position)
    s = np.einsum("bi,bi->b", position, position)
    a = profile.lapse_a
    A = 1.0 + a * s
    q = profile.q(s)
    X, Y = position[:, 0], position[:, 1]
    rotation = np.column_stack((-Y, X, np.zeros(count)))
    w = q[:, None] * rotation
    metric = np.zeros((count, 4, 4), dtype=np.float64)
    metric[:, 0, 0] = -A
    metric[:, 0, 1:4] = w
    metric[:, 1:4, 0] = w
    outer = np.einsum("bi,bj->bij", position, position)
    metric[:, 1:4, 1:4] = np.eye(3)[None, :, :] - (a / A)[:, None, None] * outer
    return metric


def metric_and_derivative(profile: Profile, position: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return g[b,m,n] and partial[b,k,m,n] = d_k g_mn."""
    count = len(position)
    s = np.einsum("bi,bi->b", position, position)
    a = profile.lapse_a
    A = 1.0 + a * s
    q = profile.q(s)
    qs = profile.qs(s)
    X, Y = position[:, 0], position[:, 1]
    rotation = np.column_stack((-Y, X, np.zeros(count)))
    metric = metric_only(profile, position)
    outer = np.einsum("bi,bj->bij", position, position)
    partial = np.zeros((count, 4, 4, 4), dtype=np.float64)
    rotation_derivative = np.array(
        [[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 0.0]], dtype=np.float64
    )
    for axis in range(3):
        derivative = partial[:, axis + 1]
        derivative[:, 0, 0] = -2.0 * a * position[:, axis]
        dw = (
            (2.0 * qs * position[:, axis])[:, None] * rotation
            + q[:, None] * rotation_derivative[axis][None, :]
        )
        derivative[:, 0, 1:4] = dw
        derivative[:, 1:4, 0] = dw
        unit = np.zeros(3)
        unit[axis] = 1.0
        product_derivative = (
            np.einsum("i,bj->bij", unit, position)
            + np.einsum("bi,j->bij", position, unit)
        )
        derivative[:, 1:4, 1:4] = (
            -(a / A)[:, None, None] * product_derivative
            + (2.0 * a * a * position[:, axis] / (A * A))[:, None, None] * outer
        )
    return metric, partial


def contracted_acceleration(metric: np.ndarray, partial: np.ndarray, tangent: np.ndarray) -> np.ndarray:
    first = np.einsum("bkml,bk,bl->bm", partial, tangent, tangent, optimize=True)
    second = 0.5 * np.einsum("bmkl,bk,bl->bm", partial, tangent, tangent, optimize=True)
    lower = first - second
    return -np.linalg.solve(metric, lower[:, :, None])[:, :, 0]


def full_gamma_acceleration(metric: np.ndarray, partial: np.ndarray, tangent: np.ndarray) -> np.ndarray:
    inverse = np.linalg.inv(metric)
    # q[b,a,c,n] = d_a g_nc + d_c g_na - d_n g_ac.
    qterm = (
        np.transpose(partial, (0, 1, 3, 2))
        + np.transpose(partial, (0, 3, 1, 2))
        - np.transpose(partial, (0, 2, 3, 1))
    )
    gamma = 0.5 * np.einsum("bmn,bacn->bmac", inverse, qterm, optimize=True)
    return -np.einsum("bmac,ba,bc->bm", gamma, tangent, tangent, optimize=True)


def rhs(profile: Profile, state: np.ndarray) -> np.ndarray:
    coordinate = state[:, :4]
    tangent = state[:, 4:8]
    metric, partial = metric_and_derivative(profile, coordinate[:, 1:4])
    acceleration = contracted_acceleration(metric, partial, tangent)
    return np.column_stack((tangent, acceleration))


def rk4(profile: Profile, state: np.ndarray, step: float) -> np.ndarray:
    k1 = rhs(profile, state)
    k2 = rhs(profile, state + 0.5 * step * k1)
    k3 = rhs(profile, state + 0.5 * step * k2)
    k4 = rhs(profile, state + step * k3)
    return state + (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def initial_state(profile: Profile, directions: np.ndarray) -> np.ndarray:
    count = len(directions)
    position = np.zeros((count, 3), dtype=np.float64)
    position[:, 0] = START_R
    s0 = np.array([START_R * START_R])
    q0 = float(profile.q(s0)[0])
    A = 1.0 + profile.lapse_a * float(s0[0])
    B = A + q0 * q0 * float(s0[0])
    tangent = np.empty((count, 4), dtype=np.float64)
    tangent[:, 0] = 1.0 / math.sqrt(A) + directions[:, 2] * q0 * START_R / math.sqrt(A * B)
    tangent[:, 1] = directions[:, 0] * math.sqrt(A)
    tangent[:, 2] = directions[:, 2] * math.sqrt(A / B)
    tangent[:, 3] = -directions[:, 1]
    coordinate = np.column_stack((np.zeros(count), position))
    return np.column_stack((coordinate, tangent))


def null_error(profile: Profile, state: np.ndarray) -> float:
    if not len(state):
        return 0.0
    metric = metric_only(profile, state[:, 1:4])
    tangent = state[:, 4:8]
    value = np.einsum("bi,bij,bj->b", tangent, metric, tangent, optimize=True)
    return float(np.max(np.abs(value)))


def integrate(profile: Profile, directions: np.ndarray, steps: int) -> dict:
    state = initial_state(profile, directions)
    endpoint = np.full((len(state), 3), np.nan, dtype=np.float64)
    crossed = np.zeros(len(state), dtype=bool)
    active = np.ones(len(state), dtype=bool)
    nonfinite = np.zeros(len(state), dtype=bool)
    maximum_null = null_error(profile, state)
    step = AFFINE_CAP / steps
    for _ in range(steps):
        if not np.any(active):
            break
        index = np.flatnonzero(active)
        old = state[index]
        new = rk4(profile, old, step)
        finite = np.all(np.isfinite(new), axis=1)
        if np.any(~finite):
            failed = index[~finite]
            nonfinite[failed] = True
            active[failed] = False
        if not np.any(finite):
            continue
        live_index = index[finite]
        old_live, new_live = old[finite], new[finite]
        old_r = np.linalg.norm(old_live[:, 1:4], axis=1)
        new_r = np.linalg.norm(new_live[:, 1:4], axis=1)
        hit = (old_r < END_R) & (new_r >= END_R)
        if np.any(hit):
            weight = np.clip(
                (END_R - old_r[hit]) / np.maximum(new_r[hit] - old_r[hit], 1.0e-15),
                0.0,
                1.0,
            )
            point = old_live[hit] + weight[:, None] * (new_live[hit] - old_live[hit])
            vector = point[:, 1:4]
            vector /= np.linalg.norm(vector, axis=1)[:, None]
            hit_index = live_index[hit]
            endpoint[hit_index] = vector
            crossed[hit_index] = True
            active[hit_index] = False
        state[live_index] = new_live
        maximum_null = max(maximum_null, null_error(profile, new_live))
    return {
        "endpoint": endpoint,
        "crossed": crossed,
        "maximum_null": maximum_null,
        "nonfinite_count": int(np.count_nonzero(nonfinite)),
        "active_remaining": int(np.count_nonzero(active)),
    }


def solid_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    numerator = np.einsum("bi,bi->b", a, np.cross(b, c))
    denominator = (
        1.0
        + np.einsum("bi,bi->b", a, b)
        + np.einsum("bi,bi->b", b, c)
        + np.einsum("bi,bi->b", c, a)
    )
    return 2.0 * np.arctan2(numerator, denominator)


def projected_face_orientation(vertices: np.ndarray, faces: np.ndarray, endpoint: np.ndarray, valid: np.ndarray) -> np.ndarray:
    output = np.full(len(faces), np.nan)
    selected = np.flatnonzero(valid)
    if not len(selected):
        return output
    tri_in = vertices[faces[selected]]
    tri_out = endpoint[faces[selected]]
    center_in = np.sum(tri_in, axis=1)
    center_out = np.sum(tri_out, axis=1)
    center_in /= np.linalg.norm(center_in, axis=1)[:, None]
    center_out /= np.linalg.norm(center_out, axis=1)[:, None]
    edge_in_1 = tri_in[:, 1] - tri_in[:, 0]
    edge_in_2 = tri_in[:, 2] - tri_in[:, 0]
    edge_out_1 = tri_out[:, 1] - tri_out[:, 0]
    edge_out_2 = tri_out[:, 2] - tri_out[:, 0]
    edge_in_1 -= np.einsum("bi,bi->b", edge_in_1, center_in)[:, None] * center_in
    edge_in_2 -= np.einsum("bi,bi->b", edge_in_2, center_in)[:, None] * center_in
    edge_out_1 -= np.einsum("bi,bi->b", edge_out_1, center_out)[:, None] * center_out
    edge_out_2 -= np.einsum("bi,bi->b", edge_out_2, center_out)[:, None] * center_out
    det_in = np.einsum("bi,bi->b", center_in, np.cross(edge_in_1, edge_in_2))
    det_out = np.einsum("bi,bi->b", center_out, np.cross(edge_out_1, edge_out_2))
    usable = np.abs(det_in) > 1.0e-14
    output[selected[usable]] = det_out[usable] / det_in[usable]
    return output


def face_diagnostics(vertices: np.ndarray, faces: np.ndarray, endpoint: np.ndarray, crossed: np.ndarray) -> dict:
    valid = np.all(crossed[faces], axis=1)
    input_area = solid_angle(vertices[faces[:, 0]], vertices[faces[:, 1]], vertices[faces[:, 2]])
    output_area = np.full(len(faces), np.nan)
    chosen = faces[valid]
    if len(chosen):
        output_area[valid] = solid_angle(endpoint[chosen[:, 0]], endpoint[chosen[:, 1]], endpoint[chosen[:, 2]])
    ratios = output_area[valid] / input_area[valid]
    projected = projected_face_orientation(vertices, faces, endpoint, valid)
    finite_projected = np.isfinite(projected)
    return {
        "valid_faces": int(np.count_nonzero(valid)),
        "degree": float(np.nansum(output_area) / (4.0 * math.pi)),
        "min_signed_area_ratio": float(np.min(ratios)) if len(ratios) else math.nan,
        "max_signed_area_ratio": float(np.max(ratios)) if len(ratios) else math.nan,
        "negative_faces": int(np.count_nonzero(ratios < 0.0)),
        "near_area_1e2": int(np.count_nonzero(np.abs(ratios) < NEAR_THRESHOLDS[0])),
        "near_area_1e3": int(np.count_nonzero(np.abs(ratios) < NEAR_THRESHOLDS[1])),
        "near_area_1e4": int(np.count_nonzero(np.abs(ratios) < NEAR_THRESHOLDS[2])),
        "projected_face_maps": int(np.count_nonzero(finite_projected)),
        "negative_projected_face_maps": int(np.count_nonzero(projected[finite_projected] < 0.0)),
        "min_projected_area_ratio": float(np.nanmin(projected)) if np.any(finite_projected) else math.nan,
        "max_projected_area_ratio": float(np.nanmax(projected)) if np.any(finite_projected) else math.nan,
    }


def endpoint_chord(left: np.ndarray, right: np.ndarray, left_mask: np.ndarray, right_mask: np.ndarray) -> tuple[float, int]:
    mismatch = int(np.count_nonzero(left_mask != right_mask))
    common = left_mask & right_mask
    chord = float(np.max(np.linalg.norm(left[common] - right[common], axis=1))) if np.any(common) else math.inf
    return chord, mismatch


def equation_control(profiles: list[Profile]) -> dict:
    control_ids = ("G75_F01_A0", "G75_AM_S03_E100", "G75_AP_S24_E05")
    lookup = {item.profile_id: item for item in profiles}
    rng = np.random.default_rng(770811)
    maximum = 0.0
    count = 0
    for profile_id in control_ids:
        profile = lookup[profile_id]
        position = rng.uniform(-0.7, 0.7, size=(8, 3))
        tangent = rng.normal(size=(8, 4))
        metric, partial = metric_and_derivative(profile, position)
        contracted = contracted_acceleration(metric, partial, tangent)
        full = full_gamma_acceleration(metric, partial, tangent)
        maximum = max(maximum, float(np.max(np.abs(contracted - full))))
        count += len(position)
    return {
        "control_states": count,
        "maximum_acceleration_difference": maximum,
        "tolerance": GAMMA_TOL,
        "pass": maximum <= GAMMA_TOL,
    }


def open_or_create(path: Path, dtype, shape, fill):
    if path.exists():
        output = np.lib.format.open_memmap(path, mode="r+")
        assert output.shape == shape and output.dtype == np.dtype(dtype), path
        return output
    output = np.lib.format.open_memmap(path, mode="w+", dtype=dtype, shape=shape)
    output[...] = fill
    output.flush()
    return output


def checkpoint_arrays(profile_count: int, ray_count: int):
    endpoint = open_or_create(HERE / "DIRECT_ENDPOINTS.npy", np.float64, (profile_count, ray_count, 3), np.nan)
    crossed = open_or_create(HERE / "DIRECT_CROSSED.npy", np.bool_, (profile_count, ray_count), False)
    completed = open_or_create(HERE / "DIRECT_COMPLETED.npy", np.bool_, (profile_count,), False)
    null_max = open_or_create(HERE / "DIRECT_NULL_MAX.npy", np.float64, (profile_count,), np.nan)
    nonfinite = open_or_create(HERE / "DIRECT_NONFINITE.npy", np.int64, (profile_count,), -1)
    active = open_or_create(HERE / "DIRECT_ACTIVE_REMAINING.npy", np.int64, (profile_count,), -1)
    return endpoint, crossed, completed, null_max, nonfinite, active


def agreement_class(chord: float, mismatch: int) -> str:
    if mismatch != 0 or not math.isfinite(chord) or chord > REGISTERED_TOL:
        return "CROSS_METHOD_NUMERICALLY_UNRESOLVED"
    if chord <= STRONG_TOL:
        return "STRONG_DIRECT_AGREEMENT"
    return "REGISTERED_DIRECT_AGREEMENT"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-new-profiles", type=int, default=None, help="Numeric scheduling control for bounded/resumed execution.")
    args = parser.parse_args()
    started = time.time()
    source_hashes = verify_sources()
    profiles = load_profiles()
    reference_rows = {row["profile_id"]: row for row in read_tsv(REFERENCE_ATLAS_PATH)}
    unresolved = {key for key, row in reference_rows.items() if row["sample_class"] == "NUMERICALLY_UNRESOLVED"}
    assert unresolved == EXPECTED_UNRESOLVED
    reference = np.load(REFERENCE_ENDPOINT_PATH, allow_pickle=False)
    directions = np.asarray(reference["level4_directions"], dtype=np.float64)
    faces = np.asarray(reference["level4_faces"], dtype=np.int64)
    assert directions.shape == (2562, 3) and faces.shape == (5120, 3)
    mesh_hashes = {"directions": array_digest(directions), "faces": array_digest(faces)}
    equation = equation_control(profiles)
    assert equation["pass"], equation

    meta = {
        "schema": "udt-cmb-g77-direct-checkpoint-v1",
        "profile_ids": [item.profile_id for item in profiles],
        "source_hashes": source_hashes,
        "mesh_hashes": mesh_hashes,
        "parameters": {
            "start_r": START_R,
            "end_r": END_R,
            "affine_cap": AFFINE_CAP,
            "steps": STEPS,
            "dtype": "float64",
            "ray_count": len(directions),
            "face_count": len(faces),
        },
    }
    meta_path = HERE / "CHECKPOINT_META.json"
    if meta_path.exists():
        assert json.loads(meta_path.read_text(encoding="utf-8")) == meta
    else:
        meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    endpoints, masks, completed, null_max, nonfinite, active = checkpoint_arrays(len(profiles), len(directions))
    new_count = 0
    for index, profile in enumerate(profiles):
        if completed[index]:
            continue
        if args.max_new_profiles is not None and new_count >= args.max_new_profiles:
            break
        row_started = time.time()
        result = integrate(profile, directions, STEPS)
        endpoints[index] = result["endpoint"]
        masks[index] = result["crossed"]
        null_max[index] = result["maximum_null"]
        nonfinite[index] = result["nonfinite_count"]
        active[index] = result["active_remaining"]
        endpoints.flush()
        masks.flush()
        null_max.flush()
        nonfinite.flush()
        active.flush()
        completed[index] = True
        completed.flush()
        new_count += 1
        print(
            f"{index + 1:03d}/591 {profile.profile_id} rays={int(np.count_nonzero(result['crossed']))}/2562 "
            f"null={result['maximum_null']:.3e} elapsed={time.time() - row_started:.2f}s",
            flush=True,
        )

    completed_count = int(np.count_nonzero(completed))
    if completed_count != len(profiles):
        partial = {
            "schema": "udt-cmb-g77-partial-run-v1",
            "completed": completed_count,
            "total": len(profiles),
            "new_this_invocation": new_count,
            "status": "PARTIAL_RESTARTABLE",
        }
        (HERE / "PARTIAL_RUN.json").write_text(json.dumps(partial, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(partial, indent=2, sort_keys=True))
        return

    atlas_rows = []
    for index, profile in enumerate(profiles):
        direct_endpoint = np.asarray(endpoints[index])
        direct_mask = np.asarray(masks[index])
        reference_endpoint = np.asarray(reference[profile.profile_id + "__endpoint"])
        reference_mask = np.asarray(reference[profile.profile_id + "__crossed"])
        chord, mismatch = endpoint_chord(direct_endpoint, reference_endpoint, direct_mask, reference_mask)
        diagnostics = face_diagnostics(directions, faces, direct_endpoint, direct_mask)
        reference_row = reference_rows[profile.profile_id]
        degree_difference = abs(diagnostics["degree"] - float(reference_row["finest_degree_estimate"]))
        classification = agreement_class(chord, mismatch)
        if float(null_max[index]) > NULL_TOL or degree_difference > DEGREE_TOL:
            classification = "CROSS_METHOD_NUMERICALLY_UNRESOLVED"
        atlas_rows.append(
            {
                "profile_id": profile.profile_id,
                "shape_id": profile.shape_id,
                "stratum_code": profile.stratum,
                "behavior_class": profile.behavior_class,
                "lapse_a": profile.lapse_a,
                "amplitude": profile.amplitude,
                "G76_sample_class": reference_row["sample_class"],
                "direct_class": classification,
                "crossed_vertices": int(np.count_nonzero(direct_mask)),
                "missing_vertices": int(np.count_nonzero(~direct_mask)),
                "crossing_mask_mismatch": mismatch,
                "direct_G76_max_chord": chord,
                "maximum_null_backward_error": float(null_max[index]),
                "nonfinite_count": int(nonfinite[index]),
                "active_remaining": int(active[index]),
                "valid_faces": diagnostics["valid_faces"],
                "degree": diagnostics["degree"],
                "G76_degree_difference": degree_difference,
                "min_signed_area_ratio": diagnostics["min_signed_area_ratio"],
                "max_signed_area_ratio": diagnostics["max_signed_area_ratio"],
                "negative_faces": diagnostics["negative_faces"],
                "near_area_1e2": diagnostics["near_area_1e2"],
                "near_area_1e3": diagnostics["near_area_1e3"],
                "near_area_1e4": diagnostics["near_area_1e4"],
                "projected_face_maps": diagnostics["projected_face_maps"],
                "negative_projected_face_maps": diagnostics["negative_projected_face_maps"],
                "min_projected_area_ratio": diagnostics["min_projected_area_ratio"],
                "max_projected_area_ratio": diagnostics["max_projected_area_ratio"],
            }
        )
    write_tsv(HERE / "DIRECT_CHRISTOFFEL_ATLAS.tsv", atlas_rows)

    refinement_rows = []
    refinement_archive = {}
    profile_lookup = {item.profile_id: item for item in profiles}
    profile_index = {item.profile_id: index for index, item in enumerate(profiles)}
    for profile_id in sorted(unresolved):
        profile = profile_lookup[profile_id]
        result_1024 = integrate(profile, directions, 1024)
        result_4096 = integrate(profile, directions, 4096)
        endpoint_2048 = np.asarray(endpoints[profile_index[profile_id]])
        mask_2048 = np.asarray(masks[profile_index[profile_id]])
        chord_1024_2048, mismatch_1024_2048 = endpoint_chord(
            result_1024["endpoint"], endpoint_2048, result_1024["crossed"], mask_2048
        )
        chord_2048_4096, mismatch_2048_4096 = endpoint_chord(
            endpoint_2048, result_4096["endpoint"], mask_2048, result_4096["crossed"]
        )
        status = (
            "DIRECT_TIME_REFINEMENT_RESOLVED"
            if mismatch_2048_4096 == 0
            and chord_2048_4096 <= REGISTERED_TOL
            and result_4096["maximum_null"] <= NULL_TOL
            else "DIRECT_TIME_REFINEMENT_UNRESOLVED"
        )
        ratio = chord_1024_2048 / chord_2048_4096 if chord_2048_4096 > 0.0 else math.inf
        refinement_rows.append(
            {
                "profile_id": profile_id,
                "G76_sample_class": reference_rows[profile_id]["sample_class"],
                "direct_1024_2048_max_chord": chord_1024_2048,
                "direct_1024_2048_mask_mismatch": mismatch_1024_2048,
                "direct_2048_4096_max_chord": chord_2048_4096,
                "direct_2048_4096_mask_mismatch": mismatch_2048_4096,
                "refinement_ratio": ratio,
                "null_1024": result_1024["maximum_null"],
                "null_2048": float(null_max[profile_index[profile_id]]),
                "null_4096": result_4096["maximum_null"],
                "G77_refinement_status": status,
            }
        )
        refinement_archive[profile_id + "__endpoint_1024"] = result_1024["endpoint"]
        refinement_archive[profile_id + "__crossed_1024"] = result_1024["crossed"]
        refinement_archive[profile_id + "__endpoint_4096"] = result_4096["endpoint"]
        refinement_archive[profile_id + "__crossed_4096"] = result_4096["crossed"]
        print(
            f"REFINE {profile_id} 1024/2048={chord_1024_2048:.3e} "
            f"2048/4096={chord_2048_4096:.3e} {status}",
            flush=True,
        )
    write_tsv(HERE / "UNRESOLVED_REFINEMENT_ATLAS.tsv", refinement_rows)
    np.savez_compressed(HERE / "UNRESOLVED_REFINEMENT_ENDPOINTS.npz", **refinement_archive)

    class_counts = {}
    for row in atlas_rows:
        class_counts[row["direct_class"]] = class_counts.get(row["direct_class"], 0) + 1
    refinement_counts = {}
    for row in refinement_rows:
        key = row["G77_refinement_status"]
        refinement_counts[key] = refinement_counts.get(key, 0) + 1
    checks = {
        "source_hashes": len(source_hashes) == 8,
        "profile_census": len(atlas_rows) == 591,
        "mesh_identity": directions.shape == (2562, 3) and faces.shape == (5120, 3),
        "contracted_full_gamma": equation["pass"],
        "complete_checkpoint": int(np.count_nonzero(completed)) == 591,
        "four_row_refinement": {row["profile_id"] for row in refinement_rows} == EXPECTED_UNRESOLVED,
        "history_preserved": all(row["G76_sample_class"] == reference_rows[row["profile_id"]]["sample_class"] for row in atlas_rows),
        "no_physical_selection": True,
    }
    result = {
        "schema": "udt-cmb-g77-direct-replay-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "equation_control": equation,
        "profile_count": len(atlas_rows),
        "ray_count_per_profile": len(directions),
        "face_count_per_profile": len(faces),
        "class_counts": class_counts,
        "refinement_counts": refinement_counts,
        "maximum_direct_G76_chord": max(float(row["direct_G76_max_chord"]) for row in atlas_rows),
        "maximum_null_backward_error": max(float(row["maximum_null_backward_error"]) for row in atlas_rows),
        "maximum_degree_difference": max(float(row["G76_degree_difference"]) for row in atlas_rows),
        "negative_faces_total": sum(int(row["negative_faces"]) for row in atlas_rows),
        "negative_projected_face_maps_total": sum(int(row["negative_projected_face_maps"]) for row in atlas_rows),
        "near_area_1e2_total": sum(int(row["near_area_1e2"]) for row in atlas_rows),
        "elapsed_seconds_this_invocation": time.time() - started,
        "runtime": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if (HERE / "PARTIAL_RUN.json").exists():
        (HERE / "PARTIAL_RUN.json").unlink()
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
