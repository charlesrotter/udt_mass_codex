#!/usr/bin/env python3
"""G278 production: one-scale Cepheid attachment and frozen DES holdout."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DES_ROOT = Path(os.environ["G236_DES_ROOT"]).resolve()
P_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
P_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES_TABLE = DES_ROOT / "DES-Dovekie_HD.csv"
DES_PRECISION = DES_ROOT / "STAT+SYS.npz"
G236_RESULT = ROOT / "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/PRODUCTION_RESULT.json"

K_VALUES = (8, 12, 16, 24)
PRIMARY_K = 12
EXPECTED_P_FLOW = 768
EXPECTED_CAL_ROWS = 77
EXPECTED_CAL_CIDS = 43
EXPECTED_DES = 1623
STATE_REPLAY_TOL = 1.0e-10
SERIALIZATION_TOL_MAG = 1.0e-4
FIVE_SIGMA = 5.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_sources() -> dict[str, bool]:
    mapping = {
        "external_data/DES-Dovekie_HD.csv": DES_TABLE,
        "external_data/STAT+SYS.npz": DES_PRECISION,
    }
    checks: dict[str, bool] = {}
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = mapping.get(row["path"], ROOT / row["path"])
            checks[row["path"]] = path.is_file() and sha256(path) == row["sha256"]
    if not checks or not all(checks.values()):
        raise AssertionError(f"source hash failure: {checks}")
    return checks


def read_pantheon() -> tuple[np.ndarray, dict[str, np.ndarray]]:
    table = np.genfromtxt(P_TABLE, names=True, dtype=None, encoding="utf-8")
    with P_COV.open() as handle:
        dimension = int(handle.readline())
        values = np.fromfile(handle, sep=" ")
    raw = values.reshape(dimension, dimension)
    routes = {
        "symmetric_mean": 0.5 * (raw + raw.T),
        "reflected_lower": np.tril(raw) + np.tril(raw, -1).T,
        "reflected_upper": np.triu(raw) + np.triu(raw, 1).T,
    }
    if len(table) != dimension:
        raise AssertionError((len(table), dimension))
    return table, routes


def read_des() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    names: list[str] | None = None
    rows: list[list[str]] = []
    with DES_TABLE.open() as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("VARNAMES:"):
                names = line.split()[1:]
                continue
            if names is None or not line.startswith("SN:"):
                raise ValueError("unexpected DES table format")
            rows.append(line.split()[1:])
    assert names is not None
    index = {name: i for i, name in enumerate(names)}
    z = np.asarray([float(row[index["zHD"]]) for row in rows], dtype=np.float64)
    mu = np.asarray([float(row[index["MU"]]) for row in rows], dtype=np.float64)
    survey = np.asarray([int(float(row[index["IDSURVEY"]])) for row in rows], dtype=np.int64)
    cid = np.asarray([row[index["CID"]] for row in rows], dtype=str)
    with np.load(DES_PRECISION, allow_pickle=False) as archive:
        dimension = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=np.float64)
    if dimension != len(rows):
        raise AssertionError((dimension, len(rows)))
    precision = np.zeros((dimension, dimension), dtype=np.float64)
    upper = np.triu_indices(dimension)
    precision[upper] = packed
    precision[(upper[1], upper[0])] = packed
    precision = 0.5 * (precision + precision.T)
    keep = np.flatnonzero(survey == 10)
    full_cov = cho_solve(cho_factor(precision, lower=True), np.eye(dimension))
    covariance = full_cov[np.ix_(keep, keep)]
    covariance = 0.5 * (covariance + covariance.T)
    return z[keep], mu[keep], covariance, cid[keep]


def hat_basis(phi: np.ndarray, knots: np.ndarray) -> np.ndarray:
    if np.min(phi) < knots[0] - 1e-13 or np.max(phi) > knots[-1] + 1e-13:
        raise AssertionError("basis extrapolation attempted")
    segment = np.searchsorted(knots, phi, side="right") - 1
    segment = np.clip(segment, 0, knots.size - 2)
    width = knots[segment + 1] - knots[segment]
    right = (phi - knots[segment]) / width
    answer = np.zeros((phi.size, knots.size), dtype=np.float64)
    answer[np.arange(phi.size), segment] = 1.0 - right
    answer[np.arange(phi.size), segment + 1] = right
    return answer


def gls_operator(design: np.ndarray, covariance: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    factor = cho_factor(covariance, lower=True, check_finite=True)
    cinv_design = cho_solve(factor, design, check_finite=True)
    normal = design.T @ cinv_design
    normal_inverse = cho_solve(
        cho_factor(normal, lower=True, check_finite=True), np.eye(normal.shape[0])
    )
    operator = normal_inverse @ cinv_design.T
    return operator, normal_inverse


def state_fit(
    phi: np.ndarray, observed: np.ndarray, covariance: np.ndarray, knots: np.ndarray
) -> dict[str, np.ndarray | float]:
    basis = hat_basis(phi, knots)
    design = np.column_stack([np.ones(phi.size), basis[:, 1:]])
    operator, coefficient_covariance = gls_operator(design, covariance)
    coefficients = operator @ observed
    residual = observed - design @ coefficients
    chi2 = float(residual @ cho_solve(cho_factor(covariance, lower=True), residual))
    return {
        "basis": basis,
        "design": design,
        "operator": operator,
        "coefficients": coefficients,
        "coefficient_covariance": coefficient_covariance,
        "chi2": chi2,
    }


def scale_fit(
    table: np.ndarray,
    covariance: np.ndarray,
    calibrator_indices: np.ndarray,
    flow_indices: np.ndarray,
    flow_intercept_operator: np.ndarray,
    flow_observed: np.ndarray,
) -> dict[str, object]:
    magnitude = np.asarray(table["m_b_corr"], dtype=np.float64)
    cepheid = np.asarray(table["CEPH_DIST"], dtype=np.float64)
    c = magnitude[calibrator_indices] - cepheid[calibrator_indices]
    b_value = float(flow_intercept_operator @ flow_observed)
    q = np.concatenate([c, [b_value]])

    ccc = covariance[np.ix_(calibrator_indices, calibrator_indices)]
    ccf = covariance[np.ix_(calibrator_indices, flow_indices)]
    cross = ccf @ flow_intercept_operator
    variance_b = float(
        flow_intercept_operator
        @ covariance[np.ix_(flow_indices, flow_indices)]
        @ flow_intercept_operator
    )
    reduced_covariance = np.block(
        [[ccc, cross[:, None]], [cross[None, :], np.asarray([[variance_b]])]]
    )
    reduced_covariance = 0.5 * (reduced_covariance + reduced_covariance.T)

    design = np.zeros((q.size, 2), dtype=np.float64)
    design[:, 0] = 1.0
    design[-1, 1] = 1.0
    operator, parameter_covariance = gls_operator(design, reduced_covariance)
    parameters = operator @ q
    residual = q - design @ parameters
    chi2 = float(
        residual
        @ cho_solve(cho_factor(reduced_covariance, lower=True), residual)
    )
    dof = int(q.size - 2)
    ceiling = float(dof + FIVE_SIGMA * math.sqrt(2.0 * dof))
    a_mag = float(parameters[1] - 25.0)
    ell_mpc = float(10.0 ** (a_mag / 5.0))

    # Exact linear weight over the complete Pantheon+ magnitude vector.
    q_operator = np.zeros((q.size, len(table)), dtype=np.float64)
    q_operator[np.arange(calibrator_indices.size), calibrator_indices] = 1.0
    q_operator[-1, flow_indices] = flow_intercept_operator
    parameter_weight = operator @ q_operator
    a_weight = parameter_weight[1]

    eig = np.linalg.eigvalsh(reduced_covariance)
    whitened_design = np.linalg.solve(np.linalg.cholesky(reduced_covariance), design)
    return {
        "M": float(parameters[0]),
        "a_mag": a_mag,
        "ell_mpc": ell_mpc,
        "parameter_covariance": parameter_covariance,
        "a_sigma_mag": float(math.sqrt(parameter_covariance[1, 1])),
        "ell_sigma_mpc_delta": float(
            ell_mpc * math.log(10.0) / 5.0 * math.sqrt(parameter_covariance[1, 1])
        ),
        "chi2_cal": chi2,
        "dof_cal": dof,
        "ceiling_cal": ceiling,
        "calibration_adequate": bool(chi2 <= ceiling),
        "reduced_covariance_min_eigenvalue": float(eig[0]),
        "reduced_covariance_positive_definite": bool(eig[0] > 0.0),
        "weighted_design_rank": int(np.linalg.matrix_rank(whitened_design)),
        "a_weight": a_weight,
        "M_weight": parameter_weight[0],
        "b_value": b_value,
    }


def jsonable(value: object) -> object:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise AssertionError(f"empty TSV: {path}")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    source_checks = verify_sources()
    table, covariance_routes = read_pantheon()
    des_z, des_mu, des_covariance, _ = read_des()
    if des_z.size != EXPECTED_DES:
        raise AssertionError(des_z.size)

    z_all = np.asarray(table["zCMB"], dtype=np.float64)
    magnitude_all = np.asarray(table["m_b_corr"], dtype=np.float64)
    calibrator_all = np.asarray(table["IS_CALIBRATOR"], dtype=np.int64)
    survey_all = np.asarray(table["IDSURVEY"], dtype=np.int64)
    cid_all = np.asarray(table["CID"], dtype=str)
    calibrator_indices = np.flatnonzero(calibrator_all == 1)
    unique_calibrator_cids = sorted(set(cid_all[calibrator_indices]))
    if calibrator_indices.size != EXPECTED_CAL_ROWS or len(unique_calibrator_cids) != EXPECTED_CAL_CIDS:
        raise AssertionError((calibrator_indices.size, len(unique_calibrator_cids)))

    phi_des = np.log1p(des_z)
    phi_min = float(np.min(phi_des))
    phi_max = float(np.max(phi_des))
    flow_mask = (
        (z_all > 0.023)
        & (calibrator_all == 0)
        & (survey_all != 10)
        & (np.log1p(z_all) >= phi_min)
        & (np.log1p(z_all) <= phi_max)
    )
    flow_indices = np.flatnonzero(flow_mask)
    if flow_indices.size != EXPECTED_P_FLOW:
        raise AssertionError(flow_indices.size)
    flow_phi = np.log1p(z_all[flow_indices])
    flow_observed = magnitude_all[flow_indices] - 10.0 * np.log10(1.0 + z_all[flow_indices])

    with G236_RESULT.open() as handle:
        g236 = json.load(handle)

    state_by_route: dict[str, dict[int, dict[str, object]]] = {}
    scale_rows: list[dict[str, object]] = []
    reproduction_errors: list[float] = []
    for route, full_covariance in covariance_routes.items():
        flow_covariance = full_covariance[np.ix_(flow_indices, flow_indices)]
        state_by_route[route] = {}
        for k in K_VALUES:
            knots = np.linspace(phi_min, phi_max, k)
            state = state_fit(flow_phi, flow_observed, flow_covariance, knots)
            coefficients = np.asarray(state["coefficients"])
            intercept_operator = np.asarray(state["operator"])[0]
            scale = scale_fit(
                table,
                full_covariance,
                calibrator_indices,
                flow_indices,
                intercept_operator,
                flow_observed,
            )
            if route == "symmetric_mean":
                frozen = g236["resolutions"][str(k)]["pantheon"]
                error = max(
                    abs(float(coefficients[0]) - float(frozen["offset"])),
                    float(np.max(np.abs(coefficients[1:] - np.asarray(frozen["theta"])))),
                )
                reproduction_errors.append(error)
            else:
                error = math.nan
            state_by_route[route][k] = {
                "knots": knots,
                "state": state,
                "scale": scale,
                "reproduction_error": error,
            }
            scale_rows.append(
                {
                    "covariance_route": route,
                    "K": k,
                    "M": scale["M"],
                    "a_mag": scale["a_mag"],
                    "a_sigma_mag": scale["a_sigma_mag"],
                    "ell_mpc": scale["ell_mpc"],
                    "ell_sigma_mpc_delta": scale["ell_sigma_mpc_delta"],
                    "chi2_cal": scale["chi2_cal"],
                    "dof_cal": scale["dof_cal"],
                    "ceiling_cal": scale["ceiling_cal"],
                    "calibration_adequate": scale["calibration_adequate"],
                    "weighted_design_rank": scale["weighted_design_rank"],
                    "state_reproduction_error": error,
                }
            )

    primary_covariance = covariance_routes["symmetric_mean"]
    mean_states = state_by_route["symmetric_mean"]
    reproduction_pass = bool(max(reproduction_errors) <= STATE_REPLAY_TOL)

    # Exact common-data resolution comparison.
    primary_a_weights = {k: np.asarray(mean_states[k]["scale"]["a_weight"]) for k in K_VALUES}
    resolution_weight = np.vstack(
        [primary_a_weights[k] - primary_a_weights[PRIMARY_K] for k in (8, 16, 24)]
    )
    resolution_difference = np.asarray(
        [
            mean_states[k]["scale"]["a_mag"] - mean_states[PRIMARY_K]["scale"]["a_mag"]
            for k in (8, 16, 24)
        ]
    )
    resolution_covariance = resolution_weight @ primary_covariance @ resolution_weight.T
    resolution_rank = int(np.linalg.matrix_rank(resolution_covariance, tol=1e-12))
    resolution_chi2 = float(
        resolution_difference @ np.linalg.pinv(resolution_covariance, rcond=1e-12) @ resolution_difference
    )
    resolution_ceiling = float(3.0 + FIVE_SIGMA * math.sqrt(6.0))
    resolution_pass = bool(resolution_rank == 3 and resolution_chi2 <= resolution_ceiling)

    # Exact calibrator-subset controls at K=12.
    primary_state = mean_states[PRIMARY_K]["state"]
    primary_intercept_operator = np.asarray(primary_state["operator"])[0]
    primary_scale = mean_states[PRIMARY_K]["scale"]
    subset_specs: list[tuple[str, set[str]]] = [
        ("all", set(unique_calibrator_cids)),
        ("even_sorted_cids", set(unique_calibrator_cids[0::2])),
        ("odd_sorted_cids", set(unique_calibrator_cids[1::2])),
    ]
    subset_specs.extend(
        (f"leave_out_{cid}", set(unique_calibrator_cids) - {cid})
        for cid in unique_calibrator_cids
    )
    subset_rows: list[dict[str, object]] = []
    subset_pass = True
    for name, included_cids in subset_specs:
        subset_indices = calibrator_indices[
            np.asarray([cid_all[index] in included_cids for index in calibrator_indices])
        ]
        subset_scale = scale_fit(
            table,
            primary_covariance,
            subset_indices,
            flow_indices,
            primary_intercept_operator,
            flow_observed,
        )
        difference = float(subset_scale["a_mag"] - primary_scale["a_mag"])
        difference_weight = np.asarray(subset_scale["a_weight"]) - np.asarray(primary_scale["a_weight"])
        variance_difference = float(difference_weight @ primary_covariance @ difference_weight)
        sigma_difference = math.sqrt(max(variance_difference, 0.0))
        z_difference = abs(difference) / sigma_difference if sigma_difference > 0.0 else 0.0
        passes = bool(
            subset_scale["weighted_design_rank"] == 2
            and subset_scale["reduced_covariance_positive_definite"]
            and z_difference <= FIVE_SIGMA
        )
        if name != "all":
            subset_pass = subset_pass and passes
        subset_rows.append(
            {
                "subset": name,
                "calibrator_rows": int(subset_indices.size),
                "unique_cids": len(included_cids),
                "a_mag": subset_scale["a_mag"],
                "ell_mpc": subset_scale["ell_mpc"],
                "difference_from_all_mag": difference,
                "difference_sigma_mag": sigma_difference,
                "absolute_z": z_difference,
                "passes": passes,
            }
        )

    # Serialization route control.
    serialization_differences: list[float] = []
    for route in ("reflected_lower", "reflected_upper"):
        for k in K_VALUES:
            serialization_differences.append(
                abs(
                    float(state_by_route[route][k]["scale"]["a_mag"])
                    - float(mean_states[k]["scale"]["a_mag"])
                )
            )
    max_serialization_difference = max(serialization_differences)
    serialization_pass = bool(max_serialization_difference <= SERIALIZATION_TOL_MAG)

    # No-retuning DES score with full Pantheon prediction covariance.
    des_rows: list[dict[str, object]] = []
    des_results: dict[int, dict[str, object]] = {}
    for k in K_VALUES:
        item = mean_states[k]
        knots = np.asarray(item["knots"])
        state = item["state"]
        scale = item["scale"]
        theta = np.asarray(state["coefficients"])[1:]
        des_basis = hat_basis(phi_des, knots)[:, 1:]
        prediction = (
            25.0
            + float(scale["a_mag"])
            + 10.0 * np.log10(1.0 + des_z)
            + des_basis @ theta
        )
        theta_weight = np.zeros((k - 1, len(table)), dtype=np.float64)
        theta_weight[:, flow_indices] = np.asarray(state["operator"])[1:]
        joint_weight = np.vstack([np.asarray(scale["a_weight"]), theta_weight])
        joint_covariance = joint_weight @ primary_covariance @ joint_weight.T
        prediction_design = np.column_stack([np.ones(des_z.size), des_basis])
        prediction_covariance = prediction_design @ joint_covariance @ prediction_design.T
        total_covariance = des_covariance + prediction_covariance
        total_covariance = 0.5 * (total_covariance + total_covariance.T)
        residual = des_mu - prediction
        chi2 = float(residual @ cho_solve(cho_factor(total_covariance, lower=True), residual))
        dof = int(des_z.size)
        ceiling = float(dof + FIVE_SIGMA * math.sqrt(2.0 * dof))
        adequate = bool(chi2 <= ceiling)
        des_results[k] = {
            "chi2": chi2,
            "dof": dof,
            "ceiling": ceiling,
            "adequate": adequate,
            "residual_mean_mag": float(np.mean(residual)),
            "residual_rms_mag": float(np.sqrt(np.mean(residual**2))),
            "prediction_min": float(np.min(prediction)),
            "prediction_max": float(np.max(prediction)),
        }
        des_rows.append({"K": k, **des_results[k]})

    primary_calibration_pass = bool(
        all(
            mean_states[k]["scale"]["reduced_covariance_positive_definite"]
            and mean_states[k]["scale"]["weighted_design_rank"] == 2
            and mean_states[k]["scale"]["ell_mpc"] > 0.0
            and mean_states[k]["scale"]["calibration_adequate"]
            for k in K_VALUES
        )
    )

    if not reproduction_pass:
        landing = "REGRESSION_OR_IMPLEMENTATION_FAILURE"
    elif not primary_calibration_pass:
        landing = "PANTHEONPLUS_CEPHEID_SCALE_ATTACHMENT_INADEQUATE"
    elif not (resolution_pass and subset_pass and serialization_pass):
        landing = "SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE"
    elif des_results[PRIMARY_K]["adequate"]:
        landing = "CONDITIONAL_ONE_SCALE_ATTACHED__DES_NO_RETUNING_CHECK_ADEQUATE"
    else:
        landing = "CONDITIONAL_ONE_SCALE_ATTACHED__DES_PUBLISHED_NORMALIZATION_MISMATCH"

    result = {
        "audit": "G278_PRODUCTION",
        "landing": landing,
        "maximum_conclusion": "one conditional empirical homothety scale for the frozen G236 state plus a no-retuning DES consistency or mismatch under its published normalization",
        "source_checks": source_checks,
        "counts": {
            "pantheon_total": int(len(table)),
            "pantheon_flow": int(flow_indices.size),
            "calibrator_rows": int(calibrator_indices.size),
            "calibrator_unique_cids": len(unique_calibrator_cids),
            "des_holdout": int(des_z.size),
        },
        "frozen": {
            "phi_min": phi_min,
            "phi_max": phi_max,
            "K_values": list(K_VALUES),
            "primary_K": PRIMARY_K,
            "kernel_retuned": False,
            "state_shape_retuned_by_calibrators": False,
            "DES_parameters_fitted": 0,
            "P1_used": False,
            "angular_coefficients_fitted": 0,
            "Xmax_used": False,
            "lcdm_distance_used": False,
            "transparent_transfer_imported": True,
        },
        "gates": {
            "g236_reproduction_pass": reproduction_pass,
            "max_g236_reproduction_error": max(reproduction_errors),
            "primary_calibration_pass": primary_calibration_pass,
            "resolution_pass": resolution_pass,
            "resolution_rank": resolution_rank,
            "resolution_chi2": resolution_chi2,
            "resolution_ceiling": resolution_ceiling,
            "subset_pass": subset_pass,
            "serialization_pass": serialization_pass,
            "max_serialization_difference_mag": max_serialization_difference,
            "primary_DES_pass": des_results[PRIMARY_K]["adequate"],
        },
        "primary_scale": {
            key: value
            for key, value in primary_scale.items()
            if key not in {"a_weight", "M_weight", "parameter_covariance"}
        },
        "primary_scale_parameter_covariance": primary_scale["parameter_covariance"],
        "resolution": {
            "difference_mag": resolution_difference,
            "covariance": resolution_covariance,
        },
        "DES": des_results,
        "conditionality": {
            "cepheid_distance_ladder": "OBSERVED_SUPPLIED",
            "transparent_radiative_transfer": "CONDITIONAL_IMPORT",
            "DES_H0_70_normalization": "OBSERVED_RELEASE_CONVENTION_NOT_UDT_SCALE",
            "CMB_temperature_used": False,
        },
    }

    with (PACKAGE / "DERIVATION_RESULT.json").open("w") as handle:
        json.dump(jsonable(result), handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_tsv(PACKAGE / "SCALE_RESULTS.tsv", scale_rows)
    write_tsv(PACKAGE / "CALIBRATOR_SUBSET_CONTROLS.tsv", subset_rows)
    write_tsv(PACKAGE / "DES_HOLDOUT_RESULTS.tsv", des_rows)

    run_summary = json.dumps(jsonable({
        "landing": landing,
        "primary_scale": result["primary_scale"],
        "gates": result["gates"],
        "primary_DES": des_results[PRIMARY_K],
    }), indent=2, sort_keys=True)
    (PACKAGE / "PRODUCTION_RUN_LOG.txt").write_text(
        "COMMAND: G236_DES_ROOT=<declared scratch data root> python3 derive_scale_and_holdout.py\n"
        + run_summary
        + "\n"
    )
    print(run_summary)


if __name__ == "__main__":
    main()
