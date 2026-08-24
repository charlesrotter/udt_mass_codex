#!/usr/bin/env python3
"""Production G242 exact quiet-subfamily comparison."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.stats import chi2 as chi2_distribution


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
STATE_PATH = ROOT / "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23" / "FROZEN_PRIMARY_K12_STATE.json"
MANIFEST_PATH = PACKAGE / "SOURCE_MANIFEST.tsv"
OUTPUT_PATH = PACKAGE / "DERIVATION_RESULT.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def preregistration_registry_digest(path: Path) -> str:
    """Retain preregistration lineage after the append-only G243 and G242 banks."""
    lines = path.read_bytes().splitlines(keepends=True)
    g242_rows = [line for line in lines if line.startswith(b"G242\t")]
    g243_rows = [line for line in lines if line.startswith(b"G243\t")]
    if not g242_rows and not g243_rows:
        return sha256(path)
    if len(g242_rows) > 1 or len(g243_rows) > 1:
        raise RuntimeError("registry may contain at most one G242 row and one G243 row")
    historical = b"".join(
        line for line in lines if not line.startswith((b"G242\t", b"G243\t"))
    )
    return hashlib.sha256(historical).hexdigest()


def verify_manifest() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
    if lines[0] != "sha256\tpath\trole":
        raise RuntimeError("unexpected manifest header")
    for line in lines[1:]:
        expected, relative, role = line.split("\t")
        source = ROOT / relative
        actual = (
            preregistration_registry_digest(source)
            if relative == "CURRENT_SCIENTIFIC_PREMISES.tsv"
            else sha256(source)
        )
        if actual != expected:
            raise RuntimeError(f"source hash mismatch: {relative}")
        rows.append({"path": relative, "role": role, "sha256": actual})
    return rows


def quiet_theta(phi: np.ndarray, phi_anchor: float) -> np.ndarray:
    numerator = -np.expm1(-2.0 * phi)
    denominator = -math.expm1(-2.0 * phi_anchor)
    if np.any(numerator <= 0.0) or denominator <= 0.0:
        raise ValueError("quiet positive-depth branch requires positive 1-exp(-2 phi)")
    return 2.5 * np.log10(numerator / denominator)


def quiet_differential_state(phi: np.ndarray) -> dict[str, np.ndarray]:
    exp2 = np.exp(2.0 * phi)
    p = exp2 - 1.0
    s_prime = 1.0 / p
    s_second = -2.0 * exp2 / (p * p)
    q = -(s_second + s_prime * s_prime) / (s_prime**3)
    exp_minus2 = np.exp(-2.0 * phi)
    tidal = exp_minus2 * (2.0 * p * p - q + 2.0 * p) - (1.0 - exp_minus2)
    return {
        "s_prime": s_prime,
        "s_second": s_second,
        "p": p,
        "q": q,
        "J": tidal,
    }


def full_covariance_chi2(residual: np.ndarray, covariance: np.ndarray) -> float:
    factor = cho_factor(covariance, lower=True, check_finite=True)
    solved = cho_solve(factor, residual, check_finite=True)
    return float(residual @ solved)


def evaluate(*, covariance_mode: str = "full", model_mode: str = "native") -> dict[str, object]:
    manifest = verify_manifest()
    state_document = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    state = state_document["state"]
    knots = np.asarray(state["knots"], dtype=np.float64)
    observed = np.asarray(state["theta"], dtype=np.float64)
    covariance = np.asarray(state["theta_covariance"], dtype=np.float64)
    if knots.shape != (12,) or observed.shape != (11,) or covariance.shape != (11, 11):
        raise RuntimeError("unexpected frozen G237 state shape")
    if covariance_mode == "diagonal":
        covariance = np.diag(np.diag(covariance))
    elif covariance_mode != "full":
        raise ValueError("unsupported covariance mode")

    phi_anchor = float(knots[0])
    if model_mode == "native":
        predicted = quiet_theta(knots[1:], phi_anchor)
    elif model_mode == "wrong_plus_sign":
        numerator = 1.0 + np.exp(-2.0 * knots[1:])
        denominator = 1.0 + math.exp(-2.0 * phi_anchor)
        predicted = 2.5 * np.log10(numerator / denominator)
    else:
        raise ValueError("unsupported model mode")

    residual = observed - predicted
    covariance_eigenvalues = np.linalg.eigvalsh(covariance)
    if float(covariance_eigenvalues[0]) <= 0.0:
        raise RuntimeError("frozen covariance is not positive definite")
    chi2 = full_covariance_chi2(residual, covariance)
    dof = int(observed.size)
    ceiling = float(chi2_distribution.ppf(0.999, dof))

    grid = np.linspace(float(knots[0]), float(knots[-1]), 4097, dtype=np.float64)
    differential = quiet_differential_state(grid)
    scale_errors: dict[str, float] = {}
    base_radius = np.sqrt(-np.expm1(-2.0 * grid))
    base_state = np.log(base_radius / base_radius[0])
    for scale in (0.125, 1.0, 7.5, 1.0e6):
        scaled_state = np.log((scale * base_radius) / (scale * base_radius[0]))
        scale_errors[str(scale)] = float(np.max(np.abs(scaled_state - base_state)))

    classification = (
        "EXACT_QUIET_SUBFAMILY_COMPATIBLE_WITH_FROZEN_SNE_STATE"
        if chi2 <= ceiling
        else "EXACT_QUIET_SUBFAMILY_INCOMPATIBLE__SMALL_NONZERO_RESPONSE_REMAINS_OPEN"
    )
    return {
        "classification": classification,
        "scope": "G237_K12_POSITIVE_DEPTH_STATIC_CENTRAL_IMPORTED_TRANSFER_CONDITIONAL",
        "boss_outcomes": "CLOSED_AND_UNREAD",
        "covariance_mode": covariance_mode,
        "model_mode": model_mode,
        "manifest": manifest,
        "phi_anchor": phi_anchor,
        "phi_max": float(knots[-1]),
        "observed_theta": observed.tolist(),
        "predicted_theta": predicted.tolist(),
        "residual": residual.tolist(),
        "chi2": chi2,
        "dof": dof,
        "chi2_ceiling_0p999": ceiling,
        "minimum_covariance_eigenvalue": float(covariance_eigenvalues[0]),
        "minimum_s_prime": float(np.min(differential["s_prime"])),
        "maximum_abs_J": float(np.max(np.abs(differential["J"]))),
        "maximum_abs_q_minus_2p2_plus_p": float(
            np.max(np.abs(differential["q"] - (2.0 * differential["p"] ** 2 + differential["p"])))
        ),
        "scale_invariance_max_errors": scale_errors,
        "grid_points": int(grid.size),
        "epistemic_ceiling": (
            "EXACT_ZERO_TIDE_SUBFAMILY_ONLY__SMALL_NONZERO_TIDE_HISTORY_TRANSFER_FINITE_PATH_"
            "NONSPHERICAL_TIME_LIVE_BAO_XMAX_AND_UDT_VALIDATION_OPEN"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT_PATH.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
