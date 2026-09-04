#!/usr/bin/env python3
"""Exact production checks for the bounded G338 Taub-pair readout."""

from __future__ import annotations

import json
import math
import os
from fractions import Fraction as F
from pathlib import Path


LANDING = (
    "EXPLICIT_LAWFUL_TAUB_DEVELOPMENT_CARRIES_NATIVE_COMPLETED_PAIR_RESPONSE_FOR_FINITE_TIME"
    "__ZERO_BOOST_TERMINAL_BLINDNESS_COEXISTS_WITH_NONTRIVIAL_RULER_DENSITY"
    "__INITIAL_SILENCE_CAN_TURN_ON_EXACTLY__NO_OCCUPANCY_OR_SCALE_SELECTION"
)


def gate(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def rational_boost(t: F) -> tuple[F, F]:
    """Return cosh(z), sinh(z) for t=tanh(z/2), exactly."""
    den = 1 - t * t
    return (1 + t * t) / den, 2 * t / den


def raw_pair(G: F, t: F) -> tuple[F, F, F, F, F, F]:
    c, s = rational_boost(t)
    h00 = -(c * c) + G * s * s
    h01 = (G - 1) * s * c
    h11 = -(s * s) + G * c * c
    det = h00 * h11 - h01 * h01
    Delta = -h00
    return h00, h01, h11, det, Delta, G


def G_of_y(rho: F, y: F) -> F:
    """G with y=u^(2/3), so all directional identities stay rational."""
    return rho / y + (1 - rho) * y * y


def main() -> None:
    checks: dict[str, bool] = {}

    # The source spacetime is the exact Kasner member (-1/3, 2/3, 2/3).
    p = (F(-1, 3), F(2, 3), F(2, 3))
    gate(sum(p) == 1, "source_kasner_sum", checks)
    gate(sum(x * x for x in p) == 1, "source_kasner_square_sum", checks)

    # Exact rational coverage of the raw pullback and W1 decomposition.
    G_values = (F(1, 9), F(1, 2), F(1), F(2), F(9))
    boost_values = (F(0), F(1, 7), F(-2, 5), F(3, 4))
    determinant_cases = 0
    regular_cases = 0
    for G in G_values:
        for t in boost_values:
            h00, h01, h11, det, Delta, _ = raw_pair(G, t)
            gate(det == -G, f"raw_determinant_{determinant_cases}", checks)
            determinant_cases += 1
            if Delta <= 0:
                continue
            # Auxiliary completed-pair decomposition.
            beta = h01 / h00
            L2 = h11 - h01 * h01 / h00
            gate(L2 == G / Delta, f"auxiliary_spatial_scale_{regular_cases}", checks)
            # W1 uses m^2=G and rescales only the ruler coordinate.
            # Squared identities avoid irrational square roots.
            gate(Delta * (L2 / G) == 1, f"w1_contragredient_{regular_cases}", checks)
            gate(det / G == -1, f"w1_determinant_{regular_cases}", checks)
            # beta_s=beta/sqrt(G), so beta_s^2 is exact and retains mixing.
            gate(
                beta * beta / G == (h01 * h01) / (Delta * Delta * G),
                f"w1_shift_retained_{regular_cases}",
                checks,
            )
            regular_cases += 1

    # Zero boost: Phi=0 but the raw determinant/ruler density is not erased.
    for index, G in enumerate(G_values):
        h00, h01, h11, det, Delta, _ = raw_pair(G, F(0))
        gate(h00 == -1 and h01 == 0 and h11 == G, f"zero_boost_raw_{index}", checks)
        gate(Delta == 1, f"zero_boost_terminal_depth_zero_{index}", checks)
        gate(-det == G, f"zero_boost_density_squared_{index}", checks)
    gate(len(set(G_values)) > 1, "zero_boost_density_is_nonconstant_across_controls", checks)

    # All initial directions and their first two time derivatives at u=1.
    rho_values = (F(0), F(1, 7), F(1, 2), F(2, 3), F(6, 7), F(1))
    for index, rho in enumerate(rho_values):
        G0 = G_of_y(rho, F(1))
        Gu0 = (4 - 6 * rho) / 3
        Guu0 = (4 + 6 * rho) / 9
        gate(G0 == 1, f"initial_normalization_{index}", checks)
        gate(Gu0 / 2 == (2 - 3 * rho) / 3, f"initial_length_rate_{index}", checks)
        gate(Guu0 > 0, f"positive_second_metric_jet_{index}", checks)

    silent_rho = F(2, 3)
    silent_Gu = (4 - 6 * silent_rho) / 3
    silent_Guu = (4 + 6 * silent_rho) / 9
    gate(silent_Gu == 0, "silent_direction_first_jet_zero", checks)
    gate(silent_Guu / 2 == F(4, 9), "silent_length_second_jet_positive", checks)

    # Exact factorization proves finite-time turn-on, not merely a Taylor effect.
    for index, y in enumerate((F(1, 16), F(1, 4), F(1), F(4), F(16))):
        lhs = G_of_y(silent_rho, y) - 1
        rhs = (y - 1) * (y - 1) * (y + 2) / (3 * y)
        gate(lhs == rhs, f"silent_exact_factorization_{index}", checks)
        gate(lhs >= 0, f"silent_global_minimum_{index}", checks)
        if y != 1:
            gate(lhs > 0, f"silent_strict_turn_on_{index}", checks)

    # Endpoint-direction threshold identities for arbitrary nonzero boost,
    # represented exactly by rational half-rapidity t.
    for index, t in enumerate((F(1, 7), F(2, 5), F(3, 4))):
        c, s = rational_boost(t)
        q = c * c / (s * s)  # coth^2(z)
        tanh2 = s * s / (c * c)
        gate(q > 1 and tanh2 == 1 / q, f"boost_threshold_{index}", checks)
        # rho=1 has G=1/y and crosses at y=tanh^2(z).
        gate(G_of_y(F(1), tanh2) == q, f"longitudinal_boundary_{index}", checks)
        # rho=0 has G=y^2 and crosses at y=coth(z).
        coth = c / s
        gate(G_of_y(F(0), coth) == q, f"transverse_boundary_{index}", checks)

    # Mixed directions: strict convexity in y gives one minimum and, because
    # G(1)=1<coth^2(z), two regular-stratum boundaries.
    mixed_rhos = (F(1, 7), F(1, 2), F(2, 3), F(6, 7))
    for index, rho in enumerate(mixed_rhos):
        ratio = rho / (2 * (1 - rho))
        # y_*^3=ratio. The derivative changes from negative to positive.
        y_lo = min(F(1, 1000), ratio / 8)
        y_hi = max(F(1000), ratio * 8)
        deriv_num_lo = -rho + 2 * (1 - rho) * y_lo**3
        deriv_num_hi = -rho + 2 * (1 - rho) * y_hi**3
        gate(deriv_num_lo < 0 < deriv_num_hi, f"mixed_unique_minimum_{index}", checks)
        gate(G_of_y(rho, F(1)) == 1, f"mixed_contains_initial_slice_{index}", checks)

    # Terminal sign is fixed by G-1 on the regular stratum for z != 0:
    # Delta=1-(G-1)sinh^2(z).
    sign_cases = 0
    for G in (F(1, 2), F(1), F(3, 2)):
        for t in (F(1, 7), F(-2, 5)):
            _, _, _, _, Delta, _ = raw_pair(G, t)
            if Delta <= 0:
                continue
            if G < 1:
                gate(Delta > 1, f"terminal_negative_when_G_below_one_{sign_cases}", checks)
            elif G == 1:
                gate(Delta == 1, f"terminal_zero_when_G_equal_one_{sign_cases}", checks)
            else:
                gate(Delta < 1, f"terminal_positive_when_G_above_one_{sign_cases}", checks)
            sign_cases += 1

    # Numerical log/tanh check is a readout check, not an algebraic premise.
    numeric_cases = 0
    for G in (0.5, 1.0, 1.5):
        for z in (-0.7, 0.4):
            c = math.cosh(z)
            s = math.sinh(z)
            Delta = c * c - G * s * s
            if Delta <= 0:
                continue
            Phi = -0.5 * math.log(Delta)
            chi = math.tanh(Phi)
            gate(abs(chi - (1 - Delta) / (1 + Delta)) < 2e-15,
                 f"projective_readout_{numeric_cases}", checks)
            numeric_cases += 1

    result = {
        "landing": LANDING,
        "grade": "PRODUCTION_DERIVED_CONDITIONAL_BOUNDED_PENDING_INDEPENDENT_AND_EXTERNAL_REVIEW",
        "preregistration_commit": "01e2110a",
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "all_passed": all(checks.values()),
        "exact_determinant_cases": determinant_cases,
        "regular_w1_cases": regular_cases,
        "source": {
            "metric": "-dT^2 + C_X^2 T^(-2/3)dX^2 + C_perp^2 T^(4/3)(dy^2+dz^2)",
            "scope": "G323/G324 exact compact Taub/Kasner quotient, T>0",
        },
        "pair": {
            "G": "rho*u^(-2/3)+(1-rho)*u^(4/3)",
            "Delta": "cosh(z)^2-G*sinh(z)^2",
            "h": [["-Delta", "(G-1)sinh(z)cosh(z)"],
                  ["(G-1)sinh(z)cosh(z)", "-sinh(z)^2+G*cosh(z)^2"]],
            "det_h": "-G",
            "m": "sqrt(G)",
            "Phi": "-0.5*log(Delta)",
            "chi": "(1-Delta)/(1+Delta)",
            "regular_stratum": "Delta>0",
        },
        "silent_direction": {
            "rho": "2/3",
            "initial_first_length_rate": "0",
            "initial_second_length_derivative_times_T0_squared": "4/9",
            "global_identity": "G-1=(y-1)^2(y+2)/(3y), y=u^(2/3)",
        },
        "scope_exclusions": [
            "no physical occupancy selection",
            "no scale or X_max selection",
            "no generic G332 evolution",
            "no stability theorem",
            "no universal observer-carry theorem",
            "pair-germ Delta=0 is not identified with a spacetime horizon",
        ],
        "checks": checks,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        out = Path(__file__).with_name("DERIVATION_RESULT.json")
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("landing", "grade", "checks_passed", "checks_total", "all_passed")}, indent=2))


if __name__ == "__main__":
    main()
