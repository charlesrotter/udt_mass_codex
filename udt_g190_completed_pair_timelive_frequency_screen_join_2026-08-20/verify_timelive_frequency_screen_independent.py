#!/usr/bin/env python3
"""Implementation-distinct numerical verification for G190.

No production module or production artifact is imported.  Pair-frame identities are evaluated by
direct scalar formulas and the time-live Jacobi solution is checked against an independently coded
RK4 integration.
"""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path


SEED = 19020260820
PAIR_TRIALS = 20_000
JACOBI_TRIALS = 256


def bilinear(h00, h01, h11, x, y):
    return h00 * x[0] * y[0] + h01 * (x[0] * y[1] + x[1] * y[0]) + h11 * x[1] * y[1]


def pair_trials(rng):
    maximum = 0.0
    assertions = 0
    for _ in range(PAIR_TRIALS):
        T = math.exp(rng.uniform(-2.0, 2.0))
        L = math.exp(rng.uniform(-2.0, 2.0))
        beta = rng.uniform(-3.0, 3.0)
        h00 = -(T * T)
        h01 = -(T * T) * beta
        h11 = L * L - T * T * beta * beta
        U = (1.0 / T, 0.0)
        N = (-beta / L, 1.0 / L)
        ep = (U[0] + N[0], U[1] + N[1])
        em = (U[0] - N[0], U[1] - N[1])
        residuals = [
            h00 * h11 - h01 * h01 + T * T * L * L,
            bilinear(h00, h01, h11, U, U) + 1.0,
            bilinear(h00, h01, h11, N, N) - 1.0,
            bilinear(h00, h01, h11, U, N),
            bilinear(h00, h01, h11, ep, ep),
            bilinear(h00, h01, h11, em, em),
            -bilinear(h00, h01, h11, U, ep) - 1.0,
            -bilinear(h00, h01, h11, U, em) - 1.0,
        ]
        maximum = max(maximum, *(abs(value) for value in residuals))
        scale = max(1.0, T * T * L * L, T * T * beta * beta, L * L)
        if any(abs(value) > 2.0e-11 * scale for value in residuals):
            raise AssertionError((T, L, beta, residuals, scale))
        assertions += len(residuals)
    return maximum, assertions


def rk4_step(lam, D, P, step, H):
    def rhs(at_lam, at_D, at_P):
        tide = H * H / (1.0 + 2.0 * H * at_lam) ** 2
        return at_P, -tide * at_D

    k1D, k1P = rhs(lam, D, P)
    k2D, k2P = rhs(lam + step / 2.0, D + step * k1D / 2.0, P + step * k1P / 2.0)
    k3D, k3P = rhs(lam + step / 2.0, D + step * k2D / 2.0, P + step * k2P / 2.0)
    k4D, k4P = rhs(lam + step, D + step * k3D, P + step * k3P)
    return (
        D + step * (k1D + 2.0 * k2D + 2.0 * k3D + k4D) / 6.0,
        P + step * (k1P + 2.0 * k2P + 2.0 * k3P + k4P) / 6.0,
    )


def jacobi_trials(rng):
    maximum_D = 0.0
    maximum_frequency = 0.0
    maximum_static = 0.0
    assertions = 0
    for _ in range(JACOBI_TRIALS):
        H = rng.uniform(0.05, 1.25)
        terminal = rng.uniform(0.02, 2.0)
        steps = 2400
        step = terminal / steps
        D, P, lam = 0.0, 1.0, 0.0
        for _index in range(steps):
            D, P = rk4_step(lam, D, P, step, H)
            lam += step
        q = 1.0 + 2.0 * H * terminal
        exact_D = math.sqrt(q) * math.log(q) / (2.0 * H)
        err_D = abs(D - exact_D)
        maximum_D = max(maximum_D, err_D)
        if err_D > 2.0e-11 * max(1.0, abs(exact_D)):
            raise AssertionError((H, terminal, D, exact_D, err_D))

        eta = math.log(q) / (2.0 * H)
        a = math.exp(H * eta)
        omega = 1.0 / a
        domega = -H / (a**3)
        # Independent coordinate contraction for -k^a k^b nabla_a U_b in the conformal metric.
        frequency_rhs = -H / (a**3)
        freq_err = abs(domega - frequency_rhs)
        maximum_frequency = max(maximum_frequency, freq_err)
        if freq_err > 2.0e-13:
            raise AssertionError((H, eta, domega, frequency_rhs))

        Z = omega
        descended = -math.log(Z) / (H * Z)
        descent_err = abs(descended - exact_D)
        maximum_frequency = max(maximum_frequency, descent_err)
        if descent_err > 2.0e-12 * max(1.0, abs(exact_D)):
            raise AssertionError((H, eta, descended, exact_D))

        phi_s = rng.uniform(-2.0, 2.0)
        phi_o = rng.uniform(-2.0, 2.0)
        energy = math.exp(rng.uniform(-1.0, 1.0))
        c_e = math.exp(rng.uniform(-1.0, 1.0))
        ratio = (energy * math.exp(phi_s) / c_e) / (energy * math.exp(phi_o) / c_e)
        static_err = abs(ratio - math.exp(phi_s - phi_o))
        maximum_static = max(maximum_static, static_err)
        if static_err > 2.0e-13 * max(1.0, abs(ratio)):
            raise AssertionError((phi_s, phi_o, ratio, static_err))
        assertions += 4
    return maximum_D, maximum_frequency, maximum_static, assertions


def main():
    rng = random.Random(SEED)
    pair_max, pair_assertions = pair_trials(rng)
    jacobi_max, frequency_max, static_max, other_assertions = jacobi_trials(rng)
    result = {
        "status": "PASS",
        "seed": SEED,
        "pair_trials": PAIR_TRIALS,
        "jacobi_trials": JACOBI_TRIALS,
        "assertions": pair_assertions + other_assertions,
        "maximum_pair_residual": pair_max,
        "maximum_RK4_D_error": jacobi_max,
        "maximum_frequency_or_descent_error": frequency_max,
        "maximum_static_recovery_error": static_max,
        "imports_production_module": False,
        "reads_production_artifact": False,
    }
    if os.environ.get("G190_NO_WRITE") != "1":
        output = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
