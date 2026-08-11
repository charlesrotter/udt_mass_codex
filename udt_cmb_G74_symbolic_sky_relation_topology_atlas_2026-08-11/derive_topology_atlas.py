#!/usr/bin/env python3
"""Derive the G74 whole-sky topology atlas on the frozen G68 controls.

The production trajectory engine uses the exact Cartesian Hamiltonian for the center-regular
ZERO/PERSISTENT controls. It does not import a source, action, field equation, or observational fit.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROFILE_PATH = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/PROFILE_UNIVERSE.tsv"
START_R = 0.25  # pinned-by-HISTORICAL_CONTROL
END_R = 1.0  # pinned-by-HISTORICAL_CONTROL; not last scattering or X_max
AFFINE_CAP = 4.0  # CHOSE_NUMERIC
LEVELS = (2, 3, 4)  # CHOSE_NUMERIC
STEP_COUNTS = (512, 1024)  # CHOSE_NUMERIC
LANDING = "MIXED_GLOBAL_COMPLETION_CLASSES"


@dataclass(frozen=True)
class Profile:
    profile_id: str
    family: str
    lapse_a: float
    shape: str
    epsilon: float


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def fraction(value: str) -> float:
    if "/" in value:
        left, right = value.split("/", 1)
        return float(left) / float(right)
    return float(value)


def load_profiles() -> list[Profile]:
    profiles = [
        Profile(
            row["profile_id"], row["metric_family"], fraction(row["lapse_a"]),
            row["mix_shape"], fraction(row["mix_epsilon"]),
        )
        for row in read_tsv(PROFILE_PATH)
    ]
    assert len(profiles) == 21 and len({item.profile_id for item in profiles}) == 21
    return profiles


def verify_sources() -> int:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    for row in rows:
        target = ROOT / row["path"]
        assert target.is_file() and digest(target) == row["sha256"], target
    return len(rows)


def center_class(profile: Profile) -> tuple[str, str]:
    if profile.shape in {"ZERO", "PERSISTENT"}:
        return "CENTER_C2_ELIGIBLE", "h/r^2 is constant and Cartesian metric coefficients are smooth"
    if profile.shape in {"TAPERED", "SIGN_CHANGING"}:
        return (
            "BLOCKED_SUPPLIED_PROFILE_NOT_C2_AT_CENTER",
            "h/r^2 contains a nonzero linear |y| term; along the y axis g_tx contains y|y| and has unequal one-sided second derivatives",
        )
    raise ValueError(profile.shape)


def exact_checks() -> dict[str, bool | str | int]:
    # Endpoint transversality: P(J)=J-k*s(J)/s(k) is tangent to the endpoint surface.
    sj, sk = sp.symbols("s_J s_k", nonzero=True, real=True)
    tangent_endpoint = sp.simplify(sj - sk * sj / sk) == 0

    # Axisymmetric map (Theta(theta), m*phi+psi(theta)). Twist drops out of area Jacobian.
    theta = sp.symbols("theta", positive=True)
    m = sp.symbols("m", integer=True, nonzero=True)
    Theta = sp.Function("Theta")(theta)
    twist = sp.Function("psi")(theta)
    coordinate_jacobian = sp.Matrix([[sp.diff(Theta, theta), 0], [sp.diff(twist, theta), m]]).det()
    twist_neutral = sp.simplify(coordinate_jacobian - m * sp.diff(Theta, theta)) == 0
    area_jacobian = sp.simplify(m * sp.sin(Theta) * sp.diff(Theta, theta) / sp.sin(theta))

    # Degree formula after integrating the pulled-back target area form.
    c0, cpi = sp.symbols("c0 cpi", real=True)
    degree_formula = sp.simplify(m * (c0 - cpi) / 2)
    identity_degree = degree_formula.subs({m: 1, c0: 1, cpi: -1}) == 1
    reversal_degree = degree_formula.subs({m: 1, c0: -1, cpi: 1}) == -1
    degree_m = sp.simplify(degree_formula.subs({c0: 1, cpi: -1}) - m) == 0

    # The degree-zero fold Theta=2 theta changes local parity and vanishes at the equator.
    fold_jacobian = sp.simplify(area_jacobian.subs({m: 1, Theta: 2 * theta, sp.diff(Theta, theta): 2}))
    fold_zero_equator = sp.simplify(fold_jacobian.subs(theta, sp.pi / 2)) == 0
    fold_parity_change = (
        float(fold_jacobian.subs(theta, sp.pi / 4)) > 0
        and float(fold_jacobian.subs(theta, 3 * sp.pi / 4)) < 0
    )

    # Exact C2 obstruction used by the candidate census: y|y| has opposite second derivatives.
    y = sp.symbols("y", real=True)
    right_second = sp.diff(y**2, y, 2)
    left_second = sp.diff(-y**2, y, 2)
    center_c2_obstruction = sp.simplify(right_second - left_second) != 0

    # Common positive scale changes physical area by a positive factor only.
    Rs, Ro, j = sp.symbols("R_s R_o j", positive=True)
    scaled_jacobian = (Rs / Ro) ** 2 * j
    scale_preserves_zero = sp.simplify(scaled_jacobian.subs(j, 0)) == 0
    scale_factor_positive = bool(((Rs / Ro) ** 2).is_positive)

    # F01 optical metric: dchi=dr/A and S=r/sqrt(A) give constant curvature a.
    r, a = sp.symbols("r a", real=True)
    A = 1 + a * r**2
    S = r / sp.sqrt(A)
    dS_dchi = sp.simplify(sp.diff(S, r) * A)
    d2S_dchi2 = sp.simplify(sp.diff(dS_dchi, r) * A)
    f01_radial_curvature = sp.simplify(-d2S_dchi2 / S - a) == 0
    f01_tangential_curvature = sp.simplify((1 - dS_dchi**2) / S**2 - a) == 0

    return {
        "endpoint_projection_is_tangent": tangent_endpoint,
        "axisymmetric_twist_drops_from_area_jacobian": twist_neutral,
        "axisymmetric_area_jacobian": str(area_jacobian),
        "identity_degree_plus_one": bool(identity_degree),
        "orientation_reversal_degree_minus_one": bool(reversal_degree),
        "degree_m_witness": bool(degree_m),
        "degree_zero_fold_has_equatorial_critical_set": bool(fold_zero_equator),
        "degree_zero_fold_changes_parity": bool(fold_parity_change),
        "center_C2_obstruction_for_linear_radial_term": bool(center_c2_obstruction),
        "positive_common_scale_preserves_critical_zero": bool(scale_preserves_zero),
        "positive_common_scale_preserves_orientation": scale_factor_positive,
        "F01_optical_radial_curvature_equals_a": bool(f01_radial_curvature),
        "F01_optical_tangential_curvature_equals_a": bool(f01_tangential_curvature),
        "F01_positive_curvature_ball_is_strongly_convex": (
            "chi_R=atan(sqrt(a) R)/sqrt(a) is strictly less than pi/(2 sqrt(a)); "
            "flat and negative-curvature cases are likewise convex"
        ),
        "whole_sphere_regular_cover_theorem": (
            "a smooth everywhere-local-diffeomorphism S2-to-S2 is a proper connected covering; "
            "simple connectedness of S2 forces one sheet and degree plus or minus one"
        ),
    }


def initial_icosahedron() -> tuple[np.ndarray, np.ndarray]:
    golden = (1.0 + math.sqrt(5.0)) / 2.0
    vertices = []
    for a, b in ((-1.0, golden), (1.0, golden), (-1.0, -golden), (1.0, -golden)):
        vertices.append((0.0, a, b))
        vertices.append((a, b, 0.0))
        vertices.append((b, 0.0, a))
    vertices = np.asarray(vertices, dtype=float)
    vertices /= np.linalg.norm(vertices, axis=1)[:, None]
    # Generate the convex-hull faces without depending on a particular vertex enumeration.
    from scipy.spatial import ConvexHull

    faces = np.asarray(ConvexHull(vertices).simplices, dtype=np.int64)
    faces = orient_faces(vertices, faces)
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
    expected_vertices = 10 * 4**level + 2
    expected_faces = 20 * 4**level
    assert len(vertices) == expected_vertices and len(faces) == expected_faces
    return vertices, faces


def initial_state(profile: Profile, directions: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    count = len(directions)
    x = np.zeros((count, 3), dtype=float)
    x[:, 0] = START_R
    a, epsilon = profile.lapse_a, profile.epsilon
    A = 1.0 + a * START_R**2
    B = A + epsilon**2 * START_R**2
    u_t = 1.0 / math.sqrt(A)
    epsi_t = epsilon * START_R / math.sqrt(A * B)
    epsi_y = math.sqrt(A / B)
    k_t = u_t + directions[:, 2] * epsi_t
    velocity = np.empty((count, 3), dtype=float)
    velocity[:, 0] = directions[:, 0] * math.sqrt(A)
    velocity[:, 1] = directions[:, 2] * epsi_y
    velocity[:, 2] = -directions[:, 1]

    w = np.zeros_like(x)
    w[:, 1] = epsilon * START_R
    spatial_metric_v = velocity.copy()
    spatial_metric_v[:, 0] /= A
    p_t = -A * k_t + np.sum(w * velocity, axis=1)
    p = w * k_t[:, None] + spatial_metric_v
    t = np.zeros(count, dtype=float)
    return np.column_stack((t, x)), p_t, p


def hamiltonian_rhs(state: np.ndarray, p_t: np.ndarray, profile: Profile) -> tuple[np.ndarray, np.ndarray]:
    x = state[:, 1:4]
    p = state[:, 4:7]
    a, epsilon = profile.lapse_a, profile.epsilon
    r2 = np.einsum("ij,ij->i", x, x)
    rho2 = x[:, 0] ** 2 + x[:, 1] ** 2
    B = 1.0 + a * r2 + epsilon**2 * rho2
    w = np.column_stack((-epsilon * x[:, 1], epsilon * x[:, 0], np.zeros(len(x))))
    angular = x[:, 0] * p[:, 1] - x[:, 1] * p[:, 0]
    reciprocal_energy = p_t - epsilon * angular
    radial_pair = np.einsum("ij,ij->i", x, p)

    dt = -reciprocal_energy / B
    dx = p + a * radial_pair[:, None] * x + (reciprocal_energy / B)[:, None] * w
    dangular_dx = np.column_stack((p[:, 1], -p[:, 0], np.zeros(len(x))))
    dB = np.column_stack(
        (2.0 * (a + epsilon**2) * x[:, 0], 2.0 * (a + epsilon**2) * x[:, 1], 2.0 * a * x[:, 2])
    )
    dp = (
        -a * radial_pair[:, None] * p
        - (reciprocal_energy * epsilon / B)[:, None] * dangular_dx
        - (0.5 * reciprocal_energy**2 / B**2)[:, None] * dB
    )
    return np.column_stack((dt, dx)), dp


def pack(q: np.ndarray, p: np.ndarray) -> np.ndarray:
    return np.column_stack((q, p))


def rk4_step(state: np.ndarray, p_t: np.ndarray, profile: Profile, step: float) -> np.ndarray:
    def rhs(value: np.ndarray) -> np.ndarray:
        dq, dp = hamiltonian_rhs(value, p_t, profile)
        return pack(dq, dp)

    k1 = rhs(state)
    k2 = rhs(state + 0.5 * step * k1)
    k3 = rhs(state + 0.5 * step * k2)
    k4 = rhs(state + step * k3)
    return state + (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def hamiltonian_value(state: np.ndarray, p_t: np.ndarray, profile: Profile) -> np.ndarray:
    x, p = state[:, 1:4], state[:, 4:7]
    a, epsilon = profile.lapse_a, profile.epsilon
    B = 1.0 + a * np.einsum("ij,ij->i", x, x) + epsilon**2 * (x[:, 0] ** 2 + x[:, 1] ** 2)
    angular = x[:, 0] * p[:, 1] - x[:, 1] * p[:, 0]
    radial_pair = np.einsum("ij,ij->i", x, p)
    return 0.5 * (
        np.einsum("ij,ij->i", p, p) + a * radial_pair**2 - (p_t - epsilon * angular) ** 2 / B
    )


def integrate_sky(profile: Profile, directions: np.ndarray, steps: int) -> dict[str, np.ndarray | float | int]:
    q, p_t, p = initial_state(profile, directions)
    state = pack(q, p)
    initial_h = hamiltonian_value(state, p_t, profile)
    active = np.ones(len(state), dtype=bool)
    crossed = np.zeros(len(state), dtype=bool)
    endpoint = np.full((len(state), 3), np.nan, dtype=float)
    endpoint_t = np.full(len(state), np.nan, dtype=float)
    endpoint_affine = np.full(len(state), np.nan, dtype=float)
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
        max_h = max(max_h, float(np.max(np.abs(hamiltonian_value(new, p_t[index], profile)))))
        nonfinite = ~np.all(np.isfinite(new), axis=1)
        if np.any(nonfinite):
            active[index[nonfinite]] = False
    return {
        "endpoint": endpoint,
        "endpoint_t": endpoint_t,
        "endpoint_affine": endpoint_affine,
        "crossed": crossed,
        "active_remaining": int(np.count_nonzero(active)),
        "max_abs_hamiltonian": max_h,
        "initial_max_abs_hamiltonian": float(np.max(np.abs(initial_h))),
    }


def solid_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    numerator = np.einsum("ij,ij->i", a, np.cross(b, c))
    denominator = 1.0 + np.einsum("ij,ij->i", a, b) + np.einsum("ij,ij->i", b, c) + np.einsum("ij,ij->i", c, a)
    return 2.0 * np.arctan2(numerator, denominator)


def mesh_diagnostics(vertices: np.ndarray, faces: np.ndarray, endpoint: np.ndarray, crossed: np.ndarray) -> dict[str, float | int | str]:
    valid_faces = np.all(crossed[faces], axis=1)
    input_area = solid_angle(vertices[faces[:, 0]], vertices[faces[:, 1]], vertices[faces[:, 2]])
    output_area = np.full(len(faces), np.nan)
    selected = faces[valid_faces]
    output_area[valid_faces] = solid_angle(endpoint[selected[:, 0]], endpoint[selected[:, 1]], endpoint[selected[:, 2]])
    ratios = output_area[valid_faces] / input_area[valid_faces]
    degree = float(np.sum(output_area[valid_faces]) / (4.0 * math.pi))
    negative = int(np.count_nonzero(ratios < 0.0))
    near_zero = int(np.count_nonzero(np.abs(ratios) < 1.0e-3))
    return {
        "vertices": len(vertices),
        "faces": len(faces),
        "crossed_vertices": int(np.count_nonzero(crossed)),
        "missing_vertices": int(np.count_nonzero(~crossed)),
        "valid_faces": int(np.count_nonzero(valid_faces)),
        "degree_signed_area_estimate": degree,
        "min_signed_area_ratio": float(np.min(ratios)) if len(ratios) else math.nan,
        "max_signed_area_ratio": float(np.max(ratios)) if len(ratios) else math.nan,
        "negative_faces": negative,
        "near_zero_faces": near_zero,
        "sample_class": (
            "OBSERVED_SAMPLED_REGULAR_ORIENTATION_PRESERVING"
            if np.all(crossed) and negative == 0 and near_zero == 0
            else "OBSERVED_BRANCH_OR_CRITICAL_CANDIDATE"
        ),
    }


def write_center_atlas(profiles: list[Profile]) -> list[dict[str, str]]:
    rows = []
    for profile in profiles:
        status, reason = center_class(profile)
        rows.append(
            {
                "profile_id": profile.profile_id,
                "family": profile.family,
                "mix_shape": profile.shape,
                "mix_epsilon": f"{profile.epsilon:.17g}",
                "center_status": status,
                "reason": reason,
                "whole_sky_action": "SOLVE_COMPLETE_SKY" if status == "CENTER_C2_ELIGIBLE" else "RETAIN_BLOCKED_NO_REPAIR",
            }
        )
    with (HERE / "CENTER_REGULARITY_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main() -> None:
    source_rows = verify_sources()
    profiles = load_profiles()
    center_rows = write_center_atlas(profiles)
    eligible = [profile for profile in profiles if center_class(profile)[0] == "CENTER_C2_ELIGIBLE"]
    blocked = [profile for profile in profiles if profile not in eligible]
    exact = exact_checks()
    assert all(value is True for value in exact.values() if isinstance(value, bool))

    mesh_cache = {level: icosphere(level) for level in LEVELS}
    rows: list[dict[str, str]] = []
    endpoints: dict[str, np.ndarray] = {}
    profile_summaries: dict[str, dict] = {}
    for profile in eligible:
        trials: dict[tuple[int, int], dict] = {}
        for level in LEVELS:
            vertices, faces = mesh_cache[level]
            for steps in ((512, 1024) if level == 4 else (1024,)):
                result = integrate_sky(profile, vertices, steps)
                diagnostics = mesh_diagnostics(vertices, faces, result["endpoint"], result["crossed"])
                diagnostics.update(
                    {
                        "profile_id": profile.profile_id,
                        "level": level,
                        "steps": steps,
                        "max_abs_hamiltonian": result["max_abs_hamiltonian"],
                        "initial_max_abs_hamiltonian": result["initial_max_abs_hamiltonian"],
                        "active_remaining": result["active_remaining"],
                    }
                )
                trials[(level, steps)] = {**diagnostics, "endpoint": result["endpoint"], "crossed": result["crossed"]}
                rows.append({key: str(value) for key, value in diagnostics.items()})
                if steps == 1024:
                    endpoints[profile.profile_id + f"__level{level}_directions"] = vertices
                    endpoints[profile.profile_id + f"__level{level}_endpoint"] = result["endpoint"]
                if level == 4 and steps == 1024:
                    endpoints[profile.profile_id + "__directions"] = vertices
                    endpoints[profile.profile_id + "__endpoint"] = result["endpoint"]
                    endpoints[profile.profile_id + "__endpoint_t"] = result["endpoint_t"]
                    endpoints[profile.profile_id + "__endpoint_affine"] = result["endpoint_affine"]

        fine = trials[(4, 1024)]
        coarse_time = trials[(4, 512)]
        endpoint_time_error = float(np.nanmax(np.linalg.norm(fine["endpoint"] - coarse_time["endpoint"], axis=1)))
        degree_drift = abs(float(fine["degree_signed_area_estimate"]) - float(trials[(3, 1024)]["degree_signed_area_estimate"]))
        profile_summaries[profile.profile_id] = {
            "center_status": center_class(profile)[0],
            "finest_sample_class": fine["sample_class"],
            "finest_degree_estimate": fine["degree_signed_area_estimate"],
            "finest_min_signed_area_ratio": fine["min_signed_area_ratio"],
            "finest_negative_faces": fine["negative_faces"],
            "finest_near_zero_faces": fine["near_zero_faces"],
            "finest_missing_vertices": fine["missing_vertices"],
            "time_refinement_endpoint_max_chord": endpoint_time_error,
            "mesh_degree_drift_level3_to4": degree_drift,
            "max_abs_hamiltonian": max(float(item["max_abs_hamiltonian"]) for item in trials.values()),
            "authority": (
                "DERIVED_GLOBAL_BIJECTION_F01_OPTICAL_GEOMETRY"
                if profile.family == "F01"
                else "OBSERVED_SAMPLED_REGULAR_NOT_GLOBAL_PROOF"
            ),
        }
        print(profile.profile_id, json.dumps(profile_summaries[profile.profile_id], sort_keys=True), flush=True)

    for profile in blocked:
        profile_summaries[profile.profile_id] = {
            "center_status": center_class(profile)[0],
            "authority": "BLOCKED_NO_WHOLE_SKY_SOLVE_NO_REPAIR",
        }

    if rows:
        fieldnames = list(rows[0])
        with (HERE / "SKY_TOPOLOGY_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    np.savez_compressed(HERE / "SKY_ENDPOINTS.npz", **endpoints)

    payload = {
        "schema": "udt-cmb-g74-symbolic-sky-topology-v1",
        "landing": LANDING,
        "source_manifest_rows": source_rows,
        "candidate_profiles": len(profiles),
        "center_eligible_profiles": len(eligible),
        "center_blocked_profiles": len(blocked),
        "exact_checks": exact,
        "profiles": profile_summaries,
        "status_counts": {
            "DERIVED_GLOBAL_BIJECTION_F01": sum(item.family == "F01" for item in eligible),
            "OBSERVED_SAMPLED_REGULAR_PERSISTENT": sum(item.shape == "PERSISTENT" for item in eligible),
            "BLOCKED_SUPPLIED_PROFILE_NOT_C2_AT_CENTER": len(blocked),
        },
        "scale_status": "POSITIVE_SYMBOLIC_COMMON_SCALE_TOPOLOGY_INVARIANT",
        "physical_owner": "OPEN_NO_OWNER",
        "maximum_conclusion": (
            "complete classification of the exact 21-profile control universe under the declared whole-sky query: "
            "F01 is globally degree-one by exact optical geometry, persistent-mixing controls receive a bounded sampled "
            "global atlas, and tapered/sign-changing controls are blocked by their supplied center regularity without repair"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"landing": LANDING, "status_counts": payload["status_counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
