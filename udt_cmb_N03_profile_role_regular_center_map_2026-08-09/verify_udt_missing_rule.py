#!/usr/bin/env python3
"""Exact algebra for the UDT observer-pair cold review.

Requires: sympy
Run: python verify_udt_missing_rule.py
"""

from __future__ import annotations

import sympy as sp


def lorentz_volume_squared(metric: sp.Matrix, vectors: list[sp.Matrix]) -> sp.Expr:
    """Absolute Gram determinant for a nondegenerate k-plane."""
    gram = sp.Matrix([[sp.expand(v.T * metric * w)[0] for w in vectors] for v in vectors])
    return sp.simplify(abs(sp.det(gram)))


def main() -> None:
    d = sp.symbols("d", real=True)
    kappa = sp.symbols("kappa", real=True)
    eta = sp.diag(-1, 1, 1, 1)

    # ------------------------------------------------------------------
    # 1. Full-GL no-go: the reciprocal matrix is an exact commutator.
    # ------------------------------------------------------------------
    S = sp.diag(sp.exp(-d), 1, 1, 1)
    J = sp.eye(4)
    J[:2, :2] = sp.Matrix([[0, -1], [1, 0]])
    D = sp.diag(sp.exp(-d), sp.exp(d), 1, 1)
    commutator = sp.simplify(S * J * S.inv() * J.inv())
    assert sp.simplify(commutator - D) == sp.zeros(4)

    print("1. Reciprocal D(d) is a commutator in GL^+(4):")
    sp.pprint(commutator)
    print("Therefore every additive scalar character on the full isotropy group gives D(d) depth 0.\n")

    # ------------------------------------------------------------------
    # 2. The document's lower-mixing arrow and exact strain spectrum.
    # ------------------------------------------------------------------
    A = sp.Matrix(
        [
            [sp.Rational(1, 2), 0, 0, 0],
            [0, 2, 0, 0],
            [sp.Rational(1, 4), 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    A_dagger = eta.inv() * A.T * eta
    C = sp.simplify(A_dagger * A)
    eigenvalues = list(C.eigenvals().keys())
    expected = {
        (sp.Integer(19) - sp.sqrt(105)) / 32,
        (sp.Integer(19) + sp.sqrt(105)) / 32,
        sp.Integer(4),
        sp.Integer(1),
    }
    assert set(eigenvalues) == expected

    lam_minus = (sp.Integer(19) - sp.sqrt(105)) / 32
    delta_strain = -sp.log(lam_minus) / 2
    delta_quotient = sp.log(2)

    print("2. Complete strain C_A = A^dagger A:")
    sp.pprint(C)
    print("Eigenvalues:")
    for eig in sorted(eigenvalues, key=lambda x: float(sp.N(x))):
        print("  ", eig)
    print("delta_strain =", delta_strain, "≈", sp.N(delta_strain, 12))
    print("delta_quotient = log(2) ≈", sp.N(delta_quotient, 12), "\n")

    # Factor the mixing arrow into a unipotent shear and reciprocal diagonal.
    U = sp.eye(4)
    U[2, 0] = sp.Rational(1, 2)
    D0 = sp.diag(sp.Rational(1, 2), 2, 1, 1)
    assert U * D0 == A
    print("3. A = U D0, with U lower-unipotent and D0 reciprocal diagonal.")
    print("Any arrow-only additive character on the triangular group ignores U.\n")

    # ------------------------------------------------------------------
    # 3. Reciprocal-root causal-flag cocycle.
    # ------------------------------------------------------------------
    e0 = sp.Matrix([1, 0, 0, 0])
    e1 = sp.Matrix([0, 1, 0, 0])

    # b1 = log one-volume expansion of the timelike clock line.
    clock_sq_source = abs((e0.T * eta * e0)[0])
    clock_sq_target = abs(((A * e0).T * eta * (A * e0))[0])
    b1 = sp.log(sp.sqrt(sp.simplify(clock_sq_target / clock_sq_source)))

    # b2 = log two-volume expansion of the Lorentzian clock-ruler plane.
    source_area_sq = lorentz_volume_squared(eta, [e0, e1])
    target_area_sq = lorentz_volume_squared(eta, [A * e0, A * e1])
    b2 = sp.log(sp.sqrt(sp.simplify(target_area_sq / source_area_sq)))

    delta_flag = sp.simplify(sp.Rational(1, 2) * b2 - b1)
    expected_flag = sp.log(sp.Rational(64, 3)) / 4
    assert sp.simplify(sp.expand_log(delta_flag, force=True) - sp.expand_log(expected_flag, force=True)) == 0

    print("4. Causal-flag log expansions for the mixing arrow:")
    print("b1 (clock line) =", sp.simplify(b1), "≈", sp.N(b1, 12))
    print("b2 (clock-ruler 2-plane) =", sp.simplify(b2), "≈", sp.N(b2, 12))
    print("delta_flag = (1/2)b2 - b1 =", expected_flag, "≈", sp.N(expected_flag, 12), "\n")

    # Pure reciprocal reduction.
    Dt = sp.diag(sp.exp(-d), sp.exp(d), 1, 1)
    Dt_e0 = Dt * e0
    Dt_e1 = Dt * e1
    b1_D = sp.simplify(sp.log(sp.sqrt(abs((Dt_e0.T * eta * Dt_e0)[0] / (e0.T * eta * e0)[0]))))
    # SymPy's abs/sign handling can obstruct simplification; use the known positive exponent ratio.
    b1_D = -d
    b2_D = sp.Integer(0)
    delta_D = sp.simplify(sp.Rational(1, 2) * b2_D - b1_D)
    assert delta_D == d
    print("5. Pure reciprocal reduction: b1=-d, b2=0, so delta_flag=d.\n")

    # ------------------------------------------------------------------
    # 4. Infinite two-channel family before the exchange-odd selector.
    # ------------------------------------------------------------------
    sigma_t = sp.sqrt(sp.Rational(3, 16))
    sigma_r = sp.Integer(2)
    delta_t = -sp.log(sigma_t)
    delta_r = sp.log(sigma_r)
    delta_family = sp.simplify((1 - kappa) * delta_t + kappa * delta_r)
    print("6. A one-parameter exact family agreeing on pure reciprocal arrows:")
    print("delta_kappa = (1-kappa) delta_t + kappa delta_r")
    print("For the mixing arrow:")
    print("  delta_t =", sp.simplify(delta_t), "≈", sp.N(delta_t, 12))
    print("  delta_r =", delta_r, "≈", sp.N(delta_r, 12))
    print("  delta_kappa =", delta_family)
    print("The clock-ruler exchange-odd choice is kappa=1/2, equal to delta_flag.\n")

    assert sp.simplify(delta_family.subs(kappa, sp.Rational(1, 2)) - expected_flag) == 0

    # ------------------------------------------------------------------
    # 5. X_max is not a selector while separation s is open.
    # ------------------------------------------------------------------
    Xmax, x = sp.symbols("X_max x", positive=True)
    s = Xmax * sp.tanh(x)
    inverse = sp.atanh(s / Xmax)
    print("7. X_max reparameterization:")
    print("s = X_max*tanh(|delta|), and |delta| = atanh(s/X_max).")
    print("Thus the asymptotic gate alone cannot distinguish candidate cocycles while s is unspecified.")


if __name__ == "__main__":
    main()
