#!/usr/bin/env python3
"""Derive the preregistered G83 stationary endpoint-asymptote candidate atlas."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import sys
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROFILE_PATH = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv"
ENGINE_PATH = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/solve_finite_path.py"
RECEIVER_X = 0.25
RECENTER_X = (0.25, 0.5, 0.75, 1.0)
APPROACH_POWERS = (4, 8, 12)
CONTROLS = dict(method="DOP853", rtol=1.0e-10, atol=1.0e-12, max_step=1.0 / 400.0)
AFFINE_CAP = 20.0
RESIDUAL_TOLERANCE = 1.0e-7
S = sp.symbols("s", real=True)


@dataclass(frozen=True)
class G75Profile:
    profile_id: str
    lapse_name: str
    lapse_a: float
    shape_id: str
    amplitude: float
    q_text: str
    q_coefficients: tuple[float, ...]
    behavior_class: str


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file(), path
        assert digest(path) == row["sha256"], path
    return len(rows)


def parse_fraction(text: str) -> float:
    return float(Fraction(text))


def parse_q(text: str) -> tuple[float, ...]:
    poly = sp.Poly(sp.sympify(text, locals={"s": S}), S)
    if poly.is_zero:
        return (0.0,)
    degree = max(0, int(poly.degree()))
    return tuple(float(poly.nth(index)) for index in range(degree + 1))


def load_profiles() -> list[G75Profile]:
    with PROFILE_PATH.open(newline="", encoding="utf-8") as stream:
        raw = list(csv.DictReader(stream, delimiter="\t"))
    profiles = [
        G75Profile(
            profile_id=row["profile_id"],
            lapse_name=row["lapse_name"],
            lapse_a=parse_fraction(row["lapse_a"]),
            shape_id=row["shape_id"],
            amplitude=parse_fraction(row["amplitude"]),
            q_text=row["q_of_s"],
            q_coefficients=parse_q(row["q_of_s"]),
            behavior_class=row["behavior_class"],
        )
        for row in raw
    ]
    assert len(profiles) == 591
    assert len({profile.profile_id for profile in profiles}) == 591
    assert sum(profile.lapse_name == "AM" for profile in profiles) == 197
    return profiles


def polynomial_triplet(coefficients: tuple[float, ...], value: float) -> tuple[float, float, float]:
    q = sum(coefficient * value**index for index, coefficient in enumerate(coefficients))
    q1 = sum(index * coefficient * value ** (index - 1) for index, coefficient in enumerate(coefficients) if index)
    q2 = sum(
        index * (index - 1) * coefficient * value ** (index - 2)
        for index, coefficient in enumerate(coefficients)
        if index >= 2
    )
    return q, q1, q2


def metric_profile_values(profile: G75Profile, x: float) -> tuple[float, float, float, float, float, float]:
    a = profile.lapse_a
    A = 1.0 + a * x * x
    A1 = 2.0 * a * x
    A2 = 2.0 * a
    s = x * x
    q, q1, q2 = polynomial_triplet(profile.q_coefficients, s)
    h = s * q
    h1 = 2.0 * x * (q + s * q1)
    h2 = 2.0 * q + 10.0 * s * q1 + 4.0 * s * s * q2
    return A, A1, A2, h, h1, h2


def import_engine():
    spec = importlib.util.spec_from_file_location("g83_g68_engine", ENGINE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def strict_domain_rows(profiles: list[G75Profile]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for profile in profiles:
        minimum = min(1.0, 1.0 + profile.lapse_a)
        receiver_A = 1.0 + profile.lapse_a * RECEIVER_X**2
        source_A = 1.0 + profile.lapse_a
        phi = 0.5 * math.log(receiver_A / source_A)
        rows.append(
            {
                "profile_id": profile.profile_id,
                "lapse_name": profile.lapse_name,
                "min_A_on_0_1": f"{minimum:.17g}",
                "A_receiver_x_1_4": f"{receiver_A:.17g}",
                "A_control_endpoint_x_1": f"{source_A:.17g}",
                "phi_receiver_to_x_1": f"{phi:.17g}",
                "finite_positive_lapse": str(minimum > 0.0).lower(),
                "strict_domain_asymptote_status": "NO_INFINITE_STATIONARY_DEPTH_ON_REGISTERED_DOMAIN",
            }
        )
    return rows


def family_rows() -> list[dict[str, object]]:
    return [
        {
            "lapse_name": "AM",
            "A_of_x": "1-x^2/4",
            "positive_lapse_zero": "2",
            "continued_stationary_status": "FINITE_X_KILLING_LAPSE_ZERO_CANDIDATE",
            "physical_status": "NOT_IDENTIFIED_WITH_X_MAX",
        },
        {
            "lapse_name": "A0",
            "A_of_x": "1",
            "positive_lapse_zero": "-",
            "continued_stationary_status": "NO_POSITIVE_LAPSE_ZERO",
            "physical_status": "OTHER_GLOBAL_REALIZATIONS_NOT_EXCLUDED",
        },
        {
            "lapse_name": "AP",
            "A_of_x": "1+x^2/4",
            "positive_lapse_zero": "-",
            "continued_stationary_status": "NO_POSITIVE_LAPSE_ZERO",
            "physical_status": "OTHER_GLOBAL_REALIZATIONS_NOT_EXCLUDED",
        },
    ]


def recenter_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for receiver in RECENTER_X:
        A_r = 1.0 - receiver**2 / 4.0
        proper_limit = 2.0 * (math.pi / 2.0 - math.asin(receiver / 2.0))
        for power in APPROACH_POWERS:
            A_s = 2.0 ** (-power)
            source = 2.0 * math.sqrt(1.0 - A_s)
            phi = 0.5 * math.log(A_r / A_s)
            c_ratio = A_s / A_r
            proper = 2.0 * (math.asin(source / 2.0) - math.asin(receiver / 2.0))
            rows.append(
                {
                    "receiver_x": f"{receiver:.17g}",
                    "approach_power": power,
                    "A_source": f"{A_s:.17g}",
                    "source_x": f"{source:.17g}",
                    "phi_pair": f"{phi:.17g}",
                    "c_eff_source_over_receiver": f"{c_ratio:.17g}",
                    "proper_length_over_R": f"{proper:.17g}",
                    "proper_limit_over_R": f"{proper_limit:.17g}",
                    "proper_gap_to_limit_over_R": f"{proper_limit-proper:.17g}",
                    "ownership": "FREE_AND_EXPLORED_CONTINUATION_NOT_X_MAX",
                }
            )
    return rows


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    assert rows
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def make_engine_profile(engine, profile: G75Profile):
    return engine.Profile(profile.profile_id, "G83", profile.lapse_a, profile.shape_id, profile.amplitude)


def endpoint_event_factory(target: float):
    def event(_affine: float, state: np.ndarray) -> float:
        return float(state[1] - target)
    event.terminal = True
    event.direction = 1.0
    return event


def finite_path_diagnostics(engine, profile: G75Profile, solution: object, final_s: float) -> dict[str, object]:
    sample_grid = np.linspace(0.0, final_s, 101)
    det_values: list[float] = []
    minimum_singular = math.inf
    maxima = {key: 0.0 for key in ("null", "screen_gram", "screen_ray", "conserved_p_t", "conserved_p_psi")}
    first_state = np.asarray(solution.sol(0.0), dtype=np.float64)
    initial_position, initial_k, _, _, _ = engine.unpack(first_state)
    initial_g, _, _ = engine.geometry(make_engine_profile(engine, profile), initial_position)
    initial_pt = float(initial_g[0] @ initial_k)
    initial_ppsi = float(initial_g[3] @ initial_k)
    last_D = None
    for affine in sample_grid:
        state = np.asarray(solution.sol(float(affine)), dtype=np.float64)
        position, k, E, _, _ = engine.unpack(state)
        D, _, _, g = engine.screen_objects(make_engine_profile(engine, profile), state)
        last_D = D
        det_values.append(float(np.linalg.det(D)))
        minimum_singular = min(minimum_singular, float(np.linalg.svd(D, compute_uv=False)[-1]))
        maxima["null"] = max(maxima["null"], abs(float(k @ g @ k)) / max(1.0, np.linalg.norm(k) ** 2 * np.linalg.norm(g)))
        maxima["screen_gram"] = max(maxima["screen_gram"], float(np.max(np.abs(E @ g @ E.T - np.eye(2)))))
        maxima["screen_ray"] = max(maxima["screen_ray"], float(np.max(np.abs(E @ g @ k))))
        maxima["conserved_p_t"] = max(maxima["conserved_p_t"], abs(float(g[0] @ k) - initial_pt))
        maxima["conserved_p_psi"] = max(maxima["conserved_p_psi"], abs(float(g[3] @ k) - initial_ppsi))
    caustic = any(left * right < 0.0 for left, right in zip(det_values, det_values[1:]))
    assert last_D is not None
    return {
        "caustic_sign_change_sampled": caustic,
        "minimum_D_singular_value_sampled": float(minimum_singular),
        "endpoint_det_D": float(np.linalg.det(last_D)),
        "residuals": {key: float(value) for key, value in maxima.items()},
    }


def classify(solution: object, endpoint_reached: bool, caustic: bool, finite: bool) -> str:
    if not finite:
        return "NUMERIC_NONFINITE_OR_SIGNATURE_FAILURE"
    if not solution.success:
        return "SOLVER_FAILURE"
    if endpoint_reached and caustic:
        return "ENDPOINT_AFTER_CAUSTIC"
    if endpoint_reached:
        return "ENDPOINT_REGULAR_NO_CAUSTIC"
    if len(solution.t_events[1]) > 0:
        return "TURNING_NO_ENDPOINT"
    return "AFFINE_CAP_NO_ENDPOINT"


def run_path_atlas(engine, profiles: list[G75Profile]) -> list[dict[str, object]]:
    by_id = {profile.profile_id: profile for profile in profiles}

    def patched_profile_values(engine_profile, x: float):
        return metric_profile_values(by_id[engine_profile.profile_id], x)

    engine.profile_values = patched_profile_values
    engine.START_X = RECEIVER_X
    engine.S_CAP = AFFINE_CAP
    rows: list[dict[str, object]] = []
    am_profiles = [profile for profile in profiles if profile.lapse_name == "AM"]
    for profile_index, profile in enumerate(am_profiles, 1):
        engine_profile = make_engine_profile(engine, profile)
        for power in APPROACH_POWERS:
            A_s = 2.0 ** (-power)
            target = 2.0 * math.sqrt(1.0 - A_s)
            event = endpoint_event_factory(target)
            try:
                solution = solve_ivp(
                    engine.full_rhs(engine_profile),
                    (0.0, AFFINE_CAP),
                    engine.initial_state(engine_profile),
                    events=(event, engine.turning_event),
                    dense_output=True,
                    **CONTROLS,
                )
                endpoint_reached = len(solution.t_events[0]) > 0
                final_s = float(solution.t_events[0][0]) if endpoint_reached else float(solution.t[-1])
                final_state = np.asarray(solution.sol(final_s), dtype=np.float64)
                finite = bool(np.all(np.isfinite(final_state)))
                diagnostics = finite_path_diagnostics(engine, profile, solution, final_s) if finite else {
                    "caustic_sign_change_sampled": False,
                    "minimum_D_singular_value_sampled": math.nan,
                    "endpoint_det_D": math.nan,
                    "residuals": {key: math.inf for key in ("null", "screen_gram", "screen_ray", "conserved_p_t", "conserved_p_psi")},
                }
                status = classify(solution, endpoint_reached, bool(diagnostics["caustic_sign_change_sampled"]), finite)
                certified = bool(
                    endpoint_reached
                    and finite
                    and all(float(value) <= RESIDUAL_TOLERANCE for value in diagnostics["residuals"].values())
                )
                rows.append(
                    {
                        "profile_id": profile.profile_id,
                        "shape_id": profile.shape_id,
                        "behavior_class": profile.behavior_class,
                        "amplitude": f"{profile.amplitude:.17g}",
                        "approach_power": power,
                        "A_source": f"{A_s:.17g}",
                        "source_x": f"{target:.17g}",
                        "status": status,
                        "endpoint_reached": endpoint_reached,
                        "numerically_certified": certified,
                        "affine_final": f"{final_s:.17g}",
                        "endpoint_x_observed": f"{final_state[1]:.17g}" if finite else "nan",
                        "endpoint_det_D": f"{float(diagnostics['endpoint_det_D']):.17g}",
                        "minimum_D_singular_value_sampled": f"{float(diagnostics['minimum_D_singular_value_sampled']):.17g}",
                        "caustic_sign_change_sampled": diagnostics["caustic_sign_change_sampled"],
                        "null_residual": f"{diagnostics['residuals']['null']:.17g}",
                        "screen_gram_residual": f"{diagnostics['residuals']['screen_gram']:.17g}",
                        "screen_ray_residual": f"{diagnostics['residuals']['screen_ray']:.17g}",
                        "p_t_residual": f"{diagnostics['residuals']['conserved_p_t']:.17g}",
                        "p_psi_residual": f"{diagnostics['residuals']['conserved_p_psi']:.17g}",
                        "nfev": int(solution.nfev),
                    }
                )
            except (FloatingPointError, np.linalg.LinAlgError, ValueError) as error:
                rows.append(
                    {
                        "profile_id": profile.profile_id,
                        "shape_id": profile.shape_id,
                        "behavior_class": profile.behavior_class,
                        "amplitude": f"{profile.amplitude:.17g}",
                        "approach_power": power,
                        "A_source": f"{A_s:.17g}",
                        "source_x": f"{target:.17g}",
                        "status": "NUMERIC_NONFINITE_OR_SIGNATURE_FAILURE",
                        "endpoint_reached": False,
                        "numerically_certified": False,
                        "affine_final": "nan",
                        "endpoint_x_observed": "nan",
                        "endpoint_det_D": "nan",
                        "minimum_D_singular_value_sampled": "nan",
                        "caustic_sign_change_sampled": False,
                        "null_residual": "inf",
                        "screen_gram_residual": "inf",
                        "screen_ray_residual": "inf",
                        "p_t_residual": "inf",
                        "p_psi_residual": "inf",
                        "nfev": 0,
                        "error_type": type(error).__name__,
                    }
                )
        print(f"{profile_index}/197 {profile.profile_id}", flush=True)
    assert len(rows) == 591
    assert len({(row["profile_id"], row["approach_power"]) for row in rows}) == 591
    return rows


def main() -> None:
    source_count = verify_sources()
    profiles = load_profiles()
    strict = strict_domain_rows(profiles)
    families = family_rows()
    recenter = recenter_rows()
    write_tsv(HERE / "STRICT_DOMAIN_ATLAS.tsv", strict)
    write_tsv(HERE / "LAPSE_FAMILY_CONTINUATION.tsv", families)
    write_tsv(HERE / "RECENTERED_ENDPOINT_LIMIT_ATLAS.tsv", recenter)

    engine = import_engine()
    paths = run_path_atlas(engine, profiles)
    write_tsv(HERE / "CONTINUED_PATH_ATLAS.tsv", paths)
    status_counts = Counter(str(row["status"]) for row in paths)
    certified_counts = Counter(str(row["numerically_certified"]).lower() for row in paths)
    payload = {
        "schema": "UDT_CMB_G83_STATIONARY_ENDPOINT_ASYMPTOTE_ATLAS_V1",
        "source_count": source_count,
        "strict_profile_rows": len(strict),
        "AM_profile_rows": 197,
        "continued_path_rows": len(paths),
        "status_counts": dict(sorted(status_counts.items())),
        "certified_counts": dict(sorted(certified_counts.items())),
        "strict_domain_positive_finite": all(row["finite_positive_lapse"] == "true" for row in strict),
        "receiver_rows": len(recenter),
        "controls": {
            "receiver_x": RECEIVER_X,
            "recenter_x": RECENTER_X,
            "approach_powers": APPROACH_POWERS,
            "affine_cap": AFFINE_CAP,
            "integrator": CONTROLS,
            "residual_tolerance": RESIDUAL_TOLERANCE,
        },
        "maximum_conclusion": "BOUNDED_STATIONARY_ENDPOINT_ASYMPTOTE_CANDIDATE_ATLAS; no physical profile, R, source surface, separation operator, X_max, CMB field, action, matter source, bootstrap closure, or time-live dynamics selected",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
