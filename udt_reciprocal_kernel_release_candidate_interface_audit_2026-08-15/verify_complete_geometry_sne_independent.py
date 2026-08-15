#!/usr/bin/env python3
"""Independent neighboring-ray and likelihood checks for the fixed G93 SNe curve."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DIRECT_PATH = ROOT / "udt_cmb_G79_same_geometry_dimensional_sne_query_2026-08-11/verify_same_geometry_sne_independent.py"
PRODUCTION_PATH = HERE / "run_complete_geometry_sne_replay.py"
DATA_PATH = ROOT / "Data/Pantheon+SH0ES.dat"
COVARIANCE_PATH = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
ANCHORS = (0.03, 0.10, 0.50, 1.00, 2.00)
DELTAS = (1.0e-4, 5.0e-5)
RECEIVER_X = 0.25
LAPSE_A = -0.25
COEFFICIENTS = (0.0, 0.0, 0.05)


def load_direct():
    spec = importlib.util.spec_from_file_location("g97_direct_neighbor", DIRECT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_production():
    spec = importlib.util.spec_from_file_location("g97_exact_anchor_production", PRODUCTION_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def source_x(z: float) -> float:
    A_receiver = 1.0 + LAPSE_A * RECEIVER_X**2
    return math.sqrt((A_receiver / (1.0 + z) ** 2 - 1.0) / LAPSE_A)


def integrate(direct, k0: np.ndarray, target_x: float | None, final_affine: float | None, with_screen: bool):
    position, _, _, e_theta, e_psi = direct.initial(LAPSE_A, COEFFICIENTS)
    y0 = np.concatenate((position, k0, e_theta, e_psi)) if with_screen else np.concatenate((position, k0))

    def rhs(_parameter: float, state: np.ndarray) -> np.ndarray:
        position_now, k = state[:4], state[4:8]
        Gamma = direct.christoffel(LAPSE_A, COEFFICIENTS, position_now)
        dk = -np.einsum("rmn,m,n->r", Gamma, k, k)
        if not with_screen:
            return np.concatenate((k, dk))
        E = state[8:16].reshape(2, 4)
        dE = -np.einsum("rmn,m,an->ar", Gamma, k, E)
        return np.concatenate((k, dk, dE.ravel()))

    events = None
    interval = (0.0, float(final_affine) if final_affine is not None else 10.0)
    if target_x is not None:
        def event(_parameter: float, state: np.ndarray) -> float:
            return float(state[1] - target_x)
        event.terminal = True
        event.direction = 1.0
        events = event
    return solve_ivp(
        rhs,
        interval,
        y0,
        method="DOP853",
        rtol=2.0e-12,
        atol=2.0e-14,
        max_step=1.0 / 400.0,
        events=events,
        dense_output=True,
    )


def independent_anchor(direct, z: float) -> dict[str, float]:
    target = source_x(z)
    position0, u, radial, e_theta, e_psi = direct.initial(LAPSE_A, COEFFICIENTS)
    central = integrate(direct, u + radial, target, None, True)
    assert central.success and len(central.t_events[0]) == 1
    affine = float(central.t_events[0][0])
    state = np.asarray(central.sol(affine), dtype=float)
    endpoint = state[:4]
    endpoint_screen = state[8:16].reshape(2, 4)
    endpoint_g, _ = direct.metric_first(LAPSE_A, COEFFICIENTS, endpoint)
    matrices: dict[float, np.ndarray] = {}
    max_null = 0.0
    for delta in DELTAS:
        D = np.zeros((2, 2), dtype=float)
        for column, screen in enumerate((e_theta, e_psi)):
            plus_k = u + radial * math.cos(delta) + screen * math.sin(delta)
            minus_k = u + radial * math.cos(delta) - screen * math.sin(delta)
            plus = integrate(direct, plus_k, None, affine, False)
            minus = integrate(direct, minus_k, None, affine, False)
            assert plus.success and minus.success
            jacobi = (plus.y[:4, -1] - minus.y[:4, -1]) / (2.0 * delta)
            D[:, column] = endpoint_screen @ endpoint_g @ jacobi
            for solution in (plus, minus):
                position_now, k = solution.y[:4, -1], solution.y[4:8, -1]
                g, _ = direct.metric_first(LAPSE_A, COEFFICIENTS, position_now)
                max_null = max(max_null, abs(float(k @ g @ k)))
        matrices[delta] = D
    coarse, fine = (matrices[value] for value in DELTAS)
    dA = math.sqrt(abs(float(np.linalg.det(fine))))
    return {
        "z": z,
        "source_x": target,
        "affine_over_R": affine,
        "dA_over_R": dA,
        "coarse_fine_relative": direct.relative(coarse, fine),
        "max_endpoint_null_absolute": max_null,
    }


def exact_production_anchors(production) -> np.ndarray:
    z = np.asarray(ANCHORS, dtype=float)
    x = production.source_x_from_z(z)
    engine = production.load_engine()
    engine.profile_values = production.fields
    profile = engine.Profile(
        profile_id=production.PROFILE_ID,
        family="G75_SELECTED",
        lapse_a=production.LAPSE_A,
        shape="S2",
        epsilon=production.MIX_C2,
    )
    solution = production.integrate_to(engine, profile, float(np.max(x)), 4096)
    return production.curve_from_solution(engine, profile, solution, z, x)["dA_over_R"]


def independent_likelihood() -> dict[str, float]:
    table = np.genfromtxt(DATA_PATH, names=True, dtype=None, encoding="utf-8")
    z_all = np.asarray(table["zCMB"], dtype=float)
    magnitude_all = np.asarray(table["m_b_corr"], dtype=float)
    calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=int)
    selected = np.flatnonzero((z_all > 0.023) & (calibrator == 0))
    with COVARIANCE_PATH.open(encoding="utf-8") as stream:
        dimension = int(stream.readline())
        values = np.fromfile(stream, sep=" ")
    covariance = values.reshape(dimension, dimension)
    covariance = 0.5 * (covariance + covariance.T)
    covariance = covariance[np.ix_(selected, selected)]

    by_row: dict[int, float] = {}
    with (HERE / "SNE_COMPLETE_GEOMETRY_CURVE.tsv").open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            by_row[int(row["source_row"])] = float(row["model_shape_mag"])
    model = np.asarray([by_row[int(index)] for index in selected])
    magnitude = magnitude_all[selected]
    inverse = np.linalg.inv(covariance)
    one = np.ones_like(magnitude)
    difference = magnitude - model
    offset = float((one @ inverse @ difference) / (one @ inverse @ one))
    residual = difference - offset
    chi2 = float(residual @ inverse @ residual)
    return {"offset": offset, "chi2": chi2, "n": int(len(selected))}


def main() -> None:
    production = json.loads((HERE / "SNE_COMPLETE_GEOMETRY_RESULT.json").read_text(encoding="utf-8"))
    direct = load_direct()
    production_module = load_production()
    production_dA = exact_production_anchors(production_module)
    anchors = [independent_anchor(direct, z) for z in ANCHORS]
    for row, exact_dA in zip(anchors, production_dA):
        row["production_dA_over_R_exact_anchor"] = float(exact_dA)
        row["independent_production_relative"] = abs(
            row["dA_over_R"] - row["production_dA_over_R_exact_anchor"]
        ) / row["dA_over_R"]
    likelihood = independent_likelihood()
    offset_difference = abs(likelihood["offset"] - production["likelihood"]["offset"])
    chi2_difference = abs(likelihood["chi2"] - production["likelihood"]["chi2"])
    checks = {
        "five_anchor_rows": len(anchors) == 5,
        "all_anchor_dA_agree_below_3e_4": max(row["independent_production_relative"] for row in anchors) < 3.0e-4,
        "all_anchor_delta_converged": max(row["coarse_fine_relative"] for row in anchors) < 3.0e-4,
        "all_anchor_null": max(row["max_endpoint_null_absolute"] for row in anchors) < 1.0e-9,
        "offset_reproduced": offset_difference < 2.0e-6,
        "chi2_reproduced": chi2_difference < 2.0e-4,
    }
    result = {
        "schema": "udt-g93-one-complete-geometry-sne-independent-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "method": "direct_loop_Christoffel_plus_finite_difference_neighboring_rays_and_explicit_covariance_inverse",
        "anchors": anchors,
        "likelihood": likelihood,
        "production_likelihood": production["likelihood"],
        "offset_absolute_difference": offset_difference,
        "chi2_absolute_difference": chi2_difference,
        "checks": checks,
    }
    (HERE / "SNE_COMPLETE_GEOMETRY_INDEPENDENT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
