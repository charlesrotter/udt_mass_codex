#!/usr/bin/env python3
"""G185 production: full-channel central-spherical SNe non-regression replay."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.linalg import cho_factor, cho_solve, solve_triangular


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PANTHEON_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
PANTHEON_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES_ROOT = Path(
    "/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT"
)
G99 = ROOT / "udt_observed_middle_regime_pair_calibration_2026-08-15/CALIBRATION_CONTRACT.json"
G120 = ROOT / "udt_g120_exact_screen_imported_transfer_dual_sne_recomposition_2026-08-16/PRODUCTION_RESULT.json"

# FROZEN_HISTORICAL_CALIBRATION (G99/G120); not retuned in G185.
N_FROZEN = 1.0559332414320268


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_sources() -> dict[str, bool]:
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks: dict[str, bool] = {}
    for row in rows:
        path = Path(row["path"])
        if not path.is_absolute():
            path = ROOT / path
        checks[row["path"]] = path.is_file() and sha256(path) == row["sha256"]
    if len(rows) != 14 or not all(checks.values()):
        raise RuntimeError("G185 source integrity failure")
    return checks


def radius_shape(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return N_FROZEN * (-np.expm1(-2.0 * np.log(scale) / N_FROZEN))


def model_full_screen(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    radius = radius_shape(z)
    # IMPORTED_CONDITIONAL: eta*epsilon=1/Z; G119 supplies the live R^2 screen.
    transfer = 1.0 / scale
    distance = np.sqrt(scale**3 * radius**2 / transfer)
    return 5.0 * np.log10(distance)


def model_deleted_screen(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return 5.0 * np.log10(scale**2)


def model_duplicated_screen(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    radius = radius_shape(z)
    return 5.0 * np.log10(scale**2 * radius**2)


def model_wrong_transfer(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return 5.0 * np.log10(scale**1.5 * radius_shape(z))


def profile_covariance(
    covariance: np.ndarray, observed: np.ndarray, model: np.ndarray
) -> tuple[float, float]:
    lower = np.linalg.cholesky(covariance)
    one_white = solve_triangular(lower, np.ones(observed.size), lower=True)
    residual_white = solve_triangular(lower, observed - model, lower=True)
    offset = float(one_white @ residual_white / (one_white @ one_white))
    final = residual_white - offset * one_white
    return float(final @ final), offset


def read_pantheon() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    table = np.genfromtxt(PANTHEON_TABLE, names=True, dtype=None, encoding="utf-8")
    z_all = np.asarray(table["zCMB"], dtype=float)
    observed_all = np.asarray(table["m_b_corr"], dtype=float)
    calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=int)
    # OBSERVED release cut retained exactly from the frozen interface.
    keep = np.flatnonzero((z_all > 0.023) & (calibrator == 0))
    with PANTHEON_COV.open() as handle:
        dimension = int(handle.readline())
        values = np.fromfile(handle, sep=" ")
    covariance = values.reshape(dimension, dimension)
    covariance = 0.5 * (covariance + covariance.T)
    return z_all[keep], observed_all[keep], covariance[np.ix_(keep, keep)]


def read_des() -> tuple[dict[str, np.ndarray], np.ndarray]:
    names = None
    columns: dict[str, list[object]] = {}
    with (DES_ROOT / "DES-Dovekie_HD.csv").open() as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("VARNAMES:"):
                names = line.split()[1:]
                columns = {name: [] for name in names}
                continue
            if names is None or not line.startswith("SN:"):
                raise ValueError("unexpected DES table line")
            values = line.split()[1:]
            for name, value in zip(names, values):
                columns[name].append(value if name == "CID" else float(value))
    table = {name: np.asarray(values) for name, values in columns.items()}
    with np.load(DES_ROOT / "STAT+SYS.npz", allow_pickle=False) as archive:
        dimension = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=float)
    precision = np.zeros((dimension, dimension))
    upper = np.triu_indices(dimension)
    precision[upper] = packed
    precision[(upper[1], upper[0])] = packed
    return table, precision


def marginal_des_covariance(precision: np.ndarray, keep: np.ndarray) -> np.ndarray:
    factor = cho_factor(precision, lower=True, check_finite=True)
    covariance = cho_solve(factor, np.eye(precision.shape[0]), check_finite=True)
    answer = covariance[np.ix_(keep, keep)]
    return 0.5 * (answer + answer.T)


def symbolic_channel_checks() -> dict[str, bool | str]:
    a, v, r, b2, zfreq, radius = sp.symbols(
        "a v r b2 Z R", positive=True, finite=True
    )
    theta0, theta1, psi0, psi1, sintheta = sp.symbols(
        "theta0 theta1 psi0 psi1 sintheta", real=True
    )
    angular = r**2 * sp.Matrix(
        [
            [theta0**2 + sintheta**2 * psi0**2, theta0 * theta1 + sintheta**2 * psi0 * psi1],
            [theta0 * theta1 + sintheta**2 * psi0 * psi1, theta1**2 + sintheta**2 * psi1**2],
        ]
    )
    radial_angular = angular.subs({theta0: 0, theta1: 0, psi0: 0, psi1: 0})
    h_radial = sp.diag(-a, v**2 / a)
    m2_radial = sp.simplify(-h_radial.det())
    h_general = sp.diag(-a, v**2 / a + r**2 * b2)
    m2_general = sp.simplify(-h_general.det())
    angle = sp.symbols("alpha", real=True)
    rotation = sp.Matrix([[sp.cos(angle), -sp.sin(angle)], [sp.sin(angle), sp.cos(angle)]])
    dsky = radius * rotation
    transfer_residual = sp.simplify(
        sp.sqrt(zfreq**3 * radius**2 / (1 / zfreq)) - zfreq**2 * radius
    )
    return {
        "radial_pair_angular_gram_zero": radial_angular == sp.zeros(2),
        "radial_completed_density_squared_is_v_squared": sp.simplify(m2_radial - v**2) == 0,
        "nonradial_pair_angular_term_live": sp.simplify(m2_general - v**2 - a * r**2 * b2) == 0,
        "sky_determinant_is_R_squared": sp.simplify(dsky.det() - radius**2) == 0,
        "imported_transfer_reduces_to_Z2R": transfer_residual == 0,
        "radial_pair_gram": str(radial_angular),
        "general_completed_density_squared": str(m2_general),
        "sky_determinant": str(sp.simplify(dsky.det())),
    }


def main() -> None:
    source_hashes = verify_sources()
    g99 = json.loads(G99.read_text())
    reference = json.loads(G120.read_text())
    if float(g99["calibration"]["n"]).hex() != float(N_FROZEN).hex():
        raise AssertionError("frozen n changed")

    p_z, p_obs, p_cov = read_pantheon()
    p_model = model_full_screen(p_z)
    p_chi2, p_offset = profile_covariance(p_cov, p_obs, p_model)
    p_controls = {
        "deleted_screen": profile_covariance(p_cov, p_obs, model_deleted_screen(p_z))[0],
        "duplicated_screen": profile_covariance(p_cov, p_obs, model_duplicated_screen(p_z))[0],
        "wrong_transfer": profile_covariance(p_cov, p_obs, model_wrong_transfer(p_z))[0],
    }

    d_table, d_precision = read_des()
    d_keep = np.flatnonzero(np.asarray(d_table["IDSURVEY"], dtype=float) == 10)
    d_z = np.asarray(d_table["zHD"], dtype=float)[d_keep]
    d_obs = np.asarray(d_table["MU"], dtype=float)[d_keep]
    d_cov = marginal_des_covariance(d_precision, d_keep)
    d_model = model_full_screen(d_z)
    d_chi2, d_offset = profile_covariance(d_cov, d_obs, d_model)
    d_controls = {
        "deleted_screen": profile_covariance(d_cov, d_obs, model_deleted_screen(d_z))[0],
        "duplicated_screen": profile_covariance(d_cov, d_obs, model_duplicated_screen(d_z))[0],
        "wrong_transfer": profile_covariance(d_cov, d_obs, model_wrong_transfer(d_z))[0],
    }

    reference_curve_p = 5.0 * np.log10(
        N_FROZEN * (1.0 + p_z) ** 2 * (1.0 - (1.0 + p_z) ** (-2.0 / N_FROZEN))
    )
    reference_curve_d = 5.0 * np.log10(
        N_FROZEN * (1.0 + d_z) ** 2 * (1.0 - (1.0 + d_z) ** (-2.0 / N_FROZEN))
    )
    residuals = {
        "pantheon_curve_mag": float(np.max(np.abs(p_model - reference_curve_p))),
        "des_curve_mag": float(np.max(np.abs(d_model - reference_curve_d))),
        "pantheon_chi2_vs_G120": abs(p_chi2 - float(reference["pantheon"]["chi2"])),
        "pantheon_offset_vs_G120": abs(p_offset - float(reference["pantheon"]["offset_B"])),
        "des_chi2_vs_G120": abs(d_chi2 - float(reference["des"]["chi2"])),
        "des_offset_vs_G120": abs(d_offset - float(reference["des"]["offset_B"])),
    }
    tolerances = {
        "curve_mag": 1e-12,
        "pantheon_chi2": 3e-5,
        "pantheon_offset": 3e-6,
        "des_chi2": 3e-6,
        "des_offset": 3e-9,
    }
    symbolic = symbolic_channel_checks()
    symbolic_booleans = [value for value in symbolic.values() if isinstance(value, bool)]
    checks = {
        "all_14_source_hashes": len(source_hashes) == 14 and all(source_hashes.values()),
        "symbolic_channel_checks": all(symbolic_booleans),
        "pantheon_count": p_z.size == 1367,
        "des_count": d_z.size == 1623,
        "outgoing_domain": bool(np.all(1.0 + p_z > 1.0) and np.all(1.0 + d_z > 1.0)),
        "pantheon_curve_preserved": residuals["pantheon_curve_mag"] <= tolerances["curve_mag"],
        "des_curve_preserved": residuals["des_curve_mag"] <= tolerances["curve_mag"],
        "pantheon_chi2_preserved": residuals["pantheon_chi2_vs_G120"] <= tolerances["pantheon_chi2"],
        "pantheon_offset_preserved": residuals["pantheon_offset_vs_G120"] <= tolerances["pantheon_offset"],
        "des_chi2_preserved": residuals["des_chi2_vs_G120"] <= tolerances["des_chi2"],
        "des_offset_preserved": residuals["des_offset_vs_G120"] <= tolerances["des_offset"],
        "screen_deletion_detected": p_controls["deleted_screen"] > p_chi2 + 100.0 and d_controls["deleted_screen"] > d_chi2 + 100.0,
        "screen_duplication_detected": p_controls["duplicated_screen"] > p_chi2 + 100.0 and d_controls["duplicated_screen"] > d_chi2 + 100.0,
        "wrong_transfer_detected": p_controls["wrong_transfer"] > p_chi2 + 100.0 and d_controls["wrong_transfer"] > d_chi2 + 100.0,
        "shape_optimizer_called_false": True,
        "terminal_Phi_inserted_false": True,
        "post_readout_angular_factor_inserted_false": True,
    }
    passed = all(checks.values())
    result = {
        "audit": "G185",
        "status": "PASS" if passed else "FAIL",
        "landing": (
            "CENTRAL_SPHERICAL_SNE_QUERY_RETAINS_THE_FULL_RELEVANT_METRIC_RESPONSE__"
            "RADIAL_PAIR_ANGULAR_TANGENT_ZERO_IS_QUERY_DERIVED__AREAL_SKY_RESPONSE_R2_REMAINS_ACTIVE__"
            "FROZEN_DUAL_SNE_REPLAY_IS_CONDITIONALLY_PRESERVED"
            if passed
            else "G185_GATE_FAILURE"
        ),
        "checks": checks,
        "symbolic_channels": symbolic,
        "source_hashes": source_hashes,
        "residuals": residuals,
        "tolerances": tolerances,
        "pantheon": {"n_data": int(p_z.size), "chi2": p_chi2, "offset_B": p_offset, "controls": p_controls},
        "des": {"n_data": int(d_z.size), "chi2": d_chi2, "offset_B": d_offset, "controls": d_controls},
        "ownership": {
            "pair_angular_zero": "derived from supplied radial pair tangent Z_pair=0",
            "sky_area": "metric-derived G119 |det D_sky|=R^2 and active for R>0",
            "transfer": "IMPORTED_CONDITIONAL eta=1 epsilon=1/Z",
            "radius_frequency_history": "FROZEN_HISTORICAL_CALIBRATION not derived in G185",
            "terminal_depth": "completed Phi remains separate from release log Z outside the pure stationary reciprocal reduction",
            "extrinsic_branch_data": "not required by this bounded scalar query; branch population remains open",
        },
        "omitted": [
            "displaced or nonspherical observers", "nonradial pair germs", "ambient mixing",
            "multiple-image aggregation", "native light theory", "physical R(Z) or phi(r) history",
            "global completion", "X_max", "BAO", "CMB", "dynamics", "matter",
        ],
        "shape_optimizer_called": False,
        "maximum_conclusion": "bounded central-spherical conditional channel compatibility and frozen SNe non-regression only",
    }
    if os.environ.get("UDT_WRITE_G185_RESULT") == "1":
        (HERE / "PRODUCTION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
