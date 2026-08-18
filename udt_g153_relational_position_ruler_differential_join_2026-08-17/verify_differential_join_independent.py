#!/usr/bin/env python3
"""Independent Fraction replay for G153."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def dchi(T, L, dT, dL):
    return 2 * (T * dL - L * dT) / (L + T) ** 2


def main() -> None:
    T, L, X, beta = F(2), F(3), F(5), F(1, 5)
    Tt, Lt = F(1, 7), F(-1, 11)
    Ts, Ls = F(2, 9), F(1, 4)
    Xt, Xs = F(1, 13), F(-1, 17)
    chi = (L - T) / (L + T)

    rho_t = Xt * chi + X * dchi(T, L, Tt, Lt)
    rho_s = Xs * chi + X * dchi(T, L, Ts, Ls)
    temporal = rho_t / T
    spatial = (rho_s - beta * rho_t) / L
    reconstructed = (temporal * T, temporal * T * beta + spatial * L)

    scale = F(7, 3)
    temporal_scaled = rho_t / (scale * T)
    spatial_scaled = (rho_s - beta * rho_t) / (scale * L)
    reconstructed_scaled = (
        temporal_scaled * scale * T,
        temporal_scaled * scale * T * beta + spatial_scaled * scale * L,
    )

    # Finite-value equality is broken by common scale while projective position stays fixed.
    T0, L0, X0 = F(1, 3), F(1), F(2)
    rho0 = X0 * (L0 - T0) / (L0 + T0)
    T1, L1 = 2 * T0, 2 * L0
    rho1 = X0 * (L1 - T1) / (L1 + T1)

    # Direct infinitesimal quotient from two nearby exact rational states.
    eps = F(1, 10_000)
    chi0 = chi
    chi_tau_step = ((L + eps * Lt) - (T + eps * Tt)) / ((L + eps * Lt) + (T + eps * Tt))
    finite_difference_tau = (chi_tau_step - chi0) / eps
    exact_tau = dchi(T, L, Tt, Lt)
    fd_error = finite_difference_tau - exact_tau

    gates = {
        "frame_reconstructs_coordinate_derivative": reconstructed == (rho_t, rho_s),
        "common_scale_reconstruction_unchanged": reconstructed_scaled == (rho_t, rho_s),
        "response_coefficients_inverse_scale": (
            temporal_scaled == temporal / scale and spatial_scaled == spatial / scale
        ),
        "Xmax_derivatives_are_live": Xt != 0 and Xs != 0,
        "base_finite_equality": rho0 == L0,
        "position_common_scale_invariant": rho1 == rho0,
        "ruler_common_scale_live": L1 != L0,
        "scaled_finite_equality_fails": rho1 != L1,
        "finite_difference_is_nonvacuous": fd_error != 0,
        "finite_difference_error_small": abs(fd_error) < F(1, 100_000),
    }

    result = {
        "schema": "udt.g153.independent_fraction.v1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "rational_witness": {
            "rho_tau": str(rho_t),
            "rho_sigma": str(rho_s),
            "Xmax_tau": str(Xt),
            "Xmax_sigma": str(Xs),
            "u_rho": str(temporal),
            "n_rho": str(spatial),
            "reconstructed": [str(q) for q in reconstructed],
            "scaled_reconstructed": [str(q) for q in reconstructed_scaled],
        },
        "common_scale_counterexample": {
            "base": {"T": str(T0), "L": str(L0), "rho": str(rho0)},
            "scaled": {"T": str(T1), "L": str(L1), "rho": str(rho1)},
        },
        "finite_difference": {
            "exact_tau": str(exact_tau),
            "forward_tau": str(finite_difference_tau),
            "error": str(fd_error),
        },
        "gates": gates,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
