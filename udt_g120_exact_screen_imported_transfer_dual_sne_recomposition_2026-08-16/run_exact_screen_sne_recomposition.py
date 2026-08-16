#!/usr/bin/env python3
"""G120 production: exact G119 screen plus imported transparent transfer, no refit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.linalg import cho_factor, cho_solve, solve_triangular
from scipy.stats import chi2 as chi2_dist


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PANTHEON_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
PANTHEON_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES_ROOT = Path("/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT")
G99 = ROOT / "udt_observed_middle_regime_pair_calibration_2026-08-15/CALIBRATION_CONTRACT.json"
G117 = ROOT / "udt_g117_operational_frequency_dual_sne_regrade_2026-08-16/PRODUCTION_RESULT.json"
N_FROZEN = 1.0559332414320268


def sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            result.update(chunk)
    return result.hexdigest()


def verify_sources() -> dict[str, bool]:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks: dict[str, bool] = {}
    for row in rows:
        path = Path(row["path"])
        if not path.is_absolute():
            path = ROOT / path
        checks[row["path"]] = path.is_file() and sha256(path) == row["sha256"]
    if len(rows) != 15 or not all(checks.values()):
        raise RuntimeError("G120 source integrity failure")
    return checks


def radius_shape(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return N_FROZEN * (-np.expm1(-2.0 * np.log(scale) / N_FROZEN))


def recomposed_magnitude_shape(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    radius = radius_shape(z)
    transfer = 1.0 / scale
    luminosity_distance = np.sqrt(scale**3 * radius**2 / transfer)
    return 5.0 * np.log10(luminosity_distance)


def frozen_g117_shape(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return 5.0 * np.log10(N_FROZEN * scale**2 * (1.0 - scale ** (-2.0 / N_FROZEN)))


def wrong_t_equal_one_shape(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    return 5.0 * np.log10(scale**1.5 * radius_shape(z))


def profile_covariance(covariance: np.ndarray, observed: np.ndarray, model: np.ndarray) -> tuple[float, float]:
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


def main() -> None:
    hashes = verify_sources()
    g99 = json.loads(G99.read_text())
    g117 = json.loads(G117.read_text())
    x_eff = float(g99["calibration"]["X_eff_Mpc"])
    if float(g99["calibration"]["n"]).hex() != float(N_FROZEN).hex():
        raise AssertionError("frozen n changed")

    p_z, p_observed, p_cov = read_pantheon()
    p_model = recomposed_magnitude_shape(p_z)
    p_reference = frozen_g117_shape(p_z)
    p_chi2, p_offset = profile_covariance(p_cov, p_observed, p_model)
    p_wrong = wrong_t_equal_one_shape(p_z)
    p_wrong_chi2, _ = profile_covariance(p_cov, p_observed, p_wrong)

    d_table, d_precision = read_des()
    d_keep = np.flatnonzero(np.asarray(d_table["IDSURVEY"], dtype=float) == 10)
    d_z = np.asarray(d_table["zHD"], dtype=float)[d_keep]
    d_observed = np.asarray(d_table["MU"], dtype=float)[d_keep]
    d_model = recomposed_magnitude_shape(d_z)
    d_reference = frozen_g117_shape(d_z)
    d_cov = marginal_des_covariance(d_precision, d_keep)
    d_chi2, d_offset = profile_covariance(d_cov, d_observed, d_model)
    d_wrong = wrong_t_equal_one_shape(d_z)
    d_wrong_chi2, _ = profile_covariance(d_cov, d_observed, d_wrong)

    sample_scale = np.geomspace(1.000001, 1000.0, 4096)
    sample_radius = N_FROZEN * (1.0 - sample_scale ** (-2.0 / N_FROZEN))
    imported_transfer = 1.0 / sample_scale
    general_factorization = np.sqrt(sample_scale**3 * sample_radius**2 / imported_transfer)
    exact_reduction = sample_scale**2 * sample_radius
    z_symbol, r_symbol = sp.symbols("Z R", positive=True)
    symbolic_factorization = sp.simplify(
        sp.sqrt(z_symbol**3 * r_symbol**2 / (1 / z_symbol)) - z_symbol**2 * r_symbol
    )
    n_symbol, x_symbol = sp.symbols("n X_eff", positive=True)
    symbolic_radius = n_symbol * x_symbol * (1 - z_symbol ** (-2 / n_symbol))
    symbolic_derivative = sp.simplify(
        sp.diff(symbolic_radius, z_symbol)
        - 2 * x_symbol * z_symbol ** (-2 / n_symbol - 1)
    )
    symbolic_origin_slope = sp.simplify(
        sp.diff(symbolic_radius, z_symbol).subs(z_symbol, 1) - 2 * x_symbol
    )
    symbolic_radius_limit = sp.simplify(
        sp.limit(symbolic_radius, z_symbol, sp.oo) - n_symbol * x_symbol
    )

    node_residuals = []
    radius_nodes = []
    for node in g99["nodes"]:
        z = float(node["z"])
        radius = float(x_eff * radius_shape(np.array([z]))[0])
        residual = abs(radius - float(node["r_cal_Mpc"]))
        node_residuals.append(residual)
        radius_nodes.append({"z": z, "Z": 1.0 + z, "R_conditional_Mpc": radius,
                             "fraction_of_formal_P1_asymptote": radius / (N_FROZEN * x_eff)})

    differences = {
        "pantheon_curve_mag": float(np.max(np.abs(p_model - p_reference))),
        "des_curve_mag": float(np.max(np.abs(d_model - d_reference))),
        "pantheon_chi2": abs(p_chi2 - float(g117["pantheon"]["chi2"])),
        "pantheon_offset": abs(p_offset - float(g117["pantheon"]["offset_B"])),
        "des_chi2": abs(d_chi2 - float(g117["des"]["chi2"])),
        "des_offset": abs(d_offset - float(g117["des"]["offset_B"])),
        "factorization": float(np.max(np.abs(general_factorization - exact_reduction))),
        "g99_radius_nodes_Mpc": float(max(node_residuals)),
    }
    hostile = {
        "replacement": "T=1 instead of imported T=1/Z",
        "pantheon_nonconstant_mag_range": float(np.ptp(p_wrong - p_model)),
        "des_nonconstant_mag_range": float(np.ptp(d_wrong - d_model)),
        "pantheon_profile_chi2": p_wrong_chi2,
        "des_profile_chi2": d_wrong_chi2,
        "caught": bool(np.ptp(p_wrong - p_model) > 0.1 and np.ptp(d_wrong - d_model) > 0.1),
    }
    tolerances = {
        "curve_mag": 1e-12,
        "pantheon_chi2": 3e-5,
        "pantheon_offset": 3e-6,
        "des_chi2": 2e-6,
        "des_offset": 2e-9,
        "radius_nodes_Mpc": 1e-9,
    }
    derivative_sample = 2.0 * x_eff * sample_scale ** (-2.0 / N_FROZEN - 1.0)
    checks = {
        "all_15_source_hashes": len(hashes) == 15 and all(hashes.values()),
        "n_bit_identical": float(g99["calibration"]["n"]).hex() == float(N_FROZEN).hex(),
        "shape_optimizer_not_called": True,
        "pantheon_count": p_z.size == 1367,
        "des_count": d_z.size == 1623,
        "catalog_domain_Z_strictly_greater_than_one": bool(
            np.all(1.0 + p_z > 1.0) and np.all(1.0 + d_z > 1.0)
        ),
        "g94_g119_transfer_reduces_to_Z2R": symbolic_factorization == 0,
        "pantheon_curve_preserved": differences["pantheon_curve_mag"] <= tolerances["curve_mag"],
        "des_curve_preserved": differences["des_curve_mag"] <= tolerances["curve_mag"],
        "pantheon_chi2_preserved": differences["pantheon_chi2"] <= tolerances["pantheon_chi2"],
        "pantheon_offset_preserved": differences["pantheon_offset"] <= tolerances["pantheon_offset"],
        "des_chi2_preserved": differences["des_chi2"] <= tolerances["des_chi2"],
        "des_offset_preserved": differences["des_offset"] <= tolerances["des_offset"],
        "g99_radius_nodes_reproduced": differences["g99_radius_nodes_Mpc"] <= tolerances["radius_nodes_Mpc"],
        "radius_zero_at_Z1": radius_shape(np.array([0.0]))[0] == 0.0,
        "radius_derivative_identity": symbolic_derivative == 0,
        "radius_strictly_increasing": symbolic_derivative == 0 and bool(np.all(derivative_sample > 0.0)),
        "origin_slope_equals_2_Xeff": symbolic_origin_slope == 0,
        "formal_asymptote_identity": symbolic_radius_limit == 0,
        "formal_asymptote_reproduces_G99_value": math.isclose(N_FROZEN * x_eff, float(g99["calibration"]["R_w_Mpc_at_joint_best"]), rel_tol=0.0, abs_tol=1e-12),
        "hostile_T_equal_one_caught": hostile["caught"],
    }
    checks = {key: bool(value) for key, value in checks.items()}
    passed = all(checks.values())
    result = {
        "schema": "UDT_G120_EXACT_SCREEN_IMPORTED_TRANSFER_DUAL_SNE_V1",
        "landing": "CONDITIONAL_RADIUS_FREQUENCY_RECOMPOSITION_PRESERVES_DUAL_SNE" if passed else "G120_GATE_FAILURE",
        "all_checks_pass": passed,
        "checks": checks,
        "source_hashes": hashes,
        "pins": {
            "metric_derived": "G119 d_A=R on the declared central-spherical radial point-observer class",
            "imported_conditional": "eta=1 and epsilon=1/Z, hence transfer product T=1/Z",
            "observed_conditional": "processed zCMB/zHD frequency slots and frozen P1 n/X_eff",
            "LambdaCDM_distance_used": False,
        },
        "domain": {
            "conditional_radius_curve": "outgoing catalog orientation Z>=1; evaluated rows have Z>1",
            "reverse_or_blueshift_queries": "not represented by extending R_P1 into 0<Z<1",
        },
        "equations": {
            "general": "d_L^2=Z^3 R^2/(eta epsilon)",
            "import": "eta epsilon=1/Z",
            "reduced": "d_L=Z^2 R",
            "conditional_radius": "R_P1(Z)=n X_eff [1-Z^(-2/n)]",
            "origin_slope": "dR/dz at z=0 equals 2 X_eff",
            "formal_family_limit": "R_P1 tends to n X_eff as Z tends to infinity; this is not X_max",
        },
        "frozen_n": N_FROZEN,
        "conditional_X_eff_Mpc": x_eff,
        "formal_P1_radius_limit_Mpc": N_FROZEN * x_eff,
        "radius_nodes": radius_nodes,
        "pantheon": {"redshift_column": "zCMB", "n_data": int(p_z.size), "chi2": p_chi2,
                      "offset_B": p_offset, **tail(p_chi2, int(p_z.size - 1))},
        "des": {"redshift_column": "zHD", "n_data": int(d_z.size), "chi2": d_chi2,
                 "offset_B": d_offset, **tail(d_chi2, int(d_z.size - 1))},
        "absolute_differences": differences,
        "symbolic_factorization_residual": str(symbolic_factorization),
        "symbolic_radius_residuals": {
            "derivative": str(symbolic_derivative),
            "origin_slope": str(symbolic_origin_slope),
            "formal_limit": str(symbolic_radius_limit),
        },
        "hostile_transfer_check": hostile,
        "tolerances": tolerances,
        "shape_optimizer_called": False,
        "maximum_conclusion": "with G119 d_A=R and explicitly imported transparent null-momentum transfer, the frozen dual-SNe luminosity relation is exactly one conditional empirical areal-radius-versus-frequency curve; no native light theory, complete physical metric history, terminal depth, X_max, or downstream cosmology is selected",
    }
    (HERE / "PRODUCTION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
