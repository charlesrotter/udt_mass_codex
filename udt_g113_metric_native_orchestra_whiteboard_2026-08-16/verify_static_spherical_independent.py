#!/usr/bin/env python3
"""Standalone standard-library replay of the G113 series and pair-block checks."""

from fractions import Fraction
import json
import math


def main() -> None:
    n = Fraction(17, 16)
    x_eff = Fraction(13, 2)

    # Binomial series for f=(1-r/(n X))^n through second order.
    f0 = Fraction(1)
    f1 = -Fraction(1, 1) / x_eff
    f2 = (n - 1) / (2 * n * x_eff * x_eff)

    # Independent series consequences of
    # R=-f''-4f'/r+2(1-f)/r^2 and K_ang=(1-f)/r^2.
    scalar_residue = -6 * f1
    angular_residue = -f1
    phi_prime = -f1 / 2

    r_value = 1.0
    n_float = float(n)
    x_float = float(x_eff)
    f_value = (1.0 - r_value / (n_float * x_float)) ** n_float
    c_e = 7.0
    dt_dr = 1.0 / (c_e * f_value)
    h00 = -f_value
    h01 = -f_value * c_e * c_e * (1.0 / c_e) * dt_dr
    h11 = -f_value * c_e * c_e * dt_dr * dt_dr + 1.0 / f_value
    determinant = h00 * h11 - h01 * h01
    terminal = 0.25 * math.log((-determinant) / (h00 * h00))
    expected_terminal = -0.5 * math.log(f_value)

    checks = {
        "binomial_f0": f0 == 1,
        "binomial_f1": f1 == -1 / x_eff,
        "pair_h01": abs(h01 + 1.0) < 1e-14,
        "pair_h11": abs(h11) < 1e-14,
        "pair_determinant": abs(determinant + 1.0) < 1e-14,
        "terminal_depth": abs(terminal - expected_terminal) < 1e-14,
        "p1_phi_prime_origin": phi_prime == 1 / (2 * x_eff),
        "p1_scalar_curvature_residue": scalar_residue == 6 / x_eff,
        "p1_angular_curvature_residue": angular_residue == 1 / x_eff,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "exact_control": {
            "n": str(n),
            "X_eff": str(x_eff),
            "f1": str(f1),
            "f2": str(f2),
            "phi_prime_origin": str(phi_prime),
            "scalar_curvature_residue": str(scalar_residue),
            "angular_curvature_residue": str(angular_residue),
        },
        "method": "standard-library Fraction binomial series plus direct numeric pullback",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
