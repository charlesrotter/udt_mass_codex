#!/usr/bin/env python3
"""Derive the complete-pair shape operator and evaluate two frozen controls."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar


EXPECTED_MEAN_SHA256 = "9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585"
EXPECTED_COV_SHA256 = "252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509"
N_SNE = 1.0559332414320268
Z_USED = (0.510, 0.706, 0.934, 1.321, 1.484, 2.330)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def symbolic_checks() -> dict[str, str | bool]:
    q, da, L, phip, phi = sp.symbols("q d_A L phi_prime phi", positive=True)
    # lambda_new=f(lambda), q=d lambda_new/d lambda > 0.
    transformed = sp.exp(phi) * da * (phip / q) / (L / q)
    base = sp.exp(phi) * da * phip / L
    reparam_ok = sp.simplify(transformed - base) == 0
    missing_l_base = sp.exp(phi) * da * phip
    missing_l_transformed = sp.exp(phi) * da * phip / q
    missing_l_reparam_ok = sp.simplify(missing_l_transformed - missing_l_base) == 0

    u, X, n = sp.symbols("u X n", positive=True)
    r_general = X / n * (1 - u ** (-2 / n))
    dr_du = sp.diff(r_general, u)
    # lambda=r, L_pair=u, dz/du=1, d_A=r.
    f_general = sp.factor(r_general / (u * dr_du))
    target_general = n / 2 * (u ** (2 / n) - 1)
    general_ok = sp.simplify(f_general - target_general) == 0
    missing_exp_general = sp.factor(f_general / u)
    missing_exp_differs = sp.simplify(missing_exp_general - target_general) != 0
    c0 = sp.simplify(target_general.subs(n, 1).subs(u, 1 + sp.Symbol("z")))
    c0_ok = sp.expand(c0 - (sp.Symbol("z") + sp.Symbol("z") ** 2 / 2)) == 0

    return {
        "operator": "F_pair=exp(phi_pair)*d_A*(dphi_pair/dlambda)/L_pair=d_A*(dz/dlambda)/L_pair",
        "orientation_preserving_reparameterization_invariant": reparam_ok,
        "missing_L_pair_reparameterization_invariant": missing_l_reparam_ok,
        "reversal": "signed F changes sign; physical unoriented pattern shape uses abs(F)",
        "general_scalar_reduction": sp.sstr(f_general),
        "general_scalar_target": sp.sstr(target_general),
        "general_scalar_exact": general_ok,
        "missing_exp_phi_general": sp.sstr(missing_exp_general),
        "missing_exp_phi_fails_scalar_reduction": missing_exp_differs,
        "c0_exact": c0_ok,
    }


def load_rows(path: Path) -> list[dict[str, float | str | int]]:
    result = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        if not line or line.startswith("#"):
            continue
        z, value, quantity = line.split()
        result.append(
            {"index": index - 1, "z": float(z), "value": float(value), "quantity": quantity}
        )
    # Header is one line, so the index above equals the zero-based numerical row index.
    return result


def controls(z: float) -> tuple[float, float]:
    u = 1.0 + z
    return z + 0.5 * z * z, 0.5 * N_SNE * (u ** (2.0 / N_SNE) - 1.0)


def profile_direction(y: np.ndarray, cov: np.ndarray, f_value: float) -> dict[str, float]:
    inv = np.linalg.inv(cov)
    v = np.array([f_value, 1.0], dtype=np.float64)
    amplitude = float((v @ inv @ y) / (v @ inv @ v))
    residual = y - amplitude * v
    chi2 = float(residual @ inv @ residual)
    objective = lambda trial: float((y - trial * v) @ inv @ (y - trial * v))
    scale = max(1.0, abs(amplitude))
    direct = minimize_scalar(
        objective,
        bracket=(amplitude - scale, amplitude, amplitude + scale),
        method="brent",
        options={"xtol": 1e-14, "maxiter": 1000},
    )
    if not direct.success:
        raise RuntimeError(f"direct nuisance minimization failed: {direct.message}")
    f_obs = float(y[0] / y[1])
    signed = float(np.sign(f_obs - f_value) * np.sqrt(max(0.0, chi2)))
    return {
        "F_pred": f_value,
        "F_observed": f_obs,
        "observed_DM": float(y[0]),
        "observed_DH": float(y[1]),
        "profiled_publication_amplitude": amplitude,
        "direct_minimizer_amplitude": float(direct.x),
        "direct_minimizer_chi2": float(direct.fun),
        "direct_amplitude_abs_delta": abs(float(direct.x) - amplitude),
        "direct_chi2_abs_delta": abs(float(direct.fun) - chi2),
        "chi2": chi2,
        "signed_sqrt_chi2": signed,
        "residual_DM": float(residual[0]),
        "residual_DH": float(residual[1]),
    }


def classify(chi2: float) -> str:
    if chi2 <= 12.592:
        return "COMPATIBLE_ON_SIX_BIN_SHAPE_QUERY"
    if chi2 <= 22.458:
        return "TENSION_ON_SIX_BIN_SHAPE_QUERY"
    return "INCOMPATIBLE_ON_SIX_BIN_SHAPE_QUERY"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mean", type=Path, required=True)
    parser.add_argument("--cov", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rows-output", type=Path, required=True)
    args = parser.parse_args()

    assert sha256(args.mean) == EXPECTED_MEAN_SHA256
    assert sha256(args.cov) == EXPECTED_COV_SHA256
    symbolic = symbolic_checks()
    assert symbolic["orientation_preserving_reparameterization_invariant"]
    assert symbolic["general_scalar_exact"] and symbolic["c0_exact"]

    rows = load_rows(args.mean)
    cov_full = np.loadtxt(args.cov)
    assert cov_full.shape == (13, 13)
    controls_out: dict[str, list[dict[str, float]]] = {"C0": [], "C1": []}

    for z in Z_USED:
        dm = next(row for row in rows if abs(float(row["z"]) - z) < 1e-12 and row["quantity"] == "DM_over_rs")
        dh = next(row for row in rows if abs(float(row["z"]) - z) < 1e-12 and row["quantity"] == "DH_over_rs")
        indices = [int(dm["index"]), int(dh["index"])]
        y = np.array([float(dm["value"]), float(dh["value"])])
        cov = cov_full[np.ix_(indices, indices)]
        f0, f1 = controls(z)
        for name, f_value in (("C0", f0), ("C1", f1)):
            item = {"z": z, **profile_direction(y, cov, f_value)}
            item["cov_DM_DM"] = float(cov[0, 0])
            item["cov_DM_DH"] = float(cov[0, 1])
            item["cov_DH_DH"] = float(cov[1, 1])
            controls_out[name].append(item)

    totals = {name: float(sum(row["chi2"] for row in values)) for name, values in controls_out.items()}
    max_direct_amplitude_delta = max(
        row["direct_amplitude_abs_delta"] for values in controls_out.values() for row in values
    )
    max_direct_chi2_delta = max(
        row["direct_chi2_abs_delta"] for values in controls_out.values() for row in values
    )
    assert max_direct_amplitude_delta < 1e-6
    assert max_direct_chi2_delta < 1e-10
    result = {
        "status": "PASS",
        "scope": "complete-pair operator plus two frozen scalar controls; no UDT fit",
        "preregistration_commit": "efdecd35",
        "mean_sha256": EXPECTED_MEAN_SHA256,
        "cov_sha256": EXPECTED_COV_SHA256,
        "n_sne_fixed": N_SNE,
        "z_used": list(Z_USED),
        "symbolic": symbolic,
        "controls": controls_out,
        "totals": {
            name: {"chi2": value, "constraints": 6, "classification": classify(value)}
            for name, value in totals.items()
        },
        "delta_chi2_C1_minus_C0": totals["C1"] - totals["C0"],
        "direct_profile_verification": {
            "method": "scipy Brent minimization of each full-2x2 quadratic",
            "amplitude_abs_tolerance": 1e-6,
            "chi2_abs_tolerance": 1e-10,
            "maximum_amplitude_abs_delta": max_direct_amplitude_delta,
            "maximum_chi2_abs_delta": max_direct_chi2_delta,
        },
        "maximum_conclusion": "bounded normalization-free six-bin shape compatibility only",
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    lines = [
        "control\tz\tF_pred\tF_observed\tprofiled_publication_amplitude\tchi2\tsigned_sqrt_chi2"
    ]
    for name, values in controls_out.items():
        for row in values:
            lines.append(
                f"{name}\t{row['z']:.3f}\t{row['F_pred']:.12g}\t{row['F_observed']:.12g}\t"
                f"{row['profiled_publication_amplitude']:.12g}\t{row['chi2']:.12g}\t"
                f"{row['signed_sqrt_chi2']:.12g}"
            )
    args.rows_output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "totals": result["totals"]}))


if __name__ == "__main__":
    main()
