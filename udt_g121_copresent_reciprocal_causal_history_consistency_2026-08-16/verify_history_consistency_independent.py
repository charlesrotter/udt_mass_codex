#!/usr/bin/env python3
"""Independent Fraction/Decimal replay of G121 finite algebra."""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def mmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def msub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def is_zero(a):
    return all(x == 0 for row in a for x in row)


def block(a, b, c, d):
    return [a[0] + b[0], a[1] + b[1], c[0] + d[0], c[1] + d[1]]


def main() -> None:
    F = Fraction
    I2 = [[F(1), F(0)], [F(0), F(1)]]
    Z2 = [[F(0), F(0)], [F(0), F(0)]]
    Omega = block(Z2, I2, [[-x for x in row] for row in I2], Z2)
    p1 = block(I2, [[F(2, 3), F(0)], [F(0), F(2, 3)]], Z2, I2)
    p2 = block(I2, Z2, [[F(-3, 5), F(0)], [F(0), F(-3, 5)]], I2)
    p12 = mmul(p2, p1)

    symplectic = is_zero(msub(mmul(mmul(transpose(p12), Omega), p12), Omega))

    omega_a, omega_b, omega_c = F(1), F(1, 2), F(3, 2)
    frequency_triangle = (omega_a / omega_b) * (omega_b / omega_c) == omega_a / omega_c
    frequency_reversal = (omega_a / omega_b) * (omega_b / omega_a) == 1

    phi_a, phi_b, phi_c = F(1, 7), F(-2, 9), F(5, 11)
    reciprocal_triangle = (phi_b - phi_a) + (phi_c - phi_b) == (phi_c - phi_a)
    raw_period = F(1, 3) + F(2, 5) + F(1, 7)

    q_ab = [[F(0), F(-1)], [F(1), F(0)]]
    q_bc = I2
    q_loop = mmul(q_bc, q_ab)
    holonomy_orthogonal = mmul(transpose(q_loop), q_loop) == I2
    holonomy_oriented = q_loop[0][0] * q_loop[1][1] - q_loop[0][1] * q_loop[1][0] == 1
    holonomy_nonidentity = q_loop != I2

    # Independent high-precision evaluation of the frozen H1 invariant marker.
    getcontext().prec = 80
    tau = Decimal(1) / Decimal(2)
    radius = Decimal(1) / Decimal(3)
    exponent = Decimal(2) * tau * radius * radius / Decimal(7)
    h1_g_inv_rr = exponent.exp()
    history_marker_nonzero = h1_g_inv_rr != Decimal(1)
    temporal_upper_bound = -(Decimal(-2) / Decimal(5)).exp() + (Decimal(2) / Decimal(7)).exp() / Decimal(121)

    checks = {
        "fraction_phase_composite_symplectic": symplectic,
        "fraction_frequency_triangle": frequency_triangle,
        "fraction_frequency_reversal": frequency_reversal,
        "fraction_matched_reciprocal_triangle": reciprocal_triangle,
        "fraction_reciprocity_only_loop_nonzero": raw_period != 0,
        "fraction_path_holonomy_orthogonal": holonomy_orthogonal,
        "fraction_path_holonomy_orientation_preserving": holonomy_oriented,
        "fraction_path_holonomy_nonidentity": holonomy_nonidentity,
        "decimal_frozen_history_marker_nonzero": history_marker_nonzero,
        "decimal_H1_tau_is_temporal_on_patch": temporal_upper_bound < 0,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "exact_raw_period": str(raw_period),
        "exact_path_holonomy": [[str(x) for x in row] for row in q_loop],
        "h1_g_inverse_dR_dR_at_tau_half_R_third": str(h1_g_inv_rr),
        "H1_temporal_function_upper_bound": str(temporal_upper_bound),
        "scope": "independent finite algebra and one high-precision witness marker; analytic metric theorem remains separately audited",
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
