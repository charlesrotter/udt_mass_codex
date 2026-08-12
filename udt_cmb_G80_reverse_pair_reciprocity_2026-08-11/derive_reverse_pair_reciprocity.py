#!/usr/bin/env python3
"""Reverse the exact G79 null/Jacobi branch and test ordered-pair reciprocity."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "e5a4a652a62c77d41bb26e7e0d662ebba97fdd41"
ENGINE_PATH = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/solve_finite_path.py"
G79_RESULT = ROOT / "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/DERIVATION_RESULT.json"
STEP_COUNTS = (1024, 2048, 4096)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == len({row["path"] for row in rows}) == 10
    for row in rows:
        path = ROOT / row["path"]
        if path.is_file() and digest(path) == row["sha256"]:
            continue
        frozen = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        assert hashlib.sha256(frozen).hexdigest() == row["sha256"]
    return len(rows)


def load_engine():
    spec = importlib.util.spec_from_file_location("g80_metric_engine", ENGINE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fields(x: float) -> tuple[float, float, float, float, float, float]:
    A = 1.0 - x**2 / 4.0
    A1 = -x / 2.0
    A2 = -0.5
    h = x**6 / 20.0
    h1 = 3.0 * x**5 / 10.0
    h2 = 1.5 * x**4
    return A, A1, A2, h, h1, h2


def observer(position: np.ndarray) -> np.ndarray:
    return np.array([1.0 / math.sqrt(fields(float(position[1]))[0]), 0.0, 0.0, 0.0])


def measured_frequency(engine, profile, position: np.ndarray, k: np.ndarray) -> float:
    g, _, _ = engine.geometry(profile, position)
    return -float(observer(position) @ g @ k)


def reverse_initial(engine, profile, forward_endpoint: np.ndarray, Z: float) -> np.ndarray:
    position, k, E, _, _ = engine.unpack(forward_endpoint)
    return np.concatenate((position, -k / Z, E.ravel(), np.zeros(8), E.ravel()))


def reverse_integrate(engine, profile, state0: np.ndarray, step_count: int) -> object:
    def receiver_event(_affine: float, state: np.ndarray) -> float:
        return float(state[1] - 0.25)

    receiver_event.terminal = True
    receiver_event.direction = -1.0
    return solve_ivp(
        engine.full_rhs(profile),
        (0.0, 10.0),
        state0,
        events=(receiver_event, engine.turning_event),
        dense_output=True,
        method="DOP853",
        rtol=2.0e-13,
        atol=2.0e-15,
        max_step=1.0 / step_count,
    )


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def main() -> None:
    source_rows = verify_sources()
    g79 = json.loads(G79_RESULT.read_text(encoding="utf-8"))
    assert g79["selected_profile"]["profile_id"] == "G75_AM_S01_E05"
    engine = load_engine()
    profile = engine.Profile("G75_AM_S01_E05", "G75_SELECTED", -0.25, "MONOMIAL_S2", 0.05)
    engine.profile_values = lambda _profile, x: fields(float(x))

    forward_by_step: dict[int, tuple[object, np.ndarray, np.ndarray]] = {}
    reverse_by_step: dict[int, tuple[object, np.ndarray, np.ndarray]] = {}
    rows: list[dict[str, float | int]] = []
    for step_count in STEP_COUNTS:
        controls = dict(method="DOP853", rtol=2.0e-13, atol=2.0e-15, max_step=1.0 / step_count)
        forward = engine.integrate(profile, controls)
        assert forward.success and len(forward.t_events[0]) == 1
        forward_affine, forward_endpoint, D_forward = engine.endpoint_map(profile, forward)
        p_s, k_s, _, _, _ = engine.unpack(forward_endpoint)
        Z = measured_frequency(engine, profile, p_s, k_s)
        reverse = reverse_integrate(engine, profile, reverse_initial(engine, profile, forward_endpoint, Z), step_count)
        assert reverse.success and len(reverse.t_events[0]) == 1
        reverse_affine, reverse_endpoint, D_reverse = engine.endpoint_map(profile, reverse)
        forward_by_step[step_count] = (forward, forward_endpoint, D_forward)
        reverse_by_step[step_count] = (reverse, reverse_endpoint, D_reverse)
        rows.append({
            "step_count": step_count,
            "forward_affine": forward_affine,
            "reverse_affine": reverse_affine,
            "Z": Z,
            "D_reciprocity_relative": relative(D_reverse, Z * D_forward.T),
            "dA_forward_over_R": math.sqrt(abs(float(np.linalg.det(D_forward)))),
            "dA_reverse_over_R": math.sqrt(abs(float(np.linalg.det(D_reverse)))),
            "dA_ratio_minus_Z": abs(
                math.sqrt(abs(float(np.linalg.det(D_reverse))))
                / math.sqrt(abs(float(np.linalg.det(D_forward)))) - Z
            ),
        })

    forward, forward_endpoint, D_forward = forward_by_step[4096]
    reverse, reverse_endpoint, D_reverse = reverse_by_step[4096]
    forward_initial = np.asarray(forward.sol(0.0), dtype=np.float64)
    p_r, k_r, E_r, _, _ = engine.unpack(forward_initial)
    p_s, k_s, E_s, _, _ = engine.unpack(forward_endpoint)
    p_back, k_back, E_back, _, _ = engine.unpack(reverse_endpoint)
    Z = measured_frequency(engine, profile, p_s, k_s)
    omega_r_forward = measured_frequency(engine, profile, p_r, k_r)
    reverse_initial_state = reverse_initial(engine, profile, forward_endpoint, Z)
    p_rev_s, k_rev_s, _, _, _ = engine.unpack(reverse_initial_state)
    omega_s_reverse_signed = measured_frequency(engine, profile, p_rev_s, k_rev_s)
    omega_r_reverse_signed = measured_frequency(engine, profile, p_back, k_back)
    inverse_Z = abs(omega_r_reverse_signed) / abs(omega_s_reverse_signed)
    phi_forward = math.log(Z)
    phi_reverse = math.log(inverse_Z)
    g_r, _, _ = engine.geometry(profile, p_r)
    screen_overlap = E_back @ g_r @ E_r.T
    forward_summary, _, _ = engine.endpoint_summary(profile, forward)
    reverse_summary, _, _ = engine.endpoint_summary(profile, reverse)
    D_prediction = Z * D_forward.T
    dA_forward = math.sqrt(abs(float(np.linalg.det(D_forward))))
    dA_reverse = math.sqrt(abs(float(np.linalg.det(D_reverse))))
    gates = {
        "endpoint_return": float(np.max(np.abs(p_back - p_r))) < 1.0e-8,
        "tangent_return": relative(k_back, -k_r / Z) < 1.0e-8,
        "screen_return": relative(E_back, E_r) < 1.0e-8,
        "frequency_reciprocity": abs(Z * inverse_Z - 1.0) < 1.0e-10,
        "phi_oddness": abs(phi_forward + phi_reverse) < 1.0e-10,
        "jacobi_reciprocity": relative(D_reverse, D_prediction) < 1.0e-8,
        "area_reciprocity": abs(dA_reverse / dA_forward - Z) < 1.0e-8,
        "forward_residuals": max(
            forward_summary["residuals"]["null"],
            forward_summary["residuals"]["conserved_p_t"],
            forward_summary["residuals"]["screen_gram"],
            forward_summary["residuals"]["screen_ray"],
        ) < 1.0e-8,
        "reverse_residuals": max(
            reverse_summary["residuals"]["null"],
            reverse_summary["residuals"]["conserved_p_t"],
            reverse_summary["residuals"]["screen_gram"],
            reverse_summary["residuals"]["screen_ray"],
        ) < 1.0e-8,
    }
    output = {
        "schema": "udt-cmb-g80-reverse-pair-reciprocity-v1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "source_rows": source_rows,
        "profile_id": "G75_AM_S01_E05",
        "query_type": "past_directed_mathematical_reversal_of_same_null_curve_not_future_signal",
        "forward": {
            "Z": Z,
            "phi": phi_forward,
            "D": D_forward.tolist(),
            "dA_over_R": dA_forward,
            "affine": float(forward_summary["affine_final"]),
            "residuals": forward_summary["residuals"],
        },
        "reverse": {
            "inverse_Z": inverse_Z,
            "phi": phi_reverse,
            "D": D_reverse.tolist(),
            "dA_over_R": dA_reverse,
            "affine": float(reverse_summary["affine_final"]),
            "source_frequency_signed": omega_s_reverse_signed,
            "receiver_frequency_signed": omega_r_reverse_signed,
            "residuals": reverse_summary["residuals"],
        },
        "reciprocity": {
            "Z_times_inverse_Z_minus_one": abs(Z * inverse_Z - 1.0),
            "phi_sum_absolute": abs(phi_forward + phi_reverse),
            "D_prediction_Z_transpose_forward": D_prediction.tolist(),
            "D_relative": relative(D_reverse, D_prediction),
            "dA_ratio": dA_reverse / dA_forward,
            "dA_ratio_minus_Z": abs(dA_reverse / dA_forward - Z),
            "endpoint_return_max_absolute": float(np.max(np.abs(p_back - p_r))),
            "tangent_return_relative": relative(k_back, -k_r / Z),
            "screen_return_relative": relative(E_back, E_r),
            "screen_overlap": screen_overlap.tolist(),
        },
        "refinement": rows,
        "gates": gates,
        "authority": {
            "maximum_conclusion": "DERIVED_CONDITIONAL_RECIPROCITY_ON_ONE_FROZEN_GEOMETRY_AND_ONE_ORDERED_PAIR",
            "past_directed_reversal_only": True,
            "future_signal_derived": False,
            "physical_profile_or_endpoint_selected": False,
            "Xmax_identified": False,
            "cmb_temp_activated": False,
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (HERE / "REFINEMENT_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    reverse_grid = np.linspace(0.0, float(reverse_summary["affine_final"]), 501)
    np.savez_compressed(
        HERE / "REVERSE_PATH_EVIDENCE.npz",
        affine=reverse_grid,
        state=np.asarray(reverse.sol(reverse_grid), dtype=np.float64),
        D_forward=D_forward,
        D_reverse=D_reverse,
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    assert all(gates.values()), gates


if __name__ == "__main__":
    main()
