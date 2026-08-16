#!/usr/bin/env python3
"""Independent numerical G108 Jacobi/Riccati and hostile-gauge verification."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
END = 0.8
RTOL = 2e-12
ATOL = 2e-14


def integrate_jacobi(curvature: np.ndarray, end: float = END):
    def rhs(_lam, state):
        W = state[:4].reshape(2, 2)
        P = state[4:].reshape(2, 2)
        return np.concatenate([P.ravel(), (-curvature @ W).ravel()])

    initial = np.concatenate([np.eye(2).ravel(), np.zeros((2, 2)).ravel()])
    return solve_ivp(
        rhs,
        (0.0, end),
        initial,
        method="DOP853",
        rtol=RTOL,
        atol=ATOL,
        max_step=0.005,
        dense_output=True,
    )


def integrate_riccati(curvature: np.ndarray, end: float = END):
    def rhs(_lam, state):
        L = state.reshape(2, 2)
        return (-(L @ L) - curvature).ravel()

    return solve_ivp(
        rhs,
        (0.0, end),
        np.zeros(4),
        method="DOP853",
        rtol=RTOL,
        atol=ATOL,
        max_step=0.005,
        dense_output=True,
    )


def analytic_control(name: str, lam: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if name == "isotropic_defocusing":
        k = 0.7
        W = np.cosh(k * lam) * np.eye(2)
        P = k * np.sinh(k * lam) * np.eye(2)
        curvature = -(k**2) * np.eye(2)
    elif name == "isotropic_focusing":
        k = 0.7
        W = np.cos(k * lam) * np.eye(2)
        P = -k * np.sin(k * lam) * np.eye(2)
        curvature = (k**2) * np.eye(2)
    elif name == "mixed_anisotropic":
        p, q = 0.6, 0.8
        W = np.diag([np.cosh(p * lam), np.cos(q * lam)])
        P = np.diag([p * np.sinh(p * lam), -q * np.sin(q * lam)])
        curvature = np.diag([-(p**2), q**2])
    else:
        raise ValueError(name)
    return W, P, curvature


def log_area(W: np.ndarray) -> float:
    return float(np.log(abs(np.linalg.det(W))))


def direct_g68_replay() -> dict[str, object]:
    path = (
        ROOT
        / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11"
        / "FINITE_PATH_RESULT.json"
    )
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    prod_atlas = {}
    with (HERE / "G68_ENDPOINT_RATE_ATLAS.tsv").open() as handle:
        header = handle.readline().rstrip("\n").split("\t")
        for line in handle:
            cells = line.rstrip("\n").split("\t")
            row = dict(zip(header, cells))
            prod_atlas[row["profile_id"]] = float(row["a_eff_affine"])

    raw = json.loads(path.read_text())
    max_production_delta = 0.0
    max_f01_delta = 0.0
    count = 0
    for profile in raw["profiles"]:
        D = np.array(profile["endpoint_D"], dtype=np.longdouble)
        Ddot = np.array(profile["endpoint_Ddot"], dtype=np.longdouble)
        invD = np.linalg.inv(np.asarray(D, dtype=np.float64)).astype(np.longdouble)
        alpha = float(np.trace(Ddot @ invD) / np.longdouble(2.0))
        max_production_delta = max(
            max_production_delta, abs(alpha - prod_atlas[profile["profile_id"]])
        )
        if profile["family"] == "F01":
            max_f01_delta = max(
                max_f01_delta, abs(alpha - 1.0 / float(profile["affine_final"]))
            )
        count += 1
    return {
        "row_count": count,
        "maximum_independent_production_rate_delta": max_production_delta,
        "maximum_F01_exact_rate_delta": max_f01_delta,
        "production_reported_rows": production["g68_saved_replay"]["row_count"],
    }


def main() -> None:
    names = ["isotropic_defocusing", "isotropic_focusing", "mixed_anisotropic"]
    controls = {}
    maximum = {
        "jacobi_analytic": 0.0,
        "riccati_from_jacobi": 0.0,
        "riccati_analytic": 0.0,
        "area_finite_difference": 0.0,
        "reparameterized_riccati": 0.0,
        "rotation_rate": 0.0,
        "factorization_rate": 0.0,
    }
    wrong_missing_depth_rate_detected = False
    varying_rate_detected = False

    for name in names:
        W_exact, P_exact, curvature = analytic_control(name, END)
        h = 2e-5
        jacobi = integrate_jacobi(curvature, END + 2.0 * h)
        riccati = integrate_riccati(curvature)
        jacobi_at_end = jacobi.sol(END)
        W = jacobi_at_end[:4].reshape(2, 2)
        P = jacobi_at_end[4:].reshape(2, 2)
        L_from_W = P @ np.linalg.inv(W)
        L_riccati = riccati.y[:, -1].reshape(2, 2)
        L_exact = P_exact @ np.linalg.inv(W_exact)

        W_plus = jacobi.sol(END + h)[:4].reshape(2, 2)
        W_minus = jacobi.sol(END - h)[:4].reshape(2, 2)
        half_area_fd = (log_area(W_plus) - log_area(W_minus)) / (4.0 * h)
        alpha_lambda = float(np.trace(L_from_W) / 2.0)

        # Nonlinear monotone reparameterization delta=lambda+s lambda^2.
        s = 0.15
        delta_dot = 1.0 + 2.0 * s * END
        delta_ddot = 2.0 * s
        K = L_from_W / delta_dot
        a_delta = float(np.trace(K) / 2.0)
        Ldot = -(L_from_W @ L_from_W) - curvature
        K_delta = Ldot / delta_dot**2 - L_from_W * delta_ddot / delta_dot**3
        f = delta_ddot / delta_dot**2
        tidal_delta = curvature / delta_dot**2
        reparam_residual = K_delta + K @ K + f * K + tidal_delta

        # A changing left screen frame must not alter the trace/area rate.
        angle = 0.3 * END**2
        angle_dot = 0.6 * END
        O = np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )
        eps = np.array([[0.0, -1.0], [1.0, 0.0]])
        Odot = angle_dot * eps @ O
        W_rot = O @ W
        P_rot = Odot @ W + O @ P
        alpha_rot = float(np.trace(P_rot @ np.linalg.inv(W_rot)) / 2.0)

        # Redistribute the same W between a nontrivial Q and N=Q^-1 W.
        c, d = 0.37, -0.19
        Q = np.diag([np.exp(c * END), np.exp(d * END)])
        Qdot = np.diag([c, d]) @ Q
        N = np.linalg.solve(Q, W)
        Ndot = np.linalg.solve(Q, P - Qdot @ N)
        q_rate = float(np.trace(Qdot @ np.linalg.inv(Q)) / 2.0)
        n_rate = float(np.trace(Ndot @ np.linalg.inv(N)) / 2.0)

        errors = {
            "jacobi_analytic": float(
                max(np.linalg.norm(W - W_exact), np.linalg.norm(P - P_exact))
            ),
            "riccati_from_jacobi": float(np.linalg.norm(L_riccati - L_from_W)),
            "riccati_analytic": float(np.linalg.norm(L_riccati - L_exact)),
            "area_finite_difference": abs(half_area_fd - alpha_lambda),
            "reparameterized_riccati": float(np.linalg.norm(reparam_residual)),
            "rotation_rate": abs(alpha_rot - alpha_lambda),
            "factorization_rate": abs(q_rate + n_rate - alpha_lambda),
        }
        for key, value in errors.items():
            maximum[key] = max(maximum[key], value)

        wrong_missing_depth_rate_detected |= abs(a_delta - alpha_lambda) > 1e-3
        early = 0.2
        W_early, P_early, _ = analytic_control(name, early)
        alpha_early = float(np.trace(P_early @ np.linalg.inv(W_early)) / 2.0)
        varying_rate_detected |= abs(alpha_early - alpha_lambda) > 1e-3
        controls[name] = {
            "alpha_lambda": alpha_lambda,
            "alpha_delta": a_delta,
            "delta_dot": delta_dot,
            "errors": errors,
        }

    # The exact constant-a special subfamily has W=e^(a lambda) I and R=-a^2 I.
    constant_a = 0.43
    W_constant = np.exp(constant_a * END) * np.eye(2)
    P_constant = constant_a * W_constant
    R_constant = -(constant_a**2) * np.eye(2)
    constant_jacobi_residual = np.linalg.norm(
        (constant_a**2) * W_constant + R_constant @ W_constant
    )
    constant_rate_residual = abs(
        float(np.trace(P_constant @ np.linalg.inv(W_constant)) / 2.0) - constant_a
    )

    g68 = direct_g68_replay()
    checks = {
        "all_jacobi_analytic": maximum["jacobi_analytic"] < 2e-11,
        "all_riccati_from_jacobi": maximum["riccati_from_jacobi"] < 2e-11,
        "all_riccati_analytic": maximum["riccati_analytic"] < 2e-11,
        "all_area_rates": maximum["area_finite_difference"] < 2e-9,
        "all_reparameterized_riccati": maximum["reparameterized_riccati"] < 2e-11,
        "all_rotation_gauge": maximum["rotation_rate"] < 2e-12,
        "all_factorization_gauge": maximum["factorization_rate"] < 2e-12,
        "wrong_missing_depth_rate_detected": wrong_missing_depth_rate_detected,
        "nonconstant_controls_vary": varying_rate_detected,
        "constant_subfamily_jacobi": constant_jacobi_residual < 1e-14,
        "constant_subfamily_rate": constant_rate_residual < 1e-14,
        "G68_all_rows_replayed": g68["row_count"] == 21,
        "G68_matches_production": g68["maximum_independent_production_rate_delta"] < 2e-14,
        "G68_F01_exact": g68["maximum_F01_exact_rate_delta"] < 2e-13,
    }
    checks = {key: bool(value) for key, value in checks.items()}
    result = {
        "schema": "UDT_G108_INDEPENDENT_SCREEN_PROPAGATION_V1",
        "controls": controls,
        "maximum_residuals": maximum,
        "constant_a_special_subfamily": {
            "a": constant_a,
            "jacobi_residual": float(constant_jacobi_residual),
            "rate_residual": float(constant_rate_residual),
        },
        "g68_saved_replay": g68,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
