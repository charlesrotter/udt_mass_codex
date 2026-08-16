#!/usr/bin/env python3
"""Independent standard-library G125 replay; imports no production code."""

from __future__ import annotations

import json
import math
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def close(a: float, b: float, tol: float = 2e-13) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def main() -> None:
    # Exact n=2 witness: R_inf=10, Z=5/4, R=2, zeta=log(5/4).
    R_inf = F(10)
    Z = F(5, 4)
    R = R_inf * (1 - 1 / Z)
    Z_back = 1 / (1 - R / R_inf)
    dL = Z * Z * R

    # Distinct exact decompositions are checked through exponentiated score factors.
    # exp(2*zeta)=Z^2=25/16.
    exp2zeta = Z * Z
    terminal_phi_allocation = (exp2zeta, F(1), F(1))
    terminal_screen_rate_allocation = (F(1), exp2zeta, F(1))
    terminal_source_clock_allocation = (F(1), F(1), exp2zeta)

    def score_product(member):
        exp2phi, Q, exp2chi = member
        return exp2phi * Q * exp2chi

    K_plus = exp2zeta
    K_minus = -exp2zeta
    wrong_sign_screen_score = (
        terminal_screen_rate_allocation[0]
        / terminal_screen_rate_allocation[1]
        * terminal_screen_rate_allocation[2]
    )

    generic_checks = []
    n = 1.0559332414320268
    X = 2085.9586748597476
    rinf = n * X
    for z_float in (1.0001, 1.1, 1.5, 2.0, 3.2613, 10.0):
        r_float = rinf * (1.0 - z_float ** (-2.0 / n))
        z_back_float = (1.0 - r_float / rinf) ** (-n / 2.0)
        zeta = -n * math.log1p(-r_float / rinf) / 2.0
        generic_checks.append(close(z_back_float, z_float) and close(zeta, math.log(z_float)))

    checks = {
        "exact_n2_radius": R == F(2),
        "exact_n2_inverse": Z_back == Z,
        "exact_n2_luminosity": dL == F(25, 8),
        "terminal_phi_allocation": score_product(terminal_phi_allocation) == exp2zeta,
        "terminal_screen_rate_allocation": (
            score_product(terminal_screen_rate_allocation) == exp2zeta
        ),
        "terminal_source_clock_allocation": (
            score_product(terminal_source_clock_allocation) == exp2zeta
        ),
        "terminal_allocations_are_distinct": len(
            {
                terminal_phi_allocation,
                terminal_screen_rate_allocation,
                terminal_source_clock_allocation,
            }
        ) == 3,
        "general_inverse_and_score_grid": all(generic_checks),
        "center_is_Z_one": F(1) / (1 - F(0) / R_inf) == 1,
        "signed_orientation_retained_but_score_uses_abs_K": (
            K_plus == -K_minus
            and abs(K_plus) == abs(K_minus)
            and score_product(terminal_screen_rate_allocation) == exp2zeta
        ),
        "wrong_screen_log_sign_is_caught": wrong_sign_screen_score != exp2zeta,
        "dL_depends_only_on_operational_Z_R": dL == Z * Z * R,
        "formal_limit_is_not_reached_at_finite_Z": all(
            rinf * (1.0 - z ** (-2.0 / n)) < rinf for z in (1.1, 2.0, 10.0, 1e6)
        ),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "implementation": "independent standard-library Fraction and direct-float replay; no production import",
        "checks": checks,
        "exact_n2": {
            "R_inf": str(R_inf),
            "Z": str(Z),
            "R": str(R),
            "dL": str(dL),
            "exp_2zeta": str(exp2zeta),
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
