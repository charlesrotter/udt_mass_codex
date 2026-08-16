#!/usr/bin/env python3
"""G117 production replay: observed frequency coordinate, frozen P1, no history fit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve, solve_triangular
from scipy.stats import chi2 as chi2_dist


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "a7890d9f"
PANTHEON_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
PANTHEON_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES_ROOT = Path("/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT")
G99 = ROOT / "udt_observed_middle_regime_pair_calibration_2026-08-15/CALIBRATION_CONTRACT.json"
G100 = ROOT / "udt_des_sn5yr_frozen_p1_holdout_2026-08-15/PRIMARY_RESULT.json"
N_FROZEN = 1.0559332414320268


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sources() -> dict[str, bool]:
    checks: dict[str, bool] = {}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        path = Path(row["path"])
        if not path.is_absolute():
            path = ROOT / path
        checks[row["path"]] = path.is_file() and sha256(path) == row["sha256"]
    if len(rows) != 18 or not all(checks.values()):
        raise RuntimeError("G117 source integrity failure")
    return checks


def retyped_shape(z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    z_obs = np.asarray(z, dtype=np.float64)
    zeta = np.log1p(z_obs)
    screen_radius = N_FROZEN * (-np.expm1(-2.0 * zeta / N_FROZEN))
    luminosity_shape = np.exp(2.0 * zeta) * np.sqrt(screen_radius * screen_radius)
    return (5.0 / np.log(10.0)) * np.log(luminosity_shape), zeta, screen_radius


def legacy_shape(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    distance = N_FROZEN * scale**2 * (1.0 - scale ** (-2.0 / N_FROZEN))
    return 5.0 * np.log10(distance)


def profile_covariance(covariance: np.ndarray, observed: np.ndarray, model: np.ndarray) -> tuple[float, float]:
    lower = np.linalg.cholesky(covariance)
    one_white = solve_triangular(lower, np.ones(observed.size), lower=True)
    residual_white = solve_triangular(lower, observed - model, lower=True)
    offset = float(one_white @ residual_white / (one_white @ one_white))
    final = residual_white - offset * one_white
    return float(final @ final), offset


def profile_precision(precision: np.ndarray, observed: np.ndarray, model: np.ndarray) -> tuple[float, float]:
    one = np.ones(observed.size)
    residual = observed - model
    offset = float(one @ precision @ residual / (one @ precision @ one))
    final = residual - offset
    return float(final @ precision @ final), offset


def read_pantheon() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    table = np.genfromtxt(PANTHEON_TABLE, names=True, dtype=None, encoding="utf-8")
    z_all = np.asarray(table["zCMB"], dtype=float)
    observed_all = np.asarray(table["m_b_corr"], dtype=float)
    calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=int)
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


def tail(chi2: float, dof: int) -> dict[str, float | str]:
    lower = float(chi2_dist.cdf(chi2, dof))
    upper = float(chi2_dist.sf(chi2, dof))
    status = "TENSION" if upper < 0.01 else (
        "LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING" if lower < 0.01 else "COMPATIBLE"
    )
    return {"status": status, "dof": dof, "lower_tail_p": lower, "upper_tail_p": upper}


def exact_local_nonidentifiability_witness() -> dict[str, str | bool]:
    # Exact rational G116 two-jet witness. It is local algebra, not a fitted cosmological history.
    zeta = Fraction(3, 100)
    radius = Fraction(1, 100)
    v_rel = Fraction(1, 50)
    dot_v_rel = Fraction(1, 70)
    optical = Fraction(1, 30)
    correction = v_rel * radius + (dot_v_rel - optical / 4) * radius**2
    phi_pure = zeta
    phi_live = zeta - correction
    recovered = phi_live + correction
    return {
        "zeta": str(zeta),
        "phi_pure": str(phi_pure),
        "phi_live": str(phi_live),
        "correction": str(correction),
        "same_frequency_depth": recovered == zeta,
        "inequivalent_terminal_depths": phi_live != phi_pure,
        "sne_curve_uses_zeta_not_either_terminal_depth": True,
    }


def main() -> None:
    hashes = verify_sources()
    g99 = json.loads(G99.read_text())
    g100 = json.loads(G100.read_text())
    if float(g99["calibration"]["n"]).hex() != float(N_FROZEN).hex():
        raise AssertionError("frozen n changed")

    p_z, p_observed, p_cov = read_pantheon()
    p_model, p_zeta, p_screen = retyped_shape(p_z)
    p_legacy = legacy_shape(p_z)
    p_chi2, p_offset = profile_covariance(p_cov, p_observed, p_model)
    g99_offset = 5.0 * math.log10(float(g99["calibration"]["X_eff_Mpc"])) + 25.0 + float(g99["calibration"]["M_B"])

    d_table, d_precision = read_des()
    d_keep = np.flatnonzero(np.asarray(d_table["IDSURVEY"], dtype=float) == 10)
    d_z = np.asarray(d_table["zHD"], dtype=float)[d_keep]
    d_observed = np.asarray(d_table["MU"], dtype=float)[d_keep]
    d_model, d_zeta, d_screen = retyped_shape(d_z)
    d_legacy = legacy_shape(d_z)
    d_cov = marginal_des_covariance(d_precision, d_keep)
    d_chi2, d_offset = profile_covariance(d_cov, d_observed, d_model)
    wrong_chi2, _ = profile_precision(d_precision[np.ix_(d_keep, d_keep)], d_observed, d_model)

    tolerances = {
        "prediction_mag": 1.0e-12,
        "pantheon_chi2": 3.0e-5,
        "pantheon_offset": 3.0e-6,
        "des_chi2": 2.0e-6,
        "des_offset": 2.0e-9,
    }
    differences = {
        "pantheon_prediction_mag": float(np.max(np.abs(p_model - p_legacy))),
        "des_prediction_mag": float(np.max(np.abs(d_model - d_legacy))),
        "pantheon_chi2": abs(p_chi2 - float(g99["calibration"]["chi2"])),
        "pantheon_offset": abs(p_offset - g99_offset),
        "des_chi2": abs(d_chi2 - float(g100["chi2"])),
        "des_offset": abs(d_offset - float(g100["offset_B"])),
    }
    witness = exact_local_nonidentifiability_witness()
    checks = {
        "all_18_source_hashes": len(hashes) == 18 and all(hashes.values()),
        "n_bit_identical": float(g99["calibration"]["n"]).hex() == float(N_FROZEN).hex(),
        "shape_optimizer_not_called": True,
        "pantheon_row_count": p_z.size == int(g99["calibration"]["n_data"]),
        "des_row_count": d_z.size == int(g100["n_data"]),
        "pantheon_prediction_invariant": differences["pantheon_prediction_mag"] <= tolerances["prediction_mag"],
        "des_prediction_invariant": differences["des_prediction_mag"] <= tolerances["prediction_mag"],
        "pantheon_chi2_reproduced": differences["pantheon_chi2"] <= tolerances["pantheon_chi2"],
        "pantheon_offset_reproduced": differences["pantheon_offset"] <= tolerances["pantheon_offset"],
        "des_chi2_reproduced": differences["des_chi2"] <= tolerances["des_chi2"],
        "des_offset_reproduced": differences["des_offset"] <= tolerances["des_offset"],
        "positive_frequency_and_screen": bool(np.all(p_zeta > 0) and np.all(d_zeta > 0) and np.all(p_screen > 0) and np.all(d_screen > 0)),
        "two_terminal_decompositions_same_frequency": bool(witness["same_frequency_depth"] and witness["inequivalent_terminal_depths"]),
        "wrong_des_precision_subblock_detectable": abs(wrong_chi2 - d_chi2) > 1.0,
    }
    passed = all(checks.values())
    result = {
        "schema": "UDT_G117_OPERATIONAL_FREQUENCY_DUAL_SNE_REGRADE_V1",
        "landing": "FROZEN_P1_DUAL_SNE_NUMERICS_PRESERVED_UNDER_CONDITIONAL_RELEASE_COORDINATE_RETYPING__TERMINAL_DECOMPOSITION_STRUCTURALLY_UNIDENTIFIED_ONLY_IN_CURRENT_INTERFACE" if passed else "G117_GATE_FAILURE",
        "all_checks_pass": passed,
        "checks": checks,
        "source_hashes": hashes,
        "frozen_n": N_FROZEN,
        "shape_optimizer_called": False,
        "declared_scope_guards": {
            "release_coordinates": "zCMB and zHD are processed release-redshift coordinates conditionally adopted for the G94 frequency slot; not raw one-ray Z, UDT distances, or G116-derived global coordinates",
            "g116_use": "reject universal phi_pair=zeta and supply one formal local R^2-jet witness only; no extrapolation across the SNe range",
            "nonidentifiability": "structural only in the current conditional P1 release-coordinate interface whose likelihood omits terminal phi and G116 coefficients by construction",
            "g94_regrade": "supersede only G94's conditional Z=exp(phi_pair) identification; retain its independent Wronskian, clock, and conditional-transfer algebra",
            "physical_history_selected": False,
            "transfer_selected": False
        },
        "typed_interface": {
            "observed": "Z_release=1+z_release; processed release coordinate conditionally adopted for the frequency-ratio slot",
            "terminal": "phi_pair=zeta_obs-v_rel*R-[dot(v_rel)-A_opt/4]*R^2+O(R^3); not identified by SNe alone",
            "screen": "D_sky=lambda_A(zeta_obs)*I2; conditional observed chord representative",
            "transfer": "dL=exp(2*zeta_obs)*sqrt(det(D_sky)); conditional",
        },
        "pantheon": {"redshift_column": "zCMB", "n_data": int(p_z.size), "chi2": p_chi2, "offset_B": p_offset, **tail(p_chi2, int(p_z.size - 1))},
        "des": {"redshift_column": "zHD", "n_data": int(d_z.size), "chi2": d_chi2, "offset_B": d_offset, **tail(d_chi2, int(d_z.size - 1)), "hostile_precision_subblock_chi2": wrong_chi2},
        "absolute_differences": differences,
        "local_nonidentifiability_witness": witness,
        "tolerances": tolerances,
        "maximum_conclusion": "frozen P1 dual-SNe numerics are preserved under conditional release-coordinate retyping; terminal decomposition is structurally unidentified only in the current interface; no global G116 history, transfer, or physics is selected",
    }
    (HERE / "PRODUCTION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
