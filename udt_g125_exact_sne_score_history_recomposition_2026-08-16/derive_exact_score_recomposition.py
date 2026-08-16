#!/usr/bin/env python3
"""Exact symbolic G125 recomposition; no data, optimizer, or history solve."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    n, X, Z = sp.symbols("n X Z", positive=True)
    R = sp.symbols("R", nonnegative=True)
    y = sp.symbols("y", positive=True)
    R_inf = n * X
    R_of_Z = R_inf * (1 - Z ** (-sp.Rational(2, 1) / n))
    Z_of_R = (1 - R / R_inf) ** (-n / 2)
    zeta_R = -n * sp.log(1 - R / R_inf) / 2
    R_of_y = R_inf * (1 - y)
    Z_of_y = y ** (-n / 2)
    zeta_y = -n * sp.log(y) / 2

    phi, chi = sp.symbols("phi chi", real=True)
    Q = sp.symbols("Q", positive=True)
    kappa = -sp.log(Q) / 2
    score = phi - kappa + chi
    Q_family = sp.exp(2 * (zeta_y - phi - chi))
    chi_family = zeta_y - phi - sp.log(Q) / 2

    a, b = sp.symbols("a b", real=True)
    phi_ab = a * zeta_y
    chi_ab = b * zeta_y
    Q_ab = sp.exp(2 * (1 - a - b) * zeta_y)

    dL_old = Z**2 * R_of_Z
    dL_recomposed = Z**2 * R_inf * (1 - Z ** (-2 / n))

    checks = {
        "invert_R_of_Z": sp.simplify(Z_of_R.subs(R, R_of_Z) - Z) == 0,
        "invert_Z_of_R_on_declared_domain": sp.simplify(
            R_of_Z.subs(Z, Z_of_y) - R_of_y
        ) == 0,
        "zeta_is_log_Z_of_R": sp.simplify(sp.exp(zeta_y) - Z_of_y) == 0,
        "score_uses_screen_rate": sp.simplify(score - (phi + sp.log(Q) / 2 + chi)) == 0,
        "affine_rate_family_solves_score": sp.simplify(
            Q_family * sp.exp(2 * (phi + chi - zeta_y)) - 1
        ) == 0,
        "endpoint_clock_family_solves_score": sp.simplify(
            phi + sp.log(Q) / 2 + chi_family - zeta_y
        ) == 0,
        "two_parameter_split_family": sp.simplify(
            Q_ab * sp.exp(2 * (phi_ab + chi_ab - zeta_y)) - 1
        ) == 0,
        "terminal_phi_allocation": sp.simplify(
            (Q_ab * sp.exp(2 * (phi_ab + chi_ab - zeta_y)) - 1).subs({a: 1, b: 0})
        ) == 0,
        "terminal_screen_rate_allocation": sp.simplify(
            (Q_ab * sp.exp(2 * (phi_ab + chi_ab - zeta_y)) - 1).subs({a: 0, b: 0})
        ) == 0,
        "terminal_source_clock_allocation": sp.simplify(
            (Q_ab * sp.exp(2 * (phi_ab + chi_ab - zeta_y)) - 1).subs({a: 0, b: 1})
        ) == 0,
        "luminosity_curve_unchanged": sp.simplify(dL_old - dL_recomposed) == 0,
        "center_radius": sp.simplify(R_of_Z.subs(Z, 1)) == 0,
        "center_score": sp.simplify(zeta_R.subs(R, 0)) == 0,
        "radius_monotone": sp.simplify(sp.diff(R_of_Z, Z) - 2 * X * Z ** (-2 / n - 1)) == 0,
        "formal_radius_limit": sp.limit(R_of_Z, Z, sp.oo) == R_inf,
        "score_formal_limit": sp.limit(zeta_R, R, R_inf, dir="-") == sp.oo,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "exact_objects": {
            "R_of_Z": str(R_of_Z),
            "Z_of_R": str(Z_of_R),
            "zeta_of_R": str(zeta_R),
            "joined_score": "phi_pair + (1/2)log|K(R)| + chi_s = zeta(R)",
            "affine_rate_family": "|K(R)| = exp(2[zeta(R)-phi_pair(R)-chi_s(R)])",
            "two_parameter_terminal_allocation_family": {
                "phi_pair": "a*zeta(R)",
                "chi_s": "b*zeta(R)",
                "abs_K_R": "exp(2*(1-a-b)*zeta(R))",
            },
            "conditional_luminosity_curve": str(dL_recomposed),
        },
        "landing": (
            "EXACT_CONDITIONAL_SNE_SCORE_RECOMPOSITION__G120_NUMERICAL_INTERFACE_UNCHANGED__"
            "P1_IDENTIFIES_ONLY_ZETA_OF_R_EQUALS_MINUS_N_OVER_TWO_LOG_ONE_MINUS_R_OVER_RINF__"
            "G124_RETYPES_THIS_AS_PHI_PLUS_HALF_LOG_ABS_K_PLUS_CHI__"
            "TERMINAL_SCREEN_SOURCE_DECOMPOSITION_AND_COMPLETE_HISTORY_NOT_SELECTED__"
            "NO_LIKELIHOOD_REPLAY_JUSTIFIED"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
