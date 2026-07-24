#!/usr/bin/env python3
"""No-retune full-covariance replay of the two preregistered SNe readouts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "Data" / "Pantheon+SH0ES.dat"
COVARIANCE = ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov"


def load_inputs() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    catalog = np.genfromtxt(DATA, names=True, dtype=None, encoding=None)
    if len(catalog) != 1701:
        raise AssertionError("catalog row count")
    z_all = np.asarray(catalog["zHD"], dtype=float)
    magnitude_all = np.asarray(catalog["m_b_corr"], dtype=float)
    calibrator = np.asarray(catalog["IS_CALIBRATOR"], dtype=int)
    selected = np.flatnonzero((calibrator == 0) & (z_all > 0.01))
    if len(selected) != 1580:
        raise AssertionError("selected row count")
    with COVARIANCE.open(encoding="utf-8") as handle:
        covariance_count = int(handle.readline().strip())
    if covariance_count != 1701:
        raise AssertionError("covariance dimension header")
    covariance_all = np.loadtxt(COVARIANCE, skiprows=1).reshape(1701, 1701)
    covariance_all = 0.5 * (covariance_all + covariance_all.T)
    covariance = covariance_all[np.ix_(selected, selected)]
    return z_all[selected], magnitude_all[selected], covariance


def shapes(z: np.ndarray) -> dict[str, np.ndarray]:
    u = 1.0 + z
    return {
        "WRL_AREAL_OPTICAL": z * (z + 2.0),
        "PROJECTIVE_AREAL_J1": u**2 * (u**2 - 1.0) / (u**2 + 1.0),
    }


def score_cholesky(
    z: np.ndarray, magnitude: np.ndarray, covariance: np.ndarray
) -> dict[str, dict[str, object]]:
    factor = cho_factor(covariance, lower=True, check_finite=False)
    ones = np.ones_like(z)
    inverse_ones = cho_solve(factor, ones, check_finite=False)
    denominator = float(ones @ inverse_ones)
    output: dict[str, dict[str, object]] = {}
    for name, distance_shape in shapes(z).items():
        predicted_shape = 5.0 * np.log10(distance_shape)
        difference = magnitude - predicted_shape
        inverse_difference = cho_solve(factor, difference, check_finite=False)
        offset = float((ones @ inverse_difference) / denominator)
        residual = difference - offset
        chi2 = float(residual @ cho_solve(factor, residual, check_finite=False))
        dof = len(z) - 1
        output[name] = {
            "formula": (
                "z*(z+2)"
                if name == "WRL_AREAL_OPTICAL"
                else "u^2*(u^2-1)/(u^2+1);u=1+z"
            ),
            "N": len(z),
            "offset_count": 1,
            "offset": offset,
            "chi2": chi2,
            "dof": dof,
            "chi2_dof": chi2 / dof,
            "rms_mag": float(np.sqrt(np.mean(residual**2))),
        }
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="SNE_RESULT.json")
    args = parser.parse_args()
    z, magnitude, covariance = load_inputs()
    scores = score_cholesky(z, magnitude, covariance)
    expected = {
        "WRL_AREAL_OPTICAL": (0.9098574003059215, 0.1581642243395007),
        "PROJECTIVE_AREAL_J1": (2.166501637078457, 0.30740259169961603),
    }
    for name, (chi2_dof, rms) in expected.items():
        if abs(float(scores[name]["chi2_dof"]) - chi2_dof) > 2e-12:
            raise AssertionError(f"{name} chi2/dof")
        if abs(float(scores[name]["rms_mag"]) - rms) > 2e-14:
            raise AssertionError(f"{name} RMS")
    result = {
        "schema": "udt-sne-readout-replay-1.0",
        "result": "PASS",
        "method": "scipy_cholesky",
        "cut": "IS_CALIBRATOR==0 and zHD>0.01",
        "shape_parameters_fit": 0,
        "additive_offsets_fit": 1,
        "scores": scores,
        "adjudication": {
            "observed_preference": "WRL_AREAL_OPTICAL_OVER_PROJECTIVE_AREAL_J1",
            "selects_pair_metric_profile": False,
            "reason": (
                "WRL score uses areal radius plus clock and optics; it is not "
                "the WRL proper-distance pair transform"
            ),
        },
    }
    (HERE / args.output).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
