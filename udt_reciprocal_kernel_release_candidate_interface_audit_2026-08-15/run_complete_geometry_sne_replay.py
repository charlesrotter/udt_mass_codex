#!/usr/bin/env python3
"""Evaluate one frozen complete geometry against SNe without fitting its shape."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.linalg import solve_triangular


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ENGINE_PATH = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/solve_finite_path.py"
DATA_PATH = ROOT / "Data/Pantheon+SH0ES.dat"
COVARIANCE_PATH = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
PROFILE_ID = "G75_AM_S01_E05"
RECEIVER_X = 0.25
LAPSE_A = -0.25
MIX_C2 = 0.05
STEP_CONTROLS = (2048, 4096)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_engine():
    spec = importlib.util.spec_from_file_location("g97_complete_sne_engine", ENGINE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fields(_profile, x: float) -> tuple[float, float, float, float, float, float]:
    A = 1.0 + LAPSE_A * x**2
    A1 = 2.0 * LAPSE_A * x
    A2 = 2.0 * LAPSE_A
    h = MIX_C2 * x**6
    h1 = 6.0 * MIX_C2 * x**5
    h2 = 30.0 * MIX_C2 * x**4
    return A, A1, A2, h, h1, h2


def load_sne() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    table = np.genfromtxt(DATA_PATH, names=True, dtype=None, encoding="utf-8")
    z_all = np.asarray(table["zCMB"], dtype=float)
    magnitude_all = np.asarray(table["m_b_corr"], dtype=float)
    calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=int)
    selected = np.flatnonzero((z_all > 0.023) & (calibrator == 0))
    with COVARIANCE_PATH.open(encoding="utf-8") as stream:
        dimension = int(stream.readline())
        values = np.fromfile(stream, sep=" ")
    covariance_all = values.reshape(dimension, dimension)
    covariance_all = 0.5 * (covariance_all + covariance_all.T)
    return (
        selected,
        z_all[selected],
        magnitude_all[selected],
        covariance_all[np.ix_(selected, selected)],
    )


def source_x_from_z(z: np.ndarray) -> np.ndarray:
    A_receiver = 1.0 + LAPSE_A * RECEIVER_X**2
    Z = 1.0 + z
    A_source = A_receiver / Z**2
    return np.sqrt((A_source - 1.0) / LAPSE_A)


def integrate_to(engine, profile, endpoint_x: float, step_count: int):
    engine.END_X = float(endpoint_x)
    controls = {
        "method": "DOP853",
        "rtol": 2.0e-13,
        "atol": 2.0e-15,
        "max_step": 1.0 / step_count,
    }
    solution = engine.integrate(profile, controls)
    assert solution.success and len(solution.t_events[0]) == 1
    return solution


def affine_for_x(solution, x_targets: np.ndarray) -> np.ndarray:
    final_affine = float(solution.t_events[0][0])
    grid_s = np.linspace(0.0, final_affine, 12001)
    grid_x = np.asarray(solution.sol(grid_s)[1], dtype=float)
    if np.any(np.diff(grid_x) <= 0.0):
        raise AssertionError("outward query is not strictly monotone")
    if float(np.min(x_targets)) <= grid_x[0] or float(np.max(x_targets)) > grid_x[-1] + 1.0e-11:
        raise AssertionError("source target lies outside integrated path")
    affine = np.interp(x_targets, grid_x, grid_s)
    # Dense interpolation is already high order; one Newton correction makes the x match explicit.
    for index, target in enumerate(x_targets):
        state = np.asarray(solution.sol(float(affine[index])), dtype=float)
        kx = float(state[5])
        affine[index] -= (float(state[1]) - float(target)) / kx
    return affine


def curve_from_solution(engine, profile, solution, z: np.ndarray, x_source: np.ndarray) -> dict[str, np.ndarray]:
    affine = affine_for_x(solution, x_source)
    dA = np.empty_like(z)
    det_D = np.empty_like(z)
    for index, parameter in enumerate(affine):
        state = np.asarray(solution.sol(float(parameter)), dtype=float)
        D, _, _, _ = engine.screen_objects(profile, state)
        det_D[index] = float(np.linalg.det(D))
        dA[index] = math.sqrt(abs(det_D[index]))
    Z = 1.0 + z
    return {
        "affine_over_R": affine,
        "det_D_dimensionless": det_D,
        "dA_over_R": dA,
        "dL_over_R": Z**2 * dA,
    }


def fit_offset(magnitude: np.ndarray, covariance: np.ndarray, dL_over_R: np.ndarray) -> dict[str, float]:
    model_shape = 5.0 * np.log10(dL_over_R)
    lower = np.linalg.cholesky(covariance)
    one_white = solve_triangular(lower, np.ones_like(magnitude), lower=True)
    data_white = solve_triangular(lower, magnitude, lower=True)
    shape_white = solve_triangular(lower, model_shape, lower=True)
    difference = data_white - shape_white
    denominator = float(one_white @ one_white)
    offset = float((one_white @ difference) / denominator)
    residual = difference - offset * one_white
    chi2 = float(residual @ residual)
    return {
        "offset": offset,
        "chi2": chi2,
        "chi2_dof": chi2 / (len(magnitude) - 1),
        "offset_sigma": 1.0 / math.sqrt(denominator),
    }


def main() -> None:
    selected, z, magnitude, covariance = load_sne()
    x_source = source_x_from_z(z)
    if not (np.all(x_source > RECEIVER_X) and np.all(x_source < 2.0)):
        raise AssertionError("observed source endpoints leave the preregistered regular chart")

    engine = load_engine()
    engine.profile_values = fields
    profile = engine.Profile(
        profile_id=PROFILE_ID,
        family="G75_SELECTED",
        lapse_a=LAPSE_A,
        shape="S2",
        epsilon=MIX_C2,
    )
    endpoint_x = float(np.max(x_source))
    solutions = {
        steps: integrate_to(engine, profile, endpoint_x, steps)
        for steps in STEP_CONTROLS
    }
    curves = {
        steps: curve_from_solution(engine, profile, solution, z, x_source)
        for steps, solution in solutions.items()
    }
    coarse = curves[STEP_CONTROLS[0]]["dA_over_R"]
    fine = curves[STEP_CONTROLS[1]]["dA_over_R"]
    relative = np.abs(coarse - fine) / np.maximum(1.0e-15, np.abs(fine))
    max_relative = float(np.max(relative))

    final_solution = solutions[STEP_CONTROLS[-1]]
    final_affine = float(final_solution.t_events[0][0])
    residuals = engine.path_residuals(profile, final_solution, final_affine)
    caustic, min_singular = engine.first_caustic(profile, final_solution, final_affine)
    final_curve = curves[STEP_CONTROLS[-1]]
    likelihood = fit_offset(magnitude, covariance, final_curve["dL_over_R"])
    min_lapse = float(np.min(1.0 + LAPSE_A * x_source**2))

    checks = {
        "all_endpoints_inside_chart": bool(np.all((x_source > RECEIVER_X) & (x_source < 2.0))),
        "positive_lapse": min_lapse > 0.0,
        "no_caustic": caustic is None,
        "refinement_relative_below_2e_7": max_relative < 2.0e-7,
        "null_residual_below_1e_8": residuals["null"] < 1.0e-8,
        "screen_gram_below_1e_7": residuals["screen_gram"] < 1.0e-7,
        "screen_ray_below_1e_7": residuals["screen_ray"] < 1.0e-7,
        "killing_energy_below_1e_8": residuals["conserved_p_t"] < 1.0e-8,
        "finite_positive_distances": bool(
            np.all(np.isfinite(final_curve["dA_over_R"]))
            and np.all(final_curve["dA_over_R"] > 0.0)
            and np.all(final_curve["dL_over_R"] > 0.0)
        ),
    }
    if not all(checks.values()):
        raise AssertionError({key: value for key, value in checks.items() if not value})

    result = {
        "schema": "udt-g93-one-complete-geometry-sne-replay-v1",
        "status": "PASS",
        "landing": (
            "OBSERVED_CONDITIONAL_ONE_CONTROL_GEOMETRY_SNE_CURVE"
            "__PROVISIONAL_TRANSPARENT_NULL_CARRIER_INTERFACE"
            "__NO_HISTORY_XMAX_EM_OR_PARTICLE_CLOSURE"
        ),
        "profile": {
            "profile_id": PROFILE_ID,
            "A_of_x": "1-x^2/4",
            "h_of_x": "x^6/20",
            "receiver_x": RECEIVER_X,
            "geometry_shape_fitted": False,
        },
        "provisional_transfer": {
            "eta": 1.0,
            "epsilon": "1/Z",
            "dL_relation": "d_L=Z^2*d_A",
            "status": "POSIT__CONDITIONAL__NOT_UDT_DERIVED",
        },
        "data": {
            "catalog": str(DATA_PATH.relative_to(ROOT)),
            "catalog_sha256": sha256(DATA_PATH),
            "covariance": str(COVARIANCE_PATH.relative_to(ROOT)),
            "covariance_sha256": sha256(COVARIANCE_PATH),
            "selection": "zCMB>0.023 and IS_CALIBRATOR==0",
            "n": int(len(z)),
            "row_index_min": int(np.min(selected)),
            "row_index_max": int(np.max(selected)),
            "z_min": float(np.min(z)),
            "z_max": float(np.max(z)),
        },
        "path": {
            "source_x_min": float(np.min(x_source)),
            "source_x_max": endpoint_x,
            "minimum_lapse": min_lapse,
            "final_affine_over_R": final_affine,
            "first_caustic_affine": caustic,
            "minimum_sampled_screen_singular_value": min_singular,
            "residuals": residuals,
        },
        "refinement": {
            "step_controls": list(STEP_CONTROLS),
            "max_relative_dA_difference": max_relative,
        },
        "likelihood": likelihood,
        "checks": checks,
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "authority": {
            "physical_history_selected": False,
            "all_sky_isotropy_derived": False,
            "native_radiative_law_derived": False,
            "Xmax_identified": False,
            "shape_parameter_fitted": False,
            "single_offset_profiled": True,
        },
    }
    atlas_path = HERE / "SNE_COMPLETE_GEOMETRY_CURVE.tsv"
    with atlas_path.open("w", newline="", encoding="utf-8") as stream:
        fields_out = (
            "source_row", "zCMB", "source_x", "affine_over_R", "det_D_dimensionless",
            "dA_over_R", "dL_over_R", "model_shape_mag",
        )
        writer = csv.DictWriter(stream, fieldnames=fields_out, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for index in range(len(z)):
            writer.writerow({
                "source_row": int(selected[index]),
                "zCMB": f"{z[index]:.17g}",
                "source_x": f"{x_source[index]:.17g}",
                "affine_over_R": f"{final_curve['affine_over_R'][index]:.17g}",
                "det_D_dimensionless": f"{final_curve['det_D_dimensionless'][index]:.17g}",
                "dA_over_R": f"{final_curve['dA_over_R'][index]:.17g}",
                "dL_over_R": f"{final_curve['dL_over_R'][index]:.17g}",
                "model_shape_mag": f"{5.0 * math.log10(final_curve['dL_over_R'][index]):.17g}",
            })
    result["curve_atlas"] = {
        "path": atlas_path.name,
        "rows": int(len(z)),
        "sha256": sha256(atlas_path),
    }
    (HERE / "SNE_COMPLETE_GEOMETRY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
