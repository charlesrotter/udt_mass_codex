#!/usr/bin/env python3
"""Exact symbolic ownership checks for the G76 variable-profile Hamiltonian."""

from __future__ import annotations

import json
import random
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    x, y, z, a, q, qs = sp.symbols("x y z a q q_s", real=True)
    pt, px, py, pz = sp.symbols("p_t p_x p_y p_z", real=True)
    X = sp.Matrix([x, y, z])
    p = sp.Matrix([px, py, pz])
    s = sp.expand(X.dot(X))
    rho2 = x**2 + y**2
    A = 1 + a * s
    w = sp.Matrix([-q * y, q * x, 0])
    gamma = sp.eye(3) + (1 / A - 1) * (X * X.T) / s
    gamma_inv = sp.eye(3) + a * X * X.T
    B = A + q**2 * rho2

    metric = sp.zeros(4)
    metric[0, 0] = -A
    metric[0, 1:4] = w.T
    metric[1:4, 0] = w
    metric[1:4, 1:4] = gamma
    inverse = sp.zeros(4)
    inverse[0, 0] = -1 / B
    inverse[0, 1:4] = (w / B).T
    inverse[1:4, 0] = w / B
    inverse[1:4, 1:4] = gamma_inv - w * w.T / B
    inverse_identity = all(sp.simplify(value) == 0 for value in metric * inverse - sp.eye(4))

    momentum = sp.Matrix([pt, px, py, pz])
    matrix_h = sp.simplify((momentum.T * inverse * momentum)[0] / 2)
    Lz = x * py - y * px
    radial = X.dot(p)
    E = pt - q * Lz
    registered_h = sp.Rational(1, 2) * (p.dot(p) + a * radial**2 - E**2 / B)
    hamiltonian_identity = sp.simplify(matrix_h - registered_h) == 0

    dq = 2 * qs * X
    dL = sp.Matrix([py, -px, 0])
    dB = 2 * a * X + 2 * q * rho2 * dq + 2 * q**2 * sp.Matrix([x, y, 0])
    registered_dx = p + a * radial * X + (E / B) * w
    registered_dp = -a * radial * p - (E / B) * (Lz * dq + q * dL) - E**2 * dB / (2 * B**2)
    registered_dt = -E / B

    # Differentiate while making the radial dependence dq_i=2*q_s*x_i explicit.
    symbolic_dp = []
    symbolic_dx = [sp.diff(registered_h, item) for item in (px, py, pz)]
    for coordinate in (x, y, z):
        direct = sp.diff(registered_h, coordinate)
        q_chain = sp.diff(registered_h, q) * 2 * qs * coordinate
        symbolic_dp.append(-sp.simplify(direct + q_chain))
    gradient_identity = all(
        sp.simplify(symbolic_dx[index] - registered_dx[index]) == 0
        and sp.simplify(symbolic_dp[index] - registered_dp[index]) == 0
        for index in range(3)
    )
    time_identity = sp.simplify(sp.diff(registered_h, pt) - registered_dt) == 0

    # Deterministic exact substitutions exercise nonzero q_s, mixing, lapse and momenta.
    rng = random.Random(760811)  # CHOSE_NUMERIC: deterministic symbolic-test seed.
    point_checks = []
    for _ in range(24):  # CHOSE_NUMERIC: bounded equation regression count.
        values = {
            x: sp.Rational(rng.randint(1, 4), 5),
            y: sp.Rational(rng.randint(-3, 3), 7),
            z: sp.Rational(rng.randint(-3, 3), 8),
            a: sp.Rational(rng.choice([-1, 0, 1]), 4),
            q: sp.Rational(rng.randint(-4, 4), 5),
            qs: sp.Rational(rng.randint(-3, 3), 5),
            pt: sp.Rational(rng.randint(-5, -1), 3),
            px: sp.Rational(rng.randint(-4, 4), 3),
            py: sp.Rational(rng.randint(-4, 4), 3),
            pz: sp.Rational(rng.randint(-4, 4), 3),
        }
        if sp.simplify(B.subs(values)) == 0:
            continue
        residuals = [sp.simplify((symbolic_dx[i] - registered_dx[i]).subs(values)) for i in range(3)]
        residuals += [sp.simplify((symbolic_dp[i] - registered_dp[i]).subs(values)) for i in range(3)]
        point_checks.append(all(value == 0 for value in residuals))

    checks = {
        "metric_times_registered_inverse_is_identity": bool(inverse_identity),
        "inverse_metric_hamiltonian_matches_registered_H": bool(hamiltonian_identity),
        "variable_q_gradient_matches_registered_rhs": bool(gradient_identity),
        "time_equation_matches_registered_rhs": bool(time_identity),
        "24_exact_control_points": len(point_checks) == 24 and all(point_checks),
        "constant_q_limit_removes_dq_terms": all(
            sp.simplify(value.subs(qs, 0)) == 0 for value in dq
        ),
    }
    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g76-equation-ownership-v1",
        "status": "PASS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "exact_control_points": len(point_checks),
        "protected_draft_read": False,
    }
    (HERE / "EQUATION_VERIFICATION.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
