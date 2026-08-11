#!/usr/bin/env python3
"""Independent primary P1 reconstruction without importing the production fitter."""

from __future__ import annotations

import json
import math
from pathlib import Path
import platform

import numpy as np
import scipy
from scipy.linalg import solve_triangular
from scipy.optimize import minimize_scalar


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "Data" / "Pantheon+SH0ES.dat"
COVARIANCE = ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov"
REFERENCE = ROOT / "udt_xmax_scale_observational_M3_runs_2026-08-07" / "sne_results.json"
LN10 = math.log(10.0)
M_B = -19.253


def load() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    table = np.genfromtxt(DATA, names=True, dtype=None, encoding="utf-8")
    z_all = np.asarray(table["zCMB"], dtype=float)
    magnitude_all = np.asarray(table["m_b_corr"], dtype=float)
    calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=int)
    selected = np.flatnonzero((z_all > 0.023) & (calibrator == 0))
    with COVARIANCE.open(encoding="utf-8") as handle:
        dimension = int(handle.readline())
        values = np.fromfile(handle, sep=" ")
    covariance_all = values.reshape(dimension, dimension)
    covariance_all = 0.5 * (covariance_all + covariance_all.T)
    return (
        z_all[selected],
        magnitude_all[selected],
        covariance_all[np.ix_(selected, selected)],
    )


def run() -> dict[str, object]:
    z, magnitude, covariance = load()
    lower = np.linalg.cholesky(covariance)
    one_white = solve_triangular(lower, np.ones_like(z), lower=True)
    y_white = solve_triangular(lower, magnitude, lower=True)
    denominator = float(one_white @ one_white)

    def evaluate(inv_n: float) -> tuple[float, float]:
        if not (1.0e-4 <= inv_n <= 40.0):
            return math.inf, math.nan
        log_r_shape = np.log(-np.expm1(-2.0 * inv_n * np.log1p(z))) - math.log(inv_n)
        model = (5.0 / LN10) * (2.0 * np.log1p(z) + log_r_shape)
        model_white = solve_triangular(lower, model, lower=True)
        difference_white = y_white - model_white
        offset = float((one_white @ difference_white) / denominator)
        residual_white = difference_white - offset * one_white
        return float(residual_white @ residual_white), offset

    grid = np.unique(
        np.concatenate(
            [
                np.geomspace(1.0e-4, 40.0, 96),
                np.linspace(0.45, 1.55, 112),
            ]
        )
    )
    sampled = np.asarray([evaluate(float(value))[0] for value in grid])
    index = int(np.argmin(sampled))
    left = float(grid[max(0, index - 1)])
    right = float(grid[min(len(grid) - 1, index + 1)])
    optimum = minimize_scalar(
        lambda value: evaluate(float(value))[0],
        bounds=(left, right),
        method="bounded",
        options={"xatol": 2.0e-11, "maxiter": 200},
    )
    inv_n = float(optimum.x)
    chi2, offset = evaluate(inv_n)
    chi2_n1, _ = evaluate(1.0)
    x_eff = 10.0 ** ((offset - 25.0 - M_B) / 5.0)

    frozen = json.loads(REFERENCE.read_text(encoding="utf-8"))["fits"]["A:zCMB:P1"]
    expected = {
        "inv_n": float(frozen["shape"]),
        "offset": float(frozen["offset_B"]),
        "chi2": float(frozen["chi2"]),
        "X_eff_Mpc": float(
            json.loads(REFERENCE.read_text(encoding="utf-8"))["fits"]["B:zCMB:P1"][
                "X_eff_Mpc"
            ]["best"]
        ),
    }
    differences = {
        "inv_n": abs(inv_n - expected["inv_n"]),
        "offset": abs(offset - expected["offset"]),
        "chi2": abs(chi2 - expected["chi2"]),
        "X_eff_Mpc": abs(x_eff - expected["X_eff_Mpc"]),
    }
    tolerances = {
        "inv_n": 2.0e-6,
        "offset": 2.0e-6,
        "chi2": 2.0e-5,
        "X_eff_Mpc": 5.0e-3,
    }
    failed = [name for name in differences if differences[name] > tolerances[name]]
    if failed:
        raise AssertionError(f"independent primary reconstruction failed: {failed}")
    if chi2 > float(np.min(sampled)) + 1.0e-7:
        raise AssertionError("refined optimum did not improve the frozen full-bounds scan")

    result = {
        "schema": "udt-sne-primary-independent-1.0",
        "status": "PASS",
        "method": "numpy_cholesky_whitening_plus_independent_bounded_scalar_search",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "n_data": len(z),
        "scan_points": len(grid),
        "best": {
            "inv_n": inv_n,
            "n": 1.0 / inv_n,
            "offset": offset,
            "chi2": chi2,
            "chi2_dof": chi2 / (len(z) - 2),
            "delta_chi2_n1": chi2_n1 - chi2,
            "sigma_equivalent_one_parameter": math.sqrt(max(0.0, chi2_n1 - chi2)),
            "X_eff_Mpc": x_eff,
        },
        "reference": expected,
        "absolute_differences": differences,
        "tolerances": tolerances,
        "full_bounds_scan_minimum": float(np.min(sampled)),
    }
    (HERE / "INDEPENDENT_PRIMARY.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        "PASS independent P1 "
        f"inv_n={inv_n:.9f} chi2={chi2:.9f} dchi2_n1={chi2_n1-chi2:.6f}"
    )
    return result


if __name__ == "__main__":
    run()
