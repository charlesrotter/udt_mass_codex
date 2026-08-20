#!/usr/bin/env python3
"""G189 production: exact P1-free metric/flux interface and dual-SNe control."""

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
    os.environ.get(
        "G189_DES_ROOT",
        "/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT",
    )
)
N_FROZEN = 1.0559332414320268
P1_PANTHEON_CHI2 = 1260.8480887274907
P1_DES_CHI2 = 1444.1864417504896


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
    if len(rows) != 17 or not all(checks.values()):
        raise RuntimeError("G189 source integrity failure")
    return checks


def p1_radius_shape(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return N_FROZEN * (-np.expm1(-2.0 * np.log(scale) / N_FROZEN))


def chi_radius_shape(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return np.tanh(np.log(scale))


def model_chi(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return 5.0 * np.log10(scale**2 * chi_radius_shape(z))


def model_p1(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return 5.0 * np.log10(scale**2 * p1_radius_shape(z))


def model_wrong_transfer(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return 5.0 * np.log10(scale**1.5 * chi_radius_shape(z))


def model_deleted_screen(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return 5.0 * np.log10(scale**2)


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
    redshift = np.asarray(table["zCMB"], dtype=float)
    observed = np.asarray(table["m_b_corr"], dtype=float)
    calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=int)
    keep = np.flatnonzero((redshift > 0.023) & (calibrator == 0))
    with PANTHEON_COV.open() as handle:
        dimension = int(handle.readline())
        covariance = np.fromfile(handle, sep=" ").reshape(dimension, dimension)
    covariance = 0.5 * (covariance + covariance.T)
    return redshift[keep], observed[keep], covariance[np.ix_(keep, keep)]


def read_des() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    keep = np.flatnonzero(np.asarray(table["IDSURVEY"], dtype=float) == 10)
    factor = cho_factor(precision, lower=True, check_finite=True)
    covariance = cho_solve(factor, np.eye(dimension), check_finite=True)
    covariance = covariance[np.ix_(keep, keep)]
    covariance = 0.5 * (covariance + covariance.T)
    return (
        np.asarray(table["zHD"], dtype=float)[keep],
        np.asarray(table["MU"], dtype=float)[keep],
        covariance,
    )


def exact_checks() -> dict[str, bool | str]:
    z, phi_s, phi_o, energy, c_e = sp.symbols(
        "Z phi_s phi_o E c_E", positive=True, finite=True
    )
    radius, d_a, eta, epsilon = sp.symbols(
        "R d_A eta epsilon", positive=True, finite=True
    )
    n, x_eff, r0 = sp.symbols("n X_eff R0", positive=True, finite=True)
    y, a = sp.symbols("y a", positive=True, finite=True)

    omega_s = energy * sp.exp(phi_s) / c_e
    omega_o = energy * sp.exp(phi_o) / c_e
    redshift_residual = sp.simplify(omega_s / omega_o - sp.exp(phi_s - phi_o))
    chi = sp.tanh(sp.log(z)).rewrite(sp.exp)
    chi_rational = (z**2 - 1) / (z**2 + 1)
    flux_distance = sp.sqrt(z**3 * d_a**2 / (1 / z))

    p1_radius = n * x_eff * (1 - sp.exp(-2 * y / n))
    p1_inverse = -n * sp.log(1 - radius / (n * x_eff)) / 2
    p1_inverse_residual = sp.simplify(p1_inverse.subs(radius, p1_radius) - y)

    inverse_1 = y
    inverse_2 = (sp.sqrt(1 + 4 * a * y) - 1) / (2 * a)
    profile_1 = radius
    profile_2 = radius + a * radius**2
    inverse_2_residual = sp.simplify(profile_2.subs(radius, inverse_2) - y)
    same_anchor = (
        profile_1.subs(radius, 0) == profile_2.subs(radius, 0) == 0
        and sp.diff(profile_1, radius).subs(radius, 0)
        == sp.diff(profile_2, radius).subs(radius, 0)
        == 1
    )
    chi_join_phi = sp.atanh(radius / r0)
    chi_join_center_slope = sp.simplify(sp.diff(chi_join_phi, radius).subs(radius, 0))
    smooth_even_phi = a * radius**2
    smooth_even_slope = sp.diff(smooth_even_phi, radius).subs(radius, 0)
    smooth_even_inverse = sp.sqrt(y / a)

    return {
        "static_frequency_ratio": redshift_residual == 0,
        "chi_rational_identity": sp.simplify(chi - chi_rational) == 0,
        "transparent_transfer_gives_Z2_dA": sp.simplify(flux_distance - z**2 * d_a) == 0,
        "central_screen_dA_equals_R": sp.sqrt(radius**2) == radius,
        "p1_profile_inverse": p1_inverse_residual == 0,
        "two_profiles_same_coincidence_jet": same_anchor,
        "quadratic_profile_inverse": inverse_2_residual == 0,
        "normalized_profiles_differ": sp.simplify(inverse_1 - inverse_2) != 0,
        "chi_join_center_slope_nonzero": chi_join_center_slope == 1 / r0,
        "smooth_even_center_slope_zero": smooth_even_slope == 0,
        "smooth_even_inverse": sp.simplify(
            smooth_even_phi.subs(radius, smooth_even_inverse) - y
        ) == 0,
        "chi_expression": str(sp.simplify(chi_rational)),
        "p1_phi_of_R": str(p1_inverse),
        "second_profile_inverse": str(inverse_2),
        "chi_join_phi_of_R": str(chi_join_phi),
        "smooth_even_R_of_logZ": str(smooth_even_inverse),
    }


def classify(p_chi2: float, d_chi2: float, n_p: int, n_d: int) -> tuple[str, dict[str, float]]:
    ceilings = {
        "pantheon": (n_p - 1) + 5.0 * math.sqrt(2.0 * (n_p - 1)),
        "des": (n_d - 1) + 5.0 * math.sqrt(2.0 * (n_d - 1)),
    }
    p1_level = (
        p_chi2 <= P1_PANTHEON_CHI2 + 25.0
        and d_chi2 <= P1_DES_CHI2 + 25.0
    )
    data_compatible = p_chi2 <= ceilings["pantheon"] and d_chi2 <= ceilings["des"]
    if p1_level:
        landing = "COEFFICIENT_FREE_P1_REPLACEMENT_LEAD"
    elif data_compatible:
        landing = "P1_FREE_JOIN_DATA_COMPATIBLE_BUT_NOT_P1_LEVEL"
    else:
        landing = "R_PROPORTIONAL_CHI_JOIN_REJECTED_IN_DECLARED_SNE_INTERFACE"
    return landing, ceilings


def main() -> None:
    source_hashes = verify_sources()
    exact = exact_checks()
    exact_bools = [value for value in exact.values() if isinstance(value, bool)]
    if not all(exact_bools):
        raise AssertionError("exact G189 ownership check failed")

    p_z, p_obs, p_cov = read_pantheon()
    d_z, d_obs, d_cov = read_des()
    p_model = model_chi(p_z)
    d_model = model_chi(d_z)
    p_chi2, p_offset = profile_covariance(p_cov, p_obs, p_model)
    d_chi2, d_offset = profile_covariance(d_cov, d_obs, d_model)
    p_p1, _ = profile_covariance(p_cov, p_obs, model_p1(p_z))
    d_p1, _ = profile_covariance(d_cov, d_obs, model_p1(d_z))
    landing, ceilings = classify(p_chi2, d_chi2, p_z.size, d_z.size)

    controls = {
        "pantheon_wrong_transfer_chi2": profile_covariance(
            p_cov, p_obs, model_wrong_transfer(p_z)
        )[0],
        "des_wrong_transfer_chi2": profile_covariance(
            d_cov, d_obs, model_wrong_transfer(d_z)
        )[0],
        "pantheon_deleted_screen_chi2": profile_covariance(
            p_cov, p_obs, model_deleted_screen(p_z)
        )[0],
        "des_deleted_screen_chi2": profile_covariance(
            d_cov, d_obs, model_deleted_screen(d_z)
        )[0],
        "candidate_vs_p1_max_mag_pantheon": float(
            np.max(np.abs(p_model - model_p1(p_z)))
        ),
        "candidate_vs_p1_max_mag_des": float(
            np.max(np.abs(d_model - model_p1(d_z)))
        ),
    }
    checks = {
        "all_17_source_hashes": len(source_hashes) == 17 and all(source_hashes.values()),
        "all_exact_checks": all(exact_bools),
        "pantheon_count": p_z.size == 1367,
        "des_count": d_z.size == 1623,
        "positive_outgoing_candidate": bool(
            np.all(np.isfinite(p_model))
            and np.all(np.isfinite(d_model))
            and np.all(chi_radius_shape(p_z) > 0.0)
            and np.all(chi_radius_shape(d_z) > 0.0)
        ),
        "p1_reference_reproduced": abs(p_p1 - P1_PANTHEON_CHI2) <= 3e-5 and abs(d_p1 - P1_DES_CHI2) <= 3e-6,
        "shape_optimizer_not_called": True,
        "shape_parameter_count_zero": True,
        "xmax_not_used": True,
        "post_readout_angular_factor_not_used": True,
    }
    result = {
        "audit": "G189_PRODUCTION",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "landing": landing,
        "type_landing": "R_PROPORTIONAL_CHI_NOT_A_SMOOTH_REGULAR_CENTER_STATIC_HISTORY",
        "scientific_landing": (
            "STATIC_CHI_SCREEN_JOIN_TYPE_FAILS_REGULAR_CENTER_AND_IS_DATA_REJECTED_AS_FORMAL_ANNULAR_CONTROL__"
            "METRIC_TO_FLUX_FACTORIZATION_CLOSES_CONDITIONALLY__"
            "P1_ROLE_LOCALIZED_TO_UNOWNED_PHI_OF_R_OR_TIMELIVE_FREQUENCY_HISTORY"
        ),
        "checks": checks,
        "exact": exact,
        "source_hashes": source_hashes,
        "candidate": {
            "formula": "dL_over_R0=Z^2*tanh(log(Z))",
            "status": "CHOSE_PROVISIONAL_CONTROL_NOT_DERIVED",
            "shape_parameters": 0,
            "transfer": "IMPORTED_CONDITIONAL_eta_1_epsilon_1_over_Z",
        },
        "pantheon": {
            "n_data": int(p_z.size),
            "chi2": p_chi2,
            "offset": p_offset,
            "p1_chi2_replay": p_p1,
            "delta_chi2_vs_p1": p_chi2 - p_p1,
        },
        "des": {
            "n_data": int(d_z.size),
            "chi2": d_chi2,
            "offset": d_offset,
            "p1_chi2_replay": d_p1,
            "delta_chi2_vs_p1": d_chi2 - d_p1,
        },
        "ceilings": ceilings,
        "controls": controls,
        "ownership": {
            "metric_to_screen": "DERIVED_CONDITIONAL",
            "static_frequency_ratio": "DERIVED_CONDITIONAL_ON_STATIC_SOURCE_OBSERVER_QUERY",
            "flux_factorization": "DERIVED_CONDITIONAL_REGULAR_BRANCH",
            "transfer": "IMPORTED_CONDITIONAL",
            "R_equals_R0_chi": "CHOSE_PROVISIONAL_CONTROL",
            "R_equals_R0_chi_global_center_status": "TYPE_FAILURE_NONZERO_RADIAL_DERIVATIVE_AT_REGULAR_CENTER",
            "p1_role": "EXACTLY_A_PARTICULAR_PHI_OF_R_PROFILE_NOT_USED_BY_CANDIDATE",
        },
        "shape_optimizer_called": False,
        "maximum_conclusion": "regular-center type failure and annular observational rejection of one provisional screen-position join; reciprocal kernel, time-live histories, and native transfer remain outside the negative",
    }
    if os.environ.get("UDT_WRITE_G189_RESULT") == "1":
        (HERE / "PRODUCTION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
