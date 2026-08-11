#!/usr/bin/env python3
"""Finite-path F01/F02 geodesic, screen, and Jacobi control atlas.

The geometry engine evaluates the metric and its analytic first/second derivatives, then builds
the Levi-Civita connection and Riemann tensor numerically. It imports no repository physics code.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


HERE = Path(__file__).resolve().parent
R_CONTROL = 1.0  # CHOSE_CONTROL: dimensionless comparison scale, not X_max.
S_CAP = 10.0  # NUMERIC: bounded affine integration cap in units of R.
START_X = 0.25  # CHOSE_CONTROL: frozen regular-chart start.
END_X = 1.0  # CHOSE_CONTROL: frozen comparison surface, not a physical boundary.
PRODUCTION = dict(method="DOP853", rtol=1.0e-10, atol=1.0e-12, max_step=1.0 / 200.0)
REFINED = dict(method="DOP853", rtol=2.0e-12, atol=2.0e-14, max_step=1.0 / 400.0)
SECOND_METHOD = dict(method="RK45", rtol=2.0e-12, atol=2.0e-14, max_step=1.0 / 400.0)


@dataclass(frozen=True)
class Profile:
    profile_id: str
    family: str
    lapse_a: float
    shape: str
    epsilon: float
    sign: float = 1.0


def load_profiles() -> list[Profile]:
    out: list[Profile] = []
    with (HERE / "PROFILE_UNIVERSE.tsv").open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            out.append(
                Profile(
                    profile_id=row["profile_id"],
                    family=row["metric_family"],
                    lapse_a=float(eval_fraction(row["lapse_a"])),
                    shape=row["mix_shape"],
                    epsilon=float(eval_fraction(row["mix_epsilon"])),
                )
            )
    if len(out) != 21 or len({p.profile_id for p in out}) != 21:
        raise RuntimeError("registered profile universe is not exactly 21 unique rows")
    return out


def eval_fraction(value: str) -> float:
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        return float(numerator) / float(denominator)
    return float(value)


def profile_values(profile: Profile, r: float) -> tuple[float, float, float, float, float, float]:
    """Return A,A',A'',h,h',h'' for R=1."""
    a = profile.lapse_a
    A = 1.0 + a * r * r
    A1 = 2.0 * a * r
    A2 = 2.0 * a
    e = profile.sign * profile.epsilon
    if profile.family == "F01" or profile.shape == "ZERO":
        h = h1 = h2 = 0.0
    elif profile.shape == "PERSISTENT":
        h = e * r**2
        h1 = e * 2.0 * r
        h2 = e * 2.0
    elif profile.shape == "TAPERED":
        h = e * (r**2 - 2.0 * r**3 + r**4)
        h1 = e * (2.0 * r - 6.0 * r**2 + 4.0 * r**3)
        h2 = e * (2.0 - 12.0 * r + 12.0 * r**2)
    elif profile.shape == "SIGN_CHANGING":
        h = e * (r**2 - 2.0 * r**3)
        h1 = e * (2.0 * r - 6.0 * r**2)
        h2 = e * (2.0 - 12.0 * r)
    else:
        raise ValueError(profile.shape)
    return A, A1, A2, h, h1, h2


def metric_derivatives(profile: Profile, position: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Metric, first derivatives dg[k,i,j], and second derivatives ddg[k,l,i,j]."""
    _, r, theta, _ = position
    A, A1, A2, h, h1, h2 = profile_values(profile, float(r))
    sine = math.sin(float(theta))
    cosine = math.cos(float(theta))
    s2 = sine * sine
    sc = sine * cosine

    g = np.zeros((4, 4), dtype=np.float64)
    g[0, 0] = -A
    g[1, 1] = 1.0 / A
    g[2, 2] = r * r
    g[3, 3] = r * r * s2
    g[0, 3] = g[3, 0] = h * s2

    dg = np.zeros((4, 4, 4), dtype=np.float64)
    dg[1, 0, 0] = -A1
    dg[1, 1, 1] = -A1 / A**2
    dg[1, 2, 2] = 2.0 * r
    dg[1, 3, 3] = 2.0 * r * s2
    dg[1, 0, 3] = dg[1, 3, 0] = h1 * s2
    dg[2, 3, 3] = 2.0 * r * r * sc
    dg[2, 0, 3] = dg[2, 3, 0] = 2.0 * h * sc

    ddg = np.zeros((4, 4, 4, 4), dtype=np.float64)
    ddg[1, 1, 0, 0] = -A2
    ddg[1, 1, 1, 1] = 2.0 * A1**2 / A**3 - A2 / A**2
    ddg[1, 1, 2, 2] = 2.0
    ddg[1, 1, 3, 3] = 2.0 * s2
    ddg[1, 1, 0, 3] = ddg[1, 1, 3, 0] = h2 * s2
    ddg[1, 2, 3, 3] = ddg[2, 1, 3, 3] = 4.0 * r * sc
    ddg[1, 2, 0, 3] = ddg[2, 1, 0, 3] = 2.0 * h1 * sc
    ddg[1, 2, 3, 0] = ddg[2, 1, 3, 0] = 2.0 * h1 * sc
    angular_second = 2.0 * (cosine * cosine - sine * sine)
    ddg[2, 2, 3, 3] = r * r * angular_second
    ddg[2, 2, 0, 3] = ddg[2, 2, 3, 0] = h * angular_second
    return g, dg, ddg


def geometry(profile: Profile, position: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return g, Gamma^rho_mn, and R^rho_sigma_mu_nu in the registered convention."""
    g, dg, ddg = metric_derivatives(profile, position)
    gi = np.linalg.inv(g)
    q = dg.transpose(1, 0, 2) + dg.transpose(1, 2, 0) - dg
    Gamma = 0.5 * np.einsum("rl,lmn->rmn", gi, q)
    dgi = -np.einsum("ra,kab,bl->krl", gi, dg, gi)
    dq = ddg.transpose(0, 2, 1, 3) + ddg.transpose(0, 2, 3, 1) - ddg
    dGamma = 0.5 * (
        np.einsum("krl,lmn->krmn", dgi, q)
        + np.einsum("rl,klmn->krmn", gi, dq)
    )
    R = (
        dGamma.transpose(1, 3, 0, 2)
        - dGamma.transpose(1, 3, 2, 0)
        + np.einsum("rml,lns->rsmn", Gamma, Gamma)
        - np.einsum("rnl,lms->rsmn", Gamma, Gamma)
    )
    return g, Gamma, R


def initial_state(profile: Profile) -> np.ndarray:
    position = np.array([0.0, START_X, math.pi / 2.0, 0.0], dtype=np.float64)
    A, _, _, h, _, _ = profile_values(profile, START_X)
    denom = A * START_X**2 + h**2
    u = np.array([1.0 / math.sqrt(A), 0.0, 0.0, 0.0])
    radial = np.array([0.0, math.sqrt(A), 0.0, 0.0])
    e_theta = np.array([0.0, 0.0, 1.0 / START_X, 0.0])
    e_psi = np.array([h / (math.sqrt(A) * math.sqrt(denom)), 0.0, 0.0, math.sqrt(A) / math.sqrt(denom)])
    k = u + radial
    E = np.stack((e_theta, e_psi))
    J = np.zeros((2, 4), dtype=np.float64)
    P = E.copy()
    return np.concatenate((position, k, E.ravel(), J.ravel(), P.ravel()))


def unpack(state: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return (
        state[0:4],
        state[4:8],
        state[8:16].reshape(2, 4),
        state[16:24].reshape(2, 4),
        state[24:32].reshape(2, 4),
    )


def full_rhs(profile: Profile):
    def rhs(_affine: float, state: np.ndarray) -> np.ndarray:
        position, k, E, J, P = unpack(state)
        _, Gamma, R = geometry(profile, position)
        dk = -np.einsum("rmn,m,n->r", Gamma, k, k)
        dE = -np.einsum("rmn,m,an->ar", Gamma, k, E)
        dJ = P - np.einsum("rmn,m,an->ar", Gamma, k, J)
        curvature = np.einsum("rsmn,s,am,n->ar", R, k, J, k)
        dP = -np.einsum("rmn,m,an->ar", Gamma, k, P) - curvature
        return np.concatenate((k, dk, dE.ravel(), dJ.ravel(), dP.ravel()))

    return rhs


def endpoint_event(_affine: float, state: np.ndarray) -> float:
    return float(state[1] - END_X)


endpoint_event.terminal = True
endpoint_event.direction = 1.0


def turning_event(_affine: float, state: np.ndarray) -> float:
    return float(state[5])


turning_event.terminal = False
turning_event.direction = -1.0


def integrate(profile: Profile, controls: dict) -> object:
    return solve_ivp(
        full_rhs(profile),
        (0.0, S_CAP),
        initial_state(profile),
        events=(endpoint_event, turning_event),
        dense_output=True,
        **controls,
    )


def screen_objects(profile: Profile, state: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    position, k, E, J, P = unpack(state)
    g, _, R = geometry(profile, position)
    D = E @ g @ J.T
    Ddot = E @ g @ P.T
    tidal = np.zeros((2, 2), dtype=np.float64)
    for aa in range(2):
        for bb in range(2):
            vector = np.einsum("rsmn,s,m,n->r", R, k, E[bb], k)
            tidal[aa, bb] = E[aa] @ g @ vector
    return D, Ddot, tidal, g


def relative_norm(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def endpoint_map(profile: Profile, solution: object) -> tuple[float, np.ndarray, np.ndarray]:
    if len(solution.t_events[0]) == 0:
        affine = float(solution.t[-1])
    else:
        affine = float(solution.t_events[0][0])
    state = np.asarray(solution.sol(affine), dtype=np.float64)
    D, _, _, _ = screen_objects(profile, state)
    return affine, state, D


def first_caustic(profile: Profile, solution: object, final_s: float) -> tuple[float | None, float]:
    grid = np.linspace(max(1.0e-5, final_s / 5000.0), final_s, 2001)
    determinants = np.empty_like(grid)
    smallest = math.inf
    for index, affine in enumerate(grid):
        D, _, _, _ = screen_objects(profile, np.asarray(solution.sol(float(affine))))
        determinants[index] = np.linalg.det(D)
        smallest = min(smallest, float(np.linalg.svd(D, compute_uv=False)[-1]))
    for index in range(1, len(grid)):
        if determinants[index - 1] * determinants[index] < 0.0:
            def det_at(value: float) -> float:
                D, _, _, _ = screen_objects(profile, np.asarray(solution.sol(value)))
                return float(np.linalg.det(D))
            root = brentq(det_at, float(grid[index - 1]), float(grid[index]), xtol=1.0e-12)
            return float(root), float(smallest)
    return None, float(smallest)


def path_residuals(profile: Profile, solution: object, final_s: float) -> dict[str, float]:
    grid = np.linspace(0.0, final_s, 301)
    maxima = dict(
        null=0.0,
        screen_gram=0.0,
        screen_ray=0.0,
        wronskian=0.0,
        tidal_antisymmetry=0.0,
        conserved_p_t=0.0,
        conserved_p_psi=0.0,
    )
    initial_state_value = np.asarray(solution.sol(0.0), dtype=np.float64)
    initial_position, initial_k, _, _, _ = unpack(initial_state_value)
    initial_g, _, _ = geometry(profile, initial_position)
    initial_pt = float(initial_g[0] @ initial_k)
    initial_ppsi = float(initial_g[3] @ initial_k)
    min_A = math.inf
    min_block_D = math.inf
    for affine in grid:
        state = np.asarray(solution.sol(float(affine)), dtype=np.float64)
        position, k, E, _, _ = unpack(state)
        D, Ddot, tidal, g = screen_objects(profile, state)
        null = abs(float(k @ g @ k)) / max(1.0, float(np.linalg.norm(k)) ** 2 * float(np.linalg.norm(g)))
        gram = E @ g @ E.T
        ray = E @ g @ k
        wronskian = D.T @ Ddot - Ddot.T @ D
        maxima["null"] = max(maxima["null"], null)
        maxima["screen_gram"] = max(maxima["screen_gram"], float(np.max(np.abs(gram - np.eye(2)))))
        maxima["screen_ray"] = max(maxima["screen_ray"], float(np.max(np.abs(ray))))
        maxima["wronskian"] = max(maxima["wronskian"], float(np.max(np.abs(wronskian))))
        maxima["tidal_antisymmetry"] = max(maxima["tidal_antisymmetry"], float(np.max(np.abs(tidal - tidal.T))))
        maxima["conserved_p_t"] = max(maxima["conserved_p_t"], abs(float(g[0] @ k) - initial_pt))
        maxima["conserved_p_psi"] = max(maxima["conserved_p_psi"], abs(float(g[3] @ k) - initial_ppsi))
        A, _, _, h, _, _ = profile_values(profile, float(position[1]))
        min_A = min(min_A, A)
        min_block_D = min(min_block_D, A * float(position[1]) ** 2 + h**2 * math.sin(float(position[2])) ** 2)
        if not np.all(np.isfinite(position)):
            raise FloatingPointError("nonfinite trajectory")
    return {**{key: float(value) for key, value in maxima.items()}, "min_A": float(min_A), "min_block_D": float(min_block_D)}


def classify_solution(solution: object, caustic: float | None) -> str:
    endpoint = len(solution.t_events[0]) > 0
    turning = len(solution.t_events[1]) > 0
    if not solution.success:
        return "SOLVER_FAILURE"
    if endpoint and caustic is not None:
        return "ENDPOINT_AFTER_CAUSTIC"
    if endpoint:
        return "ENDPOINT_REGULAR_NO_CAUSTIC"
    if turning:
        return "TURNING_NO_ENDPOINT"
    return "AFFINE_CAP_NO_ENDPOINT"


def endpoint_summary(profile: Profile, solution: object) -> tuple[dict, np.ndarray, np.ndarray]:
    affine, state, D = endpoint_map(profile, solution)
    position, k, E, _, _ = unpack(state)
    _, Ddot, tidal, g = screen_objects(profile, state)
    caustic, min_singular_path = first_caustic(profile, solution, affine)
    singular = np.linalg.svd(D, compute_uv=False)
    polar_u, _, polar_vt = np.linalg.svd(D)
    polar = polar_u @ polar_vt
    rotation = math.atan2(float(polar[1, 0]), float(polar[0, 0]))
    symmetric = 0.5 * (D + D.T)
    antisymmetric = 0.5 * (D - D.T)
    p_t = float(g[0] @ k)
    p_psi = float(g[3] @ k)
    summary = {
        "profile_id": profile.profile_id,
        "family": profile.family,
        "lapse_a": profile.lapse_a,
        "mix_shape": profile.shape,
        "mix_epsilon": profile.sign * profile.epsilon,
        "status": classify_solution(solution, caustic),
        "solver_success": bool(solution.success),
        "solver_message": str(solution.message),
        "endpoint_reached": bool(len(solution.t_events[0]) > 0),
        "turning_events": [float(x) for x in solution.t_events[1]],
        "first_caustic_affine": caustic,
        "affine_final": affine,
        "endpoint_coordinates": position.tolist(),
        "endpoint_k": k.tolist(),
        "endpoint_screen": E.tolist(),
        "endpoint_D": D.tolist(),
        "endpoint_Ddot": Ddot.tolist(),
        "endpoint_tidal": tidal.tolist(),
        "det_D": float(np.linalg.det(D)),
        "singular_values": singular.tolist(),
        "min_singular_value_sampled_path": min_singular_path,
        "symmetric_D": symmetric.tolist(),
        "antisymmetric_D": antisymmetric.tolist(),
        "antisymmetric_norm": float(np.linalg.norm(antisymmetric)),
        "polar_rotation": rotation,
        "conserved_p_t_endpoint": p_t,
        "conserved_p_psi_endpoint": p_psi,
        "residuals": path_residuals(profile, solution, affine),
        "nfev": int(solution.nfev),
    }
    return summary, state, D


def run_registered_profile(profile: Profile) -> tuple[dict, dict[str, np.ndarray]]:
    production = integrate(profile, PRODUCTION)
    refined = integrate(profile, REFINED)
    second = integrate(profile, SECOND_METHOD)
    summary, _, D = endpoint_summary(profile, production)
    refined_affine, refined_state, refined_D = endpoint_map(profile, refined)
    second_affine, second_state, second_D = endpoint_map(profile, second)
    summary["convergence"] = {
        "production_refined_D_relative": relative_norm(D, refined_D),
        "production_refined_state_relative": relative_norm(np.asarray(production.sol(summary["affine_final"])), refined_state),
        "production_refined_affine_absolute": abs(summary["affine_final"] - refined_affine),
        "refined_second_D_relative": relative_norm(refined_D, second_D),
        "refined_second_state_relative": relative_norm(refined_state, second_state),
        "refined_second_affine_absolute": abs(refined_affine - second_affine),
    }
    if profile.family == "F01" and summary["endpoint_reached"]:
        summary["F01_exact_D_relative"] = relative_norm(D, summary["affine_final"] * np.eye(2))
    sample_s = np.linspace(0.0, summary["affine_final"], 501)
    samples = {"s": sample_s, "state": np.asarray(production.sol(sample_s), dtype=np.float64)}
    return summary, samples


def reflection_check(profile: Profile, positive: dict) -> dict:
    negative_profile = replace(profile, profile_id=profile.profile_id + "__HNEG", sign=-1.0)
    negative = integrate(negative_profile, REFINED)
    negative_affine, negative_state, negative_D = endpoint_map(negative_profile, negative)
    positive_D = np.asarray(positive["endpoint_D"], dtype=np.float64)
    positive_position = np.asarray(positive["endpoint_coordinates"], dtype=np.float64)
    negative_position = negative_state[:4]
    screen_reflection = np.diag([1.0, -1.0])
    coordinate_target = positive_position.copy()
    coordinate_target[3] *= -1.0
    return {
        "negative_endpoint_reached": bool(len(negative.t_events[0]) > 0),
        "affine_absolute": abs(float(positive["affine_final"]) - negative_affine),
        "coordinate_reflection_max_absolute": float(np.max(np.abs(coordinate_target - negative_position))),
        "D_conjugation_relative": relative_norm(negative_D, screen_reflection @ positive_D @ screen_reflection),
    }


def epsilon_limit_checks(profiles: list[Profile], f01_by_a: dict[float, dict]) -> list[dict]:
    rows = []
    for lapse_a in (-0.25, 0.0, 0.25):
        for shape in ("PERSISTENT", "TAPERED", "SIGN_CHANGING"):
            values = []
            for epsilon in (1.0e-2, 5.0e-3):
                auxiliary = Profile(f"EPS_{lapse_a}_{shape}_{epsilon}", "F02", lapse_a, shape, epsilon)
                solution = integrate(auxiliary, REFINED)
                affine, _, D = endpoint_map(auxiliary, solution)
                f01 = f01_by_a[lapse_a]
                values.append(
                    {
                        "epsilon": epsilon,
                        "endpoint_reached": bool(len(solution.t_events[0]) > 0),
                        "affine": affine,
                        "D_error_from_F01": relative_norm(D, np.asarray(f01["endpoint_D"])),
                    }
                )
            e_large = values[0]["D_error_from_F01"]
            e_small = values[1]["D_error_from_F01"]
            rows.append(
                {
                    "lapse_a": lapse_a,
                    "mix_shape": shape,
                    "controls": values,
                    "large_to_small_error_ratio": e_large / max(e_small, 1.0e-300),
                    "nonincrease_or_below_floor": bool(e_small <= e_large or max(e_small, e_large) < 1.0e-10),
                }
            )
    return rows


def main() -> None:
    profiles = load_profiles()
    results = []
    sample_payload: dict[str, np.ndarray] = {}
    stdout_lines: list[str] = []
    for profile in profiles:
        summary, samples = run_registered_profile(profile)
        results.append(summary)
        sample_payload[profile.profile_id + "__s"] = samples["s"]
        sample_payload[profile.profile_id + "__state"] = samples["state"]
        line = f'{profile.profile_id} {summary["status"]} {summary["det_D"]}'
        stdout_lines.append(line)
        print(line, flush=True)

    by_id = {row["profile_id"]: row for row in results}
    reflection = {
        profile.profile_id: reflection_check(profile, by_id[profile.profile_id])
        for profile in profiles
        if profile.family == "F02"
    }
    f01_by_a = {row["lapse_a"]: row for row in results if row["family"] == "F01"}
    epsilon_checks = epsilon_limit_checks(profiles, f01_by_a)

    status_counts: dict[str, int] = {}
    for row in results:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    payload = {
        "schema": "UDT_CMB_G68_FINITE_PATH_JACOBI_V1",
        "profile_rows": len(results),
        "status_counts": status_counts,
        "profiles": results,
        "reflection_checks": reflection,
        "epsilon_limit_checks": epsilon_checks,
        "controls": {
            "R": R_CONTROL,
            "start_x": START_X,
            "endpoint_x": END_X,
            "affine_cap": S_CAP,
            "production": PRODUCTION,
            "refined": REFINED,
            "second_method": SECOND_METHOD,
        },
        "maximum_conclusion": "finite-path classification of the exact 21-row control ensemble only; no physical CMB profile, endpoint, scale, TT power, polarization, local signalling, Xmax value, action, source, bootstrap result, or dynamics",
    }
    (HERE / "FINITE_PATH_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    np.savez_compressed(HERE / "FINITE_PATH_SAMPLES.npz", **sample_payload)
    final_line = json.dumps({"profile_rows": len(results), "status_counts": status_counts}, sort_keys=True)
    stdout_lines.append(final_line)
    (HERE / "DERIVATION_STDOUT.txt").write_text("\n".join(stdout_lines) + "\n", encoding="utf-8")
    print(final_line)


if __name__ == "__main__":
    main()
