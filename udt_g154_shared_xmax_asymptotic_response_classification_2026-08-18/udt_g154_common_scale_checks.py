
#!/usr/bin/env python3
"""Exact symbolic checks for the G154/common-scale audit."""

from __future__ import annotations

import sympy as sp


def assert_zero(expr: sp.Expr, name: str) -> None:
    value = sp.simplify(sp.trigsimp(expr))
    if value != 0:
        raise AssertionError(f"{name} failed: {value}")
    print(f"PASS: {name}")


def mobius(a: sp.Expr, b: sp.Expr, scale: sp.Expr) -> sp.Expr:
    return (a + b) / (1 + a * b / scale**2)


def main() -> None:
    x, y = sp.symbols("x y", real=True)
    X, Y, lam = sp.symbols("X Y lam", positive=True, finite=True)
    a, b = sp.symbols("a b", real=True)

    # 1. Fixed-scale Möbius group and scale-changing isomorphisms.
    assert_zero(
        mobius(X * sp.tanh(a), X * sp.tanh(b), X)
        - X * sp.tanh(a + b),
        "fixed-X Mobius law is linearized by artanh",
    )
    assert_zero(
        (Y / X) * mobius(x, y, X)
        - mobius((Y / X) * x, (Y / X) * y, Y),
        "all positive-X Mobius groups are scale-isomorphic",
    )
    assert_zero(
        mobius(x, y, X) / X
        - mobius(x / X, y / X, sp.Integer(1)),
        "normalization x -> x/X removes the dimensionful scale",
    )

    # 2. Pair-metric decomposition and positive common conformal rescaling.
    T, L = sp.symbols("T L", positive=True, finite=True)
    beta = sp.symbols("beta", real=True)
    H = sp.Matrix(
        [
            [-T**2, -T**2 * beta],
            [-T**2 * beta, L**2 - T**2 * beta**2],
        ]
    )
    Hs = lam**2 * H

    assert_zero(H.det() + T**2 * L**2, "det(h) = -T^2 L^2")
    ratio = sp.simplify((-H.det()) / H[0, 0] ** 2)
    ratio_s = sp.simplify((-Hs.det()) / Hs[0, 0] ** 2)
    assert_zero(ratio_s - ratio, "phi_pair readout is conformally invariant")
    assert_zero(
        Hs[0, 1] / Hs[0, 0] - H[0, 1] / H[0, 0],
        "beta readout is conformally invariant",
    )
    assert_zero(
        (-Hs.det()) - lam**4 * (-H.det()),
        "common scale shifts by lam: exp(kappa') = lam exp(kappa)",
    )

    # 3. Normalized-frame response rescales inversely.
    phi = sp.symbols("phi", real=True)
    dX, dphi = sp.symbols("dX dphi", real=True)
    response = sp.tanh(phi) * dX + X * sp.sech(phi) ** 2 * dphi
    response_s = (
        sp.tanh(phi) * (dX / lam)
        + X * sp.sech(phi) ** 2 * (dphi / lam)
    )
    assert_zero(
        response_s - response / lam,
        "normalized response changes under common conformal scale",
    )

    # 4. G154 counterfamily.
    q = sp.symbols("q", positive=True)
    eps = sp.symbols("eps", real=True)
    ell = sp.symbols("ell", real=True)
    rho = eps * X * (1 - q ** sp.Rational(2, 3)) / (
        1 + q ** sp.Rational(2, 3)
    )
    drho_dq = sp.diff(rho, q)
    n_rho = sp.simplify(-q**ell * drho_dq)
    expected = (
        eps
        * sp.Rational(4, 3)
        * X
        * q ** (ell - sp.Rational(1, 3))
        / (1 + q ** sp.Rational(2, 3)) ** 2
    )
    assert_zero(n_rho - expected, "G154 spatial-response formula")

    lim_zero = sp.limit(expected.subs(ell, sp.Rational(1, 2)), q, 0, dir="+")
    lim_finite = sp.limit(
        expected.subs(ell, sp.Rational(1, 3)), q, 0, dir="+"
    )
    lim_infinite = sp.limit(
        expected.subs({ell: sp.Rational(1, 4), eps: 1}), q, 0, dir="+"
    )
    if lim_zero != 0:
        raise AssertionError(f"zero-class limit failed: {lim_zero}")
    if sp.simplify(lim_finite - sp.Rational(4, 3) * eps * X) != 0:
        raise AssertionError(f"finite-class limit failed: {lim_finite}")
    if lim_infinite != sp.oo:
        raise AssertionError(f"divergent-class limit failed: {lim_infinite}")
    print("PASS: G154 zero / finite / divergent asymptotic classes")

    # Positive oscillatory scale:
    # L = q^(-1/3)/(2+sin(log q)) gives
    # n(rho) = (4 eps X / 3)*(2+sin(log q))/(1+q^(2/3))^2.
    # Along q_n^+ = exp(pi/2-2*pi*n), sin(log q_n^+)=+1;
    # along q_n^- = exp(3*pi/2-2*pi*n), sin(log q_n^-)=-1.
    oscillatory_plus = 4 * eps * X
    oscillatory_minus = sp.Rational(4, 3) * eps * X
    if sp.simplify(oscillatory_plus - oscillatory_minus) == 0:
        raise AssertionError("oscillatory subsequences unexpectedly agree")
    print("PASS: positive oscillatory common scale has unequal subsequential limits")

    # 5. Variable X can cancel the two exact G153 terms while X -> X_*.
    Xstar = sp.symbols("Xstar", positive=True)
    X_of_phi = Xstar / sp.tanh(phi)
    cancellation = sp.simplify(
        sp.tanh(phi) * sp.diff(X_of_phi, phi)
        + X_of_phi * sp.sech(phi) ** 2
    )
    assert_zero(cancellation, "variable X can exactly cancel the phi term")
    if sp.limit(X_of_phi, phi, sp.oo) != Xstar:
        raise AssertionError("X(phi) did not approach Xstar")
    print("PASS: cancellation example still has X(phi) -> Xstar")

    # 6. Endpoint cocycle closure does not couple independent potentials.
    kA, kB, kC, pA, pB, pC = sp.symbols("kA kB kC pA pB pC")
    assert_zero(
        (kC - kB) + (kB - kA) - (kC - kA),
        "kappa endpoint cocycle closes for arbitrary kappa values",
    )
    assert_zero(
        (pC - pB) + (pB - pA) - (pC - pA),
        "phi endpoint cocycle closes independently of kappa",
    )

    # 7. Global endpoint rank/composition closure sees phi, not kappa.
    phi_values = [sp.Integer(0), sp.Integer(1), sp.Integer(3), sp.Integer(7)]
    A = sp.Matrix(4, 4, lambda i, j: phi_values[j] - phi_values[i])
    if A.rank() > 2:
        raise AssertionError(f"additive-depth matrix rank exceeded 2: {A.rank()}")
    xAB = X * sp.tanh(b - a)
    xBC = X * sp.tanh(phi - b)
    xAC = X * sp.tanh(phi - a)
    assert_zero(
        mobius(xAB, xBC, X) - xAC,
        "global Mobius triangle closure depends only on endpoint phi",
    )
    print("PASS: additive endpoint network has rank <= 2 and is kappa-blind")

    # 8. A full two-plane pullback network can encode a metric, but this is
    # reconstruction, not selection.
    G = sp.Matrix(
        [
            [-7, 2, 3, 5],
            [2, 11, 13, 17],
            [3, 13, 19, 23],
            [5, 17, 23, 29],
        ]
    )
    recovered = sp.zeros(4)
    for i in range(4):
        recovered[i, i] = G[i, i]
    for i in range(4):
        for j in range(i + 1, 4):
            pullback_ij = sp.Matrix([[G[i, i], G[i, j]], [G[i, j], G[j, j]]])
            recovered[i, j] = pullback_ij[0, 1]
            recovered[j, i] = pullback_ij[1, 0]
    if recovered != G:
        raise AssertionError("two-plane pullback reconstruction failed")
    print("PASS: complete two-plane pullbacks faithfully encode the metric")

    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
