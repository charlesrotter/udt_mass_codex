#!/usr/bin/env python3
"""Independent standard-library checks for the grok2 integration crosswalk."""

import json
import math


N = 1.0559332414320268
X_EFF = 2085.9586748597476
C_KM_S = 299792.458
H0 = 73.9
SIGMA_H0 = 3.0


def r_tanh(z: float, x: float) -> float:
    Z = 1.0 + z
    return x * (Z * Z - 1.0) / (Z * Z + 1.0)


def r_p1(z: float, n: float, x_eff: float) -> float:
    Z = 1.0 + z
    return n * x_eff * (1.0 - Z ** (-2.0 / n))


def centered_first(fn, h=1.0e-5):
    return (fn(h) - fn(-h)) / (2.0 * h)


def centered_second(fn, h=1.0e-4):
    return (fn(h) - 2.0 * fn(0.0) + fn(-h)) / (h * h)


def close(a, b, rtol=1.0e-8, atol=1.0e-8):
    if not math.isclose(a, b, rel_tol=rtol, abs_tol=atol):
        raise AssertionError(f"{a!r} != {b!r}")


def main():
    x_tanh = 2.0 * X_EFF
    p1_wall = N * X_EFF
    maser_length = C_KM_S / H0
    maser_sigma = C_KM_S * SIGMA_H0 / (H0 * H0)

    close(centered_first(lambda z: r_tanh(z, x_tanh)), x_tanh, rtol=2e-10)
    close(centered_first(lambda z: r_p1(z, N, X_EFF)), 2.0 * X_EFF, rtol=2e-10)
    close(centered_second(lambda z: r_tanh(z, x_tanh)), -x_tanh, rtol=2e-7)
    close(
        centered_second(lambda z: r_p1(z, N, X_EFF)),
        -2.0 * X_EFF * (1.0 + 2.0 / N),
        rtol=2e-7,
    )
    close(r_tanh(1.0e8, x_tanh), x_tanh, rtol=2e-8)
    close(r_p1(1.0e8, N, X_EFF), p1_wall, rtol=2e-8)
    close(x_tanh / p1_wall, 2.0 / N)

    result = {
        "status": "PASS",
        "checks": 7,
        "n": N,
        "X_eff_Mpc": X_EFF,
        "p1_origin_slope_Mpc": 2.0 * X_EFF,
        "p1_radius_asymptote_Mpc": p1_wall,
        "matched_tanh_X_Mpc": x_tanh,
        "matched_asymptote_ratio_tanh_over_p1": 2.0 / N,
        "maser_c_over_H0_Mpc": maser_length,
        "maser_c_over_H0_sigma_Mpc": maser_sigma,
        "central_fractional_difference": (2.0 * X_EFF - maser_length) / maser_length,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
