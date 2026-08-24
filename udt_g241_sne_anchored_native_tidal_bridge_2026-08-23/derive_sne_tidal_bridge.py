#!/usr/bin/env python3
"""Evaluate the preregistered G241 SNe carrier and native tidal bridge."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from numpy.polynomial import chebyshev as cheb
from scipy.stats import chi2 as chi2_dist


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
STATE_PATH = REPO / "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23" / "FROZEN_PRIMARY_K12_STATE.json"
STATE_SHA256 = "88d3006a646f2be105a3fb15f2c4c694732b884da97f8fdeefc39323e6bbc8cf"
CANDIDATE_DEGREES = (2, 3, 4)
ADEQUACY_QUANTILE = 0.999
SLOPE_TOLERANCE = 1.0e-10
DENSE_GRID_SIZE = 2001


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_frozen_state() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    assert sha256(STATE_PATH) == STATE_SHA256, "frozen G237 state hash mismatch"
    payload = json.loads(STATE_PATH.read_text())
    assert payload["freeze"] == "G237_PRIMARY_K12_RELATIVE_STATE__NO_REFIT_ON_HELDOUT_QUERY"
    state = payload["state"]
    knots = np.asarray(state["knots"], dtype=np.float64)
    theta = np.asarray(state["theta"], dtype=np.float64)
    covariance = np.asarray(state["theta_covariance"], dtype=np.float64)
    assert knots.shape == (12,)
    assert theta.shape == (11,)
    assert covariance.shape == (11, 11)
    assert np.all(np.diff(knots) > 0.0)
    assert np.allclose(covariance, covariance.T, rtol=0.0, atol=1.0e-15)
    np.linalg.cholesky(covariance)
    return knots, theta, covariance


def normalized_depth(phi: np.ndarray | float, phi_lo: float, phi_hi: float) -> np.ndarray:
    return 2.0 * (np.asarray(phi, dtype=np.float64) - phi_lo) / (phi_hi - phi_lo) - 1.0


def anchored_basis(t: np.ndarray, degree: int) -> np.ndarray:
    vandermonde = cheb.chebvander(t, degree)[:, 1:]
    anchor = np.asarray([(-1.0) ** k for k in range(1, degree + 1)])
    return vandermonde - anchor[None, :]


def full_cheb_coefficients(coefficients: np.ndarray) -> np.ndarray:
    degree = coefficients.size
    full = np.zeros(degree + 1, dtype=np.float64)
    full[1:] = coefficients
    full[0] = -sum(coefficients[k - 1] * ((-1.0) ** k) for k in range(1, degree + 1))
    return full


def derivative_candidates(full: np.ndarray, phi_lo: float, phi_hi: float) -> np.ndarray:
    second_t = cheb.chebder(full, 2)
    roots = [] if second_t.size <= 1 else cheb.chebroots(second_t)
    points = [-1.0, 1.0]
    for root in roots:
        if abs(root.imag) <= 1.0e-11 and -1.0 <= root.real <= 1.0:
            points.append(float(root.real))
    return np.asarray(sorted(set(points)), dtype=np.float64)


def evaluate_history(full_theta: np.ndarray, phi: np.ndarray, phi_lo: float, phi_hi: float) -> dict[str, np.ndarray]:
    t = normalized_depth(phi, phi_lo, phi_hi)
    dt_dphi = 2.0 / (phi_hi - phi_lo)
    log_factor = np.log(10.0) / 5.0
    theta = cheb.chebval(t, full_theta)
    theta_t = cheb.chebval(t, cheb.chebder(full_theta, 1))
    theta_tt = cheb.chebval(t, cheb.chebder(full_theta, 2))
    s = log_factor * theta
    s_prime = log_factor * theta_t * dt_dphi
    s_second = log_factor * theta_tt * dt_dphi**2
    p = 1.0 / s_prime
    q = -(s_second + s_prime**2) / s_prime**3
    exp_minus_2phi = np.exp(-2.0 * phi)
    tidal_j = exp_minus_2phi * (2.0 * p**2 - q + 2.0 * p) - (1.0 - exp_minus_2phi)
    return {
        "theta": theta,
        "s": s,
        "s_prime": s_prime,
        "s_second": s_second,
        "p": p,
        "q": q,
        "tidal_J": tidal_j,
    }


def scale_invariance_residual(history: dict[str, np.ndarray], phi: np.ndarray) -> float:
    s = history["s"]
    s_prime = history["s_prime"]
    s_second = history["s_second"]
    target = history["tidal_J"]
    residual = 0.0
    for scale in (0.125, 1.0, 8.0):
        radius = scale * np.exp(s)
        radius_prime = radius * s_prime
        radius_second = radius * (s_second + s_prime**2)
        phi_prime = 1.0 / radius_prime
        phi_second = -radius_second / radius_prime**3
        xi = np.exp(-2.0 * phi) * (
            2.0 * phi_prime**2 - phi_second + 2.0 * phi_prime / radius
        ) - (1.0 - np.exp(-2.0 * phi)) / radius**2
        direct = radius**2 * xi
        residual = max(residual, float(np.max(np.abs(direct - target))))
    return residual


def fit_candidate(degree: int, knots: np.ndarray, theta: np.ndarray, covariance: np.ndarray) -> dict:
    phi_lo = float(knots[0])
    phi_hi = float(knots[-1])
    t_data = normalized_depth(knots[1:], phi_lo, phi_hi)
    basis = anchored_basis(t_data, degree)
    precision_basis = np.linalg.solve(covariance, basis)
    precision_theta = np.linalg.solve(covariance, theta)
    normal = basis.T @ precision_basis
    np.linalg.cholesky(normal)
    coefficient_covariance = np.linalg.inv(normal)
    coefficients = np.linalg.solve(normal, basis.T @ precision_theta)
    residual = theta - basis @ coefficients
    chi2 = float(residual @ np.linalg.solve(covariance, residual))
    dof = int(theta.size - degree)
    ceiling = float(chi2_dist.ppf(ADEQUACY_QUANTILE, dof))
    full = full_cheb_coefficients(coefficients)

    stationary_t = derivative_candidates(full, phi_lo, phi_hi)
    stationary_phi = phi_lo + 0.5 * (stationary_t + 1.0) * (phi_hi - phi_lo)
    stationary_history = evaluate_history(full, stationary_phi, phi_lo, phi_hi)
    slope_index = int(np.argmin(stationary_history["s_prime"]))
    slope_min = float(stationary_history["s_prime"][slope_index])
    slope_location = float(stationary_phi[slope_index])

    dense_phi = np.linspace(phi_lo, phi_hi, DENSE_GRID_SIZE)
    dense = evaluate_history(full, dense_phi, phi_lo, phi_hi)
    finite = bool(all(np.all(np.isfinite(values)) for values in dense.values()))
    scale_residual = scale_invariance_residual(dense, dense_phi)
    adequate = bool(chi2 <= ceiling)
    monotone = bool(slope_min > SLOPE_TOLERANCE)
    passed = bool(adequate and monotone and finite)

    knot_history = evaluate_history(full, knots, phi_lo, phi_hi)
    return {
        "degree": degree,
        "coefficients_theta_units": coefficients.tolist(),
        "coefficient_covariance": coefficient_covariance.tolist(),
        "chi2": chi2,
        "dof": dof,
        "chi2_quantile": ADEQUACY_QUANTILE,
        "chi2_ceiling": ceiling,
        "adequate": adequate,
        "minimum_s_prime": slope_min,
        "minimum_s_prime_phi": slope_location,
        "monotone_invertible": monotone,
        "finite_dense_grid": finite,
        "scale_invariance_max_abs_residual": scale_residual,
        "passed": passed,
        "knot_theta_model": knot_history["theta"].tolist(),
        "knot_relative_R_model": np.exp(knot_history["s"]).tolist(),
        "knot_s_prime": knot_history["s_prime"].tolist(),
        "knot_s_second": knot_history["s_second"].tolist(),
        "knot_p": knot_history["p"].tolist(),
        "knot_q": knot_history["q"].tolist(),
        "knot_tidal_J": knot_history["tidal_J"].tolist(),
        "dense_tidal_J_min": float(np.min(dense["tidal_J"])),
        "dense_tidal_J_max": float(np.max(dense["tidal_J"])),
    }


def derive() -> dict:
    knots, theta, covariance = load_frozen_state()
    candidates = [fit_candidate(degree, knots, theta, covariance) for degree in CANDIDATE_DEGREES]
    selected = next((candidate for candidate in candidates if candidate["passed"]), None)
    if selected is None:
        landing = "NO_REGISTERED_SMOOTH_ANCHOR_ADEQUATE__STOP_BEFORE_BOSS"
    else:
        landing = f"D{selected['degree']}_SNE_ANCHOR_ADEQUATE__NATIVE_TIDAL_BRIDGE_FROZEN"
    return {
        "package": "G241",
        "status": "OBSERVED_CALIBRATION_PLUS_DERIVED_CONDITIONAL_TIDAL_BRIDGE",
        "landing": landing,
        "boss_outcomes_opened": False,
        "state_sha256": STATE_SHA256,
        "candidate_degrees": list(CANDIDATE_DEGREES),
        "selection_rule": "smallest_degree_passing_all_preregistered_gates",
        "selected_degree": None if selected is None else selected["degree"],
        "absolute_radial_scale": "OPEN_AND_CANCELS_FROM_TIDAL_J",
        "angular_fit_coefficient": None,
        "candidates": candidates,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        expected = (PACKAGE / "DERIVATION_RESULT.json").read_text()
        assert rendered == expected, "no-write replay differs from frozen production result"
    else:
        (PACKAGE / "DERIVATION_RESULT.json").write_text(rendered)
    print(result["landing"])
    for candidate in result["candidates"]:
        print(
            f"d={candidate['degree']} chi2={candidate['chi2']:.12g}/"
            f"{candidate['chi2_ceiling']:.12g} slope_min={candidate['minimum_s_prime']:.12g} "
            f"pass={candidate['passed']}"
        )


if __name__ == "__main__":
    main()
