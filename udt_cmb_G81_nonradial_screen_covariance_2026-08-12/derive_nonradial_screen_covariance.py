#!/usr/bin/env python3
"""Run the preregistered G81 full-Jacobi screen-covariance controls."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "f112a32e4fbc5319de4e964e869f9024e9bdb1b9"
ENGINE_PATH = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/solve_finite_path.py"
STEP_COUNTS = (1024, 2048, 4096)  # NUMERIC: preregistered refinement ladder.
A_ROT = np.array([[3.0 / 5.0, -4.0 / 5.0], [4.0 / 5.0, 3.0 / 5.0]])  # CHOSE_CONTROL.
B_ROT = np.array([[5.0 / 13.0, -12.0 / 13.0], [12.0 / 13.0, 5.0 / 13.0]])  # CHOSE_CONTROL.


@dataclass(frozen=True)
class Control:
    control_id: str
    direction: tuple[float, float, float]
    screen1: tuple[float, float, float]
    screen2: tuple[float, float, float]


CONTROLS = (
    Control("C0_RADIAL_ROTATED", (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
    Control(
        "C1_FULL_ANGULAR",
        (12.0 / 13.0, 3.0 / 13.0, 4.0 / 13.0),
        (0.0, 4.0 / 5.0, -3.0 / 5.0),
        (-5.0 / 13.0, 36.0 / 65.0, 48.0 / 65.0),
    ),
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_preregistered_inputs() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == len({row["path"] for row in rows}) == 9
    for row in rows:
        frozen = subprocess.check_output(["git", "show", f"{row['base_commit']}:{row['path']}"], cwd=ROOT)
        assert digest(frozen) == row["sha256"]
        assert row["base_commit"] == BASE
    with (HERE / "CONTROL_UNIVERSE.tsv").open(newline="", encoding="utf-8") as stream:
        controls = list(csv.DictReader(stream, delimiter="\t"))
    assert [row["control_id"] for row in controls] == [control.control_id for control in CONTROLS]
    assert len(controls) == 2
    return len(rows)


def load_engine():
    spec = importlib.util.spec_from_file_location("g81_metric_engine", ENGINE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fields(x: float) -> tuple[float, float, float, float, float, float]:
    return 1.0 - x**2 / 4.0, -x / 2.0, -0.5, x**6 / 20.0, 3.0 * x**5 / 10.0, 1.5 * x**4


def observer(engine, profile, position: np.ndarray) -> np.ndarray:
    g, _, _ = engine.geometry(profile, position)
    return np.array([1.0 / math.sqrt(-float(g[0, 0])), 0.0, 0.0, 0.0])


def frequency(engine, profile, position: np.ndarray, tangent: np.ndarray) -> float:
    g, _, _ = engine.geometry(profile, position)
    return -float(observer(engine, profile, position) @ g @ tangent)


def receiver_frame(engine, profile) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    position = np.array([0.0, 0.25, math.pi / 2.0, 0.0], dtype=np.float64)  # CHOSE_CONTROL.
    A, _, _, h, _, _ = fields(0.25)
    block = A * 0.25**2 + h**2
    u = observer(engine, profile, position)
    radial = np.array([0.0, math.sqrt(A), 0.0, 0.0])
    theta = np.array([0.0, 0.0, 4.0, 0.0])
    psi = np.array([h / (math.sqrt(A) * math.sqrt(block)), 0.0, 0.0, math.sqrt(A) / math.sqrt(block)])
    triad = np.stack((radial, theta, psi))
    g, _, _ = engine.geometry(profile, position)
    assert np.max(np.abs(triad @ g @ triad.T - np.eye(3))) < 1.0e-13
    assert np.max(np.abs(triad @ g @ u)) < 1.0e-13
    return position, u, triad


def initial_state(engine, profile, control: Control) -> np.ndarray:
    position, u, triad = receiver_frame(engine, profile)
    n = np.asarray(control.direction) @ triad
    E = np.stack((np.asarray(control.screen1) @ triad, np.asarray(control.screen2) @ triad))
    k = u + n
    g, _, _ = engine.geometry(profile, position)
    assert abs(float(k @ g @ k)) < 1.0e-13
    assert abs(frequency(engine, profile, position, k) - 1.0) < 1.0e-13
    assert np.max(np.abs(E @ g @ E.T - np.eye(2))) < 1.0e-13
    assert np.max(np.abs(E @ g @ k)) < 1.0e-13
    J = np.zeros((2, 4), dtype=np.float64)
    P = E.copy()
    return np.concatenate((position, k, E.ravel(), J.ravel(), P.ravel()))


def integrate(engine, profile, state0: np.ndarray, step_count: int, target_x: float, direction: float) -> object:
    def endpoint_event(_affine: float, state: np.ndarray) -> float:
        return float(state[1] - target_x)

    endpoint_event.terminal = True
    endpoint_event.direction = direction
    return solve_ivp(
        engine.full_rhs(profile),
        (0.0, 10.0),  # NUMERIC: preregistered inherited affine cap.
        state0,
        events=(endpoint_event, engine.turning_event),
        dense_output=True,
        method="DOP853",
        rtol=2.0e-13,
        atol=2.0e-15,
        max_step=1.0 / step_count,
    )


def reverse_state(engine, forward_endpoint: np.ndarray, Z: float, rotation: np.ndarray) -> np.ndarray:
    position, k, E, _, _ = engine.unpack(forward_endpoint)
    E_rot = rotation @ E
    return np.concatenate((position, -k / Z, E_rot.ravel(), np.zeros(8), E_rot.ravel()))


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def endpoint(engine, profile, solution: object) -> tuple[float, np.ndarray, np.ndarray]:
    affine = float(solution.t_events[0][0])
    state = np.asarray(solution.sol(affine), dtype=np.float64)
    D, _, _, _ = engine.screen_objects(profile, state)
    return affine, state, D


def run_control(engine, profile, control: Control, source_rows: int) -> tuple[dict, list[dict], dict[str, np.ndarray]]:
    refinement: list[dict] = []
    finest: dict | None = None
    evidence: dict[str, np.ndarray] = {}
    for step_count in STEP_COUNTS:
        forward = integrate(engine, profile, initial_state(engine, profile, control), step_count, 1.0, 1.0)
        if not forward.success or len(forward.t_events[0]) != 1:
            refinement.append({
                "control_id": control.control_id,
                "step_count": step_count,
                "status": "NO_REGISTERED_FORWARD_CROSSING",
                "forward_affine": float(forward.t[-1]),
            })
            if step_count == STEP_COUNTS[-1]:
                finest = {
                    "control_id": control.control_id,
                    "status": "NO_REGISTERED_FORWARD_CROSSING",
                    "solver_success": bool(forward.success),
                    "turning_events": [float(value) for value in forward.t_events[1]],
                    "source_rows": source_rows,
                }
            continue

        forward_affine, forward_endpoint, D_forward = endpoint(engine, profile, forward)
        p_r, k_r, E_r, _, _ = engine.unpack(np.asarray(forward.sol(0.0), dtype=np.float64))
        p_s, k_s, E_s, _, _ = engine.unpack(forward_endpoint)
        Z = frequency(engine, profile, p_s, k_s)
        reverse_unrot = integrate(
            engine, profile, reverse_state(engine, forward_endpoint, Z, np.eye(2)), step_count, 0.25, -1.0
        )
        reverse_rot = integrate(
            engine, profile, reverse_state(engine, forward_endpoint, Z, A_ROT), step_count, 0.25, -1.0
        )
        if any(not item.success or len(item.t_events[0]) != 1 for item in (reverse_unrot, reverse_rot)):
            refinement.append({
                "control_id": control.control_id,
                "step_count": step_count,
                "status": "NO_REGISTERED_REVERSE_CROSSING",
                "forward_affine": forward_affine,
            })
            if step_count == STEP_COUNTS[-1]:
                finest = {
                    "control_id": control.control_id,
                    "status": "NO_REGISTERED_REVERSE_CROSSING",
                    "source_rows": source_rows,
                }
            continue

        reverse_affine, reverse_endpoint, D_reverse = endpoint(engine, profile, reverse_unrot)
        reverse_rot_affine, reverse_rot_endpoint, _ = endpoint(engine, profile, reverse_rot)
        p_back, k_back, E_back, _, _ = engine.unpack(reverse_endpoint)
        p_back_rot, _, E_back_rot, J_back_rot, _ = engine.unpack(reverse_rot_endpoint)
        g_back, _, _ = engine.geometry(profile, p_back_rot)
        D_reverse_AB = (B_ROT @ E_r) @ g_back @ J_back_rot.T
        D_prediction = Z * D_forward.T
        D_prediction_AB = Z * B_ROT @ D_forward.T @ A_ROT.T
        inverse_Z = abs(frequency(engine, profile, p_back, k_back))
        dA_forward = math.sqrt(abs(float(np.linalg.det(D_forward))))
        dA_reverse = math.sqrt(abs(float(np.linalg.det(D_reverse))))
        row = {
            "control_id": control.control_id,
            "step_count": step_count,
            "status": "CROSSED",
            "forward_affine": forward_affine,
            "reverse_affine": reverse_affine,
            "Z": Z,
            "unrotated_D_relative": relative(D_reverse, D_prediction),
            "rotated_D_relative": relative(D_reverse_AB, D_prediction_AB),
            "area_ratio_minus_Z": abs(dA_reverse / dA_forward - Z),
            "forward_offdiagonal_norm": float(np.linalg.norm(D_forward - np.diag(np.diag(D_forward)))),
        }
        refinement.append(row)

        if step_count == STEP_COUNTS[-1]:
            forward_summary, _, _ = engine.endpoint_summary(profile, forward)
            reverse_summary, _, _ = engine.endpoint_summary(profile, reverse_unrot)
            reverse_rot_summary, _, _ = engine.endpoint_summary(profile, reverse_rot)
            screen_unrot_overlap = E_back @ g_back @ E_r.T
            screen_rot_overlap = E_back_rot @ g_back @ E_r.T
            gates = {
                "forward_endpoint": len(forward.t_events[0]) == 1,
                "reverse_endpoints": len(reverse_unrot.t_events[0]) == len(reverse_rot.t_events[0]) == 1,
                "endpoint_return": max(
                    float(np.max(np.abs(p_back - p_r))), float(np.max(np.abs(p_back_rot - p_r)))
                ) < 1.0e-8,
                "tangent_return": relative(k_back, -k_r / Z) < 1.0e-8,
                "screen_return_unrotated": relative(E_back, E_r) < 1.0e-8,
                "screen_return_rotated": relative(E_back_rot, A_ROT @ E_r) < 1.0e-8,
                "frequency_reciprocity": abs(Z * inverse_Z - 1.0) < 1.0e-10,
                "phi_oddness": abs(math.log(Z) + math.log(inverse_Z)) < 1.0e-10,
                "unrotated_matrix_reciprocity": relative(D_reverse, D_prediction) < 1.0e-8,
                "rotated_matrix_covariance": relative(D_reverse_AB, D_prediction_AB) < 1.0e-8,
                "area_reciprocity": abs(dA_reverse / dA_forward - Z) < 1.0e-8,
                "no_forward_caustic": forward_summary["first_caustic_affine"] is None,
                "path_residuals": max(
                    *(
                        summary["residuals"][key]
                        for summary in (forward_summary, reverse_summary, reverse_rot_summary)
                        for key in ("null", "conserved_p_t", "conserved_p_psi", "screen_gram", "screen_ray", "wronskian")
                    )
                ) < 1.0e-8,
            }
            finest = {
                "control_id": control.control_id,
                "status": "PASS" if all(gates.values()) else "FAIL",
                "source_rows": source_rows,
                "direction": list(control.direction),
                "forward": {
                    "affine": forward_affine,
                    "endpoint": p_s.tolist(),
                    "Z": Z,
                    "phi": math.log(Z),
                    "D": D_forward.tolist(),
                    "dA_over_R": dA_forward,
                    "offdiagonal_norm": row["forward_offdiagonal_norm"],
                    "summary": forward_summary,
                },
                "reverse_unrotated": {
                    "affine": reverse_affine,
                    "inverse_Z": inverse_Z,
                    "phi": math.log(inverse_Z),
                    "D": D_reverse.tolist(),
                    "prediction": D_prediction.tolist(),
                    "D_relative": row["unrotated_D_relative"],
                    "dA_over_R": dA_reverse,
                    "area_ratio_minus_Z": row["area_ratio_minus_Z"],
                    "summary": reverse_summary,
                },
                "reverse_rotated": {
                    "affine": reverse_rot_affine,
                    "A": A_ROT.tolist(),
                    "B": B_ROT.tolist(),
                    "D": D_reverse_AB.tolist(),
                    "prediction": D_prediction_AB.tolist(),
                    "D_relative": row["rotated_D_relative"],
                    "transported_screen_overlap_with_receiver": screen_rot_overlap.tolist(),
                    "summary": reverse_rot_summary,
                },
                "reciprocity": {
                    "frequency_product_error": abs(Z * inverse_Z - 1.0),
                    "phi_sum_absolute": abs(math.log(Z) + math.log(inverse_Z)),
                    "endpoint_return_max_absolute": max(
                        float(np.max(np.abs(p_back - p_r))), float(np.max(np.abs(p_back_rot - p_r)))
                    ),
                    "tangent_return_relative": relative(k_back, -k_r / Z),
                    "screen_return_unrotated_relative": relative(E_back, E_r),
                    "screen_return_rotated_relative": relative(E_back_rot, A_ROT @ E_r),
                    "screen_unrotated_overlap": screen_unrot_overlap.tolist(),
                },
                "gates": gates,
            }
            grid_f = np.linspace(0.0, forward_affine, 501)
            grid_r = np.linspace(0.0, reverse_affine, 501)
            evidence = {
                "forward_affine": grid_f,
                "forward_state": np.asarray(forward.sol(grid_f), dtype=np.float64),
                "reverse_affine": grid_r,
                "reverse_unrotated_state": np.asarray(reverse_unrot.sol(grid_r), dtype=np.float64),
                "reverse_rotated_state": np.asarray(reverse_rot.sol(grid_r), dtype=np.float64),
                "D_forward": D_forward,
                "D_reverse": D_reverse,
                "D_reverse_AB": D_reverse_AB,
            }
    assert finest is not None
    return finest, refinement, evidence


def main() -> None:
    source_rows = verify_preregistered_inputs()
    engine = load_engine()
    profile = engine.Profile("G75_AM_S01_E05", "G75_SELECTED", -0.25, "MONOMIAL_S2", 0.05)
    engine.profile_values = lambda _profile, x: fields(float(x))
    results, refinement, evidence = [], [], {}
    for control in CONTROLS:
        result, rows, arrays = run_control(engine, profile, control, source_rows)
        results.append(result)
        refinement.extend(rows)
        for key, value in arrays.items():
            evidence[f"{control.control_id}__{key}"] = value
    both_pass = len(results) == 2 and all(row["status"] == "PASS" for row in results)
    output = {
        "schema": "udt-cmb-g81-nonradial-screen-covariance-v1",
        "status": "PASS" if both_pass else "PARTIAL_OR_FAIL",
        "source_rows": source_rows,
        "control_count": len(results),
        "profile_id": "G75_AM_S01_E05",
        "controls": results,
        "authority": {
            "maximum_conclusion": (
                "DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS"
                if both_pass else "CONTROL_SCOPED_OUTCOME_ONLY"
            ),
            "generic_geometric_reciprocity_not_UDT_selector": True,
            "past_directed_reversal_only": True,
            "future_signal_derived": False,
            "physical_profile_endpoint_scale_source_or_observable_selected": False,
            "Xmax_identified": False,
            "cmb_temp_activated": False,
        },
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    (HERE / "DERIVATION_RESULT.json").write_text(rendered, encoding="utf-8")
    keys = sorted({key for row in refinement for key in row})
    with (HERE / "REFINEMENT_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=keys, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(refinement)
    np.savez_compressed(HERE / "PATH_EVIDENCE.npz", **evidence)
    (HERE / "DERIVATION_STDOUT.txt").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if all(row["status"] != "PASS" for row in results):
        raise SystemExit("neither preregistered control passed")


if __name__ == "__main__":
    main()
