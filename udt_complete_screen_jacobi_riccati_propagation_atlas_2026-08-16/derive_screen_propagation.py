#!/usr/bin/env python3
"""Exact G108 screen-area derivation plus saved G68 endpoint recomputation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sources() -> dict[str, bool]:
    checks: dict[str, bool] = {}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            checks[row["path"]] = sha256(ROOT / row["path"]) == row["sha256"]
    return checks


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def exact_derivation() -> dict[str, object]:
    lam = sp.symbols("lambda", real=True)
    a, b, kappa, p, q, c, d, rho = sp.symbols(
        "a b kappa p q c d rho", real=True
    )
    identity = sp.eye(2)

    rotation = sp.Matrix(
        [
            [sp.cos(b * lam), -sp.sin(b * lam)],
            [sp.sin(b * lam), sp.cos(b * lam)],
        ]
    )
    constant_map = sp.exp(a * lam) * rotation
    constant_optical = sp.simplify(sp.diff(constant_map, lam) * constant_map.inv())
    constant_area = sp.simplify(constant_map.det())
    constant_rate = sp.simplify(sp.trace(constant_optical) / 2)

    defocusing = sp.cosh(kappa * lam) * identity
    focusing = sp.cos(kappa * lam) * identity
    anisotropic = sp.diag(sp.cosh(p * lam), sp.cos(q * lam))
    controls = {
        "isotropic_defocusing": {
            "W": defocusing,
            "R": -(kappa**2) * identity,
            "a_eff_lambda": kappa * sp.tanh(kappa * lam),
        },
        "isotropic_focusing": {
            "W": focusing,
            "R": (kappa**2) * identity,
            "a_eff_lambda": -kappa * sp.tan(kappa * lam),
        },
        "mixed_anisotropic": {
            "W": anisotropic,
            "R": sp.diag(-(p**2), q**2),
            "a_eff_lambda": (
                p * sp.tanh(p * lam) - q * sp.tan(q * lam)
            )
            / 2,
        },
    }

    control_results: dict[str, object] = {}
    for name, item in controls.items():
        W = item["W"]
        curvature = item["R"]
        optical = sp.simplify(sp.diff(W, lam) * W.inv())
        jacobi_residual = sp.simplify(sp.diff(W, lam, 2) + curvature * W)
        area_rate = sp.simplify(sp.diff(sp.log(W.det()), lam) / 2)
        expected = sp.simplify(item["a_eff_lambda"])
        control_results[name] = {
            "jacobi_residual_zero": zero_matrix(jacobi_residual),
            "trace_rate": sp.sstr(sp.simplify(sp.trace(optical) / 2)),
            "area_rate": sp.sstr(area_rate),
            "expected_rate": sp.sstr(expected),
            "rates_equal": sp.simplify(sp.trace(optical) / 2 - expected) == 0
            and sp.simplify(area_rate - expected) == 0,
        }

    # A nontrivial complete screen map is factored into coframe and realization pieces.
    generic_W = sp.Matrix(
        [[sp.exp(2 * lam), lam], [0, sp.exp(-lam)]]
    )
    Q = sp.diag(sp.exp(c * lam), sp.exp(d * lam))
    N = sp.simplify(Q.inv() * generic_W)
    total_rate = sp.simplify(sp.trace(sp.diff(generic_W, lam) * generic_W.inv()) / 2)
    q_rate = sp.simplify(sp.trace(sp.diff(Q, lam) * Q.inv()) / 2)
    n_rate = sp.simplify(sp.trace(sp.diff(N, lam) * N.inv()) / 2)

    gauge_rotation = sp.Matrix(
        [
            [sp.cos(rho * lam**2), -sp.sin(rho * lam**2)],
            [sp.sin(rho * lam**2), sp.cos(rho * lam**2)],
        ]
    )
    rotated_W = sp.simplify(gauge_rotation * generic_W)
    rotated_rate = sp.simplify(
        sp.trace(sp.diff(rotated_W, lam) * rotated_W.inv()) / 2
    )

    return {
        "constant_extension": {
            "area": sp.sstr(constant_area),
            "half_log_area_rate": sp.sstr(
                sp.simplify(sp.diff(sp.log(constant_area), lam) / 2)
            ),
            "half_optical_trace": sp.sstr(constant_rate),
            "optical_matrix": [[sp.sstr(x) for x in row] for row in constant_optical.tolist()],
            "recovers_a": sp.simplify(constant_rate - a) == 0,
            "rotation_drops_from_area": not constant_area.has(b),
        },
        "analytic_controls": control_results,
        "factorization": {
            "W_equals_QN": zero_matrix(sp.simplify(generic_W - Q * N)),
            "total_rate": sp.sstr(total_rate),
            "Q_rate": sp.sstr(q_rate),
            "N_rate": sp.sstr(n_rate),
            "rates_add": sp.simplify(total_rate - q_rate - n_rate) == 0,
            "coframe_rate_not_separately_invariant": sp.simplify(q_rate - total_rate) != 0,
        },
        "screen_rotation": {
            "determinant_unchanged": sp.simplify(rotated_W.det() - generic_W.det()) == 0,
            "area_rate_unchanged": sp.simplify(rotated_rate - total_rate) == 0,
            "nonconstant_rotation_used": sp.diff(rho * lam**2, lam) != 0,
        },
    }


def direct_det_derivative(D: np.ndarray, Ddot: np.ndarray) -> float:
    return float(
        Ddot[0, 0] * D[1, 1]
        + D[0, 0] * Ddot[1, 1]
        - Ddot[0, 1] * D[1, 0]
        - D[0, 1] * Ddot[1, 0]
    )


def replay_g68() -> tuple[list[dict[str, object]], dict[str, object]]:
    path = (
        ROOT
        / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11"
        / "FINITE_PATH_RESULT.json"
    )
    raw = json.loads(path.read_text())
    rows: list[dict[str, object]] = []
    for profile in raw["profiles"]:
        D = np.asarray(profile["endpoint_D"], dtype=float)
        Ddot = np.asarray(profile["endpoint_Ddot"], dtype=float)
        det_D = float(np.linalg.det(D))
        optical = Ddot @ np.linalg.inv(D)
        theta_trace = float(np.trace(optical))
        detdot_direct = direct_det_derivative(D, Ddot)
        theta_det = detdot_direct / det_D
        a_affine = theta_trace / 2.0
        symmetric = 0.5 * (optical + optical.T)
        shear = symmetric - a_affine * np.eye(2)
        twist = 0.5 * (optical - optical.T)
        affine = float(profile["affine_final"])
        f01_expected = 1.0 / affine if profile["family"] == "F01" else None
        rows.append(
            {
                "profile_id": profile["profile_id"],
                "family": profile["family"],
                "lapse_a": profile["lapse_a"],
                "mix_shape": profile["mix_shape"],
                "mix_epsilon": profile["mix_epsilon"],
                "affine_final": affine,
                "screen_area": abs(det_D),
                "theta_affine": theta_trace,
                "a_eff_affine": a_affine,
                "shear_frobenius": float(np.linalg.norm(shear)),
                "twist_frobenius": float(np.linalg.norm(twist)),
                "area_identity_residual": abs(theta_trace - theta_det),
                "f01_exact_rate_residual": (
                    abs(a_affine - f01_expected) if f01_expected is not None else "NA"
                ),
            }
        )

    f01 = [row for row in rows if row["family"] == "F01"]
    f02 = [row for row in rows if row["family"] == "F02"]
    summary = {
        "row_count": len(rows),
        "f01_count": len(f01),
        "f02_count": len(f02),
        "all_rates_finite": all(np.isfinite(row["a_eff_affine"]) for row in rows),
        "max_area_identity_residual": max(row["area_identity_residual"] for row in rows),
        "max_f01_exact_rate_residual": max(
            row["f01_exact_rate_residual"] for row in f01
        ),
        "a_eff_affine_range_all": [
            min(row["a_eff_affine"] for row in rows),
            max(row["a_eff_affine"] for row in rows),
        ],
        "a_eff_affine_range_f02": [
            min(row["a_eff_affine"] for row in f02),
            max(row["a_eff_affine"] for row in f02),
        ],
        "max_twist_frobenius": max(row["twist_frobenius"] for row in rows),
        "max_shear_frobenius_f02": max(row["shear_frobenius"] for row in f02),
    }
    return rows, summary


def write_tsv(rows: list[dict[str, object]]) -> None:
    fields = list(rows[0])
    with (HERE / "G68_ENDPOINT_RATE_ATLAS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    source_checks = verify_sources()
    exact = exact_derivation()
    rows, g68_summary = replay_g68()
    result = {
        "schema": "UDT_G108_COMPLETE_SCREEN_PROPAGATION_V1",
        "source_hashes": source_checks,
        "all_source_hashes_match": all(source_checks.values()),
        "exact": exact,
        "g68_saved_replay": g68_summary,
        "maximum_conclusion": (
            "when the supplied query identifies the complete pair-screen block with the physical "
            "Jacobi map, its conditional screen dilation rate is derived from propagated area; "
            "constant a is a special propagation subfamily; metric history, query, initial data, "
            "branch, and depth map remain supplied"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    write_tsv(rows)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
