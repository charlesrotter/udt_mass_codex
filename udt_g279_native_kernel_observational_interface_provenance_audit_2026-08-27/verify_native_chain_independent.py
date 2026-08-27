#!/usr/bin/env python3
"""Independent algebraic and random-matrix reconstruction for G279.

This module imports no production UDT implementation and reads no stored scientific result.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import sympy as sp


PACKAGE = Path(__file__).resolve().parent


def exact_checks() -> int:
    checks = 0
    u, v = sp.symbols("u v", positive=True)
    P = sp.diag(u, v)
    K = sp.Matrix([[0, 1], [1, 0]])
    assert P.T * K * P == (u * v) * K
    checks += 1

    d1, d2 = sp.symbols("d1 d2", real=True)
    D1 = sp.diag(sp.exp(-d1), sp.exp(d1))
    D2 = sp.diag(sp.exp(-d2), sp.exp(d2))
    assert sp.simplify(D2 * D1 - sp.diag(sp.exp(-(d1 + d2)), sp.exp(d1 + d2))) == sp.zeros(2)
    assert sp.simplify(D1.det()) == 1
    checks += 2

    phi, ce, r, theta = sp.symbols("phi ce r theta", real=True, positive=True)
    E = sp.diag(ce * sp.exp(-phi), sp.exp(phi), r, r * sp.sin(theta))
    eta4 = sp.diag(-1, 1, 1, 1)
    metric = sp.simplify(E.T * eta4 * E)
    assert metric == sp.diag(-ce**2 * sp.exp(-2 * phi), sp.exp(2 * phi), r**2, r**2 * sp.sin(theta) ** 2)
    checks += 1

    h00, h01, h11 = sp.symbols("h00 h01 h11", real=True)
    determinant = h00 * h11 - h01**2
    T2 = -h00
    beta = h01 / h00
    L2 = h11 - h01**2 / h00
    assert sp.simplify(T2 * L2 + determinant) == 0
    checks += 1

    m2 = -determinant
    normalized_det = sp.simplify(determinant / m2)
    assert normalized_det == -1
    assert sp.simplify(T2 * (L2 / m2)) == 1
    checks += 2

    delta = sp.symbols("delta", real=True)
    radial_h00 = -sp.exp(-2 * delta)
    radial_det = -1
    Phi = -sp.Rational(1, 2) * sp.log(-radial_h00)
    control = sp.Rational(1, 4) * sp.log((-radial_det) / radial_h00**2)
    assert sp.simplify(Phi - delta) == 0
    assert sp.simplify(control - delta) == 0
    checks += 2

    projective = sp.simplify((sp.exp(delta) - sp.exp(-delta)) / (sp.exp(delta) + sp.exp(-delta)))
    assert sp.simplify(projective - sp.tanh(delta)) == 0
    checks += 1

    z, R = sp.symbols("z R", positive=True)
    Z = 1 + z
    dL = Z**2 * R  # explicitly imported transparent transfer, not native kernel algebra
    magnitude_part = 5 * sp.log(dL, 10)
    reduced = sp.expand_log(magnitude_part - 10 * sp.log(Z, 10), force=True)
    assert sp.simplify(reduced - 5 * sp.log(R, 10)) == 0
    checks += 1

    a = sp.symbols("a", real=True)
    ell = 10 ** (a / 5)
    assert sp.simplify(5 * sp.log(ell, 10) - a) == 0
    checks += 1
    return checks


def random_complete_pair_checks(seed: int = 279, target: int = 10000) -> tuple[int, int]:
    rng = np.random.default_rng(seed)
    accepted = 0
    assertions = 0
    eta2 = np.diag([-1.0, 1.0])
    eta4 = np.diag([-1.0, 1.0, 1.0, 1.0])
    attempts = 0
    while accepted < target:
        attempts += 1
        B = rng.normal(size=(2, 2))
        Q = rng.normal(size=(2, 2))
        if abs(np.linalg.det(B)) < 0.2 or abs(np.linalg.det(Q)) < 0.2:
            continue
        S = rng.normal(scale=0.4, size=(2, 2))
        Y = rng.normal(size=(2, 2))
        Z = rng.normal(scale=0.5, size=(2, 2))
        E = np.block([[B, np.zeros((2, 2))], [Q @ S, Q]])
        J = np.vstack([Y, Z])
        direct = J.T @ E.T @ eta4 @ E @ J
        block = Y.T @ B.T @ eta2 @ B @ Y + (S @ Y + Z).T @ Q.T @ Q @ (S @ Y + Z)
        np.testing.assert_allclose(direct, block, rtol=2e-12, atol=2e-12)
        assertions += 1
        h00 = float(direct[0, 0])
        det = float(np.linalg.det(direct))
        if h00 >= -1e-7 or det >= -1e-7:
            continue
        T = math.sqrt(-h00)
        beta = float(direct[0, 1] / h00)
        L2 = float(direct[1, 1] - direct[0, 1] ** 2 / h00)
        if L2 <= 0.0:
            continue
        L = math.sqrt(L2)
        m = math.sqrt(-det)
        np.testing.assert_allclose(T * L, m, rtol=2e-11, atol=2e-11)
        np.testing.assert_allclose(T * (L / m), 1.0, rtol=2e-11, atol=2e-11)
        np.testing.assert_allclose(det / (m * m), -1.0, rtol=2e-11, atol=2e-11)
        normalized_shift = beta / m
        assert math.isfinite(normalized_shift)
        phi_completed = -math.log(T)
        assert math.isfinite(phi_completed)
        assertions += 5
        accepted += 1
    return accepted, assertions


def projective_checks(seed: int = 280, count: int = 10000) -> int:
    rng = np.random.default_rng(seed)
    assertions = 0
    for _ in range(count):
        direction = rng.normal(size=3)
        direction /= np.linalg.norm(direction)
        magnitude = float(rng.uniform(0.0, 0.999999))
        velocity = magnitude * direction
        gamma = 1.0 / math.sqrt(1.0 - magnitude * magnitude)
        spatial = gamma * velocity
        np.testing.assert_allclose(gamma * gamma - spatial @ spatial, 1.0, rtol=2e-12, atol=2e-12)
        recovered = spatial / gamma
        np.testing.assert_allclose(recovered, velocity, rtol=2e-12, atol=2e-12)
        assertions += 2
    return assertions


def main() -> None:
    symbolic = exact_checks()
    accepted, matrix_assertions = random_complete_pair_checks()
    projective_assertions = projective_checks()
    result = {
        "audit": "G279_INDEPENDENT_NATIVE_CHAIN_RECONSTRUCTION",
        "status": "PASS",
        "production_modules_imported": 0,
        "stored_scientific_results_read": 0,
        "symbolic_checks": symbolic,
        "regular_complete_pair_cases": accepted,
        "matrix_assertions": matrix_assertions,
        "projective_cases": projective_assertions // 2,
        "projective_assertions": projective_assertions,
        "total_assertions": symbolic + matrix_assertions + projective_assertions,
        "transfer_identity_status": "CHECKED_ONLY_AFTER_EXPLICIT_CONDITIONAL_IMPORT",
    }
    (PACKAGE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
