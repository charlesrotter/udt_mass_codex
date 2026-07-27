#!/usr/bin/env python3
"""CPU transport/Jacobi atlas over the preregistered 36-path universe."""

from __future__ import annotations

import csv
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp

import transport_geometry as geometry

HERE = Path(__file__).resolve().parent
OMEGA = np.block([[np.zeros((2, 2)), np.eye(2)], [-np.eye(2), np.zeros((2, 2))]])
LENGTH = 0.25
CHECKPOINTS = (0.0625, 0.125, 0.1875, 0.25)


def unpack(state: np.ndarray):
    x = state[0:4]
    tangent = state[4:8]
    transported = state[8:24].reshape(4, 4)
    jacobi = state[24:40].reshape(4, 4)
    return x, tangent, transported, jacobi


def pack(x, tangent, transported, jacobi):
    return np.concatenate((x, tangent, transported.reshape(-1), jacobi.reshape(-1)))


def initial_state(event: np.ndarray, direction: str) -> np.ndarray:
    x = np.concatenate(([0.0], event))
    tangent = np.array((1.0, 1.0 if direction == "plus" else -1.0, 0.0, 0.0))
    return pack(x, tangent, np.eye(4), np.eye(4))


def rhs(_affine: float, state: np.ndarray, lambda_value: float) -> np.ndarray:
    x, tangent, transported, jacobi = unpack(state)
    riemann, connection, frame, _phi = geometry.curvature_frame(x[1:], lambda_value)
    dx = frame @ tangent
    dtangent = -np.einsum("abc,b,c->a", connection, tangent, tangent)
    dtransported = -np.einsum("abc,b,cj->aj", connection, tangent, transported)
    optical = geometry.optical_curvature(riemann, tangent, transported)
    generator = np.block([[np.zeros((2, 2)), np.eye(2)], [optical, np.zeros((2, 2))]])
    djacobi = generator @ jacobi
    return pack(dx, dtangent, dtransported, djacobi)


def integrate(state: np.ndarray, lambda_value: float, duration: float, *, tight: bool = False):
    if tight:
        rtol, atol, max_step = 2.0e-10, 2.0e-12, 1.0 / 128.0
    else:
        rtol, atol, max_step = 1.0e-9, 1.0e-11, 1.0 / 64.0
    solution = solve_ivp(
        lambda affine, values: rhs(affine, values, lambda_value), (0.0, duration), state,
        method="DOP853", rtol=rtol, atol=atol, max_step=max_step, dense_output=True,
    )
    assert solution.success, solution.message
    return solution


def initial_anchor(event: np.ndarray, direction: str, lambda_value: float) -> dict[str, float]:
    _phi, dphi, _coframe, frame = geometry.coframe_data(event, lambda_value)
    p = frame[1:, :].T @ dphi
    state = initial_state(event, direction)
    derivative = rhs(0.0, state, lambda_value)
    tangent_derivative = derivative[4:8]
    expected = np.array((2.0 * p[2], 2.0 * p[3]))
    return {
        "E1phi": float(p[1]), "E2phi": float(p[2]), "E3phi": float(p[3]),
        "dv2": float(tangent_derivative[2]), "dv3": float(tangent_derivative[3]),
        "anchor_error": float(np.max(np.abs(tangent_derivative[2:4] - expected))),
    }


def checkpoint_row(path_id: str, event_id: str, direction: str, lambda_value: float,
                   affine: float, state: np.ndarray, initial_phi: float,
                   initial_energy: float) -> dict[str, object]:
    x, tangent, transported, jacobi = unpack(state)
    diagnostics = geometry.state_diagnostics(x, tangent, transported, jacobi, lambda_value)
    riemann = geometry.curvature_frame(x[1:], lambda_value)[0]
    optical = geometry.optical_curvature(riemann, tangent, transported)
    curvature_asymmetry = float(np.max(np.abs(optical - optical.T)))
    energy = math.exp(-diagnostics["phi"]) * tangent[0]
    delta_phi = diagnostics["phi"] - initial_phi
    block_b = jacobi[:2, 2:]
    det_b = float(np.linalg.det(block_b))
    angular_distance = math.sqrt(abs(det_b))
    wrl = abs(1.0 - math.exp(-2.0 * delta_phi))
    lambda_complement = abs(1.0 - math.exp(lambda_value * delta_phi))
    return {
        "path_id": path_id, "event_id": event_id, "direction": direction,
        "lambda": f"{lambda_value:g}", "affine": f"{affine:.8f}",
        "t": f"{x[0]:.17g}", "x": f"{x[1]:.17g}", "y": f"{x[2]:.17g}",
        "z": f"{x[3]:.17g}", "phi": f"{diagnostics['phi']:.17g}",
        "delta_phi": f"{delta_phi:.17g}", "frequency_Q": f"{tangent[0]:.17g}",
        "clock_law_residual": f"{abs(tangent[0]-math.exp(delta_phi)):.17g}",
        "killing_energy_drift": f"{abs(energy-initial_energy)/max(abs(initial_energy),1e-300):.17g}",
        "null_residual": f"{diagnostics['null_residual']:.17g}",
        "screen_gram_residual": f"{diagnostics['screen_gram_residual']:.17g}",
        "k_screen_residual": f"{diagnostics['k_screen_residual']:.17g}",
        "curvature_asymmetry": f"{curvature_asymmetry:.17g}",
        "symplectic_residual": f"{diagnostics['symplectic_residual']:.17g}",
        "detM_residual": f"{diagnostics['detM_residual']:.17g}",
        "screen_leakage": f"{diagnostics['screen_leakage']:.17g}",
        "pair_leakage": f"{diagnostics['pair_leakage']:.17g}",
        "ray_transverse_mismatch": f"{diagnostics['ray_transverse_mismatch']:.17g}",
        "detB": f"{det_b:.17g}", "D_A": f"{angular_distance:.17g}",
        "WRL_W": f"{wrl:.17g}", "lambda_complement": f"{lambda_complement:.17g}",
    }


def load_universe():
    with (HERE / "PATH_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    paths = []
    for row in rows:
        event = np.array([float(Fraction(row[key])) for key in ("x", "y", "z")])
        for direction in row["directions"].split(";"):
            for raw_lambda in row["lambda_values"].split(";"):
                paths.append((row["event_id"], event, direction, float(Fraction(raw_lambda))))
    assert len(paths) == 36
    return paths


def main() -> int:
    np.seterr(over="raise", divide="raise", invalid="raise", under="ignore")
    checkpoint_rows: list[dict[str, object]] = []
    path_rows: list[dict[str, object]] = []
    for index, (event_id, event, direction, lambda_value) in enumerate(load_universe(), start=1):
        path_id = f"{event_id}_{direction}_L{lambda_value:g}"
        state0 = initial_state(event, direction)
        initial_phi = float(geometry.profile_and_gradient(event)[0])
        initial_energy = math.exp(-initial_phi)
        anchor = initial_anchor(event, direction, lambda_value)
        production = integrate(state0, lambda_value, LENGTH, tight=False)
        convergence = integrate(state0, lambda_value, LENGTH, tight=True)
        production_end = production.y[:, -1]
        convergence_end = convergence.y[:, -1]
        convergence_difference = float(np.max(np.abs(production_end - convergence_end)))

        middle_state = production.sol(LENGTH / 2.0)
        x_mid, tangent_mid, transported_mid, _jacobi_mid = unpack(middle_state)
        second_initial = pack(x_mid, tangent_mid, transported_mid, np.eye(4))
        second = integrate(second_initial, lambda_value, LENGTH / 2.0, tight=False)
        m1 = unpack(middle_state)[3]
        m2 = unpack(second.y[:, -1])[3]
        direct_m = unpack(production_end)[3]
        composition_residual = float(np.max(np.abs(m2 @ m1 - direct_m)))

        rows_this_path = []
        for affine in CHECKPOINTS:
            row = checkpoint_row(path_id, event_id, direction, lambda_value, affine,
                                 production.sol(affine), initial_phi, initial_energy)
            rows_this_path.append(row)
            checkpoint_rows.append(row)
        da_end = float(rows_this_path[-1]["D_A"])
        wrl_end = float(rows_this_path[-1]["WRL_W"])
        da_norm = [float(row["D_A"]) / da_end if da_end > 1e-14 else math.nan for row in rows_this_path]
        wrl_norm = [float(row["WRL_W"]) / wrl_end if wrl_end > 1e-14 else math.nan for row in rows_this_path]
        shape_rms = (math.sqrt(sum((left-right)**2 for left, right in zip(da_norm, wrl_norm))/4)
                     if all(math.isfinite(value) for value in da_norm+wrl_norm) else math.nan)
        maxima_keys = (
            "clock_law_residual", "killing_energy_drift", "null_residual", "screen_gram_residual",
            "k_screen_residual", "curvature_asymmetry", "symplectic_residual", "detM_residual",
        )
        maxima = {key: max(float(row[key]) for row in rows_this_path) for key in maxima_keys}
        path_rows.append({
            "path_id": path_id, "event_id": event_id, "direction": direction,
            "lambda": f"{lambda_value:g}", "anchor_E1phi": f"{anchor['E1phi']:.17g}",
            "anchor_E2phi": f"{anchor['E2phi']:.17g}", "anchor_E3phi": f"{anchor['E3phi']:.17g}",
            "anchor_error": f"{anchor['anchor_error']:.17g}",
            "endpoint_screen_leakage": rows_this_path[-1]["screen_leakage"],
            "endpoint_pair_leakage": rows_this_path[-1]["pair_leakage"],
            "endpoint_D_A": rows_this_path[-1]["D_A"], "endpoint_WRL_W": rows_this_path[-1]["WRL_W"],
            "normalized_shape_rms": f"{shape_rms:.17g}",
            "composition_residual": f"{composition_residual:.17g}",
            "convergence_difference": f"{convergence_difference:.17g}",
            **{f"max_{key}": f"{value:.17g}" for key, value in maxima.items()},
            "production_nfev": production.nfev, "convergence_nfev": convergence.nfev,
        })
        print(f"completed {index}/36 {path_id}", file=sys.stderr, flush=True)

    checkpoint_fields = list(checkpoint_rows[0])
    with (HERE / "CHECKPOINT_ATLAS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=checkpoint_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(checkpoint_rows)
    path_fields = list(path_rows[0])
    with (HERE / "PATH_OUTCOMES.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=path_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(path_rows)

    numerical_maxima = {}
    for key in path_rows[0]:
        if key.startswith("max_") or key in {"anchor_error", "composition_residual", "convergence_difference"}:
            numerical_maxima[key] = max(float(row[key]) for row in path_rows)
    leakages = [float(row["endpoint_screen_leakage"]) for row in path_rows]
    shape_values = [float(row["normalized_shape_rms"]) for row in path_rows
                    if math.isfinite(float(row["normalized_shape_rms"]))]
    lambda_summary = {}
    for lambda_value in (-2.0, -1.0, 0.0, 0.5, 1.0, 2.0):
        subset = [row for row in path_rows if float(row["lambda"]) == lambda_value]
        lambda_summary[f"{lambda_value:g}"] = {
            "paths": len(subset),
            "screen_leakage_min": min(float(row["endpoint_screen_leakage"]) for row in subset),
            "screen_leakage_max": max(float(row["endpoint_screen_leakage"]) for row in subset),
            "shape_rms_min": min(float(row["normalized_shape_rms"]) for row in subset),
            "shape_rms_max": max(float(row["normalized_shape_rms"]) for row in subset),
        }
    result = {
        "schema": "udt-intrinsic-optical-transport-atlas-1.0", "status": "PASS",
        "paths": len(path_rows), "checkpoints": len(checkpoint_rows), "cpu_only": True,
        "dtype": "float64", "numpy_version": np.__version__, "scipy_version": scipy.__version__,
        "numerical_maxima": numerical_maxima,
        "endpoint_screen_leakage_min": min(leakages), "endpoint_screen_leakage_max": max(leakages),
        "normalized_shape_rms_min": min(shape_values), "normalized_shape_rms_max": max(shape_values),
        "lambda_summary": lambda_summary,
        "lambda_selected": False, "SNe_fit_performed": False, "on_shell_claimed": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
